# ============================================================
# @Akitti C*Hive – Spectral MHD (induction + Lorentz)
# ============================================================
# Incompressible MHD on the same Fourier grid as the NS vorticity
# stepper. Plain-language picture:
#   • B is the magnetic field (like "frozen-in" rubber bands in the fluid).
#   • Induction: fluid motion stretches / folds B; resistivity η lets it slip.
#   • Lorentz: currents J=curl(B) push back on the fluid (tension + pressure).
# Vorticity form (matches ns_vorticity rotational form):
#   ∂t ω = curl(u×ω) + ν ∇²ω + curl(J×B) + force
#   ∂t B = curl(u×B) + η ∇²B
# Both u and B stay divergence-free via spectral projection.
# Hypotheses from MHD2 notes (Crow + guide field): prefer b_guide="z",
# η≈1e-3, B0≈0.08 for mild Crow-tube magnetic tension — research only.

from functools import partial

import jax.numpy as jnp
from jax import jit

from .grid import ik_cross, project_div_free, _u_from_vort_3d
from .vorticity import _rhs_3d

# Safe smoke defaults from MHD2/02 hive correction note (hypotheses only).
DEFAULT_MHD = dict(
    eta=1e-3,       # magnetic diffusivity (Ohmic slip)
    B0=0.08,        # uniform guide-field strength
    b_guide="z",    # "x" | "y" | "z" — spanwise "z" tensions Crow tubes
)


def zero_B_hat(grid, dtype=jnp.complex128):
    """Quiescent magnetic field on the spectral grid."""
    d, N = int(grid["dim"]), int(grid["N"])
    return jnp.zeros((d,) + (N,) * d, dtype=dtype)


def guide_field_B_hat(grid, B0=0.08, b_guide="z", dtype=jnp.complex128):
    """Uniform guide field B = B0 * e_axis (exactly div-free on the torus).

    Axis choice matters for Crow tubes: "z" (reconnection-plane / spanwise)
    builds tension and current sheets; "x" (along the tubes) is nearly passive
    (see MHD2/02). This is an IC helper, not a claim about physics.
    """
    d, N = int(grid["dim"]), int(grid["N"])
    if d != 3:
        raise ValueError("guide_field_B_hat is 3D-only")
    axis = {"x": 0, "y": 1, "z": 2}.get(str(b_guide).lower())
    if axis is None:
        raise ValueError(f"b_guide must be 'x', 'y', or 'z' (got {b_guide!r})")
    B = jnp.zeros((3, N, N, N), dtype=jnp.float64)
    B = B.at[axis].set(float(B0))
    B_hat = jnp.fft.fftn(B, axes=(1, 2, 3)).astype(dtype) * grid["dealias"]
    return project_div_free(B_hat, grid)


@jit
def lorentz_vorticity_force(B_hat, grid):
    """curl(J × B) in Fourier space — magnetic kick onto vorticity.

    J = curl(B). Positive tension resists bending of field lines.
    """
    dealias = grid["dealias"]
    J_hat = ik_cross(B_hat, grid) * dealias
    J = jnp.fft.ifftn(J_hat, axes=(1, 2, 3)).real
    B = jnp.fft.ifftn(B_hat, axes=(1, 2, 3)).real
    JxB = jnp.stack([
        J[1] * B[2] - J[2] * B[1],
        J[2] * B[0] - J[0] * B[2],
        J[0] * B[1] - J[1] * B[0],
    ])
    JxB_hat = jnp.fft.fftn(JxB, axes=(1, 2, 3)) * dealias
    return ik_cross(JxB_hat, grid) * dealias


@jit
def induction_rhs(B_hat, u_hat, grid, eta):
    """∂t B̂ = curl(u × B) − η k² B̂  (unmollified spectral velocity).

    Using the same u that advances vorticity avoids a hidden magnetic
    diffusivity from any velocity filter (MHD2/02 audit note).
    """
    dealias, k2 = grid["dealias"], grid["k2"]
    u = jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real
    B = jnp.fft.ifftn(B_hat, axes=(1, 2, 3)).real
    uxB = jnp.stack([
        u[1] * B[2] - u[2] * B[1],
        u[2] * B[0] - u[0] * B[2],
        u[0] * B[1] - u[1] * B[0],
    ])
    uxB_hat = jnp.fft.fftn(uxB, axes=(1, 2, 3)) * dealias
    return (ik_cross(uxB_hat, grid) - eta * k2 * B_hat) * dealias


@jit
def mhd_rhs(omega_hat, B_hat, grid, nu, eta, force_hat):
    """Coupled (ω, B) right-hand sides. 3D only."""
    lorentz = lorentz_vorticity_force(B_hat, grid)
    dw = _rhs_3d(omega_hat, grid, nu, force_hat + lorentz)
    u_hat = _u_from_vort_3d(omega_hat, grid)
    dB = induction_rhs(B_hat, u_hat, grid, eta)
    return dw, dB


@partial(jit, static_argnums=(7,))
def mhd_step(omega_hat, B_hat, grid, nu, eta, dt, force_hat, scheme="rk2"):
    """One coupled NS+MHD step (RK2 Heun or forward Euler). Projects both fields."""
    def rhs(omega, B):
        return mhd_rhs(omega, B, grid, nu, eta, force_hat)

    if scheme == "euler":
        dw, dB = rhs(omega_hat, B_hat)
        omega = omega_hat + dt * dw
        B = B_hat + dt * dB
    else:
        k1w, k1B = rhs(omega_hat, B_hat)
        k2w, k2B = rhs(omega_hat + dt * k1w, B_hat + dt * k1B)
        omega = omega_hat + 0.5 * dt * (k1w + k2w)
        B = B_hat + 0.5 * dt * (k1B + k2B)
    omega = project_div_free(omega, grid)
    B = project_div_free(B, grid)
    return omega, B


def cfl_dt_mhd(u, B, dx, nu, eta, cfl=0.4):
    """Advective + Alfven + viscous/resistive CFL bound."""
    umax = jnp.max(jnp.sqrt(jnp.sum(u**2, axis=0)))
    Bmax = jnp.max(jnp.sqrt(jnp.sum(B**2, axis=0)))
    return cfl * dx / (umax + Bmax + 4.0 * (nu + eta) / dx + 1e-12)

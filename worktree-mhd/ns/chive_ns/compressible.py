# ============================================================
# @Akitti C*Hive – Compressible MHD scaffold (patches 3b + 4)
# Continuity:  dt rho + div(rho u) = 0. Dealias the product rho u.
# Energy: Russell Dp/Dt = -gamma p div(u) + (gamma-1) Q
#         ideal EOS p = (gamma-1) rho e ; gamma=5/3 default.
# Helmholtz stays ON: u is Qin-projected. No nabla p in momentum
# (that is patch 5). mode="cmhd" only; mode="mhd" untouched.
# No mean-pin and no floor: a pin would hide a continuity leak.
# ============================================================

from functools import partial

import jax.numpy as jnp
from jax import jit

from .grid import velocity_from_vorticity
from .vorticity import coupled_mhd_step
from .mhd import current_from_b
from .diagnostics import strain_tensor


GAMMA_DEFAULT = 5.0 / 3.0


def uniform_rho_hat(grid, rho0=1.0, dtype=jnp.complex128):
    """Fourier transform of uniform density rho === rho0 (default 1)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    rho = jnp.full((N,) * dim, float(rho0), dtype=jnp.float64)
    return jnp.fft.fftn(rho).astype(dtype)


def bump_rho_hat(grid, eps=0.01, dtype=jnp.complex128):
    """rho = 1 + eps sin(2 pi x / L) on the periodic box. Mean is 1.

    Small eps (default 0.01) so min rho stays positive with no floor.
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, _Y = jnp.meshgrid(x, x, indexing="ij")
    else:
        X, _Y, _Z = jnp.meshgrid(x, x, x, indexing="ij")
    rho = 1.0 + float(eps) * jnp.sin(2.0 * jnp.pi * X / L)
    return jnp.fft.fftn(rho).astype(dtype)


def uniform_p_hat(grid, p0=1.0, dtype=jnp.complex128):
    """Fourier pressure field with uniform physical value p0 (default 1)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    p = jnp.full((N,) * dim, float(p0), dtype=jnp.float64)
    return jnp.fft.fftn(p).astype(dtype)


def uniform_eint_hat(grid, e0=1.5, dtype=jnp.complex128):
    """Fourier specific internal energy, uniform e0 (p0=1, gamma=5/3, rho=1)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    e = jnp.full((N,) * dim, float(e0), dtype=jnp.float64)
    return jnp.fft.fftn(e).astype(dtype)


def zero_eint_hat(grid, dtype=jnp.complex128):
    """Zeros in Fourier internal energy (parked helper; live field is p_hat)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    return jnp.zeros((N,) * dim, dtype=dtype)


def eos_pressure(rho, e_int, gamma=GAMMA_DEFAULT):
    """Ideal EOS: p = (gamma - 1) rho e  (e = specific internal energy)."""
    return (gamma - 1.0) * rho * e_int


def eos_eint(rho, p, gamma=GAMMA_DEFAULT):
    """Ideal EOS inverse: e = p / ((gamma - 1) rho). No floor."""
    return p / ((gamma - 1.0) * rho)


@jit
def continuity_rhs(rho_hat, u_hat, grid):
    """Spectral 2/3-dealiased continuity: d_t rho = -div(rho u)."""
    dealias = grid["dealias"]
    k_stack = grid["k_stack"]
    rho = jnp.fft.ifftn(rho_hat).real
    u = jnp.fft.ifftn(u_hat, axes=range(1, u_hat.ndim)).real
    mom = rho[None] * u
    mom_hat = jnp.fft.fftn(mom, axes=range(1, mom.ndim)) * dealias[None]
    div_hat = jnp.sum(1j * k_stack * mom_hat, axis=0)
    return -div_hat * dealias


@partial(jit, static_argnums=(4,))
def continuity_step(rho_hat, u_hat, grid, dt, scheme="rk2"):
    """Advance rho with frozen Helmholtz-on u. No pin, no floor."""
    if scheme == "euler":
        out = rho_hat + dt * continuity_rhs(rho_hat, u_hat, grid)
    else:
        k1 = continuity_rhs(rho_hat, u_hat, grid)
        k2 = continuity_rhs(rho_hat + dt * k1, u_hat, grid)
        out = rho_hat + 0.5 * dt * (k1 + k2)
    return out * grid["dealias"]


density_step = continuity_step


def density_diagnostics(rho_hat, u_hat, grid):
    """mean/min/max rho and max|d_t rho|. Leftover <rho>-1 is not pinned."""
    rho = jnp.fft.ifftn(rho_hat).real
    drho = jnp.fft.ifftn(continuity_rhs(rho_hat, u_hat, grid)).real
    return {
        "mean_rho": jnp.mean(rho),
        "max_rho": jnp.max(rho),
        "min_rho": jnp.min(rho),
        "max_abs_rho_m1": jnp.max(jnp.abs(rho - 1.0)),
        "max_drho_dt": jnp.max(jnp.abs(drho)),
    }


@jit
def heating_Q(u_hat, B_hat, grid, eta_mag, nu, B_ext_hat=None):
    """Volumetric Q = Ohmic eta|J|^2 + viscous 2 nu S:S (physical space).

    For incompressible u, 2<S:S> = <omega^2> so mean Q_visc matches eps_nu.
    """
    Btot = B_hat if B_ext_hat is None else (B_hat + B_ext_hat)
    J_hat = current_from_b(Btot, grid)
    spatial = tuple(range(1, u_hat.ndim))
    if B_hat.shape[0] == 2:
        J = jnp.fft.ifftn(J_hat).real
        Q_ohm = eta_mag * (J * J)
    else:
        J = jnp.fft.ifftn(J_hat, axes=spatial).real
        Q_ohm = eta_mag * jnp.sum(J * J, axis=0)
    S = strain_tensor(u_hat, grid)
    Q_visc = 2.0 * nu * jnp.sum(S * S, axis=(0, 1))
    return Q_ohm + Q_visc


@jit
def pressure_rhs(p_hat, u_hat, grid, gamma, Q):
    """Eulerian Russell: dt p = -u.grad p - gamma p div(u) + (gamma-1) Q.

    Russell: Dp/Dt = -gamma p div(u) + (gamma-1) Q.
    Helmholtz on => div u ~ 0, so E_int = p/(gamma-1) rises by Q.
    Products are 2/3-dealiased. No floor.
    """
    spatial = tuple(range(1, u_hat.ndim))
    dealias = grid["dealias"]
    u = jnp.fft.ifftn(u_hat, axes=spatial).real
    p = jnp.fft.ifftn(p_hat).real
    grad_p_hat = 1j * grid["k_stack"] * p_hat
    grad_p = jnp.fft.ifftn(grad_p_hat, axes=spatial).real
    u_dot_grad_p = jnp.sum(u * grad_p, axis=0)
    div_u_hat = 1j * jnp.sum(grid["k_stack"] * u_hat, axis=0)
    div_u = jnp.fft.ifftn(div_u_hat).real
    adv_hat = jnp.fft.fftn(u_dot_grad_p) * dealias
    pdiv_hat = jnp.fft.fftn(p * div_u) * dealias
    Q_hat = jnp.fft.fftn(Q) * dealias
    return (-adv_hat - gamma * pdiv_hat + (gamma - 1.0) * Q_hat) * dealias


@partial(jit, static_argnums=(4,))
def pressure_step(p_hat, u_hat, grid, dt, scheme, gamma, Q):
    """Advance p one step with frozen u and Q. Euler or Heun (rk2). No floor."""
    def rhs(p_hat):
        return pressure_rhs(p_hat, u_hat, grid, gamma, Q)

    if scheme == "euler":
        out = p_hat + dt * rhs(p_hat)
    else:
        k1 = rhs(p_hat)
        k2 = rhs(p_hat + dt * k1)
        out = p_hat + 0.5 * dt * (k1 + k2)
    return out * grid["dealias"]


def energy_diagnostics(rho_hat, p_hat, gamma=GAMMA_DEFAULT):
    """e_int here is volumetric internal energy density <p/(gamma-1)>."""
    p = jnp.fft.ifftn(p_hat).real
    e_dens = p / (gamma - 1.0)
    return {
        "e_int": jnp.mean(e_dens),
        "mean_e_int": jnp.mean(e_dens),
        "p": jnp.mean(p),
        "mean_p": jnp.mean(p),
        "min_p": jnp.min(p),
        "gamma": jnp.asarray(gamma, dtype=jnp.float64),
    }


def coupled_cmhd_step(omega_hat, tau_hat, B_hat, rho_hat, p_hat, grid, nu, dt,
                      force_hat=0, scheme="rk2", t=0.0,
                      eta_p=0.003, lambda_relax=0.6, alpha=0.085,
                      beta_scar=0.13, stress_diff=1e-4, clay_gain=0.0,
                      gum_scale=1.0, stress_couple=1.0, regs=None,
                      eta_mag=1.0e-3, eta_odd=0.0, B_ext_hat=None,
                      induct_ext=1.0, mu_eff=0.0, berry_gain=0.0,
                      eta_hyper=0.0, posdiv=0.0, hyper_kcut=0.0,
                      psi_hat=None, glm_ch=0.0, glm_cr=0.18,
                      gamma=GAMMA_DEFAULT):
    """One incompressible MHD step plus density tracer and Russell p.

    Helmholtz stays ON. Density does not back-react (no nabla p).
    Q = eta|J|^2 + 2 nu S:S. mode="mhd" is not this function.
    """
    omega_hat, tau_hat, B_hat, psi_hat = coupled_mhd_step(
        omega_hat, tau_hat, B_hat, grid, nu, dt, force_hat, scheme, t,
        eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
        gum_scale, stress_couple, regs, eta_mag, eta_odd,
        B_ext_hat, induct_ext, mu_eff, berry_gain, eta_hyper, posdiv,
        hyper_kcut, psi_hat, glm_ch, glm_cr)
    u_hat = velocity_from_vorticity(omega_hat, grid)
    rho_hat = continuity_step(rho_hat, u_hat, grid, dt, scheme)
    Q = heating_Q(u_hat, B_hat, grid, eta_mag, nu, B_ext_hat)
    p_hat = pressure_step(p_hat, u_hat, grid, dt, scheme, gamma, Q)
    return omega_hat, tau_hat, B_hat, psi_hat, rho_hat, p_hat

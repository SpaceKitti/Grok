# ============================================================
# @Akitti C*Hive – Compressible density tracer (patch 3)
# Continuity:  ∂t ρ + ∇·(ρ u) = 0
# Dealias the product ρu (2/3 mask).
#
# Helmholtz projection stays ON: u is still the incompressible
# (Qin-projected) velocity. This is a density TRACER, not acoustics.
# Mean density is pinned to ⟨ρ⟩=1. Tiny positive floor after the step.
# mode="cmhd" (alias "compressible") enables the tracer.
# mode="mhd" is unchanged incompressible MHD.
# ============================================================

from functools import partial

import jax.numpy as jnp
from jax import jit

from .grid import velocity_from_vorticity
from .vorticity import coupled_mhd_step

# Tiny positive floor so ρ cannot go negative after a step.
RHO_FLOOR = 1e-14

# I_glm = 0  # Dedner damping −αψ is a sink not in I_leak. Stub only; no live-ψ test.


def uniform_rho_hat(grid, rho0=1.0, dtype=jnp.complex128):
    """Fourier density field with uniform physical value rho0 (default 1)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    rho = jnp.full((N,) * dim, float(rho0), dtype=jnp.float64)
    return jnp.fft.fftn(rho).astype(dtype)


def rho_from_hat(rho_hat):
    """Physical-space density (real)."""
    return jnp.fft.ifftn(rho_hat).real


@jit
def continuity_rhs(rho_hat, u_hat, grid):
    """Fourier RHS of ∂t ρ = −∇·(ρ u). Dealias the product ρu.

    u is the Helmholtz-projected incompressible velocity (tracer, not acoustics).
    """
    spatial = tuple(range(1, u_hat.ndim))
    u = jnp.fft.ifftn(u_hat, axes=spatial).real
    rho = jnp.fft.ifftn(rho_hat).real
    mom_hat = jnp.fft.fftn(rho * u, axes=spatial) * grid["dealias"]
    div_hat = 1j * jnp.sum(grid["k_stack"] * mom_hat, axis=0)
    return -div_hat * grid["dealias"]


def constrain_rho_hat(rho_hat, grid, floor=RHO_FLOOR):
    """Physical floor then pin ⟨ρ⟩=1. Re-dealias."""
    rho = jnp.fft.ifftn(rho_hat).real
    rho = jnp.maximum(rho, floor)
    rho = rho - jnp.mean(rho) + 1.0
    return jnp.fft.fftn(rho) * grid["dealias"]


@partial(jit, static_argnums=(4,))
def density_step(rho_hat, u_hat, grid, dt, scheme="rk2"):
    """Advance ρ one step with frozen Helmholtz-on u. Euler or Heun (rk2)."""

    def rhs(rho_hat):
        return continuity_rhs(rho_hat, u_hat, grid)

    if scheme == "euler":
        rho_hat = rho_hat + dt * rhs(rho_hat)
    else:
        k1 = rhs(rho_hat)
        k2 = rhs(rho_hat + dt * k1)
        rho_hat = rho_hat + 0.5 * dt * (k1 + k2)
    return constrain_rho_hat(rho_hat * grid["dealias"], grid)


# Alias used by __init__ / leftover driver notes.
continuity_step = density_step


def rho_diagnostics(rho_hat):
    """mean ρ, min ρ, max ρ, max|ρ−1|."""
    rho = jnp.fft.ifftn(rho_hat).real
    return {
        "mean_rho": jnp.mean(rho),
        "min_rho": jnp.min(rho),
        "max_rho": jnp.max(rho),
        "max_abs_rho_m1": jnp.max(jnp.abs(rho - 1.0)),
    }


def density_diagnostics(rho_hat, u_hat, grid):
    """Tracer monitors including max|∂t ρ| from the dealiased continuity RHS."""
    d = rho_diagnostics(rho_hat)
    drho_dt = jnp.fft.ifftn(continuity_rhs(rho_hat, u_hat, grid)).real
    d["max_drho_dt"] = jnp.max(jnp.abs(drho_dt))
    return d


def coupled_cmhd_step(omega_hat, tau_hat, B_hat, rho_hat, grid, nu, dt,
                      force_hat=0, scheme="rk2", t=0.0,
                      eta_p=0.003, lambda_relax=0.6, alpha=0.085,
                      beta_scar=0.13, stress_diff=1e-4, clay_gain=0.0,
                      gum_scale=1.0, stress_couple=1.0, regs=None,
                      eta_mag=1.0e-3, eta_odd=0.0, B_ext_hat=None,
                      induct_ext=1.0, mu_eff=0.0, berry_gain=0.0,
                      eta_hyper=0.0, posdiv=0.0, hyper_kcut=0.0,
                      psi_hat=None, glm_ch=0.0, glm_cr=0.18):
    """One MHD step (unchanged coupled_mhd_step) plus the density tracer.

    Helmholtz stays ON: u is the projected incompressible velocity.
    Density does not back-react (no ∇p, not acoustics).
    """
    omega_hat, tau_hat, B_hat, psi_hat = coupled_mhd_step(
        omega_hat, tau_hat, B_hat, grid, nu, dt, force_hat, scheme, t,
        eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
        gum_scale, stress_couple, regs, eta_mag, eta_odd,
        B_ext_hat, induct_ext, mu_eff, berry_gain, eta_hyper, posdiv,
        hyper_kcut, psi_hat, glm_ch, glm_cr)
    u_hat = velocity_from_vorticity(omega_hat, grid)
    rho_hat = density_step(rho_hat, u_hat, grid, dt, scheme)
    return omega_hat, tau_hat, B_hat, psi_hat, rho_hat

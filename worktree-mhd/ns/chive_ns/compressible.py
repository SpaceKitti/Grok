# ============================================================
# @Akitti C*Hive – Compressible MHD scaffold (patch 3)
# Live density rho(x) + continuity. Does not replace mode="mhd".
# Velocity remains the incompressible Helmholtz / Qin field from
# vorticity.coupled_mhd_step; density is passive here (no nabla p,
# no variable-rho inertia, no internal energy / EOS, no Brio-Wu).
# Patch 5 will drop Helmholtz. Patches 4, 6-8 are not in this file.
# No mean-pin and no floor: a pin would hide a continuity leak.
# I_glm = 0  # Dedner damping −αψ is a sink not in I_leak. Stub only.
# ============================================================

from functools import partial

import jax.numpy as jnp
from jax import jit

from .constants import DELTA_MIN
from .grid import velocity_from_vorticity
from .vorticity import coupled_mhd_step


def uniform_rho_hat(grid, rho0=1.0, dtype=jnp.complex128):
    """Fourier transform of uniform density rho === rho0 (default 1)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    rho = jnp.full((N,) * dim, float(rho0), dtype=jnp.float64)
    return jnp.fft.fftn(rho).astype(dtype)


def zero_eint_hat(grid, dtype=jnp.complex128):
    """Placeholder only: internal energy / EOS (patch 4). Not evolved."""
    N, dim = int(grid["N"]), int(grid["dim"])
    return jnp.zeros((N,) * dim, dtype=dtype)


@jit
def continuity_rhs(rho_hat, u_hat, grid):
    """Spectral 2/3-dealiased continuity: d_t rho = -div(rho u).

    Uniform rho and solenoidal (projected) u => RHS = 0 to roundoff.
    """
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
    """Advance rho with frozen u (projected incompressible u in this scaffold)."""
    if scheme == "euler":
        out = rho_hat + dt * continuity_rhs(rho_hat, u_hat, grid)
    else:
        k1 = continuity_rhs(rho_hat, u_hat, grid)
        k2 = continuity_rhs(rho_hat + dt * k1, u_hat, grid)
        out = rho_hat + 0.5 * dt * (k1 + k2)
    return out * grid["dealias"]


def density_diagnostics(rho_hat, u_hat, grid):
    """Uniform-rho leftover monitors: max|rho-1| and max|d_t rho|."""
    rho = jnp.fft.ifftn(rho_hat).real
    drho = jnp.fft.ifftn(continuity_rhs(rho_hat, u_hat, grid)).real
    return {
        "mean_rho": jnp.mean(rho),
        "max_rho": jnp.max(rho),
        "min_rho": jnp.min(rho),
        "max_abs_rho_m1": jnp.max(jnp.abs(rho - 1.0)),
        "max_drho_dt": jnp.max(jnp.abs(drho)),
    }


def coupled_cmhd_step(omega_hat, tau_hat, B_hat, rho_hat, grid, nu, dt, force_hat=0,
                      scheme="rk2", t=0.0, eta_p=0.003,
                      lambda_relax=0.6, alpha=0.085,
                      beta_scar=0.13, stress_diff=1e-4,
                      clay_gain=float(DELTA_MIN),
                      gum_scale=1.0, stress_couple=1.0,
                      regs=None, eta_mag=1.0e-3, eta_odd=0.0,
                      B_ext_hat=None, induct_ext=1.0, mu_eff=0.0,
                      berry_gain=0.0, eta_hyper=0.0, posdiv=0.0, hyper_kcut=0.0,
                      psi_hat=None, glm_ch=0.0, glm_cr=0.18):
    """One (omega, tau, B, psi, rho) step.

    MHD uses the existing incompressible coupled_mhd_step (Qin / Helmholtz
    on u). Continuity is advanced with that projected u; rho does not
    feed back into momentum in this scaffold.
    """
    u_hat = velocity_from_vorticity(omega_hat, grid)
    rho_hat = continuity_step(rho_hat, u_hat, grid, dt, scheme)
    omega_hat, tau_hat, B_hat, psi_hat = coupled_mhd_step(
        omega_hat, tau_hat, B_hat, grid, nu, dt, force_hat, scheme, t,
        eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
        gum_scale, stress_couple, regs, eta_mag, eta_odd,
        B_ext_hat, induct_ext, mu_eff, berry_gain, eta_hyper, posdiv,
        hyper_kcut, psi_hat, glm_ch, glm_cr)
    return omega_hat, tau_hat, B_hat, psi_hat, rho_hat

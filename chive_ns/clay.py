# ============================================================
# @Akitti C*Hive – Oldroyd-B E-brane Clay (tensor extra-stress)
# ============================================================

from functools import partial

import jax.numpy as jnp
from jax import jit

from .constants import DELTA_MIN, NU_GUM
from .grid import project_div_free, ik_cross, _vort_from_u_2d

# eta_p=0.003: holds Crow max|ω| near the IC without the η_p=0.008 energy drain.
DEFAULT_CLAY = dict(
    eta_p=0.003,
    lambda_relax=0.6,
    alpha=0.085,
    beta_scar=0.13,
    stress_diff=1e-4,
    clay_gain=float(DELTA_MIN),
    gum_scale=1.0,
    stress_couple=1.0,
)


@jit
def _trilinear_2d(u_hat, grid, alpha, beta_scar):
    u = jnp.fft.ifftn(u_hat, axes=(1, 2)).real
    F = alpha * jnp.stack([u[0]**3 + u[0] * u[1]**2,
                           u[1]**3 + u[1] * u[0]**2])
    F_hat = jnp.fft.fftn(F, axes=(1, 2))
    scar_amp = jnp.exp(1j * jnp.angle(jnp.sum(F_hat, 0))) * DELTA_MIN
    sigma = beta_scar * jnp.real(scar_amp**3 * jnp.conj(F_hat))
    return project_div_free(F_hat + sigma, grid)


@jit
def _trilinear_3d(u_hat, grid, alpha, beta_scar):
    u = jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real
    F = alpha * jnp.stack([
        u[0]**3 + u[0] * (u[1]**2 + u[2]**2),
        u[1]**3 + u[1] * (u[0]**2 + u[2]**2),
        u[2]**3 + u[2] * (u[0]**2 + u[1]**2),
    ])
    F_hat = jnp.fft.fftn(F, axes=(1, 2, 3))
    scar_amp = jnp.exp(1j * jnp.angle(jnp.sum(F_hat, 0))) * DELTA_MIN
    sigma = beta_scar * jnp.real(scar_amp**3 * jnp.conj(F_hat))
    return project_div_free(F_hat + sigma, grid)


def nonlinear_trilinear(u_hat, grid, alpha=0.085, beta_scar=0.13):
    """Fourier trilinear 3-pt scattering + scar multipoles (div-free)."""
    if u_hat.ndim == 3:
        return _trilinear_2d(u_hat, grid, alpha, beta_scar)
    return _trilinear_3d(u_hat, grid, alpha, beta_scar)


@jit
def gum_damping(tau_hat, t, gum_scale=1.0):
    """Gum E-brane damping + temporal flip + a small FG feed.

    gum_scale=0 disables both the shrink and the t-mod-1 flip (the flip
    would otherwise negate τ at t=0.5). The FG piece stays a perturbation.
    """
    damping = gum_scale * NU_GUM * DELTA_MIN * jnp.exp(-t * NU_GUM)
    raw_flip = jnp.where((t % 1.0) < 0.5, 1.0, -1.0)
    flip = 1.0 + gum_scale * (raw_flip - 1.0)
    fg00 = 0.92 + 0.31j
    return tau_hat * (1.0 - damping) * flip + damping * jnp.real(fg00 * tau_hat)


def zero_tau_hat(grid, dtype=jnp.complex128):
    """Quiescent extra-stress — C∞, Clay Case 1 compatible."""
    d, N = int(grid["dim"]), int(grid["N"])
    return jnp.zeros((d, d) + (N,) * d, dtype=dtype)


@jit
def _div_tau(tau_hat, grid):
    """(∇·τ)̂_i = i k_j τ̂_ij."""
    return 1j * jnp.einsum("j...,ij...->i...", grid["k_stack"], tau_hat)


@jit
def _stress_vort_force_2d(tau_hat, grid):
    return _vort_from_u_2d(_div_tau(tau_hat, grid), grid) * grid["dealias"]


@jit
def _stress_vort_force_3d(tau_hat, grid):
    return ik_cross(_div_tau(tau_hat, grid), grid) * grid["dealias"]


def stress_vorticity_force(tau_hat, grid):
    """∇×(∇·τ) in Fourier space — extra-stress feedback onto ω."""
    if tau_hat.ndim == 4:
        return _stress_vort_force_2d(tau_hat, grid)
    return _stress_vort_force_3d(tau_hat, grid)


@jit
def _oldroyd_rhs_2d(tau_hat, u_hat, grid, eta_p, lambda_relax, alpha,
                    beta_scar, stress_diff, clay_gain):
    dealias, k2, k = grid["dealias"], grid["k2"], grid["k_stack"]
    u = jnp.fft.ifftn(u_hat, axes=(1, 2)).real
    tau = jnp.fft.ifftn(tau_hat, axes=(2, 3)).real
    L = jnp.fft.ifftn(1j * u_hat[:, None] * k[None, :], axes=(2, 3)).real
    S = 0.5 * (L + jnp.swapaxes(L, 0, 1))
    grad_tau = jnp.fft.ifftn(
        1j * tau_hat[:, :, None] * k[None, None, :], axes=(3, 4)).real
    conv = jnp.einsum("k...,ijk...->ij...", u, grad_tau)
    deform = (jnp.einsum("ik...,kj...->ij...", L, tau) +
              jnp.einsum("ik...,jk...->ij...", tau, L))
    F_hat = _trilinear_2d(u_hat, grid, alpha, beta_scar)
    grad_F = jnp.fft.ifftn(1j * F_hat[:, None] * k[None, :], axes=(2, 3)).real
    clay_src = clay_gain * 0.5 * (grad_F + jnp.swapaxes(grad_F, 0, 1))
    dtau = (-conv + deform - tau / lambda_relax
            + (2.0 * eta_p / lambda_relax) * S + clay_src)
    dtau_hat = jnp.fft.fftn(dtau, axes=(2, 3)) * dealias - stress_diff * k2 * tau_hat
    return 0.5 * (dtau_hat + jnp.swapaxes(dtau_hat, 0, 1))


@jit
def _oldroyd_rhs_3d(tau_hat, u_hat, grid, eta_p, lambda_relax, alpha,
                    beta_scar, stress_diff, clay_gain):
    dealias, k2, k = grid["dealias"], grid["k2"], grid["k_stack"]
    u = jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real
    tau = jnp.fft.ifftn(tau_hat, axes=(2, 3, 4)).real
    L = jnp.fft.ifftn(1j * u_hat[:, None] * k[None, :], axes=(2, 3, 4)).real
    S = 0.5 * (L + jnp.swapaxes(L, 0, 1))
    grad_tau = jnp.fft.ifftn(
        1j * tau_hat[:, :, None] * k[None, None, :], axes=(3, 4, 5)).real
    conv = jnp.einsum("k...,ijk...->ij...", u, grad_tau)
    deform = (jnp.einsum("ik...,kj...->ij...", L, tau) +
              jnp.einsum("ik...,jk...->ij...", tau, L))
    F_hat = _trilinear_3d(u_hat, grid, alpha, beta_scar)
    grad_F = jnp.fft.ifftn(1j * F_hat[:, None] * k[None, :], axes=(2, 3, 4)).real
    clay_src = clay_gain * 0.5 * (grad_F + jnp.swapaxes(grad_F, 0, 1))
    dtau = (-conv + deform - tau / lambda_relax
            + (2.0 * eta_p / lambda_relax) * S + clay_src)
    dtau_hat = jnp.fft.fftn(dtau, axes=(2, 3, 4)) * dealias - stress_diff * k2 * tau_hat
    return 0.5 * (dtau_hat + jnp.swapaxes(dtau_hat, 0, 1))


def oldroyd_b_rhs(tau_hat, u_hat, grid, eta_p=0.003, lambda_relax=0.6,
                  alpha=0.085, beta_scar=0.13, stress_diff=1e-4,
                  clay_gain=float(DELTA_MIN)):
    """dτ/dt in Fourier space (no gum map — that is applied after the step)."""
    args = (tau_hat, u_hat, grid, eta_p, lambda_relax, alpha, beta_scar,
            stress_diff, clay_gain)
    if tau_hat.ndim == 4:
        return _oldroyd_rhs_2d(*args)
    return _oldroyd_rhs_3d(*args)


@partial(jit, static_argnums=(5,))
def _oldroyd_step_2d(tau_hat, u_hat, t, dt, grid, scheme,
                     eta_p, lambda_relax, alpha, beta_scar, stress_diff,
                     clay_gain, gum_scale):
    def rhs(tau):
        return _oldroyd_rhs_2d(tau, u_hat, grid, eta_p, lambda_relax,
                               alpha, beta_scar, stress_diff, clay_gain)
    if scheme == "euler":
        tau = tau_hat + dt * rhs(tau_hat)
    else:
        k1 = rhs(tau_hat)
        tau = tau_hat + 0.5 * dt * (k1 + rhs(tau_hat + dt * k1))
    return gum_damping(tau, t, gum_scale)


@partial(jit, static_argnums=(5,))
def _oldroyd_step_3d(tau_hat, u_hat, t, dt, grid, scheme,
                     eta_p, lambda_relax, alpha, beta_scar, stress_diff,
                     clay_gain, gum_scale):
    def rhs(tau):
        return _oldroyd_rhs_3d(tau, u_hat, grid, eta_p, lambda_relax,
                               alpha, beta_scar, stress_diff, clay_gain)
    if scheme == "euler":
        tau = tau_hat + dt * rhs(tau_hat)
    else:
        k1 = rhs(tau_hat)
        tau = tau_hat + 0.5 * dt * (k1 + rhs(tau_hat + dt * k1))
    return gum_damping(tau, t, gum_scale)


def oldroyd_b_step(tau_hat, u_hat, t, dt, grid, scheme="rk2",
                   eta_p=0.003, lambda_relax=0.6, alpha=0.085,
                   beta_scar=0.13, stress_diff=1e-4,
                   clay_gain=float(DELTA_MIN), gum_scale=1.0):
    """Advance the extra-stress tensor one step at frozen velocity.

    Does not replace the NS / stretching update — that lives in the
    coupled vorticity stepper. τ_0 = 0 is the Clay-smooth rest state.
    """
    args = (tau_hat, u_hat, t, dt, grid, scheme,
            eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
            gum_scale)
    if tau_hat.ndim == 4:
        return _oldroyd_step_2d(*args)
    return _oldroyd_step_3d(*args)

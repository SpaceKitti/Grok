# ============================================================
# @Akitti C*Hive – Late-May Oldroyd-B E-brane Clay
# ============================================================

import jax.numpy as jnp
from jax import jit
from functools import partial
from .constants import DELTA_MIN, NU_GUM
from .grid import project_div_free

@jit
def nonlinear_trilinear(u_hat, grid, alpha=0.085, beta_scar=0.13):
    """Fourier trilinear 3-pt scattering + scar multipoles."""
    u = jnp.fft.ifftn(u_hat, axes=range(1, grid["dim"]+1)).real
    if grid["dim"] == 2:
        F = alpha * jnp.stack([u[0]**3 + u[0]*u[1]**2,
                               u[1]**3 + u[1]*u[0]**2])
    else:
        F = alpha * jnp.stack([
            u[0]**3 + u[0]*(u[1]**2 + u[2]**2),
            u[1]**3 + u[1]*(u[0]**2 + u[2]**2),
            u[2]**3 + u[2]*(u[0]**2 + u[1]**2)])
    F_hat = jnp.fft.fftn(F, axes=range(1, grid["dim"]+1))
    scar_amp = jnp.exp(1j * jnp.angle(jnp.sum(F_hat, 0))) * DELTA_MIN
    sigma = beta_scar * jnp.real(scar_amp**3 * jnp.conj(F_hat))
    return project_div_free(F_hat + sigma[None], grid)

@jit
def gum_damping(tau_hat, t):
    """Gum E-brane + FG transport + temporal flip."""
    damping = NU_GUM * DELTA_MIN * jnp.exp(-t * NU_GUM)
    flip = jnp.where((t % 1.0) < 0.5, 1.0, -1.0)
    FG = jnp.array([[0.92+0.31j, -0.15-0.22j],
                    [0.18+0.25j, 0.88-0.29j]], dtype=jnp.complex128)
    return tau_hat * (1 - damping) * flip + jnp.real(FG[0,0] * tau_hat)

@partial(jit, static_argnums=(4,))
def oldroyd_b_step(state, t, dt, grid, piezo=None,
                   nu=5e-5, eta_p=0.12, lambda_relax=0.6, alpha=0.085):
    u_hat, tau_hat = state
    nl = nonlinear_trilinear(u_hat, grid, alpha)
    if piezo is not None:
        nl = nl + 0.4 * piezo[None] * jnp.exp(-0.05 * grid["k2"])
    du = -nl - nu * grid["k2"][None] * u_hat
    dtau = (2*eta_p * sum(grid["k"][i]*u_hat[i] for i in range(grid["dim"]))[None]
            - tau_hat / lambda_relax + nl[None]*alpha)
    return (project_div_free(u_hat + du*dt, grid),
            gum_damping(tau_hat, t) + dtau*dt)

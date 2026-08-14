# ============================================================
# @Akitti C*Hive – Early-May Vorticity + Z₇ Scar Forcing
# ============================================================

import jax.numpy as jnp
from jax import jit
from functools import partial

@jit
def modest_liar(t_norm):
 return jnp.sqrt(1.0 - jnp.clip(t_norm, 0.0, 1.0))

@partial(jit, static_argnums=(2,))
def z7_braid_forcing(grid, amplitude, center=None):
 """Z₇ anyonic phase + Gaussian mollifier → fractal butterfly scars."""
 N, L, dim = grid["N"], grid["L"], grid["dim"]
 if center is None:
 center = (L/2,) * dim
 x = jnp.linspace(0, L, N, endpoint=False)
 if dim == 2:
 X, Y = jnp.meshgrid(x, x, indexing="ij")
 dx, dy = X-center[0], Y-center[1]
 theta = jnp.arctan2(dy, dx)
 phase = jnp.cos(7*theta) + 0.5*jnp.sin(7*theta)
 force = amplitude * phase * jnp.exp(-(dx**2+dy**2)/(2*0.35**2))
 else:
 X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
 dx, dy = X-center[0], Y-center[1]
 theta = jnp.arctan2(dy, dx)
 phase = jnp.cos(7*theta) + 0.5*jnp.sin(7*theta)
 force = amplitude * phase * jnp.exp(-(dx**2+dy**2)/(2*0.30**2))
 force_hat = jnp.fft.fftn(force) * grid["dealias"]
 return force_hat * jnp.exp(-0.02 * grid["k2"])

@partial(jit, static_argnums=(3,))
def ns_vorticity_step(vort_hat, grid, nu, dt, force_hat=None):
 """Classic vorticity formulation (early-May)."""
 k2, dealias = grid["k2"], grid["dealias"]
 if grid["dim"] == 2:
 psi_hat = -vort_hat / k2
 u_hat = 1j * grid["k"][1] * psi_hat
 v_hat = -1j * grid["k"][0] * psi_hat
 u = jnp.fft.ifftn(u_hat).real
 v = jnp.fft.ifftn(v_hat).real
 adv = (u * jnp.fft.ifftn(1j*grid["k"][0]*vort_hat).real +
 v * jnp.fft.ifftn(1j*grid["k"][1]*vort_hat).real)
 adv_hat = jnp.fft.fftn(adv) * dealias
 else:
 adv_hat = 0.0 * vort_hat # full stretching can be inserted later
 rhs = -adv_hat - nu * k2 * vort_hat
 if force_hat is not None:
 rhs = rhs + force_hat
 return (vort_hat + dt * rhs) * dealias

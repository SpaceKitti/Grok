# ============================================================
# @Akitti C*Hive – Spectral Grid & Projection Utilities
# ============================================================

import jax
import jax.numpy as jnp
from jax import jit, random

@jit
def make_grid(N, L=1.0, dim=2):
 """Periodic torus (Clay Case 1). L=1 is the official Clay period."""
 k1d = jnp.fft.fftfreq(N, d=L/N) * 2 * jnp.pi
 if dim == 2:
 kx, ky = jnp.meshgrid(k1d, k1d, indexing="ij")
 k = (kx, ky)
 k2 = kx**2 + ky**2 + 1e-12
 dealias = (jnp.abs(kx) < (2/3)*k1d.max()) & (jnp.abs(ky) < (2/3)*k1d.max())
 else:
 kx, ky, kz = jnp.meshgrid(k1d, k1d, k1d, indexing="ij")
 k = (kx, ky, kz)
 k2 = kx**2 + ky**2 + kz**2 + 1e-12
 dealias = jnp.all(jnp.abs(jnp.stack(k)) < (2/3)*k1d.max(), axis=0)
 return {"k": k, "k2": k2, "dealias": dealias, "N": N, "L": L, "dim": dim}

@jit
def project_div_free(u_hat, grid):
 """Exact divergence-free projection on the torus (Clay-compatible)."""
 k, k2, dealias = grid["k"], grid["k2"], grid["dealias"]
 div = sum(k[i] * u_hat[i] for i in range(grid["dim"]))
 return (u_hat - jnp.stack(k) * div[None] / k2) * dealias[None]

@jit
def generate_smooth_div_free_u0(key, grid, scale=0.008, modes=8):
 """C∞ smooth, exactly divergence-free IC (Clay requirement)."""
 coeffs = random.normal(key, (grid["dim"],) + (grid["N"],)*grid["dim"],
 dtype=jnp.complex128)
 coeffs *= jnp.exp(-grid["k2"] / (2 * modes**2))
 u_hat = jnp.fft.fftn(coeffs, axes=range(1, grid["dim"]+1))
 u_hat = project_div_free(u_hat, grid)
 return jnp.fft.ifftn(u_hat, axes=range(1, grid["dim"]+1)).real * scale

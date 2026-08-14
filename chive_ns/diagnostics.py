# ============================================================
# @Akitti C*Hive – Diagnostics (λ₂, energy, IPR, etc.)
# ============================================================

import jax.numpy as jnp
from jax import jit

@jit
def lambda2_criterion(u, v, dx, dy):
    """Jeong–Hussain λ₂ criterion – negative regions = coherent structures / UNMI modes."""
    dudx = (jnp.roll(u, -1, 1) - jnp.roll(u, 1, 1)) / (2*dx)
    dudy = (jnp.roll(u, -1, 0) - jnp.roll(u, 1, 0)) / (2*dy)
    dvdx = (jnp.roll(v, -1, 1) - jnp.roll(v, 1, 1)) / (2*dx)
    dvdy = (jnp.roll(v, -1, 0) - jnp.roll(v, 1, 0)) / (2*dy)
    S11, S22 = dudx, dvdy
    S12 = 0.5*(dudy + dvdx)
    O12 = 0.5*(dudy - dvdx)
    return S11**2 + S12**2 - O12**2

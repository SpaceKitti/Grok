# ============================================================
# @Akitti C*Hive – Rayleigh–Plesset + Liu–Sun Attractor Tower
# ============================================================

import jax.numpy as jnp
from jax import jit, vmap
from .constants import DELTA_MIN

@jit
def rayleigh_plesset(R, dR, t, p):
    """Classic RP (spherical reduction of NS)."""
    Pg = p["Pg0"] * (p["R0"]/R)**(3*p["kappa"])
    Pinf = p["P0"] + p["Pa"]*jnp.sin(p["omega"]*t)
    return ((Pg - 4*p["mu"]*dR/R - 2*p["sigma"]/R - Pinf)/p["rho"]
            - 1.5*dR**2) / R

@jit
def attractor_tower(n, omega1_r, omega1_i, A1, alpha, t,
                    scar_floor=DELTA_MIN, mu_visc=0.01):
    """Liu–Sun attractor mapped onto bubble harmonics."""
    omega_n_r = n * omega1_r
    omega_n_i = n * omega1_i
    amp_n = alpha**(n-1) * A1**n
    protected = jnp.maximum(amp_n * jnp.exp(-omega_n_i*t), scar_floor)
    return protected * jnp.exp(-mu_visc*n*t) * jnp.cos(omega_n_r*t)

attractor_tower_v = vmap(attractor_tower, in_axes=(0, None, None, None, None, None, None, None))

@jit
def coupled_rp_attractor_rhs(y, t, p):
    """State y = [R, dR, A1]. Higher modes feed back as pressure forcing."""
    R, dR, A1 = y
    ns = jnp.arange(1, p["n_max"]+1)
    tower = attractor_tower_v(ns, p["omega1_r"], p["omega1_i"], A1,
                              p["alpha"], t, p["scar_floor"], p["mu_visc"])
    forcing = jnp.sum(tower * p["beta"])
    d2R = rayleigh_plesset(R, dR, t, p) + forcing / (p["rho"]*R)
    dA1 = -p["omega1_i"]*A1 + p["drive"]*jnp.sin(p["omega"]*t)
    return jnp.array([dR, d2R, dA1])

# ============================================================
# @Akitti C*Hive – Unified Driver
# ============================================================

import jax
import jax.numpy as jnp
from jax import random

from .grid import make_grid, project_div_free, generate_smooth_div_free_u0
from .vorticity import modest_liar, z7_braid_forcing, ns_vorticity_step
from .clay import oldroyd_b_step
from .bubble import coupled_rp_attractor_rhs
from .diagnostics import lambda2_criterion
from .constants import DELTA_MIN

def run_framework(N=32, dim=2, steps=800, mode="vorticity",
                  nu=0.001, dt=0.005, seed=42, force_on=True,
                  bubble_params=None):
    """
    mode = "vorticity"   → early-May scar-forced NS
         = "clay"        → late-May Oldroyd-B E-brane
         = "bubble"      → pure RP + Liu–Sun tower
         = "hybrid"      → clay + live λ₂ monitor
    """
    grid = make_grid(N, L=1.0 if mode != "bubble" else 2*jnp.pi, dim=dim)
    key = random.PRNGKey(seed)

    if mode == "bubble":
        p = bubble_params or {
            "rho": 1000., "sigma": 0.072, "mu": 0.001,
            "Pg0": 1.01325e5, "R0": 1e-5, "kappa": 1.4,
            "P0": 1.01325e5, "Pa": 1.2e5, "omega": 2*jnp.pi*20e3,
            "omega1_r": 2*jnp.pi*20e3, "omega1_i": 5e3,
            "alpha": 0.125, "n_max": 8, "beta": 0.05,
            "scar_floor": DELTA_MIN, "mu_visc": 0.01, "drive": 0.1
        }
        y = jnp.array([p["R0"], 0.0, 1.0])
        hist = []
        for step in range(steps):
            t = step * dt
            y = y + dt * coupled_rp_attractor_rhs(y, t, p)
            if step % 20 == 0:
                hist.append(y)
        return {"traj": jnp.stack(hist), "params": p}

    # Field-based modes
    u0 = generate_smooth_div_free_u0(key, grid)
    u_hat = jnp.fft.fftn(u0, axes=range(1, dim+1))
    tau_hat = jnp.zeros_like(u_hat)
    piezo = jnp.zeros((N,)*dim)

    energy, enstrophy, ipr, lambda2_hist = [], [], [], []

    for step in range(steps):
        t = step * dt
        t_norm = step / max(steps-1, 1)

        if mode == "vorticity":
            amp = modest_liar(t_norm) if force_on else 0.0
            force = z7_braid_forcing(grid, amp) if force_on else None
            if dim == 2:
                vort_hat = 1j*(grid["k"][0]*u_hat[1] - grid["k"][1]*u_hat[0])
            else:
                vort_hat = u_hat
            vort_hat = ns_vorticity_step(vort_hat, grid, nu, dt, force)
            u_hat = project_div_free(u_hat, grid)

        elif mode in ("clay", "hybrid"):
            u_hat, tau_hat = oldroyd_b_step(
                (u_hat, tau_hat), t, dt, grid, piezo, nu=nu)

        # Diagnostics
        if step % 20 == 0:
            u = jnp.fft.ifftn(u_hat, axes=range(1, dim+1)).real
            e = 0.5 * jnp.mean(jnp.sum(u**2, 0))
            energy.append(e)
            if dim == 2:
                vort = jnp.fft.ifftn(
                    1j*(grid["k"][0]*u_hat[1] - grid["k"][1]*u_hat[0])).real
                enstrophy.append(jnp.mean(vort**2))
                ipr.append(jnp.sum(vort**4) / (jnp.sum(vort**2)**2 + 1e-30))
                if mode == "hybrid":
                    dx = grid["L"] / N
                    l2 = lambda2_criterion(u[0], u[1], dx, dx)
                    lambda2_hist.append(jnp.mean(l2 < 0))
            else:
                enstrophy.append(e)
                ipr.append(0.0)

    out = {
        "energy": jnp.array(energy),
        "enstrophy": jnp.array(enstrophy),
        "ipr": jnp.array(ipr),
        "u_hat": u_hat,
        "grid": grid
    }
    if mode == "hybrid":
        out["lambda2_neg_frac"] = jnp.array(lambda2_hist)
    return out

# ============================================================
# @Akitti C*Hive – Unified Driver
# ============================================================

import jax
import jax.numpy as jnp
from jax import random

from .grid import (
    make_grid, project_div_free, generate_smooth_div_free_u0,
    generate_taylor_green, generate_antiparallel_tubes,
    velocity_from_vorticity, vorticity_from_velocity, cfl_dt,
)
from .vorticity import (
    modest_liar, z7_braid_forcing, ns_vorticity_step,
    coupled_vorticity_stress_step, resolve_scar_centres,
)
from .clay import DEFAULT_CLAY, zero_tau_hat
from .bubble import coupled_rp_attractor_rhs
from .diagnostics import field_diagnostics, millennium_series, sample_times
from .constants import DELTA_MIN


_TUBE_KEYS = ("circulation", "radius", "separation", "perturbation", "axial_wave")


def _initial_velocity(key, grid, ic, dim, ic_params=None):
    p = ic_params or {}
    if dim == 3 and ic == "taylor_green":
        return generate_taylor_green(grid, scale=p.get("scale", 1.0))
    if dim == 3 and ic == "tubes":
        return generate_antiparallel_tubes(
            grid, **{k: p[k] for k in _TUBE_KEYS if k in p})
    return generate_smooth_div_free_u0(key, grid)


def _scan_loop(advance, snapshot, state0, steps, diag_every):
    """Chunked lax.scan with a t=0 snapshot. `advance(state, idx) -> state`."""
    n_chunks = int(steps // diag_every)
    remainder = int(steps % diag_every)
    d0 = snapshot(state0)

    def chunk(state, cidx):
        start = cidx * diag_every

        def one(state, j):
            return advance(state, start + j), None

        state, _ = jax.lax.scan(one, state, jnp.arange(diag_every))
        return state, snapshot(state)

    if n_chunks:
        state, hist = jax.lax.scan(chunk, state0, jnp.arange(n_chunks))
        hist = jax.tree.map(lambda a, b: jnp.concatenate([a[None], b]), d0, hist)
    else:
        state, hist = state0, jax.tree.map(lambda v: v[None], d0)
    if remainder:
        start = n_chunks * diag_every

        def tail(state, j):
            return advance(state, start + j), None

        state, _ = jax.lax.scan(tail, state, jnp.arange(remainder))
        last = snapshot(state)
        hist = jax.tree.map(lambda a, b: jnp.concatenate([a, b[None]]), hist, last)
    return state, hist


def _run_vorticity_scanned(omega_hat, grid, nu, dt, steps, force_on,
                           scheme, diag_every, n_scars=1, scar_centres=None,
                           force_amp=1.0):
    """Pure NS stretching loop."""
    force_pat = z7_braid_forcing(grid, 1.0, n_scars=n_scars,
                                 scar_centres=scar_centres)
    force_scale = (1.0 if force_on else 0.0) * float(force_amp)

    def advance(omega_hat, idx):
        t_norm = idx / jnp.maximum(steps - 1, 1)
        force = force_pat * (modest_liar(t_norm) * force_scale)
        return ns_vorticity_step(omega_hat, grid, nu, dt, force, scheme)

    def snapshot(omega_hat):
        u_hat = velocity_from_vorticity(omega_hat, grid)
        return field_diagnostics(u_hat, grid, tau_hat=None)

    return _scan_loop(advance, snapshot, omega_hat, steps, diag_every)


def _run_clay_scanned(omega_hat, tau_hat, grid, nu, dt, steps, force_on,
                      scheme, diag_every, clay_params, n_scars=1,
                      scar_centres=None, force_amp=1.0):
    """Coupled NS stretching + Oldroyd-B extra-stress loop."""
    force_pat = z7_braid_forcing(grid, 1.0, n_scars=n_scars,
                                 scar_centres=scar_centres)
    force_scale = (1.0 if force_on else 0.0) * float(force_amp)
    eta_p = clay_params["eta_p"]
    lambda_relax = clay_params["lambda_relax"]
    alpha = clay_params["alpha"]
    beta_scar = clay_params["beta_scar"]
    stress_diff = clay_params["stress_diff"]
    clay_gain = clay_params["clay_gain"]
    gum_scale = clay_params.get("gum_scale", 1.0)
    stress_couple = clay_params.get("stress_couple", 1.0)

    def advance(state, idx):
        omega_hat, tau_hat = state
        t = idx * dt
        t_norm = idx / jnp.maximum(steps - 1, 1)
        force = force_pat * (modest_liar(t_norm) * force_scale)
        return coupled_vorticity_stress_step(
            omega_hat, tau_hat, grid, nu, dt, force, scheme, t,
            eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
            gum_scale, stress_couple)

    def snapshot(state):
        omega_hat, tau_hat = state
        u_hat = velocity_from_vorticity(omega_hat, grid)
        return field_diagnostics(u_hat, grid, tau_hat=tau_hat)

    return _scan_loop(advance, snapshot, (omega_hat, tau_hat), steps, diag_every)


def _pack_out(hist, u_hat, omega_hat, tau_hat, grid, dt, N, nu, ic, scheme,
              viscoelastic, clay_params, steps, diag_every, n_scars,
              scar_centres, force_on):
    time = sample_times(hist["energy"].shape[0], steps, dt, diag_every)
    mill = millennium_series(hist, time, nu)
    return {
        "energy": hist["energy"],
        "enstrophy": hist["enstrophy"],
        "ipr": hist["ipr"],
        "helicity": hist["helicity"],
        "max_vort": hist["max_vort"],
        "stretch": hist["stretch"],
        "max_div": hist["max_div"],
        "lambda2_neg_frac": hist["lambda2_neg_frac"],
        "mean_tau": hist["mean_tau"],
        "max_tau": hist["max_tau"],
        "tau_s": hist["tau_s"],
        "max_strain": mill["max_strain"],
        "palinstrophy": mill["palinstrophy"],
        "bkm_integral": mill["bkm_integral"],
        "dZ_dt": mill["dZ_dt"],
        "dE_dt": mill["dE_dt"],
        "dissipation": mill["dissipation"],
        "dZ_dt_budget": mill["dZ_dt_budget"],
        "time": mill["time"],
        "u_hat": u_hat,
        "omega_hat": omega_hat,
        "tau_hat": tau_hat,
        "grid": grid,
        "dt": dt,
        "N": N,
        "nu": nu,
        "ic": ic,
        "scheme": scheme,
        "viscoelastic": viscoelastic,
        "clay_params": clay_params,
        "n_scars": n_scars,
        "scar_centres": scar_centres,
        "force_on": force_on,
    }


def run_framework(N=None, dim=2, steps=800, mode="vorticity",
                  nu=None, dt=None, seed=42, force_on=True,
                  bubble_params=None, ic=None, scheme=None,
                  cfl=0.4, diag_every=20, viscoelastic=None,
                  clay_params=None, ic_params=None,
                  n_scars=1, scar_centres=None, force_amp=1.0):
    """
    mode = "vorticity"   → rotational-form NS (full 3D stretching)
         = "clay"        → same NS + Oldroyd-B E-brane extra-stress
         = "hybrid"      → alias for clay (λ₂ is always recorded in 3D)
         = "bubble"      → pure RP + Liu–Sun tower

    viscoelastic=True forces the clay coupling even if mode="vorticity".
    ic = "taylor_green" | "tubes" | "smooth".  tubes = Crow-perturbed
    anti-parallel pair (reconnection / singularity IC).
    n_scars / scar_centres select the helical Z₇ lattice (n_scars=1 default).
    dim=3 defaults: N=64, Taylor–Green IC, RK2, CFL dt, helical Z₇ force.
    """
    if viscoelastic is None:
        viscoelastic = mode in ("clay", "hybrid")
    if mode == "hybrid":
        mode = "clay" if viscoelastic else "vorticity"
    if clay_params is None:
        clay_params = dict(DEFAULT_CLAY)
    else:
        merged = dict(DEFAULT_CLAY)
        merged.update(clay_params)
        clay_params = merged

    if N is None:
        N = 64 if dim == 3 else 32
    if nu is None:
        nu = 5e-4 if dim == 3 else 0.001
    if ic is None:
        ic = "taylor_green" if dim == 3 else "smooth"
    if scheme is None:
        scheme = "rk2" if (dim == 3 or viscoelastic) else "euler"

    grid = make_grid(N, L=1.0 if mode != "bubble" else 2 * jnp.pi, dim=dim)
    key = random.PRNGKey(seed)

    if mode == "bubble":
        p = bubble_params or {
            "rho": 1000., "sigma": 0.072, "mu": 0.001,
            "Pg0": 1.01325e5, "R0": 1e-5, "kappa": 1.4,
            "P0": 1.01325e5, "Pa": 1.2e5, "omega": 2 * jnp.pi * 20e3,
            "omega1_r": 2 * jnp.pi * 20e3, "omega1_i": 5e3,
            "alpha": 0.125, "n_max": 8, "beta": 0.05,
            "scar_floor": DELTA_MIN, "mu_visc": 0.01, "drive": 0.1
        }
        y = jnp.array([p["R0"], 0.0, 1.0])
        hist = []
        bubble_dt = dt if dt is not None else 0.005
        for step in range(steps):
            t = step * bubble_dt
            y = y + bubble_dt * coupled_rp_attractor_rhs(y, t, p)
            if step % 20 == 0:
                hist.append(y)
        return {"traj": jnp.stack(hist), "params": p}

    u0 = _initial_velocity(key, grid, ic, dim, ic_params)
    if dt is None:
        nu_cfl = nu + (clay_params["eta_p"] if (viscoelastic or mode == "clay") else 0.0)
        dt = float(cfl_dt(u0, grid["dx"], nu_cfl, cfl=cfl))
        if dim == 2:
            dt = 0.005

    u_hat = project_div_free(jnp.fft.fftn(u0, axes=range(1, dim + 1)), grid)
    omega_hat = vorticity_from_velocity(u_hat, grid)
    if dim == 3:
        omega_hat = project_div_free(omega_hat, grid)

    centres = resolve_scar_centres(grid, n_scars, scar_centres)
    n_scars = len(centres)

    if viscoelastic or mode == "clay":
        tau_hat = zero_tau_hat(grid, dtype=omega_hat.dtype)
        (omega_hat, tau_hat), hist = _run_clay_scanned(
            omega_hat, tau_hat, grid, nu, dt, steps, force_on,
            scheme, diag_every, clay_params, n_scars, centres, force_amp)
    else:
        omega_hat, hist = _run_vorticity_scanned(
            omega_hat, grid, nu, dt, steps, force_on, scheme, diag_every,
            n_scars, centres, force_amp)
        tau_hat = zero_tau_hat(grid, dtype=omega_hat.dtype)

    u_hat = velocity_from_vorticity(omega_hat, grid)
    return _pack_out(hist, u_hat, omega_hat, tau_hat, grid, dt, N, nu, ic,
                     scheme, bool(viscoelastic or mode == "clay"), clay_params,
                     steps, diag_every, n_scars, centres, force_on)

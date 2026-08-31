"""Tubes + 4-scar Z₇: clay vs pure NS at the highest practical N.

    python examples/compare_tubes_scars.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax.numpy as jnp

from chive_ns import (
    run_framework, make_grid, generate_antiparallel_tubes, cfl_dt,
    default_scar_centres,
)


def _pick_dt(N, nu, eta_p, cfl=0.35):
    grid = make_grid(N, 1.0, 3)
    u = generate_antiparallel_tubes(grid)
    dt_ns = float(cfl_dt(u, 1.0 / N, nu, cfl))
    dt_cl = float(cfl_dt(u, 1.0 / N, nu + eta_p, cfl))
    umax = float(jnp.max(jnp.sqrt(jnp.sum(u**2, 0))))
    return min(dt_ns, dt_cl), umax


def main():
    # Same setup as the last successful N=96 Crow window, extended to t≈0.5.
    nu = 5.0e-4
    N = 96
    dt = 7.5542e-04
    umax = 1.562
    diag_every = 30
    steps = 660  # 660 * dt = 0.4986
    t_end = steps * dt
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=N, steps=steps, dt=dt, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=nu, diag_every=diag_every,
    )
    print(f"N={N}  umax={umax:.3f}  dt={dt:.4e}  steps={steps}  "
          f"t_end={steps*dt:.3f}  n_scars=4  force_amp=0.35", flush=True)
    print(f"scar lattice: {centres}", flush=True)
    print("tubes: Γ=0.7, r=0.08, sep=0.24, Crow ε=0.04 along x at y=0.38/0.62, z=0.5",
          flush=True)

    print("--- NS  tubes + 4 scars ---", flush=True)
    ns = run_framework(mode="vorticity", viscoelastic=False, **common)
    print("--- clay  tubes + 4 scars ---", flush=True)
    clay = run_framework(mode="clay", viscoelastic=True, **common)

    print(f"\nN={ns['N']}  nu={ns['nu']:.2e}  dt={ns['dt']:.4e}  "
          f"steps={steps}  t={float(ns['time'][-1]):.3f}")
    print(f"max|div u|  NS {float(ns['max_div'].max()):.3e}   "
          f"clay {float(clay['max_div'].max()):.3e}")
    print()
    print(f"{'t':>6}  {'E_NS':>9} {'E_cl':>9}  {'Z_NS':>9} {'Z_cl':>9}  "
          f"{'|ω|_NS':>9} {'|ω|_cl':>9}  {'|S|_NS':>9} {'|S|_cl':>9}")
    for i in range(len(ns["time"])):
        print(f"{float(ns['time'][i]):6.3f}  "
              f"{float(ns['energy'][i]):9.4e} {float(clay['energy'][i]):9.4e}  "
              f"{float(ns['enstrophy'][i]):9.4e} {float(clay['enstrophy'][i]):9.4e}  "
              f"{float(ns['max_vort'][i]):9.4e} {float(clay['max_vort'][i]):9.4e}  "
              f"{float(ns['max_strain'][i]):9.4e} {float(clay['max_strain'][i]):9.4e}")

    print()
    print(f"{'t':>6}  {'BKM_NS':>9} {'BKM_cl':>9}  {'dZ_NS':>9} {'dZ_cl':>9}  "
          f"{'ωSω_NS':>9} {'ωSω_cl':>9}  {'⟨|τ|⟩':>9} {'max|τ|':>9}")
    for i in range(len(ns["time"])):
        print(f"{float(ns['time'][i]):6.3f}  "
              f"{float(ns['bkm_integral'][i]):9.4e} {float(clay['bkm_integral'][i]):9.4e}  "
              f"{float(ns['dZ_dt'][i]):9.4e} {float(clay['dZ_dt'][i]):9.4e}  "
              f"{float(ns['stretch'][i]):9.4e} {float(clay['stretch'][i]):9.4e}  "
              f"{float(clay['mean_tau'][i]):9.4e} {float(clay['max_tau'][i]):9.4e}")

    print()
    print(f"peak max|ω|     NS {float(ns['max_vort'].max()):.4e}   clay {float(clay['max_vort'].max()):.4e}")
    print(f"peak max|S|     NS {float(ns['max_strain'].max()):.4e}   clay {float(clay['max_strain'].max()):.4e}")
    print(f"final BKM       NS {float(ns['bkm_integral'][-1]):.4e}   clay {float(clay['bkm_integral'][-1]):.4e}")
    print(f"peak dZ/dt      NS {float(ns['dZ_dt'].max()):.4e}   clay {float(clay['dZ_dt'].max()):.4e}")
    print(f"peak stretch    NS {float(ns['stretch'].max()):.4e}   clay {float(clay['stretch'].max()):.4e}")
    print(f"ΔE/E0           NS {(float(ns['energy'][0])-float(ns['energy'][-1]))/float(ns['energy'][0]):.3%}   "
          f"clay {(float(clay['energy'][0])-float(clay['energy'][-1]))/float(clay['energy'][0]):.3%}")
    print(f"peak ⟨|τ|⟩ / max|τ|  {float(clay['mean_tau'].max()):.4e}  /  {float(clay['max_tau'].max()):.4e}")
    return ns, clay


if __name__ == "__main__":
    main()

"""N=64 Crow tubes: pure NS vs Oldroyd-B clay.

Run from the repo root:

    python examples/compare_tubes.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import run_framework


def main():
    common = dict(dim=3, N=64, steps=80, ic="tubes", scheme="rk2",
                  force_on=False, diag_every=20, nu=5e-4, dt=0.0015)
    print("Compiling / running tubes, pure NS ...")
    ns = run_framework(mode="vorticity", viscoelastic=False, **common)
    print("Compiling / running tubes, clay ...")
    clay = run_framework(mode="clay", viscoelastic=True, **common)

    print(f"\nN={ns['N']}  nu={ns['nu']:.2e}  dt={ns['dt']:.4e}  ic={ns['ic']}")
    print(f"clay params: {clay['clay_params']}")
    print()
    print("Crow tubes — Clay–Millennium monitors  (NS left, clay right)")
    print(f"{'t':>6}  {'E_NS':>9} {'E_clay':>9}  {'Z_NS':>9} {'Z_clay':>9}  "
          f"{'max|ω|_NS':>9} {'max|ω|_cl':>9}  {'max|S|_NS':>9} {'max|S|_cl':>9}")
    for i in range(len(ns["energy"])):
        t = float(ns["time"][i])
        print(f"{t:6.3f}  "
              f"{float(ns['energy'][i]):9.4e} {float(clay['energy'][i]):9.4e}  "
              f"{float(ns['enstrophy'][i]):9.4e} {float(clay['enstrophy'][i]):9.4e}  "
              f"{float(ns['max_vort'][i]):9.4e} {float(clay['max_vort'][i]):9.4e}  "
              f"{float(ns['max_strain'][i]):9.4e} {float(clay['max_strain'][i]):9.4e}")

    print()
    print(f"{'t':>6}  {'BKM_NS':>9} {'BKM_cl':>9}  {'ω·S·ω_NS':>9} {'ω·S·ω_cl':>9}  "
          f"{'dZ/dt_NS':>9} {'dZ/dt_cl':>9}  {'⟨|τ|⟩':>9} {'max|τ|':>9}")
    for i in range(len(ns["energy"])):
        t = float(ns["time"][i])
        print(f"{t:6.3f}  "
              f"{float(ns['bkm_integral'][i]):9.4e} {float(clay['bkm_integral'][i]):9.4e}  "
              f"{float(ns['stretch'][i]):9.4e} {float(clay['stretch'][i]):9.4e}  "
              f"{float(ns['dZ_dt'][i]):9.4e} {float(clay['dZ_dt'][i]):9.4e}  "
              f"{float(clay['mean_tau'][i]):9.4e} {float(clay['max_tau'][i]):9.4e}")

    print()
    print(f"max |div u|        NS {float(ns['max_div'].max()):.3e}   clay {float(clay['max_div'].max()):.3e}")
    print(f"final BKM          NS {float(ns['bkm_integral'][-1]):.4e}   clay {float(clay['bkm_integral'][-1]):.4e}")
    print(f"peak max|ω|        NS {float(ns['max_vort'].max()):.4e}   clay {float(clay['max_vort'].max()):.4e}")
    print(f"peak max|S|        NS {float(ns['max_strain'].max()):.4e}   clay {float(clay['max_strain'].max()):.4e}")
    print(f"peak stretch ω·S·ω NS {float(ns['stretch'].max()):.4e}   clay {float(clay['stretch'].max()):.4e}")
    print(f"peak dZ/dt         NS {float(ns['dZ_dt'].max()):.4e}   clay {float(clay['dZ_dt'].max()):.4e}")
    print(f"peak |τ|           clay {float(clay['max_tau'].max()):.4e}")
    return ns, clay


if __name__ == "__main__":
    main()

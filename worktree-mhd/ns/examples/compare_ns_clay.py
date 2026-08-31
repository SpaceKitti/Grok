"""N=64 3D Taylor–Green: pure NS vs Oldroyd-B clay, Clay-Millennium diagnostics.

Run from the repo root:

    python examples/compare_ns_clay.py

Higher-resolution / lower-viscosity sweep:

    python examples/study_hires_nu.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import run_framework


def main():
    common = dict(dim=3, N=64, steps=80, ic="taylor_green", scheme="rk2",
                  force_on=False, diag_every=20, nu=5e-4, dt=0.002)
    print("Compiling / running pure NS ...")
    ns = run_framework(mode="vorticity", viscoelastic=False, **common)
    print("Compiling / running clay (Oldroyd-B + stretching) ...")
    clay = run_framework(mode="clay", viscoelastic=True, **common)

    print(f"\nN={ns['N']}  nu={ns['nu']:.2e}  dt={ns['dt']:.4e}  ic={ns['ic']}")
    print(f"clay params: {clay['clay_params']}")
    print()
    print("Clay–Millennium monitors  (NS left, clay right)")
    hdr = (f"{'t':>6}  {'max|ω|':>9} {'':>9}  {'max|S|':>9} {'':>9}  "
           f"{'BKM':>9} {'':>9}  {'dZ/dt':>9} {'':>9}  {'ε':>9} {'':>9}")
    print(hdr)
    print(f"{'':>6}  {'NS':>9} {'clay':>9}  {'NS':>9} {'clay':>9}  "
          f"{'NS':>9} {'clay':>9}  {'NS':>9} {'clay':>9}  {'NS':>9} {'clay':>9}")
    for i in range(len(ns["energy"])):
        t = float(ns["time"][i])
        print(f"{t:6.3f}  "
              f"{float(ns['max_vort'][i]):9.4e} {float(clay['max_vort'][i]):9.4e}  "
              f"{float(ns['max_strain'][i]):9.4e} {float(clay['max_strain'][i]):9.4e}  "
              f"{float(ns['bkm_integral'][i]):9.4e} {float(clay['bkm_integral'][i]):9.4e}  "
              f"{float(ns['dZ_dt'][i]):9.4e} {float(clay['dZ_dt'][i]):9.4e}  "
              f"{float(ns['dissipation'][i]):9.4e} {float(clay['dissipation'][i]):9.4e}")

    print()
    print("Energy / enstrophy / stretch / stress")
    print(f"{'t':>6}  {'E_NS':>10} {'E_clay':>10}  {'Z_NS':>10} {'Z_clay':>10}  "
          f"{'ω·S·ω_NS':>10} {'ω·S·ω_cl':>10}  {'⟨|τ|⟩':>10} {'max|τ|':>10}")
    for i in range(len(ns["energy"])):
        t = float(ns["time"][i])
        print(f"{t:6.3f}  "
              f"{float(ns['energy'][i]):10.4e} {float(clay['energy'][i]):10.4e}  "
              f"{float(ns['enstrophy'][i]):10.4e} {float(clay['enstrophy'][i]):10.4e}  "
              f"{float(ns['stretch'][i]):10.4e} {float(clay['stretch'][i]):10.4e}  "
              f"{float(clay['mean_tau'][i]):10.4e} {float(clay['max_tau'][i]):10.4e}")

    print()
    print(f"max |div u|      NS {float(ns['max_div'].max()):.3e}   clay {float(clay['max_div'].max()):.3e}")
    print(f"final BKM ∫||ω||∞  NS {float(ns['bkm_integral'][-1]):.4e}   clay {float(clay['bkm_integral'][-1]):.4e}")
    print(f"peak max|ω|      NS {float(ns['max_vort'].max()):.4e}   clay {float(clay['max_vort'].max()):.4e}")
    print(f"peak max|S|      NS {float(ns['max_strain'].max()):.4e}   clay {float(clay['max_strain'].max()):.4e}")
    print(f"peak dZ/dt       NS {float(ns['dZ_dt'].max()):.4e}   clay {float(clay['dZ_dt'].max()):.4e}")
    print(f"peak ε           NS {float(ns['dissipation'].max()):.4e}   clay {float(clay['dissipation'].max()):.4e}")
    print(f"final dE/dt      NS {float(ns['dE_dt'][-1]):.4e}   clay {float(clay['dE_dt'][-1]):.4e}")
    print(f"peak |τ|         clay {float(clay['max_tau'].max()):.4e}")
    return ns, clay


if __name__ == "__main__":
    main()

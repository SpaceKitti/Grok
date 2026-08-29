"""N=32 Crow tubes: pure NS vs spectral MHD (smoke).

Short CPU-friendly check that mode="mhd" advances induction + Lorentz
on the same Fourier grid. Defaults follow MHD2/02 hypotheses
(b_guide="z", eta=1e-3, B0=0.08) -- research dials, not settled physics.

Run from the repo root:

    python examples/compare_tubes_mhd.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import run_framework


def main():
    common = dict(dim=3, N=32, steps=40, ic="tubes", scheme="rk2",
                  force_on=False, diag_every=10, nu=5e-4, dt=0.002)
    mhd_params = dict(eta=1e-3, B0=0.08, b_guide="z")

    print("Compiling / running tubes, pure NS ...")
    ns = run_framework(mode="vorticity", viscoelastic=False, **common)
    print("Compiling / running tubes, MHD ...")
    mhd = run_framework(mode="mhd", viscoelastic=False,
                        mhd_params=mhd_params, **common)

    print(f"\nN={ns['N']}  nu={ns['nu']:.2e}  dt={ns['dt']:.4e}  ic={ns['ic']}")
    print(f"mhd params: {mhd['mhd_params']}")
    print()
    print("Crow tubes -- NS vs MHD monitors")
    print(f"{'t':>6}  {'E_NS':>9} {'E_MHD':>9}  {'Emag':>9}  "
          f"{'max|w|_NS':>9} {'max|w|_M':>9}  {'max|J|':>9}  {'max|divB|':>9}")
    for i in range(len(ns["energy"])):
        t = float(ns["time"][i])
        print(f"{t:6.3f}  "
              f"{float(ns['energy'][i]):9.4e} {float(mhd['energy'][i]):9.4e}  "
              f"{float(mhd['mag_energy'][i]):9.4e}  "
              f"{float(ns['max_vort'][i]):9.4e} {float(mhd['max_vort'][i]):9.4e}  "
              f"{float(mhd['max_J'][i]):9.4e}  {float(mhd['max_divB'][i]):9.4e}")

    print()
    print(f"{'t':>6}  {'BKM_NS':>9} {'BKM_M':>9}  {'H_cross':>9}  {'H_mag':>9}  "
          f"{'ohmic':>9}")
    for i in range(len(ns["energy"])):
        t = float(ns["time"][i])
        print(f"{t:6.3f}  "
              f"{float(ns['bkm_integral'][i]):9.4e} {float(mhd['bkm_integral'][i]):9.4e}  "
              f"{float(mhd['cross_helicity'][i]):9.4e}  "
              f"{float(mhd['mag_helicity'][i]):9.4e}  "
              f"{float(mhd['ohmic'][i]):9.4e}")

    print()
    print(f"max |div u|   NS {float(ns['max_div'].max()):.3e}   MHD {float(mhd['max_div'].max()):.3e}")
    print(f"max |div B|   MHD {float(mhd['max_divB'].max()):.3e}")
    print(f"final BKM     NS {float(ns['bkm_integral'][-1]):.4e}   MHD {float(mhd['bkm_integral'][-1]):.4e}")
    print(f"peak max|w|   NS {float(ns['max_vort'].max()):.4e}   MHD {float(mhd['max_vort'].max()):.4e}")
    print(f"peak Emag     MHD {float(mhd['mag_energy'].max()):.4e}")
    print(f"peak max|J|   MHD {float(mhd['max_J'].max()):.4e}")
    return ns, mhd


if __name__ == "__main__":
    main()

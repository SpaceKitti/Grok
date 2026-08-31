"""Twins identical except B. No retune.

    python examples/twin_hydro_mhd_drop.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import run_framework, DEFAULT_MHD, default_scar_centres


def main():
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=48, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    mhd = dict(DEFAULT_MHD, freeze_ext=0.0, eta_mag=1e-3,
               eta_odd=0.0, mu_eff=0.0, eta_hyper=0.0,
               posdiv=0.0, hyper_kcut=0.0)

    print("--- 1 MHD Crow-pair ---", flush=True)
    m = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                      mhd_params=mhd, **common)
    em0 = float(m["energy"][0] + m["e_mag_tot"][0])
    em1 = float(m["energy"][-1] + m["e_mag_tot"][-1])
    drop_mhd = em0 - em1
    pct_mhd = 100.0 * drop_mhd / em0

    print("--- 2 hydro Crow-pair B=0 ---", flush=True)
    h = run_framework(mode="vorticity", viscoelastic=False, magnetic=False,
                      **common)
    eh0 = float(h["energy"][0])
    eh1 = float(h["energy"][-1])
    drop_hy = eh0 - eh1
    pct_hy = 100.0 * drop_hy / eh0

    diff = drop_mhd - drop_hy
    print("\n========== three numbers ==========")
    print(f"E drop hydro     {drop_hy:.6e}   ({pct_hy:.2f}%)")
    print(f"E drop MHD       {drop_mhd:.6e}   ({pct_mhd:.2f}%)")
    print(f"MHD − hydro      {diff:.6e}   ({100.0 * diff / eh0:.2f}% of E_hydro(0))")
    print(f"E_hydro(0)={eh0:.6e}  E_MHD_tot(0)={em0:.6e}  "
          f"|ω|_h={float(h['max_vort'][-1]):.3f}  |ω|_m={float(m['max_vort'][-1]):.3f}")


if __name__ == "__main__":
    main()

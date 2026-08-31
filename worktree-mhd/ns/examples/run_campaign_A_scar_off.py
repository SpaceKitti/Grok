"""Clone of Campaign A NS+MHD with ONLY force_on=False.

Exact source: examples/compare_lorentz_channels.py _run()
  N=48, steps=240, dt=0.0015, t=0.36, ic=tubes, n_scars=4,
  force_amp=0.35, nu=5e-4, eta_mag=1e-3, eta_hyper=0, hyper_kcut=0,
  freeze_ext=0, scheme=rk2, viscoelastic=False.

    python examples/run_campaign_A_scar_off.py
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax.numpy as jnp

from chive_ns import run_framework, DEFAULT_MHD, default_scar_centres

OUT_DIR = Path(__file__).resolve().parent / "mhd_n48_hyperkcut"


def _trapz(y, t):
    y, t = jnp.asarray(y), jnp.asarray(t)
    if y.shape[0] < 2:
        return 0.0
    return float(jnp.sum(0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])))


def main():
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=48, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=False, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    mhd = dict(DEFAULT_MHD, freeze_ext=0.0, eta_mag=1e-3,
               eta_odd=0.0, mu_eff=0.0, eta_hyper=0.0,
               posdiv=0.0, hyper_kcut=0.0)

    print("Campaign A clone  scar force OFF", flush=True)
    print(f"force_on={common['force_on']}  force_amp={common['force_amp']}",
          flush=True)
    print(f"N={common['N']} dt={common['dt']} steps={common['steps']}  "
          f"ic={common['ic']} n_scars={common['n_scars']} nu={common['nu']}  "
          f"eta_mag={mhd['eta_mag']} eta_hyper={mhd['eta_hyper']}  "
          f"hyper_kcut={mhd['hyper_kcut']} scheme={common['scheme']}  "
          f"viscoelastic=False", flush=True)

    out = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                        mhd_params=mhd, **common)

    t = out["time"]
    nu = float(out["nu"])
    e_k, e_m = out["energy"], out["e_mag_tot"]
    I_WL = _trapz(out["lorentz_work"], t)
    I_nu = _trapz(nu * out["enstrophy"], t)
    I_eta = _trapz(out["ohmic"], t)
    dEk = float(e_k[-1] - e_k[0])
    dEm = float(e_m[-1] - e_m[0])
    dEtot = 100.0 * (-(dEk + dEm)) / max(float(e_k[0] + e_m[0]), 1e-30)
    dEkin = 100.0 * (-dEk) / max(float(e_k[0]), 1e-30)
    dEmag = 100.0 * dEm / max(float(e_m[0]), 1e-30)
    trans = abs(I_WL) + 1e-30
    kin_res = 100.0 * (dEk - (I_WL - I_nu)) / trans
    mag_res = 100.0 * (dEm - (-I_WL - I_eta)) / trans
    w1 = float(out["max_vort"][-1])
    max_j = float(out["max_j"].max())
    lam = float(out["lam_min_dx"][-1])

    print("\n========== Campaign A scar_off ledger t=0.36 ==========")
    print(f"force_on={common['force_on']}  force_amp={common['force_amp']}")
    print(f"{'ΔE_tot%':>8} {'ΔE_kin%':>8} {'ΔE_mag%':>8} {'∫W_L':>11} "
          f"{'∫ε_ν':>11} {'∫ε_η':>11}")
    print(f"{dEtot:8.2f} {dEkin:8.2f} {dEmag:8.2f} {I_WL:11.3e} "
          f"{I_nu:11.3e} {I_eta:11.3e}")
    print(f"{'kin_res%':>9} {'mag_res%':>9} {'|ω|_end':>8} {'max|J|':>9} "
          f"{'λ_min/dx':>9}")
    print(f"{kin_res:9.2f} {mag_res:9.2f} {w1:8.3f} {max_j:9.3e} {lam:9.3f}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUT_DIR / "mhd_dissipation_scar_off.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "case", "force_on", "force_amp", "dE_tot_pct", "dE_kin_pct",
            "dE_mag_pct", "int_WL", "int_eps_nu", "int_eps_eta",
            "kin_res_pct", "mag_res_pct", "omega_end", "max_J", "lam_min_dx",
        ])
        w.writerow([
            "NS+MHD scar_off", common["force_on"], common["force_amp"],
            f"{dEtot:.4f}", f"{dEkin:.4f}", f"{dEmag:.4f}",
            f"{I_WL:.6e}", f"{I_nu:.6e}", f"{I_eta:.6e}",
            f"{kin_res:.3f}", f"{mag_res:.3f}", f"{w1:.4f}",
            f"{max_j:.6e}", f"{lam:.4f}",
        ])
        w.writerow([])
        w.writerow(["t", "energy", "e_mag_tot", "max_vort", "max_j",
                    "lam_min_dx", "lorentz_work", "ohmic", "enstrophy"])
        for i in range(len(t)):
            w.writerow([
                f"{float(t[i]):.4f}",
                f"{float(e_k[i]):.8e}",
                f"{float(e_m[i]):.8e}",
                f"{float(out['max_vort'][i]):.6e}",
                f"{float(out['max_j'][i]):.6e}",
                f"{float(out['lam_min_dx'][i]):.4f}",
                f"{float(out['lorentz_work'][i]):.8e}",
                f"{float(out['ohmic'][i]):.8e}",
                f"{float(out['enstrophy'][i]):.8e}",
            ])
    print(f"\nwrote {csv_path}")


if __name__ == "__main__":
    main()

"""B0 scan only. Same N=96 twins otherwise. No retune.

    python examples/b0_halo_vs_sheet.py
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from chive_ns import run_framework, DEFAULT_MHD, default_scar_centres
from chive_ns.mhd import current_from_b

NU = 5e-4
DT = 0.0015
STEPS = 240
N = 96
OUT = Path(__file__).resolve().parent / "mhd_n96_b0_scan"

# Same B=0 hydro twin as the N=96 mask run. Hydro does not depend on B0.
# Do not re-run hydro: that twin already printed 5.96%.
DROP_HY = 4.198410307079917e-03
I_NU_HY = 4.073760338582395e-03
W_HY = 37.71638285089682
HY_PCT = 5.96


def _trapz(y, t):
    y, t = np.asarray(y), np.asarray(t)
    if y.shape[0] < 2:
        return 0.0
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])))


def _ohmic_fracs(m):
    J_hat = np.array(current_from_b(m["B_hat"], m["grid"]))
    J = np.fft.ifftn(J_hat, axes=(1, 2, 3)).real
    j2 = np.sum(J**2, axis=0)
    jmag = np.sqrt(j2)
    jmax = float(jmag.max())
    tot = float(np.sum(j2)) + 1e-30
    f_half = float(np.sum(j2 * (jmag >= 0.5 * jmax))) / tot
    f_eighth = float(np.sum(j2 * (jmag >= 0.125 * jmax))) / tot
    return jmax, f_half, f_eighth


def _finite(m):
    keys = ("energy", "e_mag_tot", "ohmic", "enstrophy", "max_vort")
    for k in keys:
        a = np.asarray(m[k], dtype=float)
        if not np.isfinite(a).all():
            return False
    return True


def _blown(m):
    if not _finite(m):
        return "nonfinite"
    w = float(np.max(np.asarray(m["max_vort"])))
    if w > 1.0e3:
        return f"max|ω|={w:.3e}"
    em = np.asarray(m["energy"]) + np.asarray(m["e_mag_tot"])
    if float(np.max(em)) > 50.0 * float(em[0] + 1e-30):
        return "energy explosion"
    return None


def run_mhd(B0):
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=N, steps=STEPS, dt=DT, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=NU, diag_every=40,
    )
    mhd_p = dict(DEFAULT_MHD, freeze_ext=0.0, eta_mag=1e-3, B0=float(B0),
                 eta_odd=0.0, mu_eff=0.0, eta_hyper=0.0,
                 posdiv=0.0, hyper_kcut=0.0)
    print(f"--- MHD B0={B0} ---", flush=True)
    m = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                      mhd_params=mhd_p, **common)
    why = _blown(m)
    if why:
        print(f"B0={B0} UNSTABLE ({why})", flush=True)
        return None
    em0 = float(m["energy"][0] + m["e_mag_tot"][0])
    em1 = float(m["energy"][-1] + m["e_mag_tot"][-1])
    drop = em0 - em1
    i_eta = _trapz(np.array(m["ohmic"]), np.array(m["time"]))
    i_nu = _trapz(NU * np.array(m["enstrophy"]), np.array(m["time"]))
    jmax, f_half, f_eighth = _ohmic_fracs(m)
    w = float(m["max_vort"][-1])
    row = dict(B0=B0, drop=drop, em0=em0, I_eta=i_eta, I_nu=i_nu,
               jmax=jmax, f_half=f_half, f_eighth=f_eighth, w=w)
    print(f"B0={B0}  dE={drop:.6e}  ∫ε_η={i_eta:.6e}  ∫ε_ν={i_nu:.6e}  "
          f"max|J|={jmax:.3f}  |J|≥½ {100*f_half:.1f}%  "
          f"|J|≥⅛ {100*f_eighth:.1f}%  ‖ω‖={w:.3f}", flush=True)
    return row


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    hydro = dict(drop=DROP_HY, I_nu=I_NU_HY, w=W_HY, pct=HY_PCT)
    rows = []
    # B0=0.08 already have from N=96 twins (same kwargs, B0 default).
    rows.append(dict(
        B0=0.08,
        drop=4.613759632526471e-03,
        I_eta=5.802100812816026e-04,
        I_nu=3.919949267936554e-03,
        jmax=24.94811633817377,
        f_half=0.221144,
        f_eighth=0.939641,
        w=34.366620158042245,
        reused=True,
    ))
    print("B0=0.08 reused from N=96 twins (same kwargs)", flush=True)

    for B0 in (0.2, 0.5):
        try:
            row = run_mhd(B0)
        except Exception as exc:
            print(f"B0={B0} FAILED {type(exc).__name__}: {exc}", flush=True)
            row = None
        if row is None:
            print(f"stopping: B0={B0} not stable", flush=True)
            break
        row["reused"] = False
        rows.append(row)

    path = OUT / "b0_scan.csv"
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["B0", "E_drop_hydro", "E_drop_MHD", "MHD_minus_hydro",
                    "int_Ohmic", "int_visc_hydro", "int_visc_MHD",
                    "max_J", "ohmic_frac_half", "ohmic_frac_eighth",
                    "max_vort_MHD", "reused"])
        for r in rows:
            w.writerow([
                r["B0"], hydro["drop"], r["drop"], r["drop"] - hydro["drop"],
                r["I_eta"], hydro["I_nu"], r["I_nu"],
                r["jmax"], r["f_half"], r["f_eighth"], r["w"],
                r.get("reused", False),
            ])
        w.writerow(["hydro_pct", hydro["pct"]])
        w.writerow(["hydro_max_vort", hydro["w"]])
    print(f"wrote {path}", flush=True)

    pct = hydro["pct"]
    valid = 5.7 <= pct <= 6.2
    print()
    print("VALID" if valid else "INVALID")
    print(f"{'B0':>6} {'E_hy':>11} {'E_MHD':>11} {'MHD-hy':>11} "
          f"{'∫ε_η':>11} {'∫ε_ν hy':>11} {'∫ε_ν MHD':>11} "
          f"{'max|J|':>8} {'%½':>6} {'%⅛':>6}")
    for r in rows:
        print(f"{r['B0']:6.2f} {hydro['drop']:11.4e} {r['drop']:11.4e} "
              f"{r['drop']-hydro['drop']:11.4e} {r['I_eta']:11.4e} "
              f"{hydro['I_nu']:11.4e} {r['I_nu']:11.4e} "
              f"{r['jmax']:8.2f} {100*r['f_half']:5.1f}% {100*r['f_eighth']:5.1f}%")


if __name__ == "__main__":
    main()

"""B0 fill-in at ν=1.25e-4. When does halo→ribbon flip. No retune.

    python examples/b0_flip_nu125.py
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from chive_ns import run_framework, DEFAULT_MHD, default_scar_centres
from chive_ns.mhd import current_from_b

NU = 1.25e-4
DT = 0.0015
STEPS = 240
N = 96
OUT = Path(__file__).resolve().parent / "mhd_n96_nu_scan"

# Same hydro twin as ν=1.25e-4 scan. Must stay ~1.71%.
HYDRO = dict(
    drop=1.2018693708298472e-03,
    I_nu=1.0775123393526897e-03,
    w=41.420576200997544,
    pct=1.71,
)

HAVE = {
    0.08: dict(
        drop=1.7785869462865894e-03,
        I_eta=6.343061417160345e-04,
        I_nu=1.0335999884504257e-03,
        jmax=27.932286653702775,
        f_half=0.21242021508082415,
        f_eighth=0.9336495715880231,
        w=37.531242289597884,
        reused=True,
    ),
    0.50: dict(
        drop=5.827784433055372e-03,
        I_eta=5.015789074133626e-03,
        I_nu=7.58982288618353e-04,
        jmax=26.621448138339066,
        f_half=0.5732249964334583,
        f_eighth=0.967444760348734,
        w=28.47702111576309,
        reused=True,
    ),
}


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


def _blown(m):
    keys = ("energy", "e_mag_tot", "ohmic", "enstrophy", "max_vort")
    for k in keys:
        if not np.isfinite(np.asarray(m[k], dtype=float)).all():
            return "nonfinite"
    w = float(np.max(np.asarray(m["max_vort"])))
    if w > 1.0e3:
        return f"max|ω|={w:.3e}"
    em = np.asarray(m["energy"]) + np.asarray(m["e_mag_tot"])
    if float(np.max(em)) > 50.0 * float(em[0] + 1e-30):
        return "energy explosion"
    return None


def _common():
    centres = default_scar_centres(1.0, 4, 3)
    return dict(
        dim=3, N=N, steps=STEPS, dt=DT, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=NU, diag_every=40,
    )


def run_mhd(B0):
    mhd_p = dict(DEFAULT_MHD, freeze_ext=0.0, eta_mag=1e-3, B0=float(B0),
                 eta_odd=0.0, mu_eff=0.0, eta_hyper=0.0,
                 posdiv=0.0, hyper_kcut=0.0)
    print(f"--- MHD ν={NU:.2e}  B0={B0} ---", flush=True)
    m = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                      mhd_params=mhd_p, **_common())
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
    print(f"B0={B0}  dE={drop:.6e}  ∫ε_η={i_eta:.6e}  ∫ε_ν={i_nu:.6e}  "
          f"max|J|={jmax:.3f}  |J|≥½ {100*f_half:.1f}%  "
          f"|J|≥⅛ {100*f_eighth:.1f}%  ‖ω‖={w:.3f}", flush=True)
    return dict(drop=drop, I_eta=i_eta, I_nu=i_nu, jmax=jmax,
                f_half=f_half, f_eighth=f_eighth, w=w, reused=False)


def try_b0(wanted, fallbacks):
    for B0 in (wanted, *fallbacks):
        try:
            row = run_mhd(B0)
        except Exception as exc:
            print(f"B0={B0} FAILED {type(exc).__name__}: {exc}", flush=True)
            row = None
        if row is not None:
            if B0 != wanted:
                print(f"B0={wanted} failed; using nearest stable B0={B0}",
                      flush=True)
            return B0, row
    return wanted, None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = dict(HAVE)
    print(f"hydro reused ν={NU:.2e} drop {HYDRO['drop']:.6e} "
          f"({HYDRO['pct']:.2f}%)", flush=True)

    for wanted, fb in ((0.30, (0.25, 0.20)), (0.40, (0.35, 0.45))):
        B0, row = try_b0(wanted, fb)
        if row is None:
            print(f"no stable B0 near {wanted}", flush=True)
            continue
        rows[B0] = row

    ordered = sorted(rows.items())
    path = OUT / "b0_flip_nu125.csv"
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["B0", "E_drop_hydro", "E_drop_MHD", "MHD_minus_hydro",
                    "int_Ohmic", "int_visc_hydro", "int_visc_MHD",
                    "max_J", "ohmic_frac_half", "ohmic_frac_eighth",
                    "max_vort_MHD", "reused"])
        for B0, r in ordered:
            w.writerow([
                B0, HYDRO["drop"], r["drop"], r["drop"] - HYDRO["drop"],
                r["I_eta"], HYDRO["I_nu"], r["I_nu"],
                r["jmax"], r["f_half"], r["f_eighth"], r["w"],
                r.get("reused", False),
            ])
        w.writerow(["hydro_pct", HYDRO["pct"]])
    print(f"wrote {path}", flush=True)

    valid = abs(HYDRO["pct"] - 1.71) < 0.05 and 0.08 in rows and 0.50 in rows
    print()
    print("VALID" if valid else "INVALID")
    print(f"{'B0':>6} {'E_hy':>11} {'E_MHD':>11} {'MHD-hy':>11} "
          f"{'∫ε_η':>11} {'∫ε_ν hy':>11} {'∫ε_ν MHD':>11} "
          f"{'max|J|':>8} {'%½':>6} {'%⅛':>6}")
    for B0, r in ordered:
        print(f"{B0:6.2f} {HYDRO['drop']:11.4e} {r['drop']:11.4e} "
              f"{r['drop']-HYDRO['drop']:11.4e} {r['I_eta']:11.4e} "
              f"{HYDRO['I_nu']:11.4e} {r['I_nu']:11.4e} "
              f"{r['jmax']:8.2f} {100*r['f_half']:5.1f}% "
              f"{100*r['f_eighth']:5.1f}%")


if __name__ == "__main__":
    main()

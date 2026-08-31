"""Viscosity scan only. Same N=96 twins otherwise. No retune.

    python examples/nu_halo_vs_sheet.py
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from chive_ns import run_framework, DEFAULT_MHD, default_scar_centres
from chive_ns.mhd import current_from_b

DT = 0.0015
STEPS = 240
N = 96
OUT = Path(__file__).resolve().parent / "mhd_n96_nu_scan"

# ν=5e-4 already have (same hydro for both B0).
HAVE_5E4 = {
    "nu": 5.0e-4,
    "hydro": dict(
        drop=4.198410307079917e-03,
        I_nu=4.073760338582395e-03,
        w=37.71638285089682,
        pct=5.96,
    ),
    "mhd": {
        0.08: dict(
            drop=4.613759632526471e-03,
            I_eta=5.802100812816026e-04,
            I_nu=3.919949267936554e-03,
            jmax=24.94811633817377,
            f_half=0.221144,
            f_eighth=0.939641,
            w=34.366620158042245,
        ),
        0.50: dict(
            drop=7.7355929023111e-03,
            I_eta=4.800540690236752e-03,
            I_nu=2.881115744154089e-03,
            jmax=24.204272909339895,
            f_half=0.6015380596828224,
            f_eighth=0.97044161022158,
            w=24.625331523054555,
        ),
    },
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


def _finite(m):
    for k in ("energy", "ohmic", "enstrophy", "max_vort"):
        if k not in m:
            continue
        if not np.isfinite(np.asarray(m[k], dtype=float)).all():
            return False
    if "e_mag_tot" in m:
        if not np.isfinite(np.asarray(m["e_mag_tot"], dtype=float)).all():
            return False
    return True


def _blown(m, magnetic=True):
    if not _finite(m):
        return "nonfinite"
    w = float(np.max(np.asarray(m["max_vort"])))
    if w > 1.0e3:
        return f"max|ω|={w:.3e}"
    e = np.asarray(m["energy"], dtype=float)
    if magnetic:
        e = e + np.asarray(m["e_mag_tot"], dtype=float)
    if float(np.max(e)) > 50.0 * float(e[0] + 1e-30):
        return "energy explosion"
    return None


def _common(nu):
    centres = default_scar_centres(1.0, 4, 3)
    return dict(
        dim=3, N=N, steps=STEPS, dt=DT, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=nu, diag_every=40,
    )


def _mhd_p(B0):
    return dict(DEFAULT_MHD, freeze_ext=0.0, eta_mag=1e-3, B0=float(B0),
                eta_odd=0.0, mu_eff=0.0, eta_hyper=0.0,
                posdiv=0.0, hyper_kcut=0.0)


def run_hydro(nu):
    print(f"--- hydro B=0  ν={nu:.2e} ---", flush=True)
    h = run_framework(mode="vorticity", viscoelastic=False, magnetic=False,
                      **_common(nu))
    why = _blown(h, magnetic=False)
    if why:
        print(f"hydro ν={nu:.2e} UNSTABLE ({why})", flush=True)
        return None
    eh0 = float(h["energy"][0])
    drop = eh0 - float(h["energy"][-1])
    i_nu = _trapz(nu * np.array(h["enstrophy"]), np.array(h["time"]))
    w = float(h["max_vort"][-1])
    pct = 100.0 * drop / eh0
    print(f"hydro ν={nu:.2e}  drop {drop:.6e} ({pct:.2f}%)  "
          f"∫ε_ν {i_nu:.6e}  ‖ω‖ {w:.3f}", flush=True)
    return dict(drop=drop, I_nu=i_nu, w=w, pct=pct, E0=eh0)


def run_mhd(nu, B0):
    print(f"--- MHD ν={nu:.2e}  B0={B0} ---", flush=True)
    m = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                      mhd_params=_mhd_p(B0), **_common(nu))
    why = _blown(m, magnetic=True)
    if why:
        print(f"MHD ν={nu:.2e} B0={B0} UNSTABLE ({why})", flush=True)
        return None
    em0 = float(m["energy"][0] + m["e_mag_tot"][0])
    em1 = float(m["energy"][-1] + m["e_mag_tot"][-1])
    drop = em0 - em1
    i_eta = _trapz(np.array(m["ohmic"]), np.array(m["time"]))
    i_nu = _trapz(nu * np.array(m["enstrophy"]), np.array(m["time"]))
    jmax, f_half, f_eighth = _ohmic_fracs(m)
    w = float(m["max_vort"][-1])
    print(f"MHD ν={nu:.2e} B0={B0}  dE={drop:.6e}  ∫ε_η={i_eta:.6e}  "
          f"∫ε_ν={i_nu:.6e}  max|J|={jmax:.3f}  "
          f"|J|≥½ {100*f_half:.1f}%  |J|≥⅛ {100*f_eighth:.1f}%  "
          f"‖ω‖={w:.3f}", flush=True)
    return dict(drop=drop, I_eta=i_eta, I_nu=i_nu, jmax=jmax,
                f_half=f_half, f_eighth=f_eighth, w=w)


def _try_nu(nu, b0s=(0.08, 0.50)):
    try:
        hydro = run_hydro(nu)
    except Exception as exc:
        print(f"hydro ν={nu:.2e} FAILED {type(exc).__name__}: {exc}", flush=True)
        return None
    if hydro is None:
        return None
    mhd = {}
    for B0 in b0s:
        try:
            row = run_mhd(nu, B0)
        except Exception as exc:
            print(f"MHD ν={nu:.2e} B0={B0} FAILED {type(exc).__name__}: {exc}",
                  flush=True)
            return None
        if row is None:
            return None
        mhd[B0] = row
    return dict(nu=nu, hydro=hydro, mhd=mhd)


def _print_block(blocks, valid, note=""):
    print()
    print("VALID" if valid else "INVALID")
    if note:
        print(note)
    print(f"{'ν':>8} {'B0':>6} {'E_hy':>11} {'E_MHD':>11} {'MHD-hy':>11} "
          f"{'∫ε_η':>11} {'∫ε_ν hy':>11} {'∫ε_ν MHD':>11} "
          f"{'max|J|':>8} {'%½':>6} {'%⅛':>6}")
    for blk in blocks:
        hy = blk["hydro"]
        for B0, r in blk["mhd"].items():
            print(f"{blk['nu']:8.2e} {B0:6.2f} {hy['drop']:11.4e} "
                  f"{r['drop']:11.4e} {r['drop']-hy['drop']:11.4e} "
                  f"{r['I_eta']:11.4e} {hy['I_nu']:11.4e} {r['I_nu']:11.4e} "
                  f"{r['jmax']:8.2f} {100*r['f_half']:5.1f}% "
                  f"{100*r['f_eighth']:5.1f}%")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    blocks = [HAVE_5E4]
    print("ν=5e-4 reused from N=96 B0 scan (same hydro for both B0)", flush=True)

    new = _try_nu(1.25e-4)
    valid = new is not None
    note = ""
    if new is None:
        note = "ν=1.25e-4 unstable; trying ν=2.5e-4"
        print(note, flush=True)
        fb = _try_nu(2.5e-4)
        if fb is not None:
            blocks.append(fb)
            note = "ν=1.25e-4 unstable; table uses ν=2.5e-4 fallback"
        else:
            note = "ν=1.25e-4 and ν=2.5e-4 both unstable"
    else:
        blocks.append(new)

    path = OUT / "nu_scan.csv"
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["nu", "B0", "E_drop_hydro", "E_drop_MHD", "MHD_minus_hydro",
                    "int_Ohmic", "int_visc_hydro", "int_visc_MHD",
                    "max_J", "ohmic_frac_half", "ohmic_frac_eighth",
                    "max_vort_hydro", "max_vort_MHD"])
        for blk in blocks:
            hy = blk["hydro"]
            for B0, r in blk["mhd"].items():
                w.writerow([
                    blk["nu"], B0, hy["drop"], r["drop"], r["drop"] - hy["drop"],
                    r["I_eta"], hy["I_nu"], r["I_nu"],
                    r["jmax"], r["f_half"], r["f_eighth"],
                    hy["w"], r["w"],
                ])
    print(f"wrote {path}", flush=True)
    _print_block(blocks, valid, note)


if __name__ == "__main__":
    main()

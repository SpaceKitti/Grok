"""Shen et al. 2025 paper Ni: co-located flux tubes. No fake Ni.

    python examples/shen_ni_regimes.py
"""

import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from chive_ns import (
    run_framework, DEFAULT_MHD, paper_ni_ic, paper_sigma_c, current_from_b,
)

NU = 5e-4
ETA = 1e-3
DT = 0.0015
STEPS = 400          # t = 0.60
N = 96
R = 0.08
GAMMA = 0.7
OUT = Path(__file__).resolve().parent / "mhd_n96_shen_ni"

# Ni = Γ_m² / (Γ η σ_c²),  σ_c = R/√2  (Shen 2025 eq. 2.11)
# Target ~16 (low 10–20) and ~144 (moderate 100–200).
SIG_C = paper_sigma_c(R)


def gamma_m_for_ni(ni):
    return math.sqrt(float(ni) * GAMMA * ETA * SIG_C * SIG_C)


GM_LOW = gamma_m_for_ni(16.0)
GM_MOD = gamma_m_for_ni(144.0)


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


def _blown(m, magnetic=True):
    keys = ("energy", "enstrophy", "max_vort")
    if magnetic:
        keys = keys + ("e_mag_tot", "ohmic", "ni_paper")
    for k in keys:
        if k not in m:
            continue
        if not np.isfinite(np.asarray(m[k], dtype=float)).all():
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


def _common():
    return dict(
        dim=3, N=N, steps=STEPS, dt=DT, ic="tubes", scheme="rk2",
        force_on=False, n_scars=1, force_amp=0.0,
        nu=NU, diag_every=40,
        ic_params=dict(circulation=GAMMA, radius=R, separation=0.24,
                       perturbation=0.04, axial_wave=1),
    )


def _mhd_p(gamma_m):
    return dict(DEFAULT_MHD, freeze_ext=0.0, eta_mag=ETA, B0=0.0,
                b_guide="flux", gamma_m=float(gamma_m),
                eta_odd=0.0, mu_eff=0.0, eta_hyper=0.0,
                posdiv=0.0, hyper_kcut=0.0,
                tube_radius=R, tube_circulation=GAMMA)


def _regime(m, h):
    """Pick one of Shen's three regimes from what the twins actually did."""
    em0 = float(m["e_mag_tot"][0]) + 1e-30
    em1 = float(m["e_mag_tot"][-1])
    mag_ratio = em1 / em0
    wh = float(h["max_vort"][-1]) + 1e-30
    wm = float(m["max_vort"][-1])
    vort_ratio = wm / wh
    ni0 = float(m["ni_paper0"][0])
    # Paper: low Ni → joint reconnection + dynamo (E_mag grows, Crow lives).
    # moderate → cascade / secondary filaments (ω not killed, mag not a dynamo).
    # high → Lorentz disruption (ω crushed, mag→kin).
    if vort_ratio < 0.55 and mag_ratio < 0.7:
        name = "disruption"
        why = (f"‖ω‖_MHD/‖ω‖_hy={vort_ratio:.2f} and E_mag×{mag_ratio:.2f}: "
               "Lorentz ripped the cores / converted mag→kin")
    elif mag_ratio > 1.05 and vort_ratio > 0.7:
        name = "reconnection"
        why = (f"E_mag×{mag_ratio:.2f} (dynamo) and Crow ω survives "
               f"({vort_ratio:.2f}): vortex-dominated joint reconnection")
    else:
        name = "cascade"
        why = (f"E_mag×{mag_ratio:.2f}, ω ratio {vort_ratio:.2f}, Ni0={ni0:.1f}: "
               "neither clean dynamo-Crow nor core disruption")
    return name, why, mag_ratio, vort_ratio


def run_hydro():
    print("--- hydro Γ_m=0 ---", flush=True)
    h = run_framework(mode="vorticity", viscoelastic=False, magnetic=False,
                      **_common())
    why = _blown(h, magnetic=False)
    if why:
        print(f"hydro UNSTABLE ({why})", flush=True)
        return None
    eh0 = float(h["energy"][0])
    drop = eh0 - float(h["energy"][-1])
    i_nu = _trapz(NU * np.array(h["enstrophy"]), np.array(h["time"]))
    print(f"hydro drop {drop:.6e} ({100*drop/eh0:.2f}%)  ∫ε_ν {i_nu:.6e}  "
          f"‖ω‖ {float(h['max_vort'][-1]):.3f}  t={float(h['time'][-1]):.3f}",
          flush=True)
    return dict(out=h, drop=drop, I_nu=i_nu, E0=eh0, pct=100.0 * drop / eh0)


def run_mhd(gamma_m, label):
    ni0 = paper_ni_ic(GAMMA, gamma_m, ETA, R)
    print(f"--- MHD {label}  Γ_m={gamma_m:.6f}  Ni0={ni0:.2f} ---", flush=True)
    m = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                      mhd_params=_mhd_p(gamma_m), **_common())
    why = _blown(m, magnetic=True)
    if why:
        print(f"{label} UNSTABLE ({why})", flush=True)
        return None
    em0 = float(m["energy"][0] + m["e_mag_tot"][0])
    em1 = float(m["energy"][-1] + m["e_mag_tot"][-1])
    drop = em0 - em1
    i_eta = _trapz(np.array(m["ohmic"]), np.array(m["time"]))
    i_nu = _trapz(NU * np.array(m["enstrophy"]), np.array(m["time"]))
    jmax, f_half, f_eighth = _ohmic_fracs(m)
    print(f"{label}  dE={drop:.6e}  ∫ε_η={i_eta:.6e}  ∫ε_ν={i_nu:.6e}  "
          f"Ni0={float(m['ni_paper0'][0]):.2f}  "
          f"Ni_end={float(m['ni_paper'][-1]):.2f}  "
          f"E_mag/E_kin={float(m['N_i'][-1]):.3f}  "
          f"|J|≥½ {100*f_half:.1f}%  |J|≥⅛ {100*f_eighth:.1f}%",
          flush=True)
    return dict(out=m, drop=drop, I_eta=i_eta, I_nu=i_nu, jmax=jmax,
                f_half=f_half, f_eighth=f_eighth, gamma_m=gamma_m,
                ni0=ni0, label=label)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Shen et al. 2025 eq. (2.11):")
    print("  Ni = Γ_m² / (Γ η σ_c²)")
    print(f"  Γ     = {GAMMA}     vortex circulation of one Crow tube")
    print(f"  Γ_m   = magnetic flux of the co-located tube")
    print(f"  η     = {ETA}   magnetic diffusivity (eta_mag)")
    print(f"  R     = {R}    Gaussian radius in exp(−r²/R²)")
    print(f"  σ_c   = R/√2 = {SIG_C:.6f}   paper tube thickness ℓ")
    print(f"  ρ     = 1,  μ = 1,  σ_elec = 1/η")
    print(f"  ℓ     = σ_c  (their characteristic length)")
    print(f"  Ni(t) uses Γ(t)=max|ω| π R², Γ_m(t)=max|B| π R², same σ_c")
    print(f"  t_end = {STEPS*DT:.3f}  (dt={DT}, N={N}, force off)")
    print(f"  Γ_m(low)={GM_LOW:.6f} → Ni0={paper_ni_ic(GAMMA, GM_LOW, ETA, R):.2f}")
    print(f"  Γ_m(mod)={GM_MOD:.6f} → Ni0={paper_ni_ic(GAMMA, GM_MOD, ETA, R):.2f}")
    print(flush=True)

    hydro = run_hydro()
    if hydro is None:
        print("CANNOT_IC" if False else "INVALID")
        print("hydro twin unstable")
        return

    cases = []
    for gm, lab in ((GM_LOW, "low"), (GM_MOD, "moderate")):
        try:
            row = run_mhd(gm, lab)
        except Exception as exc:
            print(f"{lab} FAILED {type(exc).__name__}: {exc}", flush=True)
            row = None
        if row is None:
            print(f"{lab} Ni0={paper_ni_ic(GAMMA, gm, ETA, R):.1f} unstable",
                  flush=True)
            continue
        cases.append(row)

    if not cases:
        print("INVALID")
        print("no stable flux-tube MHD run")
        return

    path = OUT / "shen_ni_regimes.csv"
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["label", "gamma_m", "ni0_ic", "ni_start_hist", "ni_end",
                    "E_mag_over_E_kin_end", "E_drop_hydro", "E_drop_MHD",
                    "MHD_minus_hydro", "int_Ohmic", "int_visc_hydro",
                    "int_visc_MHD", "max_J", "ohmic_frac_half",
                    "ohmic_frac_eighth", "regime"])
        for c in cases:
            m = c["out"]
            name, why, _, _ = _regime(m, hydro["out"])
            w.writerow([
                c["label"], c["gamma_m"], c["ni0"],
                float(m["ni_paper"][0]), float(m["ni_paper"][-1]),
                float(m["N_i"][-1]), hydro["drop"], c["drop"],
                c["drop"] - hydro["drop"], c["I_eta"], hydro["I_nu"],
                c["I_nu"], c["jmax"], c["f_half"], c["f_eighth"], name,
            ])
            c["regime"] = name
            c["why"] = why
    print(f"wrote {path}", flush=True)

    print()
    print("VALID")
    print(f"t={STEPS*DT:.3f}  N={N}  ν={NU}  η={ETA}  force off  "
          f"hydro drop {hydro['pct']:.2f}%")
    print(f"{'case':<10} {'Ni0':>8} {'Ni_end':>8} {'Em/Ek':>8} "
          f"{'MHD-hy':>11} {'%½':>6} {'%⅛':>6} {'regime':<14}")
    for c in cases:
        m = c["out"]
        print(f"{c['label']:<10} {float(m['ni_paper0'][0]):8.2f} "
              f"{float(m['ni_paper'][-1]):8.2f} {float(m['N_i'][-1]):8.3f} "
              f"{c['drop']-hydro['drop']:11.4e} {100*c['f_half']:5.1f}% "
              f"{100*c['f_eighth']:5.1f}% {c['regime']:<14}")
        print(f"           {c['why']}")


if __name__ == "__main__":
    main()

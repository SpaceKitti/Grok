"""Ohmic split on better masks. Same twins. No retune.

    python examples/ohmic_mask_split.py          # N=48
    python examples/ohmic_mask_split.py 96       # N=96 if it fits
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


def _trapz(y, t):
    y, t = np.asarray(y), np.asarray(t)
    if y.shape[0] < 2:
        return 0.0
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])))


def _frac(j2, mask):
    tot = float(np.sum(j2)) + 1e-30
    m = np.broadcast_to(np.asarray(mask, dtype=bool), j2.shape)
    n = int(np.sum(m))
    f = float(np.sum(j2 * m)) / tot
    return n, f


def _dilate_chebyshev(mask, r):
    """Periodic max-norm ball of radius r (r-cell neighborhood)."""
    out = np.zeros_like(mask, dtype=bool)
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            for dz in range(-r, r + 1):
                out |= np.roll(np.roll(np.roll(mask, dx, 0), dy, 1), dz, 2)
    return out


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 48
    out_dir = Path(__file__).resolve().parent / f"mhd_n{N}_mhd_minus_hydro"
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=N, steps=STEPS, dt=DT, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=NU, diag_every=40,
    )
    mhd_p = dict(DEFAULT_MHD, freeze_ext=0.0, eta_mag=1e-3,
                 eta_odd=0.0, mu_eff=0.0, eta_hyper=0.0,
                 posdiv=0.0, hyper_kcut=0.0)

    print("--- 1 MHD Crow-pair (Campaign A) ---", flush=True)
    m = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                      mhd_params=mhd_p, **common)
    print("--- 2 hydro Crow-pair B=0 ---", flush=True)
    h = run_framework(mode="vorticity", viscoelastic=False, magnetic=False,
                      **common)

    em0 = float(m["energy"][0] + m["e_mag_tot"][0])
    em1 = float(m["energy"][-1] + m["e_mag_tot"][-1])
    drop_mhd = em0 - em1
    eh0 = float(h["energy"][0])
    eh1 = float(h["energy"][-1])
    drop_hy = eh0 - eh1
    diff = drop_mhd - drop_hy

    I_eta = _trapz(np.array(m["ohmic"]), np.array(m["time"]))
    I_nu_m = _trapz(NU * np.array(m["enstrophy"]), np.array(m["time"]))
    I_nu_h = _trapz(NU * np.array(h["enstrophy"]), np.array(h["time"]))
    w_h = float(h["max_vort"][-1])
    w_m = float(m["max_vort"][-1])
    z_h = float(h["enstrophy"][-1])
    z_m = float(m["enstrophy"][-1])

    J_hat = np.array(current_from_b(m["B_hat"], m["grid"]))
    J = np.fft.ifftn(J_hat, axes=(1, 2, 3)).real
    j2 = np.sum(J**2, axis=0)
    jmag = np.sqrt(j2)
    jmax = float(jmag.max())
    N = int(m["grid"]["N"])
    mid = N // 2
    # indexing='ij': axis 0 = x (along tubes), 1 = y (separation), 2 = z
    iy = np.arange(N)[None, :, None]
    iz = np.arange(N)[None, None, :]
    sheet_half = jmag >= 0.5 * jmax

    masks = [
        ("|J|>=1/2 max", sheet_half),
        ("|J|>=1/4 max", jmag >= 0.25 * jmax),
        ("|J|>=1/8 max", jmag >= 0.125 * jmax),
        ("midplane y +/-2", np.abs(iy - mid) <= 2),
        ("midplane y +/-3", np.abs(iy - mid) <= 3),
        ("midplane yz +/-3", (np.abs(iy - mid) <= 3) & (np.abs(iz - mid) <= 3)),
        ("sheet +/-2 cells", _dilate_chebyshev(sheet_half, 2)),
        ("sheet +/-3 cells", _dilate_chebyshev(sheet_half, 3)),
    ]
    nall = int(j2.size)

    print()
    print(f"========== twins (N={N}, t=0.36, no retune) ==========")
    print(f"E drop hydro     {drop_hy:.6e}   ({100.0 * drop_hy / eh0:.2f}% of E_hydro(0))")
    print(f"E drop MHD       {drop_mhd:.6e}   ({100.0 * drop_mhd / em0:.2f}% of E_MHD_tot(0))")
    print(f"MHD − hydro      {diff:.6e}   ({100.0 * diff / eh0:.2f}% of E_hydro(0))")
    print(f"∫ ε_η            {I_eta:.6e}")
    print()
    print("========== viscous dissipation (ν⟨ω²⟩) ==========")
    print(f"∫ ε_ν  hydro     {I_nu_h:.6e}    ‖ω‖_end {w_h:.3f}    ⟨ω²⟩_end {z_h:.4e}    ε_ν(end) {NU * z_h:.4e}")
    print(f"∫ ε_ν  MHD       {I_nu_m:.6e}    ‖ω‖_end {w_m:.3f}    ⟨ω²⟩_end {z_m:.4e}    ε_ν(end) {NU * z_m:.4e}")
    print(f"MHD − hydro visc {I_nu_m - I_nu_h:.6e}   (negative = Crow suppression)")
    print(f"Ohmic + Δvisc    {I_eta + (I_nu_m - I_nu_h):.6e}   vs MHD−hydro {diff:.6e}")
    print()
    print(f"max|J|={jmax:.4f}   N={N}   cells={nall}   "
          f"mid y=z=index {mid}")
    print()
    print("MHD−hydro is a global twin difference, not a spatial field.")
    print("Ohmic/Δ = (mask share of ∫ε_η) / (MHD−hydro); proxy only.")
    print()
    print(f"{'mask':<22} {'cells':>8} {'% vol':>8} {'% ∫ε_η':>8} "
          f"{'Ohmic/Δ':>9}")
    rows = []
    for name, mask in masks:
        n, f = _frac(j2, mask)
        vs_diff = (f * I_eta) / diff if diff else 0.0
        print(f"{name:<22} {n:8d} {100.0 * n / nall:7.2f}% {100.0 * f:7.1f}% "
              f"{vs_diff:9.2f}")
        rows.append((name, n, n / nall, f, vs_diff))

    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "ohmic_masks.csv"
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["mask", "cells", "vol_frac", "ohmic_frac",
                    "ohmic_in_mask_over_MHDminus_hydro"])
        for name, n, vf, f, vd in rows:
            w.writerow([name, n, f"{vf:.6f}", f"{f:.6f}", f"{vd:.4f}"])
        w.writerow(["int_Ohmic", I_eta])
        w.writerow(["int_visc_hydro", I_nu_h])
        w.writerow(["int_visc_MHD", I_nu_m])
        w.writerow(["E_drop_hydro", drop_hy])
        w.writerow(["E_drop_MHD", drop_mhd])
        w.writerow(["MHD_minus_hydro", diff])
        w.writerow(["max_vort_hydro", w_h])
        w.writerow(["max_vort_MHD", w_m])
        w.writerow(["max_J", jmax])
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()

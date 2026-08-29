"""NS+MHD residual-dissipation run: measure the MHD2/02 6–8% ΔE_tot band.

Quote (MHD2/02, Crow tubes + 4-scar, N=48, t=0.36):

    ΔE_tot(t) = 1 - E_tot(t) / E_tot(0)
    E_tot     = E_kin + E_mag
    E_kin     = (1/2) < |u|^2 >
    E_mag     = (1/2) < |B|^2 >

    NS + MHD (b_guide="z", η=1e-3, B0=0.08, viscoelastic=False):
        ΔE_tot(0.36) = 6.26%
        most kinetic loss is stored as E_mag
    Hybrid + MHD (same magnetic dials): ΔE_tot = 8.57%
    NS (no B): ΔE_tot = 5.95%

That 6–8% band is measured TOTAL energy loss, not the polymer residual
diagnostics in MHD/01 (D1, D2, D3, E_AN, T_*). MHD/01's magnetic counterpart
is the Ohmic sink η <|J|^2> plus late-time residual Lorentz work; this script
integrates Ohmic and reports max|J| / max|div B| so you can see whether a
6–8% ΔE_tot is viscous+Ohmic or a low-N sheet artifact (MHD2/02 open Q).

This run: mode="mhd", viscoelastic=False, note defaults, N=32 (start; notes
used N=48), t_end=0.36 (not the old t=0.08 smoke).

    python examples/mhd_dissipation.py
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from chive_ns import run_framework

# MHD2/02 table target (do not treat as settled physics).
T_NOTE = 0.36
BAND_LO, BAND_HI = 6.0, 8.0  # percent ΔE_tot
NOTE_N = 48
NOTE_NS_MHD_PCT = 6.26
NOTE_HYBRID_PCT = 8.57

# Safe default from MHD2/02 for low-residual Crow suppression.
MHD_PARAMS = dict(eta=1e-3, B0=0.08, b_guide="z")


def _running_trapz(y: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Running trapezoidal integral; out[0] = 0."""
    y = np.asarray(y, dtype=float)
    t = np.asarray(t, dtype=float)
    out = np.zeros_like(y)
    if y.size < 2:
        return out
    pieces = 0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])
    out[1:] = np.cumsum(pieces)
    return out


def _interp_at(t: np.ndarray, y: np.ndarray, t_query: float) -> float:
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    if t.size == 0:
        return float("nan")
    if t_query <= t[0]:
        return float(y[0])
    if t_query >= t[-1]:
        return float(y[-1])
    return float(np.interp(t_query, t, y))


def _verdict(t, pct_tot, max_J, max_divB, ohmic_int, n, t_end):
    """HIT / MISS / TOO EARLY / LOW-N ARTIFACT plus a one-line why."""
    t = np.asarray(t, dtype=float)
    pct_tot = np.asarray(pct_tot, dtype=float)
    t_final = float(t[-1]) if t.size else 0.0
    pct_at_note = _interp_at(t, pct_tot, T_NOTE)
    pct_final = float(pct_tot[-1]) if pct_tot.size else float("nan")
    j_final = float(max_J[-1]) if len(max_J) else float("nan")
    j_peak = float(np.max(max_J)) if len(max_J) else float("nan")
    divb_peak = float(np.max(np.abs(max_divB))) if len(max_divB) else float("nan")
    ohm_end = float(ohmic_int[-1]) if len(ohmic_int) else 0.0

    in_band = BAND_LO <= pct_at_note <= BAND_HI

    if t_final < 0.90 * T_NOTE:
        return (
            "TOO EARLY",
            f"t_end={t_final:.3f} < MHD2/02 t={T_NOTE} so ΔE_tot={pct_final:.2f}% "
            f"is not comparable to the 6–8% table yet",
        )

    # Spectral projection should keep div B ~ roundoff. Anything much larger
    # is a solver leak, not the physical 6–8%.
    if not np.isfinite(divb_peak) or divb_peak > 1e-6:
        return (
            "LOW-N ARTIFACT",
            f"max|div B|={divb_peak:.2e} (expect ~1e-15); ΔE_tot is not a clean energy budget",
        )

    # MHD2/02 open Q: late Ohmic ramps may be under-resolved sheets.
    # Notes used N=48 and asked for N=64/96. At N=32 a late |J| spike plus a
    # miss of the band is treated as resolution, not a physics miss.
    late = t >= (0.7 * T_NOTE)
    j_late = float(np.max(max_J[late])) if np.any(late) else j_peak
    j_early = float(np.max(max_J[~late])) if np.any(~late) else j_peak
    ohmic_ramp = np.isfinite(j_late) and np.isfinite(j_early) and j_late > 3.0 * max(j_early, 1e-12)

    if in_band:
        extra = ""
        if n < NOTE_N:
            extra = (
                f" (N={n} < note N={NOTE_N}; treat as a hit on this grid, "
                f"not a confirmation of the N=48 table)"
            )
        return (
            "HIT",
            f"ΔE_tot({T_NOTE})={pct_at_note:.2f}% sits in [{BAND_LO:g}, {BAND_HI:g}]% "
            f"(note NS+MHD {NOTE_NS_MHD_PCT:g}%, hybrid {NOTE_HYBRID_PCT:g}%)"
            + extra,
        )

    if n < NOTE_N and ohmic_ramp:
        return (
            "LOW-N ARTIFACT",
            f"ΔE_tot({T_NOTE})={pct_at_note:.2f}% outside 6–8%, but N={n} "
            f"(notes used {NOTE_N}) and late max|J| spiked {j_early:.3g} → {j_late:.3g} "
            f"(∫Ohmic={ohm_end:.3e}); MHD2/02 flagged this as possible sheet under-resolution",
        )

    if n < NOTE_N:
        return (
            "MISS",
            f"ΔE_tot({T_NOTE})={pct_at_note:.2f}% outside [{BAND_LO:g}, {BAND_HI:g}]% "
            f"at N={n} (notes used N={NOTE_N}). Not an Ohmic-ramp artifact by the |J| test; "
            f"rerun at N={NOTE_N} before treating as physics",
        )

    return (
        "MISS",
        f"reached t={t_final:.3f} at N={n} with ΔE_tot({T_NOTE})={pct_at_note:.2f}% "
        f"outside [{BAND_LO:g}, {BAND_HI:g}]% (peak max|J|={j_peak:.3g}, ∫Ohmic={ohm_end:.3e})",
    )


def _write_csv(path: Path, t, e_kin, e_mag, e_tot, pct_kin, pct_tot,
               ohmic, ohmic_int, max_J, max_divB):
    fields = [
        "t", "E_kin", "Emag", "E_tot",
        "pct_loss_E_kin", "pct_loss_E_tot",
        "ohmic", "ohmic_integrated", "max_J", "max_divB",
    ]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i in range(len(t)):
            w.writerow({
                "t": float(t[i]),
                "E_kin": float(e_kin[i]),
                "Emag": float(e_mag[i]),
                "E_tot": float(e_tot[i]),
                "pct_loss_E_kin": float(pct_kin[i]),
                "pct_loss_E_tot": float(pct_tot[i]),
                "ohmic": float(ohmic[i]),
                "ohmic_integrated": float(ohmic_int[i]),
                "max_J": float(max_J[i]),
                "max_divB": float(max_divB[i]),
            })


def _write_png(path: Path, t, e_kin, e_mag, e_tot, pct_kin, pct_tot,
               ohmic_int, max_J, max_divB, n, verdict):
    t = np.asarray(t, dtype=float)
    fig, axes = plt.subplots(4, 1, sharex=True, figsize=(7.5, 9.0))

    axes[0].plot(t, e_kin, label="E_kin", color="C0")
    axes[0].plot(t, e_mag, label="Emag", color="C3")
    axes[0].plot(t, e_tot, label="E_tot", color="k")
    axes[0].set_ylabel("energy")
    axes[0].legend(loc="best", fontsize=8)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t, pct_kin, label="% loss E_kin", color="C0")
    axes[1].plot(t, pct_tot, label="% loss E_tot", color="k")
    axes[1].axhline(BAND_LO, color="0.5", ls="--", lw=0.8)
    axes[1].axhline(BAND_HI, color="0.5", ls="--", lw=0.8, label="6–8% band")
    axes[1].axvline(T_NOTE, color="C1", ls=":", lw=0.8, label=f"t={T_NOTE}")
    axes[1].set_ylabel("% loss vs t=0")
    axes[1].legend(loc="best", fontsize=8)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(t, ohmic_int, color="C4", label="integrated Ohmic")
    axes[2].set_ylabel("∫ η <|J|^2> dt")
    axes[2].legend(loc="best", fontsize=8)
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(t, max_J, color="C2", label="max|J|")
    axes[3].plot(t, max_divB, color="C5", label="max|div B|")
    axes[3].set_ylabel("magnetic")
    axes[3].set_xlabel("t")
    axes[3].legend(loc="best", fontsize=8)
    axes[3].grid(True, alpha=0.3)

    fig.suptitle(
        f"MHD dissipation  N={n}  t_end={float(t[-1]):.3f}  {verdict}"
    )
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main(argv=None):
    p = argparse.ArgumentParser(description="MHD2/02 6–8% ΔE_tot dissipation check")
    p.add_argument("--N", type=int, default=32, help="spectral resolution (default 32)")
    p.add_argument("--t-end", type=float, default=T_NOTE,
                   help=f"physical end time (default {T_NOTE}, MHD2/02 table)")
    p.add_argument("--dt", type=float, default=0.002,
                   help="timestep (default 0.002, same as MHD smoke)")
    p.add_argument("--diag-every", type=int, default=20)
    p.add_argument("--outdir", type=str, default=None)
    args = p.parse_args(argv)

    t_end = float(args.t_end)
    dt = float(args.dt)
    steps = max(int(round(t_end / dt)), 1)
    n = int(args.N)

    outdir = Path(args.outdir) if args.outdir else Path(__file__).resolve().parent
    outdir.mkdir(parents=True, exist_ok=True)

    print(
        f"MHD dissipation: mode=mhd  N={n}  t_end={t_end}  dt={dt}  "
        f"steps={steps}  eta={MHD_PARAMS['eta']}  B0={MHD_PARAMS['B0']}  "
        f"b_guide={MHD_PARAMS['b_guide']!r}  ic=tubes  n_scars=4"
    )
    print("Compiling / running (first JAX compile is slow) ...")

    out = run_framework(
        mode="mhd",
        viscoelastic=False,
        dim=3,
        N=n,
        steps=steps,
        dt=dt,
        ic="tubes",
        scheme="rk2",
        force_on=True,
        n_scars=4,
        diag_every=int(args.diag_every),
        nu=5e-4,
        mhd_params=dict(MHD_PARAMS),
    )

    t = np.asarray(out["time"], dtype=float)
    e_kin = np.asarray(out["energy"], dtype=float)
    e_mag = np.asarray(out["mag_energy"], dtype=float)
    e_tot = e_kin + e_mag
    e_kin0 = float(e_kin[0]) if e_kin.size else 0.0
    e_tot0 = float(e_tot[0]) if e_tot.size else 0.0
    pct_kin = 100.0 * (1.0 - e_kin / (e_kin0 + 1e-30))
    pct_tot = 100.0 * (1.0 - e_tot / (e_tot0 + 1e-30))
    ohmic = np.asarray(out["ohmic"], dtype=float)  # η < |J|^2 >  (instantaneous)
    ohmic_int = _running_trapz(ohmic, t)
    max_J = np.asarray(out["max_J"], dtype=float)
    max_divB = np.asarray(out["max_divB"], dtype=float)

    print()
    print(f"{'t':>7}  {'E_kin':>10} {'Emag':>10} {'E_tot':>10}  "
          f"{'dEkin%':>8} {'dEtot%':>8}  {'∫Ohmic':>10}  {'max|J|':>9} {'max|divB|':>10}")
    for i in range(len(t)):
        print(
            f"{t[i]:7.3f}  "
            f"{e_kin[i]:10.4e} {e_mag[i]:10.4e} {e_tot[i]:10.4e}  "
            f"{pct_kin[i]:8.3f} {pct_tot[i]:8.3f}  "
            f"{ohmic_int[i]:10.4e}  "
            f"{max_J[i]:9.4e} {max_divB[i]:10.3e}"
        )

    label, why = _verdict(t, pct_tot, max_J, max_divB, ohmic_int, n, t_end)
    pct_note = _interp_at(t, pct_tot, T_NOTE)
    pct_kin_note = _interp_at(t, pct_kin, T_NOTE)

    csv_path = outdir / "mhd_dissipation.csv"
    png_path = outdir / "mhd_dissipation.png"
    _write_csv(csv_path, t, e_kin, e_mag, e_tot, pct_kin, pct_tot,
               ohmic, ohmic_int, max_J, max_divB)
    _write_png(png_path, t, e_kin, e_mag, e_tot, pct_kin, pct_tot,
               ohmic_int, max_J, max_divB, n, label)

    print()
    print(f"wrote {csv_path}")
    print(f"wrote {png_path}")
    print(
        f"at t={T_NOTE}: ΔE_kin={pct_kin_note:.2f}%  ΔE_tot={pct_note:.2f}%  "
        f"(∫Ohmic={float(ohmic_int[-1]):.4e}, peak max|J|={float(np.max(max_J)):.4e})"
    )
    print(f"6–8% check: {label} / {why}")
    return out


if __name__ == "__main__":
    main()

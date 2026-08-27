"""Short viz smoke: run a tiny case, save CSV + PNG of key monitors.

Produces (in the working directory, usually repo root / examples/):
  - smoke_monitors.csv
  - smoke_monitors.png

Modes:
  python examples/smoke_plot.py            # NS tubes N=32
  python examples/smoke_plot.py --mhd      # MHD tubes N=32
  python examples/interactive_toy.py       # same entry point
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

# Headless-friendly backend before pyplot import.
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from chive_ns import run_framework


def _run(mhd: bool):
    common = dict(dim=3, N=32, steps=30, ic="tubes", scheme="rk2",
                  force_on=False, diag_every=10, nu=5e-4, dt=0.002)
    if mhd:
        return run_framework(
            mode="mhd", viscoelastic=False,
            mhd_params=dict(eta=1e-3, B0=0.08, b_guide="z"), **common)
    return run_framework(mode="vorticity", viscoelastic=False, **common)


def _write_csv(path: Path, out: dict, mhd: bool):
    fields = ["t", "energy", "max_vort", "bkm_integral"]
    if mhd:
        fields += ["mag_energy", "max_J", "max_divB"]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i in range(len(out["energy"])):
            row = {
                "t": float(out["time"][i]),
                "energy": float(out["energy"][i]),
                "max_vort": float(out["max_vort"][i]),
                "bkm_integral": float(out["bkm_integral"][i]),
            }
            if mhd:
                row["mag_energy"] = float(out["mag_energy"][i])
                row["max_J"] = float(out["max_J"][i])
                row["max_divB"] = float(out["max_divB"][i])
            w.writerow(row)


def _write_png(path: Path, out: dict, mhd: bool):
    t = np.asarray(out["time"], dtype=float)
    n = 3 if mhd else 2
    fig, axes = plt.subplots(n, 1, sharex=True, figsize=(7.0, 2.2 * n))
    if n == 2:
        axes = list(axes)

    axes[0].plot(t, np.asarray(out["energy"], dtype=float), label="E_kin", color="C0")
    if mhd:
        axes[0].plot(t, np.asarray(out["mag_energy"], dtype=float),
                     label="E_mag", color="C3")
    axes[0].set_ylabel("energy")
    axes[0].legend(loc="best", fontsize=8)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t, np.asarray(out["max_vort"], dtype=float), color="C1", label="max|w|")
    axes[1].plot(t, np.asarray(out["bkm_integral"], dtype=float), color="C2",
                 label="BKM integral max|w|")
    axes[1].set_ylabel("vorticity")
    axes[1].legend(loc="best", fontsize=8)
    axes[1].grid(True, alpha=0.3)

    if mhd:
        axes[2].plot(t, np.asarray(out["max_J"], dtype=float), color="C4", label="max|J|")
        axes[2].plot(t, np.asarray(out["max_divB"], dtype=float), color="C5",
                     label="max|div B|")
        axes[2].set_ylabel("magnetic")
        axes[2].legend(loc="best", fontsize=8)
        axes[2].grid(True, alpha=0.3)

    axes[-1].set_xlabel("t")
    title = "MHD smoke" if mhd else "NS smoke"
    fig.suptitle(f"{title}  N={out['N']}  ic={out['ic']}  mode={out['mode']}")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main(argv=None):
    p = argparse.ArgumentParser(description="C*Hive viz smoke (CSV + PNG)")
    p.add_argument("--mhd", action="store_true", help="run mode=mhd instead of NS")
    p.add_argument("--outdir", type=str, default=None,
                   help="directory for CSV/PNG (default: this script's folder)")
    args = p.parse_args(argv)

    outdir = Path(args.outdir) if args.outdir else Path(__file__).resolve().parent
    outdir.mkdir(parents=True, exist_ok=True)

    label = "MHD" if args.mhd else "NS"
    print(f"Compiling / running {label} smoke (N=32, steps=30) ...")
    out = _run(args.mhd)

    csv_path = outdir / "smoke_monitors.csv"
    png_path = outdir / "smoke_monitors.png"
    _write_csv(csv_path, out, args.mhd)
    _write_png(png_path, out, args.mhd)

    print(f"wrote {csv_path}")
    print(f"wrote {png_path}")
    print(f"final E={float(out['energy'][-1]):.4e}  "
          f"max|w|={float(out['max_vort'][-1]):.4e}  "
          f"BKM={float(out['bkm_integral'][-1]):.4e}")
    if args.mhd:
        print(f"final Emag={float(out['mag_energy'][-1]):.4e}  "
              f"max|J|={float(out['max_J'][-1]):.4e}  "
              f"max|divB|={float(out['max_divB'].max()):.3e}")
    return out


if __name__ == "__main__":
    main()

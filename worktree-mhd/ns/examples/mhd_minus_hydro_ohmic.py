"""MHD−hydro residual vs Ohmic location. Same twins as last pair.

Hydro numbers from twin_hydro_mhd_drop.py (identical kwargs).
MHD is re-run only to get end-state J for the sheet mask.

    python examples/mhd_minus_hydro_ohmic.py
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from chive_ns import run_framework, DEFAULT_MHD, default_scar_centres
from chive_ns.grid import ik_cross

OUT = Path(__file__).resolve().parent / "mhd_n48_mhd_minus_hydro"

# Last twin (Crow+4-scar N=48 t=0.36, same ν, dt, grid)
DROP_HY = 4.193588e-03
DROP_MHD = 4.607887e-03
E_HY0 = 7.042472e-02
DIFF = DROP_MHD - DROP_HY


def _trapz(y, t):
    y, t = np.asarray(y), np.asarray(t)
    if y.shape[0] < 2:
        return 0.0
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])))


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

    print("--- MHD Campaign A (fields for Ohmic mask) ---", flush=True)
    m = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                      mhd_params=mhd, **common)
    eta = 1e-3
    I_eta = _trapz(np.array(m["ohmic"]), np.array(m["time"]))
    B_hat = m["B_hat"]
    grid = m["grid"]
    J = np.fft.ifftn(np.array(ik_cross(B_hat, grid)), axes=(1, 2, 3)).real
    j2 = np.sum(J**2, axis=0)
    jmag = np.sqrt(j2)
    sheets = jmag >= 0.5 * float(jmag.max())
    tubes = ~sheets
    tot = float(np.sum(j2)) + 1e-30
    frac_s = float(np.sum(j2 * sheets)) / tot
    frac_t = float(np.sum(j2 * tubes)) / tot
    n_s = int(sheets.sum())
    n_all = j2.size
    ohm_end = eta * float(np.mean(j2))
    ohm_s = eta * float(np.mean(j2 * sheets))
    ohm_t = eta * float(np.mean(j2 * tubes))

    diff = DIFF
    eh0 = E_HY0
    print()
    print(f"E drop hydro     {DROP_HY:.6e}   ({100.0 * DROP_HY / eh0:.2f}%)")
    print(f"E drop MHD       {DROP_MHD:.6e}   ({100.0 * DROP_MHD / (DROP_MHD + float(m['energy'][-1] + m['e_mag_tot'][-1])):.2f}%)")
    # MHD tot 0 is DROP_MHD + E_end; use last twin em0
    em0 = DROP_MHD + float(m["energy"][-1] + m["e_mag_tot"][-1])
    print(f"MHD − hydro      {diff:.6e}   ({100.0 * diff / eh0:.2f}% of E_hydro(0))")
    print(f"∫ ε_η (Ohmic)    {I_eta:.6e}")
    print(f"Ohmic in sheets  {100.0 * frac_s:.1f}%   (|J|>=0.5 max|J|, {n_s}/{n_all} cells)")
    print(f"Ohmic in rest    {100.0 * frac_t:.1f}%   (tubes / complement)")
    print(f"MHD−hydro / ∫ε_η = {diff / I_eta:.2f}")
    print(f"instantaneous ε_η end: tot {ohm_end:.3e}  sheet {ohm_s:.3e}  rest {ohm_t:.3e}")
    print()
    x = diff
    y = "high-|J| sheets" if frac_s >= 0.5 else "the tube complement, not a sheet spike"
    print(f"MHD differs from hydro by {x:.3e} ({100.0 * x / eh0:.2f}% of E_hydro(0)), "
          f"located in {y} ({100.0 * frac_s:.0f}% of Ohmic in |J|>=0.5 max|J|).")

    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "mhd_minus_hydro.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["qty", "value"])
        for row in [
            ("E_drop_hydro", DROP_HY),
            ("E_drop_MHD", DROP_MHD),
            ("MHD_minus_hydro", diff),
            ("MHD_minus_hydro_pct_of_E_hydro0", 100.0 * diff / eh0),
            ("int_Ohmic", I_eta),
            ("Ohmic_frac_sheets", frac_s),
            ("Ohmic_frac_tubes_rest", frac_t),
            ("n_sheet_cells", n_s),
            ("n_all", n_all),
            ("MHD_minus_hydro_over_Ohmic", diff / I_eta),
        ]:
            w.writerow(row)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.6))
        ax[0].bar(["hydro", "MHD", "MHD−hydro", "∫ε_η"],
                  [DROP_HY, DROP_MHD, diff, I_eta],
                  color=["0.5", "C0", "C3", "C1"])
        ax[0].set_ylabel("energy")
        ax[0].set_title("drops vs Ohmic")
        ax[0].tick_params(axis="x", rotation=20)
        ax[1].pie([frac_s, frac_t], labels=["sheets |J|", "rest (tubes)"],
                  colors=["C3", "0.7"], autopct="%.1f%%")
        ax[1].set_title("Ohmic at t=0.36")
        fig.tight_layout()
        png_path = OUT / "mhd_minus_hydro.png"
        fig.savefig(png_path, dpi=140)
        plt.close(fig)
        print(f"wrote {csv_path}")
        print(f"wrote {png_path}")
    except ImportError:
        print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()

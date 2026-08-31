"""Campaign A with hyper_kcut ON (η_h on k ≥ 0.5 k_max only).

    python examples/run_hyperkcut_A.py
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax.numpy as jnp
import numpy as np

from chive_ns import run_framework, DEFAULT_MHD, default_scar_centres

OUT = Path(__file__).resolve().parent / "mhd_n48_hyperkcut"

# Hyper-off Campaign A (last good Lorentz run)
OFF = {
    "NS+MHD": dict(max_j=22.97, lam=2.122, I_WL=-3.216e-3, w1=34.749,
                   dE_tot=6.26, I_eta=5.791e-4, I_h=0.0),
    "+η_h all-k": dict(max_j=18.52, lam=2.625, I_WL=-3.157e-3, w1=35.068,
                       dE_tot=6.38, I_eta=5.037e-4, I_h=1.594e-4),
}


def _trapz(y, t):
    y, t = jnp.asarray(y), jnp.asarray(t)
    if y.shape[0] < 2:
        return 0.0
    return float(jnp.sum(0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])))


def _pack(name, out):
    t = out["time"]
    nu = float(out["nu"])
    e_k, e_m = out["energy"], out["e_mag_tot"]
    I_WL = _trapz(out["lorentz_work"], t)
    I_nu = _trapz(nu * out["enstrophy"], t)
    I_eta = _trapz(out["ohmic"], t)
    I_h = _trapz(out["hyper_ohmic"], t)
    dEk = float(e_k[-1] - e_k[0])
    dEm = float(e_m[-1] - e_m[0])
    trans = abs(I_WL) + 1e-30
    return {
        "name": name,
        "t": np.array(t),
        "max_j_t": np.array(out["max_j"]),
        "lam_t": np.array(out["lam_min_dx"]),
        "w_t": np.array(out["max_vort"]),
        "WL_t": np.array(out["lorentz_work"]),
        "dE_tot": 100.0 * (-(dEk + dEm)) / max(float(e_k[0] + e_m[0]), 1e-30),
        "dE_kin": 100.0 * (-dEk) / max(float(e_k[0]), 1e-30),
        "w1": float(out["max_vort"][-1]),
        "max_j": float(out["max_j"].max()),
        "lam": float(out["lam_min_dx"][-1]),
        "I_WL": I_WL,
        "I_nu": I_nu,
        "I_eta": I_eta,
        "I_h": I_h,
        "res_k": 100.0 * (dEk - (I_WL - I_nu)) / trans,
        "res_m": 100.0 * (dEm - (-I_WL - I_eta - I_h)) / trans,
        "K_sheet": float(out["K_sheet"][-1]),
        "j_w": float(out["j_w"][-1]),
        "wlj": float(out["wl_j"][-1]),
        "divB": float(out["max_div_b"].max()),
    }


def _run(name, centres, eta_hyper, hyper_kcut):
    common = dict(
        dim=3, N=48, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    mhd = dict(DEFAULT_MHD, freeze_ext=0.0, eta_mag=1e-3, eta_odd=0.0,
               mu_eff=0.0, eta_hyper=float(eta_hyper),
               posdiv=1.0 if eta_hyper else 0.0,
               hyper_kcut=float(hyper_kcut))
    print(f"--- {name}  eta_h={eta_hyper:g}  hyper_kcut={hyper_kcut:g} ---",
          flush=True)
    out = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                        mhd_params=mhd, **common)
    r = _pack(name, out)
    print(f"    ΔE_tot={r['dE_tot']:.2f}%  |ω|={r['w1']:.3f}  "
          f"max|J|={r['max_j']:.3e}  λ/dx={r['lam']:.3f}  "
          f"∫W_L={r['I_WL']:.3e}  ∫η_h={r['I_h']:.3e}", flush=True)
    return r


def _write(ns, hk):
    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "campaign_A_hyperkcut.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "case", "hyper_kcut", "dE_tot_pct", "omega_end", "max_J",
            "lam_min_dx", "int_WL", "int_eps_eta", "int_eta_h",
            "kin_res_pct", "mag_res_pct", "K_sheet", "j_w",
        ])
        w.writerow([
            "NS+MHD (this run)", 0, f"{ns['dE_tot']:.4f}", f"{ns['w1']:.4f}",
            f"{ns['max_j']:.6e}", f"{ns['lam']:.4f}", f"{ns['I_WL']:.6e}",
            f"{ns['I_eta']:.6e}", f"{ns['I_h']:.6e}", f"{ns['res_k']:.3f}",
            f"{ns['res_m']:.3f}", f"{ns['K_sheet']:.6e}", f"{ns['j_w']:.6e}",
        ])
        w.writerow([
            "NS+MHD+η_h hyper_kcut=0.5", 0.5, f"{hk['dE_tot']:.4f}",
            f"{hk['w1']:.4f}", f"{hk['max_j']:.6e}", f"{hk['lam']:.4f}",
            f"{hk['I_WL']:.6e}", f"{hk['I_eta']:.6e}", f"{hk['I_h']:.6e}",
            f"{hk['res_k']:.3f}", f"{hk['res_m']:.3f}", f"{hk['K_sheet']:.6e}",
            f"{hk['j_w']:.6e}",
        ])
        w.writerow([])
        w.writerow(["reference hyper-off Campaign A"])
        w.writerow(["NS+MHD hyper-off", 0, OFF["NS+MHD"]["dE_tot"],
                    OFF["NS+MHD"]["w1"], OFF["NS+MHD"]["max_j"],
                    OFF["NS+MHD"]["lam"], OFF["NS+MHD"]["I_WL"],
                    OFF["NS+MHD"]["I_eta"], OFF["NS+MHD"]["I_h"], "", "", "", ""])
        w.writerow(["+η_h all-k hyper-off", 0, OFF["+η_h all-k"]["dE_tot"],
                    OFF["+η_h all-k"]["w1"], OFF["+η_h all-k"]["max_j"],
                    OFF["+η_h all-k"]["lam"], OFF["+η_h all-k"]["I_WL"],
                    OFF["+η_h all-k"]["I_eta"], OFF["+η_h all-k"]["I_h"],
                    "", "", "", ""])
        w.writerow([])
        w.writerow(["t", "max_J_NS", "max_J_kcut", "lam_NS", "lam_kcut",
                    "omega_NS", "omega_kcut", "WL_NS", "WL_kcut"])
        for i in range(len(ns["t"])):
            w.writerow([
                f"{float(ns['t'][i]):.4f}",
                f"{float(ns['max_j_t'][i]):.6e}",
                f"{float(hk['max_j_t'][i]):.6e}",
                f"{float(ns['lam_t'][i]):.4f}",
                f"{float(hk['lam_t'][i]):.4f}",
                f"{float(ns['w_t'][i]):.4f}",
                f"{float(hk['w_t'][i]):.4f}",
                f"{float(ns['WL_t'][i]):.6e}",
                f"{float(hk['WL_t'][i]):.6e}",
            ])

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available, csv only", flush=True)
        return csv_path, None

    fig, axes = plt.subplots(2, 2, figsize=(9.5, 7.2))
    t = ns["t"]
    axes[0, 0].plot(t, ns["max_j_t"], "k-o", label="NS+MHD")
    axes[0, 0].plot(t, hk["max_j_t"], "C0-s", label="η_h high-k")
    axes[0, 0].axhline(OFF["+η_h all-k"]["max_j"], color="C1", ls="--",
                       label="η_h all-k (ref)")
    axes[0, 0].set_ylabel("max |J|")
    axes[0, 0].legend(fontsize=8)
    axes[0, 1].plot(t, ns["lam_t"], "k-o")
    axes[0, 1].plot(t, hk["lam_t"], "C0-s")
    axes[0, 1].axhline(OFF["+η_h all-k"]["lam"], color="C1", ls="--")
    axes[0, 1].set_ylabel("λ_min / dx")
    axes[1, 0].plot(t, ns["w_t"], "k-o")
    axes[1, 0].plot(t, hk["w_t"], "C0-s")
    axes[1, 0].axhline(OFF["+η_h all-k"]["w1"], color="C1", ls="--")
    axes[1, 0].set_ylabel("max |ω|")
    axes[1, 0].set_xlabel("t")
    axes[1, 1].plot(t, ns["WL_t"], "k-o")
    axes[1, 1].plot(t, hk["WL_t"], "C0-s")
    axes[1, 1].set_ylabel("W_L")
    axes[1, 1].set_xlabel("t")
    for ax in axes.ravel():
        ax.grid(True, alpha=0.3)
    fig.suptitle("Campaign A  N=48  hyper_kcut=0.5  η_h=2e-7")
    fig.tight_layout()
    png_path = OUT / "campaign_A_hyperkcut.png"
    fig.savefig(png_path, dpi=140)
    plt.close(fig)
    return csv_path, png_path


def main():
    centres = default_scar_centres(1.0, 4, 3)
    print("Campaign A  N=48 t=0.36 Crow+4-scar  η=1e-3  η_h=2e-7  "
          "hyper_kcut=0.5 (high k only)", flush=True)
    ns = _run("NS+MHD", centres, 0.0, 0.0)
    hk = _run("η_h high-k", centres, 2e-7, 0.5)
    csv_path, png_path = _write(ns, hk)

    print("\n========== vs hyper-off Campaign A ==========")
    print(f"{'case':<22} {'max|J|':>9} {'λ_min/dx':>9} {'∫W_L':>11} "
          f"{'|ω|_end':>8}")
    print(f"{'NS+MHD this':<22} {ns['max_j']:9.3e} {ns['lam']:9.3f} "
          f"{ns['I_WL']:11.3e} {ns['w1']:8.3f}")
    print(f"{'η_h high-k this':<22} {hk['max_j']:9.3e} {hk['lam']:9.3f} "
          f"{hk['I_WL']:11.3e} {hk['w1']:8.3f}")
    print(f"{'NS+MHD hyper-off':<22} {OFF['NS+MHD']['max_j']:9.3e} "
          f"{OFF['NS+MHD']['lam']:9.3f} {OFF['NS+MHD']['I_WL']:11.3e} "
          f"{OFF['NS+MHD']['w1']:8.3f}")
    print(f"{'η_h all-k hyper-off':<22} {OFF['+η_h all-k']['max_j']:9.3e} "
          f"{OFF['+η_h all-k']['lam']:9.3f} {OFF['+η_h all-k']['I_WL']:11.3e} "
          f"{OFF['+η_h all-k']['w1']:8.3f}")
    print(f"\nwrote {csv_path}")
    if png_path:
        print(f"wrote {png_path}")
    return ns, hk


if __name__ == "__main__":
    main()

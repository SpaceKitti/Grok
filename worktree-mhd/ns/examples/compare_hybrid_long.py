"""NS vs old clay vs hybrid on tubes + 4-scar, N=64, t≈0.48.

    python examples/compare_hybrid_long.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import run_framework, DEFAULT_CLAY, default_scar_centres


def _row(name, out):
    e0, e1 = float(out["energy"][0]), float(out["energy"][-1])
    return {
        "name": name,
        "dE": 100.0 * (e0 - e1) / e0,
        "w0": float(out["max_vort"][0]),
        "w1": float(out["max_vort"][-1]),
        "w_peak": float(out["max_vort"].max()),
        "work": float(out["work"][-1]),
        "tau": float(out["max_tau"].max()),
        "bkm": float(out["bkm_integral"][-1]),
        "bkm_w": float(out["I_bkm_w"][-1]),
        "eps": float(out["eps_ratio"][-1]),
        "Tstar": float(out["Tstar"][-1]),
        "sheet": float(out["sheet_order"][-1]),
        "lam": float(out["lambda_kin"][-1]),
        "I_sigma": float(out["I_sigma"][-1]),
        "Gamma": float(out["Gamma"][-1]),
        "stretch": float(out["stretch"].max()),
        "t": float(out["time"][-1]),
        "div": float(out["max_div"].max()),
        "out": out,
    }


def main():
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=64, steps=320, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    old = dict(DEFAULT_CLAY, soft_J=0.0, alpha_par=0.0, alpha_perp=0.0,
               high_de=0.0, alpha_LB=0.0, lam_kin_gain=0.0,
               epsilon_frechet=0.0, gamma_s=0.0)
    print(f"N=64  dt=0.0015  steps=320  t={320*0.0015:.3f}  "
          f"tubes + 4-scar  force_amp=0.35", flush=True)
    print("scar lattice:", centres, flush=True)

    print("--- NS ---", flush=True)
    ns = _row("NS", run_framework(mode="vorticity", viscoelastic=False, **common))
    print("--- old clay (dials off) ---", flush=True)
    oc = _row("old", run_framework(mode="clay", viscoelastic=True,
                                   clay_params=old, **common))
    print("--- hybrid clay (defaults) ---", flush=True)
    hy = _row("hybrid", run_framework(mode="clay", viscoelastic=True, **common))

    print("\n========== End-state table ==========")
    print(f"{'case':<8} {'ΔE%':>7} {'|ω|_end':>8} {'|ω|_peak':>9} "
          f"{'W=τ:S':>10} {'max|τ|':>8} {'stretch':>8}")
    for r in (ns, oc, hy):
        print(f"{r['name']:<8} {r['dE']:7.2f} {r['w1']:8.3f} {r['w_peak']:9.3f} "
              f"{r['work']:10.3e} {r['tau']:8.4f} {r['stretch']:8.3f}")

    print("\n========== Live diagnostics at t_end ==========")
    print(f"{'case':<8} {'I_bkm_w':>9} {'BKM':>8} {'ε-ratio':>9} "
          f"{'T*':>8} {'sheet':>7} {'λ_kin':>7} {'I_σ':>9} {'Γ':>8}")
    for r in (ns, oc, hy):
        print(f"{r['name']:<8} {r['bkm_w']:9.4f} {r['bkm']:8.4f} {r['eps']:9.4f} "
              f"{r['Tstar']:8.3f} {r['sheet']:7.3f} {r['lam']:7.3f} "
              f"{r['I_sigma']:9.4f} {r['Gamma']:8.3f}")

    print("\n========== Time series: max|ω| / energy / W ==========")
    print(f"{'t':>6}  {'|ω|_NS':>8} {'|ω|_old':>8} {'|ω|_hy':>8}  "
          f"{'E_NS':>9} {'E_old':>9} {'E_hy':>9}  "
          f"{'W_old':>9} {'W_hy':>9}")
    no, oo, ho = ns["out"], oc["out"], hy["out"]
    for i in range(len(no["time"])):
        print(f"{float(no['time'][i]):6.3f}  "
              f"{float(no['max_vort'][i]):8.3f} {float(oo['max_vort'][i]):8.3f} "
              f"{float(ho['max_vort'][i]):8.3f}  "
              f"{float(no['energy'][i]):9.4e} {float(oo['energy'][i]):9.4e} "
              f"{float(ho['energy'][i]):9.4e}  "
              f"{float(oo['work'][i]):9.3e} {float(ho['work'][i]):9.3e}")

    print(f"\nmax|div u|  NS {ns['div']:.2e}  old {oc['div']:.2e}  "
          f"hybrid {hy['div']:.2e}")
    return ns, oc, hy


if __name__ == "__main__":
    main()

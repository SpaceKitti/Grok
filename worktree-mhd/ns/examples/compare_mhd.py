"""NS / old clay / hybrid clay / MHD-augmented comparison.

    python examples/compare_mhd.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax.numpy as jnp

from chive_ns import run_framework, DEFAULT_CLAY, DEFAULT_MHD, default_scar_centres


def _trapz(y, t):
    y = jnp.asarray(y)
    t = jnp.asarray(t)
    if y.shape[0] < 2:
        return 0.0
    return float(jnp.sum(0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])))


def _row(name, out):
    e0, e1 = float(out["energy"][0]), float(out["energy"][-1])
    em0, em1 = float(out["e_mag"][0]), float(out["e_mag"][-1])
    et0, et1 = e0 + em0, e1 + em1
    t = out["time"]
    return {
        "name": name,
        "dE": 100.0 * (e0 - e1) / max(e0, 1e-30),
        "dE_tot": 100.0 * (et0 - et1) / max(et0, 1e-30),
        "e0": e0, "e1": e1, "em0": em0, "em1": em1,
        "w0": float(out["max_vort"][0]),
        "w1": float(out["max_vort"][-1]),
        "w_peak": float(out["max_vort"].max()),
        "work": float(out["work"][-1]),
        "I_W": _trapz(out["work"], t),
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
        "ohmic": float(out["ohmic"][-1]),
        "I_ohm": _trapz(out["ohmic"], t),
        "I_nuZ": _trapz(float(out["nu"]) * out["enstrophy"], t),
        "max_j": float(out["max_j"].max()),
        "max_b": float(out["max_b"].max()),
        "H_cross": float(out["H_cross"][-1]),
        "H_mag": float(out["H_mag"][-1]),
        "H_j": float(out["H_current"][-1]),
        "Lwork": float(out["lorentz_work"][-1]),
        "I_L": _trapz(out["lorentz_work"], t),
        "maxwell": float(out["maxwell"][-1]),
        "op": float(out["op_ratio"][-1]),
        "divB": float(out["max_div_b"].max()),
        "out": out,
    }


def main():
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=48, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    old = dict(DEFAULT_CLAY, soft_J=0.0, alpha_par=0.0, alpha_perp=0.0,
               high_de=0.0, alpha_LB=0.0, lam_kin_gain=0.0,
               epsilon_frechet=0.0, gamma_s=0.0)
    mhd = dict(DEFAULT_MHD)
    print(f"N={common['N']}  dt={common['dt']}  steps={common['steps']}  "
          f"t={common['steps']*common['dt']:.3f}  tubes + 4-scar  "
          f"force_amp={common['force_amp']}", flush=True)
    print("scar lattice:", centres, flush=True)
    print(f"MHD defaults: eta_mag={mhd['eta_mag']}  B0={mhd['B0']}  "
          f"b_guide={mhd['b_guide']}  eta_odd={mhd['eta_odd']}", flush=True)

    print("--- NS ---", flush=True)
    ns = _row("NS", run_framework(mode="vorticity", viscoelastic=False,
                                  magnetic=False, **common))
    print("--- old clay (dials off) ---", flush=True)
    oc = _row("old", run_framework(mode="clay", viscoelastic=True,
                                   magnetic=False, clay_params=old, **common))
    print("--- hybrid clay (defaults) ---", flush=True)
    hy = _row("hybrid", run_framework(mode="clay", viscoelastic=True,
                                      magnetic=False, **common))
    print("--- NS + MHD ---", flush=True)
    nm = _row("NS+MHD", run_framework(mode="mhd", viscoelastic=False,
                                      magnetic=True, mhd_params=mhd, **common))
    print("--- hybrid clay + MHD ---", flush=True)
    hm = _row("hy+MHD", run_framework(mode="mhd", viscoelastic=True,
                                      magnetic=True, mhd_params=mhd, **common))

    rows = (ns, oc, hy, nm, hm)

    print("\n========== End-state table (kinetic) ==========")
    print(f"{'case':<8} {'ΔE_kin%':>8} {'|ω|_end':>8} {'|ω|_peak':>9} "
          f"{'W=τ:S':>10} {'max|τ|':>8} {'stretch':>8}")
    for r in rows:
        print(f"{r['name']:<8} {r['dE']:8.2f} {r['w1']:8.3f} {r['w_peak']:9.3f} "
              f"{r['work']:10.3e} {r['tau']:8.4f} {r['stretch']:8.3f}")

    print("\n========== Energy budget (kin + mag) ==========")
    print(f"{'case':<8} {'ΔE_tot%':>8} {'E_kin0':>9} {'E_kin1':>9} "
          f"{'E_mag0':>9} {'E_mag1':>9} {'∫νZ':>9} {'∫W':>9} {'∫Ohm':>9} "
          f"{'∫u·(J×B)':>10}")
    for r in rows:
        print(f"{r['name']:<8} {r['dE_tot']:8.2f} {r['e0']:9.3e} {r['e1']:9.3e} "
              f"{r['em0']:9.3e} {r['em1']:9.3e} {r['I_nuZ']:9.3e} "
              f"{r['I_W']:9.3e} {r['I_ohm']:9.3e} {r['I_L']:10.3e}")

    print("\n========== Magnetic / OP monitors at t_end ==========")
    print(f"{'case':<8} {'Ohmic':>9} {'max|J|':>8} {'max|B|':>8} "
          f"{'H_cross':>9} {'H_mag':>9} {'H_J':>9} {'op_ratio':>8} "
          f"{'max|divB|':>10}")
    for r in rows:
        print(f"{r['name']:<8} {r['ohmic']:9.3e} {r['max_j']:8.3e} "
              f"{r['max_b']:8.4f} {r['H_cross']:9.3e} {r['H_mag']:9.3e} "
              f"{r['H_j']:9.3e} {r['op']:8.3f} {r['divB']:10.2e}")

    print("\n========== Live diagnostics at t_end ==========")
    print(f"{'case':<8} {'I_bkm_w':>9} {'BKM':>8} {'ε-ratio':>9} "
          f"{'T*':>8} {'sheet':>7} {'λ_kin':>7} {'I_σ':>9} {'Γ':>8}")
    for r in rows:
        print(f"{r['name']:<8} {r['bkm_w']:9.4f} {r['bkm']:8.4f} {r['eps']:9.4f} "
              f"{r['Tstar']:8.3f} {r['sheet']:7.3f} {r['lam']:7.3f} "
              f"{r['I_sigma']:9.4f} {r['Gamma']:8.3f}")

    print("\n========== Time series: max|ω| / E_kin / E_mag / W ==========")
    print(f"{'t':>6}  {'|ω|_NS':>8} {'|ω|_old':>8} {'|ω|_hy':>8} "
          f"{'|ω|_NM':>8} {'|ω|_HM':>8}  "
          f"{'E_NS':>9} {'E_HM':>9} {'Em_NM':>9} {'Em_HM':>9}  "
          f"{'W_hy':>9} {'W_HM':>9}")
    outs = [r["out"] for r in rows]
    for i in range(len(outs[0]["time"])):
        print(f"{float(outs[0]['time'][i]):6.3f}  "
              f"{float(outs[0]['max_vort'][i]):8.3f} "
              f"{float(outs[1]['max_vort'][i]):8.3f} "
              f"{float(outs[2]['max_vort'][i]):8.3f} "
              f"{float(outs[3]['max_vort'][i]):8.3f} "
              f"{float(outs[4]['max_vort'][i]):8.3f}  "
              f"{float(outs[0]['energy'][i]):9.4e} "
              f"{float(outs[4]['energy'][i]):9.4e} "
              f"{float(outs[3]['e_mag'][i]):9.4e} "
              f"{float(outs[4]['e_mag'][i]):9.4e}  "
              f"{float(outs[2]['work'][i]):9.3e} "
              f"{float(outs[4]['work'][i]):9.3e}")

    print(f"\nmax|div u|  NS {ns['div']:.2e}  old {oc['div']:.2e}  "
          f"hybrid {hy['div']:.2e}  NS+MHD {nm['div']:.2e}  "
          f"hy+MHD {hm['div']:.2e}")
    print(f"max|div B|  NS+MHD {nm['divB']:.2e}  hy+MHD {hm['divB']:.2e}")
    return rows


if __name__ == "__main__":
    main()

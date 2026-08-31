"""NS+MHD vs PosDiv/hyperresistivity layer. Same Crow + 4-scar N=48 t=0.36.

    python examples/compare_posdiv.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax.numpy as jnp

from chive_ns import run_framework, DEFAULT_MHD, default_scar_centres


def _trapz(y, t):
    y, t = jnp.asarray(y), jnp.asarray(t)
    if y.shape[0] < 2:
        return 0.0
    return float(jnp.sum(0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])))


def _row(name, out):
    e0, e1 = float(out["energy"][0]), float(out["energy"][-1])
    em0, em1 = float(out["e_mag_tot"][0]), float(out["e_mag_tot"][-1])
    t = out["time"]
    I_nu = _trapz(float(out["nu"]) * out["enstrophy"], t)
    I_W = _trapz(out["work"], t)
    I_ohm = _trapz(out["ohmic"], t)
    I_h = _trapz(out.get("hyper_ohmic", 0.0 * out["ohmic"]), t)
    I_L = _trapz(out["lorentz_work"], t)
    dEk, dEm = e0 - e1, em1 - em0
    return {
        "name": name,
        "dE_tot": 100.0 * ((e0 + em0) - (e1 + em1)) / max(e0 + em0, 1e-30),
        "dE": 100.0 * (e0 - e1) / max(e0, 1e-30),
        "w1": float(out["max_vort"][-1]),
        "w_peak": float(out["max_vort"].max()),
        "max_j": float(out["max_j"].max()),
        "I_ohm": I_ohm,
        "I_h": I_h,
        "ohmic": float(out["ohmic"][-1]),
        "lam_end": float(out["lam_min_dx"][-1]),
        "N_i": float(out["N_i"][-1]),
        "divB": float(out["max_div_b"].max()),
        "dEk": dEk, "dEm": dEm,
        "pred_k": I_nu + I_W - I_L,
        "pred_m": -I_L - I_ohm - I_h,
        "out": out,
    }


def main():
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=48, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    print("N=48 t=0.36 Crow+4-scar B0=0.08 η=1e-3 b_guide=z", flush=True)
    print("control: freeze=0, eta_hyper=0, posdiv=0", flush=True)
    print("new:     freeze=0, eta_hyper=2e-7, posdiv=1  "
          "(hyperresistivity + Heun midpoint Helmholtz)", flush=True)

    print("--- NS+MHD control ---", flush=True)
    ctrl = _row("NS+MHD", run_framework(
        mode="mhd", viscoelastic=False, magnetic=True,
        mhd_params=dict(DEFAULT_MHD, freeze_ext=0.0, eta_hyper=0.0, posdiv=0.0),
        **common))
    print(f"    ΔE_tot={ctrl['dE_tot']:.2f}%  |ω|={ctrl['w1']:.3f}  "
          f"max|J|={ctrl['max_j']:.3e}  ∫Ohm={ctrl['I_ohm']:.3e}  "
          f"λ/dx={ctrl['lam_end']:.2f}", flush=True)

    print("--- PosDiv + hyperresistivity ---", flush=True)
    new = _row("posdiv", run_framework(
        mode="mhd", viscoelastic=False, magnetic=True,
        mhd_params=dict(DEFAULT_MHD, freeze_ext=0.0, eta_hyper=2.0e-7,
                        posdiv=1.0, eta_odd=0.0, mu_eff=0.0),
        **common))
    print(f"    ΔE_tot={new['dE_tot']:.2f}%  |ω|={new['w1']:.3f}  "
          f"max|J|={new['max_j']:.3e}  ∫Ohm={new['I_ohm']:.3e}  "
          f"∫η_h={new['I_h']:.3e}  λ/dx={new['lam_end']:.2f}", flush=True)

    print("\n========== Comparison ==========")
    print(f"{'case':<10} {'ΔE_tot%':>8} {'ΔE_kin%':>8} {'|ω|_end':>8} "
          f"{'max|J|':>9} {'∫Ohm':>9} {'∫η_h∇⁴':>9} {'λ_min/dx':>9} {'N_i':>7}")
    for r in (ctrl, new):
        print(f"{r['name']:<10} {r['dE_tot']:8.2f} {r['dE']:8.2f} {r['w1']:8.3f} "
              f"{r['max_j']:9.3e} {r['I_ohm']:9.3e} {r['I_h']:9.3e} "
              f"{r['lam_end']:9.3f} {r['N_i']:7.3f}")
    print(f"{'case':<10} {'dE_kin':>10} {'pred_k':>10} {'kin_err%':>8} "
          f"{'dE_mag':>10} {'pred_m':>10} {'mag_err%':>8} {'divB':>10}")
    for r in (ctrl, new):
        ek = abs(r["dEk"]) + 1e-30
        em = abs(r["dEm"]) + 1e-30
        print(f"{r['name']:<10} {r['dEk']:10.3e} {r['pred_k']:10.3e} "
              f"{100.0 * (r['dEk'] - r['pred_k']) / ek:8.2f} "
              f"{r['dEm']:10.3e} {r['pred_m']:10.3e} "
              f"{100.0 * (r['dEm'] - r['pred_m']) / em:8.2f} "
              f"{r['divB']:10.2e}")
    return ctrl, new


if __name__ == "__main__":
    main()

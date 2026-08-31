"""Lorentz-work energy isolation: NS+MHD vs NS+MHD+η_h.

    python examples/compare_lorentz_budget.py
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


def _cumtrapz(y, t):
    y, t = jnp.asarray(y), jnp.asarray(t)
    out = jnp.zeros_like(y)
    if y.shape[0] < 2:
        return out
    pieces = 0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])
    return jnp.concatenate([jnp.zeros((1,), dtype=y.dtype), jnp.cumsum(pieces)])


def _pack(name, out):
    t = out["time"]
    nu = float(out["nu"])
    e_k = out["energy"]
    e_m = out["e_mag_tot"]
    W_L = out["lorentz_work"]
    eps_eta = out["ohmic"]
    eps_h = out.get("hyper_ohmic", 0.0 * eps_eta)
    eps_nu = nu * out["enstrophy"]
    I_WL = _cumtrapz(W_L, t)
    I_nu = _cumtrapz(eps_nu, t)
    I_eta = _cumtrapz(eps_eta, t)
    I_h = _cumtrapz(eps_h, t)
    dEk = e_k - e_k[0]
    dEm = e_m - e_m[0]
    # ΔE_kin^Lorentz = ∫ W_L ; ΔE_mag^ind = −that
    pred_k = I_WL - I_nu
    pred_m = -I_WL - I_eta - I_h
    leak_k = dEk[-1] - pred_k[-1]
    leak_m = dEm[-1] - pred_m[-1]
    trans = abs(float(I_WL[-1])) + 1e-30
    return {
        "name": name,
        "t": t, "W_L": W_L, "eps_eta": eps_eta, "eps_nu": eps_nu, "eps_h": eps_h,
        "I_WL": I_WL, "I_nu": I_nu, "I_eta": I_eta, "I_h": I_h,
        "dEk": dEk, "dEm": dEm, "pred_k": pred_k, "pred_m": pred_m,
        "e0": float(e_k[0]), "e1": float(e_k[-1]),
        "em0": float(e_m[0]), "em1": float(e_m[-1]),
        "dE_tot": 100.0 * ((e_k[0] + e_m[0]) - (e_k[-1] + e_m[-1]))
                  / max(float(e_k[0] + e_m[0]), 1e-30),
        "w1": float(out["max_vort"][-1]),
        "max_j": float(out["max_j"].max()),
        "I_ohm": float(I_eta[-1]),
        "I_h_end": float(I_h[-1]),
        "I_WL_end": float(I_WL[-1]),
        "lam": float(out["lam_min_dx"][-1]),
        "sheet": float(out["sheet_ind"][-1]),
        "b_stretch": float(out["b_stretch"][-1]),
        "b_comp": float(out["b_comp"][-1]),
        "divB": float(out["max_div_b"].max()),
        "leak_k": float(leak_k),
        "leak_m": float(leak_m),
        "res_k": 100.0 * float(leak_k) / trans,
        "res_m": 100.0 * float(leak_m) / trans,
        "out": out,
    }


def _run(name, centres, hyper):
    common = dict(
        dim=3, N=48, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    mhd = dict(DEFAULT_MHD, freeze_ext=0.0, eta_odd=0.0, mu_eff=0.0,
               eta_hyper=float(hyper), posdiv=1.0 if hyper else 0.0)
    print(f"--- {name}  eta_hyper={hyper:g}  posdiv={mhd['posdiv']} ---",
          flush=True)
    out = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                        mhd_params=mhd, **common)
    r = _pack(name, out)
    print(f"    ΔE_tot={r['dE_tot']:.2f}%  |ω|={r['w1']:.3f}  "
          f"max|J|={r['max_j']:.3e}  ∫Ohm={r['I_ohm']:.3e}  "
          f"∫W_L={r['I_WL_end']:.3e}  λ/dx={r['lam']:.2f}  "
          f"kin_res={r['res_k']:.2f}%  mag_res={r['res_m']:.2f}%", flush=True)
    return r


def main():
    centres = default_scar_centres(1.0, 4, 3)
    print("N=48 t=0.36 Crow+4-scar B0=0.08 η=1e-3 b_guide=z freeze=0",
          flush=True)
    print("Lorentz isolation: W_L=⟨u·(J×B)⟩  ε_η=η⟨|J|²⟩  ε_ν=ν⟨|ω|²⟩",
          flush=True)
    a = _run("NS+MHD", centres, 0.0)
    b = _run("NS+MHD+η_h", centres, 2.0e-7)

    print("\n========== End-state table ==========")
    print(f"{'case':<12} {'ΔE_tot%':>8} {'|ω|_end':>8} {'max|J|':>9} "
          f"{'∫Ohm':>9} {'∫η_h':>9} {'λ_min/dx':>9} {'|J|/B':>8}")
    for r in (a, b):
        print(f"{r['name']:<12} {r['dE_tot']:8.2f} {r['w1']:8.3f} "
              f"{r['max_j']:9.3e} {r['I_ohm']:9.3e} {r['I_h_end']:9.3e} "
              f"{r['lam']:9.3f} {r['sheet']:8.3f}")

    print("\n========== Lorentz-work integrals ==========")
    print(f"{'case':<12} {'∫W_L':>11} {'−∫W_L':>11} {'∫ε_ν':>11} "
          f"{'∫ε_η':>11} {'∫ε_h':>11}")
    for r in (a, b):
        print(f"{r['name']:<12} {r['I_WL_end']:11.3e} {-r['I_WL_end']:11.3e} "
              f"{float(r['I_nu'][-1]):11.3e} {r['I_ohm']:11.3e} "
              f"{r['I_h_end']:11.3e}")

    print("\n========== Budget identities (leak vs |∫W_L|) ==========")
    print(f"{'case':<12} {'ΔE_kin':>11} {'∫W_L−∫ε_ν':>12} {'kin_res%':>9} "
          f"{'ΔE_mag':>11} {'−∫W_L−∫ε_η':>12} {'mag_res%':>9}")
    for r in (a, b):
        print(f"{r['name']:<12} {float(r['dEk'][-1]):11.3e} "
              f"{float(r['pred_k'][-1]):12.3e} {r['res_k']:9.2f} "
              f"{float(r['dEm'][-1]):11.3e} {float(r['pred_m'][-1]):12.3e} "
              f"{r['res_m']:9.2f}")
    print("kin: E_kin(t)−E_kin(0) ≈ ∫W_L − ∫ε_ν")
    print("mag: E_mag(t)−E_mag(0) ≈ −∫W_L − ∫ε_η − ∫ε_h")
    print("res% = (measured − predicted) / |∫W_L|   (leak vs transfer)")

    print("\n========== Time series  W_L / ε_η / ε_ν / stretching / |J|/B ==========")
    print(f"{'t':>6}  {'W_L_A':>10} {'W_L_B':>10}  {'εη_A':>10} {'εη_B':>10}  "
          f"{'εν_A':>10} {'εν_B':>10}  {'B:S_A':>10} {'J/B_A':>8} {'J/B_B':>8}")
    for i in range(len(a["t"])):
        print(f"{float(a['t'][i]):6.3f}  "
              f"{float(a['W_L'][i]):10.3e} {float(b['W_L'][i]):10.3e}  "
              f"{float(a['eps_eta'][i]):10.3e} {float(b['eps_eta'][i]):10.3e}  "
              f"{float(a['eps_nu'][i]):10.3e} {float(b['eps_nu'][i]):10.3e}  "
              f"{float(a['out']['b_stretch'][i]):10.3e} "
              f"{float(a['out']['sheet_ind'][i]):8.3f} "
              f"{float(b['out']['sheet_ind'][i]):8.3f}")

    print(f"\n⟨B_i S_ij B_j⟩_end  A {a['b_stretch']:.3e}  B {b['b_stretch']:.3e}")
    print(f"−½⟨B² ∇·u⟩_end      A {a['b_comp']:.3e}  B {b['b_comp']:.3e}")
    print(f"max|div B|          A {a['divB']:.2e}  B {b['divB']:.2e}")
    return a, b


if __name__ == "__main__":
    main()

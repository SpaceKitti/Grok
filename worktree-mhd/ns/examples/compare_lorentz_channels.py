"""Lorentz-channel diagnostics: Campaign A (η=1e-3) and B (η=5e-4).

    python examples/compare_lorentz_channels.py
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


def _pack(name, out):
    t = out["time"]
    nu = float(out["nu"])
    e_k, e_m = out["energy"], out["e_mag_tot"]
    W_L = out["lorentz_work"]
    eps_eta = out["ohmic"]
    eps_h = out["hyper_ohmic"]
    eps_nu = nu * out["enstrophy"]
    I_WL = _trapz(W_L, t)
    I_nu = _trapz(eps_nu, t)
    I_eta = _trapz(eps_eta, t)
    I_h = _trapz(eps_h, t)
    dEk = float(e_k[-1] - e_k[0])
    dEm = float(e_m[-1] - e_m[0])
    dEtot = 100.0 * (-(dEk + dEm)) / max(float(e_k[0] + e_m[0]), 1e-30)
    dEkin = 100.0 * (-dEk) / max(float(e_k[0]), 1e-30)
    dEmag = 100.0 * dEm / max(float(e_m[0]), 1e-30)
    pred_k = I_WL - I_nu
    pred_m = -I_WL - I_eta - I_h
    trans = abs(I_WL) + 1e-30
    st = float(out["b_stretch"][-1])
    cp = float(out["b_comp"][-1])
    stj = float(out["b_stretch_j"][-1])
    cpj = float(out["b_comp_j"][-1])
    wl = float(W_L[-1])
    wlj = float(out["wl_j"][-1])
    return {
        "name": name,
        "dE_tot": dEtot, "dE_kin": dEkin, "dE_mag": dEmag,
        "dEk": dEk, "dEm": dEm,
        "I_WL": I_WL, "I_nu": I_nu, "I_eta": I_eta, "I_h": I_h,
        "res_k": 100.0 * (dEk - pred_k) / trans,
        "res_m": 100.0 * (dEm - pred_m) / trans,
        "w1": float(out["max_vort"][-1]),
        "max_j": float(out["max_j"].max()),
        "lam": float(out["lam_min_dx"][-1]),
        "j_w": float(out["j_w"][-1]),
        "j_over_b_w": float(out["j_over_b_w"][-1]),
        "K_sheet": float(out["K_sheet"][-1]),
        "st": st, "cp": cp, "stj": stj, "cpj": cpj,
        "wl": wl, "wlj": wlj,
        "split": wl + st - cp,
        "split_j": wlj + stj - cpj,
        "divB": float(out["max_div_b"].max()),
        "out": out,
    }


def _run(name, centres, eta_mag, eta_hyper):
    common = dict(
        dim=3, N=48, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    mhd = dict(DEFAULT_MHD, freeze_ext=0.0, eta_mag=float(eta_mag),
               eta_odd=0.0, mu_eff=0.0, eta_hyper=float(eta_hyper),
               posdiv=1.0 if eta_hyper else 0.0, hyper_kcut=0.0)
    print(f"--- {name}  eta={eta_mag:g}  eta_h={eta_hyper:g} ---", flush=True)
    out = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                        mhd_params=mhd, **common)
    r = _pack(name, out)
    print(f"    ΔE_tot={r['dE_tot']:.2f}%  |ω|={r['w1']:.3f}  "
          f"max|J|={r['max_j']:.3e}  ∫W_L={r['I_WL']:.3e}  "
          f"K={r['K_sheet']:.3e}  λ/dx={r['lam']:.2f}", flush=True)
    return r


def _print_block(title, rows):
    print(f"\n========== {title} ==========")
    print(f"{'case':<14} {'ΔE_tot%':>8} {'ΔE_kin%':>8} {'ΔE_mag%':>8} "
          f"{'∫W_L':>11} {'∫ε_ν':>11} {'∫ε_η':>11} {'∫η_h':>11}")
    for r in rows:
        print(f"{r['name']:<14} {r['dE_tot']:8.2f} {r['dE_kin']:8.2f} "
              f"{r['dE_mag']:8.2f} {r['I_WL']:11.3e} {r['I_nu']:11.3e} "
              f"{r['I_eta']:11.3e} {r['I_h']:11.3e}")
    print(f"{'case':<14} {'kin_res%':>9} {'mag_res%':>9} {'|ω|_end':>8} "
          f"{'max|J|':>9} {'⟨|J|⟩_J':>9} {'λ_min/dx':>9} {'|J|/|B|_w':>10} "
          f"{'K_sheet':>10}")
    for r in rows:
        print(f"{r['name']:<14} {r['res_k']:9.2f} {r['res_m']:9.2f} "
              f"{r['w1']:8.3f} {r['max_j']:9.3e} {r['j_w']:9.3e} "
              f"{r['lam']:9.3f} {r['j_over_b_w']:10.3f} {r['K_sheet']:10.3e}")
    print(f"{'case':<14} {'W_L':>11} {'B:S vol':>11} {'B:S |J|':>11} "
          f"{'W_L |J|':>11} {'comp vol':>11} {'comp |J|':>11} {'split':>10}")
    for r in rows:
        print(f"{r['name']:<14} {r['wl']:11.3e} {r['st']:11.3e} {r['stj']:11.3e} "
              f"{r['wlj']:11.3e} {r['cp']:11.3e} {r['cpj']:11.3e} {r['split']:10.2e}")


def main():
    centres = default_scar_centres(1.0, 4, 3)
    print("N=48 t=0.36 Crow+4-scar B0=0.08 freeze=0  unmollified induction",
          flush=True)
    print("hyper_kcut=0 (tweak OFF). Campaign B: η=5e-4 (higher Rm, same t).",
          flush=True)

    print("\n##### Campaign A  η=1e-3 #####", flush=True)
    a0 = _run("A NS+MHD", centres, 1e-3, 0.0)
    a1 = _run("A +η_h", centres, 1e-3, 2e-7)
    _print_block("Campaign A  η=1e-3", (a0, a1))

    print("\n##### Campaign B  η=5e-4  (higher Rm) #####", flush=True)
    b0 = _run("B NS+MHD", centres, 5e-4, 0.0)
    b1 = _run("B +η_h", centres, 5e-4, 2e-7)
    _print_block("Campaign B  η=5e-4", (b0, b1))

    print("\n========== Does transfer live in sheets?  W_L vs W_L_|J|  ==========")
    print(f"{'case':<14} {'W_L vol':>11} {'W_L |J|-wt':>12} {'ratio':>8} "
          f"{'∫W_L':>11}")
    for r in (a0, a1, b0, b1):
        ratio = r["wlj"] / (abs(r["wl"]) + 1e-30)
        print(f"{r['name']:<14} {r['wl']:11.3e} {r['wlj']:12.3e} {ratio:8.2f} "
              f"{r['I_WL']:11.3e}")
    print("ratio ~ 1 and |W_L_|J|| ≫ volume mean ⇒ transfer concentrated in high-|J|.")
    print(f"\nmax|div B|  A0 {a0['divB']:.2e}  A1 {a1['divB']:.2e}  "
          f"B0 {b0['divB']:.2e}  B1 {b1['divB']:.2e}")
    return a0, a1, b0, b1


if __name__ == "__main__":
    main()

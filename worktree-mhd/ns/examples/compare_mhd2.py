"""NS / hybrid / NS+MHD vs freeze-out, odd, mu_eff layers.

    python examples/compare_mhd2.py
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
    em0 = float(out["e_mag_tot"][0]) if "e_mag_tot" in out else float(out["e_mag"][0])
    em1 = float(out["e_mag_tot"][-1]) if "e_mag_tot" in out else float(out["e_mag"][-1])
    et0, et1 = e0 + em0, e1 + em1
    t = out["time"]
    nu = float(out["nu"])
    I_nu = _trapz(nu * out["enstrophy"], t)
    I_W = _trapz(out["work"], t)
    I_ohm = _trapz(out["ohmic"], t)
    I_L = _trapz(out["lorentz_work"], t)
    dEk, dEm = e0 - e1, em1 - em0
    return {
        "name": name,
        "finite": bool(jnp.isfinite(out["energy"][-1])),
        "dE": 100.0 * (e0 - e1) / max(e0, 1e-30),
        "dE_tot": 100.0 * (et0 - et1) / max(et0, 1e-30),
        "e0": e0, "e1": e1, "em0": em0, "em1": em1,
        "w1": float(out["max_vort"][-1]),
        "w_peak": float(out["max_vort"].max()),
        "work": float(out["work"][-1]),
        "I_W": I_W, "I_nuZ": I_nu, "I_ohm": I_ohm, "I_L": I_L,
        "tau": float(out["max_tau"].max()),
        "ohmic": float(out["ohmic"][-1]),
        "max_j": float(out["max_j"].max()),
        "max_b": float(out["max_b"].max()),
        "N_i": float(out["N_i"][-1]),
        "N_i0": float(out["N_i"][0]),
        "lam": float(out["lam_min_dx"].min()),
        "lam_end": float(out["lam_min_dx"][-1]),
        "P_back": float(out["P_back"][-1]),
        "em_ext": float(out["e_mag_ext"][-1]),
        "dEk": dEk, "dEm": dEm,
        "pred_k": I_nu + I_W - I_L,
        "pred_m": -I_L - I_ohm,
        "pred_tot": I_nu + I_W + I_ohm,
        "divB": float(out["max_div_b"].max()),
        "out": out,
    }


def _print_main(rows):
    print(f"\n========== Kinetic + Crow ==========")
    print(f"{'case':<14} {'ΔE_kin%':>8} {'ΔE_tot%':>8} {'|ω|_end':>8} {'|ω|_peak':>9} "
          f"{'W':>10} {'max|τ|':>8}")
    for r in rows:
        print(f"{r['name']:<14} {r['dE']:8.2f} {r['dE_tot']:8.2f} {r['w1']:8.3f} "
              f"{r['w_peak']:9.3f} {r['work']:10.3e} {r['tau']:8.4f}")
    print(f"\n========== Magnetic / sheets / N_i ==========")
    print(f"{'case':<14} {'max|J|':>9} {'max|B|':>8} {'∫Ohm':>9} {'Ohm_end':>9} "
          f"{'λ_min/dx':>9} {'N_i':>7} {'E_mag1':>9}")
    for r in rows:
        print(f"{r['name']:<14} {r['max_j']:9.3e} {r['max_b']:8.4f} {r['I_ohm']:9.3e} "
              f"{r['ohmic']:9.3e} {r['lam_end']:9.3f} {r['N_i']:7.3f} {r['em1']:9.3e}")
    print(f"\n========== Energy identities ==========")
    print(f"{'case':<14} {'dE_kin':>10} {'pred_k':>10} {'dE_mag':>10} {'pred_m':>10} "
          f"{'kin_err%':>8} {'mag_err%':>8}")
    for r in rows:
        ek = abs(r["dEk"]) + 1e-30
        em = abs(r["dEm"]) + 1e-30
        print(f"{r['name']:<14} {r['dEk']:10.3e} {r['pred_k']:10.3e} "
              f"{r['dEm']:10.3e} {r['pred_m']:10.3e} "
              f"{100.0 * (r['dEk'] - r['pred_k']) / ek:8.2f} "
              f"{100.0 * (r['dEm'] - r['pred_m']) / em:8.2f}")


def run_one(name, common, viscoelastic, **mhd_kw):
    mhd = dict(DEFAULT_MHD, **mhd_kw)
    print(f"--- {name}  freeze={mhd.get('freeze_ext', 0)}  "
          f"odd={mhd.get('eta_odd', 0)}  mu={mhd.get('mu_eff', 0)} ---",
          flush=True)
    out = run_framework(mode="mhd", viscoelastic=viscoelastic, magnetic=True,
                        mhd_params=mhd, **common)
    r = _row(name, out)
    print(f"    ΔE_tot={r['dE_tot']:.2f}%  |ω|={r['w1']:.3f}  "
          f"max|J|={r['max_j']:.3e}  ∫Ohm={r['I_ohm']:.3e}  "
          f"λ/dx={r['lam_end']:.2f}  N_i={r['N_i']:.3f}  "
          f"Em {r['em0']:.3e}→{r['em1']:.3e}", flush=True)
    return r


def main():
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=48, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    print(f"N=48  t={240*0.0015:.3f}  tubes+4-scar  B0=0.08  η=1e-3  "
          f"b_guide=z", flush=True)
    print("unmollified induction; freeze-out = uniform B_ext not stretched",
          flush=True)

    # 1. NS+MHD control (fully advected guide, freeze=0)
    ns_m = run_one("NS+MHD", common, False, freeze_ext=0.0, eta_odd=0.0, mu_eff=0.0)
    # 2. freeze-out: 75% of B0 is Lorentz-only, 25% is stretched
    fr = run_one("freeze", common, False, freeze_ext=0.75, ext_profile="uniform",
                 eta_odd=0.0, mu_eff=0.0)
    # 3. hybrid + freeze-out (polymer + magnetic back-pressure)
    hf = run_one("hy+freeze", common, True, freeze_ext=0.75, ext_profile="uniform",
                 eta_odd=0.0, mu_eff=0.0)
    # 4. Berry/odd viscosity regulariser
    od = run_one("odd", common, False, freeze_ext=0.0, eta_odd=1.0e-3,
                 berry_gain=0.5, mu_eff=0.0)
    # 5. effective even viscosity
    mu = run_one("mu_eff", common, False, freeze_ext=0.0, eta_odd=0.0,
                 mu_eff=2.0e-4)
    # 6. freeze-out + odd (clean combo)
    fo = run_one("freeze+odd", common, False, freeze_ext=0.75,
                 ext_profile="uniform", eta_odd=1.0e-3, berry_gain=0.5,
                 mu_eff=0.0)

    print("\n(NS / hybrid clay from the previous N=48 t=0.36 hydro campaign:)")
    print("NS           ΔE_kin=5.95%  |ω|_end=38.480  W=0")
    print("hybrid       ΔE_kin=8.43%  |ω|_end=37.955  W=8.71e-3  max|τ|=0.021")

    rows = [ns_m, fr, hf, od, mu, fo]
    _print_main(rows)
    print(f"\nmax|div B|", "  ".join(f"{r['name']} {r['divB']:.2e}" for r in rows))
    return rows


if __name__ == "__main__":
    main()

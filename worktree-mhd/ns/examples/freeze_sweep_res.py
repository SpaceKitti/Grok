"""1) freeze_ext sweep  2) NS+MHD sheet resolution N=48/64/96.

    python examples/freeze_sweep_res.py
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
    em0 = float(out["e_mag_tot"][0])
    em1 = float(out["e_mag_tot"][-1])
    et0, et1 = e0 + em0, e1 + em1
    t = out["time"]
    return {
        "name": name,
        "finite": bool(jnp.isfinite(out["energy"][-1])),
        "dE": 100.0 * (e0 - e1) / max(e0, 1e-30),
        "dE_tot": 100.0 * (et0 - et1) / max(et0, 1e-30),
        "w1": float(out["max_vort"][-1]),
        "w_peak": float(out["max_vort"].max()),
        "max_j": float(out["max_j"].max()),
        "I_ohm": _trapz(out["ohmic"], t),
        "ohmic": float(out["ohmic"][-1]),
        "lam_end": float(out["lam_min_dx"][-1]),
        "lam_min": float(out["lam_min_dx"].min()),
        "N_i": float(out["N_i"][-1]),
        "em0": em0, "em1": em1,
        "divB": float(out["max_div_b"].max()),
        "dEk": e0 - e1,
        "pred_k": _trapz(float(out["nu"]) * out["enstrophy"], t)
                  + _trapz(out["work"], t) - _trapz(out["lorentz_work"], t),
        "dEm": em1 - em0,
        "pred_m": -_trapz(out["lorentz_work"], t) - _trapz(out["ohmic"], t),
        "out": out,
    }


def _run(name, N, freeze, centres, extra=None):
    common = dict(
        dim=3, N=N, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    mhd = dict(DEFAULT_MHD, freeze_ext=float(freeze),
               ext_profile="uniform", eta_odd=0.0, mu_eff=0.0,
               harris=False, es_lhdi=False)
    if extra:
        mhd.update(extra)
    print(f"--- {name}  N={N}  freeze={freeze} ---", flush=True)
    out = run_framework(mode="mhd", viscoelastic=False, magnetic=True,
                        mhd_params=mhd, **common)
    r = _row(name, out)
    print(f"    finite={r['finite']}  ΔE_tot={r['dE_tot']:.2f}%  "
          f"|ω|={r['w1']:.3f}  max|J|={r['max_j']:.3e}  "
          f"∫Ohm={r['I_ohm']:.3e}  λ/dx={r['lam_end']:.2f}  "
          f"N_i={r['N_i']:.3f}", flush=True)
    return r


def _print_freeze(rows):
    print("\n========== 1. freeze_ext sweep  (NS+MHD, N=48, t=0.36) ==========")
    print(f"{'freeze':<10} {'ΔE_tot%':>8} {'|ω|_end':>8} {'|ω|_peak':>9} "
          f"{'max|J|':>9} {'∫Ohm':>9} {'λ_min/dx':>9} {'N_i':>7}")
    for r in rows:
        print(f"{r['name']:<10} {r['dE_tot']:8.2f} {r['w1']:8.3f} {r['w_peak']:9.3f} "
              f"{r['max_j']:9.3e} {r['I_ohm']:9.3e} {r['lam_end']:9.3f} {r['N_i']:7.3f}")
    print(f"{'freeze':<10} {'dE_kin':>10} {'pred_k':>10} {'kin_err%':>8} "
          f"{'dE_mag':>10} {'pred_m':>10} {'mag_err%':>8}")
    for r in rows:
        ek = abs(r["dEk"]) + 1e-30
        em = abs(r["dEm"]) + 1e-30
        print(f"{r['name']:<10} {r['dEk']:10.3e} {r['pred_k']:10.3e} "
              f"{100.0 * (r['dEk'] - r['pred_k']) / ek:8.2f} "
              f"{r['dEm']:10.3e} {r['pred_m']:10.3e} "
              f"{100.0 * (r['dEm'] - r['pred_m']) / em:8.2f}")


def _print_res(rows):
    print("\n========== 2. Sheet resolution  (NS+MHD, freeze=0) ==========")
    print(f"{'N':<6} {'ΔE_tot%':>8} {'|ω|_end':>8} {'max|J|':>9} {'∫Ohm':>9} "
          f"{'Ohm_end':>9} {'λ_min/dx':>9} {'min λ/dx':>9}")
    for r in rows:
        print(f"{r['name']:<6} {r['dE_tot']:8.2f} {r['w1']:8.3f} {r['max_j']:9.3e} "
              f"{r['I_ohm']:9.3e} {r['ohmic']:9.3e} {r['lam_end']:9.3f} "
              f"{r['lam_min']:9.3f}")
    print("\n========== λ_min/dx  /  max|J|  /  Ohmic(t) ==========")
    print(f"{'t':>6}", end="")
    for r in rows:
        print(f"  {'λ_'+r['name']:>8} {'J_'+r['name']:>8} {'ηJ2_'+r['name']:>10}",
              end="")
    print()
    n = min(len(r["out"]["time"]) for r in rows)
    for i in range(n):
        print(f"{float(rows[0]['out']['time'][i]):6.3f}", end="")
        for r in rows:
            print(f"  {float(r['out']['lam_min_dx'][i]):8.3f} "
                  f"{float(r['out']['max_j'][i]):8.3e} "
                  f"{float(r['out']['ohmic'][i]):10.3e}", end="")
        print()


def main():
    centres = default_scar_centres(1.0, 4, 3)
    print("N=48 t=0.36 tubes+4-scar B0=0.08 η=1e-3 b_guide=z  "
          "unmollified induction", flush=True)

    # --- 1. freeze sweep (freeze=0 is also the N=48 resolution baseline)
    sweep = []
    for f in (0.0, 0.3, 0.5, 0.6, 0.75):
        tag = "f=0" if f == 0.0 else f"f={f:g}"
        sweep.append(_run(tag, 48, f, centres))
    _print_freeze(sweep)

    n48 = sweep[0]
    print("\n--- resolution N=64 ---", flush=True)
    n64 = _run("N=64", 64, 0.0, centres)
    print("\n--- resolution N=96 (may be slow) ---", flush=True)
    try:
        n96 = _run("N=96", 96, 0.0, centres)
        res = [n48, n64, n96]
    except Exception as exc:
        print("N=96 failed:", exc, flush=True)
        res = [n48, n64]
    n48 = dict(n48, name="N=48")
    res[0] = n48
    _print_res(res)
    return sweep, res


if __name__ == "__main__":
    main()

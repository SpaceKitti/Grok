"""Post-fix hy+MHD recheck, eta-sweep, and b_guide=x vs z.

    python examples/mhd_followup.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax.numpy as jnp

from chive_ns import run_framework, DEFAULT_MHD, default_scar_centres


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
    finite = bool(jnp.isfinite(out["energy"][-1]) and jnp.isfinite(out["e_mag"][-1])
                  and jnp.isfinite(out["max_vort"][-1]))
    I_nu = _trapz(float(out["nu"]) * out["enstrophy"], t)
    I_W = _trapz(out["work"], t)
    I_ohm = _trapz(out["ohmic"], t)
    I_L = _trapz(out["lorentz_work"], t)
    dEk, dEm = e0 - e1, em1 - em0
    return {
        "name": name,
        "finite": finite,
        "dE": 100.0 * (e0 - e1) / max(e0, 1e-30),
        "dE_tot": 100.0 * (et0 - et1) / max(et0, 1e-30),
        "e0": e0, "e1": e1, "em0": em0, "em1": em1,
        "w1": float(out["max_vort"][-1]),
        "w_peak": float(out["max_vort"].max()),
        "work": float(out["work"][-1]),
        "I_W": I_W,
        "tau": float(out["max_tau"].max()),
        "stretch": float(out["stretch"].max()),
        "I_nuZ": I_nu,
        "ohmic": float(out["ohmic"][-1]),
        "I_ohm": I_ohm,
        "max_j": float(out["max_j"].max()),
        "max_b": float(out["max_b"].max()),
        "H_cross": float(out["H_cross"][-1]),
        "H_mag": float(out["H_mag"][-1]),
        "H_j": float(out["H_current"][-1]),
        "I_L": I_L,
        "op": float(out["op_ratio"][-1]),
        "div": float(out["max_div"].max()),
        "divB": float(out["max_div_b"].max()),
        "dEk": dEk,
        "dEm": dEm,
        "pred_k": I_nu + I_W - I_L,
        "pred_m": -I_L - I_ohm,
        "pred_tot": I_nu + I_W + I_ohm,
        "t": float(out["time"][-1]),
        "out": out,
    }


def _print_budget(rows, title):
    print(f"\n========== {title} ==========")
    print(f"{'case':<14} {'ΔE_tot%':>8} {'ΔE_kin%':>8} {'E_mag0':>9} {'E_mag1':>9} "
          f"{'∫νZ':>9} {'∫W':>9} {'∫Ohm':>9} {'∫u·(J×B)':>10}")
    for r in rows:
        print(f"{r['name']:<14} {r['dE_tot']:8.2f} {r['dE']:8.2f} "
              f"{r['em0']:9.3e} {r['em1']:9.3e} {r['I_nuZ']:9.3e} "
              f"{r['I_W']:9.3e} {r['I_ohm']:9.3e} {r['I_L']:10.3e}")
    print(f"{'case':<14} {'dE_kin':>10} {'pred_k':>10} {'dE_mag':>10} {'pred_m':>10} "
          f"{'dE_tot':>10} {'pred_tot':>10} {'kin_err%':>8} {'mag_err%':>8}")
    for r in rows:
        ek = abs(r["dEk"]) + 1e-30
        em = abs(r["dEm"]) + 1e-30
        print(f"{r['name']:<14} {r['dEk']:10.3e} {r['pred_k']:10.3e} "
              f"{r['dEm']:10.3e} {r['pred_m']:10.3e} "
              f"{r['dEk'] - r['dEm']:10.3e} {r['pred_tot']:10.3e} "
              f"{100.0 * (r['dEk'] - r['pred_k']) / ek:8.2f} "
              f"{100.0 * (r['dEm'] - r['pred_m']) / em:8.2f}")


def _print_mag(rows, title):
    print(f"\n========== {title} ==========")
    print(f"{'case':<14} {'ΔE_tot%':>8} {'|ω|_end':>8} {'|ω|_peak':>9} "
          f"{'max|J|':>9} {'max|B|':>8} {'∫Ohm':>9} {'Ohm_end':>9} "
          f"{'op':>7} {'divB':>10}")
    for r in rows:
        print(f"{r['name']:<14} {r['dE_tot']:8.2f} {r['w1']:8.3f} {r['w_peak']:9.3f} "
              f"{r['max_j']:9.3e} {r['max_b']:8.4f} {r['I_ohm']:9.3e} "
              f"{r['ohmic']:9.3e} {r['op']:7.3f} {r['divB']:10.2e}")


def _print_kinetic(rows, title):
    print(f"\n========== {title} ==========")
    print(f"{'case':<14} {'ΔE_kin%':>8} {'|ω|_end':>8} {'|ω|_peak':>9} "
          f"{'W=τ:S':>10} {'max|τ|':>8} {'stretch':>8}")
    for r in rows:
        print(f"{r['name']:<14} {r['dE']:8.2f} {r['w1']:8.3f} {r['w_peak']:9.3f} "
              f"{r['work']:10.3e} {r['tau']:8.4f} {r['stretch']:8.3f}")


def run_one(name, common, viscoelastic, eta, guide):
    print(f"--- {name}  eta={eta:g}  b_guide={guide} ---", flush=True)
    mhd = dict(DEFAULT_MHD, eta_mag=float(eta), b_guide=guide, B0=0.08, eta_odd=0.0)
    out = run_framework(
        mode="mhd", viscoelastic=viscoelastic, magnetic=True,
        mhd_params=mhd, **common)
    r = _row(name, out)
    print(f"    finite={r['finite']}  ΔE_tot={r['dE_tot']:.2f}%  "
          f"|ω|={r['w1']:.3f}  max|J|={r['max_j']:.3e}  "
          f"max|B|={r['max_b']:.4f}  ∫Ohm={r['I_ohm']:.3e}  "
          f"Em {r['em0']:.3e}→{r['em1']:.3e}  divB={r['divB']:.2e}",
          flush=True)
    return r


def main():
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=48, steps=240, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    print(f"N={common['N']}  dt={common['dt']}  steps={common['steps']}  "
          f"t={common['steps'] * common['dt']:.3f}  tubes + 4-scar  "
          f"force_amp={common['force_amp']}", flush=True)
    print("scar lattice:", centres, flush=True)
    print("induction uses unmollified u; J-mollify is polymer-only", flush=True)

    # (1) post-fix hybrid+MHD at default η, b_guide=z
    hy = run_one("hy+MHD z", common, True, 1e-3, "z")

    # (2) eta sweep, including NS+MHD at 1e-3 and the other etas
    sweep = [hy]
    for eta in (5e-4, 1e-3, 5e-3):
        sweep.append(run_one(f"NS+MHD η={eta:g}", common, False, eta, "z"))
        if abs(eta - 1e-3) > 1e-15:
            sweep.append(run_one(f"hy+MHD η={eta:g}", common, True, eta, "z"))

    # (3) b_guide = x at default η
    nx = run_one("NS+MHD x", common, False, 1e-3, "x")
    hx = run_one("hy+MHD x", common, True, 1e-3, "x")

    # Locate NS+MHD z 1e-3 from the sweep
    ns_z = next(r for r in sweep if r["name"] == "NS+MHD η=0.001")

    print("\n\n################  1. POST-FIX hy+MHD vs previous hydro  ################")
    # Previous hydro campaign (unchanged code path), N=48 t=0.36:
    print("(NS / old / hybrid kinetic numbers from the previous hydro campaign;")
    print(" NS+MHD z and hy+MHD z are this run, after the induction-u fix.)")
    _print_kinetic([hy, ns_z], "Post-fix kinetic (MHD pair)")
    _print_budget([hy, ns_z], "Post-fix energy budget (magnetic column)")
    _print_mag([hy, ns_z], "Post-fix magnetic monitors")

    print("\n\n################  2. ETA SWEEP  (b_guide=z, B0=0.08)  ################")
    # order: eta then NS / hy
    ordered = []
    for eta in (5e-4, 1e-3, 5e-3):
        ordered.append(next(r for r in sweep if r["name"] == f"NS+MHD η={eta:g}"))
        if abs(eta - 1e-3) < 1e-15:
            ordered.append(hy)
        else:
            ordered.append(next(r for r in sweep if r["name"] == f"hy+MHD η={eta:g}"))
    _print_mag(ordered, "Eta sweep: ΔE_tot / |ω| / |J| / ∫Ohm / |B|")
    _print_budget(ordered, "Eta sweep energy identities")
    _print_kinetic(ordered, "Eta sweep kinetic + polymer")

    print("\n\n################  3. b_guide x vs z  (η=1e-3)  ################")
    xz = [ns_z, hy, nx, hx]
    _print_mag(xz, "Guide-field orientation")
    _print_budget(xz, "Guide-field energy identities")
    _print_kinetic(xz, "Guide-field kinetic + polymer")

    print(f"\nmax|div u|  hy+MHD z {hy['div']:.2e}  NS+MHD z {ns_z['div']:.2e}  "
          f"NS+MHD x {nx['div']:.2e}  hy+MHD x {hx['div']:.2e}")
    print(f"max|div B|  hy+MHD z {hy['divB']:.2e}  NS+MHD z {ns_z['divB']:.2e}  "
          f"NS+MHD x {nx['divB']:.2e}  hy+MHD x {hx['divB']:.2e}")
    return hy, sweep, nx, hx


if __name__ == "__main__":
    main()

"""Higher-resolution / lower-viscosity Taylor–Green study (NS vs clay).

Default: N=96, ν ∈ {5e-4, 2e-4, 1e-4}, shared dt=0.001, 120 RK2 steps.

    python examples/study_hires_nu.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import run_framework


NUS = (5.0e-4, 2.0e-4, 1.0e-4)


def _peaks(out):
    e0, e1 = float(out["energy"][0]), float(out["energy"][-1])
    return {
        "E0": e0,
        "E1": e1,
        "dE_frac": (e0 - e1) / (e0 + 1e-30),
        "Z0": float(out["enstrophy"][0]),
        "Z_peak": float(out["enstrophy"].max()),
        "Z1": float(out["enstrophy"][-1]),
        "max_w_peak": float(out["max_vort"].max()),
        "max_w1": float(out["max_vort"][-1]),
        "max_S_peak": float(out["max_strain"].max()),
        "bkm": float(out["bkm_integral"][-1]),
        "dZ_peak": float(out["dZ_dt"].max()),
        "stretch_peak": float(out["stretch"].max()),
        "eps_peak": float(out["dissipation"].max()),
        "max_tau": float(out["max_tau"].max()),
        "mean_tau": float(out["mean_tau"][-1]),
        "max_div": float(out["max_div"].max()),
        "t_end": float(out["time"][-1]),
    }


def run_sweep(N=96, steps=120, dt=0.001, diag_every=20, nus=NUS):
    common = dict(dim=3, N=N, steps=steps, ic="taylor_green", scheme="rk2",
                  force_on=False, diag_every=diag_every, dt=dt)
    results = {}
    for mode, flag, label in (
        ("vorticity", False, "NS"),
        ("clay", True, "clay"),
    ):
        for nu in nus:
            print(f"--- {label}  N={N}  nu={nu:.1e}  steps={steps}  dt={dt} ---",
                  flush=True)
            out = run_framework(mode=mode, viscoelastic=flag, nu=nu, **common)
            results[(label, nu)] = (out, _peaks(out))
            p = results[(label, nu)][1]
            print(f"    t={p['t_end']:.3f}  E {p['E0']:.4e}->{p['E1']:.4e}  "
                  f"Z_peak={p['Z_peak']:.4e}  max|w|={p['max_w_peak']:.4e}  "
                  f"max|S|={p['max_S_peak']:.4e}  BKM={p['bkm']:.4e}  "
                  f"dZ/dt_peak={p['dZ_peak']:.4e}  max|tau|={p['max_tau']:.4e}")
    return results


def print_tables(results, nus=NUS):
    print("\n========== Peak / end-state summary ==========")
    print(f"{'nu':>8} {'mode':>5}  {'max|ω|':>9} {'max|S|':>9} {'BKM':>9} "
          f"{'Z_peak':>9} {'dZ/dt':>9} {'ΔE/E0':>8} {'max|τ|':>9}")
    for nu in nus:
        for label in ("NS", "clay"):
            p = results[(label, nu)][1]
            print(f"{nu:8.1e} {label:>5}  {p['max_w_peak']:9.4e} {p['max_S_peak']:9.4e} "
                  f"{p['bkm']:9.4e} {p['Z_peak']:9.4e} {p['dZ_peak']:9.4e} "
                  f"{p['dE_frac']:8.3%} {p['max_tau']:9.4e}")

    print("\n========== Clay regularisation (NS / clay) ==========")
    print(f"{'nu':>8}  {'max|ω|':>8} {'max|S|':>8} {'BKM':>8} {'Z_peak':>8} "
          f"{'dZ/dt':>8} {'stretch':>8}  {'ηp/ν':>7}")
    eta_p = 0.008
    for nu in nus:
        ns, cl = results[("NS", nu)][1], results[("clay", nu)][1]
        def r(a, b):
            return a / (b + 1e-30)
        print(f"{nu:8.1e}  {r(ns['max_w_peak'], cl['max_w_peak']):8.3f} "
              f"{r(ns['max_S_peak'], cl['max_S_peak']):8.3f} "
              f"{r(ns['bkm'], cl['bkm']):8.3f} "
              f"{r(ns['Z_peak'], cl['Z_peak']):8.3f} "
              f"{r(ns['dZ_peak'], cl['dZ_peak']):8.3f} "
              f"{r(ns['stretch_peak'], cl['stretch_peak']):8.3f}  "
              f"{eta_p/nu:7.1f}")

    print("\n========== Time series (max|ω|, max|S|, BKM, Z) ==========")
    for nu in nus:
        ns_out, cl_out = results[("NS", nu)][0], results[("clay", nu)][0]
        print(f"\nnu={nu:.1e}")
        print(f"{'t':>6}  {'|ω|_NS':>9} {'|ω|_cl':>9}  {'|S|_NS':>9} {'|S|_cl':>9}  "
              f"{'BKM_NS':>9} {'BKM_cl':>9}  {'Z_NS':>9} {'Z_cl':>9}")
        for i in range(len(ns_out["time"])):
            print(f"{float(ns_out['time'][i]):6.3f}  "
                  f"{float(ns_out['max_vort'][i]):9.4e} {float(cl_out['max_vort'][i]):9.4e}  "
                  f"{float(ns_out['max_strain'][i]):9.4e} {float(cl_out['max_strain'][i]):9.4e}  "
                  f"{float(ns_out['bkm_integral'][i]):9.4e} {float(cl_out['bkm_integral'][i]):9.4e}  "
                  f"{float(ns_out['enstrophy'][i]):9.4e} {float(cl_out['enstrophy'][i]):9.4e}")


def main():
    results = run_sweep()
    print_tables(results)
    return results


if __name__ == "__main__":
    main()

"""N=64 helical Z₇: no force vs 1 scar vs 4-scar lattice, NS and clay.

    python examples/compare_scars.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import run_framework, default_scar_centres


def _end(out):
    return {
        "E0": float(out["energy"][0]),
        "E1": float(out["energy"][-1]),
        "Z0": float(out["enstrophy"][0]),
        "Z1": float(out["enstrophy"][-1]),
        "Z_peak": float(out["enstrophy"].max()),
        "w_peak": float(out["max_vort"].max()),
        "w1": float(out["max_vort"][-1]),
        "stretch_peak": float(out["stretch"].max()),
        "stretch1": float(out["stretch"][-1]),
        "tau": float(out["max_tau"].max()),
        "bkm": float(out["bkm_integral"][-1]),
        "div": float(out["max_div"].max()),
    }


def main():
    # Quiet C∞ IC so the Z₇ lattice is the main driver (TG/tubes also work).
    common = dict(dim=3, N=64, steps=80, ic="smooth", scheme="rk2",
                  nu=5e-4, dt=0.001, diag_every=20, force_amp=1.0)
    configs = (
        ("none", False, 1, None),
        ("single", True, 1, None),
        ("multi4", True, 4, None),
    )
    results = {}
    for mode, flag, label in (("vorticity", False, "NS"), ("clay", True, "clay")):
        for name, force_on, n_scars, centres in configs:
            key = (label, name)
            print(f"--- {label}  {name}  n_scars={n_scars}  force={force_on} ---",
                  flush=True)
            out = run_framework(mode=mode, viscoelastic=flag, force_on=force_on,
                                n_scars=n_scars, scar_centres=centres, **common)
            results[key] = (out, _end(out))
            p = results[key][1]
            print(f"    E {p['E0']:.4e}->{p['E1']:.4e}  Z {p['Z0']:.3e}->{p['Z1']:.3e}  "
                  f"max|w|={p['w_peak']:.3e}  stretch={p['stretch_peak']:.3e}  "
                  f"max|tau|={p['tau']:.3e}", flush=True)

    print(f"\n4-scar lattice: {default_scar_centres(1.0, 4, 3)}")
    print("\n========== End-state / peaks ==========")
    print(f"{'mode':<5} {'force':<7}  {'E_end':>9} {'Z_end':>9} {'Z_peak':>9} "
          f"{'max|ω|':>9} {'stretch':>9} {'max|τ|':>9} {'BKM':>8}")
    for label in ("NS", "clay"):
        for name, _, _, _ in configs:
            p = results[(label, name)][1]
            print(f"{label:<5} {name:<7}  {p['E1']:9.4e} {p['Z1']:9.4e} {p['Z_peak']:9.4e} "
                  f"{p['w_peak']:9.4e} {p['stretch_peak']:9.4e} {p['tau']:9.4e} "
                  f"{p['bkm']:8.3e}")

    print("\n========== Time series: energy / stretch / max|ω| ==========")
    for label in ("NS", "clay"):
        print(f"\n{label}")
        outs = {name: results[(label, name)][0] for name, _, _, _ in configs}
        t = outs["none"]["time"]
        print(f"{'t':>6}  {'E_off':>9} {'E_1':>9} {'E_4':>9}  "
              f"{'S_off':>9} {'S_1':>9} {'S_4':>9}  "
              f"{'|ω|_off':>9} {'|ω|_1':>9} {'|ω|_4':>9}")
        for i in range(len(t)):
            print(f"{float(t[i]):6.3f}  "
                  f"{float(outs['none']['energy'][i]):9.4e} "
                  f"{float(outs['single']['energy'][i]):9.4e} "
                  f"{float(outs['multi4']['energy'][i]):9.4e}  "
                  f"{float(outs['none']['stretch'][i]):9.4e} "
                  f"{float(outs['single']['stretch'][i]):9.4e} "
                  f"{float(outs['multi4']['stretch'][i]):9.4e}  "
                  f"{float(outs['none']['max_vort'][i]):9.4e} "
                  f"{float(outs['single']['max_vort'][i]):9.4e} "
                  f"{float(outs['multi4']['max_vort'][i]):9.4e}")
    return results


if __name__ == "__main__":
    main()

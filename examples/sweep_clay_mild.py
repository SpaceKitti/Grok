"""Rank milder clay settings on tubes + 4-scar (N=64, t≈0.45).

    python examples/sweep_clay_mild.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import run_framework, DEFAULT_CLAY, default_scar_centres


def _metrics(out):
    e0, e1 = float(out["energy"][0]), float(out["energy"][-1])
    w0 = float(out["max_vort"][0])
    return {
        "dE": 100.0 * (e0 - e1) / e0,
        "w0": w0,
        "w1": float(out["max_vort"][-1]),
        "w_peak": float(out["max_vort"].max()),
        "bkm": float(out["bkm_integral"][-1]),
        "stretch": float(out["stretch"].max()),
        "tau": float(out["max_tau"].max()),
        "t": float(out["time"][-1]),
    }


def main():
    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=64, steps=280, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=40,
    )
    cases = [
        ("NS", None),
        ("old", dict(DEFAULT_CLAY)),
        ("eta_p=0.003", dict(DEFAULT_CLAY, eta_p=0.003)),
        ("eta_p=0.002", dict(DEFAULT_CLAY, eta_p=0.002)),
        ("lam=1.5", dict(DEFAULT_CLAY, lambda_relax=1.5)),
        ("gum=0", dict(DEFAULT_CLAY, gum_scale=0.0)),
        ("gain=0", dict(DEFAULT_CLAY, clay_gain=0.0)),
        ("mild-combo", dict(DEFAULT_CLAY, eta_p=0.003, lambda_relax=1.5,
                            gum_scale=0.25, clay_gain=0.01)),
    ]
    rows = []
    for name, params in cases:
        print(f"--- {name} ---", flush=True)
        if params is None:
            out = run_framework(mode="vorticity", viscoelastic=False, **common)
        else:
            out = run_framework(mode="clay", viscoelastic=True,
                                clay_params=params, **common)
        m = _metrics(out)
        m["name"] = name
        rows.append(m)
        print(f"    t={m['t']:.3f}  dE={m['dE']:.2f}%  "
              f"max|w| {m['w0']:.2f}->{m['w1']:.2f} (peak {m['w_peak']:.2f})  "
              f"BKM={m['bkm']:.3f}  stretch={m['stretch']:.3f}  "
              f"max|tau|={m['tau']:.4f}", flush=True)

    ns = next(r for r in rows if r["name"] == "NS")
    print("\n========== Ranking (N=64, t≈0.42) ==========")
    print(f"{'case':<14} {'ΔE%':>7} {'w_end':>8} {'w_peak':>8} {'BKM':>8} "
          f"{'stretch':>8} {'max|τ|':>8}  {'sup%':>6}")
    for r in rows:
        # suppression of end-state max|ω| relative to NS rise from w0
        sup = 100.0 * (ns["w1"] - r["w1"]) / (ns["w1"] - ns["w0"] + 1e-12)
        print(f"{r['name']:<14} {r['dE']:7.2f} {r['w1']:8.3f} {r['w_peak']:8.3f} "
              f"{r['bkm']:8.3f} {r['stretch']:8.3f} {r['tau']:8.4f}  {sup:6.1f}")
    return rows


if __name__ == "__main__":
    main()

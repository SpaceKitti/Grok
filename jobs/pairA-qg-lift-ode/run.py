"""Solve r(χ). F fixed. Einstein+Λ first solver."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))

from load_have import EPS_EP, TAU
from ode_r import integrate_from_bolt, residual_E, seed_R1, seed_R2
from residuals import seed_report


def regular_at_bolts(sol) -> dict:
    if sol is None or not sol.success:
        return {"regular": False, "r_end": np.nan, "rp_end": np.nan, "r_min": np.nan}
    chi = sol.t
    r, rp = sol.y
    r_min = float(np.min(r))
    rp_end = float(rp[-1])
    # r'(π)≈0 and r>0
    ok = bool(sol.success and r_min > 1e-4 and abs(rp_end) < 0.05)
    return {
        "regular": ok,
        "r_end": float(r[-1]),
        "rp_end": rp_end,
        "r_min": r_min,
        "n": int(chi.size),
    }


def main() -> int:
    chi = np.linspace(1e-3, np.pi - 1e-3, 400)
    r1, rp1, rpp1 = seed_R1(chi)
    r2, rp2, rpp2 = seed_R2(chi)
    rep1 = seed_report("R1 r=ε_EP", chi, r1, rp1, rpp1)
    rep2 = seed_report("R2 r=ε_EP sinχ", chi, r2, rp2, rpp2)
    print("R1", rep1)
    print("R2", rep2)

    r0_list = [0.0, 0.3, EPS_EP, 0.7, 1.0, 1.3]
    profiles = {}
    regular = []
    for r0 in r0_list:
        tag = f"r0={r0:g}"
        print("integrate", tag)
        if abs(r0) < 1e-14:
            profiles[tag] = {
                "r0": 0.0,
                "regular": False,
                "note": "R2 tip r0=0: 1/r in the ODE, not started",
            }
            continue
        sol = integrate_from_bolt(float(r0))
        info = regular_at_bolts(sol)
        rec = {"r0": float(r0), **info}
        if sol is not None and sol.t.size:
            rec["chi"] = sol.t
            rec["r"] = sol.y[0]
            rec["rp"] = sol.y[1]
        profiles[tag] = rec
        if info["regular"]:
            regular.append(tag)
        print(" ", info)

    # pack npz: seeds + numeric
    pack = {
        "chi_seed": chi,
        "r_R1": r1,
        "r_R2": r2,
        "E_R1": residual_E(chi, r1, rp1, rpp1),
        "E_R2": residual_E(chi, r2, rp2, rpp2),
        "eps_EP": np.array([EPS_EP]),
        "tau": np.array([TAU]),
    }
    for tag, rec in profiles.items():
        if "chi" in rec:
            key = tag.replace("=", "_").replace(".", "p")
            pack[f"{key}_chi"] = rec["chi"]
            pack[f"{key}_r"] = rec["r"]
    np.savez(OUT / "r_profiles.npz", **pack)

    lam1 = "none"
    if rep1["solved"]:
        lam1 = f"{rep1['Lambda_if_solved']}"
    lam2 = "none"
    if rep2["solved"]:
        lam2 = f"{rep2['Lambda_if_solved']}"

    lines = []
    lines.append("# r(χ) ODE on the lifted chart")
    lines.append("")
    lines.append(f"ε_EP={EPS_EP}")
    lines.append(f"τ={TAU}")
    lines.append("")
    lines.append("ODE (Einstein+Λ, Λ eliminated, a=ε_EP sinχ fixed):")
    lines.append("  r r'' - cot(χ) r r' + (r')² + r² - 1 = 0")
    lines.append("  r'(0)=0, r'(π)=0, r>0 on (0,π)")
    lines.append("")
    lines.append("## Seeds")
    lines.append(
        f"R1 residual rms_E={rep1['rms_E']:.6g} max|E|={rep1['max_abs_E']:.6g}  "
        f"Λ_mean={rep1['Lambda_mean']:.6g} Λ_std={rep1['Lambda_std']:.6g}  "
        f"Λ if solved: {lam1}"
    )
    lines.append(
        f"R2 residual rms_E={rep2['rms_E']:.6g} max|E|={rep2['max_abs_E']:.6g}  "
        f"Λ_mean={rep2['Lambda_mean']:.6g} Λ_std={rep2['Lambda_std']:.6g}  "
        f"Λ if solved: {lam2}"
    )
    lines.append("")
    lines.append("## Numeric profiles regular at both bolts")
    if regular:
        for tag in regular:
            rec = profiles[tag]
            lines.append(
                f"{tag}: r_end={rec['r_end']:.6g} r'(π)={rec['rp_end']:.6g} r_min={rec['r_min']:.6g}"
            )
    else:
        lines.append("none")
    lines.append("")
    lines.append("A B still lifted, C held")
    lines.append("")
    (ROOT / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "summary.json").write_text(
        json.dumps(
            {
                "eps_EP": EPS_EP,
                "tau": TAU,
                "R1": {k: v for k, v in rep1.items() if k != "name"},
                "R2": {k: v for k, v in rep2.items() if k != "name"},
                "regular": regular,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("regular", regular)
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

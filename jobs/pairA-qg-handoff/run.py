"""Pair A handoff: triad, r=0, Wick, Jhat, J on cut, three histories."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))

from gauge_J import run_strip, save as save_Jhat, swap_test
from histories import run_histories
from probe import run as run_probe
from imaginary_flips import flips
from jump_on_cut import run_cut, save as save_Jcut
from r0_bolts import bolts, save_txt
from seed import A, B, EPS_EP, ETA, LAM_EP, V, ep_condition
from tracker import USED_HELPER
from triad import build_triad, save as save_triad
from wick_lorentzian import chart


def fmtM(M: np.ndarray) -> str:
    return np.array2string(M, precision=12, suppress_small=False)


def main() -> int:
    print("USED HELPER:", USED_HELPER)
    print("LAYER 0 Pair A")
    cond = ep_condition(EPS_EP)
    print(f"  a={A} b={B} v={V} eta={ETA}")
    print(f"  eps_EP={EPS_EP} lam_EP={LAM_EP}")
    print(f"  |ε v|={cond['abs_eps_v']:.12g}  |b-a|/2={cond['abs_b_minus_a_over_2']:.12g}  match={cond['match']}")

    print("LAYER T triad")
    tri = build_triad()
    save_triad(tri, OUT / "triad.npz")
    print(f"  n_plus={tri['n_plus']} n_minus={tri['n_minus']} n_join={tri['n_join']}")

    print("LAYER R0")
    r0 = bolts()
    save_txt(r0, OUT / "r0.txt")
    print(f"  bolts eps={r0['eps']}  tau={r0['tau']}")

    print("LAYER W")
    w = chart()
    print(f"  real-section support = {w['real_section_support']}")
    print(f"  dies at ±ε_EP = {w['dies_at']}")

    print("LAYER 1 strip U(1)")
    strip = run_strip()
    save_Jhat(strip, OUT / "Jhat.npz")
    sw = swap_test(strip["V0"], strip["V2PI"], strip["V4PI"])
    print("PASTE BACK")
    print(f"  r={strip['r']}")
    print(f"  phi={strip['phi']}")
    print(f"  Jhat2=\n{fmtM(strip['Jhat2'])}")
    print(f"  Jhat4=\n{fmtM(strip['Jhat4'])}")
    print(f"  det Jhat2={strip['det_Jhat2']}")
    print(f"  det Jhat4={strip['det_Jhat4']}")
    print(f"  ||Jhat4-I||_F={strip['fro_Jhat4_I']}")
    print(f"  ||Jhat2@Jhat2-I||_F={strip['fro_Jhat2sq_I']}")
    print(f"  swap V0 vs V2PI |ov|=\n{sw['V0_vs_V2']}")
    print(f"  swap V0 vs V4PI |ov|=\n{sw['V0_vs_V4']}")

    print("LAYER F flips")
    fl = flips(strip)
    print(f"  2π swap={fl['swap_2pi']}  4π return={fl['return_4pi']}  Jhat2^2=I={fl['Jhat2_is_involution']}")

    print("LAYER 2 J on cut")
    cut = run_cut()
    save_Jcut(cut, OUT / "J_on_cut.npz")
    print(f"  n_points={cut['n_points']}  tip+ defective={cut['tips'][1]['defective']}  tip- defective={cut['tips'][-1]['defective']}")

    print("LAYER 4 histories")
    hist = run_histories()
    for k in "ABC":
        h = hist[k]
        print(f"  {h['name']}: ReI={h['Re']:.8g} ImI={h['Im']:.8g} inter={h['intersection']} {h['score']}")
    print("FIXED")

    print("QG PROBE")
    pr = run_probe(hist, strip, r0)
    print("  P1", {k: pr["p1"][k]["result"] for k in pr["p1"]})
    print("  P3", pr["p3"]["result"])
    print("  allowed past Wick:", pr["p2"]["allowed_past_Wick"], "held:", pr["p2"]["held"])

    lines = []
    lines.append("# Pair A QG handoff")
    lines.append("")
    lines.append(f"USED HELPER: `{USED_HELPER}`")
    lines.append("")
    lines.append("## Pair A numbers")
    lines.append(f"a={A}  b={B}  v={V}  η={ETA}")
    lines.append(f"ε_EP={EPS_EP}  λ_EP={LAM_EP}")
    lines.append(f"EP check |ε v|={cond['abs_eps_v']:.12g} vs |b-a|/2={cond['abs_b_minus_a_over_2']:.12g} match={cond['match']}")
    lines.append("Dirichlet slab. Two Alfvén labels. H_A is the cut Hamiltonian.")
    lines.append("")
    lines.append("## Triad legs and n_points")
    lines.append("Triad = two real sheets + joining structure on Γ (not a two-arm fork).")
    lines.append(f"leg plus (real sheet +): n={tri['n_plus']}")
    lines.append(f"leg minus (real sheet −): n={tri['n_minus']}")
    lines.append(f"leg join (complex pair on Γ, tips ±ε_EP): n={tri['n_join']}")
    lines.append("")
    lines.append("## r=0 bolts")
    lines.append(f"ε=ε_EP cos χ. bolts χ=0 → ε={r0['eps'][0]}, χ=π → ε={r0['eps'][1]}")
    lines.append(f"period τ=4π/ε_EP={r0['tau']:.12f}")
    lines.append("")
    lines.append("## Wick/Lorentzian")
    lines.append("real-section support = Γ")
    lines.append("dies at ±ε_EP")
    lines.append("")
    lines.append("## flip")
    lines.append("2π swap, 4π return")
    lines.append(f"swap_2pi={fl['swap_2pi']}  return_4pi={fl['return_4pi']}  Jhat2^2=I={fl['Jhat2_is_involution']}")
    lines.append("")
    lines.append("## φ and ||Jhat4-I||")
    lines.append(f"φ={strip['phi']}")
    lines.append(f"||Jhat4-I||_F={strip['fro_Jhat4_I']}")
    lines.append(f"||Jhat2@Jhat2-I||_F={strip['fro_Jhat2sq_I']}")
    lines.append("")
    lines.append("## J(z) n_points on Γ")
    lines.append(f"n_points={cut['n_points']} (odd, includes 0 and both tips)")
    lines.append(
        f"J(+ε_EP) defective={cut['tips'][1]['defective']} rank={cut['tips'][1]['rank']} geom={cut['tips'][1]['geom_mult']}"
    )
    lines.append(
        f"J(−ε_EP) defective={cut['tips'][-1]['defective']} rank={cut['tips'][-1]['rank']} geom={cut['tips'][-1]['geom_mult']}"
    )
    lines.append("endpoint holonomy = Jhat2 (Layer 1 gauge)")
    lines.append("")
    lines.append("## A/B/C scores")
    for k in "ABC":
        h = hist[k]
        lines.append(
            f"{h['name']}: Re I={h['Re']:.8g}  Im I={h['Im']:.8g}  "
            f"intersection={h['intersection']}  {h['score']}"
        )
    lines.append("")
    path = ROOT / "RESULTS.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "summary.json").write_text(
        json.dumps(
            {
                "a": A, "b": B, "v": V, "eta": ETA,
                "eps_EP": EPS_EP,
                "n_plus": tri["n_plus"], "n_minus": tri["n_minus"], "n_join": tri["n_join"],
                "tau": r0["tau"],
                "phi": strip["phi"],
                "fro_Jhat4_I": strip["fro_Jhat4_I"],
                "fro_Jhat2sq_I": strip["fro_Jhat2sq_I"],
                "n_J_on_cut": cut["n_points"],
                "hist": {k: {"Re": hist[k]["Re"], "Im": hist[k]["Im"], "score": hist[k]["score"]} for k in "ABC"},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

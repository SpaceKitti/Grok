"""Lift A,B onto S²/4d charts. C held. No new Pair A Hamiltonian."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))

from bolts import poles
from lift_metric import F
from load_surface import EPS_EP, I_A, I_B, LAM_EP, TAU, load_jhat
from sheets_AB import build_sheets, save as save_sheets


def main() -> int:
    jh = load_jhat()
    print("LOADED Jhat from", jh["path"])
    print(f"ε_EP={EPS_EP}  τ={TAU}  I_A={I_A}  I_B={I_B}")

    Fp, Fm = F(EPS_EP), F(-EPS_EP)
    print(f"F(+ε_EP)={Fp}  F(-ε_EP)={Fm}")

    pol = poles()
    print("R1 r=ε_EP  r(0)=", pol["r_charts"]["R1"]["r_chi0"], "bolt", pol["R1_bolt"])
    print("R2 r=ε_EP sinχ  r(0)=", pol["r_charts"]["R2"]["r_chi0"], "bolt", pol["R2_bolt"])
    print("4π cover", pol["reg"]["four_pi_cover"], "2π polar", pol["reg"]["two_pi_polar"])
    print("ε_EP * τ =", pol["reg"]["eps_EP_times_tau"], "(want 4π)")

    sh = build_sheets()
    save_sheets(sh, OUT / "sheets_AB.npz")
    print("A lifted  B lifted  C held")

    lines = []
    lines.append("# Pair A lift to S² / 4d chart")
    lines.append("")
    lines.append(f"ε_EP={EPS_EP}")
    lines.append(f"λ_EP={LAM_EP}")
    lines.append(f"τ={TAU}")
    lines.append(f"I_A={I_A}")
    lines.append(f"I_B={I_B}")
    lines.append("")
    lines.append("## F zeros")
    lines.append(f"F(+ε_EP)={Fp}")
    lines.append(f"F(-ε_EP)={Fm}")
    lines.append("")
    lines.append("## Bolts")
    lines.append(f"R1 bolt {pol['R1_bolt']}  (product r=ε_EP, r(0)=ε_EP≠0)")
    lines.append(f"R2 bolt {pol['R2_bolt']}  (round r=ε_EP sinχ, r(0)=0)")
    lines.append(
        f"(χ,τ) circumference/radius = ε_EP·τ = {pol['reg']['eps_EP_times_tau']:.6f} "
        f"(4π-cover {pol['reg']['four_pi_cover']}, 2π-polar {pol['reg']['two_pi_polar']})"
    )
    lines.append("Poles = χ=0,π = ±ε_EP. GoldbergHexa S².")
    lines.append("")
    lines.append("A lifted  B lifted  C held")
    lines.append("")
    lines.append("next is the ODE for r(ε) if you want a solved 4d metric")
    lines.append("")
    (ROOT / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "summary.json").write_text(
        json.dumps(
            {
                "eps_EP": EPS_EP,
                "tau": TAU,
                "F_plus": Fp,
                "F_minus": Fm,
                "R1_bolt": pol["R1_bolt"],
                "R2_bolt": pol["R2_bolt"],
                "A_lifted": True,
                "B_lifted": True,
                "C_held": True,
                "jhat_path": jh["path"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

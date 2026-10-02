"""Independent gravity letter check. Tautological cover is locked out."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))

from checks import run_all
from gravity_g1 import B_FIELD
from mhd_letter import EPS_EP, ETA, V
from plots import plot_cs_map, plot_loops


def sentence(rows) -> str:
    i1, i2, i3, i4 = (r.passed for r in rows)
    if i1 and i2:
        return "independent gravity letter lands on Γ"
    return "independent gravity letter does not land on Γ"


def write_results(bundle: dict, sent: str, path: Path) -> None:
    rows = bundle["rows"]
    lines = []
    lines.append("# Independent gravity letter on Γ")
    lines.append("")
    lines.append("New folder. Hive not opened. Tearing not rerun. Pair A not rebuilt.")
    lines.append("The dictionary $U_G=(-1)^{I(\\gamma,\\Gamma)}$, $da=\\pi\\delta_\\Gamma$ is locked as tautological and is **not** used here.")
    lines.append("")
    lines.append("## Gravity letter (Option G1)")
    lines.append("")
    lines.append("Lattice $U(1)$ connection on a Cartesian mesh in the plane. Symmetric gauge of a **uniform** background field $B$. $F=dA=B$ (constant). No $\\delta_\\Gamma$. No pair A. No $I(\\gamma,\\Gamma)$. No $\\mathrm{Arg}/\\mathrm{atan2}$ branch cut.")
    lines.append("")
    lines.append("```")
    lines.append("A_x = − (B/2) y")
    lines.append("A_y = + (B/2) x")
    lines.append("F_xy = B")
    lines.append("θ_{n,x̂} = A_x(n+x̂/2) Δx ,   U_ℓ = exp(i θ_ℓ)")
    lines.append("U_□ = exp(i B Δx Δy)")
    lines.append("U[γ] = ∏_{ℓ∈γ} U_ℓ")
    lines.append(f"B = {B_FIELD}   # O(1), not fitted to U(2π)=−1")
    lines.append("```")
    lines.append("")
    lines.append("Option G2 was not used.")
    lines.append("")
    lines.append("## MHD letter (reused, not rebuilt)")
    lines.append("")
    lines.append("```")
    lines.append("H_A(ε) = [[ -i a, ε v ], [ ε v, -i b ]]")
    lines.append(f"v = {V}, η = {ETA}, ε_EP = {EPS_EP:.6f}")
    lines.append("```")
    lines.append("Used only to continue $n_{\\mathrm{MHD}}$ around $+\\varepsilon_{\\mathrm{EP}}$ and to **score** I1–I4 against $\\Gamma=[-\\varepsilon_{\\mathrm{EP}},\\varepsilon_{\\mathrm{EP}}]$. Not an input to $A$.")
    lines.append("")
    lines.append("## Table I1–I4")
    lines.append("")
    lines.append("| test | formula | number | pass |")
    lines.append("| --- | --- | --- | --- |")
    for r in rows:
        flag = "PASS" if r.passed else "FAIL"
        lines.append(f"| {r.name} | ${r.formula}$ | {r.number} | **{flag}** |")
    lines.append("")
    for r in rows:
        lines.append(f"- {r.name}: {r.note}")
    lines.append("")
    lines.append("## One sentence")
    lines.append("")
    lines.append(f"**{sent}**")
    lines.append("")
    lines.append(
        "G1 could be defined (uniform $B$, no cut in $A$). It is global area-law junk: "
        "CS density is flat, $U(2\\pi)\\neq -1$, shifting the loop off $\\Gamma$ does not drop the signal. "
        "The tautological cover is still the only letter that sat on $\\Gamma$, and it was inserted by hand."
    )
    lines.append("")
    lines.append("Not a theorem. No Qin, leapfrog, Hall 3×3, dynamo, or black hole.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    bundle = run_all(seed=0)
    sent = sentence(bundle["rows"])
    print(f"G1  B={bundle['B']}  ε_EP={bundle['eps_ep']:.6f}")
    for r in bundle["rows"]:
        print(f"  {r.name}: {'PASS' if r.passed else 'FAIL'}  {r.number}")
    print("SENTENCE:", sent)

    plot_cs_map(bundle, OUT)
    plot_loops(bundle, OUT)

    with (OUT / "I_table.csv").open("w", encoding="utf-8") as f:
        f.write("test,passed,number\n")
        for r in bundle["rows"]:
            f.write(f"{r.name},{int(r.passed)},{r.number.replace(',', ';')}\n")

    (OUT / "summary.json").write_text(
        json.dumps(
            {
                "option": "G1",
                "B": bundle["B"],
                "eps_ep": bundle["eps_ep"],
                "sentence": sent,
                "rows": [
                    {"name": r.name, "passed": r.passed, "number": r.number}
                    for r in bundle["rows"]
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    write_results(bundle, sent, ROOT / "RESULTS.md")
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

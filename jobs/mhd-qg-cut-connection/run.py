"""
MHD–QG cut connection. One job, one report.
Tearing not rerun. Same-ε EP2 theorem not rerun.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))

from connection import run_all
from mhd import ETA, coupling_v, damp_n
from plots import plot_c4, plot_gamma_sheets


def sentence(passed: list[str]) -> str:
    if not passed:
        return "no connection found on this stack"
    kinds = {
        "C1": "C1 shared support",
        "C2": "C2 shared sheet jump",
        "C3": "C3 jump map",
        "C4": "C4 residual lock",
    }
    named = [kinds[p] for p in passed if p in kinds]
    return "connection type found: " + " + ".join(named)


def write_results(bundle: dict, path: Path, sent: str) -> None:
    ep = bundle["eps_ep"]
    eps = bundle["eps_slit"]
    rows = bundle["rows"]
    v = coupling_v()
    a, b = damp_n(1), damp_n(2)
    lines: list[str] = []
    lines.append("# MHD–QG cut connection")
    lines.append("")
    lines.append("New folder. Hive not opened. Tearing not rerun. Same-ε EP₂ theorem not rerun.")
    lines.append("")
    lines.append("Locked: tearing is Δ'>0 FKR, not an EP₂. Pair A is a label 2×2 on Γ, not “the MHD operator.”")
    lines.append("Ohmic vs CS do not form an EP₂ at pair A’s ε. Connection ≠ same operator.")
    lines.append("")
    lines.append("## (0) Geometry of Γ")
    lines.append("")
    lines.append(rf"Slit $\Gamma=[-|\varepsilon|,|\varepsilon|]$ at working $\varepsilon=\varepsilon_{{\mathrm{{EP}}}}={ep:.4f}$.")
    lines.append(r"Two sheets glued along $\Gamma$. Endpoints are square-root branch points. Standard faces: Arg $=+\pi$ / $-\pi$.")
    lines.append("Figure: `outputs/0_gamma_two_sheets.png`.")
    jmp = bundle["c2_extras"]["jump"]
    lines.append(
        f"Label-2×2 jump around the $+$ endpoint: swap at 2π={jmp['swapped_2pi']}, "
        f"$\\Delta n_{{\\mathrm{{MHD}}}}(2\\pi)={jmp['dn_2pi']}$, "
        f"$\\Delta n_{{\\mathrm{{MHD}}}}(4\\pi)={jmp['dn_4pi']}$."
    )
    lines.append("Exports `n_sheet`, `Arg_Γ`, jump in `outputs/track0_exports.npz` / `outputs/C_table.csv`.")
    lines.append("")
    lines.append("## (1) MHD letter — pair A (not tearing)")
    lines.append("")
    lines.append(r"Generator $A=\varepsilon x + i\eta\partial_{xx}$ on $[-1,1]$, two Dirichlet sines.")
    lines.append("")
    lines.append("```")
    lines.append(f"H_A(ε) = [[ -i a,  ε v ],")
    lines.append(f"          [  ε v, -i b ]]")
    lines.append(f"a = η(π/2)^2 = {a:.6g}")
    lines.append(f"b = η π^2     = {b:.6g}")
    lines.append(f"v = ⟨φ1, x φ2⟩ = {v:.6g}")
    lines.append(f"η = {ETA}")
    lines.append(f"ε_EP = |b-a|/(2|v|) = {ep:.6g}")
    lines.append("```")
    lines.append("Letters: two field-line / Alfvén labels. Continuum interval Γ=[−|ε|,|ε|].")
    lines.append("Locked N×N fact: the continuum is a cut (min gap ~0.05); discrete EP₂ lives only in this 2×2 map.")
    lines.append("")
    lines.append("## (2) Gravity letter — separate operator on the same Γ")
    lines.append("")
    lines.append("Not pair A’s matrix. No EP₂ demand at ε=0.514.")
    lines.append("")
    lines.append("```")
    lines.append("da = π δ_Γ                         # Z2 / square-root edge defect")
    lines.append("U_G[γ] = exp(i π I(γ, Γ)) = (−1)^{I(γ,Γ)}")
    lines.append("ΔCS[γ] = I(γ, Γ)/2")
    lines.append("U_G(θ) = exp(i θ/2) around one endpoint   # U(2π)=−1, U(4π)=+1")
    lines.append("```")
    lines.append("This is a discrete holonomy / spin-foam edge sitting on Γ, not a 2×2 fusion.")
    lines.append("")
    lines.append("## (3) Connection table C1–C4")
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
    lines.append("Coordinate for C4 is arc length $s$ at one $\\varepsilon$ (the slit at $\\varepsilon_{\\mathrm{EP}}$). No collage of different $\\varepsilon$ into one point.")
    lines.append("Figure: `outputs/4_C4_overlay.png`.")
    lines.append("")
    lines.append("## (4) One sentence")
    lines.append("")
    lines.append(f"**{sent}**")
    lines.append("")
    lines.append(
        "Named type only. Not a theorem. Not “they are the same operator.” "
        "C1 and C4 are support of the slit (Track 2 sits on Γ). "
        "C2 and C3 are the non-tautological dictionary: MHD continuation and the π-flux covering share $\\Delta n$ and $\\Phi(n)=U_G$."
    )
    lines.append("No Qin, no leapfrog, no Hall 3×3, no dynamo phenomenology, no black-hole claim.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    bundle = run_all()
    sent = sentence(bundle["passed_ids"])
    print("eps_EP", bundle["eps_ep"], "eps_slit", bundle["eps_slit"])
    for r in bundle["rows"]:
        print(f"  {r.name}: {'PASS' if r.passed else 'FAIL'}  {r.number}")
    print("SENTENCE:", sent)

    jump = bundle["c2_extras"]["jump"]
    plot_gamma_sheets(bundle["eps_slit"], jump, OUT)
    plot_c4(bundle["c4_extras"], OUT)

    arg = jump["arg_split"]
    np.savez(
        OUT / "track0_exports.npz",
        theta=jump["theta"],
        n_sheet_MHD=jump["n_sheet"],
        Arg_split=arg,
        n_sheet_QG=bundle["c2_extras"]["n_qg"],
        U_G=bundle["c2_extras"]["U"],
        evals=jump["evals"],
        eps_ep=np.array([bundle["eps_ep"]]),
        s=bundle["c4_extras"]["s"],
        R_MHD=bundle["c4_extras"]["R_mhd"],
        R_QG=bundle["c4_extras"]["R_qg"],
        Gamma_lo=np.array([bundle["c4_extras"]["lo"]]),
        Gamma_hi=np.array([bundle["c4_extras"]["hi"]]),
    )

    with (OUT / "C_table.csv").open("w", encoding="utf-8") as f:
        f.write("test,passed,number,formula\n")
        for r in bundle["rows"]:
            num = r.number.replace(",", ";")
            f.write(f"{r.name},{int(r.passed)},{num},{r.formula}\n")

    summary = {
        "passed": bundle["passed_ids"],
        "sentence": sent,
        "eps_ep": bundle["eps_ep"],
        "eps_slit": bundle["eps_slit"],
        "rows": [
            {"name": r.name, "passed": r.passed, "number": r.number, "formula": r.formula}
            for r in bundle["rows"]
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_results(bundle, ROOT / "RESULTS.md", sent)
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
Object C — candidate operator for Akitti's branch cut.
Tearing is closed (read as a negative). This folder does not reopen it.
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

from pair_A import H_A, eps_ep_analytic, score_A, sweep_A, sweep_N
from pair_B import H_B1, H_B2, score_B1, score_B2, sweep_B
from plots import plot_N_check, plot_pair


def _chk_dict(c) -> dict:
    return {
        "ep2_found": c.ep2_found,
        "jordan": c.jordan,
        "puiseux_half": c.puiseux_half,
        "mono_4pi": c.mono_4pi,
        "on_cut": c.on_cut,
        "passed": c.passed,
        "exponent": c.exponent,
        "eps_ep": c.eps_ep,
        "lam_ep": repr(c.lam_ep),
        "Gamma": c.Gamma,
        "notes": c.notes,
        "petermann": c.petermann,
        "defect": c.defect,
    }


def verdict(A, B1, B2) -> str:
    a, b1, b2 = A["checklist"], B1["checklist"], B2["checklist"]
    same = False
    if a.ep2_found and b2.ep2_found and a.eps_ep == a.eps_ep and b2.eps_ep == b2.eps_ep:
        rel = abs(a.eps_ep - b2.eps_ep) / (abs(a.eps_ep) + abs(b2.eps_ep) + 1e-16)
        same = bool(rel < 0.15 and a.on_cut and b2.on_cut)
    if a.passed and b2.passed and same:
        return "cut-operator found"
    if a.passed and not (b1.passed or (b2.passed and same)):
        return "one-sided"
    if (b1.passed or b2.passed) and not a.passed:
        return "one-sided"
    if a.ep2_found or b2.ep2_found:
        # EP exists but checklist incomplete, or two-sided ε mismatch
        if a.passed or b2.passed:
            return "one-sided"
        return "cut-operator not found"
    return "cut-operator not found"


def write_results(A, B1, B2, Ninfo, path: Path, sent: str) -> None:
    a, b1, b2 = A["checklist"], B1["checklist"], B2["checklist"]
    lines = []
    lines.append("# Object C — branch-cut operator")
    lines.append("")
    lines.append("New folder. Hive not opened. Tearing not re-tested.")
    lines.append("Negative input: `ep-reconnection-operator/RESULTS.md` — Δ'>0 FKR, not an EP₂.")
    lines.append("GSG 2004 is used as a 2×2 recipe, not as a dynamo.")
    lines.append("")
    lines.append("## Matrix definitions")
    lines.append("")
    lines.append("### Pair A — two Alfvén labels on Γ (derived, not a dynamo rename)")
    lines.append("")
    lines.append("Generator: $A = \\varepsilon x + i\\eta\\partial_{xx}$ on $x\\in[-1,1]$ (Dirichlet).")
    lines.append(r"Ideal spectrum of $\varepsilon x$ is the cut $\Gamma(\varepsilon)=[-|\varepsilon|,|\varepsilon|]$.")
    lines.append("Two-mode Galerkin on $\\varphi_n=\\sin\\bigl(n\\pi(x+1)/2\\bigr)$, $n=1,2$:")
    lines.append("")
    lines.append(f"`{A['matrix_form']}`")
    lines.append("")
    lines.append(f"Explicit numbers: $v={A['v']:.6g}$, $\\eta={A['eta']}$.")
    lines.append("Off-diagonal is Hermitian shear; diagonal is unequal Ohmic loss. Not the GSG dynamo matrix.")
    lines.append("")
    lines.append("### Pair B — two readings of the same meridian")
    lines.append("")
    lines.append(f"B1 (dissipation vs CS defect at 0): `{B1['matrix_form']}`")
    lines.append(f"B2 (GSG grading, MHD shear vs CS/Landau width): `{B2['matrix_form']}`")
    lines.append("")
    lines.append("Shared parameter $\\varepsilon$ = shear. $\\eta$ = resistivity-as-cut-width, held fixed.")
    lines.append("")
    lines.append("## Pair A checklist")
    lines.append("")
    lines.append(f"- EP₂ found: **{a.ep2_found}** at $\\varepsilon={a.eps_ep}$, $\\lambda={a.lam_ep}$")
    lines.append(f"- Jordan (alg 2, geom 1): **{a.jordan}**")
    lines.append(f"- Puiseux $p=1/2$: **{a.puiseux_half}** (fitted $p={a.exponent:.4f}$)")
    lines.append(f"- 4π monodromy: **{a.mono_4pi}**")
    lines.append(f"- On the cut $\\Gamma={a.Gamma}$: **{a.on_cut}**")
    lines.append(f"- Pair A overall: **{'PASS' if a.passed else 'FAIL'}**")
    lines.append(f"- N×N least-damped pair min gap: {Ninfo['min_gap']:.4g} (continuum discretisation, not used as the operator).")
    lines.append("")
    lines.append("## Pair B checklist")
    lines.append("")
    lines.append(f"- B1 EP₂: **{b1.ep2_found}** — {b1.notes}")
    lines.append(
        f"- B2 EP₂: **{b2.ep2_found}** at $\\varepsilon={b2.eps_ep}$, $\\lambda={b2.lam_ep}$; "
        f"Jordan={b2.jordan}, Puiseux={b2.puiseux_half} ($p={b2.exponent}$), "
        f"4π={b2.mono_4pi}, on cut={b2.on_cut}. Overall **{'PASS' if b2.passed else 'FAIL'}**."
    )
    if a.ep2_found and b2.ep2_found:
        rel = abs(a.eps_ep - b2.eps_ep) / (abs(a.eps_ep) + abs(b2.eps_ep) + 1e-16)
        lines.append(
            f"- Same $\\varepsilon$? relative distance {rel:.3f} "
            f"(A at {a.eps_ep:.4g}, B2 at {b2.eps_ep:.4g}). "
            f"{'YES — both readings meet.' if rel < 0.15 else 'NO — not a MHD–QG theorem.'}"
        )
    lines.append("")
    lines.append("## One sentence")
    lines.append("")
    lines.append(f"**{sent}**")
    lines.append("")
    if sent == "one-sided":
        lines.append(
            "An EP₂ lives on the MHD label/cut 2×2 (pair A) and/or on the GSG-graded slit (B2), "
            "but the two readings do not share a critical $\\varepsilon$. Keep CS orthogonal to a QG claim."
        )
    elif sent == "cut-operator not found":
        lines.append("No EP₂ of branching type on the cut. Candidate failed. Did not fall back to tearing.")
    else:
        lines.append("Both readings meet at the same $\\varepsilon$ on $\\Gamma$. Still no Qin/leapfrog write.")
    lines.append("")
    lines.append("No Qin. No leapfrog. No black-hole or spin-foam theorem.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    print("=== OBJECT C pair A : Alfvén labels on Γ ===")
    A = score_A()
    ca = A["checklist"]
    print(A["matrix_form"])
    print(f"  EP2={ca.ep2_found} jordan={ca.jordan} p={ca.exponent:.4f} "
          f"puis={ca.puiseux_half} 4pi={ca.mono_4pi} oncut={ca.on_cut} "
          f"eps={ca.eps_ep:.6g} lam={ca.lam_ep}")
    print(f"  PASS={ca.passed}")

    eps_grid = np.linspace(-2.5 * max(ca.eps_ep, 0.2), 2.5 * max(ca.eps_ep, 0.2), 401)
    swA = sweep_A(eps_grid)
    swN = sweep_N(np.linspace(0.0, 2.5 * max(ca.eps_ep, 0.2), 41), n=81)
    Ninfo = {"min_gap": float(np.min(swN["gap"][1:] if swN["gap"].size > 1 else swN["gap"]))}
    print(f"  N×N min gap (least-damped pair)={Ninfo['min_gap']:.4g}")

    print("=== OBJECT C pair B : MHD dissipation vs CS on the same meridian ===")
    B1 = score_B1()
    B2 = score_B2()
    print(B1["matrix_form"], "EP2", B1["checklist"].ep2_found, B1["checklist"].notes)
    cb = B2["checklist"]
    print(B2["matrix_form"], f"EP2={cb.ep2_found} PASS={cb.passed} eps={cb.eps_ep} p={cb.exponent}")

    swB1 = sweep_B(H_B1, eps_grid)
    swB2 = sweep_B(H_B2, eps_grid)

    sent = verdict(A, B1, B2)
    print("VERDICT:", sent)

    plot_pair("A_labels", swA, A, OUT)
    plot_pair("B1_ohm_cs", swB1, B1, OUT)
    plot_pair("B2_GSG_slit", swB2, B2, OUT)
    plot_N_check(swN, ca.eps_ep if ca.eps_ep == ca.eps_ep else 0.0, OUT)

    np.savez(
        OUT / "objectC_data.npz",
        eps_A=swA["eps"],
        ev_A=swA["evals"],
        gap_A=swA["gap"],
        eps_B2=swB2["eps"],
        ev_B2=swB2["evals"],
        eps_N=swN["eps"],
        ev_N=swN["evals"],
    )
    summary = {
        "pair_A": _chk_dict(ca),
        "pair_B1": _chk_dict(B1["checklist"]),
        "pair_B2": _chk_dict(cb),
        "NxN_min_gap": Ninfo["min_gap"],
        "verdict": sent,
        "matrix_A": A["matrix_form"],
        "matrix_B1": B1["matrix_form"],
        "matrix_B2": B2["matrix_form"],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    write_results(A, B1, B2, Ninfo, ROOT / "RESULTS.md", sent)
    print("Wrote RESULTS.md and outputs/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

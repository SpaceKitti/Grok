"""
P1 — CS connection change across γ_cross.

U(1)_k CS, k=8. Vacuum A=0 (F=0, no δ_Γ source).
Letter along a segment: ∫ A·dl = 0.
J = |∫_{γ} A|  (before/after is the same vacuum).
Not copied from n_MHD.
"""

from __future__ import annotations

from protocol import X_OFF, X_ON, ratio, verdict, z_after, z_before

K_CS = 8


def operator_block() -> str:
    return (
        "P1  U(1)_k CS, k=8, vacuum A_ℓ=0\n"
        "    S_CS=(k/4π)∫ A dA,  eom F=0\n"
        "    J=|∫_γ A·dl|"
    )


def line_integral_A(x: float) -> float:
    return 0.0


def run() -> dict:
    j_on = abs(line_integral_A(X_ON))
    j_off = abs(line_integral_A(X_OFF))
    r = ratio(j_on, j_off)
    passed = bool(r >= 3.0 and j_on > 1e-9)
    return {
        "family": "P1 CS",
        "operator": operator_block(),
        "J_on": j_on,
        "J_off": j_off,
        "ratio": r,
        "passed": passed,
        "verdict": verdict(passed, False, True, False),
        "defined_without_mhd": True,
        "inserted": False,
    }

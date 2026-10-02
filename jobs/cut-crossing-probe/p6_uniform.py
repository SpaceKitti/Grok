"""
P6 — uniform U(1) control.

  A_x=−(B/2)y, A_y=(B/2)x, B=1
  J = |∫_γ A·dl| along the vertical segment
    path x=const, y: +δ→−δ,  ∫ A_y dy = (B/2) x (−2δ) = −B x δ
  |J| ∝ |x|  → larger OFF the slit than on it.
"""

from __future__ import annotations

from protocol import B_DAMP, DELTA, X_OFF, X_ON, ratio, verdict

B_FIELD = 1.0


def operator_block() -> str:
    return (
        "P6  uniform U(1), B=1\n"
        "    A=(−By/2, Bx/2)\n"
        "    J=|∫_γ A|=|B x δ|"
    )


def J(x: float) -> float:
    return abs(B_FIELD * x * DELTA)


def run() -> dict:
    j_on = J(X_ON)
    j_off = J(X_OFF)
    r = ratio(j_on, j_off)
    passed = bool(r >= 3.0)
    globalish = bool(r < 3.0 and j_on > 1e-12 and j_off > 1e-12)
    return {
        "family": "P6 uniform U(1) control",
        "operator": operator_block(),
        "J_on": j_on,
        "J_off": j_off,
        "ratio": r,
        "passed": passed,
        "verdict": verdict(passed, False, True, globalish),
        "defined_without_mhd": True,
        "inserted": False,
    }

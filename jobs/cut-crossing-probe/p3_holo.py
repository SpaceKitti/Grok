"""
P3 — holographic membrane: jump of the boundary field across the slit.

  3-layer bulk, ds²=dr²+(1+r)² dx²
  Boundary field χ(x+iy) = β x,  β=1/3  (smooth, no cut in the definition)
  J = |χ(x+iδ) − χ(x−iδ)|
"""

from __future__ import annotations

from protocol import DELTA, X_OFF, X_ON, ratio, verdict, z_after, z_before

BETA = 1.0 / 3.0


def operator_block() -> str:
    return (
        "P3  3-layer bulk, χ=βx on the boundary, β=1/3\n"
        "    J=|χ(x+iδ)−χ(x−iδ)|   (smooth field, no slit inserted)"
    )


def chi(z: complex) -> float:
    return BETA * z.real


def J(x: float) -> float:
    return abs(chi(z_before(x)) - chi(z_after(x)))


def run() -> dict:
    j_on = J(X_ON)
    j_off = J(X_OFF)
    r = ratio(j_on, j_off)
    passed = bool(r >= 3.0 and j_on > 1e-9)
    return {
        "family": "P3 holo",
        "operator": operator_block(),
        "J_on": j_on,
        "J_off": j_off,
        "ratio": r,
        "passed": passed,
        "verdict": verdict(passed, False, True, False),
        "defined_without_mhd": True,
        "inserted": False,
    }

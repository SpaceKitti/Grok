"""
P5 — hybrid. Only after P1 and P3 already have rows.
J_h = hypot(J_P1, J_P3) on the same meridian. Not exp(iπ n_MHD).
"""

from __future__ import annotations

import numpy as np

from protocol import ratio, verdict


def operator_block() -> str:
    return (
        "P5  hybrid  J_h = hypot(J_P1_CS, J_P3_holo)\n"
        "    same γ_cross / γ_miss\n"
        "    not exp(iπ n_MHD)"
    )


def run(p1: dict, p3: dict) -> dict:
    _ = (p1["family"], p3["family"])
    j_on = float(np.hypot(p1["J_on"], p3["J_on"]))
    j_off = float(np.hypot(p1["J_off"], p3["J_off"]))
    r = ratio(j_on, j_off)
    passed = bool(r >= 3.0 and j_on > 1e-9)
    return {
        "family": "P5 hybrid",
        "operator": operator_block(),
        "J_on": j_on,
        "J_off": j_off,
        "ratio": r,
        "passed": passed,
        "verdict": verdict(passed, False, True, False),
        "defined_without_mhd": True,
        "inserted": False,
    }

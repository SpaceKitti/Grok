"""
P4 — worldsheet crossing/pinch cost on γ_cross vs γ_miss.

  Nambu length of the short vertical segment: S = 2δ  (same for both)
  No wall factor. Letter = S. J = S (path cost, not a sheet jump).
"""

from __future__ import annotations

from protocol import DELTA, X_OFF, X_ON, ratio, verdict


def operator_block() -> str:
    return (
        "P4  Nambu length of the probe segment\n"
        "    S=∫ds=2δ for both γ_cross and γ_miss\n"
        "    no wall weight in the action"
    )


def nambu(_x: float) -> float:
    return 2.0 * DELTA


def run() -> dict:
    j_on = nambu(X_ON)
    j_off = nambu(X_OFF)
    r = ratio(j_on, j_off)
    passed = bool(r >= 3.0 and abs(j_on - j_off) > 1e-9)
    # equal cost everywhere the path has the same length → global
    globalish = bool(abs(r - 1.0) < 0.05)
    return {
        "family": "P4 worldsheet",
        "operator": operator_block(),
        "J_on": j_on,
        "J_off": j_off,
        "ratio": r,
        "passed": passed,
        "verdict": verdict(passed, False, True, globalish),
        "defined_without_mhd": True,
        "inserted": False,
    }

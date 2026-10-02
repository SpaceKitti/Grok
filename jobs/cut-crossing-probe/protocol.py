"""
Crossing probe: γ_cross through Γ vs γ_miss of equal length that does not hit Γ.
Γ is a score mask, not an input to P1–P6 letters.
"""

from __future__ import annotations

import numpy as np

ETA = 0.05
V = -0.360253
A_DAMP = ETA * (np.pi / 2.0) ** 2
B_DAMP = ETA * np.pi ** 2
EPS_EP = abs(B_DAMP - A_DAMP) / (2.0 * abs(V))
GAMMA = (-EPS_EP, EPS_EP)

# vertical segments, same length 2δ
DELTA = 0.05
X_ON = 0.25  # interior of Γ
X_OFF = 1.20  # real axis but off the slit


def z_before(x: float) -> complex:
    return complex(x, DELTA)


def z_after(x: float) -> complex:
    return complex(x, -DELTA)


def on_gamma_x(x: float) -> bool:
    return GAMMA[0] <= x <= GAMMA[1]


def ratio(j_on: float, j_off: float) -> float:
    return float(abs(j_on) / (abs(j_off) + 1e-16))


def verdict(pass_ratio: bool, inserted: bool, defined: bool, globalish: bool) -> str:
    if not defined:
        return "could not define"
    if inserted:
        return "inserted"
    if pass_ratio:
        return "sees the wall"
    if globalish:
        return "global junk"
    return "misses the wall"

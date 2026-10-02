"""
F5 — Control. Uniform U(1) field (G1 from the independent-check).
COPIED here, not imported from F1 (F1 is CS vacuum, this is uniform B).
Expect FAIL. If this track PASSES, the sweep is broken.

  A_x = −(B/2) y
  A_y = +(B/2) x
  F = B = 1.0   (not fitted to U(2π)=−1)
  U[γ] = exp(i B × Area_swept)
"""

from __future__ import annotations

import numpy as np

from protocol import (
    CENTER_OFF,
    CENTER_ON,
    EPS_EP,
    GAMMA,
    N_THETA,
    R_LOOP,
    loop_points,
    score_S,
)

B_FIELD = 1.0
FAMILY = "F5 uniform U(1) control"
INSERTED = False


def operator_block() -> str:
    return (
        "F5  uniform U(1)  (independent-check G1, copied)\n"
        "    A_x = −(B/2) y ,  A_y = +(B/2) x ,  B=1\n"
        "    U[γ] = exp(i B Area)"
    )


def _dA(z0: complex, z1: complex) -> float:
    x0, y0 = z0.real, z0.imag
    x1, y1 = z1.real, z1.imag
    return 0.5 * B_FIELD * (-y0 * (x1 - x0) + x0 * (y1 - y0))


def holonomy(center: complex) -> np.ndarray:
    theta, z = loop_points(center, N_THETA)
    U = np.ones(theta.size, dtype=complex)
    for i in range(1, theta.size):
        U[i] = U[i - 1] * np.exp(1j * _dA(z[i - 1], z[i]))
    return U


def spatial_means() -> tuple[float, float]:
    """Plaquette |F|/2π is B dx dy / 2π, uniform. on/off = 1."""
    dx = 4.0 / 80.0
    val = abs(B_FIELD * dx * dx / (2.0 * np.pi))
    return val, val


def run(mhd: dict) -> dict:
    U_on = holonomy(CENTER_ON)
    U_off = holonomy(CENTER_OFF)
    son, soff = spatial_means()
    sc = score_S(U_on, U_off, son, soff, mhd["n_sheet"], mhd["i2"], mhd["i4"], True, INSERTED)
    return {
        "family": FAMILY,
        "operator": operator_block(),
        "inserted": INSERTED,
        "defined_without_mhd": True,
        "U_on": U_on,
        "U_off": U_off,
        "score": sc,
    }

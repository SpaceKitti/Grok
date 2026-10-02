"""
MHD letter: locked pair A, reused numerically. Not rebuilt.
ε_EP = 0.513681, η = 0.05, v = -0.360253.
"""

from __future__ import annotations

import numpy as np

ETA = 0.05
V = -0.360253
A_DAMP = ETA * (np.pi / 2.0) ** 2
B_DAMP = ETA * np.pi ** 2
EPS_EP = abs(B_DAMP - A_DAMP) / (2.0 * abs(V))  # 0.513681


def H_A(eps: complex) -> np.ndarray:
    return np.array(
        [[-1j * A_DAMP, eps * V], [eps * V, -1j * B_DAMP]],
        dtype=complex,
    )


def Gamma(eps: float = EPS_EP) -> tuple[float, float]:
    return (-abs(eps), abs(eps))


def n_mhd_around_endpoint(n_theta: int = 721, radius_frac: float = 0.25) -> dict:
    """Continuation of pair A around +ε_EP. Scoring only; not used to build A_gauge."""
    r = radius_frac * EPS_EP
    theta = np.linspace(0.0, 4.0 * np.pi, n_theta)
    z = EPS_EP + r * np.exp(1j * theta)
    evals = np.zeros((n_theta, 2), dtype=complex)
    for i, zi in enumerate(z):
        w = np.linalg.eigvals(H_A(zi))
        if i == 0:
            evals[0] = w
            continue
        d00 = abs(w[0] - evals[i - 1, 0]) + abs(w[1] - evals[i - 1, 1])
        d01 = abs(w[0] - evals[i - 1, 1]) + abs(w[1] - evals[i - 1, 0])
        evals[i] = w[::-1] if d01 < d00 else w
    mid = 0.5 * (evals[0, 0] + evals[0, 1])
    arg = np.unwrap(np.angle(evals[:, 0] - mid))
    n_sheet = np.floor((arg - arg[0]) / np.pi + 1e-9)
    i2 = int(np.argmin(np.abs(theta - 2.0 * np.pi)))
    i4 = n_theta - 1
    return {
        "theta": theta,
        "z": z,
        "evals": evals,
        "n_sheet": n_sheet,
        "dn_2pi": int(n_sheet[i2] - n_sheet[0]),
        "dn_4pi": int(n_sheet[i4] - n_sheet[0]),
        "i2": i2,
        "i4": i4,
        "radius": r,
        "center": EPS_EP,
    }

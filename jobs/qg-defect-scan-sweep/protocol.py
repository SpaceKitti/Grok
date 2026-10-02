"""Locked MHD + shared loop family. Γ is a SCORE mask, never an input to A."""

from __future__ import annotations

import numpy as np

ETA = 0.05
V = -0.360253
A_DAMP = ETA * (np.pi / 2.0) ** 2
B_DAMP = ETA * np.pi ** 2
EPS_EP = abs(B_DAMP - A_DAMP) / (2.0 * abs(V))
R_LOOP = 0.25 * EPS_EP
CENTER_ON = complex(EPS_EP, 0.0)
CENTER_OFF = complex(0.0, 1.2)
N_THETA = 241
GAMMA = (-EPS_EP, EPS_EP)
EXTENT = 2.0
N_GRID = 41  # dx = 0.1


def H_A(eps: complex) -> np.ndarray:
    return np.array(
        [[-1j * A_DAMP, eps * V], [eps * V, -1j * B_DAMP]],
        dtype=complex,
    )


def loop_points(center: complex) -> tuple[np.ndarray, np.ndarray]:
    theta = np.linspace(0.0, 4.0 * np.pi, N_THETA)
    z = center + R_LOOP * np.exp(1j * theta)
    return theta, z


def n_mhd() -> dict:
    theta, z = loop_points(CENTER_ON)
    evals = np.zeros((theta.size, 2), dtype=complex)
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
    i4 = theta.size - 1
    return {
        "theta": theta,
        "z": z,
        "n_sheet": n_sheet,
        "i2": i2,
        "i4": i4,
        "dn_2pi": int(n_sheet[i2] - n_sheet[0]),
        "dn_4pi": int(n_sheet[i4] - n_sheet[0]),
    }


def sites_2d() -> np.ndarray:
    x = np.linspace(-EXTENT, EXTENT, N_GRID)
    X, Y = np.meshgrid(x, x, indexing="xy")
    return (X + 1j * Y).ravel()


def sites_boundary() -> np.ndarray:
    x = np.linspace(-EXTENT, EXTENT, N_GRID)
    return x.astype(complex)


def on_gamma(z: complex, band: float = 0.06) -> bool:
    lo, hi = GAMMA
    return (lo - 1e-12) <= z.real <= (hi + 1e-12) and abs(z.imag) <= band


def winding(loop_z: np.ndarray, p: complex) -> float:
    """Net winding of a closed 0→2π sub-loop about p (first half of 0→4π path)."""
    n = loop_z.size
    z = loop_z[: n // 2 + 1]
    d = z - p
    if np.min(np.abs(d)) < 1e-12:
        return 1.0  # on the contour: count as enclosed
    ang = np.unwrap(np.angle(d))
    return float((ang[-1] - ang[0]) / (2.0 * np.pi))


def running_winding(loop_z: np.ndarray, p: complex) -> np.ndarray:
    ang = np.unwrap(np.angle(loop_z - p))
    return (ang - ang[0]) / (2.0 * np.pi)

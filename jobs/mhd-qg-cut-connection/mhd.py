"""
Track 1 — MHD reading. Pair A label map, restated. Not tearing.
Discrete EP2 lives in this 2×2; the N×N continuum is a cut (locked).
"""

from __future__ import annotations

import numpy as np

ETA = 0.05
OMEGA0 = 0.0


def _sines(x: np.ndarray, n: int) -> np.ndarray:
    return np.sin(n * np.pi * (x + 1.0) / 2.0)


def coupling_v() -> float:
    x = np.linspace(-1.0, 1.0, 4001)
    w = np.trapezoid(_sines(x, 1) * x * _sines(x, 2), x)
    n1 = np.trapezoid(_sines(x, 1) ** 2, x)
    n2 = np.trapezoid(_sines(x, 2) ** 2, x)
    return float(w / np.sqrt(n1 * n2))


def damp_n(n: int, eta: float = ETA) -> float:
    return eta * (n * np.pi / 2.0) ** 2


V = coupling_v()
A_DAMP = damp_n(1)
B_DAMP = damp_n(2)


def H_A(eps: complex, eta: float = ETA) -> np.ndarray:
    """Pair A. Hermitian shear, unequal Ohmic loss. Not the dynamo matrix."""
    v = coupling_v()
    a = damp_n(1, eta)
    b = damp_n(2, eta)
    return np.array([[-1j * a, eps * v], [eps * v, -1j * b]], dtype=complex)


def eps_ep(eta: float = ETA) -> float:
    a, b = damp_n(1, eta), damp_n(2, eta)
    return float(abs(b - a) / (2.0 * abs(coupling_v())))


def Gamma(eps: float) -> tuple[float, float]:
    """Alfvén continuum interval / slit. Γ = [−|ε|, |ε|]."""
    return (-abs(eps), abs(eps))


def lam_A(eps: complex, eta: float = ETA) -> np.ndarray:
    return np.linalg.eigvals(H_A(eps, eta))


def label_split(eps: float, eta: float = ETA) -> float:
    """|Im λ+ − Im λ−|: lights when unique real labeling fails."""
    w = lam_A(complex(eps), eta)
    return float(abs(w[0].imag - w[1].imag))

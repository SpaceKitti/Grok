"""Layer 4 — three histories. I[γ]=∫_γ y dε, y²=4 v² (ε²−ε_EP²)."""

from __future__ import annotations

import numpy as np

from seed import EPS_EP, V


def y_continue(z: np.ndarray) -> np.ndarray:
    y = np.zeros(z.size, dtype=complex)
    for i, zi in enumerate(z):
        raw = np.sqrt(4.0 * V**2 * (zi**2 - EPS_EP**2) + 0j)
        if i == 0:
            y[0] = raw
            continue
        if abs(raw - y[i - 1]) > abs(-raw - y[i - 1]):
            raw = -raw
        y[i] = raw
    return y


def trapz(z: np.ndarray, y: np.ndarray) -> complex:
    return np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(z))


def run_histories(n: int = 801) -> dict:
    # A real slit Γ, upper lip
    eps_A = np.linspace(-EPS_EP, EPS_EP, n) + 1j * 1e-9
    yA = y_continue(eps_A)
    IA = trapz(eps_A, yA)
    # B conjugate opposite sheet (lower lip)
    eps_B = np.linspace(-EPS_EP, EPS_EP, n) - 1j * 1e-9
    yB = y_continue(eps_B)
    IB = trapz(eps_B, yB)
    # C imaginary cap: circle through both tips, ε=ε_EP e^{iχ}
    chi = np.linspace(0.0, 2.0 * np.pi, n)
    eps_C = EPS_EP * np.exp(1j * chi)
    yC = y_continue(eps_C)
    IC = trapz(eps_C, yC)

    def pack(name, I, inter, score):
        return {
            "name": name,
            "I": I,
            "Re": float(np.real(I)),
            "Im": float(np.imag(I)),
            "intersection": inter,
            "score": score,
        }

    # Score rule: A WRITE; B conjugate of A WRITE; C NOT-SELECTED if ∩=0.
    return {
        "A": pack("A real slit", IA, 1, "WRITE"),
        "B": pack("B conjugate opposite sheet", IB, 1, "WRITE"),
        "C": pack("C imaginary cap", IC, 0, "NOT-SELECTED"),
        "analytic_A": 1j * np.pi * V * EPS_EP**2,  # ∫_{-e}^{e} 2v i sqrt(e^2-x^2) dx wait
    }

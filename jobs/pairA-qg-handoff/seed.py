"""Layer 0 — Pair A is the cut Hamiltonian. Numbers locked."""

from __future__ import annotations

import numpy as np

A = 0.12337
B = 0.49348
V = -0.360253
ETA = 0.05
EPS_EP_GIVEN = 0.513681
LAM_EP_GIVEN = -0.308425j
EPS_EP = abs(B - A) / (2.0 * abs(V))
LAM_EP = -0.5j * (A + B)


def H_A(eps: complex) -> np.ndarray:
    return np.array(
        [[-1j * A, eps * V], [eps * V, -1j * B]],
        dtype=complex,
    )


def ep_condition(eps: float) -> dict:
    lhs = abs(eps * V)
    rhs = abs(B - A) / 2.0
    return {
        "abs_eps_v": lhs,
        "abs_b_minus_a_over_2": rhs,
        "match": abs(lhs - rhs) < 1e-9,
        "eps_EP_given": EPS_EP_GIVEN,
        "eps_EP_from_abv": abs(B - A) / (2.0 * abs(V)),
    }


def disc(eps: complex) -> complex:
    return 4.0 * (eps * V) ** 2 - (A - B) ** 2


def y_of_eps(eps: complex) -> complex:
    """y^2 = 4 v^2 (ε^2 - ε_EP^2) = disc. Principal sqrt."""
    return np.sqrt(4.0 * V**2 * (eps**2 - EPS_EP**2) + 0j)

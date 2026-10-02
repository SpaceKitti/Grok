"""
Layer T — triad, not a two-arm fork.
Two real sheets + joining structure at the EPs, meeting at the cut tips.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from seed import EPS_EP, H_A


def _evals_real(eps: float) -> np.ndarray:
    w = np.linalg.eigvals(H_A(eps))
    return w[np.argsort(w.real + 1e-12 * w.imag)]


def build_triad(n_out: int = 41, n_join: int = 41) -> dict:
    # real sheets: |ε| > ε_EP on the real line (both sides of the slit)
    eps_out = np.concatenate(
        [
            np.linspace(-2.0 * EPS_EP, -EPS_EP, n_out // 2 + 1)[:-1],
            np.linspace(EPS_EP, 2.0 * EPS_EP, n_out // 2 + 1),
        ]
    )
    lam_p = np.zeros(eps_out.size, dtype=complex)
    lam_m = np.zeros(eps_out.size, dtype=complex)
    for i, e in enumerate(eps_out):
        w = _evals_real(float(e))
        lam_m[i], lam_p[i] = w[0], w[1]
    # joining structure: interior of Γ, complex-conjugate pair connecting ±ε_EP
    eps_g = np.linspace(-EPS_EP, EPS_EP, n_join)
    lam_j0 = np.zeros(n_join, dtype=complex)
    lam_j1 = np.zeros(n_join, dtype=complex)
    for i, e in enumerate(eps_g):
        w = _evals_real(float(e))
        # sort by Im
        w = w[np.argsort(w.imag)]
        lam_j0[i], lam_j1[i] = w[0], w[1]
    return {
        "leg_plus_eps": eps_out,
        "leg_plus_lam": lam_p,
        "leg_minus_eps": eps_out,
        "leg_minus_lam": lam_m,
        "leg_join_eps": eps_g,
        "leg_join_lam0": lam_j0,
        "leg_join_lam1": lam_j1,
        "n_plus": int(eps_out.size),
        "n_minus": int(eps_out.size),
        "n_join": int(n_join),
        "tips": np.array([-EPS_EP, EPS_EP]),
    }


def save(tri: dict, path: Path) -> None:
    np.savez(path, **{k: (np.array(v) if np.isscalar(v) else v) for k, v in tri.items()})

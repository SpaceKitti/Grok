"""Continuous eigenvalue tracking along eps paths (small steps, nearest-distance match)."""
from __future__ import annotations

import numpy as np

from vortices import EPS_EP, H_A, align_evals


def track(z: np.ndarray, first=None) -> dict:
    """Track the eigenvalue pair along z. Matching rule = handoff tracker.align_evals."""
    n = z.size
    ev = np.zeros((n, 2), dtype=complex)
    for i, zi in enumerate(z):
        w = np.linalg.eigvals(H_A(complex(zi)))
        if i == 0:
            if first is not None:  # order the start pair as requested (sheet A first)
                w = align_evals(np.asarray(first), w)
            ev[0] = w
            continue
        ev[i] = align_evals(ev[i - 1], w)
    steps = np.abs(np.diff(ev, axis=0)).max(axis=1)
    gap = np.abs(ev[:, 0] - ev[:, 1])
    # jump flag: a step comparable to the local gap means the matching was ambiguous
    jump_ratio = float(np.max(steps / np.maximum(gap[1:], 1e-300)))
    return {"z": z, "evals": ev, "max_step": float(steps.max()), "jump_ratio": jump_ratio}


def circle(center: float, r: float, turns: float = 2.0, n_per_turn: int = 4000,
           theta0: float = 0.0, sense: int = +1):
    th = np.linspace(0.0, 2.0 * np.pi * turns, int(n_per_turn * turns) + 1)
    return th, center + r * np.exp(1j * (theta0 + sense * th))


def figure_eight(n_per_lobe: int = 4000):
    """Start at eps=0 (real, in Gamma). Lobe 1: circle centre +eps_EP radius eps_EP,
    anticlockwise. Lobe 2: circle centre -eps_EP radius eps_EP, clockwise."""
    t = np.linspace(0.0, 2.0 * np.pi, n_per_lobe + 1)
    l1 = EPS_EP + EPS_EP * np.exp(1j * (np.pi + t))   # anticlockwise about +eps_EP
    l2 = -EPS_EP + EPS_EP * np.exp(-1j * t)           # clockwise about -eps_EP
    z = np.concatenate([l1, l2[1:]])
    s = np.concatenate([t, 2.0 * np.pi + t[1:]])
    return s, z

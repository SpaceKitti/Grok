"""Residuals of Einstein+Λ ODE on the two seeds."""

from __future__ import annotations

import numpy as np

from load_have import EPS_EP
from ode_r import Lambda_chi, residual_E, seed_R1, seed_R2


def seed_report(name: str, chi: np.ndarray, r, rp, rpp) -> dict:
    # avoid poles for cot
    m = (chi > 1e-3) & (chi < np.pi - 1e-3) & (np.abs(r) > 1e-8)
    E = residual_E(chi[m], r[m], rp[m], rpp[m])
    Lam = Lambda_chi(chi[m], r[m], rp[m])
    rms = float(np.sqrt(np.mean(E**2)))
    lam_std = float(np.std(Lam))
    lam_mean = float(np.mean(Lam))
    solved = rms < 1e-6 and lam_std < 1e-6
    return {
        "name": name,
        "rms_E": rms,
        "max_abs_E": float(np.max(np.abs(E))),
        "Lambda_mean": lam_mean,
        "Lambda_std": lam_std,
        "solved": solved,
        "Lambda_if_solved": lam_mean if solved else None,
    }

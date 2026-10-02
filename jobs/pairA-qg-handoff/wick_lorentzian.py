"""Layer W — Lorentzian/real chart only on Γ. Dies at ±ε_EP."""

from __future__ import annotations

import numpy as np

from seed import EPS_EP, H_A


def chart() -> dict:
    # on Γ: Re λ ≈ 0 (vertical split). Off Γ on real ε: Re λ ≠ 0.
    on = []
    for e in np.linspace(-EPS_EP, EPS_EP, 9):
        w = np.linalg.eigvals(H_A(float(e)))
        on.append((float(e), w))
    off = []
    for e in (1.2 * EPS_EP, 1.6 * EPS_EP, -1.2 * EPS_EP):
        w = np.linalg.eigvals(H_A(float(e)))
        off.append((float(e), w))
    tips = []
    for e in (-EPS_EP, EPS_EP):
        w = np.linalg.eigvals(H_A(float(e)))
        gap = abs(w[0] - w[1])
        tips.append((float(e), w, float(gap)))
    return {
        "real_section_support": "Γ=[-ε_EP, ε_EP]",
        "dies_at": (-EPS_EP, EPS_EP),
        "on_cut_samples": on,
        "off_cut_samples": off,
        "tips": tips,
    }

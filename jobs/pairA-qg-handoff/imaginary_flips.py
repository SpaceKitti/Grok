"""Layer F — 2π swap / 4π return is the imaginary flip. Uses Layer 1 Jhat."""

from __future__ import annotations

import numpy as np


def flips(strip: dict) -> dict:
    J2 = strip["Jhat2"]
    J4 = strip["Jhat4"]
    J2sq = J2 @ J2
    return {
        "swap_2pi": bool(strip["fro_Jhat2sq_I"] < 0.05 and np.linalg.norm(J2 - np.eye(2), "fro") > 0.5),
        "return_4pi": bool(strip["fro_Jhat4_I"] < 0.05),
        "Jhat2_is_involution": bool(np.linalg.norm(J2sq - np.eye(2), "fro") < 0.05),
    }

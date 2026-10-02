"""Load HAVE numbers from pairA-qg-handoff. Do not rebuild H_A."""

from __future__ import annotations

from pathlib import Path

import numpy as np

HANDOFF = Path(r"C:\Users\Akitt\pairA-qg-handoff")

A = 0.12337
B = 0.49348
V = -0.360253
EPS_EP = 0.5136806633116171
LAM_EP = -0.308425j
TAU = 4.0 * np.pi / EPS_EP  # 24.46339
I_A = -0.29862325j
I_B = +0.29862325j


def load_jhat() -> dict:
    path = HANDOFF / "outputs" / "Jhat.npz"
    d = np.load(path)
    return {
        "path": str(path),
        "Jhat2": np.array(d["Jhat2"]),
        "Jhat4": np.array(d["Jhat4"]),
        "phi": float(d["phi"]) if "phi" in d.files else float("nan"),
    }

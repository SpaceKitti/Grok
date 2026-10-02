"""Load Pair A surface from handoff. Do not rebuild H_A."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HANDOFF = Path(r"C:\Users\Akitt\pairA-qg-handoff")
sys.path.insert(0, str(HANDOFF))

from seed import EPS_EP, ETA, H_A, LAM_EP  # noqa: E402

TAU = 4.0 * np.pi / EPS_EP
R_LOOP = 0.25 * EPS_EP


def load_jhat() -> dict:
    p = HANDOFF / "outputs" / "Jhat.npz"
    d = np.load(p)
    return {"path": str(p), "Jhat2": np.array(d["Jhat2"]), "Jhat4": np.array(d["Jhat4"])}

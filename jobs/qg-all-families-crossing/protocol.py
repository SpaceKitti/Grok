"""Locked crossing probe. Do not rebuild pair A. Γ is a score mask."""

from __future__ import annotations

import numpy as np

EPS_EP = 0.513681
GAMMA = (-EPS_EP, EPS_EP)
DELTA = 0.05
X_ON = 0.25
X_OFF = 1.20
# P0 locked (cut-crossing-probe): pair A sees the wall, ratio 8.18


def ratio(j_on: float, j_off: float) -> float:
    return float(abs(j_on) / (abs(j_off) + 1e-16))


def verdict(defined: bool, inserted: bool, r: float, j_on: float, j_off: float) -> str:
    if not defined:
        return "could not define"
    if inserted:
        return "inserted"
    if r >= 3.0 and j_on > 1e-12:
        return "prefers Γ"
    if abs(r - 1.0) < 0.15 and j_on > 1e-12 and j_off > 1e-12:
        return "global junk"
    if j_on < 1e-12 and j_off < 1e-12:
        return "misses Γ"
    if r < 1.0 and j_off > j_on:
        return "global junk"
    return "misses Γ"


def undef(name: str, why: str) -> dict:
    return {
        "family": name,
        "operator": why,
        "J_on": float("nan"),
        "J_off": float("nan"),
        "ratio": float("nan"),
        "wall_site": "n/a",
        "verdict": "could not define",
        "defined": False,
        "inserted": False,
    }

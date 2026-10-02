"""Sheet A carries I_A and Jhat2. Sheet B carries I_B and Jhat2. Meet at bolts. C not lifted."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from load_surface import EPS_EP, I_A, I_B, load_jhat


def build_sheets() -> dict:
    jh = load_jhat()
    J2 = jh["Jhat2"]
    return {
        "jhat_path": jh["path"],
        "A": {"I": I_A, "Jhat2": J2, "lifted": True},
        "B": {"I": I_B, "Jhat2": J2, "lifted": True},
        "C": {"lifted": False, "held": True},
        "meet": "bolts χ=0,π = ±ε_EP",
        "eps_EP": EPS_EP,
    }


def save(sh: dict, path: Path) -> None:
    np.savez(
        path,
        I_A=np.array([sh["A"]["I"]]),
        I_B=np.array([sh["B"]["I"]]),
        Jhat2=sh["A"]["Jhat2"],
        eps_EP=np.array([EPS_EP]),
        A_lifted=np.array([True]),
        B_lifted=np.array([True]),
        C_lifted=np.array([False]),
    )

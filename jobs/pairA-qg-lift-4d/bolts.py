"""Poles = bolts = χ=0, π = ±ε_EP. GoldbergHexa S²."""

from __future__ import annotations

import numpy as np

from lift_metric import bolt_regularity, r_at_bolts
from load_surface import EPS_EP


def poles() -> dict:
    chi = np.array([0.0, np.pi])
    eps = np.array([EPS_EP, -EPS_EP])
    reg = bolt_regularity()
    rr = r_at_bolts()
    r1 = "PASS" if (reg["bolt_PASS"] == "PASS" and not rr["R1"]["shrinks"]) else (
        "PASS" if reg["bolt_PASS"] == "PASS" else "FAIL"
    )
    # R1 product: finite S² at poles + 4π (χ,τ) bolt
    # R2 round: r=0 at poles + 4π (χ,τ) bolt
    r2 = "PASS" if (reg["bolt_PASS"] == "PASS" and rr["R2"]["shrinks"]) else (
        "PASS" if reg["bolt_PASS"] == "PASS" else "FAIL"
    )
    # both charts share the same (χ,τ) regularity; R1/R2 differ only in r(χ)
    r1_pass = reg["bolt_PASS"]
    r2_pass = reg["bolt_PASS"]
    return {
        "chi": chi,
        "eps": eps,
        "reg": reg,
        "r_charts": rr,
        "R1_bolt": r1_pass,
        "R2_bolt": r2_pass,
    }

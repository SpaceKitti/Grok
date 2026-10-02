"""4d line element. F=ε_EP²−ε², ε=ε_EP cos χ. Two r-charts."""

from __future__ import annotations

import numpy as np

from load_surface import EPS_EP, TAU


def F(eps: float) -> float:
    return EPS_EP**2 - eps**2


def eps_of_chi(chi: float) -> float:
    return EPS_EP * np.cos(chi)


def r_R1(chi: float) -> float:
    """Product: r = ε_EP (constant)."""
    return EPS_EP


def r_R2(chi: float) -> float:
    """Round: r = ε_EP sin χ."""
    return EPS_EP * np.sin(chi)


def bolt_regularity(tau: float = TAU) -> dict:
    """
    Near χ=0: ds_E² = dχ² + (ε_EP χ)² dτ_E² + r(χ)² dΩ².
    Circumference/radius of the τ-circle = ε_EP * τ.
    2π-polar needs ε_EP*τ = 2π ⇒ τ=2π/ε_EP.
    HAVE τ=4π/ε_EP ⇒ ε_EP*τ=4π. Smooth on the 4π cover (Jhat4=I), not 2π-polar.
    """
    circ_over_rad = EPS_EP * tau
    pass_4pi = abs(circ_over_rad - 4.0 * np.pi) < 1e-6
    pass_2pi = abs(circ_over_rad - 2.0 * np.pi) < 1e-6
    return {
        "tau": tau,
        "eps_EP_times_tau": circ_over_rad,
        "two_pi_polar": "PASS" if pass_2pi else "FAIL",
        "four_pi_cover": "PASS" if pass_4pi else "FAIL",
        "bolt_PASS": "PASS" if pass_4pi else "FAIL",
    }


def r_at_bolts() -> dict:
    return {
        "R1": {"r_chi0": r_R1(0.0), "r_chipi": r_R1(np.pi), "shrinks": False},
        "R2": {"r_chi0": float(r_R2(0.0)), "r_chipi": float(abs(r_R2(np.pi))), "shrinks": True},
        "F_plus": F(EPS_EP),
        "F_minus": F(-EPS_EP),
    }

"""
Spherical reduction of Euclidean Einstein + Λ.

ds_E² = dχ² + a(χ)² dτ_E² + r(χ)² dΩ₂²
a(χ) = ε_EP sin χ   (fixed by the cut)
a''/a = -1,  a'/a = cot χ

Einstein R_μν = Λ g_μν implies (Λ eliminated):

  r r'' - cot(χ) r r' + (r')² + r² - 1 = 0

or
  r'' = cot(χ) r' - (r')²/r - r + 1/r

Λ from the (χ,τ) block, when it is constant:
  Λ = 1 - 2 cot(χ) (r'/r)
For r=const, Λ=1, and the S² equation needs r=1.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

from load_have import EPS_EP


def a_over_a(chi: np.ndarray | float) -> np.ndarray | float:
    return np.cos(chi) / np.sin(chi)


def ode_rhs(chi: float, y: np.ndarray) -> list:
    r, rp = y
    if abs(r) < 1e-12:
        return [rp, np.nan]
    cot = np.cos(chi) / (np.sin(chi) + 1e-16)
    rpp = cot * rp - (rp * rp) / r - r + 1.0 / r
    return [rp, rpp]


def residual_E(chi: np.ndarray, r: np.ndarray, rp: np.ndarray, rpp: np.ndarray) -> np.ndarray:
    """E = r r'' - cot χ r r' + (r')² + r² - 1. Zero iff Einstein+Λ."""
    cot = np.cos(chi) / np.sin(chi)
    return r * rpp - cot * r * rp + rp**2 + r**2 - 1.0


def Lambda_chi(chi: np.ndarray, r: np.ndarray, rp: np.ndarray) -> np.ndarray:
    """Λ from R_ττ = Λ g_ττ:  Λ = 1 - 2 cot(χ) r'/r."""
    cot = np.cos(chi) / np.sin(chi)
    return 1.0 - 2.0 * cot * rp / r


def seed_R1(chi: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    r = np.full_like(chi, EPS_EP)
    rp = np.zeros_like(chi)
    rpp = np.zeros_like(chi)
    return r, rp, rpp


def seed_R2(chi: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    r = EPS_EP * np.sin(chi)
    rp = EPS_EP * np.cos(chi)
    rpp = -EPS_EP * np.sin(chi)
    return r, rp, rpp


def integrate_from_bolt(r0: float, chi_min: float = 1e-4, chi_max: float = np.pi - 1e-4):
    """
    r'(0)=0. Taylor: r''(0)=1/r0 - r0.
    Start at chi_min with r=r0+(1/2)r''(0) χ², r'=r''(0) χ.
    """
    if abs(r0) < 1e-14:
        return None
    rpp0 = 1.0 / r0 - r0
    r_s = r0 + 0.5 * rpp0 * chi_min**2
    rp_s = rpp0 * chi_min
    if r_s <= 0:
        return None

    def event_nonpos(chi, y):
        return y[0] - 1e-8

    event_nonpos.terminal = True
    event_nonpos.direction = -1

    sol = solve_ivp(
        ode_rhs,
        (chi_min, chi_max),
        [r_s, rp_s],
        rtol=1e-8,
        atol=1e-10,
        dense_output=True,
        events=event_nonpos,
        max_step=0.02,
    )
    return sol

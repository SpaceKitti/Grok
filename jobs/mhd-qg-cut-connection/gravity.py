"""
Track 2 — gravity reading. Separate operator on the SAME slit Γ.

Not pair A's matrix. No EP2 demand at ε=0.514.

Discrete U(1) / Z2 holonomy of a connection whose curvature is a
π-flux supported on Γ (square-root / edge defect). Equivalent abelian
CS increment: ΔCS = (1/2) × intersection number with Γ.

  da = π δ_Γ
  U_G[γ] = exp(i π I(γ, Γ)) = (−1)^{I(γ,Γ)}
  ΔCS[γ] = I(γ, Γ) / 2
  n_QG  += I(γ, Γ)     (sheet index; holonomy sees n mod 2)
"""

from __future__ import annotations

import numpy as np


def intersection_number(theta: np.ndarray, cut_angle: float = np.pi) -> np.ndarray:
    """
    A circular loop z = z_b + r e^{iθ}, θ: 0→T.
    The standard cut is the ray arg = π (or the segment Γ).
    Crossing the branch cut of sqrt(z−z_b) happens when θ crosses π + 2πk.
    Intersection count along the path: number of times θ crosses the cut.
    """
    # unwrapped θ / 2π is the winding; each 2π is one encirclement = one
    # cut crossing for a ray attached to z_b.
    wind = np.unwrap(theta) / (2.0 * np.pi)
    # crossings of the cut ray at odd multiples of π in arg
    arg = np.mod(np.unwrap(theta) + np.pi, 2.0 * np.pi) - np.pi
    cross = np.zeros_like(theta, dtype=int)
    for i in range(1, theta.size):
        # crossed the branch cut if the principal Arg jumped by ~2π
        d = np.unwrap(np.array([arg[i - 1], arg[i]]))[1] - arg[i - 1]
        crossed = abs((np.unwrap(theta)[i] - np.unwrap(theta)[i - 1])) > 0
        # simpler: floor of wind
        cross[i] = int(np.floor(wind[i] + 1e-12) - np.floor(wind[0] + 1e-12))
    return cross


def holonomy(I: int | np.ndarray) -> np.ndarray:
    return np.exp(1j * np.pi * np.asarray(I, dtype=float))


def cs_increment(I: int | np.ndarray) -> np.ndarray:
    return np.asarray(I, dtype=float) / 2.0


def n_qg_from_loop(theta: np.ndarray) -> np.ndarray:
    """Sheet index along a loop around one branch point: Δn = winding."""
    return np.floor(np.unwrap(theta) / (2.0 * np.pi) + 1e-12) - np.floor(
        theta[0] / (2.0 * np.pi) + 1e-12
    )


def U_of_theta(theta: np.ndarray) -> np.ndarray:
    """
    Geometric holonomy of the π-flux at a branch point:
    U(θ) = exp(i θ / 2)  (sqrt covering), so U(2π) = −1, U(4π) = +1.
    """
    return np.exp(1j * np.unwrap(theta) / 2.0)


def flux_density_on_line(s: np.ndarray, lo: float, hi: float) -> np.ndarray:
    """
    R_QG(s): curvature density of the edge defect on the slit [lo, hi].
    Uniform π-flux on Γ, zero off it. Normalised so ∫_Γ R_QG = 1/2 = ΔCS
    of a once-crossing loop (π / 2π).
    """
    on = (s >= lo) & (s <= hi)
    length = max(hi - lo, 1e-16)
    rho = np.zeros_like(s, dtype=float)
    rho[on] = 0.5 / length
    return rho

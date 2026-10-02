"""
Local unfolding only.
NO global polynomial.
NO s' = |z-z_NN|√ρ on a thin arm.
CSR forbidden on thin arms. CSR only if the cloud is thick (it should not be).
"""

from __future__ import annotations

import numpy as np
from scipy.interpolate import UnivariateSpline


def arm_arc_length(pts: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    """Order by ε, polyline in the complex plane, cumulative arc length ℓ."""
    if len(pts) < 2:
        return np.array([]), np.array([])
    pts = sorted(pts, key=lambda p: p["eps"])
    z = np.array([p["lam"] for p in pts], dtype=complex)
    d = np.abs(np.diff(z))
    ell = np.concatenate([[0.0], np.cumsum(d)])
    return ell, z


def density_1d(ell: np.ndarray, bw: float | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Gaussian KDE on ℓ. Returns grid, ρ ≥ 0."""
    ell = np.asarray(ell, float)
    n = ell.size
    if n < 3:
        return ell, np.ones_like(ell)
    if bw is None:
        bw = 1.06 * np.std(ell) * n ** (-0.2)
        bw = max(bw, 1e-6)
    grid = np.linspace(ell[0], ell[-1], max(64, 4 * n))
    d = (grid[:, None] - ell[None, :]) / bw
    rho = np.exp(-0.5 * d**2).sum(axis=1) / (bw * np.sqrt(2.0 * np.pi) * n)
    rho = np.maximum(rho, 0.0)
    return grid, rho


def Nbar_monotone(ell: np.ndarray) -> np.ndarray:
    """
    N_bar(ℓ) = n * ∫_0^ℓ ρ, ρ = 1-D KDE. Monotone by construction (ρ≥0).
    Not a global polynomial. Not interpolating every point (that would give s≡1).
    """
    if ell.size < 3:
        return np.arange(ell.size, dtype=float)
    grid, rho = density_1d(ell)
    integ = np.concatenate([[0.0], np.cumsum(0.5 * (rho[1:] + rho[:-1]) * np.diff(grid))])
    # scale so N_bar spans ~ n at the end
    if integ[-1] > 0:
        integ = integ * (ell.size / integ[-1])
    return np.interp(ell, grid, integ)


def spacings(ell: np.ndarray) -> np.ndarray:
    """s_i = N_bar(ℓ_{i+1}) - N_bar(ℓ_i), then ⟨s⟩=1."""
    if ell.size < 3:
        return np.array([])
    Nb = Nbar_monotone(ell)
    s = np.diff(Nb)
    s = s[s > 0]
    if s.size == 0:
        return s
    s = s / np.mean(s)
    return s


def unfolding_ratio_r(s: np.ndarray) -> np.ndarray:
    """Hermitian consecutive-spacing ratio r_i = min(s_i,s_{i+1})/max(...)."""
    if s.size < 2:
        return np.array([])
    a, b = s[:-1], s[1:]
    return np.minimum(a, b) / (np.maximum(a, b) + 1e-16)


def number_variance(ell: np.ndarray, L_grid: np.ndarray | None = None) -> dict:
    """Σ²(L) on unfolded coordinates u_i = N_bar(ℓ_i). Poisson: L. GUE: ~log L."""
    if ell.size < 8:
        return {"L": np.array([]), "Sigma2": np.array([])}
    u = Nbar_monotone(ell)
    u = np.sort(u)
    span = u[-1] - u[0]
    if L_grid is None:
        L_grid = np.linspace(0.5, max(2.0, 0.25 * span), 12)
    sig = []
    for L in L_grid:
        if L >= span:
            sig.append(np.nan)
            continue
        starts = np.linspace(u[0], u[-1] - L, 40)
        counts = np.array([np.sum((u >= t) & (u < t + L)) for t in starts], float)
        sig.append(float(np.var(counts)))
    return {"L": np.asarray(L_grid, float), "Sigma2": np.asarray(sig, float)}


def airy_zoom(z: np.ndarray, z_ep: complex) -> np.ndarray:
    """Microscope ζ ∝ (z-z_EP)^{2/3}. Not arm unfolding."""
    return (z - z_ep) ** (2.0 / 3.0)


P_GUE = lambda s: (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)
P_POISSON = lambda s: np.exp(-s)

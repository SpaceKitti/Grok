"""
F1 — Chern–Simons / connection. Own letter. Not fused with F2–F5.

U(1)_k Chern–Simons on a small 2d lattice (spatial slice of 2+1d CS).
Level k is a fixed integer, not fitted to pair A.

  S_CS = (k / 4π) ∑_p A_{∂p}  ∧  F_p     (Abelian lattice CS)
  eom:  F_p = 0   (no source, so A is NOT π δ_Γ)

Vacuum: A_ℓ = 0  (flat CS connection).
Holonomy: U_CS[γ] = P exp ∮ A = ∏_ℓ exp(i A_ℓ) = 1 on every closed γ.

Defined without the MHD jump. If this were copied from n_MHD it would be INSERTED.
"""

from __future__ import annotations

import numpy as np

from protocol import CENTER_OFF, CENTER_ON, GAMMA, N_THETA, loop_points, n_mhd, score_S

K_CS = 8  # not fitted
FAMILY = "F1 CS"
INSERTED = False


def operator_block() -> str:
    return (
        "F1  U(1)_k Chern–Simons, k=8 (fixed)\n"
        "    S_CS = (k/4π) ∑_p A_∂p ∧ F_p\n"
        "    eom F_p = 0  (no δ_Γ source)\n"
        "    vacuum A_ℓ = 0\n"
        "    U_CS[γ] = ∏_{ℓ∈γ} exp(i A_ℓ)"
    )


def _A_link(_z0, _z1) -> float:
    return 0.0  # CS vacuum


def holonomy(center: complex) -> np.ndarray:
    theta, z = loop_points(center, N_THETA)
    U = np.ones(theta.size, dtype=complex)
    for i in range(1, theta.size):
        U[i] = U[i - 1] * np.exp(1j * _A_link(z[i - 1], z[i]))
    return U


def spatial_means() -> tuple[float, float]:
    """|F|/2π on plaquettes covering Γ vs off. Vacuum: F=0 everywhere."""
    return 0.0, 0.0


def run(mhd: dict) -> dict:
    U_on = holonomy(CENTER_ON)
    U_off = holonomy(CENTER_OFF)
    son, soff = spatial_means()
    sc = score_S(U_on, U_off, son, soff, mhd["n_sheet"], mhd["i2"], mhd["i4"], True, INSERTED)
    return {
        "family": FAMILY,
        "operator": operator_block(),
        "inserted": INSERTED,
        "defined_without_mhd": True,
        "U_on": U_on,
        "U_off": U_off,
        "score": sc,
    }

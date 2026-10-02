"""Layer 1 — strip U(1). Raw J then gauge so Jhat4=I and Jhat2^2=I."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from seed import EPS_EP, ETA
from tracker import USED_HELPER, continue_loop


def run_strip(n_theta: int = 721, radius_frac: float = 0.25) -> dict:
    r = radius_frac * EPS_EP
    theta = np.linspace(0.0, 4.0 * np.pi, n_theta)
    z = EPS_EP + r * np.exp(1j * theta)
    cont = continue_loop(z)
    i2 = int(np.argmin(np.abs(theta - 2.0 * np.pi)))
    i4 = n_theta - 1
    V0 = cont["evecs"][0]
    V2 = cont["evecs"][i2]
    V4 = cont["evecs"][i4]
    J2 = V2 @ np.linalg.pinv(V0)
    J4 = V4 @ np.linalg.pinv(V0)
    # φ from J4 ≈ e^{iφ} I
    phi = float(np.angle(0.5 * (J4[0, 0] + J4[1, 1])))
    # gauge: V(θ) ← exp(-i φ θ / 4π) V(θ)
    phase = np.exp(-1j * phi * theta / (4.0 * np.pi))
    Vg = cont["evecs"] * phase[:, None, None]
    V0g, V2g, V4g = Vg[0], Vg[i2], Vg[i4]
    Jhat2 = V2g @ np.linalg.pinv(V0g)  # = exp(-i φ/2) J2
    Jhat4 = V4g @ np.linalg.pinv(V0g)  # = exp(-i φ) J4
    return {
        "r": r,
        "n_theta": n_theta,
        "eps_EP": EPS_EP,
        "eta": ETA,
        "phi": phi,
        "helper": USED_HELPER,
        "V0": V0g,
        "V2PI": V2g,
        "V4PI": V4g,
        "J2_raw": J2,
        "J4_raw": J4,
        "Jhat2": Jhat2,
        "Jhat4": Jhat4,
        "det_Jhat2": np.linalg.det(Jhat2),
        "det_Jhat4": np.linalg.det(Jhat4),
        "Jhat2@Jhat2": Jhat2 @ Jhat2,
        "fro_Jhat4_I": float(np.linalg.norm(Jhat4 - np.eye(2), "fro")),
        "fro_Jhat2sq_I": float(np.linalg.norm(Jhat2 @ Jhat2 - np.eye(2), "fro")),
        "i2": i2,
        "i4": i4,
        "evals0": cont["evals"][0],
        "evals2": cont["evals"][i2],
        "evals4": cont["evals"][i4],
    }


def swap_test(V0: np.ndarray, V2: np.ndarray, V4: np.ndarray) -> dict:
    def ov(A, B):
        M = np.zeros((2, 2))
        for i in range(2):
            for j in range(2):
                M[i, j] = abs(np.vdot(A[:, i], B[:, j]))
        return M

    return {"V0_vs_V2": ov(V0, V2), "V0_vs_V4": ov(V0, V4)}


def save(d: dict, path: Path) -> None:
    np.savez(
        path,
        r=d["r"],
        phi=d["phi"],
        Jhat2=d["Jhat2"],
        Jhat4=d["Jhat4"],
        J2_raw=d["J2_raw"],
        J4_raw=d["J4_raw"],
        V0=d["V0"],
        V2PI=d["V2PI"],
        V4PI=d["V4PI"],
    )

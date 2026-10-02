"""
P2 — foam face/edge whose dual meets the path (scan site).

  S_BF = ∑_f Tr(B_f F_f)
  One defect g_*=exp(2πi/3) on a scanned face.
  J(path; f) = |g_*-1| if the dual of f meets the path, else 0.

Scan f over a 2d face grid (on / near / far from Γ).
If the only nonzero J is when the defect is stamped on γ_cross ∩ Γ → INSERTED.
"""

from __future__ import annotations

import numpy as np

from protocol import DELTA, EPS_EP, GAMMA, X_OFF, X_ON, on_gamma_x, ratio, verdict

G_STAR = np.exp(2j * np.pi / 3.0)
N_FACE = 21
EXTENT = 2.0


def operator_block() -> str:
    return (
        "P2  BF defect g_*=exp(2πi/3) on scanned face f\n"
        "    J=|g_*-1| if dual(f) meets the path, else 0\n"
        "    scan faces on a 21×21 grid over [-2,2]²"
    )


def _faces():
    x = np.linspace(-EXTENT, EXTENT, N_FACE)
    X, Y = np.meshgrid(x, x, indexing="xy")
    return (X + 1j * Y).ravel()


def meets(path_x: float, zf: complex) -> bool:
    """Face centre near the vertical segment x=path_x, y∈[-δ,δ]."""
    return abs(zf.real - path_x) <= (2 * EXTENT / (N_FACE - 1)) * 0.75 and abs(zf.imag) <= DELTA * 1.5


def J_path(path_x: float, zf: complex) -> float:
    return float(abs(G_STAR - 1.0)) if meets(path_x, zf) else 0.0


def run() -> dict:
    faces = _faces()
    j_on_map = np.array([J_path(X_ON, complex(z)) for z in faces])
    j_off_map = np.array([J_path(X_OFF, complex(z)) for z in faces])
    i_max = int(np.argmax(j_on_map))
    p_max = complex(faces[i_max])
    j_on = float(np.max(j_on_map))
    j_off = float(J_path(X_OFF, p_max))  # same defect, miss path
    r = ratio(j_on, j_off)
    # stamping: max sits on the crossing segment, which was drawn through Γ
    stamped = bool(meets(X_ON, p_max) and on_gamma_x(p_max.real))
    inserted = stamped and j_on > 0
    passed = bool(r >= 3.0 and j_on > 1e-9 and not inserted)
    v = verdict(passed, inserted, True, False)
    return {
        "family": "P2 foam",
        "operator": operator_block(),
        "J_on": j_on,
        "J_off": j_off,
        "ratio": r,
        "P_site": p_max,
        "passed": passed,
        "verdict": v,
        "defined_without_mhd": True,
        "inserted": inserted,
    }

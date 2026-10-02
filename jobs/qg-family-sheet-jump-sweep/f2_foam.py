"""
F2 — Spin-foam / BF defect. Own letter. Not fused with F1,F3–F5.

  S_BF = ∑_faces Tr(B_f F_f)
  Face amplitude: 1 if g_f = 1,  else  δ(g_f, g_*) for the defect face.

Defect location by a FOAM RULE, not pasted on Γ:
  on an N×N face grid over [-2,2]², put nontrivial g_* on the unique face
  of MAXIMUM graph distance from the mesh origin (farthest corner).

g_* = exp(2π i / 3)   # cube root of unity, not fitted to −1
Curvature is concentrated on that one face; elsewhere F=0.
U_BF[γ] = exp(i flux enclosed by γ)  = g_* if γ winds the defect face, else 1.
"""

from __future__ import annotations

import numpy as np

from protocol import CENTER_OFF, CENTER_ON, GAMMA, N_THETA, R_LOOP, loop_points, score_S

N_FACE = 9
EXTENT = 2.0
G_STAR = np.exp(2j * np.pi / 3.0)
FAMILY = "F2 foam"
INSERTED = False


def _grid():
    x = np.linspace(-EXTENT, EXTENT, N_FACE + 1)
    xc = 0.5 * (x[:-1] + x[1:])
    X, Y = np.meshgrid(xc, xc, indexing="xy")
    dist = np.sqrt((X - 0.0) ** 2 + (Y - 0.0) ** 2)
    # foam rule: farthest face from origin
    j, i = np.unravel_index(np.argmax(dist), dist.shape)
    return x, xc, i, j, X, Y


def operator_block() -> str:
    _, _, i, j, X, Y = _grid()
    return (
        "F2  BF / spin-foam on a 9×9 face lattice over [-2,2]²\n"
        "    S_BF = ∑_f Tr(B_f F_f)\n"
        f"    defect g_* = exp(2πi/3) on face (i,j)=({i},{j}) "
        f"at ({X[j, i]:.3f},{Y[j, i]:.3f})\n"
        "    foam rule: unique face of max graph-distance from the origin\n"
        "    (NOT pasted onto Γ)\n"
        "    U_BF[γ] = g_*^{winding around that face}"
    )


def _defect_center() -> complex:
    _, _, i, j, X, Y = _grid()
    return complex(X[j, i], Y[j, i])


def holonomy(center: complex) -> np.ndarray:
    """Winding of the circular loop about the defect centre (output, not input)."""
    theta, z = loop_points(center, N_THETA)
    zc = _defect_center()
    ang = np.unwrap(np.angle(z - zc))
    wind = (ang - ang[0]) / (2.0 * np.pi)
    U = G_STAR ** wind
    return U


def spatial_means() -> tuple[float, float]:
    lo, hi = GAMMA
    _, xc, i_d, j_d, X, Y = _grid()
    mag = np.zeros_like(X, dtype=float)
    mag[j_d, i_d] = abs(G_STAR - 1.0)
    on = (X >= lo) & (X <= hi) & (np.abs(Y) <= (xc[1] - xc[0]))
    on_m = float(np.mean(mag[on])) if np.any(on) else 0.0
    off_m = float(np.mean(mag[~on])) if np.any(~on) else 0.0
    return on_m, off_m


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
        "defect_center": _defect_center(),
        "U_on": U_on,
        "U_off": U_off,
        "score": sc,
    }

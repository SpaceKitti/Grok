"""Cover check: U_G[gamma] = (-1)^{I(gamma, Gamma)} vs Phi(n) = (-1)^n, n = sheet swap from tracking."""
from __future__ import annotations

import numpy as np

from load_surface import y_cut_gamma

N = 8000


def crossings(z: np.ndarray, lo: float, hi: float):
    """Crossings of the closed discretised loop z with the segment [lo, hi] on the real axis (Gamma itself).
    Half-open rule on Im (standard ray-casting convention) so vertices on the axis are counted once."""
    x0, y0, x1, y1 = z[:-1].real, z[:-1].imag, z[1:].real, z[1:].imag
    up = (y0 <= 0) & (y1 > 0)
    dn = (y1 <= 0) & (y0 > 0)
    m = up | dn
    xc = x0[m] + (0 - y0[m]) * (x1[m] - x0[m]) / (y1[m] - y0[m])
    inside = (xc >= lo) & (xc <= hi)
    unsigned = int(np.sum(inside))
    signed = int(np.sum(np.where(up[m], 1, -1)[inside]))
    return unsigned, signed, xc[inside]


def loops(E: float):
    t = np.linspace(0.0, 2.0 * np.pi, N + 1)
    r = 0.25 * E
    a = np.sqrt(2.0) * E  # lemniscate of Bernoulli with foci at +-eps_EP
    lem = a * np.cos(t) / (1 + np.sin(t) ** 2) + 1j * a * np.sin(t) * np.cos(t) / (1 + np.sin(t) ** 2)
    t2 = np.linspace(0.0, 4.0 * np.pi, 2 * N + 1)
    return {
        "+EP once (circle r=0.25 eps_EP, start 1.25 eps_EP, ccw)": E + r * np.exp(1j * t),
        "-EP once (circle r=0.25 eps_EP, start -1.25 eps_EP, ccw)": -E + r * np.exp(1j * (np.pi + t)),
        "+EP twice (same circle, 4pi)": E + r * np.exp(1j * t2),
        "-EP twice (same circle, 4pi)": -E + r * np.exp(1j * (np.pi + t2)),
        "figure-eight (lemniscate, foci +-eps_EP, lobes opposite senses, start sqrt2 eps_EP)": lem,
        "big loop around both (circle r=2 eps_EP, start 2 eps_EP)": 2.0 * E * np.exp(1j * t),
    }


def track_n(z, S):
    """n for the start sheets A and B: 1 if the tracked eigenvalue ends on the other sheet (swap), 0 if it returns."""
    H, align = S["H_A"], S["align_evals"]
    y0 = y_cut_gamma(z[0], S["EPS_EP"], S["V"])
    first = np.array([S["LAM_EP"] + 0.5 * y0, S["LAM_EP"] - 0.5 * y0])  # [A, B]
    ev = align(first, np.linalg.eigvals(H(complex(z[0]))))
    start = ev.copy()
    maxstep, mingap = 0.0, np.inf
    for zi in z[1:]:
        new = align(ev, np.linalg.eigvals(H(complex(zi))))
        maxstep = max(maxstep, float(np.max(np.abs(new - ev))))
        mingap = min(mingap, float(abs(new[0] - new[1])))
        ev = new
    n = [0 if abs(ev[j] - start[j]) < abs(ev[j] - start[1 - j]) else 1 for j in range(2)]
    return {"n_A": n[0], "n_B": n[1], "jump_ratio": maxstep / mingap}


def encloses(z, p):
    ang = np.unwrap(np.angle(z - p))
    return int(round((ang[-1] - ang[0]) / (2 * np.pi)))


def run_cover(S) -> list:
    E = S["EPS_EP"]
    rows = []
    for name, z in loops(E).items():
        un, sg, xs = crossings(z, -E, E)
        U = (-1) ** un
        tr = track_n(z, S)
        phiA, phiB = (-1) ** tr["n_A"], (-1) ** tr["n_B"]
        rows.append({"name": name, "start": complex(z[0]), "wind_plus": encloses(z, E), "wind_minus": encloses(z, -E),
                     "I": un, "I_signed": sg, "x_cross": xs, "U_G": U, **tr, "Phi_A": phiA, "Phi_B": phiB,
                     "match": (phiA == U) and (phiB == U)})
    return rows

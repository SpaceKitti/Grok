"""L4: the space H_QG acts on. Fiber C^2 (the two modes) over eps; measure on eps-space from sqrt|g| of the R1 2D metric
ds^2 = d eps^2 / F + F d tau^2 (Euclidean, F > 0, outside Gamma) and ds^2 = -F dt^2 + d eps^2 / F (Lorentzian chart, F < 0 inside Gamma)."""
from __future__ import annotations

import numpy as np
from scipy import integrate

import H_QG as HQ

E = HQ.E


def F(x):
    return x * x - E * E


def run():
    out = {"fiber_dim": 2}
    # sqrt|g| in (tau, eps) or (t, eps): |g_tt g_ee| = |F * (1/F)| = 1 on both sides
    xs = np.concatenate([np.linspace(-3 * E, -1.01 * E, 7), np.linspace(-0.99 * E, 0.99 * E, 7), np.linspace(1.01 * E, 3 * E, 7)])
    out["sqrtg"] = (min(abs(F(x) * (1 / F(x))) for x in xs), max(abs(F(x) * (1 / F(x))) for x in xs))
    # tip behaviour: g_ee = 1/F diverges, g_tautau = F -> 0; proper radial distance int d eps / sqrt|F| finite
    tip = []
    for d in (1e-2, 1e-4, 1e-6):
        x = E * (1 + d)
        lo = integrate.quad(lambda u: 1 / np.sqrt(u + E), E, x, weight="alg", wvar=(-0.5, 0.0))[0]
        tip.append({"d": d, "g_ee": 1 / F(x), "g_tt": F(x), "proper_dist": lo})
    out["tip"] = tip
    # regions: outside Gamma infinite eps-length -> constant fiber densities not normalizable; inside finite length 2 eps_EP
    out["lengths"] = {"inside": 2 * E, "outside": np.inf}
    # biorthogonal (c-product) inner product: H complex symmetric -> left eigenvectors = right^T; self-orthogonality at the EP
    sym = max(float(np.max(np.abs(HQ.H_qg_a(z) - HQ.H_qg_a(z).T))) for z in (0.3 + 0.2j, 1.4 - 0.3j, -0.8j))
    so = []
    for d in (1e-2, 1e-4, 1e-6, 1e-8):
        e = E + d
        w, R = np.linalg.eig(HQ.H_qg_a(e))
        R = R / np.linalg.norm(R, axis=0, keepdims=True)
        cprod = abs(R[:, 0] @ R[:, 0])        # |R^T R| for unit R (c-product norm)
        eta_cond = float(np.linalg.cond(np.linalg.inv(R @ R.conj().T)))   # metric operator eta = (R R^dagger)^-1
        so.append({"d": d, "cprod": float(cprod), "eta_cond": eta_cond})
    out["sym"] = sym
    out["selforth"] = so
    p = np.polyfit(np.log([s["d"] for s in so]), np.log([s["cprod"] for s in so]), 1)[0]
    q = np.polyfit(np.log([s["d"] for s in so]), np.log([s["eta_cond"] for s in so]), 1)[0]
    out["exp_cprod"], out["exp_eta"] = float(p), float(q)
    # does H_QG act on eps? as an operator on a grid L^2(eps) x C^2 it is block diagonal: [H_QG, eps_hat] = 0
    grid = np.linspace(1.05 * E, 3 * E, 12)
    Hbig = np.zeros((24, 24), dtype=complex); X = np.zeros((24, 24), dtype=complex)
    for i, x in enumerate(grid):
        Hbig[2 * i:2 * i + 2, 2 * i:2 * i + 2] = HQ.H_qg_a(x); X[2 * i:2 * i + 2, 2 * i:2 * i + 2] = x * np.eye(2)
    out["comm_eps"] = float(np.max(np.abs(Hbig @ X - X @ Hbig)))
    return out

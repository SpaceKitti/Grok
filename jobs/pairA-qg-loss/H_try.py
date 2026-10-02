"""H_try(eps) = H_curve(eps) + i eta_g F_JT(eps) M; spectrum, EPs, swap/return, copy test."""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

import loss_term as LT

E, LAM, V, I2, SZ = LT.EPS_EP, LT.LAM_EP, LT.V, LT.I2, LT.SZ


def H_curve(eps):
    e = complex(eps)
    return LAM * I2 + V * np.array([[e, E], [-E, -e]], dtype=complex)


def make_H(eta, M):
    def H(eps):
        return H_curve(eps) + LT.loss(eps, eta, M)
    return H


def disc_poly(eta, M):
    """discriminant (tr^2 - 4 det) of H_try as a polynomial in eps (exact coefficients by sampling, degree <= 4)."""
    H = make_H(eta, M)
    xs = np.linspace(-2, 2, 9)
    d = [np.trace(H(x)) ** 2 - 4 * np.linalg.det(H(x)) for x in xs]
    c = np.polyfit(xs, np.array(d), 4)
    c[np.abs(c) < 1e-12 * np.max(np.abs(c))] = 0
    return np.trim_zeros(c, "f")


def eps_points(eta, M):
    c = disc_poly(eta, M)
    return np.roots(c) if len(c) > 1 else np.array([])


def swap_around(H, z0, r, turns, n=6000):
    th = np.linspace(0, 2 * np.pi * turns, n * turns + 1)
    z = z0 + r * np.exp(1j * th)
    w0 = np.linalg.eigvals(H(z[0])); cur = w0.copy()
    for zi in z[1:]:
        w = np.linalg.eigvals(H(zi))
        cur = w if np.sum(np.abs(w - cur)) <= np.sum(np.abs(w[::-1] - cur)) else w[::-1]
    return [int(np.argmin(np.abs(w0 - cur[j])) != j) for j in range(2)]


def ep_report(eta, M):
    H = make_H(eta, M)
    roots = eps_points(eta, M)
    rows = []
    for z0 in roots:
        others = [abs(z0 - o) for o in roots if o is not z0 and abs(z0 - o) > 1e-9]
        r = 0.2 * min(others + [E])
        rows.append({"eps": complex(z0), "swap": swap_around(H, z0, r, 1), "ret": swap_around(H, z0, r, 2),
                     "in_loop": abs(z0 - E) < 0.25 * E, "r": r})
    keep = [abs(H(s * E)[0, 0] - H_curve(s * E)[0, 0]) < 1e-15 and min(abs(roots - s * E)) < 1e-6 for s in (1, -1)] if len(roots) else [False, False]
    return {"roots": roots, "rows": rows, "pm_kept": keep, "coeffs": disc_poly(eta, M)}


# ---------------------------------------------------------------- copy test
def copy_test(H, traceless=False, n_starts=4, seed=0):
    # ===== COPY-CHECK ONLY: a and b appear here and nowhere else in the construction =====
    A_RATE, B_RATE = 0.12337, 0.49348      # handoff seed.py constants, used ONLY for this comparison
    def H_A(eps):
        return np.array([[-1j * A_RATE, V * eps], [V * eps, -1j * B_RATE]], dtype=complex)
    # =======================================================================================
    samples = [0.31 + 0.12j, -0.77 + 0.05j, 1.3 - 0.4j, 0.05 - 0.6j, -1.6 + 0.3j, 0.9 + 0.7j]
    def tl(M):
        return M - np.trace(M) / 2 * I2 if traceless else M
    def smin(al, be):
        rows = []
        for e in samples:
            P, Q = tl(H(e)), tl(H_A(al * e + be))
            rows.append(np.kron(P.T, I2) - np.kron(I2, Q))
        Mx = np.vstack(rows)
        sv = np.linalg.svd(Mx, compute_uv=False)
        return sv[-1] / sv[0]
    rng = np.random.default_rng(seed)
    best = (np.inf, None)
    starts = [(1, 0, 0, 0)] + [tuple(rng.normal(size=4)) for _ in range(n_starts)]
    for s0 in starts:
        f = lambda p: smin(p[0] + 1j * p[1], p[2] + 1j * p[3])
        res = minimize(f, np.array(s0, dtype=float), method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-16, "maxiter": 1500})
        if res.fun < best[0]:
            best = (float(res.fun), res.x)
    s_id = smin(1.0, 0.0)
    # spectrum comparison on a grid (identity parametrisation)
    grid = [complex(x, y) for x in np.linspace(-3 * E, 3 * E, 25) for y in np.linspace(-E, E, 7)]
    def spec_err(a, b):
        err = 0.0
        for e in grid:
            w1 = np.linalg.eigvals(tl(a(e))); w2 = np.linalg.eigvals(tl(b(e)))
            err = max(err, min(np.max(np.abs(w1 - w2)), np.max(np.abs(w1 - w2[::-1]))))
        return err
    return {"smin_identity": float(s_id), "smin_best": best[0], "alpha_beta": best[1], "spec_err": float(spec_err(H, H_A)),
            "copy": best[0] <= 1e-8}

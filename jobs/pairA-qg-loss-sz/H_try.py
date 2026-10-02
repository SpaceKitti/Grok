"""pairA-qg-loss-sz: H_try = H_A(eta_g = 0 part) + i eta_g F_JT sigma_z, in H_A's basis. Numbers only from the job spec (Akitti, 2026-09-26)."""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

# ---- numbers from the job spec (Akitti, pairA-qg-loss-sz), hard-coded; no folder is loaded
A, B = 0.12337, 0.49348
V = -0.360253
EPS_EP = 0.51368066
LAM_EP = -0.308425j
KAPPA = (B - A) / 2          # > 0; -i(a-b)/2 = +i kappa

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def F_JT(e):
    return e * e - EPS_EP ** 2


def H_A_rates(eps, a, b):
    return np.array([[-1j * a, V * eps], [V * eps, -1j * b]], dtype=complex)


def H_A(eps):
    return H_A_rates(complex(eps), A, B)


def H_real(eps):
    """lambda_EP*1 + v eps sigma_x - i(a-b)/2 sigma_z  (= H_A, by construction)."""
    return LAM_EP * I2 + V * eps * SX - 1j * (A - B) / 2 * SZ


def make_H(eta):
    def H(eps):
        e = complex(eps)
        return H_real(e) + 1j * eta * F_JT(e) * SZ
    return H


def disc_coeffs(eta):
    """D(eps) = v^2 eps^2 - (kappa + eta F)^2, highest power first."""
    c = KAPPA - eta * EPS_EP ** 2
    return np.array([-eta ** 2, 0.0, V ** 2 - 2 * eta * c, 0.0, -c ** 2])


def disc_numeric(H, eps):
    M = H(eps)
    return (np.trace(M) ** 2 - 4 * np.linalg.det(M)) / 4


def swap_around(H, z0, r, turns, n=6000):
    th = np.linspace(0, 2 * np.pi * turns, n * turns + 1)
    z = z0 + r * np.exp(1j * th)
    w0 = np.linalg.eigvals(H(z[0])); cur = w0.copy()
    for zi in z[1:]:
        w = np.linalg.eigvals(H(zi))
        cur = w if np.sum(np.abs(w - cur)) <= np.sum(np.abs(w[::-1] - cur)) else w[::-1]
    return [int(np.argmin(np.abs(w0 - cur[j])) != j) for j in range(2)]


def copy_test(H, traceless=False, n_starts=4, seed=0):
    samples = [0.31 + 0.12j, -0.77 + 0.05j, 1.3 - 0.4j, 0.05 - 0.6j, -1.6 + 0.3j, 0.9 + 0.7j]
    def tl(M):
        return M - np.trace(M) / 2 * I2 if traceless else M
    def smin(al, be):
        rows = [np.kron(tl(H(e)).T, I2) - np.kron(I2, tl(H_A(al * e + be))) for e in samples]
        sv = np.linalg.svd(np.vstack(rows), compute_uv=False)
        return sv[-1] / sv[0]
    rng = np.random.default_rng(seed)
    best = (np.inf, None)
    for s0 in [(1, 0, 0, 0)] + [tuple(rng.normal(size=4)) for _ in range(n_starts)]:
        f = lambda p: smin(p[0] + 1j * p[1], p[2] + 1j * p[3])
        res = minimize(f, np.array(s0, dtype=float), method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-16, "maxiter": 1500})
        if res.fun < best[0]:
            best = (float(res.fun), res.x)
    return {"smin_best": best[0], "alpha_beta": best[1], "copy": best[0] <= 1e-8}

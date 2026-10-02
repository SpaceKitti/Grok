"""
Layer A.2 — Galerkin spectrum of the dissipative Alfvén generator.

  A = ε x + i η ∂_xx on x∈[-1,1], Dirichlet.
  φ_n = sin(n π (x+1)/2), n = 1..N.

Square Galerkin in the N-dimensional sine subspace. ∂_xx is diagonal
in this basis, so there is no larger operator to rectangular-truncate.
(N+3)×N Petrov–Galerkin is not used; flagged in RESULTS.

Not tearing. Not a dynamo rename.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

ETA = 0.05
A_REF = 0.12337
B_REF = 0.49348
V_REF = -0.360253
EPS_EP_REF = 0.513681
LAM_EP_REF = -0.308425j
REQUIRED_EPS = np.array([0.20, 0.35, 0.45, 0.513681, 0.60, 0.80, 1.00])


def phi_n(x: np.ndarray, n: int) -> np.ndarray:
    return np.sin(n * np.pi * (x + 1.0) / 2.0)


def X_element(m: int, n: int) -> float:
    """⟨φ_m, x φ_n⟩ on [-1,1]. Zero unless m-n odd. Diagonal is 0."""
    if m == n:
        return 0.0
    if (m - n) % 2 == 0:
        return 0.0
    return (4.0 / np.pi**2) * (1.0 / (m + n) ** 2 - 1.0 / (m - n) ** 2)


def assemble_H(N: int, eps: float, eta: float = ETA) -> np.ndarray:
    """Square N×N Galerkin. Orthonormal Dirichlet sines, M = I."""
    n = np.arange(1, N + 1, dtype=float)
    Ddiag = -((n * np.pi / 2.0) ** 2)
    H = np.diag(1j * eta * Ddiag).astype(complex)
    for i in range(N):
        for j in range(i + 1, N):
            xij = X_element(i + 1, j + 1)
            H[i, j] = eps * xij
            H[j, i] = eps * xij
    return H


def n2_check(eta: float = ETA) -> dict:
    """Rebuild a,b,v from N=2 Galerkin. STOP if max abs err > 0.05."""
    a = eta * (np.pi / 2.0) ** 2
    b = eta * np.pi**2
    v = X_element(1, 2)
    err = np.array([abs(a - A_REF), abs(b - B_REF), abs(v - V_REF)])
    H = assemble_H(2, 1.0, eta)
    return {
        "a": float(a),
        "b": float(b),
        "v": float(v),
        "err": err,
        "max_abs_err": float(np.max(err)),
        "pass": bool(np.max(err) <= 0.05),
        "H_eps1": H,
    }


def eigensolve(N: int, eps: float, eta: float = ETA) -> dict:
    H = assemble_H(N, eps, eta)
    w, V = np.linalg.eig(H)
    res = np.zeros(N)
    for k in range(N):
        Av = H @ V[:, k]
        res[k] = float(np.linalg.norm(Av - w[k] * V[:, k]) / (np.linalg.norm(V[:, k]) + 1e-16))
    # highly damped Dirichlet tail: n ≳ 2N/3
    n_idx = np.arange(1, N + 1)
    damp_scale = eta * (n_idx * np.pi / 2.0) ** 2
    # participation: which sine weights dominate each eigenvector
    weights = np.abs(V) ** 2
    n_bar = weights.T @ n_idx
    spurious = n_bar > (2.0 * N / 3.0)
    return {
        "H": H,
        "evals": w,
        "evecs": V,
        "residual": res,
        "n_bar": n_bar,
        "spurious": spurious,
        "damp_scale": damp_scale,
        "eps": eps,
        "eta": eta,
        "N": N,
    }


def sweep(N: int, eps_list: np.ndarray, eta: float = ETA) -> dict:
    recs = []
    for e in eps_list:
        recs.append(eigensolve(N, float(e), eta))
    nmax = max(r["evals"].size for r in recs)
    ev = np.full((len(recs), nmax), np.nan + 1j * np.nan)
    res = np.full((len(recs), nmax), np.nan)
    spur = np.zeros((len(recs), nmax), dtype=bool)
    nbar = np.full((len(recs), nmax), np.nan)
    for i, r in enumerate(recs):
        m = r["evals"].size
        ev[i, :m] = r["evals"]
        res[i, :m] = r["residual"]
        spur[i, :m] = r["spurious"]
        nbar[i, :m] = r["n_bar"]
    return {
        "eps": np.asarray(eps_list, float),
        "eta": eta,
        "N": N,
        "evals": ev,
        "residual": res,
        "spurious": spur,
        "n_bar": nbar,
        "records": recs,
    }


def save_sweep(sw: dict, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / f"slab_eigs_N{sw['N']}.npz"
    np.savez(
        path,
        eps=sw["eps"],
        eta=np.array([sw["eta"]]),
        N=np.array([sw["N"]]),
        evals=sw["evals"],
        residual=sw["residual"],
        spurious=sw["spurious"],
        n_bar=sw["n_bar"],
    )
    for e in REQUIRED_EPS:
        j = int(np.argmin(np.abs(sw["eps"] - e)))
        np.savez(
            outdir / f"slab_eigs_N{sw['N']}_eps{e:g}.npz",
            eps=np.array([sw["eps"][j]]),
            eta=np.array([sw["eta"]]),
            N=np.array([sw["N"]]),
            evals=sw["evals"][j],
            residual=sw["residual"][j],
            spurious=sw["spurious"][j],
            n_bar=sw["n_bar"][j],
        )
    return path

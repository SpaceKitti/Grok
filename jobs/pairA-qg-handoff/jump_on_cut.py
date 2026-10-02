"""Layer 2 — J(ε) on Γ. V+(ε)=J(ε) V−(ε). Tips defective; holonomy = Jhat2."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from seed import EPS_EP, H_A, LAM_EP
from tracker import align_evecs, evecs_of


def jordan_at(eps: float) -> dict:
    H = H_A(complex(eps))
    lam = LAM_EP
    M = H - lam * np.eye(2)
    s = np.linalg.svd(M, compute_uv=False)
    rank = int(np.linalg.matrix_rank(M, tol=1e-8))
    return {
        "eps": eps,
        "rank": rank,
        "geom_mult": 2 - rank if rank < 2 else 2,
        "smin": float(s[-1]),
        "smax": float(s[0]),
        "defective": bool(rank == 1),
    }


def run_cut(n: int = 21, delta: float = 1e-7) -> dict:
    assert n % 2 == 1
    eps = np.linspace(-EPS_EP, EPS_EP, n)
    Jlist = np.zeros((n, 2, 2), dtype=complex)
    Vp = np.zeros((n, 2, 2), dtype=complex)
    Vm = np.zeros((n, 2, 2), dtype=complex)
    lam_p = np.zeros((n, 2), dtype=complex)
    lam_m = np.zeros((n, 2), dtype=complex)
    for i, e in enumerate(eps):
        if abs(abs(e) - EPS_EP) < 1e-12:
            w, V = evecs_of(complex(e))
            Vp[i] = Vm[i] = V
            lam_p[i] = lam_m[i] = w
            Jlist[i] = np.eye(2, dtype=complex)
            continue
        wp, Vp_i = evecs_of(complex(e) + 1j * delta)
        wm, Vm_i = evecs_of(complex(e) - 1j * delta)
        if i > 0 and abs(abs(eps[i - 1]) - EPS_EP) > 1e-12:
            Vp_i = align_evecs(Vp[i - 1], Vp_i)
            Vm_i = align_evecs(Vm[i - 1], Vm_i)
        Vp[i], Vm[i] = Vp_i, Vm_i
        lam_p[i], lam_m[i] = wp, wm
        Jlist[i] = Vp_i @ np.linalg.pinv(Vm_i)
    tips = {+1: jordan_at(EPS_EP), -1: jordan_at(-EPS_EP)}
    return {
        "eps": eps,
        "J": Jlist,
        "Vplus": Vp,
        "Vminus": Vm,
        "lam_plus": lam_p,
        "lam_minus": lam_m,
        "n_points": n,
        "tips": tips,
        "include_zero": bool(np.any(np.abs(eps) < 1e-14)),
    }


def save(d: dict, path: Path) -> None:
    np.savez(
        path,
        eps=d["eps"],
        J=d["J"],
        Vplus=d["Vplus"],
        Vminus=d["Vminus"],
        lam_plus=d["lam_plus"],
        lam_minus=d["lam_minus"],
        n_points=np.array([d["n_points"]]),
    )

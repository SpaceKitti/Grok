"""Layer R0 — r=0 bolts at χ=0, π. Period τ=4π/ε_EP."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from seed import EPS_EP, H_A, LAM_EP


def bolts() -> dict:
    chi = np.array([0.0, np.pi])
    eps = EPS_EP * np.cos(chi)
    tau = 4.0 * np.pi / EPS_EP
    w0 = np.linalg.eigvals(H_A(eps[0]))
    wpi = np.linalg.eigvals(H_A(eps[1]))
    return {
        "chi": chi,
        "eps": eps,
        "tau": tau,
        "evals_chi0": w0,
        "evals_chipi": wpi,
        "lam_ep": LAM_EP,
    }


def save_txt(d: dict, path: Path) -> None:
    path.write_text(
        f"r=0\n"
        f"chi=0  eps={d['eps'][0]:.12f}  (bolt +)\n"
        f"chi=pi eps={d['eps'][1]:.12f}  (bolt -)\n"
        f"tau=4*pi/eps_EP={d['tau']:.12f}\n"
        f"evals chi=0  {d['evals_chi0']}\n"
        f"evals chi=pi {d['evals_chipi']}\n",
        encoding="utf-8",
    )

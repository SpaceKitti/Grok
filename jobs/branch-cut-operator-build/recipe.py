"""
GSG 2004 recipe, stolen as a checklist — not a dynamo.

Two modes, one parameter that can drive them together, allow a Jordan
block (algebraic 2, geometric 1). If an EP2 appears, demand square-root
Puiseux and 4π monodromy. Object 0 already showed this pipeline fires
when an EP2 is present.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def jordan_defect(H: np.ndarray, lam: complex | None = None) -> float:
    """smin / smax of (H - λI). ~1 at a rank-1 Jordan block, ~0 at a scalar matrix."""
    w = np.linalg.eigvals(H)
    if lam is None:
        lam = 0.5 * (w[0] + w[1])
    s = np.linalg.svd(H - lam * np.eye(H.shape[0]), compute_uv=False)
    if s[0] < 1e-14:
        return 0.0
    return float(s[-1] / (s[0] + 1e-16))


def petermann(H: np.ndarray, idx: int = 0) -> float:
    w, Vr = np.linalg.eig(H)
    wl, Vl = np.linalg.eig(H.conj().T)
    j = int(np.argmin(np.abs(wl - w[idx].conj())))
    L, R = Vl[:, j], Vr[:, idx]
    ov = np.vdot(L, R) / ((np.linalg.norm(L) * np.linalg.norm(R)) + 1e-30)
    return float(1.0 / (np.abs(ov) ** 2 + 1e-30))


def _align_sheets(prev: np.ndarray, curr: np.ndarray) -> np.ndarray:
    d00 = np.abs(curr[0] - prev[0]) + np.abs(curr[1] - prev[1])
    d01 = np.abs(curr[0] - prev[1]) + np.abs(curr[1] - prev[0])
    return curr[::-1].copy() if d01 < d00 else curr.copy()


def _align_evecs(prev: np.ndarray, curr: np.ndarray) -> np.ndarray:
    ov = np.abs(prev.conj().T @ curr)
    perm = [0, 1]
    used: set[int] = set()
    for i in range(2):
        j = int(np.argmax(ov[i]))
        if j in used:
            j = 1 - j
        used.add(j)
        perm[i] = j
    out = curr[:, perm]
    for i in range(2):
        ph = np.vdot(prev[:, i], out[:, i])
        if np.abs(ph) > 0:
            out[:, i] = out[:, i] * np.exp(-1j * np.angle(ph))
        out[:, i] = out[:, i] / (np.linalg.norm(out[:, i]) + 1e-16)
    return out


def monodromy_loop(H_of_z, z_ep: complex, radius: float = 0.2, n_theta: int = 721) -> dict:
    """Encircling z_ep in a complex parameter. EP2: swap at 2π, return at 4π."""
    theta = np.linspace(0.0, 4.0 * np.pi, n_theta)
    z_path = z_ep + radius * np.exp(1j * theta)
    evals = np.zeros((n_theta, 2), dtype=complex)
    evecs = np.zeros((n_theta, 2, 2), dtype=complex)
    for i, z in enumerate(z_path):
        H = H_of_z(z)
        w_raw, V_raw = np.linalg.eig(H)
        if i == 0:
            evals[0] = w_raw
            nrm = np.linalg.norm(V_raw, axis=0, keepdims=True) + 1e-16
            evecs[0] = V_raw / nrm
            continue
        w = _align_sheets(evals[i - 1], w_raw)
        perm = [int(np.argmin(np.abs(w_raw - w[0]))), 0]
        perm[1] = (
            1 - perm[0]
            if int(np.argmin(np.abs(w_raw - w[1]))) == perm[0]
            else int(np.argmin(np.abs(w_raw - w[1])))
        )
        if perm[0] == perm[1]:
            perm = [0, 1]
        V = _align_evecs(evecs[i - 1], V_raw[:, perm])
        evals[i] = w
        evecs[i] = V
    i2 = int(np.argmin(np.abs(theta - 2.0 * np.pi)))
    i4 = n_theta - 1
    swap = float(np.abs(evals[i2, 0] - evals[0, 1]) + np.abs(evals[i2, 1] - evals[0, 0]))
    stay = float(np.abs(evals[i2, 0] - evals[0, 0]) + np.abs(evals[i2, 1] - evals[0, 1]))
    stay4 = float(np.abs(evals[i4, 0] - evals[0, 0]) + np.abs(evals[i4, 1] - evals[0, 1]))
    swapped = swap < stay

    def rp(a, b):
        return float(np.arccos(np.clip(np.abs(np.vdot(a, b)), 0.0, 1.0)))

    ang2 = rp(evecs[0, :, 0], evecs[i2, :, 0])
    ang4 = rp(evecs[0, :, 0], evecs[i4, :, 0])
    ang2x = rp(evecs[0, :, 1], evecs[i2, :, 0])
    needs_4pi = (ang4 < 0.25) and (ang2x < 0.35 or ang2 > 0.4)
    return {
        "theta": theta,
        "evals": evals,
        "evecs": evecs,
        "swapped_at_2pi": bool(swapped),
        "return_4pi": float(stay4),
        "needs_4pi": bool(needs_4pi),
        "ep2_monodromy": bool(swapped and stay4 < 0.08 and needs_4pi),
        "z_path": z_path,
        "z_ep": z_ep,
        "radius": radius,
    }


def puiseux_real(H_of_eps, eps_ep: float, side: float = 1.0, n: int = 24) -> dict:
    """Approach eps_ep from the split side. Expect |λ+-λ-| ~ c |ε-ε_ep|^{1/2}."""
    delta = side * np.logspace(-7, -2, n)
    split = np.zeros(n)
    for i, d in enumerate(delta):
        w = np.linalg.eigvals(H_of_eps(eps_ep + d))
        split[i] = 0.5 * np.abs(w[0] - w[1])
    mask = split > 0
    logd = np.log(np.abs(delta[mask]))
    logs = np.log(split[mask])
    p, intercept = np.polyfit(logd, logs, 1)
    fit = np.exp(intercept) * np.abs(delta[mask]) ** p
    rel = float(np.max(np.abs(split[mask] - fit) / (split[mask] + fit + 1e-16)))
    return {
        "exponent": float(p),
        "c": float(np.exp(intercept)),
        "rel_residual": rel,
        "delta": np.abs(delta),
        "split": split,
        "passed": bool(abs(p - 0.5) < 0.12 and rel < 0.08),
    }


@dataclass
class Checklist:
    ep2_found: bool
    jordan: bool
    puiseux_half: bool
    mono_4pi: bool
    on_cut: bool
    exponent: float
    defect: float
    petermann: float
    lam_ep: complex
    eps_ep: float
    Gamma: tuple[float, float]
    notes: str

    @property
    def passed(self) -> bool:
        return self.ep2_found and self.jordan and self.puiseux_half and self.mono_4pi and self.on_cut

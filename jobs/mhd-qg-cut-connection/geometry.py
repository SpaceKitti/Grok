"""
Track 0 — geometry of the cut. No new physics claim.

Γ is a finite slit (the Alfvén continuum interval). Two sheets are glued
along it. The endpoints are square-root branch points. Standard cut
convention: Arg = ±π on the two faces of Γ.

Exports: n_sheet, Arg_Γ, jump of the MHD label-2×2 across a loop that
encircles one endpoint.
"""

from __future__ import annotations

import numpy as np

from mhd import H_A, eps_ep, lam_A


def _align(prev: np.ndarray, curr: np.ndarray) -> np.ndarray:
    d00 = abs(curr[0] - prev[0]) + abs(curr[1] - prev[1])
    d01 = abs(curr[0] - prev[1]) + abs(curr[1] - prev[0])
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
            out[:, i] *= np.exp(-1j * np.angle(ph))
        nrm = np.linalg.norm(out[:, i]) + 1e-16
        out[:, i] /= nrm
    return out


def label_jump_around_endpoint(n_theta: int = 721, radius_frac: float = 0.25) -> dict:
    """
    Loop ε(θ) = ε_EP + r e^{iθ}, θ: 0 → 4π, around the + branch point.
    Jump of the 2×2: eigenvalue permutation and eigenvector sign.
    """
    ep = eps_ep()
    r = radius_frac * ep
    theta = np.linspace(0.0, 4.0 * np.pi, n_theta)
    z = ep + r * np.exp(1j * theta)
    evals = np.zeros((n_theta, 2), dtype=complex)
    evecs = np.zeros((n_theta, 2, 2), dtype=complex)
    for i, zi in enumerate(z):
        H = H_A(zi)
        w_raw, V_raw = np.linalg.eig(H)
        if i == 0:
            evals[0] = w_raw
            evecs[0] = V_raw / (np.linalg.norm(V_raw, axis=0, keepdims=True) + 1e-16)
            continue
        w = _align(evals[i - 1], w_raw)
        perm = [int(np.argmin(np.abs(w_raw - w[0]))), 0]
        perm[1] = (
            1 - perm[0]
            if int(np.argmin(np.abs(w_raw - w[1]))) == perm[0]
            else int(np.argmin(np.abs(w_raw - w[1])))
        )
        if perm[0] == perm[1]:
            perm = [0, 1]
        evals[i] = w
        evecs[i] = _align_evecs(evecs[i - 1], V_raw[:, perm])

    i2 = int(np.argmin(np.abs(theta - 2.0 * np.pi)))
    i4 = n_theta - 1
    swap2 = abs(evals[i2, 0] - evals[0, 1]) + abs(evals[i2, 1] - evals[0, 0])
    stay2 = abs(evals[i2, 0] - evals[0, 0]) + abs(evals[i2, 1] - evals[0, 1])
    stay4 = abs(evals[i4, 0] - evals[0, 0]) + abs(evals[i4, 1] - evals[0, 1])
    swapped = swap2 < stay2

    # sheet index from sqrt covering: Arg(λ − λ_mid) / π
    mid = 0.5 * (evals[0, 0] + evals[0, 1])
    split = evals[:, 0] - mid
    arg = np.unwrap(np.angle(split))
    n_sheet = np.floor((arg - arg[0]) / np.pi + 1e-9)

    # jump matrix on eigenvectors after 2π: v(2π) ≈ J v(0)
    # with continuation, column 0 at 2π is the continuation of column 0,
    # which has moved to the other sheet.
    J2 = evecs[i2] @ np.linalg.pinv(evecs[0])
    J4 = evecs[i4] @ np.linalg.pinv(evecs[0])

    return {
        "theta": theta,
        "z": z,
        "evals": evals,
        "evecs": evecs,
        "n_sheet": n_sheet,
        "arg_split": arg,
        "swapped_2pi": bool(swapped),
        "dn_2pi": int(n_sheet[i2] - n_sheet[0]),
        "dn_4pi": int(n_sheet[i4] - n_sheet[0]),
        "stay4": float(stay4),
        "J_2pi": J2,
        "J_4pi": J4,
        "eps_ep": ep,
        "radius": r,
        "i2": i2,
        "i4": i4,
    }


def arg_along_gamma(eps: float, n: int = 401) -> dict:
    """
    Faces of the slit: Arg = +π on the upper face, −π on the lower face
    (standard cut). Midpoint Arg = 0 off the cut on the principal sheet.
    """
    lo, hi = -abs(eps), abs(eps)
    s = np.linspace(lo, hi, n)
    arg_plus = np.full(n, np.pi)   # upper face
    arg_minus = np.full(n, -np.pi)  # lower face
    jump = arg_plus - arg_minus  # 2π across the two faces of a log;
    # for a square-root cut the *function* jumps by π in Arg(sqrt).
    arg_sqrt_jump = np.pi * np.ones(n)
    return {
        "s": s,
        "lo": lo,
        "hi": hi,
        "Arg_plus": arg_plus,
        "Arg_minus": arg_minus,
        "Arg_sqrt_jump": arg_sqrt_jump,
        "n_sheet_plus": np.zeros(n, dtype=int),
        "n_sheet_minus": np.ones(n, dtype=int),
    }

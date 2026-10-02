"""
Nearest-neighbour sheet align + overlap phase pin.
Rule copied from C:\\Users\\Akitt\\mhd-qg-cut-connection\\geometry.py
(used, not rewritten as new physics).
"""

from __future__ import annotations

import numpy as np

from seed import H_A


USED_HELPER = r"C:\Users\Akitt\mhd-qg-cut-connection\geometry.py"


def align_evals(prev: np.ndarray, curr: np.ndarray) -> np.ndarray:
    d00 = abs(curr[0] - prev[0]) + abs(curr[1] - prev[1])
    d01 = abs(curr[0] - prev[1]) + abs(curr[1] - prev[0])
    return curr[::-1].copy() if d01 < d00 else curr.copy()


def align_evecs(prev: np.ndarray, curr: np.ndarray) -> np.ndarray:
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


def evecs_of(eps: complex) -> tuple[np.ndarray, np.ndarray]:
    w, V = np.linalg.eig(H_A(eps))
    V = V / (np.linalg.norm(V, axis=0, keepdims=True) + 1e-16)
    return w, V


def continue_loop(z_path: np.ndarray) -> dict:
    n = z_path.size
    evals = np.zeros((n, 2), dtype=complex)
    evecs = np.zeros((n, 2, 2), dtype=complex)
    for i, zi in enumerate(z_path):
        w_raw, V_raw = np.linalg.eig(H_A(zi))
        if i == 0:
            evals[0] = w_raw
            evecs[0] = V_raw / (np.linalg.norm(V_raw, axis=0, keepdims=True) + 1e-16)
            continue
        w = align_evals(evals[i - 1], w_raw)
        perm = [int(np.argmin(np.abs(w_raw - w[0]))), 0]
        perm[1] = (
            1 - perm[0]
            if int(np.argmin(np.abs(w_raw - w[1]))) == perm[0]
            else int(np.argmin(np.abs(w_raw - w[1])))
        )
        if perm[0] == perm[1]:
            perm = [0, 1]
        evals[i] = w
        evecs[i] = align_evecs(evecs[i - 1], V_raw[:, perm])
    return {"evals": evals, "evecs": evecs, "z": z_path}

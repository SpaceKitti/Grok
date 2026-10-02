"""
Shared EXPERIMENT, not a QG letter.
Locked pair A (not rebuilt). Same loop family for every track.
"""

from __future__ import annotations

import numpy as np

ETA = 0.05
V = -0.360253
A_DAMP = ETA * (np.pi / 2.0) ** 2
B_DAMP = ETA * np.pi ** 2
EPS_EP = abs(B_DAMP - A_DAMP) / (2.0 * abs(V))  # 0.513681
R_LOOP = 0.25 * EPS_EP
CENTER_ON = complex(EPS_EP, 0.0)
CENTER_OFF = complex(0.0, 1.2)
N_THETA = 361
GAMMA = (-EPS_EP, EPS_EP)


def H_A(eps: complex) -> np.ndarray:
    return np.array(
        [[-1j * A_DAMP, eps * V], [eps * V, -1j * B_DAMP]],
        dtype=complex,
    )


def loop_points(center: complex, n: int = N_THETA) -> tuple[np.ndarray, np.ndarray]:
    theta = np.linspace(0.0, 4.0 * np.pi, n)
    z = center + R_LOOP * np.exp(1j * theta)
    return theta, z


def n_mhd() -> dict:
    theta, z = loop_points(CENTER_ON)
    evals = np.zeros((theta.size, 2), dtype=complex)
    for i, zi in enumerate(z):
        w = np.linalg.eigvals(H_A(zi))
        if i == 0:
            evals[0] = w
            continue
        d00 = abs(w[0] - evals[i - 1, 0]) + abs(w[1] - evals[i - 1, 1])
        d01 = abs(w[0] - evals[i - 1, 1]) + abs(w[1] - evals[i - 1, 0])
        evals[i] = w[::-1] if d01 < d00 else w
    mid = 0.5 * (evals[0, 0] + evals[0, 1])
    arg = np.unwrap(np.angle(evals[:, 0] - mid))
    n_sheet = np.floor((arg - arg[0]) / np.pi + 1e-9)
    i2 = int(np.argmin(np.abs(theta - 2.0 * np.pi)))
    i4 = theta.size - 1
    return {
        "theta": theta,
        "z": z,
        "n_sheet": n_sheet,
        "i2": i2,
        "i4": i4,
        "dn_2pi": int(n_sheet[i2] - n_sheet[0]),
        "dn_4pi": int(n_sheet[i4] - n_sheet[0]),
    }


def score_S(U_on: np.ndarray, U_off: np.ndarray, spatial_on: float, spatial_off: float,
            n_sheet: np.ndarray, i2: int, i4: int, defined: bool, inserted: bool) -> dict:
    """S1–S4 and verdict language. spatial_* = mean |letter−1| on/off Γ."""
    if not defined:
        return {
            "S1": False, "S2": False, "S3": False, "S4": False,
            "s1": "undefined", "s2": "undefined", "s3": "undefined", "s4": "undefined",
            "verdict": "could not define",
            "defined": False,
        }
    if inserted:
        return {
            "S1": False, "S2": False, "S3": False, "S4": False,
            "s1": "inserted", "s2": "inserted", "s3": "inserted", "s4": "inserted",
            "verdict": "inserted",
            "defined": True,
        }
    ratio = float(spatial_on / (spatial_off + 1e-16))
    s1 = bool(ratio >= 3.0)
    U2, U4 = U_on[i2], U_on[i4]
    s2 = bool(abs(U2 + 1.0) < 0.2 and abs(U4 - 1.0) < 0.2)
    # S3: letter jumps when n jumps, not merely drifts with θ
    n = n_sheet
    dU = np.abs(np.diff(U_on, prepend=U_on[0]))
    dn = np.abs(np.diff(n, prepend=n[0]))
    jump_mask = dn > 0.5
    quiet_mask = (dn <= 0.5) & (np.arange(n.size) > 2)
    mean_at = float(np.mean(dU[jump_mask])) if np.any(jump_mask) else 0.0
    mean_quiet = float(np.mean(dU[quiet_mask])) if np.any(quiet_mask) else 1.0
    s3 = bool(mean_at > 3.0 * mean_quiet + 1e-6)
    sig_on = float(abs(U_on[i2] - 1.0))
    sig_off = float(abs(U_off[min(i2, U_off.size - 1)] - 1.0))
    drop = sig_on / (sig_off + 1e-16)
    s4 = bool(drop >= 3.0)

    if s1 and s2 and s4:
        verdict = "jumps with MHD"
    elif s1 is False and abs(spatial_on) < 1e-9 and abs(spatial_off) < 1e-9:
        verdict = "misses Γ"
    elif not s1 and abs(drop - 1.0) < 0.3 and sig_on > 1e-6:
        verdict = "global junk"
    elif not s1:
        verdict = "misses Γ"
    else:
        verdict = "misses Γ"

    return {
        "S1": s1, "S2": s2, "S3": s3, "S4": s4,
        "s1": f"on/off={ratio:.4f} (on={spatial_on:.4g}, off={spatial_off:.4g})",
        "s2": f"U(2π)={U2.real:.4f}{U2.imag:+.4f}j |U+1|={abs(U2+1):.3f}; U(4π)={U4.real:.4f}{U4.imag:+.4f}j |U-1|={abs(U4-1):.3f}",
        "s3": f"|ΔU|_at n-jump / |ΔU|_quiet = {mean_at / (mean_quiet + 1e-16):.4f}",
        "s4": f"drop={drop:.4f}  |U-1|_on={sig_on:.4f} |_off={sig_off:.4f}",
        "verdict": verdict,
        "defined": True,
        "U2": U2, "U4": U4, "ratio": ratio, "drop": drop,
    }

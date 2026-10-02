"""Scoring only. Not a QG letter."""

from __future__ import annotations

import numpy as np

from protocol import GAMMA, on_gamma


def summarize_scan(sites: np.ndarray, signal: np.ndarray, band: float = 0.06) -> dict:
    i_max = int(np.argmax(signal))
    p_max = complex(sites[i_max])
    sig_max = float(signal[i_max])
    on = np.array([on_gamma(complex(s), band) for s in sites])
    max_on = float(np.max(signal[on])) if np.any(on) else 0.0
    max_off = float(np.max(signal[~on])) if np.any(~on) else 0.0
    ratio = max_on / (max_off + 1e-16)
    n_tie = int(np.sum(np.abs(signal - sig_max) < 1e-9 * max(sig_max, 1.0) + 1e-15))
    if n_tie > 1:
        tied = sites[np.abs(signal - sig_max) < 1e-9 * max(sig_max, 1.0) + 1e-15]
        p_max = complex(np.mean(tied.real), np.mean(tied.imag))
    return {
        "P_site": p_max,
        "sig_max": sig_max,
        "max_on": max_on,
        "max_off": max_off,
        "ratio": float(ratio),
        "n_tie": n_tie,
        "on_gamma": bool(on_gamma(p_max, band)),
    }


def s2_s3_s4(U_on: np.ndarray, U_off: np.ndarray, n_sheet: np.ndarray, i2: int, i4: int) -> dict:
    U2, U4 = U_on[i2], U_on[i4]
    s2 = bool(abs(U2 + 1.0) < 0.2 and abs(U4 - 1.0) < 0.2)
    dU = np.abs(np.diff(U_on, prepend=U_on[0]))
    dn = np.abs(np.diff(n_sheet, prepend=n_sheet[0]))
    jump = dn > 0.5
    quiet = (dn <= 0.5) & (np.arange(n_sheet.size) > 2)
    at = float(np.mean(dU[jump])) if np.any(jump) else 0.0
    qi = float(np.mean(dU[quiet])) if np.any(quiet) else 1.0
    s3 = bool(at > 3.0 * qi + 1e-6)
    sig_on = float(abs(U_on[i2] - 1.0))
    sig_off = float(abs(U_off[min(i2, U_off.size - 1)] - 1.0))
    drop = sig_on / (sig_off + 1e-16)
    s4 = bool(drop >= 3.0)
    return {
        "S2": s2, "S3": s3, "S4": s4,
        "s2": (
            f"U(2π)={U2.real:.4f}{U2.imag:+.4f}j |U+1|={abs(U2+1):.3f}; "
            f"U(4π)={U4.real:.4f}{U4.imag:+.4f}j |U-1|={abs(U4-1):.3f}"
        ),
        "s3": f"|ΔU|_jump / |ΔU|_quiet = {at / (qi + 1e-16):.4f}",
        "s4": f"drop={drop:.4f} |U-1|_on={sig_on:.4f} |_off={sig_off:.4f}",
        "U2": U2, "U4": U4, "drop": drop,
    }


def verdict(inserted: bool, defined: bool, s1: bool, s2: bool, s3: bool, s4: bool,
            p_on_gamma: bool, p_off_on_gamma: bool, ratio: float, drop: float,
            uniform: bool) -> str:
    if not defined:
        return "could not define"
    if inserted:
        return "inserted"
    if uniform:
        return "global junk"
    # max follows the control loop off Γ → not a slit preference
    if p_on_gamma and not p_off_on_gamma:
        return "misses Γ"
    if s1 and p_on_gamma and p_off_on_gamma:
        return "prefers Γ"
    if abs(drop - 1.0) < 0.3 and ratio < 1.5:
        return "global junk"
    return "misses Γ"

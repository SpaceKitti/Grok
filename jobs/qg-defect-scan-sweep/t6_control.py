"""
T6 — Control. Uniform U(1) B, no defect. Must fail.

  A_x = −(B/2) y,  A_y = +(B/2) x,  B=1
  No puncture. Scan is a dummy (signal independent of site).
"""

from __future__ import annotations

import numpy as np

from protocol import CENTER_OFF, CENTER_ON, N_THETA, loop_points, sites_2d
from score import s2_s3_s4, summarize_scan, verdict

B_FIELD = 1.0
INSERTED = False


def operator_block() -> str:
    return (
        "T6  uniform U(1), no defect  (control)\n"
        "    A_x=−(B/2)y, A_y=+(B/2)x, B=1\n"
        "    U[γ]=exp(i B Area)  independent of any site"
    )


def _dA(z0: complex, z1: complex) -> float:
    x0, y0 = z0.real, z0.imag
    x1, y1 = z1.real, z1.imag
    return 0.5 * B_FIELD * (-y0 * (x1 - x0) + x0 * (y1 - y0))


def holonomy(center: complex) -> np.ndarray:
    theta, z = loop_points(center)
    U = np.ones(theta.size, dtype=complex)
    for i in range(1, theta.size):
        U[i] = U[i - 1] * np.exp(1j * _dA(z[i - 1], z[i]))
    return U


def run(mhd: dict) -> dict:
    sites = sites_2d()
    U_on = holonomy(CENTER_ON)
    U_off = holonomy(CENTER_OFF)
    sig = np.full(sites.size, abs(U_on[mhd["i2"]] - 1.0))
    sum_on = summarize_scan(sites, sig)
    sum_off = summarize_scan(sites, np.full(sites.size, abs(U_off[mhd["i2"]] - 1.0)))
    ss = s2_s3_s4(U_on, U_off, mhd["n_sheet"], mhd["i2"], mhd["i4"])
    s1 = False  # uniform: cannot prefer Γ
    v = verdict(
        INSERTED, True, s1, ss["S2"], ss["S3"], ss["S4"],
        False, False, 1.0, ss["drop"], uniform=True,
    )
    return {
        "family": "T6 uniform U(1) control",
        "operator": operator_block(),
        "inserted": INSERTED,
        "defined_without_mhd": True,
        "P_site": "uniform / none",
        "P_site_off": "uniform / none",
        "S1": s1, "S2": ss["S2"], "S3": ss["S3"], "S4": ss["S4"],
        "s1": f"P=uniform, max_on/max_off={sum_on['ratio']:.4f} (flat)",
        "s2": ss["s2"], "s3": ss["s3"], "s4": ss["s4"],
        "verdict": v,
        "U_on": U_on,
        "sig_on": sig,
        "sites": sites,
        "sum_on": sum_on,
        "sum_off": sum_off,
    }

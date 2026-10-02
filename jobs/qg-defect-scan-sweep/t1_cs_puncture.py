"""
T1 — CS puncture scan. Own operator.

U(1)_k Chern–Simons, k=8, with ONE puncture of charge q=2π/3
(not π, not fitted to −1).

  S_CS = (k/4π) ∫ A dA + q ∫_{z_p} A
  F = q δ(z − z_p)          # source at scanned site z_p, NOT stamped on Γ
  U[γ] = exp(i q W(γ, z_p))  # W = winding, an OUTPUT of the scan

Scan z_p over the 2d mesh. Holonomy of the FIXED endpoint loop vs z_p.
"""

from __future__ import annotations

import numpy as np

from protocol import (
    CENTER_OFF,
    CENTER_ON,
    loop_points,
    n_mhd,
    running_winding,
    sites_2d,
    winding,
)
from score import s2_s3_s4, summarize_scan, verdict

K_CS = 8
Q_PUNCTURE = 2.0 * np.pi / 3.0  # not π
INSERTED = False


def operator_block() -> str:
    return (
        "T1  U(1)_k CS, k=8, one puncture\n"
        "    S_CS = (k/4π)∫ A dA  +  q ∫_{z_p} A\n"
        "    q = 2π/3  (not π, not fitted)\n"
        "    F = q δ(z−z_p)  at scanned z_p\n"
        "    U[γ] = exp(i q W(γ, z_p))"
    )


def U_of_puncture(center: complex, p: complex) -> np.ndarray:
    _, z = loop_points(center)
    W = running_winding(z, p)
    return np.exp(1j * Q_PUNCTURE * W)


def signal_map(center: complex, sites: np.ndarray) -> np.ndarray:
    _, z = loop_points(center)
    sig = np.empty(sites.size)
    for i, p in enumerate(sites):
        w = winding(z, complex(p))
        U = np.exp(1j * Q_PUNCTURE * w)
        sig[i] = abs(U - 1.0)
    return sig


def run(mhd: dict) -> dict:
    sites = sites_2d()
    sig_on = signal_map(CENTER_ON, sites)
    sig_off = signal_map(CENTER_OFF, sites)
    sum_on = summarize_scan(sites, sig_on)
    sum_off = summarize_scan(sites, sig_off)
    p = sum_on["P_site"]
    U_on = U_of_puncture(CENTER_ON, p)
    U_off = U_of_puncture(CENTER_OFF, p)
    ss = s2_s3_s4(U_on, U_off, mhd["n_sheet"], mhd["i2"], mhd["i4"])
    s1 = bool(sum_on["ratio"] >= 3.0 and sum_on["on_gamma"])
    v = verdict(
        INSERTED, True, s1, ss["S2"], ss["S3"], ss["S4"],
        sum_on["on_gamma"], sum_off["on_gamma"],
        sum_on["ratio"], ss["drop"], uniform=False,
    )
    return {
        "family": "T1 CS puncture",
        "operator": operator_block(),
        "inserted": INSERTED,
        "defined_without_mhd": True,
        "P_site": sum_on["P_site"],
        "P_site_off": sum_off["P_site"],
        "S1": s1, "S2": ss["S2"], "S3": ss["S3"], "S4": ss["S4"],
        "s1": f"P={sum_on['P_site']:.4f}, n_tie={sum_on['n_tie']}, max_on/max_off={sum_on['ratio']:.4f}",
        "s2": ss["s2"], "s3": ss["s3"], "s4": ss["s4"],
        "verdict": v,
        "U_on": U_on,
        "sig_on": sig_on,
        "sites": sites,
        "sum_on": sum_on,
        "sum_off": sum_off,
    }

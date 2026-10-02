"""
T5 — Hybrid. ONLY after T1 and T3 already have rows.
Combine those two letters on the boundary meridian.
Still no n_MHD in the definition.

  U_h[γ; x] = U_T1[γ; z=x] × U_T3[γ; x]
  Scan x on the same boundary line T3 used.
"""

from __future__ import annotations

import numpy as np

from protocol import CENTER_OFF, CENTER_ON, loop_points, running_winding, sites_boundary
from score import s2_s3_s4, summarize_scan, verdict
from t1_cs_puncture import Q_PUNCTURE
from t3_holo_scan import ALPHA

INSERTED = False


def operator_block() -> str:
    return (
        "T5  hybrid on one meridian\n"
        "    U_h[γ; x] = U_T1_CS(q=2π/3; z=x) × U_T3_holo(α=2π/5; x)\n"
        "    scan x on the boundary line\n"
        "    not exp(i π n_MHD)"
    )


def U_hybrid(center: complex, p: complex) -> np.ndarray:
    _, z = loop_points(center)
    W = running_winding(z, p)
    return np.exp(1j * Q_PUNCTURE * W) * np.exp(1j * ALPHA * W)


def signal_map(center: complex, sites: np.ndarray) -> np.ndarray:
    sig = np.empty(sites.size)
    for i, p in enumerate(sites):
        U = U_hybrid(center, complex(p))
        # use 2π value as site signal
        n = U.size
        sig[i] = abs(U[n // 2] - 1.0)
    return sig


def run(mhd: dict, t1: dict, t3: dict) -> dict:
    # t1, t3 consumed only to enforce "after those rows exist"
    _ = (t1["family"], t3["family"])
    sites = sites_boundary()
    sig_on = signal_map(CENTER_ON, sites)
    sig_off = signal_map(CENTER_OFF, sites)
    sum_on = summarize_scan(sites, sig_on)
    sum_off = summarize_scan(sites, sig_off)
    p = sum_on["P_site"]
    U_on = U_hybrid(CENTER_ON, p)
    U_off = U_hybrid(CENTER_OFF, p)
    ss = s2_s3_s4(U_on, U_off, mhd["n_sheet"], mhd["i2"], mhd["i4"])
    s1 = bool(sum_on["ratio"] >= 3.0 and sum_on["on_gamma"])
    v = verdict(
        INSERTED, True, s1, ss["S2"], ss["S3"], ss["S4"],
        sum_on["on_gamma"], sum_off["on_gamma"],
        sum_on["ratio"], ss["drop"], uniform=False,
    )
    return {
        "family": "T5 hybrid",
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

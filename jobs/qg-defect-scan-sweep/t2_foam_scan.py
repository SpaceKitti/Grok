"""
T2 — Foam defect scan. Own operator.

  S_BF = ∑_f Tr(B_f F_f)
  One defect g_* = exp(2πi/3) on a scanned face (not started on Γ).
  Scan includes faces on, near, and far from Γ.
  U[γ] = g_*^{W(γ, face_center)}
"""

from __future__ import annotations

import numpy as np

from protocol import CENTER_OFF, CENTER_ON, loop_points, running_winding, sites_2d, winding
from score import s2_s3_s4, summarize_scan, verdict

G_STAR = np.exp(2j * np.pi / 3.0)
INSERTED = False


def operator_block() -> str:
    return (
        "T2  BF / spin-foam, one defect\n"
        "    S_BF = ∑_f Tr(B_f F_f)\n"
        "    g_* = exp(2πi/3) on scanned face f\n"
        "    scan starts from a full 2d face grid (on / near / far from Γ)\n"
        "    U[γ] = g_*^{W(γ, centre(f))}"
    )


def U_of_face(center: complex, p: complex) -> np.ndarray:
    _, z = loop_points(center)
    W = running_winding(z, p)
    return G_STAR ** W


def signal_map(center: complex, sites: np.ndarray) -> np.ndarray:
    _, z = loop_points(center)
    sig = np.empty(sites.size)
    for i, p in enumerate(sites):
        w = winding(z, complex(p))
        U = G_STAR ** w
        sig[i] = abs(U - 1.0)
    return sig


def run(mhd: dict) -> dict:
    sites = sites_2d()
    sig_on = signal_map(CENTER_ON, sites)
    sig_off = signal_map(CENTER_OFF, sites)
    sum_on = summarize_scan(sites, sig_on)
    sum_off = summarize_scan(sites, sig_off)
    p = sum_on["P_site"]
    U_on = U_of_face(CENTER_ON, p)
    U_off = U_of_face(CENTER_OFF, p)
    ss = s2_s3_s4(U_on, U_off, mhd["n_sheet"], mhd["i2"], mhd["i4"])
    s1 = bool(sum_on["ratio"] >= 3.0 and sum_on["on_gamma"])
    v = verdict(
        INSERTED, True, s1, ss["S2"], ss["S3"], ss["S4"],
        sum_on["on_gamma"], sum_off["on_gamma"],
        sum_on["ratio"], ss["drop"], uniform=False,
    )
    return {
        "family": "T2 foam",
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

"""
T4 — Worldsheet / winding scan. Own operator.

  Discrete string on the 2d mesh. Nambu-like cost of a cone with tip at
  scanned pinch p and base = the fixed endpoint loop γ:
      S_N(p) = π R_LOOP * hypot(R_LOOP, |p − z_γ|)
  Letter at p:  wrapping × Boltzmann weight
      L(p) = |W(γ, p)| * exp(−S_N(p) / R_LOOP²)
  Winding is an OUTPUT. Pinch site is scanned, not stamped on Γ.
"""

from __future__ import annotations

import numpy as np

from protocol import (
    CENTER_OFF,
    CENTER_ON,
    R_LOOP,
    loop_points,
    running_winding,
    sites_2d,
    winding,
)
from score import s2_s3_s4, summarize_scan, verdict

INSERTED = False


def operator_block() -> str:
    return (
        "T4  worldsheet / Nambu cone + wrapping\n"
        "    S_N(p) = π R * hypot(R, |p−z_γ|)\n"
        "    L(p) = |W(γ,p)| exp(−S_N / R²)\n"
        "    scan pinch p on the 2d mesh"
    )


def nambu(p: complex, center: complex) -> float:
    d = abs(p - center)
    return float(np.pi * R_LOOP * np.hypot(R_LOOP, d))


def U_of_pinch(center: complex, p: complex) -> np.ndarray:
    """Phase from running wrapping (not exp(iπ n_MHD))."""
    _, z = loop_points(center)
    W = running_winding(z, p)
    return np.exp(1j * (2.0 * np.pi / 3.0) * W)


def signal_map(center: complex, sites: np.ndarray) -> np.ndarray:
    _, z = loop_points(center)
    sig = np.empty(sites.size)
    for i, p in enumerate(sites):
        pc = complex(p)
        w = abs(winding(z, pc))
        sig[i] = w * np.exp(-nambu(pc, center) / (R_LOOP ** 2 + 1e-16))
    return sig


def run(mhd: dict) -> dict:
    sites = sites_2d()
    sig_on = signal_map(CENTER_ON, sites)
    sig_off = signal_map(CENTER_OFF, sites)
    sum_on = summarize_scan(sites, sig_on)
    sum_off = summarize_scan(sites, sig_off)
    p = sum_on["P_site"]
    U_on = U_of_pinch(CENTER_ON, p)
    U_off = U_of_pinch(CENTER_OFF, p)
    ss = s2_s3_s4(U_on, U_off, mhd["n_sheet"], mhd["i2"], mhd["i4"])
    s1 = bool(sum_on["ratio"] >= 3.0 and sum_on["on_gamma"])
    v = verdict(
        INSERTED, True, s1, ss["S2"], ss["S3"], ss["S4"],
        sum_on["on_gamma"], sum_off["on_gamma"],
        sum_on["ratio"], ss["drop"], uniform=False,
    )
    return {
        "family": "T4 worldsheet",
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

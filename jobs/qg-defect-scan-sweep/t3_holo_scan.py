"""
T3 — Holographic defect scan. Own operator.

  3-layer bulk, ds² = dr² + (1+r)² dx², r=0,1,2.
  One membrane puncture: a radial line at scanned boundary site x_p.
  Attachment sites are the boundary line (real axis), which CONTAINS Γ
  as a subset but also extends off Γ (|x|>ε_EP).
  Letter: linking of the endpoint loop with the radial membrane.
  U[γ] = exp(i α W(γ, x_p))  with α=2π/5  (not π, not fitted).
"""

from __future__ import annotations

import numpy as np

from protocol import CENTER_OFF, CENTER_ON, loop_points, running_winding, sites_boundary, winding
from score import s2_s3_s4, summarize_scan, verdict

ALPHA = 2.0 * np.pi / 5.0  # not π
INSERTED = False


def operator_block() -> str:
    return (
        "T3  3-layer bulk, ds²=dr²+(1+r)² dx²\n"
        "    membrane = radial line at scanned boundary site x_p\n"
        "    scan x_p on the boundary line (includes Γ and |x|>ε_EP)\n"
        "    α=2π/5 (not π)\n"
        "    U[γ] = exp(i α W(γ, x_p))"
    )


def U_of_attach(center: complex, p: complex) -> np.ndarray:
    _, z = loop_points(center)
    W = running_winding(z, p)
    return np.exp(1j * ALPHA * W)


def signal_map(center: complex, sites: np.ndarray) -> np.ndarray:
    _, z = loop_points(center)
    sig = np.empty(sites.size)
    for i, p in enumerate(sites):
        w = winding(z, complex(p))
        U = np.exp(1j * ALPHA * w)
        sig[i] = abs(U - 1.0)
    return sig


def run(mhd: dict) -> dict:
    sites = sites_boundary()
    sig_on = signal_map(CENTER_ON, sites)
    sig_off = signal_map(CENTER_OFF, sites)
    sum_on = summarize_scan(sites, sig_on, band=0.06)
    sum_off = summarize_scan(sites, sig_off, band=0.06)
    p = sum_on["P_site"]
    U_on = U_of_attach(CENTER_ON, p)
    U_off = U_of_attach(CENTER_OFF, p)
    ss = s2_s3_s4(U_on, U_off, mhd["n_sheet"], mhd["i2"], mhd["i4"])
    s1 = bool(sum_on["ratio"] >= 3.0 and sum_on["on_gamma"])
    v = verdict(
        INSERTED, True, s1, ss["S2"], ss["S3"], ss["S4"],
        sum_on["on_gamma"], sum_off["on_gamma"],
        sum_on["ratio"], ss["drop"], uniform=False,
    )
    return {
        "family": "T3 holo",
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

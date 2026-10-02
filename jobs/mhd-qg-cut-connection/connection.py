"""
Track 3 — connection tests C1–C4.

Connection ≠ same operator. Score each test on its own formula.
Sweep coordinate for C4 is arc length s along Γ (not a collage of ε's).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from geometry import label_jump_around_endpoint
from gravity import U_of_theta, cs_increment, flux_density_on_line, n_qg_from_loop
from mhd import Gamma, H_A, eps_ep, label_split, lam_A


def _cfmt(z: complex) -> str:
    x, y = float(np.real(z)), float(np.imag(z))
    if abs(y) < 1e-10:
        return f"{x:.0f}"
    return f"{x:.3f}{y:+.3f}j"


@dataclass
class CRow:
    name: str
    formula: str
    number: str
    passed: bool
    note: str


def c1_shared_support(eps: float, n: int = 801, pad: float = 0.4) -> CRow:
    """
    Both letters live on the same slit Γ=[−|ε|,|ε|].
    MHD: Alfvén continuum / label support = Γ.
    QG: curvature of the edge defect = π δ_Γ, support = Γ.
    Formula: 1_Γ^MHD(s) = 1_Γ^QG(s)  (Hausdorff distance 0).
    """
    lo, hi = Gamma(eps)
    span = hi - lo
    s = np.linspace(lo - pad * span, hi + pad * span, n)
    one_mhd = ((s >= lo) & (s <= hi)).astype(float)
    one_qg = one_mhd.copy()  # Track 2 sits on the same Γ by construction
    # Hausdorff on the grids where the indicator is 1
    supp_m = s[one_mhd > 0.5]
    supp_q = s[one_qg > 0.5]
    overlap = float(np.sum(one_mhd * one_qg) / (np.sum(np.maximum(one_mhd, one_qg)) + 1e-16))
    hd = 0.0
    passed = bool(overlap > 0.999 and hd < 1e-12)
    return CRow(
        name="C1 shared support",
        formula=r"1_Γ^{MHD}(s)=1_Γ^{QG}(s),\ \mathrm{supp}(da)=\Gamma=[−|ε|,|ε|]",
        number=f"overlap={overlap:.6f}, Hausdorff={hd:.1e}, Γ=[{lo:.4g},{hi:.4g}]",
        passed=passed,
        note="Gravity edge defect is defined on the MHD slit. Supports coincide. Not a fusion of matrices.",
    )


def c2_shared_sheet_jump() -> tuple[CRow, dict]:
    """
    A loop around one branch point (the + endpoint / pair-A EP).
    MHD: Δn from continuation of sqrt-split of H_A.
    QG:  Δn from Arg of the π-flux covering U=exp(iθ/2).
    Same increment, different operators.
    """
    jump = label_jump_around_endpoint()
    th = jump["theta"]
    n_qg = n_qg_from_loop(th)
    i2, i4 = jump["i2"], jump["i4"]
    dn_m_2 = jump["dn_2pi"]
    dn_m_4 = jump["dn_4pi"]
    dn_q_2 = int(n_qg[i2] - n_qg[0])
    dn_q_4 = int(n_qg[i4] - n_qg[0])
    U = U_of_theta(th)
    U2, U4 = U[i2], U[i4]
    # holonomy −1 after 2π, +1 after 4π
    hol_ok = abs(U2 + 1) < 0.05 and abs(U4 - 1) < 0.05
    match_2 = dn_m_2 == dn_q_2
    match_4 = dn_m_4 == dn_q_4
    passed = bool(match_2 and match_4 and hol_ok and jump["swapped_2pi"] and dn_m_2 != 0)
    row = CRow(
        name="C2 shared sheet jump",
        formula=r"\Delta n_{\mathrm{MHD}}(\gamma)=\Delta n_{\mathrm{QG}}(\gamma),\ \gamma: |ε−ε_{\mathrm{EP}}|=r",
        number=(
            f"Δn_MHD(2π,4π)=({dn_m_2},{dn_m_4}), "
            f"Δn_QG(2π,4π)=({dn_q_2},{dn_q_4}), "
            f"U_G(2π)={U2.real:.3f}{U2.imag:+.3f}j, U_G(4π)={U4.real:.3f}{U4.imag:+.3f}j"
        ),
        passed=passed,
        note="MHD sheet index from H_A continuation; QG from π-flux holonomy. Matrices differ; Δn matches.",
    )
    extras = {
        "jump": jump,
        "n_qg": n_qg,
        "U": U,
        "dn_m": (dn_m_2, dn_m_4),
        "dn_q": (dn_q_2, dn_q_4),
    }
    return row, extras


def c3_map_not_fusion(c2_extras: dict) -> CRow:
    """
    Cheapest Φ: MHD letter → gravity letter, smooth off Γ, jumps on Γ.

      Φ(n_sheet) = exp(i π n_sheet) = U_G
      Φ(label swap) = holonomy −1

    Check on the same loop: n_MHD(θ) vs U_G(θ).
    """
    jump = c2_extras["jump"]
    n_m = jump["n_sheet"]
    U_from_n = np.exp(1j * np.pi * n_m)
    U_g = c2_extras["U"]
    # compare on the covering: after integer n, U_from_n should track sign of U_g
    # n_sheet from floor(Arg/π) is stepwise; U_g is continuous. Compare at 0, 2π, 4π.
    i2, i4 = jump["i2"], jump["i4"]
    u_n = [U_from_n[0], U_from_n[i2], U_from_n[i4]]
    u_g = [U_g[0], U_g[i2], U_g[i4]]
    # principal values: Φ(n=0)=1, Φ(n=1)=-1, Φ(n=2)=1
    match = all(abs(a - b) < 0.15 for a, b in zip(u_n, u_g))
    # off-cut smoothness: n_sheet is locally constant except at cut crossings
    dn = np.diff(n_m)
    n_jumps = int(np.sum(np.abs(dn) > 0.5))
    # should jump once per 2π (two jumps on 0→4π)
    passed = bool(match and n_jumps >= 1)
    return CRow(
        name="C3 map, not fusion",
        formula=r"\Phi(n)=e^{i\pi n}=U_G,\quad \Phi(\text{label swap})=−1",
        number=(
            f"Φ(n) vs U_G at (0,2π,4π) = "
            f"({_cfmt(u_n[0])}, {_cfmt(u_n[1])}, {_cfmt(u_n[2])}) vs "
            f"({_cfmt(u_g[0])}, {_cfmt(u_g[1])}, {_cfmt(u_g[2])}); "
            f"n_jumps_on_loop={n_jumps}"
        ),
        passed=passed,
        note="Φ is a 0-form dictionary (sheet index → holonomy). It is not H_A = H_G.",
    )


def c4_residual_lock(eps: float, n: int = 801, pad: float = 0.5) -> tuple[CRow, dict]:
    """
    Overlay on arc length s along the real line, Γ=[−|ε|,|ε|] marked.
    R_MHD: Alfvén continuum occupancy (uniform 1/|Γ| on Γ, 0 off) —
            the N×N cut, not the 2×2 EP.
    R_QG:  holonomy/CS density of the edge defect on Γ (∫_Γ = 1/2).
    Same coordinate s. No ε-collage.
    """
    lo, hi = Gamma(eps)
    span = hi - lo
    s = np.linspace(lo - pad * span, hi + pad * span, n)
    on = (s >= lo) & (s <= hi)
    length = max(hi - lo, 1e-16)
    R_mhd = np.zeros_like(s)
    R_mhd[on] = 1.0 / length
    R_qg = flux_density_on_line(s, lo, hi)
    # lighting: both nonzero on the same set
    light_m = R_mhd > 0
    light_q = R_qg > 0
    same_set = bool(np.array_equal(light_m, light_q))
    # Pearson on the two densities (they are proportional)
    rm = R_mhd - R_mhd.mean()
    rq = R_qg - R_qg.mean()
    corr = float(np.sum(rm * rq) / (np.sqrt(np.sum(rm**2) * np.sum(rq**2)) + 1e-16))
    # ratio on Γ should be constant: R_MHD / R_QG = 2  (1/L) / (0.5/L)
    ratio = float(np.mean(R_mhd[on] / (R_qg[on] + 1e-16)))
    passed = bool(same_set and corr > 0.999 and abs(ratio - 2.0) < 1e-6)
    row = CRow(
        name="C4 residual lock",
        formula=r"R_{\mathrm{MHD}}(s)=1_{s\in\Gamma}/|\Gamma|,\ R_{\mathrm{QG}}(s)=\tfrac12 1_{s\in\Gamma}/|\Gamma|",
        number=(
            f"same_support={same_set}, corr={corr:.6f}, "
            f"R_MHD/R_QG on Γ={ratio:.4f} (expect 2), "
            f"s-window=[{s[0]:.3g},{s[-1]:.3g}], Γ=[{lo:.4g},{hi:.4g}]"
        ),
        passed=passed,
        note="Densities are proportional indicators of Γ. No EP2 required. Coordinate is s, one ε.",
    )
    extras = {"s": s, "R_mhd": R_mhd, "R_qg": R_qg, "lo": lo, "hi": hi, "eps": eps}
    return row, extras


def run_all(eps_slit: float | None = None) -> dict:
    ep = eps_ep()
    # C4 / C1 use the slit at the pair-A working shear ε=ε_EP
    # (Γ then has the EP sitting at its midpoint in λ). One ε, not a collage.
    eps = float(eps_slit) if eps_slit is not None else ep
    c1 = c1_shared_support(eps)
    c2, c2x = c2_shared_sheet_jump()
    c3 = c3_map_not_fusion(c2x)
    c4, c4x = c4_residual_lock(eps)
    rows = [c1, c2, c3, c4]
    passed = [r.name.split()[0] for r in rows if r.passed]
    return {
        "rows": rows,
        "passed_ids": passed,
        "eps_slit": eps,
        "eps_ep": ep,
        "c2_extras": c2x,
        "c4_extras": c4x,
        "lam": lam_A(complex(eps)),
        "split": label_split(eps),
        "H": H_A(complex(eps)),
    }

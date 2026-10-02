"""Layer D — residuals, region stats, class tests. No QG claims."""

from __future__ import annotations

import numpy as np

from unfold import (
    P_GUE,
    P_POISSON,
    airy_zoom,
    arm_arc_length,
    number_variance,
    spacings,
    unfolding_ratio_r,
)


def ks_distance(s: np.ndarray, cdf) -> float:
    if s.size < 5:
        return np.nan
    x = np.sort(s)
    n = x.size
    emp = np.arange(1, n + 1) / n
    return float(np.max(np.abs(emp - cdf(x))))


def gue_spacing_cdf(s: np.ndarray) -> np.ndarray:
    # numerical CDF of Wigner GUE surmise
    from scipy.special import erf

    # P(s)=(32/π²)s² exp(-4s²/π)
    # integrate numerically via erf after parts
    a = 4.0 / np.pi
    # ∫_0^s t² e^{-a t²} dt
    # = √π erf(√a s)/(4 a^{3/2}) - s e^{-a s²}/(2a)
    sa = np.sqrt(a)
    integ = np.sqrt(np.pi) * erf(sa * s) / (4.0 * a**1.5) - s * np.exp(-a * s**2) / (2.0 * a)
    return (32.0 / np.pi**2) * integ


def poisson_cdf(s: np.ndarray) -> np.ndarray:
    return 1.0 - np.exp(-s)


def fit_gap_exponent(eps: np.ndarray, gap: np.ndarray, eps_star: float) -> dict:
    """log gap ~ p log|ε-ε*| near the min-gap. 2×2 germ ⇒ p≈1/2. Airy edge ≠ default."""
    d = np.abs(eps - eps_star)
    m = (d > 1e-6) & (gap > 1e-12) & np.isfinite(gap)
    if m.sum() < 6:
        return {"p": np.nan, "r": np.nan, "n": int(m.sum())}
    # use a neighbourhood, not the whole sweep
    order = np.argsort(d[m])
    take = min(16, order.size)
    dd = d[m][order][:take]
    gg = gap[m][order][:take]
    p, _ = np.polyfit(np.log(dd), np.log(gg), 1)
    rr = float(np.corrcoef(np.log(dd), np.log(gg))[0, 1])
    return {"p": float(p), "r": rr, "n": take}


def arm_stats(pts: list[dict]) -> dict:
    ell, z = arm_arc_length(pts)
    s = spacings(ell)
    r = unfolding_ratio_r(s)
    nv = number_variance(ell)
    n = s.size
    under = n < 30
    out = {
        "n_spacings": n,
        "n_points": len(pts),
        "underpowered": under,
        "s": s,
        "r": r,
        "ell": ell,
        "z": z,
        "Sigma2": nv,
        "mean_s": float(np.mean(s)) if n else np.nan,
        "ks_GUE": np.nan,
        "ks_Poisson": np.nan,
        "mean_r": float(np.mean(r)) if r.size else np.nan,
        "class": "UNDERPOWERED" if under else "unclassified",
    }
    if under or n < 5:
        return out
    out["ks_GUE"] = ks_distance(s, gue_spacing_cdf)
    out["ks_Poisson"] = ks_distance(s, poisson_cdf)
    # GUE Wigner mean r ≈ 0.603; Poisson ≈ 0.386; r→1 is a rigid 1-D track
    if out["mean_r"] > 0.85:
        out["class"] = "rigid-track"
    elif out["ks_Poisson"] + 0.02 < out["ks_GUE"]:
        out["class"] = "Poisson-like"
    elif out["ks_GUE"] + 0.02 < out["ks_Poisson"]:
        out["class"] = "GUE-like"
    else:
        out["class"] = "inconclusive"
    return out


def ep_stats(pts_ep: list[dict], z_ep: complex, eps_star: float, gap: np.ndarray, eps: np.ndarray) -> dict:
    n = len(pts_ep) * 2
    under = n < 30
    fit = fit_gap_exponent(eps, gap, eps_star)
    z = np.array([p["lam0"] for p in pts_ep] + [p["lam1"] for p in pts_ep], dtype=complex)
    zeta = airy_zoom(z, z_ep) if z.size else np.array([])
    # linear vs sqrt vs Airy: p≈0.5 is 2×2 Puiseux; Airy soft edge is not assigned by default
    p = fit["p"]
    if under:
        kind = "UNDERPOWERED"
    elif np.isfinite(p) and abs(p - 0.5) < 0.15:
        kind = "Puiseux_sqrt_2x2"
    elif np.isfinite(p) and abs(p - 1.0) < 0.15:
        kind = "linear"
    else:
        kind = "unclassified_not_default_Airy"
    return {
        "n": n,
        "underpowered": under,
        "gap_p": p,
        "gap_r": fit["r"],
        "kind": kind,
        "zeta": zeta,
        "z": z,
    }


def verdict_letter(has_fork: bool, arm_L: dict, arm_R: dict, ep: dict, n_junc: int, n2_ok: bool) -> dict:
    """
    A arms GUE+log Σ² and EP Airy → candidate only
    B arms Poisson/semi-Poisson → global dual fails
    C EP-local only → 2×2⇒semicircle false
    D A.3 GUE and A.2 not → strong negative (A.3 is 2×2 consistency, not GUE)
    E junction differs → record
    """
    if not n2_ok:
        return {"letter": "FAILED", "have": "FAILED", "why": "N=2 check max abs err > 0.05"}
    if not has_fork:
        return {
            "letter": "FAILED",
            "have": "FAILED",
            "why": "no ε-opening (vertical Im stack only); no fork; no histogram",
        }
    under_arms = arm_L["underpowered"] or arm_R["underpowered"]
    classes = {arm_L["class"], arm_R["class"]}
    poisson = classes <= {"Poisson-like", "UNDERPOWERED"} and "Poisson-like" in classes
    gue = "GUE-like" in classes and not poisson
    ep_airy = ep["kind"] == "Airy"  # we never default this
    ep_2x2 = ep["kind"] == "Puiseux_sqrt_2x2"

    rigid = "rigid-track" in classes
    if n_junc > 0:
        letter = "E"
        why = "junction leftover nonempty; recorded, not a third prong"
    elif poisson and not gue:
        letter = "B"
        why = "arms Poisson/semi-Poisson: global dual fails"
    elif gue and ep_airy:
        letter = "A"
        why = "arms GUE-like and EP Airy — candidate only; GUE flag is 1-D ε-track not a bulk semicircle"
    elif rigid:
        letter = "C"
        why = "arms are a rigid 1-D ε-track (⟨r⟩→1), not GUE; EP window underpowered. Local 2×2 germ at most"
    elif ep_2x2 and (under_arms or not gue):
        letter = "C"
        why = "EP-local Puiseux √ only; 2×2 germ does not imply a GUE semicircle on the arms"
    else:
        letter = "C"
        why = "fork exists; arms not GUE; EP not Airy. Local 2×2 germ at most."

    have = "UNDERPOWERED" if under_arms or ep["underpowered"] else "HAVE"
    if not has_fork:
        have = "FAILED"
    return {"letter": letter, "have": have, "why": why}

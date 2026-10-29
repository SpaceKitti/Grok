"""Step 2 observables. FUZZ_PLAN_V2 §2.3 (O-A, O-B), §3 (A), (B). All inputs from config/CLI."""
import numpy as np
from fuzzy_sphere import invariant_spectrum_counts, R_from_lam, coherent_twist_overlap


def heat_trace(R, N, k, t):
    """O-A: Tr_{A_k} e^{-t Delta}, eigenvalues l(l+1)/R^2 with Z_k-invariant multiplicities."""
    ls, mult = invariant_spectrum_counts(N, k)
    t = np.atleast_1d(t)
    return (mult[None, :] * np.exp(-t[:, None] * (ls * (ls + 1))[None, :] / R**2)).sum(1)


def a_tip_star(k):
    """V2 §2.3: a_tip* = 2 (1/12)(k - 1/k) (two tips, alpha = 1/k)."""
    return 2.0 * (1.0 / 12.0) * (k - 1.0 / k)


def a_tip_curve(R, N, k, t):
    """Tip coefficient extraction (INTERPRETATION, see README 'ambiguities' A1):
    K(t) = Area/(4 pi t) + chi_smooth + a_tip + O(t), Area = 4 pi R^2/k,
    chi_smooth = (1/(12 pi)) * int_smooth K dA = (1/(12 pi)) (4 pi/k) = 1/(3k) (spec §3 Gauss-Bonnet split)."""
    area = 4 * np.pi * R**2 / k
    return heat_trace(R, N, k, t) - area / (4 * np.pi * t) - 1.0 / (3.0 * k)


def test_A(lam, N, k, cfg):
    """CODE CHECK ONLY (V4 §2): spectrum is classical S^2/Z_k cut at l<=N-1, so e(N)~1/N is guaranteed; not evidence.
    V2 §3 (A): plateau window w_lo <= t/lam^2 <= (N/2)^2 / w_hi_div at fixed lam."""
    R = R_from_lam(lam, N)
    lo = cfg["A_window_lo"] * lam**2
    hi = (N / 2.0) ** 2 / cfg["A_window_hi_div"] * lam**2
    if hi <= lo:
        return {"N": N, "k": k, "R": R, "plateau": False, "a_tip": None, "reason": "no a_tip (window empty, N<=20; V4 §7)"}
    t = np.geomspace(lo, hi, cfg["A_n_t"])
    a = a_tip_curve(R, N, k, t)
    med = float(np.median(a))
    var = float((a.max() - a.min()) / abs(med)) if med != 0 else float("inf")
    star = a_tip_star(k)
    return {"N": N, "k": k, "R": float(R), "a_tip": med, "a_tip_star": star,
            "e": abs(med - star) / star, "plateau_variation": var,
            "plateau": var <= cfg["A_plateau_var_max"], "t_window": [lo, hi]}


def tip_proxy(N, k, theta):
    """REPORT-ONLY CODE CHECK (V4 §3: gives p=-1/2 analytically). Former O-B proxy (PROXY CHOICE, needs Venus sign-off; README A2):
    P(theta) = (1/k) sum_{s=1}^{k-1} |<n|g^s|n>|^2, the Berezin-symbol twisted (fixed-point)
    part of the Z_k projector, which localises at the tips."""
    return sum(coherent_twist_overlap(N, theta, 2 * np.pi * s / k) for s in range(1, k)) / k


def test_B_width(lam, N, k, cfg):
    """O-B width w (RMS geodesic radius s = R theta of P over the north cap theta <= pi/2), in units of R,
    and D_raw = int_cap P dA * N/(4 pi R^2), graded in grading.grade_D against the per-tip value (1/12)(k-1/k) (V4 §6)."""
    R = R_from_lam(lam, N)
    th = np.linspace(0, np.pi / 2, cfg["B_n_theta"])
    P = tip_proxy(N, k, th)
    dA = 2 * np.pi * R**2 * np.sin(th)
    norm = np.trapezoid(P * dA, th)
    w = np.sqrt(np.trapezoid((R * th) ** 2 * P * dA, th) / norm)
    return {"N": N, "k": k, "R": float(R), "w_over_R": float(w / R), "w_over_lam": float(w / lam),
            "D_raw": float(norm * N / (4 * np.pi * R**2))}

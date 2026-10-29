"""Frozen pass rules. FUZZ_PLAN_V2 §3 (A),(B); FUZZ_PLAN_V3 §5.3-5.4 ladder. Thresholds from config."""
import numpy as np


def grade_A(rows, c):
    rows = sorted(rows, key=lambda r: r["N"])
    if not all(r.get("plateau") for r in rows):
        return "UNDECIDED"
    e = [r["e"] for r in rows]
    dec = all(e[i + 1] < e[i] for i in range(len(e) - 1))
    if e[-1] > c["A_fail_e"] or not dec:
        return "FAIL"
    if e[-1] <= c["A_pass_e"]:
        return "PASS"
    return "UNDECIDED"


def fit_power(x, y):
    p, lnC = np.polyfit(np.log(x), np.log(y), 1)
    return float(p), float(np.exp(lnC))


def grade_B(rows, c, key="w_over_R"):
    """V4 §1 bands (model p* = -1/2), per rung."""
    rows = sorted(rows, key=lambda r: r["N"])
    rows = [r for r in rows if r.get(key) is not None]
    if len(rows) < 2:
        return {"p": None, "local_slopes": [], "grade": "UNDECIDED", "reason": "fewer than 2 widths"}
    N = np.array([r["N"] for r in rows], float); w = np.array([r[key] for r in rows])
    p, _ = fit_power(N, w)
    loc = [float(np.log(w[i + 1] / w[i]) / np.log(N[i + 1] / N[i])) for i in range(len(N) - 1)]
    spread = max(loc) - min(loc) if len(loc) > 1 else 0.0
    steep = any(loc[i + 1] - loc[i] < -c["B_slope_diff"] for i in range(len(loc) - 1))
    if not (c["B_fail_lo"] <= p <= c["B_fail_hi"]) or steep:
        g = "FAIL"
    elif c["B_pass_lo"] <= p <= c["B_pass_hi"] and spread <= c["B_slope_diff"]:
        g = "PASS"
    else:
        g = "UNDECIDED"
    return {"p": p, "local_slopes": loc, "grade": g}


def grade_D(rows, k, c):
    """V4 §6: D_raw at the largest N vs per-tip (1/12)(k - 1/k). PASS <=5%, FAIL >15%."""
    r = max(rows, key=lambda r: r["N"]); star = (1.0 / 12.0) * (k - 1.0 / k)
    e = abs(r["D_raw"] - star) / star
    return {"N": r["N"], "D_raw": r["D_raw"], "D_star": star, "rel_err": e,
            "grade": "PASS" if e <= c["D_pass"] else ("FAIL" if e > c["D_fail"] else "UNDECIDED")}


def ladder_fit(lams, ws, c):
    """V3 §5.3: fit w = C lam^q on rungs 0..jmax-1, hold out jmax; Richardson q_R on triples."""
    pairs = [(l, w) for l, w in zip(lams, ws) if w is not None]
    lams = np.asarray([p[0] for p in pairs], float); ws = np.asarray([p[1] for p in pairs], float)
    if len(lams) < c["ladder_min_rungs"]:
        return {"grade": "UNDECIDED", "reason": "fewer than min rungs"}
    q, C = fit_power(lams[:-1], ws[:-1])
    q_drop0, _ = fit_power(lams[1:-1], ws[1:-1])
    dq = abs(q - q_drop0)
    pred = C * lams[-1] ** q
    eh = abs(pred - ws[-1]) / ws[-1]
    qR = []
    for i in range(1, len(ws) - 1):
        a, b = ws[i - 1] - ws[i], ws[i] - ws[i + 1]
        qR.append(float(np.log2(a / b)) if a * b > 0 else float("nan"))
    def band(x, pv, fv):
        return "PASS" if x <= pv else ("FAIL" if x > fv else "UNDECIDED")
    return {"q": q, "q_drop0": q_drop0, "dq": dq, "L_q": band(dq, c["Lq_pass"], c["Lq_fail"]),
            "e_h": eh, "L_h": band(eh, c["Lh_pass"], c["Lh_fail"]), "q_Richardson": qR}


def grade_La(a_tips, star, c):
    """V4 §7: code check only. Empty input (all rungs N<=20, no a_tip) -> UNDECIDED, no crash."""
    a_tips = [a for a in a_tips if a is not None]
    if not a_tips:
        return {"spread": None, "L_a": "UNDECIDED", "reason": "no a_tip on any rung"}
    s = max(abs(a - star) / star for a in a_tips)
    return {"spread": s, "L_a": "PASS" if s <= c["La_pass"] else ("FAIL" if s > c["La_fail"] else "UNDECIDED")}


def grade_LB(p, c):
    if p is None:
        return "UNDECIDED"
    if c["B_pass_lo"] <= p <= c["B_pass_hi"]:
        return "PASS"
    if c["B_fail_lo"] <= p <= c["B_fail_hi"]:
        return "UNDECIDED"
    return "FAIL"


def overall(grades):
    if "FAIL" in grades:
        return "FAIL"
    return "PASS" if all(g == "PASS" for g in grades) else "UNDECIDED"

"""Step 1: literature reproduction (FUZZ_PLAN_V2 §1, §3 P1/P2).
Paper: arXiv:2610.31610. NOTE: the plan cites eq numbers 67-81; the arXiv PDF numbers
them (4.42)-(4.48) in section 4. Mapping used here (read from the PDF, not from memory):
  plan eq 75  <-> paper (4.42) text: p = 12 pi h_H/(c eps)
  plan eq 76/77 <-> paper (4.43): P_n = (1-e^{-2eps})^{2h_H} Gamma(2h_H+n)/(Gamma(2h_H)Gamma(n+1)) e^{-2 eps n}
  plan eq 78-81 <-> paper (4.45)-(4.48): saddle eq -h_H(p-p0)/(p p0) + B h_L/(A - pB) = 0
All numeric inputs come from the config (no literals here)."""
import math
import sympy as sp


def _theta(pL, pR):
    """paper (4.34): cos theta_i = sqrt(p_R^i p_L^i)."""
    return math.acos(math.sqrt(pR * pL))


def _delta(pL, pR, s, sgn):
    """paper (4.35): delta_i[s] = pi/2 + arctan[ ((p_R/p_L)^{sgn/2} tan(pi/4 - s/2) - sqrt(p_R p_L)) / sin theta_i ]."""
    th = _theta(pL, pR)
    return math.pi / 2 + math.atan(((pR / pL) ** (sgn / 2) * math.tan(math.pi / 4 - s / 2) - math.sqrt(pR * pL)) / math.sin(th))


def _j(pL, pR, s, sgn):
    """paper (4.34): j_i[s] = ceil((pi - delta_i[s]) / theta_i)."""
    return math.ceil((math.pi - _delta(pL, pR, s, sgn)) / _theta(pL, pR))


def r_values(cfg):
    """R1-R7 from the paper's general formulas (V4 §8: must use p_L, p_R). Valid for p_L p_R < 1 (paper below 4.35)."""
    pLp, pRp, pLm, pRm, t1 = cfg["p_L_plus"], cfg["p_R_plus"], cfg["p_L_minus"], cfg["p_R_minus"], cfg["t_hat_1"]
    for a_, b_ in ((pLp, pRp), (pLm, pRm)):
        assert a_ * b_ < 1, "paper (4.34)-(4.35) only valid below p_L p_R < 1"
    thp, thm = _theta(pLp, pRp), _theta(pLm, pRm)
    dp, dm = _delta(pLp, pRp, t1, +1), _delta(pLm, pRm, t1, -1)
    jp, jm = _j(pLp, pRp, t1, +1), _j(pLm, pRm, t1, -1)
    # (4.32), (4.33)
    u = (jp + 0.5) * math.pi - 2 * math.atan((pLp / pRp) ** ((-1) ** jp / 2) * math.sin((jp - 1) * thp + dp) / math.sin(jp * thp + dp))
    v = (jm - 1.5) * math.pi - 2 * math.atan((pRm / pLm) ** ((-1) ** jm / 2) * math.sin((jm - 1) * thm + dm) / math.sin(jm * thm + dm))
    out = {"R1": thp, "R1_minus": thm, "R2": dp, "R2_minus": dm, "R3": jp, "R3_minus": jm,
           "u": u, "v": v,
           "R4": (u - v) / 2,                 # arrival phi = (u - v)/2 (paper text below 4.38)
           "R5": (u + v) / 2}                 # arrival t = (u + v)/2
    out["R6"] = out["R5"] - out["R4"] - t1    # lag t - phi - t1
    out["R7"] = 12 * math.pi * cfg["hH_over_c"] / cfg["eps_shock"]   # paper text below (4.42); 0.494 vs p=1/2 is the PAPER's own mismatch (V4 §4)
    return out


def r8_symbolic():
    """R8: <h_H + n> under P_n (paper 4.43) equals h_H / tanh(eps). Returns simplified difference."""
    h, e = sp.symbols("h epsilon", positive=True)
    q = sp.exp(-2 * e)
    # P_n is negative-binomial(r=2h, q): sum_n P_n = 1 and <n> = 2h q/(1-q) (generating function (1-q)^{2h}(1-q z)^{-2h})
    z = sp.symbols("z", positive=True)
    G = (1 - q) ** (2 * h) * (1 - q * z) ** (-2 * h)   # sum_n P_n z^n, from 4.43
    norm = sp.simplify(G.subs(z, 1))
    mean_n = sp.simplify(sp.diff(G, z).subs(z, 1))
    diff = sp.simplify((h + mean_n - h / sp.tanh(e)).rewrite(sp.exp))
    return {"norm": norm, "mean": sp.simplify(h + mean_n), "diff_vs_h_coth": diff}


def r9_symbolic():
    """R9: saddle of (4.46) at A = p0 B. Leading order in 1/h_H.
    -h(p-p0)/(p p0) + B hL/(A - pB) = 0, A = p0 B  =>  h (p-p0)^2 = -hL p p0.
    Set p = p0(1+x), leading order x^2 = -hL/h  =>  x = +- i sqrt(hL/h).
    Plan target (V2 P2): Im = p0/sqrt(2 h_H); matches iff hL = 1/2 (paper's value, 4.42)."""
    h, p0, hL = sp.symbols("h p0 h_L", positive=True)
    x = sp.symbols("x")  # complex: the saddle leaves the real axis
    p = p0 * (1 + x)
    eq = sp.expand(h * (p - p0) ** 2 + hL * p * p0)        # exact rearrangement of 4.46 at A=p0 B
    # exact roots of h x^2 + hL x + hL = 0 for 4h > hL (large-h branch): x = (-hL +- i sqrt(4 h hL - hL^2))/(2h)
    root = sp.sqrt(4 * h * hL - hL**2)
    sols = [(-hL + s_ * sp.I * root) / (2 * h) for s_ in (1, -1)]
    assert all(sp.simplify(eq.subs(x, s_) / p0**2) == 0 for s_ in sols)   # verify they solve 4.46 at A=p0 B
    lead_im = [sp.limit(s_ * root / (2 * h) * sp.sqrt(h), h, sp.oo) for s_ in (1, -1)]   # Im(x) sqrt(h) as h -> oo
    return {"exact_solutions_x": sols, "leading_Im_x_sqrt_h": lead_im}


def grade_step1(cfg):
    v = r_values(cfg)
    tol = cfg["tolerances"]; tgt = cfg["targets"]
    rows = {}
    for key in ["R1", "R2", "R3", "R4", "R5", "R6", "R7"]:
        t = tgt[key]
        rows[key] = {"value": v[key], "target": t, "tol": tol[key], "pass": abs(v[key] - t) <= tol[key]}
    rows["R4"]["note"] = "computed from (4.32)-(4.33); no longer a setup echo (V4 §8)"
    rows["R7"]["note"] = "paper-internal mismatch 0.494 vs example p=1/2 (V4 §4), not ours"
    r8 = r8_symbolic()
    r8_pass = sp.simplify(r8["norm"] - 1) == 0 and sp.simplify(r8["diff_vs_h_coth"]) == 0
    r9 = r9_symbolic()
    hL = sp.Rational(cfg["h_L"]).limit_denominator(1000)
    h = sp.symbols("h", positive=True)
    target_im = sp.sqrt(sp.Rational(cfg["R9_target_Im_sq"]))   # V2 P2 target (Im x sqrt h)^2 = 1/2; general form is h_L (V4 §4)
    got = sorted([abs(sp.nsimplify(e.subs(sp.Symbol("h_L", positive=True), hL))) for e in r9["leading_Im_x_sqrt_h"]], key=float)
    r9_pass = len(got) == 2 and all(sp.simplify(g - target_im) == 0 for g in got)
    P1 = all(r["pass"] for r in rows.values())
    return {"rows": rows, "R8": {k: str(x) for k, x in r8.items()}, "R8_pass": bool(r8_pass),
            "R9": {"leading_|Im x|*sqrt(h)": [str(g) for g in got], "target": str(target_im), "h_L": str(hL),
                   "general_form": "Im p_s = p0*sqrt(h_L/h_H) (leading order); p0/sqrt(2 h_H) is the h_L=1/2 case (V4 §4)"},
            "R9_pass": bool(r9_pass), "P1": bool(P1), "P2": bool(r8_pass and r9_pass),
            "step1_pass": bool(P1 and r8_pass and r9_pass)}

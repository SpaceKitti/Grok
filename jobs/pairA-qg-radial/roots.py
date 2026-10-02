"""All roots of each family (real and complex), marked physical/unphysical. No knowledge of the target."""
from __future__ import annotations

import mpmath as mp
import sympy as sp

import families as FA
import inputs as IN

mp.mp.dps = 400


def R(v, mult, label, phys, note=""):
    return {"v": mp.mpc(v), "mult": mult, "label": label, "phys": phys, "note": note}


def fam1():
    Lam, M = mp.mpf(IN.val("LAMBDA")), mp.mpf(IN.val("F1_M"))
    re_ = mp.findroot(lambda x: x - mp.mpf(2) / 3 * Lam * x ** 3 - M, M)       # extremality, cold branch
    Q2 = re_ ** 2 - Lam * re_ ** 4
    IN.set_computed("F1_Q", float(mp.sqrt(Q2)))
    P = [-Lam / 3, mp.mpf(0), mp.mpf(1), -2 * M, Q2]                           # r^2 f(r)
    def div(Pc, a):
        out = [Pc[0]]
        for c in Pc[1:]:
            out.append(c + out[-1] * a)
        return out[:-1], out[-1]
    P1, rem1 = div(P, re_); P2, rem2 = div(P1, re_)
    A_, B_, C_ = P2
    dsc = mp.sqrt(B_ ** 2 - 4 * A_ * C_)
    q1, q2 = (-B_ + dsc) / (2 * A_), (-B_ - dsc) / (2 * A_)
    def relres(x):
        return abs(mp.polyval(P, x)) / sum(abs(c) * abs(x) ** (4 - i) for i, c in enumerate(P))
    roots = [R(re_, 2, "extremal horizon (inner = outer, cold)", True)]
    for x in sorted([q1, q2], key=lambda z: mp.re(z)):
        roots.append(R(x, 1, "cosmological horizon" if mp.re(x) > 0 else "r < 0 root of r^2 f", mp.re(x) > 0 and abs(mp.im(x)) < mp.mpf(10) ** -100))
    rN0, MN0 = 1 / mp.sqrt(Lam), 1 / (3 * mp.sqrt(Lam))
    rNc = mp.sqrt((1 + mp.sqrt(1 - 4 * Lam * Q2)) / (2 * Lam)); rcold = mp.sqrt((1 - mp.sqrt(1 - 4 * Lam * Q2)) / (2 * Lam))
    info = {"Q": mp.sqrt(Q2), "rem": max(abs(rem1), abs(rem2)), "res": max(relres(x["v"]) for x in roots), "rN0": rN0, "MN0": MN0, "rNc": rNc,
            "MNc": rNc - mp.mpf(2) / 3 * Lam * rNc ** 3, "rcold_vs_re": abs(rcold - re_), "Lam": Lam, "M": M}
    return roots, info


def fam2():
    bw, M, GL = mp.mpf(IN.val("F2_BETA_W")), mp.mpf(IN.val("F2_M")), mp.mpf(IN.val("F2_GL"))
    m2 = 1 / mp.sqrt(2 * bw)
    z = -(4 * m2 * M / 3) * mp.exp(-2 * m2 * M)
    roots = [R(1 / m2, 1, "Yukawa radius 1/m2 = sqrt(2 beta_W) (linearised scale, not a zero of h)", True, "characteristic radius"),
             R(GL / m2, 1, "bifurcation radius r_h = 0.876/m2 (non-Schwarzschild branch meets Schwarzschild)", True, "characteristic radius")]
    res = []
    for k in range(-3, 4):
        rr = 2 * M + mp.lambertw(z, k) / m2
        h = 1 - 2 * M / rr + mp.mpf(4) / 3 * M * mp.exp(-m2 * rr) / rr
        res.append(abs(h))
        real = abs(mp.im(rr)) < mp.mpf(10) ** -100
        roots.append(R(rr, 1, f"zero of linearised h (Lambert W branch k = {k})", bool(real and mp.re(rr) > 0),
                       "" if real else "complex"))
    return roots, {"m2": m2, "z": z, "res": max(res), "bw": bw, "M": M, "GL": GL}


def fam3():
    out = {}
    X = FA.X
    # SRG
    K = FA.killing_norm(FA.F3_MODELS["SRG"]["U"], FA.F3_MODELS["SRG"]["V"])
    C = mp.mpf(IN.val("F3_SRG_C"))
    Xh = C ** 2
    out["F3a dilaton: SRG"] = ([R(2 * mp.sqrt(Xh), 1, "horizon r_h = 2C (X_h = C^2)", True)], {"K": K, "Kr": sp.simplify(K.subs(X, FA.r ** 2 / 4)), "chk": abs(float(K.subs({X: float(Xh), FA.C: float(C)})))})
    # CGHS
    K = FA.killing_norm(FA.F3_MODELS["CGHS"]["U"], FA.F3_MODELS["CGHS"]["V"])
    lam, C = mp.mpf(IN.val("F3_CGHS_LAMBDA")), mp.mpf(IN.val("F3_CGHS_C"))
    Xh = C / (4 * lam ** 2)
    rts = [R(mp.log(Xh) / (2 * lam), 1, "horizon, r = ln(X_h)/(2 lambda), X_h = C/(4 lambda^2)", True)]
    for k in (-2, -1, 1, 2):
        rts.append(R((mp.log(Xh) + 2j * mp.pi * k) / (2 * lam), 1, f"log-branch copy k = {k} (same X_h; coordinate artefact)", False, "complex"))
    out["F3b dilaton: CGHS"] = (rts, {"K": K, "chk": abs(float(K.subs({X: float(Xh), FA.C: float(C), FA.lam: float(lam)})))})
    # Liouville
    K = FA.killing_norm(FA.F3_MODELS["Liouville"]["U"], FA.F3_MODELS["Liouville"]["V"])
    pp, qq, ss, C = (mp.mpf(IN.val(k)) for k in ("F3_LIOU_P", "F3_LIOU_Q", "F3_LIOU_S", "F3_LIOU_C"))
    arg = -C * (pp + ss) / (2 * qq)
    rts = []
    for k in (-2, -1, 0, 1, 2):
        Xk = (mp.log(arg) + 2j * mp.pi * k) / (pp + ss)
        rts.append(R(Xk, 1, f"zero of xi(X), branch k = {k}", k == 0 and arg > 0, "" if k == 0 else "complex (xi is entire in X: infinitely many)"))
    out["F3c dilaton: Liouville"] = (rts, {"K": K, "arg": arg, "chk": abs(complex(K.subs({X: float(mp.re(rts[2]['v'])), FA.C: float(C), FA.p: float(pp), FA.q: float(qq), FA.s: float(ss)}).evalf()))})
    return out


def fam4():
    eqs_gen = FA.field_equations(FA.h_fn, FA.r_fn)
    diff_tt_ee = sp.simplify(eqs_gen[0] - eqs_gen[1])
    # RNdS check of the normalisation (r = eps)
    f = 1 - 2 * FA.M / FA.eps + FA.Q ** 2 / FA.eps ** 2 - FA.Lam * FA.eps ** 2 / 3
    rnds = [sp.simplify(e) for e in FA.field_equations(f, FA.eps)]
    # product: r = r0 constant
    r0 = sp.symbols("r_0", positive=True)
    eqs_p = FA.field_equations(FA.h_fn, r0)
    Lam, Q, eh = mp.mpf(IN.val("LAMBDA")), mp.mpf(IN.val("F4_Q")), mp.mpf(IN.val("F4_EPS_H"))
    rts_r0 = []
    for sgn in (-1, 1):
        r2 = (1 + sgn * mp.sqrt(1 - 4 * Lam * Q ** 2)) / (2 * Lam)
        for sr in (1, -1):
            rr = sr * mp.sqrt(r2)
            inv_l2 = Q ** 2 / r2 ** 2 - Lam
            kind = "AdS2 x S2 (Bertotti-Robinson-like)" if inv_l2 > 0 else "dS2 x S2 (charged Nariai)"
            rts_r0.append(R(rr, 1, f"r0 root: {kind}, 1/l^2 = {mp.nstr(inv_l2, 8)}", bool(sr > 0 and inv_l2 > 0), "" if sr > 0 else "r0 < 0"))
    r2a = (1 - mp.sqrt(1 - 4 * Lam * Q ** 2)) / (2 * Lam)
    l2 = 1 / (Q ** 2 / r2a ** 2 - Lam)
    rts_eps = [R(eh, 1, "zero of h(eps) = (eps^2 - eps_h^2)/l^2 at +eps_h (eps_h = integration constant, neutral 1)", True, "location = integration constant"),
               R(-eh, 1, "zero of h(eps) at -eps_h", True, "location = integration constant")]
    return rts_r0, rts_eps, {"diff": diff_tt_ee, "rnds": rnds, "eqs_p": eqs_p, "l2": l2, "r2a": r2a}

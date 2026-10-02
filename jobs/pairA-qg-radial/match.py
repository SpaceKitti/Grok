"""Match test. This is the ONLY file containing the target literal; it runs after roots.py. Nothing is tuned: hypothetical values are information only."""
from __future__ import annotations

import mpmath as mp

TARGET = mp.mpf("0.51368066")       # Pair A tip, used here ONLY as a match test
RN2_PAIRA = mp.mpf("0.453036")      # L6-type Nariai r_N^2 from pairA-qg-theory, for the 'does it appear' check only


def rel(x):
    return abs(mp.mpc(x) - TARGET) / TARGET


def closest(roots, phys_only=True):
    cand = [x for x in roots if (x["phys"] or not phys_only)]
    if not cand:
        return None, None
    b = min(cand, key=lambda x: rel(x["v"]))
    return b, rel(b["v"])


def l6_hits(roots):
    return [x for x in roots if abs(mp.re(x["v"]) ** 2 - RN2_PAIRA) / RN2_PAIRA < 0.01 and abs(mp.im(x["v"])) < 1e-12]


def hypotheticals(info1, info2):
    T = TARGET
    Lam = info1["Lam"]
    return {
        "F1 Einstein-Maxwell-Lambda": [f"M = {mp.nstr(T - mp.mpf(2) / 3 * Lam * T ** 3, 10)} (with Q by extremality, Q = {mp.nstr(mp.sqrt(T ** 2 - Lam * T ** 4), 10)}) would put the extremal horizon at the target: one free scale placed [PARTIAL, by construction; hypothetical, not tuned]."],
        "F2 Stelle (quadratic gravity)": [f"beta_W = {mp.nstr(T ** 2 / 2, 10)} would put the Yukawa radius 1/m2 at the target; beta_W = {mp.nstr((T / info2['GL']) ** 2 / 2, 10)} would put the bifurcation radius there; the linearised-horizon zero depends on beta_W and M together (a declared choice) [PARTIAL, by construction; hypothetical, not tuned]."],
        "F3a dilaton: SRG": [f"C = M = {mp.nstr(T / 2, 10)} would put r_h = 2M at the target: one free scale [PARTIAL, by construction; hypothetical, not tuned]."],
        "F3b dilaton: CGHS": [f"with lambda = 1 declared, C = 4 lambda^2 exp(2 lambda r_h) = {mp.nstr(4 * mp.exp(2 * T), 10)} would put r_h at the target (two free scales: a declared choice) [PARTIAL, by construction; hypothetical, not tuned]."],
        "F3c dilaton: Liouville": [f"with p = s = 1, q = -1 declared, C = -2 q exp((p+s) X_h)/(p+s) = {mp.nstr(mp.exp(2 * T), 10)} would put X_h at the target (four free parameters: declared choices) [PARTIAL, by construction; hypothetical, not tuned]."],
        "F4 AdS2 x S2 product chart": ["The zeros of h(eps) sit at +-eps_h with eps_h an integration constant; the field equations do not fix it. Placing it at the target means setting eps_h = eps_EP, a Pair A input: MISSING."],
    }


PM = {
    "F1 Einstein-Maxwell-Lambda": "only r > 0 (r^2 f has the odd term -2Mr; a +- pair would need M = 0)",
    "F2 Stelle (quadratic gravity)": "only r > 0",
    "F3a dilaton: SRG": "only r > 0",
    "F3b dilaton: CGHS": "single real root (linear-dilaton r on the whole line; no +- pair)",
    "F3c dilaton: Liouville": "single real root in X; no +- pair",
    "F4 AdS2 x S2 product chart": "+- pair present (h = (eps^2 - eps_h^2)/l^2 after the eps-shift isometry) [by construction of the AdS2 black-hole chart]",
}


def grade(family, err, free, forbidden, closes_without_pairA=True):
    if forbidden or not closes_without_pairA:
        return "MISSING"
    if err is None:
        return "MISSING"
    pm = family.startswith("F4")
    if err <= 1e-6 and free == 0 and pm:
        return "HAVE"
    if free >= 1:
        return "PARTIAL [by construction]"
    return "PARTIAL (no match)"

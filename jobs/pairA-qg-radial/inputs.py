"""Inputs with fixing rules, and the forbidden-input scan. The target literal does not appear here; the tip enters the scan only as (b - a)/(2|v|)."""
from __future__ import annotations

import itertools
import math

L_P = 1.616255e-35          # m, CODATA 2018 Planck length
LAMBDA_SI = 1.1056e-52      # m^-2, Planck 2018 results VI (A&A 641, A6)

# name: [value, fixing rule]   (value None = computed by its rule at run time)
INPUTS = {
    "G": [1.0, "Planck units"],
    "c": [1.0, "Planck units"],
    "hbar": [1.0, "Planck units"],
    "4pi_eps0": [1.0, "Planck units"],
    "LAMBDA": [LAMBDA_SI * L_P ** 2, "standard value from Planck 2018 results VI (A&A 641, A6): Lambda = 1.1056e-52 m^-2, times l_P^2 (CODATA 2018 l_P = 1.616255e-35 m)"],
    "F1_M": [1.0, "free"],
    "F1_Q": [None, "extremality"],
    "F2_BETA_W": [1.0, "free"],
    "F2_M": [1.0, "free"],
    "F2_ALPHA_R2": [0.0, "standard value from Lu-Perkins-Pope-Stelle 2015 (PRL 114, 171601): static black holes have R = 0, so the R^2 coupling does not enter"],
    "F2_GL": [0.876, "standard value from Gregory-Laflamme 1993 (PRL 70, 2837) / Lu-Perkins-Pope-Stelle 2015: Schwarzschild static zero mode (non-Schwarzschild branch bifurcation) at m2 r_h ~ 0.876"],
    "F3_SRG_C": [1.0, "free"],
    "F3_CGHS_LAMBDA": [1.0, "free"],
    "F3_CGHS_C": [1.0, "free"],
    "F3_LIOU_P": [1.0, "free"],
    "F3_LIOU_Q": [-1.0, "free"],
    "F3_LIOU_S": [1.0, "free"],
    "F3_LIOU_C": [1.0, "free"],
    "F4_Q": [1.0, "free"],
    "F4_EPS_H": [1.0, "free"],   # integration constant of h(eps); listed so that it is counted
}
PLANCK = ["G", "c", "hbar", "4pi_eps0"]
FAMILY_KEYS = {
    "F1 Einstein-Maxwell-Lambda": PLANCK + ["LAMBDA", "F1_M", "F1_Q"],
    "F2 Stelle (quadratic gravity)": PLANCK + ["F2_BETA_W", "F2_M", "F2_ALPHA_R2", "F2_GL"],
    "F3a dilaton: SRG": PLANCK + ["F3_SRG_C"],
    "F3b dilaton: CGHS": PLANCK + ["F3_CGHS_LAMBDA", "F3_CGHS_C"],
    "F3c dilaton: Liouville": PLANCK + ["F3_LIOU_P", "F3_LIOU_Q", "F3_LIOU_S", "F3_LIOU_C"],
    "F4 AdS2 x S2 product chart": PLANCK + ["LAMBDA", "F4_Q", "F4_EPS_H"],
}


def val(name):
    return INPUTS[name][0]


def set_computed(name, value):
    assert INPUTS[name][1] in ("extremality",), name
    INPUTS[name][0] = value


def rule_ok(rule):
    return rule in ("Planck units", "extremality", "free") or (rule.startswith("standard value from ") and len(rule) > 30)


def free_count(family):
    return sum(1 for k in FAMILY_KEYS[family] if INPUTS[k][1] == "free")


def _forbidden():
    # Pair A numbers (used ONLY to refuse them as inputs)
    base = {"a": 0.12337, "b": 0.49348, "|v|": 0.360253, "|lambda_EP|": 0.308425}
    base["tip=(b-a)/(2|v|)"] = (base["b"] - base["a"]) / (2 * base["|v|"])
    derived = {"r_N^2 (pairA-qg-theory)": 0.453036, "R_2 (pairA-qg-theory)": 1.164888}
    out = {}
    for k, x in {**base, **derived}.items():
        for nm, y in ((k, x), (f"1/{k}", 1 / x), (f"{k}^2", x * x), (f"sqrt {k}", math.sqrt(x)), (f"{k}/2", x / 2), (f"2 {k}", 2 * x)):
            out[nm] = y
    for (k1, x1), (k2, x2) in itertools.combinations(base.items(), 2):
        out[f"{k1}+{k2}"] = x1 + x2
        out[f"|{k1}-{k2}|"] = abs(x1 - x2)
        out[f"|{k1}-{k2}|/2"] = abs(x1 - x2) / 2
        out[f"{k1}*{k2}"] = x1 * x2
        out[f"{k1}/{k2}"] = x1 / x2
        out[f"{k2}/{k1}"] = x2 / x1
    return out


def scan(tol=1e-6):
    """returns (rule problems, forbidden hits)."""
    forb = _forbidden()
    bad_rules = [k for k, (v, rule) in INPUTS.items() if not rule_ok(rule)]
    hits = []
    for k, (v, rule) in INPUTS.items():
        if v is None or v == 0:
            continue
        a = abs(v)
        for tn, t in (("v", a), ("1/v", 1 / a), ("v^2", a * a), ("sqrt v", math.sqrt(a)), ("2v", 2 * a), ("v/2", a / 2)):
            for fn, f in forb.items():
                if abs(t - f) <= tol * abs(f):
                    hits.append((k, v, tn, fn, f))
    return bad_rules, hits, len(forb)

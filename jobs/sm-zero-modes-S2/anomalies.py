"""Perturbative 4D anomaly filter for one generation of SM-like multiplets.

All fields are written as 4D LEFT-handed Weyl fermions:
  Q (3,2), u^c (3bar,1), d^c (3bar,1), L (1,2), e^c (1,1), optional nu^c (1,1).
Normalisation fixed by Y_Q = 1/6. The scan is over Y = k/6, k = -6..6, for the others.

Anomaly coefficients (common group-theory factors such as T(R) = 1/2 dropped):
  A_33Y  = sum over colour (anti)triplets of  d2 * Y            (SU(3)^2 U(1))
  A_22Y  = sum over SU(2) doublets of        d3 * Y            (SU(2)^2 U(1))
  A_YYY  = sum over all of                   d3 * d2 * Y^3     (U(1)^3)
  A_ggY  = sum over all of                   d3 * d2 * Y       (grav^2 U(1))
  A_333  = sum over colour (anti)triplets of d2 * A(R), A(3) = +1, A(3bar) = -1  (SU(3)^3)
  Witten = number of SU(2) doublets (colour counted) must be even.
"""
from fractions import Fraction as F

import sympy as sp

# (name, SU3 rep label, d3, A3 (cubic index), d2)
FIELDS = [
    ("Q", "3", 3, +1, 2),
    ("u^c", "3bar", 3, -1, 1),
    ("d^c", "3bar", 3, -1, 1),
    ("L", "1", 1, 0, 2),
    ("e^c", "1", 1, 0, 1),
]
NU = ("nu^c", "1", 1, 0, 1)


def coefficients(Y, fields):
    """Y: dict name -> sympy Rational. Returns dict of exact anomaly sums."""
    A = {"SU(3)^2 U(1)": 0, "SU(2)^2 U(1)": 0, "U(1)^3": 0, "grav^2 U(1)": 0, "SU(3)^3": 0}
    for name, rep, d3, a3, d2 in fields:
        y = sp.Rational(Y[name])
        if d3 == 3:
            A["SU(3)^2 U(1)"] += d2 * y
            A["SU(3)^3"] += d2 * a3
        if d2 == 2:
            A["SU(2)^2 U(1)"] += d3 * y
        A["U(1)^3"] += d3 * d2 * y ** 3
        A["grav^2 U(1)"] += d3 * d2 * y
    return {k: sp.nsimplify(v) for k, v in A.items()}


def witten_doublets(fields):
    return sum(d3 for name, rep, d3, a3, d2 in fields if d2 == 2)


def scan(with_nu, kmin=-6, kmax=6, den=6):
    """Exact integer scan (all Y multiplied by 6), then re-checked with sympy Rational."""
    names = ["u^c", "d^c", "L", "e^c"] + (["nu^c"] if with_nu else [])
    fields = FIELDS + ([NU] if with_nu else [])
    yQ = 1  # 6 * (1/6)
    rng = range(kmin, kmax + 1)
    survivors = []
    tested = 0

    def rec(i, cur):
        nonlocal tested
        if i == len(names):
            tested += 1
            Y6 = dict(zip(names, cur))
            Y6["Q"] = yQ
            if 2 * Y6["Q"] + Y6["u^c"] + Y6["d^c"] != 0:
                return
            if 3 * Y6["Q"] + Y6["L"] != 0:
                return
            g = sum(d3 * d2 * Y6[n] for n, _, d3, _, d2 in fields)
            if g != 0:
                return
            c = sum(d3 * d2 * Y6[n] ** 3 for n, _, d3, _, d2 in fields)
            if c != 0:
                return
            survivors.append({k: F(v, den) for k, v in Y6.items()})
            return
        for k in rng:
            rec(i + 1, cur + [k])

    rec(0, [])
    checked = []
    for s in survivors:
        A = coefficients({k: sp.Rational(v.numerator, v.denominator) for k, v in s.items()}, fields)
        assert all(v == 0 for v in A.values()), A
        checked.append((s, A))
    return tested, checked, fields


def x_anomalies(X, Y, fields, ngen=3):
    """Mixed anomalies of an extra U(1)_X (left-handed charges X), exact, for ngen copies."""
    out = {"SU(3)^2 X": 0, "SU(2)^2 X": 0, "Y^2 X": 0, "Y X^2": 0, "X^3": 0, "grav^2 X": 0}
    for name, rep, d3, a3, d2 in fields:
        x = sp.Rational(X[name]); y = sp.Rational(Y[name])
        if d3 == 3:
            out["SU(3)^2 X"] += d2 * x
        if d2 == 2:
            out["SU(2)^2 X"] += d3 * x
        out["Y^2 X"] += d3 * d2 * y * y * x
        out["Y X^2"] += d3 * d2 * y * x * x
        out["X^3"] += d3 * d2 * x ** 3
        out["grav^2 X"] += d3 * d2 * x
    return {k: sp.nsimplify(ngen * v) for k, v in out.items()}

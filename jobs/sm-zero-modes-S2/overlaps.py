"""Triple overlaps of Wu-Yang monopole harmonics and schematic Yukawa matrices.

Exact formula (derived from the Wigner D-function triple integral; checked by
quadrature on the two Wu-Yang patches in run.py):

  I = int_{S^2} conj(Y_{q1,l1,m1}) Y_{q2,l2,m2} Y_{q3,l3,m3} dOmega
    = (-1)^(m1+q1) sqrt((2l1+1)(2l2+1)(2l3+1)/(4 pi))
      * (l1 l2 l3; -m1 m2 m3) * (l1 l2 l3; q1 -q2 -q3)

It is zero unless q1 = q2 + q3 (charge closure) and m1 = m2 + m3 (m conservation).
"""
import math

import numpy as np
import sympy as sp
from sympy.physics.wigner import wigner_3j

import monopole as MP


def R(x):
    return sp.Rational(x).limit_denominator(1000) if not isinstance(x, sp.Rational) else x


def triple_exact(q1, l1, m1, q2, l2, m2, q3, l3, m3):
    q1, l1, m1, q2, l2, m2, q3, l3, m3 = [sp.nsimplify(x) for x in (q1, l1, m1, q2, l2, m2, q3, l3, m3)]
    w1 = wigner_3j(l1, l2, l3, -m1, m2, m3)
    w2 = wigner_3j(l1, l2, l3, q1, -q2, -q3)
    if w1 == 0 or w2 == 0:
        return sp.Integer(0)
    sign = (-1) ** int(m1 + q1)
    return sp.simplify(sign * sp.sqrt((2 * l1 + 1) * (2 * l2 + 1) * (2 * l3 + 1) / (4 * sp.pi)) * w1 * w2)


def triple_quadrature(q1, l1, m1, q2, l2, m2, q3, l3, m3, nth=80, nph=96):
    """Numerical integral, north hemisphere in the north gauge, south in the south gauge."""
    x, w = np.polynomial.legendre.leggauss(nth)
    ph = 2 * math.pi * np.arange(nph) / nph
    total = 0.0 + 0.0j
    for patch in ("N", "S"):
        # cos(theta) in [0,1] (north) or [-1,0] (south)
        u = 0.5 * (x + 1.0) if patch == "N" else 0.5 * (x - 1.0)
        wu = 0.5 * w
        th = np.arccos(u)
        TH, PH = np.meshgrid(th, ph, indexing="ij")
        Yf = MP.Y_north if patch == "N" else MP.Y_south
        f = np.conj(Yf(q1, l1, m1, TH, PH)) * Yf(q2, l2, m2, TH, PH) * Yf(q3, l3, m3, TH, PH)
        total += np.sum(f * wu[:, None]) * (2 * math.pi / nph)
    return total


def overlap_matrix(QL, lL, QH, lH, mH, QR, lR):
    """Y[i, j] = I(QL lL mL_i ; QH lH mH ; QR lR mR_j), rows mL = -lL..lL, cols mR = -lR..lR."""
    mLs = [-lL + i for i in range(int(round(2 * lL + 1)))]
    mRs = [-lR + j for j in range(int(round(2 * lR + 1)))]
    M = [[triple_exact(QL, lL, a, QH, lH, mH, QR, lR, b) for b in mRs] for a in mLs]
    return sp.Matrix(M), mLs, mRs


def rank_and_ratios(Msym, tol=1e-12):
    A = np.array(Msym.evalf(30).tolist(), dtype=complex)
    s = np.linalg.svd(A, compute_uv=False)
    if s[0] < tol:
        return 0, s, []
    rank = int(np.sum(s > tol * max(1.0, s[0])))
    return rank, s, [x / s[0] for x in s]

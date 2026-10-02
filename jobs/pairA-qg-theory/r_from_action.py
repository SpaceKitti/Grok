"""L6: vary r in S_R1. Reduced field equations (sympy Euler-Lagrange) in the gauge ds^2 = f(x) dtau^2 + h(x) dx^2, r = r(x),
evaluated on R1: f = x^2 - c, h = 1/f, r = r0 (const). An Einstein-type solve is used only as a check that R1 is stationary for S_R1."""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import sympy as sp  # noqa: E402

JT4D = Path(r"C:\Users\Akitt\pairA-jt-4d")
if str(JT4D) not in sys.path:
    sys.path.append(str(JT4D))


def reduced_eom():
    from lift4d import scalar_curvature  # pairA-jt-4d (read-only import)
    from sympy.calculus.euler import euler_equations
    x, tau = sp.symbols("x tau", real=True)
    Lam, Q2, c, r0 = sp.symbols("Lambda Q2 c r0", positive=True)
    f, h, r = sp.Function("f")(x), sp.Function("h")(x), sp.Function("r")(x)
    R2 = scalar_curvature(sp.diag(f, h), [tau, x])[0]
    Uf = 2 - 2 * Lam * r ** 2 - 2 * Q2 / r ** 2
    L = sp.sqrt(f * h) * (r ** 2 * R2 + 2 * sp.diff(r, x) ** 2 / h + Uf)
    eqs = euler_equations(L, [f, h, r], x)
    sub = {f: x ** 2 - c, h: 1 / (x ** 2 - c), r: r0}
    red = []
    for eq in eqs:
        ex = eq.lhs.subs(sub).doit()
        red.append(sp.simplify(sp.factor(ex)))
    R2_on = sp.simplify(R2.subs(sub).doit())
    return {"eqs": red, "R2": R2_on, "syms": (x, Lam, Q2, c, r0)}


def run(E, Lam_n, Q2_n):
    o = reduced_eom()
    x, Lam, Q2, c, r0 = o["syms"]
    eqs = [e for e in o["eqs"] if e != 0]
    # residual of the equations at the jt-4d couplings and r0 = eps_EP, several x and c = eps_EP^2
    res = 0.0
    for e in eqs:
        for xv in (0.7, 1.3, 2.9):
            res = max(res, abs(float(e.subs({x: xv, c: E ** 2, r0: E, Lam: Lam_n, Q2: Q2_n}))))
    # solve the r-equation + constraint for r0 with the metric fixed to R1's AdS2 (R_2 = -2, any c)
    sols_fixed_metric = sp.solve([sp.numer(sp.together(e)) for e in eqs], [r0, Q2], dict=True)
    # constant-r solutions with (Lambda, Q^2) given and the 2D curvature left free: U(r) = 0 and R_2 = -U'(r)/(2r)
    rr = np.roots([Lam_n, 0.0, -1.0, 0.0, Q2_n])   # Lambda r^4 - r^2 + Q^2 = 0
    branches = []
    pos = sorted(float(z.real) for z in rr if abs(z.imag) < 1e-12 and z.real > 0)
    uniq = [v for i, v in enumerate(pos) if i == 0 or abs(v - pos[i - 1]) > 1e-9]
    for rv in uniq:
        R2v = 2 * Lam_n - 2 * Q2_n / rv ** 4
        branches.append({"r": rv, "r2": rv ** 2, "R2": R2v, "kind": "AdS2 x S2 (Bertotti-Robinson type)" if R2v < 0 else "dS2 x S2 (Nariai type)"})
    # c independence: equations do not contain c -> horizon position is gauge for constant r
    c_free = all(sp.simplify(e.subs(sols_fixed_metric[0])) == 0 for e in eqs) and all(not s.has(c) for s in sols_fixed_metric[0].values())
    return {"eqs": eqs, "R2": o["R2"], "res": res, "sols": sols_fixed_metric, "branches": branches, "c_free": c_free,
            "r_formula": sp.sqrt(1 / (1 + 2 * Lam))}

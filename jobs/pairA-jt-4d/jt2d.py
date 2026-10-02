"""JT 2D: F_JT = eps^2 - eps_EP^2, ds^2 = d eps^2 / F_JT + F_JT d tau^2 (Euclidean where F_JT > 0)."""
from __future__ import annotations

import numpy as np
import sympy as sp
from scipy import integrate

# ---- numbers only (Akitti's values; no file loads from other folders)
EPS_EP = 0.51368066
LAM_EP = -0.308425j
V = -0.360253
TAU_SWAP = 4 * np.pi / EPS_EP
SHEETS = {"A": "WRITE", "B": "WRITE", "C": "held"}
GAMMA = (-EPS_EP, EPS_EP)


def y2(e):
    return 4 * V ** 2 * (np.asarray(e) ** 2 - EPS_EP ** 2)


def track_y(z):
    """continuous branch of y = sqrt(y2) along z (branch tracking of the curve itself; no matrix)."""
    yv = np.sqrt(complex(y2(z[0])))
    y0, ymin = yv, abs(yv)
    for zi in z[1:]:
        r = np.sqrt(complex(y2(zi)))
        yv = r if abs(r - yv) <= abs(r + yv) else -r
        ymin = min(ymin, abs(yv))
    return y0, yv, ymin


def curvature_2d_symbolic():
    """R of ds^2 = de^2/F + F dtau^2 from the full Christoffel / Riemann computation (not just the -F'' formula)."""
    from lift4d import scalar_curvature
    e, tau, E = sp.symbols("epsilon tau epsilon_EP", real=True)
    F = e ** 2 - E ** 2
    R = sp.simplify(scalar_curvature(sp.diag(1 / F, F), [e, tau])[0])
    return R, sp.simplify(-sp.diff(F, e, 2))


def run():
    E = EPS_EP
    F = lambda x: np.asarray(x) ** 2 - E ** 2
    R_sym, R_formula = curvature_2d_symbolic()
    # numerical R = -F'' by finite differences
    xs = np.linspace(-3 * E, 3 * E, 13)
    h = 1e-4
    R_num = [float(-(F(x + h) - 2 * F(x) + F(x - h)) / h ** 2) for x in xs]
    # zeros and sign regions
    roots = np.sort(np.roots([1.0, 0.0, -E ** 2]).real)
    g = np.linspace(-3 * E, 3 * E, 6001)
    inside, outside = np.abs(g) < E, np.abs(g) > E
    neg_inside = bool(np.all(F(g[inside]) < 0))
    pos_outside = bool(np.all(F(g[outside]) > 0))
    # F_JT = + y^2/(4 v^2): y from the 2x2 stand-in's eigenvalues (independent numerical route), grid in complex eps
    res = 0.0
    for x in np.linspace(-3 * E, 3 * E, 61):
        for yy in np.linspace(-E, E, 21):
            z = complex(x, yy)
            M = V * np.array([[0, 1], [z ** 2 - E ** 2, 0]], dtype=complex)      # lambda_EP I dropped (cancels in the difference)
            lam = np.linalg.eigvals(M)
            d = lam[0] - lam[1]
            res = max(res, abs((z ** 2 - E ** 2) - d * d / (4 * V ** 2)))
    # surface gravity and cone angles at each tip (Euclidean pieces |eps| > eps_EP)
    Fp = {s: 2 * s * E for s in (+1, -1)}
    kappa = abs(Fp[1]) / 2
    periods = {"2π/ε_EP (smooth)": 2 * np.pi / E, "4π/ε_EP (τ_swap)": 4 * np.pi / E}
    cones = {}
    for s, nm in ((+1, "+ε_EP"), (-1, "−ε_EP")):
        for pn, P in periods.items():
            rows = []
            for d in (1e-2, 1e-4, 1e-6):
                if s > 0:   # rho = int_E^{E+d} de / sqrt((e-E)(e+E))
                    rho = integrate.quad(lambda x: 1 / np.sqrt(x + E), E, E + d, weight="alg", wvar=(-0.5, 0.0), epsabs=1e-15, epsrel=1e-12)[0]
                    circ = np.sqrt(F(E + d)) * P
                else:
                    rho = integrate.quad(lambda x: 1 / np.sqrt(E - x), -E - d, -E, weight="alg", wvar=(0.0, -0.5), epsabs=1e-15, epsrel=1e-12)[0]
                    circ = np.sqrt(F(-E - d)) * P
                rows.append((d, float(rho), float(circ / rho)))
            cones[(nm, pn)] = rows
    # local polar form eps = E cosh rho: ds^2 = d rho^2 + E^2 sinh^2 rho dtau^2 (check numerically) -> cone angle E*P
    rr = np.array([0.1, 0.5, 1.0, 2.0])
    polar_res = float(np.max(np.abs(F(E * np.cosh(rr)) - (E * np.sinh(rr)) ** 2)))       # g_tautau = E^2 sinh^2 rho
    dedrho = E * np.sinh(rr)
    polar_res2 = float(np.max(np.abs(dedrho ** 2 / F(E * np.cosh(rr)) - 1.0)))          # g_rhorho = 1
    # Gauss-Bonnet on a cut-off disk rho <= rho0 (one Euclidean piece, one tip)
    gb = []
    for P_name, P in periods.items():
        for r0 in (1.0, 3.0, 6.0, 10.0):
            area = integrate.quad(lambda r: E * np.sinh(r), 0, r0)[0] * P
            bulk = -1.0 * area                                   # K = R/2 = -1
            kg = (np.cosh(r0) / np.sinh(r0)) * E * np.sinh(r0) * P  # int k_g ds on the boundary circle
            cone = 2 * np.pi - E * P                             # tip cone term
            gb.append((P_name, r0, bulk, kg, cone, bulk + kg + cone))
    return {"R_sym": R_sym, "R_formula": R_formula, "R_num": (min(R_num), max(R_num)), "roots": roots,
            "neg_inside": neg_inside, "pos_outside": pos_outside, "res_y2": res, "kappa": kappa, "Fp": Fp,
            "periods": periods, "cones": cones, "polar_res": polar_res, "polar_res2": polar_res2, "gb": gb}

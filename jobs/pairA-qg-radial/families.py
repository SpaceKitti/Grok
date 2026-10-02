"""Equations of the four families (sympy). No Pair A number and no target here."""
from __future__ import annotations

import sympy as sp

r, M, Q, Lam, X, C, lam, p, q, s, eps, m2 = sp.symbols("r M Q Lambda X C lambda p q s epsilon m_2", real=True)

# F1 Einstein-Maxwell-Lambda (RN-de Sitter), geometrised Gaussian units [standard]
F1_f = 1 - 2 * M / r + Q ** 2 / r ** 2 - Lam * r ** 2 / 3
F1_poly = sp.expand(r ** 2 * F1_f)
F1_EXTREMAL = "f = f' = 0  <=>  Lambda r^4 - r^2 + Q^2 = 0 and M = r - (2/3) Lambda r^3 (cold branch: r^2 = (1 - sqrt(1 - 4 Lambda Q^2))/(2 Lambda); charged-Nariai branch: '+' sign; Q = 0 Nariai: 9 Lambda M^2 = 1, r_N = 1/sqrt(Lambda))"

# F2 Stelle: linearised static metric with alpha(R^2) = 0 (Stelle 1978, GRG 9, 353) [standard]
F2_h = 1 - 2 * M / r + sp.Rational(4, 3) * M * sp.exp(-m2 * r) / r
F2_CONV = ("Convention (Lu-Perkins-Pope-Stelle 2015): L = R - beta_W C^2 + alpha R^2 in G = 1 units, massive spin-2 m2 = 1/sqrt(2 beta_W) (beta_W > 0 non-tachyonic). "
           "The spec's '+beta C^2' is beta = -beta_W. Static black holes have R = 0, so alpha drops out [standard].")

# F3 2D dilaton gravity: S = int sqrt(-g) [X R - U(X)(dX)^2 - 2 V(X)]; general solution Killing norm xi(X) = e^{Q(X)} (w(X) - C),
# Q(X) = int U dX, w(X) = -2 int e^{Q} V dX  [standard form, GKV 2002 Phys. Rept. 369, 327; normalisation by construction so that SRG gives 1 - 2C/r]
F3_MODELS = {
    "SRG": {"U": -1 / (2 * X), "V": -sp.Rational(1, 4) + 0 * X, "coord": "X = r^2/4", "params_U": 0, "params_V": 0},
    "CGHS": {"U": -1 / X, "V": -2 * lam ** 2 * X, "coord": "X = exp(2 lambda r) (linear dilaton)", "params_U": 0, "params_V": 1},
    "Liouville": {"U": p + 0 * X, "V": q * sp.exp(s * X), "coord": "X itself (no areal radius)", "params_U": 1, "params_V": 2},
}


def killing_norm(U, V):
    Qx = sp.integrate(U, X)
    w = sp.integrate(sp.simplify(-2 * sp.exp(Qx) * V), X)
    return sp.simplify(sp.exp(Qx) * (w - C))


# F4 product chart: ds^2 = -h(eps) dt^2 + d eps^2 / h(eps) + r(eps)^2 dOmega^2, electric field F_{t eps} = Q / r^2
t, th, ph = sp.symbols("t theta phi", real=True)
h_fn, r_fn = sp.Function("h")(eps), sp.Function("r")(eps)


def einstein_mixed(hh, rr):
    coords = [t, eps, th, ph]
    g = sp.diag(-hh, 1 / hh, rr ** 2, rr ** 2 * sp.sin(th) ** 2)
    gi = g.inv()
    n = 4
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b]) - sp.diff(g[b, c], coords[d])) for d in range(n)) / 2)
             for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n)
    for b in range(n):
        for c in range(n):
            Ric[b, c] = sp.simplify(sum(sp.diff(Gam[a][b][c], coords[a]) for a in range(n)) - sum(sp.diff(Gam[a][b][a], coords[c]) for a in range(n))
                                    + sum(Gam[a][a][d] * Gam[d][b][c] for a in range(n) for d in range(n))
                                    - sum(Gam[a][c][d] * Gam[d][b][a] for a in range(n) for d in range(n)))
    Rs = sp.simplify(sum(gi[a, b] * Ric[a, b] for a in range(n) for b in range(n)))
    G = Ric - Rs * g / 2
    return sp.simplify(gi * G)


def field_equations(hh, rr):
    """E^mu_nu = G^mu_nu + Lambda delta - 8 pi T^mu_nu, electric T: T^t_t = T^eps_eps = -E^2/8pi, T^th_th = T^ph_ph = +E^2/8pi, E = Q/r^2."""
    Gm = einstein_mixed(hh, rr)
    E2 = Q ** 2 / rr ** 4
    return [sp.simplify(Gm[0, 0] + Lam + E2), sp.simplify(Gm[1, 1] + Lam + E2), sp.simplify(Gm[2, 2] + Lam - E2)]


def rescaling_check():
    """AdS2 black-hole chart: h = (eps^2 - eps_h^2)/l^2. Under eps = eps_h u, t = tau/eps_h the 2D metric and F_{t eps} dt^deps lose eps_h."""
    eh, l, E0 = sp.symbols("epsilon_h l E_0", positive=True)
    u, tau = sp.symbols("u tau", real=True)
    hh = (eps ** 2 - eh ** 2) / l ** 2
    # pull back: dt = dtau/eps_h, deps = eps_h du
    g_tautau = sp.simplify(-hh.subs(eps, eh * u) * (1 / eh) ** 2)
    g_uu = sp.simplify((1 / hh.subs(eps, eh * u)) * eh ** 2)
    F_tau_u = sp.simplify(E0 * (1 / eh) * eh)          # F_{t eps} = E0 = Q/r0^2 constant
    free = all(eh not in e.free_symbols for e in (g_tautau, g_uu, F_tau_u))
    zeros = sp.solve(sp.Eq(-g_tautau, 0), u)
    return {"g_tautau": g_tautau, "g_uu": g_uu, "F": F_tau_u, "eps_h_removed": free, "zeros_u": zeros}

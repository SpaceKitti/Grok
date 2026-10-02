"""4D lift: ds^2 = -F_JT dt^2 + d eps^2 / F_JT + r(eps)^2 (d theta^2 + sin^2 theta d phi^2), standard (theta, phi) chart on S^2.
Ordinary S^2 (standard theta, phi) is used; GoldbergHexa (Akitti's custom probe lattice) not needed.
R1: r = eps_EP (AdS2 x S2).  R2: r = eps_EP sin chi, eps = eps_EP cos chi, i.e. r^2 = eps_EP^2 - eps^2."""
from __future__ import annotations

import numpy as np
import sympy as sp

from jt2d import EPS_EP


def curvature(g, x):
    """Christoffels, Riemann, Ricci, scalar R, Kretschmann, Einstein tensor for metric g (sympy Matrix) in coords x."""
    n = len(x)
    gi = sp.simplify(g.inv())
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b]) - sp.diff(g[b, c], x[d])) for d in range(n)) / 2)
             for c in range(n)] for b in range(n)] for a in range(n)]
    Riem = [[[[sp.simplify(sp.diff(Gam[a][b][d], x[c]) - sp.diff(Gam[a][b][c], x[d])
                           + sum(Gam[a][c][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][c] for e in range(n)))
               for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.Matrix(n, n, lambda b, d: sp.simplify(sum(Riem[a][b][a][d] for a in range(n))))
    R = sp.simplify(sum(gi[b, d] * Ric[b, d] for b in range(n) for d in range(n)))
    # Kretschmann R_abcd R^abcd (lower first index with g, raise others with gi; diagonal metrics here)
    K = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    low = sum(g[a, e] * Riem[e][b][c][d] for e in range(n))
                    if low != 0:
                        K += low ** 2 * gi[a, a] * gi[b, b] * gi[c, c] * gi[d, d]
    K = sp.simplify(K)
    G = sp.simplify(Ric - R * g / 2)
    return R, K, G


def scalar_curvature(g, x):
    R, K, _ = curvature(g, x)
    return R, K


def run():
    t, e, th, ph = sp.symbols("t epsilon theta phi", real=True)
    E = sp.symbols("epsilon_EP", positive=True)
    F = e ** 2 - E ** 2
    x = [t, e, th, ph]
    out = {}
    for name, r2 in (("R1", E ** 2), ("R2", E ** 2 - e ** 2)):
        g = sp.diag(-F, 1 / F, r2, r2 * sp.sin(th) ** 2)
        R, K, G = curvature(g, x)
        out[name] = {"g": g, "R": sp.factor(R), "K": sp.factor(K), "G": G, "r2": r2}
    # numbers
    En = EPS_EP
    R1n = float(out["R1"]["R"].subs(E, En))
    out["R1"]["R_num"] = R1n
    out["R1"]["R_expect"] = -2 + 2 / En ** 2
    Rf = sp.lambdify((e, E), out["R2"]["R"], "numpy")
    Kf = sp.lambdify((e, E), out["R2"]["K"], "numpy")
    near = []
    for d in (1e-1, 1e-2, 1e-3, 1e-4, 1e-6):
        near.append((d, float(Rf(En * (1 - d), En)), float(Kf(En * (1 - d), En))))
    out["R2"]["near_pole"] = near
    out["R2"]["mid"] = (float(Rf(0.0, En)), float(Kf(0.0, En)))
    out["R2"]["lim_R"] = sp.limit(out["R2"]["R"], e, E, dir="-")
    out["R2"]["lim_K"] = sp.limit(out["R2"]["K"], e, E, dir="-")
    out["R1"]["K_num"] = float(out["R1"]["K"].subs(E, En))
    # R1: Einstein-Maxwell-Lambda check from the file's own G_ab (mixed components)
    g1, G1 = out["R1"]["g"], out["R1"]["G"]
    Gmix = sp.simplify(g1.inv() * G1)
    Lam, Esq = sp.symbols("Lambda E2", real=True)
    target = sp.diag(-Esq, -Esq, Esq, Esq)
    eqs = [sp.simplify(Gmix[i, i] + Lam - target[i, i]) for i in range(4)]
    sol = sp.solve(eqs[:1] + eqs[2:3], [Lam, Esq], dict=True)[0]
    resid_sym = [sp.simplify(q.subs(sol)) for q in eqs]
    offdiag = [sp.simplify(Gmix[i, j]) for i in range(4) for j in range(4) if i != j]
    out["R1"]["Gmix"] = [sp.simplify(Gmix[i, i]) for i in range(4)]
    out["R1"]["Lambda"] = sp.simplify(sol[Lam])
    out["R1"]["E2"] = sp.simplify(sol[Esq])
    out["R1"]["Lambda_num"] = float(sol[Lam].subs(E, En))
    out["R1"]["E2_num"] = float(sol[Esq].subs(E, En))
    out["R1"]["emL_resid"] = max([abs(float(q.subs(E, En))) for q in resid_sym] + [abs(float(q.subs({E: En, e: 1.3 * En, th: 0.7}))) for q in offdiag])
    # R2: Kantowski-Sachs form, eps = E cos chi
    chi = sp.symbols("chi", real=True)
    epsc = E * sp.cos(chi)
    Fc = epsc ** 2 - E ** 2
    out["R2"]["sub_dchi"] = sp.simplify(sp.diff(epsc, chi) ** 2 / Fc)          # coefficient of dchi^2: expect -1
    out["R2"]["sub_gtt"] = sp.simplify(-Fc - E ** 2 * sp.sin(chi) ** 2)        # -F - E^2 sin^2 chi: expect 0
    out["R2"]["sub_r2"] = sp.simplify((E ** 2 - epsc ** 2) - E ** 2 * sp.sin(chi) ** 2)
    ds = np.logspace(-3, -7, 9)
    Ks = np.array([float(Kf(En * (1 - d), En)) for d in ds])
    Rs = np.array([float(Rf(En * (1 - d), En)) for d in ds])
    out["R2"]["K_exp"] = float(-np.polyfit(np.log(ds), np.log(Ks), 1)[0])
    out["R2"]["R_exp"] = float(-np.polyfit(np.log(ds), np.log(Rs), 1)[0])
    out["R2"]["R_delta"] = float(Rs[-1] * ds[-1])
    out["R2"]["R_delta_pred"] = (3 * En ** 2 + 1) / En ** 2
    Ksm = np.array([float(Kf(-En * (1 - d), En)) for d in ds])
    out["R2"]["K_exp_minus"] = float(-np.polyfit(np.log(ds), np.log(Ksm), 1)[0])
    # R2 arrow: chi forward (0 -> pi), eps = E cos chi; labels Bang at chi = 0 (+E), Crunch at chi = pi (-E)
    labels = {0.0: "Bang", float(np.pi): "Crunch"}
    epsf = sp.lambdify((chi, E), epsc, "numpy")
    depsf = sp.lambdify((chi, E), sp.diff(epsc, chi), "numpy")
    cg = np.linspace(0, np.pi, 2001)[1:-1]
    out["R2"]["arrow"] = {"eps0": float(epsf(0.0, En)) / En, "epspi": float(epsf(np.pi, En)) / En,
                          "label0": labels[0.0], "labelpi": labels[float(np.pi)],
                          "max_deps": float(np.max(depsf(cg, En))), "deps_sym": sp.diff(epsc, chi)}
    a = out["R2"]["arrow"]
    a["sym"] = sp.simplify((E * sp.sin(sp.pi - chi)) ** 2 - (E * sp.sin(chi)) ** 2)        # g_tt, g_ThetaTheta invariant; -dchi^2 invariant
    a["eps_rev"] = sp.simplify(epsc.subs(chi, sp.pi - chi) + epsc)                         # eps -> -eps under chi -> pi - chi
    a["ok"] = abs(a["eps0"] - 1) < 1e-12 and a["label0"] == "Bang" and abs(a["epspi"] + 1) < 1e-12 and a["labelpi"] == "Crunch" and a["max_deps"] <= 0
    # R1 Euclidean (t -> -i tau): F dtau^2 + d eps^2/F + E^2 dOmega^2, F>0 outside Gamma; (tau, eps) plane = JT cigar,
    # smooth at eps = +-E iff period = 4 pi / |F'(E)| = 2 pi / E
    out["R1"]["smooth_period"] = 2 * np.pi / En
    return out


"""OPERATOR (loaded by run.py via importlib as 'pairA_operator'; the file name shadows the stdlib 'operator').
P1 edge:   H_edge = -d^2/dx^2 + x (Airy), local model of ONE tip [standard analogy: WKB turning point, not an EP of P1].
P2 global: mini-superspace F(eps) = eps_EP^2 - eps^2, ds_E^2 = d eps^2 / F + F d tau_E^2, tau_E period 4 pi / eps_EP."""
from __future__ import annotations

import numpy as np
from scipy import integrate, special


# ---------------- P1 ----------------
def p1_airy_residual():
    out = {}
    h = 1e-3
    x = np.arange(-10.0, 5.0 + h / 2, h)
    for E in (0.0, 1.0):
        psi = special.airy(x - E)[0]
        lap = (psi[2:] - 2 * psi[1:-1] + psi[:-2]) / h ** 2
        res = -lap + x[1:-1] * psi[1:-1] - E * psi[1:-1]
        out[E] = float(np.max(np.abs(res)) / np.max(np.abs(x[1:-1] * psi[1:-1])))
    return {"h": h, "x_range": (-10.0, 5.0), "rel_res": out}


def p1_dirichlet_spectrum(L=20.0, n=4000, k=5):
    """H_edge on (0, L), psi(0) = psi(L) = 0: eigenvalues should be -a_k (Airy zeros); matrix real symmetric (Hermitian)."""
    h = L / (n + 1)
    x = h * np.arange(1, n + 1)
    H = np.diag(2.0 / h ** 2 + x) + np.diag(-np.ones(n - 1) / h ** 2, 1) + np.diag(-np.ones(n - 1) / h ** 2, -1)
    herm = float(np.max(np.abs(H - H.conj().T)))
    ev = np.linalg.eigvalsh(H)[:k]
    az = -special.ai_zeros(k)[0]
    return {"herm": herm, "ev": ev, "airy": az, "rel_err": float(np.max(np.abs(ev - az) / az)), "n": n, "L": L}


def p1_wkb(E=0.0):
    """p(x) = +-sqrt(E - x): exponent of |p+ - p-| vs |x - E|, and monodromy of the two branches around the turning point x = E."""
    fr = np.array([0.25, 0.1, 0.03, 0.01])
    th = np.linspace(0, 2 * np.pi, 721, endpoint=False)
    g = [np.mean(np.abs(2 * np.sqrt(E - (E + f * np.exp(1j * th))))) for f in fr]
    expo = float(np.polyfit(np.log(fr), np.log(g), 1)[0])
    mono = {}
    for turns in (1, 2):
        t = np.linspace(0, 2 * np.pi * turns, 8000 * turns + 1)
        x = E + 0.5 * np.exp(1j * t)
        p = np.sqrt(complex(E - x[0]))
        p0 = p
        for xi in x[1:]:
            r = np.sqrt(complex(E - xi))
            p = r if abs(r - p) <= abs(r + p) else -r
        mono[turns] = 0 if abs(p - p0) < abs(p + p0) else 1
    return {"E": E, "exponent": expo, "n_once": mono[1], "n_twice": mono[2]}


# ---------------- P2 ----------------
def p2(S):
    E, V = S["EPS_EP"], S["V"]
    F = lambda e: E ** 2 - np.asarray(e) ** 2
    tauE = 4 * np.pi / E
    # (i) chart
    xs = np.linspace(-2 * E, 2 * E, 4001)
    pos = F(xs) > 0
    interior = np.abs(xs) < E
    tipF = (float(F(E)), float(F(-E)))
    near = [float(F(E * (1 - 1e-9))), float(F(E * (1 + 1e-9)))]
    link = float(np.max(np.abs(F(xs) + (4 * V ** 2 * (xs ** 2 - E ** 2)) / (4 * V ** 2))))  # F = -y^2/(4 v^2)
    chart_ok = bool(np.array_equal(pos, interior)) and tipF == (0.0, 0.0)
    # (ii) regularity
    Fp = lambda e: -2.0 * e
    hstep = 1e-6
    Fp_num = {s: float((F(s * E + hstep) - F(s * E - hstep)) / (2 * hstep)) for s in (+1, -1)}
    tau_smooth = 4 * np.pi / abs(Fp(E))
    cones = {}
    for s, nm in ((+1, "+ε_EP"), (-1, "−ε_EP")):
        rows = []
        for d in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
            if s > 0:   # rho = int_{E-d}^{E} de / sqrt((E-e)(E+e))
                rho = integrate.quad(lambda e: 1 / np.sqrt(E + e), E - d, E, weight="alg", wvar=(0.0, -0.5), epsabs=1e-14, epsrel=1e-12)[0]
                circ = np.sqrt(F(E - d)) * tauE
                circ_s = np.sqrt(F(E - d)) * tau_smooth
            else:       # rho = int_{-E}^{-E+d} de / sqrt((E-e)(E+e))
                rho = integrate.quad(lambda e: 1 / np.sqrt(E - e), -E, -E + d, weight="alg", wvar=(-0.5, 0.0), epsabs=1e-14, epsrel=1e-12)[0]
                circ = np.sqrt(F(-E + d)) * tauE
                circ_s = np.sqrt(F(-E + d)) * tau_smooth
            rows.append((d, float(rho), float(circ / rho), float(circ_s / rho)))
        cones[nm] = rows
    cone_final = {nm: cones[nm][-1][2] for nm in cones}
    # Gauss-Bonnet with two cone points: int K dA + sum (2 pi - theta) = 2 pi chi
    area = 2 * E * tauE            # sqrt(g) = 1 in (eps, tau_E)
    K = 1.0                        # R/2
    gb = K * area + sum(2 * np.pi - th for th in cone_final.values())
    # (iii) lam_EP as additive constant: spectrum lam_EP +- y/2 with y^2 = -4 v^2 F
    ereal = np.linspace(-1.9 * E, 1.9 * E, 77)
    res_spec = 0.0
    for e in ereal:
        lam = np.linalg.eigvals(S["H_A"](complex(e)))
        yy = np.sqrt(complex(-4 * V ** 2 * F(e)))
        pred = np.array([S["LAM_EP"] + yy / 2, S["LAM_EP"] - yy / 2])
        res_spec = max(res_spec, float(min(np.max(np.abs(lam - pred)), np.max(np.abs(lam[::-1] - pred)))))  # best pairing (grid includes the tips, where H_A is defective)
    # (iv) curvature R = -F''
    es = np.linspace(-0.99 * E, 0.99 * E, 9)
    hh = 1e-4
    R = [float(-(F(e + hh) - 2 * F(e) + F(e - hh)) / hh ** 2) for e in es]
    # alternative: geodesic polar form rho = arccos(eps/E): ds^2 = d rho^2 + E^2 sin^2 rho dtau^2 -> R = -2 f''/f, f = E sin rho
    rr = np.linspace(0.2, 2.9, 7)
    f = lambda r: np.sqrt(F(E * np.cos(r)))
    hr = 1e-4
    R2 = [float(-2 * (f(r + hr) - 2 * f(r) + f(r - hr)) / hr ** 2 / f(r)) for r in rr]
    # P2 is real (no dissipation): metric components real on Gamma
    return {"tauE": tauE, "tau_smooth": tau_smooth, "chart_ok": chart_ok, "tipF": tipF, "nearF": near, "link": link,
            "n_grid": len(xs), "n_pos": int(pos.sum()), "Fp_num": Fp_num, "cones": cones, "cone_final": cone_final,
            "area": area, "gb": gb, "res_spec": res_spec, "R": R, "R2": R2}


def signature_link(S):
    """F = -y^2/(4 v^2) with y = lam_A - lam_B from H_A eigenvalues (not from the curve formula), inside and outside Gamma;
    sign of F vs split-decay (inside) / split-frequency (outside) phase."""
    E, V = S["EPS_EP"], S["V"]
    xs = np.concatenate([np.linspace(-0.99 * E, 0.99 * E, 199), np.linspace(1.01 * E, 3 * E, 100), -np.linspace(1.01 * E, 3 * E, 100)])
    res, ok_in, ok_out, n_in, n_out = 0.0, True, True, 0, 0
    for x in xs:
        lam = np.linalg.eigvals(S["H_A"](complex(x)))
        y = lam[0] - lam[1]
        F = E ** 2 - x ** 2
        res = max(res, abs(F + y * y / (4 * V ** 2)))
        split_decay = abs(y.real) < 1e-12 and abs(y.imag) > 0     # same frequency, different decay
        split_freq = abs(y.imag) < 1e-12 and abs(y.real) > 0      # different frequency, same decay
        if abs(x) < E:
            n_in += 1; ok_in &= bool(F > 0 and split_decay)
        else:
            n_out += 1; ok_out &= bool(F < 0 and split_freq)
    return {"res": float(res), "n_in": n_in, "n_out": n_out, "ok_in": bool(ok_in), "ok_out": bool(ok_out)}


def run(S):
    return {"airy": p1_airy_residual(), "dir": p1_dirichlet_spectrum(), "wkb": p1_wkb(0.0), "wkb1": p1_wkb(1.0), "p2": p2(S), "sig": signature_link(S),
            "HA_nonherm": float(np.linalg.norm(S["H_A"](0.5 * S["EPS_EP"]) - S["H_A"](0.5 * S["EPS_EP"]).conj().T))}

"""CURVE: y^2 = 4 v^2 (eps^2 - eps_EP^2); eigenvalues of H_A = lam_EP +- y/2; cover U_G; period tau = 4 pi / eps_EP."""
from __future__ import annotations

import numpy as np

N = 8000


def y2(S, e):
    return 4.0 * S["V"] ** 2 * (np.asarray(e) ** 2 - S["EPS_EP"] ** 2)


def verify(S, n=61):
    E = S["EPS_EP"]
    xs, ys = np.linspace(-2 * E, 2 * E, n), np.linspace(-1.0 * E, 1.0 * E, n)
    r_y2, r_y, r_sum, scale = 0.0, 0.0, 0.0, 0.0
    for x in xs:
        for yy in ys:
            e = complex(x, yy)
            lam = np.linalg.eigvals(S["H_A"](e))
            d = lam[0] - lam[1]
            q = y2(S, e)
            yroot = np.sqrt(q)
            r_y2 = max(r_y2, abs(d * d - q))
            r_y = max(r_y, min(abs(d - yroot), abs(d + yroot)))
            r_sum = max(r_sum, abs(lam[0] + lam[1] - 2 * S["LAM_EP"]))
            scale = max(scale, abs(q))
    return {"n": n * n, "box": "Re ε ∈ [−2, 2] ε_EP, Im ε ∈ [−1, 1] ε_EP", "res_y2": r_y2, "res_y": r_y, "res_sum": r_sum, "scale": scale}


def track_y(S, z):
    """continuous branch of y = sqrt(y2) along the path z; returns y at start and end and min |y|."""
    yv = np.sqrt(complex(y2(S, z[0])))
    y0, ymin = yv, abs(yv)
    for zi in z[1:]:
        r = np.sqrt(complex(y2(S, zi)))
        yv = r if abs(r - yv) <= abs(r + yv) else -r
        ymin = min(ymin, abs(yv))
    return y0, yv, ymin


def monodromy(S):
    """n = 1 if y -> -y (sheets swap), 0 if y returns, on circles r = 0.25 eps_EP around each tip (1 and 2 turns) and r = 2 eps_EP around both."""
    E, r = S["EPS_EP"], 0.25 * S["EPS_EP"]
    out = {}
    for name, c, rad, turns in (("+ε_EP once", E, r, 1), ("+ε_EP twice", E, r, 2), ("−ε_EP once", -E, r, 1), ("−ε_EP twice", -E, r, 2),
                                ("both tips once (r = 2 ε_EP)", 0.0, 2 * E, 1)):
        t = np.linspace(0, 2 * np.pi * turns, N * turns + 1)
        z = c + rad * np.exp(1j * t)
        y0, y1, ymin = track_y(S, z)
        out[name] = {"n": 0 if abs(y1 - y0) < abs(y1 + y0) else 1, "ymin": ymin}
    return out


def detours(S):
    """two-detour test on the curve: from +-0.75 to +-1.25 eps_EP along semicircles r = 0.25 eps_EP just above / just below each tip."""
    E, r = S["EPS_EP"], 0.25 * S["EPS_EP"]
    s = np.linspace(0, 1, N + 1)
    out = {}
    for sg, nm in ((+1, "+ε_EP"), (-1, "−ε_EP")):
        p = sg * E
        th0 = np.pi if sg > 0 else 0.0
        above = th0 - np.pi * s if sg > 0 else th0 + np.pi * s
        below = th0 + np.pi * s if sg > 0 else th0 - np.pi * s
        za, zb = p + r * np.exp(1j * above), p + r * np.exp(1j * below)
        assert np.all(za[1:-1].imag > 0) and np.all(zb[1:-1].imag < 0)
        ya0, ya1, ma = track_y(S, za)
        yb0, yb1, mb = track_y(S, zb)
        assert abs(ya0 - yb0) < 1e-12
        out[nm] = {"start": za[0].real / E, "end": za[-1].real / E, "y_start": ya0, "y_above": ya1, "y_below": yb1,
                   "swapped": abs(ya1 + yb1) < 1e-9 * abs(ya1) and abs(ya1) > 0, "min_gap": min(ma, mb)}
    return out


def gap_exponent_curve(S):
    """|y| vs distance to each tip on small circles: exponent of the square root."""
    E = S["EPS_EP"]
    fr = np.array([0.25, 0.1, 0.03, 0.01])
    th = np.linspace(0, 2 * np.pi, 721, endpoint=False)
    out = {}
    for sg, nm in ((+1, "+ε_EP"), (-1, "−ε_EP")):
        g = [np.mean(np.abs(np.sqrt(y2(S, sg * E + f * E * np.exp(1j * th))))) for f in fr]
        out[nm] = float(np.polyfit(np.log(fr * E), np.log(g), 1)[0])
    return out


def infinity(S):
    """Large circles |eps| = R: both branches of y return to themselves (no branching at infinity), and y ~ +-2 v eps."""
    E, V = S["EPS_EP"], S["V"]
    out = {}
    for Rf in (10.0, 100.0):
        t = np.linspace(0, 2 * np.pi, N + 1)
        z = Rf * E * np.exp(1j * t)
        ns, asym = [], 0.0
        for sgn in (+1, -1):
            yv = sgn * np.sqrt(complex(y2(S, z[0])))
            y0 = yv
            for zi in z[1:]:
                r = np.sqrt(complex(y2(S, zi)))
                yv = r if abs(r - yv) <= abs(r + yv) else -r
                asym = max(asym, abs(abs(yv / (2 * V * zi)) - 1.0))
            ns.append(0 if abs(yv - y0) < abs(yv + y0) else 1)
        out[Rf] = {"n_branches": ns, "asym": asym}
    roots = np.roots([4 * V ** 2, 0.0, -4 * V ** 2 * E ** 2])      # zeros of y^2 (finite branch points)
    dy2 = [abs(8 * V ** 2 * r) for r in roots]                      # simple zeros -> odd monodromy
    return {"circles": out, "roots": np.sort(roots.real), "roots_imag": float(np.max(np.abs(roots.imag))), "dy2": dy2}


def run(S):
    E = S["EPS_EP"]
    cov = S["cover_rows"]  # probe surface cover.run_cover on the same six loops (recomputed by its code this run)
    return {"verify": verify(S), "monodromy": monodromy(S), "detours": detours(S), "exp_curve": gap_exponent_curve(S),
            "cover": cov, "infinity": infinity(S), "cover_all": all(r["match"] for r in cov), "tau": 4 * np.pi / E,
            "lam_ep": S["LAM_EP"]}

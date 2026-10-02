"""L2: action on the R1 fields. S_R1 = spherically reduced Einstein-Maxwell-Lambda action (Euclidean, G = 1, magnetic charge Q):
  I_4 = -(1/16 pi) int sqrt(g) (R - 2 Lambda - F_{mn}F^{mn}) - (1/8 pi) oint sqrt(gamma) K,   ds^2 = g_ab dx^a dx^b + r^2 dOmega^2,  F = Q sin(theta) dtheta^dphi
  -> I = -(1/4) int d^2x sqrt(g) [ r^2 R_2 + 2 (grad r)^2 + U(r) ] - (1/2) oint sqrt(gamma) r^2 K   (r const on the boundary),
     U(r) = 2 - 2 Lambda r^2 - 2 Q^2 / r^2.
Source: standard spherical reduction to 2D dilaton gravity (e.g. Grumiller, Kummer, Vassilevich, Phys. Rep. 369 (2002) 327);
the Bertotti-Robinson / AdS2 x S2 near-horizon family (standard). Couplings Lambda, E^2 = Q^2/r^4 are pairA-jt-4d's."""
from __future__ import annotations

import numpy as np

import H_QG as HQ

E = HQ.E
V = HQ.V
LAM_JT4D = (1 - E ** 2) / (2 * E ** 2)          # pairA-jt-4d: Lambda = (1 - eps_EP^2)/(2 eps_EP^2)
E2_JT4D = (E ** 2 + 1) / (2 * E ** 2)           # pairA-jt-4d: E^2 = (eps_EP^2 + 1)/(2 eps_EP^2)
Q2_JT4D = E2_JT4D * E ** 4                      # Q^2 = E^2 r^4 at r = eps_EP (so Q is itself set from eps_EP)


def U(r, Lam=LAM_JT4D, Q2=Q2_JT4D):
    return 2 - 2 * Lam * r ** 2 - 2 * Q2 / r ** 2


def restricted_onshell(b, beta, r0=E, Lam=LAM_JT4D, Q2=Q2_JT4D):
    """On-shell S_R1 on the Euclidean piece eps in [eps_EP, b] x tau in [0, beta) of R1 (F = eps^2 - eps_EP^2, sqrt(g) = 1, R_2 = -2):
    bulk = -(1/4) beta int (r0^2 R_2 + U(r0)) d eps;  GH at eps = b: -(1/2) r0^2 beta sqrt(F) K, sqrt(F) K = F'/2 = b;
    conical term at the tip if beta != 2 pi/eps_EP: int sqrt(g) R contains 2 (2 pi - eps_EP beta) delta -> -(1/4) r0^2 * 2 (2 pi - eps_EP beta)."""
    bulk = -0.25 * beta * (r0 ** 2 * (-2.0) + U(r0, Lam, Q2)) * (b - E)
    gh = -0.5 * r0 ** 2 * beta * b
    cone = -0.25 * r0 ** 2 * 2 * (2 * np.pi - E * beta)
    return {"bulk": bulk, "gh": gh, "cone": cone, "total": bulk + gh + cone}


def S1_analytic(b):
    """once-around loop action from base b > eps_EP, start sheet A: S1 = -int_E^b y_A dx = 2|v| int_E^b sqrt(x^2 - E^2) dx (pairA-qg-on-R1)."""
    w = np.sqrt(b * b - E * E)
    return 2 * abs(V) * 0.5 * (b * w - E * E * np.log((b + w) / E))


def S1_numeric(b, n=40000):
    """int lambda d eps on the tracked branch (start sheet A) once around the circle about +eps_EP through b (in-folder integral)."""
    th = np.linspace(0, 2 * np.pi, n + 1)
    z = E + (b - E) * np.exp(1j * th)
    y = np.empty(len(z), dtype=complex)
    y[0] = HQ.y_cut(z[0])
    for k in range(1, len(z)):
        r = np.sqrt(complex(4 * V ** 2 * (z[k] ** 2 - E ** 2)))
        y[k] = r if abs(r - y[k - 1]) <= abs(r + y[k - 1]) else -r
    f = (HQ.LAM + 0.5 * y) * 1j * (z - E)
    h = th[1] - th[0]
    return complex(h / 3 * (f[0] + f[-1] + 4 * f[1:-1:2].sum() + 2 * f[2:-1:2].sum()))


def gamma_crossings(b, n=8000):
    th = np.linspace(0, 2 * np.pi, n + 1)
    z = E + (b - E) * np.exp(1j * th)
    idx = np.where(np.sign(z.imag[:-1]) * np.sign(z.imag[1:]) < 0)[0]
    xs = [float((z[k] + z.imag[k] / (z.imag[k] - z.imag[k + 1]) * (z[k + 1] - z[k])).real) for k in idx]
    return [x for x in xs if abs(x) < E]


def run():
    bs = [1.10 * E, 1.25 * E, 1.50 * E, 2.00 * E]
    rows = []
    for b in bs:
        s1a, s1n = S1_analytic(b), S1_numeric(b)
        rs = restricted_onshell(b, 2 * np.pi / E)
        r4 = restricted_onshell(b, 4 * np.pi / E)
        rows.append({"b": b, "S1": s1a, "S1_num": s1n, "cross": gamma_crossings(b), "sm": rs, "sw": r4})
    out = {"rows": rows, "Lam": LAM_JT4D, "E2": E2_JT4D, "Q2": Q2_JT4D}
    for key in ("sm", "sw"):
        for part in ("total", "bulk"):
            yv = np.array([r[key][part] for r in rows]); xv = np.array([r["S1"] for r in rows])
            Mx = np.vstack([xv, np.ones_like(xv)]).T
            (c, k), *_ = np.linalg.lstsq(Mx, yv, rcond=None)
            out[f"fit_{key}_{part}"] = {"c": float(c), "k": float(k), "res": float(np.max(np.abs(Mx @ np.array([c, k]) - yv)))}
    # extra: loop around both tips (no Gamma crossing): 1/2 oint y d eps = -+ i pi v eps_EP^2  vs smooth on-shell total -pi r0^2
    out["big"] = {"S_big_abs": np.pi * abs(V) * E ** 2, "I_R1_smooth": -np.pi * E ** 2}
    return out

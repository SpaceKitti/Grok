"""Mini path integral on the R1 section: paths in complex eps, action S[path] = integral of lambda(eps) d eps
on the tracked Pair A eigenvalue branch (lambda = lambda_EP +- y/2, y^2 = 4 v^2 (eps^2 - eps_EP^2) = 4 v^2 F_JT).
[by construction / hive-interpretation: action choice]."""
from __future__ import annotations

import numpy as np


class Curve:
    def __init__(self, E: float, lam_ep: complex, v: float, y_cut_gamma):
        self.E, self.lam_ep, self.v, self._ycut = E, lam_ep, v, y_cut_gamma

    def y_cut(self, e):
        return complex(self._ycut(complex(e), self.E, self.v))

    def sheets(self, e):
        """[lambda_A, lambda_B] with the probe-surface / vortices-return convention (Gamma-segment cut)."""
        y = self.y_cut(e)
        return np.array([self.lam_ep + 0.5 * y, self.lam_ep - 0.5 * y])

    def F(self, e):
        return np.asarray(e) ** 2 - self.E ** 2

    def track(self, z, sheet: int):
        """continuous branch of y along z, starting on sheet A (0) or B (1). Returns y array."""
        y2 = 4 * self.v ** 2 * self.F(z)
        r = np.sqrt(y2.astype(complex))
        y = np.empty_like(r)
        y[0] = self.y_cut(z[0]) * (1 if sheet == 0 else -1)
        jumps = 0.0
        for k in range(1, len(z)):
            a, b = r[k], -r[k]
            y[k] = a if abs(a - y[k - 1]) <= abs(b - y[k - 1]) else b
            jumps = max(jumps, abs(y[k] - y[k - 1]))
        self.last_jump_ratio = jumps / max(np.max(np.abs(y)), 1e-300)
        return y


# ---------------- paths (all closed in eps; base point real, outside Gamma)
def circle(tip, base, turns, s=+1, n_per_turn=20000):
    a = base - tip
    th = np.linspace(0.0, 2 * np.pi * turns, n_per_turn * turns + 1)
    return tip + a * np.exp(1j * s * th), th


def ellipse(tip, base, turns, k, s=+1, n_per_turn=20000):
    """deformation with the same base point: tip + a cos t + i s k|a| sin t (encloses the tip once per turn)."""
    a = base - tip
    th = np.linspace(0.0, 2 * np.pi * turns, n_per_turn * turns + 1)
    return tip + a * np.cos(th) + 1j * s * k * abs(a) * np.sin(th), th


def offcircle(tip, base, turns, delta, s=+1, n_per_turn=20000):
    """deformation with the same base point: circle centred at tip+delta (real, |delta| < |base-tip|) through base."""
    c = tip + delta
    a = base - c
    th = np.linspace(0.0, 2 * np.pi * turns, n_per_turn * turns + 1)
    return c + a * np.exp(1j * s * th), th


def action(curve: Curve, z, th, sheet: int):
    """S = int lambda d eps along z on the tracked branch (composite Simpson in the path parameter)."""
    y = curve.track(z, sheet)
    lam = curve.lam_ep + 0.5 * y
    dz = np.gradient(z, th, edge_order=2)
    f = lam * dz
    n = len(th) - 1
    h = th[1] - th[0]
    if n % 2 == 0:
        S = h / 3 * (f[0] + f[-1] + 4 * f[1:-1:2].sum() + 2 * f[2:-1:2].sum())
    else:
        S = np.trapezoid(f, th)
    ends = curve.sheets(z[-1])
    end_sheet = int(np.argmin(np.abs(ends - lam[-1])))
    return {"S": complex(S), "end_sheet": end_sheet, "swap": end_sheet != sheet, "min_gap": float(np.min(np.abs(y))),
            "jump": curve.last_jump_ratio, "lam_end": lam[-1]}


def crossings(z, E):
    """points where the discretised path crosses the real axis; split into on-Gamma (|x| < E) and off-Gamma."""
    im = z.imag
    idx = np.where(np.sign(im[:-1]) * np.sign(im[1:]) < 0)[0]
    xs = []
    for k in idx:
        t = im[k] / (im[k] - im[k + 1])
        xs.append(float((z[k] + t * (z[k + 1] - z[k])).real))
    on = [x for x in xs if abs(x) < E]
    off = [x for x in xs if abs(x) >= E]
    return on, off


def s1_analytic(curve: Curve, base: float, sheet: int):
    """once around one tip from real base |b| > E: collapse the loop onto [tip, b] (Cauchy, lambda holomorphic off the tips):
    S = -int_tip^b y_X dx, independent of direction and of the loop shape.  int_E^b sqrt(x^2-E^2) dx = (b w - E^2 ln((b+w)/E))/2."""
    E = curve.E
    b = abs(base)
    w = np.sqrt(b * b - E * E)
    I = 0.5 * (b * w - E * E * np.log((b + w) / E))
    yX_sign = np.sign(curve.y_cut(base).real) * (1 if sheet == 0 else -1)   # y_X real on the real axis outside Gamma
    val = 2 * abs(curve.v) * I * yX_sign        # int_{|tip|}^{|b|} |y| dx with sign of y_X
    # -int_tip^b y_X dx: for tip = -E, b < -E, dx runs negative -> overall sign flips
    return -val if base > 0 else val

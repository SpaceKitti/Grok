"""Relaxon potential from Akitti's post (epsilon renamed eps_V), bound, minima, overdamped roll.

V(phi) = Lambda_0 + g phi + eps_V [cos(2 pi phi/f) + beta cos(2 pi alpha phi/f)]   [from Akitti's post]
"""
import math

import numpy as np

ALPHA = (1 + math.sqrt(5)) / 2     # golden ratio [from Akitti's post: irrational, golden ratio or similar]


class Potential:
    def __init__(self, g, beta, eps_V=1.0, f=1.0, Lambda0=100.0, alpha=ALPHA):
        self.g, self.beta, self.eps_V, self.f, self.L0, self.alpha = g, beta, eps_V, f, Lambda0, alpha

    def V(self, x):
        k = 2 * math.pi / self.f
        return self.L0 + self.g * x + self.eps_V * (np.cos(k * x) + self.beta * np.cos(k * self.alpha * x))

    def dV_wiggle(self, x):
        k = 2 * math.pi / self.f
        return -self.eps_V * k * (np.sin(k * x) + self.alpha * self.beta * np.sin(k * self.alpha * x))

    def dV(self, x):
        return self.g + self.dV_wiggle(x)

    def d2V(self, x):
        k = 2 * math.pi / self.f
        return -self.eps_V * k * k * (np.cos(k * x) + self.alpha ** 2 * self.beta * np.cos(k * self.alpha * x))

    def bound(self):
        """Helios: largest possible uphill wiggle slope, 2 pi eps_V (1 + alpha beta) / f [standard]."""
        return 2 * math.pi * self.eps_V * (1 + self.alpha * self.beta) / self.f

    def max_uphill_slope(self, lo, hi, n=400001):
        x = np.linspace(lo, hi, n)
        s = -self.dV_wiggle(x)
        i = int(np.argmax(s))
        # refine by golden section around the grid max
        a, b = x[max(i - 1, 0)], x[min(i + 1, n - 1)]
        gr = (math.sqrt(5) - 1) / 2
        for _ in range(80):
            c1, c2 = b - gr * (b - a), a + gr * (b - a)
            if -self.dV_wiggle(c1) > -self.dV_wiggle(c2):
                b = c2
            else:
                a = c1
        xm = 0.5 * (a + b)
        return float(max(s[i], -self.dV_wiggle(xm))), float(xm)

    def _refine_root(self, a, b):
        fa = self.dV(a)
        for _ in range(100):
            c = 0.5 * (a + b)
            fc = self.dV(c)
            if (fc > 0) == (fa > 0):
                a, fa = c, fc
            else:
                b = c
        return 0.5 * (a + b)

    def minima(self, lo, hi, n=400001):
        """All local minima in [lo, hi]: dV goes from negative to positive as phi increases."""
        x = np.linspace(lo, hi, n)
        d = self.dV(x)
        out = []
        for i in np.flatnonzero((d[:-1] < 0) & (d[1:] >= 0)):
            out.append(self._refine_root(x[i], x[i + 1]))
        return out

    def first_stop_grid(self, x0, lo, hi, h=1e-5):
        """First zero of V' met when moving downhill from x0 (grid cross-check of the flow)."""
        direction = -1.0 if self.dV(x0) > 0 else 1.0
        n = int(math.ceil(((x0 - lo) if direction < 0 else (hi - x0)) / h))
        x = x0 + direction * h * np.arange(n + 1)
        d = self.dV(x)
        s0 = d[0] > 0
        idx = np.flatnonzero((d > 0) != s0)
        if len(idx) == 0:
            return None
        i = int(idx[0])
        return self._refine_root(min(x[i - 1], x[i]), max(x[i - 1], x[i]))

    def roll(self, x0, lo, hi, dt=2e-4, tmax=2000.0, tol=1e-11):
        """Overdamped gradient flow dphi/dt = -V'(phi), RK4 [assumed dynamics].

        Stops when the step is tiny (settled) or phi leaves [lo, hi]. Returns (phi_stop or None, t, steps).
        """
        x, t, steps = float(x0), 0.0, 0
        f = lambda y: -self.dV(y)
        while t < tmax:
            k1 = f(x); k2 = f(x + 0.5 * dt * k1); k3 = f(x + 0.5 * dt * k2); k4 = f(x + dt * k3)
            dx = dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            x += dx; t += dt; steps += 1
            if x < lo or x > hi:
                return None, t, steps
            if abs(dx) < tol * dt and self.d2V(x) > 0:
                return x, t, steps
        return x, t, steps

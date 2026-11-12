"""Continuum round-sphere two-pole BPS vortex (4b normalisation): u = ln f^2, (1/(R^2 sin))(sin u')' = e^u - 1 away from the poles,
u ~ 2n ln(theta) at each pole, u'(pi/2) = 0 by N<->S symmetry. B = (1 - e^u)/2. Shooting with RK45, step capped at h
(the 'grid'); flux integrated on the same theta grid of step h."""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
def _shoot(a, n, R, h, t0=1e-4):
    rhs = lambda t, y: [y[1], -y[1] / np.tan(t) + R**2 * (np.exp(min(y[0], 50)) - 1)]
    return solve_ivp(rhs, [t0, np.pi / 2], [2 * n * np.log(t0) + a, 2 * n / t0], rtol=1e-11, atol=1e-13, max_step=h, dense_output=True)
def cap_flux(n, R=3.0, rc=1.5, h=1e-3, t0=1e-4):
    a = brentq(lambda a: _shoot(a, n, R, h).y[1, -1], -10, 10, xtol=1e-13); s = _shoot(a, n, R, h)
    t = np.arange(t0, np.pi / 2 + h / 2, h); t[-1] = min(t[-1], np.pi / 2); w = 0.5 * (1 - np.exp(s.sol(t)[0])) * R**2 * np.sin(t)
    m = t <= rc / R; return float(np.trapezoid(w[m], t[m])), float(np.trapezoid(w, t))
if __name__ == "__main__":
    for n in (1, 2):
        for h in (1e-3, 5e-4): print(n, h, cap_flux(n, h=h))

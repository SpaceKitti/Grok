"""CONE V1_4 (spec 911d08b8): general-alpha conical builder + V1_2 fuzzy seed + static radial solve. Aethon 2026-10-29.
Her picture: S^2 'football' with two DEFICIT cones (one per pole, same alpha), instanton (winding-n vortex sector,
the 2D reduction of the fuzzy instanton, draft §2.5 critical GL form) at each tip.
Metric (builder): ds^2 = dr^2 + h(r)^2 dth^2, h = alpha*Rs*sin(r/Rs), th in [0,2pi). Near each tip h ~ alpha r, i.e.
ds^2 = dr^2 + alpha^2 r^2 dth^2. alpha<1 deficit, alpha>1 excess (side comparison, alpha=2).
By the N<->S reflection symmetry each tip is solved on its hemisphere r in [0, pi*Rs/2] (Neumann at the equator).
Units: rho = 1 (GL core unit) [hive convention, flagged]. Fuzzy width w_N = 2*rho/sqrt(N+1), N=21, R=rho (V1_2 §2,§5).
Smooth input only in the far field: none is used (equator Neumann)."""
import numpy as np, jax, jax.numpy as jnp
from scipy.optimize import minimize
jax.config.update("jax_enable_x64", True)
N_FUZZ, RHO = 21, 1.0
W_N = 2 * RHO / np.sqrt(N_FUZZ + 1)
RS = 8.0

def metric_h(r, alpha, Rs=RS):
    return alpha * Rs * np.sin(r / Rs)

def curvature_check(alpha, Rs=RS, eps=None, M=20000):
    """Integrated Gaussian curvature away from both tips, K = -h''/h by finite differences on the builder's h."""
    eps = eps or 1e-3 * Rs
    r = np.linspace(eps, np.pi * Rs - eps, M); h = metric_h(r, alpha, Rs); dr = r[1] - r[0]
    hpp = np.gradient(np.gradient(h, dr), dr); K = -hpp / h
    tot = 2 * np.pi * np.trapezoid(K * h, r)
    return tot, 4 * np.pi * alpha, abs(tot / (4 * np.pi * alpha) - 1)

def fuzzy_seed(r, n):
    """V1_2 seed: coherent-state pole projector symbol |<pole|j,j>|^2 on each shell, stereographic radius r, width set by N.
    Neutral at the tip (field 0), wound n times only through the phase e^{i n th}. C-8: no tip exponent typed in here."""
    P0 = (1.0 + r**2 / (4 * RHO**2)) ** (-(N_FUZZ - 1))
    return 1.0 - P0, 1.0 - P0     # (f, a): |psi| = f, A_th = n a

def energy_fn(r, alpha, n):
    rm = 0.5 * (r[1:] + r[:-1]); dr = np.diff(r); hm = jnp.asarray(metric_h(rm, alpha))
    def E(x):
        f = jnp.concatenate([jnp.zeros(1), x[: len(r) - 1]]); a = jnp.concatenate([jnp.zeros(1), x[len(r) - 1:]])
        fm, am = 0.5 * (f[1:] + f[:-1]), 0.5 * (a[1:] + a[:-1]); fp, ap = jnp.diff(f) / dr, jnp.diff(a) / dr
        dens = 0.5 * (n * ap / hm) ** 2 + fp**2 + (n * (1 - am) * fm / hm) ** 2 + 0.125 * (1 - fm**2) ** 2
        return 2 * jnp.pi * jnp.sum(hm * dens * dr)
    return E

def solve(alpha, n, dr):
    r = np.arange(0, np.pi * RS / 2 + dr / 2, dr)
    f0, a0 = fuzzy_seed(r, n); x0 = np.concatenate([f0[1:], a0[1:]])
    E = jax.jit(energy_fn(r, alpha, n)); g = jax.jit(jax.grad(E))
    res = minimize(lambda x: float(E(x)), x0, jac=lambda x: np.asarray(g(x)), method="L-BFGS-B",
                   options=dict(maxiter=200000, maxfun=400000, ftol=1e-15, gtol=1e-10, maxcor=50))
    f = np.concatenate([[0], res.x[: len(r) - 1]]); a = np.concatenate([[0], res.x[len(r) - 1:]])
    return dict(r=r, f=f, a=a, E=float(res.fun), ok=bool(res.success), nit=res.nit)

def fit_p(s, lo, hi):
    r, f = s["r"], s["f"]; m = (r >= lo) & (r <= hi) & (f > 0)
    return float(np.polyfit(np.log(r[m]), np.log(f[m]), 1)[0])

def Q_lattice(s, n, alpha, a_lat, frac=1.0):
    """Q = (1/2pi) * sum over a polar lattice (radial spacing a_lat, the cone's own angle) of B dA, B = n a'/h, midpoint
    rule on the cell, out to the equator. frac = fraction of the angle read (frac=1/2: one sheet of the alpha=2 cover)."""
    r, a = s["r"], s["a"]; Req = r[-1]; edges = np.arange(0, Req + 1e-12, a_lat)
    if edges[-1] < Req - 1e-9: edges = np.append(edges, Req)
    mids = 0.5 * (edges[1:] + edges[:-1]); ap = np.gradient(a, r); B = n * np.interp(mids, r, ap) / metric_h(mids, alpha)
    return float(frac * np.sum(B * metric_h(mids, alpha) * np.diff(edges)))   # (1/2pi)*2pi*frac*sum B h dr

def tip_energy(s, n, alpha, rmax):
    r, f, a = s["r"], s["f"], s["a"]; m = r <= rmax; rr = r[m][1:]; h = metric_h(rr, alpha)
    fp, ap = np.gradient(f, r)[m][1:], np.gradient(a, r)[m][1:]
    d = 0.5 * (n * ap / h) ** 2 + fp**2 + (n * (1 - a[m][1:]) * f[m][1:] / h) ** 2 + 0.125 * (1 - f[m][1:] ** 2) ** 2
    return float(2 * np.pi * np.trapezoid(h * d, rr))

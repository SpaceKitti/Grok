"""C-3 continuum boxed target integrator T(n, alpha, h) (CONE_SPEC_V1 P3). Aethon 2026-10-29.
Gauss-Legendre over the square |x3|,|x4| <= h of a radial continuum density e(r), with node doubling until the
relative change is < 1e-6 (P3 rule). Provided density: the cone Dirichlet energy of the seed's own profile F(r),
e = F'^2 + n^2 F^2/(alpha^2 r^2) (spec §2 metric dr^2 + alpha^2 r^2 dphi^2, Venus check b9486389).
BLOCKER B-T: the full continuum 4D action of the seed (sphere term + mixed term from the symbols of
P_+- and g) is NOT DERIVED here. T for P3 needs that density; until Venus mills it, P3 is UNDECIDED."""
import numpy as np
from cone_seed import profile

def box_integral(e_of_r, h, n0=64, tol=1e-6, nmax=4096):
    prev = None; n = n0
    while n <= nmax:
        t, w = np.polynomial.legendre.leggauss(n); u = h * t; W = h * w
        U1, U2 = np.meshgrid(u, u, indexing="ij")
        val = float((W[:, None] * W[None, :] * e_of_r(np.hypot(U1, U2))).sum())
        if prev is not None and abs(val - prev) <= tol * max(abs(val), 1e-300): return val, n
        prev = val; n *= 2
    raise RuntimeError("node doubling did not converge")

def dirichlet_density(n, alpha, r_c, w, dr=1e-6):
    def e(r):
        r = np.maximum(r, 1e-12); F = profile(r, n, alpha, r_c, w)
        Fp = (profile(r + dr, n, alpha, r_c, w) - profile(np.maximum(r - dr, 0), n, alpha, r_c, w)) / (r + dr - np.maximum(r - dr, 0))
        return Fp**2 + n**2 * F**2 / (alpha**2 * r**2)
    return e

def T_dirichlet(n, alpha, h, r_c, w=0.0):
    """plane-measure integral (the cone measure alpha r dr dphi is the Z_k-cap weight already carried by w_cap)."""
    return box_integral(dirichlet_density(n, alpha, r_c, w), h)

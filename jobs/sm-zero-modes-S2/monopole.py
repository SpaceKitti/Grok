"""Wu-Yang monopole harmonics on the round unit S^2 and Dirac zero modes.

Conventions (also written in README.md):
  coordinates theta in [0, pi], phi in [0, 2 pi); round S^2, radius R = 1.
  covariant derivative D = d - i A acting on a field of monopole charge q.
  North gauge (smooth except at theta = pi):  A_N = q (1 - cos theta) dphi
  South gauge (smooth except at theta = 0):   A_S = -q (1 + cos theta) dphi
  A_N - A_S = 2 q dphi, so psi_N = exp(i 2 q phi) psi_S  (transition function).
  Single-valuedness of exp(i 2 q phi) needs 2q integer: Dirac quantisation.
  A field of U(1)_X charge x in flux n has q = x n / 2.

Monopole harmonic (our normalisation, via Wigner small-d):
  Y^N_{q,l,m}(theta, phi) = sqrt((2l+1)/(4 pi)) d^l_{m,-q}(theta) exp(i (m+q) phi)
  Y^S_{q,l,m}(theta, phi) = exp(-i 2 q phi) Y^N_{q,l,m}
  l = |q|, |q|+1, ...; m = -l..l. It solves -Laplacian_A Y = (l(l+1) - q^2) Y.
"""
import math

import numpy as np


# ---------------- Wigner small-d (explicit sum, works for half-integers) -------------
def _fact(x):
    xi = int(round(x))
    assert abs(x - xi) < 1e-9 and xi >= 0, x
    return math.factorial(xi)


def wigner_d(l, mp, m, beta):
    """d^l_{mp,m}(beta), standard (Wigner / Condon-Shortley) convention, numpy array beta."""
    beta = np.asarray(beta, dtype=float)
    pref = math.sqrt(_fact(l + mp) * _fact(l - mp) * _fact(l + m) * _fact(l - m))
    c = np.cos(beta / 2.0)
    s = np.sin(beta / 2.0)
    out = np.zeros_like(beta)
    kmin = int(round(max(0, m - mp)))
    kmax = int(round(min(l + m, l - mp)))
    for k in range(kmin, kmax + 1):
        den = _fact(l + m - k) * _fact(k) * _fact(mp - m + k) * _fact(l - mp - k)
        pc = int(round(2 * l + m - mp - 2 * k))
        ps = int(round(mp - m + 2 * k))
        out = out + ((-1) ** (k + int(round(mp - m)))) / den * c ** pc * s ** ps
    return pref * out


def Y_north(q, l, m, theta, phi):
    return math.sqrt((2 * l + 1) / (4 * math.pi)) * wigner_d(l, m, -q, theta) * np.exp(1j * (m + q) * phi)


def Y_south(q, l, m, theta, phi):
    return np.exp(-1j * 2 * q * phi) * Y_north(q, l, m, theta, phi)


# ---------------- Dirac operator, method 1: monopole-harmonic basis ------------------
def dirac_harmonic_basis(n, lmax_extra=6):
    """Truncated Dirac matrix on S^2 with charge-1 field in flux n (q = n/2).

    Spinor components: upper (2D chirality +1) is a section of effective charge q - 1/2,
    lower (chirality -1) of effective charge q + 1/2. For each (l, m) where both
    exist, the Dirac operator is the 2x2 block [[0, lam], [lam, 0]] with
    lam = sqrt((l + 1/2)^2 - q^2)  [standard]. Where only one exists it is a 1x1 zero.
    Returns eigenvalues, chiralities (sigma3 expectation) of the zero eigenvectors.
    """
    q = n / 2.0
    qu, ql = q - 0.5, q + 0.5
    lmin = min(abs(qu), abs(ql))
    states = []   # (component sign, l, m)
    l = lmin
    while l <= lmin + lmax_extra + 1e-9:
        for comp, qe in ((+1, qu), (-1, ql)):
            if l >= abs(qe) - 1e-9:
                k = int(round(2 * l + 1))
                for i in range(k):
                    states.append((comp, l, -l + i))
        l += 1.0
    idx = {s: i for i, s in enumerate(states)}
    M = np.zeros((len(states), len(states)))
    for (comp, l, m), i in idx.items():
        if comp == +1 and (-1, l, m) in idx:
            j = idx[(-1, l, m)]
            lam = math.sqrt((l + 0.5) ** 2 - q * q)
            M[i, j] = M[j, i] = lam
    w, V = np.linalg.eigh(M)
    sig3 = np.array([s[0] for s in states], dtype=float)
    zero = np.abs(w) < 1e-9
    chir = [float(np.sum(sig3 * V[:, k] ** 2)) for k in np.where(zero)[0]]
    nonzero = np.sort(np.abs(w[~zero]))
    return int(zero.sum()), chir, (float(nonzero[0]) if len(nonzero) else float("nan")), len(states)


# ---------------- Dirac operator, method 2: independent finite differences ----------
# Frame e1 = dtheta, e2 = sin(theta) dphi, north gauge. With psi = e^{i m phi} sin(theta)^(-1/2) (u, v),
# m half-integer (rotating frame), the Dirac operator is off-diagonal with
#   L+ = d/dtheta - W,  L- = -d/dtheta - W,  W = (m - A_phi)/sin(theta), A_phi = q (1 - cos theta).
# D^2 on the upper component: -u'' + (W^2 + W') u ; on the lower: -v'' + (W^2 - W') v.
# Dirichlet ends u(0) = u(pi) = 0 select the regular solutions.

def _sturm_count(d, e, tau):
    """Number of eigenvalues < tau of a symmetric tridiagonal matrix (Sylvester inertia)."""
    cnt = 0
    piv = d[0] - tau
    if piv < 0:
        cnt += 1
    e2 = e * e
    for i in range(1, len(d)):
        if piv == 0.0:
            piv = 1e-300
        piv = (d[i] - tau) - e2[i - 1] / piv
        if piv < 0:
            cnt += 1
    return cnt


def _kth_eig(d, e, k, lo=-5.0, hi=200.0, iters=55):
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if _sturm_count(d, e, mid) > k:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def fd_operator(q, m, N, chirality):
    h = math.pi / (N + 1)
    th = h * np.arange(1, N + 1)
    s, c = np.sin(th), np.cos(th)
    W = (m - q + q * c) / s
    Wp = (-q - (m - q) * c) / s ** 2
    V = W ** 2 + (Wp if chirality > 0 else -Wp)
    d = 2.0 / h ** 2 + V
    e = -np.ones(N - 1) / h ** 2
    return d, e


def dirac_fd_count(n, N=4000, tau=0.5, mpad=6):
    """Count D^2 eigenvalues below tau, per chirality, summed over half-integer m.

    tau = 0.5 sits well below the smallest non-zero D^2 eigenvalue, which is >= 1
    on the unit sphere [standard]. Returns counts and the m values that carry them.
    """
    q = n / 2.0
    out = {+1: 0, -1: 0}
    ms = {+1: [], -1: []}
    M = abs(q) + mpad
    k = -int(math.ceil(M)) - 1
    while k <= int(math.ceil(M)) + 1:
        m = k + 0.5
        for ch in (+1, -1):
            d, e = fd_operator(q, m, N, ch)
            c = _sturm_count(d, e, tau)
            if c:
                out[ch] += c
                ms[ch].append(m)
        k += 1
    return out, ms


def fd_lowest(n, m, chirality, N, k=0):
    d, e = fd_operator(n / 2.0, m, N, chirality)
    return _kth_eig(d, e, k)

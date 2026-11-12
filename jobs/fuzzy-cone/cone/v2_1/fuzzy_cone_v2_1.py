"""FUZZY_CONE_SPEC_V2_1 (9dbd2f86) short test. Aethon 2026-10-30. Round fuzzy sphere, all matrices, no ring rule, no alpha.
Field content (fuzzy-sphere abelian Higgs, literature form): gauge = covariant coordinates X_a (N' x N', N' = N + 2n, spin j');
Higgs Phi = N' x N rectangular map V_j -> V_j'. Phi sections a monopole bundle of flux 2(j'-j) = 2n -> n strings per pole when
Phi vanishes at both poles. Physical units: sphere radius R, F_phys = F_matrix / R^2, D Phi = (X Phi - Phi L)/R,
integral dA <-> (4 pi R^2 / dim) Tr. [derived, flagged: spec silent; chosen so the continuum Bogomolny bound is E = pi * flux = 2 pi n]
Energy (4b self-dual): E = int [ B^2/2 + |D Phi|^2/2 + (1/8)(1 - |Phi|^2)^2 ] + radial-mode penalty (standard fuzzy-sphere
constraint X.X = j'(j'+1); flagged convention). B = n/R^2 (the bundle's own flux) + radial part of F_ab = i[X_a,X_b] + eps_abc X_c."""
import numpy as np, jax, jax.numpy as jnp
from scipy.optimize import minimize
jax.config.update("jax_enable_x64", True)
EPS = np.zeros((3, 3, 3))
for a, b, c in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]: EPS[a, b, c], EPS[b, a, c] = 1, -1

def spin(j):
    m = np.arange(j, -j - 1, -1); d = len(m)
    jp = np.diag(np.sqrt(j * (j + 1) - m[1:] * (m[1:] + 1)), 1)
    return [(jp + jp.T) / 2, (jp - jp.T) / 2j, np.diag(m).astype(complex)], m

class Model:
    def __init__(s, N, n, R=3.0, wrad=1000.0):
        s.N, s.n, s.R = N, n, R; s.j = (N - 1) / 2; s.jp = s.j + n; s.Np = N + 2 * n
        s.L, s.m = spin(s.j); s.Lp, s.mp = spin(s.jp); s.c = s.jp * (s.jp + 1); s.wrad = wrad
    def unpack(s, x):
        Np, N = s.Np, s.N; k = 0; X = []
        for a in range(3):
            A = x[k:k + Np * Np].reshape(Np, Np) + 1j * x[k + Np * Np:k + 2 * Np * Np].reshape(Np, Np); k += 2 * Np * Np
            X.append(jnp.asarray(s.Lp[a]) + 0.5 * (A + A.conj().T))
        P = x[k:k + Np * N].reshape(Np, N) + 1j * x[k + Np * N:].reshape(Np, N)
        return X, P
    def pieces(s, x):
        X, P = s.unpack(x); R = s.R; I = jnp.eye(s.Np)
        F = [[1j * (X[a] @ X[b] - X[b] @ X[a]) + sum(EPS[a, b, c] * X[c] for c in range(3)) for b in range(3)] for a in range(3)]
        xh = [Xa / np.sqrt(s.c) for Xa in X]
        Bd = sum(EPS[a, b, c] * 0.25 * (xh[a] @ F[b][c] + F[b][c] @ xh[a]) for a in range(3) for b in range(3) for c in range(3) if EPS[a, b, c])
        B = s.n / R**2 * I + Bd / R**2
        K = [(X[a] @ P - P @ jnp.asarray(s.L[a])) / R for a in range(3)]
        rad = (sum(Xa @ Xa for Xa in X) - s.c * I) / s.c
        return X, P, B, K, rad
    def dens(s, x):
        X, P, B, K, rad = s.pieces(x)
        eB = 0.5 * jnp.real(jnp.diag(B @ B))                                    # on V_j'
        xh = [Xa / np.sqrt(s.c) for Xa in X]; Kr = sum(xh[a] @ K[a] for a in range(3))   # radial part of the derivative
        eK = 0.5 * jnp.real(sum(jnp.diag(Ka.conj().T @ Ka) for Ka in K) - jnp.diag(Kr.conj().T @ Kr))   # tangential |D Phi|^2 only
        V = jnp.eye(s.N) - P.conj().T @ P; eV = 0.125 * jnp.real(jnp.diag(V @ V))
        return eB, eK, eV, rad
    def energy(s, x):
        eB, eK, eV, rad = s.dens(x); R = s.R
        return (4 * np.pi * R**2 / s.Np) * jnp.sum(eB) + (4 * np.pi * R**2 / s.N) * jnp.sum(eK + eV) \
               + s.wrad * (4 * np.pi * R**2 / s.Np) * jnp.real(jnp.sum(jnp.abs(rad) ** 2))
    def nX(s): return 6 * s.Np * s.Np
    def seed_fuzzy(s):
        """Coherent-state pole projectors: Phi = isometric embedding |j,m> -> |j',m>, so ker Phi^+ = top n and bottom n states of V_j',
        i.e. the rank-n coherent-state projectors at the north and south poles. X = L' (round sphere)."""
        P = np.zeros((s.Np, s.N)); P[s.n:s.n + s.N, :] = np.eye(s.N)
        return np.concatenate([np.zeros(s.nX()), P.ravel(), np.zeros(P.size)])
    def seed_smooth(s, f_of_r):
        """Smooth continuum seed: same embedding times the continuum V1_4b (alpha=1) vortex profile of the geodesic distance to the
        nearer pole, sampled at x3 = m/(j+1/2)."""
        th = np.arccos(np.clip(s.m / (s.j + 0.5), -1, 1)); r = s.R * np.minimum(th, np.pi - th)
        P = np.zeros((s.Np, s.N)); P[s.n:s.n + s.N, :] = np.diag(f_of_r(r))
        return np.concatenate([np.zeros(s.nX()), P.ravel(), np.zeros(P.size)])

def relax(M, x0):
    E = jax.jit(M.energy); G = jax.jit(jax.grad(E))
    r = minimize(lambda x: float(E(x)), x0, jac=lambda x: np.asarray(G(x)), method="L-BFGS-B",
                 options=dict(maxiter=40000, maxfun=80000, ftol=1e-16, gtol=1e-11, maxcor=30))
    return r.x, float(r.fun), bool(r.success), int(r.nit)

def symbol_diag(M, A, th):
    """<theta|A|theta> for spin-j' coherent states at polar angle theta (phi=0), basis ordered m = j'..-j'."""
    from scipy.special import gammaln
    j = M.jp; m = M.mp; lb = 0.5 * (gammaln(2 * j + 1) - gammaln(j + m + 1) - gammaln(j - m + 1))
    c, s_ = np.cos(th / 2)[:, None], np.sin(th / 2)[:, None]
    with np.errstate(divide="ignore"):
        lc, ls = np.log(np.abs(c)), np.log(np.abs(s_))
        lv = lb[None, :] + np.where((j + m)[None, :] == 0, 0.0, (j + m)[None, :] * lc) + np.where((j - m)[None, :] == 0, 0.0, (j - m)[None, :] * ls)
    v = np.exp(lv); return np.real(np.einsum("ti,ij,tj->t", v, A, v))

def cap_flux_symbol(M, B, thc, nth=4001):
    th = np.linspace(0, thc, nth); R = M.R
    bN = symbol_diag(M, B, th); bS = symbol_diag(M, B, np.pi - th)
    w = R**2 * np.sin(th)                                   # (1/2pi) * int B R^2 sin dth dphi
    return float(np.trapezoid(bN * w, th)), float(np.trapezoid(bS * w, th))

def observe(M, x, rc=1.5):
    X, P, B, K, rad = (np.asarray(v) if not isinstance(v, list) else [np.asarray(u) for u in v] for v in M.pieces(x))
    eB, eK, eV, _ = (np.asarray(v) for v in M.dens(x)); R = M.R
    # position read-out only: spectral projectors of x3 (X_3 eigenbasis) on each space
    w3, U3 = np.linalg.eigh(X[2]); cosp = w3 / np.sqrt(M.c)
    Bm = np.real(np.einsum("ia,ij,ja->a", U3.conj(), B, U3)); area_p = 4 * np.pi * R**2 / M.Np
    thc = rc / R
    # cap flux: symbol of B (spin-j' coherent states of the round background) integrated on a fixed fine theta grid
    QN, QS = cap_flux_symbol(M, np.asarray(B), thc)
    Qtot = area_p * Bm.sum() / (2 * np.pi)
    wP, UP = np.linalg.eigh(P @ P.conj().T); ker = UP[:, wP < 1e-8]
    kx3 = np.real(np.einsum("ik,ij,jk->k", ker.conj(), X[2], ker)) / np.sqrt(M.c)
    rankN, rankS = int((kx3 > 0).sum()), int((kx3 < 0).sum())
    # energy density per x3-shell (shell index ordered by x3), mapped to geodesic distance from each pole
    eBm = np.real(np.einsum("ia,ij,ja->a", U3.conj(), np.asarray(B @ B) * 0.5, U3))
    cos_j = M.m / (M.j + 0.5); cos_p = cosp
    dens_p = eBm                                              # B^2/2 on V_j' shells
    dens_j = eK + eV                                          # on V_j shells (J3 basis; X-side background)
    def prof(cosv, dv, north):
        th = np.arccos(np.clip(cosv, -1, 1)); r = R * (th if north else np.pi - th); sel = r <= np.pi * R / 2
        o = np.argsort(r[sel]); return r[sel][o], dv[sel][o]
    out = {}
    for pole, north in (("north", True), ("south", False)):
        r1, d1 = prof(cos_p, dens_p, north); r2, d2 = prof(cos_j, dens_j, north)
        rr = np.union1d(r1, r2); tot = np.interp(rr, r1, d1) + np.interp(rr, r2, d2)
        out[pole] = dict(r=rr.tolist(), e=tot.tolist(), r_peak=float(rr[np.argmax(tot)]), ring=bool(rr[np.argmax(tot)] > rr[0] + 1e-9),
                         mu=float(area_p * dens_p[(cos_p >= 0) if north else (cos_p < 0)].sum() + (4 * np.pi * R**2 / M.N) * dens_j[(cos_j >= 0) if north else (cos_j < 0)].sum()))
    return dict(Q_cap_N=float(QN), Q_cap_S=float(QS), Q_total=float(Qtot), rank_N=rankN, rank_S=rankS, kernel_dim=int(ker.shape[1]),
                radial_resid=float(np.linalg.norm(np.asarray(rad))), profiles=out)

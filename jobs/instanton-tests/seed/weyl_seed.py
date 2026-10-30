"""Weyl (Stratonovich-Weyl / canonical, rotation-equivariant) quantisation of functions on S^2, and the
classical IT1b seed field (regular-gauge BPST core, gauge-rotated to singular gauge for chart radius r >= r_g,
then tapered). Fix list VENUS_IT1B_CODE_CHECK 1db2bdc3 items 16 (B3), 18 (B5), 19 (seed level); addendum V2 b3e1b9d1.

Q(f) = sum_{l<N, m} f_lm Yhat_lm,  f_lm = int f Y_lm^* dOmega,  Yhat_lm the spin-l tensor operators normalised
isometrically, (4 pi/N) Tr(Yhat_lm^+ Yhat_l'm') = delta delta, phases fixed by Yhat_ll ~ (-1)^l (L+)^l and the
L- ladder (same as Condon-Shortley Y_lm). Properties (unit-tested): Q(n_i) = L_i/sqrt(j(j+1)) exactly;
[L_i, Q f] = Q(L_i f) (equivariance); (4 pi R^2/N) Tr Q(f) = R^2 int f dOmega exactly.
"""
import numpy as np
from scipy.special import sph_harm_y

ETA = np.zeros((3, 4, 4))
for a in range(3):
    for mu in range(4):
        for nu in range(4):
            if mu < 3 and nu < 3:
                ETA[a, mu, nu] = ((a - mu) * (mu - nu) * (nu - a)) / 2 if len({a, mu, nu}) == 3 else 0.0
            elif nu == 3 and mu < 3: ETA[a, mu, nu] = float(a == mu)
            elif mu == 3 and nu < 3: ETA[a, mu, nu] = -float(a == nu)
SIG = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], complex)


def smooth_step(x):
    """0 for x<=0, 1 for x>=1, C-infinity (FUZZ_PLAN_V5 §2 s)."""
    x = np.clip(x, 0.0, 1.0)
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        e0 = np.where(x > 0, np.exp(-1 / np.where(x > 0, x, 1)), 0.0)
        e1 = np.where(x < 1, np.exp(-1 / np.where(x < 1, 1 - x, 1)), 0.0)
    return e0 / (e0 + e1)


class WeylQuantizer:
    def __init__(self, N, quad_mult=2, quad_extra=32):
        self.N = N; j = (N - 1) / 2.0; mv = j - np.arange(N)
        lp = np.sqrt(j * (j + 1) - mv[1:] * (mv[1:] + 1))          # (L+)[a-1, a] = lp[a-1]
        self.nth = quad_mult * N + quad_extra; self.nph = 12 * int(np.ceil(2 * self.nth / 12))   # multiple of 12: Z_k grid symmetry exact for k | 12
        t, w = np.polynomial.legendre.leggauss(self.nth)
        self.cth, self.wth = t, w; self.th = np.arccos(t); self.ph = 2 * np.pi * np.arange(self.nph) / self.nph
        nrm = np.sqrt(N / (4 * np.pi))
        # Yhat_lm on the offset-m diagonal (entries [a, a+m]) = eigenvectors of the su(2) Casimir
        # sum_i [L_i,[L_i, .]] restricted to that diagonal (symmetric tridiagonal, eigenvalue l(l+1), stable).
        # Phases: Yhat_ll ~ (-1)^l (L+)^l; Yhat_{l,m-1} has positive overlap with [L-, Yhat_lm] (Condon-Shortley);
        # Yhat_{l,-m} = (-1)^m Yhat_lm^+ (same as Y_{l,-m} = (-1)^m Y_lm^*).
        from scipy.linalg import eigh_tridiagonal
        self.K = {}
        V = {}
        for m in range(N):
            a = np.arange(N - m); b = a + m
            dg = 2 * j * (j + 1) - 2 * mv[a] * mv[b]
            off = -(lp[a[1:] - 1] * lp[b[1:] - 1])
            ev, vec = eigh_tridiagonal(dg, off)
            ls = np.rint((-1 + np.sqrt(1 + 4 * ev)) / 2).astype(int)
            assert np.all(ls == np.arange(m, N)), "Casimir spectrum"
            V[m] = vec * nrm                       # column l-m <-> l
        D = {}
        for l in range(N):
            d = V[l][:, 0].copy()
            top = np.array([np.prod(lp[x:x + l]) for x in range(N - l)])
            if np.dot(d, top) * (-1) ** l < 0: d = -d
            D[(l, l)] = d
            for m in range(l, 0, -1):               # sign from the ladder
                prev = D[(l, m)]; full = np.zeros(N); full[:N - m] = prev
                lad = np.zeros(N - m + 1)
                for x in range(N - m + 1):          # [L-, Y][x, x+m-1]
                    v = 0.0
                    if x >= 1: v += lp[x - 1] * full[x - 1]
                    if x + m - 1 < N - 1 and x < N - m: v -= full[x] * lp[x + m - 1]
                    lad[x] = v
                d = V[m - 1][:, l - (m - 1)].copy()
                if np.dot(d, lad) < 0: d = -d
                D[(l, m - 1)] = d
        for m in range(0, N):
            Ys = sph_harm_y(np.arange(m, N)[:, None], m, self.th[None, :], 0.0).real   # (l, nth)
            K = np.zeros((self.nth, N)); K[:, :N - m] = Ys.T @ np.stack([D[(l, m)] for l in range(m, N)])
            self.K[m] = K
            if m > 0:
                # Yhat_{l,-m}[a, a-m] = (-1)^m conj(Yhat_lm[a-m, a]); Y_{l,-m}(th,0) = (-1)^m Y_lm(th,0)
                Kn = np.zeros((self.nth, N)); Kn[:, m:] = K[:, :N - m]          # signs cancel
                self.K[-m] = Kn
        self.n = np.stack([np.sin(self.th)[:, None] * np.cos(self.ph)[None, :],
                           np.sin(self.th)[:, None] * np.sin(self.ph)[None, :],
                           np.cos(self.th)[:, None] * np.ones(self.nph)[None, :]])   # (3, nth, nph)

    def quantize(self, f):
        """f: (..., nth, nph) real samples on the grid -> (..., N, N) Hermitian matrices."""
        N = self.N; sh = f.shape[:-2]; f = f.reshape((-1, self.nth, self.nph))
        F = np.fft.fft(f, axis=-1) * (2 * np.pi / self.nph)          # F_m(theta) at index m mod nph
        out = np.zeros((f.shape[0], N, N), complex)
        for m in range(-(N - 1), N):
            Fm = F[:, :, m % self.nph] * self.wth[None, :]           # (P, nth)
            v = Fm @ self.K[m]                                       # (P, N): entry [a, a+m]
            a = np.arange(max(0, -m), min(N, N - m))
            out[:, a, a + m] = v[:, a]
        return out.reshape(sh + (N, N))


class SeedField:
    """Classical seed on (S^2 radius R) x (x3,x4). Chart from the SOUTH pole, x_a = 2R n_a/(1+n3).
    A = regular-gauge BPST (t Hooft, A = A^a sigma_a), gauge-rotated by g(x) = (y4 - i y.sigma)/|y| with
    y = (x1, x2, x3, x4 + (1 - s(r)) D), s = smooth step from r_a to r_g in chart radius r: g is exactly the
    singular-gauge map for r >= r_g (A ~ rho^2/r^3) and smooth (no singularity in the box) inside; then all
    components multiplied by the taper chi(r) (=1 for r<=r0, 0 for r>=r1)."""
    def __init__(self, R, rho, r0, r1, gauge):
        self.R, self.rho, self.r0, self.r1 = R, rho, r0, r1; self.gauge = gauge   # gauge dict or None (regular)

    def A4(self, n, x3, x4, mus=(0, 1, 2, 3)):
        """n: (3, ...) unit vectors; x3, x4 broadcastable scalars/arrays. Returns chart-frame A_mu^a, shape (4,3,...),
        and chart helpers. mu = 0,1 chart; 2,3 = x3,x4."""
        R, rho = self.R, self.rho
        den = 1 + n[2]
        x1 = 2 * R * n[0] / den; x2 = 2 * R * n[1] / den
        shp = np.broadcast_shapes(x1.shape, np.shape(x3), np.shape(x4))
        x1, x2 = np.broadcast_to(x1, shp), np.broadcast_to(x2, shp)
        x3 = np.broadcast_to(x3, shp); x4 = np.broadcast_to(x4, shp)
        X = np.stack([x1, x2, x3, x4]); r = np.sqrt(x1**2 + x2**2)
        x2s = (X**2).sum(0)
        mus = list(mus)
        A = np.einsum("amn,n...->ma...", ETA[:, mus], X) / (x2s + rho**2)   # (len(mus),3,...)
        if self.gauge is not None and self.gauge.get("mode") == "antipode_v4":
            # V4 seed (SEED_PASS_RULES_V4 73b3cae4): G = (x4 + i x.sigma)/|x| = exp(theta m.(-i sigma)), m = -xvec/|xvec|,
            # cos theta = x4/|x|, at every full 4D point; h = G^{-s(r_p)} = cos(s theta) - i sin(s theta) u.sigma, u = xvec/|xvec|;
            # s = 1 for r_p <= eps/2, C-inf smoothstep to 0 at r_p = eps. A' = h A h^+ + i h dh^+, analytic dh.
            A = self._antipode_v4(A, X, mus, self.gauge["eps"], R)
            return A, (x1, x2, r, den)
        if self.gauge is not None and self.gauge.get("mode") == "antipode":
            # V3 seed (SEED_PASS_RULES_V3): regular gauge, then on the polar cap (polar distance r_p < eps from the
            # S^2 south pole = chart infinity) h = M(s,phi) G^-1, s = 1 - r_p/eps; h = 1 outside. A' = h A h^+ + i h dh^+
            # (this code's D = d - iA convention). G = (x4 + i x.sigma)/|x| is the pure gauge the regular field tends to
            # (A_reg -> i G dG^+); at the pole G -> Linf(phi) = i(cos phi s1 + sin phi s2) [= -i s1 e^{i phi s3} of the
            # brief up to the sign convention]; M = sin(pi s/2) 1 + cos(pi s/2) Linf(phi). A' sampled from this formula.
            A = self._antipode_rotate(A, X, mus, self.gauge["eps"], R)
            return A, (x1, x2, r, den)
        if self.gauge is not None and self.gauge.get("mode") == "patch":
            # two-patch seed (pass rules V1): regular BPST for |x| < r_g, singular-gauge BPST (own formula,
            # = x̂-rotated regular, ~rho^2/r^3) for |x| >= r_g; glued by g = x̂.sigma across the 4D S^3 |x| = r_g.
            dY = np.zeros((4, 4) + shp)
            for q in range(4): dY[q, q] = 1.0
            As = self._gauge_rotate(A, X, dY, mus)
            A = np.where(np.sqrt(x2s) < self.gauge["r_g"], A, As)
        elif self.gauge is not None:
            ra, rg, D = self.gauge["r_a"], self.gauge["r_g"], self.gauge["D"]
            u = (r - ra) / (rg - ra); s = smooth_step(u)
            h = 1e-6; sp = (smooth_step(u + h) - smooth_step(u - h)) / (2 * h) / (rg - ra)   # ds/dr
            Y = X.copy(); Y[3] = x4 + (1 - s) * D
            dY = np.zeros((4, 4) + shp)        # dY[nu, mu] = dy_nu/dx_mu
            for q in range(4): dY[q, q] = 1.0
            with np.errstate(invalid="ignore", divide="ignore"):
                rr = np.where(r > 0, r, 1.0)
                dY[3, 0] = -sp * x1 / rr * D; dY[3, 1] = -sp * x2 / rr * D
            A = self._gauge_rotate(A, Y, dY, mus)
        chi = smooth_step((self.r1 - r) / (self.r1 - self.r0))
        return A * chi, (x1, x2, r, den)

    @staticmethod
    def h_field(X, eps, R):
        """h(x) as 2x2 matrices (..., 2, 2) on chart points X (4, ...); h = 1 outside the polar cap."""
        x1, x2 = X[0], X[1]; r = np.sqrt(x1**2 + x2**2)
        rp = np.pi - 2 * np.arctan(r / (2 * R))                  # polar distance from the south pole
        s = np.clip(1 - rp / eps, 0.0, 1.0); ph = np.arctan2(x2, x1)
        I = np.eye(2, dtype=complex); S1, S2, S3 = (np.array(m) for m in SIG)
        Linf = 1j * (np.cos(ph)[..., None, None] * S1 + np.sin(ph)[..., None, None] * S2)
        M = np.sin(np.pi * s / 2)[..., None, None] * I + np.cos(np.pi * s / 2)[..., None, None] * Linf
        nx = np.sqrt((X**2).sum(0))
        G = (X[3][..., None, None] * I + 1j * np.einsum("a...,aij->...ij", X[:3], SIG)) / nx[..., None, None]
        h = M @ np.conj(np.swapaxes(G, -1, -2))
        return np.where((rp < eps)[..., None, None], h, I)

    @staticmethod
    def s_v4(rp, eps):
        """C-infinity step: 1 for rp <= eps/2, 0 for rp >= eps; returns (s, ds/drp)."""
        t = np.clip((eps - rp) / (eps / 2), 0.0, 1.0)
        with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
            f = np.where(t > 0, np.exp(-1 / np.where(t > 0, t, 1)), 0.0)
            g = np.where(t < 1, np.exp(-1 / np.where(t < 1, 1 - t, 1)), 0.0)
            df = np.where(t > 0, f / np.where(t > 0, t, 1)**2, 0.0)
            dg = np.where(t < 1, -g / np.where(t < 1, 1 - t, 1)**2, 0.0)
            S = f / (f + g); dS = (df * (f + g) - f * (df + dg)) / (f + g)**2
        return S, dS * (-2 / eps)

    @classmethod
    def h_v4(cls, X, eps, R):
        """Unit quaternion (Y (4,...): y1..3 = sin(s th) u, y4 = cos(s th)) and dY[nu, mu] = dy_nu/dx_mu; h = y4 - i y.sigma."""
        x1, x2 = X[0], X[1]; r = np.sqrt(x1**2 + x2**2); R2 = 2 * R
        rp = np.pi - 2 * np.arctan(r / R2)
        s, dsr = cls.s_v4(rp, eps)
        r3 = np.sqrt((X[:3]**2).sum(0)); n2 = (X**2).sum(0)
        th = np.arctan2(r3, X[3]); u = X[:3] / r3
        drp = np.zeros_like(X); drp[0] = -2 / R2 / (1 + (r / R2)**2) * x1 / r; drp[1] = -2 / R2 / (1 + (r / R2)**2) * x2 / r
        dth = np.zeros_like(X); dth[:3] = X[3] * X[:3] / (r3 * n2); dth[3] = -r3 / n2
        ph = s * th; dph = dsr * drp * th + s * dth                  # (4 mu, ...)
        Y = np.concatenate([np.sin(ph) * u, np.cos(ph)[None]])
        dY = np.zeros((4,) + X.shape)
        for mu in range(4):
            du = -u * u[mu if mu < 3 else 0] / r3 * (mu < 3)
            if mu < 3: du[mu] += 1 / r3
            dY[:3, mu] = np.cos(ph) * dph[mu] * u + np.sin(ph) * du
            dY[3, mu] = -np.sin(ph) * dph[mu]
        return Y, dY, th, s

    def _antipode_v4(self, A, X, mus, eps, R):
        r = np.sqrt(X[0]**2 + X[1]**2); cap = (np.pi - 2 * np.arctan(r / (2 * R))) < eps
        if not cap.any(): return A
        Y, dY, _, _ = self.h_v4(X[:, cap], eps, R)
        qv, q0 = Y[:3], Y[3]; Ac = A[:, :, cap]
        Ar = (q0**2 - (qv**2).sum(0)) * Ac + 2 * qv[None] * (qv[None] * Ac).sum(1, keepdims=True) \
             - 2 * q0 * np.cross(Ac, qv[None] * np.ones_like(Ac), axis=1)
        out = A.copy()
        for o, mu in enumerate(mus):
            dqv, dq0 = dY[:3, mu], dY[3, mu]
            out[o][:, cap] = Ar[o] - (q0 * dqv - dq0 * qv + np.cross(qv, dqv, axis=0))
        return out

    def _antipode_rotate(self, A, X, mus, eps, R, hstep=None):
        mus = list(mus)
        r = np.sqrt(X[0]**2 + X[1]**2); rp = np.pi - 2 * np.arctan(r / (2 * R))
        cap = rp < eps
        if not cap.any(): return A
        Xc = X[:, cap]; Ac = A[:, :, cap]                           # (4, P), (m, 3, P)
        h = self.h_field(Xc, eps, R); hd = np.conj(np.swapaxes(h, -1, -2))
        out = A.copy()
        for o, mu in enumerate(mus):
            st = (hstep or 1e-5) * np.maximum(1.0, np.abs(Xc[mu]))
            Xp = Xc.copy(); Xm = Xc.copy(); Xp[mu] += st; Xm[mu] -= st
            dhd = (np.conj(np.swapaxes(self.h_field(Xp, eps, R), -1, -2)) - np.conj(np.swapaxes(self.h_field(Xm, eps, R), -1, -2))) / (2 * st)[..., None, None]
            Am = np.einsum("a...,aij->...ij", Ac[o], SIG)
            Mx = h @ Am @ hd + 1j * h @ dhd
            out[o][:, cap] = 0.5 * np.einsum("...ij,aji->a...", Mx, SIG).real
        return out

    @staticmethod
    def _gauge_rotate(A, Y, dY, mus=(0, 1, 2, 3)):
        """Same as _gauge_rotate_ref (unit-tested), in real quaternion algebra. g = q0 - i q.sigma, q = (Y_1..3, Y_4)/|Y|:
        g sigma_b g^+ = O_ab sigma_a, O_ab = (q0^2-|q|^2) d_ab + 2 q_a q_b - 2 q0 eps_abc q_c;
        i g dg^+ = -(q0 dq - dq0 q + q x dq).sigma.  Only dY[3,0], dY[3,1] differ from the identity."""
        ny = np.sqrt((Y**2).sum(0)); qv = Y[:3] / ny; q0 = Y[3] / ny
        Ar = (q0**2 - (qv**2).sum(0)) * A + 2 * qv[None] * (qv[None] * A).sum(1, keepdims=True) \
             - 2 * q0 * np.cross(A, qv[None] * np.ones_like(A), axis=1)
        Q4 = np.concatenate([qv, q0[None]])                     # (4, ...) components y1,y2,y3,y4
        out = np.empty_like(A)
        for o, mu in enumerate(mus):
            dq = (-(Q4 * Q4[mu])); dq[mu] += 1.0
            if mu < 2 and dY[3, mu].any():
                ex = -(Q4 * Q4[3]); ex[3] += 1.0; dq = dq + dY[3, mu] * ex
            dq = dq / ny
            dqv, dq0 = dq[:3], dq[3]
            out[o] = Ar[o] - (q0 * dqv - dq0 * qv + np.cross(qv, dqv, axis=0))
        return out

    @staticmethod
    def _gauge_rotate_ref(A, Y, dY):
        """A' = g A g^+ + i g dg^+ (D = d - iA), g = (y4 - i y.sigma)/|y|, A = A^a sigma_a; explicit 2x2 matrices.
        dY[nu, mu] = dy_nu/dx_mu. Returns A'^a (4, 3, ...)."""
        ny = np.sqrt((Y**2).sum(0)); q = Y / ny
        g = q[3][..., None, None] * np.eye(2) - 1j * np.einsum("a...,aij->...ij", q[:3], SIG)
        gd = np.conj(np.swapaxes(g, -1, -2))
        dq = np.einsum("nm...,n...->m...", dY, (np.eye(4).reshape((4, 4) + (1,) * ny.ndim) - q[:, None] * q[None]) / ny)  # dq_nu/dx_mu summed -> [mu][nu]
        out = np.empty_like(A)
        for mu in range(4):
            Am = np.einsum("a...,aij->...ij", A[mu], SIG)
            dg = dq[mu][3][..., None, None] * np.eye(2) - 1j * np.einsum("a...,aij->...ij", dq[mu][:3], SIG)
            M = g @ Am @ gd + 1j * g @ np.conj(np.swapaxes(dg, -1, -2))
            out[mu] = 0.5 * np.einsum("...ij,aji->a...", M, SIG).real
        return out

def link_functions(sf, n, x3, x4, mu):
    """A_{x3}^a (mu=0) or A_{x4}^a (mu=1) on unit vectors n, shape (3 a, ...)."""
    A, _ = sf.A4(n, x3, x4, mus=(2 + mu,)); return A[0]

def seed_functions(sf, n, x3, x4):
    """Return Ahat_i^a (3 i, 3 a, ...) = R eps_ijk A_j n_k and A_x3^a, A_x4^a, on unit vectors n."""
    R = sf.R
    A, chart = sf.A4(n, x3, x4)
    den = chart[3]; c = 2 / den; d = -2 / (R * den**2); X = R * n
    Ae = np.stack([A[0] * c, A[1] * c, A[0] * X[0] * d + A[1] * X[1] * d])     # (3 i, 3 a, ...)
    nA = (Ae * n[:, None]).sum(0)
    At = Ae - n[:, None] * nA[None]
    Ahat = R * np.cross(At, n[:, None] * np.ones_like(At), axis=0)               # (A x n)_i
    return Ahat, A[2], A[3]

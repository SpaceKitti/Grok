"""Open (non-periodic) hypercubic box for boundary fix B1 (2BA983A1), amending gates 1A723DCE [hive proposal, untested].
Subclass of hc_kernel.HCLoops (hc_kernel.py unchanged). Sites 0..L-1 in each direction; link U_mu(x) exists only for x_mu <= L-2.
No loop wraps: every loop whose corners leave the box is masked out of the action, density and force (np.roll wrap-arounds
therefore never contribute). Links with x_mu = L-1 are dummies (identity, frozen, in no loop).
Clamp: links touching a site in the outer NFIX=2 site layers (min(x_i, L-1-x_i) < 2) are fixed and never flowed.
Config: exact regular-gauge BPST everywhere (B1 sets the clamp in regular gauge and leaves the interior gauge unspecified ->
regular gauge used for the interior too), P-ordered holonomy over nsub midpoint segments, no cooling.
Default centre: cell centre (L-1)/2 in all four directions (box symmetric; regular gauge has no singular point)."""
import numpy as np
import hc_kernel as H
from lattice import qmul, qconj, qexp_im

class HCOpen(H.HCLoops):
    def __init__(self, L, eps, centre=None, nfix=H.NFIX):
        super().__init__(L, eps, centre=((L-1)/2 if centre is None else centre), nfix=nfix)
        X = self.X
        self.dummy = np.stack([X[..., mu] == L-1 for mu in range(4)]).reshape(-1)
        lay = np.minimum(X, L-1-X).min(-1)
        fz = np.zeros((4,)+(L,)*4, bool)
        for mu in range(4):
            nb = np.full(lay.shape, 99.); nb[tuple(slice(None) if i != mu else slice(0, L-1) for i in range(4))] = \
                lay[tuple(slice(None) if i != mu else slice(1, L) for i in range(4))]
            fz[mu] = (lay < nfix) | (nb < nfix)
        self.clamp = fz.reshape(-1) & ~self.dummy        # real clamped links
        self.frozen = self.clamp | self.dummy
        self.layer = lay
    def valid(self, mu, nu, s):
        """1.0 where the s x s loop with lower-left corner x lies inside the box."""
        X = self.X; return ((X[..., mu] + s <= self.L-1) & (X[..., nu] + s <= self.L-1)).astype(float)
    def action(self, U, per_site=False, loop_mask=None):
        U4 = self.U4(U); S = 0.0; dens = np.zeros((self.L,)*4) if per_site else None
        for s, cs in self.loops():
            for mu in range(4):
                for nu in range(mu+1, 4):
                    m = self.valid(mu, nu, s)
                    if loop_mask is not None: m = m*loop_mask(mu, nu, s)
                    val = m*cs*4*(1 - self.squares(U4, mu, nu, s)[..., 0]); S += float(val.sum())
                    if per_site:
                        q = val/4
                        dens += q + np.roll(q, s, axis=mu) + np.roll(np.roll(q, s, axis=mu), s, axis=nu) + np.roll(q, s, axis=nu)
        return (S, dens.reshape(-1)) if per_site else S
    def staple_sum(self, U4, mu):
        """As HCLoops.staple_sum, each staple weighted by the in-box mask of its loop's corner."""
        tot = None
        for s, cs in self.loops():
            Lm = self.line(U4, mu, s)
            for nu in range(4):
                if nu == mu: continue
                Ln = self.line(U4, nu, s); V = self.valid(mu, nu, s)[..., None]
                for k in range(s):
                    rest = self.line(U4, mu, s-k-1) if s-k-1 > 0 else None
                    x_up = lambda A: self.sh(A, mu, -k)
                    one = H.ident(U4.shape[1:-1])
                    up = qmul(qmul(x_up(self.sh(Ln, mu, s)), qconj(x_up(self.sh(Lm, nu, s)))), qmul(qconj(x_up(Ln)), x_up(self.line(U4, mu, k)) if k else one))
                    x_dn = lambda A: self.sh(self.sh(A, mu, -k), nu, -s)
                    dn = qmul(qmul(qconj(x_dn(self.sh(Ln, mu, s))), qconj(x_dn(Lm))), qmul(x_dn(Ln), x_dn(self.sh(self.line(U4, mu, k), nu, s)) if k else one))
                    st = x_up(V)*up + x_dn(V)*dn
                    if rest is not None: st = qmul(self.sh(rest, mu, 1), st)
                    tot = cs*st if tot is None else tot + cs*st
        return tot
    def clamp_loop_mask(self, U):
        """Loop mask: 1 where the loop contains at least one clamped link."""
        C = self.clamp.reshape((4,)+(self.L,)*4)
        def lm(mu, nu, s):
            hit = np.zeros(C.shape[1:], bool)
            for j in range(s):
                hit |= self.sh(C[mu], mu, j) | self.sh(self.sh(C[mu], mu, j), nu, s) | self.sh(C[nu], nu, j) | self.sh(self.sh(C[nu], nu, j), mu, s)
            return hit.astype(float)
        return lm
    def interior_charge(self, U, rball=None):
        """Clover Q summed over sites with |x - centre| <= rball (B1: interior Q only).
        q = (1/2pi^2) sum (f12.f34 - f13.f24 + f14.f23): Q = (1/32pi^2) int F^a Ftilde^a, Ftilde = eps F / 2, F^a = 2 f / a^2.
        NOTE hc_kernel.HCLoops.charge (frozen 305F518F) uses 1/pi^2, i.e. it is 2x too large; not used on the open box."""
        rball = self.L/2-3 if rball is None else rball
        U4 = self.U4(U); f = {}
        for mu in range(4):
            for nu in range(mu+1, 4):
                Um, Un = U4[mu], U4[nu]
                l1 = self.squares(U4, mu, nu, 1)
                l2 = qmul(qmul(Un, qconj(self.sh(self.sh(Um, nu, 1), mu, -1))), qmul(qconj(self.sh(Un, mu, -1)), self.sh(Um, mu, -1)))
                l3 = qmul(qmul(qconj(self.sh(Um, mu, -1)), qconj(self.sh(self.sh(Un, mu, -1), nu, -1))), qmul(self.sh(self.sh(Um, mu, -1), nu, -1), self.sh(Un, nu, -1)))
                l4 = qmul(qmul(qconj(self.sh(Un, nu, -1)), self.sh(Um, nu, -1)), qmul(self.sh(self.sh(Un, mu, 1), nu, -1), qconj(Um)))
                f[(mu, nu)] = ((l1 + l2 + l3 + l4)/4)[..., 1:]
        dot = lambda a, b: (f[a]*f[b]).sum(-1)
        q = (dot((0, 1), (2, 3)) - dot((0, 2), (1, 3)) + dot((0, 3), (1, 2)))/(2*np.pi**2)
        assert rball <= min(self.centre.min(), self.L-1-self.centre.max()) - 1, "ball clover would leave the box"
        return float(q[self.dist <= rball].sum())

def bpst_regular(hc, rho, nsub=16):
    """Exact regular-gauge BPST links (A = Im(xbar dx)/(|x|^2+rho^2), as lattice.bpst_links before its gauge rotation),
    no wrap (displacement y = x - centre, unwrapped); dummy links = identity."""
    y = hc.X - hc.centre; U = np.empty((4,)+y.shape[:-1]+(4,))
    for mu in range(4):
        e = np.zeros(4); e[mu] = 1.0; Hh = None
        for s in range(nsub):
            xm = y + e*(s+0.5)/nsub
            v = qmul(qconj(xm), np.broadcast_to(e/nsub, xm.shape))[..., 1:]/(np.sum(xm**2, -1)+rho**2)[..., None]
            E = qexp_im(v); Hh = E if Hh is None else qmul(Hh, E)
        U[mu] = Hh
    U = U.reshape(-1, 4); U[hc.dummy] = [1., 0, 0, 0]; return U

def continuum_density(d, rho):
    """BPST action density normalised so its integral over R^4 is 8 pi^2: 48 rho^4/(x^2+rho^2)^4."""
    return 48*rho**4/(d**2+rho**2)**4

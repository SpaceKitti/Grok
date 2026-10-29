"""Hypercubic periodic L^4 SU(2) kernel for the over-improved-flow reproduction (HYPERCUBIC_REPRO_GATES) [hive proposal, untested].
Quaternion links U[mu][x] (q0..q3, Tr U = 2 q0), same normalisation as the polar code: a continuum BPST has S = 8 pi^2.
S(eps) = sum_x sum_{mu<nu} [ c1 * 4(1 - q0(W_1x1)) + c2 * 4(1 - q0(W_2x2)) ],  c1 = (4-eps)/3, c2 = (eps-1)/48  (true 2x2 SQUARES).
(4(1-q0) = 2 Re Tr(1-W); summing mu<nu with this factor equals the ordered-pair sum of Re Tr(1-W) used in NPB413.)
Reused UNCHANGED from IT1b (run.py D9D6766D tree): quaternion algebra (lattice.py), Loops.step and Loops.flow (kernels.py, Luscher RK3).
Force = staples of the same S(eps): left variation U -> exp(tau) U, dS/dtau = 4 Im(U * sum_s c_s * staples_s).
Fixed boundary: links touching the outer NFIX site layers of the periodic box (seam included) are frozen (never flowed).
rho: same definition as IT1b Loops.rho_moment: per-site action density (each loop split equally over its 4 corners),
rho = sqrt(<d^2>/2), d = distance to the BPST centre, sites with d >= RMIN only, here further restricted to the interior ball d <= L/2-3."""
import numpy as np
from lattice import qmul, qconj, qexp_im, ident
from kernels import Loops

RMIN = 2.0   # as Loops.rho_moment default (rmin=2.0)
NFIX = 2     # outer link layers held fixed

def coeffs(eps):
    """Same formula as kernels.Loops.__init__ / lattice.Lattice.action: c11, c22 = (4-eps)/3, (eps-1)/48."""
    return (4-eps)/3, (eps-1)/48

class HCLoops:
    flow = Loops.flow          # unchanged RK3 flow (uses self.action, self.grad, self.step)
    step = Loops.step          # unchanged U <- exp(X) U on free links (uses self.frozen)
    def __init__(self, L, eps, centre=None, nfix=NFIX):
        self.L, self.eps = L, eps; self.c1, self.c2 = coeffs(eps)
        self.Ns = L**4; self.NL = 4*self.Ns
        k = np.arange(L); c = (L//2 if centre is None else centre)
        self.centre = np.array([c]*4, float) if np.isscalar(c) else np.array(c, float)
        X = np.stack(np.meshgrid(k, k, k, k, indexing='ij'), -1).astype(float)   # (L,L,L,L,4)
        self.X = X
        lay = np.minimum(X, L-1-X).min(-1)                                      # site layer from the periodic seam
        fz = np.zeros((4, L, L, L, L), bool)
        for mu in range(4): fz[mu] = (lay < nfix) | (np.roll(lay, -1, axis=mu) < nfix)
        self.frozen = fz.reshape(-1)
        d = X - self.centre; self.dist = np.sqrt((d**2).sum(-1))
    # ---- layout ----
    def U4(self, U): return U.reshape(4, self.L, self.L, self.L, self.L, 4)
    @staticmethod
    def sh(A, mu, n): return np.roll(A, -n, axis=mu) if n else A      # A(x + n mu)
    def line(self, U4, mu, n):
        """Path product from x to x + n mu along mu."""
        P = U4[mu]
        for j in range(1, n): P = qmul(P, self.sh(U4[mu], mu, j))
        return P
    def squares(self, U4, mu, nu, s):
        """W_{mu nu}^{s x s}(x), lower-left corner x, path +mu, +nu, -mu, -nu."""
        Lm, Ln = self.line(U4, mu, s), self.line(U4, nu, s)
        return qmul(qmul(Lm, self.sh(Ln, mu, s)), qmul(qconj(self.sh(Lm, nu, s)), qconj(Ln)))
    def loops(self):
        out = [(1, self.c1)]
        if self.c2 != 0: out.append((2, self.c2))
        return out
    # ---- action ----
    def action(self, U, per_site=False):
        U4 = self.U4(U); S = 0.0; dens = np.zeros((self.L,)*4) if per_site else None
        for s, cs in self.loops():
            for mu in range(4):
                for nu in range(mu+1, 4):
                    val = cs*4*(1 - self.squares(U4, mu, nu, s)[..., 0]); S += float(val.sum())
                    if per_site:   # split over the 4 corners x, x+s mu, x+s mu+s nu, x+s nu
                        q = val/4
                        dens += q + np.roll(q, s, axis=mu) + np.roll(np.roll(q, s, axis=mu), s, axis=nu) + np.roll(q, s, axis=nu)
        return (S, dens.reshape(-1)) if per_site else S
    # ---- force ----
    def staple_sum(self, U4, mu):
        """sum_s c_s sum_{nu != mu} sum_{k<s} (up + down staples) for link U_mu(y): loop rotated to start at U_mu(y)."""
        tot = None
        for s, cs in self.loops():
            Lm = self.line(U4, mu, s)
            for nu in range(4):
                if nu == mu: continue
                Ln = self.line(U4, nu, s)
                for k in range(s):
                    rest = self.line(U4, mu, s-k-1) if s-k-1 > 0 else None   # L_mu^{s-k-1}(y+mu), shifted below
                    # up: corner x = y - k mu
                    x_up = lambda A: self.sh(A, mu, -k)
                    up = qmul(qmul(x_up(self.sh(Ln, mu, s)), qconj(x_up(self.sh(Lm, nu, s)))), qmul(qconj(x_up(Ln)), x_up(self.line(U4, mu, k)) if k else ident(U4.shape[1:-1])))
                    # down: corner x' = y - k mu - s nu
                    x_dn = lambda A: self.sh(self.sh(A, mu, -k), nu, -s)
                    dn = qmul(qmul(qconj(x_dn(self.sh(Ln, mu, s))), qconj(x_dn(Lm))), qmul(x_dn(Ln), x_dn(self.sh(self.line(U4, mu, k), nu, s)) if k else ident(U4.shape[1:-1])))
                    st = up + dn
                    if rest is not None: st = qmul(self.sh(rest, mu, 1), st)
                    tot = cs*st if tot is None else tot + cs*st
        return tot
    def grad(self, U):
        """dS/dtau for left variations U -> exp(tau) U (same convention as Loops.grad); frozen links zero."""
        U4 = self.U4(U); G = np.zeros((4,)+U4.shape[1:-1]+(3,))
        for mu in range(4): G[mu] = 4*qmul(U4[mu], self.staple_sum(U4, mu))[..., 1:]
        G = G.reshape(-1, 3); G[self.frozen] = 0; return G
    # ---- observables ----
    def rho_moment(self, U, rball=None, rmin=RMIN):
        """IT1b definition (Loops.rho_moment): sqrt(sum dens d^2 / sum dens / 2) over rmin <= d <= rball."""
        _, dens = self.action(U, per_site=True); d = self.dist.reshape(-1)
        rball = self.L/2-3 if rball is None else rball; m = (d >= rmin) & (d <= rball)
        return float(np.sqrt(np.sum(dens[m]*d[m]**2)/np.sum(dens[m])/2))
    def interior_action(self, U, rball=None):
        S, dens = self.action(U, per_site=True); d = self.dist.reshape(-1); rball = self.L/2-3 if rball is None else rball
        Si = float(dens[d <= rball].sum()); return dict(S=S, S_ball=Si, S_outside=S-Si, rball=rball)
    def charge(self, U):
        """Clover Q = (1/pi^2) sum_x (f12.f34 - f13.f24 + f14.f23), f = Im of the clover average (1/4 sum of 4 plaquettes);
        quaternion i_k ~ -i sigma_k so F^a = 2 f_k / a^2. Overall sign is convention-dependent: compare |Q| with 1."""
        U4 = self.U4(U); f = {}
        for mu in range(4):
            for nu in range(mu+1, 4):
                P = self.squares(U4, mu, nu, 1)   # leaf 1 of the 4 plaquettes meeting at x, all oriented mu->nu
                Um, Un = U4[mu], U4[nu]
                l1 = P
                l2 = qmul(qmul(Un, qconj(self.sh(self.sh(Um, nu, 1), mu, -1))), qmul(qconj(self.sh(Un, mu, -1)), self.sh(Um, mu, -1)))
                l3 = qmul(qmul(qconj(self.sh(Um, mu, -1)), qconj(self.sh(self.sh(Un, mu, -1), nu, -1))), qmul(self.sh(self.sh(Um, mu, -1), nu, -1), self.sh(Un, nu, -1)))
                l4 = qmul(qmul(qconj(self.sh(Un, nu, -1)), self.sh(Um, nu, -1)), qmul(self.sh(self.sh(Un, mu, 1), nu, -1), qconj(Um)))
                f[(mu, nu)] = ((l1 + l2 + l3 + l4)/4)[..., 1:]
        dot = lambda a, b: (f[a]*f[b]).sum(-1)
        return float((dot((0, 1), (2, 3)) - dot((0, 2), (1, 3)) + dot((0, 3), (1, 2))).sum()/np.pi**2)

# ---- singular-gauge BPST (same construction as lattice.Lattice.bpst_links, conv=(0,1), nsub midpoint P-ordering) ----
def bpst_links(hc, rho, nsub=16):
    """Regular-gauge holonomy along each link (A = Im(xbar dx)/(|x|^2+rho^2), P-ordered over nsub segments), then the
    singular-gauge rotation g(x) = x/|x| at both ends (g = 1 at the centre site, as in the polar code). Positions are the
    periodic-image coordinates nearest the centre, so every link is single-valued on T^4; links crossing the seam join
    images on opposite sides (their mismatch is the seam/boundary excess, frozen and reported)."""
    L = hc.L; c = hc.centre
    y = hc.X - c; y = (y + L/2) % L - L/2                      # nearest-image displacement in [-L/2, L/2)
    def gsite(v):
        n = np.linalg.norm(v, axis=-1, keepdims=True)
        return np.where(n > 1e-12, v/np.where(n > 1e-12, n, 1), np.array([1., 0, 0, 0]))
    U = np.empty((4,)+y.shape[:-1]+(4,))
    for mu in range(4):
        e = np.zeros(4); e[mu] = 1.0; H = None
        for s in range(nsub):
            xm = y + e*(s+0.5)/nsub; dx = e/nsub
            v = qmul(qconj(xm), np.broadcast_to(dx, xm.shape))[..., 1:]/(np.sum(xm**2, -1)+rho**2)[..., None]
            E = qexp_im(v); H = E if H is None else qmul(H, E)
        g0 = qconj(gsite(y)); g1 = qconj(gsite(np.roll(y, -1, axis=mu)))   # conv[1]==1: g -> conj(g)
        U[mu] = qmul(qmul(qconj(g0), H), g1)
    return U.reshape(-1, 4)

def bpst_tail(R, rho):
    """Continuum fraction of 8 pi^2 outside radius R (same formula as run.bpst_tail)."""
    return rho**4*(3*R**2+rho**2)/(R**2+rho**2)**3

def eq19(eps, rho):
    """NPB413 eq. (19): S(eps)/8pi^2 = 1 - (eps/5)(a/rho)^2 - ((15 eps - 12)/210)(a/rho)^4."""
    return 1 - (eps/5)/rho**2 - ((15*eps-12)/210)/rho**4

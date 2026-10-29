"""Flat-link loop kernels for the polar lattice (Aethon). Builds every loop of S(eps) as index
arrays so one code path gives: action, Lie-algebra gradient, RK3 gradient flow with target-rho stop,
clover F / Q, self-duality shells, Hessian-vector products with background gauge fixing, Lanczos,
and a seed bootstrap for the Richardson order error."""
import numpy as np
from lattice import Lattice, qmul, qconj, qexp_im, ident

class Loops:
    def __init__(self, lat, eps):
        self.lat, self.eps = lat, eps
        Mr, Lc, M3, M4, a, dth = lat.Mr, lat.Lc, lat.M3, lat.M4, lat.a, lat.dth
        self.Nn = Nn = 1 + Mr*Lc; self.Ns = Nn*M3*M4
        nr = Mr*Lc*M3*M4; nt = Nn*M3*M4
        self.off = dict(rad=0, ang=nr, d3=2*nr, d4=2*nr+nt); self.NL = 2*nr + 2*nt
        site = lambda node, k3, k4: (node*M3 + k3)*M4 + k4
        node = lambda n, j: 1 + n*Lc + (j % Lc)
        self.site = site; self.node = node
        R = lambda n, j, k3, k4: self.off['rad'] + ((n*Lc + j % Lc)*M3 + k3)*M4 + k4
        A = lambda n, j, k3, k4: self.off['ang'] + ((n*Lc + j % Lc)*M3 + k3)*M4 + k4
        D3 = lambda nd, k3, k4: self.off['d3'] + (nd*M3 + k3)*M4 + k4
        D4 = lambda nd, k3, k4: self.off['d4'] + (nd*M3 + k3)*M4 + k4
        # tails/heads
        tail = np.full(self.NL, -1, np.int64); head = np.full(self.NL, -1, np.int64)
        n_, j_, k3_, k4_ = np.meshgrid(np.arange(Mr), np.arange(Lc), np.arange(M3), np.arange(M4), indexing='ij')
        inner = np.where(n_ == 0, 0, node(n_-1, j_))
        tail[R(n_, j_, k3_, k4_)] = site(inner, k3_, k4_); head[R(n_, j_, k3_, k4_)] = site(node(n_, j_), k3_, k4_)
        tail[A(n_, j_, k3_, k4_)] = site(node(n_, j_), k3_, k4_); head[A(n_, j_, k3_, k4_)] = site(node(n_, j_+1), k3_, k4_)
        nd_, q3, q4 = np.meshgrid(np.arange(Nn), np.arange(M3), np.arange(M4), indexing='ij')
        ok3 = q3 < M3-1; ok4 = q4 < M4-1
        tail[D3(nd_, q3, q4)[ok3]] = site(nd_, q3, q4)[ok3]; head[D3(nd_, q3, q4)[ok3]] = site(nd_, q3+1, q4)[ok3]
        tail[D4(nd_, q3, q4)[ok4]] = site(nd_, q3, q4)[ok4]; head[D4(nd_, q3, q4)[ok4]] = site(nd_, q3, q4+1)[ok4]
        self.tail, self.head = tail, head
        # boundary sites: outer ring, transverse end sites
        nd_s, s3, s4 = np.meshgrid(np.arange(Nn), np.arange(M3), np.arange(M4), indexing='ij')
        ringn = np.where(nd_s == 0, -1, (nd_s-1)//Lc)
        self.bsite = ((ringn == Mr-1) | (s3 == 0) | (s3 == M3-1) | (s4 == 0) | (s4 == M4-1)).ravel()
        self.site_ring = ringn.ravel()  # -1 = tip
        self.site_x3 = lat.x3[s3].ravel(); self.site_x4 = lat.x4[s4].ravel()
        self.site_r = np.where(ringn < 0, 0.0, lat.r[np.clip(ringn, 0, None)]).ravel()
        self.site_th = np.where(nd_s == 0, 0.0, ((nd_s-1) % Lc)*dth).ravel()
        tipA, ringA = lat.dual_area()
        self.site_vol = np.where(ringn < 0, tipA, ringA[np.clip(ringn, 0, None)]).ravel()*a*a
        unused = tail < 0
        self.frozen = unused | (self.bsite[np.clip(tail, 0, None)] & self.bsite[np.clip(head, 0, None)])
        # ---------- loops ----------
        c11, c22 = (4-eps)/3, (eps-1)/48
        far = lambda n: n >= 2
        cls = []   # (ids (N,len), conj (len,), w (N,), plane, size, area (N,))
        def add(ids, conj, w, plane, size, area):
            ids = np.stack([np.broadcast_to(x, np.broadcast_shapes(*[np.shape(y) for y in ids])).ravel() for x in ids], 1)
            w = np.broadcast_to(w, ids.shape[:1]).astype(float); area = np.broadcast_to(area, ids.shape[:1]).astype(float)
            keep = w != 0
            if keep.any(): cls.append(dict(ids=ids[keep].astype(np.int64), conj=np.array(conj), w=w[keep], plane=plane, size=size, area=area[keep]))
        rr = lat.r; rdual = lat.radial_dual()
        J = np.arange(Lc)[:, None, None]
        for s in (1, 2):
            if s == 2 and c22 == 0: continue
            cs = (lambda nfar: (c11 if nfar else 1.0)) if s == 1 else (lambda nfar: c22)
            K3 = np.arange(M3-s)[None, :, None]; K4 = np.arange(M4-s)[None, None, :]
            # 34
            nodes = [(0, tipA, False)] if s == 1 else []
            for n in range(Mr):
                if s == 2 and not far(n): continue
                nodes.append((None, ringA[n], far(n), n))
            for item in nodes:
                if item[0] == 0: nd = np.array(0)[None, None, None]; area_d, isfar = item[1], False
                else: nd = node(item[3], J); area_d, isfar = item[1], item[2]
                ids = [D3(nd, K3+t, K4) for t in range(s)] + [D4(nd, K3+s, K4+t) for t in range(s)] + \
                      [D3(nd, K3+s-1-t, K4+s) for t in range(s)] + [D4(nd, K3, K4+s-1-t) for t in range(s)]
                add(ids, [0]*2*s+[1]*2*s, area_d/a**2*cs(isfar), '34', s, (s*a)**2)
            # r phi
            K3a = np.arange(M3)[None, :, None]; K4a = np.arange(M4)[None, None, :]
            for n in range(s, Mr):
                ni = n-s
                if s == 2 and ni < 2: continue
                Ar = 0.5*(rr[n]**2-rr[ni]**2)*s*lat.dth
                ids = [R(m, J, K3a, K4a) for m in range(ni+1, n+1)] + [A(n, J+t, K3a, K4a) for t in range(s)] + \
                      [R(m, J+s, K3a, K4a) for m in range(n, ni, -1)] + [A(ni, J+s-1-t, K3a, K4a) for t in range(s)]
                add(ids, [0]*2*s+[1]*2*s, a**2/(Ar/s**2)*cs(ni >= 2), 'rphi', s, Ar)
            if s == 1:
                At = 0.5*(a/2)**2*lat.dth
                add([R(0, J, K3a, K4a), A(0, J, K3a, K4a), R(0, J+1, K3a, K4a)], [0, 0, 1], a**2/At, 'rphi', 1, At)
            # r3 / r4
            rmid = np.concatenate([[a/4], 0.5*(rr[1:]+rr[:-1])]); Lrad = np.concatenate([[a/2], np.full(Mr-1, a)])
            for pl in ('r3', 'r4'):
                for n in range(s-1, Mr):
                    ni = n-s
                    if s == 2 and ni < 2: continue
                    innd = np.array(0)[None, None, None] if ni < 0 else node(ni, J)
                    if pl == 'r3':
                        KA, KB = np.arange(M3-s)[None, :, None], np.arange(M4)[None, None, :]
                        T = lambda nd, t: D3(nd, KA+t, KB); rs = lambda m, t: R(m, J, KA+t, KB)
                        Tb = lambda nd, t: D3(nd, KA+s-1-t, KB)
                    else:
                        KA, KB = np.arange(M3)[None, :, None], np.arange(M4-s)[None, None, :]
                        T = lambda nd, t: D4(nd, KA, KB+t); rs = lambda m, t: R(m, J, KA, KB+t)
                        Tb = lambda nd, t: D4(nd, KA, KB+s-1-t)
                    ids = [rs(m, 0) for m in range(ni+1, n+1)] + [T(node(n, J), t) for t in range(s)] + \
                          [rs(m, s) for m in range(n, ni, -1)] + [Tb(innd, t) for t in range(s)]
                    if s == 1: w = (rmid[n]*lat.dth)/Lrad[n]*cs(ni >= 2); area = Lrad[n]*a
                    else: w = (rr[n-1]*lat.dth)/a*c22; area = (2*a)**2
                    add(ids, [0]*2*s+[1]*2*s, w, pl, s, area)
            # phi3 / phi4
            for pl in ('phi3', 'phi4'):
                for n in range(Mr):
                    if s == 2 and not far(n): continue
                    if pl == 'phi3':
                        KA, KB = np.arange(M3-s)[None, :, None], np.arange(M4)[None, None, :]
                        Ap = lambda t, d: A(n, J+t, KA+d, KB); T = lambda jj, t: D3(node(n, jj), KA+t, KB); Tb = lambda jj, t: D3(node(n, jj), KA+s-1-t, KB)
                    else:
                        KA, KB = np.arange(M3)[None, :, None], np.arange(M4-s)[None, None, :]
                        Ap = lambda t, d: A(n, J+t, KA, KB+d); T = lambda jj, t: D4(node(n, jj), KA, KB+t); Tb = lambda jj, t: D4(node(n, jj), KA, KB+s-1-t)
                    ids = [Ap(t, 0) for t in range(s)] + [T(J+s, t) for t in range(s)] + \
                          [Ap(s-1-t, s) for t in range(s)] + [Tb(J, t) for t in range(s)]
                    w = rdual[n]/(rr[n]*lat.dth)*cs(far(n))
                    add(ids, [0]*2*s+[1]*2*s, w, pl, s, rr[n]*lat.dth*s*s*a)
        self.cls = cls
    # ---- conversion from Lattice dict layout ----
    def flat(self, L):
        lat = self.lat
        d3 = np.concatenate([L['tip3'][None], L['d3'].reshape(-1, lat.M3, lat.M4, 4)], 0)
        d4 = np.concatenate([L['tip4'][None], L['d4'].reshape(-1, lat.M3, lat.M4, 4)], 0)
        U = np.concatenate([L['rad'].reshape(-1, 4), L['ang'].reshape(-1, 4), d3.reshape(-1, 4), d4.reshape(-1, 4)], 0)
        U[self.frozen] = ident((int(self.frozen.sum()),))
        return U
    def _products(self, U, c):
        V = U[c['ids']]
        V = np.where(c['conj'][None, :, None], V*np.array([1, -1, -1, -1]), V)
        n = V.shape[1]; P = [None]*(n+1); P[0] = None
        pre = [ident((V.shape[0],))]
        for k in range(n): pre.append(qmul(pre[-1], V[:, k]))
        suf = [ident((V.shape[0],))]*(n+1)
        for k in range(n-1, -1, -1): suf[k] = qmul(V[:, k], suf[k+1])
        return V, pre, suf
    def action(self, U, per_site=False):
        S = 0.0; dens = np.zeros(self.Ns) if per_site else None
        for c in self.cls:
            V, pre, suf = self._products(U, c)
            val = c['w']*4*(1-pre[-1][:, 0]); S += val.sum()
            if per_site:
                corners = self.corners(c)
                for col in corners.T: np.add.at(dens, col, val/corners.shape[1])
        return (S, dens) if per_site else S
    def corners(self, c):
        n = c['ids'].shape[1]; s = c['size']
        pos = [0, 1, 2] if n == 3 else [0, s, 2*s, 3*s]
        out = []
        for p in pos:
            l = c['ids'][:, p]; out.append(np.where(c['conj'][p], self.head[l], self.tail[l]))
        return np.stack(out, 1)
    def grad(self, U):
        """dS/dtau for left variations U -> exp(tau)U, tau imaginary quaternion; frozen links zero."""
        G = np.zeros((self.NL, 3))
        for c in self.cls:
            V, pre, suf = self._products(U, c); n = V.shape[1]; w4 = 4*c['w'][:, None]
            for k in range(n):
                M = qmul(suf[k+1], pre[k]); Uk = U[c['ids'][:, k]]
                if not c['conj'][k]: g = w4*qmul(Uk, M)[:, 1:]
                else: g = -w4*qmul(M, qconj(Uk))[:, 1:]
                np.add.at(G, c['ids'][:, k], g)
        G[self.frozen] = 0; return G
    def step(self, U, X):  # U <- exp(X) U on free links
        E = qexp_im(X); E[self.frozen] = ident((int(self.frozen.sum()),)); out = qmul(E, U)
        return out/np.linalg.norm(out, axis=-1, keepdims=True)
    # ---- gradient flow (Luscher RK3), dU/dt = -grad S ----
    def flow(self, U, h=0.01, rho_target=None, centre=None, rho_fn=None, max_steps=100000, record=10):
        hist = []; t = 0.0; S_prev = self.action(U)
        for it in range(max_steps):
            if it and it % record == 0:
                S_now = self.action(U)
                if S_now > S_prev: raise FloatingPointError(f"flow unstable at h={h}: S rose {S_prev:.6g} -> {S_now:.6g}")
                S_prev = S_now
            if it % record == 0 or rho_target is not None:
                rho = rho_fn(U) if rho_fn else None; hist.append((t, rho))
                if rho_target is not None and rho is not None and rho >= rho_target: break
            Z0 = -h*self.grad(U); W1 = self.step(U, Z0/4)
            Z1 = -h*self.grad(W1); W2 = self.step(W1, 8/9*Z1-17/36*Z0)
            Z2 = -h*self.grad(W2); U = self.step(W2, 3/4*Z2-8/9*Z1+17/36*Z0); t += h
        return U, hist
    # ---- rho from action density second moment, r >= rmin only ----
    def rho_moment(self, U, centre=(0., 0., 0., 0.), rmin=2.0, alpha_embed=True):
        _, dens = self.action(U, per_site=True)
        r, th, x3, x4 = self.site_r, self.site_th, self.site_x3, self.site_x4
        cx, cy = centre[0], centre[1]; rc = np.hypot(cx, cy); thc = np.arctan2(cy, cx)
        dth = np.abs(((th-thc)+np.pi) % (2*np.pi) - np.pi)
        d2 = r**2+rc**2-2*r*rc*np.cos(dth) + (x3-centre[2])**2 + (x4-centre[3])**2
        m = (r >= rmin) & ~self.bsite
        return float(np.sqrt(np.sum(dens[m]*d2[m])/np.sum(dens[m])/2))   # BPST: <x^2> = 2 rho^2
    # ---- clover F in the (r, phi, 3, 4) frame, Q and self-duality ----
    PL = {'rphi': (0, 1), 'r3': (0, 2), 'r4': (0, 3), 'phi3': (1, 2), 'phi4': (1, 3), '34': (2, 3)}
    def field_strength(self, U):
        F = np.zeros((self.Ns, 4, 4, 3)); Asum = np.zeros((self.Ns, 4, 4))
        for c in self.cls:
            if c['size'] != 1: continue
            V, pre, suf = self._products(U, c); n = V.shape[1]; mu, nu = self.PL[c['plane']]
            cor = self.corners(c); pos = [0, 1, 2] if n == 3 else [0, 1, 2, 3]
            for i, p in enumerate(pos):
                Wk = qmul(suf[p], pre[p])[:, 1:]
                np.add.at(F[:, mu, nu], cor[:, i], Wk); np.add.at(Asum[:, mu, nu], cor[:, i], c['area'])
        with np.errstate(invalid='ignore', divide='ignore'):
            F = np.where(Asum[..., None] > 0, F/Asum[..., None], 0)
        F = F - np.swapaxes(F, 1, 2); return F
    def charge(self, U, F=None, mask=None):
        F = self.field_strength(U) if F is None else F
        q = (np.sum(F[:, 0, 1]*F[:, 2, 3], -1) - np.sum(F[:, 0, 2]*F[:, 1, 3], -1) + np.sum(F[:, 0, 3]*F[:, 1, 2], -1))
        m = np.ones(self.Ns, bool) if mask is None else mask
        return float(np.sum((self.site_vol*q)[m])/(2*np.pi**2))
    def selfduality(self, U, shells, F=None, sign=None):
        F = self.field_strength(U) if F is None else F
        sgn = np.sign(self.charge(U, F)) if sign is None else sign
        D = np.stack([F[:, 0, 1]-sgn*F[:, 2, 3], F[:, 0, 2]+sgn*F[:, 1, 3], F[:, 0, 3]-sgn*F[:, 1, 2]], 1)
        N = np.stack([F[:, i, j] for i, j in self.PL.values()], 1)
        out = {}
        for lo, hi in shells:
            m = (self.site_r >= lo) & (self.site_r < hi) & ~self.bsite
            num = np.sum(self.site_vol[m]*2*np.sum(D[m]**2, (1, 2))); den = np.sum(self.site_vol[m]*2*np.sum(N[m]**2, (1, 2)))
            out[(lo, hi)] = float(np.sqrt(num/den)) if den > 0 else None
        return out
    # ---- Hessian with background gauge fixing ----
    def free_index(self):
        fl = np.where(~self.frozen)[0]; gs = np.where(~self.bsite)[0]; return fl, gs
    def gauge_G(self, U, omega_sites):
        """tau_l = omega_tail - Ad_U(omega_head) on free links; omega on interior sites only."""
        om = np.zeros((self.Ns, 4)); om[:, 1:] = omega_sites
        fl = ~self.frozen; tl = np.clip(self.tail, 0, None); hd = np.clip(self.head, 0, None)
        X = np.zeros((self.NL, 3))
        Ad = qmul(qmul(U, om[hd]), qconj(U))[:, 1:]
        X[fl] = om[tl][fl, 1:] - Ad[fl]; return X
    def gauge_GT(self, U, X):
        out = np.zeros((self.Ns, 3)); fl = np.where(~self.frozen)[0]
        Xq = np.zeros((self.NL, 4)); Xq[:, 1:] = X
        np.add.at(out, self.tail[fl], X[fl])
        back = qmul(qmul(qconj(U[fl]), Xq[fl]), U[fl])[:, 1:]
        np.add.at(out, self.head[fl], -back); out[self.bsite] = 0; return out
    def hessian_op(self, U, lam=1.0, h=1e-4):
        fl = np.where(~self.frozen)[0]; n = 3*len(fl); g0 = self.grad(U)
        def mv(v):
            X = np.zeros((self.NL, 3)); X[fl] = v.reshape(-1, 3)
            gp = self.grad(self.step(U, h*X)); gm = self.grad(self.step(U, -h*X))
            Hv = (gp-gm)/(2*h) - np.cross(X, g0)   # symmetric (Riemannian) part; = H at a stationary point
            if lam: Hv = Hv + lam*self.gauge_G(U, self.gauge_GT(U, X))
            return Hv[fl].ravel()
        return n, mv
    def lanczos(self, U, k=30, lam=1.0, min_free_gb=3.3, free_fn=None, tol=1e-6):
        from scipy.sparse.linalg import LinearOperator, eigsh
        if free_fn is not None and free_fn() < min_free_gb: raise MemoryError("free RAM below guard")
        n, mv = self.hessian_op(U, lam); op = LinearOperator((n, n), matvec=mv, dtype=float)
        vals, vecs = eigsh(op, k=k, which='SA', tol=tol, ncv=max(2*k+1, 20)); o = np.argsort(vals)
        return vals[o], vecs[:, o]
    def tip_weight(self, vec, rmax=1.0):
        """fraction of |mode|^2 on links touching sites with r < rmax (tip-localised test)."""
        fl = np.where(~self.frozen)[0]; v2 = np.sum(vec.reshape(-1, 3)**2, 1)
        near = (self.site_r[self.tail[fl]] < rmax) | (self.site_r[self.head[fl]] < rmax)
        return float(v2[near].sum()/v2.sum())

def generic_seed(lat, rho, seed, stretch=0.15, noise=0.05, centre=(0., 0., 0., 0.)):
    """Generic smooth seed (NOT a BPST profile): BPST deformed by a random symmetric stretch of x
    and multiplied by smooth random link noise that vanishes on the faces. Singular gauge."""
    rng = np.random.default_rng(seed); M = np.eye(4) + stretch*rng.standard_normal((4, 4)); M = 0.5*(M+M.T)
    L = lat.bpst_links(rho, centre=centre, xform=M)
    lp = Loops(lat, 1); U = lp.flat(L)
    mid = 0.5*(np.c_[lp.site_r*np.cos(lp.site_th), lp.site_r*np.sin(lp.site_th), lp.site_x3, lp.site_x4][np.clip(lp.tail, 0, None)] +
               np.c_[lp.site_r*np.cos(lp.site_th), lp.site_r*np.sin(lp.site_th), lp.site_x3, lp.site_x4][np.clip(lp.head, 0, None)])
    k = rng.standard_normal((3, 3, 4))/max(rho, 1.0)
    ph = rng.uniform(0, 2*np.pi, (3, 3))
    X = np.zeros((lp.NL, 3))
    env = np.exp(-np.sum(mid**2, 1)/(2*(1.5*rho)**2))
    for a_ in range(3):
        for b in range(3): X[:, a_] += np.sin(mid@k[a_, b] + ph[a_, b])
    X *= noise*env[:, None]/3
    return lp.step(U, X)

def bootstrap_order(per_seed, a_vals, richardson, n_boot=2000, rng_seed=0):
    """per_seed: array (n_grids=3, n_seeds). Returns measured order on seed means and its bootstrap std."""
    per_seed = np.asarray(per_seed, float); rng = np.random.default_rng(rng_seed)
    base = richardson(per_seed.mean(1), a_vals)['order']; ps = []
    ns = per_seed.shape[1]
    for _ in range(n_boot):
        idx = rng.integers(0, ns, ns); p = richardson(per_seed[:, idx].mean(1), a_vals)['order']
        if p is not None: ps.append(p)
    frac = len(ps)/n_boot
    return dict(order=base, order_err=float(np.std(ps)) if len(ps) > 1 else None, valid_frac=frac)

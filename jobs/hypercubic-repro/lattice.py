"""Polar SU(2) lattice over C_alpha x R^2 (INSTANTON_TESTS rev 11).
Quaternion links (q0,q1,q2,q3); Tr U = 2 q0. Wilson normalisation beta=4 (g=1), so a
continuum BPST has S = 8 pi^2.
Geometry (spec l.12, l.14, l.70): one tip site at r=0 (no zero-length links), rings at
r=(n+1/2)a, n=0..M_r-1 (outermost ring = Dirichlet face), Lc=alpha*L_phi angular sites,
transverse sites x=(k-(M-1)/2)a with k=0 and k=M-1 the Dirichlet faces.
Action per plane: beta_munu*[(4-eps)/3 Tr(1-W11) + (eps-1)/48 Tr(1-W22)], 1x1-only
(Wilson weight 1) for loops touching r<2a, 2x2 only when every corner has r>=2a.
"""
import numpy as np

TWO_PI = 2*np.pi

def qmul(a, b):
    a0,a1,a2,a3 = a[...,0],a[...,1],a[...,2],a[...,3]
    b0,b1,b2,b3 = b[...,0],b[...,1],b[...,2],b[...,3]
    return np.stack([a0*b0-a1*b1-a2*b2-a3*b3, a0*b1+a1*b0+a2*b3-a3*b2,
                     a0*b2-a1*b3+a2*b0+a3*b1, a0*b3+a1*b2-a2*b1+a3*b0], -1)
def qconj(a):
    c = a.copy(); c[...,1:] *= -1; return c
def qexp_im(v):  # exp of imaginary quaternion v (...,3)
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    s = np.where(n > 0, np.sin(n)/np.where(n > 0, n, 1), 1.0)
    return np.concatenate([np.cos(n), v*s], -1)
def ident(shape):
    q = np.zeros(shape+(4,)); q[...,0] = 1; return q

class Lattice:
    def __init__(self, Mr, Lphi, M3, M4, alpha, a=1.0):
        self.Mr, self.Lphi, self.M3, self.M4, self.a = Mr, Lphi, M3, M4, a
        Lc = alpha*Lphi
        if abs(Lc-round(Lc)) > 1e-9: raise ValueError("alpha*L_phi not integer")
        self.Lc = int(round(Lc)); self.alpha = alpha
        self.dth = TWO_PI/Lphi
        self.r = (np.arange(Mr)+0.5)*a
        self.x3 = (np.arange(M3)-(M3-1)/2)*a; self.x4 = (np.arange(M4)-(M4-1)/2)*a
        self.n_sites = (1+Mr*self.Lc)*M3*M4
        self.n_sites_upper = Mr*Lphi*M3*M4
    # ring-0 radial dual extent [a/4, a]; tip disc r<a/4 (half the a/2 tip link) [build choice]
    def dual_area(self):  # 2D dual cell area per node, tip first then rings (per angular site)
        a, dth = self.a, self.dth
        ring = self.r*a*dth
        ring[0] = 0.5*(a**2-(a/4)**2)*dth
        tip = 0.5*(a/4)**2*TWO_PI*self.alpha
        return tip, ring
    def radial_dual(self):
        d = np.full(self.Mr, self.a); d[0] = 0.75*self.a; return d

    def positions(self):
        th = np.arange(self.Lc)*self.dth
        return th

    def bpst_links(self, rho, nsub=16, centre=(0.,0.,0.,0.), conv=(0,1), xform=None):
        """BPST (alpha=1 embedding only) in regular gauge A=Im(xbar dx)/(|x|^2+rho^2),
        P-ordered product over nsub midpoint segments, then gauge-rotated to singular gauge
        g(x)=x/|x| at sites so far links -> 1; Dirichlet face links then set to identity."""
        # alpha<1: cone-mapped seed, pullback of the flat BPST by theta -> theta/alpha (smooth, closes across the
        # glued wedge; NOT a solution on C_alpha). alpha=1 is the exact BPST.
        amap = 1.0/self.alpha
        c = np.array(centre)
        th = self.positions(); r = self.r
        X3, X4 = np.meshgrid(self.x3, self.x4, indexing='ij')
        def link(p0, p1, path):  # path(t)->point, p arrays broadcast (...,4)
            U = None
            for s in range(nsub):
                t0, t1 = s/nsub, (s+1)/nsub
                xa, xb = path(t0), path(t1)
                xm = path(0.5*(t0+t1)) - c
                dx = xb - xa
                if xform is not None: xm = xm@xform.T; dx = dx@xform.T
                v = (qmul(qconj(xm), dx) if conv[0]==0 else qmul(xm, qconj(dx)))[...,1:]/(np.sum(xm**2,-1)+rho**2)[...,None]
                e = qexp_im(v)
                U = e if U is None else qmul(U, e)
            return U
        def gsite(x):
            y = x - c
            if xform is not None: y = y@xform.T
            n = np.linalg.norm(y, axis=-1, keepdims=True)
            # at the centre site (tip-site row) the singular-gauge rotation is undefined; any single-site
            # gauge choice leaves the action invariant, so take g = 1 there. Links touching the centre are
            # the exact (regular-gauge, smooth) path-ordered holonomies, converged in nsub.
            return np.where(n > 1e-12, y/np.where(n > 1e-12, n, 1), np.array([1., 0, 0, 0]))
        def gauge(U, x0, x1):  # U' = g(x0)^-1 U g(x1)  (singular-gauge rotation)
            g0, g1 = gsite(x0), gsite(x1)
            if conv[1]==1: g0, g1 = qconj(g0), qconj(g1)
            return qmul(qmul(qconj(g0), U), g1) if conv[1] in (0,1) else qmul(qmul(g0, U), qconj(g1))
        def pt(rr, tt, x3, x4):
            return np.stack(np.broadcast_arrays(rr*np.cos(tt*amap), rr*np.sin(tt*amap), x3, x4), -1)
        R = r[:,None,None,None]; T = th[None,:,None,None]
        x3 = X3[None,None]; x4 = X4[None,None]
        # radial links: inner radius (tip 0 for n=0) -> r_n
        rin = np.concatenate([[0.], r[:-1]])[:,None,None,None]
        pr = lambda t: pt(rin+(R-rin)*t, T, x3, x4)
        Ur = gauge(link(None,None,pr), pr(0.), pr(1.))
        pa = lambda t: pt(R, T+self.dth*t, x3, x4)
        Ua = gauge(link(None,None,pa), pa(0.), pa(1.))
        p3 = lambda t: pt(R, T, x3+self.a*t, x4)
        U3 = gauge(link(None,None,p3), p3(0.), p3(1.))
        p4 = lambda t: pt(R, T, x3, x4+self.a*t)
        U4 = gauge(link(None,None,p4), p4(0.), p4(1.))
        t3 = lambda t: pt(0., 0., X3+self.a*t, X4)
        T3 = gauge(link(None,None,t3), t3(0.), t3(1.))
        t4 = lambda t: pt(0., 0., X3, X4+self.a*t)
        T4 = gauge(link(None,None,t4), t4(0.), t4(1.))
        L = dict(rad=Ur, ang=Ua, d3=U3, d4=U4, tip3=T3, tip4=T4)
        self.face_dev = self.apply_dirichlet(L)
        return L

    def apply_dirichlet(self, L):
        """Identity on links lying in an outer face (outer ring, x3/x4 end sites); returns
        max |1-q0| removed (size of the truncation, report-only)."""
        dev = 0.0
        def setid(arr, idx):
            nonlocal dev
            sub = arr[idx]; dev = max(dev, float(np.max(1-sub[...,0])) if sub.size else 0.)
            arr[idx] = ident(sub.shape[:-1])
        f = self.Mr-1
        setid(L['ang'], (f,)); setid(L['d3'], (f,)); setid(L['d4'], (f,))
        for k in (0, self.M3-1):
            setid(L['rad'], (slice(None),slice(None),k)); setid(L['ang'], (slice(None),slice(None),k))
            setid(L['d4'], (slice(None),slice(None),k)); setid(L['tip4'], (k,))
        for k in (0, self.M4-1):
            setid(L['rad'], (slice(None),slice(None),slice(None),k)); setid(L['ang'], (slice(None),slice(None),slice(None),k))
            setid(L['d3'], (slice(None),slice(None),slice(None),k)); setid(L['tip3'], (slice(None),k))
        # the last d3 link index (k=M3-1) leaves the box: identity, unused
        setid(L['d3'], (slice(None),slice(None),self.M3-1)); setid(L['tip3'], (self.M3-1,))
        setid(L['d4'], (slice(None),slice(None),slice(None),self.M4-1)); setid(L['tip4'], (slice(None),self.M4-1))
        return dev

    def action(self, L, eps, per_node=False):
        """Total S(eps) and per-ring/tip node shares (each loop split equally over its corners'
        2D nodes). Returns dict."""
        a, dth, Mr, Lc = self.a, self.dth, self.Mr, self.Lc
        c11 = (4-eps)/3; c22 = (eps-1)/48
        ring_share = np.zeros(Mr); tip_share = 0.0
        S_by_plane = {}
        roll = lambda A, s, ax: np.roll(A, -s, axis=ax)
        def tr1m(W): return 4*(1-W[...,0])   # beta=4 Wilson normalisation: 2 Tr(1-W)
        rad, ang, d3, d4, tip3, tip4 = (L[k] for k in ('rad','ang','d3','d4','tip3','tip4'))
        far = np.arange(Mr) >= 2       # ring r=(n+1/2)a >= 2a  <=> n>=2
        def add(name, val):
            S_by_plane[name] = S_by_plane.get(name, 0.0) + float(np.sum(val))
        # ---- 34 plane at rings: W = d3(x) d4(x+3) d3(x+4)^-1 d4(x)^-1
        def p34(A3, A4, s):
            # A arrays (..., M3, M4, 4); loop size s
            M3, M4 = A3.shape[-3], A3.shape[-2]
            def path(A, ax, start3, start4, n):
                U = None
                for t in range(n):
                    i3 = start3 + (t if ax == 3 else 0); i4 = start4 + (t if ax == 4 else 0)
                    seg = A[..., i3:i3+M3-s, i4:i4+M4-s, :]
                    U = seg if U is None else qmul(U, seg)
                return U
            W = qmul(qmul(path(A3,3,0,0,s), path(A4,4,s,0,s)), qconj(qmul(path(A4,4,0,0,s), path(A3,3,0,s,s))))
            return tr1m(W)
        _, ring_area = self.dual_area(); tip_area = self.dual_area()[0]
        w34 = ring_area/a**2
        coef1 = np.where(far, c11, 1.0)
        v = p34(d3, d4, 1)*(w34*coef1)[:,None,None,None]
        add('34', v); ring_share += v.sum(axis=(1,2,3))
        if c22 != 0:
            v = p34(d3[far], d4[far], 2)*(w34[far]*c22)[:,None,None,None]
            add('34', v); ring_share[far] += v.sum(axis=(1,2,3))
        v = p34(tip3, tip4, 1)*(tip_area/a**2); add('34', v); tip_share += float(v.sum())
        # ---- r phi plane: trapezoid between ring n-1 and n (n>=1)
        rr = self.r
        for s in (1, 2):
            cc = c11 if s == 1 else c22
            if s == 2 and c22 == 0: continue
            for n in range(s, Mr):
                ninner = n - s
                if s == 2 and ninner < 2: continue
                # radial path at angle j from ninner to n: product rad[ninner+1..n]
                def radpath(jshift):
                    U = None
                    for m in range(ninner+1, n+1):
                        seg = roll(rad[m], jshift, 0)
                        U = seg if U is None else qmul(U, seg)
                    return U
                def angpath(ring):
                    U = None
                    for t in range(s):
                        seg = roll(ang[ring], t, 0)
                        U = seg if U is None else qmul(U, seg)
                    return U
                W = qmul(qmul(radpath(0), angpath(n)), qconj(qmul(angpath(ninner), radpath(s))))
                A = 0.5*(rr[n]**2-rr[ninner]**2)*s*dth
                w = a**2/(A/(s*s))
                coef = cc if (s == 2 or ninner >= 2) else (1.0 if s == 1 else 0)
                if s == 1 and ninner >= 2: coef = c11
                v = tr1m(W)*w*coef
                add('rphi', v); share = v.sum()/2
                ring_share[n] += share; ring_share[ninner] += share
            # tip triangles (1x1 only)
        Wt = qmul(qmul(rad[0], ang[0]), qconj(roll(rad[0], 1, 0)))
        At = 0.5*(a/2)**2*dth
        v = tr1m(Wt)*(a**2/At); add('rphi', v)
        tip_share += float(v.sum())/3; ring_share[0] += float(v.sum())*2/3
        # ---- r3, r4 planes: radial step x transverse step
        rmid_rad = np.concatenate([[a/4], 0.5*(rr[1:]+rr[:-1])])
        Lrad = np.concatenate([[a/2], np.full(Mr-1, a)])
        for name, D, T, ax in (('r3', d3, tip3, 2), ('r4', d4, tip4, 3)):
            for s in (1, 2):
                if s == 2 and c22 == 0: continue
                for n in range(s-1, Mr):
                    ninner = n - s  # -1 = tip
                    if s == 2 and ninner < 2: continue
                    if s == 1 and n == 0:
                        inner = np.broadcast_to(T[None], D[0].shape)
                    else:
                        inner = D[ninner]
                    R0 = None
                    for m in range(ninner+1, n+1):
                        R0 = rad[m] if R0 is None else qmul(R0, rad[m])
                    def tpath(A):
                        U = None
                        for t in range(s):
                            seg = np.roll(A, -t, axis=ax-1)
                            U = seg if U is None else qmul(U, seg)
                        return U
                    W = qmul(qmul(R0, tpath(D[n])), qconj(qmul(tpath(inner), np.roll(R0, -s, axis=ax-1))))
                    # drop wrapped transverse loops (np.roll wrap): zero the last s slices
                    val = tr1m(W)
                    sl = [slice(None)]*3; sl[ax-1] = slice(D.shape[ax]-s, None); val[tuple(sl)] = 0
                    if s == 1:
                        w = (rmid_rad[n]*dth)/Lrad[n]
                        coef = c11 if ninner >= 2 else 1.0
                    else:
                        w = (rr[n-1]*dth)/a; coef = c22
                    v = val*w*coef; add(name, v)
                    sh = float(v.sum())/2; ring_share[n] += sh
                    if ninner >= 0: ring_share[ninner] += sh
                    else: tip_share += sh
        # ---- phi3, phi4 planes
        rdual = self.radial_dual()
        for name, D, ax in (('phi3', d3, 2), ('phi4', d4, 3)):
            for s in (1, 2):
                if s == 2 and c22 == 0: continue
                rows = np.arange(Mr) if s == 1 else np.where(far)[0]
                for n in rows:
                    def apath(): 
                        U = None
                        for t in range(s):
                            seg = np.roll(ang[n], -t, axis=0)
                            U = seg if U is None else qmul(U, seg)
                        return U
                    def tpath(A):
                        U = None
                        for t in range(s):
                            seg = np.roll(A, -t, axis=ax-1)
                            U = seg if U is None else qmul(U, seg)
                        return U
                    Ap = apath()
                    W = qmul(qmul(Ap, tpath(np.roll(D[n], -s, axis=0))), qconj(qmul(tpath(D[n]), np.roll(Ap, -s, axis=ax-1))))
                    val = tr1m(W)
                    sl = [slice(None)]*3; sl[ax-1] = slice(D.shape[ax]-s, None); val[tuple(sl)] = 0
                    w = rdual[n]/(rr[n]*dth)
                    coef = (c11 if far[n] else 1.0) if s == 1 else c22
                    v = val*w*coef; add(name, v); ring_share[n] += float(v.sum())
        tot = sum(S_by_plane.values())
        return dict(S=tot, planes=S_by_plane, ring=ring_share, tip=tip_share)

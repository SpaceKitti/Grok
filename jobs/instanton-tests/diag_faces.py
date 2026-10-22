"""Scratch (H5) face diagnosis: identity-face jump vs physics vs bug. Writes out/diag_faces.json"""
import json, sys, numpy as np, run
from lattice import Lattice, qmul, qconj, qexp_im
S8 = 8*np.pi**2; out = {}
def polar(name, rho):
    lat = Lattice(*run.BOXES[name], alpha=1.0); L = lat.bpst_links(rho); fd = lat.face_dev
    Sd = lat.action(L, 1)['S']; lat.apply_dirichlet = lambda L: 0.0; Ln = lat.bpst_links(rho)
    Sn = lat.action(Ln, 1)['S']; ct, cr = run.continuum_shares(lat, rho)
    return dict(S_dirichlet=Sd/S8, S_no_face_reset=Sn/S8, S_cont_in_box=(ct+cr.sum())/S8, face_jump=(Sd-Sn)/S8,
                lattice_minus_cont_noface=(Sn-S8*0)/S8-(ct+cr.sum())/S8, max_face_link_1mq0=fd, ell=float(lat.r[-1]))
def cart(half, a, rho, nsub=16):
    x = np.arange(-half+a/2, half, a); N = len(x); X = np.stack(np.meshgrid(x, x, x, x, indexing='ij'), -1)
    def link(mu):
        e = np.zeros(4); e[mu] = a; U = None
        for s in range(nsub):
            xm = X + e*(s+0.5)/nsub; v = qmul(qconj(xm), np.broadcast_to(e/nsub, xm.shape))[..., 1:]/(np.sum(xm**2, -1)+rho**2)[..., None]
            E = qexp_im(v); U = E if U is None else qmul(U, E)
        g = lambda y: y/np.linalg.norm(y, axis=-1, keepdims=True)
        return qmul(qmul(qconj(qconj(g(X))), U), qconj(g(X+e)))
    Us = [link(m) for m in range(4)]
    def S(Us):
        tot = 0.0
        for m in range(4):
            for n in range(m+1, 4):
                A = Us[m]; B = np.roll(Us[n], -1, m); C = np.roll(Us[m], -1, n); D = Us[n]
                W = qmul(qmul(A, B), qconj(qmul(D, C))); v = 4*(1-W[..., 0])
                sl = [slice(None)]*4; sl[m] = slice(0, N-1); sl[n] = slice(0, N-1); tot += v[tuple(sl)].sum()
        return tot
    Sn = S(Us); fd = 0.0
    Ud = [u.copy() for u in Us]
    for m in range(4):
        for f in range(4):
            if f == m: continue
            for k in (0, N-1):
                sl = [slice(None)]*4; sl[f] = k; fd = max(fd, float(np.max(1-Ud[m][tuple(sl)][..., 0]))); Ud[m][tuple(sl)] = [1, 0, 0, 0]
    Sd = S(Ud)
    hb = half-a/2; G, W = np.polynomial.legendre.leggauss(40); xs = hb*G; ws = hb*W
    R2 = sum(np.meshgrid(*(xs**2,)*4, indexing='ij')); wt = np.einsum('i,j,k,l->ijkl', ws, ws, ws, ws)
    Sc = float(np.sum(wt*run.bpst_density(R2, rho)))
    return dict(a=a, half=half, S_dirichlet=Sd/S8, S_no_face_reset=Sn/S8, S_cont_in_box=Sc/S8, face_jump=(Sd-Sn)/S8, max_face_link_1mq0=fd)
which = sys.argv[1]
if which == "polar":
    for name in ("B10", "B12", "B16", "B20"):
        out[name] = {str(r): polar(name, r) for r in (2.9, 3.0, 3.1)}; print(name, out[name]["3.0"], flush=True)
else:
    for a in (1.0, 0.5): out[f"cart_a{a}"] = {str(r): cart(8.0, a, r) for r in (2.9, 3.0, 3.1)}; print(a, out[f"cart_a{a}"]["3.0"], flush=True)
json.dump(out, open(f"out/diag_faces_{which}.json", "w"), indent=1, default=float)

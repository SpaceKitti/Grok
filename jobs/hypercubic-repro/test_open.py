"""Tests for hc_open (open box, clamp geometry). G0_open_full (L=24) is defined here and run by run_B1.py."""
import sys, re, time, numpy as np, hc_open as O, hc_kernel as H
from test_hc import rand_links, q2m

def wilson_ref_open(U, L):
    """Independent plain Wilson on the open box: complex 2x2 matrices, explicit loops, skip any loop leaving 0..L-1."""
    M = q2m(U).reshape(4, L, L, L, L, 2, 2); S = 0.0; G = np.zeros((4, L, L, L, L, 3))
    inb = lambda x: np.all((x >= 0) & (x <= L-1))
    def at(mu, x): return M[(mu,)+tuple(x)]
    def e(m): v = np.zeros(4, int); v[m] = 1; return v
    dag = lambda A: A.conj().T
    pauli = [np.array([[0, -1j], [-1j, 0]]), np.array([[0, -1], [1, 0]]), np.array([[-1j, 0], [0, 1j]])]
    for x in np.indices((L,)*4).reshape(4, -1).T:
        for mu in range(4):
            for nu in range(mu+1, 4):
                if inb(x+e(mu)+e(nu)):
                    P = at(mu, x) @ at(nu, x+e(mu)) @ dag(at(mu, x+e(nu))) @ dag(at(nu, x)); S += 2*(2 - np.trace(P).real)
        for mu in range(4):
            if not inb(x+e(mu)): continue
            St = np.zeros((2, 2), complex)
            for nu in range(4):
                if nu == mu: continue
                if inb(x+e(mu)+e(nu)): St += at(nu, x+e(mu)) @ dag(at(mu, x+e(nu))) @ dag(at(nu, x))
                if inb(x-e(nu)) and inb(x+e(mu)-e(nu)): St += dag(at(nu, x+e(mu)-e(nu))) @ dag(at(mu, x-e(nu))) @ at(nu, x-e(nu))
            W = at(mu, x) @ St; G[(mu,)+tuple(x)] = [-2*np.trace(T @ W).real for T in pauli]
    return S, G.reshape(-1, 3)

def G0_open_full(L=24, seed=3):
    U = rand_links(L, seed); hc = O.HCOpen(L, 1, nfix=0); S, G = wilson_ref_open(U, L)
    m = ~hc.dummy; dS = abs(hc.action(U)-S)/abs(S); dG = float(np.max(np.abs(hc.grad(U)[m]-G[m])))
    return dict(dS=dS, dG=dG, ok=bool(dS < 1e-12 and dG < 1e-12))
def test_open_wilson_match_L4():
    r = G0_open_full(4, 1); assert r['ok'], r
def test_open_wilson_match_L5():
    r = G0_open_full(5, 2); assert r['ok'], r
def _fd(eps, L=7, seed=2):
    U = rand_links(L, seed, 0.4); hc = O.HCOpen(L, eps, nfix=1); g = hc.grad(U)
    X = np.random.default_rng(9).standard_normal((hc.NL, 3)); X[hc.frozen] = 0
    h = 1e-5; fd = (hc.action(hc.step(U, h*X)) - hc.action(hc.step(U, -h*X)))/(2*h); return fd, float(np.sum(g*X))
def test_open_fd_eps_m1():
    fd, an = _fd(-1); assert abs(fd-an) < 1e-6*abs(an), (fd, an)
def test_open_fd_eps_1():
    fd, an = _fd(1); assert abs(fd-an) < 1e-6*abs(an), (fd, an)
def test_open_fd_eps_m1_noclamp_L6():
    U = rand_links(6, 5, 0.4); hc = O.HCOpen(6, -1, nfix=0); g = hc.grad(U); X = np.random.default_rng(3).standard_normal((hc.NL, 3)); X[hc.dummy] = 0
    h = 1e-5; fd = (hc.action(hc.step(U, h*X)) - hc.action(hc.step(U, -h*X)))/(2*h); assert abs(fd-np.sum(g*X)) < 1e-6*abs(fd)
def test_no_wrap_dummy_links_irrelevant():
    L = 6; U = rand_links(L, 4); hc = O.HCOpen(L, -1); S0 = hc.action(U); V = U.copy(); V[hc.dummy] = rand_links(L, 8)[hc.dummy]
    assert abs(hc.action(V) - S0) < 1e-12*S0 and np.allclose(hc.grad(V)[~hc.frozen], hc.grad(U)[~hc.frozen], atol=1e-12)
def test_no_wrap_far_faces_decoupled():
    """Changing links at x_0 = 0 must not change any loop touching x_0 = L-1 only (no wrap)."""
    L = 6; U = rand_links(L, 4); hc = O.HCOpen(L, -1); _, d0 = hc.action(U, per_site=True)
    V = U.copy(); m = (hc.X[..., 0] == 0)[None].repeat(4, 0).reshape(-1); V[m] = rand_links(L, 11)[m]
    _, d1 = hc.action(V, per_site=True); far = (hc.X[..., 0] >= 3).reshape(-1); assert np.allclose(d0[far], d1[far], atol=1e-13)
def test_open_loop_count():
    L = 6; hc = O.HCOpen(L, -1); U = np.zeros((hc.NL, 4)); U[:, 0] = 1
    n1 = sum(hc.valid(m, n, 1).sum() for m in range(4) for n in range(m+1, 4)); n2 = sum(hc.valid(m, n, 2).sum() for m in range(4) for n in range(m+1, 4))
    assert n1 == 6*L**2*(L-1)**2 and n2 == 6*L**2*(L-2)**2
def test_clamp_geometry_L24():
    L = 24; hc = O.HCOpen(L, -1); C = hc.clamp.reshape(4, L, L, L, L); D = hc.dummy.reshape(4, L, L, L, L)
    assert C[0, 0, 12, 12, 12] and C[0, 1, 12, 12, 12] and not C[0, 2, 12, 12, 12] and C[0, 21, 12, 12, 12] and not C[0, 20, 12, 12, 12]
    assert D[0, 23, 12, 12, 12] and not C[0, 23, 12, 12, 12] and C[1, 12, 0, 12, 12] and C[0, 12, 12, 12, 1] and not C[1, 12, 12, 12, 12]
    inner = (hc.layer >= 3); assert not np.any(hc.frozen.reshape(4, L, L, L, L)[:, inner])   # every link from a layer>=3 site is free
    assert np.allclose(hc.centre, 11.5) and hc.dist.reshape(L, L, L, L)[hc.layer < 2].min() > 9   # ball |x|<=9 never touches clamp
def test_clamp_never_moves():
    L = 7; hc = O.HCOpen(L, -1, nfix=1); U = rand_links(L, 3, 0.3); U2, _ = hc.flow(U, h=0.01, max_steps=2, record=10**9)
    assert np.abs(U2[hc.frozen] - U[hc.frozen]).max() < 1e-15   # Loops.step renormalises every link: clamp may move by 1 ulp
    assert not np.array_equal(U2[~hc.frozen], U[~hc.frozen])
def test_regular_bpst_su2_and_smooth():
    hc = O.HCOpen(10, 1); U = O.bpst_regular(hc, 2.0, nsub=8); assert np.allclose(np.linalg.norm(U, axis=-1), 1, atol=1e-12)
    assert np.all(U[hc.dummy] == [1, 0, 0, 0])
def test_continuum_density_normalisation():
    r = np.linspace(0, 400, 400001); f = O.continuum_density(r, 3.0)*2*np.pi**2*r**3; I = np.sum((f[1:]+f[:-1])/2)*(r[1]-r[0])
    assert abs(I/(8*np.pi**2) - 1) < 1e-6 and abs(1 - np.sum(((f[1:]+f[:-1])/2*(r[1]-r[0]))[r[1:] <= 9])/(8*np.pi**2) - H.bpst_tail(9, 3.0)) < 1e-4
def test_clamp_loop_mask():
    L = 7; hc = O.HCOpen(L, -1, nfix=1); U = rand_links(L, 1); lm = hc.clamp_loop_mask(U)
    Sc = hc.action(U, loop_mask=lm); Sf = hc.action(U, loop_mask=lambda m, n, s: 1 - lm(m, n, s)); assert abs(Sc + Sf - hc.action(U)) < 1e-9
    V = U.copy(); V[hc.clamp] = rand_links(L, 2)[hc.clamp]; assert abs(hc.action(V, loop_mask=lambda m, n, s: 1 - lm(m, n, s)) - Sf) < 1e-12
def test_interior_Q_normalisation_smooth_selfdual():
    """Wide BPST (rho=6a, L=20): |Q_ball| must match S_ball/8pi^2 (self-duality) within 3%; regular-gauge orientation gives Q<0."""
    hc = O.HCOpen(20, 1); U = O.bpst_regular(hc, 6.0); _, dens = hc.action(U, per_site=True); rb = 5.0
    Sb = dens[hc.dist.reshape(-1) <= rb].sum()/(8*np.pi**2); Q = hc.interior_charge(U, rb); assert Q < 0 and abs(-Q/Sb - 1) < 0.03, (Q, Sb)
def test_no_placeholders():
    for f in ("hc_open.py", "test_open.py"):
        src = open(f).read().replace("no_place" + "holders", ""); assert not re.search(r"\b(TO" + r"DO|FIX" + r"ME|XX" + r"X|NotImpl" + r"emented)\b|place" + "holder|if " + "False", src), f

if __name__ == "__main__":
    n = f = 0
    for k, v in sorted(globals().items()):
        if k.startswith("test_") and callable(v):
            n += 1; t0 = time.time()
            try: v(); print("PASS", k, f"{time.time()-t0:.1f}s")
            except Exception as e: f += 1; print("FAIL", k, repr(e))
    print(f"OPEN TESTS {n-f}/{n} passed"); sys.exit(1 if f else 0)

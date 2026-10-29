"""Small tests for hc_kernel (plain loop runner at the bottom). G0 (full L=24) is written here but NOT run by default."""
import sys, re, time, numpy as np, hc_kernel as H
from lattice import qmul, qconj, qexp_im

def rand_links(L, seed=0, amp=0.6):
    r = np.random.default_rng(seed); return qexp_im(amp*r.standard_normal((4*L**4, 3)))

# independent plain Wilson reference: complex 2x2 matrices, explicit site loops via index arithmetic (no quaternions, no rolls)
def q2m(q):
    a, b, c, d = q[..., 0], q[..., 1], q[..., 2], q[..., 3]
    return np.stack([np.stack([a-1j*d, -c-1j*b], -1), np.stack([c-1j*b, a+1j*d], -1)], -2)   # i,j,k -> -i sigma_1,2,3
def wilson_ref(U, L):
    M = q2m(U).reshape(4, L, L, L, L, 2, 2); S = 0.0; G = np.zeros((4, L, L, L, L, 3))
    idx = np.indices((L,)*4).reshape(4, -1).T
    def at(mu, x): return M[(mu,)+tuple(x % L)]
    def e(m): v = np.zeros(4, int); v[m] = 1; return v
    dag = lambda A: A.conj().T
    pauli = [np.array([[0, -1j], [-1j, 0]]), np.array([[0, -1], [1, 0]]), np.array([[-1j, 0], [0, 1j]])]   # q2m images of i, j, k
    for x in idx:
        for mu in range(4):
            for nu in range(mu+1, 4):
                P = at(mu, x) @ at(nu, x+e(mu)) @ dag(at(mu, x+e(nu))) @ dag(at(nu, x))
                S += 2*(2 - np.trace(P).real)          # 4(1-q0) = 2(2 - Re Tr P)
        for mu in range(4):
            St = np.zeros((2, 2), complex)
            for nu in range(4):
                if nu == mu: continue
                St += at(nu, x+e(mu)) @ dag(at(mu, x+e(nu))) @ dag(at(nu, x))
                St += dag(at(nu, x+e(mu)-e(nu))) @ dag(at(mu, x-e(nu))) @ at(nu, x-e(nu))
            W = at(mu, x) @ St
            # dS/dtau_k for U -> exp(tau_k i_k) U: d/dtau [-2 Re Tr(e^{tau T_k} W)] = -2 Re Tr(T_k W)
            G[(mu,)+tuple(x)] = [-2*np.trace(T @ W).real for T in pauli]
    return S, G.reshape(-1, 3)

def test_q2m_homomorphism():
    r = np.random.default_rng(0); a, b = r.standard_normal((2, 7, 4)); assert np.abs(q2m(qmul(a, b)) - q2m(a) @ q2m(b)).max() < 1e-13
def test_coeffs_normalisation():
    for e in (1, 0, -1): c1, c2 = H.coeffs(e); assert abs(c1 + 16*c2 - 1) < 1e-15
    assert H.coeffs(-1) == (5/3, -1/24) and H.coeffs(1) == (1.0, 0.0)
def test_coeffs_same_as_polar_code():
    assert "c11, c22 = (4-eps)/3, (eps-1)/48" in open("kernels.py").read() and "c11 = (4-eps)/3; c22 = (eps-1)/48" in open("lattice.py").read()
def test_flow_step_reused_unchanged():
    from kernels import Loops
    assert H.HCLoops.flow is Loops.flow and H.HCLoops.step is Loops.step
def test_wilson_match_L4():
    L = 4; U = rand_links(L, 1); hc = H.HCLoops(L, 1, nfix=0); S, G = wilson_ref(U, L)
    assert abs(hc.action(U) - S) < 1e-12*max(1, abs(S)) and np.max(np.abs(hc.grad(U) - G)) < 1e-12
def G0_full(L=24, seed=3):
    """G0: eps=1 action and force vs plain Wilson to 1e-12 on the full lattice (slow; run only when G0 is authorised)."""
    U = rand_links(L, seed); hc = H.HCLoops(L, 1, nfix=0); S, G = wilson_ref(U, L)
    return dict(dS=abs(hc.action(U)-S)/abs(S), dG=float(np.max(np.abs(hc.grad(U)-G))), ok=bool(abs(hc.action(U)-S)/abs(S) < 1e-12 and np.max(np.abs(hc.grad(U)-G)) < 1e-12))
def _fd(eps, L=6, seed=2):
    U = rand_links(L, seed, 0.4); hc = H.HCLoops(L, eps); g = hc.grad(U)
    r = np.random.default_rng(9); X = r.standard_normal((hc.NL, 3)); X[hc.frozen] = 0
    h = 1e-5; Sp = hc.action(hc.step(U, h*X)); Sm = hc.action(hc.step(U, -h*X))
    return (Sp-Sm)/(2*h), float(np.sum(g*X))
def test_fd_gradient_eps_m1_L6():
    fd, an = _fd(-1); assert abs(fd-an) < 1e-6*abs(an)
def test_fd_gradient_eps_1_L6():
    fd, an = _fd(1); assert abs(fd-an) < 1e-6*abs(an)
def test_fd_gradient_eps_0_L6_no_freeze():
    U = rand_links(6, 4, 0.4); hc = H.HCLoops(6, 0, nfix=0); g = hc.grad(U); X = np.random.default_rng(5).standard_normal((hc.NL, 3))
    h = 1e-5; fd = (hc.action(hc.step(U, h*X)) - hc.action(hc.step(U, -h*X)))/(2*h); assert abs(fd - np.sum(g*X)) < 1e-6*abs(fd)
def test_frozen_layers():
    hc = H.HCLoops(8, -1); fz = hc.frozen.reshape(4, 8, 8, 8, 8)
    assert fz[0, 0, 4, 4, 4] and fz[0, 7, 4, 4, 4] and fz[1, 4, 4, 4, 1] and not fz[0, 2, 4, 4, 4] and not fz[0, 4, 4, 4, 4] and fz[0, 5, 4, 4, 4]
    U = rand_links(8, 6); g = hc.grad(U); assert np.all(g[hc.frozen] == 0)
def test_per_site_density_sums_to_action():
    U = rand_links(6, 7); hc = H.HCLoops(6, -1); S, d = hc.action(U, per_site=True); assert abs(d.sum() - S) < 1e-9*S
def test_identity_zero():
    hc = H.HCLoops(6, -1); U = np.zeros((hc.NL, 4)); U[:, 0] = 1
    assert hc.action(U) == 0 and np.all(hc.grad(U) == 0) and hc.charge(U) == 0
def test_bpst_small_is_su2_and_gauge_sane():
    hc = H.HCLoops(8, 1); U = H.bpst_links(hc, 1.5, nsub=8); assert np.allclose(np.linalg.norm(U, axis=-1), 1, atol=1e-12)
def test_eq19_and_tail():
    assert abs(H.eq19(-1, 3.0) - (1 + 1/45 + 27/210/81)) < 1e-12 and abs(H.bpst_tail(9.5, 3.0) - (1-0.97682)) < 1e-5
def test_no_placeholders():
    for f in ("hc_kernel.py", "test_hc.py"):
        src = open(f).read().replace("placeholders", "").replace("TO" + "DO|", "")
        assert not re.search(r"\b(TO" + r"DO|FIX" + r"ME|XX" + r"X|NotImpl" + r"emented)\b|place" + "holder", src), f

if __name__ == "__main__":
    n = f = 0
    for k, v in sorted(globals().items()):
        if k.startswith("test_") and callable(v):
            n += 1; t0 = time.time()
            try: v(); print("PASS", k, f"{time.time()-t0:.1f}s")
            except Exception as e: f += 1; print("FAIL", k, repr(e))
    print(f"HC TESTS {n-f}/{n} passed"); sys.exit(1 if f else 0)

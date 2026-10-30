import os, sys, json
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np, pytest
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from fuzzy_instanton import Model, herm_expm
import grading_it1b as gr, run_it1b as rn
CFG = json.load(open(os.path.join(HERE, "it1b_fuzzy_config_v4.json")))
def small(**kw):
    c = rn.model_cfg(CFG); c.update({"L3": 6, "L4": 6, "n_clamp": 1, "nsub": 4, "quad": {"mult": 2, "extra": 8}}); c.update(kw); return c
def H(rng, shape):
    Y = rng.normal(size=shape) + 1j * rng.normal(size=shape); return Y + np.swapaxes(Y.conj(), -1, -2)

def test_config_ladder_and_x():
    """Fix 7: R=5rho, ladder 21,29,41,57 (addendum V2 C2); x values as Venus checked; 20rho G1 point at N=81."""
    R = CFG["R_over_rho"]["main"]; assert R == 5.0 and CFG["ladder"]["k2"] == [21, 29, 41, 57] == CFG["ladder"]["k1"]
    xs = [gr.x_of(R, n, 1) for n in CFG["ladder"]["k2"]]
    assert np.allclose(xs, [0.227, 0.119, 0.060, 0.031], atol=1e-3)
    assert CFG["R_over_rho"]["G1R_points"] == [5.0, 10.0, 20.0] and CFG["R_over_rho"]["G1_N"]["20.0"] == 81
    for r, n in CFG["R_over_rho"]["G1_N"].items(): assert gr.x_of(float(r), n, 1) <= CFG["x_max"]
    assert CFG["flow"]["checkpoint_every"] == 100

@pytest.mark.parametrize("k", [1, 2, 3])
def test_G0(k):
    ce, se, ie = rn.g0_check(9 if k != 2 else 9, k, CFG)
    assert gr.grade_G0(ce, se, ie, CFG["bands"]["G0_tol"]) == "PASS"

@pytest.mark.parametrize("k,N", [(2, 5), (3, 7)])
def test_seed_zk_invariant(k, N):
    m = Model(small(), N, k, 3.0, -1.0); B, U = m.seed(1.0)
    # Weyl-map seed: invariant to quadrature/eigh round-off (~1e-11), tolerance 1e-10 (was 1e-12 for the old seed)
    assert np.abs(m.project_B(B) - B).max() < 1e-10
    assert all(np.abs(m.project_scalar(U[i]) - U[i]).max() < 1e-10 for i in (0, 1))

def test_twist_sign_minus_breaks_k3():
    m = Model(small(color_twist_sign=-CFG["color_twist_sign"]), 7, 3, 3.0, -1.0); B, U = m.seed(1.0)
    assert np.abs(m.project_B(B) - B).max() > 1e-3

@pytest.mark.parametrize("eps", [-1.0, 1.0])
def test_grad_B_fd(eps):
    m = Model(small(), 5, 1, 3.0, eps); B, U = m.seed(1.0); rng = np.random.default_rng(1)
    _, _, GB, _ = m.action_grad(B, U); dB = H(rng, B.shape); dB[:, m.clamp_site] = 0; e = 1e-6
    fd = (m.action_grad(B + e * dB, U, False, True)[0] - m.action_grad(B - e * dB, U, False, True)[0]) / (2 * e)
    an = np.sum(GB * np.swapaxes(dB, -1, -2)).real
    assert abs(fd - an) < 1e-6 * max(1, abs(an))

@pytest.mark.parametrize("eps", [-1.0, 1.0])
def test_grad_U_fd(eps):
    m = Model(small(), 5, 1, 3.0, eps); B, U = m.seed(1.0); rng = np.random.default_rng(2)
    _, _, _, FU = m.action_grad(B, U); T = H(rng, U.shape); T[m.frozen_link] = 0; e = 1e-6
    fd = (m.action_grad(B, herm_expm(T, -e) @ U, False, True)[0] - m.action_grad(B, herm_expm(T, e) @ U, False, True)[0]) / (2 * e)
    an = np.sum(FU * np.swapaxes(T, -1, -2)).real
    assert abs(fd - an) < 1e-6 * max(1, abs(an))

def test_gauge_invariance():
    m = Model(small(), 5, 1, 3.0, -1.0); B, U = m.seed(1.0); rng = np.random.default_rng(3)
    g = herm_expm(H(rng, (m.L3, m.L4, m.M, m.M)), -0.3); gd = np.swapaxes(g.conj(), -1, -2)
    Bg = g[None] @ B @ gd[None]
    Ug = np.stack([g @ U[0] @ np.roll(gd, -1, 0), g @ U[1] @ np.roll(gd, -1, 1)])
    S0 = m.action_grad(B, U, False, True)[0]; S1 = m.action_grad(Bg, Ug, False, True)[0]
    # periodic wrap links are excluded from the action, so only the open-boundary-consistent sum must match
    assert abs(S0 - S1) < 1e-9 * abs(S0)

def test_eps_plus1_wilson_only():
    m = Model(small(), 5, 1, 3.0, 1.0); assert m.c1 == 1.0 and m.c2 == 0.0

def test_clamp_frozen_in_flow():
    m = Model(small(), 5, 1, 3.0, -1.0); B, U = m.seed(1.0)
    B2, U2, hist = m.flow(B, U, 0.002 * m.a**2, 2, 1)
    assert np.abs(B2[:, m.clamp_site] - B[:, m.clamp_site]).max() == 0
    assert np.abs(U2[m.frozen_link] - U[m.frozen_link]).max() == 0
    assert hist[-1]["S_over_8pi2k"] <= hist[0]["S_over_8pi2k"] + 1e-12

def test_grade_G1_G1R():
    b = CFG["bands"]
    assert gr.grade_G1(1.005, 0.99, b["G1"]) == "PASS" and gr.grade_G1(1.05, 1, b["G1"]) == "FAIL"
    assert gr.grade_G1(1.02, 1, b["G1"]) == "UNDECIDED"
    assert gr.grade_G1R(1.04, 1.01, b["G1R"])[0] == "PASS"
    assert gr.grade_G1R(1.025, 1.01, b["G1R"])[0] == "UNDECIDED"
    assert gr.grade_G1R(1.04, 0.99, b["G1R"])[0] == "FAIL"

def test_fix5_G1_box_fraction():
    """Fix 5 (B4): G1 graded against the analytic box fraction; Venus's numbers 1.09% (8a=2.67rho), 0.10% (5rho)."""
    assert abs((1 - gr.box_fraction(8 / 3)) - 0.0109) < 5e-5 and abs((1 - gr.box_fraction(5)) - 0.0010) < 5e-5
    b = CFG["bands"]["G1"]; bf = gr.box_fraction(8 / 3)
    assert gr.grade_G1(bf * 0.995, 1.0, b, bf) == "PASS"
    assert gr.grade_G1(bf * 0.995, 1.0, b) == "UNDECIDED"          # would mis-grade without the box fraction
    g, r1, r2 = gr.grade_G1R3(bf * 1.16, bf * 1.04, bf * 1.01, CFG["bands"]["G1R"], bf)
    assert g == "PASS" and abs(r1 - 4) < 1e-9 and abs(r2 - 4) < 1e-9
    assert gr.grade_G1R3(bf * 1.16, bf * 1.04, bf * 0.99, CFG["bands"]["G1R"], bf)[0] == "FAIL"

def test_grade_G2_heldout_and_freeze():
    x = np.array([gr.x_of(5, n, 1) for n in CFG["ladder"]["k1"]]); E = 0.3 * x - 0.5 * x**2
    g, err, p = gr.grade_G2(x, E, CFG["bands"]["G2"])
    assert g == "PASS" and err < 1e-10 and abs(p["c1"] - 0.3) < 1e-8 and p["c0"] == 0.0
    g, *_ = gr.grade_G2(x, E + np.array([0, 0, 0, 0.05]), CFG["bands"]["G2"]); assert g == "FAIL"

def test_fix6_c_a_in_E_pred_and_G2():
    """Fix 6 (B1): constant c_a in E_pred (fitted at k=1, frozen); G2 on E - c_a; Q1 label; G2 UNDECIDED if <4 rungs."""
    x = np.array([gr.x_of(5, n, 1) for n in CFG["ladder"]["k1"]]); E = -0.016 + 0.3 * x - 0.5 * x**2
    g, err, p = gr.grade_G2(x, E, CFG["bands"]["G2"])
    assert g == "PASS" and abs(p["c_a"] + 0.016) < 1e-9 and abs(float(gr.E_pred(p, 0.0)) + 0.016) < 1e-9
    assert gr.grade_G2(x[:3], E[:3], CFG["bands"]["G2"])[0].startswith("UNDECIDED")
    assert gr.Q1_LABEL == CFG["Q1_label"] and "x3,x4 only" in gr.Q1_LABEL
    with pytest.raises(ValueError): gr.check_same_R({"21": {"R": 5.0}}, {"21": {"R": 10.0}})
    assert gr.check_same_R({"21": {"R": 5.0}}, {"29": {"R": 5.0}}) == 5.0

def test_grade_Q1_Q2():
    b = CFG["bands"]; lam = np.array([0.488, 0.351, 0.247, 0.177])
    assert gr.grade_Q1(lam, 0.05 * lam**2, b["Q1"])[0] == "REMOVES"
    assert gr.grade_Q1(lam, 0.1 + 0 * lam, b["Q1"])[0] == "DOES NOT REMOVE"
    assert gr.grade_Q2(lam, [0.90, 0.92, 0.94, 0.96], b["Q2"])[0] == "CHANGES"
    assert gr.grade_Q2(lam, [0.913, 0.915, 0.914, 0.913], b["Q2"])[0] == "NO CHANGE"
    assert gr.undecided_if_few([41, 57, 81], CFG["min_valid_rungs"])

def test_fix1_Q1_reads_finest_rung():
    """Fix 1: |X| is read at the finest rung (smallest lam). Coarse rung big, finest small -> REMOVES."""
    b = CFG["bands"]["Q1"]; lam = np.array([0.488, 0.351, 0.247, 0.177]); X = 0.5 * (lam / lam[0])**3 * 0.2
    assert X[0] > b["removes_absX"] and X[-1] <= b["removes_absX"]
    assert gr.grade_Q1(lam, X, b)[0] == "REMOVES"
    assert gr.grade_Q1(lam[::-1], X[::-1], b)[0] == "REMOVES"      # order-independent

@pytest.mark.parametrize("eps", [-1.0, 1.0])
@pytest.mark.parametrize("k,N", [(1, 5), (2, 9), (3, 7)])
def test_fast_action_grad_matches_reference(eps, k, N):
    """Speed-up (fuzzy_instanton.action_grad) == original action_grad_ref to 1e-9: S, density, GB, FU."""
    m = Model(small(), N, k, 3.0, eps); B, U = m.seed(1.0); rng = np.random.default_rng(7)
    B = B + 0.05 * H(rng, B.shape); U = herm_expm(0.05 * H(rng, U.shape), 1.0) @ U   # off-seed, still Hermitian/unitary
    S0, d0, G0, F0 = m.action_grad_ref(B, U); S1, d1, G1, F1 = m.action_grad(B, U)
    assert abs(S1 - S0) <= 1e-9 * max(1, abs(S0))
    assert np.abs(d1 - d0).max() <= 1e-9 * max(1, np.abs(d0).max())
    assert np.abs(G1 - G0).max() <= 1e-9 * max(1, np.abs(G0).max())
    assert np.abs(F1 - F0).max() <= 1e-9 * max(1, np.abs(F0).max())
    assert abs(m.action_grad(B, U, False) - m.action_grad_ref(B, U, False)) <= 1e-9 * max(1, abs(S0))


# ---------------- fix list 2026-10-29 (VENUS_IT1B_CODE_CHECK 1db2bdc3) ----------------
from weyl_seed import WeylQuantizer, SeedField
from fuzzy_instanton import spin_matrices

@pytest.mark.parametrize("N", [5, 12, 21])
def test_fix4_weyl_map_exact_properties(N):
    """Fix 4 (B5): Weyl map Q is exact on l=1 (Q(n_i) = L_i/sqrt(j(j+1))), rotation-equivariant
    ([L_i, Q f] = Q(L_i f)) and trace-exact. These are what remove the O(lam) ordering error."""
    W = WeylQuantizer(N); L = spin_matrices(N); j = (N - 1) / 2; x, y, z = W.n
    Qn = W.quantize(W.n)
    assert max(np.abs(Qn[i] - L[i] / np.sqrt(j * (j + 1))).max() for i in range(3)) < 1e-12
    f = np.exp(2 * x + y * z + 0.5 * x * z * z); fx, fy, fz = (2 + 0.5 * z * z) * f, z * f, (y + x * z) * f
    Q = W.quantize(f)
    assert np.abs(L[0] @ Q - Q @ L[0] + 1j * W.quantize(y * fz - z * fy)).max() < 1e-8
    assert np.abs(L[1] @ Q - Q @ L[1] + 1j * W.quantize(z * fx - x * fz)).max() < 1e-8
    assert abs(4 * np.pi / N * np.trace(Q).real - (W.wth[:, None] * f).sum() * 2 * np.pi / W.nph) < 1e-10

def test_fix3_singular_gauge_rotation():
    """Fix 3 (B3): fast quaternion gauge rotation == explicit 2x2 matrices; outside r_g the field is the
    singular-gauge BPST, |A| ~ rho^2/|x|^3."""
    rng = np.random.default_rng(3); A = rng.normal(size=(4, 3, 5)); Y = rng.normal(size=(4, 5)); dY = np.zeros((4, 4, 5))
    for q in range(4): dY[q, q] = 1
    dY[3, 0] = rng.normal(size=5); dY[3, 1] = rng.normal(size=5)
    assert np.abs(SeedField._gauge_rotate(A, Y, dY) - SeedField._gauge_rotate_ref(A, Y, dY)).max() < 1e-12
    sf = SeedField(1e6, 1.0, 1e6, 2e6, {"r_a": 1.5, "r_g": 3.0, "D": 10.0})
    amp = []
    for r in (10.0, 20.0):
        th = 2 * np.arctan(r / 2e6); n = np.array([np.sin(th), 0.0, np.cos(th)])[:, None]
        Ar, _ = sf.A4(n, 0.0, 0.0); amp.append(np.abs(Ar).max())
    assert abs(np.log(amp[0] / amp[1]) / np.log(2) - 3) < 0.05

def test_fix3_seed_smooth_gauge_inside_box():
    """Fix 3: the interpolated gauge map has no singularity in the box (offset D > box), field finite everywhere."""
    sf = SeedField(5.0, 1.0, 5.0, 10.0, {"r_a": 1.5, "r_g": 3.0, "D": 10.0}); W = WeylQuantizer(9)
    x34 = np.linspace(-3.2, 3.2, 9)
    A, _ = sf.A4(W.n[:, None, None], x34[:, None, None, None], x34[None, :, None, None])
    assert np.all(np.isfinite(A)) and np.abs(A).max() < 10

@pytest.mark.parametrize("k,N", [(1, 5), (2, 9)])
def test_fix_seed_hermitian_unitary(k, N):
    m = Model(small(), N, k, 3.0, -1.0); B, U = m.seed(1.0)
    assert np.abs(B - np.swapaxes(B.conj(), -1, -2)).max() < 1e-12
    assert np.abs(U @ np.swapaxes(U.conj(), -1, -2) - np.eye(m.M)).max() < 1e-12

def test_fix7_checkpoint_resume_bit_identical(tmp_path):
    """Fix 7 / item 20: n steps in one go == n/2 + checkpoint + load + n/2, np.array_equal on B, U, hist."""
    m = Model(small(), 5, 1, 3.0, -1.0); B, U = m.seed(1.0); h = 0.002 * m.a**2; n = 6
    Bf, Uf, hf = m.flow(B, U, h, n, 1)
    cp = str(tmp_path / "ck.npz")
    m2 = Model(small(), 5, 1, 3.0, -1.0); m2.flow(B, U, h, n, 1, ckpt_path=cp, ckpt_every=2, stop_after=3)
    st = Model.load_checkpoint(cp); assert st["step"] == 3 and not st["finished"]
    m3 = Model(small(), 5, 1, 3.0, -1.0); Br, Ur, hr = m3.flow(B, U, h, n, 1, ckpt_path=cp, ckpt_every=2, state=st)
    assert np.array_equal(Bf, Br) and np.array_equal(Uf, Ur)
    assert [(d["t"], d["S_over_8pi2k"]) for d in hf] == [(d["t"], d["S_over_8pi2k"]) for d in hr]
    assert Model.load_checkpoint(cp)["finished"] and not os.path.exists(cp + ".tmp")

def test_fix8_flow_rehermitises():
    """Item 6 slip: B re-Hermitised after each RK3 stage so the fast path never silently falls back."""
    m = Model(small(), 5, 1, 3.0, -1.0); B, U = m.seed(1.0)
    B2, U2, _ = m.flow(B, U, 0.002 * m.a**2, 2, 1)
    assert np.array_equal(B2, np.swapaxes(B2.conj(), -1, -2)) and m.herm_drift_max < 1e-12


def test_patch_seed_two_formulas():
    """Pass-rules V1 seed (a): regular BPST inside |x|<r_g, singular-gauge BPST (rho^2/r^3) outside."""
    import numpy as np
    from weyl_seed import SeedField
    R = 5.0; sf = SeedField(R, 1.0, 50, 100, {"mode": "patch", "r_g": 3.0}); reg = SeedField(R, 1.0, 50, 100, None)
    def at(f, x):
        q = (x[0]**2 + x[1]**2) / (4 * R * R); n3 = (1 - q) / (1 + q)
        n = np.array([x[0] * (1 + n3) / (2 * R), x[1] * (1 + n3) / (2 * R), n3])
        return f.A4(n, np.array(x[2]), np.array(x[3]))[0]
    xin = np.array([0.3, 0.5, -0.4, 0.2]); assert np.allclose(at(sf, xin), at(reg, xin))
    for s in (4.0, 8.0):
        x = s * np.array([0.5, 0.5, 0.5, -0.5]); r = np.linalg.norm(x)
        assert np.abs(at(sf, x)).max() < 2.0 / (r**2 * (r**2 + 1)) * r     # singular gauge: rho^2 |x| / (x^2 (x^2+rho^2))


def test_pure_gauge_plaquette_is_one_O_a2():
    """V2 seed links: midpoint path-ordered transporter (2nd order in a/nsub), same convention as Model.seed
    (U = prod_s exp(-i (a/ns) A(mid_s)), D = d - iA). Pure gauge A = i g dg^+ -> plaquette = 1 + O(a^2)."""
    import numpy as np
    S = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.diag([1.0 + 0j, -1.0])]
    def g(x3, x4):
        v = np.array([0.7 * x3 + 0.3 * x4**2, -0.4 * x4 + 0.2 * x3 * x4, 0.5 * np.sin(x3)])
        th = np.linalg.norm(v); nv = v / th
        return np.cos(th) * np.eye(2) + 1j * np.sin(th) * sum(nv[i] * S[i] for i in range(3))
    def A(x, mu, h=1e-6):
        e = np.zeros(2); e[mu] = h
        dg = (g(*(x + e)) - g(*(x - e))) / (2 * h)
        return 1j * g(*x) @ dg.conj().T
    def expmH(H, s):
        w, V = np.linalg.eigh(0.5 * (H + H.conj().T)); return (V * np.exp(-1j * s * w)) @ V.conj().T
    def link(x, mu, a, ns):
        U = np.eye(2, dtype=complex)
        for s in range(ns):
            y = np.array(x, float); y[mu] += (s + 0.5) * a / ns
            U = U @ expmH(A(y, mu), a / ns)
        return U
    errs = []
    for a in (0.4, 0.2):
        x = np.array([0.3, -0.2]); e3 = np.array([a, 0]); e4 = np.array([0, a])
        P = link(x, 0, a, 2) @ link(x + e3, 1, a, 2) @ link(x + e4, 0, a, 2).conj().T @ link(x, 1, a, 2).conj().T
        errs.append(abs(np.trace(P).real / 2 - 1) + np.abs(P - np.eye(2)).max())
    assert errs[0] < 0.05 and errs[1] < errs[0] / 3.0, errs


def test_v3_antipode_cap_gauge():
    """SEED_PASS_RULES_V3 P0: h -> 1 at the cap edge (on the x3=x4=0 axis), A' bounded at the pole, A' = A outside."""
    import numpy as np
    from weyl_seed import SeedField, seed_functions
    R, eps = 5.0, 0.3
    sf = SeedField(R, 1.0, 1e9, 2e9, {"mode": "antipode", "eps": eps}); reg = SeedField(R, 1.0, 1e9, 2e9, None)
    rp = eps * (1 - 1e-9); r = 2 * R * np.tan((np.pi - rp) / 2)
    X = np.array([[r * np.cos(0.3)], [r * np.sin(0.3)], [0.0], [0.0]])
    assert np.abs(sf.h_field(X, eps, R) - np.eye(2)).max() < 1e-6
    def at(f, n3, ph=0.7):
        s = np.sqrt(1 - n3 * n3); n = np.array([[s * np.cos(ph)], [s * np.sin(ph)], [n3]])
        return seed_functions(f, n, np.array(1.0), np.array(-0.5))
    big = [np.abs(at(sf, -1 + d)[0]).max() for d in (1e-4, 1e-6, 1e-8)]
    assert max(big) < 10 and abs(big[-1] - big[-2]) < 1e-2          # bounded, converges at the pole
    for n3 in (0.5, -0.5):
        for u, v in zip(at(sf, n3), at(reg, n3)): assert np.allclose(u, v)


def test_v4_antipode_P0():
    """SEED_PASS_RULES_V4 P0: h = 1 on the cap edge over the full (x3,x4) range, A' edge jump < 1e-6,
    max theta over the cap <= pi - 0.2; analytic dh matches FD; h = G^-1 in the inner cap; A' = A outside."""
    import numpy as np
    from weyl_seed import SeedField, seed_functions, SIG
    R = 5.0
    for eps in (0.3, 0.5):
        sf = SeedField(R, 1.0, 1e9, 2e9, {"mode": "antipode_v4", "eps": eps}); reg = SeedField(R, 1.0, 1e9, 2e9, None)
        re = 2 * R * np.tan((np.pi - eps) / 2); xs = np.linspace(-6, 6, 13)
        X3, X4 = np.meshgrid(xs, xs); P = X3.size
        X = np.array([np.full(P, 0.6 * re), np.full(P, 0.8 * re), X3.ravel(), X4.ravel()])
        Y, _, th, s = SeedField.h_v4(X, eps, R)
        assert np.abs(Y[3] - 1).max() < 1e-12 and np.abs(Y[:3]).max() < 1e-12
        assert th.max() <= np.pi - 0.2
        rp = 0.7 * eps; rr = 2 * R * np.tan((np.pi - rp) / 2); x = np.array([[rr * .8], [rr * .6], [1.3], [-2.1]])
        Y, dY, _, _ = SeedField.h_v4(x, eps, R)
        for mu in range(4):
            e = np.zeros((4, 1)); e[mu] = 1e-4 * rr if mu < 2 else 1e-5
            fd = (SeedField.h_v4(x + e, eps, R)[0] - SeedField.h_v4(x - e, eps, R)[0]) / (2 * e[mu])
            assert np.abs(fd - dY[:, mu]).max() < 1e-7
        x = np.array([[rr], [0.3 * rr], [1.0], [-2.0]]); x[:2] *= np.tan((np.pi - 0.2 * eps) / 2) / np.tan((np.pi - rp) / 2)
        Y, _, _, _ = SeedField.h_v4(x, eps, R); I = np.eye(2)
        h = Y[3, 0] * I - 1j * np.einsum("a,aij->ij", Y[:3, 0], SIG)
        G = (x[3, 0] * I + 1j * np.einsum("a,aij->ij", x[:3, 0], SIG)) / np.linalg.norm(x)
        assert np.abs(h @ G - I).max() < 1e-12
        def at(f, n3, ph=0.7):
            q = np.sqrt(1 - n3 * n3); n = np.array([[q * np.cos(ph)], [q * np.sin(ph)], [n3]])
            return seed_functions(f, n, np.array(1.3), np.array(-2.1))
        ne = -np.cos(eps)
        assert max(np.abs(a - b).max() for a, b in zip(at(sf, ne * (1 - 1e-9)), at(sf, ne * (1 + 1e-9)))) < 1e-6
        assert np.abs(at(sf, -1 + 1e-8)[0]).max() < 1e-3                 # bounded (-> 0) at the pole
        for u, v in zip(at(sf, 0.2), at(reg, 0.2)): assert np.allclose(u, v)

import os, sys, json, numpy as np, pytest
os.environ["OPENBLAS_NUM_THREADS"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from fuzzy_sphere import *
from observables import heat_trace, a_tip_star, tip_proxy
from step1_paper import grade_step1
import grading as G
CFG = json.load(open(os.path.join(os.path.dirname(HERE), "fuzz_config_v4.json")))

@pytest.mark.parametrize("N", [2, 3, 5, 8])
def test_su2_algebra(N):
    Lx, Ly, Lz = spin_matrices(N)
    assert np.allclose(Lx @ Ly - Ly @ Lx, 1j * Lz)
    assert np.allclose(Lx@Lx + Ly@Ly + Lz@Lz, (N*N-1)/4 * np.eye(N))

@pytest.mark.parametrize("N,R", [(4, 1.7), (7, 0.3)])
def test_X_radius_and_lambda(N, R):
    X = X_matrices(R, N); lam = lam_N(R, N)
    assert np.allclose(sum(x@x for x in X), R*R*np.eye(N))
    assert np.allclose(X[0]@X[1]-X[1]@X[0], 1j*lam*X[2])
    assert np.isclose(R_from_lam(lam, N), R)

@pytest.mark.parametrize("N,k", [(5, 2), (6, 3), (7, 2), (6, 1)])
def test_invariant_algebra_and_spectrum(N, k):
    g = g_matrix(N, k); mask = invariant_mask(N, k)
    M = np.random.default_rng(0).normal(size=(N, N)) * mask
    assert np.allclose(g @ M @ np.linalg.inv(g), M)
    assert mask.sum() == invariant_spectrum_counts(N, k)[1].sum()
    # numerical spectrum of adjoint Laplacian restricted to A_k vs analytic l(l+1)/R^2 counts
    R = 1.3; D = adjoint_laplacian(R, N); idx = np.flatnonzero(mask.ravel())
    ev = np.sort(np.linalg.eigvalsh(D[np.ix_(idx, idx)]))
    ls, mult = invariant_spectrum_counts(N, k)
    an = np.sort(np.repeat(ls*(ls+1)/R**2, mult))
    assert np.allclose(ev, an, atol=1e-9)

def test_coherent_overlap_closed_form():
    N, th, ph = 6, 0.7, 2*np.pi/3
    v = coherent_state(N, th); _, _, Lz = spin_matrices(N)
    num = abs(v.conj() @ np.diag(np.exp(1j*ph*np.diag(Lz).real)) @ v)**2
    assert np.isclose(num, coherent_twist_overlap(N, th, ph))

def test_heat_trace_k1_t0_and_large_t():
    assert np.isclose(heat_trace(1.0, 6, 1, 0.0)[0], 36)   # dim Mat_N
    assert np.isclose(heat_trace(1.0, 6, 3, 1e4)[0], 1)    # only l=0

def test_atip_star():
    assert np.isclose(a_tip_star(2), 0.25) and np.isclose(a_tip_star(3), 4/9)

def test_proxy_peaks_at_tip():
    th = np.linspace(0, np.pi/2, 50); P = tip_proxy(10, 2, th)
    assert np.isclose(P[0], 0.5) and P[-1] < P[0]

def test_step1_pass():
    r = grade_step1(CFG["step1"])
    assert r["P1"] and r["R8_pass"] and r["R9_pass"], r

def test_graders_synthetic():
    rows = [{"N": n, "e": e, "plateau": True} for n, e in [(32, .2), (64, .1), (128, .03)]]
    assert G.grade_A(rows, CFG) == "PASS"
    rows[-1]["e"] = .3; assert G.grade_A(rows, CFG) == "FAIL"
    B = [{"N": n, "w_over_R": 3.0/np.sqrt(n)} for n in (32, 64, 128)]
    assert G.grade_B(B, CFG)["grade"] == "PASS"
    B = [{"N": n, "w_over_R": 3.0/n} for n in (32, 64, 128)]
    assert G.grade_B(B, CFG)["grade"] == "FAIL"   # old w~lam model fails V4 §1 bands
    B = [{"N": n, "w_over_R": np.exp(-n/20)} for n in (32, 64, 128)]
    assert G.grade_B(B, CFG)["grade"] == "FAIL"
    lams = [1, .5, .25, .125]; f = G.ladder_fit(lams, [2*l for l in lams], CFG)
    assert f["L_q"] == "PASS" and f["L_h"] == "PASS" and abs(f["q"]-1) < 1e-9
    assert G.ladder_fit(lams[:3], [1, 1, 1], CFG)["grade"] == "UNDECIDED"
    assert G.overall(["PASS", "UNDECIDED"]) == "UNDECIDED" and G.overall(["PASS", "FAIL"]) == "FAIL"

def test_step1_R9_fails_if_hL_wrong():
    c = dict(CFG["step1"]); c["h_L"] = 1.0
    assert not grade_step1(c)["R9_pass"]

def test_window_empty_small_N():
    from observables import test_A
    assert test_A(1.0, 20, 2, CFG)["plateau"] is False


# ---- V4 additions
from ldos import cg_sq, K_fuzzy, K_classical, ldos_width
import run_fuzz

def test_grade_La_empty_no_crash():
    r = G.grade_La([], a_tip_star(2), CFG)
    assert r["L_a"] == "UNDECIDED"
    assert G.grade_La([None, None], a_tip_star(2), CFG)["L_a"] == "UNDECIDED"

def test_ladder_fit_and_LB_with_missing():
    assert G.ladder_fit([1, .5], [None, None], CFG)["grade"] == "UNDECIDED"
    assert G.grade_LB(None, CFG) == "UNDECIDED"

@pytest.mark.parametrize("N,k", [(5, 1), (6, 2), (7, 2)])
def test_ldos_cg_matches_explicit_matrices(N, k):
    """sum over normalised invariant eigvecs at level l of |<pole|M|pole>|^2 = (2l+1) c_l / N (HS norm)."""
    R = 1.0; D = adjoint_laplacian(R, N); idx = np.flatnonzero(invariant_mask(N, k).ravel())
    ev, V = np.linalg.eigh(D[np.ix_(idx, idx)])
    pole = 0 * N + 0                          # |j,j><j,j| entry in row-major vec
    c = cg_sq(N)
    for l in range(N):
        sel = np.isclose(ev, l*(l+1)); full = np.zeros((N*N, sel.sum()), complex); full[idx] = V[:, sel]
        assert np.isclose((abs(full[pole])**2).sum(), (2*l+1)*c[l]/N)

def test_ldos_limits():
    R, N, k = 2.0, 30, 2
    assert np.isclose(cg_sq(N)[0], 1.0)
    big = np.array([5.0]) * R**2
    assert np.isclose(K_fuzzy(R, N, k, big)/K_classical(R, k, big, CFG["ldos_exp_cut"]), 1, atol=1e-3)
    small = np.array([1e-5]) * R**2
    assert K_fuzzy(R, N, k, small)[0] < K_classical(R, k, small, CFG["ldos_exp_cut"])[0]
    w = ldos_width(R, N, k, CFG); assert w["w_over_R"] is not None and w["w_over_R"] > 0

def test_ldos_ratio_k_independent():
    t = np.array([0.01, 0.1])
    r2 = K_fuzzy(1, 20, 2, t)/K_classical(1, 2, t, 50); r3 = K_fuzzy(1, 20, 3, t)/K_classical(1, 3, t, 50)
    assert np.allclose(r2, r3)

def test_step1_uses_p():
    c = json.loads(json.dumps(CFG["step1"])); c["p_R_plus"] = 0.6
    from step1_paper import r_values
    assert abs(r_values(c)["R2"] - r_values(CFG["step1"])["R2"]) > 1e-3
    assert abs(r_values(CFG["step1"])["R4"] - np.pi) < 1e-9

def test_k_labels():
    assert "exact" in run_fuzz.k_label(2, CFG)
    assert "REDUCED MODEL" in run_fuzz.k_label(3, CFG)
    assert "NO TIP" in run_fuzz.k_label(1, CFG)

def test_grade_D():
    star = (1/12)*(2-0.5)
    assert G.grade_D([{"N": 128, "D_raw": star*1.01}], 2, CFG)["grade"] == "PASS"
    assert G.grade_D([{"N": 128, "D_raw": star*1.2}], 2, CFG)["grade"] == "FAIL"

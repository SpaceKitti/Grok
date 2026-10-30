import os, sys, json
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np, pytest
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "it1b"))
from fuzzy_instanton import Model
import run_it1b as rn, cone_seed as cs, cone_grading as cg, cone_target as ct
CFG = json.load(open(os.path.join(HERE, "..", "it1b", "it1b_fuzzy_config_v4.json")))
PRED = json.load(open(os.path.join(HERE, "CONE_PREDICTIONS_V1.json")))
def mk(N, k, L=8, a=1/3):
    c = rn.model_cfg(CFG, L); c["a"] = a; c["n_clamp"] = 1; return Model(c, N, k, 1.0, 1.0)

def test_projectors_exact():
    for N in (3, 5, 9):
        Pp, Pm = cs.projectors(N)
        assert np.abs(Pp @ Pp - Pp).max() < 1e-12 and np.abs(Pp @ Pm).max() < 1e-12
        assert round(np.trace(Pp).real) == N + 1 and round(np.trace(Pm).real) == N - 1

@pytest.mark.parametrize("k", [1, 2, 3])
def test_seed_zk_invariant_and_hermitian_unitary(k):
    m = mk(5, k); B, U = cs.build(m, 1, 1.5)
    assert np.abs(m.project_B(B) - B).max() < 1e-12
    assert np.abs(B - np.swapaxes(B.conj(), -1, -2)).max() < 1e-12
    I = np.eye(m.M); assert np.abs(U @ np.swapaxes(U.conj(), -1, -2) - I).max() < 1e-12

def test_far_field_exact_pure_gauge():
    N = 5; Pp, Pm = cs.projectors(N); m = mk(N, 1)
    th = 0.7; g = Pp + np.exp(2j * th) * Pm
    Bpg = [g @ L @ g.conj().T for L in m.Lfull]
    for i, j, c in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        assert np.abs(Bpg[i] @ Bpg[j] - Bpg[j] @ Bpg[i] - 1j * Bpg[c]).max() < 1e-12
    assert 1 - cs.profile(np.array([20.0]), 1, 1.0, 1.5, 0.3)[0] < 1e-5   # NOT exact: 1-F = exp(-u) (blocker B-F)

def test_profile_tip_law():
    r = np.array([1e-3, 2e-3]); 
    for n, k in [(1, 1), (2, 3)]:
        F = cs.profile(r, n, 1 / k, 1.5, 0.0); assert abs(np.log(F[1] / F[0]) / np.log(2) - n * k) < 1e-3
    F = cs.profile(r, 1, 1.0, 1.5, 0.3); assert abs(np.log(F[1] / F[0]) / np.log(2) - 3) < 1e-3  # fuzzy: smooth r^(p+2)

def test_radial_charge_regression_V4():
    """C-2: Venus radial charge must give 0.9327 on the V4 N21 L20 (eps=0.3, a=rho/3, R=5) seed."""
    mc = rn.model_cfg(CFG, 20); mc["a"] = 1 / 3; mc["taper_r0_over_R"], mc["taper_r1_over_R"] = 1e9, 2e9
    mc["gauge"] = {"mode": "antipode_v4", "eps": 0.3}
    m = Model(mc, 21, 1, 5.0, 1.0); B, U = m.seed(1.0)
    q = cg.charge_radial(m, B, U); assert abs(q - 0.9327) < 5e-5
    assert abs(cg.charge_radial(m, B, U, "su2") + cg.charge_radial(m, B, U, "u1") - q) < 1e-10   # C-7 split adds up

def test_charge_sign_flip():
    m = mk(5, 1, L=12); B, U = cs.build(m, 1, 1.0); B2, U2 = cs.build(m, 1, 1.0, sgn=-1)
    assert abs(cg.charge_radial(m, B, U) + cg.charge_radial(m, B2, U2)) < 1e-10

def test_predictions_frozen_and_in_Zk():
    for e in PRED["P1"]:
        n, k, m_, Q = e["n"], e["k"], e["m_hol"], e["Q_pred"]
        assert abs(k * Q - round(k * Q)) < 1e-12 and (round(k * Q) - m_) % k == 0
        assert (m_, Q) == cs.tip_holonomy(n, k)
    for e in PRED["P2"]: assert e["p"] == abs(e["n"]) * e["k"] and e["slope"] == 2 * e["p"] - 2

def test_grade_P1_rules():
    g = cg.grade_P1(0.48, 0.495, 1, 2, 1, 0.5); assert g["grade"] == "PASS" and g["cover_ok"]
    assert cg.grade_P1(0.40, 0.45, 1, 2, 1, 0.5)["grade"].startswith("FAIL (cover")
    assert cg.grade_P1(0.499, 0.49, 1, 2, 1, 0.5)["grade"].startswith("FAIL (construction")
    with pytest.raises(AssertionError): cg.grade_P1(0.3, 0.3, 1, 3, 1, 0.3)

def test_tip_fitter_synthetic():
    r = np.linspace(0.5, 3, 40); e = 7 * r**2
    assert cg.fit_tip_exponent(r, e, 0.2, 4.0, 1, 0.5)["grade"] == "PASS"
    assert cg.fit_tip_exponent(r, e, 1.0, 2.0, 1, 0.5)["grade"].startswith("UNDECIDED")

def test_casimir_l_content():
    N = 5; m = mk(N, 1); B, U = cs.build(m, 1, 1.0)
    for i in range(3): assert cg.max_l_content(B[i, 3, 3] - m.Lfull[i], N) <= N - 1
    Pp, Pm = cs.projectors(N); assert cg.max_l_content(Pp, N) <= 1          # Lam has l <= 1

@pytest.mark.parametrize("k", [1, 2, 3])
def test_P7_deficit(k):
    d = cg.cone_deficit(mk(5, k)); assert d["grade"] == "PASS" and abs(d["target"] - 2 * np.pi * (1 - 1 / k)) < 1e-12

def test_target_integrator_doubling_and_alpha_free_core():
    # Venus check: harmonic winding core energy is alpha independent (=|n| per unit 2pi). Sharp profile r^p cut at r=1.
    v, nn = ct.box_integral(lambda r: np.exp(-r**2), 6.0); assert abs(v - np.pi) < 1e-6
    T1, _ = ct.T_dirichlet(1, 1.0, 3.0, 1.5); assert T1 > 0

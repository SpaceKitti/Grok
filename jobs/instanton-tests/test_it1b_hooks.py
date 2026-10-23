import numpy as np, run as R
def test_hist_window():
    h = [(0.0, 3.0), (0.05, 2.9), (0.1, 2.8), (0.35, 2.7), (0.6, 2.6), (0.61, 2.5), (0.3, float("nan"))]
    assert R.it1b_hist_window(h) == [(0.1, 2.8), (0.35, 2.7), (0.6, 2.6)]
def test_tip_log():
    d = R.it1b_tip_log(10.0, [4., 2., 1., 3.], [2., 1., 1., 1.], np.array([1, 1, 0, 0], bool), np.array([1, 0, 1, 0], bool))
    assert d["peak_tip"] == 2.0 and d["peak_all"] == 3.0 and abs(d["frac_r_lt_2a"]-0.5) < 1e-12 and d["finite"]
def test_tip_log_nonfinite():
    assert not R.it1b_tip_log(1.0, [np.inf, 1.], [1., 1.], np.array([1, 0], bool), np.array([1, 1], bool))["finite"]
t = np.round(np.arange(0.1, 0.6001, 0.01), 10)
def _row(al, s, d, p):
    h = [(x, 3.0*x**(-p)) for x in t]; return dict(alpha=al, seed=s, delta=d, ell=100.0, hist=h, hist_full=h)
def _all(f):
    rl = [_row(al, -1, 0.0, 1.0) for al in R.IT1B_ALPHAS]
    rl += [_row(al, s, d, 1.0 + f(d, s)) for al in R.IT1B_ALPHAS for s in R.IT1B_SEEDS for d in R.IT1B_DELTAS]
    return rl
def test_p3_switch_refuses():
    R.IT1B_P3 = "dp"
    try: R.it1b_p3_control(_all(lambda d, s: 10*d), 0.03); assert False
    except RuntimeError: pass
    finally: R.IT1B_P3 = "dX"
def test_short_check():
    ok = R.it1b_short_check(dict(hist_full=[(0.59, 2.95), (0.6, 2.93)])); bad = R.it1b_short_check(dict(hist_full=[(0.6, 3.0)]))
    assert ok["ok"] and not bad["ok"] and not R.it1b_short_check(dict(hist_full=[(0.5, 2.9)]))["ok"]
def test_old_constants_unchanged():
    assert R.IT1_T_MAX_OVER_TF == 4.0 and R.DIAG21_FLOW_MAX_OVER_TF == 6.0 and R.IT1_WIN_SETTLE == 0.10 and R.FLOW_STEP == 0.002


def test_row_path_and_modes():
    assert "diag22b" in R.it1b_row_path(1, 0, 0.003)
    src = open(R.__file__, encoding="utf-8").read(); assert '"it1b-row", "it1b-cal", "it1b-grade"' in src

# ---- rev 6 (E360229B) hooks ----
def _all6(L, alpha_scale=None):
    rl = [_row(al, -1, 0.0, 1.0) for al in R.IT1B_ALPHAS]
    for al in R.IT1B_ALPHAS:
        for s in R.IT1B_SEEDS:
            for sd in R.IT1B_SIGNED_DELTAS:
                r = _row(al, s, sd, 1.0); r["hist"] = r["hist_full"] = [(x, y*(1+sd*L(abs(sd), s))) for x, y in r["hist"]]; rl.append(r)
    return rl
def test_r6_grade_from_pass():
    g = R.it1b_grade_from(_all6(lambda d, s: 1.0+0.01*s), 0.03)
    assert g["status"] == "graded" and all(v["verdict"] == "PASS" for v in g["per_alpha"].values()) and "E360229B" in g["measure"]
    assert g["label"] == "linear response at t=0.6, reduced model" and g["tag"] == "[hive proposal, untested]" and g["flow_eps"] == -1
def test_r6_p3_uses_plus_rows_and_restores():
    old = R.DIAG22_DELTAS; g = R.it1b_grade_from(_all6(lambda d, s: 1.0), 0.03)
    assert R.DIAG22_DELTAS == old and g["P3"]["deltas_used"] == [0.003, 0.006] and g["P3"]["ok"]
def test_r6_p3_fail():
    rl = _all6(lambda d, s: 1.0)
    for r in rl:
        if r["alpha"] == 0.5 and r["delta"] > 0: r["hist"] = r["hist_full"] = [(x, 1.5*y) for x, y in r["hist"]]
    g = R.it1b_grade_from(rl, 0.03); assert g["P3"]["value"] >= 0.23 and g["per_alpha"]["0.5"]["verdict"] == "FAIL"
def test_r6_missing_minus_row():
    rl = [r for r in _all6(lambda d, s: 1.0) if not (r["delta"] == -0.006 and r["seed"] == 1 and r["alpha"] == 1.0)]
    g = R.it1b_grade_from(rl, 0.03); assert g["status"] == "NOT COMPUTED (YET)" and g["missing"] == [(1.0, 1, -0.006)]
def test_r6_signed_deltas_and_paths():
    assert R.IT1B_DELTAS == (0.003, 0.006) and sorted(R.IT1B_SIGNED_DELTAS) == [-0.006, -0.003, 0.003, 0.006]
    p = R.it1b_row_path(0.5, 1, -0.003); assert p.endswith("B10_a0.5_s1_delta-0.003.json") and "rows_rev6" in p
    assert R.it1b_row_path(1, 0, 0.0).endswith("B10_a1.0_s-1_delta0.0.json") and R.it1b_row_path(1, 1, 0.0) == R.it1b_row_path(1, 0, 0.0)
def test_r6_cli_negative_delta():
    import argparse
    src = open(R.__file__, encoding="utf-8").read(); i = src.index("ap = argparse.ArgumentParser()"); line = src[i:src.index("\n", i)]
    ns = {"argparse": argparse}; exec(line, ns); A = ns["ap"].parse_args(["it1b-row", "--alpha", "0.5", "--seed", "1", "--delta", "-0.003"])
    assert A.delta == -0.003 and A.seed == 1 and A.mode == "it1b-row"
    assert ns["ap"].parse_args(["it1b-bpst", "--eps", "-1"]).eps == -1.0 and ns["ap"].parse_args(["it1b-x0"]).mode == "it1b-x0"
def test_r6_flow_eps_and_docstring():
    assert R.IT1B_FLOW_EPS == -1 and R.IT1_EPS == 0 and "LEFT-multiplied" in R.it1_perturb.__doc__ and "exp(delta * xi) U" in R.it1_perturb.__doc__
def test_r6_perturb_is_left_and_antisymmetric():
    from kernels import Loops, generic_seed
    from lattice import Lattice, qmul, qexp_im
    lat = Lattice(3, 4, 4, 4, alpha=1.0); lp = Loops(lat, -1); c = (0., 0., lat.x3[2], lat.x4[2]); U = generic_seed(lat, 1.0, seed=0, centre=c)
    xi = R.it1_smooth_field(lp, 0); Up = R.it1_perturb(lp, U, 0, 0.003); Um = R.it1_perturb(lp, U, 0, -0.003)
    free = ~lp.frozen; Ex = qexp_im(0.003*xi); left = qmul(Ex, U); left = left/np.linalg.norm(left, axis=-1, keepdims=True)
    assert np.allclose(Up[free], left[free], atol=1e-13) and np.allclose(Up[lp.frozen], U[lp.frozen])
    back = R.it1_perturb(lp, Up, 0, -0.003); assert np.allclose(back, U, atol=1e-12) and not np.allclose(Up, Um)
def test_r6_x0_check():
    h = [(0.5, 2.0), (0.6, 2.1)]; ok = R.it1b_x0_check(dict(alpha=1.0, hist_full=h, err=None, Q=1.0, absQ_minus_1=0.0))
    bad = R.it1b_x0_check(dict(alpha=1.0, hist_full=h, err="flow unstable", Q=1.0, absQ_minus_1=0.0))
    badq = R.it1b_x0_check(dict(alpha=1.0, hist_full=h, err=None, Q=0.9, absQ_minus_1=0.1))
    assert ok["ok"] and not bad["ok"] and not badq["ok"] and not R.it1b_x0_check(dict(alpha=1.0, hist_full=[(0.5, 2.)], err=None, Q=1., absQ_minus_1=0.))["ok"]
def test_r6_grade_from_duplicate():
    rl = _all6(lambda d, s: 1.0); rl.append(rl[-1])
    try: R.it1b_grade_from(rl, 0.03); assert False
    except ValueError: pass

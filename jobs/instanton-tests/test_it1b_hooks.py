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
    return dict(alpha=al, seed=s, delta=d, hist=[(x, 3.0*x**(-p)) for x in t])
def _all(f):
    rl = [_row(al, -1, 0.0, 1.0) for al in R.IT1B_ALPHAS]
    rl += [_row(al, s, d, 1.0 + f(d, s)) for al in R.IT1B_ALPHAS for s in R.IT1B_SEEDS for d in R.IT1B_DELTAS]
    return rl
def test_grade_from_pass():
    g = R.it1b_grade_from(_all(lambda d, s: 10*d*(1+0.01*s)), 0.03)
    assert g["status"] == "graded" and all(v["verdict"] == "PASS" for v in g["per_alpha"].values())
def test_grade_from_control_fail():
    g = R.it1b_grade_from(_all(lambda d, s: 100*d*(1+0.01*s)), 0.03)
    assert g["control_dp_alpha05"] >= 0.23 and g["per_alpha"]["0.5"]["verdict"] == "FAIL"
def test_grade_from_missing():
    g = R.it1b_grade_from(_all(lambda d, s: 10*d)[:-1], 0.03); assert g["status"] == "NOT COMPUTED (YET)" and len(g["missing"]) == 1
def test_grade_from_duplicate():
    rl = _all(lambda d, s: 10*d); rl.append(rl[-1])
    try: R.it1b_grade_from(rl, 0.03); assert False
    except ValueError: pass
def test_row_path_and_modes():
    assert R.it1b_row_path(1, 0, 0.0015).endswith("B10_a1.0_s0_delta0.0015.json") and "diag22b" in R.it1b_row_path(1, 0, 0.0015)
    src = open(R.__file__, encoding="utf-8").read(); assert '"it1b-row", "it1b-cal", "it1b-grade"' in src
def test_old_constants_unchanged():
    assert R.IT1_T_MAX_OVER_TF == 4.0 and R.DIAG21_FLOW_MAX_OVER_TF == 6.0 and R.IT1_WIN_SETTLE == 0.10 and R.FLOW_STEP == 0.002

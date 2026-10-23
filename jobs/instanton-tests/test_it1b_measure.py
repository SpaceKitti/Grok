import numpy as np, it1b_measure as m
t = np.round(np.arange(0.1, 0.6001, 0.01), 10)
def H(A, p, noise=0.0, seed=0):
    r = np.random.default_rng(seed); return np.c_[t, A*t**(-p)*np.exp(noise*r.standard_normal(t.size))]
def base(): return {0: H(3.0, 1.0), 1: H(3.1, 1.0)}
def test_fit_p(): p, c = m.fit_p(H(2.0, 0.98)); assert abs(p-0.98) < 1e-9 and abs(c-np.log(2)) < 1e-9
def test_g1_pass(): assert m.g1(H(3, 1.0))["ok"]
def test_g1_fail_curved():
    h = np.c_[t, 3*t**-1.0 + 5*t]; assert not m.g1(h)["ok"]
def test_fit_r_exact():
    dp, dA = m.fit_r(H(3*np.exp(.01), 1.02), H(3, 1.0)); assert abs(dp-0.02) < 1e-9 and abs(dA-0.01) < 1e-9
def test_grid_mismatch():
    try: m.fit_r(H(3, 1)[:-1], H(3, 1)); assert False
    except ValueError: pass
def _rows(f):
    b = base(); return b, {1.0: {d: {s: H(b[s][0, 1]*0.1**1.0*np.exp(f(d, s)[1]), 1.0+f(d, s)[0]) for s in b} for d in (0.0015, 0.003)}}
def test_linear_dp_pass():
    b, rows = _rows(lambda d, s: (10*d*(1+0.01*s), 0.0)); g = m.grade_it1b({1.0: b}, rows, 0.03, 0.1)[1.0]
    assert g["lin_quantity"] == "dp" and abs(g["lin_ratio"]-2) < 0.05 and g["verdict"] == "PASS"
def test_time_rescale():
    b, rows = _rows(lambda d, s: (0.0, 5*d*(1+0.01*s))); g = m.grade_it1b({1.0: b}, rows, 0.03, 0.1)[1.0]
    assert g["lin_quantity"] == "dlnA" and g["verdict"] == "PASS" and g["helios_note"].startswith("time-rescale")
def test_noise_undecided():
    b = base(); rows = {1.0: {d: {s: H(b[s][0, 1]*0.1, 1.0, noise=0.05, seed=10*s+int(d*1e4)) for s in b} for d in (0.0015, 0.003)}}
    assert m.grade_it1b({1.0: b}, rows, 0.03, 0.1)[1.0]["verdict"] == "UNDECIDED"
def test_nonlinear_fail():
    b, rows = _rows(lambda d, s: (10*d*(1+0.01*s) if d < .002 else 10*.0015*(1+0.01*s)*1.2, 0.0))
    g = m.grade_it1b({1.0: b}, rows, 0.03, 0.1)[1.0]; assert g["verdict"] == "FAIL" and not g["P1"]
def test_cal_and_control_gates():
    b, rows = _rows(lambda d, s: (10*d*(1+0.01*s), 0.0))
    assert m.grade_it1b({1.0: b}, rows, 0.06, 0.1)[1.0]["verdict"] == "FAIL"
    assert m.grade_it1b({1.0: b}, rows, 0.03, 0.23)[1.0]["verdict"] == "FAIL"

import numpy as np, it1b_measure as m
t = np.round(np.arange(0.1, 0.6001, 0.01), 10)
X0 = np.c_[t, 3.0*t**-0.03]
def _rows(L, Ec=0.0):
    """L(d, s): linear response; X(+-d) = X0 + -+... = X0 +/- d L + d^2 Ec, so E_s = 2 Ec."""
    return {1.0: {sg*d: {s: np.c_[t, X0[:, 1] + sg*d*L(d, s) + d*d*Ec] for s in (0, 1)} for d in (0.003, 0.006) for sg in (1, -1)}}
def G(rows, cal=0.03, ctl=0.1): return m.grade_rev6({1.0: X0}, rows, cal, ctl)[1.0]
def test_r6_linear_pass():
    g = G(_rows(lambda d, s: 10*(1+0.01*s), Ec=50.0)); assert g["verdict"] == "PASS" and abs(g["chi"]-10.05) < 1e-9
    assert all(abs(q-1) < 1e-9 for q in g["lin_ratio_per_seed"].values()) and g["label"] == "linear response at t=0.6, reduced model"
def test_r6_even_part_cancels_and_reported():
    g = G(_rows(lambda d, s: 10.0, Ec=400.0)); a = g["antithetic"]["0.003"]
    assert abs(a["L"]-10) < 1e-6 and abs(a["E"]-2*400) < 1e-3 and a["E_role"] == "report-only" and g["verdict"] == "PASS"
def test_r6_even_part_does_not_gate():
    assert G(_rows(lambda d, s: 10.0, Ec=1e6))["verdict"] == "PASS"
def test_r6_noise_undecided():
    g = G(_rows(lambda d, s: 10.0 if s == 0 else -10.0)); assert g["verdict"] == "UNDECIDED" and not g["noise_gate"]["ok"]
def test_r6_noise_beats_fails():
    assert G(_rows(lambda d, s: 0.0), cal=0.5, ctl=0.9)["verdict"] == "UNDECIDED"
def test_r6_lin_band():
    for k, ok in ((0.851, True), (1.149, True), (0.84, False), (1.16, False)):
        g = G(_rows(lambda d, s: 10.0 if d < 0.004 else 10.0*k)); assert g["P1"] == ok and g["verdict"] == ("PASS" if ok else "FAIL")
def test_r6_lin_every_seed():
    g = G(_rows(lambda d, s: 10.0 if (d < 0.004 or s == 0) else 13.0)); assert not g["P1"] and g["verdict"] == "FAIL"
def test_r6_cal_signed_and_ctl():
    r = _rows(lambda d, s: 10.0)
    assert G(r, cal=-0.05)["verdict"] == "PASS" and G(r, cal=-0.051)["verdict"] == "FAIL" and G(r, cal=0.051)["verdict"] == "FAIL"
    assert G(r, ctl=0.23)["verdict"] == "FAIL"
def test_r6_seed_mismatch():
    r = _rows(lambda d, s: 10.0); del r[1.0][-0.003][1]
    try: G(r); assert False
    except ValueError: pass
def test_r6_measure_hash(): assert "E360229B" in G(_rows(lambda d, s: 10.0))["measure"]

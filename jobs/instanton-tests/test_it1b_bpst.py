import numpy as np, run as R
def test_tail_formula():
    # tail(R) = 1 - int_0^R 48 rho^4 r^3 2pi^2/(r^2+rho^2)^4 dr / 8pi^2 ; check numerically
    from scipy.integrate import quad
    rho, Rr = 3.0, 9.5; inside = quad(lambda r: 48*rho**4*r**3*2*np.pi**2/(r**2+rho**2)**4, 0, Rr)[0]/(8*np.pi**2)
    assert abs(R.bpst_tail(Rr, rho) - (1-inside)) < 1e-10 and abs(R.bpst_tail(0.0, rho) - 1) < 1e-12
def test_tail_12p5_under_1pct(): assert 0.008 < R.bpst_tail(12.5, 3.0) < 0.01   # 0.86%: R>=12.5 is a conservative 1% cut
def test_half_widths():
    assert R.box_half_width("B10") == 9.5 and R.box_half_width("B16") == 15.5 and R.box_half_width("B20") == 19.5
def test_target_tail_corrected():
    t = R.bpst_target("B10"); assert t["R"] < 12.5 and abs(t["target"] - (1-R.bpst_tail(9.5, 3.0))) < 1e-15 and "tail" in t["kind"]
    assert R.bpst_target("B16")["target"] == 1.0
def test_dims():
    assert R.bpst_dims("B10", 0.5) == (20, 20, 40, 40) and R.bpst_dims("B10", 2/3) == (15, 20, 30, 30) and R.bpst_dims("B10", 0.3) is None
def test_fit_exact_h2():
    hs = [1.0, 2/3, 0.5]; S = [0.95 - 0.04*h**2 for h in hs]; f = R.bpst_fit(hs, S); assert abs(f["S0"]-0.95) < 1e-12 and f["max_resid"] < 1e-12
def test_fit_needs_two():
    for hs in ([1.0], [1.0, 1.0]):
        try: R.bpst_fit(hs, [1.0]*len(hs)); assert False
        except ValueError: pass
def test_grade_pass_fail():
    tg = R.bpst_target("B10")["target"]; hs = [1.0, 0.5]
    assert R.bpst_grade("B10", hs, [tg*1.005 - 0.03*h**2 for h in hs])["ok"]
    assert not R.bpst_grade("B10", hs, [1.02 - 0.03*h**2 for h in hs])["ok"]
def test_grade_band():
    # frozen band (BPST_PRESTEP_FROZEN.md): PASS iff 0.99*(1-tail(9.5)) <= S0 <= 1.01
    tg = R.bpst_target("B10")["target"]; hs = [1.0, 2/3, 0.5]; g = lambda s0: R.bpst_grade("B10", hs, [s0 - 0.05*h**2 for h in hs])["ok"]
    assert abs(tg - 0.97682) < 1e-5
    assert g(tg) and g(1.0) and g(0.99) and g(1.009) and g(tg*0.991)
    assert not g(tg*0.989) and not g(1.011) and not g(0.9)
    assert R.bpst_grade("B10", hs, [0.99]*3)["band"] == [tg*0.99, 1.01]
    assert "tail-corrected" in R.bpst_grade("B10", hs, [tg]*len(hs))["label"]
def test_plan_lists_all_boxes():
    p = R.bpst_plan(); assert set(p) == set(R.BOXES) and p["B10"]["spacings"]["0.5"]["dims"] == (20, 20, 40, 40)
def test_mode_registered():
    src = open(R.__file__, encoding="utf-8").read(); assert '"it1b-bpst", "it1b-bpst-plan"' in src and "C99963A0" in src

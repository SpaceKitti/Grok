"""Unit tests on small boxes (scratch). python -B tests.py"""
import numpy as np, sys, time
from lattice import Lattice, qmul, qconj
from kernels import Loops, generic_seed, bootstrap_order
import run
RES = {}
def check(name, cond, info):
    RES[name] = (bool(cond), info); print(("PASS " if cond else "FAIL ") + name, info, flush=True)
small = (6, 20, 10, 10)
for al in (1.0, 0.55):
    lat = Lattice(*small, alpha=al); rng = np.random.default_rng(1)
    for eps in (1, 0, -1):
        lp = Loops(lat, eps)
        g = rng.standard_normal((lp.Ns, 4)); g /= np.linalg.norm(g, axis=1, keepdims=True); g[lp.bsite] = [1, 0, 0, 0]
        t, h = np.clip(lp.tail, 0, None), np.clip(lp.head, 0, None)
        U = qmul(g[t], qconj(g[h])); U[lp.frozen] = [1, 0, 0, 0]
        check(f"pure_gauge_zero a={al} eps={eps}", abs(lp.action(U)) < 1e-9, lp.action(U))
        V = lp.step(np.tile([1., 0, 0, 0], (lp.NL, 1)), 0.3*rng.standard_normal((lp.NL, 3)))
        Vg = qmul(qmul(g[t], V), qconj(g[h])); Vg[lp.frozen] = [1, 0, 0, 0]
        s1, s2 = lp.action(V), lp.action(Vg)
        check(f"gauge_invariance a={al} eps={eps}", abs(s1-s2) < 1e-8*abs(s1), (s1, s2))
        G = lp.grad(V); fl = np.where(~lp.frozen)[0]; ok = True; errs = []
        for l in rng.choice(fl, 6, replace=False):
            for a_ in range(3):
                d = np.zeros((lp.NL, 3)); d[l, a_] = 1e-6
                fd = (lp.action(lp.step(V, d))-lp.action(lp.step(V, -d)))/2e-6; errs.append(abs(fd-G[l, a_])); ok &= abs(fd-G[l, a_]) < 1e-4*(1+abs(fd))  # FD roundoff ~ S*1e-16/1e-6
        check(f"gradient_fd a={al} eps={eps}", ok, max(errs))
lat = Lattice(*small, alpha=1.0); L = lat.bpst_links(2.0)
for eps in (1, 0, -1):
    lp = Loops(lat, eps); a1 = lat.action(L, eps)['S']; a2 = lp.action(lp.flat(L))
    check(f"regression_vs_smoke_action eps={eps}", abs(a1-a2) < 1e-9*a1, (a1, a2))
lat = Lattice(*small, alpha=1.0); lp = Loops(lat, 1); U = generic_seed(lat, 2.0, seed=3)
Ss = [lp.action(U)]; V = U
for _ in range(5): V, _h = lp.flow(V, h=0.005, max_steps=4); Ss.append(lp.action(V))
check("flow_monotone_decrease_h0.005", all(np.diff(Ss) < 0), [round(s, 4) for s in Ss])
try: lp.flow(U, h=0.01, max_steps=40, record=4); check("flow_guard_catches_h0.01_instability", False, "no raise")
except FloatingPointError as e: check("flow_guard_catches_h0.01_instability", True, str(e))
r0 = lp.rho_moment(U, rmin=0.0); V, hist = lp.flow(U, h=0.01, rho_target=r0*0.99, rho_fn=lambda W: lp.rho_moment(W, rmin=0.0), max_steps=50)
check("target_rho_stop_fires", len(hist) == 1, (r0, hist[:2]))
lat = Lattice(12, 20, 24, 24, alpha=1.0); lp = Loops(lat, 1); U = lp.flat(lat.bpst_links(3.0))
F = lp.field_strength(U); Q = lp.charge(U, F); sd = lp.selfduality(U, [(2, 4)], F); sd_report = lp.selfduality(U, [(4, 8)], F)
check("clover_Q_BPST_B12", abs(abs(Q)-1) < 0.1, Q)
check("selfduality_BPST_small_2to4a", all(v < 0.1 for v in sd.values()), dict(graded_shell=str(sd), report_4to8a=str(sd_report)))
anti = lp.selfduality(U, [(2, 4)], F, sign=-np.sign(Q))
check("anti_selfduality_large_for_wrong_sign", list(anti.values())[0] > 1.0, anti)
rho_est = lp.rho_moment(U, rmin=2.0); check("rho_moment_BPST_order_rho", 2.0 < rho_est < 4.5, rho_est)
lat = Lattice(4, 20, 6, 6, alpha=1.0); lp = Loops(lat, 1); U = lp.flat(lat.bpst_links(1.5)); rng = np.random.default_rng(5)
n, mv = lp.hessian_op(U, lam=0.0); x, y = rng.standard_normal(n), rng.standard_normal(n)
check("hessian_symmetric", abs(x@mv(y)-y@mv(x)) < 1e-4*abs(x@mv(y)), (x@mv(y), y@mv(x)))
fl = np.where(~lp.frozen)[0]; om = rng.standard_normal((lp.Ns, 3)); om[lp.bsite] = 0
U1 = np.tile([1., 0, 0, 0], (lp.NL, 1)); n, mv1 = lp.hessian_op(U1, lam=0.0); gv1 = lp.gauge_G(U1, om)[fl].ravel()
check("gauge_dir_zero_mode_vacuum", np.linalg.norm(mv1(gv1))/np.linalg.norm(gv1) < 1e-5, float(np.linalg.norm(mv1(gv1))/np.linalg.norm(gv1)))
Xr = rng.standard_normal((lp.NL, 3)); Xr[lp.frozen] = 0
check("gauge_G_GT_adjoint", abs(np.sum(lp.gauge_G(U, om)*Xr) - np.sum(om*lp.gauge_GT(U, Xr))) < 1e-8, None)
t0 = time.time(); vals, vecs = lp.lanczos(U1, k=4, lam=1.0, free_fn=run.free_ram_gb)
check("lanczos_vacuum_gaugefixed_positive", vals[0] > 1e-6, (vals.tolist(), round(time.time()-t0, 1)))
check("tip_weight_in_[0,1]", 0 <= lp.tip_weight(vecs[:, 0]) <= 1, lp.tip_weight(vecs[:, 0]))
try: lp.lanczos(U1, k=2, free_fn=lambda: 1.0); check("ram_guard_refuses", False, None)
except MemoryError: check("ram_guard_refuses", True, "MemoryError below 3.3 GB")
a = np.array([1/3, 1/4, 1/5]); rng = np.random.default_rng(2)
data = (1 + 0.7*a**2)[:, None] + 0.002*rng.standard_normal((3, 8))
bo = bootstrap_order(data, a, run.richardson_3pt)
check("bootstrap_order_recovers_2", bo['order'] is not None and bo['order_err'] is not None and abs(bo['order']-2) < 3*bo['order_err'], bo)
# ---- rev 15: cone-mapped seed unit tests (alpha<1) ----
def theta_spread(lat, U, lp):
    _, d = lp.action(U, per_site=True); worst = 0.0
    for n in range(lat.Mr-1):
        for k3 in (len(lat.x3)//2,):
            m = (lp.site_ring == n) & (lp.site_x3 == lat.x3[k3]) & (lp.site_x4 == lat.x4[len(lat.x4)//2])
            v = d[m]; worst = max(worst, float(np.std(v)/max(abs(np.mean(v)), 1e-30)))
    return worst
for al in (0.9, 0.75, 0.55, 0.5):
    lat = Lattice(*small, alpha=al); lp = Loops(lat, 1); c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2])
    L = lat.bpst_links(2.0, centre=c); U = lp.flat(L)
    check(f"cone_seed_unit_quaternions a={al}", np.max(np.abs(np.linalg.norm(U, axis=1)-1)) < 1e-12, float(np.max(np.abs(np.linalg.norm(U, axis=1)-1))))
    check(f"cone_seed_theta_invariant_across_glue a={al}", theta_spread(lat, U, lp) < 1e-8, theta_spread(lat, U, lp))
lat = Lattice(*small, alpha=0.55); lp = Loops(lat, 1); c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2]); lat.alpha = 1.0
Ubad = lp.flat(lat.bpst_links(2.0, centre=c)); lat.alpha = 0.55
check("cone_seed_negative_control_unmapped_breaks_glue", theta_spread(lat, Ubad, lp) > 1e-3, theta_spread(lat, Ubad, lp))
lat1 = Lattice(*small, alpha=1.0); lp1 = Loops(lat1, 1); c = (0., 0., lat1.x3[lat1.M3//2], lat1.x4[lat1.M4//2])
def indep_loop_trace(rho, c, corners, nrk=200):
    """Independent BPST check: RK4 path-ordered holonomy of A = Im(xbar dx)/(|x|^2+rho^2) round a closed
    straight-edged loop (gauge-invariant trace, so independent of the singular-gauge rotation and of lattice.link)."""
    def qm(a, b):
        return np.array([a[0]*b[0]-a[1:]@b[1:], *(a[0]*b[1:]+b[0]*a[1:]+np.cross(a[1:], b[1:]))])
    def w(x, dx):
        y = x-c; yb = np.array([y[0], -y[1], -y[2], -y[3]]); q = qm(yb, dx); return np.array([0., *q[1:]])/(y@y+rho**2)
    U = np.array([1., 0, 0, 0])
    for x0, x1 in zip(corners, corners[1:]+corners[:1]):
        dx = x1-x0; f = lambda t, U: qm(U, w(x0+t*dx, dx)); h = 1.0/nrk
        for i in range(nrk):
            t = i*h; k1 = f(t, U); k2 = f(t+h/2, U+h/2*k1); k3 = f(t+h/2, U+h/2*k2); k4 = f(t+h, U+h*k3); U = U+h/6*(k1+2*k2+2*k3+k4)
    return U[0]/np.linalg.norm(U)
lat1 = Lattice(*small, alpha=1.0); c = np.array((0., 0., lat1.x3[lat1.M3//2], lat1.x4[lat1.M4//2])); L1 = lat1.bpst_links(2.0, centre=c, nsub=64)
errs = []; errs_bad = []
for (n, j, k3, k4) in [(1, 3, 2, 3), (2, 7, 4, 4), (3, 12, 5, 3), (0, 0, 4, 5)]:
    U3, U4 = L1["d3"], L1["d4"]
    P = qmul(qmul(U3[n, j, k3, k4], U4[n, j, k3+1, k4]), qmul(qconj(U3[n, j, k3, k4+1]), qconj(U4[n, j, k3, k4])))
    r, th = lat1.r[n], j*lat1.dth; x = lambda a3, a4: np.array([r*np.cos(th), r*np.sin(th), lat1.x3[k3]+a3, lat1.x4[k4]+a4])
    cor = [x(0, 0), x(1, 0), x(1, 1), x(0, 1)]
    errs.append(abs(P[0]-indep_loop_trace(2.0, c, cor))); errs_bad.append(abs(P[0]-indep_loop_trace(2.6, c, cor)))
check("cone_seed_alpha1_matches_independent_BPST_holonomy", max(errs) < 1e-6 and min(errs_bad) > 1e-4, dict(max_err=max(errs), min_err_wrong_rho=min(errs_bad)))
for al in (1.0, 0.55):
    lat = Lattice(12, 20, 24, 24, alpha=al); lp = Loops(lat, 1); c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2]); U = lp.flat(lat.bpst_links(3.0, centre=c))
    Q = lp.charge(U, lp.field_strength(U)); check(f"cone_seed_charge_B12 a={al} (|Q|-1 within 0.15 [assumed])", abs(abs(Q)-1) < 0.15, Q)
# ---- cut IT1 runner and IT3 observed-order rule (rev 17) ----
check("it1_job_count_82_and_70_small_sample", len(run.it1_jobs("6+6")) == 123 and len(run.it1_jobs("3+3")) == 105 and sum(j[2] == run.IT1_D0_DRAW for j in run.it1_jobs()) == 15, (len(run.it1_jobs("6+6")), len(run.it1_jobs("3+3"))))
check("it1_jobs_diag21_16", len(run.it1_jobs_diag21()) == 16 and run.DIAG21_DELTA == 0.001 and run.DIAG21_BOXES == ("B10", "B12") and all(j[0] != "B14" for j in run.it1_jobs_diag21()), len(run.it1_jobs_diag21()))
check("it1_delta_candidates_rev21", run.IT1_DELTA_CANDIDATES == [0.001, 0.002, 0.003], run.IT1_DELTA_CANDIDATES)
check("it1_B14_grid_rho_4.2", run.BOXES["B14"] == (14, 20, 28, 28) and run.IT1_GRIDS == {"B10": 3.0, "B12": 3.6, "B14": 4.2} and run.IT1_BOX_ORDER == ("B10", "B12", "B14"), (run.BOXES["B14"], run.IT1_GRIDS))
check("it3_job_count_120_plus_3_bpst_refs", len(run.it3_jobs()) == 123 and sum(j[3] == "generic" for j in run.it3_jobs()) == 120, len(run.it3_jobs()))
check("it3_grids_rev16", run.IT3_GRIDS == {"B10": 3.0, "B12": 3.6, "B16": 4.8}, run.IT3_GRIDS)
hist = [(0.002*k, np.sqrt(9.0 + 0.7*0.002*k)) for k in range(0, 101, 5)] + [(0.3, 5.0)]
dr, n = run.it1_fit_drift(hist, 9.5); check("it1_fit_drift_recovers_slope_and_windows", abs(dr-0.7) < 1e-9 and n == 21, (dr, n))
# rev 19 smooth perturbation: reproducible, distinct, frozen untouched, smooth (low-k), theta-independent
latp = Lattice(8, 20, 16, 16, alpha=0.55); lpp = Loops(latp, 0); U0 = lpp.flat(latp.bpst_links(2.0))
X0, X0b, X1 = run.it1_smooth_field(lpp, 0), run.it1_smooth_field(lpp, 0), run.it1_smooth_field(lpp, 1)
P = run.it1_perturb(lpp, U0, 0, 0.01)
check("it1_smooth_reproducible_distinct_frozen", np.array_equal(X0, X0b) and not np.allclose(X0, X1) and np.all(X0[lpp.frozen] == 0) and np.allclose(P[lpp.frozen], U0[lpp.frozen]), None)
sl = slice(lpp.off["d3"], lpp.off["d4"]); t = lpp.tail[sl]; key = np.c_[lpp.site_ring[t], lpp.site_x3[t], lpp.site_x4[t]]
_, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel()
spread = max(float(np.ptp(X0[sl][inv == k_], axis=0).max()) for k_ in range(inv.max()+1))
check("it1_smooth_theta_independent", spread < 1e-12, spread)
Xd3 = X0[sl].reshape(-1, latp.M3, latp.M4, 3); jump = np.abs(np.diff(Xd3, axis=1)).max(); amp = np.abs(Xd3).max()
check("it1_smooth_low_k", jump < 0.5*amp, dict(max_neighbour_jump=float(jump), max_amp=float(amp)))
B = dict(monotone=True, Q_tf=-0.995, rho_tf=3.0)
def dd(q=-0.996, r=3.05, m=True, dr=1.0): return dict(monotone=m, Q_tf=q, rho_tf=r, drift=dr)
good = [dd(dr=1.0+0.01*k_) for k_ in range(6)]
check("pick_valid", run.pick_verdict(B, good)["valid"], run.pick_verdict(B, good))
check("pick_refuses_rho_shift_gt_5pct", not run.pick_verdict(B, good[:5]+[dd(r=3.2)])["valid"], run.pick_verdict(B, good[:5]+[dd(r=3.2)])["reason"])
check("pick_refuses_zero_spread", "spread" in run.pick_verdict(B, [dd(dr=1.0)]*6)["reason"], run.pick_verdict(B, [dd(dr=1.0)]*6)["reason"])
B2 = dict(B, Q_tf=-0.9437); good2 = [dd(q=-0.9437, dr=1.0+0.01*k_) for k_ in range(6)]; v2 = run.pick_verdict(B2, good2)
check("pick_absQ_report_only_rev20", v2["valid"] and abs(v2["absQ_report"]["base"]-0.0563) < 1e-9, v2["absQ_report"])
check("pick_refuses_Q0_shift", "Q_0" in run.pick_verdict(dict(B, Q_tf=-0.975), good[:5]+[dd(q=-0.99)])["reason"], None)
check("pick_refuses_nonmonotone", "monotone" in run.pick_verdict(B, good[:5]+[dd(m=False)])["reason"], None)
_lin_ok = run.pick_linearity(dict(drift=0.0), {"0.001": dict(drift=[1.0]*6), "0.002": dict(drift=[2.0]*6), "0.003": dict(drift=[3.1]*6)})
_lin_bad = run.pick_linearity(dict(drift=0.0), {"0.001": dict(drift=[1.0]*6), "0.002": dict(drift=[4.0]*6)})
check("pick_linearity_in_band_report_only", _lin_ok["ok"] is True and abs(_lin_ok["ratio"]-2.0) < 1e-12, _lin_ok)
check("pick_linearity_out_of_band_still_report_only", _lin_bad["ok"] is False and abs(_lin_bad["ratio"]-4.0) < 1e-12, _lin_bad)
try: run.it1_perturb(lpp, U0, 0); check("it1_delta_unset_refuses", False, "no raise")
except RuntimeError as e: check("it1_delta_unset_refuses", run.IT1_DELTA is None, str(e))
def fake(box, al, draw, d, **kw):
    rec = dict(box=box, alpha=al, draw=draw, drift=d); rec.update(kw); return rec
rng = np.random.default_rng(7)
def rows(delta_fn, b_offset=0.0, paired=True, d0_shift=0.0):
    R = []
    for b in run.IT1_GRIDS:
        for d in run.IT1_DRAWS_A:
            base = 1.0 + 0.1*rng.standard_normal(); R.append(fake(b, 1.0, d, base))
            for al in run.IT1_ALPHAS[1:]: R.append(fake(b, al, d, (base if paired else 1.0 + 0.1*rng.standard_normal()) + delta_fn(b, al) + 0.01*rng.standard_normal()))
        for d in run.IT1_DRAWS_B: R.append(fake(b, 1.0, d, 1.0 + b_offset + 0.1*rng.standard_normal()))
        for al in run.IT1_ALPHAS: R.append(fake(b, al, run.IT1_D0_DRAW, 0.7 + delta_fn(b, al) + d0_shift*(1-al),
                                               drift_h1=0.70, drift_h2=0.70, n_h1=6, n_h2=6, window_disagree_flag=False))
    return R
CAL = {b: dict(rel_shift=0.02) for b in run.IT1_GRIDS}
g0 = run.it1_grade_rows(rows(lambda b, al: 0.0), CAL, "6+6"); g0s = run.it1_grade_rows(rows(lambda b, al: 0.0), CAL, "3+3")
check("it1_guard_6+6_bound_3sigma1_sqrt_1_3", abs(g0["guard"]["B10"]["bound"] - 3*g0["guard"]["B10"]["sigma1"]*np.sqrt(1/3)) < 1e-12 and g0["guard"]["B10"]["ok"], g0["guard"]["B10"])
check("it1_guard_3+3_bound_small_sample", "small sample" in g0s["guard_mode"] and abs(g0s["guard"]["B10"]["bound"] - 3*g0s["guard"]["B10"]["sigma1"]*np.sqrt(2/3)) < 1e-12, g0s["guard"]["B10"])
check("it1_grade_null_AGAINST_paired", g0["paired"] and all(v["verdict"].startswith("AGAINST") for v in g0["alphas"].values()), g0["pairing"]["B10"])
check("it1_delta0_control_passes_on_null", g0["delta0_control_pass"] and g0["delta0_control"]["B10"]["0.55"]["ok"] and abs(g0["delta0_control"]["B10"]["drift_shift_by_delta_alpha1"]["value"]) > 0.2, g0["delta0_control"]["B10"]["0.55"])
gd = run.it1_grade_rows(rows(lambda b, al: 0.0, d0_shift=5.0), CAL)
check("it1_delta0_control_fails_makes_report_only", (not gd["delta0_control_pass"]) and gd["status"].startswith("REPORT-ONLY") and gd["guard"]["B10"]["ok"], gd["delta0_control"]["B12"]["0.55"])
check("it1_guard_pass_tracks_alpha1_only", gd["guard_pass"] is True and (not gd["delta0_control_pass"]) and "delta0_control" in gd["fail_reasons"], gd["fail_reasons"])
hw = [(0.002*k_, np.sqrt(9.0 + 0.7*0.002*k_)) for k_ in range(0, 51, 5)]; w2 = run.it1_window2(hw, 9.5)
hk = [(0.002*k_, np.sqrt(9.0 + 0.7*min(k_, 25)*0.002 + 3.0*max(k_-25, 0)*0.002)) for k_ in range(0, 51, 5)]; wk = run.it1_window2(hk, 9.5)
check("it1_disjoint_half_windows_flag", (not w2["flag"]) and abs(w2["drift_h1"]-0.7) < 1e-9 and abs(w2["drift_h2"]-0.7) < 1e-9 and w2["n_h1"] == 6 and w2["n_h2"] == 6
      and wk["flag"] and abs(wk["drift_h1"]-0.7) < 1e-9 and abs(wk["drift_h2"]-3.0) < 1e-9 and run.IT1_GUARD_MODE == "6+6", dict(linear=(w2["drift_h1"], w2["drift_h2"]), kinked=(wk["drift_h1"], wk["drift_h2"])))
# rev 21 windows [T,1.5T] and [1.5T,2T] on absolute hist times
_hT = [(0.002*k_, np.sqrt(9.0 + 0.7*0.002*k_)) for k_ in range(0, 201)]
_wp = run.it1_window_pair(_hT, 9.5, 0.1)
check("it1_window_pair_T_windows", (not _wp["flag"]) and _wp["settled"] and abs(_wp["drift_h1"]-0.7) < 1e-9 and abs(_wp["drift_h2"]-0.7) < 1e-9 and abs(_wp["T"]-0.1) < 1e-15, _wp)
_hkT = []
_r2 = 9.0
for k_ in range(0, 401):
    t_ = 0.002*k_; _hkT.append((t_, np.sqrt(_r2))); _r2 += (3.0 if t_ < 0.16 else 0.7)*0.002
_ch = run.it1_choose_T(_hkT, 9.5, 0.1)
check("it1_choose_T_raises_past_kink", _ch["settled"] is True and _ch["T"] > 0.1 and _ch["windows"]["rel"] is not None and _ch["windows"]["rel"] < run.IT1_WIN_SETTLE, _ch)
_ch_cap = run.it1_choose_T(_hkT, 9.5, 0.1, t_max_over=1.0)
check("it1_choose_T_diag21_cap_at_3tf_style", _ch_cap["settled"] is False and abs(_ch_cap["T"]-0.1) < 1e-12, _ch_cap)
g1 = run.it1_grade_rows(rows(lambda b, al: 1.0*(1-al)), CAL)
check("it1_grade_large_Delta_not_AGAINST", all(v["verdict"].startswith("UNDECIDED") for v in g1["alphas"].values()), {k: round(v["Delta_inf_p4"], 3) for k, v in g1["alphas"].items()})
check("it1_3grid_fallback_p4_assumed", "3-grid order not measurable" in g1["alphas"]["0.55"]["order_gate"] and g1["alphas"]["0.55"]["order"] is None, g1["alphas"]["0.55"]["order_gate"])
g4 = run.it1_grade_rows(rows(lambda b, al: (0.2 + 5000.0/run.BOXES[b][0]**4)*(1-al)), CAL)
_o55 = g4["alphas"]["0.55"]
check("it1_3grid_order_measured_near_4", _o55.get("order") is not None and abs(_o55["order"]-4) < 0.5 and "3-grid" in _o55["order_gate"] and "measured" in _o55["order_gate"] and _o55.get("Delta_B14") is not None, dict(order=_o55.get("order"), gate=_o55.get("order_gate"), D10=_o55.get("Delta_B10"), D12=_o55.get("Delta_B12"), D14=_o55.get("Delta_B14")))
g2 = run.it1_grade_rows(rows(lambda b, al: 0.0, b_offset=5.0), CAL)
check("it1_guard_fails_when_sets_disagree", (not g2["guard_pass"]) and g2["status"].startswith("REPORT-ONLY"), g2["guard"]["B10"])
gu = run.it1_grade_rows(rows(lambda b, al: 0.0, paired=False), CAL)
check("it1_unpaired_fallback_when_corr_lt_0.5", (not gu["paired"]) and abs(gu["grids"]["B12"]["0.55"]["var_term"] - gu["grids"]["B12"]["0.55"]["sigma"]**2/3) < 1e-15, gu["pairing"]["B12"])
a55 = g1["alphas"]["0.55"]; slope_exp = abs(np.log(a55["Delta_B12"]/a55["Delta_B10"])/np.log(3.6/3.0))
check("it1_cal_term_measured_slope", a55["cal_slope_tag"].startswith("[measured") and abs(a55["cal_slope"]-slope_exp) < 1e-12 and abs(a55["E_a_cal_sys"]-slope_exp*0.02*abs(a55["Delta_B12"])) < 1e-12, (a55["cal_slope"], a55["E_a_cal_sys"]))
gs = run.it1_grade_rows(rows(lambda b, al: (0.3 if b == "B10" else -0.3)*(1-al)), CAL)
check("it1_cal_slope_default_2_on_sign_change", gs["alphas"]["0.55"]["cal_slope"] == 2.0 and gs["alphas"]["0.55"]["cal_slope_tag"] == "[assumed]", None)
import os as _os, json as _json, inspect as _inspect, shutil as _shutil, glob as _glob
g3 = run.it1_grade_rows(rows(lambda b, al: 0.0), None)
check("it1_cal_rows_required", "cal_missing" in g3["fail_reasons"] and g3["status"].startswith("REPORT-ONLY") and g3["guard_pass"] is True, g3["fail_reasons"])
check("it1_grade_label_rev21", "rev 21" in g0["test"], g0["test"])
check("it1_grade_delta_from_frozen", g0["delta"] is not None and abs(g0["delta"]-0.005) < 1e-15, g0["delta"])
check("it1_grade_delta_none_without_frozen", run.it1_grade_rows(rows(lambda b, al: 0.0), CAL, frozen_fn=_os.path.join(run.HERE, "out", "_no_such_frozen.json"))["delta"] is None, None)
check("it1_grade_records_delta0_windows", g0["delta0_control"]["B10"]["windows_delta0"]["0.55"]["drift_h1"] == 0.70 and g0["delta0_control"]["B10"]["windows_delta0"]["0.55"]["flag"] is False, g0["delta0_control"]["B10"]["windows_delta0"]["0.55"])
_frozen = run.FROZEN_PATH
_fbak = _frozen + ".bak_test"
_had_fr = _os.path.exists(_frozen)
if _had_fr: _os.replace(_frozen, _fbak)
try:
    try: run.it1_delta_gate(); check("it1_gate_refuses_without_delta_check", False, "no raise")
    except RuntimeError as e: check("it1_gate_refuses_without_delta_check", True, str(e))
    try: run.it1_row("B10", 1.0, 0); check("it1_row_refuses_without_frozen", False, "no raise")
    except RuntimeError as e: check("it1_row_refuses_without_frozen", "delta_frozen" in str(e) or "frozen" in str(e).lower(), str(e))
finally:
    if _had_fr and not _os.path.exists(_frozen): _os.replace(_fbak, _frozen)
    elif _os.path.exists(_fbak) and _os.path.exists(_frozen): _os.remove(_fbak)

def _write_pick_box(indir, box, passing, smoke=False, Q0=-0.94, rho0=3.09):
    d = _os.path.join(run.HERE, "out", indir); _os.makedirs(d, exist_ok=True)
    base = dict(box=box, delta=None, draw=-1, monotone=True, Q_tf=Q0, rho_tf=rho0, drift=-3.7, n_fit=11, smoke=smoke, spec=run.FINAL_SPEC_HASH)
    open(_os.path.join(d, f"{box}_base.json"), "w").write(_json.dumps(base))
    for dl in run.IT1_DELTA_CANDIDATES:
        for r in range(run.IT1_SEEDS):
            ok = dl in passing
            rec = dict(box=box, delta=dl, draw=r, monotone=True,
                       Q_tf=Q0 + (0.0 if ok else 0.05), rho_tf=rho0*(1 + (0.001 if ok else 0.10)*r),
                       drift=(1.0 + 0.1*r) if ok else 1.0, n_fit=11, smoke=smoke, spec=run.FINAL_SPEC_HASH)
            open(_os.path.join(d, f"{box}_d{dl}_r{r}.json"), "w").write(_json.dumps(rec))

def _stash(paths):
    bak = {}
    for p in paths:
        if _os.path.exists(p):
            q = p + ".bak_test"; _os.replace(p, q); bak[p] = q
    return bak
def _unstash(bak):
    for p, q in bak.items():
        if _os.path.exists(p): _os.remove(p)
        if _os.path.exists(q): _os.replace(q, p)

_grade_paths = [_os.path.join(run.HERE, "out", f"it1_pick_grade_{b}.json") for b in ("B10", "B12")] + [_os.path.join(run.HERE, "out", "it1_pick_grade.json"), _frozen]
_bak = _stash(_grade_paths)
try:
    # per-box grade files from synthetic pick rows (reuse pick schema; no flow rerun)
    _write_pick_box("_t_pick", "B10", {0.001, 0.002}, smoke=False)
    _write_pick_box("_t_pick", "B12", {0.002, 0.003}, smoke=False)
    g10 = run.it1_pick_grade(indir="_t_pick", box="B10")
    g12 = run.it1_pick_grade(indir="_t_pick", box="B12")
    p10 = _os.path.join(run.HERE, "out", "it1_pick_grade_B10.json")
    p12 = _os.path.join(run.HERE, "out", "it1_pick_grade_B12.json")
    check("it1_pick_grade_writes_per_box_B10", _os.path.exists(p10) and _json.load(open(p10))["box"] == "B10", p10)
    check("it1_pick_grade_writes_per_box_B12", _os.path.exists(p12) and _json.load(open(p12))["box"] == "B12", p12)
    check("it1_pick_grade_box_not_stuck_on_B10", g12["box"] == "B12" and g10["box"] == "B10", (g10.get("chosen"), g12.get("chosen")))
    check("it1_pick_grade_records_linearity", g10.get("linearity") is not None and "ratio" in g10["linearity"] and "report-only" in (g10["linearity"].get("note") or ""), g10.get("linearity"))
    tdir = _os.path.join(run.HERE, "out", "_t_freeze"); _os.makedirs(tdir, exist_ok=True)
    _shutil.copy(p10, _os.path.join(tdir, "it1_pick_grade_B10.json"))
    _shutil.copy(p12, _os.path.join(tdir, "it1_pick_grade_B12.json"))
    fz = _os.path.join(tdir, "delta_frozen.json")
    rc = run.it1_freeze(grade_dir=tdir, outfile=fz)
    fr = _json.load(open(fz))
    check("it1_freeze_picks_largest_common_delta", rc == 0 and abs(fr["delta"]-0.002) < 1e-15, fr)
    check("it1_freeze_records_rule_rows_hashes", "BOTH" in fr["rule"] and "B10" in fr["boxes"] and "B12" in fr["boxes"] and fr["spec"] == run.FINAL_SPEC_HASH and "run_py" in fr, {k: fr["boxes"][k]["valid"] for k in fr["boxes"]})
    check("it1_row_accepts_with_frozen", abs(run.it1_resolve_delta(0, fn=fz)-0.002) < 1e-15 and run.it1_load_frozen(fz)["delta"] == fr["delta"], run.it1_resolve_delta(0, fn=fz))
    check("it1_delta0_control_unchanged_with_frozen", run.it1_resolve_delta(run.IT1_D0_DRAW, fn=fz) == 0.0, run.it1_resolve_delta(run.IT1_D0_DRAW, fn=fz))
    # NO_DELTA: disjoint passing sets
    _write_pick_box("_t_pick_none", "B10", {0.001}, smoke=False)
    _write_pick_box("_t_pick_none", "B12", {0.003}, smoke=False)
    run.it1_pick_grade(indir="_t_pick_none", box="B10")
    run.it1_pick_grade(indir="_t_pick_none", box="B12")
    ndir = _os.path.join(run.HERE, "out", "_t_nodelta"); _os.makedirs(ndir, exist_ok=True)
    _shutil.copy(_os.path.join(run.HERE, "out", "it1_pick_grade_B10.json"), _os.path.join(ndir, "it1_pick_grade_B10.json"))
    _shutil.copy(_os.path.join(run.HERE, "out", "it1_pick_grade_B12.json"), _os.path.join(ndir, "it1_pick_grade_B12.json"))
    nfn = _os.path.join(ndir, "delta_frozen.json")
    rc2 = run.it1_freeze(grade_dir=ndir, outfile=nfn)
    check("it1_freeze_NO_DELTA_when_none_passes", rc2 == 1 and not _os.path.exists(nfn), rc2)
    # smoke-built freeze is refused by the gate
    sm = dict(delta=0.01, smoke=True, rule="test", spec=run.FINAL_SPEC_HASH)
    sfn = _os.path.join(tdir, "delta_smoke.json"); open(sfn, "w").write(_json.dumps(sm))
    try: run.it1_load_frozen(sfn); check("it1_gate_refuses_smoke_frozen", False, "no raise")
    except RuntimeError as e: check("it1_gate_refuses_smoke_frozen", "smoke" in str(e).lower(), str(e))
    check("it1_row_save_evecs_flag", "save_evecs" in _inspect.signature(run.it1_row).parameters, None)
finally:
    _unstash(_bak)
    # drop canonical grade/freeze the tests just wrote if they weren't stashed
    for p in _grade_paths:
        if p not in _bak and _os.path.exists(p): _os.remove(p)
# re-grade saved out/it1/*.json (no flow rerun)
_it1dir = _os.path.join(run.HERE, "out", "it1")
_it1fs = [f for f in _glob.glob(_os.path.join(_it1dir, "*.json")) if not _os.path.basename(f).startswith("cal_")]
if len(_it1fs) >= 80:
    _R = [_json.load(open(f)) for f in _it1fs]
    _cal = {_json.load(open(f))["box"]: _json.load(open(f)) for f in _glob.glob(_os.path.join(_it1dir, "cal_*.json"))}
    gv = run.it1_grade_rows(_R, _cal)
    check("it1_saved_guard_pass_true", gv["guard_pass"] is True and gv["guard"]["B10"]["ok"] is True and gv["guard"]["B12"]["ok"] is True, gv["guard"])
    check("it1_saved_delta_from_frozen", gv["delta"] is not None and abs(gv["delta"]-0.005) < 1e-15, gv["delta"])
    check("it1_saved_label_rev21", "rev 21" in gv["test"], gv["test"])
    check("it1_saved_fail_reason_is_delta0", gv["fail_reasons"] == ["delta0_control"] and not gv["delta0_control_pass"], gv["fail_reasons"])
    w12 = gv["delta0_control"]["B12"]["windows_delta0"]
    check("it1_saved_B12_windows_all_flagged", len(w12) == 5 and all(w12[a]["flag"] for a in w12) and w12["1.0"]["drift_h1"] is not None, {a: (w12[a].get("drift_h1"), w12[a].get("drift_h2"), w12[a].get("flag")) for a in w12})
    d09 = gv["delta0_control"]["B10"]["0.9"]
    check("it1_saved_delta0_ratio_recorded", d09.get("ratio") is not None and d09["abs_diff"] > d09["bound"] and d09["ok"] is False, d09)
else:
    check("it1_saved_rows_present", False, len(_it1fs))
check("it1_explicit_delta_skips_freeze", abs(run.it1_resolve_delta(0, 0.001)-0.001) < 1e-15 and run.it1_resolve_delta(run.IT1_D0_DRAW, 0.001) == 0.0, None)
check("it1_row_path_lin_suffix", "delta0.002" in run.it1_row_path("B10", 1.0, 0, "diag21/it1", delta=0.002) and "delta0.002" not in run.it1_row_path("B10", 1.0, 0, "diag21/it1", delta=0.001), run.it1_row_path("B10", 1.0, 0, "diag21/it1", delta=0.002))
_skipd = _os.path.join(run.HERE, "out", "_t_skip", "it1"); _os.makedirs(_skipd, exist_ok=True)
_skipp = run.it1_row_path("B10", 1.0, 0, "_t_skip/it1", delta=0.001)
open(_skipp, "w").write(_json.dumps(dict(box="B10", alpha=1.0, draw=0, drift=-9.0, delta=0.001, marker="kept")))
_sk = run.it1_row("B10", 1.0, 0, outdir="_t_skip/it1", delta=0.001, skip_existing=True)
check("it1_row_skip_existing", _sk.get("marker")=="kept" and _json.load(open(_skipp))["marker"]=="kept", _sk)
_ftskip = _os.path.join(run.HERE, "out", "_t_skip", "it1_T.json")
open(_ftskip, "w").write(_json.dumps(dict(boxes=dict(B12=dict(T=0.288, t_f=0.144, marker="kept")))))
_fts = run.it1_find_T("B12", skip_existing=True, path=_ftskip)
check("it1_find_T_skip_existing", _fts.get("marker")=="kept" and _json.load(open(_ftskip))["boxes"]["B12"]["marker"]=="kept", _fts)
_calskip = _os.path.join(run.HERE, "out", "_t_skip", "it1", "cal_B10.json")
open(_calskip, "w").write(_json.dumps(dict(box="B10", marker="kept")))
_cs = run.it1_cal("B10", outdir="_t_skip/it1", skip_existing=True)
check("it1_cal_skip_existing", _cs.get("marker")=="kept" and _json.load(open(_calskip))["marker"]=="kept", _cs)
_frzskip = _os.path.join(run.HERE, "out", "_t_skip", "delta_frozen.json")
open(_frzskip, "w").write(_json.dumps(dict(delta=0.001, marker="kept")))
_frc = run.it1_freeze(outfile=_frzskip, skip_existing=True)
check("it1_freeze_skip_existing", _frc == 0 and _json.load(open(_frzskip))["marker"]=="kept", _frc)
_tp = _os.path.join(run.HERE, "out", "_t_ratio", "it1_T.json"); _os.makedirs(_os.path.dirname(_tp), exist_ok=True)
open(_tp, "w").write(_json.dumps(dict(boxes=dict(B12=dict(T=0.288, t_f=0.144, settled=True, t_max=0.432)))))
_ar = run.it1_apply_T_ratio("B12", ["B10", "B12"], path=_tp)
check("it1_apply_T_ratio_copies_B12_to_B10", abs(_ar["ratio"]-2.0) < 1e-12 and abs(_ar["T"]["B10"]-2.0*run.flow_tf(3.0)) < 1e-12 and abs(_ar["T"]["B12"]-0.288) < 1e-12, _ar)
_d21 = _os.path.join(run.HERE, "out", "_t_d21", "it1"); _os.makedirs(_d21, exist_ok=True)
for _b in ("B10", "B12"):
    open(_os.path.join(_d21, f"cal_{_b}.json"), "w").write(_json.dumps(dict(test="IT1-cal", box=_b, rel_shift=0.02)))
    for _d in range(3):
        open(_os.path.join(_d21, f"{_b}_a1.0_d{_d}.json"), "w").write(_json.dumps(dict(box=_b, alpha=1.0, draw=_d, drift=1.0+0.01*_d, delta=0.001)))
        open(_os.path.join(_d21, f"{_b}_a0.5_d{_d}.json"), "w").write(_json.dumps(dict(box=_b, alpha=0.5, draw=_d, drift=1.2+0.01*_d, delta=0.001)))
    open(_os.path.join(_d21, f"{_b}_a1.0_delta0.json"), "w").write(_json.dumps(dict(box=_b, alpha=1.0, draw=-1, drift=0.7, delta=0.0, drift_h1=0.70, drift_h2=0.68, window_disagree_flag=False, window_rel=0.029, window_settled=True, T=0.2)))
    open(_os.path.join(_d21, f"{_b}_a0.5_delta0.json"), "w").write(_json.dumps(dict(box=_b, alpha=0.5, draw=-1, drift=0.9, delta=0.0, drift_h1=0.70, drift_h2=0.68, window_disagree_flag=False, window_rel=0.029, window_settled=True, T=0.2)))
for _d in range(3):
    open(_os.path.join(_d21, f"B10_a1.0_d{_d}_delta0.002.json"), "w").write(_json.dumps(dict(box="B10", alpha=1.0, draw=_d, drift=1.3+0.02*_d, delta=0.002)))
_g21 = run.it1_diag21_grade(indir="_t_d21/it1", outfile=_os.path.join(run.HERE, "out", "_t_d21", "it1_grade.json"), t_path=_tp)
check("it1_diag21_grade_report_only_no_verdict", _g21["status"].startswith("REPORT-ONLY") and "verdict" not in _g21 and _g21.get("note") and "no AGAINST" in _g21["note"], _g21["status"])
check("it1_diag21_grade_delta0_and_windows", _g21["delta0_control_pass"] is True and _g21["delta0_control"]["B10"]["0.5"]["ok"] is True and _g21["windows"]["B12"]["1.0"]["rel"] == 0.029, _g21["delta0_control"]["B10"]["0.5"])
check("it1_diag21_grade_linearity_ratio", _g21["linearity"]["ratio"] is not None and _g21["delta"] == 0.001 and "deviation" in _g21["delta_note"], _g21["linearity"])
_chp = open(_os.path.join(run.HERE, "chain.ps1"), encoding="utf-8").read()
check("chain_diag21_and_resume_and_notify", ("-Diag21" in _chp) and ("skip-existing" in _chp) and ("notify.ps1" in _chp) and ("if($Smoke -or $NoNotify)" in _chp) and ("it1-diag21-grade" in _chp) and ("--delta 0.001" in _chp) and ("FIND_T_B12" in _chp) and ("B14" in _chp) and ("--outdir diag21" in _chp) and ("-GradeFile" in _chp) and ("--flow-max-over 6" in _chp) and ("--t-max-over 3" in _chp), None)
check("chain_notify_skipped_on_smoke", "if($Smoke -or $NoNotify){ return }" in _chp.replace(" ", "").replace("return", " return ") or "if($Smoke -or $NoNotify){ return }" in _chp, None)
check("chain_diag21_findT_before_freeze", _chp.find("FIND_T_B12") < _chp.find("it1-diag21-grade") < _chp.find("it1-freeze$od$skip") and "foreach($b in 'B10','B12','B14')" in _chp, None)
Ns = [10, 12, 16]; h = np.array([1/n for n in Ns])
p4 = run.observed_order(list(0.2 + 50*h**4), Ns); p1 = run.observed_order(list(0.2 + 0.5*h), Ns)
check("observed_order_recovers_4", p4 is not None and abs(p4-4) < 1e-6, p4)
check("observed_order_recovers_1", p1 is not None and abs(p1-1) < 1e-6, p1)
def g3(vals):
    G = {b: {"0.9": dict(s_minus_s1=v, s_minus_sBPST=v)} for b, v in zip(run.IT3_GRIDS, vals)}
    return run.it3_verdicts(G)["verdict_alpha_0.9"]
va = g3(list(0.3 + 50*h**4)); vb = g3(list(0.3 + 0.5*h)); vc = g3([0.3, 0.1, 0.25])
check("it3_order_in_window_grades", va["verdict"].startswith("AGAINST") and abs(va["d_inf"]-0.3) < 0.01, (va["verdict"], va.get("d_inf")))
check("it3_order_outside_window_undecided", vb["verdict"].startswith("UNDECIDED"), (vb["verdict"], vb["observed_order"]))
check("it3_nonmonotone_undecided", vc["verdict"].startswith("UNDECIDED") and vc["observed_order"] is None, vc["verdict"])
# ---- diag22 / Venus H10 regression ----
_p0 = run.it1_row_path("B10", 1.0, -1, "diag22/it1", delta=None); _pa = run.it1_row_path("B10", 1.0, 0, "diag22/it1", delta=0.003); _pb = run.it1_row_path("B10", 1.0, 0, "diag22/it1", delta=0.0015)
check("h10_diag22_paths_distinct", len({_p0, _pa, _pb}) == 3, (_p0, _pa, _pb))
check("h10_legacy_paths_unchanged", run.it1_row_path("B10", 1.0, 0, "diag21/it1", delta=0.001).endswith("B10_a1.0_d0.json"), None)
try: run.diag22_check_row_key(0, 0.0); check("h10_delta_row_with_zero_refused", False, None)
except ValueError: check("h10_delta_row_with_zero_refused", True, None)
try: run.diag22_check_row_key(-1, 0.003); check("h10_control_with_delta_refused", False, None)
except ValueError: check("h10_control_with_delta_refused", True, None)
def _r22(al, d, dl, drift, wr=0.05): return dict(alpha=al, draw=d, delta=dl, drift=drift, window_rel=wr)
_R = [_r22(1.0, -1, 0.0, 1.0), _r22(0.5, -1, 0.0, 1.5)]
for _d in range(2):
    _R += [_r22(1.0, _d, 0.0015, 1.1+0.001*_d), _r22(1.0, _d, 0.003, 1.2+0.001*_d), _r22(0.5, _d, 0.0015, 1.6+0.002*_d), _r22(0.5, _d, 0.003, 1.7+0.003*_d)]
_g = run.diag22_grade_rows(_R, dict(rel_shift=0.01, T=0.3))
check("diag22_grade_pass_and_linearity", _g["status"] == "PASS" and abs(_g["criteria"]["linearity"]["ratio"]-2.0) < 0.05 and _g["n_rows"] == 10 and not _g["missing"], _g["status"])
_bad = [dict(r) for r in _R]; _bad[0]["window_rel"] = 0.2
check("diag22_grade_window_fail_report_only", run.diag22_grade_rows(_bad, dict(rel_shift=0.01))["status"].startswith("REPORT-ONLY"), None)
check("diag22_grade_cal_fail", run.diag22_grade_rows(_R, dict(rel_shift=0.06))["criteria"]["rho_cal_shift"]["ok"] is False, None)
try: run.diag22_grade_rows(_R + [_r22(1.0, 0, 0.003, 9.9)], None); check("h10_duplicate_row_refused", False, None)
except ValueError: check("h10_duplicate_row_refused", True, None)
_ctl_alias = [dict(r) for r in _R]   # delta=0 control copied into a delta row slot must be refused, not graded
_ctl_alias[2] = dict(_R[0], draw=0)
try: run.diag22_grade_rows(_ctl_alias, None); check("h10_control_copied_into_delta_row_refused", False, None)
except ValueError: check("h10_control_copied_into_delta_row_refused", True, None)
_f = run.tip_fit([8, 10, 12, 16], [3.0*n**2.5 for n in (8, 10, 12, 16)])
check("tip_fit_recovers_p_dof2", abs(_f["p"]-2.5) < 1e-9 and _f["dof"] == 2 and _f["p_err"] < 1e-6, _f)
check("tip_thresholds_missing_report_only", run.TIP_THRESHOLDS is None and len(run.diag22_jobs()) == 10, None)
nf = sum(1 for v in RES.values() if not v[0]); print(f"{len(RES)-nf}/{len(RES)} passed"); sys.exit(1 if nf else 0)

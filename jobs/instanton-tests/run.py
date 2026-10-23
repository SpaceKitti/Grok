"""INSTANTON_TESTS runner (Aethon). Outputs change ONLY through this file.
Modes:  smoke   -> SCRATCH timing smoke + two report-only flat-space checks (H5: scratch, not graded)
        graded  -> refused unless --launch-authorised AND every kernel it needs is implemented.
All thresholds/predictions are fixed below BEFORE any run; every printed number comes from a variable.
"""
import argparse, hashlib, json, os, platform, sys, time, ctypes
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lattice import Lattice

FINAL_SPEC_HASH = "2AD8FA1A"          # INSTANTON_TESTS rev 21
HOLD_REV12 = False                     # rev 14 releases graded rows (gated below)
INV_A_CHECK = "FAIL"                   # rev 14 can-fail 1/a check verdict: None (not run) / "PASS" / "FAIL"; FAIL => p_box UNDECIDED, no IT4
SPEC_PATH = os.path.join(HERE, "spec", "INSTANTON_TESTS.md")
NCY = "NOT COMPUTED (YET)"

# ---------------- fixed before any run (spec rev 11) ----------------
ALPHAS = [1.0, 0.9, 0.75, 0.55, 0.5]          # 0.5 = [orbifold, C/Z2, 1/2-charge allowed], never pooled
ORBIFOLD = 0.5
EPS_ROWS = {1: "[Wilson, inward control]", 0: "[outward, +2/35 (a/rho)^4]", -1: "[paper's over-improved, outward]", -0.25: "[hive row, labelled]"}
L_PHI = 20
BOXES = {"B10": (10, 20, 20, 20), "B12": (12, 20, 24, 24), "B14": (14, 20, 28, 28), "B16": (16, 20, 32, 32), "B20": (20, 20, 40, 40)}
N1PHI = (12, 40, 24, 24)
SEEDS = 8
RHO_OVER_A_FLOOR = 3.0                         # [assumed]
GRADE_R_MIN_A = 2.0
# IT1
K_DELTA = 3.0                                  # [assumed]
WIN_ONTIP = 0.3; WIN_OFFTIP = 0.4              # [assumed]
A_SERIES_ONTIP = {"B12": 3.0, "B16": 4.0, "B20": 5.0}   # rho/a at rho/l = 1/4
OFFTIP = {"B16": dict(d0=10.5, rho=4.2, graded=True, centre_from_face=5.0), "B20": dict(d0=12.5, rho=5.0, graded=True, centre_from_face=7.0),
          "B12": dict(d0=10.0, rho=3.0, graded=False, note="report-only; centre 2a from face; out of order estimate")}
P_A_EXPECTED = {1: 2, -1: 2, 0: 4, -0.25: 2}  # rev 10/11 per-eps gate [assumed, not measured]
IT1_PRED = "|Delta(alpha)| <= k_Delta*E for alpha in {0.9,0.75,0.55} at every eps; drift signs at alpha=1: inward eps=1, outward eps=0,-1,-0.25"
REPRO_TOL = 0.10                               # [assumed]
# IT2
TAU_FACTOR = 3.0                               # tau = 3 E_a(Q) [assumed]
IT2_PRED = "|Q - nearest integer| <= tau after a->0 at generic alpha; Q in Z/2 within tau at alpha=0.5; density peak at r>=2a following the centre"
# IT3
S_SELFDUAL = None; S_NOT_SELFDUAL = 0.10; GRID_STAB = 0.20   # [assumed]; absolute S_SELFDUAL withdrawn rev 13 (see SD_REL_CUT)
IT3_SHELLS_A = [2, 4, 8]
# IT4
IT4_BOXES = ["B10", "B12", "B16"]; IT4_RHO_A = 3.0; IT4_OPT_B16_RHO_A = 4.0
LANCZOS_VECTORS = 30; WORKSPACE_FACTOR = 2
P_BOX_TAG = "[measured, flowed smoke][face artefact rho^4/(a l^3), not physical box cost]; l->inf extrapolation only"
P_BOX_EPS = {1: (3.006, 0.025), 0: (2.904, 0.028), -1: (2.818, 0.031), -0.25: (2.881, 0.029)}   # rev 14 frozen, per eps
S_INF_CHECK_EPS1 = 0.9827                       # extrapolation must reproduce this at eps=1
P_BOX = None                                    # legacy single value unused; use P_BOX_EPS
FLOW_STEP = 0.002                              # rev 13 eps_f [assumed] (0.01, 0.005 unstable [measured])
FLOW_STEP_CHECK = 0.001                        # rev 13 rerun on B10, must agree to < E_Delta/3
FLOW_TF = 0.1                                  # rev 13 t_f = 0.1 a^2: WITHDRAWN for graded rows (rev 15); scratch re-smoke only
FLOW_TF_RHO_DIV = 90.0                         # rev 15: graded t_f = rho^2/90 [assumed, frozen; Venus]
def flow_tf(rho): return rho**2/FLOW_TF_RHO_DIV
SD_REL_CUT = 0.02                              # rev 13: s_meas - s_BPST <= 0.02 [assumed]; absolute cut withdrawn
RHO_CAL_RHOS = [3.0, 4.0, 5.0]; RHO_CAL_VAR = 0.05   # rev 13 calibration on exact BPST; >5% variation => interpolate, tagged
FACE_PULL_REPRO = 1/3                          # rev 12 guard: alpha=1 face pull reproduces seed-for-seed to < E_Delta/3
ELL_OF = lambda Mr: Mr - 0.5                   # rev 12 gap 1: l = (M_r - 1/2) a
RESID_SIGMA = 1.0                              # [assumed]
B10_NEXT_ORDER = 0.09                          # (rho/l)^2 on B10, in quadrature [assumed]
IT4_PRED_CONE = 6; IT4_PRED_CONTROL = 8        # [hive proposal, untested; Venus] / control
TIP_LOCAL_R_A = 1.0                            # [assumed]
RAM_FREE_GB_ASSUMED = 4.0
IT4_MIN_FREE_GB = 3.3                          # wait rather than overlap a cone job (parent rule)

# ---------------- utilities ----------------
def spec_hash():
    with open(SPEC_PATH, "rb") as f: return hashlib.sha256(f.read()).hexdigest()[:8].upper()

def free_ram_gb():
    if platform.system() == "Windows":
        class MS(ctypes.Structure):
            _fields_ = [("l", ctypes.c_ulong), ("load", ctypes.c_ulong), ("tot", ctypes.c_ulonglong), ("avail", ctypes.c_ulonglong),
                        ("tp", ctypes.c_ulonglong), ("ap", ctypes.c_ulonglong), ("tv", ctypes.c_ulonglong), ("av", ctypes.c_ulonglong), ("ax", ctypes.c_ulonglong)]
        m = MS(); m.l = ctypes.sizeof(MS); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)); return m.avail/2**30
    for line in open("/proc/meminfo"):
        if line.startswith("MemAvailable"): return int(line.split()[1])/2**20
def peak_rss_gb():
    if platform.system() == "Windows":
        class PMC(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong), ("pf", ctypes.c_ulong), ("peak", ctypes.c_size_t), ("ws", ctypes.c_size_t)] + [(f"x{i}", ctypes.c_size_t) for i in range(6)]
        p = PMC(); p.cb = ctypes.sizeof(PMC)
        ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(p), p.cb); return p.peak/2**30
    import resource; return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20

# ---------------- grading logic (pure; no kernel runs here) ----------------
def richardson_3pt(vals, a):
    """Observed order from 3 spacings (a values), extrapolated value and error. vals ordered coarse->fine."""
    f1, f2, f3 = vals; a1, a2, a3 = a
    d12, d23 = f1-f2, f2-f3
    if d12 == 0 or d23 == 0 or np.sign(d12) != np.sign(d23): return dict(order=None, extrap=None, E_a=None)
    from scipy.optimize import brentq
    g = lambda p: (a1**p-a2**p)/(a2**p-a3**p) - d12/d23
    try: p = brentq(g, 0.05, 12)
    except ValueError: return dict(order=None, extrap=None, E_a=None)
    E = abs(d23)/((a2/a3)**p-1); return dict(order=p, extrap=f3-np.sign(d23)*E, E_a=E)
def offtip_E_a(d16, d20, eps, a16=1/4.2, a20=1/5.0):
    p = P_A_EXPECTED[eps]; return abs(d20-d16)/((a16/a20)**p-1)
def eps_offtip_gate(eps, ontip_order, ontip_order_err):
    """Graded only if on-tip B12/B16/B20 measures the expected order at that eps within its error."""
    if ontip_order is None: return False
    return abs(ontip_order - P_A_EXPECTED[eps]) <= ontip_order_err
def it1_combined_E(E_a, sigma_seed): return float(np.sqrt(E_a**2 + sigma_seed**2/SEEDS))
def p_box(eps):
    if INV_A_CHECK not in ("PASS", "PASS_RHO_TF"): raise RuntimeError(f"p_box UNDECIDED until the 1/a check passes (INV_A_CHECK={INV_A_CHECK})")
    return P_BOX_EPS[eps][0]
def it4_fit(ell, lam, sig, names, eps=0):
    """lambda(l) = lam_inf + A l^-P_BOX, weighted; B10 gets B10_NEXT_ORDER*A-term in quadrature (iterated)."""
    P = p_box(eps)
    ell, lam, sig = (np.asarray(v, dtype=float) for v in (ell, lam, sig)); s = sig.copy()
    for _ in range(5):
        X = np.c_[np.ones_like(ell), ell**-P]; W = 1/s**2
        cov = np.linalg.inv(X.T@(X*W[:, None])); beta = cov@(X.T@(W*lam))
        s = np.sqrt(sig**2 + np.where(np.array(names) == "B10", (B10_NEXT_ORDER*beta[1]*ell**-P)**2, 0))
    chi2 = float(np.sum(((lam - X@beta)/s)**2))
    return dict(lam_inf=beta[0], A=beta[1], err_lam_inf=float(np.sqrt(cov[0, 0])), chi2=chi2, report_only=chi2 > RESID_SIGMA**2)
def it4_ram_gb(sites):
    dim = 12*sites; return dim*LANCZOS_VECTORS*8*WORKSPACE_FACTOR/1e9, dim

def wait_for_ram_before_it4(poll_s=60):
    while free_ram_gb() < IT4_MIN_FREE_GB:
        print(f'free RAM {free_ram_gb():.2f} GB < {IT4_MIN_FREE_GB} GB; waiting before IT4/Lanczos', flush=True); time.sleep(poll_s)

def face_pull_guard(pull_run1, pull_run2, E_delta):
    d = np.max(np.abs(np.asarray(pull_run1)-np.asarray(pull_run2))); return bool(d < FACE_PULL_REPRO*E_delta), float(d)

KERNELS = {"gradient_flow_target_rho": True, "clover_Q": True, "selfduality_shells": True,
           "hessian_lanczos_projected": True, "smooth_generic_seed": True, "seed_bootstrap_order": True,
           "cartesian_wedge_row": False, "p_box_frozen": False, "rho_estimator_calibrated": False, "flow_step_stable": False}
GRADED_ROWS = ["IT1 on-tip", "IT1 off-tip (B16 d0=10.5a rho=4.2a; B20 d0=12.5a rho=5a)", "IT2", "IT3", "IT4"]

# ---------------- smoke ----------------
def bpst_density(R2, rho): return 48*rho**4/(R2+rho**2)**4
def continuum_shares(lat, rho):
    g, w = np.polynomial.legendre.leggauss(12)
    def band(r0, r1):
        r = 0.5*(r1-r0)*g + 0.5*(r1+r0); wr = 0.5*(r1-r0)*w
        h3 = lat.x3[[0, -1]]; h4 = lat.x4[[0, -1]]
        G, Wg = np.polynomial.legendre.leggauss(160)
        x3 = 0.5*(h3[1]-h3[0])*G + 0.5*(h3[1]+h3[0]); w3 = 0.5*(h3[1]-h3[0])*Wg
        x4 = 0.5*(h4[1]-h4[0])*G + 0.5*(h4[1]+h4[0]); w4 = 0.5*(h4[1]-h4[0])*Wg
        R2 = r[:, None, None]**2 + x3[None, :, None]**2 + x4[None, None, :]**2
        return float(np.einsum('i,j,k,ijk->', wr*r*2*np.pi*lat.alpha, w3, w4, bpst_density(R2, rho)))
    a = lat.a; tip = band(0, a/4); rings = [band(a/4, a)] + [band(n*a, (n+1)*a) for n in range(1, lat.Mr)]
    return tip, np.array(rings)

def smoke(out):
    S8 = 8*np.pi**2; rep = dict(kind="SCRATCH timing smoke (H5) - not graded, not a test", spec_hash=spec_hash(),
                                 FINAL_SPEC_HASH=FINAL_SPEC_HASH, python=sys.version.split()[0], numpy=np.__version__,
                                 host=platform.node(), started=time.strftime("%Y-%m-%d %H:%M:%S %Z"))
    rep["free_ram_gb_start"] = free_ram_gb(); boxes = {}
    for name, dims in BOXES.items():
        b = {}; t0 = time.perf_counter()
        for al in ALPHAS: Lattice(*dims, alpha=al)
        b["geometry_all_alpha_s"] = time.perf_counter()-t0
        lat = Lattice(*dims, alpha=1.0); t0 = time.perf_counter(); L = lat.bpst_links(3.0)
        b["bpst_links_s"] = time.perf_counter()-t0; t0 = time.perf_counter(); o = lat.action(L, 0)
        b["action_eps0_s"] = time.perf_counter()-t0
        b["S_eps0_over_8pi2_rho3a_alpha1"] = o["S"]/S8; b["face_truncation_max_1mq0"] = lat.face_dev
        b["sites_alpha1"] = lat.n_sites; b["sites_upper_bound"] = lat.n_sites_upper
        b["sites_alpha_0p5"] = Lattice(*dims, alpha=0.5).n_sites
        b["free_ram_gb_after"] = free_ram_gb(); b["peak_rss_gb_so_far"] = peak_rss_gb()
        if name in IT4_BOXES:
            ram_up, dim_up = it4_ram_gb(lat.n_sites_upper); ram_act, dim_act = it4_ram_gb(lat.n_sites)
            b["IT4_lanczos_ram_gb_upper"] = ram_up; b["IT4_lanczos_ram_gb_actual_sites"] = ram_act; b["IT4_hessian_dim_actual"] = dim_act
        boxes[name] = b; del L
        print(f"{name}: geom {b['geometry_all_alpha_s']:.3f}s links {b['bpst_links_s']:.2f}s action {b['action_eps0_s']:.2f}s "
              f"S/8pi^2 {b['S_eps0_over_8pi2_rho3a_alpha1']:.5f} free {b['free_ram_gb_after']:.2f} GB peak {b['peak_rss_gb_so_far']:.3f} GB", flush=True)
    rep["boxes"] = boxes
    rep["IT4_total_ram_gb_upper"] = sum(boxes[n]["IT4_lanczos_ram_gb_upper"] for n in IT4_BOXES)
    # (a) trapezoid / O(a/r) check: per-ring lattice share vs continuum, eps=0, alpha=1
    chk_a = {}
    for name in ("B16", "B20"):
        lat = Lattice(*BOXES[name], alpha=1.0); rho = 3.0; L = lat.bpst_links(rho)
        ct, cr = continuum_shares(lat, rho); n = np.arange(lat.Mr); keep = (lat.r >= GRADE_R_MIN_A) & (lat.r <= rho*2.5)
        for e in (0, 1):   # eps=0 as asked; eps=1 has no 2x2 seams so its per-ring profile isolates the polar terms
            o = lat.action(L, e); dev = o["ring"]/cr - 1
            X = np.c_[np.ones(keep.sum()), 1/lat.r[keep], 1/lat.r[keep]**2]
            coef, *_ = np.linalg.lstsq(X, dev[keep], rcond=None); inner = (lat.r < GRADE_R_MIN_A)
            chk_a[f"{name}_eps{e}"] = dict(rho_a=rho, fit_rings_2a_to_2p5rho=[float(v) for v in lat.r[keep]], r_a=lat.r.tolist(), ring_dev=dev.tolist(),
                tip_lat=o["tip"], tip_cont=ct, fit_r_ge_2a=dict(c0=coef[0], c1_a_over_r=coef[1], c2_a2_over_r2=coef[2]),
                S_lat_r_lt_2a=float(o["ring"][inner].sum()+o["tip"]), S_cont_r_lt_2a=float(cr[inner].sum()+ct),
                S_lat_total_over_8pi2=o["S"]/S8, S_cont_in_box_over_8pi2=float((cr.sum()+ct)/S8),
                eq19_flat_prediction_over_8pi2=1-(e/5)*(1/rho)**2-((15*e-12)/210)*(1/rho)**4)
    rep["check_a_trapezoid"] = chk_a
    # (b) sign of the outward push: scale-mode projection at alpha=1 on B20
    name = "B20"; lat = Lattice(*BOXES[name], alpha=1.0); ell = lat.r[-1]
    rhos = [2.5, 2.9, 3.1, 3.5, 4.0, 5.0, 6.0]; S = {e: [] for e in (1, 0, -1)}; Sc = []
    for rho in rhos:
        L = lat.bpst_links(rho)
        for e in S: S[e].append(lat.action(L, e)["S"]/S8)
        ct, cr = continuum_shares(lat, rho); Sc.append(float((ct+cr.sum())/S8))
    i29, i31 = rhos.index(2.9), rhos.index(3.1); rho0 = 3.0  # centred difference at rho=3a
    chk_b = dict(box=name, ell_a=float(ell), rhos=rhos, S_over_8pi2=S, S_cont_in_box_over_8pi2=Sc)
    for e in S:
        dS = (S[e][i31]-S[e][i29])/(rhos[i31]-rhos[i29]); dScont = (Sc[i31]-Sc[i29])/(rhos[i31]-rhos[i29])
        drho2 = -2*rho0*dS; drho2_lat = -2*rho0*(dS-dScont)
        chk_b[f"eps{e}"] = dict(dS_drho=dS, drho2dt_scale_mode_total=drho2, sign_total="outward" if drho2 > 0 else "inward",
                                dS_drho_minus_continuum_box=dS-dScont, drho2dt_lattice_part=drho2_lat,
                                sign_lattice_part="outward" if drho2_lat > 0 else "inward")
    x = 1/np.array(rhos); y = np.array(S[0])-np.array(Sc)
    X = np.c_[np.ones_like(x), x**2, x**4]; coef, res, *_ = np.linalg.lstsq(X, y, rcond=None)
    chk_b["eps0_fit_Slat_minus_Scont"] = dict(c0=coef[0], c2=coef[1], c4=coef[2], eq19_c4=12/210)
    rep["check_b_outward_push"] = chk_b
    rep["free_ram_gb_end"] = free_ram_gb(); rep["peak_rss_gb"] = peak_rss_gb()
    rep["NOT_COMPUTED_YET"] = [k for k, v in KERNELS.items() if not v]
    rep["finished"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    txt = json.dumps(rep, indent=1, default=float)
    with open(out, "w", encoding="utf-8") as f: f.write(txt)
    print("check (a)", json.dumps({k: dict(v["fit_r_ge_2a"], S_lat=v["S_lat_total_over_8pi2"], S_cont=v["S_cont_in_box_over_8pi2"], eq19=v["eq19_flat_prediction_over_8pi2"]) for k, v in chk_a.items()}, default=float))
    print("check (b)", json.dumps({k: chk_b[k] for k in chk_b if k.startswith("eps")}, default=float))
    print("wrote", out, hashlib.sha256(txt.encode()).hexdigest()[:8].upper())


# ---------------- rev 13 flowed re-smoke (SCRATCH, H5) ----------------
def eq19(eps, rho): return -(eps/5)/rho**2 - ((15*eps-12)/210)/rho**4
def flowed_row(name, eps, rho, centre_kind, h=None, nsub=16, alpha=1.0, tf=None):
    from kernels import Loops
    h = FLOW_STEP if h is None else h
    lat = Lattice(*BOXES[name], alpha=alpha); lp = Loops(lat, eps)
    k3c, k4c = lat.M3//2, lat.M4//2
    c = (0., 0., lat.x3[k3c], lat.x4[k4c]) if centre_kind == "tip_site" else (0., 0., 0., 0.)
    t0 = time.perf_counter(); U = lp.flat(lat.bpst_links(rho, nsub=nsub, centre=c)); t_build = time.perf_counter()-t0
    S0 = lp.action(U); rho0 = lp.rho_moment(U, centre=c)
    tf = FLOW_TF if tf is None else tf
    nsteps = int(round(tf/h)); t0 = time.perf_counter()
    U, _ = lp.flow(U, h=h, max_steps=nsteps, record=5)    # guard raises if S rises
    t_flow = time.perf_counter()-t0
    S1, dens = lp.action(U, per_site=True); rho1 = lp.rho_moment(U, centre=c)
    F = lp.field_strength(U); Q = lp.charge(U, F); sd = lp.selfduality(U, [(2, 4), (4, 8)], F)
    outer = lp.site_r >= lat.r[-3]; face3 = (np.abs(lp.site_x3) >= lat.x3[-1]-1.01) | (np.abs(lp.site_x4) >= lat.x4[-1]-1.01)
    S8 = 8*np.pi**2
    return dict(box=name, eps=eps, rho_seed=rho, centre=centre_kind, centre_xyz=list(map(float, c)), h=h, t_f=tf, steps=nsteps, nsub=nsub,
                S_seed=S0/S8, S_flowed=S1/S8, rho_raw_seed=rho0, rho_raw_flowed=rho1, Q=Q,
                s_2to4=sd[(2, 4)], s_4to8=sd[(4, 8)], S_outer2rings=float(dens[outer].sum()/S8), S_transverse_face_layer=float(dens[face3 & ~outer].sum()/S8),
                ell=float(lat.r[-1]), t_build_s=t_build, t_flow_s=t_flow, s_per_rk3_step=t_flow/nsteps, free_ram_gb=free_ram_gb(), peak_rss_gb=peak_rss_gb())

def resmoke_box(name):
    rows = []
    def go(*a, **k):
        r = flowed_row(*a, **k); rows.append(r); print(json.dumps(r, default=float), flush=True)
        json.dump(rows, open(os.path.join(HERE, "out", f"resmoke_{name}.json"), "w"), indent=1, default=float)
    for eps in (1, 0, -1, -0.25): go(name, eps, 3.0, "tip_site")
    go(name, 1, 3.0, "between_sites_control")
    for rho in RHO_CAL_RHOS[1:]: go(name, 1, rho, "tip_site")
    if name == "B10": go(name, 1, 3.0, "tip_site", h=FLOW_STEP_CHECK)

def holonomy_convergence(name="B10", rho=3.0):
    from kernels import Loops
    lat = Lattice(*BOXES[name], alpha=1.0); lp = Loops(lat, 1); c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2]); out = {}
    for ns in (4, 8, 16, 32, 64):
        out[ns] = lp.action(lp.flat(lat.bpst_links(rho, nsub=ns, centre=c)))/(8*np.pi**2); print("nsub", ns, out[ns], flush=True)
    return out

def gap_check(name="B20"):
    out = {}
    for rho in (3.0, 4.0):
        lat = Lattice(*BOXES[name], alpha=1.0); lat.apply_dirichlet = lambda L: 0.0
        L = lat.bpst_links(rho); S = lat.action(L, 1)["S"]/(8*np.pi**2); ct, cr = continuum_shares(lat, rho); Sc = (ct+cr.sum())/(8*np.pi**2)
        out[rho] = dict(S_noface=S, S_cont_in_box=Sc, lat_minus_cont=S-Sc, eq19=eq19(1, rho), residual=S-Sc-eq19(1, rho)); print(rho, out[rho], flush=True)
    out["residual_ratio_4a_over_3a"] = out[4.0]["residual"]/out[3.0]["residual"]; out["next_order_expectation"] = (3/4)**6
    return out

def summarize():
    import glob
    from scipy.optimize import curve_fit
    rows = []
    for f in glob.glob(os.path.join(HERE, "out", "resmoke_B*.json")):
        d = json.load(open(f)); rows += d if isinstance(d, list) else [d]
    key = lambda r: (r["box"], r["eps"], r["rho_seed"], r["centre"], r["h"])
    uniq = {key(r): r for r in rows}; rows = list(uniq.values())
    get = lambda **k: [r for r in rows if all(r[a] == b for a, b in k.items())]
    out = dict(kind="SCRATCH flowed re-smoke summary (H5), not graded", spec=FINAL_SPEC_HASH, rows=len(rows), cal={}, eps_rows={}, p_box={}, controls={}, h_check=None)
    for b in BOXES:
        cal = {}
        for rho in RHO_CAL_RHOS:
            r = get(box=b, eps=1, rho_seed=rho, centre="tip_site", h=FLOW_STEP)
            if r: cal[rho] = dict(raw=r[0]["rho_raw_flowed"], ratio=rho/r[0]["rho_raw_flowed"])
        if len(cal) == 3:
            rat = [c["ratio"] for c in cal.values()]; var = (max(rat)-min(rat))/np.mean(rat)
            cal["variation"] = var; cal["interpolate"] = bool(var > RHO_CAL_VAR)
        out["cal"][b] = {str(k): v for k, v in cal.items()}
    def corr(b, raw):
        c = out["cal"][b]; pts = sorted((v["raw"], v["ratio"]) for k, v in c.items() if k not in ("variation", "interpolate"))
        if not pts: return None, "NOT COMPUTED (YET)"
        if len(pts) == 3 and c.get("interpolate"): return raw*np.interp(raw, [p[0] for p in pts], [p[1] for p in pts]), "interpolated [measured, calibration]"
        if len(pts) < 3: return raw*pts[0][1], "partial calibration [measured, calibration]"
        r3 = dict((k, v) for k, v in c.items() if k == "3.0")
        return raw*r3["3.0"]["ratio"], "ratio at 3a [measured, calibration]"
    for e in (1, 0, -1, -0.25):
        er = {}
        for b in BOXES:
            r = get(box=b, eps=e, rho_seed=3.0, centre="tip_site", h=FLOW_STEP)
            if not r: er[b] = "NOT COMPUTED (YET)"; continue
            r = r[0]; rc, tag = corr(b, r["rho_raw_flowed"]); bp = get(box=b, eps=1, rho_seed=3.0, centre="tip_site", h=FLOW_STEP)
            er[b] = dict(S_flowed=r["S_flowed"], S_seed=r["S_seed"], rho_raw=r["rho_raw_flowed"], rho_corr=rc, rho_tag=tag, ell=r["ell"],
                         rho_over_ell=(rc/r["ell"]) if rc else None, Q=r["Q"], s_2to4=r["s_2to4"], s_4to8=r["s_4to8"],
                         s_minus_sBPST_2to4=(r["s_2to4"]-bp[0]["s_2to4"]) if bp else None, outer2rings=r["S_outer2rings"], transverse_face_layer=r["S_transverse_face_layer"],
                         s_per_step=r["s_per_rk3_step"], free_ram_gb=r["free_ram_gb"])
        out["eps_rows"][str(e)] = er
        pts = [(v["rho_over_ell"], v["S_flowed"]) for v in er.values() if isinstance(v, dict) and v["rho_over_ell"]]
        if len(pts) == 4:
            x, y = map(np.array, zip(*pts))
            try:
                popt, pcov = curve_fit(lambda x, S0, c, p: S0 + c*x**p, x, y, p0=[1.0, 1.0, 3.0], maxfev=20000)
                out["p_box"][str(e)] = dict(p=popt[2], p_err=float(np.sqrt(pcov[2, 2])), S_inf=popt[0], c=popt[1], points=pts, tag="[measured, smoke] flowed t_f=0.1")
            except Exception as ex: out["p_box"][str(e)] = f"fit failed: {ex}"
        else: out["p_box"][str(e)] = f"NOT COMPUTED (YET): {len(pts)}/4 boxes"
    for b in BOXES:
        t = get(box=b, eps=1, rho_seed=3.0, centre="tip_site", h=FLOW_STEP); c = get(box=b, eps=1, rho_seed=3.0, centre="between_sites_control", h=FLOW_STEP)
        if t and c: out["controls"][b] = {k: dict(tip_site=t[0][k], between_sites_control=c[0][k]) for k in ("S_seed", "S_flowed", "rho_raw_flowed", "Q", "s_2to4")}
    a = get(box="B10", eps=1, rho_seed=3.0, centre="tip_site", h=FLOW_STEP); bb = get(box="B10", eps=1, rho_seed=3.0, centre="tip_site", h=FLOW_STEP_CHECK)
    if a and bb: out["h_check"] = dict(dS=bb[0]["S_flowed"]-a[0]["S_flowed"], drho_raw=bb[0]["rho_raw_flowed"]-a[0]["rho_raw_flowed"], dQ=bb[0]["Q"]-a[0]["Q"],
                                      E_Delta="NOT COMPUTED (YET): needs alpha<1 rows; pass/fail vs E_Delta/3 deferred")
    txt = json.dumps(out, indent=1, default=float); open(os.path.join(HERE, "out", "resmoke_summary.json"), "w").write(txt); print(txt)

INV_A_PRED = None   # computed from geometry below: ratio (rho/a)^4/(l/a)^3 B20@6a over B10@3a
INV_A_TOL = 0.15    # [assumed, stated before the run] |measured/predicted - 1| <= 15% => PASS
INV_A_RHO_TF_DIV = 90.0   # rev 14 Venus rerun: t_f = rho^2/90 (0.1a^2 on B10@3a, 0.4a^2 on B20@6a), frozen before run
INV_A_PRED_FIXED = 1.850  # 1/a prediction quoted by Venus; checked against geometry in output
def inv_a_check(rho_tf=False):
    outname = "inv_a_check_rho_tf.json" if rho_tf else "inv_a_check.json"
    S8 = 8*np.pi**2; res = {}
    for name, rho in (("B10", 3.0), ("B20", 6.0)):
        lat = Lattice(*BOXES[name], alpha=1.0); ell = float(lat.r[-1])
        L = lat.bpst_links(rho); Sd = lat.action(L, 1)["S"]/S8
        lat2 = Lattice(*BOXES[name], alpha=1.0); lat2.apply_dirichlet = lambda L: 0.0; Sn = lat2.action(lat2.bpst_links(rho), 1)["S"]/S8
        tf = rho**2/INV_A_RHO_TF_DIV if rho_tf else None
        row = flowed_row(name, 1, rho, "tip_site", tf=tf)
        res[name] = dict(rho_a=rho, ell_a=ell, rho_over_ell=rho/ell, S_seed=Sd, S_noface=Sn, jump_seed=Sd-Sn, S_flowed=row["S_flowed"],
                         excess_flowed=row["S_flowed"]-Sn, t_f=row["t_f"], steps=row["steps"], Q=row["Q"], s_2to4=row["s_2to4"], t_flow_s=row["t_flow_s"], outer2rings_flowed=row["S_outer2rings"], s_per_step=row["s_per_rk3_step"], free_ram_gb=row["free_ram_gb"],
                         model=(rho**4)/(ell**3))
        print(name, json.dumps(res[name], default=float), flush=True)
    pred = res["B20"]["model"]/res["B10"]["model"]; phys = (res["B20"]["rho_over_ell"]/res["B10"]["rho_over_ell"])**P_BOX_EPS[1][0]
    m_seed = res["B20"]["jump_seed"]/res["B10"]["jump_seed"]; m_flow = res["B20"]["excess_flowed"]/res["B10"]["excess_flowed"]
    if rho_tf: assert abs(pred-INV_A_PRED_FIXED) < 5e-3, (pred, INV_A_PRED_FIXED)
    ok = abs(m_flow/pred-1) <= INV_A_TOL
    out = dict(rows=res, predicted_ratio_inv_a=pred, a_independent_ratio=phys, measured_ratio_seed=m_seed, measured_ratio_flowed=m_flow,
               tol=INV_A_TOL, verdict=("PASS_RHO_TF" if rho_tf else "PASS") if ok else "FAIL", flow_rule=("t_f=rho^2/90" if rho_tf else "t_f=0.1a^2"), deviation=m_flow/pred-1, graded_on="flowed excess (S_flowed - S_noface), eps=1, alpha=1")
    # S_inf reproduction with frozen p at eps=1 (flowed smoke points from resmoke_summary.json)
    try:
        sm = json.load(open(os.path.join(HERE, "out", "resmoke_summary.json"))); pts = sm["p_box"]["1"]["points"]
        x, y = map(np.array, zip(*pts)); X = np.c_[np.ones_like(x), x**P_BOX_EPS[1][0]]; beta = np.linalg.lstsq(X, y, rcond=None)[0]
        out["S_inf_frozen_p_eps1"] = float(beta[0]); out["S_inf_check"] = bool(abs(beta[0]-S_INF_CHECK_EPS1) < 5e-4)
    except Exception as ex: out["S_inf_check"] = f"failed: {ex}"
    txt = json.dumps(out, indent=1, default=float); assert not (rho_tf and outname == "inv_a_check.json")
    open(os.path.join(HERE, "out", outname), "w").write(txt); print(txt)

# ---------------- IT3 graded rows (rev 14) ----------------
IT3_GRIDS = {"B10": 3.0, "B12": 3.6, "B16": 4.8}   # rev 16/17 cut: three grids at rho/l = 0.3, 8 seeds
IT3_EPS = 0                                    # rev 16: eps=0 only; eps=1 control deferred, NOT COMPUTED (YET)
IT3_Q_PLATEAU = 0.05                           # rev 15: |Q-1| <= 0.05 after flow [assumed, Helios]
IT3_ALPHAS = [1.0, 0.9, 0.75, 0.55, 0.5]
def it3_row(box, alpha, seed, kind="generic", steps=None, outdir="it3"):
    from kernels import Loops, generic_seed
    rho = IT3_GRIDS[box]; lat = Lattice(*BOXES[box], alpha=alpha); lp = Loops(lat, IT3_EPS)
    c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2]); t0 = time.perf_counter()
    U = generic_seed(lat, rho, seed=seed, centre=c) if kind == "generic" else lp.flat(lat.bpst_links(rho, centre=c))
    S0 = lp.action(U); U, _ = lp.flow(U, h=FLOW_STEP, max_steps=(steps or int(round(flow_tf(rho)/FLOW_STEP))), record=5)
    # rev 15: fixed t_f = rho^2/90 replaces the target-rho stop
    S1 = lp.action(U); F = lp.field_strength(U); Q = lp.charge(U, F); sd = lp.selfduality(U, [(2, 4), (4, 8)], F)
    out = dict(test="IT3", box=box, alpha=alpha, seed=seed, kind=kind, eps=IT3_EPS, rho_seed=rho, S_seed=S0/(8*np.pi**2), S_flowed=S1/(8*np.pi**2),
               rho_raw=lp.rho_moment(U, centre=c), Q=Q, plateau=bool(abs(abs(Q)-1) <= IT3_Q_PLATEAU), s_2to4=sd[(2, 4)], s_4to8=sd[(4, 8)],
               wall_s=time.perf_counter()-t0, free_ram_gb=free_ram_gb(), spec=FINAL_SPEC_HASH, orbifold=(alpha == ORBIFOLD))
    out["steps"] = steps or int(round(flow_tf(rho)/FLOW_STEP)); out["smoke"] = steps is not None
    fn = os.path.join(HERE, "out", outdir, f"{box}_a{alpha}_{kind}_s{seed}.json"); os.makedirs(os.path.dirname(fn), exist_ok=True)
    tmp = fn + ".tmp"; open(tmp, "w").write(json.dumps(out, default=float)); os.replace(tmp, fn); print(json.dumps(out, default=float), flush=True)
def it3_jobs():
    jobs = [(b, 1.0, 0, "bpst") for b in IT3_GRIDS]
    for b in IT3_GRIDS:
        for al in IT3_ALPHAS:
            for s in range(SEEDS): jobs.append((b, al, s, "generic"))
    return jobs
def it3_campaign(workers=3, min_free=1.5):
    import subprocess
    jobs = [j for j in it3_jobs() if not os.path.exists(os.path.join(HERE, "out", "it3", f"{j[0]}_a{j[1]}_{j[3]}_s{j[2]}.json"))]
    jobs.sort(key=lambda j: j[0])   # B16 first
    running = []
    while jobs or running:
        running = [p for p in running if p.poll() is None]
        if jobs and len(running) < workers and free_ram_gb() >= min_free:
            b, al, s, k = jobs.pop(0)
            log = open(os.path.join(HERE, "out", "it3", f"{b}_a{al}_{k}_s{s}.log"), "w")
            running.append(subprocess.Popen([sys.executable, "-B", os.path.join(HERE, "run.py"), "it3-row", "--box", b, "--alpha", str(al), "--seed", str(s), "--kind", k], stdout=log, stderr=subprocess.STDOUT))
        time.sleep(10)
def it3_grade(indir="it3"):
    import glob
    R = [json.load(open(f)) for f in glob.glob(os.path.join(HERE, "out", indir, "*.json"))]
    out = dict(test="IT3", spec=FINAL_SPEC_HASH, rows=len(R), expected=len(it3_jobs()), grids={})
    for b in IT3_GRIDS:
        bp = [r for r in R if r["box"] == b and r["kind"] == "bpst"]; ctrl = [r for r in R if r["box"] == b and r["alpha"] == 1.0 and r["kind"] == "generic" and r["plateau"]]
        g = {}
        for al in IT3_ALPHAS:
            rs = [r for r in R if r["box"] == b and r["alpha"] == al and r["kind"] == "generic"]; pl = [r for r in rs if r["plateau"]]
            if not pl or not bp or not ctrl: g[str(al)] = dict(n=len(rs), n_plateau=len(pl), verdict="NOT COMPUTED (YET)"); continue
            s = np.mean([r["s_2to4"] for r in pl]); s1 = np.mean([r["s_2to4"] for r in ctrl]); sb = bp[0]["s_2to4"]
            g[str(al)] = dict(n=len(rs), n_plateau=len(pl), s_2to4=s, s_seed_sd=float(np.std([r["s_2to4"] for r in pl])), s_minus_sBPST=s-sb, s_minus_s1=s-s1,
                              Q_mean=float(np.mean([r["Q"] for r in pl])), orbifold=(al == ORBIFOLD))
        out["grids"][b] = g
    out.update(it3_verdicts(out["grids"]))
    txt = json.dumps(out, indent=1, default=float); open(os.path.join(HERE, "out", f"{indir}_grade.json"), "w").write(txt); print(txt)


# ---------------- rev 16: B16 box-cost point (SCRATCH, H5) + timed-step costing ----------------
B16PT_RHO = 4.8          # rho/l = 4.8/15.5 = 0.310, matches B10 (0.316) and B20 (0.308)
B16PT_TOL = 0.15         # [hive proposal, untested] PASS iff all three flowed excesses within 15% of their mean, fixed before the run
def boxcost_b16(max_steps=None):
    S8 = 8*np.pi**2; name, rho = "B16", B16PT_RHO
    lat = Lattice(*BOXES[name], alpha=1.0); ell = float(lat.r[-1]); Sd = lat.action(lat.bpst_links(rho), 1)["S"]/S8
    lat2 = Lattice(*BOXES[name], alpha=1.0); lat2.apply_dirichlet = lambda L: 0.0; Sn = lat2.action(lat2.bpst_links(rho), 1)["S"]/S8
    tf = flow_tf(rho) if max_steps is None else max_steps*FLOW_STEP
    row = flowed_row(name, 1, rho, "tip_site", tf=tf)
    r = dict(rho_a=rho, ell_a=ell, rho_over_ell=rho/ell, S_seed=Sd, S_noface=Sn, jump_seed=Sd-Sn, S_flowed=row["S_flowed"], excess_flowed=row["S_flowed"]-Sn,
             t_f=row["t_f"], steps=row["steps"], Q=row["Q"], s_2to4=row["s_2to4"], s_per_step=row["s_per_rk3_step"], t_flow_s=row["t_flow_s"], t_build_s=row["t_build_s"], free_ram_gb=row["free_ram_gb"])
    if max_steps is not None:
        txt = json.dumps(dict(kind="timing probe only", **r), indent=1, default=float); open(os.path.join(HERE, "out", "boxcost_b16_timing.json"), "w").write(txt); print(txt); return
    prev = json.load(open(os.path.join(HERE, "out", "inv_a_check_rho_tf.json")))["rows"]
    ex = {"B10": prev["B10"]["excess_flowed"], "B16": r["excess_flowed"], "B20": prev["B20"]["excess_flowed"]}
    m = float(np.mean(list(ex.values()))); dev = {k: v/m-1 for k, v in ex.items()}
    ok = all(abs(d) <= B16PT_TOL for d in dev.values())
    out = dict(kind="SCRATCH (H5) B16 box-cost point", spec=FINAL_SPEC_HASH, row=r, excess=ex, mean=m, rel_dev=dev, tol=B16PT_TOL,
               verdict="PASS" if ok else "FAIL", hypothesis="flowed excess a-independent at fixed rho/l ~ 0.31 (real box cost)")
    txt = json.dumps(out, indent=1, default=float); open(os.path.join(HERE, "out", "boxcost_b16.json"), "w").write(txt); print(txt)
def time_steps(box, eps, alpha, rho, nsteps=3):
    """Timed RK3 steps (generic seed, tip-site), for costing only; writes nothing graded."""
    from kernels import Loops, generic_seed
    lat = Lattice(*BOXES[box], alpha=alpha); lp = Loops(lat, eps); c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2])
    t0 = time.perf_counter(); U = generic_seed(lat, rho, seed=0, centre=c); tb = time.perf_counter()-t0
    t0 = time.perf_counter(); U, _ = lp.flow(U, h=FLOW_STEP, max_steps=nsteps, record=nsteps); tf_ = time.perf_counter()-t0
    t0 = time.perf_counter(); F = lp.field_strength(U); lp.charge(U, F); lp.selfduality(U, [(2, 4), (4, 8)], F); lp.rho_moment(U, centre=c); tm = time.perf_counter()-t0
    out = dict(box=box, eps=eps, alpha=alpha, rho=rho, steps=nsteps, s_per_step=tf_/nsteps, build_s=tb, measure_s=tm, free_ram_gb=free_ram_gb())
    fn = os.path.join(HERE, "out", "timing", f"{box}_e{eps}_a{alpha}.json"); os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, "w").write(json.dumps(out, default=float)); print(json.dumps(out, default=float), flush=True)

# ---- rev 17 observed-order rule (IT3) and cut IT1 (rev 16/17) ----
ORDER_WINDOW = (2.0, 6.0); P_RICH = 4.0            # [Venus ruling, rev 17]
def observed_order(vals, Ns, lo=0.25, hi=12.0):
    """Order p from three grids with a ~ 1/N: (v1-v2)/(v2-v3) = (h1^p-h2^p)/(h2^p-h3^p). None if not monotone/convergent."""
    h = [1.0/n for n in Ns]; d1, d2 = vals[0]-vals[1], vals[1]-vals[2]
    if d2 == 0 or d1/d2 <= 0: return None
    f = lambda p: (h[0]**p-h[1]**p)/(h[1]**p-h[2]**p) - d1/d2
    if f(lo)*f(hi) > 0: return None
    a, b = lo, hi
    for _ in range(200):
        m = 0.5*(a+b)
        if f(a)*f(m) <= 0: b = m
        else: a = m
    return 0.5*(a+b)
def it3_verdicts(grids):
    out = {}; names = list(IT3_GRIDS); Ns = [BOXES[b][0] for b in names]
    for al in IT3_ALPHAS:
        if al == 1.0: continue
        rows = [grids.get(b, {}).get(str(al), {}) for b in names]
        if any("s_minus_s1" not in r for r in rows): out[f"verdict_alpha_{al}"] = dict(verdict="NOT COMPUTED (YET)"); continue
        d = [r["s_minus_s1"] for r in rows]; sbd = [r["s_minus_sBPST"] for r in rows]
        p = observed_order(d, Ns); rec = dict(observed_order=p, values=d)
        if p is None or not (ORDER_WINDOW[0] <= p <= ORDER_WINDOW[1]):
            rec["verdict"] = "UNDECIDED (observed order outside [2,6] or not measurable)"
        else:
            r = (Ns[2]/Ns[1])**P_RICH - 1; dinf = d[2] + (d[2]-d[1])/r; sinf = sbd[2] + (sbd[2]-sbd[1])/r
            stable = all(abs(x-dinf) <= GRID_STAB*abs(dinf) for x in d[1:]) if dinf else False
            rec.update(d_inf=dinf, sBPST_diff_inf=sinf, grid_stable_20pct=stable)
            if dinf >= S_NOT_SELFDUAL and stable: rec["verdict"] = "AGAINST (not self-dual at tip)"
            elif sinf <= SD_REL_CUT: rec["verdict"] = "SUPPORTS (self-dual at tip)"
            else: rec["verdict"] = "UNDECIDED"
        if al == ORBIFOLD: rec["note"] = "orbifold, reported separately"
        out[f"verdict_alpha_{al}"] = rec
    return out

IT1_GRIDS = {"B10": 3.0, "B12": 3.6, "B14": 4.2}   # rev 21: rho = 0.3*M_r, tip-site, eps = 0
IT1_BOX_ORDER = ("B10", "B12", "B14")              # coarse -> fine for 3-grid Richardson
IT1_EPS = 0; IT1_SEEDS = 6; IT1_ALPHAS = [1.0, 0.9, 0.75, 0.55, 0.5]; IT1_WIN = 0.4; IT1_REC = 5; IT1_PA = 4.0
IT1_BASE_SEED = 0                                  # one generic seed; the 6 "seeds" are link perturbations of it (rev 18)
IT1_DELTA = None                                   # rev 19: smooth-perturbation amplitude, set ONLY from the freeze file
IT1_DELTA_CANDIDATES = [0.001, 0.002, 0.003]       # rev 21 pick list; largest passing candidate is chosen [assumed]
IT1_PICK_RHO_SHIFT = 0.05                          # calibrated rho shift vs unperturbed at t_f <= 5% [assumed, Venus]
IT1_Q_SHIFT = 0.01                                 # |Q_delta - Q_0| <= 0.01 at t_f [assumed, Venus]
IT1_SMOOTH_MODES = (1, 2)                          # low-k sine modes per axis (r, x3, x4), theta-independent; a smooth field, NOT a pre-flow, so no smoothing time enters and t_f=rho^2/90 and the unflowed-BPST calibration are unchanged
IT1_GUARD_K = 3.0                                  # guard |meanA-meanB| <= k*sqrt(sigma1^2/3) (3+3: k*sigma1*sqrt(2/3)) [assumed]
IT1_PAIR_CORR_MIN = 0.5                            # per-seed correlation across alpha below this => unpaired sigma^2/3 (decided before Delta)
IT1_CAL_SLOPE_DEFAULT = 2.0                        # |dlnDelta/dlnrho| fallback [assumed]
IT1_RNG_BASE = 180000                              # draw d uses default_rng(IT1_RNG_BASE + d); recorded in every row
IT1_DRAWS_A = list(range(6)); IT1_DRAWS_B = list(range(6, 12))   # A: paired with every alpha; B: independent alpha=1 guard set
IT1_GUARD_MODE = "6+6"                             # "6+6" (A vs B) or "3+3" [small sample] (A split 0-2 vs 3-5, no B runs)
IT1_Q_TOL = 0.05                                   # Helios check: delta valid only if ||Q|-1| <= 0.05 after pre-flow and flow monotone
IT1_D0_DRAW = -1                                   # rev 20: deterministic delta=0 control row, one per alpha
IT1_WINDOWS_TF = ((1.0, 1.5), (1.5, 2.0))          # disjoint halves of [T, 2T]; T per box (rev 21)
IT1_WIN_AGREE = 0.20                               # flag if the two window drifts differ by > 20% [assumed]
IT1_WIN_SETTLE = 0.10                              # T chosen so |h1-h2|/max < 10% on delta=0, alpha=1 [assumed]
IT1_LINEAR_RATIO = 2.0; IT1_LINEAR_TOL = 0.3       # report-only: drift-shift(2d)/drift-shift(d) within 2 +/- 0.3
IT1_T_PATH = os.path.join(HERE, "out", "it1_T.json")
IT1_T_MAX_OVER_TF = 4.0                            # find-T flows to 2*(this)*t_f; cap [assumed]
DIAG21_DELTA = 0.001                               # [deviation] smallest rev 21 candidate; Venus reviews post-hoc
DIAG21_DELTA_NOTE = "[deviation] smallest rev 21 candidate; Venus reviews post-hoc"
DIAG21_LIN_DELTA = 0.002
DIAG21_ALPHAS = (1.0, 0.5)
DIAG21_SEEDS = 3
DIAG21_BOXES = ("B10", "B12")
DIAG21_FLOW_MAX_OVER_TF = 6.0                      # find-T stops at 10% settle or 6 t_f of flow
DIAG21_T_MAX_OVER_TF = 3.0                         # 2T must fit in 6 t_f of hist
def it1_jobs(mode=None):
    mode = mode or IT1_GUARD_MODE; J = []
    for b in IT1_GRIDS:
        for d in IT1_DRAWS_A:
            for al in IT1_ALPHAS: J.append((b, al, d))
        if mode == "6+6":
            for d in IT1_DRAWS_B: J.append((b, 1.0, d))
        for al in IT1_ALPHAS: J.append((b, al, IT1_D0_DRAW))
    return J
def it1_jobs_diag21():
    """B10+B12, alpha in {1, 0.5}, 3 seeds at DIAG21_DELTA plus delta=0 controls. No B14, no B-set."""
    J = []
    for b in DIAG21_BOXES:
        for d in range(DIAG21_SEEDS):
            for al in DIAG21_ALPHAS: J.append((b, al, d))
        for al in DIAG21_ALPHAS: J.append((b, al, IT1_D0_DRAW))
    return J
def it1_row_path(box, alpha, draw, outdir="it1", delta=None):
    if draw == IT1_D0_DRAW: name = f"{box}_a{alpha}_delta0.json"
    elif delta is not None and abs(float(delta) - DIAG21_LIN_DELTA) < 1e-12: name = f"{box}_a{alpha}_d{draw}_delta{DIAG21_LIN_DELTA}.json"
    elif delta is not None and "diag22" in str(outdir).replace("\\", "/"): name = f"{box}_a{alpha}_d{draw}_delta{float(delta)}.json"   # H10: diag22 has two nonzero deltas
    else: name = f"{box}_a{alpha}_d{draw}.json"
    return os.path.join(HERE, "out", outdir, name)
def it1_smooth_field(lp, draw):
    """Low-k su(2) field per link class: sum over sine modes in (r, x3, x4) vanishing on the faces, random N(0,1)/sqrt(nmodes)
    coefficients from default_rng(IT1_RNG_BASE+draw); theta-independent (smooth across the glued wedge). Rev 19 smooth perturbation."""
    lat = lp.lat; rng = np.random.default_rng(IT1_RNG_BASE + draw)
    t = np.clip(lp.tail, 0, None); r = lp.site_r[t]; x3 = lp.site_x3[t]; x4 = lp.site_x4[t]
    R = lat.r[-1]; L3 = lat.x3[-1]-lat.x3[0]; L4 = lat.x4[-1]-lat.x4[0]
    modes = [(m1, m2, m3) for m1 in IT1_SMOOTH_MODES for m2 in IT1_SMOOTH_MODES for m3 in IT1_SMOOTH_MODES]
    bounds = [0, lp.off["ang"], lp.off["d3"], lp.off["d4"], lp.NL]; xi = np.zeros((lp.NL, 3))
    for cls in range(4):
        sl = slice(bounds[cls], bounds[cls+1]); c = rng.standard_normal((len(modes), 3))/np.sqrt(len(modes))
        for (m1, m2, m3), cc in zip(modes, c):
            env = np.sin(np.pi*m1*r[sl]/R)*np.sin(np.pi*m2*(x3[sl]-lat.x3[0])/L3)*np.sin(np.pi*m3*(x4[sl]-lat.x4[0])/L4)
            xi[sl] += env[:, None]*cc[None, :]
    xi[lp.frozen] = 0
    return xi
def it1_perturb(lp, U, draw, delta=None):
    """U -> exp(delta * xi) U, LEFT-multiplied on free links (Loops.step), xi = smooth low-k field from default_rng(IT1_RNG_BASE+draw)
    (rev 19; per-link noise dropped). Paired across alpha by RNG stream [accepted, Venus]. delta may be negative: exp(-delta xi) is the
    same perturbation direction reversed (IT1b rev 6 antithetic pairs)."""
    delta = IT1_DELTA if delta is None else delta
    if delta is None: raise RuntimeError("IT1_DELTA not set: run the rev 19 delta pick first")
    return lp.step(U, delta*it1_smooth_field(lp, draw))
def it1_fit_drift(hist, ell, win=IT1_WIN):
    """d(rho^2)/dt from (t, rho) points with rho <= win*ell (early times), least squares; units a^2 per unit t (a^2)."""
    pts = [(t, r) for t, r in hist if r is not None and r <= win*ell]
    if len(pts) < 2: return None, len(pts)
    t, r = map(np.array, zip(*pts)); A = np.c_[np.ones_like(t), t]; c = np.linalg.lstsq(A, r**2, rcond=None)[0]
    return float(c[1]), len(pts)
def pick_verdict(base, draws, rho_tol=IT1_PICK_RHO_SHIFT, q_tol=IT1_Q_TOL, dq_tol=IT1_Q_SHIFT):
    """Rev 20 rule for one candidate amplitude: every draw monotone; at t_f |Q_d-Q_0| <= 0.01 ALONE [rule changed after smoke data: Venus]
    (||Q|-1| is a report-only row per box);
    calibrated rho at t_f within 5% of unperturbed; spread of drift(1) over the draws nonzero."""
    if not base["monotone"]: return dict(valid=False, reason="baseline flow not monotone")
    if not all(d["monotone"] for d in draws): return dict(valid=False, reason="flow not monotone under delta")
    if any(abs(d["Q_tf"]-base["Q_tf"]) > dq_tol for d in draws): return dict(valid=False, reason="|Q_delta-Q_0| > 0.01 at t_f")
    sh = max(abs(d["rho_tf"]/base["rho_tf"]-1) for d in draws)
    if sh > rho_tol: return dict(valid=False, reason=f"rho shift {sh:.4f} > {rho_tol}", rho_shift=sh)
    dr = [d["drift"] for d in draws]
    if any(x is None for x in dr): return dict(valid=False, reason="drift not fitted (window)", rho_shift=sh)
    sp = float(np.std(dr, ddof=1)) if len(dr) > 1 else 0.0
    if not sp > 0: return dict(valid=False, reason="drift(1) spread is zero", rho_shift=sh, spread=sp)
    return dict(valid=True, reason="ok", rho_shift=sh, spread=sp, absQ_report=dict(base=abs(abs(base["Q_tf"])-1), draws=[abs(abs(d["Q_tf"])-1) for d in draws], tol=q_tol, note="report-only per box [rev 20]"))
def pick_linearity(base, res, d=None, two_d=None, ratio0=IT1_LINEAR_RATIO, tol=IT1_LINEAR_TOL):
    """Report-only: (mean_drift(2d)-drift(0))/(mean_drift(d)-drift(0)) within 2 +/- 0.3. Does not gate the pick.
    Exact 2x pair in the rev 21 list is 0.001 vs 0.002."""
    d = IT1_DELTA_CANDIDATES[0] if d is None else d
    two_d = (2.0*d if two_d is None else two_d)
    bdrift = base.get("drift") if isinstance(base, dict) else None
    def mean_drift(dl):
        rec = res.get(str(dl)) or res.get(dl) or {}
        xs = [x for x in (rec.get("drift") or []) if x is not None]
        return float(np.mean(xs)) if xs else None
    m1, m2 = mean_drift(d), mean_drift(two_d)
    out = dict(d=d, two_d=two_d, drift_0=bdrift, mean_d=m1, mean_2d=m2, ratio=None, ok=None, band=[ratio0-tol, ratio0+tol],
               note="report-only; does not gate the pick")
    if bdrift is None or m1 is None or m2 is None: return out
    den = m1 - bdrift
    if den == 0: return out
    ratio = (m2 - bdrift)/den
    out["ratio"] = float(ratio); out["ok"] = bool(abs(ratio - ratio0) <= tol)
    return out
def it1_pick_row(box, delta, draw, steps=None, outdir="it1_pick", skip_existing=False):
    """One flow for the delta pick at alpha=1: baseline (draw<0) or smooth draw; Q and calibrated rho at t_f, then the drift window."""
    from kernels import Loops, generic_seed
    fn = os.path.join(HERE, "out", outdir, f"{box}_d{delta}_r{draw}.json" if draw >= 0 else f"{box}_base.json")
    if skip_existing and os.path.exists(fn):
        rec = json.load(open(fn, encoding="utf-8")); print(json.dumps(dict(skipped=True, path=fn, box=box, draw=draw), default=float), flush=True); return rec
    rho = IT1_GRIDS[box]; lat = Lattice(*BOXES[box], alpha=1.0); lp = Loops(lat, IT1_EPS); ell = float(lat.r[-1]); c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2])
    n_pre = steps or int(round(flow_tf(rho)/FLOW_STEP)); n_drift = steps or n_pre; t0 = time.perf_counter()
    cal = rho/lp.rho_moment(lp.flat(lat.bpst_links(rho, centre=c)), centre=c); rf = lambda W: cal*lp.rho_moment(W, centre=c)
    U = generic_seed(lat, rho, seed=IT1_BASE_SEED, centre=c)
    if draw >= 0: U = it1_perturb(lp, U, draw, delta)
    mono = True; Q_tf = rho_tf = drift = None; npts = 0
    try:
        U, _ = lp.flow(U, h=FLOW_STEP, max_steps=n_pre, record=5); Q_tf = lp.charge(U, lp.field_strength(U)); rho_tf = rf(U)
        U, hist = lp.flow(U, h=FLOW_STEP, max_steps=n_drift, record=min(IT1_REC, n_drift), rho_fn=rf); hist.append((n_drift*FLOW_STEP, rf(U)))
        drift, npts = it1_fit_drift(hist, ell)
    except FloatingPointError: mono = False
    out = dict(box=box, delta=delta, draw=draw, rng_seed=(IT1_RNG_BASE+draw) if draw >= 0 else None, monotone=mono, Q_tf=Q_tf, rho_tf=rho_tf, drift=drift, n_fit=npts,
               steps_pre=n_pre, steps_drift=n_drift, smoke=steps is not None, wall_s=time.perf_counter()-t0, spec=FINAL_SPEC_HASH)
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    tmp = fn+".tmp"; open(tmp, "w").write(json.dumps(out, default=float)); os.replace(tmp, fn); print(json.dumps(out, default=float), flush=True)
def it1_pick_grade(indir="it1_pick", box="B10", grade_dir=None):
    import glob
    base = json.load(open(os.path.join(HERE, "out", indir, f"{box}_base.json"))); res = {}
    for dl in IT1_DELTA_CANDIDATES:
        D = [json.load(open(f)) for f in glob.glob(os.path.join(HERE, "out", indir, f"{box}_d{dl}_r*.json"))]
        res[str(dl)] = dict(n=len(D), **(pick_verdict(base, D) if len(D) == IT1_SEEDS else dict(valid=False, reason=f"{len(D)}/{IT1_SEEDS} draws")),
                            Q=[d["Q_tf"] for d in D], rho_tf=[d["rho_tf"] for d in D], drift=[d["drift"] for d in D])
    ok = [dl for dl in IT1_DELTA_CANDIDATES if res[str(dl)]["valid"]]
    out = dict(box=box, base=base, candidates=res, chosen=(max(ok) if ok else None), rule="largest passing candidate [assumed]", spec=FINAL_SPEC_HASH, smoke=base["smoke"],
               n_rows=1+sum(res[str(dl)]["n"] for dl in IT1_DELTA_CANDIDATES), indir=indir,
               linearity=pick_linearity(base, res))
    txt = json.dumps(out, indent=1, default=float)
    gdir = grade_dir or os.path.join(HERE, "out"); os.makedirs(gdir, exist_ok=True)
    fn = os.path.join(gdir, f"it1_pick_grade_{box}.json")
    open(fn, "w").write(txt)
    if box == "B10" and grade_dir is None:  # in-flight chain Copy-Item of the old name
        open(os.path.join(HERE, "out", "it1_pick_grade.json"), "w").write(txt)
    print(txt); return out
FROZEN_PATH = os.path.join(HERE, "out", "delta_frozen.json")
def it1_load_frozen(fn=None):
    """Read out/delta_frozen.json. Refuses if missing, smoke-built, or delta is None."""
    fn = fn or FROZEN_PATH
    if not os.path.exists(fn): raise RuntimeError("IT1 refused: no delta_frozen.json (run it1-freeze)")
    d = json.load(open(fn, encoding="utf-8"))
    if d.get("smoke"): raise RuntimeError("IT1 refused: frozen delta built from smoke grades")
    if d.get("delta") is None: raise RuntimeError("IT1 refused: frozen delta is None (NO_DELTA)")
    return d
def it1_delta_gate(fn=None):
    return it1_load_frozen(fn)
def it1_resolve_delta(draw, delta=None, smoke=False, fn=None):
    """delta=0 control is always 0. Explicit --delta is used as-is (diag21 deviation). Else freeze file. Smoke still needs --delta."""
    if draw == IT1_D0_DRAW: return 0.0
    if delta is not None: return delta
    if smoke: raise RuntimeError("IT1_DELTA not set: smoke row needs an explicit --delta")
    return it1_load_frozen(fn)["delta"]
def it1_freeze(boxes=("B10", "B12"), grade_dir=None, outfile=None, skip_existing=False):
    """Largest candidate that pick_verdict.valid on BOTH B10 and B12 [assumed rule]. Writes out/delta_frozen.json.
    No common pass => print NO_DELTA and return 1; does not write a usable freeze."""
    grade_dir = grade_dir or os.path.join(HERE, "out")
    outfile = outfile or FROZEN_PATH
    if skip_existing and os.path.exists(outfile):
        print(json.dumps(dict(skipped=True, path=outfile), default=float), flush=True); return 0
    grades, valid = {}, {}
    for b in boxes:
        fn = os.path.join(grade_dir, f"it1_pick_grade_{b}.json")
        if not os.path.exists(fn):
            print("NO_DELTA", flush=True); return 1
        g = json.load(open(fn, encoding="utf-8")); grades[b] = g
        valid[b] = {float(k) for k, v in g.get("candidates", {}).items() if v.get("valid")}
    common = set.intersection(*valid.values()) if valid else set()
    smoke = any(g.get("smoke") for g in grades.values())
    chosen = max(common) if common else None
    rows = {b: dict(chosen=g.get("chosen"), valid=sorted(valid[b]), n_rows=g.get("n_rows"), smoke=g.get("smoke"), spec=g.get("spec"),
                    candidates={k: dict(n=v.get("n"), valid=v.get("valid"), reason=v.get("reason")) for k, v in g.get("candidates", {}).items()})
            for b, g in grades.items()}
    out = dict(delta=chosen, rule="largest delta that passes on BOTH B10 and B12 [assumed]", boxes=rows,
               smoke=bool(smoke), spec=FINAL_SPEC_HASH, spec_file=spec_hash(),
               run_py=hashlib.sha256(open(os.path.join(HERE, "run.py"), "rb").read()).hexdigest()[:8].upper(),
               grade_files={b: os.path.join(grade_dir, f"it1_pick_grade_{b}.json") for b in boxes})
    if chosen is None or smoke:
        print("NO_DELTA", flush=True)
        print(json.dumps(out, indent=1, default=float), flush=True)
        return 1
    os.makedirs(os.path.dirname(outfile) or ".", exist_ok=True)
    txt = json.dumps(out, indent=1, default=float); open(outfile, "w", encoding="utf-8").write(txt); print(txt, flush=True)
    return 0
def it1_cal(box, steps=None, outdir="it1", skip_existing=False):
    """alpha=1 exact BPST: raw rho unflowed vs after the pre-flow; the shift is the calibration systematic (rev 18)."""
    from kernels import Loops
    fn = os.path.join(HERE, "out", outdir, f"cal_{box}.json")
    if skip_existing and os.path.exists(fn):
        rec = json.load(open(fn, encoding="utf-8")); print(json.dumps(dict(skipped=True, path=fn, box=box), default=float), flush=True); return rec
    rho = IT1_GRIDS[box]; lat = Lattice(*BOXES[box], alpha=1.0); lp = Loops(lat, IT1_EPS); c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2])
    U = lp.flat(lat.bpst_links(rho, centre=c)); r0 = lp.rho_moment(U, centre=c); n = steps or int(round(flow_tf(rho)/FLOW_STEP))
    U, _ = lp.flow(U, h=FLOW_STEP, max_steps=n, record=5); r1 = lp.rho_moment(U, centre=c)
    out = dict(test="IT1-cal", box=box, rho=rho, raw_unflowed=r0, raw_flowed=r1, cal=rho/r0, rel_shift=abs(r1-r0)/r0, steps=n, smoke=steps is not None,
               tag="[H3 deviation, accepted: Venus] unflowed calibration; flowed shift enters E_a as systematic")
    os.makedirs(os.path.dirname(fn), exist_ok=True); open(fn, "w").write(json.dumps(out, default=float)); print(json.dumps(out, default=float), flush=True)
def it1_window2(hist, ell, drift=None):
    """Helios/Venus (rev 20): fit the two disjoint halves of hist (t relative to the window start);
    flag (report-only) if they differ by > IT1_WIN_AGREE [assumed]. The graded drift stays the full-window fit."""
    t0, t1 = hist[0][0], hist[-1][0]; tm = t0 + 0.5*(t1-t0)
    d1, n1 = it1_fit_drift([h_ for h_ in hist if h_[0] <= tm+1e-12], ell); d2, n2 = it1_fit_drift([h_ for h_ in hist if h_[0] >= tm-1e-12], ell)
    flag = (d1 is not None and d2 is not None and abs(d1-d2) > IT1_WIN_AGREE*max(abs(d1), abs(d2)))
    return dict(drift_h1=d1, n_h1=n1, drift_h2=d2, n_h2=n2, t_split=tm, flag=bool(flag))
def it1_window_pair(hist, ell, T, agree=IT1_WIN_AGREE, settle=IT1_WIN_SETTLE):
    """Fit the two disjoint windows [T, 1.5 T] and [1.5 T, 2 T] (hist times from t=0 of the seed flow).
    20% flag unchanged (report-only). settled iff |h1-h2|/max < 10%."""
    if T is None or T <= 0 or not hist:
        return dict(drift_h1=None, n_h1=0, drift_h2=None, n_h2=0, t_split=None, T=T, flag=False, rel=None, settled=False)
    T = float(T); t1, t2, t3 = T, 1.5*T, 2.0*T
    d1, n1 = it1_fit_drift([(t, r) for t, r in hist if t1-1e-12 <= t <= t2+1e-12], ell)
    d2, n2 = it1_fit_drift([(t, r) for t, r in hist if t2-1e-12 <= t <= t3+1e-12], ell)
    mx = max(abs(d1 or 0.0), abs(d2 or 0.0))
    rel = (abs(d1-d2)/mx) if (d1 is not None and d2 is not None and mx > 0) else None
    return dict(drift_h1=d1, n_h1=n1, drift_h2=d2, n_h2=n2, t_split=t2, T=T, flag=bool(rel is not None and rel > agree),
                rel=rel, settled=bool(rel is not None and rel < settle))
def it1_choose_T(hist, ell, tf, t_max_over=IT1_T_MAX_OVER_TF, settle=IT1_WIN_SETTLE):
    """Smallest T in [t_f, t_max] whose windows [T,1.5T] and [1.5T,2T] disagree by < settle; else t_max.
    Found on delta=0, alpha=1 only. hist times from t=0 of the seed flow."""
    tf, t_max = float(tf), float(t_max_over)*float(tf)
    times = sorted({float(h[0]) for h in hist}) if hist else []
    t_end = times[-1] if times else 0.0
    cands = []
    for t in times:
        if tf-1e-12 <= t <= t_max+1e-12 and 2.0*t <= t_end+1e-12: cands.append(t)
    if tf > 0 and 2.0*tf <= t_end+1e-12: cands.append(tf)
    if t_end > 0: cands.append(min(t_max, 0.5*t_end))
    cands.append(t_max)
    cands = sorted({round(c, 12) for c in cands if c > 0})
    picked = last = None
    for T in cands:
        w = it1_window_pair(hist, ell, T, settle=settle); last = (T, w)
        if w["settled"] and w["n_h1"] >= 2 and w["n_h2"] >= 2:
            picked = (T, w); break
    if picked is None:
        T, w = last if last is not None else (min(t_max, 0.5*t_end) if t_end else t_max, it1_window_pair(hist, ell, t_max, settle=settle))
        return dict(T=float(T), settled=False, windows=w, t_f=tf, t_max=t_max, note="cap (windows not <10%)")
    T, w = picked
    return dict(T=float(T), settled=True, windows=w, t_f=tf, t_max=t_max, note="windows <10%")
def it1_load_T(box=None, fn=None):
    """Read out/it1_T.json. Missing file => {} / None. Per-box record has T, t_f, settled."""
    fn = fn or IT1_T_PATH
    if not os.path.exists(fn): return {} if box is None else None
    d = json.load(open(fn, encoding="utf-8"))
    boxes = d.get("boxes", d)
    return boxes if box is None else boxes.get(box)
def it1_apply_T_ratio(src_box, dest_boxes, path=None):
    """Copy T/t_f from src_box onto dest_boxes (diag21: measure B12, apply to B10 and B12)."""
    path = path or IT1_T_PATH
    allT = dict(boxes={}, spec=FINAL_SPEC_HASH, smoke=False)
    if os.path.exists(path):
        try:
            prev = json.load(open(path, encoding="utf-8"))
            if isinstance(prev, dict):
                allT["boxes"] = dict(prev.get("boxes", {}))
                allT["smoke"] = bool(prev.get("smoke"))
                allT["spec"] = prev.get("spec", FINAL_SPEC_HASH)
        except Exception:
            pass
    src = allT["boxes"].get(src_box)
    if not src or not src.get("T") or not src.get("t_f"):
        raise RuntimeError(f"it1_apply_T_ratio: {src_box} has no T in {path}")
    ratio = float(src["T"])/float(src["t_f"])
    dests = [b.strip() for b in (dest_boxes.split(",") if isinstance(dest_boxes, str) else dest_boxes) if b and str(b).strip()]
    for b in dests:
        tf = flow_tf(IT1_GRIDS[b])
        if b == src_box:
            allT["boxes"][b] = dict(src, T_over_tf=ratio)
        else:
            allT["boxes"][b] = dict(box=b, T=ratio*tf, t_f=tf, T_over_tf=ratio, copied_from=src_box,
                                    settled=src.get("settled"), t_max=src.get("t_max"), spec=FINAL_SPEC_HASH,
                                    note=f"T/t_f copied from {src_box}")
    allT["ratio"] = ratio; allT["src"] = src_box; allT["spec"] = FINAL_SPEC_HASH
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path+".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(allT, indent=1, default=float)); os.replace(tmp, path)
    out = dict(ratio=ratio, src=src_box, T={b: allT["boxes"][b]["T"] for b in dests})
    print(json.dumps(out, default=float), flush=True); return out
def it1_find_T(box, steps=None, path=None, t_max_over=None, flow_max_over=None, apply_ratio_to=None, skip_existing=False):
    """delta=0, alpha=1 flow; pick T; write/merge out/it1_T.json.
    Full chain: flow to 2*(IT1_T_MAX_OVER_TF)*t_f. diag21: stop at 10% settle or flow_max_over*t_f (6)."""
    from kernels import Loops, generic_seed
    path = path or IT1_T_PATH
    t_max_over = IT1_T_MAX_OVER_TF if t_max_over is None else float(t_max_over)
    flow_max_over = (2.0*t_max_over) if flow_max_over is None else float(flow_max_over)
    dests = apply_ratio_to
    if skip_existing and os.path.exists(path):
        prev = json.load(open(path, encoding="utf-8")); boxes = prev.get("boxes", prev)
        if box in boxes and boxes[box].get("T") is not None:
            rec = boxes[box]
            if dests: it1_apply_T_ratio(box, dests, path)
            print(json.dumps(dict(skipped=True, box=box, T=rec.get("T")), default=float), flush=True); return rec
    rho = IT1_GRIDS[box]; lat = Lattice(*BOXES[box], alpha=1.0); lp = Loops(lat, IT1_EPS)
    ell = float(lat.r[-1]); c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2]); tf = flow_tf(rho)
    n_max = steps or int(round(flow_max_over*tf/FLOW_STEP)); n_chunk = n_max if steps else max(int(round(tf/FLOW_STEP)), 1)
    t0 = time.perf_counter()
    cal = rho/lp.rho_moment(lp.flat(lat.bpst_links(rho, centre=c)), centre=c); rf = lambda W: cal*lp.rho_moment(W, centre=c)
    U = generic_seed(lat, rho, seed=IT1_BASE_SEED, centre=c); recn = 1 if steps else IT1_REC; mono = True; hist = []; t_off = 0.0; n_done = 0
    try:
        while n_done < n_max:
            n_this = min(n_chunk, n_max - n_done)
            U, h = lp.flow(U, h=FLOW_STEP, max_steps=n_this, record=min(recn, n_this), rho_fn=rf)
            hist.extend((t + t_off, r) for t, r in h)
            t_off += n_this*FLOW_STEP; n_done += n_this
            hist.append((t_off, rf(U)))
            choice = it1_choose_T(hist, ell, tf, t_max_over=t_max_over) if hist else None
            if choice and choice.get("settled") and not steps: break
    except FloatingPointError:
        mono = False
        choice = it1_choose_T(hist, ell, tf, t_max_over=t_max_over) if hist else None
    if not hist: choice = dict(T=tf, settled=False, windows=None, t_f=tf, t_max=t_max_over*tf, note="no hist")
    elif choice is None: choice = it1_choose_T(hist, ell, tf, t_max_over=t_max_over)
    rec_out = dict(box=box, alpha=1.0, delta=0.0, **choice, monotone=mono, n_steps=n_done, flow_max_over=flow_max_over,
                   t_max_over=t_max_over, smoke=steps is not None, wall_s=time.perf_counter()-t0, spec=FINAL_SPEC_HASH, hist_n=len(hist))
    allT = dict(boxes={}, spec=FINAL_SPEC_HASH, smoke=False)
    if os.path.exists(path):
        try:
            prev = json.load(open(path, encoding="utf-8"))
            if isinstance(prev, dict):
                allT["boxes"] = dict(prev.get("boxes", prev if "T" not in prev else {}))
                allT["smoke"] = bool(prev.get("smoke"))
        except Exception:
            pass
    allT["boxes"][box] = rec_out; allT["spec"] = FINAL_SPEC_HASH; allT["smoke"] = bool(allT.get("smoke")) or bool(steps is not None)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path+".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(allT, indent=1, default=float)); os.replace(tmp, path)
    if dests: it1_apply_T_ratio(box, dests, path)
    print(json.dumps(rec_out, default=float), flush=True); return rec_out
def it1_row(box, alpha, draw, steps=None, outdir="it1", delta=None, save_evecs=False, t_path=None, skip_existing=False, delta_note=None):
    from kernels import Loops, generic_seed
    d0 = (draw == IT1_D0_DRAW)
    fn = it1_row_path(box, alpha, draw, outdir, delta=None if d0 else delta)
    if skip_existing and os.path.exists(fn):
        rec = json.load(open(fn, encoding="utf-8")); print(json.dumps(dict(skipped=True, path=fn, box=box, alpha=alpha, draw=draw), default=float), flush=True); return rec
    use_delta = it1_resolve_delta(draw, delta, smoke=steps is not None)
    rho = IT1_GRIDS[box]; lat = Lattice(*BOXES[box], alpha=alpha); lp = Loops(lat, IT1_EPS); ell = float(lat.r[-1])
    c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2]); t0 = time.perf_counter(); tf = flow_tf(rho)
    Trec = it1_load_T(box, fn=t_path); T_file = (Trec or {}).get("T") if Trec else None
    if steps is not None:
        n_pre = n_drift = steps; T_win = n_pre*FLOW_STEP
    else:
        T_win = float(T_file) if T_file is not None else tf
        n_pre = n_drift = int(round(T_win/FLOW_STEP))
    U = generic_seed(lat, rho, seed=IT1_BASE_SEED, centre=c)
    if not d0: U = it1_perturb(lp, U, draw, use_delta)
    U, _ = lp.flow(U, h=FLOW_STEP, max_steps=n_pre, record=min(IT1_REC, n_pre) if n_pre else 1)
    Q_pre = lp.charge(U, lp.field_strength(U))
    lat1 = Lattice(*BOXES[box], alpha=1.0); lp1 = Loops(lat1, IT1_EPS)
    cal = rho/lp1.rho_moment(lp1.flat(lat1.bpst_links(rho, centre=c)), centre=c); del lat1, lp1
    rf = lambda W: cal*lp.rho_moment(W, centre=c)
    rec = min(IT1_REC, n_drift) if n_drift else 1
    U, hist = lp.flow(U, h=FLOW_STEP, max_steps=n_drift, record=rec, rho_fn=rf)
    hist.append((n_drift*FLOW_STEP, rf(U)))
    hist = [(t + T_win, r) for t, r in hist]
    drift, npts = it1_fit_drift(hist, ell)
    W2 = it1_window_pair(hist, ell, T_win)
    Q = lp.charge(U, lp.field_strength(U))
    out = dict(test="IT1", box=box, alpha=alpha, draw=draw, set=("0" if d0 else "A" if draw in IT1_DRAWS_A else "B"), rng_seed=None if d0 else IT1_RNG_BASE+draw,
               delta=use_delta, perturbation="none (delta=0 control)" if d0 else "smooth low-k (rev 19)",
               drift_h1=W2["drift_h1"], n_h1=W2["n_h1"], drift_h2=W2["drift_h2"], n_h2=W2["n_h2"], windows_tf=[[1.0, 1.5], [1.5, 2.0]],
               windows_t=[[T_win, 1.5*T_win], [1.5*T_win, 2*T_win]], t_f=tf, T=T_win, T_from_file=T_file, window_disagree_flag=W2["flag"],
               window_rel=W2.get("rel"), window_settled=W2.get("settled"), window_note="report-only (Helios); 20% flag unchanged",
               absQ_minus_1=abs(abs(Q)-1), absQ_note="report-only per box (rev 20)", base_seed=IT1_BASE_SEED,
               eps=IT1_EPS, rho_seed=rho, ell=ell, steps_pre=n_pre, steps_drift=n_drift, hist=hist, drift=drift, n_fit=npts, Q_pre=Q_pre, Q=Q, rho_cal=cal,
               rho_note="calibrated second moment (r>=2a), true/raw from unflowed exact BPST, same grid, alpha=1 [H3 deviation, accepted: Venus]",
               wall_s=time.perf_counter()-t0, free_ram_gb=free_ram_gb(), spec=FINAL_SPEC_HASH, smoke=steps is not None, orbifold=(alpha == ORBIFOLD))
    note = delta_note or (DIAG21_DELTA_NOTE if (not d0 and outdir and "diag21" in outdir.replace("\\", "/")) else None)
    if note: out["delta_note"] = note
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    if save_evecs:
        vals, vecs = lp.lanczos(U, k=min(8, LANCZOS_VECTORS), lam=1.0, free_fn=free_ram_gb)
        efn = fn.replace(".json", "_evecs.npy"); np.save(efn, vecs)
        out["evals"] = [float(x) for x in vals]; out["evecs_path"] = efn
    tmp = fn+".tmp"; open(tmp, "w").write(json.dumps(out, default=float)); os.replace(tmp, fn); print(json.dumps({k: v for k, v in out.items() if k != "hist"}, default=float), flush=True)
def it1_grade_rows(R, cal=None, mode=None, delta=None, frozen_fn=None):
    """Cut IT1 grading (rev 21). Paired Delta per draw; correlation of drift(alpha,d) with drift(1,d) decides paired (sigma_pair^2/6) vs
    unpaired (sigma^2/3) BEFORE Delta is read; E = sqrt(E_a^2 + that); E_a = Richardson term (+) |dlnDelta/dlnrho|*(shift/rho)*|Delta|.
    Guard: |meanA-meanB| <= 3*sqrt(sigma1^2/3) (6+6) or 3*sigma1*sqrt(2/3) [small sample] (3+3), sigma1 = per-seed spread at alpha=1.
    guard_pass is that alpha=1 A-vs-B test only (empty boxes skipped). GRADED status still needs cal rows and the delta=0 control.
    3-grid Richardson on B10/B12/B14 replaces p=4 assumed when the order is measurable; else 2-grid p=4 tagged
    [assumed, 3-grid order not measurable]. delta is the frozen pick (out/delta_frozen.json); IT1_DELTA stays None.
    Rev 20 gates/thresholds otherwise unchanged."""
    mode = mode or IT1_GUARD_MODE; cal = cal or {}
    if delta is None:
        try: delta = it1_load_frozen(frozen_fn)["delta"]
        except RuntimeError: delta = IT1_DELTA
    out = dict(test="IT1 (cut, rev 21)", guard_mode=mode + (" [small sample]" if mode == "3+3" else ""), grids={}, guard={}, alphas={}, delta=delta, rng_base=IT1_RNG_BASE, pairing={})
    boxes_present = {r["box"] for r in R}; A_ = {}
    for b in IT1_GRIDS:
        A = {r["draw"]: r["drift"] for r in R if r["box"] == b and r["alpha"] == 1.0 and r["draw"] in IT1_DRAWS_A and r["drift"] is not None}; A_[b] = A
        if mode == "6+6": S1, S2 = list(A.values()), [r["drift"] for r in R if r["box"] == b and r["alpha"] == 1.0 and r["draw"] in IT1_DRAWS_B and r["drift"] is not None]
        else: S1, S2 = [A[d] for d in IT1_DRAWS_A[:3] if d in A], [A[d] for d in IT1_DRAWS_A[3:] if d in A]
        s1 = float(np.std(list(A.values()), ddof=1)) if len(A) > 1 else None
        bound = None if s1 is None else (IT1_GUARD_K*np.sqrt(s1**2/3) if mode == "6+6" else IT1_GUARD_K*s1*np.sqrt(2/3))
        md = abs(np.mean(S1)-np.mean(S2)) if S1 and S2 else None
        out["guard"][b] = dict(n1=len(S1), n2=len(S2), mean_diff=md, sigma1=s1, bound=bound, ok=bool(md is not None and bound is not None and bound > 0 and md <= bound))
        corr = {}
        for al in IT1_ALPHAS[1:]:
            P = [(A[r["draw"]], r["drift"]) for r in R if r["box"] == b and r["alpha"] == al and r["draw"] in A and r["drift"] is not None]
            corr[str(al)] = float(np.corrcoef(*zip(*P))[0, 1]) if len(P) > 2 else None
        out["pairing"][b] = corr
    live_pair = [v for b, g in out["pairing"].items() if out["guard"][b]["n1"] > 0 for v in g.values()]
    paired = bool(live_pair) and all(v is not None and v >= IT1_PAIR_CORR_MIN for v in live_pair)
    out["paired"] = paired; out["pairing_rule"] = f"paired iff all per-seed correlations >= {IT1_PAIR_CORR_MIN} (decided before Delta)"
    for b in IT1_GRIDS:
        A = A_[b]
        for al in IT1_ALPHAS[1:]:
            xs = {r["draw"]: r["drift"] for r in R if r["box"] == b and r["alpha"] == al and r["draw"] in A and r["drift"] is not None}
            ds = [xs[d]-A[d] for d in xs]
            if paired: sig = float(np.std(ds, ddof=1)) if len(ds) > 1 else None; var = None if sig is None else sig**2/IT1_SEEDS
            else:
                sa = np.std(list(xs.values()), ddof=1) if len(xs) > 1 else None; s1 = np.std(list(A.values()), ddof=1) if len(A) > 1 else None
                sig = None if sa is None or s1 is None else float(np.sqrt((sa**2+s1**2)/2)); var = None if sig is None else sig**2/3
            out["grids"].setdefault(b, {})[str(al)] = dict(n=len(ds), Delta=float(np.mean(ds)) if ds else None, sigma=sig, var_term=var)
    r4 = (BOXES["B12"][0]/BOXES["B10"][0])**IT1_PA - 1; E_all = []
    shift = max([cal[b]["rel_shift"] for b in cal], default=None)
    a_pts = [1.0/BOXES[b][0] for b in IT1_BOX_ORDER]
    for al in IT1_ALPHAS[1:]:
        g10 = out["grids"].get("B10", {}).get(str(al), {}); g12 = out["grids"].get("B12", {}).get(str(al), {})
        g14 = out["grids"].get("B14", {}).get(str(al), {})
        if g10.get("Delta") is None or g12.get("Delta") is None or g12.get("var_term") is None:
            out["alphas"][str(al)] = dict(verdict="NOT COMPUTED (YET)"); continue
        if g10["Delta"]*g12["Delta"] > 0:
            slope = abs(np.log(g12["Delta"]/g10["Delta"])/np.log(IT1_GRIDS["B12"]/IT1_GRIDS["B10"])); stag = "[measured, B10/B12]"
        else: slope = IT1_CAL_SLOPE_DEFAULT; stag = "[assumed]"
        Ea_r4 = abs(g12["Delta"]-g10["Delta"])/r4; Dinf_p4 = g12["Delta"] + (g12["Delta"]-g10["Delta"])/r4
        order = None; Dinf = Dinf_p4; Ea_r = Ea_r4; var = g12["var_term"]; finest = "B12"
        order_gate = "[assumed, 3-grid order not measurable]"
        if g14.get("Delta") is not None:
            r3 = richardson_3pt([g10["Delta"], g12["Delta"], g14["Delta"]], a_pts)
            if r3["order"] is not None:
                order = float(r3["order"]); Dinf = float(r3["extrap"]); Ea_r = float(r3["E_a"])
                if g14.get("var_term") is not None: var = g14["var_term"]; finest = "B14"
                order_gate = f"[measured, 3-grid p={order:.3g}]"
        Ea_sys = slope*shift*abs(g12["Delta"]) if shift is not None else None
        Ea = float(np.hypot(Ea_r, Ea_sys or 0.0)); E = float(np.sqrt(Ea**2 + var)); E_all.append(E)
        v = "AGAINST (|Delta| <= k_Delta*E)" if abs(Dinf) <= K_DELTA*E else "UNDECIDED (|Delta| > k_Delta*E; support needs a measured order, 2-grid gate report-only)"
        rec = dict(Delta_B10=g10["Delta"], Delta_B12=g12["Delta"], Delta_B14=g14.get("Delta"), Delta_inf=Dinf, Delta_inf_p4=Dinf_p4,
                   E_a_richardson=Ea_r, cal_slope=slope, cal_slope_tag=stag,
                   E_a_cal_sys=Ea_sys if Ea_sys is not None else "NOT COMPUTED (YET): no cal rows", E_a=Ea, E=E, k_Delta=K_DELTA, verdict=v,
                   orbifold=(al == ORBIFOLD), order=order, order_gate=order_gate, finest_grid=finest)
        out["alphas"][str(al)] = rec
    out["E_min"] = min(E_all) if E_all else None
    # rev 20 delta=0 control (failable): |mean Delta_delta - Delta_0| <= 3 E_Delta at every alpha, on each grid present in R
    ctrl = {}; ctrl_ok = True
    for b in IT1_GRIDS:
        if b not in boxes_present: continue
        z = {r["alpha"]: r["drift"] for r in R if r["box"] == b and r.get("draw") == IT1_D0_DRAW and r["drift"] is not None}
        z1 = z.get(1.0); ctrl[b] = {}
        for al in IT1_ALPHAS[1:]:
            a_ = out["alphas"].get(str(al), {}); g = out["grids"][b][str(al)]
            if z1 is None or al not in z or g["Delta"] is None or "E" not in a_: ctrl[b][str(al)] = dict(ok=None, note="NOT COMPUTED (YET)"); ctrl_ok = False; continue
            D0 = z[al]-z1; diff = g["Delta"]-D0; bound = 3*a_["E"]; abs_diff = abs(diff); ok_ = abs_diff <= bound; ctrl_ok &= bool(ok_)
            ctrl[b][str(al)] = dict(Delta_delta=g["Delta"], Delta_0=D0, diff=diff, abs_diff=abs_diff, bound=bound,
                                   ratio=(abs_diff/bound if bound else None), ok=bool(ok_))
        As = [r["drift"] for r in R if r["box"] == b and r["alpha"] == 1.0 and r.get("draw") in IT1_DRAWS_A and r["drift"] is not None]
        ctrl[b]["drift_shift_by_delta_alpha1"] = dict(value=(np.mean(As)-z1) if As and z1 is not None else None, rel=((np.mean(As)-z1)/z1) if As and z1 else None, note="report-only")
        wins = {}
        for r in R:
            if r["box"] != b or r.get("draw") != IT1_D0_DRAW: continue
            fl = r.get("window_disagree_flag"); wins[str(r["alpha"])] = dict(
                drift_h1=r.get("drift_h1"), drift_h2=r.get("drift_h2"), n_h1=r.get("n_h1"), n_h2=r.get("n_h2"),
                flag=(None if fl is None else bool(fl)))
        ctrl[b]["windows_delta0"] = wins
        ctrl[b]["window_flags_delta0"] = {k: v["flag"] for k, v in wins.items()}
        ctrl[b]["absQ_minus_1_delta0"] = {str(r["alpha"]): r.get("absQ_minus_1") for r in R if r["box"] == b and r.get("draw") == IT1_D0_DRAW}
    out["delta0_control"] = ctrl; out["delta0_control_pass"] = bool(ctrl_ok)
    reasons = []
    if not all(g["ok"] for g in out["guard"].values() if g["n1"] > 0): reasons.append("alpha1_guard")
    if shift is None: reasons.append("cal_missing")
    if not ctrl_ok: reasons.append("delta0_control")
    out["fail_reasons"] = reasons
    out["guard_pass"] = all(bool(g["ok"]) for g in out["guard"].values() if g["n1"] > 0)  # alpha=1 A-vs-B only; empty boxes skipped
    out["status"] = "GRADED" if not reasons else "REPORT-ONLY (" + ", ".join(reasons) + ")"
    return out
def it1_grade(indir="it1", outfile=None):
    import glob
    fs = glob.glob(os.path.join(HERE, "out", indir, "*.json"))
    R = [json.load(open(f)) for f in fs if not os.path.basename(f).startswith("cal_")]
    cal = {json.load(open(f))["box"]: json.load(open(f)) for f in fs if os.path.basename(f).startswith("cal_")}
    out = it1_grade_rows(R, cal); out.update(spec=FINAL_SPEC_HASH, rows=len(R), expected=len(it1_jobs()), cal=cal)
    txt = json.dumps(out, indent=1, default=float)
    fn = outfile or os.path.join(HERE, "out", f"{indir}_grade.json")
    os.makedirs(os.path.dirname(fn) or ".", exist_ok=True); open(fn, "w").write(txt); print(txt); return out
def it1_diag21_grade(indir="diag21/it1", outfile=None, t_path=None):
    """Report-only diag21 grade: delta0_control pass/fail + ratios, window drift, linearity. No AGAINST/UNDECIDED verdict."""
    import glob
    fs = glob.glob(os.path.join(HERE, "out", indir, "*.json"))
    rows = [json.load(open(f, encoding="utf-8")) for f in fs if not os.path.basename(f).startswith("cal_")]
    cal = {json.load(open(f, encoding="utf-8"))["box"]: json.load(open(f, encoding="utf-8")) for f in fs if os.path.basename(f).startswith("cal_")}
    R = [r for r in rows if abs(float(r.get("delta") or 0.0) - DIAG21_LIN_DELTA) > 1e-12]
    Rlin = [r for r in rows if abs(float(r.get("delta") or 0.0) - DIAG21_LIN_DELTA) < 1e-12]
    draws = list(range(DIAG21_SEEDS))
    grids = {}; boxes_present = {r["box"] for r in R}
    for b in DIAG21_BOXES:
        A = {r["draw"]: r["drift"] for r in R if r["box"] == b and r["alpha"] == 1.0 and r["draw"] in draws and r["drift"] is not None}
        for al in DIAG21_ALPHAS:
            if al == 1.0: continue
            xs = {r["draw"]: r["drift"] for r in R if r["box"] == b and r["alpha"] == al and r["draw"] in A and r["drift"] is not None}
            ds = [xs[d]-A[d] for d in xs]
            n = len(ds); sig = float(np.std(ds, ddof=1)) if n > 1 else None
            var = None if sig is None else sig**2/n
            grids.setdefault(b, {})[str(al)] = dict(n=n, Delta=float(np.mean(ds)) if ds else None, sigma=sig, var_term=var)
    shift = max([cal[b]["rel_shift"] for b in cal], default=None) if cal else None
    r4 = (BOXES["B12"][0]/BOXES["B10"][0])**IT1_PA - 1
    E_at = {}
    for al in DIAG21_ALPHAS:
        if al == 1.0: continue
        g10 = grids.get("B10", {}).get(str(al), {}); g12 = grids.get("B12", {}).get(str(al), {})
        if g10.get("Delta") is None or g12.get("Delta") is None or g12.get("var_term") is None: continue
        if g10["Delta"]*g12["Delta"] > 0:
            slope = abs(np.log(g12["Delta"]/g10["Delta"])/np.log(IT1_GRIDS["B12"]/IT1_GRIDS["B10"]))
        else: slope = IT1_CAL_SLOPE_DEFAULT
        Ea_r = abs(g12["Delta"]-g10["Delta"])/r4
        Ea_sys = slope*shift*abs(g12["Delta"]) if shift is not None else 0.0
        Ea = float(np.hypot(Ea_r, Ea_sys or 0.0)); E = float(np.sqrt(Ea**2 + g12["var_term"]))
        E_at[str(al)] = dict(E=E, E_a=Ea, Delta_B10=g10["Delta"], Delta_B12=g12["Delta"], cal_slope=slope)
    ctrl = {}; ctrl_ok = True; any_cell = False
    for b in DIAG21_BOXES:
        if b not in boxes_present: continue
        z = {r["alpha"]: r["drift"] for r in R if r["box"] == b and r.get("draw") == IT1_D0_DRAW and r["drift"] is not None}
        z1 = z.get(1.0); ctrl[b] = {}
        for al in DIAG21_ALPHAS:
            if al == 1.0: continue
            g = grids.get(b, {}).get(str(al), {}); ea = E_at.get(str(al))
            if z1 is None or al not in z or g.get("Delta") is None or not ea:
                ctrl[b][str(al)] = dict(ok=None, note="NOT COMPUTED (YET)"); ctrl_ok = False; continue
            D0 = z[al]-z1; diff = g["Delta"]-D0; bound = 3*ea["E"]; abs_diff = abs(diff)
            ok_ = abs_diff <= bound + 1e-12
            any_cell = True; ctrl_ok &= bool(ok_)
            ctrl[b][str(al)] = dict(Delta_delta=g["Delta"], Delta_0=D0, diff=diff, abs_diff=abs_diff, bound=bound,
                                   ratio=(abs_diff/bound if bound > 0 else 0.0), ok=bool(ok_))
        wins = {}
        for r in R:
            if r["box"] != b or r.get("draw") != IT1_D0_DRAW: continue
            rel = r.get("window_rel"); fl = r.get("window_disagree_flag")
            wins[str(r["alpha"])] = dict(drift_h1=r.get("drift_h1"), drift_h2=r.get("drift_h2"),
                                         n_h1=r.get("n_h1"), n_h2=r.get("n_h2"), rel=rel,
                                         flag=(None if fl is None else bool(fl)), settled=r.get("window_settled"), T=r.get("T"))
        ctrl[b]["windows_delta0"] = wins
        ctrl[b]["window_flags_delta0"] = {k: v["flag"] for k, v in wins.items()}
    if not any_cell: ctrl_ok = False
    base_d = next((r["drift"] for r in R if r["box"]=="B10" and r["alpha"]==1.0 and r.get("draw")==IT1_D0_DRAW), None)
    d001 = [r["drift"] for r in R if r["box"]=="B10" and r["alpha"]==1.0 and r.get("draw") in draws and r["drift"] is not None]
    d002 = [r["drift"] for r in Rlin if r["box"]=="B10" and r["alpha"]==1.0 and r.get("draw") in draws and r["drift"] is not None]
    lin = pick_linearity(dict(drift=base_d), {str(DIAG21_DELTA): dict(drift=d001), str(DIAG21_LIN_DELTA): dict(drift=d002)})
    Trec = it1_load_T(fn=t_path or os.path.join(os.path.dirname(os.path.join(HERE, "out", indir)), "it1_T.json"))
    if not Trec:
        Trec = it1_load_T()
    out = dict(test="IT1 (cut, rev 21 diag21)", status="REPORT-ONLY (diag21)", delta=DIAG21_DELTA, delta_note=DIAG21_DELTA_NOTE,
               spec=FINAL_SPEC_HASH, rows=len(R), lin_rows=len(Rlin), expected=len(it1_jobs_diag21()),
               grids=grids, E=E_at, delta0_control=ctrl, delta0_control_pass=bool(ctrl_ok and any_cell),
               windows={b: (ctrl.get(b) or {}).get("windows_delta0") for b in DIAG21_BOXES},
               linearity=lin, T=Trec, cal={b: dict(rel_shift=cal[b]["rel_shift"]) for b in cal},
               note="report-only; no AGAINST/UNDECIDED verdict")
    txt = json.dumps(out, indent=1, default=float)
    fn = outfile or os.path.join(HERE, "out", "diag21", "it1_grade.json")
    os.makedirs(os.path.dirname(fn) or ".", exist_ok=True); open(fn, "w", encoding="utf-8").write(txt); print(txt); return out
def smoke_cut(steps=1, only=None):
    """<=5 min end-to-end smoke: one IT1 row set (alpha=1, 0.55, guard repeat) per IT1 grid and one IT3 row per IT3 grid, `steps` RK3 steps each."""
    t0 = time.perf_counter()
    for b in IT1_GRIDS:
        it1_cal(b, steps=steps, outdir="smoke_it1")
        for al, d in (((1.0, 0), (1.0, 6), (0.55, 0), (1.0, IT1_D0_DRAW), (0.55, IT1_D0_DRAW)) if b == "B10" else ((1.0, 0), (1.0, IT1_D0_DRAW))): it1_row(b, al, d, steps=steps, outdir="smoke_it1", delta=IT1_DELTA_CANDIDATES[0])
    it1_grade("smoke_it1")
    if only == "it1": print("SMOKE wall_s", time.perf_counter()-t0, flush=True); return
    for b in IT3_GRIDS:
        it3_row(b, 1.0, 0, kind="bpst", steps=steps, outdir="smoke_it3"); it3_row(b, 1.0, 0, steps=steps, outdir="smoke_it3"); it3_row(b, 0.55, 0, steps=steps, outdir="smoke_it3")
    it3_grade("smoke_it3"); print("SMOKE wall_s", time.perf_counter()-t0, flush=True)
# ---- diag22 (NanoRibbon job, 2026-10-22): IT1 re-check on B10 + tip probe. Rules frozen by Venus/Helios before the run. ----
DIAG22_OUT = "diag22"
DIAG22_BOX = "B10"; DIAG22_ALPHAS = (1.0, 0.5); DIAG22_SEEDS = 2; DIAG22_DELTAS = (0.003, 0.0015)
DIAG22_T_CAP_OVER_TF = 6.0                         # T cap = 6 t_f (B10: 0.6)
DIAG22_FLOW_MAX_OVER_TF = 12.0                     # find-T history long enough that 2T fits at the cap
DIAG22_WIN_MAX = 0.10                              # PASS: window drift |h1-h2|/max <= 10% on every delta=0 row
DIAG22_LIN_BAND = (1.7, 2.3)                       # PASS: (drift(0.003)-drift0)/(drift(0.0015)-drift0) at alpha=1
DIAG22_RHO_SHIFT_MAX = 0.05                        # PASS: calibrated rho shift at the new T <= 5%
DIAG22_CTRL_SLOPE = IT1_CAL_SLOPE_DEFAULT          # B10 only: no B12 Richardson term; cal slope [assumed] 2
TIP_BOXES = {"B8": (8, 20, 16, 16), "B10": BOXES["B10"], "B12": BOXES["B12"], "B16": BOXES["B16"]}
TIP_ALPHAS = (1.0, 0.5); TIP_RHO_OVER_MR = 0.3     # rho = 0.3 M_r a (rev 21 convention, fixed rho/l)
TIP_FLOW_OVER_TF = 6.0                             # flow to 6 t_f(rho): equal t/rho^2 => equal physical flow time
TIP_REC = 5
TIP_THRESHOLDS = None                              # NOT FOUND in any written spec => tip probe REPORT-ONLY (no DELTA_SPIKE/INTEGRABLE_SINGULAR/REGULAR)
def diag22_jobs():
    J = []
    for dl in DIAG22_DELTAS:
        for d in range(DIAG22_SEEDS):
            for al in DIAG22_ALPHAS: J.append((DIAG22_BOX, al, d, dl))
    for al in DIAG22_ALPHAS: J.append((DIAG22_BOX, al, IT1_D0_DRAW, 0.0))
    return J
def diag22_check_row_key(draw, delta):
    """H10 guard: a delta row must carry delta>0, a delta=0 control must be draw -1. Never mix."""
    if draw == IT1_D0_DRAW and float(delta or 0.0) != 0.0: raise ValueError("delta=0 control row with delta != 0")
    if draw != IT1_D0_DRAW and not (delta is not None and float(delta) > 0): raise ValueError(f"delta row draw={draw} needs delta>0, got {delta}")
def diag22_paths():
    base = os.path.join(HERE, "out", DIAG22_OUT)
    return dict(base=base, it1=f"{DIAG22_OUT}/it1", T=os.path.join(base, "it1_T.json"), grade=os.path.join(base, "it1_grade.json"), tip=os.path.join(base, "tip"))
def diag22_row(alpha, draw, delta, steps=None, skip_existing=False):
    diag22_check_row_key(draw, delta); P = diag22_paths()
    return it1_row(DIAG22_BOX, alpha, draw, steps=steps, outdir=P["it1"], delta=(None if draw == IT1_D0_DRAW else delta), t_path=P["T"],
                   skip_existing=skip_existing, delta_note="diag22 re-check")
def diag22_find_T(steps=None):
    P = diag22_paths()
    return it1_find_T(DIAG22_BOX, steps, path=P["T"], t_max_over=DIAG22_T_CAP_OVER_TF, flow_max_over=DIAG22_FLOW_MAX_OVER_TF)
def diag22_cal(steps=None):
    """alpha=1 exact BPST rho calibration, flowed to the NEW T (not t_f)."""
    from kernels import Loops
    P = diag22_paths(); box = DIAG22_BOX; Trec = it1_load_T(box, fn=P["T"]) or {}
    rho = IT1_GRIDS[box]; T = Trec.get("T") or flow_tf(rho); n = steps or int(round(T/FLOW_STEP))
    lat = Lattice(*BOXES[box], alpha=1.0); lp = Loops(lat, IT1_EPS); c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2])
    U = lp.flat(lat.bpst_links(rho, centre=c)); r0 = lp.rho_moment(U, centre=c)
    U, _ = lp.flow(U, h=FLOW_STEP, max_steps=n, record=5); r1 = lp.rho_moment(U, centre=c)
    out = dict(test="IT1-cal (diag22, at new T)", box=box, rho=rho, T=T, raw_unflowed=r0, raw_flowed=r1, cal=rho/r0, rel_shift=abs(r1-r0)/r0,
               steps=n, smoke=steps is not None, spec=FINAL_SPEC_HASH)
    fn = os.path.join(P["base"], "it1", f"cal_{box}.json"); os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, "w").write(json.dumps(out, default=float)); print(json.dumps(out, default=float), flush=True); return out
def diag22_grade_rows(rows, cal):
    """Explicit pass/fail per frozen criterion. Rows keyed by (alpha, draw, delta) from the row's OWN fields; duplicate keys refused (H10)."""
    key = {}
    for r in rows:
        diag22_check_row_key(r.get("draw"), r.get("delta"))
        k = (float(r["alpha"]), int(r["draw"]), float(r.get("delta") or 0.0))
        if k in key: raise ValueError(f"duplicate diag22 row {k}")
        key[k] = r
    dr = lambda al, d, dl: (key.get((al, d, dl)) or {}).get("drift")
    z = {al: dr(al, IT1_D0_DRAW, 0.0) for al in DIAG22_ALPHAS}
    crit = {}
    # 1 window drift on delta=0 rows
    w = {str(al): (key.get((al, IT1_D0_DRAW, 0.0)) or {}).get("window_rel") for al in DIAG22_ALPHAS}
    crit["window_drift"] = dict(rule=f"|h1-h2|/max <= {DIAG22_WIN_MAX} on every delta=0 row", values=w,
                                ok=bool(all(v is not None and v <= DIAG22_WIN_MAX for v in w.values())))
    # 2 linearity at alpha=1
    m = {}
    for dl in DIAG22_DELTAS:
        xs = [dr(1.0, d, dl) for d in range(DIAG22_SEEDS)]; xs = [x for x in xs if x is not None]
        m[str(dl)] = float(np.mean(xs)) if len(xs) == DIAG22_SEEDS else None
    hi, lo = m[str(max(DIAG22_DELTAS))], m[str(min(DIAG22_DELTAS))]; ratio = None
    if None not in (hi, lo, z[1.0]) and lo != z[1.0]: ratio = float((hi - z[1.0])/(lo - z[1.0]))
    crit["linearity"] = dict(rule=f"ratio in {list(DIAG22_LIN_BAND)}", drift0=z[1.0], mean_drift=m, ratio=ratio,
                             ok=bool(ratio is not None and DIAG22_LIN_BAND[0] <= ratio <= DIAG22_LIN_BAND[1]))
    # 3 delta=0 control at alpha=0.5, per delta
    shift = (cal or {}).get("rel_shift"); ctl = {}
    for dl in DIAG22_DELTAS:
        ds = [dr(0.5, d, dl) - dr(1.0, d, dl) for d in range(DIAG22_SEEDS) if dr(0.5, d, dl) is not None and dr(1.0, d, dl) is not None]
        if len(ds) < 2 or None in (z[1.0], z[0.5]): ctl[str(dl)] = dict(ok=False, note="NOT COMPUTED (YET)", n=len(ds)); continue
        D = float(np.mean(ds)); sig = float(np.std(ds, ddof=1)); D0 = z[0.5] - z[1.0]
        E = float(np.sqrt(sig**2/len(ds) + (DIAG22_CTRL_SLOPE*(shift or 0.0)*abs(D))**2)); diff = D - D0
        ctl[str(dl)] = dict(Delta_delta=D, Delta_0=D0, diff=diff, sigma=sig, n=len(ds), E=E, bound=3*E, ratio=(abs(diff)/(3*E) if E > 0 else None), ok=bool(abs(diff) <= 3*E))
    crit["delta0_control"] = dict(rule="|Delta_delta - Delta_0| <= 3E at alpha=0.5, each delta; E = sqrt(sigma^2/n + (2*shift*|Delta|)^2) [B10 only, slope assumed 2]",
                                  per_delta=ctl, ok=bool(ctl and all(v["ok"] for v in ctl.values())))
    crit["rho_cal_shift"] = dict(rule=f"rel_shift at new T <= {DIAG22_RHO_SHIFT_MAX}", value=shift, T=(cal or {}).get("T"),
                                 ok=bool(shift is not None and shift <= DIAG22_RHO_SHIFT_MAX))
    allok = all(c["ok"] for c in crit.values())
    exp = diag22_jobs(); have = {(al, d, dl) for (_, al, d, dl) in exp if (al, d, dl) in key}
    listed = [dict(alpha=r["alpha"], draw=r["draw"], delta=r.get("delta"), drift=r.get("drift"), window_rel=r.get("window_rel"), Q=r.get("Q"), T=r.get("T"))
              for k, r in sorted(key.items())]
    return dict(test="IT1 re-check (diag22)", status=("PASS" if allok else "REPORT-ONLY (" + ", ".join(k for k, c in crit.items() if not c["ok"]) + ")"),
                criteria=crit, rows=listed, n_rows=len(key), expected=len(exp), missing=[list(j[1:]) for j in exp if (j[1], j[2], j[3]) not in have],
                note="no further tuning; every row listed", spec=FINAL_SPEC_HASH)
def diag22_grade():
    import glob
    P = diag22_paths(); fs = glob.glob(os.path.join(P["base"], "it1", "*.json"))
    rows = [json.load(open(f, encoding="utf-8")) for f in fs if not os.path.basename(f).startswith("cal_")]
    cfn = os.path.join(P["base"], "it1", f"cal_{DIAG22_BOX}.json"); cal = json.load(open(cfn)) if os.path.exists(cfn) else None
    out = diag22_grade_rows(rows, cal); out["T"] = it1_load_T(DIAG22_BOX, fn=P["T"])
    tg = os.path.join(P["tip"], "tip_fit.json")
    if os.path.exists(tg): out["tip_probe"] = json.load(open(tg, encoding="utf-8"))
    txt = json.dumps(out, indent=1, default=float); os.makedirs(P["base"], exist_ok=True); open(P["grade"], "w", encoding="utf-8").write(txt); print(txt); return out
def diag22_tip_row(box, alpha, steps=None, rec=TIP_REC):
    """Peak action density (per dual 4-volume) at the tip cell vs flow time, plus action fraction inside r<2a. CSV + JSON."""
    from kernels import Loops, generic_seed
    dims = TIP_BOXES[box]; lat = Lattice(*dims, alpha=alpha); lp = Loops(lat, IT1_EPS)
    rho = TIP_RHO_OVER_MR*dims[0]; tf = flow_tf(rho); n = steps or int(round(TIP_FLOW_OVER_TF*tf/FLOW_STEP))
    c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2]); tipA, ringA = lat.dual_area()
    nodeA = np.r_[tipA, np.repeat(ringA, lat.Lc)]; vol = np.repeat(nodeA, lat.M3*lat.M4)*lat.a**2
    node_of = np.arange(lp.Ns)//(lat.M3*lat.M4); tip = node_of == 0; inner = lp.site_r < 2.0*lat.a
    U = generic_seed(lat, rho, seed=IT1_BASE_SEED, centre=c); t = 0.0; T = []; mono = True; S_prev = None; err = None; t0 = time.perf_counter()
    def log():
        S, dens = lp.action(U, per_site=True); dv = dens/vol; Q = lp.charge(U, lp.field_strength(U))
        T.append(dict(t=t, t_over_tf=t/tf, S=float(S), Q=float(Q), peak_tip=float(dv[tip].max()), peak_all=float(dv.max()),
                      peak_all_r=float(lp.site_r[int(np.argmax(dv))]), frac_r_lt_2a=float(dens[inner].sum()/S) if S > 0 else None, finite=bool(np.isfinite(dv).all())))
        return S
    try:
        S_prev = log(); done = 0
        while done < n:
            k = min(rec, n - done); U, _ = lp.flow(U, h=FLOW_STEP, max_steps=k, record=k + 1); done += k; t = done*FLOW_STEP
            S = log()
            if S > S_prev*(1 + 1e-12): mono = False
            if not np.isfinite(S): err = "non-finite action"; break
            S_prev = S
    except FloatingPointError as e: err = str(e); mono = False
    d = os.path.join(diag22_paths()["tip"]); os.makedirs(d, exist_ok=True); stem = os.path.join(d, f"{box}_a{alpha}")
    with open(stem + ".csv", "w") as f:
        f.write("t,t_over_tf,S,Q,peak_tip,peak_all,peak_all_r,frac_r_lt_2a,finite\n")
        for r in T: f.write(",".join(str(r[k]) for k in ("t", "t_over_tf", "S", "Q", "peak_tip", "peak_all", "peak_all_r", "frac_r_lt_2a", "finite")) + "\n")
    out = dict(test="tip probe (diag22)", box=box, N=dims[0], alpha=alpha, rho=rho, t_f=tf, t_end=t, steps=n, monotone_S=mono, error=err,
               cells_across_rho=rho/lat.a, final=(T[-1] if T else None), max_peak_tip=max((r["peak_tip"] for r in T), default=None),
               n_records=len(T), smoke=steps is not None, wall_s=time.perf_counter()-t0, spec=FINAL_SPEC_HASH,
               density_note="action per site / dual 4-volume (tip disc r<a/4 x a^2); tip cell = r=0 sites")
    open(stem + ".json", "w").write(json.dumps(out, default=float)); print(json.dumps(out, default=float), flush=True); return out
def tip_fit(Ns, peaks):
    """log peak = p log N + c, weighted least squares; p error from fit covariance (residual-scaled), dof = n-2."""
    x = np.log(np.asarray(Ns, float)); y = np.log(np.asarray(peaks, float)); n = len(x)
    if n < 3: return dict(p=None, p_err=None, dof=n-2, note="need >= 3 boxes for an error bar")
    coef, cov = np.polyfit(x, y, 1, cov=True)
    return dict(p=float(coef[0]), p_err=float(np.sqrt(cov[0, 0])), dof=n-2, intercept=float(coef[1]))
def diag22_tip_fit():
    P = diag22_paths(); out = dict(test="tip probe fit peak ~ N^p (diag22)", thresholds=TIP_THRESHOLDS, per_alpha={}, rows=[])
    for al in TIP_ALPHAS:
        R = []
        for b in TIP_BOXES:
            fn = os.path.join(P["tip"], f"{b}_a{al}.json")
            if os.path.exists(fn): r = json.load(open(fn)); R.append(r); out["rows"].append({k: r.get(k) for k in ("box", "N", "alpha", "error", "monotone_S", "max_peak_tip", "final")})
        ok = [r for r in R if r.get("final") and not r.get("error")]
        f_end = tip_fit([r["N"] for r in ok], [r["final"]["peak_tip"] for r in ok]) if ok else None
        f_max = tip_fit([r["N"] for r in ok], [r["max_peak_tip"] for r in ok]) if ok else None
        out["per_alpha"][str(al)] = dict(n_boxes=len(ok), fit_final_peak=f_end, fit_max_peak=f_max,
                                         verdict=("REPORT-ONLY: frozen tip thresholds missing" if TIP_THRESHOLDS is None else None))
    os.makedirs(P["tip"], exist_ok=True); txt = json.dumps(out, indent=1, default=float)
    open(os.path.join(P["tip"], "tip_fit.json"), "w").write(txt); print(txt); return out
# ---- IT1b power-law hooks (2026-10-23, [hive proposal, untested]); new modes only, old paths untouched ----
IT1B_OUT = "diag22b"; IT1B_T_LO = 0.1; IT1B_T_CAP = 0.6; IT1B_REC = 5    # record every 5 steps = 0.01 in t
IT1B_DELTAS = (0.003, 0.006); IT1B_SEEDS = (0, 1); IT1B_ALPHAS = (1.0, 0.5)   # rev 6: antithetic +/-d per seed
IT1B_SIGNED_DELTAS = tuple(sg*d for d in IT1B_DELTAS for sg in (1, -1))
IT1B_MEASURE = "out/diag22b/IT1B_REV6_FROZEN.md E360229B"   # rev 6 (Venus + Helios), replaces C99963A0
IT1B_FLOW_EPS = -1   # rev 6 (b): over-improved flow S(eps=-1), Garcia Perez et al. NPB413 (1994); calibration and every row
IT1B_SPEC = "E360229B"   # sha256[:8] of out/diag22b/IT1B_REV6_FROZEN.md, checked by it1b_spec_ok()
def it1b_spec_ok():
    import hashlib; p = os.path.join(HERE, "out", "diag22b", "IT1B_REV6_FROZEN.md")
    return os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest()[:8].upper() == IT1B_SPEC
IT1B_ROWS_DIR = "rows_rev6"   # fresh dir: the old eps=0 short-check row stays in rows/
IT1B_LABEL = "linear response at t=0.6, reduced model"
def it1b_paths():
    base = os.path.join(HERE, "out", IT1B_OUT); return dict(base=base, rows=os.path.join(base, "rows"), cal=os.path.join(base, "cal_B10_eps-1.json"),
                                                           grade=os.path.join(base, "it1b_grade_rev6.json"), rows6=os.path.join(base, IT1B_ROWS_DIR))
def it1b_row_path(alpha, seed, delta):
    """Rev 6: deterministic X0 is ONE file per alpha (seed label -1); signed delta in the name, e.g. B10_a1.0_s0_delta-0.003.json."""
    if float(delta) == 0.0: seed = IT1_D0_DRAW
    return os.path.join(it1b_paths()["rows6"], f"B10_a{float(alpha)}_s{int(seed)}_delta{float(delta)}.json")
def it1b_hist_window(hist, lo=IT1B_T_LO, hi=IT1B_T_CAP):
    """X(t) from flow start, restricted to [lo, hi]; drops non-finite."""
    return [(float(t), float(x)) for t, x in hist if lo-1e-12 <= t <= hi+1e-12 and x is not None and np.isfinite(x)]
def it1b_tip_log(S, dens, vol, tip, inner):
    """Report-only: peak tip density (per dual 4-volume), r<2a action fraction, finiteness."""
    dv = np.asarray(dens, float)/np.asarray(vol, float)
    return dict(peak_tip=float(dv[tip].max()) if np.any(tip) else None, peak_all=float(dv.max()),
                frac_r_lt_2a=(float(np.asarray(dens)[inner].sum()/S) if S > 0 else None), finite=bool(np.isfinite(dv).all()))
def it1b_r0_bc(lat, lp):
    """Report-only description of the r=0 boundary condition actually used."""
    node_of = np.arange(lp.Ns)//(lat.M3*lat.M4); tip = node_of == 0
    return dict(kind="cone tip node 0 (r=0 sites), alpha-measure only", alpha=float(lat.alpha) if hasattr(lat, "alpha") else None,
                n_tip_sites=int(tip.sum()), tip_sites_boundary=int(np.sum(lp.bsite[tip])) if hasattr(lp, "bsite") else None,
                tip_r_max=float(np.max(lp.site_r[tip])))
def it1b_row(alpha, seed, delta, steps=None):
    """Flow from t=0 to IT1B_T_CAP, recording X(t)=cal*rho_moment every IT1B_REC steps (incl. t<T). seed=-1 & delta=0 => control."""
    from kernels import Loops, generic_seed
    box = DIAG22_BOX; rho = IT1_GRIDS[box]; lat = Lattice(*BOXES[box], alpha=alpha); lp = Loops(lat, IT1B_FLOW_EPS)
    c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2]); t0 = time.perf_counter()
    lat1 = Lattice(*BOXES[box], alpha=1.0); lp1 = Loops(lat1, IT1B_FLOW_EPS)
    cal = rho/lp1.rho_moment(lp1.flat(lat1.bpst_links(rho, centre=c)), centre=c); del lat1, lp1
    tipA, ringA = lat.dual_area(); nodeA = np.r_[tipA, np.repeat(ringA, lat.Lc)]; vol = np.repeat(nodeA, lat.M3*lat.M4)*lat.a**2
    node_of = np.arange(lp.Ns)//(lat.M3*lat.M4); tip = node_of == 0; inner = lp.site_r < 2.0*lat.a
    U = generic_seed(lat, rho, seed=IT1_BASE_SEED, centre=c)
    if delta: U = it1_perturb(lp, U, seed, delta)
    n = steps or int(round(IT1B_T_CAP/FLOW_STEP)); done = 0; hist = []; logs = []; err = None
    def snap(t):
        S, dens = lp.action(U, per_site=True); hist.append((t, cal*lp.rho_moment(U, centre=c)))
        logs.append(dict(t=t, **it1b_tip_log(S, dens, vol, tip, inner)))
    try:
        snap(0.0)
        while done < n:
            k = min(IT1B_REC, n-done); U, _ = lp.flow(U, h=FLOW_STEP, max_steps=k, record=k+1); done += k; snap(done*FLOW_STEP)
    except FloatingPointError as e: err = str(e)
    Q = lp.charge(U, lp.field_strength(U))
    if float(delta) == 0.0: seed = IT1_D0_DRAW
    out = dict(test="IT1b", box=box, alpha=alpha, seed=seed, delta=delta, flow_eps=IT1B_FLOW_EPS, rng=(IT1_RNG_BASE+seed if delta else None), ell=float(lat.r[-1]), rho_seed=rho, rho_cal=cal, hist_full=hist,
               hist=it1b_hist_window(hist), window=[IT1B_T_LO, IT1B_T_CAP], Q=Q, absQ_minus_1=abs(abs(Q)-1), err=err,
               r0_bc=it1b_r0_bc(lat, lp), tip_log=logs, log_note="report-only (r=0 BC, peak tip density, r<2a fraction)",
               steps=n, smoke=steps is not None, wall_s=time.perf_counter()-t0, free_ram_gb=free_ram_gb(), spec=IT1B_SPEC, master_spec=FINAL_SPEC_HASH,
               measure=IT1B_MEASURE, tag="[hive proposal, untested]", model="reduced model")
    fn = it1b_row_path(alpha, seed, delta); os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, "w", encoding="utf-8").write(json.dumps(out, default=float)); print(json.dumps(dict(path=fn, err=err), default=float), flush=True); return out
def it1b_cal(steps=None, centre_r=0.0):
    """Same as diag22_cal at T=IT1B_T_CAP but flowed with S(IT1B_FLOW_EPS) (rev 6); signed shift recorded; |shift| <= 5% (no retune)."""
    from kernels import Loops
    box = DIAG22_BOX; rho = IT1_GRIDS[box]; n = steps or int(round(IT1B_T_CAP/FLOW_STEP))
    lat = Lattice(*BOXES[box], alpha=1.0); lp = Loops(lat, IT1B_FLOW_EPS); c = (float(centre_r), 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2])   # centre_r=0: tip (default, unchanged)
    U = lp.flat(lat.bpst_links(rho, centre=c)); r0 = lp.rho_moment(U, centre=c)
    U, _ = lp.flow(U, h=FLOW_STEP, max_steps=n, record=5); r1 = lp.rho_moment(U, centre=c)
    out = dict(test="IT1b-cal", model="reduced model", box=box, rho=rho, T=n*FLOW_STEP, raw_unflowed=r0, raw_flowed=r1, cal=rho/r0, rel_shift=abs(r1-r0)/r0, rel_shift_signed=(r1-r0)/r0,
               rho_flowed_cal=rho*r1/r0, direction=("grows" if r1 > r0 else "shrinks"), flow_eps=IT1B_FLOW_EPS, limit=0.05, ok=bool(abs(r1-r0)/r0 <= 0.05), steps=n,
               centre=list(map(float, c)), centre_r=float(centre_r), smoke=steps is not None, spec=IT1B_SPEC, master_spec=FINAL_SPEC_HASH, measure=IT1B_MEASURE)
    P = it1b_paths(); os.makedirs(P["base"], exist_ok=True); P["cal"] = P["cal"] if not centre_r else os.path.join(P["base"], f"cal_B10_eps-1_offtip_r{centre_r:g}.json"); open(P["cal"], "w").write(json.dumps(out, default=float)); print(json.dumps(out, default=float)); return out
IT1B_P3 = "dX"   # spec rev2 FD9FD866, unchanged in C99963A0: paired shift at alpha=0.5 via UNCHANGED diag22_grade_rows; only "dX" accepted
IT1B_P3_MAX = 0.23; IT1B_X0_REF = 2.9027; IT1B_X0_TOL = 0.02   # short check: diag22 alpha=1 delta=0 X at t=0.6
def it1b_short_check(row, ref=IT1B_X0_REF, tol=IT1B_X0_TOL):
    """Single point t=0.6 (only overlap with stored diag22 rows) [flagged for Venus]."""
    x = [x for t, x in row["hist_full"] if abs(t-0.6) < 1e-9]
    if not x: return dict(ok=False, note="no t=0.6 point")
    rel = abs(x[-1]-ref)/ref; return dict(X_06=x[-1], ref=ref, rel=rel, tol=tol, ok=bool(rel <= tol))
def it1b_p3_control(rowlist, cal_shift):
    """P3: feed the +d IT1b rows (drift = it1_fit_drift on the [0.1,0.6] hist) and the X0 row into the UNCHANGED diag22_grade_rows; take delta0_control.
    [deviation, flagged for Venus] rev 6 has no 0.0015 rows, so the diag22 per-delta loop runs over the +d values (0.003, 0.006); the statistic,
    E, 3E bound and the < 0.23 cut on max|diff| are unchanged. -d rows are not fed (the diag22 statistic is defined on +d only)."""
    global DIAG22_DELTAS
    if IT1B_P3 != "dX": raise RuntimeError(f"IT1B_P3={IT1B_P3!r}: only 'dX' is frozen (unchanged from FD9FD866); refusing to grade")
    conv = []
    for r in rowlist:
        d0 = float(r["delta"]) == 0.0
        if d0 and int(r["seed"]) != IT1_D0_DRAW: continue
        if not d0 and float(r["delta"]) < 0: continue
        conv.append(dict(alpha=float(r["alpha"]), draw=(IT1_D0_DRAW if d0 else int(r["seed"])), delta=(0.0 if d0 else float(r["delta"])),
                         drift=it1_fit_drift(r["hist"], float(r["ell"]))[0]))
    old = DIAG22_DELTAS; DIAG22_DELTAS = tuple(IT1B_DELTAS)
    try: ctl = diag22_grade_rows(conv, dict(rel_shift=cal_shift))["criteria"]["delta0_control"]
    finally: DIAG22_DELTAS = old
    diffs = [abs(v["diff"]) for v in ctl["per_delta"].values() if "diff" in v]
    val = max(diffs) if len(diffs) == len(IT1B_DELTAS) else float("inf")
    return dict(value=val, limit=IT1B_P3_MAX, ok=bool(val < IT1B_P3_MAX), diag22_control=ctl, deltas_used=list(IT1B_DELTAS))
def it1b_grade_from(rowlist, cal_shift):
    """Pure: rowlist -> rev 6 antithetic grade via it1b_measure (E360229B). X0 is one deterministic row per alpha (seed -1), shared by every seed.
    Missing rows listed as NOT COMPUTED (YET). P3 = unchanged diag22 paired shift at alpha=0.5."""
    import it1b_measure as M
    idx = {}; missing = []
    for r in rowlist:
        k = (float(r["alpha"]), int(r["seed"]) if float(r["delta"]) != 0.0 else IT1_D0_DRAW, float(r["delta"]))
        if k in idx: raise ValueError(f"duplicate IT1b row {k}")
        idx[k] = r
    h0 = {}; rows = {}
    for al in IT1B_ALPHAS:
        r0 = idx.get((al, IT1_D0_DRAW, 0.0))
        if r0 is None: missing.append((al, IT1_D0_DRAW, 0.0))
        else: h0[al] = r0["hist"]
        rows[al] = {sd: {} for sd in IT1B_SIGNED_DELTAS}
        for s in IT1B_SEEDS:
            for sd in IT1B_SIGNED_DELTAS:
                r = idx.get((al, s, sd))
                if r is None: missing.append((al, s, sd))
                else: rows[al][sd][s] = r["hist"]
    if missing:
        return dict(status="NOT COMPUTED (YET)", missing=missing)
    P3 = it1b_p3_control(rowlist, cal_shift)
    g = M.grade_rev6(h0, rows, cal_shift, P3["value"])
    return dict(status="graded", P3=P3, control_note="P3 = max|Delta_delta-Delta_0| at alpha=0.5 via unchanged diag22_grade_rows on +d rows, < 0.23",
                cal_shift=cal_shift, per_alpha={str(k): v for k, v in g.items()}, tag="[hive proposal, untested]", model="reduced model",
                label=IT1B_LABEL, measure=IT1B_MEASURE, flow_eps=IT1B_FLOW_EPS,
                verdict_rule="L_s=(X(+d)-X(-d))/(2d) at t=0.6; noise |mean L|>spread else UNDECIDED; P1 L_s(2d)/L_s(d) in [0.85,1.15] every seed; P2 cal<=5%; P3<0.23; E_s report-only")
IT1B_X0_QTOL = IT1_Q_TOL
def it1b_x0_check(row):
    """Rev 6 condition 3 X0 re-read under eps=-1. No numeric X0 target is frozen in E360229B [flagged]; the check is: flow completed (no guard error),
    X(t=0.6) present and finite, ||Q|-1| <= 0.05 (IT1_Q_TOL). The eps=0 value 2.9027 is reported for comparison only, not gated."""
    x = [x for t, x in row["hist_full"] if abs(t-0.6) < 1e-9]
    X = x[-1] if x else None; fin = X is not None and bool(np.isfinite(X))
    ok = row.get("err") is None and fin and row["absQ_minus_1"] <= IT1B_X0_QTOL
    return dict(alpha=row["alpha"], X_06=X, err=row.get("err"), Q=row["Q"], absQ_minus_1=row["absQ_minus_1"], qtol=IT1B_X0_QTOL,
                eps0_ref=IT1B_X0_REF, rel_vs_eps0=(abs(X-IT1B_X0_REF)/IT1B_X0_REF if fin else None), wall_s=row.get("wall_s"), ok=bool(ok), flow_eps=row.get("flow_eps"))
IT1B_BPST_BOX = "B10"; IT1B_BPST_RHO = 3.0; IT1B_BPST_H = (1.0, 2/3, 0.5)   # pre-step: physical box = BOXES[box] at a=1, spacing h
IT1B_BPST_TOL = 0.01; IT1B_BPST_R_FULL = 12.5; IT1B_BPST_EPS = 1               # Wilson; 1% after h->0 fit (C99963A0 rev 4)
def bpst_tail(R, rho):
    """Fraction of 8pi^2 outside 4-radius R: rho^4(3R^2+rho^2)/(R^2+rho^2)^3 (Venus, C99963A0)."""
    return rho**4*(3*R**2+rho**2)/(R**2+rho**2)**3
def box_half_width(name):
    """Physical half-width of BOXES[name] at a=1: min(l=(M_r-1/2)a, M3 a/2, M4 a/2) (inscribed 4-ball radius)."""
    Mr, _, M3, M4 = BOXES[name]; return float(min(ELL_OF(Mr), M3/2, M4/2))
def bpst_target(name, rho=IT1B_BPST_RHO):
    R = box_half_width(name)
    if R >= IT1B_BPST_R_FULL: return dict(R=R, target=1.0, kind="1 (R >= 12.5)", tail=bpst_tail(R, rho))
    t = bpst_tail(R, rho); return dict(R=R, target=1.0-t, tail=t, kind=f"1 - tail(R={R}) [box R < 12.5, tail-corrected target]")
def bpst_dims(name, h):
    """Integer lattice dims for BOXES[name] at spacing h (L_phi fixed); None if not integer."""
    Mr, Lp, M3, M4 = BOXES[name]; d = [Mr/h, M3/h, M4/h]
    if any(abs(x-round(x)) > 1e-9 for x in d): return None
    return (int(round(d[0])), Lp, int(round(d[1])), int(round(d[2])))
def bpst_plan(hs=IT1B_BPST_H):
    """Pure: every box in BOXES, half-width, target, spacings with integer dims and site counts (alpha=1)."""
    out = {}
    for b in BOXES:
        sp = {}
        for h in hs:
            dm = bpst_dims(b, h)
            sp[f"{h:.4g}"] = None if dm is None else dict(dims=dm, sites=(1+dm[0]*dm[1])*dm[2]*dm[3], rho_over_a=IT1B_BPST_RHO/h)
        out[b] = dict(half_width=box_half_width(b), **bpst_target(b), spacings=sp)
    return out
def bpst_fit(hs, S):
    """S(h) = S0 + c h^2 (Wilson O(a^2)); >=2 spacings. Returns S0, c, residual (None for 2 points)."""
    hs, S = np.asarray(hs, float), np.asarray(S, float)
    if len(hs) < 2 or len(set(np.round(hs, 12))) < 2: raise ValueError("need >= 2 distinct lattice spacings")
    c, S0 = np.polyfit(hs**2, S, 1); res = S - (S0 + c*hs**2)
    return dict(S0=float(S0), c=float(c), max_resid=(float(np.abs(res).max()) if len(hs) > 2 else None))
def bpst_grade(name, hs, S, rho=IT1B_BPST_RHO):
    f = bpst_fit(hs, S); tg = bpst_target(name, rho); rel = abs(f["S0"]-tg["target"])/tg["target"]; lo = tg["target"]*(1-IT1B_BPST_TOL); hi = 1.0+IT1B_BPST_TOL   # band rule frozen in out/diag22b/BPST_PRESTEP_FROZEN.md
    return dict(test="IT1b BPST pre-step", box=name, rho=rho, alpha=1.0, spacings=list(map(float, hs)), S_over_8pi2=list(map(float, S)),
                fit=f, **tg, rel_err=rel, tol=IT1B_BPST_TOL, band=[lo, hi], rule="PASS iff 0.99*(1-tail(R)) <= S0 <= 1.01 (cube > ball: 1-tail is a lower bound)", ok=bool(lo <= f["S0"] <= hi),
                label=("literature benchmark BPST S=8pi^2|Q|" + ("" if tg["R"] >= IT1B_BPST_R_FULL else ", tail-corrected target 1 - tail(R)")),
                measure=IT1B_MEASURE, tag="[hive proposal, untested]")
def it1b_bpst(name=IT1B_BPST_BOX, hs=IT1B_BPST_H, rho=IT1B_BPST_RHO, eps=IT1B_BPST_EPS):
    """Exact BPST links (alpha=1, tip-site centre), action S(eps) (eps=1 Wilson; rev 6 re-check at eps=-1), no Dirichlet face, per spacing; h->0 fit.
    Same frozen band (FBF5C7DB) for every eps: the O(a^2) term -(eps/5)(a/rho)^2 (NPB413 eq. 19) is removed by the h^2 fit."""
    S = []; used = []; extra = []
    for h in hs:
        dm = bpst_dims(name, h)
        if dm is None: raise ValueError(f"{name} at h={h}: non-integer dims")
        f = free_ram_gb()
        if f is not None and f < IT4_MIN_FREE_GB: raise MemoryError(f"free RAM {f} GB < {IT4_MIN_FREE_GB} GB before h={h}")
        t0 = time.perf_counter(); lat = Lattice(*dm, alpha=1.0, a=h); lat.apply_dirichlet = lambda L: 0.0
        c = (0., 0., lat.x3[lat.M3//2], lat.x4[lat.M4//2]); L = lat.bpst_links(rho, centre=c)
        s = lat.action(L, eps)["S"]/(8*np.pi**2); S.append(s); used.append(h)
        extra.append(dict(h=h, dims=dm, S_over_8pi2=s, wall_s=time.perf_counter()-t0)); print(json.dumps(extra[-1], default=float), flush=True)
        del lat, L
    out = bpst_grade(name, used, S, rho); out["per_spacing"] = extra; out["eps"] = eps; out["eq19_a2_coeff_pred"] = -eps/5/rho**2
    if eps != 1: out["measure"] = IT1B_MEASURE
    P = it1b_paths(); os.makedirs(P["base"], exist_ok=True); fn = os.path.join(P["base"], "bpst_prestep.json" if eps == 1 else f"bpst_prestep_eps{eps:g}.json")
    open(fn, "w", encoding="utf-8").write(json.dumps(out, indent=1, default=float)); print(json.dumps(out, default=float), flush=True)
    return out
def it1b_grade():
    import glob
    P = it1b_paths(); rl = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(P["rows6"], "*.json")))]
    cal = json.load(open(P["cal"])) if os.path.exists(P["cal"]) else None
    out = it1b_grade_from(rl, cal["rel_shift"] if cal else float("nan")) if cal else dict(status="NOT COMPUTED (YET)", missing=["cal"])
    out["rows"] = [dict(alpha=r["alpha"], seed=r["seed"], delta=r["delta"], err=r.get("err"), n=len(r["hist"])) for r in rl]
    txt = json.dumps(out, indent=1, default=float); open(P["grade"], "w", encoding="utf-8").write(txt); print(txt); return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=["smoke", "graded", "resmoke", "resmoke-row", "holonomy", "gapcheck", "summarize", "inv_a", "inv_a_rho_tf", "boxcost-b16", "time-steps", "it1-row", "it1-grade", "it1-cal", "it1-pick-row", "it1-pick-grade", "it1-freeze", "it1-find-T", "it1-apply-T-ratio", "it1-diag21-grade", "smoke-cut", "it3-row", "it3-campaign", "it3-grade", "diag22-find-T", "diag22-cal", "diag22-row", "diag22-grade", "diag22-tip-row", "diag22-tip-fit", "it1b-row", "it1b-cal", "it1b-grade", "it1b-bpst", "it1b-bpst-plan", "it1b-x0"]); ap.add_argument("--alpha", type=float, default=1.0); ap.add_argument("--seed", type=int, default=0); ap.add_argument("--kind", default="generic"); ap.add_argument("--workers", type=int, default=3); ap.add_argument("--box", default="B10"); ap.add_argument("--eps", type=float, default=1); ap.add_argument("--rho", type=float, default=3.0); ap.add_argument("--centre", default="tip_site"); ap.add_argument("--launch-authorised", action="store_true"); ap.add_argument("--steps", type=int, default=None); ap.add_argument("--rep", type=int, default=0); ap.add_argument("--delta", type=float, default=None); ap.add_argument("--save-evecs", action="store_true"); ap.add_argument("--outdir", default=None, help="optional subdir under out/ (smoke/diag21 chain)"); ap.add_argument("--skip-existing", action="store_true"); ap.add_argument("--t-max-over", type=float, default=None); ap.add_argument("--flow-max-over", type=float, default=None); ap.add_argument("--apply-ratio-to", default=None); ap.add_argument("--delta-note", default=None); ap.add_argument("--centre-r", type=float, default=0.0, help="it1b-cal only: BPST centre at r (units of a) on theta=0; 0 = tip (default)")
    A = ap.parse_args(); h = spec_hash()
    if h != FINAL_SPEC_HASH: sys.exit(f"spec hash {h} != FINAL_SPEC_HASH {FINAL_SPEC_HASH}; stop")
    if A.mode == "graded":
        missing = [k for k, v in KERNELS.items() if not v]
        if HOLD_REV12: sys.exit("HOLD_REV12 set: graded rows refused")
        if not A.launch_authorised: sys.exit("graded rows need Akitti's launch; refused")
        if missing: sys.exit(f"graded rows refused: kernels {NCY}: {missing}")
        sys.exit("graded runner not wired")
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    if A.mode == "summarize": return summarize()
    if A.mode == "inv_a": return inv_a_check()
    if A.mode == "inv_a_rho_tf": return inv_a_check(rho_tf=True)
    if A.mode == "boxcost-b16": return boxcost_b16(A.steps)
    root = A.outdir
    if A.mode == "it1-row":
        return it1_row(A.box, A.alpha, A.seed, steps=A.steps, outdir=(f"{root}/it1" if root else "it1"), delta=A.delta,
                       save_evecs=A.save_evecs, t_path=(os.path.join(HERE, "out", root, "it1_T.json") if root else None),
                       skip_existing=A.skip_existing, delta_note=A.delta_note)
    if A.mode == "it1-cal": return it1_cal(A.box, A.steps, outdir=(f"{root}/it1" if root else "it1"), skip_existing=A.skip_existing)
    if A.mode == "it1-pick-row": return it1_pick_row(A.box, A.delta, A.seed, A.steps, outdir=(f"{root}/it1_pick" if root else "it1_pick"), skip_existing=A.skip_existing)
    if A.mode == "it1-pick-grade":
        return it1_pick_grade(indir=(f"{root}/it1_pick" if root else "it1_pick"), box=A.box,
                              grade_dir=(os.path.join(HERE, "out", root) if root else None))
    if A.mode == "it1-freeze":
        if root:
            base = os.path.join(HERE, "out", root)
            sys.exit(it1_freeze(grade_dir=base, outfile=os.path.join(base, "delta_frozen.json"), skip_existing=A.skip_existing))
        sys.exit(it1_freeze(skip_existing=A.skip_existing))
    if A.mode == "it1-find-T":
        return it1_find_T(A.box, A.steps, path=(os.path.join(HERE, "out", root, "it1_T.json") if root else None),
                          t_max_over=A.t_max_over, flow_max_over=A.flow_max_over, apply_ratio_to=A.apply_ratio_to,
                          skip_existing=A.skip_existing)
    if A.mode == "it1-apply-T-ratio":
        return it1_apply_T_ratio(A.box, A.apply_ratio_to or "B10,B12",
                                 path=(os.path.join(HERE, "out", root, "it1_T.json") if root else None))
    if A.mode == "it1-grade":
        if root: return it1_grade(indir=f"{root}/it1", outfile=os.path.join(HERE, "out", root, "it1_grade.json"))
        return it1_grade()
    if A.mode == "it1-diag21-grade":
        base = os.path.join(HERE, "out", root or "diag21")
        return it1_diag21_grade(indir=f"{root or 'diag21'}/it1", outfile=os.path.join(base, "it1_grade.json"),
                                t_path=os.path.join(base, "it1_T.json"))
    if A.mode == "diag22-find-T": return diag22_find_T(A.steps)
    if A.mode == "diag22-cal": return diag22_cal(A.steps)
    if A.mode == "diag22-row": return diag22_row(A.alpha, A.seed, (0.0 if A.seed == IT1_D0_DRAW else A.delta), A.steps, A.skip_existing)
    if A.mode == "diag22-grade": return diag22_grade()
    if A.mode == "it1b-row": return it1b_row(A.alpha, A.seed, (A.delta or 0.0), A.steps)
    if A.mode == "it1b-x0":
        r = it1b_row(A.alpha, IT1_D0_DRAW, 0.0, A.steps); c = it1b_x0_check(r); print("X0CHECK " + json.dumps(c, default=float), flush=True); sys.exit(0 if c["ok"] else 3)
    if A.mode.startswith("it1b-") and A.mode not in ("it1b-bpst-plan",) and not it1b_spec_ok(): print("IT1b spec hash mismatch: expected " + IT1B_SPEC); sys.exit(4)
    if A.mode == "it1b-cal": c = it1b_cal(A.steps, A.centre_r); sys.exit(0 if c["ok"] else 3)
    if A.mode == "it1b-grade": return it1b_grade()
    if A.mode == "it1b-bpst": r = it1b_bpst(A.box, eps=(int(A.eps) if float(A.eps).is_integer() else A.eps)); sys.exit(0 if r["ok"] else 3)
    if A.mode == "it1b-bpst-plan": print(json.dumps(bpst_plan(), indent=1, default=float)); return
    if A.mode == "diag22-tip-row": return diag22_tip_row(A.box, A.alpha, A.steps)
    if A.mode == "diag22-tip-fit": return diag22_tip_fit()
    if A.mode == "smoke-cut": return smoke_cut(A.steps or 1, A.kind if A.kind == "it1" else None)
    if A.mode == "time-steps": return time_steps(A.box, A.eps, A.alpha, A.rho, A.steps or 3)
    if A.mode == "it3-row": return it3_row(A.box, A.alpha, A.seed, A.kind)
    if A.mode == "it3-campaign":
        if not A.launch_authorised: sys.exit("IT3 campaign needs an agreed start time (rev 16/17); refused")
        return it3_campaign(A.workers)
    if A.mode == "it3-grade": return it3_grade()
    if A.mode == "resmoke": return resmoke_box(A.box)
    if A.mode == "resmoke-row":
        e = int(A.eps) if float(A.eps).is_integer() else A.eps; row = flowed_row(A.box, e, A.rho, A.centre); print(json.dumps(row, default=float))
        json.dump(row, open(os.path.join(HERE, "out", f"resmoke_{A.box}_{A.centre}_eps{e}_rho{A.rho}.json"), "w"), indent=1, default=float); return
    if A.mode == "holonomy": json.dump(holonomy_convergence(A.box), open(os.path.join(HERE, "out", "holonomy_convergence.json"), "w"), indent=1, default=float); return
    if A.mode == "gapcheck": json.dump(gap_check(A.box), open(os.path.join(HERE, "out", f"gapcheck_{A.box}.json"), "w"), indent=1, default=float); return
    smoke(os.path.join(HERE, "out", "smoke_scratch.json"))
if __name__ == "__main__": main()

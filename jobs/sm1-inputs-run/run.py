"""SM1-INPUTS-RUN (JOB_SM1_INPUTS_RUN_SPEC.md, SHA-256 prefix C9683FDD; second graded run, first run 235D00E5 on DB7ECF85 crashed; per-kappa-path error boundary on top of B11D43D5): tensioned vortices at a conical tip.

Writes RESULTS.md, profiles.csv, per_tip.csv, consistency_curve.csv, nc_scan.csv and SM1_INPUTS_FILLED.md in this
folder. Those files are generated here only and are never hand-edited. Every number in them is printed from a
variable. Thresholds, grids and predictions are fixed in the block below exactly as the spec states them, before
the graded run. Sources are read-only and hashed before and after; the run stops if a hash differs.
Part B (JOB_SM1B_SPEC.md 6611EE3B) is HELD and is not built; the MHD core job (A0756351) is not built.

Symbol map (hive agreement, spec line 23):
  code `u`      = spec chi(t), the Taubes function (B0's name; h = log|phi|^2 = lw + u). The spec writes it chi(t).
  `u_flow`      = the velocity (spec u). This run has no MHD solve, so u_flow is NOT COMPUTED (YET); never a bare u.
  kappa (KAPPA) = coupling lambda/e^2 = m_scalar^2/m_vector^2 (kappa = 1 is critical, B0's model).
  beta          = plasma beta only; not used in this run (the cone angle is written 2 pi alpha).
  P2_SHAPE      = spec eta, the P2 shape parameter (= 1/2).
  s_c           = proper (geodesic) core radius from the tip; r_c = f(theta_c)/alpha_i is the exterior cone
                  coordinate (circumference/2 pi alpha_i). s_c is never copied into r_c.
No chive_ns name (chi, any eta_*, lambda_in) is imported or used here (Venus N1-d, 76BC2EB1).
Run (PowerShell, TrinityOrb):
  $env:PYTHONIOENCODING='utf-8'; C:\\Users\\Akitt\\Grok\\.venv\\Scripts\\python.exe -B run.py
"""
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
sys.dont_write_bytecode = True

import ast
import csv
import datetime
import hashlib
import math
import platform
import re
import time
import zlib
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import cumulative_simpson, simpson, solve_bvp, solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

np.seterr(over="ignore", under="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
SMDIR = os.path.dirname(HERE)                 # ...\open-problems\01_sm_from_sphere
OP = os.path.dirname(SMDIR)                   # ...\open-problems
USER = os.path.dirname(OP)                    # C:\Users\Akitt
J = os.path.join
SMOKE = os.environ.get("SM1_SMOKE") == "1"    # scratch smoke test at NON-graded settings only (README disclosures)

# ======================= fixed before the graded run (spec C9683FDD, verbatim values; unchanged from DB7ECF85) =======================
SPEC_HASH = "C9683FDD"                                # revised spec (389 lines; Helios ruling + node cap); first run used DB7ECF85
INPUTS_HASH = "E0D7D41D"
ALPHA_GRID = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]          # spec 1 Grids
EPS_GRID = [1.0, 4.0, 24.0, 99.0]                     # spec 1: A = 4 pi n (1 + eps)
N_1T = [1, 2, 3, 4]                                   # spec 1 layouts
N_2T = [2, 4]
P2_SHAPE = 0.5                                        # spec eta (P2 shape)
P12_ALPHAS = (0.8, 0.5)                               # optional unequal row
KAPPA_GRID = [0.25, 0.5, 1.0, 2.0, 4.0]               # spec 3b
KAPPA_PATHS = ([1.0, 0.5, 0.25], [1.0, 2.0, 4.0])     # spec 3b continuation
DELTA = 1e-3                                          # s_c,delta rule (spec 2(e))
SC_GRID = [2.0, 4.0, 6.0, 8.0]                        # secondary s_c grid (INPUT PARAMETER)
EPS_BRADLOW_MAX = 4.0                                 # printed-reason split "Bradlow regime (eps <= 4)"
EPS_LARGE = 99.0                                      # G5 third item, NC6, NC7 second item
G1_ROWS = [(1, 1.0, 35, 58), (1, 4.0, 36, 59), (2, 1.0, 41, 64), (2, 4.0, 42, 65), (3, 1.0, 47, 70), (3, 4.0, 48, 71)]
G1_E_TOL, G1_PROF_TOL = 1e-9, 1e-6
G2_FLUX_TOL, G2_PHI_TOL, G2_GB_TOL = 1e-8, 1e-8, 1e-9
G3_BOG_TOL, G3_LOW_TOL, G3_RES_TOL = 1e-8, 1e-9, 1e-8
G4_MU_TOL, G4_MUI_TOL, G4_SC_TOL = 1e-9, 1e-8, 1e-3
G4_NQ_FAC, T_FAC = 2, 1.5
G5_TOL, G5_SPLIT_TOL, G5_TIP_TOL = 1e-8, 1e-10, 1e-3
G6_TOL, G7_TOL = 1e-8, 1e-8
NC1_MU_TOL, NC1_PROF_TOL = 1e-8, 1e-7
NC2_INT_TOL, NC2_PW_TOL = 1e-6, 1e-6                  # pointwise: max|H - H(-T_N) - int RHS| < 1e-6 mu/(2 pi)
NC3_TOL, NC4_MU_TOL, NC4_SC_TOL, NC5_TOL = 1e-10, 1e-8, 1e-3, 1e-7
NC6_MARGIN_FAC = 10.0
NC7_SPLIT_TOL, NC7_SAME_R_TOL = 1e-10, 1e-3
BG_FLOOR, BG_NUM_FAC = 1e-6, 100.0                    # mu depends on the background iff Delta_bg > max(1e-6, 100 e_num)
PROF_FLOOR, PROF_NUM_FAC = 1e-3, 10.0                 # profile depends iff s_c changes > max(1e-3 rel, 10 x NC4 change)
PLANE_RMAX0 = 40.0                                    # r_max = 40 / min(1, sqrt(kappa)) (spec I-11)
B0_REG_ERRATUM = 5e-12                                # Venus 76BC2EB1 N4-a: B0's energy rel. errors are <= 5e-12, not 1e-12
# ---- solver choices [assumed], fixed before the graded run (not thresholds) ----
EPS_LADDER_EXTRA = [10.0, 24.0, 50.0, 99.0]           # continuation beyond B0's CONT_EPS (B0 stops at eps = 4)
PLANE_RMIN = 1e-5                                     # flat-plane reference inner radius
NC5_H = (0.02, 0.01)                                  # L-BFGS grids in t; Richardson (4 E_{h/2} - E_h)/3
NC5_MAXITER = 60000
PROFILE_NTH = 200                                     # theta samples per row in profiles.csv (cell centres)
FD_TH = (0.3, 2001)                                   # G3 report-only FD residual: theta in [0.3, pi - 0.3], 2001 and 4001 points
MAX_SUBSTEP_DEPTH = 4                                 # continuation fallback: bisect a failed parameter step
# ---- second graded run (NanoRibbon go-ahead; Venus-approved code-only changes after crash 1, README_crash1.md) ----
MAX_NODES = 100_000                                   # mesh-node cap on BOTH solve_bvp calls (235D00E5 had 3_000_000 -> 29-42 GB workers)
N_WORKERS = 8                                         # worker processes (TrinityOrb: 15.4 GB RAM; 235D00E5 used 16)
# Spec C9683FDD section 3b "Affected rows (32 = 16 per kappa, at eps = 1 and kappa in {0.25, 0.5})", copied literally:
#   P0 1T n in {1,2,3,4}; P1 1T alpha = 1, n in {1,2,3,4}; C-GR 1T alpha = 1, n in {1,2,3,4}; C-GR 2T alpha = 1, n in {2,4}; P2 2T alpha = 1, n in {2,4}.
NORMAL_STATE_ROWS = tuple(
    [(kind, "1T", n, 1.0, 1.0, kap) for kap in (0.25, 0.5) for kind in ("P0", "P1", "CGR") for n in (1, 2, 3, 4)] +
    [(kind, "2T", n, 1.0, 1.0, kap) for kap in (0.25, 0.5) for kind in ("CGR", "P2") for n in (2, 4)])
NORMAL_STATE_TAG = ("[normal state: exact solution, linearly stable for B > \u03ba/2, marginal at B = \u03ba/2; whether a vortex branch coexists "
                    "(\u03ba < 1, subcritical) is NOT COMPUTED (YET)] [by construction; not a test] [Venus 20:44]")   # spec C9683FDD 3b, verbatim
NORMAL_STATE_ZERO_MODES = "marginal at B = kappa/2 (n + 1 zero modes)"   # spec 3b wording, printed with the (1, 0.5) rows
# ---- [prediction] (written before the run) ----
PRED = {
    "mu": "mu_matter = pi n at every alpha, on every background, for both layouts (Bogomolny) [prediction]",
    "bradlow": "no s_c,delta before the midpoint at eps = 1 and 4 (Bradlow regime) [prediction]",
    "greq": "G_req = (1 - alpha)/(4 pi n): a straight line in alpha with no preferred point [prediction]",
    "g5tip": "at eps = 99 each tip of a 2T row carries pi n/2 (relative 1e-3) [prediction]",
    "nc7": "C-GR eps = 99: mu(2T, n) = 2 mu(1T, n/2) on the same sphere (relative 1e-3) [prediction]",
    "cone": "P1 rows approach mu_cone = alpha E^plane_{nu = n/alpha}(kappa) (report-only) [prediction]",
    "w": "w = int T_zz / int T_tt = -1 [prediction/identity]",
}
if SMOKE:   # NON-graded settings for scratch smoke tests only (spec 5: 'for example eps = 0.3')
    ALPHA_GRID = [1.0, 0.95, 0.55]
    EPS_GRID = [0.3, 30.0]
    N_1T, N_2T = [1, 2], [2]
    P12_ALPHAS = (0.85, 0.55)
    KAPPA_GRID = [0.3, 0.6, 1.0, 1.7, 3.5]
    KAPPA_PATHS = ([1.0, 0.6, 0.3], [1.0, 1.7, 3.5])
    SC_GRID = [2.5, 5.0]
    EPS_LARGE = 30.0
    EPS_BRADLOW_MAX = 0.3
    EPS_LADDER_EXTRA = [10.0, 30.0]
    G1_ROWS = []
    # smoke: the same rule (smooth tipless rows with B = 1/(2(1 + eps)) >= kappa/2), so the fill path is exercised at smoke settings
    NORMAL_STATE_ROWS = tuple((kind, lay, n, e, 1.0, k) for e in EPS_GRID for k in KAPPA_GRID if 1 / (2 * (1 + e)) >= k / 2
                              for kind, lay, ns_ in (("P0", "1T", N_1T), ("P1", "1T", N_1T), ("CGR", "1T", N_1T), ("CGR", "2T", N_2T), ("P2", "2T", N_2T))
                              for n in ns_)


def sha8(path):
    with open(path, "rb") as fh:
        b = fh.read()
    return hashlib.sha256(b).hexdigest()[:8].upper(), "%08X" % (zlib.crc32(b) & 0xFFFFFFFF)


# ======================= read-only sources =======================
SPEC = J(SMDIR, "SM1_filter", "JOB_SM1_INPUTS_RUN_SPEC.md")
INPUTS = J(SMDIR, "SM1_filter", "SM1_INPUTS.md")
B0DIR = J(OP, "Bradlow_cap", "B0_taubes_base")
JFDIR = J(USER, "sm-rugby-yukawa")
SOURCES = [
    ("spec", SPEC, SPEC_HASH),
    ("inputs sheet", INPUTS, INPUTS_HASH),
    ("CONE_TIP_NOTE", J(OP, "CONE_TIP_NOTE.md"), "4EAAEAA9"),
    ("B0 run.py", J(B0DIR, "run.py"), "15F2B139"),
    ("B0 RESULTS.md", J(B0DIR, "RESULTS.md"), "AE4E8FFB"),
    ("B0 README.md", J(B0DIR, "README.md"), None),        # spec lists it without a hash
    ("Job Four run.py", J(JFDIR, "run.py"), "8FA69F08"),
    ("Job Four README.md", J(JFDIR, "README.md"), "D28E4934"),
    ("Job Four RESULTS.md", J(JFDIR, "RESULTS.md"), "BBABA152"),
]


def b0_namespace():
    """Execute ONLY B0's background helpers and constants (its module level runs the whole B0 job)."""
    path = J(B0DIR, "run.py")
    tree = ast.parse(open(path, encoding="utf-8").read())
    want_f = {"logsig2", "logcos2", "sech2", "solve_bg", "bg_fields", "integrals"}
    want_c = {"T_BVP", "N_BVP0", "BVP_TOL", "N_QUAD", "CONT_EPS"}
    keep = []
    for nd in tree.body:
        if isinstance(nd, ast.FunctionDef) and nd.name in want_f:
            keep.append(nd)
        elif isinstance(nd, ast.Assign):
            names = []
            for tg in nd.targets:
                if isinstance(tg, ast.Name):
                    names.append(tg.id)
                elif isinstance(tg, ast.Tuple):
                    names += [e.id for e in tg.elts if isinstance(e, ast.Name)]
            if any(nm in want_c for nm in names):
                keep.append(nd)
    ns = {"np": np, "math": math, "solve_bvp": solve_bvp, "simpson": simpson}
    exec(compile(ast.Module(body=keep, type_ignores=[]), path, "exec"), ns)
    return ns, sorted(nd.name if isinstance(nd, ast.FunctionDef) else "assign@%d" % nd.lineno for nd in keep)


def jobfour_alphas():
    path = J(JFDIR, "run.py")
    for nd in ast.parse(open(path, encoding="utf-8").read()).body:
        if isinstance(nd, ast.Assign) and any(isinstance(tg, ast.Name) and tg.id == "ALPHAS" for tg in nd.targets):
            return [float(v) for v in ast.literal_eval(nd.value)], nd.lineno
    return None, None


try:
    B0NS, B0_KEPT = b0_namespace()
except Exception:            # missing source: main() stops on the hash check
    B0NS, B0_KEPT = None, []
if B0NS is not None:
    logsig2, logcos2, sech2 = B0NS["logsig2"], B0NS["logcos2"], B0NS["sech2"]
    T_BASE, N_BVP0, BVP_TOL, N_QUAD = B0NS["T_BVP"], B0NS["N_BVP0"], B0NS["BVP_TOL"], B0NS["N_QUAD"]
    EPS_LADDER = sorted(set(B0NS["CONT_EPS"]) | set(EPS_LADDER_EXTRA) | set(EPS_GRID))
    if SMOKE:
        EPS_LADDER = [0.1, 0.2, 0.3, 0.5, 2.0, 10.0, 30.0]


# ======================= backgrounds (fixed, not back-reacted) [assumed] =======================
XS = sp.symbols("x", real=True)                       # x = ln tan(theta/2): sin theta = sech x, sin^2(theta/2) = sigma(2x)
_S2H = sp.exp(2 * XS) / (1 + sp.exp(2 * XS))
_C2H = 1 / (1 + sp.exp(2 * XS))
_SECH2 = 1 / sp.cosh(XS) ** 2


def g_expr(kind, aN, aS):
    """f(theta) = R sin(theta) g(theta); g written in x = ln tan(theta/2)."""
    aN, aS = sp.nsimplify(aN), sp.nsimplify(aS)
    if kind == "P0":
        return sp.Integer(1)
    if kind in ("P1", "P12"):          # R sin th [a_N cos^2(th/2) + a_S sin^2(th/2)]
        return aN * _C2H + aS * _S2H
    if kind == "P2":                   # R a sin th (1 + eta sin^2 th)
        return aN * (1 + sp.nsimplify(P2_SHAPE) * _SECH2)
    if kind == "CGR":                  # R a sin th  [GR control]
        return aN * sp.Integer(1)
    raise ValueError(kind)


def tip_alphas(kind, a):
    if kind == "P0":
        return 1.0, 1.0
    if kind == "P1":
        return a, 1.0
    if kind == "P12":
        return a
    return a, a


def radius(kind, n, eps, a):
    """R from the row's area formula with A = 4 pi n (1 + eps) [identity]."""
    A = 4 * math.pi * n * (1 + eps)
    if kind == "P0":
        return math.sqrt(A / (4 * math.pi))
    if kind == "P1":
        return math.sqrt(A / (2 * math.pi * (1 + a)))
    if kind == "P2":
        return math.sqrt(A / (2 * math.pi * a * (2 + 4 * P2_SHAPE / 3)))
    if kind == "CGR":
        return math.sqrt(A / (4 * math.pi * a))
    if kind == "P12":
        return math.sqrt(A / (2 * math.pi * (a[0] + a[1])))
    raise ValueError(kind)


def area_formula(kind, R, a):
    if kind == "P0":
        return 4 * math.pi * R ** 2
    if kind == "P1":
        return 2 * math.pi * R ** 2 * (1 + a)
    if kind == "P2":
        return 2 * math.pi * R ** 2 * a * (2 + 4 * P2_SHAPE / 3)
    if kind == "CGR":
        return 4 * math.pi * R ** 2 * a
    return 2 * math.pi * R ** 2 * (a[0] + a[1])


class Geo:
    """Fixed background ds^2 = R^2 dtheta^2 + f^2 dphi^2 in t(theta) = int_{pi/2}^theta R dtheta'/f (ds^2 = f^2 (dt^2 + dphi^2)).
    dx/dt = g(x) with x = ln tan(theta/2): integrated by DOP853 (the quadrature for t(theta)), stored as a spline."""

    def __init__(self, kind, aN, aS, R, tmaxN, tmaxS):
        self.kind, self.aN, self.aS, self.R = kind, aN, aS, R
        g = g_expr(kind, aN, aS)
        gx = sp.diff(g, XS)
        self._g = sp.lambdify(XS, g, "numpy")
        self._gx = sp.lambdify(XS, gx, "numpy")
        self._gxx = sp.lambdify(XS, sp.diff(gx, XS), "numpy")
        hstep = 2e-3
        segs = {}
        for sgn, tm in ((-1, tmaxN), (1, tmaxS)):
            te = np.arange(0.0, tm + 20 * hstep, hstep) * sgn
            sol = solve_ivp(lambda tt, xx: self.g(xx), (0.0, te[-1]), [0.0], method="DOP853", rtol=1e-13, atol=1e-14, t_eval=te)
            segs[sgn] = (te, sol.y[0])
        tg = np.r_[segs[-1][0][::-1], segs[1][0][1:]]
        xg = np.r_[segs[-1][1][::-1], segs[1][1][1:]]
        self.tgrid, self.xgrid = tg, xg
        self._x = CubicSpline(tg, xg, bc_type=((1, float(self.g(xg[:1])[0])), (1, float(self.g(xg[-1:])[0]))))
        self._t = CubicSpline(xg, tg)

    def _b(self, fn, x):
        return np.broadcast_to(np.asarray(fn(x), dtype=float), np.shape(x)).astype(float)

    def g(self, x):
        return self._b(self._g, x)

    def x(self, t):
        return self._x(t)

    def t_of_theta(self, th):
        return self._t(np.log(np.tan(th / 2)))

    def lnf(self, t):
        x = self.x(t)
        return math.log(self.R) + math.log(2.0) - np.logaddexp(x, -x) + np.log(self.g(x))

    def f2(self, t):
        return np.exp(2 * self.lnf(t))

    def f_theta(self, th):
        return self.R * np.sin(th) * self.g(np.log(np.tan(th / 2)))

    def dlnf(self, t):
        """(ln f)' = d ln f/dt = (1/2 pi) * (geodesic-curvature integral of the circle through t) [NC2 weight]."""
        x = self.x(t)
        return -self.g(x) * np.tanh(x) + self._b(self._gx, x)

    def Kf2(self, t):
        """K f^2, with K = -f_thth/(R^2 f) = -(1/f^2) d_t^2 ln f (conformal form) [identity]."""
        x = self.x(t)
        g, gx, gxx = self.g(x), self._b(self._gx, x), self._b(self._gxx, x)
        return g * (g * sech2(x) + gx * np.tanh(x) - gxx)

    def dN(self, t):
        return 2 * self.R * np.arctan(np.exp(self.x(t)))

    def dS(self, t):
        return 2 * self.R * np.arctan(np.exp(-self.x(t)))


def T_ends(R, aN, aS, fac=1.0):
    """T_i = (14 + ln R)/alpha_i (spec 1; 14 = B0's T_BVP)."""
    return fac * (T_BASE + math.log(R)) / aN, fac * (T_BASE + math.log(R)) / aS


def make_geo(kind, n, eps, a, R=None):
    aN, aS = tip_alphas(kind, a)
    if R is None:
        R = radius(kind, n, eps, a)
    TN, TS = T_ends(R, aN, aS)
    return Geo(kind, aN, aS, R, (T_FAC + 0.1) * TN, (T_FAC + 0.1) * TS), TN, TS


# ======================= critical stage: Taubes equation (B0 run.py:124-131 with Omega^2 -> f^2) =======================
MAXN = {"nodes": 0}     # largest node count of any converged solve_bvp in this process since the last reset (report-only; H3)


def note_nodes(s):
    if s.status == 0 and s.x.size > MAXN["nodes"]:
        MAXN["nodes"] = int(s.x.size)
    return s


def solve_taubes(G, nN, nS, TN, TS, guess, nodes=None):
    """u'' = n sech^2 t + f^2 (e^{lw + u} - 1), u'(-T_N) = u'(T_S) = 0; code u = spec chi(t)."""
    n = nN + nS
    nodes = N_BVP0 if nodes is None else nodes

    def lw(tt):
        return nN * logsig2(tt) + nS * logcos2(tt)

    def fun(tt, y):
        return np.vstack([y[1], n * sech2(tt) + G.f2(tt) * (np.exp(lw(tt) + y[0]) - 1.0)])

    def jac(tt, y):
        Jm = np.zeros((2, 2, tt.size))
        Jm[0, 1] = 1.0
        Jm[1, 0] = G.f2(tt) * np.exp(lw(tt) + y[0])
        return Jm

    bc = lambda ya, yb: np.array([ya[1], yb[1]])
    bcj = lambda ya, yb: (np.array([[0.0, 1.0], [0.0, 0.0]]), np.array([[0.0, 0.0], [0.0, 1.0]]))
    tt = np.linspace(-TN, TS, nodes)
    s = note_nodes(solve_bvp(fun, bc, tt, guess(tt), fun_jac=jac, bc_jac=bcj, tol=BVP_TOL, max_nodes=MAX_NODES))
    return s, lw


def clamp(s):
    lo, hi = s.x[0], s.x[-1]
    return lambda tt: s.sol(np.clip(tt, lo, hi))


def crit_eval(G, s, lw, nN, nS, tt):
    y = s.sol(tt)
    u, up = y[0], y[1]
    h = lw(tt) + u
    sig = np.exp(logsig2(tt))
    hp = 2 * nN * (1 - sig) - 2 * nS * sig + up
    f2 = G.f2(tt)
    ph2 = np.exp(h)
    dens = ph2 * hp ** 2 / 4 + f2 * (1 - ph2) ** 2 / 4       # eps_m f^2 (BPS-reduced; kappa = 1 only)
    B = 0.5 * (1 - ph2)
    F = np.exp(h / 2)
    Fp = hp * F / 2
    a = cumulative_simpson(f2 * B, x=tt, initial=0.0)
    return dict(u=u, h=h, hp=hp, f2=f2, ph2=ph2, dens=dens, B=B, F=F, Fp=Fp, a=a)


# ======================= stage NC: second-order equations on the fixed background =======================
def solve_nc(f2fun, nN, nS, kap, TL, TR, guess, nodes=None, plane=False):
    """y = [F, F', a, b], b = a'/f^2 = B. F'' = (nN - a)^2 F + (kap/2) f^2 F (F^2 - 1); (a'/f^2)' = -(nN - a) F^2."""
    n = nN + nS
    nodes = N_BVP0 if nodes is None else nodes

    def fun(tt, y):
        F, Fp, a, b = y
        f2 = f2fun(tt)
        return np.vstack([Fp, (nN - a) ** 2 * F + 0.5 * kap * f2 * F * (F ** 2 - 1), f2 * b, -(nN - a) * F ** 2])

    def jac(tt, y):
        F, Fp, a, b = y
        f2 = f2fun(tt)
        Jm = np.zeros((4, 4, tt.size))
        Jm[0, 1] = 1.0
        Jm[1, 0] = (nN - a) ** 2 + 0.5 * kap * f2 * (3 * F ** 2 - 1)
        Jm[1, 2] = -2 * (nN - a) * F
        Jm[2, 3] = f2
        Jm[3, 0] = -2 * (nN - a) * F
        Jm[3, 2] = F ** 2
        return Jm

    def bc(ya, yb):
        if plane:                                   # flat plane: F' = nu F, a = 0 at r_min; F = 1, a = nu at r_max
            return np.array([ya[1] - nN * ya[0], ya[2], yb[0] - 1.0, yb[2] - nN])
        right = (yb[1] + nS * yb[0]) if nS else yb[1]
        return np.array([ya[1] - nN * ya[0], ya[2], right, yb[2] - (n if nS else nN)])

    tt = np.linspace(TL, TR, nodes)
    return note_nodes(solve_bvp(fun, bc, tt, guess(tt), fun_jac=jac, tol=BVP_TOL, max_nodes=MAX_NODES))


def nc_eval(f2fun, dlnf, s, nN, kap, tt):
    F, Fp, a, b = s.sol(tt)
    f2 = f2fun(tt)
    eB = 0.5 * b ** 2
    eV = kap / 8 * (1 - F ** 2) ** 2
    dens = 0.5 * Fp ** 2 + 0.5 * (nN - a) ** 2 * F ** 2 + f2 * (eB + eV)       # full T_tt f^2
    H = 0.5 * Fp ** 2 + 0.5 * f2 * b ** 2 - 0.5 * (nN - a) ** 2 * F ** 2 - kap / 8 * f2 * (F ** 2 - 1) ** 2
    rhs = 2 * f2 * dlnf(tt) * (eB - eV)
    return dict(F=F, Fp=Fp, a=a, b=b, f2=f2, eB=eB, eV=eV, dens=dens, H=H, rhs=rhs, ph2=F ** 2, B=b)


def stress_and_tzz(F, Fp, a, b, f2, nN, kap):
    """Full formulas from the solved fields: T_zz = -[1/2|D phi|^2 + 1/2 B^2 + V]; orthonormal radial/azimuthal stress."""
    with np.errstate(divide="ignore", invalid="ignore"):
        Dr2 = Fp ** 2 / f2
        Dp2 = (nN - a) ** 2 * F ** 2 / f2
    V = kap / 8 * (1 - F ** 2) ** 2
    tzz_f2 = -(0.5 * Fp ** 2 + 0.5 * (nN - a) ** 2 * F ** 2 + f2 * (0.5 * b ** 2 + V))     # T_zz f^2
    ok = f2 > 1e-20
    Trr = 0.5 * Dr2 - 0.5 * Dp2 + 0.5 * b ** 2 - V
    Tpp = 0.5 * Dp2 - 0.5 * Dr2 + 0.5 * b ** 2 - V
    return tzz_f2, float(np.max(np.abs(Trr[ok]))), float(np.max(np.abs(Tpp[ok])))


def ansatz_J_Iz(F, f2, tt):
    """J = int T_{t phi} dA and I_z = int Im(phi* D_z phi) dA. For the static ansatz D_time phi = 0 (A_t = 0, no time
    dependence) and D_z phi = 0 (A_z = 0, z-independent), so both integrands are identically zero [identity]."""
    D_time_phi = np.zeros_like(F)
    D_z_phi = np.zeros_like(F)
    J_val = 2 * math.pi * simpson(D_time_phi * F * f2, x=tt)
    Iz_val = 2 * math.pi * simpson(F * D_z_phi * f2, x=tt)
    return float(J_val), float(Iz_val)


# ======================= per-tip helpers =======================
def core_radius(d, ph2, B, delta):
    """Smallest d (from the tip, up to the midpoint) beyond which 1 - |phi|^2 < delta and |B| < delta/2 everywhere.
    d is ascending from the tip to the midpoint. Returns (s_c or None, index-based crossing)."""
    g1 = (1 - ph2) - delta
    g2 = np.abs(B) - delta / 2
    bad = (g1 >= 0) | (g2 >= 0)
    if bad[-1]:
        return None
    idx = np.where(bad)[0]
    if idx.size == 0:
        return float(d[0])
    i = idx[-1]
    cross = []
    for gk in (g1, g2):
        if gk[i] >= 0:
            cross.append(d[i] + (d[i + 1] - d[i]) * gk[i] / (gk[i] - gk[i + 1]))
    return float(max(cross))


def tip_data(G, tt, dens, ph2, B, f2, nN, nS, eps, mid_tol_grid=True, H=None):
    """Per-tip energies, core radius, derived r_c, secondary grid. tt is the full grid with t = 0 (midpoint) a node."""
    out = {}
    i0 = int(np.argmin(np.abs(tt)))
    cum = cumulative_simpson(dens, x=tt, initial=0.0)
    flux_cum = cumulative_simpson(f2 * B, x=tt, initial=0.0)
    total = cum[-1]
    for tip, ni, sl, sgn, alpha_i in (("N", nN, slice(0, i0 + 1), 1, G.aN), ("S", nS, slice(i0, None), -1, G.aS)):
        tseg = tt[sl]
        dseg = G.dN(tseg) if tip == "N" else G.dS(tseg)
        o = {"n_i": ni, "alpha_i": alpha_i}
        if tip == "N":
            o["mu_i"] = 2 * math.pi * simpson(dens[sl], x=tseg)
            mu_d = lambda tq: 2 * math.pi * np.interp(tq, tt, cum)
            phi_d = lambda tq: 2 * math.pi * np.interp(tq, tt, flux_cum)
            order = slice(None)
        else:
            o["mu_i"] = 2 * math.pi * simpson(dens[sl], x=tseg)
            mu_d = lambda tq: 2 * math.pi * (total - np.interp(tq, tt, cum))
            phi_d = lambda tq: 2 * math.pi * (flux_cum[-1] - np.interp(tq, tt, flux_cum))
            order = slice(None, None, -1)
        dd, pp, bb, ts = dseg[order], ph2[sl][order], B[sl][order], tseg[order]
        dmid = float(dd[-1])
        o["d_mid"] = dmid
        if ni > 0:
            sc = core_radius(dd, pp, bb, DELTA)
        else:
            sc = None
        o["s_c"] = sc
        if ni == 0:
            o["s_c_reason"] = "n/a: no vortex at this tip (n_%s = 0); s_c,delta is defined around a vortex tip" % tip
        elif sc is None:
            o["s_c_reason"] = ("no s_c,delta before midpoint: Bradlow regime (eps <= 4)" if eps <= EPS_BRADLOW_MAX
                               else "no s_c,delta before midpoint: tail longer than midpoint distance")
        else:
            o["s_c_reason"] = ""
        if sc is not None:
            tc = float(np.interp(sc, dd, ts))
            o["t_c"] = tc
            o["r_c"] = float(math.sqrt(G.f2(np.array([tc]))[0]) / alpha_i)
            o["mu_sc"] = float(mu_d(tc))
            o["phi_sc"] = float(phi_d(tc))
            o["B_sc"] = float(np.interp(tc, tt, B))
            if H is not None:
                o["piH_tc"] = float(math.pi * np.interp(tc, tt, H))
        grid = []
        for s in SC_GRID:
            if s < dmid:
                tq = float(np.interp(s, dd, ts))
                grid.append((s, float(mu_d(tq)), float(phi_d(tq)), tq))
            else:
                grid.append((s, None, None, None))
        o["grid"] = grid
        out[tip] = o
    return out


def gauss_bonnet(G, TN, TS, tipd):
    """G2(iii) total and G2(iv) per tip at the midpoint and at each secondary-grid circle below it."""
    t1 = np.linspace(-TN, TS, N_QUAD)
    tot = 2 * math.pi * simpson(G.Kf2(t1), x=t1) + 2 * math.pi * (2 - G.aN - G.aS) - 4 * math.pi
    errs = []
    for tip in ("N", "S"):
        circles = [0.0] + [g[3] for g in tipd[tip]["grid"] if g[3] is not None]
        for tc in circles:
            if tip == "N":
                tq = np.linspace(-TN, tc, (N_QUAD - 1) // 2 + 1)
                val = 2 * math.pi * simpson(G.Kf2(tq), x=tq) + 2 * math.pi * float(G.dlnf(np.array([tc]))[0]) - 2 * math.pi * G.aN
            else:
                tq = np.linspace(tc, TS, (N_QUAD - 1) // 2 + 1)
                val = 2 * math.pi * simpson(G.Kf2(tq), x=tq) - 2 * math.pi * float(G.dlnf(np.array([tc]))[0]) - 2 * math.pi * G.aS
            errs.append(abs(val))
    return abs(tot), max(errs)


def fd_residual(G, s, lw, npts):
    """Report-only: max|Delta_g h - (e^h - 1)|, Delta_g h = (1/(R^2 f)) d_th (f d_th h), theta in [0.3, pi - 0.3]."""
    th = np.linspace(FD_TH[0], math.pi - FD_TH[0], npts)
    dth = th[1] - th[0]
    hval = lambda thq: (lambda tq: lw(tq) + s.sol(tq)[0])(G.t_of_theta(thq))
    hh = hval(th)
    fp = G.f_theta(th + dth / 2)
    fm = G.f_theta(th - dth / 2)
    f0 = G.f_theta(th)
    lap = (fp[1:-1] * (hh[2:] - hh[1:-1]) - fm[1:-1] * (hh[1:-1] - hh[:-2])) / (G.R ** 2 * f0[1:-1] * dth ** 2)
    return float(np.max(np.abs(lap - (np.exp(hh[1:-1]) - 1))[5:-5]))


def profile_rows(G, s, lw, nN, nS):
    th = math.pi * (np.arange(PROFILE_NTH) + 0.5) / PROFILE_NTH
    tq = G.t_of_theta(th)
    y = s.sol(tq)
    h = lw(tq) + y[0]
    sig = np.exp(logsig2(tq))
    hp = 2 * nN * (1 - sig) - 2 * nS * sig + y[1]
    ph2 = np.exp(h)
    f2 = G.f2(tq)
    em = (ph2 * hp ** 2 / 4 + f2 * (1 - ph2) ** 2 / 4) / f2
    return th, G.R * th, ph2, 0.5 * (1 - ph2), em


# ======================= NC5: direct minimisation (L-BFGS) =======================
def min_energy(f2fun, nN, n_end, kap, TN, TS, h, F0fun, b0fun):
    """Staggered second-order discretisation of E = 2 pi int [F'^2/2 + (nN - a)^2 F^2/2 + f^2 b^2/2 + (kap/8) f^2 (F^2 - 1)^2] dt
    on [-T_N, T_S]: F at nodes, b = B at cell midpoints, a = int f^2 b with a(-T_N) = 0, flux a(T_S) = n_end imposed by a
    uniform shift of b; natural boundary conditions for F. Minimised by L-BFGS from (F0, b0)."""
    M = int(round((TN + TS) / h))
    t = np.linspace(-TN, TS, M + 1)
    hh = t[1] - t[0]
    tm = 0.5 * (t[1:] + t[:-1])
    c = f2fun(tm)
    f2n = f2fun(t)
    w = np.full(M + 1, hh)
    w[0] = w[-1] = hh / 2
    sc = np.sqrt(hh * c)
    sF = math.sqrt(hh)
    Csum = float(np.sum(hh * c))

    def fg(x):
        F = x[:M + 1] * sF
        bf = x[M + 1:] / sc
        lam = (n_end - np.sum(hh * c * bf)) / Csum
        b = bf + lam
        a = np.r_[0.0, np.cumsum(hh * c * b)]
        dF = np.diff(F) / hh
        E = np.sum(hh * (0.5 * dF ** 2 + 0.5 * c * b ** 2)) + np.sum(w * (0.5 * (nN - a) ** 2 * F ** 2 + kap / 8 * f2n * (F ** 2 - 1) ** 2))
        gF = np.zeros(M + 1)
        gF[:-1] -= dF
        gF[1:] += dF
        gF += w * ((nN - a) ** 2 * F + kap / 2 * f2n * F * (F ** 2 - 1))
        ga = -w * (nN - a) * F ** 2
        rc = np.cumsum(ga[::-1])[::-1]
        gb = hh * c * b + hh * c * rc[1:]
        gbf = gb - np.sum(gb) * (hh * c) / Csum
        return 2 * math.pi * E, 2 * math.pi * np.r_[gF * sF, gbf / sc]

    x0 = np.r_[F0fun(t) / sF, b0fun(tm) * sc]
    r = minimize(fg, x0, jac=True, method="L-BFGS-B",
                 options=dict(maxiter=NC5_MAXITER, maxfun=2 * NC5_MAXITER, ftol=1e-16, gtol=1e-14, maxcor=50))
    return float(r.fun), int(r.nit), str(r.message)


class CapHit(Exception):
    """A solve_bvp result that the chain uses is not converged (status != 0; status 1 = node cap MAX_NODES reached). Spec C9683FDD 3b."""


def solve_state(s):
    """Report-only description of a solve (Venus/Helios: record what a stalled or capped solution looks like)."""
    y = getattr(s, "y", None)
    p2 = ("max|phi|^2 = %.3e" % float(np.max(y[0] ** 2))) if (y is not None and y.shape[0] == 4) else "max|phi|^2 not formed (Taubes form)"
    return "status %d, %s, iterations %s, nodes %d" % (s.status, p2, getattr(s, "niter", "?"), s.x.size)


def capcheck(s, where):
    """Spec C9683FDD 3b: any non-converged solve (status != 0, or the cap reached) is 'not converged (cap hit)', FAILED, never retried."""
    if s.status != 0:
        why = "node cap MAX_NODES = %d reached" % MAX_NODES if s.status == 1 else "solve_bvp status %d: %s" % (s.status, s.message)
        raise CapHit("not converged (cap hit) at %s [%s; %s]" % (where, why, solve_state(s)))
    return s


def err_text(e):
    return str(e) if isinstance(e, CapHit) else "error: %s: %s" % (type(e).__name__, e)


def fail_entry(how, error, src=None):
    """A failed row (per-kappa-path boundary): how = 'directly' or 'upstream' (src = the row that failed directly). It carries no values
    (its slots stay NOT COMPUTED (YET)), counts as FAILED in the tally, and is never retried or re-started from another guess."""
    return dict(failed=how, error=error, src=src)


def fail_text(x):
    return ("failed directly: %s" % x["error"]) if x["failed"] == "directly" else ("failed upstream (row %s): %s" % (x["src"], x["error"]))


def isfail(x):
    return x is None or bool(x.get("failed"))


def check_normal_state_rows(jobs):
    """Assert: the filled set is exactly the spec's 32-row list (16 per kappa) and matches the chain list and the B >= kappa/2 rule."""
    rows = set(NORMAL_STATE_ROWS)
    assert len(rows) == len(NORMAL_STATE_ROWS) == 32, "normal-state list must have 32 distinct rows"
    for kap in (0.25, 0.5):
        assert sum(1 for r in rows if r[5] == kap) == 16, "16 rows per kappa"
    rule = set()
    for j in jobs:
        tipless = j["kind"] in ("P0", "P1", "P2", "CGR") and not j.get("R_n") and 1.0 in j["alphas"]
        for kap in KAPPA_GRID:
            if tipless and 1 / (2 * (1 + j["eps"])) >= kap / 2:
                rule.add((j["kind"], j["layout"], j["n"], j["eps"], 1.0, kap))
    assert rule == rows, "normal-state list != chain list under B >= kappa/2: extra %s missing %s" % (sorted(rows - rule), sorted(rule - rows))
    return len(rows)


# ---- normal-state fill (Helios ruling): isolated, OFF unless NORMAL_STATE_ROWS names the row ----
def normal_state_listed(kind, layout, n, eps, alpha, kap):
    """True only for a row named in NORMAL_STATE_ROWS (from the revised spec). Cone-tip rows are never filled analytically."""
    key = (kind, layout, n, eps, alpha, kap)
    if key not in NORMAL_STATE_ROWS:
        return False
    if isinstance(alpha, tuple) or alpha != 1.0:
        raise ValueError("cone-tip row listed for the analytic normal state (never allowed): %s" % (key,))
    return True


class NormalState:
    """Exact normal state phi = 0, uniform B = 2 pi n / A, a(t) = B int_{-T_N}^t f^2 dt; no BVP call. Mimics a solve_bvp result."""
    status = 0

    def __init__(self, G, TN, TS, n, area):
        self.B = 2 * math.pi * n / area
        tt = tgrid(TN, TS, N_QUAD)
        self._t = tt
        self._a = self.B * cumulative_simpson(G.f2(tt), x=tt, initial=0.0)
        self.x = np.zeros(0)
        self.rms_residuals = np.zeros(1)

    def sol(self, tq):
        tq = np.asarray(tq, dtype=float)
        z = np.zeros(tq.shape)
        return np.vstack([z, z, np.interp(tq, self._t, self._a), np.full(tq.shape, self.B)])


def tgrid(TN, TS, N):
    """N-point grid on [-T_N, T_S] with the midpoint t = 0 as a node (uniform on each side)."""
    nh = (N + 1) // 2
    return np.r_[np.linspace(-TN, 0.0, nh), np.linspace(0.0, TS, nh)[1:]]


def guess_const(n, nN, nS, eps):
    """B0's start guesses at the first ladder area (run.py:259 coincident; run.py:469 spread)."""
    if nS == 0:
        u0 = math.log((n + 1) * (1 - 1 / (1 + eps)))
    else:
        Bf = math.gamma(nN + 1) * math.gamma(nS + 1) / math.gamma(n + 2)
        u0 = math.log((1 - 1 / (1 + eps)) / Bf)
    return lambda tt: np.vstack([np.full(tt.size, u0), np.zeros(tt.size)])


def continue_param(solve_at, p0, p1, sol0, depth=0, log=None):
    """Solve at parameter p1 starting from sol0 (solved at p0); if it fails, bisect the step (pre-registered fallback)."""
    s = solve_at(p1, sol0)
    if s[0].status == 0:
        return s
    if depth >= MAX_SUBSTEP_DEPTH:
        return s
    pm = tuple(0.5 * (np.asarray(p0) + np.asarray(p1))) if isinstance(p0, tuple) else 0.5 * (p0 + p1)
    if log is not None:
        log.append("substep %s -> %s via %s (failed attempt: %s)" % (p0, p1, pm, solve_state(s[0])))
    sm = continue_param(solve_at, p0, pm, sol0, depth + 1, log)
    if sm[0].status != 0:
        return sm
    return continue_param(solve_at, pm, p1, sm[0], depth + 1, log)


def nc_guess_from_crit(C, tt):
    Y = np.vstack([C["F"], C["Fp"], C["a"], C["B"]])
    return lambda tq: np.vstack([np.interp(np.clip(tq, tt[0], tt[-1]), tt, Y[k]) for k in range(4)])


def nc_row(G, TN, TS, nN, nS, kap, s, eps, Ccrit=None, tt=None):
    """Evaluate one stage-NC solution s on the base grid tt."""
    D = nc_eval(G.f2, G.dlnf, s, nN, kap, tt)
    mu = 2 * math.pi * simpson(D["dens"], x=tt)
    S = 2 * math.pi * simpson(D["f2"] * (D["eB"] + D["eV"]), x=tt)
    W = 2 * math.pi * simpson(D["f2"] * G.dlnf(tt) * (D["eB"] - D["eV"]), x=tt)       # int (ln f)'(e_B - e_V) dA
    cumr = cumulative_simpson(D["rhs"], x=tt, initial=0.0)
    pw = float(np.max(np.abs(D["H"] - D["H"][0] - cumr)))
    flux = 2 * math.pi * simpson(D["f2"] * D["b"], x=tt)
    tzz_f2, trr, tpp = stress_and_tzz(D["F"], D["Fp"], D["a"], D["b"], D["f2"], nN, kap)
    tzz = 2 * math.pi * simpson(tzz_f2, x=tt)
    tips = tip_data(G, tt, D["dens"], D["ph2"], D["B"], D["f2"], nN, nS, eps, H=D["H"])
    r = dict(status=int(s.status), nodes=int(s.x.size), rms=float(np.max(s.rms_residuals)), mu=float(mu), S=float(S),
             W=float(W), pw=pw, flux=float(flux), tzz=float(tzz), w=float(tzz / mu), trr=trr, tpp=tpp, tips=tips,
             ph2max=float(np.max(D["ph2"])))
    if Ccrit is not None:
        r["prof_diff"] = float(np.max(np.abs(D["ph2"] - Ccrit["ph2"])))
    return r


def chain_name(job):
    return "%s %s n=%d eps=%g%s" % (job["kind"], job["layout"], job["n"], job["eps"], " (same R as n=%d)" % job["R_n"] if job.get("R_n") else "")


def run_chain(job):
    """Row failures are handled per kappa path inside _run_chain; an error outside any row (a bug) still fails the whole chain here:
    no rows (they stay NOT COMPUTED (YET)), other chains continue."""
    log = []
    t_start = time.time()
    MAXN["nodes"] = 0
    print("[chain start] %s at %s" % (chain_name(job), datetime.datetime.now().strftime("%H:%M:%S")), flush=True)
    try:
        out = _run_chain(job, log, t_start)
        out.update(error=None, max_nodes=MAXN["nodes"])
        for f in out["failed"]:
            print("[row FAILED] %s: %s" % (f["row"], fail_text(f)), flush=True)
        for r in out["results"]:
            for k, x in sorted(r["nc"].items()):
                if isfail(x):
                    print("[row FAILED] %s alpha=%s stage NC kappa=%g: %s" % (chain_name(job), lab_alpha(r["alpha"]), k, fail_text(x)), flush=True)
        return out
    except CapHit as e:
        err = str(e)
    except Exception as e:                       # the actual error, reported as such
        err = "error: %s: %s" % (type(e).__name__, e)
    print("[chain ERROR] %s: %s" % (chain_name(job), err), flush=True)
    return dict(job=job, results=[], log=log, seconds=time.time() - t_start, error=err, failed=[], max_nodes=MAXN["nodes"])


def _run_chain(job, log, t_start):
    """One (row, layout, n, eps) chain: eps ladder at alpha = 1, then alpha continuation; critical stage and stage NC.
    Error boundary (Venus, on top of B11D43D5): per row along each path, not per chain. The critical-stage alpha ladder is one path (each
    alpha starts from the previous alpha's critical solution). At each alpha, every kappa path in KAPPA_PATHS starts only from that alpha's
    kappa = 1 solution. A row whose own solve or check re-solve (G4 1.5 x T; NC4 2 x nodes, 1.5 x T) does not converge, or that raises, is
    'failed directly'. Every row that would start from it is 'failed upstream (row X)': later alphas and all their kappa paths for a critical
    row, every kappa path for kappa = 1, later rows on the same path otherwise. Rows on other paths carry on. No row is retried or given
    another start guess; a failed row carries no values (NOT COMPUTED (YET)) and counts as FAILED."""
    kind, layout, n, eps = job["kind"], job["layout"], job["n"], job["eps"]
    nN, nS = job["nN"], job["nS"]
    R_n = job.get("R_n")              # NC7 same-R rows: R taken from the 2T row with total winding R_n
    cname = chain_name(job)

    def lab(a, kap=None):
        return "%s alpha=%s %s" % (cname, lab_alpha(a), "critical (kappa = 1)" if kap is None else "stage NC kappa=%g" % kap)

    failed = []       # critical-stage rows that failed: no entry in results (every slot of the row NOT COMPUTED (YET))
    pending = None    # error on a step that is not itself a row (eps ladder, intermediate ladder point): the next row fails directly
    crit_up = None    # (row label, error) once a critical row has failed: every later alpha fails upstream
    # ---- eps ladder at alpha = 1 (B0 continuation, run.py:253-263, extended) ----
    prev = None
    a1 = (1.0, 1.0) if kind == "P12" else 1.0
    try:
        for e in [x for x in EPS_LADDER if x <= eps]:
            Rr = radius(kind, R_n if R_n else n, e, a1)
            G, TN, TS = make_geo(kind, n, e, a1, R=Rr)
            guess = guess_const(n, nN, nS, e) if prev is None else clamp(prev)
            prev, lw = solve_taubes(G, nN, nS, TN, TS, guess)
            if prev.status != 0:
                log.append("eps ladder status %d at eps %g" % (prev.status, e))
            capcheck(prev, "critical eps ladder eps=%g" % e)
    except Exception as ex:
        pending = "on the eps ladder before this row: " + err_text(ex)
    results = []
    alist = job["alphas"]
    ladder = job.get("ladder", alist)
    sa = prev
    pa = a1
    for a in ladder:
        if crit_up is None and pending is None:
            def crit_at(av, s0):
                Rr_ = radius(kind, R_n if R_n else n, eps, av)
                G_, TN_, TS_ = make_geo(kind, n, eps, av, R=Rr_)
                s_, lw_ = solve_taubes(G_, nN, nS, TN_, TS_, clamp(s0))
                return s_, lw_, G_, TN_, TS_
            try:
                if a == pa and a == a1:
                    G, TN, TS = make_geo(kind, n, eps, a, R=radius(kind, R_n if R_n else n, eps, a))
                    sa, lw = solve_taubes(G, nN, nS, TN, TS, clamp(sa))
                else:
                    sa, lw, G, TN, TS = continue_param(crit_at, pa, a, sa, log=log)
                capcheck(sa, "critical alpha=%s" % lab_alpha(a))
                pa = a
            except Exception as ex:
                pending = err_text(ex) if a in alist else "on the alpha ladder before this row (alpha=%s): %s" % (lab_alpha(a), err_text(ex))
        if a not in alist:
            continue
        if crit_up is not None:
            failed.append(dict(alpha=a, row=lab(a), **fail_entry("upstream", crit_up[1], crit_up[0])))
            continue
        if pending is not None:
            failed.append(dict(alpha=a, row=lab(a), **fail_entry("directly", pending)))
            crit_up = (lab(a), pending)
            continue
        try:
            res = dict(kind=kind, layout=layout, n=n, nN=nN, nS=nS, eps=eps, alpha=a, R=G.R, aN=G.aN, aS=G.aS, TN=TN, TS=TS,
                       same_R=bool(R_n), R_n=R_n)
            tt = tgrid(TN, TS, N_QUAD)
            C = crit_eval(G, sa, lw, nN, nS, tt)
            mu = 2 * math.pi * simpson(C["dens"], x=tt)
            phi2 = 2 * math.pi * simpson(C["f2"] * C["ph2"], x=tt)
            flux = 2 * math.pi * simpson(C["f2"] * C["B"], x=tt)
            area_num = 2 * math.pi * simpson(C["f2"], x=tt)
            tzz_f2, trr, tpp = stress_and_tzz(C["F"], C["Fp"], C["a"], C["B"], C["f2"], nN, 1.0)
            tzz = 2 * math.pi * simpson(tzz_f2, x=tt)
            Jv, Izv = ansatz_J_Iz(C["F"], C["f2"], tt)
            tips = tip_data(G, tt, C["dens"], C["ph2"], C["B"], C["f2"], nN, nS, eps)
            gb_tot, gb_tip = gauss_bonnet(G, TN, TS, tips)
            fd1 = fd_residual(G, sa, lw, FD_TH[1])
            fd2 = fd_residual(G, sa, lw, 2 * FD_TH[1] - 1)
            # G4: 2 x N_QUAD on the same solution, and a re-solve at 1.5 x T_i
            tt2 = tgrid(TN, TS, G4_NQ_FAC * N_QUAD - 1)
            C2 = crit_eval(G, sa, lw, nN, nS, tt2)
            mu_q = 2 * math.pi * simpson(C2["dens"], x=tt2)
            tips_q = tip_data(G, tt2, C2["dens"], C2["ph2"], C2["B"], C2["f2"], nN, nS, eps)
            TNb, TSb = T_FAC * TN, T_FAC * TS
            sb, lwb = solve_taubes(G, nN, nS, TNb, TSb, clamp(sa))
            ttb = tgrid(TNb, TSb, N_QUAD)
            T_err, mu_T, tips_T = None, None, None
            try:                                 # Venus N6: a non-converged check re-solve fails its own check only
                capcheck(sb, "critical G4 1.5 x T alpha=%s" % lab_alpha(a))
            except CapHit as ex:
                T_err = str(ex)
            if T_err is None:
                Cb = crit_eval(G, sb, lwb, nN, nS, ttb)
                mu_T = float(2 * math.pi * simpson(Cb["dens"], x=ttb))
                tips_T = tip_data(G, ttb, Cb["dens"], Cb["ph2"], Cb["B"], Cb["f2"], nN, nS, eps)
            g1prof = [float(np.exp(lw(tq) + sa.sol(tq)[0])) for tq in G.t_of_theta(np.array([math.pi / 4, math.pi / 2, 3 * math.pi / 4]))]
            res["crit"] = dict(status=int(sa.status), nodes=int(sa.x.size), rms=float(np.max(sa.rms_residuals)), mu=float(mu),
                               phi2=float(phi2), flux=float(flux), area_num=float(area_num),
                               area=float(area_formula(kind, G.R, a)), tzz=float(tzz), w=float(tzz / mu), trr=trr, tpp=tpp,
                               J=Jv, Iz=Izv, tips=tips, gb_tot=gb_tot, gb_tip=gb_tip, fd=(fd1, fd2), mu_q=float(mu_q), tips_q=tips_q,
                               mu_T=mu_T, tips_T=tips_T, statusT=int(sb.status), rmsT=float(np.max(sb.rms_residuals)), T_err=T_err,
                               g1prof=g1prof, end_f2R2=float(max(G.f2(np.array([-TN, TS]))) / G.R ** 2),
                               profile=profile_rows(G, sa, lw, nN, nS))
        except Exception as ex:
            e_ = err_text(ex)
            failed.append(dict(alpha=a, row=lab(a), **fail_entry("directly", e_)))
            crit_up = (lab(a), e_)
            continue
        # ---- stage NC: every kappa path starts only from this alpha's kappa = 1 solution ----
        nc = {}
        guess0 = nc_guess_from_crit(C, tt)
        listed = {k for path in KAPPA_PATHS for k in path if normal_state_listed(kind, layout, n, eps, a, k)}
        for k in sorted(listed):                 # Helios ruling (only rows the revised spec names): exact normal state, no BVP call
            r = nc_row(G, TN, TS, nN, nS, k, NormalState(G, TN, TS, n, res["crit"]["area"]), eps, tt=tt)
            r.update(normal_state=True, conv=None, min=None, tag=NORMAL_STATE_TAG)
            nc[k] = r

        def nc_full(kap, s, s1):
            r = nc_row(G, TN, TS, nN, nS, kap, s, eps, Ccrit=C if kap == 1.0 else None, tt=tt)
            r["normal_state"] = False
            # NC4: 2 x nodes (initial mesh and quadrature) and 1.5 x T_i
            # (Venus N6: a non-converged re-solve fails this entry's NC4 check only; nothing starts from it, so the path carries on)
            s2 = solve_nc(G.f2, nN, nS, kap, -TN, TS, clamp(s), nodes=2 * N_BVP0 - 1)
            s3 = solve_nc(G.f2, nN, nS, kap, -TNb, TSb, clamp(s))
            errs, okc = [], []
            for s_, wh in ((s2, "NC4 2 x nodes"), (s3, "NC4 1.5 x T")):
                try:
                    capcheck(s_, "%s kappa=%g alpha=%s" % (wh, kap, lab_alpha(a)))
                    okc.append(True)
                except CapHit as ex:
                    errs.append(str(ex))
                    okc.append(False)
            r2 = nc_row(G, TN, TS, nN, nS, kap, s2, eps, tt=tt2) if okc[0] else None
            r3 = nc_row(G, TNb, TSb, nN, nS, kap, s3, eps, tt=ttb) if okc[1] else None
            g_ = lambda rr, *ks: None if rr is None else (rr[ks[0]] if len(ks) == 1 else rr["tips"][ks[0]]["s_c"])
            r["conv"] = dict(status2=int(s2.status), status3=int(s3.status), mu2=g_(r2, "mu"), mu3=g_(r3, "mu"),
                             sc2=g_(r2, "N", 0), sc3=g_(r3, "N", 0), sc2S=g_(r2, "S", 0), sc3S=g_(r3, "S", 0), err="; ".join(errs) or None)
            # NC5: direct minimisation from the kappa = 1 solution of the same row
            Es = []
            info = []
            for hstep in NC5_H:
                Em, nit, msg = min_energy(G.f2, nN, n, kap, TN, TS, hstep, lambda tq: s1.sol(tq)[0], lambda tq: s1.sol(tq)[3])
                Es.append(Em)
                info.append((hstep, Em, nit, msg))
            r["min"] = dict(E=float((4 * Es[1] - Es[0]) / 3), info=info)
            return r

        s1, up1 = None, None
        try:
            s1 = capcheck(solve_nc(G.f2, nN, nS, 1.0, -TN, TS, guess0), "NC kappa=1 alpha=%s" % lab_alpha(a))
            nc[1.0] = nc_full(1.0, s1, s1)
        except Exception as ex:
            up1 = (lab(a, 1.0), err_text(ex))
            nc[1.0] = fail_entry("directly", up1[1])
        for path in KAPPA_PATHS:
            sp_, kb, up = s1, path[0], up1
            for k1 in path[1:]:
                if k1 in listed:
                    continue
                if up is not None:
                    nc[k1] = fail_entry("upstream", up[1], up[0])
                    continue
                try:
                    s_ = continue_param(lambda kv, s0: (solve_nc(G.f2, nN, nS, kv, -TN, TS, clamp(s0)),), kb, k1, sp_, log=log)[0]
                    capcheck(s_, "NC kappa=%g alpha=%s" % (k1, lab_alpha(a)))
                    nc[k1] = nc_full(k1, s_, s1)
                    sp_, kb = s_, k1
                except Exception as ex:
                    up = (lab(a, k1), err_text(ex))
                    nc[k1] = fail_entry("directly", up[1])
        res["nc"] = nc
        results.append(res)
    return dict(job=job, results=results, log=log, seconds=time.time() - t_start, failed=failed)


def plane_E(s, nu, kap, tt):
    F, Fp, a, b = s.sol(tt)
    f2 = np.exp(2 * tt)
    eB = 0.5 * b ** 2
    eV = kap / 8 * (1 - F ** 2) ** 2
    E = 2 * math.pi * simpson(0.5 * Fp ** 2 + 0.5 * (nu - a) ** 2 * F ** 2 + f2 * (eB + eV), x=tt)
    EB = 2 * math.pi * simpson(f2 * eB, x=tt)
    EV = 2 * math.pi * simpson(f2 * eV, x=tt)
    H = 0.5 * Fp ** 2 + 0.5 * f2 * b ** 2 - 0.5 * (nu - a) ** 2 * F ** 2 - kap / 8 * f2 * (F ** 2 - 1) ** 2
    rhs = 2 * f2 * (eB - eV)
    pw = float(np.max(np.abs(H - H[0] - cumulative_simpson(rhs, x=tt, initial=0.0))))
    flux = 2 * math.pi * simpson(f2 * b, x=tt)
    return dict(E=float(E), EB=float(EB), EV=float(EV), pw=pw, flux=float(flux))


def run_plane(nu):
    """Per-plane error handling (as for chains): a cap hit or any error returns no result; NC0 counts it FAILED."""
    t_start = time.time()
    MAXN["nodes"] = 0
    print("[plane start] nu=%g at %s" % (nu, datetime.datetime.now().strftime("%H:%M:%S")), flush=True)
    try:
        out = _run_plane(nu)
        out.update(error=None, seconds=time.time() - t_start, max_nodes=MAXN["nodes"])
        return out
    except CapHit as e:
        err = str(e)
    except Exception as e:
        err = "error: %s: %s" % (type(e).__name__, e)
    print("[plane ERROR] nu=%g: %s" % (nu, err), flush=True)
    return dict(nu=nu, res=None, log=[], error=err, seconds=time.time() - t_start, max_nodes=MAXN["nodes"])


def _run_plane(nu):
    """Flat-plane reference f = e^t (t = ln r), winding nu (integer or nu = n/alpha for the exact-cone row)."""
    tL = math.log(PLANE_RMIN)
    rmax = lambda kap, fac=1.0: fac * PLANE_RMAX0 / min(1.0, math.sqrt(kap))
    f2fun = lambda tt: np.exp(2 * tt)

    def g0(tt):
        r = np.exp(tt)
        F = np.tanh(r) ** nu
        Fp = nu * np.tanh(r) ** (nu - 1) / np.cosh(np.minimum(r, 300)) ** 2 * r
        return np.vstack([F, Fp, nu * (1 - np.exp(-r ** 2 / 2)), nu * np.exp(-r ** 2 / 2)])

    out = {}
    log = []
    s1 = capcheck(solve_nc(f2fun, nu, 0, 1.0, tL, math.log(rmax(1.0)), g0, plane=True), "plane nu=%g kappa=1" % nu)
    sols = {1.0: s1}
    for path in KAPPA_PATHS:
        sp_ = s1
        for k0, k1 in zip(path[:-1], path[1:]):
            sp_ = continue_param(lambda kv, s0: (solve_nc(f2fun, nu, 0, kv, tL, math.log(rmax(kv)), clamp(s0), plane=True),),
                                 k0, k1, sp_, log=log)[0]
            capcheck(sp_, "plane nu=%g kappa=%g" % (nu, k1))
            sols[k1] = sp_
    for kap in KAPPA_GRID:
        s = sols[kap]
        tR = math.log(rmax(kap))
        tt = np.linspace(tL, tR, N_QUAD)
        r = plane_E(s, nu, kap, tt)
        r.update(status=int(s.status), rms=float(np.max(s.rms_residuals)), rmax=rmax(kap))
        s2 = solve_nc(f2fun, nu, 0, kap, tL, tR, clamp(s), nodes=2 * N_BVP0 - 1, plane=True)
        tR3 = math.log(rmax(kap, T_FAC))
        s3 = solve_nc(f2fun, nu, 0, kap, tL, tR3, clamp(s), plane=True)
        r["conv_status"] = (int(s2.status), int(s3.status))
        if s2.status == 0 and s3.status == 0:
            r2 = plane_E(s2, nu, kap, np.linspace(tL, tR, G4_NQ_FAC * N_QUAD - 1))
            r3 = plane_E(s3, nu, kap, np.linspace(tL, tR3, N_QUAD))
            r["conv"] = max(abs(r2["E"] - r["E"]), abs(r3["E"] - r["E"])) / r["E"]
        else:                                    # Venus N6: fails the plane's NC4 check only (pl_ok), not the plane
            r["conv"] = float("inf")
            log.append("NC4 re-solve not converged at kappa=%g (status %s); NC4 FAILED for this plane" % (kap, r["conv_status"]))
        out[kap] = r
    return dict(nu=nu, res=out, log=log)


# ======================= main: inventory, jobs, grading, outputs =======================
OUT = []
REF = {}


def w(s=""):
    OUT.append(s)
    print(s, flush=True)


def pf(b):
    return "PASS" if b else "FAIL"


def fe(x):
    return "NOT COMPUTED (YET)" if x is None else "%.3e" % x


def fv(x, nd=10):
    return "NOT COMPUTED (YET)" if x is None else ("%." + str(nd) + "f") % x


def lab_alpha(a):
    return "(%g, %g)" % a if isinstance(a, tuple) else "%g" % a


def rowname(kind):
    return {"P0": "P0", "P1": "P1", "P2": "P2", "CGR": "C-GR [GR control]", "P12": "P12 (optional)"}[kind]


def relch(x, y):
    if x is None and y is None:
        return 0.0
    if x is None or y is None:
        return float("inf")
    return abs(x - y) / abs(x)


def write_outputs(files):
    for name, text in files.items():
        with open(J(HERE, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)


def sympy_identities():
    res = []
    th, Rs, a, aN, aS, et = sp.symbols("theta R alpha alpha_N alpha_S eta", positive=True)
    fP1 = Rs * sp.sin(th) * (a * sp.cos(th / 2) ** 2 + sp.sin(th / 2) ** 2)
    fP2 = Rs * a * sp.sin(th) * (1 + et * sp.sin(th) ** 2)
    fP12 = Rs * sp.sin(th) * (aN * sp.cos(th / 2) ** 2 + aS * sp.sin(th / 2) ** 2)
    for nm, f, A in (("P0", Rs * sp.sin(th), 4 * sp.pi * Rs ** 2), ("P1", fP1, 2 * sp.pi * Rs ** 2 * (1 + a)),
                     ("P2", fP2, 2 * sp.pi * Rs ** 2 * a * (2 + 4 * et / 3)), ("C-GR", Rs * a * sp.sin(th), 4 * sp.pi * Rs ** 2 * a),
                     ("P12", fP12, 2 * sp.pi * Rs ** 2 * (aN + aS))):
        res.append(("area A(%s) = 2 pi R int_0^pi f dtheta equals the spec formula" % nm,
                    str(sp.simplify(2 * sp.pi * Rs * sp.integrate(f, (th, 0, sp.pi)) - A))))
    res.append(("P1 at alpha = 1 reduces to P0", str(sp.simplify(fP1.subs(a, 1) - Rs * sp.sin(th)))))
    for nm, f, an, as_ in (("P1", fP1, a, 1), ("P2", fP2, a, a), ("C-GR", Rs * a * sp.sin(th), a, a), ("P12", fP12, aN, aS)):
        res.append(("tip angles of %s: f_theta(0)/R - alpha_N and -f_theta(pi)/R - alpha_S" % nm,
                    str((sp.simplify(sp.diff(f, th).subs(th, 0) / Rs - an), sp.simplify(-sp.diff(f, th).subs(th, sp.pi) / Rs - as_)))))
    tt, nn, kp = sp.symbols("t n kappa", real=True)
    res.append(("lw'' = -n sech^2 t for lw = n_N log sigma(2t) + n_S log sigma(-2t) (n = n_N + n_S)",
                str(sp.simplify(sp.diff(sp.Symbol("n_N") * sp.log(1 / (1 + sp.exp(-2 * tt))) + sp.Symbol("n_S") * sp.log(1 / (1 + sp.exp(2 * tt))), tt, 2)
                                + (sp.Symbol("n_N") + sp.Symbol("n_S")) / sp.cosh(tt) ** 2).rewrite(sp.exp))))
    F, A_, fs = sp.Function("F")(tt), sp.Function("a")(tt), sp.Function("f")(tt)
    L = sp.Rational(1, 2) * F.diff(tt) ** 2 + sp.Rational(1, 2) * (nn - A_) ** 2 * F ** 2 + sp.Rational(1, 2) * A_.diff(tt) ** 2 / fs ** 2 \
        + kp / 8 * fs ** 2 * (F ** 2 - 1) ** 2
    Fpp = (nn - A_) ** 2 * F + kp / 2 * fs ** 2 * F * (F ** 2 - 1)
    app = sp.solve(sp.Eq(sp.diff(A_.diff(tt) / fs ** 2, tt), -(nn - A_) * F ** 2), A_.diff(tt, 2))[0]
    el_F = sp.simplify(sp.diff(L.diff(F.diff(tt)), tt) - L.diff(F) - (Fpp - F.diff(tt, 2)) * 0 - (F.diff(tt, 2) - Fpp))
    Hs = F.diff(tt) * L.diff(F.diff(tt)) + A_.diff(tt) * L.diff(A_.diff(tt)) - L
    eB = sp.Rational(1, 2) * (A_.diff(tt) / fs ** 2) ** 2
    eV = kp / 8 * (1 - F ** 2) ** 2
    dH = sp.diff(Hs, tt).subs({F.diff(tt, 2): Fpp, A_.diff(tt, 2): app})
    res.append(("EL equation for F from the reduced energy equals the spec's F'' (residual of d/dt dL/dF' - dL/dF - (F'' - RHS))",
                str(sp.simplify(el_F))))
    res.append(("NC2: on shell dH/dt = 2 f^2 (ln f)' (e_B - e_V)", str(sp.simplify(dH - 2 * fs ** 2 * fs.diff(tt) / fs * (eB - eV)))))
    Lc = L.subs(kp, 1)
    bog = sp.Rational(1, 2) * (F.diff(tt) - (nn - A_) * F) ** 2 + (A_.diff(tt) - fs ** 2 * (1 - F ** 2) / 2) ** 2 / (2 * fs ** 2) \
        + sp.diff((nn - A_) * F ** 2 / 2 + A_ / 2, tt)
    res.append(("Bogomolny completion at kappa = 1: L = squares + d/dt[(n - a)F^2/2 + a/2]", str(sp.simplify(sp.expand(Lc - bog)))))
    return res


def prologue():
    T0 = time.time()
    now = datetime.datetime.now().astimezone()
    z = now.strftime("%z")
    w("Symbol map: code `u` = spec chi(t) (Taubes function, B0's name) | velocity = `u_flow` (never a bare u; NOT COMPUTED (YET) here: no MHD solve) | "
      "kappa = lambda/e^2 (coupling) | beta = plasma beta only (unused) | eta = P2 shape parameter (code P2_SHAPE = %g) | "
      "s_c = proper (geodesic) core radius from the tip vs r_c = f(theta_c)/alpha_i, the exterior cone coordinate (never copy s_c into r_c)." % P2_SHAPE)
    w("")
    w("# SM1-INPUTS-RUN: tensioned vortices at a tip (RESULTS, generated by run.py; do not edit by hand)")
    w("")
    w("Generated %s (local time, UTC%s:%s) on %s. Python %s, numpy %s, scipy %s, sympy %s; %d CPUs.%s" % (
        now.strftime("%Y-%m-%d %H:%M:%S"), z[:3], z[3:], platform.node(), platform.python_version(), np.__version__,
        scipy.__version__, sp.__version__, os.cpu_count(), "  **SMOKE MODE: non-graded settings, not a graded run.**" if SMOKE else ""))
    w("")
    w("**Scope.** Matter only, on fixed (non-back-reacted) backgrounds [assumed]. No gravitational equation is used anywhere; alpha is "
      "scanned, never derived from mu; G appears only as the output curve G_req(alpha); the core's f(theta) is unknown QG and is NOT "
      "COMPUTED (YET). C-GR is a [GR control] row, never the core. Part B (JOB_SM1B_SPEC.md 6611EE3B) is HELD and is not built; "
      "the MHD core job (JOB_SM1_MHD_CORE_SPEC.md A0756351) is not built. Stability of every axisymmetric critical point is NOT COMPUTED (YET).")
    w("")
    # ---------------- inventory ----------------
    w("## Inventory: read-only sources (SHA-256 prefix; run stops on any mismatch)")
    w("")
    w("| source | path | expected | found | CRC32 | match |")
    w("|---|---|---|---|---|---|")
    before = {}
    bad = []
    for nm, path, exp in SOURCES:
        if not os.path.isfile(path):
            w("| %s | %s | %s | MISSING | - | NO |" % (nm, os.path.relpath(path, USER), exp))
            bad.append(nm)
            continue
        hsh, crc = sha8(path)
        before[path] = (hsh, crc)
        ok = (exp is None) or (hsh == exp)
        w("| %s | %s | %s | %s | %s | %s |" % (nm, os.path.relpath(path, USER), exp if exp else "(no hash in spec; recorded)", hsh, crc,
                                              "YES" if exp and ok else ("recorded" if ok else "NO")))
        if not ok:
            bad.append(nm)
    if B0NS is None:
        bad.append("B0 AST import")
    w("")
    if bad:
        w("**STOP: %d source(s) missing or with a different hash (%s). Nothing computed.**" % (len(bad), ", ".join(bad)))
        write_outputs({"RESULTS.md": "\n".join(OUT) + "\n"})
        sys.exit(2)
    w("All hashed sources match: YES. Spec line count: %d." % len(open(SPEC, encoding="utf-8").read().splitlines()))
    w("Part B (JOB_SM1B_SPEC.md 6611EE3B) is box-only and HELD; this run does not read it. Venus's pre-check (085B3E96) and re-check "
      "(76BC2EB1) are box-only references, not inputs.")
    w("B0 code taken read-only by AST from B0 run.py (functions/constants: %s): T_BVP = %g (the 14 in T_i), N_BVP0 = %d, BVP_TOL = %g, N_QUAD = %d, "
      "CONT_EPS = %s." % (", ".join(B0_KEPT), T_BASE, N_BVP0, BVP_TOL, N_QUAD, B0NS["CONT_EPS"]))
    jf_al, jf_line = jobfour_alphas()
    w("Job Four ALPHAS read by AST from run.py line %s: %s; contained in this run's alpha grid: %s." % (
        jf_line, jf_al, all(any(abs(x - y) < 1e-12 for y in ALPHA_GRID) for x in jf_al)))
    own_skip = ("RESULTS.md", "profiles.csv", "per_tip.csv", "consistency_curve.csv", "nc_scan.csv", "SM1_INPUTS_FILLED.md")
    own_before = {f: sha8(J(HERE, f)) for f in sorted(os.listdir(HERE)) if os.path.isfile(J(HERE, f)) and f not in own_skip}
    w("This folder before the run (files other than this run's outputs): %s." % ", ".join("%s %s" % (f, h[0]) for f, h in own_before.items()))
    slots = []
    in_block = False
    for ln in open(INPUTS, encoding="utf-8").read().splitlines():
        if ln.strip().startswith("```"):
            in_block = not in_block
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z_/]*) = ", ln)
        if in_block and m:
            slots.append(m.group(1))
    w("SM1_INPUTS.md (E0D7D41D) slots read (names only; no value is used): %s." % ", ".join(slots))
    w("")
    # ---------------- fixed settings and predictions ----------------
    w("## Fixed before the graded run (spec %s)" % SPEC_HASH)
    w("")
    w("- Grids: alpha in %s; eps in %s (A = 4 pi n (1 + eps)); 1T n in %s; 2T n in %s (n/2 per tip); P2 eta = %g; P12 (alpha_N, alpha_S) = %s; "
      "kappa in %s via %s; delta = %g; secondary s_c grid %s." % (ALPHA_GRID, EPS_GRID, N_1T, N_2T, P2_SHAPE, P12_ALPHAS, KAPPA_GRID,
                                                                 " and ".join(" -> ".join("%g" % k for k in p) for p in KAPPA_PATHS), DELTA, SC_GRID))
    w("- Tolerances: G1 %g rel (energy, int|phi|^2), %g abs (profiles); G2 (i),(ii) %g rel, (iii),(iv) %g abs; G3 Bogomolny %g, lower bound "
      "mu >= pi n (1 - %g), solver rms residual < %g; G4 (x%d N_QUAD, x%g T_i) mu %g, mu_i %g, s_c %g; G5 %g / %g / %g; G6 %g; G7 %g; "
      "NC1 %g / %g; NC2 %g (integral) and %g mu/(2 pi) (pointwise); NC3 %g; NC4 %g / s_c %g; NC5 %g; NC6 margin > %g x NC4 error; "
      "NC7 %g / %g (same R only); background test max(%g, %g e_num); profile test max(%g rel, %g x NC4)." % (
          G1_E_TOL, G1_PROF_TOL, G2_FLUX_TOL, G2_GB_TOL, G3_BOG_TOL, G3_LOW_TOL, G3_RES_TOL, G4_NQ_FAC, T_FAC, G4_MU_TOL, G4_MUI_TOL,
          G4_SC_TOL, G5_TOL, G5_SPLIT_TOL, G5_TIP_TOL, G6_TOL, G7_TOL, NC1_MU_TOL, NC1_PROF_TOL, NC2_INT_TOL, NC2_PW_TOL, NC3_TOL,
          NC4_MU_TOL, NC4_SC_TOL, NC5_TOL, NC6_MARGIN_FAC, NC7_SPLIT_TOL, NC7_SAME_R_TOL, BG_FLOOR, BG_NUM_FAC, PROF_FLOOR, PROF_NUM_FAC))
    w("- Solver choices [assumed]: solve_bvp tol %g (B0); T_i = (%g + ln R)/alpha_i; eps continuation %s; alpha continuation downward from 1; "
      "bisection fallback depth %d; flat plane r in [%g, 40/min(1, sqrt kappa)]; NC5 L-BFGS on grids h = %s with Richardson (4E_{h/2} - E_h)/3, "
      "started from the kappa = 1 solution of the same row. Mesh-node cap on both solve_bvp calls: MAX_NODES = %d (crash-1 fix; a capped "
      "solve fails its whole chain, which stays NOT COMPUTED (YET) and FAILED in check C0/NC0); worker processes: %d; normal-state fill: %s." % (
          BVP_TOL, T_BASE, EPS_LADDER, MAX_SUBSTEP_DEPTH, PLANE_RMIN, NC5_H, MAX_NODES, N_WORKERS,
          ("ON for %d named rows %s" % (len(NORMAL_STATE_ROWS), NORMAL_STATE_TAG)) if NORMAL_STATE_ROWS else "OFF (no rows named)"))
    w("- Reading tags: every mu and G_req is printed in units v^2 (e = v = 1) with both readings: Reading I = brane tension T_b at the tip "
      "(mass^4, G_req is G_6-type); Reading II = 4D string mu (mass^2, G_req is dimensionless G v^2).")
    w("")
    w("PREDICTIONS (written before the run):")
    for k, v in PRED.items():
        w("- %s: %s" % (k, v))
    w("")
    # ---------------- section 0 copied from the spec ----------------
    spec_lines = open(SPEC, encoding="utf-8").read().splitlines()
    i0 = next(i for i, l in enumerate(spec_lines) if l.startswith("## 0."))
    i1 = next(i for i, l in enumerate(spec_lines) if l.startswith("## 1."))
    w("## Section 0 of the spec, copied verbatim (spec lines %d-%d)" % (i0 + 1, i1))
    w("")
    for l in spec_lines[i0 + 1:i1]:
        w("> " + l if l else ">")
    w("")
    # ---------------- identities ----------------
    w("## Identities [identity; sympy]")
    w("")
    w("| statement | sympy residual |")
    w("|---|---|")
    for stt, r in sympy_identities():
        w("| %s | %s |" % (stt, r))
    w("")
    return before, own_before, slots, T0


def build_jobs():
    jobs = []
    ladder = ALPHA_GRID if not SMOKE else [1.0, 0.95, 0.8, 0.65, 0.55]
    for eps in EPS_GRID:
        for n in N_1T:
            jobs.append(dict(kind="P0", layout="1T", n=n, nN=n, nS=0, eps=eps, alphas=[1.0], ladder=[1.0]))
            for kind in ("P1", "CGR"):
                jobs.append(dict(kind=kind, layout="1T", n=n, nN=n, nS=0, eps=eps, alphas=list(ALPHA_GRID), ladder=list(ladder)))
        for n in N_2T:
            for kind in ("P2", "CGR"):
                jobs.append(dict(kind=kind, layout="2T", n=n, nN=n // 2, nS=n // 2, eps=eps, alphas=list(ALPHA_GRID), ladder=list(ladder)))
        mid = tuple(0.5 * (1 + x) for x in P12_ALPHAS)
        jobs.append(dict(kind="P12", layout="2T-unequal", n=2, nN=1, nS=1, eps=eps, alphas=[P12_ALPHAS], ladder=[(1.0, 1.0), mid, P12_ALPHAS]))
    for n in N_2T:       # NC7 second item: the 1T n/2 row solved on the 2T row's sphere (same R)
        jobs.append(dict(kind="CGR", layout="1T-sameR", n=n // 2, nN=n // 2, nS=0, eps=EPS_LARGE, alphas=list(ALPHA_GRID),
                         ladder=list(ladder), R_n=n))
    jobs.sort(key=lambda j: -(len(j["alphas"]) * 10 + j["n"] + j["eps"] / 1000))
    return jobs


def nus_needed():
    nus = {1.0, 2.0}
    for n in N_1T:
        for a in ALPHA_GRID:
            nus.add(round(n / a, 12))
    return sorted(nus)


def b0_code_regression():
    """Report-only: B0's own solve_bg/integrals (AST-imported) re-run with B0's continuation, for n = 1, 2, 3 at eps = 1, 4."""
    out = {}
    for n in (1, 2, 3):
        prev = None
        for eps in B0NS["CONT_EPS"]:
            R2 = n * (1 + eps)
            if prev is None:
                u0 = math.log((n + 1) * (1 - 1 / (1 + eps)))
                guess = lambda tt, u0=u0: np.vstack([np.full(tt.size, u0), np.zeros(tt.size)])
            else:
                guess = lambda tt, s=prev: s.sol(tt)
            s, lw = B0NS["solve_bg"](n, n, R2, guess)
            prev = s
            if eps in (1.0, 4.0):
                phi2, E, _ = B0NS["integrals"](s, lw, n, n, R2)
                out[(n, eps)] = (E, phi2)
    return out


def main():
    before, own_before, slots, T0 = prologue()
    jobs = build_jobs()
    nns = check_normal_state_rows(jobs) if not SMOKE else len(NORMAL_STATE_ROWS)
    nus = nus_needed()
    nproc = min(os.cpu_count() or 1, N_WORKERS)
    w("## Run log")
    w("")
    w("%d chains (row x layout x n x eps; alpha and kappa continued inside each chain) and %d flat-plane windings, on %d worker processes. "
      "Mesh-node cap on both solve_bvp calls: MAX_NODES = %d (a solve that hits it is 'not converged (cap hit)'). Error boundary: per row "
      "along each path (the alpha ladder; at each alpha, every kappa path starts only from that alpha's kappa = 1 solution). A row that does not "
      "converge is 'failed directly'; every row that would start from it is 'failed upstream (row X)'; both stay NOT COMPUTED (YET) and count as "
      "FAILED; rows on other paths carry on; nothing is retried or re-started. A non-converged check re-solve (G4 1.5 x T, NC4 2 x nodes or "
      "1.5 x T) fails only its own check: nothing starts from it (Venus N6). A plane whose main solve fails fails as a whole; a plane's NC4 "
      "re-solve fails only its NC4 check. Normal-state rows filled analytically (spec C9683FDD 3b; asserted equal to the spec list and "
      "to the chain list under B >= kappa/2): %d %s; at (eps, kappa) = (1, 0.5): %s." % (
        len(jobs), len(nus), nproc, MAX_NODES, nns, NORMAL_STATE_TAG, NORMAL_STATE_ZERO_MODES))
    with ProcessPoolExecutor(max_workers=nproc) as ex:
        fut_c = [ex.submit(run_chain, j) for j in jobs]
        fut_p = [ex.submit(run_plane, nu) for nu in nus]
        b0reg = b0_code_regression() if G1_ROWS else {}
        done = 0
        for f in as_completed(fut_c + fut_p):          # console progress only (not written to RESULTS)
            done += 1
            r_ = f.result()
            print("[progress] %d/%d done at %.0f s: %s (%.0f s)%s" % (done, len(fut_c) + len(fut_p), time.time() - T0,
                  ("plane nu=%g" % r_["nu"]) if "nu" in r_ else chain_name(r_["job"]), r_["seconds"],
                  (" FAILED: " + r_["error"]) if r_["error"] is not None else
                  ("" if not (r_.get("failed") or any(isfail(x) for r in r_.get("results", []) for x in r["nc"].values()))
                   else " (some rows FAILED; listed in RESULTS)")), flush=True)
        chains = [f.result() for f in fut_c]
        pl_all = [f.result() for f in fut_p]
    planes = {p["nu"]: p for p in pl_all if p["error"] is None}
    FAILS = dict(chains=[(chain_name(c["job"]), c["error"], c["seconds"]) for c in chains if c["error"] is not None],
                 failed_jobs=[(c["job"], c["error"]) for c in chains if c["error"] is not None],
                 crit=[(c["job"], f) for c in chains for f in c["failed"]],
                 nc=[(c["job"], r["alpha"], k, x) for c in chains for r in c["results"] for k, x in sorted(r["nc"].items()) if isfail(x)],
                 n_crit_rows=sum(len(j["alphas"]) for j in jobs), n_paths=sum(len(j["alphas"]) for j in jobs) * len(KAPPA_PATHS),
                 planes=[("plane nu=%g" % p["nu"], p["error"], p["seconds"]) for p in pl_all if p["error"] is not None],
                 n_chains=len(chains), n_planes=len(pl_all))
    w("All workers finished after %.0f s [computed]. Continuation fallbacks used: %d (listed below if any)." % (
        time.time() - T0, sum(len(c["log"]) for c in chains) + sum(len(p["log"]) for p in planes.values())))
    w("")
    w("### Chain and plane completion (every chain and plane listed; failures are never dropped or retried)")
    w("")
    w("'Never retried' (spec C9683FDD 3b) means: after the pre-registered continuation fallback (bisection of a failed parameter step, "
      "MAX_SUBSTEP_DEPTH = %d, already in 235D00E5 and DB7ECF85's run) is used up, the row is not solved again (Venus N7)." % MAX_SUBSTEP_DEPTH)
    w("")
    w("| task | outcome | largest converged node count | seconds |")
    w("|---|---|---:|---:|")

    def c_outcome(c):
        if c["error"] is not None:
            return "**FAILED (error outside any row): %s**; every row NOT COMPUTED (YET)" % c["error"]
        cd = sum(1 for f in c["failed"] if f["failed"] == "directly")
        ncx = [x for r in c["results"] for x in r["nc"].values() if isfail(x)]
        nd = sum(1 for x in ncx if x["failed"] == "directly")
        nre = sum(1 for r in c["results"] for x in r["nc"].values() if not isfail(x) and x.get("conv") and x["conv"].get("err")) + \
            sum(1 for r in c["results"] if r["crit"].get("T_err"))
        if not c["failed"] and not ncx and not nre:
            return "converged (every row)"
        if not c["failed"] and not ncx:
            return "every row's main solve converged; %d check re-solve(s) not converged (listed below)" % nre
        return ("**rows FAILED**: critical rows %d directly, %d upstream; stage-NC entries %d directly, %d upstream (listed below); "
                "every other row converged" % (cd, len(c["failed"]) - cd, nd, len(ncx) - nd))
    for c in sorted(chains, key=lambda c: chain_name(c["job"])):
        w("| %s | %s | %d | %.0f |" % (chain_name(c["job"]), c_outcome(c), c["max_nodes"], c["seconds"]))
    for p in sorted(pl_all, key=lambda p: p["nu"]):
        w("| plane nu=%g | %s | %d | %.0f |" % (p["nu"], "converged" if p["error"] is None else "**FAILED: %s**; NOT COMPUTED (YET)" % p["error"],
                                             p["max_nodes"], p["seconds"]))
    w("")
    mx = max(chains + pl_all, key=lambda c: c["max_nodes"])
    FAILS["max_nodes"] = (mx["max_nodes"], ("plane nu=%g" % mx["nu"]) if "nu" in mx else chain_name(mx["job"]))
    w("Largest node count used by any converged solve_bvp (every chain and plane; includes eps/alpha/kappa continuation substeps and the "
      "G4/NC4 check re-solves): %d (%s), against MAX_NODES = %d [computed; report-only, H3]." % (FAILS["max_nodes"][0], FAILS["max_nodes"][1], MAX_NODES))
    w("")
    if FAILS["crit"] or FAILS["nc"] or FAILS["chains"] or any(r["crit"].get("T_err") or any(
            not isfail(x) and x.get("conv") and x["conv"].get("err") for x in r["nc"].values()) for c in chains for r in c["results"]):
        w("### Failed rows (every one listed; 'failed directly' or 'failed upstream (row X)'; NOT COMPUTED (YET); FAILED in the tally; never retried)")
        w("")
        for nm, err, _ in FAILS["chains"]:
            w("- %s, every row: failed directly (error outside any row): %s" % (nm, err))
        for j, f in FAILS["crit"]:
            w("- %s: %s" % (f["row"], fail_text(f)))
        for r in sorted([r for c in chains for r in c["results"]], key=lambda r: str((r["kind"], r["layout"], r["n"], r["eps"], r["alpha"]))):
            if r["crit"].get("T_err"):
                w("- %s %s n=%d eps=%g alpha=%s critical (kappa = 1): G4 1.5 x T re-solve failed directly: %s (fails G3/G4 and C0; the row's other "
                  "values stand and nothing starts from the re-solve)" % (r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), r["crit"]["T_err"]))
            for k, x in sorted(r["nc"].items()):
                if not isfail(x) and x.get("conv") and x["conv"].get("err"):
                    w("- %s %s n=%d eps=%g alpha=%s stage NC kappa=%g: NC4 re-solve failed directly: %s (fails this entry's NC4 check only; the "
                      "path carries on from the converged solve)" % (r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), k, x["conv"]["err"]))
        for j, a, k, x in FAILS["nc"]:
            w("- %s alpha=%s stage NC kappa=%g: %s" % (chain_name(j), lab_alpha(a), k, fail_text(x)))
        w("")
    for c in chains:
        for l in c["log"]:
            w("- %s %s n=%d eps=%g: %s" % (c["job"]["kind"], c["job"]["layout"], c["job"]["n"], c["job"]["eps"], l))
    for p in planes.values():
        for l in p["log"]:
            w("- plane nu=%g: %s" % (p["nu"], l))
    w("")
    ROWS = {}
    SAMER = {}
    for c in chains:
        for r in c["results"]:
            key = (r["kind"], r["layout"], r["n"], r["eps"], r["alpha"])
            (SAMER if r["same_R"] else ROWS)[key] = r
    try:
        report(ROWS, SAMER, planes, b0reg, before, own_before, slots, T0, FAILS)
    except Exception:                            # never lose the run: write what exists plus the traceback
        import traceback
        w("")
        w("## REPORT ERROR (run.py could not finish the report; everything above is valid as printed)")
        w("")
        w("```")
        for line in traceback.format_exc().splitlines():
            w(line)
        w("```")
        write_outputs({"RESULTS.md": "\n".join(OUT) + "\n"})
        raise


def report(ROWS, SAMER, planes, b0reg, before, own_before, slots, T0, FAILS):
    PI = math.pi
    graded = {k: r for k, r in ROWS.items() if r["kind"] != "P12"}
    CHK = []          # (id, item, worst, tol, n, ok)
    nfail_c = len(FAILS["chains"])
    n_whole = sum(len(j["alphas"]) for j, _ in FAILS["failed_jobs"])
    n_cd = sum(1 for _, f in FAILS["crit"] if f["failed"] == "directly")
    n_cu = len(FAILS["crit"]) - n_cd
    n_T = sum(1 for r in list(ROWS.values()) + list(SAMER.values()) if r["crit"].get("T_err"))
    CHK.append(("C0", "every critical-stage solve converged under the cap (eps ladder, alpha continuation, G4 1.5 x T re-solve; stage-NC solves "
                "are counted in NC0, never here); a failed row is 'failed directly' or 'failed upstream (row X)', NOT COMPUTED (YET), never dropped",
                "%d of %d rows failed (%d directly, %d upstream, %d in %d chains that errored outside a row); %d G4 1.5 x T re-solves not converged" % (
                    n_cd + n_cu + n_whole, FAILS["n_crit_rows"], n_cd, n_cu, n_whole, nfail_c, n_T), "0 failed", FAILS["n_crit_rows"],
                n_cd + n_cu + n_whole + n_T == 0))

    def add(cid, item, vals, tol, ok=None, fmt=fe):
        vals = [v for v in vals]
        worst = max(vals) if vals else None
        okv = (worst is not None and worst < tol) if ok is None else ok
        CHK.append((cid, item, fmt(worst) if worst is not None else "-", ("%g" % tol) if isinstance(tol, float) else str(tol), len(vals), okv))
        return okv

    # ---------------- G1 ----------------
    w("## G1: B0 regression (P0, 1T) against B0 RESULTS.md (AE4E8FFB) [standard]")
    w("")
    b0lines = open(J(B0DIR, "RESULTS.md"), encoding="utf-8").read().splitlines()
    g1_ok = bool(G1_ROWS)
    w("| n | eps | B0 line (energy, int|phi|^2) | B0 energy | this run mu_matter | rel. err | B0 int|phi|^2 | this run | rel. err | "
      "B0 profile line | |phi|^2 at pi/4, pi/2, 3pi/4 (B0) | this run | max abs err | B0 code re-run (AST): energy rel. diff vs this run (report-only) |")
    w("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|")
    g1E, g1P = [], []
    for n, eps, Lr, Lp in G1_ROWS:
        c = [x.strip() for x in b0lines[Lr - 1].split("|")]
        cp = [x.strip() for x in b0lines[Lp - 1].split("|")]
        okline = (int(c[1]) == n and float(c[2]) == eps and int(cp[1]) == n and float(cp[2]) == eps)
        E0, P0v = float(c[10]), float(c[7])
        prof0 = [float(x) for x in cp[3].split(",")][1:4]
        rr_ = ROWS.get(("P0", "1T", n, eps, 1.0))
        if rr_ is None:                          # row failed (counted in C0): this G1 row cannot pass
            g1_ok = False
            w("| %d | %g | %d | %s | NOT COMPUTED (YET) (row failed) | - | %s | NOT COMPUTED (YET) | - | %d | %s | NOT COMPUTED (YET) | - | - |" % (
                n, eps, Lr, c[10], c[7], Lp, ", ".join(cp[3].split(",")[1:4])))
            continue
        r = rr_["crit"]
        eE = abs(r["mu"] - E0) / E0
        eP = abs(r["phi2"] - P0v) / P0v
        eQ = max(abs(a - b) for a, b in zip(r["g1prof"], prof0))
        g1E += [eE, eP]
        g1P.append(eQ)
        g1_ok &= okline and eE < G1_E_TOL and eP < G1_E_TOL and eQ < G1_PROF_TOL
        b0c = b0reg.get((n, eps))
        w("| %d | %g | %d | %s | %.10f | %.1e | %s | %.10f | %.1e | %d | %s | %s | %.1e | %s |" % (
            n, eps, Lr, c[10], r["mu"], eE, c[7], r["phi2"], eP, Lp, ", ".join(cp[3].split(",")[1:4]),
            ", ".join("%.6f" % x for x in r["g1prof"]), eQ, ("%.1e" % (abs(b0c[0] - r["mu"]) / r["mu"])) if b0c else "-"))
    w("")
    b0err = []
    for L in range(31, 49):
        c = [x.strip() for x in b0lines[L - 1].split("|")]
        b0err.append(float(c[12]))
    w("B0's printed energy relative errors (RESULTS.md lines 31-48): max %.1e; <= %g (Venus 76BC2EB1 N4-a): %s. SM1_INPUTS.md line 58 says "
      "'to 1e-12' (erratum found by Venus; the correct bound is <= 5e-12) [report-only]." % (max(b0err), B0_REG_ERRATUM, max(b0err) <= B0_REG_ERRATUM))
    w("")
    add("G1", "B0 regression: energy and int|phi|^2 (relative)", g1E, G1_E_TOL, ok=g1_ok and all(x < G1_E_TOL for x in g1E))
    add("G1", "B0 regression: |phi|^2 profile (absolute)", g1P, G1_PROF_TOL, ok=g1_ok and all(x < G1_PROF_TOL for x in g1P))

    # ---------------- G2-G7 ----------------
    e_fl, e_ph, e_gb, e_gbt, e_bog, low_ok, e_rms, st_ok = [], [], [], [], [], True, [], True
    e4m, e4i, e4s = [], [], []
    e4i_v, e4i_0, e4i_abs, e4i_frac = [], [], [], []        # report-only breakdown of G4 mu_i (vortex tips / n_i = 0 tips / change over mu_matter)
    e7 = []
    for k, r in graded.items():
        c = r["crit"]
        n = r["n"]
        e_fl.append(abs(c["flux"] - 2 * PI * n) / (2 * PI * n))
        e_ph.append(abs(c["phi2"] - (c["area"] - 4 * PI * n)) / (c["area"] - 4 * PI * n))
        e_gb.append(c["gb_tot"])
        e_gbt.append(c["gb_tip"])
        e_bog.append(abs(c["mu"] - PI * n) / (PI * n))
        low_ok &= c["mu"] >= PI * n * (1 - G3_LOW_TOL)
        e_rms.append(max(c["rms"], c["rmsT"]))
        st_ok &= c["status"] == 0 and c["statusT"] == 0 and not c.get("T_err")
        e4m.append(max(relch(c["mu"], c["mu_q"]), relch(c["mu"], c["mu_T"])))
        for tip in ("N", "S"):
            for alt in ("tips_q", "tips_T"):
                if c[alt] is None:               # G4 1.5 x T re-solve not converged (Venus N6): this check fails
                    e4i.append(float("inf"))
                    e4s.append(float("inf"))
                    continue
                e4i.append(relch(c["tips"][tip]["mu_i"], c[alt][tip]["mu_i"]))
                (e4i_v if c["tips"][tip]["n_i"] > 0 else e4i_0).append(e4i[-1])
                if c["tips"][tip]["n_i"] == 0:
                    e4i_frac.append(c["tips"][tip]["mu_i"] / c["mu"])
                e4i_abs.append(abs(c["tips"][tip]["mu_i"] - c[alt][tip]["mu_i"]) / c["mu"])
                if c["tips"][tip]["n_i"] > 0:
                    e4s.append(relch(c["tips"][tip]["s_c"], c[alt][tip]["s_c"]))
        e7.append(abs(c["w"] + 1))
    add("G2", "(i) total flux = 2 pi n (relative)", e_fl, G2_FLUX_TOL)
    add("G2", "(ii) int|phi|^2 dA = A - 4 pi n (relative)", e_ph, G2_PHI_TOL)
    add("G2", "(iii) Gauss-Bonnet total (absolute)", e_gb, G2_GB_TOL)
    add("G2", "(iv) per-tip disk Gauss-Bonnet at the midpoint and secondary circles (absolute)", e_gbt, G2_GB_TOL)
    add("G3", "Bogomolny |mu - pi n|/(pi n)", e_bog, G3_BOG_TOL, ok=max(e_bog) < G3_BOG_TOL and low_ok)
    add("G3", "lower bound mu >= pi n (1 - 1e-9) on every row", [0.0 if low_ok else 1.0], 0.5, ok=low_ok, fmt=lambda x: "all rows" if low_ok else "violated")
    add("G3", "solver: max solve_bvp rms_residuals (base and 1.5 T solves), all converged", e_rms, G3_RES_TOL, ok=max(e_rms) < G3_RES_TOL and st_ok)
    add("G4", "mu_matter relative change (2 x N_QUAD; 1.5 x T_i)", e4m, G4_MU_TOL)
    add("G4", "mu_i relative change, both tips (2 x N_QUAD; 1.5 x T_i)", e4i, G4_MUI_TOL)
    add("G4", "s_c,delta relative change at vortex tips (2 x N_QUAD; 1.5 x T_i)", e4s, G4_SC_TOL)
    # G5
    e5a, e5b, e5c = [], [], []
    for (kind, lay, n, eps, a), r in graded.items():
        if lay == "2T":
            m = r["crit"]["mu"]
            e5b.append(abs(r["crit"]["tips"]["N"]["mu_i"] + r["crit"]["tips"]["S"]["mu_i"] - m) / m)
            other = ("CGR", "1T", n, eps, a) if kind == "CGR" else ("P1", "1T", n, eps, a)
            if other in graded:                  # a missing partner is a failed chain, already FAILED in C0
                e5a.append(abs(m - graded[other]["crit"]["mu"]) / graded[other]["crit"]["mu"])
            if eps == EPS_LARGE:
                for tip in ("N", "S"):
                    e5c.append(abs(r["crit"]["tips"][tip]["mu_i"] - PI * n / 2) / (PI * n / 2))
    add("G5", "mu(2T, n) = mu(1T, n): C-GR 2T vs C-GR 1T and P2 2T vs P1 1T (relative)", e5a, G5_TOL)
    add("G5", "mu_N + mu_S = mu_matter on every 2T row (relative)", e5b, G5_SPLIT_TOL)
    add("G5", "eps = %g: each 2T tip carries pi n/2 (relative) [prediction]" % EPS_LARGE, e5c, G5_TIP_TOL)
    e6 = []
    for (kind, lay, n, eps, a), r in graded.items():
        if kind in ("P1", "P2"):
            if ("CGR", lay, n, eps, a) in graded:
                o = graded[("CGR", lay, n, eps, a)]["crit"]["mu"]
                e6.append(abs(r["crit"]["mu"] - o) / o)
    add("G6", "background independence at BPS: P1 vs C-GR (1T), P2 vs C-GR (2T) (relative)", e6, G6_TOL)
    add("G7", "|int T_zz / int T_tt + 1| (T_zz from the full formula; T_tt = BPS-form mu)", e7, G7_TOL)
    crit_pass = all(c[5] for c in CHK)
    w("## Critical stage (kappa = 1): graded checks G1-G7 over %d graded rows (P12 optional row excluded: report-only)" % len(graded))
    w("")
    w("| id | check | worst value | tolerance | values | verdict |")
    w("|---|---|---:|---:|---:|---|")
    for c in CHK:
        w("| %s | %s | %s | %s | %d | %s |" % (c[0], c[1], c[2], c[3], c[4], pf(c[5])))
    w("")
    first_fail = next((c for c in CHK if not c[5]), None)
    w("**Critical stage: %s**%s" % (pf(crit_pass), "" if crit_pass else " (first failing check: %s, %s)" % (first_fail[0], first_fail[1])))
    w("")
    if not crit_pass:
        w("All failing critical-stage checks: %s." % "; ".join("%s %s (worst %s, tolerance %s)" % (c[0], c[1], c[2], c[3]) for c in CHK if not c[5]))
        w("")
    g4i_alt = max(e4i_v) < G4_MUI_TOL if e4i_v else False
    w("G4 mu_i breakdown [report-only; H14 flag for Venus/Helios]: vortex tips (n_i > 0) worst relative change %s over %d values; tips with no "
      "vortex (n_i = 0, the 1T S tip, where mu_i is only the exponential tail: mu_i/mu_matter from %s to %s) worst %s over %d values; "
      "max |delta mu_i|/mu_matter over all tips %s. The graded G4 row above applies 'mu_i relative 1e-8' literally to both tips. "
      "Under a vortex-tips-only reading the mu_i item would be %s, and the critical stage would be %s." % (
          fe(max(e4i_v) if e4i_v else None), len(e4i_v), fe(min(e4i_frac) if e4i_frac else None), fe(max(e4i_frac) if e4i_frac else None),
          fe(max(e4i_0) if e4i_0 else None), len(e4i_0),
          fe(max(e4i_abs) if e4i_abs else None), pf(g4i_alt),
          pf(all(c[5] for c in CHK if not (c[0] == "G4" and c[1].startswith("mu_i"))) and g4i_alt)))
    w("")
    fd1 = [r["crit"]["fd"][0] for r in graded.values()]
    fdr = [r["crit"]["fd"][0] / r["crit"]["fd"][1] for r in graded.values() if r["crit"]["fd"][1] > 0]
    w("G3 report-only: finite-difference BPS residual max|Delta_g h - (e^h - 1)| on theta in [%g, pi - %g] (%d points): max %.1e, min %.1e; "
      "ratio under step halving: min %.2f, max %.2f (O(h^2) gives about 4)." % (FD_TH[0], FD_TH[0], FD_TH[1], max(fd1), min(fd1), min(fdr), max(fdr)))
    endf = max(r["crit"]["end_f2R2"] for r in ROWS.values())
    w("Domain ends: max f^2/R^2 at t = -T_N, T_S over all rows: %.1e (the spec's rationale 'f^2 < 1e-12 R^2' for T_i = (14 + ln R)/alpha_i) [report-only]." % endf)
    arel = max(abs(r["crit"]["area_num"] - r["crit"]["area"]) / r["crit"]["area"] for r in ROWS.values())
    w("Area: numerical 2 pi int f^2 dt vs the row's area formula: max relative difference %.1e [report-only]." % arel)
    w("")

    # ---------------- per-row tables ----------------
    def tipcells(tp, R):
        if tp["n_i"] == 0:
            return ["n/a (n_i = 0)"] * 5
        if tp["s_c"] is None:
            nc_ = "NOT COMPUTED (YET): " + tp["s_c_reason"]
            return [nc_, "NOT COMPUTED (YET)", "NOT COMPUTED (YET)", "NOT COMPUTED (YET)", "NOT COMPUTED (YET)"]
        return ["%.6f" % tp["s_c"], "%.6f" % (tp["s_c"] / R), "%.6f" % (tp["s_c"] / (PI * R / 2)), "%.6f" % tp["r_c"], "%.6f" % (tp["r_c"] / R)]

    def fluxcells(tp):
        if tp["n_i"] == 0:
            return "n/a (n_i = 0)"
        return "; ".join(("%g: %.8f" % (g[0], g[2] / (2 * PI * tp["n_i"]))) if g[1] is not None else ("%g: NOT COMPUTED (YET) (s >= midpoint)" % g[0])
                         for g in tp["grid"])

    w("## Critical-stage rows (kappa = 1) [computed]")
    w("")
    w("mu in v^2 (e = v = 1); Reading I: mu_matter = T_b (brane tension at the tip, mass^4); Reading II: mu_matter = string mu (mass^2). "
      "s_c = s_c,delta (proper radius, delta = %g); r_c = f(theta_c)/alpha_i [definition: circumference match with alpha_ext := alpha_i (scanned), "
      "Part B section 1.0b; the slope is scored separately] (Venus N1-a). J and I_z are exact zeros by the ansatz, not physics findings. "
      "Flux fractions Phi_i(s)/(2 pi n_i) on the secondary grid s in %s. Stress maxima are report-only (full non-BPS-reduced formula)." % (DELTA, SC_GRID))
    w("")
    for kind in ("P0", "P1", "P2", "CGR", "P12"):
        keys = sorted([k for k in ROWS if k[0] == kind], key=lambda k: (k[1], k[2], k[3], -(k[4] if not isinstance(k[4], tuple) else k[4][0])))
        if not keys:
            continue
        w("### Row %s%s" % (rowname(kind), "  (report-only, never required for a pass)" if kind == "P12" else ""))
        w("")
        w("| layout | n | eps | alpha | R | mu_matter [Reading I: T_b; Reading II: mu] | mu/(pi n) - 1 | mu_N | mu_S | s_c(N) | s_c/R | s_c/(pi R/2) | "
          "r_c(N) | r_c/R | s_c(S) | r_c(S) | int T_zz dA | w | J | I_z | Phi_N(s)/(2 pi n_N) | Phi_S(s)/(2 pi n_S) | B_U1(s_c,N) (report-only) | max|T_rr| | max|T_phiphi|/f^2 |")
        w("|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---:|---:|")
        start = len(OUT) + 1
        for k in keys:
            r = ROWS[k]
            c = r["crit"]
            tN, tS = c["tips"]["N"], c["tips"]["S"]
            cn, cs = tipcells(tN, r["R"]), tipcells(tS, r["R"])
            w("| %s | %d | %g | %s | %.6f | %.12f | %+.2e | %.12f | %.6e | %s | %s | %s | %s | %s | %s | %s | %.12f | %.12f | %.1f (by the ansatz) | "
              "%.1f (by the ansatz) | %s | %s | %s | %.1e | %.1e |" % (
                  r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), r["R"], c["mu"], c["mu"] / (PI * r["n"]) - 1, tN["mu_i"], tS["mu_i"],
                  cn[0], cn[1], cn[2], cn[3], cn[4], cs[0], cs[3], c["tzz"], c["w"], c["J"], c["Iz"], fluxcells(tN), fluxcells(tS),
                  ("%.6e" % tN["B_sc"]) if tN.get("B_sc") is not None else "NOT COMPUTED (YET)", c["trr"], c["tpp"]))
        REF["crit_" + kind] = (start, len(OUT))
        w("")
    w("C-Stelle: **[Stelle control] NOT COMPUTED (YET)** (no Stelle background exists in our code). C-cigar: **[GR control] NOT COMPUTED (YET)** "
      "(the L1 Schwarzschild cigar is a Euclidean time-radius plane, not a transverse surface; omitted). f_theta_core: NOT COMPUTED (YET) "
      "(fixed background, rule 1). Psi = (u_flow, B, rho, p) on the matching circle: NOT COMPUTED (YET) (no MHD solve on a curved or conical "
      "background; u_flow = 0 in this static ansatz and B_U1(s_c) above are report-only, never written to Psi_rc). At kappa = 1, B_U1(s_c,delta) "
      "= delta/2 by construction of s_c,delta (Venus M-1).")
    w("")
    # prediction: Bradlow
    brad = [(k, r) for k, r in graded.items() if r["eps"] <= EPS_BRADLOW_MAX]
    brad_ok = all(r["crit"]["tips"][t]["s_c"] is None for k, r in brad for t in ("N", "S") if r["crit"]["tips"][t]["n_i"] > 0)
    big = [(k, r) for k, r in graded.items() if r["eps"] > EPS_BRADLOW_MAX]
    big_have = sum(1 for k, r in big for t in ("N", "S") if r["crit"]["tips"][t]["n_i"] > 0 and r["crit"]["tips"][t]["s_c"] is not None)
    big_tot = sum(1 for k, r in big for t in ("N", "S") if r["crit"]["tips"][t]["n_i"] > 0)

    # ---------------- consistency curve ----------------
    w("## Consistency curve G_req(alpha) = (1 - alpha)/(4 mu_matter(alpha)) at kappa = 1 [identity, exterior only; G is an output, never an input]")
    w("")
    w("Printed as G v^2 (Reading II: dimensionless G mu); under Reading I it is G_6 times a mass^4 tension. Columns: alpha. "
      "max |G_req - (1 - alpha)/(4 pi n)| over the row is the deviation from the predicted straight line. P12 has no single alpha: NOT COMPUTED (YET).")
    w("")
    w("| row | layout | n | eps | " + " | ".join("alpha = %g" % a for a in ALPHA_GRID) + " | max deviation from (1 - alpha)/(4 pi n) |")
    w("|---|---|---:|---:|" + "---:|" * len(ALPHA_GRID) + "---:|")
    start = len(OUT) + 1
    greq_dev = []
    for kind in ("P1", "P2", "CGR"):
        for (kk, lay, n, eps) in sorted({k[:4] for k in ROWS if k[0] == kind}):
            vals, devs = [], []
            for a in ALPHA_GRID:
                r = ROWS.get((kk, lay, n, eps, a))
                if r is None:                    # failed critical row (counted in C0)
                    vals.append("NOT COMPUTED (YET) (row failed)")
                    continue
                g = (1 - a) / (4 * r["crit"]["mu"])
                vals.append("%.10f" % g)
                devs.append(abs(g - (1 - a) / (4 * PI * n)))
            greq_dev.append(max(devs) if devs else float("inf"))
            w("| %s | %s | %d | %g | %s | %s |" % (rowname(kind), lay, n, eps, " | ".join(vals), fe(max(devs)) if devs else "NOT COMPUTED (YET)"))
    REF["greq"] = (start, len(OUT))
    w("")
    w("P0 rows (alpha = 1) give G_req = 0 by the formula.")
    w("")
    return report_nc(ROWS, SAMER, planes, graded, CHK, crit_pass, before, own_before, slots, T0, FAILS,
                     dict(brad_ok=brad_ok, big_have=big_have, big_tot=big_tot, greq_dev=max(greq_dev) if greq_dev else None))


def report_nc(ROWS, SAMER, planes, graded, CHK, crit_pass, before, own_before, slots, T0, FAILS, pinfo):
    PI = math.pi
    NCK = []
    NA = {}                  # check id -> number of graded entries filled as the exact normal state (tally column 'n/a (normal state)')

    def add(cid, item, vals, tol, ok=None, fmt=fe):
        worst = max(vals) if vals else None
        okv = (worst is not None and worst < tol) if ok is None else ok
        NCK.append((cid, item, fmt(worst) if worst is not None else "-", ("%g" % tol) if isinstance(tol, float) else str(tol), len(vals), okv))
        return okv

    def ns(r, kap):          # analytic normal-state entry (Helios ruling; only rows named in NORMAL_STATE_ROWS)
        return r["nc"][kap].get("normal_state", False)

    nfail_p = len(FAILS["planes"])
    add("NC0", "every flat-plane reference converged under the cap (failed planes: NOT COMPUTED (YET), counted here)",
        [float(nfail_p)], "0 failed", ok=(nfail_p == 0), fmt=lambda v: "%d of %d failed" % (nfail_p, FAILS["n_planes"]))
    n_br = 0                 # kappa paths with at least one failed entry (every chain; report-only rows included)
    for r in list(ROWS.values()) + list(SAMER.values()):
        for path in KAPPA_PATHS:
            n_br += any(isfail(r["nc"].get(k)) for k in path)
    n_br += (len(FAILS["crit"]) + sum(len(j["alphas"]) for j, _ in FAILS["failed_jobs"])) * len(KAPPA_PATHS)
    def ntip(r):
        return max(r["nN"], r["nS"])

    def ro(r, kap):          # report-only rows in stage NC
        return r["kind"] == "P12" or (kap > 1 and ntip(r) > 1)

    def nc4f(x):             # NC4 re-solve not converged (Venus N6): this entry's NC4 check fails; the path carries on
        return bool(x.get("conv") and x["conv"].get("err"))

    def nc4(r, kap):
        x = r["nc"][kap]
        cv = x["conv"]
        e_mu = max(relch(x["mu"], cv["mu2"]), relch(x["mu"], cv["mu3"]))
        e_sc = []
        for tip, k2, k3 in (("N", "sc2", "sc3"), ("S", "sc2S", "sc3S")):
            if x["tips"][tip]["n_i"] > 0:
                e_sc += [relch(x["tips"][tip]["s_c"], cv[k2]), relch(x["tips"][tip]["s_c"], cv[k3])]
        st = x["status"] == 0 and cv["status2"] == 0 and cv["status3"] == 0 and not cv.get("err")
        return e_mu, (max(e_sc) if e_sc else 0.0), st

    def nc5(r, kap):
        x = r["nc"][kap]
        return abs(x["min"]["E"] - x["mu"]) / x["mu"]

    # ---------------- plane reference ----------------
    w("## Stage NC: flat-plane reference (f = e^t, r in [%g, r_max], r_max = %g/min(1, sqrt kappa)) [computed]" % (PLANE_RMIN, PLANE_RMAX0))
    w("")
    w("| nu | " + " | ".join("E/(pi nu) at kappa = %g" % k for k in KAPPA_GRID) + " | max NC2 |E_B - E_V|/(E_B + E_V) | max NC4 rel. change | all solves converged |")
    w("|---:|" + "---:|" * len(KAPPA_GRID) + "---:|---:|---|")
    pl_nc2, pl_pw, pl_ok = [], [], True
    for nu in sorted(planes):
        rr = planes[nu]["res"]
        d2 = max(abs(rr[k]["EB"] - rr[k]["EV"]) / (rr[k]["EB"] + rr[k]["EV"]) for k in KAPPA_GRID)
        pl_nc2.append(d2)
        pl_pw += [rr[k]["pw"] / (rr[k]["E"] / (2 * PI)) for k in KAPPA_GRID]
        conv_ok = all(rr[k]["status"] == 0 and rr[k]["conv_status"] == (0, 0) for k in KAPPA_GRID)
        pl_ok &= conv_ok
        w("| %.6f | %s | %.1e | %.1e | %s |" % (nu, " | ".join("%.8f" % (rr[k]["E"] / (PI * nu)) for k in KAPPA_GRID), d2,
                                               max(rr[k]["conv"] for k in KAPPA_GRID), conv_ok))
    w("")
    # ---------------- NC1 + negative control ----------------
    e1m, e1p = [], []
    for r in graded.values():
        x = r["nc"][1.0]
        if isfail(x):                            # failed kappa = 1 row: FAILED in the tally and NC0
            continue
        e1m.append(abs(x["mu"] - r["crit"]["mu"]) / r["crit"]["mu"])
        e1p.append(x["prof_diff"])
    add("NC1", "mu(kappa = 1) equals the critical-stage mu (relative)", e1m, NC1_MU_TOL)
    add("NC1", "|phi|^2 profile at kappa = 1 equals the critical stage (absolute, on the quadrature grid)", e1p, NC1_PROF_TOL)
    # ---------------- NC2, NC3, NC4, NC5 ----------------
    e2i, e2p, e3, e4m, e4s, st4, e5 = [], [], [], [], [], True, []
    nc_rows = 0
    TALLY = {}               # (kind, layout, n, eps, alpha, kappa) -> "passed" / "FAILED: ..." / "n/a (normal state)"
    CONVF = {}               # graded entries FAILED by a non-converged solve -> "directly" / "upstream" / "NC4 re-solve" (NC0, H10)
    for r in ROWS.values():
        for kap in KAPPA_GRID:
            if ro(r, kap):
                continue
            ek = (r["kind"], r["layout"], r["n"], r["eps"], r["alpha"], kap)
            if ns(r, kap):
                NA["NC2-NC5"] = NA.get("NC2-NC5", 0) + 1
                TALLY[ek] = "n/a (normal state)"
                continue
            x = r["nc"][kap]
            if isfail(x):
                TALLY[ek] = "FAILED: " + fail_text(x)
                CONVF[ek] = x["failed"]
                continue
            nc_rows += 1
            e2i.append(abs(x["W"]) / x["S"])
            e2p.append(x["pw"] / (x["mu"] / (2 * PI)))
            e3.append(abs(x["flux"] - 2 * PI * r["n"]) / (2 * PI * r["n"]))
            a_, b_, c_ = nc4(r, kap)
            e4m.append(a_)
            e4s.append(b_)
            st4 &= c_
            e5.append(nc5(r, kap))
            bad = [cid for cid, v, t in (("NC2", e2i[-1], NC2_INT_TOL), ("NC2", e2p[-1], NC2_PW_TOL), ("NC3", e3[-1], NC3_TOL),
                                         ("NC4", a_, NC4_MU_TOL), ("NC4", b_, NC4_SC_TOL), ("NC5", e5[-1], NC5_TOL)) if not v < t]
            if not c_:
                bad.append("NC4 status")
                if nc4f(x):
                    CONVF[ek] = "NC4 re-solve"
                    bad.append("NC4 re-solve not converged (failed directly: %s)" % x["conv"]["err"])
            if kap == 1.0 and r["kind"] != "P12":
                if not abs(x["mu"] - r["crit"]["mu"]) / r["crit"]["mu"] < NC1_MU_TOL or not x["prof_diff"] < NC1_PROF_TOL:
                    bad.append("NC1")
            if r["layout"] == "2T" and not abs(x["tips"]["N"]["mu_i"] + x["tips"]["S"]["mu_i"] - x["mu"]) / x["mu"] < NC7_SPLIT_TOL:
                bad.append("NC7")
            TALLY[ek] = "passed" if not bad else "FAILED: " + ", ".join(sorted(set(bad)))
    for j, err in FAILS["failed_jobs"]:      # chain errored outside any row: every graded entry is FAILED (normal-state entries stay n/a)
        for a in j["alphas"]:
            for kap in KAPPA_GRID:
                if j["kind"] == "P12" or (kap > 1 and max(j["nN"], j["nS"]) > 1) or j.get("R_n"):
                    continue
                ek = (j["kind"], j["layout"], j["n"], j["eps"], a, kap)
                if ek in set(NORMAL_STATE_ROWS):
                    TALLY[ek] = "n/a (normal state)"
                else:
                    TALLY[ek] = "FAILED: failed directly (chain error outside a row): %s" % err
                    CONVF[ek] = "directly"
    for j, f in FAILS["crit"]:               # failed critical row: every stage-NC entry at that alpha starts from it -> failed upstream
        src_ = f["row"] if f["failed"] == "directly" else f["src"]
        for kap in KAPPA_GRID:
            if j["kind"] == "P12" or (kap > 1 and max(j["nN"], j["nS"]) > 1) or j.get("R_n"):
                continue
            ek = (j["kind"], j["layout"], j["n"], j["eps"], f["alpha"], kap)
            if ek in set(NORMAL_STATE_ROWS):
                TALLY[ek] = "n/a (normal state)"
            else:
                TALLY[ek] = "FAILED: failed upstream (row %s): %s" % (src_, f["error"])
                CONVF[ek] = "upstream"
    n_br = 0                 # kappa paths with a failed entry (every chain; report-only rows included; report-only)
    for r in list(ROWS.values()) + list(SAMER.values()):
        for path in KAPPA_PATHS:
            n_br += any(isfail(r["nc"].get(k)) for k in path)
    n_br += (len(FAILS["crit"]) + sum(len(j["alphas"]) for j, _ in FAILS["failed_jobs"])) * len(KAPPA_PATHS)
    cv_ = list(CONVF.values())
    add("NC0", "every graded stage-NC entry converged under the cap (each kappa path starts only from its alpha's kappa = 1 solution; a "
        "non-converged entry is 'failed directly' or 'failed upstream (row X)', FAILED in the tally, never dropped) (H10)",
        [float(len(cv_))], "0 failed", ok=(not cv_),
        fmt=lambda v: "%d of %d graded entries (%d failed directly, %d upstream, %d NC4 re-solve); %d of %d kappa paths broken (all chains)" % (
            len(cv_), len(TALLY), cv_.count("directly"), cv_.count("upstream"), cv_.count("NC4 re-solve"), n_br, FAILS["n_paths"]))
    NCK.insert(1, NCK.pop())
    add("NC2", "weighted virial: |int (ln f)'(e_B - e_V) dA| / int (e_B + e_V) dA (every graded row and kappa)", e2i, NC2_INT_TOL)
    add("NC2", "pointwise: max_t |H(t) - H(-T_N) - int RHS| / (mu/2 pi)", e2p, NC2_PW_TOL)
    add("NC2", "flat reference (weight 1): |E_B - E_V|/(E_B + E_V), every nu and kappa", pl_nc2, NC2_INT_TOL)
    add("NC2", "flat reference pointwise / (E/2 pi)", pl_pw, NC2_PW_TOL)
    add("NC3", "flux = 2 pi n (relative)", e3, NC3_TOL)
    add("NC4", "mu relative change (2 x nodes; 1.5 x T_i); all solves converged", e4m, NC4_MU_TOL, ok=(bool(e4m) and max(e4m) < NC4_MU_TOL and st4 and pl_ok))
    add("NC4", "s_c,delta relative change at vortex tips", e4s, NC4_SC_TOL)
    add("NC5", "BVP vs direct minimisation (L-BFGS, Richardson) |E_min - mu|/mu", e5, NC5_TOL)
    # ---------------- NC6 ----------------
    w("## Stage NC: NC6 type I/II sign check (plane and P0 at eps = %g)" % EPS_LARGE)
    w("")
    w("Note (Venus N1-b): on P0 the two sides of E_2 vs 2E_1 sit on spheres of different R (A = 4 pi n (1 + eps) depends on n: R^2 = %g vs %g); "
      "the ~4%% margin far exceeds the finite-size shift (<= 3e-3) (Venus's figures, quoted; the margins computed here are in the table)." % (2 * (1 + EPS_LARGE), 1 + EPS_LARGE))
    w("")
    w("| background | kappa | E_1/pi | expected | margin |E_1/pi - 1| | (E_2 - 2E_1)/(2E_1) | expected sign | margin | 10 x NC4 error | verdict |")
    w("|---|---:|---:|---|---:|---:|---|---:|---:|---|")
    nc6_ok = True
    for bg in ("plane", "P0"):
        for kap in KAPPA_GRID:
            if kap == 1.0:
                continue
            if bg == "plane":
                if 1.0 not in planes or 2.0 not in planes:
                    nc6_ok = False
                    w("| flat plane | %g | NOT COMPUTED (YET) (plane failed) | | | | | | | FAIL |" % kap)
                    continue
                E1, E2 = planes[1.0]["res"][kap]["E"], planes[2.0]["res"][kap]["E"]
                err = max(planes[1.0]["res"][kap]["conv"], planes[2.0]["res"][kap]["conv"])
            else:
                r1, r2 = ROWS.get(("P0", "1T", 1, EPS_LARGE, 1.0)), ROWS.get(("P0", "1T", 2, EPS_LARGE, 1.0))
                if r1 is None or r2 is None or isfail(r1["nc"][kap]) or isfail(r2["nc"][kap]):
                    nc6_ok = False
                    w("| P0 eps = %g | %g | NOT COMPUTED (YET) (row failed) | | | | | | | FAIL |" % (EPS_LARGE, kap))
                    continue
                E1, E2 = r1["nc"][kap]["mu"], r2["nc"][kap]["mu"]
                err = max(nc4(r1, kap)[0], nc4(r2, kap)[0])
            x1 = E1 / PI - 1
            x2 = (E2 - 2 * E1) / (2 * E1)
            sgn = -1 if kap < 1 else 1
            ok = (sgn * x1 > NC6_MARGIN_FAC * err) and (sgn * x2 > NC6_MARGIN_FAC * err)
            nc6_ok &= ok
            w("| %s | %g | %.8f | %s 1 | %.2e | %+.4e | %s | %.2e | %.1e | %s |" % (
                "flat plane" if bg == "plane" else "P0 eps = %g (1T n = 1 and 2; different R)" % EPS_LARGE, kap, E1 / PI,
                "<" if sgn < 0 else ">", abs(x1), x2, "negative" if sgn < 0 else "positive", abs(x2), NC6_MARGIN_FAC * err, pf(ok)))
    w("")
    add("NC6", "type I/II signs with margin > 10 x NC4 error (plane and P0 eps = %g)" % EPS_LARGE, [0.0 if nc6_ok else 1.0], 0.5, ok=nc6_ok,
        fmt=lambda v: "all signs as stated" if nc6_ok else "a sign or margin failed")
    # ---------------- NC7 ----------------
    e7a = []
    for r in ROWS.values():
        if r["layout"] != "2T":
            continue
        for kap in KAPPA_GRID:
            if ro(r, kap) or ns(r, kap) or isfail(r["nc"][kap]):
                continue
            x = r["nc"][kap]
            e7a.append(abs(x["tips"]["N"]["mu_i"] + x["tips"]["S"]["mu_i"] - x["mu"]) / x["mu"])
    add("NC7", "mu_N + mu_S = mu_matter on every graded 2T row (relative)", e7a, NC7_SPLIT_TOL)
    w("## Stage NC: NC7 second item, C-GR eps = %g: mu(2T, n) vs 2 mu(1T, n/2)" % EPS_LARGE)
    w("")
    w("Graded only when both sides use the same R (the 1T n/2 row solved on the 2T row's sphere); rows with n_tip > 1 at kappa > 1 are report-only. "
      "The default-grid comparison (different spheres) is report-only.")
    w("")
    w("| n | alpha | kappa | mu(2T, n) | 2 mu(1T, n/2), same R | rel. diff (same R) | graded? | 2 mu(1T, n/2), default grid (different R) | rel. diff (report-only) |")
    w("|---:|---:|---:|---:|---:|---:|---|---:|---:|")
    e7b = []
    for n in N_2T:
        for a in ALPHA_GRID:
            r2 = ROWS.get(("CGR", "2T", n, EPS_LARGE, a))
            rs = SAMER.get(("CGR", "1T-sameR", n // 2, EPS_LARGE, a))
            rd = ROWS.get(("CGR", "1T", n // 2, EPS_LARGE, a))
            if r2 is None or rs is None:         # failed chain (counted in C0): the graded same-R item cannot pass
                e7b.append(float("inf"))
                w("| %d | %g | all | NOT COMPUTED (YET) (row failed) | | | | | |" % (n, a))
                continue
            for kap in KAPPA_GRID:
                if isfail(r2["nc"][kap]) or isfail(rs["nc"][kap]):
                    if not (kap > 1 and n // 2 > 1):
                        e7b.append(float("inf"))
                    w("| %d | %g | %g | NOT COMPUTED (YET) (row failed) | | | | | |" % (n, a, kap))
                    continue
                m2 = r2["nc"][kap]["mu"]
                ms = 2 * rs["nc"][kap]["mu"]
                gr = not (kap > 1 and n // 2 > 1)
                dv = abs(m2 - ms) / m2
                if gr:
                    e7b.append(dv)
                md = 2 * rd["nc"][kap]["mu"] if (rd and not isfail(rd["nc"][kap])) else None
                w("| %d | %g | %g | %.10f | %.10f | %.2e | %s | %s | %s |" % (n, a, kap, m2, ms, dv, "yes" if gr else "report-only (n_tip > 1, kappa > 1)",
                                                                       fv(md), fe(abs(m2 - md) / m2 if md else None)))
    w("")
    add("NC7", "same-R mu(2T, n) = 2 mu(1T, n/2) on C-GR eps = %g (relative) [prediction]" % EPS_LARGE, e7b, NC7_SAME_R_TOL)
    # ---------------- background dependence ----------------
    groups = sorted({(k[0], k[1], k[2], k[3]) for k in ROWS if k[0] in ("P1", "P2", "CGR")})
    BG = {}
    for (kind, lay, n, eps) in groups:
        for kap in KAPPA_GRID:
            rs_ = [ROWS.get((kind, lay, n, eps, a)) for a in ALPHA_GRID]
            r0 = next(r for r in rs_ if r is not None)
            ok_ = [r for r in rs_ if r is not None and not isfail(r["nc"][kap]) and not nc4f(r["nc"][kap])]
            nfg = len(ok_) < len(rs_)            # a member row failed (FAILED in the tally): Delta_bg NOT COMPUTED (YET)
            nsg = any(ns(r, kap) for r in ok_)
            mus = [r["nc"][kap]["mu"] for r in rs_] if (not nfg and not nsg) else []
            dbg = max(abs(m - mus[0]) / mus[0] for m in mus) if mus else None
            enum = max([max(nc4(r, kap)[0], nc5(r, kap)) for r in ok_ if not ns(r, kap)] or [0.0])
            thr = max(BG_FLOOR, BG_NUM_FAC * enum)
            scs = [r["nc"][kap]["tips"]["N"]["s_c"] if r in ok_ else None for r in rs_]
            have = [s for s in scs if s is not None]
            nc4sc = max([nc4(r, kap)[1] for r in ok_ if not ns(r, kap)] or [0.0])
            if len(have) >= 2:
                ref = scs[0] if scs[0] is not None else min(have)
                chg = (max(have) - min(have)) / ref
                thrp = max(PROF_FLOOR, PROF_NUM_FAC * nc4sc)
                fprof = chg > thrp
            else:
                chg, thrp, fprof = None, max(PROF_FLOOR, PROF_NUM_FAC * nc4sc), None
            BG[(kind, lay, n, eps, kap)] = dict(dbg=dbg, enum=enum, thr=thr, fmu=None if (nfg and not nsg) else ((dbg is not None and dbg > thr) and not nsg),
                                                chg=chg, thrp=thrp, fprof=fprof, nsg=nsg, nfg=nfg,
                                                nhave=len(have), ro=(kap > 1 and max(r0["nN"], r0["nS"]) > 1))
    neg_mu = all(v["fmu"] is False for k, v in BG.items() if k[4] == 1.0)
    neg_prof = all(v["fprof"] is not True for k, v in BG.items() if k[4] == 1.0)
    neg_ok = neg_mu and neg_prof
    reasons = []
    if any(v["fmu"] is None for k, v in BG.items() if k[4] == 1.0):
        reasons.append("negative control FAIL: not evaluable at kappa = 1 (a group has a failed row; Delta_bg NOT COMPUTED (YET))")
    if any(v["fmu"] for k, v in BG.items() if k[4] == 1.0):
        reasons.append("negative control FAIL: mu background-dependent at kappa = 1")
    if not neg_prof:
        reasons.append("negative control FAIL: profile (s_c,delta) background-dependent at kappa = 1")
    add("NC1-neg", "negative control at kappa = 1: mu flag AND profile flag both 'no' (spec 3b, literal)", [0.0 if neg_ok else 1.0], 0.5, ok=neg_ok,
        fmt=lambda v: "both no" if neg_ok else "; ".join(reasons))
    nc_pass = crit_pass and all(c[5] for c in NCK)
    first = next((c for c in NCK if not c[5]), None)
    if nc_pass:
        nc_reason = "stage NC PASS"
    elif not crit_pass:
        nc_reason = "stage NC FAIL: critical stage failed; no stage-NC value is used"
    elif first[0] == "NC1-neg":
        nc_reason = "; ".join(reasons) + "; critical-stage values stand"
    else:
        nc_reason = "stage NC FAIL: %s; critical-stage values stand" % first[0]
    w("## Stage NC: graded checks NC1-NC7 (%d computed graded row x kappa entries; P12 and n_tip > 1 at kappa > 1 are report-only)" % nc_rows)
    w("")
    w("| id | check | worst value | tolerance | values | n/a (normal state) | verdict |")
    w("|---|---|---:|---:|---:|---:|---|")
    for c in NCK:
        w("| %s | %s | %s | %s | %d | %d | %s |" % (c[0], c[1], c[2], c[3], c[4], NA.get("NC2-NC5", 0) if c[0] in ("NC2", "NC3", "NC4", "NC5") and
                                                    not c[1].startswith("flat") else 0, pf(c[5])))
    w("")
    t_pass = sum(1 for v in TALLY.values() if v == "passed")
    t_fail = sum(1 for v in TALLY.values() if v.startswith("FAILED"))
    t_na = sum(1 for v in TALLY.values() if v.startswith("n/a"))
    w("**Stage-NC row tally** (graded row x kappa entries; P12 and n_tip > 1 at kappa > 1 are report-only and not counted):")
    w("")
    w("| passed | FAILED (incl. not converged (cap hit)) | n/a (normal state) | total |")
    w("|---:|---:|---:|---:|")
    w("| %d | %d | %d | %d |" % (t_pass, t_fail, t_na, len(TALLY)))
    w("")
    fl = sorted((k, v) for k, v in TALLY.items() if v.startswith("FAILED"))
    if fl:
        w("FAILED entries: %s." % "; ".join("%s %s n=%d eps=%g alpha=%s kappa=%g: %s" % (rowname(k[0]), k[1], k[2], k[3], lab_alpha(k[4]), k[5], v[8:])
                                            for k, v in fl))
        w("")
    if NORMAL_STATE_ROWS:
        w("")
        w("Rows filled as the exact normal state %s (no BVP call; named in the revised spec): %d graded row x kappa entries; "
          "their Delta_bg counts as neither pass nor fail." % (NORMAL_STATE_TAG, NA.get("NC2-NC5", 0)))
    w("")
    w("**Stage NC: %s** (%s)" % (pf(nc_pass), nc_reason))
    w("")
    w("Report-only, not graded (H14 flag for Venus/Helios): at kappa = 1 the mu flag alone is %s ('%s'); the profile flag at kappa = 1 is 'yes' in %d "
      "of %d groups where s_c,delta exists at two or more alpha. The spec's rationale '(mu is topological)' covers mu only; the core profile "
      "(s_c,delta) changes with the tip angle even at BPS, so a literal 'both no' negative control cannot pass on these grids. "
      "Under a mu-only negative control, stage NC would be %s by the other checks." % (
          "no" if neg_mu else "yes or NOT COMPUTED (YET)", "negative control mu-part PASS" if neg_mu else "mu background-dependent or not evaluable at kappa = 1",
          sum(1 for k, v in BG.items() if k[4] == 1.0 and v["fprof"] is True), sum(1 for k, v in BG.items() if k[4] == 1.0 and v["fprof"] is not None),
          pf(crit_pass and neg_mu and all(c[5] for c in NCK if c[0] != "NC1-neg"))))
    w("")
    bvpn = lambda r, kap: (not isfail(r["nc"][kap])) and (not ns(r, kap)) and r["nc"][kap]["ph2max"] < 1e-6
    norm = sorted({(r["eps"], kap) for r in ROWS.values() for kap in KAPPA_GRID if bvpn(r, kap)})
    nn = sum(1 for r in ROWS.values() for kap in KAPPA_GRID if bvpn(r, kap))
    nfill = sum(1 for r in ROWS.values() for kap in KAPPA_GRID if not isfail(r["nc"][kap]) and ns(r, kap))
    w("Normal state, BVP-solved entries [computed; report-only observation]: %d row x kappa entries solved by the BVP (not filled) have "
      "max|phi|^2 < 1e-6, i.e. the BVP converged to the normal state phi = 0 with uniform B = 2 pi n/A, energy (2 pi n)^2/(2A) + kappa A/8 "
      "(area only). (eps, kappa) pairs: %s; B = 1/(2(1 + eps)) vs kappa/2 per pair: %s." % (
          nn, ", ".join("(%g, %g)" % x for x in norm) if norm else "none",
          ", ".join("(%g, %g): %.4f vs %.4f" % (e, k, 1 / (2 * (1 + e)), k / 2) for e, k in norm) if norm else "-"))
    w("Normal state, filled entries [not computed; by construction; not a test]: %d row x kappa entries named in spec C9683FDD 3b are filled "
      "with the exact normal state %s. Spec 3b [identity]: on any smooth tipless metric on S^2 the normal state is linearly unstable iff "
      "B < kappa/2 and marginal at B = kappa/2 (n + 1 zero modes); whether a vortex branch coexists (kappa < 1, subcritical) is NOT COMPUTED (YET). "
      "For cone-tip rows the branch point is [open] and no stability statement is made here." % (nfill, NORMAL_STATE_TAG))
    w("")
    w("### Background-dependence test (Delta_bg over the alpha grid at fixed eps; R changes with alpha, so finite-size curvature is included)")
    w("")
    w("| row | layout | n | eps | kappa | Delta_bg | e_num | threshold max(1e-6, 100 e_num) | mu depends on the background | s_c,delta change | "
      "threshold | profile depends | report-only |")
    w("|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---|---|")
    start = len(OUT) + 1
    for k in sorted(BG):
        v = BG[k]
        w("| %s | %s | %d | %g | %g | %s | %s | %.1e | %s | %s | %.1e | %s | %s |" % (
            rowname(k[0]), k[1], k[2], k[3], k[4], "NOT COMPUTED (YET) (alpha = 1 member is the normal state)" if v["nsg"] else
            ("NOT COMPUTED (YET) (a row in the group failed)" if v["dbg"] is None else "%.3e" % v["dbg"]),
            "%.1e" % v["enum"], v["thr"],
            "n/a (normal state)" if v["nsg"] else ("NOT COMPUTED (YET) (row failed)" if v["fmu"] is None else ("yes" if v["fmu"] else "no")), fe(v["chg"]), v["thrp"],
            "NOT COMPUTED (YET) (s_c,delta at < 2 alpha)" if v["fprof"] is None else ("yes" if v["fprof"] else "no"),
            "yes (n_tip > 1, kappa > 1)" if v["ro"] else "no"))
    REF["bg"] = (start, len(OUT))
    w("")
    # ---------------- mu(kappa) tables with the exact-cone row ----------------
    w("### mu_matter(kappa)/(pi n) per row [axisymmetric critical point; stability NOT COMPUTED (YET)]; Reading I: T_b; Reading II: string mu")
    w("")
    w("Exact-cone prediction row (report-only): mu_cone/(pi n) = alpha E^plane_{nu = n/alpha}(kappa)/(pi n), printed under each P1 group. "
      "Entries marked * are report-only (n_tip > 1 at kappa > 1, or P12).")
    w("")
    w("| row | layout | n | eps | kappa | " + " | ".join("alpha = %g" % a for a in ALPHA_GRID) + " |")
    w("|---|---|---:|---:|---:|" + "---:|" * len(ALPHA_GRID))
    start = len(OUT) + 1
    for (kind, lay, n, eps) in groups:
        for kap in KAPPA_GRID:
            cells = []
            for a in ALPHA_GRID:
                r = ROWS.get((kind, lay, n, eps, a))
                if r is None:
                    cells.append("NOT COMPUTED (YET) (critical row failed)")
                elif isfail(r["nc"][kap]):
                    cells.append("NOT COMPUTED (YET) (failed %s)" % r["nc"][kap]["failed"])
                elif ns(r, kap):
                    cells.append("NOT COMPUTED (YET) (vortex); n/a (normal state; its energy/(pi n) = %.8f, not a vortex value) %s%s" % (
                        r["nc"][kap]["mu"] / (PI * n), NORMAL_STATE_TAG, (" " + NORMAL_STATE_ZERO_MODES) if 1 / (2 * (1 + eps)) == kap / 2 else ""))
                else:
                    cells.append("%.8f%s" % (r["nc"][kap]["mu"] / (PI * n), "*" if ro(r, kap) else ""))
            w("| %s | %s | %d | %g | %g | %s |" % (rowname(kind), lay, n, eps, kap, " | ".join(cells)))
        if kind == "P1":
            for kap in KAPPA_GRID:
                cells = []
                for a in ALPHA_GRID:
                    nu = round(n / a, 12)
                    cells.append(("%.8f" % (a * planes[nu]["res"][kap]["E"] / (PI * n))) if nu in planes else "NOT COMPUTED (YET) (plane failed)")
                w("| exact cone (report-only) | 1T | %d | infinite | %g | %s |" % (n, kap, " | ".join(cells)))
    for k in sorted(k for k in ROWS if k[0] in ("P0", "P12")):
        r = ROWS[k]
        w("| %s | %s | %d | %g | alpha %s | %s |" % (rowname(k[0]), k[1], k[2], k[3], lab_alpha(k[4]),
                                                   "; ".join(("kappa %g: NOT COMPUTED (YET) (failed %s)" % (kap, r["nc"][kap]["failed"])) if isfail(r["nc"][kap]) else
                                                             ("kappa %g: NOT COMPUTED (YET) (vortex); n/a (normal state; its energy/(pi n) = %.8f, not a vortex value) %s" % (kap, r["nc"][kap]["mu"] / (PI * k[2]), NORMAL_STATE_TAG))
                                                             if ns(r, kap) else ("kappa %g: %.8f%s" % (kap, r["nc"][kap]["mu"] / (PI * k[2]), "*" if ro(r, kap) else ""))
                                                             for kap in KAPPA_GRID)))
    REF["nc_mu"] = (start, len(OUT))
    w("")
    cone_dev = []
    for k, r in ROWS.items():
        if k[0] == "P1" and k[3] == EPS_LARGE:
            nu = round(k[2] / k[4], 12)
            for kap in KAPPA_GRID:
                if nu not in planes or isfail(r["nc"][kap]):
                    continue
                mc = k[4] * planes[nu]["res"][kap]["E"]
                cone_dev.append(abs(r["nc"][kap]["mu"] - mc) / mc)
    cdev = max(cone_dev) if cone_dev else None
    w("P1 at eps = %g vs the exact-cone prediction: max relative difference %s over all n, alpha, kappa [report-only]." % (EPS_LARGE, fe(cdev)))
    w("")
    return finish(ROWS, SAMER, planes, graded, CHK, NCK, crit_pass, nc_pass, nc_reason, BG, before, own_before, slots, T0, pinfo,
                  dict(neg_mu=neg_mu, cone_dev=cdev, fails=FAILS))


def code_names_clean():
    import io
    import tokenize
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    bad = set()
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.NAME and (tok.string in ("chi", "lambda_in") or tok.string.startswith("eta_")):
            bad.add(tok.string)
    return sorted(bad)


def csv_text(header, rows):
    import io
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator="\n")
    wr.writerow(header)
    for r in rows:
        wr.writerow(r)
    return buf.getvalue()


def g12(x):
    return "NOT COMPUTED (YET)" if x is None else "%.12g" % x


def finish(ROWS, SAMER, planes, graded, CHK, NCK, crit_pass, nc_pass, nc_reason, BG, before, own_before, slots, T0, pinfo, ninfo):
    PI = math.pi
    files = {}
    # ---------------- CSVs ----------------
    prow = []
    for k in sorted(ROWS, key=str):
        r = ROWS[k]
        th, d, ph2, B, em = r["crit"]["profile"]
        for j in range(th.size):
            prow.append([r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), "%.10f" % th[j], "%.10f" % d[j], "%.12e" % ph2[j],
                         "%.12e" % B[j], "%.12e" % em[j]])
    files["profiles.csv"] = csv_text(["row", "layout", "n", "eps", "alpha", "theta", "d_from_N", "phi2", "B", "eps_m"], prow)
    trow = []
    for k in sorted(ROWS, key=str):
        r = ROWS[k]
        for tip in ("N", "S"):
            tp = r["crit"]["tips"][tip]
            frac = (lambda ph: ("%.12g" % (ph / (2 * PI * tp["n_i"]))) if (ph is not None and tp["n_i"] > 0) else ("n/a (n_i = 0)" if tp["n_i"] == 0 else "NOT COMPUTED (YET)"))
            for g in tp["grid"]:
                trow.append([r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), 1.0, tip, tp["n_i"], "%.12g" % tp["mu_i"],
                             "%g" % g[0], "secondary grid", g12(g[1]), g12(g[2]), frac(g[2]) if g[1] is not None else "NOT COMPUTED (YET) (s >= midpoint)"])
            if tp["s_c"] is not None:
                trow.append([r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), 1.0, tip, tp["n_i"], "%.12g" % tp["mu_i"],
                             "%.10g" % tp["s_c"], "s_c,delta (report-only extra)", g12(tp["mu_sc"]), g12(tp["phi_sc"]), frac(tp["phi_sc"])])
    files["per_tip.csv"] = csv_text(["row", "layout", "n", "eps", "alpha", "kappa", "tip", "n_i", "mu_i", "s", "s_kind", "mu_i(s)", "Phi_i(s)",
                                     "Phi_i(s)/(2 pi n_i)"], trow)
    crow = []
    for k in sorted(ROWS, key=str):
        r = ROWS[k]
        for kap in KAPPA_GRID:
            if kap != 1.0 and isfail(r["nc"][kap]):
                for rd in ("II: G v^2 (dimensionless G mu)", "I: G_6 x T_b (T_b in mass^4)"):
                    crow.append([r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), kap, rd, "NOT COMPUTED (YET)", "NOT COMPUTED (YET)",
                                 "FAILED: " + fail_text(r["nc"][kap])])
                continue
            mu = r["crit"]["mu"] if kap == 1.0 else r["nc"][kap]["mu"]
            if kap != 1.0 and r["nc"][kap].get("normal_state"):     # never fed as the vortex solution
                for rd in ("II: G v^2 (dimensionless G mu)", "I: G_6 x T_b (T_b in mass^4)"):
                    crow.append([r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), kap, rd, "NOT COMPUTED (YET)", "NOT COMPUTED (YET)",
                                 "n/a (normal state) %s; normal-state energy (not a vortex value) = %.12g" % (NORMAL_STATE_TAG, mu)])
                continue
            if kap == 1.0:
                st = "critical stage %s" % pf(crit_pass)
            else:
                st = ("stage NC PASS" if nc_pass else "report-only (%s)" % nc_reason)
                if r["kind"] == "P12" or (kap > 1 and max(r["nN"], r["nS"]) > 1):
                    st += "; report-only row"
                st += "; axisymmetric critical point; stability NOT COMPUTED (YET)"
            g = "NOT COMPUTED (YET) (unequal tips: no single alpha)" if r["kind"] == "P12" else "%.12g" % ((1 - r["alpha"]) / (4 * mu))
            for rd in ("II: G v^2 (dimensionless G mu)", "I: G_6 x T_b (T_b in mass^4)"):
                crow.append([r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), kap, rd, "%.12g" % mu, g, st])
    for j, f in ninfo["fails"]["crit"]:       # failed critical rows: listed, never dropped
        for kap in KAPPA_GRID:
            for rd in ("II: G v^2 (dimensionless G mu)", "I: G_6 x T_b (T_b in mass^4)"):
                crow.append([j["kind"], j["layout"], j["n"], j["eps"], lab_alpha(f["alpha"]), kap, rd, "NOT COMPUTED (YET)", "NOT COMPUTED (YET)",
                             "FAILED: critical row %s" % fail_text(f)])
    files["consistency_curve.csv"] = csv_text(["row", "layout", "n", "eps", "alpha", "kappa", "reading", "mu_matter", "G_req", "status"], crow)
    nrow = []
    NHDR = ["row", "layout", "n", "eps", "alpha", "kappa", "mu_matter", "mu_N", "mu_S", "s_c_N", "r_c_N", "s_c_S", "r_c_S",
            "w", "NC2_integral_residual", "NC2_pointwise_ratio", "piH_tc_N", "piH_tc_S", "NC3_flux_rel", "NC4_mu_rel",
            "NC4_s_c_rel", "NC5_rel", "NC5_LBFGS_iterations", "max_T_rr", "max_T_phiphi_over_f2", "max_phi2", "Delta_bg", "e_num",
            "mu_depends_on_background", "profile_depends_on_background", "exact_cone_mu", "report_only", "tag"]
    for k in sorted(ROWS, key=str):
        r = ROWS[k]
        for kap in KAPPA_GRID:
            x = r["nc"][kap]
            if isfail(x):                        # failed row: listed with no values
                nrow.append([r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), kap] + ["NOT COMPUTED (YET)"] * (len(NHDR) - 8) +
                            ["FAILED", "FAILED: " + fail_text(x)])
                continue
            if x.get("normal_state"):            # exact normal state: no vortex-derived quantity is written
                NCY_ = "NOT COMPUTED (YET)"
                nrow.append([r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), kap, NCY_] + [NCY_] * 6 +
                            [NCY_] + ["n/a (normal state)"] * 2 + [NCY_] * 2 + ["n/a (normal state)"] +
                            ["n/a (normal state)"] * 4 + ["%.3e" % x["trr"], "%.3e" % x["tpp"], "%.6e" % x["ph2max"]] +
                            ["n/a (normal state)"] * 4 + ["n/a", "n/a (normal state)",
                                                          "%s; normal-state energy (not a vortex value) = %.12g" % (NORMAL_STATE_TAG, x["mu"])])
                continue
            cv = x["conv"]
            e4 = max(relch(x["mu"], cv["mu2"]), relch(x["mu"], cv["mu3"]))
            e4s = max(relch(x["tips"]["N"]["s_c"], cv["sc2"]), relch(x["tips"]["N"]["s_c"], cv["sc3"]))
            e4t = ("NOT COMPUTED (YET) (NC4 re-solve not converged: FAILED)", "NOT COMPUTED (YET) (NC4 re-solve not converged: FAILED)") if cv.get("err") \
                else ("%.3e" % e4, "%.3e" % e4s)
            bgk = (r["kind"], r["layout"], r["n"], r["eps"], kap)
            bg = BG.get(bgk)
            cone = None
            if r["kind"] == "P1" and round(r["n"] / r["alpha"], 12) in planes:
                cone = r["alpha"] * planes[round(r["n"] / r["alpha"], 12)]["res"][kap]["E"]
            rmk = []
            if r["kind"] == "P12":
                rmk.append("report-only (optional P12)")
            if kap > 1 and max(r["nN"], r["nS"]) > 1:
                rmk.append("report-only (n_tip > 1 at kappa > 1)")
            tN, tS = x["tips"]["N"], x["tips"]["S"]
            nrow.append([r["kind"], r["layout"], r["n"], r["eps"], lab_alpha(r["alpha"]), kap, "%.12g" % x["mu"], "%.12g" % tN["mu_i"], "%.12g" % tS["mu_i"],
                         g12(tN["s_c"]) if tN["n_i"] else "n/a", g12(tN.get("r_c")) if tN["n_i"] else "n/a",
                         g12(tS["s_c"]) if tS["n_i"] else "n/a", g12(tS.get("r_c")) if tS["n_i"] else "n/a",
                         "%.12g" % x["w"], "%.3e" % (abs(x["W"]) / x["S"]), "%.3e" % (x["pw"] / (x["mu"] / (2 * PI))),
                         g12(tN.get("piH_tc")) if tN["n_i"] else "n/a", g12(tS.get("piH_tc")) if tS["n_i"] else "n/a",
                         "%.3e" % (abs(x["flux"] - 2 * PI * r["n"]) / (2 * PI * r["n"])), e4t[0], e4t[1],
                         "%.3e" % (abs(x["min"]["E"] - x["mu"]) / x["mu"]), ";".join("h=%g:nit=%d" % (i[0], i[2]) for i in x["min"]["info"]),
                         "%.3e" % x["trr"], "%.3e" % x["tpp"],
                         "%.6e" % x["ph2max"], ("NOT COMPUTED (YET)" if (bg["nsg"] or bg["dbg"] is None) else "%.3e" % bg["dbg"]) if bg else "n/a",
                         ("%.3e" % bg["enum"]) if bg else "n/a",
                         ("n/a (set has a normal-state row)" if bg["nsg"] else ("NOT COMPUTED (YET)" if bg["fmu"] is None else ("yes" if bg["fmu"] else "no"))) if bg else "n/a",
                         ("NOT COMPUTED (YET)" if bg["fprof"] is None else ("yes" if bg["fprof"] else "no")) if bg else "n/a",
                         g12(cone) if cone is not None else "n/a", "; ".join(rmk) if rmk else "graded",
                         "[axisymmetric critical point; stability NOT COMPUTED (YET)]"])
    for j, f in ninfo["fails"]["crit"]:       # failed critical rows: listed, never dropped
        for kap in KAPPA_GRID:
            nrow.append([j["kind"], j["layout"], j["n"], j["eps"], lab_alpha(f["alpha"]), kap] + ["NOT COMPUTED (YET)"] * (len(NHDR) - 8) +
                        ["FAILED", "FAILED: upstream of critical row %s" % fail_text(f)])
    files["nc_scan.csv"] = csv_text(NHDR, nrow)
    # ---------------- filled table ----------------
    def ref(key):
        a, b = REF[key]
        return "[hive-run: SM1-INPUTS-RUN, RESULTS.md, %d-%d]" % (a, b)

    crit_refs = ", ".join("%d-%d" % REF["crit_" + k] for k in ("P0", "P1", "P2", "CGR") if "crit_" + k in REF)
    tagc = "[hive-run: SM1-INPUTS-RUN, RESULTS.md, %s]" % crit_refs
    fill = ["# SM1_INPUTS_FILLED.md (generated by SM1-INPUTS-RUN run.py; do not edit by hand)", "",
            "Same slots as SM1_INPUTS.md E0D7D41D, Part A spec 0.2 line format. The run does not edit SM1_INPUTS.md; after Venus and Helios sign off, "
            "the parent copies rows across. No Part B verdict is written here. Part B (6611EE3B) stays HELD. Parser caveat (SM1_INPUTS.md line 5): "
            "Part A only reads alpha_ext tagged [Akitti: ...]; nothing here changes a Part A run.", "",
            "Critical stage: %s. Stage NC: %s (%s)." % (pf(crit_pass), pf(nc_pass), nc_reason), "", "```"]
    NCY = "NOT COMPUTED (YET)"
    if crit_pass:
        mus = [abs(r["crit"]["mu"] / (PI * r["n"]) - 1) for r in graded.values()]
        g4 = max(max(relch(r["crit"]["mu"], r["crit"]["mu_q"]), relch(r["crit"]["mu"], r["crit"]["mu_T"])) for r in graded.values())
        scr = [(r["crit"]["tips"][t]["s_c"], r["crit"]["tips"][t]["r_c"], r["R"]) for r in graded.values() for t in ("N", "S")
               if r["crit"]["tips"][t]["n_i"] > 0 and r["crit"]["tips"][t]["s_c"] is not None]
        ws = max(abs(r["crit"]["w"] + 1) for r in graded.values())
        kap_note = ("kappa != 1 values: RESULTS.md lines %d-%d [axisymmetric critical point; stability NOT COMPUTED (YET)]; rows with n_tip > 1 at kappa > 1 "
                    "are never written%s" % (REF["nc_mu"] + (("; entries marked 'n/a (normal state)' are not vortex values and feed no slot",)
                                                              if NORMAL_STATE_ROWS else ("",)))) if nc_pass else "kappa != 1: NOT COMPUTED (YET) (%s)" % nc_reason
        val = {
            "mu": "pi n at kappa = 1 on every graded row: max |mu/(pi n) - 1| = %.1e over %d rows (per row, layout, n, eps, alpha in the tables); %s; "
                  "units v^2, e = v = 1; Reading I: T_b (brane tension, mass^4); Reading II: string mu (mass^2); matter side only; which n and kappa "
                  "apply is for Part B %s" % (max(mus), len(mus), kap_note, tagc),
            "sigma_mu": "numerical only (G4): max relative change %.1e; the physical uncertainty is NOT COMPUTED (YET) %s" % (g4, tagc),
            "r_c": "r_c = f(theta_c)/alpha_i per vortex tip where s_c,delta exists (%d tips; range %.6f-%.6f); otherwise NOT COMPUTED (YET) "
                   "[definition: circumference match with alpha_ext := alpha_i (scanned), Part B section 1.0b; the slope is scored separately]; "
                   "never a copy of s_c %s" % (len(scr), min(x[1] for x in scr), max(x[1] for x in scr), tagc) if scr else NCY + " (no s_c,delta on any row) " + tagc,
            "r_c/R": "same rows: range %.6f-%.6f %s" % (min(x[1] / x[2] for x in scr), max(x[1] / x[2] for x in scr), tagc) if scr else NCY + " " + tagc,
            "s_c": "s_c,delta (proper radius, delta = %g) per vortex tip where it exists (%d tips; range %.6f-%.6f); otherwise NOT COMPUTED (YET) "
                   "with the printed reason %s" % (DELTA, len(scr), min(x[0] for x in scr), max(x[0] for x in scr), tagc) if scr else NCY + " " + tagc,
            "s_c/R": "same rows: range %.6f-%.6f %s" % (min(x[0] / x[2] for x in scr), max(x[0] / x[2] for x in scr), tagc) if scr else NCY + " " + tagc,
            "T_b": "T_b := mu_matter per tip (mu_N, mu_S columns) [identity for these rows: w = -1 exactly, so tension = energy per unit worldvolume; "
                   "fixed background, matter side only; Venus Q3]; Reading I: brane tension (6D units); Reading II: string mu; never filled from alpha; "
                   "not a back-reacted gravitating source %s" % tagc,
            "gauge_norm": "toy normalisation e = v = 1 (B0 RESULTS.md:8) [assumed]; the map to Part A's U(1)_X coupling is NOT COMPUTED (YET) %s" % tagc,
            "tips": "both 1T and 2T reported; the run does not choose %s" % tagc,
            "T_zz_int": "int T_zz dA per row (column 'int T_zz dA'), = -mu_matter %s" % tagc,
            "eos_w": "int T_zz / int T_tt per row: max |w + 1| = %.1e %s" % (ws, tagc),
            "J": "0 by the ansatz (static, A_t = 0); NOT COMPUTED (YET) for spinning states %s" % tagc,
            "I_z": "0 by the ansatz (A_z = 0, z-independent); NOT COMPUTED (YET) for current-carrying states %s" % tagc,
        }
    else:
        first = next(c for c in CHK if not c[5])
        val = {k: NCY + " (critical stage FAIL: %s %s)" % (first[0], first[1]) for k in ("mu", "sigma_mu", "r_c", "r_c/R", "s_c", "s_c/R", "T_b", "gauge_norm", "tips",
                                                                     "T_zz_int", "eos_w", "J", "I_z")}
    fixed = {
        "alpha_ext": NCY + " (alpha is a scanned input here, not an output) [hive-run: SM1-INPUTS-RUN, none]",
        "G": NCY + " as a single value; the G_req(alpha) curve is in consistency_curve.csv and %s" % ref("greq"),
        "sigma_G": NCY + " [hive-run: SM1-INPUTS-RUN, none]",
        "Psi_rc": NCY + " (no MHD solve on a curved or conical background; spec 2(f)) [hive-run: SM1-INPUTS-RUN, none]",
        "pressure": NCY + " [hive-run: SM1-INPUTS-RUN, none]",
        "Pi": "definition, not a value; Part B scores both versions",
        "tau": NCY + " (no physical uncertainty exists) [hive-run: SM1-INPUTS-RUN, none]",
        "f_theta_core": NCY + " (fixed background, rule 1) [hive-run: SM1-INPUTS-RUN, none]",
    }
    order = list(slots) + [s for s in ("T_zz_int", "eos_w", "J", "I_z") if s not in slots]
    for s in order:
        fill.append("%s = %s" % (s, val.get(s, fixed.get(s, NCY))))
    fill += ["```", ""]
    files["SM1_INPUTS_FILLED.md"] = "\n".join(fill) + "\n"
    # ---------------- prediction vs outcome ----------------
    allmu = max(abs(r["crit"]["mu"] / (PI * r["n"]) - 1) for r in ROWS.values())
    e5c = [abs(r["crit"]["tips"][t]["mu_i"] - PI * r["n"] / 2) / (PI * r["n"] / 2) for r in graded.values() if r["layout"] == "2T" and r["eps"] == EPS_LARGE for t in ("N", "S")]
    wmax = max(abs(r["crit"]["w"] + 1) for r in ROWS.values())
    nc7v = next((c for c in NCK if c[1].startswith("same-R")), None)
    w("## PREDICTION versus outcome (a miss stays a miss)")
    w("")
    w("| prediction | outcome | verdict |")
    w("|---|---|---|")
    w("| %s | max |mu/(pi n) - 1| = %.1e over all %d rows (P12 included) | %s |" % (PRED["mu"], allmu, len(ROWS), "HIT" if allmu < G3_BOG_TOL else "MISS"))
    w("| %s | at eps <= %g: no s_c,delta at every vortex tip = %s; at eps > %g: s_c,delta exists at %d of %d vortex tips | %s |" % (
        PRED["bradlow"], EPS_BRADLOW_MAX, pinfo["brad_ok"], EPS_BRADLOW_MAX, pinfo["big_have"], pinfo["big_tot"], "HIT" if pinfo["brad_ok"] else "MISS"))
    w("| %s | max |G_req - (1 - alpha)/(4 pi n)| = %s | %s |" % (PRED["greq"], fe(pinfo["greq_dev"]), "HIT" if (pinfo["greq_dev"] or 0) < 1e-9 else "MISS"))
    w("| %s | max relative deviation %s | %s |" % (PRED["g5tip"], fe(max(e5c) if e5c else None), "HIT" if e5c and max(e5c) < G5_TIP_TOL else "MISS"))
    w("| %s | worst %s (graded entries) | %s |" % (PRED["nc7"], nc7v[2] if nc7v else "-", "HIT" if nc7v and nc7v[5] else "MISS"))
    w("| %s | P1 at eps = %g: max relative difference %s | report-only |" % (PRED["cone"], EPS_LARGE, fe(ninfo["cone_dev"])))
    w("| %s | max |w + 1| = %.1e (critical stage, all rows) | %s |" % (PRED["w"], wmax, "HIT" if wmax < G7_TOL else "MISS"))
    w("")
    # ---------------- audit ----------------
    after_bad = [nm for nm, path, exp in SOURCES if sha8(path) != before[path]]
    own_skip = set(files) | {"RESULTS.md"}
    own_after = {f: sha8(J(HERE, f)) for f in sorted(os.listdir(HERE)) if os.path.isfile(J(HERE, f)) and f not in own_skip}
    bad_names = code_names_clean()
    w("## Audit")
    w("")
    w("- Rule 1 / H2: no gravitational equation anywhere in run.py; alpha is a loop variable over the fixed grid; G_req is computed from alpha and "
      "mu_matter only and is an output curve; no alpha is derived from mu; backgrounds fixed [assumed].")
    w("- GR/Stelle controls: C-GR is labelled [GR control] in every table; C-Stelle and C-cigar are NOT COMPUTED (YET) rows.")
    w("- Missing values are labelled NOT COMPUTED (YET): alpha_ext, G (single value), sigma_G, Psi_rc, pressure, tau, f_theta_core, J and I_z "
      "for spinning/current-carrying states, the U(1)->MHD map, and the stability of every axisymmetric critical point.")
    w("- Thresholds, grids and predictions are constants in run.py's fixed block (printed above from those constants).")
    w("- Sources re-hashed after the run: %d of %d unchanged%s." % (len(SOURCES) - len(after_bad), len(SOURCES), "" if not after_bad else " (CHANGED: %s)" % after_bad))
    w("- This folder after the run, files other than the outputs: unchanged = %s." % (own_after == own_before))
    w("- Symbol map: line 1 of this file. Code names chi / eta_* / lambda_in (chive_ns, Venus N1-d) used in run.py: %s." % (bad_names if bad_names else "none"))
    w("- Every number in this file and the CSVs is printed from variables by run.py.")
    w("")
    write_outputs(files)
    hashes = {nm: sha8(J(HERE, nm))[0] for nm in files}
    w("## Grade")
    w("")
    w("- Critical stage (C0 critical-stage convergence + G1-G7): **%s**." % pf(crit_pass))
    w("- Stage NC (NC0 convergence incl. the stage-NC tally's non-converged entries, NC1-NC7, negative control): **%s** (%s)." % (pf(nc_pass), nc_reason))
    w("- SM1_INPUTS_FILLED.md written with values: %s." % ("YES (critical-stage slots)" if crit_pass else "NO (every slot NOT COMPUTED (YET))"))
    w("- Output files written by this run (SHA-256 prefix): %s; RESULTS.md is this file." % ", ".join("%s %s" % (k, v) for k, v in sorted(hashes.items())))
    w("- Runtime: %.0f s [computed]." % (time.time() - T0))
    files2 = {"RESULTS.md": "\n".join(OUT) + "\n"}
    write_outputs(files2)


if __name__ == "__main__":
    main()

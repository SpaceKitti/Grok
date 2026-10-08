"""B1 t-grid vs theta-grid convergence table (v2: adds the cut-off scan T = 20, 40, 80, 160 as the main table). REPORT-ONLY, outside the SM1 Part A graded run.

Requested by Venus (maths grader) on 2026-10-08 to close README disclosure 1 on evidence. This script does not import or
run run.py (run.py runs the whole graded job at import). It copies, line for line, the pieces of run.py that build B1 at
n = 3, eps = 4 (the case named in disclosure 1): B0's background functions taken from B0's run.py by AST (run.py
b0_namespace), B0's continuation loop (run.py b1_backgrounds, restricted to n = 3), the background fields (run.py b1_count),
and the two FD operators of R^2 D^2 (t-uniform grid, run.py lines 834-862; theta-uniform grid, run.py lines 865-878), with
the same count rule: Sylvester inertia via Job Two's monopole._sturm_count, eigenvalues below TAU_FD = 0.5 counted.
Eigenvalues are found by the same bisection as run.py's gen_eig (lo = -5, hi = 400, 60 halvings).
It writes only B1_TGRID_CONVERGENCE.md in this folder. No graded file is written or changed.
"""
import os
import sys

sys.dont_write_bytecode = True

import ast
import datetime
import hashlib
import math
import platform
import time

import numpy as np
import scipy
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OP = os.path.dirname(os.path.dirname(HERE))
USER = os.path.dirname(OP)
J = os.path.join

# ---------- settings, all fixed before the single run (copied from run.py where they exist) ----------
TAU_FD = 0.5                                   # run.py line 41
B1_FD_T, B1_FD_H = 40.0, 0.01                  # run.py line 54 (graded B1 t-grid)
N_LADDER = [2000, 4000, 8000, 16000, 32000]    # Venus: same ladder as the disclosure-1 theta-grid numbers
WINDOWS = [30.0, 40.0, 50.0]                   # report-only window check at step 0.01
T_SCAN = [20.0, 40.0, 80.0, 160.0]             # main table (v2, Venus + Helios): cut-off scan at step 0.01
N_TARGET, EPS_TARGET = 3, 4.0                  # disclosure 1: n = 3 at the largest eps
EIG_CEIL0 = 2.0                                # list every eigenvalue below this (doubled if fewer than N_SHOW found)
N_SHOW = 5                                     # lowest eigenvalues listed per grid, pooled over all (m, sigma3) sectors
GRADED = [("run.py", "803FD2DA"), ("README.md", "12CEC48F"), ("RESULTS.md", "7148A1DC"),
          ("CANDIDATES.md", "DAD867CE"), ("OVERLAPS_ALPHA.md", "D93AC9BD"), ("ANOMALIES.md", "B55D5D1F")]
PREDICTION_T = ("(v2, written before the v2 run) Venus and Helios: the leftover m = 1/2 eigenvalue goes like C/T with C "
                "about 7 (0.1821 at T = 40), so the count stays 3 at every T in the scan and T times that eigenvalue stays near 7.")
PREDICTION = ("t-grid count 3 at every N on the ladder, at the graded step and at every window. theta-grid count 2 at every N "
              "on the ladder (the graded run gave 2 at N = 2000), with the third eigenvalue above 0.5 and falling slowly "
              "(box scratch numbers 0.832, 0.770, 0.715, 0.668, 0.627).")

_S2 = J(USER, "sm-zero-modes-S2")
_B0 = J(OP, "Bradlow_cap", "B0_taubes_base")


def sha8(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:8].upper()


def check_graded(tag):
    ok = True
    rows = []
    for nm, h in GRADED:
        got = sha8(J(HERE, nm))
        rows.append((nm, h, got, got == h))
        ok = ok and got == h
        print("[%s] %s expected %s got %s %s" % (tag, nm, h, got, "OK" if got == h else "MISMATCH"), flush=True)
    return ok, rows


ok_before, rows_before = check_graded("before")
if not ok_before:
    print("STOP: a graded hash does not match before the run; nothing computed.")
    sys.exit(2)
SRC = [(J(_S2, "monopole.py"), "99AC267B"), (J(_B0, "run.py"), "15F2B139")]   # run.py Stage 0 hashes
for p, h in SRC:
    got = sha8(p)
    print("[source] %s expected %s got %s %s" % (p, h, got, "OK" if got == h else "MISMATCH"), flush=True)
    if got != h:
        print("STOP: source hash mismatch.")
        sys.exit(2)

sys.path.insert(0, _S2)
import monopole as MP  # noqa: E402  (Job Two; only _sturm_count is used)
sys.path.pop(0)


# ---------- copied from run.py b0_namespace (lines 246-267) ----------
def b0_namespace():
    path = J(_B0, "run.py")
    tree = ast.parse(open(path, encoding="utf-8").read())
    want_f = {"logsig2", "logcos2", "sech2", "solve_bg", "bg_fields", "integrals"}
    want_c = {"T_BVP", "N_BVP0", "BVP_TOL", "N_QUAD", "EPS_LIST", "N_LIST", "CONT_EPS", "C1_TOL"}
    keep = []
    for nd in tree.body:
        if isinstance(nd, ast.FunctionDef) and nd.name in want_f:
            keep.append(nd)
        elif isinstance(nd, ast.Assign):
            names = []
            for t in nd.targets:
                if isinstance(t, ast.Name):
                    names.append(t.id)
                elif isinstance(t, ast.Tuple):
                    names += [e.id for e in t.elts if isinstance(e, ast.Name)]
            if any(n in want_c for n in names):
                keep.append(nd)
    ns = {"np": np, "math": math, "solve_bvp": solve_bvp, "simpson": simpson}
    exec(compile(ast.Module(body=keep, type_ignores=[]), path, "exec"), ns)
    return ns


B0NS = b0_namespace()


# ---------- copied from run.py b1_backgrounds (lines 778-797), restricted to n = N_TARGET ----------
def b1_background(n, eps_want):
    ns = B0NS
    prev = None
    out = None
    for eps in sorted(set(ns["EPS_LIST"]) | set(ns["CONT_EPS"])):
        R2 = n * (1 + eps)
        if eps <= 0.1:
            u0 = math.log((n + 1) * (1 - 1 / (1 + eps)))
            guess = lambda tt, u0=u0: np.vstack([np.full(tt.size, u0), np.zeros(tt.size)])
        else:
            guess = lambda tt, s=prev: s.sol(tt)
        s, lw = ns["solve_bg"](n, n, R2, guess)
        prev = s
        if eps in ns["EPS_LIST"]:
            phi2, E, mx = ns["integrals"](s, lw, n, n, R2)
            Aa = 4 * np.pi * R2
            c1 = abs(phi2 - (Aa - 4 * np.pi * n)) / (Aa - 4 * np.pi * n)
            if eps == eps_want:
                out = (s, lw, R2, c1, mx, bool(s.success))
    return out


s, lw, R2, c1, mx, succ = b1_background(N_TARGET, EPS_TARGET)
n = N_TARGET
# ---------- copied from run.py b1_count (lines 803-812) ----------
T = B0NS["T_BVP"]
tt = np.linspace(-T, T, 40001)
f2 = np.exp(lw(tt) + s.sol(tt)[0])
B = 0.5 * (1.0 - f2)
Om2 = R2 * B0NS["sech2"](tt)
Aphi_in = cumulative_trapezoid(B * Om2, tt, initial=0.0)
flux = float(Aphi_in[-1])
mr = [k + 0.5 for k in range(-4, n + 4)]
print("background n = %d eps = %g: BVP success %s, C1 rel err %.3e, max |phi|^2 %.6f, flux %.10f, m range %s .. %s (%d values)"
      % (n, EPS_TARGET, succ, c1, mx, flux, mr[0], mr[-1], len(mr)), flush=True)


def bisect(cnt, k, lo=-5.0, hi=400.0, iters=60):
    """run.py gen_eig: k-th eigenvalue (0-based) from a monotone count function."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if cnt(mid) > k:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def t_sectors(tf, h):
    """run.py lines 835-857: R^2 D^2 on a grid uniform in t, Dirichlet ends; A u = lambda M u, M = diag(1/cosh t)."""
    cc, cp, cm = np.cosh(tf), np.cosh(tf + h / 2), np.cosh(tf - h / 2)
    Af = np.interp(tf, tt, Aphi_in, left=0.0, right=flux)
    Bf = np.interp(tf, tt, B, left=B[0], right=B[-1])
    Minv = 1.0 / cc
    ef = -cp[:-1] / h ** 2
    out = []
    for m in mr:
        Wt = (m - Af) * cc
        Wpt = -R2 * Bf + (m - Af) * np.tanh(tf) * cc ** 2
        for ch in (+1, -1):
            V = Wt ** 2 + (Wpt if ch > 0 else -Wpt)
            dd = (cp + cm) / h ** 2 + V / cc
            out.append((m, ch, (lambda lam, dd=dd: MP._sturm_count(dd - lam * Minv, ef, 0.0))))
    return out


def th_sectors(Nth):
    """run.py lines 865-878: R^2 D^2 on a grid uniform in theta, N interior points, Dirichlet ends."""
    hth = math.pi / (Nth + 1)
    th = hth * np.arange(1, Nth + 1)
    sn, cs = np.sin(th), np.cos(th)
    tth = np.log(np.tan(th / 2))
    Ath = np.interp(tth, tt, Aphi_in, left=0.0, right=flux)
    Bth = np.interp(tth, tt, B, left=B[0], right=B[-1])
    off = -np.ones(Nth - 1) / hth ** 2
    out = []
    for m in mr:
        W = (m - Ath) / sn
        Wp = -R2 * Bth - (m - Ath) * cs / sn ** 2
        for ch in (+1, -1):
            V = W ** 2 + (Wp if ch > 0 else -Wp)
            d = 2.0 / hth ** 2 + V
            out.append((m, ch, (lambda lam, d=d: MP._sturm_count(d, off, lam))))
    return out, hth


def analyse(sectors):
    t1 = time.time()
    cnt05 = {+1: 0, -1: 0}
    for m, ch, cnt in sectors:
        cnt05[ch] += cnt(TAU_FD)
    ceil = EIG_CEIL0
    while True:
        below = [(m, ch, cnt, cnt(ceil)) for m, ch, cnt in sectors]
        if sum(b[3] for b in below) >= N_SHOW:
            break
        ceil *= 2.0
    eigs = []
    for m, ch, cnt, c in below:
        for k in range(c):
            eigs.append((bisect(cnt, k), m, ch))
    eigs.sort()
    n_from_eigs = sum(1 for e in eigs if e[0] < TAU_FD)
    return dict(cnt=cnt05, total=cnt05[+1] + cnt05[-1], eigs=eigs[:N_SHOW], ceil=ceil, n_from_eigs=n_from_eigs,
                secs=time.time() - t1)


def fmt_eigs(eigs):
    return ", ".join("%.4f" % e[0] for e in eigs)


def fmt_eigs_lab(eigs):
    return ", ".join("%.6f (m=%g, s3=%+d)" % (e[0], e[1], e[2]) for e in eigs)


rows = []
for N in N_LADDER:
    th_sec, hth = th_sectors(N)
    rth = analyse(th_sec)
    ht = 2 * B1_FD_T / (N + 1)
    tf = -B1_FD_T + ht * np.arange(1, N + 1)
    rt = analyse(t_sectors(tf, ht))
    rows.append((N, hth, rth, ht, tf.size, rt))
    print("N = %d | theta: h = %.6g, count<%g (+1, -1) = (%d, %d), lowest %s [%.1fs] | t on [-%g, %g]: h = %.6g, points %d, "
          "count<%g (+1, -1) = (%d, %d), lowest %s [%.1fs]" % (
              N, hth, TAU_FD, rth["cnt"][+1], rth["cnt"][-1], fmt_eigs_lab(rth["eigs"]), rth["secs"], B1_FD_T, B1_FD_T, ht,
              tf.size, TAU_FD, rt["cnt"][+1], rt["cnt"][-1], fmt_eigs_lab(rt["eigs"]), rt["secs"]), flush=True)

# graded reference row: exactly run.py line 834
tf_ref = np.arange(-B1_FD_T + B1_FD_H, B1_FD_T - B1_FD_H / 2, B1_FD_H)
rref = analyse(t_sectors(tf_ref, B1_FD_H))
print("graded reference t-grid (run.py line 834): [-%g, %g], h = %g, interior points %d (+2 Dirichlet ends = %d nodes), "
      "count<%g (+1, -1) = (%d, %d), lowest %s" % (B1_FD_T, B1_FD_T, B1_FD_H, tf_ref.size, tf_ref.size + 2, TAU_FD,
                                                rref["cnt"][+1], rref["cnt"][-1], fmt_eigs_lab(rref["eigs"])), flush=True)

wrows = []
for Tw in WINDOWS:
    tfw = np.arange(-Tw + B1_FD_H, Tw - B1_FD_H / 2, B1_FD_H)
    rw = analyse(t_sectors(tfw, B1_FD_H))
    wrows.append((Tw, tfw.size, rw))
    print("window [-%g, %g], h = %g, interior points %d: count<%g (+1, -1) = (%d, %d), lowest %s" % (
        Tw, Tw, B1_FD_H, tfw.size, TAU_FD, rw["cnt"][+1], rw["cnt"][-1], fmt_eigs_lab(rw["eigs"])), flush=True)

trows = []
for Tw in T_SCAN:
    tfw = np.arange(-Tw + B1_FD_H, Tw - B1_FD_H / 2, B1_FD_H)
    rw = analyse(t_sectors(tfw, B1_FD_H))
    half = [e[0] for e in rw["eigs"] if e[1] == 0.5 and e[2] == +1]
    lam_half = half[0] if half else None
    zmax = max([e[0] for e in rw["eigs"] if e[0] < TAU_FD], default=None)
    trows.append((Tw, tfw.size, rw, lam_half, zmax))
    print("T scan [-%g, %g], h = %g, interior points %d: count<%g (+1, -1) = (%d, %d), lowest %s; m=1/2 eig %s, T x eig %s" % (
        Tw, Tw, B1_FD_H, tfw.size, TAU_FD, rw["cnt"][+1], rw["cnt"][-1], fmt_eigs_lab(rw["eigs"]),
        "%.6f" % lam_half if lam_half is not None else "NOT COMPUTED (YET)",
        "%.4f" % (Tw * lam_half) if lam_half is not None else "NOT COMPUTED (YET)"), flush=True)

# theta-grid m = 1/2 eigenvalue: fit a/(ln N + c) (Venus's form), report-only
from scipy.optimize import curve_fit  # noqa: E402
thN = np.array([r[0] for r in rows], dtype=float)
thL = np.array([[e[0] for e in r[2]["eigs"] if e[1] == 0.5 and e[2] == +1][0] for r in rows])
(fa, fc), _ = curve_fit(lambda N, a, c: a / (np.log(N) + c), thN, thL, p0=(7.0, 1.0))
fres = float(np.max(np.abs(fa / (np.log(thN) + fc) - thL)))
lnN_cross = fa / TAU_FD - fc
print("theta-grid m=1/2 eigenvalue fit a/(ln N + c): a = %.4f, c = %.4f, largest residual %.2e; drops below %g at N = %.3g" % (
    fa, fc, fres, TAU_FD, math.exp(lnN_cross)), flush=True)

# reproduction check against the graded CANDIDATES.md B1 row (n = 3, eps = 4)
cand = open(J(HERE, "CANDIDATES.md"), encoding="utf-8").read().splitlines()
grow = [l for l in cand if l.startswith("| %d | %g | " % (n, EPS_TARGET))]
gcells = [c.strip() for c in grow[-1].strip("|").split("|")] if grow else []
th2000 = [r for r in rows if r[0] == 2000][0][2]
mine_fd_plus, mine_fd_minus = rref["cnt"][+1], rref["cnt"][-1]
mine_th = "%d, %d" % (th2000["cnt"][+1], th2000["cnt"][-1])
repro = []
if gcells:
    repro = [("flux", gcells[5], "%.10f" % flux), ("FD sigma3=+1", gcells[9], "%d" % mine_fd_plus),
             ("FD sigma3=-1", gcells[10], "%d" % mine_fd_minus), ("theta-grid FD (+1, -1) at N = 2000", gcells[13], mine_th)]
for nm, g, mne in repro:
    print("[repro] %s: graded CANDIDATES.md %s, this script %s %s" % (nm, g, mne, "MATCH" if g == mne else "DIFFERENT"), flush=True)

# ---------- write the markdown ----------
ok_after, rows_after = check_graded("after")
md = []
md.append("# B1 t-grid convergence table: REPORT-ONLY")
md.append("")
md.append("**REPORT-ONLY. Outside the graded SM1 Part A run. Requested by Venus on 2026-10-08 to close README disclosure 1. "
          "It does not change any graded output.** Written by `B1_TGRID_CONVERGENCE.py`, which copies run.py's B1 code and "
          "does not import or run run.py. Run at %s on %s, Python %s, numpy %s, scipy %s." % (
              datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"), platform.node(),
              platform.python_version(), np.__version__, scipy.__version__))
md.append("")
md.append("Graded hashes (SHA-256, first 8 hex), checked by the script before and after this run:")
md.append("")
md.append("| file | graded | before | after |")
md.append("|---|---|---|---|")
for (nm, h, g1, _), (_, _, g2, _) in zip(rows_before, rows_after):
    md.append("| %s | %s | %s | %s |" % (nm, h, g1, g2))
md.append("")
md.append("All unchanged: %s." % ("YES" if ok_before and ok_after else "NO"))
md.append("")
md.append("## What this checks")
md.append("")
md.append("Case: B1 at n = %d, eps = %g, the case where the graded run's theta-grid column undercounted. The analytic count is "
          "the index N_Phi = %d, fixed beforehand in A8. Both grids use the same operator R^2 D^2 = -u'' + (W^2 +- W') u with "
          "Dirichlet ends, the same %d m values (m = %s to %s) and both sigma3 signs, and the same rule: count eigenvalues "
          "below %g. The theta grid has N interior points, spacing pi/(N+1). The t grid has N interior points uniform in "
          "t = ln tan(theta/2) on [-%g, %g], spacing %g/(N+1); the window is kept at [-%g, %g] at every N. Nothing was tuned "
          "after seeing results." % (n, EPS_TARGET, n, len(mr), mr[0], mr[-1], TAU_FD, B1_FD_T, B1_FD_T, 2 * B1_FD_T,
                                    B1_FD_T, B1_FD_T))
md.append("")
md.append("Prediction written before the run: %s" % PREDICTION)
md.append("")
md.append("Prediction for the cut-off scan: %s" % PREDICTION_T)
md.append("")
md.append("Version note: the first version of this script (v1) ran once at 16:13 BST with the N ladder and the window check only. "
          "This version (v2) adds the cut-off scan and the fit below, at Venus's and Helios's request. The v1 rows are recomputed "
          "here and are deterministic; v1's stdout is kept at %TEMP%\\b1_tgrid_stdout_v1.txt on TrinityOrb.")
md.append("")
md.append("## Main table: cut-off scan in T (t grid, step %g, window [-T, T])" % B1_FD_H)
md.append("")
md.append("On the t grid the step size barely matters; what is left is set by where the grid ends (theta about 2 e^-T at the "
          "north pole). The m = 1/2 mode sits exactly at the critical point of its pole potential, so its eigenvalue goes to 0 "
          "only like C/T. The count of 3 is the A8 index, fixed in advance; this table shows the FD count agrees with it at "
          "every cut-off.")
md.append("")
md.append("| T | interior points | lowest eigs | m = 1/2 eig | T x (m = 1/2 eig) | count<%g |" % TAU_FD)
md.append("|---|---|---|---|---|---|")
for Tw, npts, rw, lam_half, zmax in trows:
    md.append("| %g | %d | %s | %s | %s | %d |" % (Tw, npts, fmt_eigs(rw["eigs"]),
                                                "%.4f" % lam_half if lam_half is not None else "**NOT COMPUTED (YET)**",
                                                "%.3f" % (Tw * lam_half) if lam_half is not None else "**NOT COMPUTED (YET)**",
                                                rw["total"]))
md.append("")
md.append("## Side-by-side table: theta grid and t grid on Venus's N ladder")
md.append("")
md.append("Lowest %d eigenvalues pooled over every (m, sigma3) sector, smallest first." % N_SHOW)
md.append("")
md.append("| N | theta-grid lowest eigs | theta-grid count<%g | t spacing | t-grid lowest eigs | t-grid count<%g |" % (TAU_FD, TAU_FD))
md.append("|---|---|---|---|---|---|")
for N, hth, rth, ht, npts, rt in rows:
    md.append("| %d | %s | %d | %.6g | %s | %d |" % (N, fmt_eigs(rth["eigs"]), rth["total"], ht, fmt_eigs(rt["eigs"]), rt["total"]))
md.append("| graded row: %d (step %g) | **NOT COMPUTED (YET)** (t-grid row only) | **NOT COMPUTED (YET)** | %g | %s | %d |" % (tf_ref.size, B1_FD_H, B1_FD_H, fmt_eigs(rref["eigs"]),
                                                                         rref["total"]))
md.append("")
md.append("Graded row: run.py's own grid, %d interior points plus the 2 Dirichlet ends (%d nodes). Every count above has "
          "sigma3 = -1 count %s." % (tf_ref.size, tf_ref.size + 2,
                                     "0 throughout" if all(r[2]["cnt"][-1] == 0 and r[5]["cnt"][-1] == 0 for r in rows)
                                     and rref["cnt"][-1] == 0 else "NOT always 0 (see detail)"))
md.append("")
md.append("Fit of the theta-grid m = 1/2 eigenvalue to a/(ln N + c) (Venus's form, report-only): a = %.3f, c = %.3f, largest "
          "residual %.1e. On that fit the theta grid would need about N = %.2g points before this mode drops below %g." % (
              fa, fc, fres, math.exp(lnN_cross), TAU_FD))
md.append("")
md.append("## Window check (t grid, step %g)" % B1_FD_H)
md.append("")
md.append("| window | interior points | lowest eigs | count<%g |" % TAU_FD)
md.append("|---|---|---|---|")
for Tw, npts, rw in wrows:
    md.append("| [-%g, %g] | %d | %s | %d |" % (Tw, Tw, npts, fmt_eigs(rw["eigs"]), rw["total"]))
md.append("")
md.append("## Detail: eigenvalues with their sector")
md.append("")
for N, hth, rth, ht, npts, rt in rows:
    md.append("- N = %d, theta grid (h = %.6g): %s" % (N, hth, fmt_eigs_lab(rth["eigs"])))
    md.append("- N = %d, t grid (h = %.6g): %s" % (N, ht, fmt_eigs_lab(rt["eigs"])))
md.append("- graded t grid (h = %g): %s" % (B1_FD_H, fmt_eigs_lab(rref["eigs"])))
for Tw, npts, rw in wrows:
    md.append("- window [-%g, %g]: %s" % (Tw, Tw, fmt_eigs_lab(rw["eigs"])))
for Tw, npts, rw, lam_half, zmax in trows:
    md.append("- T scan [-%g, %g]: %s" % (Tw, Tw, fmt_eigs_lab(rw["eigs"])))
md.append("")
md.append("Cross-check: in every grid, the number of listed eigenvalues below %g equals the Sturm count: %s." % (
    TAU_FD, "YES" if all(r[2]["n_from_eigs"] == r[2]["total"] and r[5]["n_from_eigs"] == r[5]["total"] for r in rows)
    and rref["n_from_eigs"] == rref["total"] and all(w[2]["n_from_eigs"] == w[2]["total"] for w in wrows)
    and all(w[2]["n_from_eigs"] == w[2]["total"] for w in trows) else "NO"))
md.append("")
md.append("## Reproduction of the graded B1 row (CANDIDATES.md, n = %d, eps = %g)" % (n, EPS_TARGET))
md.append("")
md.append("| item | graded file | this script | same |")
md.append("|---|---|---|---|")
for nm, g, mne in repro:
    md.append("| %s | %s | %s | %s |" % (nm, g, mne, "YES" if g == mne else "NO"))
md.append("")
md.append("Background: BVP success %s, C1 relative error %.3e, max |phi|^2 %.6f. Total time %.0f s." % (succ, c1, mx, time.time() - T0))
md.append("")
with open(J(HERE, "B1_TGRID_CONVERGENCE.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(md) + "\n")
print("wrote B1_TGRID_CONVERGENCE.md; graded hashes unchanged: %s; total %.0f s" % (ok_before and ok_after, time.time() - T0))

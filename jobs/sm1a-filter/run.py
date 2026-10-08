"""SM1 Part A (JOB_SM1A_SPEC.md, SHA-256 prefix 04B9AA05): the input-free stages.

Writes CANDIDATES.md, OVERLAPS_ALPHA.md, ANOMALIES.md and RESULTS.md in this folder. Those four files are
generated here only and are never hand-edited. Sources are imported read-only with no bytecode written, and every
source file is hashed before and after the run. Akitti's inputs are not used: only the single alpha_ext slot of
SM1_INPUTS.md (spec 0.2) is read, and only if it carries an [Akitti: ...] tag. Part B is HELD and is not built here.
"""
import os
import sys

sys.dont_write_bytecode = True

import ast
import datetime
import hashlib
import importlib.util
import itertools
import math
import platform
import re
import time
import zlib
from fractions import Fraction as Fr

import numpy as np
import scipy
from scipy.integrate import cumulative_trapezoid, simpson, solve_bvp
import sympy as sp
import mpmath as mpm

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OP = os.path.dirname(os.path.dirname(HERE))       # ...\open-problems
USER = os.path.dirname(OP)                        # C:\Users\Akitt

# ======================= thresholds and settings (fixed before the graded run) =======================
SPEC_HASH = "04B9AA05"           # JOB_SM1A_SPEC.md; Venus passed this hash; replaces 712EF4A8
ALPHA_GRID = [Fr(1), Fr(4, 5), Fr(3, 5), Fr(1, 2)]   # spec 0.2 [assumed] (Job Four's grid)
NPHI_TABLE_MAX = 4               # 1b-8 (c): general fusion table for N_Phi <= 4
SPINS = [Fr(0), Fr(1, 2), Fr(1)]  # E4 [Venus]
TAU_FD = 0.5                     # FD zero-mode threshold on R^2 D^2 (Job Two / Job Four value)
NFD_S = 4000                     # Job Two's FD grid (S family)
NFD_R = 2000                     # Job Four's FD grid (R family, B1)
REG_TOL = -1e-6                  # Job Four's regularity tolerance (tip exponents >= -1e-6)
NORM_TOL = 1e-8                  # Job Four's normalisability tolerance |lnZ(40) - lnZ(20)| < 1e-8
OA_TOL = 1e-12                   # O-a: absolute, against Job Two's exact wigner_3j values
OB_TOL = 1e-9                    # O-b: relative, quadrature vs closed form
OC_TOL = 1e-12                   # O-c: absolute, entries that break the m rule
OD_TOL = 1e-12                   # O-d: absolute, Gram row = 1/sqrt(4 pi alpha)
NQ, NQ_CHECK, TQ = 2000, 4000, 40.0   # Gauss-Legendre quadrature in t = ln tan(theta/2) on [-TQ, TQ]
NPH = 64                          # phi points for the O-c 2D check
MP_DPS = 40                       # mpmath precision for closed forms
B1_NT = 160001                    # B1: t grid on [-40, 40] for the zero-mode ODE and norms
B1_FD_T, B1_FD_H = 40.0, 0.01        # B1 FD: uniform grid in t = ln tan(theta/2) on [-40, 40], Dirichlet ends [post-hoc, development: box scratch run]
mpm.mp.dps = MP_DPS

OUT = {"RESULTS": [], "CANDIDATES": [], "OVERLAPS_ALPHA": [], "ANOMALIES": []}
GRADE = []                        # (item, description, ok)


def w(f, s=""):
    OUT[f].append(s)
    if f == "RESULTS":
        print(s, flush=True)


def yn(b):
    return "YES" if b else "NO"


def pf(b):
    return "PASS" if b else "FAIL"


def sha8(path):
    with open(path, "rb") as fh:
        b = fh.read()
    return hashlib.sha256(b).hexdigest()[:8].upper(), "%08X" % (zlib.crc32(b) & 0xFFFFFFFF)


def R(x):
    return sp.Rational(str(x)) if not isinstance(x, sp.Basic) else x


def fr(x):
    return str(sp.nsimplify(x)) if not isinstance(x, Fr) else (str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator))


class Stop(Exception):
    pass


def write_all(stopped=None):
    stamp = datetime.datetime.now().astimezone()
    for name, lines in OUT.items():
        if stopped and name != "RESULTS":
            continue
        with open(os.path.join(HERE, name + ".md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")


# ======================= Stage 0: inventory (spec section 2) =======================
J = os.path.join
SOURCES = [
    ("spec", J(OP, "01_sm_from_sphere", "SM1_filter", "JOB_SM1A_SPEC.md"), SPEC_HASH),
    ("framework", J(OP, "AKITTI_FRAMEWORK_2026-10-08.md"), "6CD5F259"),
    ("LIFT spec (n-convention lines 85-86)", J(OP, "JOB_LIFT_SPEC.md"), "77D663CE"),
]
_S2 = J(USER, "sm-zero-modes-S2")
for nm, h in [("README.md", "9189C7C8"), ("RESULTS.md", "FEF2BA79"), ("RESULTS_alt.md", "38A2B07C"), ("RESULTS_final.md", "78C1BC24"),
              ("anomalies.py", "EFE2723B"), ("monopole.py", "99AC267B"), ("overlaps.py", "3BFD8603"), ("run.py", "DCE6413E")]:
    SOURCES.append(("D1 Job Two", J(_S2, nm), h))
_JF = J(USER, "sm-rugby-yukawa")
for nm, h in [("README.md", "D28E4934"), ("RESULTS.md", "BBABA152"), ("run.py", "8FA69F08"), ("ratios.png", "630FB985")]:
    SOURCES.append(("D2 Job Four", J(_JF, nm), h))
for nm, h in [("README.md", "BC001743"), ("RESULTS.md", "9E8D0411"), ("run.py", "C70AD870")]:
    SOURCES.append(("D3 Job 4b", J(USER, "sm-yukawa-4b-ckm", nm), h))
for nm, h in [("README.md", "DAB95C99"), ("RESULTS.md", "066D9B4E"), ("run.py", "C16D5DD9")]:
    SOURCES.append(("D4 Job 4c", J(USER, "Job4c_rs_anarchy", nm), h))
SOURCES.append(("D4 Job 4c spec", J(OP, "01_sm_from_sphere", "JOB_4c_SPEC.md"), "EAE66844"))
_U1 = J(OP, "U1_fuzzy_sphere_strings")
for nm, h in [("README.md", "0D584792"), ("RESULTS.md", "232B3059"), ("run.py", "851363FB")]:
    SOURCES.append(("D5 U1", J(_U1, nm), h))
_B0 = J(OP, "Bradlow_cap", "B0_taubes_base")
for nm, h in [("RESULTS.md", "AE4E8FFB"), ("README.md", "D0F1A74C"), ("run.py", "15F2B139"), ("B0_GRADE_HELIOS.md", "E58EFC2F")]:
    SOURCES.append(("D6 B0", J(_B0, nm), h))
SOURCES.append(("D7 B1 outline", J(OP, "Bradlow_cap", "JOB_B1_SM_ZEROMODES_SPEC.md"), "AFF0FB0D"))
for nm, h in [("README.md", "8FEAA480"), ("RESULTS.md", "1EAF64BD")]:
    SOURCES.append(("D8 B2", J(OP, "Bradlow_cap", "02_vacuum", nm), h))
for nm, h in [("RESULTS.md", "12E53647"), ("README.md", "BDCC8DAE"), ("run.py", "FF91D4B9")]:
    SOURCES.append(("D9 Job 5d", J(OP, "5d_rugby_ball_flux", nm), h))
for nm, h in [("README.md", "8767634D"), ("RESULTS.md", "6146CF25"), ("run.py", "586C6BC8")]:
    SOURCES.append(("D10 Job 5b", J(USER, "radion-5b-tension-casimir", nm), h))
SOURCES += [("D11 Job 5c", J(USER, "vacuum-flux-share", "RESULTS.md"), "F02E9CA9"),
            ("D11 A1", J(OP, "A1_axion_sees_n", "RESULTS.md"), "F9F57321"),
            ("D11 radion-onshell", J(USER, "radion-onshell-filter", "RESULTS.md"), "345FB29A"),
            ("D12 Betti-Berry", J(USER, "betti-berry-vacuum-filter", "goldberg.py"), "404800FA"),
            ("D12 Betti-Berry", J(USER, "betti-berry-vacuum-filter", "README.md"), "D779A5BD")]


def folder_state(path, skip=()):
    out = {}
    for nm in sorted(os.listdir(path)):
        p = J(path, nm)
        if nm in skip or not os.path.isfile(p):
            continue
        out[nm] = sha8(p)
    return out


OWN_OUTPUTS = ("CANDIDATES.md", "OVERLAPS_ALPHA.md", "ANOMALIES.md", "RESULTS.md")
now = datetime.datetime.now().astimezone()
z = now.strftime("%z")
w("RESULTS", "# SM1 Part A - input-free stages (RESULTS, generated by run.py; do not edit by hand)")
w("RESULTS", "")
w("RESULTS", "Generated %s (local time, UTC%s:%s). Python %s, numpy %s, scipy %s, sympy %s, mpmath %s." % (
    now.strftime("%Y-%m-%d %H:%M:%S"), z[:3], z[3:], platform.python_version(), np.__version__, scipy.__version__,
    sp.__version__, mpm.__version__))
w("RESULTS", "")
w("RESULTS", "**Scope.** Part A builds and counts only; it scores nothing and grades no physics. The lift's gravity is "
  "unknown quantum gravity [Akitti]; nothing here uses an Einstein equation, and GR appears only as labelled reference "
  "rows in the source datasets (D9 [GR control]). Part B (scoring against Akitti's integrals and MHD trace) is HELD "
  "and is not built. None of Akitti's inputs (mu, G, r_c, Psi, Pi) is filled in anywhere.")
w("RESULTS", "")
w("RESULTS", "Thresholds fixed before the graded run: C-a/C-b/C-c/C-d exact (integers, sympy Rational); FD zero-mode "
  "threshold %g on R^2 D^2 (N = %d S family, %d R family and B1); regularity p >= %g; normalisability |lnZ(40) - lnZ(20)| < %g; "
  "O-a %g abs; O-b %g rel; O-c %g abs; O-d %g abs; A-a and A-b exact. Quadrature: Gauss-Legendre, %d nodes in t = ln tan(theta/2) "
  "on [-%g, %g] (check with %d). mpmath %d digits. Build PASS = every graded item passes." % (
      TAU_FD, NFD_S, NFD_R, REG_TOL, NORM_TOL, OA_TOL, OB_TOL, OC_TOL, OD_TOL, NQ, TQ, TQ, NQ_CHECK, MP_DPS))
w("RESULTS", "")
w("RESULTS", "## Stage 0: inventory check (spec section 2) [graded, build]")
w("RESULTS", "")
w("RESULTS", "| dataset | file | expected SHA-256 prefix | found | CRC32 | match |")
w("RESULTS", "|---|---|---|---|---|---|")
BEFORE = {}
bad = []
for ds, path, exp in SOURCES:
    if not os.path.isfile(path):
        w("RESULTS", "| %s | %s | %s | MISSING | - | NO |" % (ds, os.path.relpath(path, USER), exp))
        bad.append(path)
        continue
    h, c = sha8(path)
    BEFORE[path] = (h, c)
    w("RESULTS", "| %s | %s | %s | %s | %s | %s |" % (ds, os.path.relpath(path, USER), exp, h, c, yn(h == exp)))
    if h != exp:
        bad.append(path)
w("RESULTS", "")
w("RESULTS", "D10's README: the spec records main 9FBE7862 and the TrinityOrb copy 8767634D; the TrinityOrb copy is the one checked. "
  "D13 (Pair A / qg-* / lift-l1) has no hashes in the spec and is not SM data, so it is not hashed.")
if bad:
    w("RESULTS", "")
    w("RESULTS", "**STOP: %d source(s) missing or with a different hash. Nothing computed.**" % len(bad))
    write_all(stopped=True)
    sys.exit(2)
w("RESULTS", "")
w("RESULTS", "All %d source files match the spec's table: YES." % len(SOURCES))
GRADE.append(("Stage 0", "inventory hashes match spec section 2 (%d files)" % len(SOURCES), True))
OWN_BEFORE = folder_state(HERE, skip=OWN_OUTPUTS)

# ---------- SM1_INPUTS.md: presence only (spec 0.2) ----------
INPUTS = J(HERE, "SM1_INPUTS.md")
FIELDS_IN = ["alpha_ext", "G", "sigma_G", "mu", "sigma_mu", "r_c", "r_c/R", "Psi_rc", "pressure", "Pi", "T_b", "gauge_norm", "tau"]
present = {}
alpha_ext = None
if os.path.isfile(INPUTS):
    txt = open(INPUTS, encoding="utf-8").read().splitlines()
    for key in FIELDS_IN:
        st = "absent"
        for ln in txt:
            m = re.match(r"\s*" + re.escape(key) + r"\s*=\s*(\S+)(.*)$", ln)
            if m:
                tagged = re.search(r"\[Akitti:[^\]]+\]", m.group(2)) is not None
                st = "present, tagged" if tagged else "present but untagged"
                if key == "alpha_ext" and tagged:
                    alpha_ext = Fr(m.group(1)).limit_denominator(10 ** 9)
        present[key] = st
else:
    present = {k: "absent (no SM1_INPUTS.md)" for k in FIELDS_IN}
w("RESULTS", "")
w("RESULTS", "### SM1_INPUTS.md fields (presence only; no value except a tagged alpha_ext is used)")
w("RESULTS", "")
w("RESULTS", "| field | status |")
w("RESULTS", "|---|---|")
for k in FIELDS_IN:
    w("RESULTS", "| %s | %s |" % (k, present[k]))
w("RESULTS", "")
ALPHAS = list(ALPHA_GRID)
if alpha_ext is None:
    w("RESULTS", "alpha_ext absent: grid-only run (alpha in {%s} [assumed])." % ", ".join(fr(a) for a in ALPHA_GRID))
else:
    ALPHAS.append(alpha_ext)
    w("RESULTS", "alpha_ext = %s [Akitti] read from SM1_INPUTS.md; added as one more alpha column." % fr(alpha_ext))
w("RESULTS", "")

# ---------- read-only imports of the source code ----------
sys.path.insert(0, _S2)
import anomalies as AN  # noqa: E402  (Job Two, D1)
import monopole as MP   # noqa: E402
import overlaps as OV   # noqa: E402
sys.path.pop(0)
_spec = importlib.util.spec_from_file_location("jobfour_run", J(_JF, "run.py"))
JF = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(JF)     # module level only: hashes Job Two's folder and imports its monopole.py; main() is not run


def b0_namespace():
    """Read B0's run.py and execute ONLY its background functions and constants (its module level runs the whole job)."""
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
    return ns, sorted(n.name if isinstance(n, ast.FunctionDef) else "assign@%d" % n.lineno for n in keep)


B0NS, B0_KEPT = b0_namespace()


def cited(path, lineno, pattern):
    """Return the regex match of a cited line; stop if the line is not what the spec cites."""
    lines = open(path, encoding="utf-8").read().splitlines()
    ln = lines[lineno - 1]
    m = re.search(pattern, ln)
    if not m:
        raise Stop("cited line %s:%d does not match %r: %r" % (os.path.basename(path), lineno, pattern, ln[:120]))
    return m


def row_cells(path, lineno):
    ln = open(path, encoding="utf-8").read().splitlines()[lineno - 1]
    if not ln.startswith("|"):
        raise Stop("cited line %s:%d is not a table row: %r" % (os.path.basename(path), lineno, ln[:120]))
    return [c.strip() for c in ln.strip().strip("|").split("|")]


# ======================= 1.2 n conventions: N_Phi objects (hard stop on unconverted n) =======================
class ConventionError(Exception):
    pass


class NPhi:
    """Number of flux quanta the field sees, N_Phi = |x| (1/2pi) int F = 2|q|. Only built by convert()."""
    __slots__ = ("value", "source", "rule")

    def __init__(self, value, source, rule, _key=None):
        if _key is not _CONVERT_KEY:
            raise ConventionError("N_Phi must be built by convert()")
        self.value, self.source, self.rule = value, source, rule


_CONVERT_KEY = object()
N_CONVENTION = {
    "JobTwo": "n = flux quanta seen by a charge-1 field; N_Phi = |x| n",
    "U1": "n = number of strings = monopole charge (Wu-Yang q = n/2); N_Phi = n",
    "JobFour": "n as Job Two (q = x n/2); N_Phi = |x| n",
    "B0": "n = vortex number = flux quanta; N_Phi = n (unit charge)",
    "RW": "n_RW = SU(2) monopole charge, q = n_RW; N_Phi = 2 n_RW",
    "q": "Wu-Yang monopole charge q; N_Phi = 2|q|",
}


def convert(source, n, x=1):
    if source not in N_CONVENTION:
        raise ConventionError("unknown n convention %r" % source)
    n = Fr(n)
    if source == "RW":
        v = 2 * abs(n)
    elif source == "q":
        v = 2 * abs(n)
    else:
        v = abs(Fr(x)) * abs(n)
    assert v.denominator == 1
    return NPhi(int(v), source, N_CONVENTION[source], _key=_CONVERT_KEY)


def _need(N):
    if not isinstance(N, NPhi):
        raise ConventionError("count formed from an unconverted n (%r)" % (N,))
    return N.value


def count_dirac(N):
    return _need(N)


def count_scalar(N):
    return _need(N) + 1


def count_spin1(N):
    return _need(N) - 1


def count_spin(N, s):
    return _need(N) + 1 - int(2 * s)


# ---------- a cited line that does not match, or any error, stops the run with RESULTS.md only ----------
def _hook(t, v, tb):
    import traceback
    w("RESULTS", "")
    if issubclass(t, Stop):
        w("RESULTS", "**STOP: %s. Only RESULTS.md is written.**" % v)
    else:
        w("RESULTS", "**RUN ERROR (no outputs except RESULTS.md):**")
        w("RESULTS", "```")
        for ln in "".join(traceback.format_exception(t, v, tb)).splitlines():
            w("RESULTS", ln)
        w("RESULTS", "```")
    write_all(stopped=True)


sys.excepthook = _hook


# ======================= Stage 1: S family recomputed with Job Two's code =======================
# 6D Weyl field: (name, d3, A3, d2, Y, Gamma7, x). A3 = +1 for a colour triplet (6D fields are never antitriplets here).
def content(kind, nu=True):
    base = [("Q", 3, 1, 2, Fr(1, 6), -1, 1), ("L", 1, 0, 2, Fr(-1, 2), -1, 1)]
    if kind == "ALT":
        g7, x = 1, 1
    elif kind == "MAIN":
        g7, x = -1, -1
    elif kind == "S5":
        g7, x = -1, 1
    else:
        raise ValueError(kind)
    s = [("u", 3, 1, 1, Fr(2, 3), g7, x), ("d", 3, 1, 1, Fr(-1, 3), g7, x), ("e", 1, 0, 1, Fr(-1), g7, x)]
    if nu:
        s.append(("nu", 1, 0, 1, Fr(0), g7, x))
    return base + s


CANDS = [
    # id, family, content kind, with nu, flux n (Job Two's n), Higgs, description
    ("S1", "S", "ALT", True, 3, "ALT", "ALT + nu^c, n = 3 (Akitti's chosen model)"),
    ("S2", "S", "ALT", False, 3, "ALT", "ALT without nu^c, n = 3"),
    ("S3", "S", "MAIN", True, 3, "A", "MAIN + nu^c, Higgs A (x = +2, j = 2), n = 3"),
    ("S4", "S", "MAIN", False, 3, "A", "MAIN without nu^c, Higgs A, n = 3"),
    ("S5", "S", "S5", True, 3, "neutral", "MAIN fermions with singlets at x = +1 (Assignment B), neutral Higgs, n = 3"),
    ("S6", "S", "MAIN", True, 3, "C", "MAIN + nu^c, Higgs C (j = 3), n = 3"),
    ("S7", "S", "ALT", True, 1, "ALT", "ALT + nu^c, n = 1"),
    ("S8", "S", "ALT", True, 2, "ALT", "ALT + nu^c, n = 2"),
    ("S9", "S", "ALT", True, 4, "ALT", "ALT + nu^c, n = 4"),
    ("R1", "R", "ALT", True, 3, "ALT", "ALT + nu^c, n = 3, rugby ball"),
    ("R2", "R", "ALT", False, 3, "ALT", "ALT without nu^c, n = 3, rugby ball"),
    ("R3", "R", "ALT", True, 1, "ALT", "ALT + nu^c, n = 1, rugby ball"),
    ("R4", "R", "ALT", True, 2, "ALT", "ALT + nu^c, n = 2, rugby ball"),
    ("R5", "R", "ALT", True, 4, "ALT", "ALT + nu^c, n = 4, rugby ball"),
    ("R6", "R", "MAIN", True, 3, "A", "MAIN + nu^c, Higgs A, n = 3, rugby ball"),
]

RS2 = J(_S2, "RESULTS.md")
RALT = J(_S2, "RESULTS_alt.md")
RJF = J(_JF, "RESULTS.md")

# --- Job Two's two Dirac methods per flux charge x n (cached) ---
_round = {}


def round_modes(xn):
    if xn not in _round:
        cnt_b, chir_b, _, _ = MP.dirac_harmonic_basis(xn)
        fd, ms = MP.dirac_fd_count(xn, N=NFD_S, tau=TAU_FD)
        _round[xn] = (cnt_b, chir_b, fd, ms)
    return _round[xn]


def zero_mode_table(cid, kind, nu, n):
    """Per 6D field: N_Phi, counts (two methods), sigma3, 4D chirality, 4D left-handed field data."""
    rows, left = [], []
    for name, d3, a3, d2, Y, g7, x in content(kind, nu):
        N = convert("JobTwo", n, x)
        xn = x * n
        cnt_b, chir_b, fd, ms = round_modes(xn)
        sig = 1 if xn > 0 else -1
        fd_slot, fd_other = fd[sig], fd[-sig]
        ok_chir = all(abs(c - sig) < 1e-9 for c in chir_b)
        g5 = g7 * sig
        hand = "left" if g5 == -1 else "right"
        cnt = count_dirac(N)
        agree = (cnt_b == cnt == fd_slot) and fd_other == 0 and ok_chir
        rows.append(dict(name=name, d3=d3, a3=a3, d2=d2, Y=Y, g7=g7, x=x, N=N, cnt=cnt, cnt_b=cnt_b, fd=fd_slot,
                         fd_other=fd_other, sig=sig, hand=hand, agree=agree))
        if hand == "left":
            left.append((name, d3, a3, d2, Y, Fr(x), cnt))
        else:
            left.append((name + "^c", d3, -a3, d2, -Y, Fr(-x), cnt))
    return rows, left


def an_fields(left):
    return [(nm, ("3" if a3 > 0 else "3bar") if d3 == 3 else "1", d3, a3, d2) for nm, d3, a3, d2, Y, X, c in left]


def sums_4d(left):
    """Job Two's anomalies.py on the 4D left-handed content, times the copy number."""
    mults = {c for *_, c in left}
    assert len(mults) == 1, mults
    mult = mults.pop()
    flds = an_fields(left)
    Yd = {nm: sp.Rational(Y.numerator, Y.denominator) for nm, d3, a3, d2, Y, X, c in left}
    Xd = {nm: sp.Rational(X.numerator, X.denominator) for nm, d3, a3, d2, Y, X, c in left}
    sm = AN.coefficients(Yd, flds)
    sm = {k: sp.nsimplify(mult * v) for k, v in sm.items()}
    xs = AN.x_anomalies(Xd, Yd, flds, ngen=mult)
    wit = AN.witten_doublets(flds) * mult
    return sm, xs, wit, mult


def sixd_counts(kind, nu):
    Np = sum(d3 * d2 for nm, d3, a3, d2, Y, g7, x in content(kind, nu) if g7 == 1)
    Nm = sum(d3 * d2 for nm, d3, a3, d2, Y, g7, x in content(kind, nu) if g7 == -1)
    T3p = sum(d2 for nm, d3, a3, d2, Y, g7, x in content(kind, nu) if g7 == 1 and d3 == 3)
    T3m = sum(d2 for nm, d3, a3, d2, Y, g7, x in content(kind, nu) if g7 == -1 and d3 == 3)
    return Np, Nm, T3p, T3m


# --- cited values (read from the files at the cited lines) ---
def cited_alt_rows():
    out = {}
    for ln in range(30, 36):
        c = row_cells(RALT, ln)
        out[c[0]] = (int(c[5]), c[8])
    return out


def cited_main_rows():
    out = {}
    for ln in range(220, 226):
        c = row_cells(RS2, ln)
        nm = {"Q_L": "Q", "u_R": "u", "d_R": "d", "L_L": "L", "e_R": "e", "nu_R (optional)": "nu"}[c[0]]
        out[nm] = (int(c[6]), c[7])
    return out


def cited_count_table():
    out = {}
    for ln in range(16, 25):
        c = row_cells(RS2, ln)
        out[int(c[0])] = (int(c[3]), c[-1])
    return out


def cited_x_alt():
    out = {}
    for ln in range(67, 73):
        c = row_cells(RALT, ln)
        out[c[0]] = dict(pg_nu=sp.Rational(c[1]), pg_nonu=sp.Rational(c[2]), g3_nu=sp.Rational(c[3]), g3_nonu=sp.Rational(c[4]))
    return out


def cited_x_main():
    out = {}
    for ln in range(110, 116):
        c = row_cells(RS2, ln)
        out[c[0]] = dict(nonu=sp.Rational(c[1]), nu=sp.Rational(c[2]))
    return out


XKEY = {"SU(3)^2 X": "SU(3)^2 X", "SU(2)^2 X": "SU(2)^2 X", "Y^2 X": "Y^2 X", "Y X^2": "Y X^2", "X^3": "X^3", "grav^2 X": "grav^2 X"}


def cited_6d():
    c82, c83, c84 = row_cells(RALT, 82), row_cells(RALT, 83), row_cells(RALT, 84)
    m = cited(RS2, 122, r"net (\d+) Weyl \((\d+) with nu\^c\)")
    return dict(S1_net=int(c82[3]), S1_m=int(c82[1].split()[0]), S1_p=int(c82[2].split()[0]), S2_net=int(c83[3]),
                F4_m=int(c84[1].split()[0]), F4_p=int(c84[2].split()[0]), F4_net=int(c84[3]),
                main_nonu_mag=int(m.group(1)), main_nu_mag=int(m.group(2)))


def cited_scan():
    m62 = cited(RS2, 62, r"(\d+) assignments tested, (\d+) survive")
    m69 = cited(RS2, 69, r"(\d+) assignments tested, (\d+) survive")
    rows_nonu = [tuple(row_cells(RS2, ln)[1:6]) for ln in (66, 67)]
    rows_nu = [tuple(row_cells(RS2, ln)[1:7]) for ln in range(73, 86)]
    return (int(m62.group(1)), int(m62.group(2)), rows_nonu), (int(m69.group(1)), int(m69.group(2)), rows_nu)


CITE_ALT, CITE_MAIN, CITE_CT, CITE_XALT, CITE_XMAIN, CITE_6D = (cited_alt_rows(), cited_main_rows(), cited_count_table(),
                                                                cited_x_alt(), cited_x_main(), cited_6d())
CITE_SCAN = cited_scan()
cited(RS2, 166, r"sigma3 = \+1, i\.e\. both are 4D left-handed")       # S5: all left-handed (Assignment B)

# --- hypercharge scan (Job Two's anomalies.scan), compared with RESULTS lines 62-85 ---
scan_res = {}
for with_nu in (False, True):
    tested, checked, _ = AN.scan(with_nu)
    names = ["Q", "u^c", "d^c", "L", "e^c"] + (["nu^c"] if with_nu else [])
    rows = [tuple(fr(s[k]) for k in names) for s, A in checked]
    scan_res[with_nu] = (tested, len(checked), rows)
scan_ok = (scan_res[False][0] == CITE_SCAN[0][0] and scan_res[False][1] == CITE_SCAN[0][1]
           and sorted(scan_res[False][2]) == sorted(CITE_SCAN[0][2])
           and scan_res[True][0] == CITE_SCAN[1][0] and scan_res[True][1] == CITE_SCAN[1][1]
           and sorted(scan_res[True][2]) == sorted(CITE_SCAN[1][2]))

SDATA = {}
ca_items = []
for cid, fam, kind, nu, n, higgs, desc in CANDS:
    if fam != "S":
        continue
    rows, left = zero_mode_table(cid, kind, nu, n)
    sm, xs, wit, mult = sums_4d(left)
    Np, Nm, T3p, T3m = sixd_counts(kind, nu)
    SDATA[cid] = dict(rows=rows, left=left, sm=sm, xs=xs, wit=wit, mult=mult, Np=Np, Nm=Nm, T3p=T3p, T3m=T3m, kind=kind, nu=nu, n=n)
    # cited comparisons
    checks = []
    if kind == "ALT" and n == 3:
        for r in rows:
            cz, ch = CITE_ALT[r["name"]]
            checks.append(("count/chirality %s" % r["name"], (r["cnt"], r["hand"]) == (cz, ch), "RESULTS_alt line %d" % (30 + ["Q", "L", "u", "d", "e", "nu"].index(r["name"]))))
        key = "g3_nu" if nu else "g3_nonu"
        for k in XKEY:
            checks.append(("X sum %s" % k, xs[k] == CITE_XALT[k][key], "RESULTS_alt lines 67-72"))
    elif kind == "ALT":
        cz, ch = CITE_CT[n]
        for r in rows:
            exp_hand = "left" if (r["g7"] * (1 if n > 0 else -1)) == -1 else "right"
            checks.append(("count %s" % r["name"], r["cnt"] == cz and r["hand"] == exp_hand, "RESULTS line %d" % (16 + n + 4)))
        for k in XKEY:
            checks.append(("X sum %s" % k, xs[k] == n * CITE_XALT[k]["pg_nu"], "RESULTS_alt lines 67-72 (per generation x %d)" % n))
    elif kind == "MAIN":
        for r in rows:
            cz, ch = CITE_MAIN[r["name"]]
            checks.append(("count/chirality %s" % r["name"], (r["cnt"], r["hand"]) == (cz, ch), "RESULTS lines 220-225"))
        for k in XKEY:
            checks.append(("X sum %s" % k, xs[k] == CITE_XMAIN[k]["nu" if nu else "nonu"], "RESULTS lines 110-115"))
    elif kind == "S5":
        for r in rows:
            checks.append(("count/chirality %s" % r["name"], (r["cnt"], r["hand"]) == (3, "left"), "RESULTS lines 163-166"))
    # SM anomalies: cited zero for SM chirality (survivor rows); S5 computed new
    if kind != "S5":
        checks.append(("SM 4D anomaly sums = 0", all(v == 0 for v in sm.values()), "RESULTS line %d" % (74 if nu else 66)))
        checks.append(("hypercharge scan survivors", scan_ok, "RESULTS lines 62-85"))
    # 6D counts (E1 signs)
    net = Np - Nm
    if kind == "ALT":
        exp_net = CITE_6D["S1_net"] if nu else CITE_6D["S2_net"]
        checks.append(("tr R^4 net N+ - N- = %d" % exp_net, net == exp_net, "RESULTS_alt line %d" % (82 if nu else 83)))
        checks.append(("tr F^4 SU(3) count %d vs %d (build reproduction only, E2)" % (CITE_6D["F4_m"], CITE_6D["F4_p"]),
                       (T3m, T3p) == (CITE_6D["F4_m"], CITE_6D["F4_p"]), "RESULTS_alt line 84"))
    elif kind == "MAIN":
        exp_net = -(CITE_6D["main_nu_mag"] if nu else CITE_6D["main_nonu_mag"])
        checks.append(("tr R^4 net N+ - N- = %d (E1 sign on the file's magnitude)" % exp_net, net == exp_net, "RESULTS line 122"))
    for r in rows:
        checks.append(("methods agree %s (basis %d, FD %d, formula N_Phi %d, other slot %d)" % (r["name"], r["cnt_b"], r["fd"], r["cnt"], r["fd_other"]),
                       r["agree"], "[computed]"))
    SDATA[cid]["checks"] = checks
    ca_items += [(cid,) + c for c in checks]
CA_OK = all(c[2] for c in ca_items)
GRADE.append(("C-a", "S family: counts, chiralities, hypercharge survivors, U(1)_X sums and 6D counts equal the cited file values (%d checks)" % len(ca_items), CA_OK))

# ======================= per-count table (1.2) and C-d =======================
cd_items = []
pc_rows = []
for nn in range(-4, 5):
    N = convert("JobTwo", nn, 1)
    cz, ch = CITE_CT[nn]
    pc_rows.append(("Dirac, round S^2, charge 1", "Job Two n = %d" % nn, "JobTwo", N.value, "N_Phi", count_dirac(N), cz, "RESULTS line %d" % (20 + nn)))
# U1 Stage A rows
u1_lines = open(J(_U1, "RESULTS.md"), encoding="utf-8").read().splitlines()
u1_ok, u1_n = True, 0
for i in range(22, len(u1_lines)):
    ln = u1_lines[i]
    if not ln.startswith("| "):
        break
    c = [x.strip() for x in ln.strip().strip("|").split("|")]
    if not c[0].isdigit():
        continue
    Nn, nn, zm, npl, nmi = int(c[0]), int(c[1]), int(c[3]), int(c[4]), int(c[5])
    u1_n += 1
    u1_ok &= (zm == count_dirac(convert("U1", nn)) and npl == zm and nmi == 0)
u1_line = cited(J(_U1, "RESULTS.md"), 139, r"in all (\d+) sectors: True")
u1_ok &= (u1_n == int(u1_line.group(1)))
pc_rows.append(("Dirac, fuzzy sphere (U1)", "all Stage A rows (%d sectors, N = 4..20, n = 0..6)" % u1_n, "U1", "n", "N_Phi",
                "count = N_Phi in every row: %s" % yn(u1_ok), "exactly |n|, chirality +1", "U1 RESULTS lines 23-%d, 139" % (22 + u1_n + 1)))
jf106 = row_cells(RJF, 106)
N = convert("JobFour", 3, 1)
pc_rows.append(("Dirac, rugby ball (Job Four)", "n = 3, alpha = 1", "JobFour", N.value, "N_Phi", count_dirac(N), int(jf106[3]), "Job Four RESULTS line 106"))
b0_lines = open(J(_B0, "RESULTS.md"), encoding="utf-8").read().splitlines()
b0_ok = True
for ln in range(82, 100):
    c = [x.strip() for x in b0_lines[ln - 1].strip().strip("|").split("|")]
    nn = int(c[0])
    found = int(c[3].strip("[]").split(",")[0])
    N = convert("B0", nn)
    if ln in (82, 88, 94):
        pc_rows.append(("scalar lowest Landau level (B0)", "n = %d (all six eps rows)" % nn, "B0", N.value, "N_Phi + 1", count_scalar(N), found, "B0 RESULTS lines %d-%d" % (ln, ln + 5)))
    b0_ok &= (found == count_scalar(N))
lift85 = cited(J(OP, "JOB_LIFT_SPEC.md"), 85, r"2n − 1")
lift86 = cited(J(OP, "JOB_LIFT_SPEC.md"), 86, r"N_Φ − 1")
for nr in (1, 2, 3):
    N = convert("RW", nr)
    pc_rows.append(("g = 2 spin-1 lowest level (RW/LNW)", "n_RW = %d" % nr, "RW", N.value, "N_Phi - 1", count_spin1(N), 2 * nr - 1, "JOB_LIFT_SPEC lines 85-86 (2n - 1)"))
h200 = row_cells(RS2, 200)
h94 = row_cells(RALT, 94)
NA = convert("JobTwo", 3, 2)
N0 = convert("JobTwo", 3, 0)
pc_rows.append(("Higgs A_z cross-check (x = +2)", "Job Two n = 3, x = 2", "JobTwo", NA.value, "N_Phi - 1", count_spin1(NA), int(h200[3]), "RESULTS line 200"))
pc_rows.append(("ALT Higgs cross-check (x = 0)", "Job Two n = 3, x = 0", "JobTwo", N0.value, "N_Phi + 1", count_scalar(N0), int(h94[2]), "RESULTS_alt line 94"))
try:
    count_dirac(3)
    hard_stop = False
except ConventionError:
    hard_stop = True
pc_ok = all((r[5] == r[6]) for r in pc_rows if isinstance(r[5], int)) and u1_ok and b0_ok
cd_items.append(("per-count table reproduces every source count from N_Phi", pc_ok))
cd_items.append(("hard stop on an unconverted n (count_dirac(3) raises)", hard_stop))
cd_items.append(("Higgs rows: A_z 5 and ALT 1", count_spin1(NA) == int(h200[3]) == 5 and count_scalar(N0) == int(h94[2]) == 1))


# ======================= E4 sections (Venus) =======================
def pclass(q, s, m):
    """Map a section to the E4 'positive class' (q' >= 0, s' >= 0); negative charge = complex conjugate [identity]."""
    q, s, m = Fr(q), Fr(s), Fr(m)
    if q > 0 or (q == 0 and s >= 0 and m >= 0):
        return q, s, m, False
    return -q, -s, -m, True


def e4_m_sets(Nphi, s, alpha):
    """Regular and normalisable m sets for the E4 form with q = Nphi/2 >= 0, spin s >= 0 (positive class)."""
    q = Fr(Nphi, 2)
    lo, hi = -(Nphi + 4), Nphi + 4
    ms = [Fr(k) + s for k in range(lo, hi + 1)]
    reg = [m for m in ms if m / alpha - s >= 0 and (2 * q - m) / alpha - s >= 0]
    nrm = [m for m in ms if m / alpha - s + 1 > 0 and (2 * q - m) / alpha - s + 1 > 0]
    return reg, nrm


e4_rows = []
e4_ok = True
for s in SPINS:
    for Nphi in range(0 if s < 1 else 1, 7):
        N = convert("q", Fr(Nphi, 2))
        for al in ALPHAS:
            reg, nrm = e4_m_sets(Nphi, s, al)
            want = count_spin(N, s)
            ok = len(reg) == len(nrm) == want and reg == nrm
            e4_ok &= ok
            e4_rows.append((s, Nphi, al, len(reg), len(nrm), want, ok))
cd_items.append(("E4 counts N_Phi + 1 - 2s at every alpha (s = 0, 1/2, 1; N_Phi <= 6), bounded = normalisable (A5)", e4_ok))


# ======================= Stage 1b: R family with Job Four's solver =======================
JF_Q0 = JF.q


def jf_counts(qval, alpha, mrange):
    """Job Four's Mode (regularity, normalisability) and fd_rugby (FD of D^2) at flux charge q = qval (module global)."""
    JF.q = float(qval)
    try:
        al = float(alpha)
        modes = {(m, ch): JF.Mode(al, m, ch) for m in mrange for ch in (+1, -1)}
        allowed = sorted([md for md in modes.values() if md.allowed], key=lambda md: (md.chir, md.m))
        reg = sum(1 for md in modes.values() if md.regular)
        nrm = sum(1 for md in modes.values() if md.normalisable)
        fd = {+1: 0, -1: 0}
        zero_m = []
        for m in mrange:
            for ch in (+1, -1):
                d, e = JF.fd_rugby(m, NFD_R, ch, al)
                c = MP._sturm_count(d, e, TAU_FD)
                fd[ch] += c
                if c:
                    zero_m.append((m, ch, c))
        zmax, nz = 0.0, float("inf")
        for m, ch, c in zero_m:
            d, e = JF.fd_rugby(m, NFD_R, ch, al)
            zmax = max(zmax, MP._kth_eig(d, e, c - 1, lo=-5.0, hi=400.0))
            nz = min(nz, MP._kth_eig(d, e, c, lo=-5.0, hi=400.0))
        exps = [(md.chir, md.m, md.pN, md.pS) + md.exact_exponents() for md in allowed]
        exp_err = max([abs(a - c) for _, _, a, b, c, d in exps] + [abs(b - d) for _, _, a, b, c, d in exps] + [0.0])
        return dict(allowed=[(md.chir, Fr(md.m).limit_denominator(4)) for md in allowed], reg=reg, nrm=nrm, fd=fd,
                    zmax=zmax, nz=nz, exps=exps, exp_err=exp_err)
    finally:
        JF.q = JF_Q0


JF_MRANGE = [k + 0.5 for k in range(-5, 8)]        # Job Four's own m range (run.py line 189)
RDATA = {}
cb_items, cc_items = [], []
# R1/R2 (n = 3): reproduce Job Four RESULTS lines 106-109
for i, al in enumerate(ALPHA_GRID):
    r = jf_counts(JF_Q0, al, JF_MRANGE)
    RDATA[("ALT", 3, al)] = r
    c = row_cells(RJF, 106 + i)
    mine_m = ", ".join(fr(m) + ("" if ch > 0 else " (sigma3 = -1)") for ch, m in r["allowed"])
    ok = (float(c[0]) == float(al) and c[2] == mine_m and int(c[3]) == r["reg"] and int(c[4]) == r["nrm"]
          and int(c[5]) == r["fd"][+1] and int(c[6]) == r["fd"][-1] and len(r["allowed"]) == 3)
    cb_items.append((fr(al), c[2], mine_m, (int(c[3]), int(c[4]), int(c[5]), int(c[6])), (r["reg"], r["nrm"], r["fd"][+1], r["fd"][-1]),
                     (c[7], c[8]), ("%.4f" % r["zmax"], "%.4f" % r["nz"]), ok))
if alpha_ext is not None:
    RDATA[("ALT", 3, alpha_ext)] = jf_counts(JF_Q0, alpha_ext, JF_MRANGE)
CB_OK = all(x[-1] for x in cb_items)
GRADE.append(("C-b", "R1/R2 (n = 3) counts and m values equal Job Four RESULTS lines 106-109 exactly at every grid alpha; three methods agree", CB_OK))
# R3-R5 (n = 1, 2, 4), R6 singlets (q = -3/2)
for nphi in (1, 2, 4):
    for al in ALPHAS:
        mr = [k + 0.5 for k in range(-5 - nphi, nphi + 6)]
        r = jf_counts(Fr(nphi, 2), al, mr)
        RDATA[("ALT", nphi, al)] = r
        N = convert("JobFour", nphi, 1)
        want = count_dirac(N)
        ok = (len(r["allowed"]) == r["reg"] == r["nrm"] == r["fd"][+1] == want and r["fd"][-1] == 0
              and all(ch == +1 for ch, m in r["allowed"]))
        cc_items.append(("R%d" % {1: 3, 2: 4, 4: 5}[nphi], "n = %d, alpha = %s" % (nphi, fr(al)), want, len(r["allowed"]), r["reg"], r["nrm"],
                         r["fd"][+1], r["fd"][-1], ok))
for al in ALPHAS:
    mr = [k + 0.5 for k in range(-9, 6)]
    r = jf_counts(Fr(-3, 2), al, mr)
    RDATA[("MAINsing", 3, al)] = r
    N = convert("JobFour", 3, -1)
    want = count_dirac(N)
    ok = (len(r["allowed"]) == r["reg"] == r["nrm"] == r["fd"][-1] == want and r["fd"][+1] == 0
          and all(ch == -1 for ch, m in r["allowed"]))
    rq = RDATA[("ALT", 3, al)]
    okq = len(rq["allowed"]) == 3
    cc_items.append(("R6", "singlets x = -1 (q = -3/2), alpha = %s; doublets as R1 (%d modes)" % (fr(al), len(rq["allowed"])), want,
                     len(r["allowed"]), r["reg"], r["nrm"], r["fd"][-1], r["fd"][+1], ok and okq))


# ======================= Stage 1b-6: B1 on B0's backgrounds =======================
def b1_backgrounds():
    ns = B0NS
    out = {}
    for n in ns["N_LIST"]:
        prev = None
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
                out[(n, eps)] = (s, lw, R2, c1, mx, bool(s.success))
    return out


def b1_count(n, eps, bg):
    s, lw, R2, c1, mx, succ = bg
    ns = B0NS
    T = ns["T_BVP"]
    tt = np.linspace(-T, T, 40001)
    f2 = np.exp(lw(tt) + s.sol(tt)[0])
    B = 0.5 * (1.0 - f2)
    Om2 = R2 * ns["sech2"](tt)
    Aphi_in = cumulative_trapezoid(B * Om2, tt, initial=0.0)       # (1/2pi) flux enclosed from the north pole
    flux = float(Aphi_in[-1])
    tg = np.linspace(-40.0, 40.0, B1_NT)
    Aphi = np.interp(tg, tt, Aphi_in, left=0.0, right=flux)
    mr = [k + 0.5 for k in range(-4, n + 4)]
    res = []
    for m in mr:
        for ch in (+1, -1):
            lna = cumulative_trapezoid(ch * (m - Aphi), tg, initial=0.0)
            lnw = 2 * lna - np.log(np.cosh(tg))
            def lnZ(S):
                k = np.abs(tg) <= S
                mxw = lnw[k].max()
                return mxw + math.log(float(np.trapezoid(np.exp(lnw[k] - mxw), tg[k])))
            normal = abs(lnZ(40.0) - lnZ(20.0)) < NORM_TOL
            lpsi = 2 * lna + np.log(np.cosh(tg))
            th = 2 * np.arctan(np.exp(tg))
            i1, i2 = np.searchsorted(tg, -30.0), np.searchsorted(tg, -29.0)
            j1, j2 = np.searchsorted(tg, 29.0), np.searchsorted(tg, 30.0)
            pN = (lpsi[i2] - lpsi[i1]) / (math.log(th[i2]) - math.log(th[i1]))
            pS = (lpsi[j2] - lpsi[j1]) / (math.log(np.pi - th[j2]) - math.log(np.pi - th[j1]))
            regular = pN > REG_TOL and pS > REG_TOL
            res.append((m, ch, regular, normal, pN, pS))
    # FD of R^2 D^2, the same operator as Job Two / Job Four (-u'' + (W^2 +- W') u in theta, Dirichlet ends), on a grid uniform
    # in t = ln tan(theta/2) [post-hoc, development]: -d^2/dtheta^2 = -c d/dt (c d/dt), c = cosh t, weight dtheta = dt / c.
    # Symmetric generalised problem A u = lambda M u, M = diag(1/c); Sylvester inertia of A - lambda M counts eigenvalues < lambda.
    tf = np.arange(-B1_FD_T + B1_FD_H, B1_FD_T - B1_FD_H / 2, B1_FD_H)
    cc, cp, cm = np.cosh(tf), np.cosh(tf + B1_FD_H / 2), np.cosh(tf - B1_FD_H / 2)
    Af = np.interp(tf, tt, Aphi_in, left=0.0, right=flux)
    Bf = np.interp(tf, tt, B, left=B[0], right=B[-1])
    Minv = 1.0 / cc
    ef = -cp[:-1] / B1_FD_H ** 2

    def gen_eig(dd, k, lo=-5.0, hi=400.0, iters=60):
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            if MP._sturm_count(dd - mid * Minv, ef, 0.0) > k:
                hi = mid
            else:
                lo = mid
        return 0.5 * (lo + hi)

    fd = {+1: 0, -1: 0}
    zmax, nz = 0.0, float("inf")
    for m in mr:
        Wt = (m - Af) * cc
        Wpt = -R2 * Bf + (m - Af) * np.tanh(tf) * cc ** 2
        for ch in (+1, -1):
            V = Wt ** 2 + (Wpt if ch > 0 else -Wpt)
            dd = (cp + cm) / B1_FD_H ** 2 + V / cc
            c = MP._sturm_count(dd - TAU_FD * Minv, ef, 0.0)
            fd[ch] += c
            if c:
                zmax = max(zmax, gen_eig(dd, c - 1))
            nz = min(nz, gen_eig(dd, c))
    # report-only: the theta-uniform grid as in Job Four (N = NFD_R), which the box scratch run showed converges only like 1/ln N
    # for a mode with |psi|^2 ~ theta^0 at a pole when the flux is concentrated there
    Nth = NFD_R
    hth = math.pi / (Nth + 1)
    th = hth * np.arange(1, Nth + 1)
    sn, cs = np.sin(th), np.cos(th)
    tth = np.log(np.tan(th / 2))
    Ath = np.interp(tth, tt, Aphi_in, left=0.0, right=flux)
    Bth = np.interp(tth, tt, B, left=B[0], right=B[-1])
    fd_th = {+1: 0, -1: 0}
    for m in mr:
        W = (m - Ath) / sn
        Wp = -R2 * Bth - (m - Ath) * cs / sn ** 2
        for ch in (+1, -1):
            V = W ** 2 + (Wp if ch > 0 else -Wp)
            fd_th[ch] += MP._sturm_count(2.0 / hth ** 2 + V, -np.ones(Nth - 1) / hth ** 2, TAU_FD)
    reg = sum(1 for r in res if r[2])
    nrm = sum(1 for r in res if r[3])
    allowed = [(r[1], r[0]) for r in res if r[2] and r[3]]
    return dict(flux=flux, reg=reg, nrm=nrm, allowed=allowed, fd=fd, fd_th=fd_th, zmax=zmax, nz=nz, c1=c1, mx=mx, succ=succ)


B1BG = b1_backgrounds()
B1 = {}
for (n, eps), bg in sorted(B1BG.items()):
    r = b1_count(n, eps, bg)
    B1[(n, eps)] = r
    N = convert("B0", n)
    want = count_dirac(N)
    ok = (len(r["allowed"]) == r["reg"] == r["nrm"] == r["fd"][+1] == want and r["fd"][-1] == 0
          and all(ch == +1 for ch, m in r["allowed"]) and r["succ"] and r["c1"] < B0NS["C1_TOL"])
    cc_items.append(("B1", "n = %d, eps = %g" % (n, eps), want, len(r["allowed"]), r["reg"], r["nrm"], r["fd"][+1], r["fd"][-1], ok))
CC_OK = all(x[-1] for x in cc_items)
GRADE.append(("C-c", "R3-R5, R6 and B1: count = N_Phi and the three methods agree (%d rows; B1 is a build check, A8)" % len(cc_items), CC_OK))
CD_OK = all(ok for _, ok in cd_items)
GRADE.append(("C-d", "every count formed from N_Phi (1.2); hard stop on unconverted n; Higgs rows 5 and 1; E4 counts (A5)", CD_OK))


# ======================= Stage 1b-8: overlaps on the E4 sections =======================
_GLC = {}


def glt(n):
    if n not in _GLC:
        x, wt = np.polynomial.legendre.leggauss(n)
        _GLC[n] = (TQ * x, TQ * wt)
    return _GLC[n]


def lnrad(qc, sc, mc, alpha, t):
    """ln of the E4 radial factor in t = ln tan(theta/2), positive class (q', s', m'); sin(theta) = sech t."""
    a = float(alpha)
    lsech = -np.logaddexp(t, -t) + math.log(2.0)
    return -float(sc) * (math.log(a) + lsech) + float(mc - qc) / a * t + float(qc) / a * lsech


def norm_closed(qc, sc, mc, alpha):
    a = mpm.mpf(alpha.numerator) / alpha.denominator
    s, q, m = [mpm.mpf(x.numerator) / x.denominator for x in (sc, qc, mc)]
    return 2 * mpm.pi * a ** (1 - 2 * s) * mpm.power(2, 1 - 2 * s + 2 * q / a) * mpm.beta(m / a - s + 1, (2 * q - m) / a - s + 1)


def triple_closed_radial(cls, alpha):
    a = mpm.mpf(alpha.numerator) / alpha.denominator
    S = sum(mpm.mpf(c[1].numerator) / c[1].denominator for c in cls)
    Q = sum(mpm.mpf(c[0].numerator) / c[0].denominator for c in cls)
    M = sum(mpm.mpf((c[2] - c[0]).numerator) / (c[2] - c[0]).denominator for c in cls)
    return 2 * mpm.pi * a ** (1 - S) * mpm.power(2, 1 - S + Q / a) * mpm.beta((-S + (Q + M) / a) / 2 + 1, (-S + (Q - M) / a) / 2 + 1)


def lsech_t(t):
    return -np.logaddexp(t, -t) + math.log(2.0)


def quad_norm(c, alpha, n):
    t, wt = glt(n)
    lw = 2 * lnrad(*c, alpha, t) + math.log(float(alpha)) + 2 * lsech_t(t)
    mx = lw.max()
    return 2 * math.pi * math.exp(mx) * float(np.sum(wt * np.exp(lw - mx)))


def quad_triple(cls, alpha, n):
    t, wt = glt(n)
    lw = sum(lnrad(*c, alpha, t) for c in cls) + math.log(float(alpha)) + 2 * lsech_t(t)
    mx = lw.max()
    return 2 * math.pi * math.exp(mx) * float(np.sum(wt * np.exp(lw - mx)))


def sec(N, s, m):
    """section label (q, s, m) with q = N/2 (signed), s signed, m in Z + s; returns positive class."""
    return pclass(Fr(N, 2), s, m)


def regular_class(c, alpha):
    q, s, m = c[:3]
    return m / alpha - s >= 0 and (2 * q - m) / alpha - s >= 0


def C_alpha(a, b, c, alpha, n=NQ):
    """C = ∫ psi_a psi_b conj(psi_c) dA / (|a||b||c|); a, b, c are (N, s, m) with signed N and s.

    Returns (closed form, quadrature, m-rule holds). The phi integral is 2 pi delta(m_a + m_b - m_c)."""
    ca, cb, cc = sec(*a), sec(*b), sec(*c)
    for x in (ca, cb, cc):
        assert regular_class(x, alpha), (a, b, c, alpha)
    ok_m = a[2] + b[2] == c[2]
    nrm_c = mpm.sqrt(norm_closed(*ca[:3], alpha) * norm_closed(*cb[:3], alpha) * norm_closed(*cc[:3], alpha))
    nrm_q = math.sqrt(quad_norm(ca[:3], alpha, n) * quad_norm(cb[:3], alpha, n) * quad_norm(cc[:3], alpha, n))
    if not ok_m:
        # O-c: the phi sum with NPH points times the radial quadrature
        ph = 2 * math.pi * np.arange(NPH) / NPH
        ang = abs(np.sum(np.exp(1j * float(a[2] + b[2] - c[2]) * ph)) / NPH)
        return 0.0, ang * quad_triple([ca[:3], cb[:3], cc[:3]], alpha, n) / nrm_q, False
    cf = triple_closed_radial([ca[:3], cb[:3], cc[:3]], alpha) / nrm_c
    return float(cf), quad_triple([ca[:3], cb[:3], cc[:3]], alpha, n) / nrm_q, True


def allowed_m(N, s):
    """zero-mode / lowest-level m set (positive N, s >= 0); alpha-independent for alpha <= 1 (A5)."""
    return [Fr(k) + s for k in range(-N - 2, N + 3) if s <= Fr(k) + s <= N - s]


OV_ROWS = []          # (table, label, {alpha: (closed, quad, quad_check)})
ob_worst, oc_worst, od_worst = 0.0, 0.0, 0.0
H, F2 = Fr(1, 2), Fr(1)


def ov_entry(table, label, a, b, c):
    global ob_worst, oc_worst
    vals = {}
    for al in ALPHAS:
        cf, qd, okm = C_alpha(a, b, c, al)
        _, qd2, _ = C_alpha(a, b, c, al, NQ_CHECK)
        if okm:
            rel = abs(qd - cf) / abs(cf)
            ob_worst = max(ob_worst, rel)
        else:
            oc_worst = max(oc_worst, abs(qd), abs(qd2))
        vals[al] = (cf, qd, qd2, okm)
    OV_ROWS.append((table, label, a, b, c, vals))
    return vals


# (a) Gram row: conj(psi_Q) H psi_u, constant Higgs (N = 0, s = 0, m = 0); also m-violating entries (O-c)
for Nf in (1, 2, 3, 4):
    ms = allowed_m(Nf, H)
    for mq in ms:
        for mu in ms:
            v = ov_entry("a", "N_Phi = %d: H(0,0,0) x psi_u(m = %s) -> psi_Q(m = %s)" % (Nf, fr(mu), fr(mq)), (0, Fr(0), Fr(0)), (Nf, H, mu), (Nf, H, mq))
            if mq == mu:
                for al in ALPHAS:
                    od_worst = max(od_worst, abs(v[al][0] - 1 / math.sqrt(4 * math.pi * float(al))), abs(v[al][1] - 1 / math.sqrt(4 * math.pi * float(al))))
# Job Four lines 16-19: cited singular values
jf_sv_ok = True
for i, al in enumerate(ALPHA_GRID):
    c = row_cells(RJF, 16 + i)
    sv = [float(x) for x in c[2].split(",")]
    jf_sv_ok &= all(abs(x - 1 / math.sqrt(4 * math.pi * float(al))) < 5e-13 for x in sv) and float(c[0]) == float(al)

# (b) MAIN-A closure: psi_H (N = 6, s = 1) x psi_R (N = -3, s = -1/2) -> psi_L (N = 3, s = 1/2)
for mh in allowed_m(6, F2):
    for mr in [-x for x in allowed_m(3, H)]:
        ml = mh + mr
        if ml in allowed_m(3, H):
            ov_entry("b", "H(m = %s) x R(m = %s) -> L(m = %s)" % (fr(mh), fr(mr), fr(ml)), (6, F2, mh), (-3, -H, mr), (3, H, ml))
# a few m-violating MAIN-A entries for O-c
for mh, mr, ml in [(Fr(3), Fr(-3, 2), Fr(1, 2)), (Fr(2), Fr(-1, 2), Fr(5, 2))]:
    ov_entry("b", "m-violating: H(m = %s) x R(m = %s) -> L(m = %s)" % (fr(mh), fr(mr), fr(ml)), (6, F2, mh), (-3, -H, mr), (3, H, ml))

# (c) general fusion table, N_1 + N_2 = N_3 <= NPHI_TABLE_MAX, spin closure s_1 + s_2 = s_3
COMBOS = [(Fr(0), Fr(0)), (Fr(0), H), (Fr(0), F2), (H, H)]
for s1, s2 in COMBOS:
    s3 = s1 + s2
    for N1 in range(1, NPHI_TABLE_MAX + 1):
        for N2 in range(1, NPHI_TABLE_MAX + 1 - N1):
            if s1 == s2 and N1 > N2:
                continue
            if N1 + 1 - 2 * s1 <= 0 or N2 + 1 - 2 * s2 <= 0:
                continue
            for m1 in allowed_m(N1, s1):
                for m2 in allowed_m(N2, s2):
                    m3 = m1 + m2
                    assert m3 in allowed_m(N1 + N2, s3)
                    ov_entry("c", "(%d, s %s, m %s) x (%d, s %s, m %s) -> (%d, s %s, m %s)" % (N1, fr(s1), fr(m1), N2, fr(s2), fr(m2), N1 + N2, fr(s3), fr(m3)),
                             (N1, s1, m1), (N2, s2, m2), (N1 + N2, s3, m3))


# O-a: alpha = 1 against Job Two's exact wigner_3j rows (RESULTS lines 139-144)
def yphase(Q, mJ):
    """Y_north(Q, |Q|, mJ) = c * normalised scalar E4 section (Q, m = mJ + Q) at alpha = 1; returns c (checked at two theta)."""
    Q, mJ = Fr(Q), Fr(mJ)
    cs = sec(2 * Q, Fr(0), mJ + Q)
    nm = math.sqrt(float(norm_closed(*cs[:3], Fr(1))))
    out = []
    for th in (0.7, 1.9):
        t = math.log(math.tan(th / 2))
        psi = math.exp(float(lnrad(*cs[:3], Fr(1), np.array([t]))[0])) / nm
        y = complex(MP.Y_north(float(Q), float(abs(Q)), float(mJ), np.array([th]), np.array([0.0]))[0])
        out.append(y / psi)
    return out[0], abs(out[0] - out[1])


oa_rows = []
oa_ok = True
for ln in range(139, 145):
    c = row_cells(RS2, ln)
    lab = [Fr(x.strip()) for x in c[0].split(",")]
    q1, l1, m1, q2, l2, m2, q3, l3, m3 = lab
    exact = OV.triple_exact(q1, l1, m1, q2, l2, m2, q3, l3, m3)
    ex = complex(sp.N(exact, 30))
    cited_val = float(c[2])
    # mine: C(psi_2, psi_3 -> psi_1) with scalar sections at alpha = 1
    a, b, cc = (2 * q2, Fr(0), m2 + q2), (2 * q3, Fr(0), m3 + q3), (2 * q1, Fr(0), m1 + q1)
    cf, qd, okm = C_alpha(a, b, cc, Fr(1))
    p1, e1 = yphase(q1, m1)
    p2, e2 = yphase(q2, m2)
    p3, e3 = yphase(q3, m3)
    mine = (p1.conjugate() * p2 * p3) * cf if okm else qd
    dif = abs(mine - ex)
    ok = dif <= OA_TOL and abs(cited_val - ex.real) <= 5e-13 and max(e1, e2, e3) <= OA_TOL and abs(abs(p1) - 1) < 1e-12
    oa_ok &= ok
    oa_rows.append((c[0], str(exact), ex.real, mine, dif, max(e1, e2, e3), ok))

# report-only: MAIN-A at alpha = 1 against Job Two's Assignment A entries (OV.triple_exact with the phases)
mainA_cmp = 0.0
for table, label, a, b, c, vals in OV_ROWS:
    if table != "b" or not vals[Fr(1)][3]:
        continue
    (Nh, sh, mh), (Nr, sr, mr), (Nl, sl, ml) = a, b, c
    QH, QR, QL = Fr(Nh, 2) - sh, Fr(Nr, 2) - sr, Fr(Nl, 2) - sl
    mJH, mJR, mJL = mh - Fr(Nh, 2), mr - Fr(Nr, 2), ml - Fr(Nl, 2)
    ex = complex(sp.N(OV.triple_exact(QL, abs(QL), mJL, QH, abs(QH), mJH, QR, abs(QR), mJR), 30))
    pL, _ = yphase(QL, mJL)
    pH, _ = yphase(QH, mJH)
    pR, _ = yphase(QR, mJR)
    mainA_cmp = max(mainA_cmp, abs(pL.conjugate() * pH * pR * vals[Fr(1)][0] - ex))

OA_OK, OB_OK, OC_OK, OD_OK = oa_ok, ob_worst <= OB_TOL, oc_worst <= OC_TOL, (od_worst <= OD_TOL and jf_sv_ok)
GRADE.append(("O-a", "alpha = 1 overlaps reproduce Job Two's exact wigner_3j rows (RESULTS lines 139-144) to %g absolute" % OA_TOL, OA_OK))
GRADE.append(("O-b", "quadrature vs closed form, every m-conserving entry at every alpha, <= %g relative" % OB_TOL, OB_OK))
GRADE.append(("O-c", "entries that break the m rule <= %g" % OC_TOL, OC_OK))
GRADE.append(("O-d", "constant-Higgs Gram row = 1/sqrt(4 pi alpha) at every grid alpha to %g (Job Four RESULTS lines 16-19)" % OD_TOL, OD_OK))


# ======================= Stage 1b-9/1b-10: I6 and I8 (E1-E3) =======================
t3, c3, t2, fY, fX, r2, r4, p1 = sp.symbols("t3 c3 t2 fY fX r2 r4 p1")
TR3 = {0: None, 1: 0, 2: t3, 3: None, 4: t3 ** 2 / 2}     # tr over a triplet; [identity] tr F^4 = (tr F^2)^2 / 2 for SU(3) (E2)
TR2 = {0: None, 1: 0, 2: t2, 3: 0, 4: t2 ** 2 / 2}        # SU(2): no cubic Casimir; same identity (E2)


def trF(k, d3, a3, d2, Y, X):
    c = sp.Rational(Y.numerator, Y.denominator) * fY + sp.Rational(X.numerator, X.denominator) * fX
    tot = 0
    for i in range(k + 1):
        for j in range(k + 1 - i):
            l = k - i - j
            if d3 == 1 and i > 0:
                continue
            if d2 == 1 and j > 0:
                continue
            a = d3 if i == 0 else (a3 * c3 if i == 3 else TR3[i])
            b = d2 if j == 0 else TR2[j]
            tot += sp.factorial(k) / (sp.factorial(i) * sp.factorial(j) * sp.factorial(l)) * a * b * c ** l
    return sp.expand(tot)


def I6_poly(left):
    tot = 0
    for nm, d3, a3, d2, Y, X, mult in left:
        tot += mult * (sp.Rational(1, 6) * trF(3, d3, a3, d2, Y, X) - sp.Rational(1, 24) * p1 * trF(1, d3, a3, d2, Y, X))
    return sp.Poly(sp.expand(tot), t3, c3, t2, fY, fX, p1)


def I8_poly(kind, nu):
    tot = 0
    for nm, d3, a3, d2, Y, g7, x in content(kind, nu):
        d = d3 * d2
        tot += g7 * (sp.Rational(d, 5760) * (r4 + sp.Rational(5, 4) * r2 ** 2) - r2 * trF(2, d3, a3, d2, Y, Fr(x)) / 96
                     + trF(4, d3, a3, d2, Y, Fr(x)) / 24)
    return sp.expand(tot)


I6_MONO = {(1, 0, 0, 0, 1, 0): ("t3 fX", "1/2 x SU(3)^2 X"), (0, 0, 1, 0, 1, 0): ("t2 fX", "1/2 x SU(2)^2 X"),
           (0, 0, 0, 2, 1, 0): ("fY^2 fX", "1/2 x Y^2 X"), (0, 0, 0, 1, 2, 0): ("fY fX^2", "1/2 x Y X^2"),
           (0, 0, 0, 0, 3, 0): ("fX^3", "1/6 x X^3"), (0, 0, 0, 0, 1, 1): ("p1 fX", "-1/24 x grav^2 X"),
           (1, 0, 0, 1, 0, 0): ("t3 fY", "1/2 x SU(3)^2 U(1)"), (0, 0, 1, 1, 0, 0): ("t2 fY", "1/2 x SU(2)^2 U(1)"),
           (0, 0, 0, 3, 0, 0): ("fY^3", "1/6 x U(1)^3"), (0, 0, 0, 1, 0, 1): ("p1 fY", "-1/24 x grav^2 U(1)"),
           (0, 1, 0, 0, 0, 0): ("c3", "1/6 x SU(3)^3")}


def i6_expected(sm, xs):
    h, s6, m24 = sp.Rational(1, 2), sp.Rational(1, 6), sp.Rational(-1, 24)
    return {(1, 0, 0, 0, 1, 0): h * xs["SU(3)^2 X"], (0, 0, 1, 0, 1, 0): h * xs["SU(2)^2 X"], (0, 0, 0, 2, 1, 0): h * xs["Y^2 X"],
            (0, 0, 0, 1, 2, 0): h * xs["Y X^2"], (0, 0, 0, 0, 3, 0): s6 * xs["X^3"], (0, 0, 0, 0, 1, 1): m24 * xs["grav^2 X"],
            (1, 0, 0, 1, 0, 0): h * sm["SU(3)^2 U(1)"], (0, 0, 1, 1, 0, 0): h * sm["SU(2)^2 U(1)"], (0, 0, 0, 3, 0, 0): s6 * sm["U(1)^3"],
            (0, 0, 0, 1, 0, 1): m24 * sm["grav^2 U(1)"], (0, 1, 0, 0, 0, 0): s6 * sm["SU(3)^3"]}


def factorise(I8):
    """Report-only: try I8 = X4 ^ X4~ (only meaningful when tr R^4 and tr F^3_SU(3) F terms vanish)."""
    P = sp.Poly(I8, r4, c3)
    if P.degree(r4) > 0:
        return "irreducible tr R^4 left over: no factorisation (Q16 reject at Part B's consistency gate)"
    if P.degree(c3) > 0:
        return "tr F^3_SU(3) F_U(1) terms present (independent cubic Casimir): no factorisation"
    lam = sp.Symbol("lam")
    v = [r2, t3, t2, fY ** 2, fY * fX, fX ** 2]
    A = sp.zeros(6, 6)
    poly = sp.Poly(I8, r2, t3, t2, fY, fX)
    def put(i, j, val):
        if i == j:
            A[i, i] += val
        else:
            A[i, j] += val / 2
            A[j, i] += val / 2
    deg = lambda i: {0: (1, 0, 0, 0, 0), 1: (0, 1, 0, 0, 0), 2: (0, 0, 1, 0, 0), 3: (0, 0, 0, 2, 0), 4: (0, 0, 0, 1, 1), 5: (0, 0, 0, 0, 2)}[i]
    used = set()
    for mono, coeff in poly.terms():
        if mono == (0, 0, 0, 2, 2):
            put(3, 5, coeff - lam)
            put(4, 4, lam)
            used.add(mono)
            continue
        hit = False
        for i in range(6):
            for j in range(i, 6):
                if tuple(a + b for a, b in zip(deg(i), deg(j))) == mono:
                    put(i, j, coeff)
                    hit = True
                    break
            if hit:
                break
        if not hit:
            return "monomial %s is not a product of two 4-forms: no factorisation" % str(mono)
    minors = [A.extract(list(r), list(c)).det() for r in itertools.combinations(range(6), 3) for c in itertools.combinations(range(6), 3)]
    minors = [sp.expand(m) for m in minors if sp.expand(m) != 0]
    if not minors:
        sols = [sp.Integer(0)]
    else:
        g = minors[0]
        for m in minors[1:]:
            g = sp.gcd(g, m)
        sols = [s for s in sp.solve(g, lam)] if g.free_symbols else []
        sols = [s for s in sols if all(sp.simplify(m.subs(lam, s)) == 0 for m in minors)]
    if not sols:
        return "no factorisation (rank of the 4-form quadratic form > 2 for every split of the fY^2 fX^2 term)"
    A0 = A.subs(lam, sols[0])
    quad = sp.expand((sp.Matrix([v]) * A0 * sp.Matrix(v))[0])
    if sp.expand(quad - I8) != 0:
        return "internal check failed: the quadratic form does not reproduce I8 (no statement)"
    fac = sp.factor(quad)
    rk = A0.rank()
    if rk == 0:
        return "I8 = 0 identically"
    nfac = [f for f, k in sp.factor_list(sp.expand((sp.Matrix([v]) * A0 * sp.Matrix(v))[0]))[1] if f.free_symbols]
    if rk == 1:
        return "factorises (rank 1, a perfect square): I8 = %s" % fac
    if rk == 2 and len(nfac) >= 2:
        return "factorises over Q (rank 2): I8 = %s" % fac
    ev = np.linalg.eigvalsh(np.array(A0.evalf(30).tolist(), dtype=float))
    ev = [x for x in ev if abs(x) > 1e-12]
    if ev[0] * ev[1] < 0:
        return "factorises over R but not over Q (rank 2, eigenvalues %.6g, %.6g); sympy factor: %s" % (ev[0], ev[1], fac)
    return "rank 2 with same-sign eigenvalues: the factors are complex conjugates (no real Green-Schwarz factorisation); sympy factor: %s" % fac


ANOM = {}
aa_ok, ab_items = True, []
AB_EXPECT = {"S1": CITE_6D["S1_net"], "S2": CITE_6D["S2_net"], "S3": -CITE_6D["main_nu_mag"], "S4": -CITE_6D["main_nonu_mag"]}
I8_cache = {}
for cid, fam, kind, nu, n, higgs, desc in CANDS:
    rows, left = zero_mode_table(cid, kind, nu, n)
    sm, xs, wit, mult = sums_4d(left)
    P6 = I6_poly(left)
    exp6 = i6_expected(sm, xs)
    got = {m: c for m, c in P6.terms()}
    extra = [m for m in got if m not in I6_MONO]
    ok6 = not extra and all(sp.nsimplify(got.get(m, 0) - exp6[m]) == 0 for m in I6_MONO)
    aa_ok &= ok6
    key = (kind, nu)
    if key not in I8_cache:
        I8 = I8_poly(kind, nu)
        I8_cache[key] = (I8, factorise(I8))
    I8, fac = I8_cache[key]
    net = sp.Poly(I8, r4).coeff_monomial(r4) * 5760
    Np, Nm, T3p, T3m = sixd_counts(kind, nu)
    assert net == Np - Nm
    if cid in AB_EXPECT:
        ab_items.append((cid, int(net), AB_EXPECT[cid], int(net) == AB_EXPECT[cid]))
    ANOM[cid] = dict(P6=P6, got=got, exp6=exp6, ok6=ok6, extra=extra, I8=I8, fac=fac, net=int(net), T3p=T3p, T3m=T3m, mult=mult, sm=sm, xs=xs, wit=wit, kind=kind, nu=nu)
AA_OK = aa_ok
AB_OK = all(x[-1] for x in ab_items)
GRADE.append(("A-a", "I6 coefficients (independent sympy expansion of [A-hat tr e^F]_6) equal the Stage 1 sums after the E3 map, every candidate", AA_OK))
GRADE.append(("A-b", "tr R^4 net N+ - N- reproduces S1 %d, S2 %d, S3 %d, S4 %d (E1)" % tuple(AB_EXPECT[k] for k in ("S1", "S2", "S3", "S4")), AB_OK))

# E2 identity check on random elements (report-only)
rng = np.random.default_rng(20261008)
def rand_herm_traceless(N):
    A = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
    Hm = (A + A.conj().T) / 2
    return Hm - np.trace(Hm) / N * np.eye(N)
E2_CHECK = {}
for N in (2, 3, 4):
    errs = []
    for _ in range(20):
        Fm = rand_herm_traceless(N)
        f2 = np.trace(Fm @ Fm).real
        f4 = np.trace(Fm @ Fm @ Fm @ Fm).real
        errs.append(abs(f4 - f2 ** 2 / 2) / f2 ** 2)
    E2_CHECK[N] = max(errs)

# A2 descent identity: int K dA = 4 pi alpha (smooth part) + 2 x 2 pi (1 - alpha) (tips) = 4 pi, exact
al_s = sp.Symbol("alpha", positive=True)
th_s = sp.Symbol("theta")
K_smooth = sp.integrate(1 / al_s * al_s * sp.sin(th_s), (th_s, 0, sp.pi)) * 2 * sp.pi * al_s   # K = 1, dA = alpha sin dth dph (unit radius)
DESCENT = sp.simplify(K_smooth + 2 * 2 * sp.pi * (1 - al_s))

# report-only: gaugino variant tr R^4 shift (A9): 8 + 3 + 1 + 1 = 13 adjoint Weyl fermions, either Gamma7
N_GAUGINI = 8 + 3 + 1 + 1


# ======================= report-only: tip-flux delta at the north tip (A3) =======================
def tipflux_counts(Nphi, s, alpha, delta):
    q = Fr(Nphi, 2)
    ms = [Fr(k) + s for k in range(-Nphi - 4, Nphi + 5)]
    reg = [m for m in ms if (m - delta) / alpha - s >= 0 and (2 * q - m) / alpha - s >= 0]
    nrm = [m for m in ms if (m - delta) / alpha - s + 1 > 0 and (2 * q - m) / alpha - s + 1 > 0]
    return len(reg), len(nrm)


TIPFLUX = [(d, al) + tipflux_counts(3, H, al, d) for d in (Fr(0), Fr(1, 4), Fr(1, 2), Fr(1)) for al in ALPHAS]


# ======================= write CANDIDATES.md =======================
def e(x):
    return "%.3e" % x


C = "CANDIDATES"
w(C, "# SM1 Part A - CANDIDATES (generated by run.py; do not edit by hand)")
w(C, "")
w(C, "Spec JOB_SM1A_SPEC.md %s. n convention (spec 1.2, A7 [Venus]): N_Phi = |x| (1/2pi) int F = 2|q|; Dirac count N_Phi, "
  "scalar lowest level N_Phi + 1, g = 2 spin-1 lowest level N_Phi - 1. Every count below is formed from an N_Phi object built by "
  "convert(); a raw n raises ConventionError (tested in C-d)." % SPEC_HASH)
w(C, "")
w(C, "Alpha grid [assumed]: %s%s. Counts and anomalies do not depend on alpha for alpha <= 1 (A2, A5 [Venus]); only tip exponents, "
  "wavefunctions and overlaps carry alpha." % (", ".join(fr(a) for a in ALPHA_GRID), "" if alpha_ext is None else "; alpha_ext = %s [Akitti]" % fr(alpha_ext)))
w(C, "")
w(C, "## Candidate table (16 rows)")
w(C, "")
w(C, "| id | geometry, alpha | assignment | N_Phi per 6D field (convention) | zero modes per field | 4D chirality | 4D left-handed content: Y | U(1)_X sums (SU3^2X, SU2^2X, Y^2X, YX^2, X^3, grav^2X) | SM 4D sums (SU3^2Y, SU2^2Y, Y^3, grav^2Y, SU3^3), Witten doublets | 6D: N+ , N-, tr R^4 net N+ - N-; triplets G7=-1 vs +1 | status |")
w(C, "|---|---|---|---|---|---|---|---|---|---|---|")
for cid, fam, kind, nu, n, higgs, desc in CANDS:
    rows, left = zero_mode_table(cid, kind, nu, n)
    sm, xs, wit, mult = sums_4d(left)
    A = ANOM[cid]
    geo = "round S^2, alpha = 1" if fam == "S" else "rugby ball, alpha in {%s}" % ", ".join(fr(a) for a in ALPHAS)
    nphi = ", ".join("%s %d" % (r["name"], r["N"].value) for r in rows) + " (Job Two n = %d, N_Phi = |x| n)" % n
    if fam == "S":
        zm = ", ".join("%s %d" % (r["name"], r["cnt"]) for r in rows)
        st = "[computed] recomputed with Job Two's monopole.py/anomalies.py; cited checks: %s" % pf(all(c[1] for c in SDATA[cid]["checks"]))
    else:
        if kind == "ALT":
            ok = all(len(RDATA[("ALT", n, al)]["allowed"]) == n for al in ALPHAS)
            zm = "every field %s at every grid alpha (sigma3 = +1 slot)" % (n if ok else "MISMATCH")
        else:
            ok = all(len(RDATA[("ALT", 3, al)]["allowed"]) == 3 and len(RDATA[("MAINsing", 3, al)]["allowed"]) == 3 for al in ALPHAS)
            zm = "Q, L 3 (sigma3 = +1); u, d, e, nu 3 (sigma3 = -1) at every grid alpha" if ok else "MISMATCH"
        st = "[computed] Job Four's solver (C-%s); 4D content as the round case [identity: zero-mode content]" % ("b" if cid in ("R1", "R2") else "c")
    chir = ", ".join("%s %s" % (r["name"], r["hand"]) for r in rows)
    lc = ", ".join("%s %s" % (nm, fr(Y)) for nm, d3, a3, d2, Y, X, c in left)
    xsum = ", ".join(fr(xs[k]) for k in XKEY)
    smsum = ", ".join(fr(sm[k]) for k in ("SU(3)^2 U(1)", "SU(2)^2 U(1)", "U(1)^3", "grav^2 U(1)", "SU(3)^3")) + "; Witten %d" % wit
    Np_, Nm_, _, _ = sixd_counts(kind, nu)
    six = "%d, %d, net %d; triplets %d vs %d" % (Np_, Nm_, A["net"], A["T3m"], A["T3p"])
    w(C, "| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (cid, geo, desc, nphi, zm, chir, lc, xsum, smsum, six, st))
w(C, "| B1 | round S^2 with B0's vortex background (n = %s; eps = %s) | unit-charge minimally coupled Dirac fermion in flux n | N_Phi = n (B0 convention) | n at every (n, eps) (C-c) | sigma3 = +1 slot (4D chirality set by the 6D Gamma7, not assigned) | n/a (no SM charges) | n/a | n/a | n/a | [identity: index theorem; independent of phi] (A8 [Venus]); build check only |" % (
    ", ".join(str(x) for x in B0NS["N_LIST"]), ", ".join("%g" % x for x in B0NS["EPS_LIST"])))
w(C, "")
w(C, "S5 is computed new here (1b-2): its 4D content is all left-handed, so the SM sums are those of Q, L, u, d, e, nu as left-handed fields (no conjugation).")
w(C, "")
w(C, "## Stage 1 cited comparisons (C-a)")
w(C, "")
w(C, "| candidate | check | recomputed = cited | cited at |")
w(C, "|---|---|---|---|")
for cid, nm, ok, where in ca_items:
    w(C, "| %s | %s | %s | %s |" % (cid, nm, yn(ok), where))
w(C, "")
w(C, "Hypercharge scan (Job Two's anomalies.scan): without nu^c %d tested, %d survive; with nu^c %d tested, %d survive. Cited (RESULTS lines 62, 69): %d/%d and %d/%d; survivor rows equal: %s." % (
    scan_res[False][0], scan_res[False][1], scan_res[True][0], scan_res[True][1], CITE_SCAN[0][0], CITE_SCAN[0][1], CITE_SCAN[1][0], CITE_SCAN[1][1], yn(scan_ok)))
w(C, "")
w(C, "## R family on the grid (1b-3, 1b-4, 1b-5)")
w(C, "")
w(C, "### R1/R2 (n = 3) against Job Four RESULTS lines 106-109 (C-b)")
w(C, "")
w(C, "| alpha | cited m | recomputed m | cited (reg, norm, FD+, FD-) | recomputed | cited (largest FD zero eig, smallest nonzero) | recomputed | equal |")
w(C, "|---|---|---|---|---|---|---|---|")
for x in cb_items:
    w(C, "| %s | %s | %s | %s | %s | %s | %s | %s |" % (x[:-1] + (yn(x[-1]),)))
w(C, "")
w(C, "The FD eigenvalue columns are printed for comparison only; C-b grades the counts and m values.")
w(C, "")
w(C, "### R3-R5, R6 and B1 (C-c): count = N_Phi, three methods")
w(C, "")
w(C, "| candidate | case | N_Phi count | allowed (reg and norm) | regular | normalisable | FD in the slot | FD other slot | agree |")
w(C, "|---|---|---|---|---|---|---|---|---|")
for x in cc_items:
    w(C, "| %s | %s | %d | %d | %d | %d | %d | %d | %s |" % (x[:-1] + (yn(x[-1]),)))
w(C, "")
w(C, "R6: the singlets sit at x = -1 (q = -3/2), so their modes are in the sigma3 = -1 slot; the doublets are the R1 modes. R6's Higgs spectrum on the rugby ball stays [open].")
w(C, "")
w(C, "### Tip exponents per alpha (|psi|^2 ~ theta^p_N at the north tip, u^p_S at the south; s = 1/2 case of A5) [computed vs identity]")
w(C, "")
w(C, "| case | alpha | modes (sigma3, m) | p_N numerical | p_S numerical | p_N exact | p_S exact | largest difference |")
w(C, "|---|---|---|---|---|---|---|---|")
for (kd, nn, al), r in sorted(RDATA.items(), key=lambda kv: (kv[0][0], kv[0][1], -kv[0][2])):
    lab = ("doublets/ALT, n = %d" % nn) if kd == "ALT" else "R6 singlets, q = -3/2"
    w(C, "| %s | %s | %s | %s | %s | %s | %s | %s |" % (
        lab, fr(al), ", ".join("(%+d, %s)" % (ch, fr(m)) for ch, m in r["allowed"]),
        ", ".join("%.6f" % x[2] for x in r["exps"]), ", ".join("%.6f" % x[3] for x in r["exps"]),
        ", ".join("%.6f" % x[4] for x in r["exps"]), ", ".join("%.6f" % x[5] for x in r["exps"]), e(r["exp_err"])))
w(C, "")
w(C, "## B1 detail (1b-6) [identity: index theorem; independent of phi] (A8 [Venus])")
w(C, "")
w(C, "Backgrounds rebuilt with B0's own solve_bg/integrals (functions taken from B0's run.py by AST; its continuation loop re-implemented "
  "as in B0 lines 249-263). Functions and constants used: %s." % ", ".join(B0_KEPT))
w(C, "")
w(C, "FD method for B1 [post-hoc, development; box scratch run]: the same operator as Job Two/Job Four (R^2 D^2 = -u'' + (W^2 +- W') u in theta, "
  "Dirichlet ends, eigenvalues below %g counted) on a grid uniform in t = ln tan(theta/2), t in [-%g, %g], step %g. The theta-uniform grid "
  "(N = %d, as Job Four) is kept as a report-only column: for a mode with |psi|^2 ~ theta^0 at a pole (m = 1/2 here) its eigenvalue error "
  "falls only like 1/ln N, which matters when the vortex flux is concentrated at the north pole (large eps)." % (TAU_FD, B1_FD_T, B1_FD_T, B1_FD_H, NFD_R))
w(C, "")
w(C, "| n | eps | BVP success | C1 rel. err (B0's check) | max abs(phi)^2 | flux (1/2pi) int B dA | count | regular | normalisable | FD sigma3=+1 | FD sigma3=-1 | largest FD zero eig | smallest FD nonzero eig | report-only: theta-grid FD (+1, -1) |")
w(C, "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for (n, eps), r in sorted(B1.items()):
    w(C, "| %d | %g | %s | %s | %.6f | %.10f | %d | %d | %d | %d | %d | %.4g | %.4f | %d, %d |" % (
        n, eps, yn(r["succ"]), e(r["c1"]), r["mx"], r["flux"], len(r["allowed"]), r["reg"], r["nrm"], r["fd"][+1], r["fd"][-1], r["zmax"], r["nz"],
        r["fd_th"][+1], r["fd_th"][-1]))
w(C, "")
w(C, "## Per-count table (spec 1.2): each count with its own n convention")
w(C, "")
w(C, "| count | case | source convention | N_Phi | formula | from N_Phi | source value | cited at |")
w(C, "|---|---|---|---|---|---|---|---|")
for r in pc_rows:
    w(C, "| %s | %s | %s (%s) | %s | %s | %s | %s | %s |" % (r[0], r[1], r[2], N_CONVENTION[r[2]], r[3], r[4], r[5], r[6], r[7]))
w(C, "")
w(C, "Hard stop on an unconverted n: count_dirac(3) raised ConventionError: %s." % yn(hard_stop))
w(C, "")
w(C, "## E4 section counts on the grid (A5 build test): bounded = normalisable = N_Phi + 1 - 2s")
w(C, "")
w(C, "| s | N_Phi | " + " | ".join("alpha = %s (bounded, normalisable)" % fr(a) for a in ALPHAS) + " | expected | agree |")
w(C, "|---|---|" + "---|" * len(ALPHAS) + "---|---|")
for s in SPINS:
    for Nphi in range(0 if s < 1 else 1, 7):
        rr = [x for x in e4_rows if x[0] == s and x[1] == Nphi]
        w(C, "| %s | %d | %s | %d | %s |" % (fr(s), Nphi, " | ".join("%d, %d" % (x[3], x[4]) for x in rr), rr[0][5], yn(all(x[6] for x in rr))))
w(C, "")
w(C, "## Report-only (never graded)")
w(C, "")
w(C, "Tip flux delta at the north tip (A3 [Venus], [open]): m -> m - delta in the north exponent; N_Phi = 3, s = 1/2.")
w(C, "")
w(C, "| delta | alpha | bounded count | normalisable count |")
w(C, "|---|---|---|---|")
for d, al, a, b in TIPFLUX:
    w(C, "| %s | %s | %d | %d |" % (fr(d), fr(al), a, b))
w(C, "")
w(C, "Jackiw-Rossi (Majorana) zero modes for B1 (A8): not run (not cheap; optional).")
w(C, "")
n_all = 16
sm_ok = [cid for cid, *_ in CANDS if all(v == 0 for v in ANOM[cid]["sm"].values()) and ANOM[cid]["wit"] % 2 == 0]
r4_zero = [cid for cid, *_ in CANDS if ANOM[cid]["net"] == 0]
w(C, "Survivor counts (information only; Part A applies no gate): all %d candidates now have every Part A entry computed; "
  "SM 4D gauge anomalies cancel (with even Witten count) for %d (%s); tr R^4 net = 0 for %d (%s); B1 has no SM charges (n/a)." % (
      n_all, len(sm_ok), ", ".join(sm_ok), len(r4_zero), ", ".join(r4_zero)))

# ======================= write OVERLAPS_ALPHA.md =======================
O = "OVERLAPS_ALPHA"
w(O, "# SM1 Part A - OVERLAPS_ALPHA (1b-8; generated by run.py; do not edit by hand)")
w(O, "")
w(O, "C_alpha(a, b -> c) = int psi_a psi_b conj(psi_c) dA / (|psi_a| |psi_b| |psi_c|), dA = alpha sin(theta) dtheta dphi (unit radius). "
  "Sections are the E4 forms [Venus]: psi_s = (alpha sin theta)^(-s) tan(theta/2)^((m - q)/alpha) sin(theta)^(q/alpha) e^{i m phi}, m in Z + s, q = N/2. "
  "A section of negative charge is taken as conj(psi_{-q,-s,-m}) [build interpretation: the E4 form with q < 0 has no regular modes]. "
  "Labels are (N, s, m) with N = 2q signed. Selection rules: m_c = m_a + m_b and s_a + s_b = s_c (counting the conjugate). "
  "Closed form: Beta functions (mpmath, %d digits); quadrature: Gauss-Legendre in t = ln tan(theta/2), %d nodes on [-%g, %g] (check column: %d nodes)." % (
      MP_DPS, NQ, TQ, TQ, NQ_CHECK))
w(O, "")
w(O, "Values are given for the alpha grid%s; the alpha_ext column is added only when the 0.2 slot holds it." % ("" if alpha_ext is None else " plus alpha_ext"))
w(O, "")
for tab, title in (("a", "(a) ALT constant-Higgs Gram row: H(N 0, s 0, m 0) x psi_u -> psi_Q (s = 1/2); expected 1/sqrt(4 pi alpha) on the diagonal, 0 off it"),
                   ("b", "(b) MAIN-A closure: H (N 6, s 1; Q_H = 2) x psi_R (N -3, s -1/2; Q_R = -1) -> psi_L (N 3, s 1/2; Q_L = 1)"),
                   ("c", "(c) general fusion table, N_1 + N_2 = N_3 <= %d" % NPHI_TABLE_MAX)):
    w(O, "## " + title)
    w(O, "")
    w(O, "| entry | " + " | ".join("alpha = %s: closed form | quad rel. (or abs.) diff | check-grid diff" % fr(a) for a in ALPHAS) + " |")
    w(O, "|---|" + "---|---|---|" * len(ALPHAS))
    for table, label, a, b, c, vals in OV_ROWS:
        if table != tab:
            continue
        cells = []
        for al in ALPHAS:
            cf, qd, qd2, okm = vals[al]
            if okm:
                cells.append("%.12f | %s | %s" % (cf, e(abs(qd - cf) / abs(cf)), e(abs(qd2 - cf) / abs(cf))))
            else:
                cells.append("0 (m rule) | %s abs | %s abs" % (e(abs(qd)), e(abs(qd2))))
        w(O, "| %s | %s |" % (label, " | ".join(cells)))
    w(O, "")
w(O, "Job Four RESULTS lines 16-19 (cited singular values 1/sqrt(4 pi alpha)) equal 1/sqrt(4 pi alpha) at the printed precision: %s." % yn(jf_sv_ok))
w(O, "")
w(O, "## O-a: alpha = 1 against Job Two's exact rows (RESULTS lines 139-144)")
w(O, "")
w(O, "Map [identity at alpha = 1]: Job Two's Y_{Q,|Q|,m_J} = c x (normalised scalar E4 section with q = Q, m = m_J + Q), with a constant c of modulus 1 "
  "read off at theta = 0.7 and checked at theta = 1.9. Job Two's I = int conj(Y1) Y2 Y3 = conj(c1) c2 c3 C_1(2, 3 -> 1).")
w(O, "")
w(O, "| row (q1,l1,m1; q2,l2,m2; q3,l3,m3) | Job Two exact (sympy, recomputed) | value | mine (phase-mapped) | abs diff | phase-constant check | pass |")
w(O, "|---|---|---|---|---|---|---|")
for lab, ex, exr, mine, dif, pe, ok in oa_rows:
    w(O, "| %s | %s | %.12f | %.12f%+.1ei | %s | %s | %s |" % (lab, ex, exr, mine.real, mine.imag, e(dif), e(pe), yn(ok)))
w(O, "")
w(O, "Report-only: table (b) at alpha = 1 against Job Two's Assignment A entries (OV.triple_exact with Q_L = 1, Q_H = 2, Q_R = -1 and the same phase map): largest abs difference %s." % e(mainA_cmp))
w(O, "")
w(O, "Worst O-b relative difference %s; worst O-c entry %s; worst O-d difference %s." % (e(ob_worst), e(oc_worst), e(od_worst)))

# ======================= write ANOMALIES.md =======================
A_ = "ANOMALIES"
w(A_, "# SM1 Part A - ANOMALIES (1b-9, 1b-10; generated by run.py; do not edit by hand)")
w(A_, "")
w(A_, "## tr R^4 net per candidate (for Part B's Q16 consistency gate)")
w(A_, "")
w(A_, "Sign convention (E1 [Venus]): net = N+ - N-, the 6D Weyl component count at Gamma7 = +1 minus the count at Gamma7 = -1 "
  "(spin-1/2 matter only; no gravitino, tensors or gaugini, A9). A nonzero net is an irreducible gravitational anomaly; "
  "Part B applies the gate (Q16 [Venus]); Part A only reports it.")
w(A_, "")
w(A_, "| candidate | N+ (Gamma7 = +1) | N- (Gamma7 = -1) | tr R^4 net | nonzero |")
w(A_, "|---|---|---|---|---|")
for cid, fam, kind, nu, n, higgs, desc in CANDS:
    Np, Nm, _, _ = sixd_counts(kind, nu)
    w(A_, "| %s | %d | %d | %d | %s |" % (cid, Np, Nm, ANOM[cid]["net"], yn(ANOM[cid]["net"] != 0)))
w(A_, "| B1 | n/a | n/a | n/a | n/a (no SM content assigned) |")
w(A_, "")
w(A_, "Graded (A-b): " + "; ".join("%s %d (cited %d) %s" % (c, a, b, yn(ok)) for c, a, b, ok in ab_items) + ".")
w(A_, "")
w(A_, "## I6 per candidate (E3 [Venus]) [computed, exact]")
w(A_, "")
w(A_, "I6 = (1/(2 pi)^3) [ ... ], summed over 4D left-handed Weyl zero modes (right-handed fields as conjugates, all charges flipped). "
  "Y is SM-normalised (Q = T3 + Y). F = F_SU(3) + F_SU(2) + Y F_Y + X F_X. Symbols: t3 = tr_3 F_SU(3)^2, t2 = tr_2 F_SU(2)^2, "
  "c3 = tr_3 F_SU(3)^3, fY = F_Y, fX = F_X, p1 = -(1/8 pi^2) tr R^2. The bracket is sum mult [(1/6) tr F^3 - (1/24) p1 tr F], "
  "expanded independently with sympy and compared with Job Two's anomalies.py sums after the E3 map.")
w(A_, "")
for cid, *_ in CANDS:
    A = ANOM[cid]
    w(A_, "### %s (copies per field %d)" % (cid, A["mult"]))
    w(A_, "")
    w(A_, "| monomial | coefficient (sympy expansion) | E3 map of the Stage 1 sum | equal |")
    w(A_, "|---|---|---|---|")
    for mono, (nm, desc_) in I6_MONO.items():
        g = A["got"].get(mono, 0)
        w(A_, "| %s | %s | %s = %s | %s |" % (nm, g, desc_, A["exp6"][mono], yn(sp.nsimplify(g - A["exp6"][mono]) == 0)))
    if A["extra"]:
        w(A_, "| other monomials | %s | - | NO |" % A["extra"])
    w(A_, "")
w(A_, "A2 [Venus, identity]: the reduction of I8 to I6 on the rugby ball uses int K dA = 4 pi alpha + 2 x 2 pi (1 - alpha) = %s (sympy, every alpha), "
  "including the tips' delta-curvature, and flux N_Phi; so I6 does not depend on alpha. A bare deficit adds no anomaly; no candidate has tip chiral fields." % DESCENT)
w(A_, "")
w(A_, "## I8 per distinct 6D content (E1, E2 [Venus]) [computed, exact]")
w(A_, "")
w(A_, "Per positive-chirality 6D Weyl field (sign Gamma7): (d/5760)(tr R^4 + (5/4)(tr R^2)^2) - (1/96) tr R^2 tr F^2 + (1/24) tr F^4 "
  "[standard: Alvarez-Gaume-Witten 1984; Green-Schwarz-West 1985], 2pi factors dropped. r4 = tr R^4, r2 = tr R^2. tr_3 F^4 = t3^2/2 and "
  "tr_2 F^4 = t2^2/2 [identity, E2], so only tr R^4 is irreducible. Random-matrix check of tr F^4 = (tr F^2)^2/2 (largest relative error over 20 draws): "
  "su(2) %s, su(3) %s, su(4) %s (fails for su(4), as expected)." % (e(E2_CHECK[2]), e(E2_CHECK[3]), e(E2_CHECK[4])))
w(A_, "")
seen = {}
for cid, fam, kind, nu, n, higgs, desc in CANDS:
    seen.setdefault((kind, nu), []).append(cid)
for (kind, nu), cids in seen.items():
    A = ANOM[cids[0]]
    w(A_, "### %s content%s (candidates %s)" % (kind, " + nu^c" if nu else " without nu^c", ", ".join(cids)))
    w(A_, "")
    w(A_, "- I8 = %s" % sp.sstr(A["I8"]))
    w(A_, "- tr R^4 net N+ - N- = %d" % A["net"])
    w(A_, "- tr F^4_SU(3) triplet count Gamma7 = -1 vs +1: %d vs %d (build-reproduction check only; not an anomaly condition, E2)" % (A["T3m"], A["T3p"]))
    w(A_, "- Green-Schwarz factorisation (report-only): %s" % A["fac"])
    w(A_, "")
w(A_, "Report-only gaugino variant (A9): %d adjoint Weyl fermions (8 + 3 + 1 + 1) of one chirality shift every tr R^4 net above by +%d (Gamma7 = +1) or -%d (Gamma7 = -1); "
  "the adjoint tr F^4 shift is not expanded here." % (N_GAUGINI, N_GAUGINI, N_GAUGINI))
w(A_, "")
w(A_, "Not a Job Two result: H - V + 29T = 273 is the 6D (1,0) supergravity condition [standard] (A4 [Venus]); it is not assumed.")


# ======================= RESULTS.md summary, audit, grade =======================
w("RESULTS", "## Stage 1 and 1b summary")
w("RESULTS", "")
w("RESULTS", "Read-only imports: Job Two's anomalies.py, monopole.py, overlaps.py (D1); Job Four's run.py module level (D2; its main() is not run); "
  "B0's background functions and constants only, taken from its run.py by AST (D6): %s." % ", ".join(B0_KEPT))
w("RESULTS", "")
w("RESULTS", "| item | result |")
w("RESULTS", "|---|---|")
w("RESULTS", "| 1b-1 S family | %d cited checks, all equal: %s |" % (len(ca_items), yn(CA_OK)))
w("RESULTS", "| 1b-2 S5 anomalies | SM sums %s; U(1)_X sums %s; tr R^4 net %d |" % (
    ", ".join(fr(ANOM["S5"]["sm"][k]) for k in ("SU(3)^2 U(1)", "SU(2)^2 U(1)", "U(1)^3", "grav^2 U(1)", "SU(3)^3")),
    ", ".join(fr(ANOM["S5"]["xs"][k]) for k in XKEY), ANOM["S5"]["net"]))
w("RESULTS", "| 1b-3 R1/R2 | grid rows equal to Job Four lines 106-109: %s |" % yn(CB_OK))
w("RESULTS", "| 1b-4/1b-5/1b-6 R3-R5, R6, B1 | %d rows, count = N_Phi with three methods agreeing: %s |" % (len(cc_items), yn(CC_OK)))
w("RESULTS", "| 1b-7 U1 | %d Stage A sectors, count = N_Phi in every one: %s |" % (u1_n, yn(u1_ok)))
w("RESULTS", "| per-count table / E4 counts | %s |" % "; ".join("%s: %s" % (nm, yn(ok)) for nm, ok in cd_items))
w("RESULTS", "| 1b-8 overlaps | %d entries x %d alpha values; worst O-b %s, worst O-c %s, worst O-d %s; O-a rows %d |" % (
    len(OV_ROWS), len(ALPHAS), e(ob_worst), e(oc_worst), e(od_worst), len(oa_rows)))
w("RESULTS", "| 1b-9 I6 | coefficients equal to the Stage 1 sums after the E3 map, all 15 S/R candidates: %s |" % yn(AA_OK))
w("RESULTS", "| 1b-10 I8 | tr R^4 net: %s |" % ", ".join("%s %d" % (cid, ANOM[cid]["net"]) for cid, *_ in CANDS))
w("RESULTS", "")
w("RESULTS", "Outputs: CANDIDATES.md, OVERLAPS_ALPHA.md, ANOMALIES.md (Part B's inputs; generated only by this file).")
w("RESULTS", "")

# audit: sources and the SM1_filter folder unchanged by the run
after_bad = []
for ds, path, exp in SOURCES:
    h, c = sha8(path)
    if (h, c) != BEFORE[path]:
        after_bad.append(path)
own_after = folder_state(HERE, skip=OWN_OUTPUTS)
bytecode = [p for p in (J(_S2, "__pycache__"), J(_JF, "__pycache__"), J(_B0, "__pycache__"), J(HERE, "__pycache__")) if os.path.exists(p)]
AUDIT_OK = not after_bad and own_after == OWN_BEFORE
w("RESULTS", "## Audit")
w("RESULTS", "")
w("RESULTS", "Every source file re-hashed after the run: %d of %d unchanged%s." % (len(SOURCES) - len(after_bad), len(SOURCES),
  "" if not after_bad else " (CHANGED: %s)" % ", ".join(after_bad)))
w("RESULTS", "SM1_filter folder (other than the four outputs) before = after: %s (%s)." % (yn(own_after == OWN_BEFORE),
  ", ".join("%s %s/%s" % (k, v[0], v[1]) for k, v in sorted(own_after.items()))))
w("RESULTS", "__pycache__ folders present next to the sources or here: %s." % (", ".join(bytecode) if bytecode else "none"))
w("RESULTS", "")
GRADE.append(("audit", "sources and the SM1_filter inputs unchanged by the run", AUDIT_OK))
w("RESULTS", "## Graded items (spec section 5)")
w("RESULTS", "")
w("RESULTS", "| item | rule | result |")
w("RESULTS", "|---|---|---|")
for it, desc, ok in GRADE:
    w("RESULTS", "| %s | %s | %s |" % (it, desc, pf(ok)))
w("RESULTS", "")
BUILD = all(ok for _, _, ok in GRADE)
w("RESULTS", "**Build %s** (Part A grades builds and counts only, never physics). Runtime %.1f s." % (pf(BUILD), time.time() - T0))
write_all()

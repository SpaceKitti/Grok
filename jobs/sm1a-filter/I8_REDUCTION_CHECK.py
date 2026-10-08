"""I8 -> I6 reduction on the sphere, both signs of the tr R^2 tr F^2 cross term. REPORT-ONLY, outside the graded SM1 Part A run.

Requested by Venus's grade (hole 1 and hole 2, VENUS_GRADE_NOTES E6754653) on 2026-10-08. This script does not import or run
run.py (run.py runs the whole graded job at import). It takes run.py's own code by AST, unchanged: the symbols line, TR3, TR2,
content(), CANDS, trF(), I6_poly(), I8_poly(), factorise(), I6_MONO, NPhi/convert()/count_dirac(); and it copies the 4D
left-handed content lines of zero_mode_table() (run.py lines 426-442) without Job Two's mode solvers, which are not needed for I6.

Reduction (A2 [Venus]): on the sphere with X-flux n (N_Phi = |x| n per field), I6 = -n dI8/dF_X with tr R^2 -> -2 p1
(p1 = -r2/2, 2 pi factors dropped as in run.py). Sphere curvature drops out: its 4-forms vanish on a 2-sphere.
The cross term is run.py's -(1/96) r2 tr F^2 (sign -1, graded, printed in ANOMALIES) or +(1/96) r2 tr F^2 (sign +1, Venus):
I8(+1) = I8(-1) + 2 * sum_fields Gamma7 r2 tr F^2 / 96. Both are compared with run.py's I6_poly and with the I6 coefficients
printed in the graded ANOMALIES.md. The +n orientation is also printed, for completeness. Writes only I8_REDUCTION_CHECK.md.
"""
import os
import sys

sys.dont_write_bytecode = True

import ast
import datetime
import hashlib
import itertools
import math
import platform
import re
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join
GRADED = [("run.py", "803FD2DA"), ("README.md", None), ("RESULTS.md", "7148A1DC"),
          ("CANDIDATES.md", "DAD867CE"), ("OVERLAPS_ALPHA.md", "D93AC9BD"), ("ANOMALIES.md", "B55D5D1F")]
README_GRADED = "12CEC48F"


def sha8(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:8].upper()


def hashes(tag):
    out = []
    for nm, h in GRADED:
        got = sha8(J(HERE, nm))
        want = h if h else README_GRADED
        out.append((nm, want, got))
        print("[%s] %s graded %s now %s %s" % (tag, nm, want, got, "OK" if got == want else "DIFFERENT"), flush=True)
    return out


H_BEFORE = hashes("before")
if H_BEFORE[0][2] != "803FD2DA" or H_BEFORE[5][2] != "B55D5D1F":
    print("STOP: run.py or ANOMALIES.md is not the graded file.")
    sys.exit(2)

# ---------- take run.py's own code by AST ----------
SRC = open(J(HERE, "run.py"), encoding="utf-8").read()
TREE = ast.parse(SRC)
WANT_F = {"content", "trF", "I6_poly", "I8_poly", "factorise", "convert", "_need", "count_dirac"}
WANT_C = {"t3", "TR3", "TR2", "CANDS", "I6_MONO", "_CONVERT_KEY", "N_CONVENTION"}
WANT_K = {"ConventionError", "NPhi"}
keep, took = [], []
for nd in TREE.body:
    if isinstance(nd, ast.FunctionDef) and nd.name in WANT_F:
        keep.append(nd); took.append("def %s@%d" % (nd.name, nd.lineno))
    elif isinstance(nd, ast.ClassDef) and nd.name in WANT_K:
        keep.append(nd); took.append("class %s@%d" % (nd.name, nd.lineno))
    elif isinstance(nd, ast.Assign):
        names = []
        for t in nd.targets:
            if isinstance(t, ast.Name):
                names.append(t.id)
            elif isinstance(t, ast.Tuple):
                names += [e.id for e in t.elts if isinstance(e, ast.Name)]
        if any(n in WANT_C for n in names):
            keep.append(nd); took.append("%s@%d" % ("/".join(names), nd.lineno))
NS = {"sp": sp, "np": np, "itertools": itertools, "Fr": Fr, "math": math}
exec(compile(ast.Module(body=keep, type_ignores=[]), J(HERE, "run.py"), "exec"), NS)
print("taken from run.py by AST: " + ", ".join(took), flush=True)
t3, c3, t2, fY, fX, r2, r4, p1 = sp.symbols("t3 c3 t2 fY fX r2 r4 p1")
content, trF, I6_poly, I8_poly, factorise = NS["content"], NS["trF"], NS["I6_poly"], NS["I8_poly"], NS["factorise"]
convert, count_dirac, CANDS, I6_MONO = NS["convert"], NS["count_dirac"], NS["CANDS"], NS["I6_MONO"]


def left_content(kind, nu, n):
    """run.py zero_mode_table lines 426-442, the 4D left-handed content only (sig = sign(x n), g5 = g7 sig)."""
    left = []
    for name, d3, a3, d2, Y, g7, x in content(kind, nu):
        N = convert("JobTwo", n, x)
        xn = x * n
        sig = 1 if xn > 0 else -1
        g5 = g7 * sig
        hand = "left" if g5 == -1 else "right"
        cnt = count_dirac(N)
        if hand == "left":
            left.append((name, d3, a3, d2, Y, Fr(x), cnt))
        else:
            left.append((name + "^c", d3, -a3, d2, -Y, Fr(-x), cnt))
    return left


def cross(kind, nu):
    return sp.expand(sum(g7 * r2 * trF(2, d3, a3, d2, Y, Fr(x)) / 96 for nm, d3, a3, d2, Y, g7, x in content(kind, nu)))


def I8_sign(kind, nu, s):
    base = I8_poly(kind, nu)                       # run.py's own I8: cross term -(1/96)
    return base if s == -1 else sp.expand(base + 2 * cross(kind, nu))


def descent(I8, n, orient=-1):
    return sp.expand(orient * n * sp.diff(I8, fX).subs(r2, -2 * p1))


# ---------- graded I6 coefficients printed in ANOMALIES.md ----------
ANL = open(J(HERE, "ANOMALIES.md"), encoding="utf-8").read().splitlines()
NAME2MONO = {v[0]: k for k, v in I6_MONO.items()}
GRADED_I6 = {}
cur = None
for ln in ANL:
    m = re.match(r"^### (S\d|R\d) \(copies per field (\d+)\)", ln)
    if m:
        cur = m.group(1); GRADED_I6[cur] = {}
        continue
    if ln.startswith("## I8"):
        cur = None
    if cur and ln.startswith("| ") and not ln.startswith("| monomial"):
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if cells[0] in NAME2MONO:
            GRADED_I6[cur][NAME2MONO[cells[0]]] = sp.Rational(cells[1])
GENS = (t3, c3, t2, fY, fX, p1)


def coeffs(expr):
    P = sp.Poly(expr, *GENS)
    return {m: c for m, c in P.terms()}


def same(d, ref):
    keys = set(d) | set(ref)
    return all(sp.nsimplify(d.get(k, 0) - ref.get(k, 0)) == 0 for k in keys), sorted(
        [I6_MONO[k][0] if k in I6_MONO else str(k) for k in keys if sp.nsimplify(d.get(k, 0) - ref.get(k, 0)) != 0])


# ---------- per candidate ----------
rows = []
I8C = {}
for cid, fam, kind, nu, n, higgs, desc in CANDS:
    key = (kind, nu)
    if key not in I8C:
        I8C[key] = {s: I8_sign(kind, nu, s) for s in (-1, +1)}
    P6 = coeffs(I6_poly(left_content(kind, nu, n)).as_expr())
    g6 = GRADED_I6.get(cid, {})
    rep_ok, _ = same(P6, g6)                       # run.py's I6 path reproduces the printed graded I6
    res = {}
    for s in (-1, +1):
        for orient in (-1, +1):
            ok, diff = same(coeffs(descent(I8C[key][s], n, orient)), g6)
            res[(s, orient)] = (ok, diff)
    rows.append((cid, kind, nu, n, len(g6), rep_ok, res))
    print("%s (%s%s, n = %d): I6_poly = graded ANOMALIES I6 (%d monomials): %s | -n dI8/dfX: -1/96 %s%s, +1/96 %s%s | +n: -1/96 %s, +1/96 %s"
          % (cid, kind, "+nu" if nu else "", n, len(g6), rep_ok,
             "REPRODUCES" if res[(-1, -1)][0] else "FAILS", "" if res[(-1, -1)][0] else " (differs in: %s)" % ", ".join(res[(-1, -1)][1]),
             "REPRODUCES" if res[(1, -1)][0] else "FAILS", "" if res[(1, -1)][0] else " (differs in: %s)" % ", ".join(res[(1, -1)][1]),
             "REPRODUCES" if res[(-1, 1)][0] else "FAILS", "REPRODUCES" if res[(1, 1)][0] else "FAILS"), flush=True)

# ---------- I8 per content, both signs; graded I8 strings reproduced; factorisation ----------
LABEL = {("ALT", True): ("ALT content + nu^c", 280, 283), ("ALT", False): ("ALT content without nu^c", 287, 290),
         ("MAIN", True): ("MAIN content + nu^c", 294, 297), ("MAIN", False): ("MAIN content without nu^c", 301, 304),
         ("S5", True): ("S5 content + nu^c", 308, 311)}
cont = []
for key, d in I8C.items():
    lab, ln_i8, ln_fac = LABEL[key]
    printed = ANL[ln_i8 - 1].strip()
    graded_match = printed == "- I8 = %s" % d[-1]
    r2terms = {}
    for s in (-1, +1):
        lin = sp.expand(sp.Poly(d[s], r2).coeff_monomial(r2) * r2)
        r2terms[s] = lin
    fac = {s: factorise(d[s]) for s in (-1, +1)}
    fac_printed = ANL[ln_fac - 1].split("(report-only): ", 1)[1] if ln_fac else None
    fac_match = (fac[-1] == fac_printed) if ln_fac else None
    yes = {s: fac[s].startswith("factorises") for s in (-1, +1)}
    cont.append((key, lab, ln_i8, ln_fac, graded_match, d, r2terms, fac, fac_match, yes))
    print("%s: graded I8 string (ANOMALIES line %d) reproduced: %s; r2-linear terms -1/96: %s ; +1/96: %s ; factorises -1/96: %s, +1/96: %s"
          % (lab, ln_i8, graded_match, r2terms[-1], r2terms[+1], yes[-1], yes[+1]), flush=True)
    print("   factorise(+1/96): %s" % fac[+1], flush=True)

H_AFTER = hashes("after")

# ---------- markdown ----------
md = []
md.append("# I8 to I6 reduction check, both cross-term signs: REPORT-ONLY")
md.append("")
md.append("**REPORT-ONLY. Outside the graded SM1 Part A run. Requested in Venus's grade (holes 1 and 2) on 2026-10-08. It does "
          "not change any graded output.** Written by `I8_REDUCTION_CHECK.py`, which takes run.py's own I8, I6, content and "
          "factorisation code by AST and does not import or run run.py. Run at %s on %s, Python %s, sympy %s." % (
              datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"), platform.node(), platform.python_version(),
              sp.__version__))
md.append("")
md.append("| file | graded hash | before | after |")
md.append("|---|---|---|---|")
for (nm, h, g1), (_, _, g2) in zip(H_BEFORE, H_AFTER):
    md.append("| %s | %s | %s | %s |" % (nm, h, g1, g2))
md.append("")
md.append("Code taken from run.py: %s." % ", ".join(took))
md.append("")
md.append("## What it checks")
md.append("")
md.append("Putting the 6D anomaly polynomial on the sphere with X-flux n should give the 4D one: I6 = -n dI8/dF_X, with "
          "tr R^2 replaced by -2 p1. The sphere's own curvature drops out, because its 4-forms vanish on a 2-sphere. run.py "
          "prints I8 with the cross term -(1/96) tr R^2 tr F^2; Venus says the sign that matches I6's convention (real F) is "
          "+(1/96). This script tries both and compares each reduction with the graded I6 coefficients printed in "
          "ANOMALIES.md (and with run.py's own I6 code path, which reproduces them). The +n orientation is shown too.")
md.append("")
md.append("## Result per candidate")
md.append("")
md.append("| candidate | content | n | run.py I6 path = graded I6 | -(1/96), -n | +(1/96), -n | -(1/96), +n | +(1/96), +n |")
md.append("|---|---|---|---|---|---|---|---|")
for cid, kind, nu, n, nmono, rep_ok, res in rows:
    def cell(k):
        ok, diff = res[k]
        return "reproduces" if ok else "FAILS (%s)" % ", ".join(diff)
    md.append("| %s | %s%s | %d | %s | %s | %s | %s | %s |" % (cid, kind, " + nu^c" if nu else "", n, "YES" if rep_ok else "NO",
                                                              cell((-1, -1)), cell((1, -1)), cell((-1, 1)), cell((1, 1))))
plus_all = all(r[6][(1, -1)][0] for r in rows)
minus_fail = [r[0] for r in rows if not r[6][(-1, -1)][0]]
md.append("")
md.append("With the -n orientation, +(1/96) reproduces the graded I6 for every candidate: %s. -(1/96) fails for: %s." % (
    "YES" if plus_all else "NO", ", ".join(minus_fail) if minus_fail else "none"))
md.append("")
md.append("## Cross-term terms of I8 per content, both signs")
md.append("")
for key, lab, ln_i8, ln_fac, graded_match, d, r2terms, fac, fac_match, yes in cont:
    md.append("### %s" % lab)
    md.append("")
    md.append("- graded I8 (ANOMALIES line %d) reproduced by run.py's I8_poly: %s" % (ln_i8, "YES" if graded_match else "NO"))
    md.append("- terms linear in r2, as printed (-1/96): %s" % r2terms[-1])
    md.append("- terms linear in r2, corrected (+1/96): %s" % r2terms[+1])
    md.append("- corrected I8 (+1/96): %s" % d[+1])
    if ln_fac:
        md.append("- factorisation as printed (ANOMALIES line %d) reproduced: %s" % (ln_fac, "YES" if fac_match else "NO"))
    md.append("- factorisation, corrected (+1/96): %s" % fac[+1])
    md.append("- factorises yes/no: printed sign %s, corrected sign %s, unchanged: %s" % (
        "yes" if yes[-1] else "no", "yes" if yes[+1] else "no", "YES" if yes[-1] == yes[+1] else "NO"))
    md.append("")
md.append("tr R^4 terms do not involve the cross term, so the tr R^4 nets are unchanged; I6 and A-a/A-b are unchanged.")
md.append("")
with open(J(HERE, "I8_REDUCTION_CHECK.md"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(md) + "\n")
print("wrote I8_REDUCTION_CHECK.md; +1/96 reproduces all: %s; -1/96 fails for: %s" % (plus_all, ", ".join(minus_fail)))

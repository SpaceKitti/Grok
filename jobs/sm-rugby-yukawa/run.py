"""Job Four: rugby-ball Yukawas from a brane-localised Higgs (toy bookkeeping).

Writes RESULTS.md and ratios.png only (never hand-edit them). Rules: README.md, written before the run.
Builds on the alternative model of sm-zero-modes-S2, which is read-only here: its monopole.py (Wu-Yang
monopole harmonics, Wigner small-d, Sturm count; credit: sm-zero-modes-S2) is imported with bytecode
writing switched off, and that folder's file hashes are printed before and after the run.
"""
import sys
sys.dont_write_bytecode = True

import datetime
import hashlib
import math
import os

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.special import betainc, beta as beta_fn

HERE = os.path.dirname(os.path.abspath(__file__))
S2 = r"C:\Users\Akitt\sm-zero-modes-S2"


def folder_state(path):
    out = {}
    for nm in sorted(os.listdir(path)):
        p = os.path.join(path, nm)
        mt = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%H:%M:%S")
        if os.path.isfile(p):
            with open(p, "rb") as fh:
                out[nm] = (hashlib.sha256(fh.read()).hexdigest()[:16].upper(), mt)
        else:
            out[nm + "/"] = (",".join(sorted(os.listdir(p))), mt)
    return out


S2_BEFORE = folder_state(S2)
sys.path.insert(0, S2)
import monopole as MP  # noqa: E402
sys.path.pop(0)

q = 1.5                      # q = x n / 2 for every alternative-model fermion (x = +1, n = 3) [assumed input]
ALPHAS = [1.0, 0.8, 0.6, 0.5]
SMAX = 40.0
L = []
w = L.append


def yn(b):
    return "YES" if b else "NO"


def pf(b):
    return "PASS" if b else "FAIL"


_GL = {}


def gl(a, b, n):
    if n not in _GL:                      # cache the Gauss-Legendre nodes (recomputing them dominated the run time)
        _GL[n] = np.polynomial.legendre.leggauss(n)
    x, wt = _GL[n]
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * wt


def fmt(x, p=6):
    return ("%." + str(p) + "g") % x


# ------------------------------------------------------------------ zero modes on the rugby ball
class Mode:
    """One zero-mode candidate: half-integer m, 2D chirality chir (+1: sigma3 = +1 slot, a' = W a).

    psi = (alpha sin theta)^(-1/2) e^{i m phi} a(theta). In s = ln tan(theta/2):
    d ln a / ds = chir (m - q (1 + tanh s)) / alpha. Solved numerically (DOP853), both directions from s = 0.
    """

    def __init__(self, alpha, m, chir=+1):
        self.alpha, self.m, self.chir = alpha, m, chir
        f = lambda s, y: [chir * (m - q * (1.0 + math.tanh(s))) / alpha]
        kw = dict(method="DOP853", rtol=1e-13, atol=1e-13, dense_output=True)
        self.up = solve_ivp(f, [0.0, SMAX], [0.0], **kw)
        self.dn = solve_ivp(f, [0.0, -SMAX], [0.0], **kw)
        self.lz20 = self.log_norm(20.0, 400)
        self.lz40 = self.log_norm(SMAX, 800)
        self.normalisable = abs(self.lz40 - self.lz20) < 1e-8
        self.pN, self.pS = self.tip_exponents()
        self.regular = self.pN > -1e-6 and self.pS > -1e-6
        self.allowed = self.normalisable and self.regular

    def lna(self, s):
        s = np.atleast_1d(np.asarray(s, dtype=float))
        out = np.empty_like(s)
        pos = s >= 0
        if pos.any():
            out[pos] = self.up.sol(s[pos])[0]
        if (~pos).any():
            out[~pos] = self.dn.sol(s[~pos])[0]
        return out

    def lna_exact(self, s):
        return self.chir * ((self.m - q) * s - q * np.log(np.cosh(s))) / self.alpha

    def logw(self, s):
        # density in s: |psi|^2 sqrt(g) dtheta dphi / (2 pi)  ->  a^2 sech(s) ds (unnormalised)
        return 2.0 * self.lna(s) - np.log(np.cosh(s))

    def log_norm(self, S, n):
        x, wt = gl(-S, S, n)
        lw = self.logw(x)
        mx = lw.max()
        return mx + math.log(float(np.sum(wt * np.exp(lw - mx))))

    def dens(self, s):
        """normalised density in s (integrates to 1)"""
        return np.exp(self.logw(s) - self.lz40)

    def tip_exponents(self):
        def lpsi2(s):   # ln |psi|^2 up to a constant = 2 ln a - ln(alpha sin theta)
            return float(2.0 * self.lna(s)[0] + math.log(math.cosh(s))) - math.log(self.alpha)
        lth = lambda s: math.log(2.0 * math.atan(math.exp(s)))
        lpt = lambda s: math.log(2.0 * math.atan(math.exp(-s)))
        pN = (lpsi2(-29.0) - lpsi2(-30.0)) / (lth(-29.0) - lth(-30.0))
        pS = (lpsi2(30.0) - lpsi2(29.0)) / (lpt(30.0) - lpt(29.0))
        return pN, pS

    def exact_exponents(self):
        return (self.chir * 2 * self.m / self.alpha - 1, self.chir * 2 * (2 * q - self.m) / self.alpha - 1)


def s_of_u(u):
    return 0.5 * math.log(u / (1.0 - u))


def tophat_Y(mode, sig, n=600):
    x, wt = gl(-SMAX, s_of_u(sig), n)
    return float(np.sum(wt * mode.dens(x)))


def radial_overlap(m1, m2, hfun, top=None, n=800):
    """∫ h a_1 a_2 dtheta / sqrt(Z_1 Z_2), in s; hfun takes u."""
    b = SMAX if top is None else s_of_u(top)
    x, wt = gl(-SMAX, b, n)
    u = 0.5 * (1.0 + np.tanh(x))
    lg = m1.lna(x) + m2.lna(x) - np.log(np.cosh(x)) - 0.5 * (m1.lz40 + m2.lz40)
    return float(np.sum(wt * hfun(u) * np.exp(lg)))


def yukawa_rugby(modes, hfun, h0=1.0, top=None, nph=16):
    ph = 2 * math.pi * np.arange(nph) / nph
    Y = np.zeros((3, 3), dtype=complex)
    for i, a in enumerate(modes):
        for j, b in enumerate(modes):
            ang = np.sum(np.exp(1j * (b.m - a.m) * ph)) / nph      # ∫ e^{i(m'-m)phi} dphi / (2 pi)
            Y[i, j] = h0 * radial_overlap(a, b, hfun, top) * ang
    return Y


def fd_rugby(m, N, chir, alpha):
    h = math.pi / (N + 1)
    th = h * np.arange(1, N + 1)
    s, c = np.sin(th), np.cos(th)
    W = (m - q + q * c) / (alpha * s)
    Wp = (-q - (m - q) * c) / (alpha * s ** 2)
    V = W ** 2 + (Wp if chir > 0 else -Wp)
    return 2.0 / h ** 2 + V, -np.ones(N - 1) / h ** 2


def main():
    now = datetime.datetime.now().astimezone()
    z = now.strftime("%z")
    w("# RESULTS (generated by run.py - do not edit by hand)")
    w("")
    w("Generated: %s (local time, UTC%s:%s)" % (now.strftime("%Y-%m-%d %H:%M:%S"), z[:3], z[3:]))
    import scipy, matplotlib
    w("Python %s, numpy %s, sympy %s, scipy %s, matplotlib %s" % (
        sys.version.split()[0], np.__version__, sp.__version__, scipy.__version__, matplotlib.__version__))
    w("")
    w("Job Four: Yukawa ratios from a brane-localised Higgs on a rugby ball, on top of the alternative model of "
      "sm-zero-modes-S2 [by construction]. Toy bookkeeping: it does not derive the Standard Model, the quark "
      "masses or the real CKM matrix. sigma, alpha and beta are [assumed input].")
    w("")
    w("Read-only source: sm-zero-modes-S2/monopole.py %s (imported, no bytecode written)." % S2_BEFORE["monopole.py"][0])
    w("")

    # ---------------------------------------------------------- zero modes for every alpha
    mrange = [k + 0.5 for k in range(-5, 8)]
    modes, allm = {}, {}
    for al in ALPHAS:
        allm[al] = {(m, ch): Mode(al, m, ch) for m in mrange for ch in (+1, -1)}
        modes[al] = sorted([md for md in allm[al].values() if md.allowed], key=lambda md: (md.chir, md.m))
    ode_err = max(float(np.max(np.abs(md.lna(np.linspace(-SMAX, SMAX, 801)) - md.lna_exact(np.linspace(-SMAX, SMAX, 801)))
                                / (1 + np.abs(md.lna_exact(np.linspace(-SMAX, SMAX, 801))))))
                  for al in ALPHAS for md in allm[al].values())
    exp_err = max(max(abs(md.pN - md.exact_exponents()[0]), abs(md.pS - md.exact_exponents()[1]))
                  for al in ALPHAS for md in allm[al].values())

    # ================================================================ Stage A
    w("## Stage A [identity]")
    w("")
    w("### A1: constant Higgs, h = 1/sqrt(4 pi alpha) (the normalised constant mode)")
    w("")
    w("| alpha | zero modes used (m) | singular values [computed] | 1/sqrt(4 pi alpha) | relative spread |")
    w("|---|---|---|---|---|")
    okA1 = True
    for al in ALPHAS:
        ms = [md for md in modes[al] if md.chir == +1]
        h0 = 1.0 / math.sqrt(4 * math.pi * al)
        Y = yukawa_rugby(ms, lambda u: np.ones_like(u), h0=h0)
        sv = np.linalg.svd(Y, compute_uv=False)
        spread = float((sv.max() - sv.min()) / sv.max())
        okA1 &= spread < 1e-12 and abs(sv.mean() - h0) / h0 < 1e-9
        w("| %s | %s | %s | %.12f | %.1e |" % (al, ", ".join(str(sp.nsimplify(md.m)) for md in ms),
                                              ", ".join("%.12f" % v for v in sv), h0, spread))
    w("")
    w("Reason [identity]: Q and the singlets share the same three zero-mode sections, so a constant Higgs gives "
      "constant x (Gram matrix) = constant x unitary on any metric. At alpha = 1 the value 0.282094791774 is the "
      "alternative model's 1/(2 sqrt(pi)).")
    w("")
    w("### A2: axially symmetric brane profiles give a diagonal Y in the m basis")
    w("")
    # alpha = 1 with the monopole harmonics of sm-zero-modes-S2, 2D quadrature
    nph = 16
    ph = 2 * math.pi * np.arange(nph) / nph

    def harm_matrix(hu, umax, n=200):
        if umax < 1:
            u, wt = gl(0.0, umax, n)
        else:
            u1, w1 = gl(0.0, min(1.0, 0.5), n)
            u2, w2 = gl(0.5, 1.0, n)
            u, wt = np.concatenate([u1, u2]), np.concatenate([w1, w2])
        th = 2 * np.arcsin(np.sqrt(u))
        TH, PH = np.meshgrid(th, ph, indexing="ij")
        WG = np.outer(wt * 4 * math.pi * hu(u), np.full(nph, 1.0 / nph))   # dOmega = 4 pi du dphi/(2 pi)
        Ys = [MP.Y_north(1, 1, mJ, TH, PH) for mJ in (-1, 0, 1)]
        return np.array([[np.sum(WG * np.conj(Ys[i]) * Ys[j]) for j in range(3)] for i in range(3)])

    w("| alpha | profile | zero modes from | largest off-diagonal abs(Y_mm') | smallest diagonal | diagonal? |")
    w("|---|---|---|---|---|---|")
    okA2 = True
    rows = []
    Yt = harm_matrix(lambda u: np.ones_like(u), 0.3)
    Ysft = harm_matrix(lambda u: np.exp(-u / 0.1), 1.0)
    rows.append((1.0, "top-hat sigma = 0.3", "monopole harmonics Y_{1,1,m} (2D quadrature)", Yt))
    rows.append((1.0, "soft sigma = 0.1", "monopole harmonics Y_{1,1,m} (2D quadrature)", Ysft))
    ms06 = [md for md in modes[0.6] if md.chir == +1]
    rows.append((0.6, "top-hat sigma = 0.3", "1D solve", yukawa_rugby(ms06, lambda u: np.ones_like(u), top=0.3)))
    rows.append((0.6, "soft sigma = 0.1", "1D solve", yukawa_rugby(ms06, lambda u: np.exp(-u / 0.1))))
    for al, prof, src, Y in rows:
        off = max(abs(Y[i, j]) for i in range(3) for j in range(3) if i != j)
        dg = min(abs(Y[i, i]) for i in range(3))
        okA2 &= off < 1e-12
        w("| %s | %s | %s | %.1e | %.3e | %s |" % (al, prof, src, off, dg, yn(off < 1e-12)))
    w("")
    w("Reason [identity]: an axially symmetric h leaves the phi integral ∫ e^{i(m'-m) phi} dphi, which vanishes for m' != m.")
    w("")

    # ================================================================ Stage B
    w("## Stage B (alpha = 1, round sphere)")
    w("")
    U, SG = sp.symbols("u sigma", positive=True)
    bern = [3 * sp.binomial(2, k) * U ** k * (1 - U) ** (2 - k) for k in range(3)]
    ug = np.linspace(0.0, 1.0, 201)
    thg = 2 * np.arcsin(np.sqrt(ug))
    bern_num = [np.array([float(b.subs(U, x)) for x in ug]) for b in bern]
    harm = {mJ: 4 * math.pi * np.abs(MP.Y_north(1, 1, mJ, thg, 0.0)) ** 2 for mJ in (-1, 0, 1)}
    kmap = {mJ: int(np.argmin([np.max(np.abs(harm[mJ] - bn)) for bn in bern_num])) for mJ in (-1, 0, 1)}
    err_h = max(float(np.max(np.abs(harm[mJ] - bern_num[kmap[mJ]]))) for mJ in (-1, 0, 1))
    ui = ug[1:-1]
    m1 = [md for md in modes[1.0] if md.chir == +1]
    err_o = 0.0
    for md in m1:
        k = int(round(md.m - 0.5))
        rho = md.dens(np.array([s_of_u(x) for x in ui])) / (2 * ui * (1 - ui))     # ds/du = 1/(2u(1-u))
        err_o = max(err_o, float(np.max(np.abs(rho - bern_num[k][1:-1]))))
    bern_ok = err_h < 1e-12 and err_o < 1e-9
    w("### B1: zero-mode densities in u = sin^2(theta/2) [computed]")
    w("")
    w("| k | expected 3 C(2,k) u^k (1-u)^(2-k) [standard, Haldane-sphere lowest level] | from Y_{1,1,m} of sm-zero-modes-S2 | from the 1D solve (rotating-frame m) |")
    w("|---|---|---|---|")
    for k in range(3):
        mJ = [x for x in kmap if kmap[x] == k]
        w("| %d | %s | m = %s | m = %s |" % (k, sp.factor(bern[k]), ", ".join(str(x) for x in mJ),
                                           sp.nsimplify(k + 0.5)))
    w("")
    w("Largest difference from the Bernstein shapes on 201 points: %.1e (harmonics), %.1e (1D solve). Confirmed: %s. "
      "k = 0 is the mode that peaks at the north tip [computed]." % (err_h, err_o, yn(bern_ok)))
    w("")

    th_ex = [sp.integrate(b, (U, 0, SG)) for b in bern]
    so_ex = [sp.integrate(sp.exp(-U / SG) * b, (U, 0, 1)) for b in bern]

    def exact(exprs, sg):
        return [float(e.subs(SG, sg).evalf(40)) for e in exprs]

    def quad(hu, umax, k_from_mJ=True):
        Y = harm_matrix(hu, umax)
        d = np.real(np.diag(Y))
        return [d[[mJ + 1 for mJ in (-1, 0, 1) if kmap[mJ] == k][0]] for k in range(3)]

    sigs = [sp.Rational(3, 10), sp.Rational(1, 10), sp.Rational(3, 100), sp.Rational(1, 100)]
    laws = {"top-hat": (lambda s: s, lambda s: s ** 2 / 3), "soft": (lambda s: 2 * s, lambda s: 2 * s ** 2)}
    lawtxt = {"top-hat": ("sigma", "sigma^2/3"), "soft": ("2 sigma", "2 sigma^2")}
    okB_law, okB_shrink, okB_shrink_all, qd_err = True, True, True, 0.0
    tables = {}
    for prof in ("top-hat", "soft"):
        ex = th_ex if prof == "top-hat" else so_ex
        devs = []
        rowsB = []
        for sg in sigs:
            Yk = exact(ex, sg)
            s = float(sg)
            Yq = quad((lambda u: np.ones_like(u)) if prof == "top-hat" else (lambda u, s=s: np.exp(-u / s)),
                      s if prof == "top-hat" else 1.0)
            qd_err = max(qd_err, max(abs(Yq[k] - Yk[k]) / Yk[k] for k in range(3)))
            r1, r2 = Yk[1] / Yk[0], Yk[2] / Yk[0]
            l1, l2 = laws[prof][0](s), laws[prof][1](s)
            devs.append((abs(r1 / l1 - 1), abs(r2 / l2 - 1)))
            rowsB.append((s, Yk, r1, l1, r2, l2))
        okB_law &= devs[-1][0] < 0.03 and devs[-1][1] < 0.03
        # P2 uses the small-sigma points 0.1 -> 0.03 -> 0.01 [post-hoc narrowing, see README]; the check as first
        # worded (also from 0.3) is still computed and printed.
        okB_shrink &= all(devs[i + 1][0] < devs[i][0] and devs[i + 1][1] < devs[i][1] for i in range(1, len(devs) - 1))
        okB_shrink_all &= all(devs[i + 1][0] < devs[i][0] and devs[i + 1][1] < devs[i][1] for i in range(len(devs) - 1))
        tables[prof] = rowsB
    for prof in ("top-hat", "soft"):
        w("### B2: %s profile, %s [computed: exact sympy integrals; quadrature cross-check below]" % (
            prof, "h = 1 for u < sigma" if prof == "top-hat" else "h = exp(-u/sigma)"))
        w("")
        w("| sigma | Y_0 : Y_1 : Y_2 (exact) | Y_1/Y_0 exact | law %s | exact/law | Y_2/Y_0 exact | law %s | exact/law |" % lawtxt[prof])
        w("|---|---|---|---|---|---|---|---|")
        for s, Yk, r1, l1, r2, l2 in tables[prof]:
            w("| %s | %s : %s : %s | %.6g | %.6g | %.4f | %.6g | %.6g | %.4f |" % (
                fmt(s, 3), fmt(Yk[0]), fmt(Yk[1]), fmt(Yk[2]), r1, l1, r1 / l1, r2, l2, r2 / l2))
        w("")
    w("Leading laws at small sigma: top-hat Y_0 : Y_1 : Y_2 = 3 sigma : 3 sigma^2 : sigma^3 = 1 : sigma : sigma^2/3; "
      "soft 3 sigma : 6 sigma^2 : 6 sigma^3 = 1 : 2 sigma : 2 sigma^2 [identity: lowest-order Taylor terms]. "
      "Every exact/law column moves towards 1 over the small-sigma points 0.1 -> 0.03 -> 0.01: %s; within 3%% at "
      "sigma = 0.01: %s [computed]." % (yn(okB_shrink), yn(okB_law)))
    w("The same check including sigma = 0.3 (as first worded in README): %s%s [post-hoc: P2 was narrowed to the "
      "small-sigma points after the staged test run; see README]." % (
          yn(okB_shrink_all), "" if okB_shrink_all else
          "; the soft Y_2/Y_0 column is non-monotone between sigma = 0.3 and 0.1 (0.3 is not a small sigma)"))
    w("Quadrature with the actual harmonics against the exact integrals: largest relative difference %.1e [computed]." % qd_err)
    w("")
    w("P2 leading corrections: measured ratio-to-law [computed] next to the next Taylor term of each ratio [identity]. "
      "Mapping checked against the laws above: top-hat 1 : sigma : sigma^2/3 gives Y_1 -> 1 + sigma/3 and "
      "Y_2 -> 1 + sigma; soft 1 : 2 sigma : 2 sigma^2 gives Y_1 -> 1 - 2 sigma^2 and Y_2 -> 1 + 2 sigma.")
    w("")
    w("| sigma | top-hat Y_1 measured | 1 + sigma/3 | top-hat Y_2 measured | 1 + sigma | soft Y_1 measured | 1 - 2 sigma^2 | soft Y_2 measured | 1 + 2 sigma | used for P2 (sigma <= 0.1) |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for rt, rs in zip(tables["top-hat"], tables["soft"]):
        s_ = rt[0]
        w("| %s | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %s |" % (
            fmt(s_, 3), rt[2] / rt[3], 1 + s_ / 3, rt[4] / rt[5], 1 + s_, rs[2] / rs[3], 1 - 2 * s_ * s_,
            rs[4] / rs[5], 1 + 2 * s_, yn(s_ <= 0.1 + 1e-12)))
    w("")
    fY = [sp.lambdify(SG, e, "mpmath") for e in so_ex]
    sgg = np.logspace(-2, 0, 401)
    rr = [float(fY[2](x) / fY[0](x)) / (2 * x * x) for x in sgg]
    imax = int(np.argmax(rr))
    w("Why the soft Y_2 ratio-to-law has to turn over: at small sigma it rises like 1 + 2 sigma, but as sigma grows "
      "Y_2/Y_0 tends to 1 while the law 2 sigma^2 keeps growing, so the ratio-to-law must come back down. On a grid "
      "sigma = 0.01 ... 1 its maximum is %.4f at sigma = %.3f [computed]%s. A monotonicity test that includes sigma = 0.3 "
      "therefore measures this turnover, not the law. P2 tests the leading-order law at sigma <= 0.1 [post-hoc], and the "
      "pass does not depend on where the cutoff sits inside that small-sigma region." % (
          rr[imax], sgg[imax], ", between the sigma = 0.1 and 0.3 test points" if 0.1 < sgg[imax] < 0.3 else ""))
    w("")
    w("### B3: the two sigma limits [computed]")
    w("")
    t1 = exact(th_ex, 1)
    th_eq = max(t1) - min(t1) < 1e-12
    w("- Top-hat at sigma = 1 (the whole sphere): Y_0 : Y_1 : Y_2 = %s : %s : %s, all equal: %s [identity: orthonormality]." % (
        fmt(t1[0], 12), fmt(t1[1], 12), fmt(t1[2], 12), yn(th_eq)))
    w("")
    w("| soft sigma | Y_1/Y_0 | Y_2/Y_0 | spread 1 - min/max |")
    w("|---|---|---|---|")
    spreads = []
    for sg in (1, 10, 100, 1000, 10000):
        Yk = exact(so_ex, sg)
        spr = 1 - min(Yk) / max(Yk)
        spreads.append(spr)
        w("| %d | %.8f | %.8f | %.2e |" % (sg, Yk[1] / Yk[0], Yk[2] / Yk[0], spr))
    w("")
    soft_ok = spreads[0] > 0.1 and all(spreads[i + 1] < spreads[i] for i in range(4)) and spreads[-1] < 1e-3
    w("Soft profile: NOT equal at sigma = 1 (spread %.3f); equal only as sigma -> infinity (spread about 1/(2 sigma)): %s [computed]." % (
        spreads[0], yn(soft_ok)))
    w("")
    w("### B4: delta-function brane [computed]")
    w("")
    eta_tip = np.array([MP.Y_north(1, 1, mJ, 0.0, 0.0) for mJ in (-1, 0, 1)])
    order = [[mJ + 1 for mJ in (-1, 0, 1) if kmap[mJ] == k][0] for k in range(3)]
    eta_tip = eta_tip[order]
    Yd = np.outer(np.conj(eta_tip), eta_tip)
    sv_d = np.linalg.svd(Yd, compute_uv=False)
    eta_p = np.array([MP.Y_north(1, 1, mJ, 0.7, 0.3) for mJ in (-1, 0, 1)])[order]
    sv_p = np.linalg.svd(np.outer(np.conj(eta_p), eta_p), compute_uv=False)
    sv_t = np.linalg.svd(Yt, compute_uv=False)
    sv_s = np.linalg.svd(Ysft, compute_uv=False)
    rank1 = sv_d[1] / sv_d[0] < 1e-12 and sv_p[1] / sv_p[0] < 1e-12
    rank3 = sv_t[2] / sv_t[0] > 1e-6 and sv_s[2] / sv_s[0] > 1e-6
    w("- At the tip: |eta_k(tip)|^2 = %s (k = 0, 1, 2); 3/(4 pi) = %.12f. Y = eta^* eta^T has singular values %s: "
      "rank 1, one heavy and two massless generations." % (", ".join("%.12f" % abs(x) ** 2 for x in eta_tip),
                                                          3 / (4 * math.pi), ", ".join("%.3e" % x for x in sv_d)))
    w("- Off the tip (theta = 0.7, phi = 0.3) a delta brane is still rank 1: singular values %s. Rank 1 is a property "
      "of the delta profile, not of the tip [identity: Y is an outer product]." % ", ".join("%.3e" % x for x in sv_p))
    w("- Finite profiles are rank 3: top-hat sigma = 0.3 gives s3/s1 = %.3e, soft sigma = 0.1 gives s3/s1 = %.3e." % (
        sv_t[2] / sv_t[0], sv_s[2] / sv_s[0]))
    w("- Delta brane rank 1: %s; finite profiles rank 3: %s." % (yn(rank1), yn(rank3)))
    w("")

    # ================================================================ Stage C
    w("## Stage C: squashing (a report, not pass/fail)")
    w("")
    w("### C1: zero-mode count for each alpha (printed first) [computed]")
    w("")
    w("| alpha | deficit 2 pi (1 - alpha) | allowed sigma3 = +1 modes (m) | regular count | normalisable count | FD count sigma3 = +1 | FD count sigma3 = -1 | largest FD zero-mode eigenvalue | smallest FD non-zero eigenvalue (those m) | count = 3 |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    counts = {}
    NFD = 2000
    for al in ALPHAS:
        reg = sum(1 for md in allm[al].values() if md.regular)
        nrm = sum(1 for md in allm[al].values() if md.normalisable)
        fd = {+1: 0, -1: 0}
        zero_m = []
        for m in mrange:
            for ch in (+1, -1):
                d, e = fd_rugby(m, NFD, ch, al)
                c = MP._sturm_count(d, e, 0.5)
                fd[ch] += c
                if c:
                    zero_m.append((m, ch, c))
        zmax, nz = 0.0, float("inf")
        for m, ch, c in zero_m:
            d, e = fd_rugby(m, NFD, ch, al)
            zmax = max(zmax, MP._kth_eig(d, e, c - 1, lo=-5.0, hi=400.0))
            nz = min(nz, MP._kth_eig(d, e, c, lo=-5.0, hi=400.0))
        allowed = [md for md in modes[al]]
        cnt = len(allowed)
        counts[al] = cnt
        w("| %s | %.4f pi | %s | %d | %d | %d | %d | %.4f | %.4f | %s |" % (
            al, 2 * (1 - al), ", ".join("%s%s" % (sp.nsimplify(md.m), "" if md.chir > 0 else " (sigma3 = -1)") for md in allowed),
            reg, nrm, fd[+1], fd[-1], zmax, nz, yn(cnt == 3)))
    w("")
    if all(counts[al] == 3 for al in ALPHAS):
        w("The count stays 3 for every alpha here, so all ratios below use three generations [computed]. Regularity and "
          "normalisability pick the same modes, m = 1/2, 3/2, 5/2 (k = 0, 1, 2), at every alpha <= 1 [computed].")
    else:
        w("THE COUNT IS NOT 3 FOR EVERY ALPHA (see table). Ratios below are only given where it is 3.")
    w("Tip exponents: |psi|^2 ~ r^p near each tip with p_N = 2m/alpha - 1 and p_S = 2(3 - m)/alpha - 1 [identity]; "
      "numerical slopes agree to %.1e. 1D solve against the closed form: largest relative difference in ln a %.1e [computed]." % (
          exp_err, ode_err))
    w("")
    w("Extra observation [computed; boundary-condition choice]: for the k = 0 mode p_N = 1/alpha - 1, which is > 0 for "
      "alpha < 1. So on a cone |psi_0|^2 vanishes at the tip, like r^(1/alpha - 1); a strictly point-like brane sitting "
      "exactly on a conical tip would couple to none of the three modes [boundary-condition choice]. This relies on the "
      "regular tip condition the code uses (both tip exponents >= 0); a brane carrying its own flux or tension would "
      "shift that exponent. A finite width is needed on the rugby ball.")
    w("Venus's note [standard]: on a cone, spinors pick up r^(1/alpha - 1) from the spin connection, so "
      "|eta_k|^2 \u221d r^((2k+1)/alpha - 1). That matches the closed form (p_N = 2m/alpha - 1 with m = k + 1/2), and "
      "the shared factor cancels in the ratios.")
    w("")
    w("### C2: top-hat ratios at a fixed area fraction sigma = 0.1 [computed]")
    w("")
    w("| alpha | Y_1/Y_0 | Y_2/Y_0 | closed-form check (regularised incomplete beta) | sigma^(1/alpha) | sigma^(2/alpha) |")
    w("|---|---|---|---|---|---|")
    c2 = {}
    beta_chk = 0.0
    for al in ALPHAS:
        if counts[al] != 3:
            continue
        ms = [md for md in modes[al] if md.chir == +1]
        Yk = [tophat_Y(md, 0.1) for md in ms]
        ab = [(md.m / al + 0.5, (2 * q - md.m) / al + 0.5) for md in ms]
        Ybeta = [float(betainc(a, b, 0.1)) for a, b in ab]
        beta_chk = max(beta_chk, max(abs(Yk[k] - Ybeta[k]) / Ybeta[k] for k in range(3)))
        c2[al] = (Yk[1] / Yk[0], Yk[2] / Yk[0])
        w("| %s | %.6g | %.6g | %.1e | %.4g | %.4g |" % (al, c2[al][0], c2[al][1],
                                                     max(abs(Yk[k] - Ybeta[k]) / Ybeta[k] for k in range(3)), 0.1 ** (1 / al), 0.1 ** (2 / al)))
    w("")
    dep = max(c2[al][0] for al in c2) / min(c2[al][0] for al in c2)
    w("At the same area fraction the ratios change with alpha (Y_1/Y_0 varies by a factor %.1f across alpha = 1 ... 0.5), "
      "so they depend on alpha as well as on sigma [computed]. Smaller alpha (bigger deficit) gives a steeper hierarchy." % dep)
    w("")
    w("### C3: slope of Y_k/Y_0 against sigma, versus Venus's estimate k/alpha [prediction]")
    w("")
    sfit = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4]
    w("| alpha | k | fitted slope (sigma = 1e-2 ... 1e-4) [computed] | k/alpha [prediction] | fitted - predicted | leading prefactor C_k [standard asymptotics] | Y_k/Y_0 / (C_k sigma^(k/alpha)) at sigma = 1e-4 |")
    w("|---|---|---|---|---|---|---|")
    slopes = {}
    for al in ALPHAS:
        if counts[al] != 3:
            continue
        ms = [md for md in modes[al] if md.chir == +1]
        Y = np.array([[tophat_Y(md, s) for md in ms] for s in sfit])
        ab = [(md.m / al + 0.5, (2 * q - md.m) / al + 0.5) for md in ms]
        for k in (1, 2):
            r = Y[:, k] / Y[:, 0]
            sl = float(np.polyfit(np.log(sfit), np.log(r), 1)[0])
            a0, b0 = ab[0]
            ak, bk = ab[k]
            Ck = (a0 * beta_fn(a0, b0)) / (ak * beta_fn(ak, bk))
            slopes[(al, k)] = sl
            w("| %s | %d | %.4f | %.4f | %+.4f | %.6g | %.5f |" % (al, k, sl, k / al, sl - k / al, Ck, r[-1] / (Ck * sfit[-1] ** (k / al))))
    w("")
    worst = max(abs(slopes[key] - key[1] / key[0]) for key in slopes)
    w("Venus's estimate holds: the fitted slopes match k/alpha to within %.3f [computed]. Reason [identity]: the solved "
      "densities are rho_k(u) ∝ u^(m/alpha - 1/2) (1 - u)^((3 - m)/alpha - 1/2), so a top-hat gives Y_k ~ sigma^((k + 1/2)/alpha + 1/2) "
      "and Y_k/Y_0 ~ C_k sigma^(k/alpha). The small residual is the O(sigma) correction [finite-size]." % worst)
    w("")

    # ================================================================ Stage D
    w("## Stage D: mixing from a tilted second brane (alpha = 1) [prediction]")
    w("")
    nt, npd = 200, 200
    xg, wg = np.polynomial.legendre.leggauss(nt)
    TH, PH = np.meshgrid(np.arccos(xg), 2 * math.pi * np.arange(npd) / npd, indexing="ij")
    WG = np.outer(wg, np.full(npd, 2 * math.pi / npd))
    Ys = [MP.Y_north(1, 1, mJ, TH, PH) for mJ in (-1, 0, 1)]
    Ys = [Ys[i] for i in order]
    sigD = 0.1

    def yuk(bt):
        cg = np.cos(TH) * math.cos(bt) + np.sin(TH) * math.sin(bt) * np.cos(PH)
        h = np.exp(-(1 - cg) / 2 / sigD)
        return np.array([[np.sum(WG * h * np.conj(Ys[i]) * Ys[j]) for j in range(3)] for i in range(3)])

    Yu = yuk(0.0)
    exD = exact(so_ex, sp.Rational(1, 10))
    dchk = max(abs(Yu[k, k].real - exD[k]) / exD[k] for k in range(3))
    Uu, Su, _ = np.linalg.svd(Yu)
    w("Up-type brane at the north tip, down-type brane at polar angle beta; soft profile sigma = 0.1 for both. "
      "Quadrature check of the up-type diagonal against the exact soft integrals: %.1e [computed]. Mass order: "
      "index 1 = heaviest (k = 0, third generation), index 3 = lightest." % dchk)
    w("")
    w("| beta (rad) | abs(V) rows (computed, mass-ordered) | max abs(abs(V) - abs(d^1(beta))) | abs(V_12) | abs(V_23) | sin(beta)/sqrt(2) | abs(V_13) | (1 - cos beta)/2 |")
    w("|---|---|---|---|---|---|---|---|")
    dmax = 0.0
    for bt in (0.05, 0.1, 0.2, 0.3, 0.5):
        Ud, Sd, _ = np.linalg.svd(yuk(bt))
        V = np.abs(Uu.conj().T @ Ud)
        d1 = np.abs(np.array([[MP.wigner_d(1, a, b, bt) for b in (-1, 0, 1)] for a in (-1, 0, 1)]))
        dd = float(np.max(np.abs(V - d1)))
        dmax = max(dmax, dd)
        w("| %s | %s | %.1e | %.5f | %.5f | %.5f | %.6f | %.6f |" % (
            bt, "; ".join(" ".join("%.4f" % x for x in row) for row in V), dd, V[2, 1], V[1, 0],
            math.sin(bt) / math.sqrt(2), V[2, 0], (1 - math.cos(bt)) / 2))
    w("")
    w("abs(V) equals abs(d^1(beta)) to %.1e for every beta [computed], as predicted: the second brane is the first one "
      "rotated, and the three generations form a j = 1 triplet [identity]. Neighbouring mixing sin(beta)/sqrt(2) ~ beta, "
      "1-3 mixing (1 - cos beta)/2 ~ beta^2/4 [computed]." % dmax)
    w("")
    w("Scope [standard]: this d^1(beta) result holds only on the round sphere (alpha = 1). On the rugby ball the "
      "isometry drops from SU(2) to U(1), so a tilt is no longer a symmetry and does not act as d^1(beta).")
    w("")
    vus, vcb, vub = 0.2243, 0.0411, 0.00382
    bfit = math.asin(math.sqrt(2) * vus)
    w("Pattern against real quark mixing [hive-interpretation]; magnitudes |V_us| = %.4f, |V_cb| = %.4f, |V_ub| = %.5f "
      "[assumed input: PDG 2024, approximate]:" % (vus, vcb, vub))
    w("- What matches: the 1-3 element is second order, much smaller than the neighbours.")
    w("- What does not: d^1(beta) makes the two neighbouring mixings EQUAL (V_12 = V_23), while real |V_cb| is about "
      "%.1f times smaller than |V_us|. Fitting beta = %.3f rad to |V_us| predicts |V_cb| = %.3f and |V_ub| = %.4f, too big by "
      "factors of about %.0f and %.0f. One tilt angle on a round sphere gives the right kind of hierarchy, not the right sizes." % (
          vus / vcb, bfit, math.sin(bfit) / math.sqrt(2), (1 - math.cos(bfit)) / 2,
          (math.sin(bfit) / math.sqrt(2)) / vcb, ((1 - math.cos(bfit)) / 2) / vub))
    w("")

    # ================================================================ PASS table
    with open(os.path.join(HERE, "README.md"), encoding="utf-8") as fh:
        rd = fh.read()
    need = ["breaks SO(3) down to U(1)", "Two of Job Two's three massless flavour", "sigma, alpha and beta are all [assumed input]",
            "R is the radion", "Randjbar-Daemi", "Cremades", "hep-th/0404229", "torus analogue"]
    okP4 = all(x in rd for x in need)
    P1 = okA1 and okA2
    P2 = bern_ok and okB_law and okB_shrink and rank1 and rank3
    P3 = th_eq and soft_ok
    w("## PASS/FAIL (criteria fixed in README.md before the run)")
    w("")
    w("| criterion | what | result |")
    w("|---|---|---|")
    w("| P1 | Stage A identities (equal singular values at every alpha; diagonal for axial profiles) | %s |" % pf(P1))
    w("| P2 | Stage B shapes confirmed; ratios match each profile's own law at small sigma (sigma <= 0.1 [post-hoc]); delta brane rank 1, finite rank 3 | %s |" % pf(P2))
    w("| P3 | both sigma limits (top-hat equal at sigma = 1; soft equal only as sigma -> infinity) | %s |" % pf(P3))
    w("| P4 | README carries the caveats and references | %s |" % pf(okP4))
    w("")
    w("Stage C (report): count 3 at every alpha = %s; slopes k/alpha confirmed. Stage D (report): abs(V) = abs(d^1(beta)) "
      "confirmed; pattern partly matches real mixing [hive-interpretation]." % yn(all(counts[al] == 3 for al in ALPHAS)))
    w("")

    # ---------------------------------------------------------------- plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
        sg = np.logspace(-3, 0, 60)
        for prof, col in (("top-hat", "tab:blue"), ("soft", "tab:red")):
            ex = th_ex if prof == "top-hat" else so_ex
            fl = [sp.lambdify(SG, e, "mpmath") for e in ex]
            r = np.array([[float(f(s)) for f in fl] for s in sg])
            ax[0].loglog(sg, r[:, 1] / r[:, 0], color=col, label="%s Y1/Y0" % prof)
            ax[0].loglog(sg, r[:, 2] / r[:, 0], color=col, ls="--", label="%s Y2/Y0" % prof)
            ax[0].loglog(sg, laws[prof][0](sg), color=col, lw=0.8, ls=":")
            ax[0].loglog(sg, laws[prof][1](sg), color=col, lw=0.8, ls=":")
        ax[0].set_xlabel("sigma (area fraction)"); ax[0].set_ylabel("ratio"); ax[0].set_title("Stage B, alpha = 1 (dotted: leading laws)")
        ax[0].legend(fontsize=8)
        sc = np.logspace(-4, -1, 13)
        for al, col in zip(ALPHAS, ("k", "tab:green", "tab:orange", "tab:purple")):
            if counts[al] != 3:
                continue
            ms = [md for md in modes[al] if md.chir == +1]
            Y = np.array([[tophat_Y(md, s) for md in ms] for s in sc])
            ax[1].loglog(sc, Y[:, 1] / Y[:, 0], color=col, label="alpha = %s, k = 1" % al)
            ax[1].loglog(sc, Y[:, 2] / Y[:, 0], color=col, ls="--", label="alpha = %s, k = 2" % al)
        ax[1].set_xlabel("sigma (area fraction)"); ax[1].set_ylabel("Y_k / Y_0"); ax[1].set_title("Stage C, top-hat (slope k/alpha)")
        ax[1].legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(os.path.join(HERE, "ratios.png"), dpi=110)
        plt.close(fig)
        w("Picture: ratios.png (left: Stage B ratios and laws; right: Stage C ratios for each alpha).")
    except Exception as exc:
        w("Picture: not made (%s)." % exc)
    w("")
    after = folder_state(S2)
    w("sm-zero-modes-S2 untouched during the run (file hashes and mtimes before = after): %s [computed]." % yn(after == S2_BEFORE))
    w("")
    w("End of results. Toy bookkeeping; no Standard-Model derivation and no quantum-gravity claim.")
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
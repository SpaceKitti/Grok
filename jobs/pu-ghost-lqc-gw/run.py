#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job Seven: (G) the Pais-Uhlenbeck ghost oscillator, free and interacting (Smilga's benign vs
malicious ghosts); (L) a tensor (gravitational-wave) mode through the effective LQC bounce.

Writes RESULTS.md (ONLY ever written by this script), pu_runaway.png and lqc_beta.png next to itself.
Run:  set PYTHONIOENCODING=utf-8;  python -B run.py      (a few minutes)
Every number in RESULTS.md is printed from a variable; no computed number is typed into prose.
Fold-in pass (after the Venus/Helios PASS): G5a, G5b and the Part L [standard] fall-off line were added, with their
thresholds fixed before the fold-in run; the G1–G4 and L1–L4 thresholds are unchanged.
Follow-up (Venus review request): G5b also prints the conditional ghost share S and the A ranges where each sign
of λ has the larger Δ and S [post-hoc]; no threshold, grade or verdict changed.
"""
import os, time, platform, math
import numpy as np
import scipy
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from scipy.special import hyp2f1, beta as Beta

HERE = os.path.dirname(os.path.abspath(__file__))
T_START = time.time()
OUT = []


def out(line=""):
    print(line, flush=True)
    OUT.append(line)


# =====================================================================================
# Parameters and PASS thresholds: FIXED BEFORE THE FIRST RUN (do not tune afterwards)
# =====================================================================================
# ---- Part G ----
W1, W2 = 1.0, (np.sqrt(5.0) - 1.0) / 2.0     # unequal, non-resonant (golden ratio) frequencies [assumed input]
DT, T_MAIN, T_LONG = 0.01, 300.0, 600.0      # RK4 step, primary horizon, sensitivity horizon [assumed input]
R_RUN = (10.0, 100.0)                        # runaway if R(t)/q_* >= 10 (primary); 100 recorded as check [assumed input]
N_SAMPLE, SEED = 200, 7                      # starts per amplitude, RNG seed [assumed input]
A_GRID = [0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0]   # |u| in units of q_*
LAM_TABLE = [0.1, 1.0, 10.0]                 # λ values for the physical-amplitude table
AMP_PHYS = [0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0]
LAM_SCALE, A_SCALE = [0.25, 4.0], [0.3, 1.0] # scaling-identity check (compare with λ = 1)
A_DTCHECK = [0.3, 0.6, 1.0, 1.5]             # step-halving check (dt/2, to T_MAIN)
A_NEG = [0.02, 0.05, 0.1, 0.2, 0.3]          # λ = -1 (report only)
C_SMILGA = np.round(np.arange(0.20, 0.45001, 0.0025), 4)   # equal-frequency Smilga model, q(0) = c Ω²/√α
C_LINE = np.round(np.arange(0.05, 3.00001, 0.01), 3)       # unequal frequencies, q(0) = c q_*, rest 0 (report)
C_NEG_EQ = [0.02, 0.05, 0.1, 0.2]            # equal frequency, λ = -1 (report only)
N_FREE, U_FREE = 50, 0.5                   # free-PU check: starts on the 3-sphere of radius 0.5
ETA_FD = [0.0, 0.4, 0.8, 1.5, 3.0, 10.0, 50.0]   # L1 finite-difference check points
TH_FREE_DRIFT, TH_FREE_BOUND = 1e-6, 50.0    # G1: E1, E2 separately conserved; max R/R0 bounded
TH_EQ_REL, TH_EQ_SLOPE = 1e-6, (0.9, 1.1)    # G2: RK4 vs exact secular solution; envelope log-log slope
TH_DRIFT, DRIFT_RMAX = 1e-6, 2.0             # G3a: |ΔH|/E_abs for survivors whose max R/q_* <= 2
TH_DT = 0.02                                 # G3b: |f(dt) - f(dt/2)|
ISLAND_A, TOP_FRAC = 0.1, 0.5                # G3c: f = 0 for A <= 0.1, f >= 0.5 at the largest A
TH_SCALE = 1                                 # G3d: counts agree within ±1 trajectory
SMILGA_WINDOW = (0.25, 0.35)                 # G4: Smilga's c_crit ≈ 0.3 Ω²/√α
# ---- Fold-in pass (Venus maths / Helios physics review): FIXED BEFORE THE FOLD-IN RUN ----
LAM_TR = [0.1, 0.25, 1.0, 4.0, 10.0]           # G5a: λ values already scanned (λ-table and scaling check)
A_TR = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6]  # G5a: scaled amplitudes A = |u|√λ/(ω₁ω₂) through the half-runaway point
TH_A50, TH_A50_SLOPE = 0.01, 0.01             # G5a: max |A₅₀(λ) − A₅₀(1)|;  |d ln a₅₀/d ln λ + 1/2|
A_SIGN = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]   # G5b: scaled amplitudes A√|λ|, |λ| = 1
SIGN_DIFF = 0.25                               # G5b: sign matters if max_A |Δ(λ>0) − Δ(λ<0)| ≥ 0.25, Δ = f_ghost − f_control, t ≤ T_MAIN
TH_XCHECK = 0.03                               # G5b: ghost in normal-mode vs q variables, same starts, |Δf| ≤ 0.03
# ---- Part L ----
K_GRID = np.logspace(-1.0, 1.0, 21)          # k/k_B over two decades
X_MAIN, X_CONV = 200.0, 400.0                # start/end at |kη| = X  (X_CONV = convergence column)
RTOL, ATOL = 1e-12, 1e-15
TH_ETA, TH_FD = 1e-10, 1e-6                  # L1: η(t) closed form vs quadrature; a''/a finite-difference check
TH_WRONSK = 1e-8                             # L2: | |α|²-|β|²-1 |
TH_CONV, CONV_FLOOR = 1e-3, 1e-10            # L3: rel. change X=200 -> 400 where |β|² > 1e-10
SMALL_K, TH_SMALLK = 0.3, 0.1                # L4a: |β|² >= 0.1 for k <= 0.3 k_B
LARGE_K, TH_LARGEK = 3.0, 1e-3               # L4b: |β|² < 1e-3 for k >= 3 k_B, and decreasing for k >= k_B


# =====================================================================================
# Part G
# =====================================================================================
def ham(Y, L, S, P):
    q, q1, q2, q3 = Y
    return 0.5 * q2 * q2 - q1 * q3 - 0.5 * S * q1 * q1 - 0.5 * P * q * q + 0.25 * L * q ** 4


def eabs(Y, L, S, P):
    q, q1, q2, q3 = Y
    return 0.5 * q2 * q2 + np.abs(q1 * q3) + 0.5 * S * q1 * q1 + 0.5 * P * q * q + 0.25 * np.abs(L) * q ** 4


def modes(Y, w1, w2):
    """Smilga (2009) eq. (4): normal-mode variables from Ostrogradsky (q, p_q, x = q̇, p_x = q̈)."""
    q, q1, q2, q3 = Y
    S = w1 * w1 + w2 * w2
    pq, x, px = -S * q1 - q3, q1, q2
    d = np.sqrt(w1 * w1 - w2 * w2)
    X1 = (pq + w1 * w1 * x) / (w1 * d); X2 = (px + w1 * w1 * q) / d
    P1 = w1 * (px + w2 * w2 * q) / d;   P2 = (pq + w2 * w2 * x) / d
    return 0.5 * (P1 ** 2 + w1 ** 2 * X1 ** 2), 0.5 * (P2 ** 2 + w2 ** 2 * X2 ** 2)


DNM = np.sqrt(W1 * W1 - W2 * W2)


def u_to_nm(Y):
    """(q, q̇, q̈, q⃛) at the main frequencies -> Smilga normal modes (X1, P1, X2, P2), eq. (4)."""
    q, q1, q2, q3 = Y
    S = W1 * W1 + W2 * W2
    pq, x, px = -S * q1 - q3, q1, q2
    return np.stack(((pq + W1 * W1 * x) / (W1 * DNM), W1 * (px + W2 * W2 * q) / DNM,
                     (px + W1 * W1 * q) / DNM, (pq + W2 * W2 * x) / DNM))


def nm_to_u(Z):
    """Inverse map, Smilga (2009) eq. (3)."""
    X1, P1, X2, P2 = Z
    S = W1 * W1 + W2 * W2
    q = (W1 * X2 - P1) / (W1 * DNM); x = (W1 * X1 - P2) / DNM
    px = (W1 * P1 - W2 * W2 * X2) / DNM; pq = W1 * (W1 * P2 - W2 * W2 * X1) / DNM
    return np.stack((q, x, px, -pq - S * x))


def ham_nm(Z, L, s):
    """s = -1: PU ghost E1 - E2 + λq⁴/4;  s = +1: no-ghost control E1 + E2 + λq⁴/4 (same q)."""
    X1, P1, X2, P2 = Z
    q = (W1 * X2 - P1) / (W1 * DNM)
    return 0.5 * (P1 ** 2 + W1 ** 2 * X1 ** 2) + s * 0.5 * (P2 ** 2 + W2 ** 2 * X2 ** 2) + 0.25 * L * q ** 4


def eabs_nm(Z, L):
    X1, P1, X2, P2 = Z
    q = (W1 * X2 - P1) / (W1 * DNM)
    return 0.5 * (P1 ** 2 + W1 ** 2 * X1 ** 2) + 0.5 * (P2 ** 2 + W2 ** 2 * X2 ** 2) + 0.25 * np.abs(L) * q ** 4


def rk4_nm(Z, L, s, h):
    def f(Zz):
        X1, P1, X2, P2 = Zz
        q = (W1 * X2 - P1) / (W1 * DNM); Vp = L * q ** 3
        return np.stack((P1 - Vp / (W1 * DNM), -W1 * W1 * X1, s * P2, -s * W2 * W2 * X2 - Vp / DNM))
    k1 = f(Z); k2 = f(Z + 0.5 * h * k1); k3 = f(Z + 0.5 * h * k2); k4 = f(Z + h * k3)
    return Z + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def run_batch_nm(Z0, L, s, Q, wb, dt, tmax):
    N = Z0.shape[1]
    tc = np.full(N, np.inf); Zend = np.full((4, N), np.nan)
    act = np.arange(N); Z, La, sa = Z0.copy(), L.copy(), s.copy(); tca = tc.copy()
    nsteps = int(round(tmax / dt))
    with np.errstate(all="ignore"):
        for n in range(1, nsteps + 1):
            Z = rk4_nm(Z, La, sa, dt)
            R = pnorm(nm_to_u(Z), wb) / Q
            new = ~(R < R_RUN[0]) & np.isinf(tca)
            if new.any():
                tca[new] = n * dt
            if n % 50 == 0 or n == nsteps:
                keep = np.isinf(tca)
                tc[act] = tca
                if n == nsteps:
                    Zend[:, act[keep]] = Z[:, keep]
                if not keep.all():
                    act, Z, La, sa, tca = act[keep], Z[:, keep], La[keep], sa[keep], tca[keep]
    return dict(tc=tc, Zend=Zend, H0=ham_nm(Z0, L, s), E0=eabs_nm(Z0, L))


def a50g(grid, fr):
    for i in range(1, len(grid)):
        if fr[i - 1] < 0.5 <= fr[i]:
            return grid[i - 1] + (0.5 - fr[i - 1]) * (grid[i] - grid[i - 1]) / (fr[i] - fr[i - 1])
    return None


def pnorm(Y, wb):
    q, q1, q2, q3 = Y
    return np.sqrt(q * q + (q1 / wb) ** 2 + (q2 / wb ** 2) ** 2 + (q3 / wb ** 3) ** 2)


def rk4(Y, L, S, P, h):
    def f(Z):
        q, q1, q2, q3 = Z
        return np.stack((q1, q2, q3, -S * q2 - P * q + L * q * q * q))
    k1 = f(Y); k2 = f(Y + 0.5 * h * k1); k3 = f(Y + 0.5 * h * k2); k4 = f(Y + h * k3)
    return Y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def run_batch(Y0, L, S, P, Q, Wb, dt, tmax, t_mark):
    N = Y0.shape[1]
    tc = np.full((2, N), np.inf)
    R0 = pnorm(Y0, Wb) / Q
    Rmax = R0.copy()
    out_mark = np.full((4, N), np.nan); out_end = np.full((4, N), np.nan)
    act = np.arange(N)
    Y, La, Sa, Pa, Qa, Wa = Y0.copy(), L.copy(), S.copy(), P.copy(), Q.copy(), Wb.copy()
    tca, Rma = tc.copy(), Rmax.copy()
    nsteps, nmark = int(round(tmax / dt)), int(round(t_mark / dt))
    with np.errstate(all="ignore"):
        for n in range(1, nsteps + 1):
            Y = rk4(Y, La, Sa, Pa, dt)
            R = pnorm(Y, Wa) / Qa
            Rma = np.fmax(Rma, R)
            for j in (0, 1):
                new = ~(R < R_RUN[j]) & np.isinf(tca[j])
                if new.any():
                    tca[j, new] = n * dt
            if n == nmark:
                out_mark[:, act] = Y
            if n % 50 == 0 or n == nsteps:
                keep = np.isinf(tca[1])
                if not keep.all() or n == nsteps:
                    tc[:, act] = tca; Rmax[act] = Rma
                    if n == nsteps:
                        out_end[:, act[keep]] = Y[:, keep]
                    act = act[keep]; Y = Y[:, keep]; La, Sa, Pa, Qa, Wa = La[keep], Sa[keep], Pa[keep], Qa[keep], Wa[keep]
                    tca, Rma = tca[:, keep], Rma[keep]
    return dict(tc=tc, Rmax=Rmax, R0=R0, H0=ham(Y0, L, S, P), E0=eabs(Y0, L, S, P),
                Ymark=out_mark, Yend=out_end)


def part_g():
    out("# Part G: the Pais–Uhlenbeck oscillator (ghost)")
    out("")
    out("L = ½[q̈² − (ω₁²+ω₂²)q̇² + ω₁²ω₂²q²] − (λ/4)q⁴  ⇒  q⁽⁴⁾ + (ω₁²+ω₂²)q̈ + ω₁²ω₂²q = λq³.")
    out("Ostrogradsky: x = q̇, p_x = q̈, p_q = −(ω₁²+ω₂²)q̇ − q⃛,  H = p_q x + p_x²/2 + (ω₁²+ω₂²)x²/2 − ω₁²ω₂²q²/2 + λq⁴/4.")
    out(f"Main frequencies [assumed input]: ω₁ = {W1:g}, ω₂ = {W2:.10f} (golden ratio, away from the 1:1, 1:2, 1:3 resonances).")
    out("")
    # ---------------- G1 identities ----------------
    out("## G1: free PU splits into two oscillators of opposite energy sign [identity]")
    out("")
    q, pq, x, px = sp.symbols("q p_q x p_x", real=True)
    w1, w2 = sp.symbols("omega1 omega2", positive=True)
    D = sp.sqrt(w1 ** 2 - w2 ** 2)
    X1 = (pq + w1 ** 2 * x) / (w1 * D); X2 = (px + w1 ** 2 * q) / D
    P1 = w1 * (px + w2 ** 2 * q) / D;   P2 = (pq + w2 ** 2 * x) / D
    Hs = pq * x + px ** 2 / 2 + (w1 ** 2 + w2 ** 2) * x ** 2 / 2 - w1 ** 2 * w2 ** 2 * q ** 2 / 2

    def pb(f, g):
        return sp.simplify(sp.diff(f, q) * sp.diff(g, pq) - sp.diff(f, pq) * sp.diff(g, q)
                           + sp.diff(f, x) * sp.diff(g, px) - sp.diff(f, px) * sp.diff(g, x))
    brackets = {"{X1,P1}": pb(X1, P1), "{X2,P2}": pb(X2, P2), "{X1,X2}": pb(X1, X2), "{P1,P2}": pb(P1, P2),
                "{X1,P2}": pb(X1, P2), "{X2,P1}": pb(X2, P1)}
    resH = sp.simplify(Hs - (P1 ** 2 + w1 ** 2 * X1 ** 2) / 2 + (P2 ** 2 + w2 ** 2 * X2 ** 2) / 2)
    ok_sym = (resH == 0 and brackets["{X1,P1}"] == 1 and brackets["{X2,P2}"] == 1
              and all(brackets[kk] == 0 for kk in ("{X1,X2}", "{P1,P2}", "{X1,P2}", "{X2,P1}")))
    out("Canonical map (Smilga 2009, eq. 4), checked with sympy for symbolic ω₁ > ω₂:")
    out("  " + ", ".join(f"{kk} = {vv}" for kk, vv in brackets.items()))
    out(f"  H − [½(P₁²+ω₁²X₁²) − ½(P₂²+ω₂²X₂²)] = {resH}   ⇒  E = E₁ − E₂ {'(exact)' if ok_sym else '(FAILED)'}.")
    out("  The map carries 1/√(ω₁²−ω₂²): it is singular at ω₁ = ω₂, where the split fails (see G2) [identity].")
    S0, P0 = W1 ** 2 + W2 ** 2, (W1 * W2) ** 2
    Ms = [10.0, 100.0, 1000.0]
    Hb = [float(ham(np.array([0.0, 1.0, 0.0, M]), 0.0, S0, P0)) for M in Ms]
    out("  Unbounded below: the state q = q̈ = 0, q̇ = 1, q⃛ = M has H = −M − (ω₁²+ω₂²)/2: " +
        ", ".join(f"M={M:g}: H={h:.3f}" for M, h in zip(Ms, Hb)) + " [identity].")
    out("")
    return ok_sym, S0, P0


def part_g_numerics(S0, P0):
    rng = np.random.default_rng(SEED)
    Dir = rng.standard_normal((4, N_SAMPLE)); Dir /= np.sqrt((Dir ** 2).sum(0))
    wb0 = np.sqrt(W1 * W2)
    groups, Ys, Ls, Ss, Ps, Qs, Wbs = [], [], [], [], [], [], []

    def add(label, Y0, lam, S, P, qs, wb):
        n = Y0.shape[1]
        groups.append((label, sum(y.shape[1] for y in Ys), n))
        Ys.append(Y0); Ls.append(np.full(n, lam)); Ss.append(np.full(n, S)); Ps.append(np.full(n, P))
        Qs.append(np.full(n, qs)); Wbs.append(np.full(n, wb))

    def sphere(Arad, qs, wb):
        return Arad * np.vstack((Dir[0], Dir[1] * wb, Dir[2] * wb ** 2, Dir[3] * wb ** 3))

    qst = lambda lam: W1 * W2 / np.sqrt(abs(lam))
    for A in A_GRID:
        add(("main", A), sphere(A * qst(1.0), 1, wb0), 1.0, S0, P0, qst(1.0), wb0)
    for lam in LAM_TABLE:
        for a in AMP_PHYS:
            add(("lam", lam, a), sphere(a, 1, wb0), lam, S0, P0, qst(lam), wb0)
    for lam in LAM_SCALE:
        for A in A_SCALE:
            add(("scale", lam, A), sphere(A * qst(lam), 1, wb0), lam, S0, P0, qst(lam), wb0)
    for A in A_NEG:
        add(("neg", A), sphere(A * qst(-1.0), 1, wb0), -1.0, S0, P0, qst(-1.0), wb0)
    Ysm = np.zeros((4, C_SMILGA.size)); Ysm[0] = C_SMILGA
    add(("smilga",), Ysm, 1.0, 2.0, 1.0, 1.0, 1.0)
    Yl = np.zeros((4, C_LINE.size)); Yl[0] = C_LINE * qst(1.0)
    add(("line",), Yl, 1.0, S0, P0, qst(1.0), wb0)
    Yn = np.zeros((4, len(C_NEG_EQ))); Yn[0] = C_NEG_EQ
    add(("negeq",), Yn, -1.0, 2.0, 1.0, 1.0, 1.0)
    rngf = np.random.default_rng(SEED + 1)
    Df = rngf.standard_normal((4, N_FREE)); Df /= np.sqrt((Df ** 2).sum(0))
    add(("free",), U_FREE * np.vstack((Df[0], Df[1] * wb0, Df[2] * wb0 ** 2, Df[3] * wb0 ** 3)), 0.0, S0, P0, 1e12, wb0)
    for lam in LAM_TR:
        for A in A_TR:
            add(("tr", lam, A), sphere(A * qst(lam), 1, wb0), lam, S0, P0, qst(lam), wb0)
    Y0 = np.hstack(Ys)
    t0 = time.time()
    res = run_batch(Y0, np.concatenate(Ls), np.concatenate(Ss), np.concatenate(Ps), np.concatenate(Qs),
                    np.concatenate(Wbs), DT, T_LONG, T_MAIN)
    t_main = time.time() - t0
    # dt/2 check
    Yd = np.hstack([sphere(A * qst(1.0), 1, wb0) for A in A_DTCHECK]); nd = Yd.shape[1]
    t0 = time.time()
    resd = run_batch(Yd, np.ones(nd), np.full(nd, S0), np.full(nd, P0), np.full(nd, qst(1.0)), np.full(nd, wb0),
                     DT / 2, T_MAIN, T_MAIN)
    t_half = time.time() - t0
    G = {g[0]: (g[1], g[2]) for g in groups}
    # G5b: ghost (s = -1) and no-ghost control (s = +1) in normal-mode variables, same starts, both signs of λ
    Us, Lz, Sz, gz = [], [], [], {}
    for s_ in (-1.0, 1.0):
        for lam in (1.0, -1.0):
            for A in A_SIGN:
                U0 = sphere(A * qst(lam), 1, wb0)
                gz[(s_, lam, A)] = (sum(u.shape[1] for u in Us), U0.shape[1])
                Us.append(U0); Lz.append(np.full(U0.shape[1], lam)); Sz.append(np.full(U0.shape[1], s_))
    U0 = np.hstack(Us); Lc = np.concatenate(Lz); Sc = np.concatenate(Sz)
    Zn0 = u_to_nm(U0)
    rt_err = float(np.abs(nm_to_u(Zn0) - U0).max() / np.abs(U0).max())
    gh = Sc < 0
    h_err = float(np.abs(ham_nm(Zn0[:, gh], Lc[gh], -1.0) - ham(U0[:, gh], Lc[gh], S0, P0)).max()
                  / eabs(U0[:, gh], Lc[gh], S0, P0).max())
    t0 = time.time()
    resn = run_batch_nm(Zn0, Lc, Sc, qst(1.0), wb0, DT, T_LONG)
    NM = dict(res=resn, groups=gz, t=time.time() - t0, n=Zn0.shape[1], rt=rt_err, herr=h_err, L=Lc, s=Sc)
    return res, resd, G, t_main, t_half, NM


def frac(res, sl, T, j=0):
    o, n = sl
    return float(np.mean(res["tc"][j, o:o + n] <= T)), int(np.sum(res["tc"][j, o:o + n] <= T)), n


def eq_free_check():
    """Equal frequencies, free: exact secular solution q = cos t + (t/2) sin t for q(0)=1."""
    Y = np.array([[1.0], [0.0], [0.0], [0.0]])
    L, S, P = np.zeros(1), np.full(1, 2.0), np.ones(1)
    n = int(round(T_LONG / DT)); ts = DT * np.arange(n + 1); qs = np.empty(n + 1); qs[0] = 1.0
    for i in range(1, n + 1):
        Y = rk4(Y, L, S, P, DT); qs[i] = Y[0, 0]
    ex = np.cos(ts) + 0.5 * ts * np.sin(ts)
    rel = np.abs(qs - ex).max() / np.abs(ex).max()
    win = 20.0
    centers, env = [], []
    for s0 in np.arange(50.0, T_LONG - win + 1e-9, win):
        m = (ts >= s0) & (ts < s0 + win)
        centers.append(s0 + win / 2); env.append(np.abs(qs[m]).max())
    slope = np.polyfit(np.log(centers), np.log(env), 1)[0]
    return rel, slope, env[0], env[-1], centers[0], centers[-1]


def report_g(ok_sym, S0, P0):
    res, resd, G, t_main, t_half, NM = part_g_numerics(S0, P0)
    o, n = G[("free",)]
    sl = slice(o, o + n)
    Y0f = None
    # free group: recover initial states and final states
    rngf = np.random.default_rng(SEED + 1)
    Df = rngf.standard_normal((4, N_FREE)); Df /= np.sqrt((Df ** 2).sum(0)); wb0 = np.sqrt(W1 * W2)
    Y0f = U_FREE * np.vstack((Df[0], Df[1] * wb0, Df[2] * wb0 ** 2, Df[3] * wb0 ** 3))
    E1a, E2a = modes(Y0f, W1, W2); E1b, E2b = modes(res["Yend"][:, sl], W1, W2)
    Hf = ham(Y0f, 0.0, S0, P0)
    split_err = np.abs(Hf - (E1a - E2a)).max()
    d1 = np.abs(E1b - E1a).max() / np.abs(E1a).max(); d2 = np.abs(E2b - E2a).max() / np.abs(E2a).max()
    bound = (res["Rmax"][sl] / res["R0"][sl]).max()
    ok_free = (d1 < TH_FREE_DRIFT) and (d2 < TH_FREE_DRIFT) and (bound < TH_FREE_BOUND) and split_err < 1e-12
    out(f"Numerical free check ({N_FREE} random starts, |u| = {U_FREE:g}, RK4 dt = {DT}, t ≤ {T_LONG:g}) [computed]:")
    out(f"  max |H − (E₁ − E₂)| at t = 0: {split_err:.1e};  max rel. drift E₁: {d1:.1e}, E₂: {d2:.1e};"
        f"  max R(t)/R(0) = {bound:.3f} (bounded).")
    out(f"G1 {'PASS' if (ok_sym and ok_free) else 'FAIL'} (thresholds: drift < {TH_FREE_DRIFT:g}, R/R0 < {TH_FREE_BOUND:g}).")
    out("")
    # ---------------- G2 equal frequencies ----------------
    rel, slope, e0, e1, c0, c1 = eq_free_check()
    ok_eq = rel < TH_EQ_REL and TH_EQ_SLOPE[0] <= slope <= TH_EQ_SLOPE[1]
    out("## G2: equal frequencies ω₁ = ω₂ = 1, EXCLUDED from the split (flagged) [identity]")
    out("")
    out("The characteristic roots are a double pair ±i; the free solution with q(0)=1 is q = cos t + (t/2) sin t (secular).")
    out(f"RK4 vs exact, t ≤ {T_LONG:g}: max |error| / max |q| = {rel:.1e}. Envelope max|q| grows from {e0:.2f} (t≈{c0:g}) "
        f"to {e1:.2f} (t≈{c1:g}); log-log slope = {slope:.3f} (linear growth).")
    out(f"G2 {'PASS' if ok_eq else 'FAIL'} (thresholds: rel. error < {TH_EQ_REL:g}, slope in {TH_EQ_SLOPE}).")
    out("")
    # ---------------- G3 interacting ----------------
    out("## G3: interacting PU, L → L − (λ/4)q⁴ (Smilga's quartic) [computed]")
    out("")
    out("Sampling and threshold [assumed input]:")
    out(f"- q_* = ω₁ω₂/√|λ| (the only nonlinear scale). Normalised state u = (q, q̇/ω̄, q̈/ω̄², q⃛/ω̄³), ω̄ = √(ω₁ω₂).")
    out(f"- {N_SAMPLE} starts per amplitude, directions uniform on the 3-sphere (seed {SEED}), |u| = A·q_*;"
        f" A ∈ {A_GRID}. The same directions are reused for every group.")
    out(f"- Runaway: R(t) = |u(t)| ≥ {R_RUN[0]:g} q_* before t_max = {T_MAIN:g} (also reported at {T_LONG:g}; "
        f"R ≥ {R_RUN[1]:g} q_* recorded as a threshold check). RK4, dt = {DT}.")
    out(f"- Integration cost: main batch {t_main:.0f} s, dt/2 batch {t_half:.0f} s [computed].")
    out("")
    out(f"| A = |u|/q_* | runaway fraction t ≤ {T_MAIN:g} | t ≤ {T_LONG:g} | R ≥ {R_RUN[1]:g} q_* by t ≤ {T_LONG:g} |")
    out("|---|---|---|---|")
    fr300, fr600 = [], []
    for A in A_GRID:
        f3, c3, nn = frac(res, G[("main", A)], T_MAIN); f6, c6, _ = frac(res, G[("main", A)], T_LONG)
        f6b, _, _ = frac(res, G[("main", A)], T_LONG, 1)
        fr300.append(f3); fr600.append(f6)
        out(f"| {A:g} | {f3:.3f} ({c3}/{nn}) | {f6:.3f} | {f6b:.3f} |")
    out("")
    fr300 = np.array(fr300); fr600 = np.array(fr600)
    onset = next((A for A, f in zip(A_GRID, fr300) if f > 0), None)
    def a50(fr):
        for i in range(1, len(A_GRID)):
            if fr[i - 1] < 0.5 <= fr[i]:
                return A_GRID[i - 1] + (0.5 - fr[i - 1]) * (A_GRID[i] - A_GRID[i - 1]) / (fr[i] - fr[i - 1])
        return None
    A50_3, A50_6 = a50(fr300), a50(fr600)
    fmt = lambda v: "none in range" if v is None else f"{v:.3g}"
    isl = 0.0
    for A, f in zip(A_GRID, fr300):
        if f > 0:
            break
        isl = A
    out(f"Stable island: no runaway for any A ≤ {isl:g} (t ≤ {T_MAIN:g}). "
        f"Runaway first appears at A = {fmt(onset)}; 50 % at A ≈ {fmt(A50_3)} (t ≤ {T_MAIN:g}), {fmt(A50_6)} (t ≤ {T_LONG:g}) [computed].")
    out("")
    # λ table
    out(f"Runaway fraction (t ≤ {T_MAIN:g}) against λ and physical amplitude |u| = a. The λ-collapse is an [identity]: with q = Q/√λ every term of L")
    out("scales by 1/λ, so the motion depends only on a√λ, i.e. on the column A = a√λ/(ω₁ω₂) = a/q_*(λ) (threshold check in G5a):")
    out("")
    out("| a | " + " | ".join(f"λ = {lam:g} (A)" for lam in LAM_TABLE) + " |")
    out("|---|" + "---|" * len(LAM_TABLE))
    for a in AMP_PHYS:
        cells = []
        for lam in LAM_TABLE:
            f3, _, _ = frac(res, G[("lam", lam, a)], T_MAIN)
            cells.append(f"{f3:.3f} ({a * np.sqrt(lam) / (W1 * W2):.3g})")
        out(f"| {a:g} | " + " | ".join(cells) + " |")
    out("")
    # scaling identity
    sc_ok = True
    lines = []
    for A in A_SCALE:
        _, cref, _ = frac(res, G[("main", A)], T_MAIN)
        for lam in LAM_SCALE:
            _, cc, _ = frac(res, G[("scale", lam, A)], T_MAIN)
            sc_ok &= abs(cc - cref) <= TH_SCALE
            lines.append(f"A={A:g}: λ=1 → {cref}, λ={lam:g} → {cc}")
    out("Scaling identity q → q_*·Q removes λ [identity]; runaway counts at equal A: " + "; ".join(lines) + ".")
    # drift
    o, n = G[("main", A_GRID[0])]
    idx = np.concatenate([np.arange(*(lambda s: (s[0], s[0] + s[1]))(G[("main", A)])) for A in A_GRID])
    surv = idx[np.isfinite(res["Yend"][0, idx]) & (res["Rmax"][idx] <= DRIFT_RMAX)]
    Lv = np.ones(surv.size)
    drift = np.abs(ham(res["Yend"][:, surv], Lv, S0, P0) - res["H0"][surv]) / res["E0"][surv]
    surv_all = idx[np.isfinite(res["Yend"][0, idx])]
    drift_all = np.abs(ham(res["Yend"][:, surv_all], np.ones(surv_all.size), S0, P0) - res["H0"][surv_all]) / res["E0"][surv_all]
    out(f"Energy drift |ΔH|/E_abs at t = {T_LONG:g} [computed]: survivors with max R ≤ {DRIFT_RMAX:g} q_*: "
        f"max {drift.max():.1e} ({surv.size} trajectories); all survivors: max {drift_all.max():.1e} ({surv_all.size}).")
    # dt/2
    dlines, dt_ok = [], True
    for i, A in enumerate(A_DTCHECK):
        fh = float(np.mean(resd["tc"][0, i * N_SAMPLE:(i + 1) * N_SAMPLE] <= T_MAIN))
        f1, _, _ = frac(res, G[("main", A)], T_MAIN)
        dt_ok &= abs(fh - f1) <= TH_DT
        dlines.append(f"A={A:g}: {f1:.3f} vs {fh:.3f}")
    out(f"Step halving (dt vs dt/2, t ≤ {T_MAIN:g}) [computed]: " + "; ".join(dlines) + ".")
    island_ok = all(f == 0 for A, f in zip(A_GRID, fr300) if A <= ISLAND_A)
    top_ok = fr300[-1] >= TOP_FRAC
    drift_ok = drift.max() < TH_DRIFT
    g3 = island_ok and top_ok and drift_ok and dt_ok and sc_ok
    out(f"G3 {'PASS' if g3 else 'FAIL'}: island (f = 0 for A ≤ {ISLAND_A:g}): {island_ok}; f ≥ {TOP_FRAC:g} at A = {A_GRID[-1]:g}: "
        f"{top_ok} (f = {fr300[-1]:.3f}); drift < {TH_DRIFT:g}: {drift_ok}; dt/2 within {TH_DT:g}: {dt_ok}; scaling ±{TH_SCALE}: {sc_ok}.")
    out("")
    # λ < 0 report
    out("λ = −1 (report only; Smilga: the wrong sign is malicious; extended with a no-ghost control in G5b) [computed]:")
    neg = []
    for A in A_NEG:
        f3, _, _ = frac(res, G[("neg", A)], T_MAIN); f6, _, _ = frac(res, G[("neg", A)], T_LONG)
        neg.append(f"A={A:g}: {f3:.3f} (t≤{T_MAIN:g}), {f6:.3f} (t≤{T_LONG:g})")
    out("  unequal frequencies, sphere starts: " + "; ".join(neg) + ".")
    o, n = G[("negeq",)]
    tneg = res["tc"][0, o:o + n]
    out("  equal frequencies, q(0) = c: " + "; ".join(f"c={c:g}: runaway at t = {('%.1f' % t) if np.isfinite(t) else f'none ≤ {T_LONG:g}'}"
                                                    for c, t in zip(C_NEG_EQ, tneg)) + ".")
    out("")
    # ---------------- G4 Smilga comparison ----------------
    out("## G4: comparison with Smilga, NPB 706 (2005) 598, eqs. (6)–(7) (equal frequencies, flagged) [computed]")
    out("")
    o, n = G[("smilga",)]
    tsm = res["tc"][0, o:o + n]
    def ccrit(T):
        run = tsm <= T
        if not run.any():
            return None, 0
        i0 = int(np.argmax(run))
        nonmono = int(np.sum(~run[i0:]))
        return float(C_SMILGA[i0]), nonmono
    c3, nm3 = ccrit(T_MAIN); c6, nm6 = ccrit(T_LONG)
    out("Model: L = ½(q̈ + Ω²q)² − (α/4)q⁴, Ω = α = 1, q(0) = c, q̇ = q̈ = q⃛ = 0; c grid "
        f"{C_SMILGA[0]:g}…{C_SMILGA[-1]:g} step {C_SMILGA[1] - C_SMILGA[0]:g}.")
    out(f"Smallest runaway c: {fmt(c3)} (t ≤ {T_MAIN:g}; {nm3} larger c survive), {fmt(c6)} (t ≤ {T_LONG:g}; {nm6} larger c survive). "
        f"Smilga: c_crit ≈ 0.3 Ω²/√α.")
    g4 = c6 is not None and SMILGA_WINDOW[0] <= c6 <= SMILGA_WINDOW[1]
    out(f"G4 {'PASS' if g4 else 'FAIL'} (window {SMILGA_WINDOW} on the t ≤ {T_LONG:g} value).")
    o, n = G[("line",)]
    tl = res["tc"][0, o:o + n]
    run = tl <= T_MAIN
    cl = float(C_LINE[int(np.argmax(run))]) if run.any() else None
    out(f"Same one-parameter start q(0) = c q_* at the main (unequal) frequencies: smallest runaway c = {fmt(cl)} "
        f"(t ≤ {T_MAIN:g}; c up to {C_LINE[-1]:g}) [computed, report only].")
    out("")
    # ---------------- G5 review fold-ins ----------------
    fmt4 = lambda v: "none" if v is None else f"{v:.4f}"
    out("## G5: review fold-ins (Venus maths, Helios physics); thresholds fixed in run.py before the fold-in run [computed]")
    out("")
    out("### G5a: the runaway threshold scales like q_* = ω₁ω₂/√|λ|")
    out("")
    out("With q = Q/√λ every term of L = ½[q̈² − (ω₁²+ω₂²)q̇² + ω₁²ω₂²q²] − (λ/4)q⁴ scales by 1/λ, so the motion depends only on a√λ")
    out("(a = |u|) [identity]. Numerical check at the λ values already scanned: same start directions, physical amplitudes")
    out(f"a = A·ω₁ω₂/√λ for A ∈ {A_TR}, runaway by t ≤ {T_MAIN:g}; A₅₀ by linear interpolation of the fraction:")
    out("")
    out("| λ | " + " | ".join(f"A={A:g}" for A in A_TR) + " | A₅₀ | a₅₀ (physical) | a₅₀·√λ |")
    out("|---|" + "---|" * (len(A_TR) + 3))
    A50s, a50s = [], []
    for lam in LAM_TR:
        fl = [frac(res, G[("tr", lam, A)], T_MAIN)[0] for A in A_TR]
        A50 = a50g(A_TR, fl)
        a50 = None if A50 is None else A50 * W1 * W2 / np.sqrt(lam)
        A50s.append(A50); a50s.append(a50)
        out(f"| {lam:g} | " + " | ".join(f"{f:.3f}" for f in fl) + f" | {fmt4(A50)} | {fmt4(a50)} | "
            + fmt4(None if a50 is None else a50 * np.sqrt(lam)) + " |")
    out("")
    if all(v is not None for v in A50s):
        ref = A50s[LAM_TR.index(1.0)]
        devA = max(abs(v - ref) for v in A50s)
        sl50 = float(np.polyfit(np.log(LAM_TR), np.log(a50s), 1)[0])
        prod = [v * np.sqrt(l) for v, l in zip(a50s, LAM_TR)]
        g5a = devA <= TH_A50 and abs(sl50 + 0.5) <= TH_A50_SLOPE
        out(f"a₅₀·√λ spans [{min(prod):.6f}, {max(prod):.6f}]; max |A₅₀(λ) − A₅₀(1)| = {devA:.1e}; "
            f"fitted d ln a₅₀ / d ln λ = {sl50:.6f} (a 1/√λ threshold gives −1/2).")
    else:
        g5a = False
        out("A₅₀ not bracketed for some λ.")
    out(f"G5a {'PASS' if g5a else 'FAIL'} (thresholds: max |A₅₀(λ) − A₅₀(1)| ≤ {TH_A50:g}, |slope + 1/2| ≤ {TH_A50_SLOPE:g}).")
    out("")
    resn, gz = NM["res"], NM["groups"]
    out("### G5b: the sign of λ against a no-ghost control at the same scaled amplitudes")
    out("")
    out("Ghost: H = ½(P₁²+ω₁²X₁²) − ½(P₂²+ω₂²X₂²) + λq⁴/4 in Smilga's normal-mode variables (the G1 map), q = (ω₁X₂ − P₁)/(ω₁√(ω₁²−ω₂²)).")
    out("No-ghost control [assumed]: the same H with +½(P₂²+ω₂²X₂²) (both modes positive energy), the same quartic λq⁴/4 in the same q,")
    out(f"the same starts (G3 sphere directions, seed {SEED}, {N_SAMPLE} per amplitude, mapped by the same map) and both signs of λ, |λ| = 1.")
    out(f"Runaway criterion (fixed before the run, as in G3): |u| ≥ {R_RUN[0]:g} q_* by t ≤ {T_MAIN:g} (t ≤ {T_LONG:g} shown as a check), "
        f"u recovered by the inverse map; RK4, dt = {DT}.")
    out("For λ > 0 the control H is bounded below, so it cannot run away [identity]. For λ < 0 the quartic is unbounded below even")
    out("without a ghost, so only runaway beyond the matching control, Δ = f_ghost − f_control, counts as ghost runaway.")
    out(f"Sign rule (fixed before the run): the sign of λ matters if max over A ≤ {A_SIGN[-1]:g} of |Δ(λ>0) − Δ(λ<0)| ≥ {SIGN_DIFF:g} at t ≤ {T_MAIN:g}.")
    out(f"Map checks at t = 0 [identity]: round trip u → (X, P) → u, max rel. error {NM['rt']:.1e}; "
        f"|H_normal-mode − H_Ostrogradsky| / max E_abs = {NM['herr']:.1e}. Batch: {NM['n']} trajectories to t = {T_LONG:g} in {NM['t']:.0f} s.")
    out("")

    def fz(s_, lam, A, T):
        o_, n_ = gz[(s_, lam, A)]
        return float(np.mean(resn["tc"][o_:o_ + n_] <= T))

    def table(T):
        out(f"Runaway fraction by t ≤ {T:g} against the scaled amplitude A = |u|√|λ|/(ω₁ω₂):")
        out("")
        out("| system | " + " | ".join(f"A={A:g}" for A in A_SIGN) + " |")
        out("|---|" + "---|" * len(A_SIGN))
        rows = {}
        for name, s_, lam in (("ghost, λ > 0", -1.0, 1.0), ("ghost, λ < 0", -1.0, -1.0),
                              ("no-ghost control, λ > 0", 1.0, 1.0), ("no-ghost control, λ < 0", 1.0, -1.0)):
            rows[(s_, lam)] = np.array([fz(s_, lam, A, T) for A in A_SIGN])
            out(f"| {name} | " + " | ".join(f"{v:.3f}" for v in rows[(s_, lam)]) + " |")
        dp = rows[(-1.0, 1.0)] - rows[(1.0, 1.0)]; dm = rows[(-1.0, -1.0)] - rows[(1.0, -1.0)]
        out("| Δ(λ>0) = ghost − control | " + " | ".join(f"{v:+.3f}" for v in dp) + " |")
        out("| Δ(λ<0) = ghost − control | " + " | ".join(f"{v:+.3f}" for v in dm) + " |")
        out("| abs(Δ(λ>0) − Δ(λ<0)) | " + " | ".join(f"{abs(v):.3f}" for v in dp - dm) + " |")
        # Venus review request [post-hoc]: conditional ghost share S = (f_ghost − f_ctrl)/(1 − f_ctrl); n/a if f_ctrl = 1
        sp_ = [None if fc >= 1.0 else d / (1.0 - fc) for d, fc in zip(dp, rows[(1.0, 1.0)])]
        sm_ = [None if fc >= 1.0 else d / (1.0 - fc) for d, fc in zip(dm, rows[(1.0, -1.0)])]
        f3n = lambda v: "n/a" if v is None else f"{v:.3f}"
        out("| S(λ>0) = Δ/(1 − f_control) [post-hoc] | " + " | ".join(f3n(v) for v in sp_) + " |")
        out("| S(λ<0) = Δ/(1 − f_control) [post-hoc] | " + " | ".join(f3n(v) for v in sm_) + " |")
        out("| S(λ>0) − S(λ<0) [post-hoc] | " + " | ".join("n/a" if (a_ is None or b_ is None) else f"{a_ - b_:+.3f}" for a_, b_ in zip(sp_, sm_)) + " |")
        out("| control survivors, λ < 0 (S denominator, of " + f"{N_SAMPLE}) | " + " | ".join(f"{int(round((1.0 - fc) * N_SAMPLE))}" for fc in rows[(1.0, -1.0)]) + " |")
        out("")
        return rows, dp, dm, sp_, sm_
    out(f"S [post-hoc; Venus review request, not a grade]: the share of the control's survivors that the ghost adds to the runaway, "
        f"S = (f_ghost − f_control)/(1 − f_control), printed as n/a where f_control = 1. For λ > 0 the control never runs away, so S(λ>0) = Δ(λ>0).")
    out("")
    rows3, dp3, dm3, sp3, sm3 = table(T_MAIN)
    rows6, dp6, dm6, sp6, sm6 = table(T_LONG)

    def side_runs(vp, vm, tol=1e-12):
        lab = []
        for a_, b_ in zip(vp, vm):
            if a_ is None or b_ is None:
                lab.append("n/a")
            elif a_ - b_ > tol:
                lab.append("λ>0")
            elif b_ - a_ > tol:
                lab.append("λ<0")
            else:
                lab.append("equal")
        runs = []
        for A, l_ in zip(A_SIGN, lab):
            if runs and runs[-1][0] == l_:
                runs[-1][2] = A
            else:
                runs.append([l_, A, A])
        return runs

    def run_txt(runs):
        parts = []
        for l_, lo, hi in runs:
            if l_ in ("λ>0", "λ<0"):
                where = (f"A ≥ {lo:g} (to the grid maximum A = {A_SIGN[-1]:g})" if hi == A_SIGN[-1] and lo != A_SIGN[0]
                         else (f"A = {lo:g}" if lo == hi else f"A in [{lo:g}, {hi:g}]"))
                parts.append(f"larger for {l_} at {where}")
            elif l_ == "equal":
                parts.append(f"equal at A in [{lo:g}, {hi:g}]" if lo != hi else f"equal at A = {lo:g}")
            else:
                parts.append(f"n/a at A in [{lo:g}, {hi:g}]")
        return "; ".join(parts)

    out(f"Which sign has the larger ghost excess, at the sampled A only [post-hoc; computed from the tables above]:")
    sr = {}
    for T, dp_, dm_, sp_, sm_ in ((T_MAIN, dp3, dm3, sp3, sm3), (T_LONG, dp6, dm6, sp6, sm6)):
        sr[("Δ", T)] = side_runs(list(dp_), list(dm_))
        sr[("S", T)] = side_runs(sp_, sm_)
        out(f"- t ≤ {T:g}, raw Δ: {run_txt(sr[('Δ', T)])}.")
        out(f"- t ≤ {T:g}, share S: {run_txt(sr[('S', T)])}.")
    out(f"Same ranges at t ≤ {T_MAIN:g} and t ≤ {T_LONG:g}: raw Δ {sr[('Δ', T_MAIN)] == sr[('Δ', T_LONG)]}; S {sr[('S', T_MAIN)] == sr[('S', T_LONG)]}. "
        f"Both statements are limited to the sampled grid {A_SIGN}: a crossover lies between neighbouring grid points [finite-size].")
    out("")
    dd = np.abs(dp3 - dm3); im = int(np.argmax(dd))
    sign_matters = bool(dd[im] >= SIGN_DIFF)
    dd6 = np.abs(dp6 - dm6)
    raw = np.abs(rows3[(-1.0, 1.0)] - rows3[(-1.0, -1.0)])
    ctrl_ok = bool(np.all(rows6[(1.0, 1.0)] == 0))
    xc = []
    for A in A_SIGN:
        if ("main", A) in G:
            xc.append(abs(frac(res, G[("main", A)], T_MAIN)[0] - fz(-1.0, 1.0, A, T_MAIN)))
        if ("neg", A) in G:
            xc.append(abs(frac(res, G[("neg", A)], T_MAIN)[0] - fz(-1.0, -1.0, A, T_MAIN)))
    xmax = max(xc)
    fin = np.isfinite(resn["Zend"][0])
    drn = np.abs(ham_nm(resn["Zend"][:, fin], NM["L"][fin], NM["s"][fin]) - resn["H0"][fin]) / resn["E0"][fin]
    sfin = NM["s"][fin]
    mx = lambda v: f"{v.max():.1e}" if v.size else "n/a"
    out(f"Max |Δ(λ>0) − Δ(λ<0)| at t ≤ {T_MAIN:g}: {dd[im]:.3f} at A = {A_SIGN[im]:g} (Δ(λ>0) = {dp3[im]:+.3f}, Δ(λ<0) = {dm3[im]:+.3f}); "
        f"at t ≤ {T_LONG:g}: {dd6.max():.3f} at A = {A_SIGN[int(np.argmax(dd6))]:g}. Uncorrected max |f_ghost(λ>0) − f_ghost(λ<0)| = "
        f"{raw.max():.3f} at A = {A_SIGN[int(np.argmax(raw))]:g}.")
    out(f"Controls: no-ghost λ > 0 never runs away up to t = {T_LONG:g}: {ctrl_ok}. Ghost in normal-mode vs q variables (same starts, "
        f"overlapping A, t ≤ {T_MAIN:g}): max |Δf| = {xmax:.3f} over {len(xc)} pairs (threshold {TH_XCHECK:g}).")
    out(f"Energy drift |ΔH|/E_abs of survivors at t = {T_LONG:g}: ghost max {mx(drn[sfin < 0])} ({int((sfin < 0).sum())}), "
        f"control max {mx(drn[sfin > 0])} ({int((sfin > 0).sum())}).")
    g5b = ctrl_ok and xmax <= TH_XCHECK
    stext = "PASS (the sign of λ matters beyond the no-ghost control)" if sign_matters else "FAIL (the sign of λ does not matter beyond the no-ghost control)"
    out(f"G5b controls {'PASS' if g5b else 'FAIL'}; sign test {stext}.")
    out("")
    g5 = f"G5a {'PASS' if g5a else 'FAIL'}; G5b controls {'PASS' if g5b else 'FAIL'}; sign test {stext}"
    gG = "PASS" if (ok_sym and ok_free and ok_eq and g3 and g4) else ("PARTIAL" if (ok_sym and ok_free and ok_eq) else "FAIL")
    out(f"**Part G verdict: {gG}** (PASS = G1–G4; PARTIAL = G1, G2 pass but G3 or G4 fails; FAIL = G1 or G2 fails; the G5 fold-ins are reported separately and do not enter it).")
    out("")
    return gG, dict(A=A_GRID, f3=fr300, f6=fr600, res=res, G=G, resd=resd, g5=g5)


# =====================================================================================
# Part L
# =====================================================================================
TS = sp.symbols("t", real=True)
A_S = (1 + 3 * TS ** 2) ** sp.Rational(1, 6)
U_CLOSED = (1 - TS ** 2) * (1 + 3 * TS ** 2) ** sp.Rational(-5, 3)
a_f = sp.lambdify(TS, A_S, "numpy")
U_f = sp.lambdify(TS, U_CLOSED, "numpy")
Ut_f = sp.lambdify(TS, sp.diff(U_CLOSED, TS), "numpy")


def eta_of_t(t):
    return t * hyp2f1(1.0 / 6.0, 0.5, 1.5, -3.0 * t * t)


def t_of_eta(e):
    s = np.sign(e); e = abs(e)
    if e == 0:
        return 0.0
    hi = 2.0 * (e / (1.5 * 3 ** (-1.0 / 6.0))) ** 1.5 + 10.0
    return s * brentq(lambda t: eta_of_t(t) - e, 0.0, hi, xtol=1e-15, rtol=8.9e-16, maxiter=500)


def mode_beta(k, X):
    te = t_of_eta(X / k)
    om = lambda t: np.sqrt(k * k - U_f(t))
    omp = lambda t: a_f(t) * (-Ut_f(t)) / (2.0 * om(t))      # dω/dη
    ti, tf = -te, te
    wi = om(ti); v0 = 1.0 / np.sqrt(2.0 * wi); dv0 = (-1j * wi - omp(ti) / (2.0 * wi)) * v0

    def rhs(t, y):
        a = a_f(t)
        return np.array([y[1] / a, -(k * k - U_f(t)) * y[0] / a])
    sol = solve_ivp(rhs, (ti, tf), np.array([v0 + 0j, dv0]), method="DOP853", rtol=RTOL, atol=ATOL)
    v, w = sol.y[:, -1]
    wf = om(tf); u = 1.0 / np.sqrt(2.0 * wf); du = (-1j * wf - omp(tf) / (2.0 * wf)) * u
    al = -1j * (v * np.conj(du) - w * np.conj(u)); be = 1j * (v * du - w * u)
    return abs(be) ** 2, abs(al) ** 2 - abs(be) ** 2 - 1.0, sol.nfev


def part_l():
    out("# Part L: a tensor mode through the effective LQC bounce")
    out("")
    out(f"Units [assumed input]: 8πG = 1, ρ_c = 1, a_B = 1, so 24πGρ_c = 3·(8πG)ρ_c = {3 * 1.0 * 1.0:g} and k_B = a_B√(8πGρ_c) = {np.sqrt(1.0 * 1.0):g}.")
    out("Background [standard]: a(t) = (1 + 24πGρ_c t²)^{1/6} = (1 + 3t²)^{1/6} (massless scalar, ρ = ρ_c a⁻⁶).")
    out("")
    out("## L1: background and a''/a [identity]")
    out("")
    rho = A_S ** -6
    Hs = sp.diff(A_S, TS) / A_S
    fried = sp.simplify(Hs ** 2 - sp.Rational(1, 3) * rho * (1 - rho))
    Usym = sp.diff(A_S * sp.diff(A_S, TS), TS)            # a''/a = d/dt(a ȧ) with ' = d/dη, dη = dt/a
    resU = sp.simplify(Usym - U_CLOSED)
    out(f"- Effective Friedmann H² − (8πG/3)ρ(1 − ρ/ρ_c) for this a(t): {fried} (sympy).")
    out(f"- a''/a = d(aȧ)/dt = (1 − t²)(1 + 3t²)^(−5/3); sympy residual {resU}. Value at the bounce: {float(U_f(0.0)):g} = k_B².")
    tq = [0.5, 2.0, 10.0, 100.0, 1.0e4]
    deta = max(abs(eta_of_t(t) - quad(lambda s: (1 + 3 * s * s) ** (-1.0 / 6.0), 0, t, limit=400, epsabs=0, epsrel=1e-13)[0]) /
               eta_of_t(t) for t in tq)
    out(f"- η(t) = t·₂F₁(1/6, 1/2; 3/2; −3t²) vs quadrature at t ∈ {tq}: max rel. difference {deta:.1e}.")
    h = 1e-2
    errs = []
    for e0 in ETA_FD:
        av = [a_f(t_of_eta(e0 + j * h)) for j in (-2, -1, 0, 1, 2)]
        app = (-av[0] + 16 * av[1] - 30 * av[2] + 16 * av[3] - av[4]) / (12 * h * h)
        errs.append(abs(app / av[2] - U_f(t_of_eta(e0))))
    fd = max(errs)
    out(f"- Numerical a''/a by 5-point differences in η (h = {h:g}) at η ∈ {ETA_FD}: max |error| {fd:.1e}.")
    ims = 0.5 * Beta(0.5, 5.0 / 6.0) / np.sqrt(3.0)
    out(f"- Late time: a''/a → −1/(4η²) (a ∝ η^(1/2)). Nearest complex singularity: t = ±i/√3, η_s = ±i·{ims:.6f} [computed].")
    ims_cf = (1.0 / math.sqrt(3.0)) * (math.sqrt(math.pi) / 2.0) * math.gamma(5.0 / 6.0) / math.gamma(4.0 / 3.0)
    out(f"- Venus's closed form Im η_s = (1/√3)(√π/2)Γ(5/6)/Γ(4/3) = {ims_cf:.12f} (math.gamma); Beta-function value {ims:.12f}; "
        f"difference {abs(ims_cf - ims):.1e} [identity].")
    ok_l1 = fried == 0 and resU == 0 and deta < TH_ETA and fd < TH_FD
    out(f"L1 {'PASS' if ok_l1 else 'FAIL'} (thresholds: η rel. diff < {TH_ETA:g}, FD error < {TH_FD:g}).")
    out("")
    out("## L2–L3: Bogoliubov coefficients, Wronskian and start/end convergence [computed]")
    out("")
    out(f"v'' + (k² − a''/a)v = 0 integrated in t (dv/dt = v'/a, dv'/dt = −(k² − a''/a)v/a), DOP853, rtol = {RTOL:g}.")
    out(f"Start at η_i = −X/k in the first-order adiabatic vacuum v = e^(−i∫ω)/√(2ω), v' = (−iω − ω'/2ω)v, ω² = k² − a''/a;")
    out(f"end at η_f = +X/k and project on the same late-time adiabatic modes. X = {X_MAIN:g}; convergence column X = {X_CONV:g}.")
    out("")
    out(f"| k/k_B | |β|² (X={X_MAIN:g}) | |β|² (X={X_CONV:g}) | rel. change | |α|²−|β|²−1 (X={X_MAIN:g}) | (X={X_CONV:g}) |")
    out("|---|---|---|---|---|---|")
    B2, B4, W2s, W4s = [], [], [], []
    t0 = time.time()
    for k in K_GRID:
        b2, w2r, _ = mode_beta(k, X_MAIN)
        b4, w4r, _ = mode_beta(k, X_CONV)
        B2.append(b2); B4.append(b4); W2s.append(w2r); W4s.append(w4r)
        out(f"| {k:.4g} | {b2:.6e} | {b4:.6e} | {abs(b2 - b4) / b4:.1e} | {w2r:+.1e} | {w4r:+.1e} |")
    tl = time.time() - t0
    B2, B4 = np.array(B2), np.array(B4)
    out("")
    wr = max(np.abs(W2s).max(), np.abs(W4s).max())
    above = B4 > CONV_FLOOR
    conv = (np.abs(B2 - B4) / B4)[above].max()
    out(f"Mode integrations: {2 * K_GRID.size} in {tl:.0f} s [computed].")
    ok_l2 = wr < TH_WRONSK
    ok_l3 = conv < TH_CONV
    out(f"L2 {'PASS' if ok_l2 else 'FAIL'}: max ||α|²−|β|²−1| = {wr:.1e} (threshold {TH_WRONSK:g}).")
    out(f"L3 {'PASS' if ok_l3 else 'FAIL'}: max rel. change X = {X_MAIN:g} → {X_CONV:g} over the {int(above.sum())} k with |β|² > {CONV_FLOOR:g}: "
        f"{conv:.1e} (threshold {TH_CONV:g}); otherwise [finite-size].")
    out("")
    out("## L4: spectrum shape against the prediction [computed]")
    out("")
    sm = K_GRID <= SMALL_K + 1e-12
    lg = K_GRID >= LARGE_K - 1e-12
    dec = np.all(np.diff(B4[K_GRID >= 1.0 - 1e-12]) < 0)
    ok_a = np.all(B4[sm] >= TH_SMALLK)
    ok_b = np.all(B4[lg] < TH_LARGEK) and dec
    out(f"- k ≤ {SMALL_K:g} k_B: min |β|² = {B4[sm].min():.3g} (need ≥ {TH_SMALLK:g}): {ok_a}.")
    out(f"- k ≥ {LARGE_K:g} k_B: max |β|² = {B4[lg].max():.3g} (need < {TH_LARGEK:g}); decreasing for k ≥ k_B: {dec}.")
    ps = np.polyfit(np.log(K_GRID[sm]), np.log(B4[sm]), 1)[0]
    out(f"- Small-k power law: d ln|β|²/d ln k over k ≤ {SMALL_K:g} = {ps:.3f}.")
    loc = np.diff(np.log(B4)) / np.diff(np.log(K_GRID))
    out("- Local log-log slopes d ln|β|²/d ln k between neighbouring k: " + ", ".join(f"{v:.2f}" for v in loc) + ".")
    kk, yy = K_GRID[lg], np.log(B4[lg])
    Mexp = np.vstack((np.ones_like(kk), kk)).T
    cexp, rexp = np.linalg.lstsq(Mexp, yy, rcond=None)[:2]
    Mmix = np.vstack((np.ones_like(kk), kk, np.log(kk))).T
    cmix, rmix = np.linalg.lstsq(Mmix, yy, rcond=None)[:2]
    Mpow = np.vstack((np.ones_like(kk), np.log(kk))).T
    cpow, rpow = np.linalg.lstsq(Mpow, yy, rcond=None)[:2]
    rms = lambda r: float(np.sqrt(r[0] / kk.size)) if len(r) else float("nan")
    out(f"- Large-k fits over k ≥ {LARGE_K:g} k_B (ln|β|²): exponential b − c·k: c = {-cexp[1]:.4f}, rms {rms(rexp):.2e}; "
        f"b − c·k + p ln k: c = {-cmix[1]:.4f}, p = {cmix[2]:.3f}, rms {rms(rmix):.2e}; pure power law: slope {cpow[1]:.2f}, rms {rms(rpow):.2e}.")
    c_e, c_m, s4 = -cexp[1], -cmix[1], 4.0 * ims_cf
    out("- Large-k fall-off [standard] (Dykhne, Sov. Phys. JETP 14 (1962) 941; Davis & Pechukas, J. Chem. Phys. 64 (1976) 3129, "
        "doi 10.1063/1.432648): |β|² ~ exp(−4k·Im η_s), η_s the nearest complex singularity of a''/a.")
    out(f"  Im η_s = {ims_cf:.6f}, 4·Im η_s = {s4:.4f}; fitted c = {c_e:.4f} (exponential; rel. diff {abs(c_e - s4) / s4:.1e}), "
        f"{c_m:.4f} (with ln k term; rel. diff {abs(c_m - s4) / s4:.1e})." )
    ok_l4 = ok_a and ok_b
    gL = "PASS" if (ok_l1 and ok_l2 and ok_l3 and ok_l4) else ("PARTIAL" if (ok_l1 and ok_l2) else "FAIL")
    out("")
    out(f"**Part L verdict: {gL}** (PASS = L1–L4; PARTIAL = L1, L2 pass but L3 or L4 fails; FAIL = L1 or L2 fails).")
    out("")
    return gL, dict(k=K_GRID, B2=B2, B4=B4, cexp=cexp, ims=ims)


def plots(dg, dl):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        out(f"(plots skipped: {e})")
        return
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogx(dg["A"], dg["f3"], "o-", label=f"t ≤ {T_MAIN:g}")
    ax.semilogx(dg["A"], dg["f6"], "s--", label=f"t ≤ {T_LONG:g}")
    res, G = dg["res"], dg["G"]
    for lam, mk in zip(LAM_TABLE, ("^", "v", "D")):
        As = [a * np.sqrt(lam) / (W1 * W2) for a in AMP_PHYS]
        fs = [frac(res, G[("lam", lam, a)], T_MAIN)[0] for a in AMP_PHYS]
        ax.semilogx(As, fs, mk, mfc="none", label=f"λ = {lam:g} (physical a, rescaled)")
    ax.set_xlabel("A = |u| / q_*"); ax.set_ylabel("runaway fraction"); ax.set_title("PU + λq⁴, ω₂/ω₁ = golden ratio")
    ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(os.path.join(HERE, "pu_runaway.png"), dpi=110); plt.close(fig)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(dl["k"], dl["B2"], "o", label=f"X = {X_MAIN:g}")
    ax.loglog(dl["k"], dl["B4"], "x", label=f"X = {X_CONV:g}")
    kk = dl["k"][dl["k"] >= LARGE_K - 1e-12]
    ax.loglog(kk, np.exp(dl["cexp"][0] + dl["cexp"][1] * kk), "k:", label=f"exp fit, k ≥ {LARGE_K:g}")
    ax.set_xlabel("k / k_B"); ax.set_ylabel("|β_k|²"); ax.set_title("Tensor mode through the LQC bounce")
    ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(os.path.join(HERE, "lqc_beta.png"), dpi=110); plt.close(fig)
    out("Plots: pu_runaway.png (runaway fraction vs A, with the λ-table rescaled onto it), lqc_beta.png (|β_k|² vs k/k_B).")
    out("")


def main():
    out("# Job Seven: Pais–Uhlenbeck ghost and a GW mode through the LQC bounce — RESULTS")
    out("")
    out("Written only by run.py; every number below is printed from a variable. Tags: [computed] [identity] [assumed]")
    out("[assumed input] [standard] [post-hoc] [finite-size] [grid-step] [prediction] [hive-interpretation].")
    out(f"Python {platform.python_version()}, numpy {np.__version__}, scipy {scipy.__version__}, sympy {sp.__version__}.")
    out("PASS thresholds are fixed in the parameter block of run.py before the first run. The G5 fold-in thresholds and the")
    out("G5b sign rule were added after the Venus/Helios review and fixed before the fold-in run; G1–G4 and L1–L4 are unchanged.")
    out("")
    ok_sym, S0, P0 = part_g()
    gG, dg = report_g(ok_sym, S0, P0)
    gL, dl = part_l()
    plots(dg, dl)
    out("## Summary")
    out("")
    out(f"- Part G (PU ghost): {gG}")
    out(f"- Part L (LQC tensor mode): {gL}")
    out(f"- Review fold-ins (G5, reported separately): {dg['g5']}")
    out("")
    out(f"Runtime: {time.time() - T_START:.0f} s [computed].")
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
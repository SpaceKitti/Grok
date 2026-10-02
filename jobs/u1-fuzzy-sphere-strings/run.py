#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job U1 (u1-fuzzy-sphere-strings): zero modes and level drift of the Ginsparg-Wilson Dirac operator
in the charge-n monopole sector of the fuzzy sphere (Aoki-Iso-Nagao hep-th/0312199; Grosse-Klimcik-Presnajder
hep-th/9510083). Spec: Helios. Writes RESULTS.md (ONLY ever written by this script) next to itself.
Run:  $env:PYTHONIOENCODING='utf-8'; python -B run.py
Every number in RESULTS.md is printed from a variable. Thresholds are fixed in the parameter block below
before the first run.
"""
import os, sys, time, platform, hashlib
import numpy as np
import scipy, scipy.linalg
import sympy as sp
from sympy.physics.quantum.spin import Rotation

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = time.time()
OUT = []


def out(s=""):
    print(s, flush=True)
    OUT.append(s)


# ---------------- parameters and thresholds (fixed before the first run) ----------------
N_A = list(range(4, 21))          # Stage A: resolution N = 2L+1 (matrix size of the base fuzzy sphere) [assumed input]
N_CHARGE_A = list(range(0, 7))    # Stage A: n = 0..6, only n < N is run [spec]
N_B = [8, 12, 16, 20]             # Stage B: N values for the collapse test [spec]
DELTA_STAR = 0.1                  # Stage B: x* is where delta_1 reaches 0.1 [spec]
TH_SPREAD = 0.20                  # Stage B PASS: max(x*)/min(x*) - 1 <= 0.20 over the four N [spec: 'within 20%']
K_LEVELS = 3                      # Stage B: lowest three nonzero levels [spec]
ZERO_TOL = 1e-8                   # |eigenvalue| < ZERO_TOL counts as a zero mode [assumed input]
LEVEL_TOL = 1e-7                  # eigenvalues within LEVEL_TOL are one degenerate level [assumed input]
N_NEG = [4, 8, 12, 16]            # reported only: opposite orientation (charge -n), dims <= ~1000
LIT_MAXDIM = 1000                 # literal AIN isospin-T construction only where its full dim <= 1000
N_LIT = [4, 5, 6, 7, 8]           # literal cross-check N values
N_C = [4, 8, 12]                  # Stage C reduced-module N values
N_C_LIT = [4, 6]                  # Stage C literal-construction N values
BETA_D1 = 0.7                     # Venus's d^1(beta) check angle [assumed input]
N_D1 = 8                          # Venus's d^1(beta) check: N for the n = 3 zero modes


# ---------------- building blocks ----------------
def spin(s):
    d = int(round(2 * s + 1))
    m = s - np.arange(d)
    Jp = np.zeros((d, d), complex)
    for i in range(1, d):
        Jp[i - 1, i] = np.sqrt(s * (s + 1) - m[i] * (m[i] + 1))
    return [(Jp + Jp.conj().T) / 2, (Jp - Jp.conj().T) / 2j, np.diag(m).astype(complex)]


SIG = [2 * x for x in spin(0.5)]
I2 = np.eye(2)


def kron3(A, B, C):
    return np.kron(np.kron(A, B), C)


def module_ops(L, Lp):
    """Reduced projective module: psi = 2-spinor x (2L'+1)x(2L+1) matrix; left action spin L' (the AIN block
    L^(a) of A_i), right action spin L (base fuzzy sphere). Order of factors: spinor, row (L'), column (L)."""
    dl, dp = int(round(2 * L + 1)), int(round(2 * Lp + 1))
    Ls, Lps = spin(L), spin(Lp)
    Il, Ip = np.eye(dl), np.eye(dp)
    a = 1.0 / (L + 0.5)                                       # AIN (2.18)
    LR = [kron3(I2, Ip, X.T) for X in Ls]                      # right action psi -> psi L_i
    AL = [kron3(I2, X, Il) for X in Lps]                       # left action of A_i restricted to the block
    S = [kron3(s, Ip, Il) for s in SIG]
    one = np.eye(2 * dl * dp)
    sLR = sum(S[i] @ LR[i] for i in range(3))
    sAL = sum(S[i] @ AL[i] for i in range(3))
    GR = a * (sLR - 0.5 * one)                                 # AIN (2.16)
    H = a * (sAL + 0.5 * one)                                  # AIN (2.19) on the block
    Gh = H / (a * (Lp + 0.5))                                  # AIN (2.17)/(3.30): sqrt(H^2) = a(L'+1/2) on the block
    D = -(1.0 / a) * GR @ (one - GR @ Gh)                      # AIN (2.23)
    DGKP = sum(S[i] @ (AL[i] - LR[i]) for i in range(3)) + one  # AIN (2.8) with A_i on the block
    J = [AL[i] - LR[i] + S[i] / 2 for i in range(3)]           # total angular momentum
    return dict(a=a, GR=GR, Gh=Gh, H=H, D=D, DGKP=DGKP, J=J, J2=sum(x @ x for x in J), dim=2 * dl * dp)


def levels(w):
    pos = np.sort(w[w > ZERO_TOL])
    lv = []
    for x in pos:
        if lv and abs(x - lv[-1][0]) < LEVEL_TOL:
            lv[-1][1] += 1
        else:
            lv.append([x, 1])
    return lv


def analyse(o, want_vecs=False):
    D = o["D"]
    w, v = np.linalg.eigh(D)
    z = np.abs(w) < ZERO_TOL
    V = v[:, z]
    chi = np.linalg.eigvalsh(V.conj().T @ o["GR"] @ V) if V.shape[1] else np.array([])
    jj = np.linalg.eigvalsh(V.conj().T @ o["J2"] @ V) if V.shape[1] else np.array([])
    idx = 0.5 * float(np.trace(o["GR"] + o["Gh"]).real)
    res = dict(w=w, nz=int(z.sum()), npos=int((chi > 0).sum()), nneg=int((chi < 0).sum()), idx=idx, jj=jj,
               gap=float(np.min(np.abs(w[~z]))) if (~z).any() else float("nan"),
               zmax=float(np.max(np.abs(w[z]))) if z.any() else 0.0)
    if want_vecs:
        res["V"] = V
    return res


def checks(o):
    one = np.eye(o["dim"])
    return dict(
        sq=max(np.abs(o["GR"] @ o["GR"] - one).max(), np.abs(o["Gh"] @ o["Gh"] - one).max()),
        gw=np.abs(o["GR"] @ o["D"] + o["D"] @ o["Gh"]).max(),
        herm=np.abs(o["D"] - o["D"].conj().T).max(),
        hgkp=np.abs(o["H"] - (o["GR"] + o["a"] * o["DGKP"])).max(),
        comm=max(np.abs(o["D"] @ Ji - Ji @ o["D"]).max() for Ji in o["J"]))


# ---------------- header ----------------
out("# Job U1: strings on the fuzzy sphere - RESULTS (generated by run.py; do not edit by hand)")
out("")
out(f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')} (local time, BST = UTC+01:00). Python {platform.python_version()}, "
    f"numpy {np.__version__}, scipy {scipy.__version__}, sympy {sp.__version__}.")
out("")
out("Fixed before the first run (Helios's spec): Stage A PASS = exactly |n| zero modes of D_GW at every (N, n) "
    f"with N in {N_A[0]}..{N_A[-1]}, n in {N_CHARGE_A[0]}..{N_CHARGE_A[-1]}, n < N. Stage B PASS = x* (n/N where "
    f"delta_1 reaches {DELTA_STAR:g}) agrees over N = {N_B} within {TH_SPREAD:.0%}, read as max(x*)/min(x*) - 1 <= {TH_SPREAD:g}. "
    f"Grade: PASS = A exact and B collapses; PARTIAL = A exact, no clean collapse; FAIL = A wrong with D_GW. "
    f"Zero-mode tolerance |lambda| < {ZERO_TOL:g}; level grouping tolerance {LEVEL_TOL:g} [assumed input].")
out("")
out("Notation: N = 2L+1 is the matrix size of the base fuzzy sphere (Venus: brane count / resolution), n = number of strings = monopole")
out("charge. The charge-n sector is the AIN block L' = L^(a) = L - n/2 of A_i = L_i x 1 + 1 x T_i with T = n/2 (AIN eqs. 3.40-3.43),")
out("i.e. fermions are 2-spinor-valued (2L'+1) x (2L+1) matrices, A_i acting from the left as spin L', L_i from the right as spin L.")
out("Operators as written in AIN: a = 1/(L+1/2) (2.18); Gamma^R = a(sigma.L^R - 1/2) (2.16); H = a(sigma.A + 1/2) (2.19);")
out("Gamma^ = H/sqrt(H^2) (2.17), = (sigma.L' + 1/2)/(L' + 1/2) on the block (3.30); D_GW = -a^-1 Gamma^R (1 - Gamma^R Gamma^) (2.23);")
out("index = (1/2) Tr(Gamma^R + Gamma^) (2.28), = 2(L - L') on the block (3.37) [standard: AIN].")
out("")

# ---------------- sympy targets ----------------
k_, n_ = sp.symbols("k n", positive=True, integer=True)
j_ = (n_ - 1) / sp.Integer(2) + k_
lam2_round = sp.expand((j_ + sp.Rational(1, 2)) ** 2 - n_ ** 2 / 4)
deg_round = sp.expand(2 * j_ + 1)
idx_closed = sp.simplify(2 * (sp.Symbol("L") - (sp.Symbol("L") - n_ / 2)))
out("## Round-sphere targets [standard; sympy]")
out("")
out(f"Charge-n Dirac operator on the round unit S^2 (Wu-Yang monopole harmonics): level j = (n-1)/2 + k has lambda^2 = (j+1/2)^2 - n^2/4 "
    f"= {lam2_round} and degeneracy 2j+1 = {deg_round} per sign; k = 0 is the zero-mode multiplet, j = (n-1)/2, {deg_round.subs(k_, 0)} states.")
out(f"AIN block index 2(L - L') with L' = L - n/2: {idx_closed} [standard: AIN (3.37)].")
out("")
lam_round = lambda k, n: float(sp.sqrt(lam2_round.subs({k_: k, n_: n})))
deg_r = lambda k, n: int(deg_round.subs({k_: k, n_: n}))

# ---------------- Stage A ----------------
out("## Stage A [standard] - zero modes vs the GW index (graded)")
out("")
out("| N | n | dim | zero modes | n+ (Gamma^R=+1) | n- | index (1/2)Tr(Gamma^R+Gamma^) | closed form 2(L-L') | J^2 on zero modes | j(j+1), j=(n-1)/2 | max|lambda| of zero modes | smallest nonzero |lambda| |")
out("|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|")
A_ok = True
A_rows = 0
worst = dict(sq=0.0, gw=0.0, herm=0.0, hgkp=0.0, comm=0.0)
jdev = 0.0
gkp_zero = {}
specA = {}
for N in N_A:
    L = (N - 1) / 2
    for n in N_CHARGE_A:
        if n >= N:
            continue
        o = module_ops(L, L - n / 2)
        r = analyse(o)
        c = checks(o)
        for kk in worst:
            worst[kk] = max(worst[kk], float(c[kk]))
        jt = ((n - 1) / 2) * ((n + 1) / 2) if n > 0 else float("nan")
        jstr = ", ".join(f"{x:.6f}" for x in np.unique(np.round(r["jj"], 9))) if r["nz"] else "-"
        if r["nz"]:
            jdev = max(jdev, float(np.max(np.abs(r["jj"] - jt))))
        ok = (r["nz"] == abs(n)) and (r["npos"] - r["nneg"] == n) and abs(r["idx"] - n) < 1e-9
        A_ok &= ok
        A_rows += 1
        wg = np.linalg.eigvalsh(o["DGKP"])
        gkp_zero[(N, n)] = (int((np.abs(wg) < ZERO_TOL).sum()), float(np.min(np.abs(wg))))
        specA[(N, n)] = r["w"]
        out(f"| {N} | {n} | {o['dim']} | {r['nz']} | {r['npos']} | {r['nneg']} | {r['idx']:.6f} | {2 * (L - (L - n / 2)):g} | {jstr} | "
            + (f"{jt:.6f}" if n > 0 else "-") + f" | {r['zmax']:.1e} | {r['gap']:.6f} |")
out("")
out(f"Operator checks over all {A_rows} Stage A sectors [identity; computed]: max |Gamma^2 - 1| = {worst['sq']:.1e}; "
    f"max |Gamma^R D + D Gamma^| (GW relation 2.27) = {worst['gw']:.1e}; max |D - D^dagger| = {worst['herm']:.1e}; "
    f"max |H - (Gamma^R + a D_GKP)| (2.20) = {worst['hgkp']:.1e}; max |[D, J_i]| = {worst['comm']:.1e}.")
out(f"J^2 on the zero modes: max |J^2 - j(j+1)| with j = (n-1)/2 over all n >= 1 sectors = {jdev:.1e}, so the |n| zero modes form one "
    f"spin-(|n|-1)/2 multiplet [computed].")
out(f"**Stage A: {'PASS' if A_ok else 'FAIL'}** - exactly |n| zero modes, all of chirality +1, index = n, in all {A_rows} sectors: {A_ok} [computed].")
out("")
g_bad = {kk: v for kk, v in gkp_zero.items() if v[0] != kk[1]}
gmin = {kk: v[1] for kk, v in gkp_zero.items() if kk[1] > 0}
out(f"Other operator, reported only (it grades only itself): D_GKP = sigma.(A - L^R) + 1 on the same block has the right zero-mode count in "
    f"{len(gkp_zero) - len(g_bad)} of {len(gkp_zero)} sectors (only the n = 0 ones); for n >= 1 its smallest |lambda| ranges over "
    f"[{min(gmin.values()):.6f}, {max(gmin.values()):.6f}], so it has no exact zero modes [computed].")
out("")

# opposite orientation, reported only
out("Opposite orientation, reported only: L' = L + n/2 (charge -n).")
out("")
out("| N | n | dim | zero modes | n+ | n- | index | closed form 2(L-L') |")
out("|---:|---:|---:|---:|---:|---:|---:|---:|")
neg_ok = True
for N in N_NEG:
    L = (N - 1) / 2
    for n in N_CHARGE_A:
        if n == 0:
            continue
        o = module_ops(L, L + n / 2)
        r = analyse(o)
        neg_ok &= (r["nz"] == n) and (r["nneg"] == n) and abs(r["idx"] + n) < 1e-9
        out(f"| {N} | {n} | {o['dim']} | {r['nz']} | {r['npos']} | {r['nneg']} | {r['idx']:.6f} | {2 * (L - (L + n / 2)):g} |")
out(f"Opposite orientation: |n| zero modes, all chirality -1, index -n: {neg_ok} [computed].")
out("")

# literal AIN isospin construction cross-check
out("Cross-check against the literal AIN construction (full space with isospin T = n/2, A_i = L_i x 1 + 1 x T_i, Gamma^ = H/sqrt(H^2)")
out("by eigendecomposition, projector P^(a) by AIN (3.43), D_GW from (2.23) then restricted to the range of P^(a)) [computed]:")


def literal(N, n, block="charge"):
    L, T = (N - 1) / 2, n / 2
    dl, dt = N, int(round(2 * T + 1))
    Ls, Ts = spin(L), spin(T)
    Il, It = np.eye(dl), np.eye(dt)
    Aleft = [np.kron(Ls[i], It) + np.kron(Il, Ts[i]) for i in range(3)]
    dA = dl * dt
    a = 1.0 / (L + 0.5)
    S = [np.kron(s, np.eye(dA * dl)) for s in SIG]
    AL = [np.kron(I2, np.kron(Aleft[i], Il)) for i in range(3)]
    LR = [np.kron(I2, np.kron(np.eye(dA), Ls[i].T)) for i in range(3)]
    one = np.eye(2 * dA * dl)
    GR = a * (sum(S[i] @ LR[i] for i in range(3)) - 0.5 * one)
    H = a * (sum(S[i] @ AL[i] for i in range(3)) + 0.5 * one)
    hw, hv = np.linalg.eigh(H)
    Gh = (hv * np.sign(hw)) @ hv.conj().T
    D = -(1.0 / a) * GR @ (one - GR @ Gh)
    spins = [abs(L - T) + i for i in range(int(round(2 * min(L, T))) + 1)]   # irreps present in A_i
    A2 = sum(x @ x for x in Aleft)
    Lsel = min(spins) if block == "charge" else block
    P = np.eye(dA, dtype=complex)
    for Lb in spins:
        if abs(Lb - Lsel) > 1e-12:
            P = P @ (A2 - Lb * (Lb + 1) * np.eye(dA)) / (Lsel * (Lsel + 1) - Lb * (Lb + 1))
    Pfull = np.kron(I2, np.kron(P, Il))
    pw, pv = np.linalg.eigh((Pfull + Pfull.conj().T) / 2)
    B = pv[:, pw > 0.5]
    Dr = B.conj().T @ D @ B
    w = np.linalg.eigvalsh((Dr + Dr.conj().T) / 2)
    idx = 0.5 * float(np.trace(Pfull @ (GR + Gh)).real)
    perr = float(np.abs(Pfull @ Pfull - Pfull).max())
    pcomm = float(np.abs(Pfull @ D - D @ Pfull).max())
    return dict(w=w, Lsel=Lsel, spins=spins, idx=idx, nz=int((np.abs(w) < ZERO_TOL).sum()), dim=2 * dA * dl,
                perr=perr, pcomm=pcomm)


lit_dev, lit_n, lit_ok, lit_p = 0.0, 0, True, 0.0
for N in N_LIT:
    for n in range(1, N):
        if 2 * N * (n + 1) * N > LIT_MAXDIM:
            continue
        lr = literal(N, n)
        red = np.sort(np.linalg.eigvalsh(module_ops((N - 1) / 2, (N - 1) / 2 - n / 2)["D"]))
        lit_dev = max(lit_dev, float(np.max(np.abs(np.sort(lr["w"]) - red))))
        lit_ok &= (lr["nz"] == n) and abs(lr["idx"] - n) < 1e-9
        lit_p = max(lit_p, lr["perr"], lr["pcomm"])
        lit_n += 1
out(f"{lit_n} sectors (N in {N_LIT}, 1 <= n < N, full dim <= {LIT_MAXDIM}): max |spectrum(literal, restricted) - spectrum(reduced module)| = "
    f"{lit_dev:.1e}; max |P^2 - P|, |[P, D_GW]| = {lit_p:.1e}; literal zero modes = n and index = n in all: {lit_ok}.")
out("So the reduced module used above is the AIN projected block, not a different operator [computed].")
out("")

# Venus: n = 3 zero modes are j = 1; rotation matrix is d^1(beta)
o = module_ops((N_D1 - 1) / 2, (N_D1 - 1) / 2 - 3 / 2)
r = analyse(o, want_vecs=True)
V = r["V"]
Jz = V.conj().T @ o["J"][2] @ V
Jy = V.conj().T @ o["J"][1] @ V
Jp = V.conj().T @ (o["J"][0] + 1j * o["J"][1]) @ V
mz, U = np.linalg.eigh(Jz)
U = U[:, ::-1]
mz = mz[::-1]
for i in range(1, U.shape[1]):              # Condon-Shortley phases: <m+1|J+|m> real positive
    el = (U[:, i - 1].conj() @ Jp @ U[:, i])
    U[:, i] *= np.conj(el) / abs(el)
Dz = U.conj().T @ scipy.linalg.expm(-1j * BETA_D1 * Jy) @ U
d1 = np.array([[float(Rotation.d(1, 1 - i, 1 - jx, BETA_D1).doit()) for jx in range(3)] for i in range(3)])
out(f"Venus's link [standard: Wigner d^1]: at N = {N_D1}, n = 3, the three zero modes have J_z = {', '.join(f'{x:+.6f}' for x in mz)}; "
    f"<m'|exp(-i beta J_y)|m> on them at beta = {BETA_D1:g} matches sympy's d^1_(m'm)(beta) to max |difference| = {np.abs(Dz - d1).max():.1e} [computed].")
out("")

# ---------------- Stage B ----------------
out("## Stage B [prediction] - lowest three nonzero levels against the round sphere (graded on n/N)")
out("")
out(f"delta_k = |lambda_k^fuzzy / lambda_k^round - 1|, lambda_k^round = sqrt(k(k+n)) (sympy target above), k = 1..{K_LEVELS}; "
    "degeneracy checked against n + 2k per sign. Rules (fixed before the run; Venus's additions agreed by Helios): the scan covers "
    f"n = 0..N-1 at each N; n* is found by linear interpolation in n between the neighbouring integers n0, n0+1 that bracket delta_1 = {DELTA_STAR:g} "
    "(first crossing), and x* = n*/N; the bracketing pair is printed; delta_1 at n = 0 is printed as the finite-N floor.")
out("")
xstar = {}
closed_dev = 0.0
ratio_dev = 0.0
deg_ok = True
for N in N_B:
    L = (N - 1) / 2
    out(f"### N = {N}")
    out("")
    out("| n | x = n/N | n/N^2 (printed only) | k | k/N (printed only) | lambda_k fuzzy | lambda_k round | degeneracy (fuzzy / n+2k) | delta_k |")
    out("|---:|---:|---:|---:|---:|---:|---:|---|---:|")
    d1s = []
    nmax_used = None
    n = 0
    while n < N:
        o = module_ops(L, L - n / 2)
        w = specA[(N, n)] if (N, n) in specA else np.linalg.eigvalsh(o["D"])
        lv = levels(w)
        for k in range(1, K_LEVELS + 1):
            if k > len(lv):
                out(f"| {n} | {n / N:.6f} | {n / N ** 2:.6f} | {k} | {k / N:.6f} | - | {lam_round(k, n):.6f} | level absent (only {len(lv)} positive levels) | - |")
                continue
            lf, dg = lv[k - 1]
            lr_ = lam_round(k, n)
            dk = abs(lf / lr_ - 1)
            deg_ok &= (dg == deg_r(k, n))
            closed_dev = max(closed_dev, abs(lf - np.sqrt(k * (k + n) * N / (N - n))) / lf)
            ratio_dev = max(ratio_dev, abs((lf / lv[0][0]) / (lr_ / lam_round(1, n)) - 1))
            if k == 1:
                d1s.append((n, dk))
            out(f"| {n} | {n / N:.6f} | {n / N ** 2:.6f} | {k} | {k / N:.6f} | {lf:.6f} | {lr_:.6f} | {dg} / {deg_r(k, n)} | {dk:.6f} |")
        nmax_used = n
        n += 1
    out("")
    floor = dict(d1s).get(0)
    out(f"N = {N}: finite-N floor delta_1(n = 0) = {floor:.3e} [computed; finite-size]. n scanned 0..{nmax_used} (= N-1).")
    xs = None
    for (n0, d0), (n1, dd1) in zip(d1s, d1s[1:]):
        if d0 < DELTA_STAR <= dd1:
            nstar = n0 + (DELTA_STAR - d0) * (n1 - n0) / (dd1 - d0)
            xs = nstar / N
            out(f"N = {N}: bracketing pair n = ({n0}, {n1}) with delta_1 = ({d0:.6f}, {dd1:.6f}); linear in n gives n* = {nstar:.6f}, "
                f"x* = n*/N = {xs:.6f} [computed].")
            break
    if xs is None:
        out(f"N = {N}: delta_1 never reaches {DELTA_STAR:g} for n < N [computed].")
    xstar[N] = xs
    out("")
have = [v for v in xstar.values() if v is not None]
spread = (max(have) / min(have) - 1) if len(have) == len(N_B) else float("inf")
B_ok = spread <= TH_SPREAD
out(f"x* per N: " + "; ".join(f"N = {N}: {('%.6f' % v) if v is not None else 'none'}" for N, v in xstar.items())
    + f". Spread max/min - 1 = {spread:.6f} (threshold {TH_SPREAD:g}); mean x* = {np.mean(have):.6f}.")
out(f"Degeneracy n + 2k per sign at every printed level: {deg_ok} [computed].")
out(f"**Stage B: {'PASS' if B_ok else 'FAIL'}** (collapse in n/N) [computed].")
out("")
xc = 1 - 1 / (1 + DELTA_STAR) ** 2
out("Reported only [post-hoc: pattern seen in a prototype before this run; verified here numerically, not proved]: every positive level "
    f"of D_GW in the block is lambda_k = sqrt(k(k+n) N/(N-n)), k = 1..N-n. Max relative deviation over all printed levels = {closed_dev:.1e}; "
    f"level ratios lambda_k/lambda_1 equal the round ratios to max |rel. difference| = {ratio_dev:.1e}. So the drift is a uniform rescaling by "
    f"sqrt(N/(N-n)) = sqrt((2L+1)/(2L'+1)), the same for every k, and delta_1 = 1/sqrt(1 - n/N) - 1 reaches {DELTA_STAR:g} at "
    f"x = 1 - 1/(1+{DELTA_STAR:g})^2 = {xc:.6f}. The per-N spread in x* comes only from the linear interpolation on the integer-n grid.")
out("")

# ---------------- Stage C ----------------
out("## Stage C [reported only] - too many strings for the bubble: n = N-1, N, N+1")
out("")
out("| construction | N | n | sector exists? | L' | dim | zero modes | index | positive levels (value x degeneracy) |")
out("|---|---:|---:|---|---:|---:|---:|---:|---|")
for N in N_C:
    L = (N - 1) / 2
    for n in (N - 1, N, N + 1):
        Lp = L - n / 2
        if Lp < 0:
            out(f"| reduced block L' = L - n/2 (charge +n) | {N} | {n} | no: L' = {Lp:g} < 0, no spin-L' representation | {Lp:g} | - | - | - | - |")
            continue
        o = module_ops(L, Lp)
        r = analyse(o)
        lv = levels(r["w"])
        out(f"| reduced block L' = L - n/2 (charge +n) | {N} | {n} | yes | {Lp:g} | {o['dim']} | {r['nz']} | {r['idx']:.6f} | "
            + ", ".join(f"{x:.6f} x {d}" for x, d in lv) + " |")
    for n in (N - 1, N, N + 1):
        o = module_ops(L, L + n / 2)
        r = analyse(o)
        out(f"| opposite block L' = L + n/2 (charge -n) | {N} | {n} | yes | {L + n / 2:g} | {o['dim']} | {r['nz']} | {r['idx']:.6f} | "
            f"lowest {levels(r['w'])[0][0]:.6f} x {levels(r['w'])[0][1]} |")
for N in N_C_LIT:
    for n in (N - 1, N, N + 1):
        lr = literal(N, n)
        out(f"| literal AIN, isospin T = n/2, lowest block of A_i | {N} | {n} | irreps of A_i: {', '.join(f'{s:g}' for s in lr['spins'])} | "
            f"{lr['Lsel']:g} | {lr['dim']} (full) | {lr['nz']} | {lr['idx']:.6f} | - |")
out("")
out(f"Reading [computed]: in the charge +n block the largest charge that exists is n = N - 1 (L' = 0). There D_GW has the N-1 zero modes and one "
    f"other level, at the cutoff value 2/a = N, with degeneracy N+1: no smooth levels are left. For n >= N the block L - n/2 does not exist. In the "
    f"literal isospin construction the lowest block of A_i is then |L - T| = T - L, whose index is 2L - 2(T - L) = 2(N-1) - n, i.e. the index "
    f"turns back down (N-2 at n = N, N-3 at n = N+1) instead of growing. The opposite orientation (charge -n) exists for every n.")
out("")

# ---------------- notes and grade ----------------
out("## Notes")
out("")
out("- Bonus [standard]: the Stage B targets lambda^2 = k(k+|n|), degeneracy |n|+2k, are also the angular levels of a charged spin-1/2 particle on the")
out("  S^2 of a magnetically charged black-hole horizon (near-horizon AdS_2 x S^2), where the flux through S^2 plays the role of n (Wu-Yang monopole harmonics).")
out(f"- Venus: N = brane count / resolution, n = number of strings; the n = 3 zero modes form j = 1 and rotate with d^1(beta) (checked above).")
out("")
grade = "PASS" if (A_ok and B_ok) else ("PARTIAL" if A_ok else "FAIL")
out("## Summary")
out("")
out(f"- Stage A (zero modes = |n|, GW index): {'PASS' if A_ok else 'FAIL'}")
out(f"- Stage B (collapse of x* in n/N): {'PASS' if B_ok else 'FAIL'} (x* spread {spread:.6f}, threshold {TH_SPREAD:g})")
out(f"- **Overall grade: {grade}**")
out(f"- Runtime: {time.time() - T0:.0f} s [computed].")
with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(OUT) + "\n")

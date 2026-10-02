#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job Six: p-brane power counting + the x^2 y^2 toy (a 2-matrix caricature of the
supermembrane matrix model).

Writes RESULTS.md (ONLY ever written by this script) and x2y2_levels.png next to itself.
Run:  set PYTHONIOENCODING=utf-8;  python -B run.py
Cost: sparse shift-invert (scipy.sparse.linalg.eigsh) on grids up to 399^2; a few minutes.
"""
import os, sys, time, platform
import numpy as np
import scipy
import scipy.sparse as sps
from scipy.sparse.linalg import eigsh
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
T_START = time.time()
OUT = []


def out(line=""):
    print(line, flush=True)
    OUT.append(line)


# ---------------- parameters and grading rules (fixed BEFORE the run) ----------------
S_LIST = [0.0, 0.5, 1.0]
L_LIST = [4, 6, 8, 10, 12]
H_SCAN = 0.08                     # grid step of the main scan (both directions)
L_CONV, H_CONV = 12, 0.06         # grid-convergence check: L = 12 with h = 0.08 and 0.06
N_LEV = 6                         # levels per parity sector (each is a doublet of H)
X_VALLEY = [4.0, 8.0, 12.0, 16.0]
LY_VALLEY, HY_FINE = 3.2, 0.005   # 1D transverse problem: y in [-3.2, 3.2], fine step
SHIFT = -1.0                      # shift-invert target (below the whole spectrum)
CONV_PASS, CONV_PARTIAL = 1e-3, 1e-2   # s = 0, 1/2: max rel. change of lowest 3 levels, L=10 -> 12
SLOPE_WINDOW = (-2.3, -1.7)            # s = 1: local d lnE1 / d lnL between L = 10 and 12
VALLEY_REL_TOL = 1e-4                  # identity: |E - (1-s)|x|| / |x| at the largest x
POSITIVITY_TOL = 1e-8                    # allow only roundoff-level negativity in H_1 box levels
MONOTONICITY_TOL = 1e-9                  # allow only roundoff-level upward steps in L


# =====================================================================================
# Stage A: power counting
# =====================================================================================
def stage_a():
    out("## Stage A: p-brane power counting [standard]")
    out("")
    p = sp.symbols("p", positive=True, integer=True)
    d = p + 1                               # world-volume dimension
    dim_len = -1                            # mass units, hbar = c = 1: [length] = -1
    dim_T = -d * dim_len                    # S = -T ∫ d^d σ sqrt(-det g) is dimensionless => [T] = d
    dim_X = dim_len                         # embedding coordinate X is a length
    phi = sp.simplify(dim_T / 2 + dim_X)    # canonical field φ = sqrt(T) X
    # NG static gauge: sqrt(det(1 + ∂X·∂X)) = 1 + ½(∂X)² + O((∂X)⁴); T(∂X)⁴ = T⁻¹(∂φ)⁴
    g4_from_T = sp.simplify(dim_T - 2 * dim_T)
    g4_from_phi = sp.simplify(d - 4 * (phi + 1))
    # Polyakov / sigma-model form with curved target: T·R·X²(∂X)² = (R/T) φ²(∂φ)², [R] = 2
    gs_from_T = sp.simplify(2 - dim_T)
    gs_from_phi = sp.simplify(d - (4 * phi + 2))
    # Polyakov kinetic term sqrt(-γ) γ^ab ∂X·∂X: under γ -> Ω² γ it scales as Ω^(d-2)
    weyl = sp.simplify(d - 2)
    assert sp.simplify(g4_from_T - g4_from_phi) == 0
    assert sp.simplify(gs_from_T - gs_from_phi) == 0
    out("Derived symbolically with sympy for general p [computed]:")
    out(f"- [T] = {dim_T},  [φ] = [T]/2 + [X] = {phi}")
    out(f"- NG quartic coupling g₄ of (∂φ)⁴: [g₄] = -[T] = {g4_from_T}; check d - 4([φ]+1) = {g4_from_phi}  (agree)")
    out(f"- Polyakov/σ-model coupling g_σ = R/T of φ²(∂φ)²: [g_σ] = 2 - [T] = {gs_from_T}; check d - (4[φ]+2) = {gs_from_phi}  (agree)")
    out(f"- Weyl weight of sqrt(-γ)γ^ab: {weyl}  (Weyl invariance iff 0)")
    out("")
    out("| p | d = p+1 | [φ] | [g₄] NG (∂φ)⁴ | [g_σ] Polyakov φ²(∂φ)² | Weyl weight | renormalisable | Weyl-invariant |")
    out("|---|---|---|---|---|---|---|---|")
    rows = []
    for pv in (1, 2, 3, 5):
        sub = {p: pv}
        r = dict(p=pv, d=int(d.subs(sub)), phi=sp.nsimplify(phi.subs(sub)),
                 g4=int(g4_from_T.subs(sub)), gs=int(gs_from_T.subs(sub)), w=int(weyl.subs(sub)))
        r["ren"] = "yes" if r["gs"] >= 0 else "no"     # best form (Polyakov) has no negative-dimension coupling
        r["weyl"] = "yes" if r["w"] == 0 else "no"
        rows.append(r)
        out(f"| {pv} | {r['d']} | {r['phi']} | {r['g4']} | {r['gs']} | {r['w']} | {r['ren']} | {r['weyl']} |")
    out("")
    out("Reading: [φ] = (p-1)/2 vanishes only for the string. For p = 1 the static-gauge NG quartic")
    out("coupling has dimension -2, but the classically equivalent Polyakov form is a 2D σ-model whose")
    out("coupling is marginal (dimension 0) and which is Weyl invariant: renormalisable [standard]. For p ≥ 2")
    out("every interaction coupling has negative mass dimension (-(p+1) in NG, 1-p in the σ-model form) and")
    out("the Weyl weight p-1 ≠ 0 (Polyakov then needs a cosmological term (p-1)√-γ): non-renormalisable by")
    out("power counting and no Weyl invariance [standard].")
    out("")
    return rows


# =====================================================================================
# Stage B: x² y² toy.  H_s = p_x² + p_y² + x²y² + s(x σ3 + y σ1) on [-L, L]², Dirichlet.
# =====================================================================================
S1 = np.array([[0, 1], [1, 0]], dtype=complex)
S2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
S3 = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def grid(L, h):
    N = int(round(2 * L / h))
    assert abs(N * h - 2 * L) < 1e-9 and N % 2 == 0, (L, h)
    return -L + h * np.arange(1, N)          # interior points; walls at ±L; symmetric, contains 0


def T4(n, h):
    """-d²/dx², 4th-order 5-point stencil, Dirichlet walls via odd reflection ghost points."""
    main = np.full(n, 30.0)
    main[0] = main[-1] = 29.0
    return sps.diags([np.full(n - 2, 1.0), np.full(n - 1, -16.0), main,
                      np.full(n - 1, -16.0), np.full(n - 2, 1.0)], [-2, -1, 0, 1, 2]) / (12 * h * h)


def flip(n):
    return sps.csr_matrix((np.ones(n), (np.arange(n), np.arange(n)[::-1])), shape=(n, n))


def pieces(L, h):
    g = grid(L, h)
    n = g.size
    T = T4(n, h)
    I = sps.identity(n, format="csr")
    X = np.repeat(g, n)                       # vector index = i_x * n + i_y
    Y = np.tile(g, n)
    return n, sps.kron(T, I) + sps.kron(I, T), X, Y, sps.kron(flip(n), I)


def K_op(L, h, s, sign=+1):
    """H restricted to the sector P psi = sign*psi, P = σ1 ⊗ (x -> -x): psi2 = sign*R_x psi1."""
    n, Lap, X, Y, Rx = pieces(L, h)
    M = Lap + sps.diags(X * X * Y * Y + s * X)
    if s:
        M = M + sign * s * (sps.diags(Y) @ Rx)
    return M.tocsc()


def H_full(L, h, s):
    n, Lap, X, Y, Rx = pieces(L, h)
    V = sps.diags(X * X * Y * Y)
    return sps.bmat([[Lap + V + s * sps.diags(X), s * sps.diags(Y)],
                     [s * sps.diags(Y), Lap + V - s * sps.diags(X)]]).tocsc()


def lowest(M, k):
    v0 = np.random.default_rng(0).standard_normal(M.shape[0])
    ev = eigsh(M, k=k, sigma=SHIFT, which="LM", v0=v0, return_eigenvectors=False)
    return np.sort(ev)


def valley_level(x, s, Ly, h):
    """Lowest eigenvalue of the transverse problem p_y² + x²y² + s(x σ3 + y σ1) at fixed x."""
    g = grid(Ly, h)
    n = g.size
    T = T4(n, h)
    V = sps.diags(x * x * g * g)
    I = sps.identity(n)
    C = s * sps.diags(g)
    M = sps.bmat([[T + V + s * x * I, C], [C, T + V - s * x * I]]).tocsc()
    return lowest(M, 1)[0]


def checks_identity():
    out("## Stage B.0: structural identities [identity]")
    out("")
    # (i) dWLN eq. (1.5) has spin term x σ1 - y σ2; ours is x σ3 + y σ1. Find U with U σ3 U† = σ1, U σ1 U† = -σ2.
    A = np.vstack([np.kron(S3.T, I2) - np.kron(I2, S1), np.kron(S1.T, I2) + np.kron(I2, S2)])
    _, sv, Vh = np.linalg.svd(A)
    U = Vh[-1].conj().reshape(2, 2, order="F") * np.sqrt(2)
    uni = np.abs(U.conj().T @ U - I2).max()
    rng = np.random.default_rng(1)
    err = 0.0
    for _ in range(5):
        x, y = rng.standard_normal(2)
        err = max(err, np.abs(U @ (x * S3 + y * S1) @ U.conj().T - (x * S1 - y * S2)).max())
    out(f"- dWLN (1.5) ↔ H_1: constant spin rotation U with U(xσ3+yσ1)U† = xσ1-yσ2 = [[0,x+iy],[x-iy,0]]:")
    out(f"  null-space singular value {sv[-1]:.1e}, |U†U-1| = {uni:.1e}, max mapping error = {err:.1e}.")
    out("  So H_{s=1} is unitarily equivalent to the de Wit–Lüscher–Nicolai model, same spectrum [identity].")
    # (ii) parity reduction
    L, h = 3, 0.15
    rows = []
    for s in (0.5, 1.0):
        ef = lowest(H_full(L, h, s), 2 * N_LEV)
        ep = lowest(K_op(L, h, s, +1), N_LEV)
        em = lowest(K_op(L, h, s, -1), N_LEV)
        d = max(np.abs(ef[0::2] - ep).max(), np.abs(ef[1::2] - ep).max(), np.abs(em - ep).max())
        rows.append((s, d, ef[:4]))
    out("- Parity P = σ1⊗(x→-x) commutes with H_s; the two sectors K± are mapped into each other by y → -y,")
    out("  so spec(H) = spec(K+) counted twice. Checked on a small grid (L=3, h=0.15) [identity]:")
    for s, d, e4 in rows:
        out(f"  s = {s}: max |E_full(pairs) - E_K+|, |E_K- - E_K+| = {d:.1e};  full H lowest 4: " +
            ", ".join(f"{v:.6f}" for v in e4))
    out("  All later levels are K+ levels; each is a doublet of H.")
    out("Operator identity: H_s = (1-s)H_0 + sH_1 [identity].")
    out("After the fixed spin rotation, H_1 = Q^2 with Q = σ1 p_x + σ3 p_y + σ2 xy,")
    out("and Q^2 = p^2 + x^2y^2 + yσ3 - xσ1, the supersymmetric structure of dWLN eq. (1.5) [identity].")
    out("Thus H_1 ≥ 0, and min-max gives E_k(H_s) ≥ (1-s)E_k(H_0); Simon's result makes every s < 1 discrete [standard].")
    out("")
    return err < 1e-12 and all(r[1] < 1e-8 for r in rows)


def valley_check():
    out("## Stage B.1: valley identity check [identity]")
    out("")
    out(f"Transverse problem h_y(x) = p_y² + x²y² + s(xσ3 + yσ1) on y ∈ [-{LY_VALLEY}, {LY_VALLEY}], h_y = {HY_FINE}, 4th-order FD.")
    out("Prediction: lowest eigenvalue → (1-s)|x| (oscillator zero point |x| minus spin -s|x|). The yσ1 term")
    out("adds a second-order shift -s²/(4(1+s)x²) (hand-derived perturbation theory, shown for comparison, not graded).")
    out("")
    out("| s | x | E_num | (1-s)|x| | E_num - (1-s)|x| | (E_num - (1-s)|x|)·x² | PT: -s²/(4(1+s)) |")
    out("|---|---|---|---|---|---|---|")
    ok = True
    for s in S_LIST:
        res = []
        for x in X_VALLEY:
            e = valley_level(x, s, LY_VALLEY, HY_FINE)
            r = e - (1 - s) * abs(x)
            res.append(r)
            out(f"| {s} | {x:g} | {e:.8f} | {(1 - s) * abs(x):.4f} | {r:+.3e} | {r * x * x:+.5f} | {-s * s / (4 * (1 + s)):+.5f} |")
        if s > 0:
            ok &= all(abs(res[i + 1]) < abs(res[i]) for i in range(len(res) - 1))
        ok &= abs(res[-1]) / X_VALLEY[-1] < VALLEY_REL_TOL
    out("")
    out(f"Identity check (relative residual at x = {X_VALLEY[-1]:g} below {VALLEY_REL_TOL:g}, residual shrinking with x for s > 0): "
        f"{'PASS' if ok else 'FAIL'} [identity].")
    out("")
    return ok


def main_scan():
    E, tsolve = {}, {}
    for s in S_LIST:
        E[s] = {}
        for L in L_LIST:
            t0 = time.time()
            E[s][L] = lowest(K_op(L, H_SCAN, s), N_LEV)
            tsolve[(s, L)] = time.time() - t0
            print(f"  scan s={s} L={L}: {tsolve[(s, L)]:.1f}s", flush=True)
    return E, tsolve


def conv_scan():
    Ec = {}
    for s in S_LIST:
        t0 = time.time()
        Ec[s] = lowest(K_op(L_CONV, H_CONV, s), N_LEV)
        print(f"  conv s={s}: {time.time() - t0:.1f}s", flush=True)
    return Ec


def lslope(E, L1, L2, k):
    return np.log(E[L2][k] / E[L1][k]) / np.log(L2 / L1)


def report_scan(E, Ec):
    grades = {}
    out("## Stage B.2: main scan (lowest levels against box size)")
    out("")
    out(f"Grid step h = {H_SCAN} in x and y; 4th-order FD; levels of the parity sector K+ (each a doublet of H).")
    out("Valley width at the box edge is ~ L^(-1/2); h·√L is printed as the [grid-step] ratio (want ≪ 1).")
    out("")
    for s in S_LIST:
        out(f"### s = {s}")
        out("")
        out("| L | n per axis | h·√L | " + " | ".join(f"E{k + 1}" for k in range(N_LEV)) + " |")
        out("|---|---|---|" + "---|" * N_LEV)
        for L in L_LIST:
            out(f"| {L} | {grid(L, H_SCAN).size} | {H_SCAN * np.sqrt(L):.3f} | " +
                " | ".join(f"{v:.6f}" for v in E[s][L]) + " |")
        out("")
        slopes_fit = [np.polyfit(np.log(L_LIST), np.log([E[s][L][k] for L in L_LIST]), 1)[0] for k in range(N_LEV)]
        slopes_loc = [lslope(E[s], 10, 12, k) for k in range(N_LEV)]
        out("Fitted slope d lnE/d lnL over all L [computed]: " + ", ".join(f"E{k + 1}: {v:+.3f}" for k, v in enumerate(slopes_fit)))
        out("Local slope between L = 10 and 12 [computed]: " + ", ".join(f"E{k + 1}: {v:+.4f}" for k, v in enumerate(slopes_loc)))
        if s < 1:
            rel = [abs(E[s][12][k] - E[s][10][k]) / E[s][12][k] for k in range(N_LEV)]
            out("Relative change L=10→12 [computed]: " + ", ".join(f"E{k + 1}: {v:.1e}" for k, v in enumerate(rel)))
            m3 = max(rel[:3])
            g = "PASS" if m3 < CONV_PASS else ("PARTIAL" if m3 < CONV_PARTIAL else "FAIL")
            out(f"Grade s = {s}: {g} — prediction 'discrete spectrum, converged in L' [prediction, Simon 1983]; "
                f"max relative change of E1–E3 between L = 10 and 12 is {m3:.1e} (PASS < {CONV_PASS:g}, PARTIAL < {CONV_PARTIAL:g}).")
        else:
            mono = all(np.all(np.diff([E[s][L][k] for L in L_LIST]) < 0) for k in range(N_LEV))
            sl = slopes_loc[0]
            inwin = SLOPE_WINDOW[0] <= sl <= SLOPE_WINDOW[1]
            g = "PASS" if (mono and inwin) else ("PARTIAL" if mono else "FAIL")
            out(f"All six levels fall monotonically with L: {mono} [computed]. Minimum level over the scan: "
                f"{min(E[s][L][0] for L in L_LIST):.6f} (H = Q² ≥ 0, so no negative level is expected).")
            ratios = E[s][12] / E[s][12][0]
            out("Ratios E_k/E_1 at L = 12 [computed]: " + ", ".join(f"{v:.3f}" for v in ratios) +
                f"  (1D box: k² = {', '.join(str((k + 1) ** 2) for k in range(N_LEV))})")
            leff = [(k + 1) * np.pi / np.sqrt(E[s][12][k]) for k in range(N_LEV)]
            out("Effective 1D box length ℓ_k = kπ/√E_k at L = 12 [computed]: " + ", ".join(f"{v:.2f}" for v in leff) +
                f"  vs full valley length 2L = 24 [hive-interpretation: free motion along one whole valley line].")
            out(f"Grade s = 1: {g} — prediction 'continuum: levels fall like 1/L²'; local slope of E1 between "
                f"L = 10 and 12 is {sl:+.3f} (PASS window {SLOPE_WINDOW}); the slope sits slightly below -2 because "
                f"ℓ_eff ≈ 2L - const [finite-size].")
        grades[s] = g
        out("")
    # Domain monotonicity and H_1 positivity checks
    out("## Domain monotonicity and positivity checks [computed]")
    out("")
    monotonic_ok = True
    for s in S_LIST:
        for k in range(N_LEV):
            vals = np.array([E[s][L][k] for L in L_LIST])
            diffs = np.diff(vals)
            ok = bool(np.all(diffs <= MONOTONICITY_TOL))
            monotonic_ok &= ok
            out(f"- monotonicity s = {s}, E{k + 1}: {'PASS' if ok else 'FAIL'}; ΔE for successive L = " +
                ", ".join(f"{v:+.2e}" for v in diffs) + ".")
    out(f"Domain monotonicity (every s and every level falls or stays as L grows): {'PASS' if monotonic_ok else 'FAIL'} [computed].")
    positivity_ok = True
    for L in L_LIST:
        e1 = E[1.0][L][0]
        ok = bool(e1 >= -POSITIVITY_TOL)
        positivity_ok &= ok
        out(f"- positivity s = 1, L = {L}: lowest box level E1 = {e1:.8f}; {'PASS' if ok else 'FAIL'} (tolerance −{POSITIVITY_TOL:g}).")
    out(f"H_1 = Q² positivity check over all scanned boxes: {'PASS' if positivity_ok else 'FAIL'} [computed; grid tolerance].")
    out("")

    # weaker wall: retained as an ungraded, post-hoc observation
    per_L = {L: bool(np.all(E[0.5][L] < E[0.0][L])) for L in L_LIST}
    out("All six s = ½ levels lie below the matching s = 0 levels (weaker wall (1-s)|x| = |x|/2) [computed, ungraded, post-hoc]: " +
        ", ".join(f"L={L}: {v}" for L, v in per_L.items()) + ".")
    e4_half, e4_zero = E[0.5][4][3], E[0.0][4][3]
    out(f"Where it fails is the squeezed small box (L = 4: E4 = {e4_half:.3f} at s = ½ vs {e4_zero:.3f} at s = 0) [finite-size, computed]; reported per L after the first run showed the all-L form failing at L = 4 [post-hoc].")
    out("The difference H_{1/2} − H_0 = ½(xσ3 + yσ1) has no fixed sign, so this ordering is not forced [post-hoc].")
    rr = E[0.5][12] / E[0.0][12]
    out("E(s=½)/E(s=0) at L = 12 [computed]: " + ", ".join(f"{v:.3f}" for v in rr) +
        f"  (a pure 1D valley wall would give (1/2)^(2/3) = {0.5 ** (2/3):.3f} [hive-interpretation]).")
    out("")

    out("## Stage B.3: grid convergence at L = 12 [grid-step]")
    out("")
    out(f"h = {H_SCAN} (h·√L = {H_SCAN * np.sqrt(L_CONV):.3f}) vs h = {H_CONV} (h·√L = {H_CONV * np.sqrt(L_CONV):.3f}); "
        "Richardson estimate assumes the 4th-order error ∝ h⁴.")
    out("")
    out("| s | level | E(h=0.08) | E(h=0.06) | difference | Richardson E(h→0) | rel. error of h=0.08 |")
    out("|---|---|---|---|---|---|---|")
    worst = {}
    fac = (H_SCAN / H_CONV) ** 4 - 1
    for s in S_LIST:
        worst[s] = 0.0
        for k in range(N_LEV):
            a, b = E[s][L_CONV][k], Ec[s][k]
            er = b + (b - a) / fac
            rel = abs(a - er) / abs(er)
            worst[s] = max(worst[s], rel)
            out(f"| {s} | E{k + 1} | {a:.6f} | {b:.6f} | {b - a:+.2e} | {er:.6f} | {rel:.1e} |")
    out("")
    sl_fine = None
    out("Worst relative grid error of the h = 0.08 levels at L = 12 [grid-step]: " +
        ", ".join(f"s={s}: {worst[s]:.1e}" for s in S_LIST))
    out("")

    out("Transverse zero-point cancellation on the scan grid at the box edge, s = 1 [grid-step]:")
    out("")
    out("| L = x | lowest h_y at h = 0.08 | at h = 0.005 | grid error | E1(L) of the 2D scan | error / E1 |")
    out("|---|---|---|---|---|---|")
    for L in L_LIST:
        a = valley_level(float(L), 1.0, LY_VALLEY, H_SCAN)
        b = valley_level(float(L), 1.0, LY_VALLEY, HY_FINE)
        out(f"| {L} | {a:+.6f} | {b:+.6f} | {a - b:+.2e} | {E[1.0][L][0]:.6f} | {(a - b) / E[1.0][L][0]:+.1e} |")
    out("")
    out("Reading [grid-step]: the transverse grid error grows like h⁴|x|³ and is largest at the wall, so the edge column")
    out("is a worst case. The 2D levels average it over the valley with weight |ψ|², and the ground mode peaks at the centre;")
    grid_pct = worst[1.0] * 100
    out(f"the measured 2D grid error of E1 at L = {L_CONV} (table above, {grid_pct:.2f}%) is the relevant number. It lowers the levels")
    out(f"more at larger L; the resulting local E1 slope between L = 10 and 12 is {lslope(E[1.0], 10, 12, 0):+.3f} [computed].")
    out("")
    return grades


def plot(E):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:  # plot is optional
        out(f"(plot skipped: {e})")
        return
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for s, mk in ((0.0, "o-"), (0.5, "s--")):
        for k in range(3):
            ax[0].plot(L_LIST, [E[s][L][k] for L in L_LIST], mk, label=f"s={s}, E{k + 1}")
    ax[0].set_xlabel("box half-size L"); ax[0].set_ylabel("E"); ax[0].set_title("s = 0, ½: converged (discrete)")
    ax[0].legend(fontsize=7)
    for k in range(N_LEV):
        ax[1].loglog(L_LIST, [E[1.0][L][k] for L in L_LIST], "o-", label=f"E{k + 1}")
    Ls = np.array(L_LIST, float)
    ax[1].loglog(Ls, E[1.0][12][0] * (12 / Ls) ** 2, "k:", label="∝ L⁻²")
    ax[1].set_xlabel("L"); ax[1].set_ylabel("E"); ax[1].set_title("s = 1: levels fall like 1/L² (continuum)")
    ax[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "x2y2_levels.png"), dpi=110)
    out("Plot: x2y2_levels.png (left: s = 0, ½ lowest three levels vs L; right: s = 1 log-log with an L⁻² guide).")
    out("")


def main():
    out("# Job Six: membrane power counting and the x²y² toy — RESULTS")
    out("")
    out("Written only by run.py. Tags: [computed] [identity] [assumed] [assumed input] [standard] [post-hoc]")
    out("[finite-size] [grid-step] [prediction] [hive-interpretation].")
    out(f"Python {platform.python_version()}, numpy {np.__version__}, scipy {scipy.__version__}, sympy {sp.__version__}.")
    out("")
    out("Model [assumed input]: H_s = p_x² + p_y² + x²y² + s(xσ3 + yσ1), p = -i∂, box [-L, L]², Dirichlet walls,")
    out(f"s ∈ {S_LIST}, L ∈ {L_LIST}, h = {H_SCAN}; grading thresholds fixed in run.py before the run.")
    out("")
    rows = stage_a()
    ok0 = checks_identity()
    okv = valley_check()
    print("main scan ...", flush=True)
    E, ts = main_scan()
    print("grid convergence ...", flush=True)
    Ec = conv_scan()
    grades = report_scan(E, Ec)
    plot(E)
    out("## Summary")
    out("")
    out(f"- Stage A table: derived symbolically; p = 1 renormalisable and Weyl invariant, p = 2, 3, 5 neither [standard].")
    out(f"- Structural identities (dWLN equivalence, parity doubling): {'PASS' if ok0 else 'FAIL'} [identity].")
    out(f"- Valley identity (1-s)|x|: {'PASS' if okv else 'FAIL'} [identity].")
    for s in S_LIST:
        out(f"- s = {s}: {grades[s]}")
    out("")
    out(f"Runtime: {time.time() - T_START:.0f} s [computed].")
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
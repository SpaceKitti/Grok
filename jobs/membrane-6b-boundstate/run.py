#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job 6b: does the supersymmetric x²y² membrane toy H = Q² have a zero-energy bound state?
Builds on Job Six (C:\\Users\\Akitt\\membrane-x2y2, main 05e6347), which is neither imported nor modified.
Writes RESULTS.md only (never hand-edited). Every number in RESULTS.md is printed from a variable.
Run:  $env:PYTHONIOENCODING='utf-8';  python -B run.py
"""
import os, time, math, hashlib, datetime, platform
import numpy as np
import scipy
import scipy.sparse as sps
from scipy.sparse.linalg import eigsh, splu, LinearOperator
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
FGHHY_PDF = r"C:\Users\Akitt\open-problems\03_membrane_renormalization\NPB567_231_Frohlich_Graf_Hasler_Hoppe_Yau_zero_energy_asymptotics.pdf"
T0 = time.time()
OUT = []


def w(line=""):
    print(line, flush=True)
    OUT.append(line)


# =====================================================================================
# Parameters and verdict rules: FIXED BEFORE THE FIRST RUN
# =====================================================================================
L_LIST = [8, 10, 12, 14, 16]       # box half-size: box [-L, L]^2 [assumed input]
H = 0.08                           # grid step (Job Six's scan step) [assumed input]
NEIG = 32                          # eigenvalues of the hermitian sector operator nearest 0 (they come in ± pairs)
N_SHOW = 8                         # singular values printed per L
N_FIT = 6                          # lowest levels fitted against L
N_LAD = 4                          # ladder test uses the median over the lowest N_LAD levels
L_A, L_B = 8, 16                   # candidate test compares L = 8 with L = 16
LADDER_WINDOW = (0.40, 0.625)      # ladder established if median σ(16)/σ(8) lies here (drop by 1.6–2.5×; 1/L gives 0.5)
CAND_TOL = 0.10                    # candidate: |σ_k(16)/σ_k(8) − 1| < 10% (spec example)
ZERO_FLOOR = 0.2                   # candidate (off-ladder near zero): σ_1 < 0.2 σ_2 at every L
GRID_L, GRID_H = 8, 0.064          # grid check of the direct Q discretisation
TRANS_X = [4.0, 8.0, 12.0, 16.0]   # 1D transverse lattice-mass diagnostic
TRANS_LY, TRANS_H = 3.2, [0.08, 0.04]
H6_NLEV, H6_SHIFT = 8, -1.0        # Job Six discretisation of H = Q² (cross-check)
PAIR_TOL = 1e-8                    # ± pairing of the spectrum of the real-antisymmetric-based Q_h [identity]
ID_TOL = 1e-10                     # small-grid identity checks
# [standard] FGHHY, Nucl. Phys. B 567 (2000) 231, Appendix 2, eqs. (50)–(53): Ψ = x^(−κ)(Ψ0 + ...), κ = −1/4, no L² solution
FGHHY_KAPPA = sp.Rational(-1, 4)
FGHHY_NORMALISABLE = False


# =====================================================================================
# Stage A (sympy): asymptotic zero mode in the valley
# =====================================================================================
def Qop(p1, p2, x, y, long=True, trans=True):
    """Our Q = −σ3 p_x + σ1 p_y + σ2 xy (p = −i∂), with Q² = H_1 = p² + x²y² + xσ3 + yσ1 (Job Six's s = 1)."""
    I = sp.I
    q1, q2 = sp.Integer(0), sp.Integer(0)
    if long:
        q1 += I * sp.diff(p1, x)
        q2 += -I * sp.diff(p2, x)
    if trans:
        q1 += -I * sp.diff(p2, y) - I * x * y * p2
        q2 += -I * sp.diff(p1, y) + I * x * y * p1
    return sp.expand(q1), sp.expand(q2)


def QF(p1, p2, x, y):
    """FGHHY Appendix 2: Q = i[[∂x, ∂y + xy], [∂y − xy, −∂x]]."""
    I = sp.I
    return (sp.expand(I * (sp.diff(p1, x) + sp.diff(p2, y) + x * y * p2)),
            sp.expand(I * (sp.diff(p1, y) - x * y * p1 - sp.diff(p2, x))))


def stage_a():
    w("## Stage A: asymptotic zero mode in the valley (sympy)")
    w("")
    xr, yr = sp.symbols("x_r y_r", real=True)
    f, g = sp.Function("f")(xr, yr), sp.Function("g")(xr, yr)
    lap = lambda u: sp.diff(u, xr, 2) + sp.diff(u, yr, 2)
    q = Qop(f, g, xr, yr); qq = Qop(*q, xr, yr)
    H1 = (-lap(f) + xr**2 * yr**2 * f + xr * f + yr * g, -lap(g) + xr**2 * yr**2 * g - xr * g + yr * f)
    id1 = all(sp.simplify(qq[i] - H1[i]) == 0 for i in range(2))
    qf = QF(f, g, xr, yr); qqf = QF(*qf, xr, yr)
    HF = (-lap(f) + xr**2 * yr**2 * f + xr * f - yr * g, -lap(g) + xr**2 * yr**2 * g - xr * g - yr * f)
    id2 = all(sp.simplify(qqf[i] - HF[i]) == 0 for i in range(2))
    f0 = sp.exp(-xr**2 - yr**2) * (1 + xr + 2 * yr + xr * yr**2)
    g0 = sp.exp(-xr**2 - 2 * yr**2) * (xr - yr**3 + 3)
    mapped = QF(f0.subs(yr, -yr), g0.subs(yr, -yr), xr, yr)
    mapped = [sp.expand(m.subs(yr, -yr)) for m in mapped]
    ours = Qop(f0, g0, xr, yr)
    id3 = all(sp.simplify(mapped[i] - ours[i]) == 0 for i in range(2))
    w("Model [assumed input; Job Six s = 1]: H = Q², Q = −σ₃p_x + σ₁p_y + σ₂xy, p = −i∂.")
    w(f"- Q² = p² + x²y² + xσ₃ + yσ₁ (Job Six's H₁) on generic f, g: {id1} [identity].")
    w(f"- FGHHY's Q_F = i[[∂x, ∂y + xy], [∂y − xy, −∂x]] squares to their eq. (50), (−Δ + x²y²) + xσ₃ − yσ₁: {id2} [identity].")
    w(f"- Our Q = R_y Q_F R_y with R_y: y → −y (checked on test functions): {id3} [identity]. So the two models are unitarily equivalent.")
    w("")
    # valley x → +∞, small y
    x = sp.symbols("x", positive=True); y = sp.symbols("y", real=True)
    kap, c = sp.symbols("kappa c", real=True)
    u = sp.Function("u")
    s_low = sp.dsolve(sp.Eq(u(y).diff(y) + x * y * u(y), 0)).rhs
    s_up = sp.dsolve(sp.Eq(u(y).diff(y) - x * y * u(y), 0)).rhs
    G = sp.exp(-x * y**2 / 2)
    k0 = Qop(sp.Integer(0), G, x, y, long=False)
    osc = sp.simplify((-sp.diff(G, y, 2) + x**2 * y**2 * G) / G)
    chi = sp.Matrix([0, 1]); sF = (chi.T * sp.Matrix([[1, 0], [0, -1]]) * chi)[0]
    w("**n = 0 (transverse) [identity]:** Q₀ = σ₁p_y + σ₂xy at fixed x. Q₀ψ = 0 splits into")
    w(f"(∂_y + xy)ψ₂ = 0 → ψ₂ = {s_low}, normalisable in y for x > 0; and (∂_y − xy)ψ₁ = 0 → ψ₁ = {s_up}, not normalisable.")
    w(f"So Ψ₀ = e^(−xy²/2)·χ with fermion state χ = (0, 1), σ₃χ = {sF}·χ; check Q₀Ψ₀ = {k0} [identity].")
    w(f"Oscillator zero point (−∂_y² + x²y²)G/G = {osc}; fermion term xσ₃ on χ gives {sF}·x; sum {sp.simplify(osc + sF * x)}: "
      "the transverse ground energy cancels exactly [identity].")
    w("")
    S = sp.simplify(sp.integrate(G * sp.diff(x**(-kap) * G, x), (y, -sp.oo, sp.oo)))
    ksol = sp.solve(sp.Eq(S, 0), kap)
    N0 = sp.integrate(G**2, (y, -sp.oo, sp.oo))
    flux = sp.simplify(S - sp.Rational(1, 2) * x**kap * sp.diff(x**(-2 * kap) * N0, x))
    w("**n = 1 (solvability) [computed, leading order]:** write Ψ = x^(−κ)Ψ₀ + Ψ₁ + …. The longitudinal part −σ₃p_x must be "
      "orthogonal to ker Q₀, so the condition is ⟨Ψ₀, σ₃∂_x(x^(−κ)Ψ₀)⟩_y = 0. With σ₃χ = −χ (fermion factor ≠ 0), this reduces to")
    w(f"∫G·∂_x(x^(−κ)G) dy = {S} = 0 → κ = {ksol}.")
    w(f"Equivalently, ∫G∂_x(x^(−κ)G)dy = ½x^κ ∂_x[x^(−2κ)∫G²dy], difference {flux} [identity]. At leading order the zero-mode condition "
      "says the transverse-integrated density x^(−2κ)·√(π/x) is constant along the valley. The x^(−1/2) width factor of the oscillator "
      "ground state therefore fixes κ = −1/4.")
    a_ans = (x**(-kap) * c * y * G / x, x**(-kap) * G)
    R = Qop(*a_ans, x, y)
    poly = sp.expand(sp.simplify(R[1] / (x**(-kap) * G)) * x)
    eqs = [sp.Eq(poly.coeff(y, 0), 0), sp.Eq(poly.coeff(y, 2), 0)]
    sol = sp.solve(eqs, [c, kap], dict=True)
    w(f"Independent route: the ansatz Ψ = x^(−κ)G·(c·y/x, 1) with Q Ψ = 0 in the lower component gives {sol} [computed].")
    kv = sol[0][kap]
    cv = sol[0][c]
    assert kv == ksol[0]
    Psi = (x**(-kv) * cv * y * G / x, x**(-kv) * G)
    Rr = Qop(*Psi, x, y)
    expo = lambda e: sp.limit(sp.log(e) / sp.log(x), x, sp.oo)
    nR = sp.simplify(sp.integrate(sp.simplify(Rr[0] * sp.conjugate(Rr[0])), (y, -sp.oo, sp.oo)) + sp.integrate(sp.simplify(Rr[1] * sp.conjugate(Rr[1])), (y, -sp.oo, sp.oo)))
    nL = sp.simplify(sp.integrate(sp.diff(x**(-kv) * G, x)**2, (y, -sp.oo, sp.oo)))
    nP = sp.simplify(sp.integrate(Psi[0]**2 + Psi[1]**2, (y, -sp.oo, sp.oo)))
    eR, eL = expo(nR) / 2, expo(nL) / 2
    w(f"With κ = {kv}, c = {cv}: Ψ ≈ x^({-kv})·e^(−xy²/2)·({cv}·y/x, 1). Residual ‖QΨ‖_y ∝ x^({eR}) against the cancelled term "
      f"‖∂_x(x^(−κ)G)‖_y ∝ x^({eL}); the gain is x^({eR - eL}), FGHHY's x^(−3/2) step [computed].")
    w("")
    N = sp.simplify(sp.integrate((x**(-kap) * G)**2, (y, -sp.oo, sp.oo)))
    p = sp.simplify(sp.log(sp.simplify(N / sp.sqrt(sp.pi))) / sp.log(x))
    pk = sp.simplify(p.subs(kap, kv))
    crit = sp.solve(sp.Eq(p, -1), kap)[0]
    Ix = sp.integrate(x**pk, (x, 1, sp.oo))
    normalisable = bool(kv > crit)
    fnorm = sp.simplify(-kv - sp.Rational(1, 4))
    w("**Normalisability [computed, leading order]:** with the transverse width included, ∫|Ψ|²dy = "
      f"{N} = √π·x^({p}). Along one valley arm, ∫^∞ x^({p}) dx < ∞ iff ({p}) < −1, i.e. κ > {crit}.")
    w(f"At κ = {kv}: ∫|Ψ|²dy ∝ x^({pk}), so ∫₁^∞ dx x^({pk}) = {Ix}, and the asymptotic zero mode is **normalisable: {normalisable}** "
      f"(∫|Ψ₀+Ψ₁|²dy = {nP}; the correction does not change the power).")
    w(f"In the normalised transverse basis, the profile is f_norm ∝ x^({fnorm}): a constant, i.e. the k = 0 threshold state of free "
      "motion along the valley [hive-interpretation].")
    w(f"Spec notation f ~ |x|^(−γ): **γ = κ = {kv}**, so f grows like |x|^({-kv}). The x < 0 arm (upper component, "
      "e^(−|x|y²/2)) and the y-valleys follow by the symmetries P = σ₁·(x → −x) and x ↔ y with σ₁ ↔ σ₃ [identity].")
    w("What is leading order: the n = 0 kernel and the n = 1 solvability condition of the formal series in x^(−3/2). FGHHY (Remark 1) "
      "note such series are typically asymptotic, not convergent. The statement covers zero modes of this asymptotic form; it is not "
      "a theorem about every possible zero mode.")
    w("")
    return dict(kappa=kv, normalisable=normalisable, ids=(id1 and id2 and id3), crit=crit, p=pk)


# =====================================================================================
# Stage B (numerics)
# =====================================================================================
def cgrid(L, h):
    N = int(round(2 * L / h)); assert abs(N * h - 2 * L) < 1e-9 and N % 2 == 0, (L, h)
    return -L + h * (np.arange(N) + 0.5)          # cell-centred, even size, symmetric, excludes 0


def vgrid(L, h):
    N = int(round(2 * L / h)); assert abs(N * h - 2 * L) < 1e-9 and N % 2 == 0, (L, h)
    return -L + h * np.arange(1, N)               # Job Six vertex grid, odd size, contains 0


def D4(n, h):
    """4th-order central first derivative, zero ghosts (antisymmetric): Job Six's 4th-order stencil family."""
    return sps.diags([np.full(n - 2, 1.0), np.full(n - 1, -8.0), np.full(n - 1, 8.0), np.full(n - 2, -1.0)],
                     [-2, -1, 1, 2]) / (12 * h)


def T4(n, h):
    """Job Six: −d²/dx², 4th-order 5-point stencil, Dirichlet walls via odd-reflection ghosts."""
    main = np.full(n, 30.0); main[0] = main[-1] = 29.0
    return sps.diags([np.full(n - 2, 1.0), np.full(n - 1, -16.0), main, np.full(n - 1, -16.0), np.full(n - 2, 1.0)],
                     [-2, -1, 0, 1, 2]) / (12 * h * h)


def flip(n):
    return sps.csr_matrix((np.ones(n), (np.arange(n), np.arange(n)[::-1])), shape=(n, n))


def q_pieces(g, h):
    n = g.size; D = D4(n, h); I = sps.identity(n, format="csr")
    return n, sps.kron(D, I).tocsr(), sps.kron(I, D).tocsr(), np.repeat(g, n) * np.tile(g, n), sps.kron(flip(n), I).tocsr()


def Q_full(g, h):
    n, Dx, Dy, XY, Rx = q_pieces(g, h)
    s1 = sps.csr_matrix([[0, 1], [1, 0]], dtype=complex); s2 = sps.csr_matrix([[0, -1j], [1j, 0]]); s3 = sps.csr_matrix([[1, 0], [0, -1]], dtype=complex)
    return (sps.kron(s3, 1j * Dx) + sps.kron(s1, -1j * Dy) + sps.kron(s2, sps.diags(XY))).tocsc()


def M_sector(g, h, s=+1):
    """Q restricted to P = σ₁⊗(x→−x) = s: ψ₂ = s R_x ψ₁, Q → K = i·M, M = Dx − s(Dy + XY)R_x real antisymmetric."""
    n, Dx, Dy, XY, Rx = q_pieces(g, h)
    return (Dx - s * (Dy + sps.diags(XY)) @ Rx).tocsc()


def q_solve(L, h, k=NEIG):
    g = cgrid(L, h); n = g.size
    M = M_sector(g, h, +1); K = (1j * M).tocsc()
    v0 = np.random.default_rng(0).standard_normal(n * n) + 0j
    path = "real LU of M, σ = 0"
    try:
        lu = splu(M)
        def kinv(v):   # (iM)^(-1) v = M^(-1) Im v − i M^(-1) Re v, with a real LU of M
            v = np.asarray(v).ravel()
            return lu.solve(np.ascontiguousarray(v.imag)) - 1j * lu.solve(np.ascontiguousarray(v.real))
        op = LinearOperator(K.shape, dtype=complex, matvec=kinv)
        vals, vecs = eigsh(K, k=k, sigma=0.0, which="LM", OPinv=op, v0=v0)
    except RuntimeError:
        path = "complex LU, σ = 1e-9"
        vals, vecs = eigsh(K, k=k, sigma=1e-9, which="LM", v0=v0)
    vals = np.real(vals); o = np.argsort(vals); vals, vecs = vals[o], vecs[:, o]
    pos, neg = vals[vals > 0], np.sort(-vals[vals < 0])
    m = min(len(pos), len(neg))
    pair = float(np.max(np.abs(pos[:m] - neg[:m]) / pos[:m])) if m else float("nan")
    vp = vecs[:, vals > 0]
    kx = np.fft.fftfreq(n, d=h) * 2 * np.pi
    hi = np.abs(kx) > np.pi / (2 * h)
    X, Y = np.meshgrid(g, g, indexing="ij")
    wall = (np.abs(X) > L - 1) | (np.abs(Y) > L - 1)
    cen = (np.abs(X) <= 2) & (np.abs(Y) <= 2)
    diag = []
    for j in range(vp.shape[1]):
        psi = vp[:, j].reshape(n, n); W = np.abs(psi)**2; W /= W.sum()
        F = np.abs(np.fft.fft2(psi))**2; F /= F.sum()
        diag.append((F[hi, :].sum(), F[:, hi].sum(), W[wall].sum(), W[cen].sum()))
    return pos, diag, pair, n, path


def h6_solve(L, h, k=H6_NLEV):
    g = vgrid(L, h); n = g.size; T = T4(n, h); I = sps.identity(n, format="csr")
    X = np.repeat(g, n); Y = np.tile(g, n)
    Kp = (sps.kron(T, I) + sps.kron(I, T) + sps.diags(X * X * Y * Y + X) + sps.diags(Y) @ sps.kron(flip(n), I)).tocsc()
    v0 = np.random.default_rng(0).standard_normal(n * n)
    ev = np.sort(eigsh(Kp, k=k, sigma=H6_SHIFT, which="LM", v0=v0, return_eigenvectors=False))
    return ev, n


def stage_b0():
    w("## Stage B.0: discretisation identities [identity]")
    w("")
    w(f"Direct discretisation of Q: Q_h = iσ₃D_x − iσ₁D_y + σ₂·xy, with D the 4th-order central first-derivative stencil (Job Six's "
      "4th-order family; zero ghosts, so D is antisymmetric and Q_h is hermitian). In this basis Q_h = i·(real antisymmetric), so its "
      "spectrum is exactly ±-paired and the singular values are |eigenvalues|.")
    g = cgrid(2, 0.25)
    Qf = Q_full(g, 0.25).toarray()
    herm = np.abs(Qf - Qf.conj().T).max()
    ef = np.sort(np.linalg.eigvalsh(Qf))
    Mp, Mm = M_sector(g, 0.25, +1).toarray(), M_sector(g, 0.25, -1).toarray()
    ep, em = np.sort(np.linalg.eigvalsh(1j * Mp)), np.sort(np.linalg.eigvalsh(1j * Mm))
    union = np.sort(np.concatenate([ep, em]))
    d_union = np.abs(ef - union).max(); d_pm = np.abs(ep - em).max(); d_sym = np.abs(ep + ep[::-1]).max()
    anti = max(np.abs(Mp + Mp.T).max(), np.abs(Mm + Mm.T).max())
    gv = vgrid(2, 0.2)
    Mv = M_sector(gv, 0.2, +1).toarray()
    zv = np.abs(np.linalg.eigvalsh(1j * Mv)).min()
    zc = np.abs(ep).min()
    ok = max(herm, d_union, d_pm, d_sym, anti) < ID_TOL
    w(f"- Small grid (cell-centred, L = 2, h = 0.25, n = {g.size}): |Q_h − Q_h†| = {herm:.1e}; parity P = σ₁⊗(x→−x) commutes with Q_h, "
      f"and spec(Q_h) = spec(K₊) ∪ spec(K₋) to {d_union:.1e}; K₊ and K₋ are isospectral to {d_pm:.1e}; ± symmetry to {d_sym:.1e}; "
      f"M antisymmetric to {anti:.1e}.")
    w(f"- Dimension parity: a real antisymmetric matrix of odd size has an exact zero eigenvalue. On Job Six's vertex grid (n odd, "
      f"here n = {gv.size}) the sector has min |λ| = {zv:.1e}, a forced lattice zero mode that is not physics. The cell-centred grid "
      f"(n even, n = {g.size}) has min |λ| = {zc:.3e}. All scans below therefore use cell-centred grids with n even.")
    w(f"Identity checks: {'PASS' if ok else 'FAIL'} (tolerance {ID_TOL:g}).")
    w("- Doublers (fermion doubling): the 4th-order central D also vanishes at k = π/h, with group speed 5/3. Each doubler "
      "copy is again a supersymmetric x²y² model (speeds 1 or 5/3 per axis), so its levels also fall like 1/L. A hard-wall truncation "
      "mixes physical and doubler components on reflection, so the box ladder of Q_h interleaves several 1/L ladders; doubler content "
      "is reported per level (fraction of |ψ̂|² with |k| > π/2h) [identity / finite-size].")
    w("")
    return ok


def trans_mass():
    w("## Stage B.1: transverse lattice mass (how well the zero-point cancellation survives on the grid) [grid-step]")
    w("")
    w(f"1D transverse operator Q₀ = σ₁(−iD_y) + σ₂·xy on cell-centred y ∈ [−{TRANS_LY}, {TRANS_LY}]. Its smallest |eigenvalue| δ(x) "
      "is 0 in the continuum. On the grid it acts as a small positive mass along the valley (it enters H = Q² as +δ²).")
    w("")
    w("| x | " + " | ".join(f"δ (h = {hh:g})" for hh in TRANS_H) + " | ratio (h⁴ scaling expects " + f"{(TRANS_H[0] / TRANS_H[1])**4:g}) |")
    w("|---|" + "---|" * len(TRANS_H) + "---|")
    res = {}
    for xv in TRANS_X:
        ds = []
        for hh in TRANS_H:
            gy = cgrid(TRANS_LY, hh); D = D4(gy.size, hh).toarray()
            s1 = np.array([[0, 1], [1, 0]]); s2 = np.array([[0, -1j], [1j, 0]])
            Q0 = np.kron(s1, -1j * D) + np.kron(s2, np.diag(xv * gy))
            ds.append(np.abs(np.linalg.eigvalsh(Q0)).min())
        res[xv] = ds
        w(f"| {xv:g} | " + " | ".join(f"{d:.3e}" for d in ds) + f" | {ds[0] / ds[1]:.1f} |")
    w("")
    return res


def fits(sv):
    nf = min(N_FIT, min(len(sv[L]) for L in L_LIST))
    lnL = np.log(L_LIST)
    sl = [np.polyfit(lnL, np.log([sv[L][k] for L in L_LIST]), 1)[0] for k in range(nf)]
    loc = [math.log(sv[16][k] / sv[14][k]) / math.log(16 / 14) for k in range(nf)]
    return nf, sl, loc


def cand_rule(sv):
    nf = min(N_FIT, min(len(sv[L]) for L in L_LIST))
    r = [sv[L_B][k] / sv[L_A][k] for k in range(nf)]
    med = float(np.median(r[:N_LAD]))
    ladder = LADDER_WINDOW[0] <= med <= LADDER_WINDOW[1]
    idx = [k + 1 for k in range(nf) if abs(r[k] - 1) < CAND_TOL]
    fl = [sv[L][0] / sv[L][1] for L in L_LIST]
    floor = all(v < ZERO_FLOOR for v in fl)
    return dict(r=r, med=med, ladder=ladder, idx=idx, fl=fl, floor=floor, cand=ladder and (bool(idx) or floor))


def stage_b(tm):
    w("## Stage B.2: direct Q_h scan, singular values against box size (primary)")
    w("")
    w(f"Box [−L, L]², h = {H}, cell-centred grid, sector P = +1 (P = −1 is isospectral, B.0). Shift-invert at 0 for the {NEIG} "
      "eigenvalues nearest zero; singular values σ = positive eigenvalues (each is also matched by −σ). E = σ².")
    w("")
    sv, dg, info = {}, {}, {}
    w("| L | n per axis | sector dim | solver | ± pairing | " + " | ".join(f"σ{k + 1}" for k in range(N_SHOW)) + " |")
    w("|---|---|---|---|---|" + "---|" * N_SHOW)
    for L in L_LIST:
        t = time.time()
        pos, diag, pair, n, path = q_solve(L, H)
        print(f"  Q_h L={L}: {time.time() - t:.1f}s", flush=True)
        sv[L], dg[L], info[L] = pos, diag, (pair, n, path)
        w(f"| {L} | {n} | {n * n} | {path} | {pair:.1e} | " + " | ".join(f"{v:.5f}" for v in pos[:N_SHOW]) + " |")
    w("")
    pair_ok = all(info[L][0] < PAIR_TOL for L in L_LIST)
    w(f"± pairing [identity]: {'PASS' if pair_ok else 'FAIL'} (tolerance {PAIR_TOL:g}).")
    nf, sl, loc = fits(sv)
    w("Fitted exponent d lnσ/d lnL over L = 8…16 [computed] (a 1/L ladder gives −1): " + ", ".join(f"σ{k + 1}: {v:+.3f}" for k, v in enumerate(sl)))
    w("Local exponent between L = 14 and 16 [computed]: " + ", ".join(f"σ{k + 1}: {v:+.3f}" for k, v in enumerate(loc)))
    w(f"Ladder comparison at L = 16 [computed]: σ_k/σ₁ = " + ", ".join(f"{sv[16][k] / sv[16][0]:.3f}" for k in range(nf)) +
      f"; E_k/E₁ = " + ", ".join(f"{(sv[16][k] / sv[16][0])**2:.2f}" for k in range(nf)) +
      f"; ℓ_k = kπ/σ_k = " + ", ".join(f"{(k + 1) * math.pi / sv[16][k]:.2f}" for k in range(nf)) + f" against 2L = {2 * 16}.")
    w("")
    w("Per-level diagnostics at L = 16 [computed]: doubler fraction in x and y (|k| > π/2h), weight within 1 of a wall, weight in |x|, |y| ≤ 2.")
    w("")
    w("| level | σ | doubler-x | doubler-y | wall weight | central weight |")
    w("|---|---|---|---|---|---|")
    for k in range(min(N_SHOW, len(sv[16]))):
        fx, fy, ww, cw = dg[16][k]
        w(f"| σ{k + 1} | {sv[16][k]:.5f} | {fx:.3f} | {fy:.3f} | {ww:.3f} | {cw:.3f} |")
    w("")
    w(f"Central weight of σ₁ against L [computed]: " + ", ".join(f"L={L}: {dg[L][0][3]:.4f}" for L in L_LIST) +
      " (an extended valley state dilutes like 1/L; a bound state would keep a fixed central weight).")
    w(f"Transverse lattice mass at the wall compared with σ₁(L) [grid-step]: " +
      ", ".join(f"x = {xv:g}: δ/σ₁(L = {int(xv)}) = {tm[xv][0] / sv[int(xv)][0]:.2e}" for xv in TRANS_X if int(xv) in sv) + ".")
    w("")
    cr = cand_rule(sv)
    w("**Bound-state criterion (fixed before the run)** applied to Q_h:")
    w(f"- ladder: median of σ_k(16)/σ_k(8) over k ≤ {N_LAD} = {cr['med']:.4f}, window {LADDER_WINDOW} → ladder established: {cr['ladder']}. "
      f"Ratios: " + ", ".join(f"σ{k + 1}: {v:.4f}" for k, v in enumerate(cr["r"])) + ".")
    w(f"- non-falling level (|σ_k(16)/σ_k(8) − 1| < {CAND_TOL:g}): {cr['idx'] if cr['idx'] else 'none'}.")
    w(f"- off-ladder level near zero (σ₁/σ₂ < {ZERO_FLOOR:g} at every L): {cr['floor']}; σ₁/σ₂ = " + ", ".join(f"{v:.3f}" for v in cr["fl"]) + ".")
    w(f"**Stage B candidate (Q_h): {cr['cand']}** [computed].")
    w("")
    # grid check
    t = time.time()
    pos2, _, _, n2, _ = q_solve(GRID_L, GRID_H)
    print(f"  Q_h grid check: {time.time() - t:.1f}s", flush=True)
    m = min(4, len(pos2), len(sv[GRID_L]))
    w(f"Grid check at L = {GRID_L} [grid-step]: h = {H} against h = {GRID_H} (n = {n2}): relative change of σ₁…σ{m} = " +
      ", ".join(f"{abs(pos2[k] - sv[GRID_L][k]) / pos2[k]:.1e}" for k in range(m)) + ".")
    w("")
    return sv, cr


def stage_b_h6():
    w("## Stage B.3: cross-check with Job Six's discretisation of H = Q² (report)")
    w("")
    w(f"Job Six's operator: 4th-order Laplacian with odd-reflection Dirichlet walls, vertex grid, h = {H}, sector K₊, s = 1; "
      "σ = sign(E)·√|E|. This Dirichlet H is not Q_h² (the boundary conditions differ), so the ladders need not coincide; both "
      "should fall like 1/L. Known bias [grid-step, Job Six]: the Laplacian error lowers the transverse zero point by ∝ h⁴|x|³ "
      "near the walls, which grows with L.")
    w("")
    sv = {}
    w("| L | n | " + " | ".join(f"σ{k + 1}" for k in range(H6_NLEV)) + " | min E |")
    w("|---|---|" + "---|" * H6_NLEV + "---|")
    for L in L_LIST:
        t = time.time()
        ev, n = h6_solve(L, H)
        print(f"  H6 L={L}: {time.time() - t:.1f}s", flush=True)
        sv[L] = np.sign(ev) * np.sqrt(np.abs(ev))
        w(f"| {L} | {n} | " + " | ".join(f"{v:.5f}" for v in sv[L]) + f" | {ev[0]:.3e} |")
    w("")
    nf, sl, loc = fits(sv)
    w("Fitted exponent d lnσ/d lnL [computed]: " + ", ".join(f"σ{k + 1}: {v:+.3f}" for k, v in enumerate(sl)))
    w("Local exponent L = 14 → 16 [computed]: " + ", ".join(f"σ{k + 1}: {v:+.3f}" for k, v in enumerate(loc)))
    w("k² ladder at L = 16 [computed]: E_k/E₁ = " + ", ".join(f"{(sv[16][k] / sv[16][0])**2:.3f}" for k in range(nf)) +
      " (k² = " + ", ".join(str((k + 1)**2) for k in range(nf)) + "); ℓ_k = kπ/σ_k = " +
      ", ".join(f"{(k + 1) * math.pi / sv[16][k]:.2f}" for k in range(nf)) + ".")
    cr = cand_rule(sv)
    w(f"Same criterion: ladder median {cr['med']:.4f} → established {cr['ladder']}; non-falling {cr['idx'] if cr['idx'] else 'none'}; "
      f"near-zero off-ladder {cr['floor']} → candidate: {cr['cand']} [computed].")
    w("")
    return sv, cr


def stage_c(A):
    w("## Stage C: comparison with Fröhlich–Graf–Hasler–Hoppe–Yau (2000) [standard]")
    w("")
    have = os.path.exists(FGHHY_PDF)
    hsh = hashlib.sha256(open(FGHHY_PDF, "rb").read()).hexdigest()[:8].upper() if have else "—"
    w(f"PDF {'present and read' if have else 'MISSING (cited only)'}: {FGHHY_PDF} (sha256 {hsh}).")
    w("- **Appendix 2 (pp. 15–16), the model of this job:** H = (−∂x² − ∂y² + x²y²)·1 + [[x, −y], [−y, −x]] (eq. 50), "
      "the square of Q = i[[∂x, ∂y + xy], [∂y − xy, −∂x]]. As x → +∞ the approximate kernel is Ψ₊ = e^(−xy²/2)(0, 1) (eq. 51). "
      "With Ψ = x^(−κ)(Ψ₀ + Ψ₁ + …) (eq. 52), the n = 1 condition gives κ = −1/4, 'which proves that (50) does not admit any "
      "square-integrable solution of the form (52)'. They give the asymptotic expansion Ψ = x^(1/4) e^(−xy²/2) Σ x^(−3n/2)(y/(4x) f_n, g_n).")
    w("- **Main theorem (p. 4), the SU(2) matrix models in d = 2, 3, 5, 9:** ψ = r^(−κ)Σ r^(−3k/2)ψ_k, square-integrable at infinity "
      "iff κ > 3/2 (Remark 2, measure r²dr). Results: d = 9 a unique solution with κ = 6 (normalisable); d = 5 κ = −1 (three) and κ = 3 "
      "(one, odd under the antipode map, so excluded); d = 3 κ = 0 (two); d = 2 none. Their reading: only d = 9 has a normalisable ground state.")
    w("- The κ there has the same origin as here. In their eq. (45)/(κ formula), κ = 1 + κ′ − ½(d − 1): the −½(d − 1) is the "
      "transverse-oscillator term, the analogue of our −1/4 from one transverse direction.")
    kmatch = A["kappa"] == FGHHY_KAPPA
    nmatch = A["normalisable"] == FGHHY_NORMALISABLE
    w(f"Our model is theirs after y → −y (Stage A identity: {A['ids']}). Our κ = {A['kappa']} against FGHHY κ = {FGHHY_KAPPA}: match {kmatch}; "
      f"normalisable {A['normalisable']} against FGHHY {FGHHY_NORMALISABLE}: match {nmatch}.")
    w("")
    return have and kmatch and nmatch and A["ids"], have


def main():
    now = datetime.datetime.now().astimezone(); z = now.strftime("%z")
    w("# RESULTS: Job 6b, zero-energy bound state of the supersymmetric x²y² toy H = Q² (generated by run.py; do not edit)")
    w("")
    w(f"Generated {now.strftime('%Y-%m-%d %H:%M:%S')} local (UTC{z[:3]}:{z[3:]}). Python {platform.python_version()}, numpy {np.__version__}, "
      f"scipy {scipy.__version__}, sympy {sp.__version__}.")
    w("Tags: [identity] [computed] [assumed input] [prediction] [standard] [standard: beyond toy] [grid-step] [finite-size] "
      "[hive-interpretation] [post-hoc]. Verdict rules fixed in run.py before the first run.")
    w("")
    A = stage_a()
    okb0 = stage_b0()
    tm = trans_mass()
    svq, crq = stage_b(tm)
    svh, crh = stage_b_h6()
    fg_ok, have = stage_c(A)
    w("## Verdict (rules fixed before the run)")
    w("")
    w("Rules: 'Bound state found' needs Stage A normalisable AND a Stage B candidate. 'No bound state' [standard: beyond toy] needs "
      "Stage A non-normalisable, no Stage B candidate on an established ladder, both discretisations agreeing, and agreement with FGHHY. "
      "Anything else is 'inconclusive', with the reasons named.")
    reasons = []
    if not okb0: reasons.append("Stage B.0 identity checks failed")
    if not crq["ladder"]: reasons.append("Q_h ladder not established")
    if crq["cand"] != crh["cand"]: reasons.append("the Q_h and Job Six discretisations disagree on a candidate")
    if not fg_ok: reasons.append("FGHHY comparison missing or not matching")
    if A["normalisable"] != crq["cand"]: reasons.append("Stage A and Stage B disagree")
    w(f"- Stage A: γ = κ = {A['kappa']}; asymptotic zero mode normalisable: {A['normalisable']} [computed, leading order].")
    w(f"- Stage B: candidate (Q_h) {crq['cand']}; ladder established {crq['ladder']}; Job Six cross-check candidate {crh['cand']} [computed].")
    w(f"- Stage C: FGHHY consistent: {fg_ok} [standard].")
    if A["normalisable"] and crq["cand"] and not reasons:
        verdict = "Bound state found"
    elif (not A["normalisable"]) and (not crq["cand"]) and not reasons:
        verdict = "No bound state [standard: beyond toy]"
    else:
        verdict = "Inconclusive: " + "; ".join(reasons if reasons else ["criteria not met"])
    w("")
    w(f"**VERDICT: {verdict}.**")
    w("")
    w("Scope: a finite box cannot exclude an eigenvalue embedded inside the continuum (E > 0) with no avoided crossing, nor a zero "
      "mode not of the asymptotic power-series form. The statement is about the threshold E = 0 and the FGHHY asymptotic form.")
    w("")
    w(f"Runtime: {time.time() - T0:.0f} s [computed].")
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
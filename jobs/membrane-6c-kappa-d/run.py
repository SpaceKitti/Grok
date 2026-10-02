#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job 6c: the valley balance of Job 6b redone for the SU(2) matrix models in d = 2, 3, 5, 9.
Derives the decay exponent κ(d) of the asymptotic zero-energy solution, the normalisability bar per d,
and compares with Fröhlich–Graf–Hasler–Hoppe–Yau, Nucl. Phys. B 567 (2000) 231, hep-th/9904182 (FGHHY).
No grids: sympy for the symbolic parts, exact-integer Clifford matrices (numpy) for the fermion algebra.
Writes RESULTS.md only (never hand-edited). Every number in RESULTS.md is printed from a variable.
"""
import os, time, math, hashlib, datetime, platform
import numpy as np
import scipy
import scipy.sparse as sps
from scipy.linalg import expm
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
FGHHY_PDF = r"C:\Users\Akitt\open-problems\03_membrane_renormalization\NPB567_231_Frohlich_Graf_Hasler_Hoppe_Yau_zero_energy_asymptotics.pdf"
T0 = time.time()
OUT = []


def w(line=""):
    print(line, flush=True)
    OUT.append(line)


# =====================================================================================
# Rules and literature inputs: FIXED BEFORE THE FIRST RUN
# =====================================================================================
D_LIST = [2, 3, 5, 9]
ID_TOL = 1e-9          # identity checks (Clifford algebra, commutators, projector checks)
NULL_TOL = 1e-8        # null-space threshold
RAT_TOL = 1e-9         # computed κ′ must be this close to a rational with small denominator
# [standard] FGHHY Theorem (p. 4), §4.2 eqs. (28)–(32), §4.6:
FGHHY_KAPPA = {2: [], 3: [0, 0], 5: [-1, -1, -1, 3], 9: [6]}
FGHHY_REP = {3: [1, 1], 5: [1, 1, 1, 5], 9: [44]}
FGHHY_SIGMA = {3: [1, 1], 5: [1, 1, 1, -1], 9: [1]}       # eq. (32)
FGHHY_THETA = {3: [-1, -1], 5: [1, 1, 1, 1], 9: [1]}      # eq. (31) (convention-dependent sign; reported, not graded)
# [standard] Witten index of the SU(2) model, the final yes/no on a bound state (separate column):
WITTEN = {
    9: (1, "Kac–Smilga hep-th/9908096 eq. (1.25) [standard]; Yi hep-th/9704098 for the bulk term 5/4 only"),
    5: (0, "Kac–Smilga hep-th/9908096 eq. (1.25) [standard]; Yi hep-th/9704098 for the bulk term 1/4 only"),
    3: (0, "Kac–Smilga hep-th/9908096 eq. (1.25) [standard]; Yi hep-th/9704098 for the bulk term 1/4 only"),
    2: (0, "[standard: Fröhlich–Hoppe CMP 191 (1998) 613, hep-th/9701119; 'simplest model' = SU(2), d = 2 per FGHHY §3]; Yi's bulk term is 0"),
}
DIMS_SOURCE = "Moore–Nekrasov–Shatashvili hep-th/9803265 (reductions of D = 3, 4, 6, 10 SYM)"
# Grading (Helios/Venus 6c update):
#  PASS iff the computed κ(d) agree with FGHHY at d = 2, 3, 5, 9 (d = 2: no invariant solution).
#  Per solution: κ > bar and even under the antipode map -> "normalisable; existence from the index";
#                κ > bar but odd -> "not a ground state" (odd [computed: σ; other two factors standard: FGHHY §4.3]) (fold-in relabel);
#                κ ≤ bar -> "not normalisable".
#  The bound-state yes/no comes only from the Witten index column.

TRIPLES = [(1, 2, 3), (1, 4, 5), (1, 7, 6), (2, 4, 6), (2, 5, 7), (3, 4, 7), (3, 6, 5)]   # octonion Fano triples


def s_of(d):
    k = d // 2
    return 2**k if d % 8 in (0, 1, 2) else 2**(k + 1)


def left_mult(nim):
    """Left multiplications by the imaginary units of C (nim = 1), H (3) or O (7): real antisymmetric, L² = −1."""
    n = nim + 1
    table = {}
    for (a, b, c) in TRIPLES:
        if max(a, b, c) <= nim:
            for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
                table[(x, y)] = (1, z); table[(y, x)] = (-1, z)
    Ls = []
    for a in range(1, n):
        L = np.zeros((n, n)); L[a, 0] = 1; L[0, a] = -1
        for b in range(1, n):
            if b != a:
                sg, cc = table[(a, b)]; L[cc, b] = sg
        Ls.append(L)
    return Ls


def gammas(d):
    """Real symmetric s_d × s_d gamma matrices in FGHHY's form (27): γ^d = diag(1, −1), γ^{d−1} = [[0,1],[1,0]],
    γ^j = [[0, iΓ_j], [−iΓ_j, 0]], with iΓ_j = A_j real antisymmetric (left multiplications)."""
    s = s_of(d); h = s // 2
    A = left_mult(h - 1)[: d - 2] if h > 1 else []
    I = np.eye(h); Z = np.zeros((h, h))
    g = [np.block([[Z, a], [-a, Z]]) for a in A]
    g.append(np.block([[Z, I], [I, Z]])); g.append(np.block([[I, Z], [Z, -I]]))
    return g


def majoranas(nm):
    X = sps.csr_matrix([[0, 1], [1, 0]], dtype=complex); Y = sps.csr_matrix([[0, -1j], [1j, 0]])
    Zp = sps.csr_matrix([[1, 0], [0, -1]], dtype=complex); I = sps.identity(2, dtype=complex, format="csr")
    out = []
    for j in range(nm):
        for P in (X, Y):
            ops = [Zp] * j + [P] + [I] * (nm - j - 1)
            m = ops[0]
            for o in ops[1:]:
                m = sps.kron(m, o, format="csr")
            out.append((m / np.sqrt(2)).tocsr())
    return out


def rat(xv):
    q = sp.nsimplify(float(xv), rational=True, tolerance=1e-12)
    q = sp.Rational(q).limit_denominator(64)
    return q, abs(float(q) - float(xv))


# =====================================================================================
# Stage A: measure and the normalisability bar per d (sympy)
# =====================================================================================
def stage_a():
    w("## Stage A: the normalisability bar per d, and the two conventions for κ (sympy)")
    w("")
    d, kap, r, y = sp.symbols("d kappa r y", positive=True)
    # FGHHY tubular coordinates q_s = r e E_s + r^(-1/2) y_s: e ∈ S² (SU(2) orbit of radius r), E ∈ S^(d−1) (radius r),
    # 2(d−1) transverse y's rescaled by r^(−1/2).
    orbit, Esph, ntr = 2, d - 1, 2 * (d - 1)
    m = sp.simplify(orbit * 1 + Esph * 1 + ntr * sp.Rational(-1, 2))
    barF = sp.solve(sp.Eq(m - 2 * kap, -1), kap)[0]
    g1 = sp.integrate(sp.exp(-r * y**2), (y, -sp.oo, sp.oo))
    w("FGHHY write ψ = r^(−κ)Σ r^(−3k/2) ψ_k(e, E, y) with ψ_k square-integrable in de dE dy (Remark 2).")
    w(f"- Measure: dq = dr · r^{orbit} de (SU(2) orbit S², radius r) · r^({Esph}) dE (S^(d−1), radius r) · r^(−({sp.factor(ntr / 2)})) dy "
      f"(transverse, width r^(−1/2)) = r^({m}) dr de dE dy [computed]. So ∫^∞ r^({m} − 2κ) dr < ∞ iff **κ > {barF}, for every d**.")
    w(f"- Does FGHHY's κ include the measure and transverse factors? **Yes.** ψ is the full wave function on R^(3d). Its transverse "
      f"Gaussian is written in rescaled y, so it carries no r-dependent normalisation (∫e^(−r y_phys²)dy_phys = {g1} per direction, "
      f"which gives r^(−(d−1)) over 2(d−1) directions). The r² of the gauge orbit sits in the measure. That is why their bar is 3/2.")
    keff = kap - 1 + (d - 1) / 2
    barE = d / 2
    equiv = sp.simplify(sp.solve(sp.Eq(keff, barE), kap)[0] - barF) == 0
    w(f"- Venus's convention: the effective (Born–Oppenheimer) wave function χ on the d flat directions (R^d, measure r^(d−1)dr), "
      f"with the transverse ground state normalised and the orbit volume absorbed, decays as r^(−κ_eff) with κ_eff = κ − 1 + (d−1)/2 = {keff}. "
      f"Its bar is κ_eff > d/2, and κ_eff = d/2 ⟺ κ = {sp.solve(sp.Eq(keff, barE), kap)[0]} for all d: equivalent to FGHHY's bar: {equiv} [identity].")
    w("- Reconciliation: the two bars are the same condition in two conventions. Applying d/2 to FGHHY's κ directly would be wrong, "
      "because their κ already contains the orbit (+1) and transverse (−(d−1)/2) factors. These are exactly the d-independent "
      "and transverse terms of their κ formula (§4.6), so κ_eff = κ′ (their fermionic term).")
    w("- 6b toy as a check [standard: Job 6b]: there is no gauge orbit, and the flat direction is one line with one transverse direction. "
      "So κ_eff = κ + 1/4, the bar is κ_eff > 1/2 ⟺ κ > 1/4, and 6b's κ = −1/4 gives κ_eff = 0 (the k = 0 threshold state).")
    w("")
    G = sp.exp(-y**2 / 2)
    t3 = sp.simplify(sp.integrate(G * sp.Rational(1, 2) * y * sp.diff(G, y), (y, -sp.oo, sp.oo)) / sp.integrate(G**2, (y, -sp.oo, sp.oo)))
    w(f"Transverse-oscillator term of κ (FGHHY eq. 45): P₀(½y·∂_y)ψ₀ = {t3}·ψ₀ per transverse direction [computed], times 2(d−1) "
      f"directions = {sp.simplify(t3 * ntr)}. This is the same −1/4 per direction as in 6b.")
    w("")
    rows = {dv: dict(bar=barF, barE=sp.Rational(dv, 2), keff=lambda k, dv=dv: k - 1 + sp.Rational(dv - 1, 2), t3=t3 * 2 * (dv - 1)) for dv in D_LIST}
    return rows, t3


# =====================================================================================
# Stage B: the fermionic term κ′(d) from the explicit Clifford module (FGHHY §4.2, §4.6)
# =====================================================================================
def clifford_checks(d):
    s = s_of(d); g = gammas(d)
    e1 = max(np.abs(g[i] @ g[j] + g[j] @ g[i] - 2 * (i == j) * np.eye(s)).max() for i in range(d) for j in range(d))
    e2 = max(np.abs(gi - gi.T).max() for gi in g)
    return s, g, max(e1, e2)


def module(d):
    s, g, eg = clifford_checks(d)
    psi = [m.toarray() for m in majoranas(s // 2)]
    n = psi[0].shape[0]
    eps = max(np.abs(psi[a] @ psi[b] + psi[b] @ psi[a] - (a == b) * np.eye(n)).max() for a in range(s) for b in range(s))
    M = [[None] * d for _ in range(d)]
    for i in range(d):
        for j in range(d):
            gst = 0.5 * (g[i] @ g[j] - g[j] @ g[i])
            M[i][j] = -0.25j * sum(gst[a, b] * psi[a] @ psi[b] for a in range(s) for b in range(s) if gst[a, b] != 0) if i != j else np.zeros((n, n), complex)
    # i[ψ_α, M_ut] = ½ γ^{ut}_{αβ} ψ_β
    ecom = 0.0
    for (u, t) in [(0, d - 1), (d - 2, d - 1)] + ([(0, 1)] if d > 2 else []):
        gst = 0.5 * (g[u] @ g[t] - g[t] @ g[u])
        for a in range(s):
            lhs = 1j * (psi[a] @ M[u][t] - M[u][t] @ psi[a]); rhs = 0.5 * sum(gst[a, b] * psi[b] for b in range(s))
            ecom = max(ecom, np.abs(lhs - rhs).max())
    C = sum(M[i][j] @ M[i][j] for i in range(d) for j in range(i + 1, d))
    Th = (2**(s // 2)) * np.linalg.multi_dot(psi) if s > 1 else None
    return dict(s=s, g=g, psi=psi, M=M, C=C, Th=Th, n=n, err=max(eg, eps, ecom))


def singlets(mod, d):
    M, n = mod["M"], mod["n"]
    gens = [M[i][j] for i in range(d - 1) for j in range(i + 1, d - 1)]
    B = np.vstack(gens) if gens else np.zeros((1, n))
    _, S, Vh = np.linalg.svd(B)
    Sfull = np.concatenate([S, np.zeros(n - len(S))]) if len(S) < n else S
    N = Vh[Sfull < NULL_TOL].conj().T
    Cs = N.conj().T @ mod["C"] @ N
    ev, V = np.linalg.eigh((Cs + Cs.conj().T) / 2)
    return [(ev[k], N @ V[:, k]) for k in range(len(ev))]


def rep_dim(mod, d, F):
    M = mod["M"]; gens = [M[i][j] for i in range(d) for j in range(i + 1, d)]
    V = F.reshape(-1, 1); rank = 1
    while True:
        W = np.hstack([V] + [G @ V for G in gens])
        U, S, _ = np.linalg.svd(W, full_matrices=False)
        nr = int((S > 1e-8 * S[0]).sum())
        V = U[:, :nr]
        if nr == rank:
            return nr
        rank = nr


def kappa_prime(mod, d, F):
    s, g, psi, M = mod["s"], mod["g"], mod["psi"], mod["M"]
    E = d - 1
    L = np.concatenate([-sum(g[t][a, b] * (psi[a] @ (M[E][t] @ F)) for a in range(s) for t in range(d) if t != E and g[t][a, b] != 0) for b in range(s)])
    R = np.concatenate([-1j * sum(g[E][a, b] * (psi[a] @ F) for a in range(s) if g[E][a, b] != 0) for b in range(s)])
    kp = np.vdot(R, L) / np.vdot(R, R)
    res = np.linalg.norm(L - kp * R) / max(np.linalg.norm(L), 1e-300) if np.linalg.norm(L) > 1e-12 else 0.0
    return kp, res


def term_i(d):
    """FGHHY eq. (39) on the full fermion space C^⊗3 (3·s_d Majoranas): P₀Θ_{αA}e_B M_{BA}F = i(Θ_α·e)F for every F in (18)."""
    s = s_of(d)
    th = majoranas(3 * s // 2)
    Th = lambda a, A: th[A * s + a]
    npl = np.array([1, 1j, 0]) / np.sqrt(2); nmi = np.array([1, -1j, 0]) / np.sqrt(2)
    ann = [sum(npl[A] * Th(a, A) for A in range(2)) for a in range(s // 2)] + [sum(nmi[A] * Th(a, A) for A in range(2)) for a in range(s // 2, s)]
    dim = th[0].shape[0]
    X = np.random.default_rng(0).standard_normal((dim, 2**(s // 2) + 6)) + 0j
    for c in ann:                      # apply the commuting projectors (1 − c†c) one at a time
        X = X - c.conj().T @ (c @ X)
    U, S, _ = np.linalg.svd(X, full_matrices=False)
    K = U[:, S > 1e-8 * S[0]]
    Mc = lambda B, A: -0.5j * sum(Th(b, B) @ Th(b, A) - Th(b, A) @ Th(b, B) for b in range(s))
    res, inv, u1 = 0.0, 0.0, 0.0
    M3 = [Mc(2, A) for A in range(3)]
    for a in range(s):
        op = sum(Th(a, A) @ M3[A] for A in range(3))
        lhs = K @ (K.conj().T @ (op @ K)); rhs = 1j * (Th(a, 2) @ K)
        res = max(res, np.abs(lhs - rhs).max())
        v = Th(a, 2) @ K; inv = max(inv, np.abs(v - K @ (K.conj().T @ v)).max())
    u1 = np.abs(Mc(0, 1) @ K).max()
    return K.shape[1], dim, res, inv, u1


def d2_check():
    s = 2; g = gammas(2)
    th = [m.toarray() for m in majoranas(3)]
    gst = 0.5 * (g[0] @ g[1] - g[1] @ g[0])
    M12 = -0.25j * sum(gst[a, b] * th[A * s + a] @ th[A * s + b] for A in range(3) for a in range(s) for b in range(s) if gst[a, b] != 0)
    ev = np.sort(np.linalg.eigvalsh((M12 + M12.conj().T) / 2))
    evr = [rat(v)[0] for v in ev]
    nonint = all(sp.Rational(v).q != 1 for v in evr)
    return evr, nonint


def stage_b(A_rows, t3):
    w("## Stage B: κ(d) = 1 + κ′ − (d − 1)/2 from the explicit fermion algebra")
    w("")
    sl = {dv: s_of(dv) for dv in range(1, 11)}
    allowed = [dv for dv in range(2, 11) if sl[dv] == 2 * (dv - 1)]
    w(f"Allowed dimensions [computed]: s_d = 2(d − 1) holds for d ∈ {allowed} among d = 2…10 (s_d = " +
      ", ".join(f"{dv}: {sl[dv]}" for dv in range(2, 11)) + f") [standard: list as in {DIMS_SOURCE}].")
    w("Method: γ-matrices in FGHHY's form (27), built from left multiplications by the imaginary units of C, H, O. Θ_α·e acts as "
      "s_d Majoranas on the 2^(s_d/2)-dimensional module C. M_st = −(i/4)Θγ^{st}Θ, C = Σ M_st². Invariant states are the "
      "Spin(d−1) singlets (E = e_d). κ′ is read off directly from FGHHY eq. (40) and cross-checked against 8C/s_d (§4.6).")
    w("")
    res = {}
    for dv in [3, 5, 9]:
        t = time.time()
        mod = module(dv)
        sing = singlets(mod, dv)
        out = []
        for (cval, F) in sing:
            F = F / np.linalg.norm(F)
            kp, rres = kappa_prime(mod, dv, F)
            rd = rep_dim(mod, dv, F)
            Rop = expm(1j * np.pi * mod["M"][dv - 1][dv - 2])
            sig = np.vdot(F, Rop @ F); sres = np.linalg.norm(Rop @ F - sig * F)
            th = np.vdot(F, mod["Th"] @ F)
            kq, kerr = rat(kp.real)
            Cq, _ = rat(cval)
            lval = (-(dv - 2) + math.sqrt((dv - 2)**2 + 4 * float(cval))) / 2
            kappa = 1 + kq - sp.Rational(dv - 1, 2)
            out.append(dict(C=Cq, rep=rd, kp=kq, kperr=kerr, kpim=abs(kp.imag), rres=rres, casim=sp.Rational(8) * Cq / mod["s"],
                            sig=sig.real, sres=sres, th=th.real, l=lval, kappa=kappa))
        res[dv] = (mod, out)
        print(f"  d={dv}: {time.time() - t:.1f}s", flush=True)
    w("| d | s_d | dim C | identity err | singlet | Spin(d) rep (dim) | Casimir C | κ′ from eq. (40) | eq. (40) residual | 8C/s_d | κ = 1 + κ′ − (d−1)/2 | σ (eq. 32) | Θ (eq. 31) |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for dv in [3, 5, 9]:
        mod, out = res[dv]
        for k, o in enumerate(out):
            w(f"| {dv} | {mod['s']} | {mod['n']} | {mod['err']:.1e} | {k + 1} | {o['rep']} | {o['C']} | {o['kp']} (±{o['kperr']:.0e}) | "
              f"{o['rres']:.1e} | {o['casim']} | {o['kappa']} | {o['sig']:+.6f} | {o['th']:+.6f} |")
    w("")
    w("Term (i) of κ, the '+1' (FGHHY eq. 39), checked on the full fermion space C^⊗3 for d = 3 and 5 [computed]. For d = 9 "
      "(2^24 states) it is taken as [standard]; the identity is pure colour algebra and the same for every d:")
    ti = {}
    for dv in [3, 5]:
        t = time.time()
        k, dim, r1, inv, u1 = term_i(dv)
        ti[dv] = max(r1, inv, u1)
        print(f"  term (i) d={dv}: {time.time() - t:.1f}s", flush=True)
        w(f"- d = {dv}: dim C^⊗3 = {dim}; states (18): {k} (= 2^(s_d/2) = {2**(s_of(dv) // 2)}); max |P₀Θ_{{αA}}e_BM_{{BA}}F − i(Θ_α·e)F| = {r1:.1e}; "
          f"Θ·e leaves the space invariant to {inv:.1e}; colour U(1) generator (22) annihilates it to {u1:.1e}.")
    evr, nonint = d2_check()
    w(f"- d = 2: on C^⊗3 (8 states), M₁₂ has eigenvalues {evr} [computed]. None is an integer: {nonint}. Since L₁₂ has integer "
      "spectrum, J₁₂ = L₁₂ + M₁₂ never vanishes, so there is **no Spin(2)-invariant state at all** [standard: Fröhlich–Hoppe CMP 191 (1998) 613, hep-th/9701119; 'simplest model' = SU(2), d = 2 per FGHHY §3].")
    w("")
    ids_ok = all(res[dv][0]["err"] < ID_TOL for dv in res) and all(ti[dv] < ID_TOL for dv in ti) and nonint
    eq40_ok = all(o["rres"] < ID_TOL and o["kperr"] < RAT_TOL and o["kpim"] < ID_TOL and o["kp"] == o["casim"] for dv in res for o in res[dv][1])
    w(f"Identity checks (Clifford algebra, i[Θ, M] = ½γΘ, eq. 39, d = 2 spectrum): {'PASS' if ids_ok else 'FAIL'}; "
      f"eq. (40) exact and equal to 8C/s_d for every singlet: {'PASS' if eq40_ok else 'FAIL'} (tolerance {ID_TOL:g}).")
    w("")
    return res, ids_ok and eq40_ok, evr


def stage_c(A_rows, res):
    w("## Stage C: κ(d) against FGHHY, the bar, and the Witten index")
    w("")
    w("Fröhlich–Graf–Hasler–Hoppe–Yau, Nucl. Phys. B 567 (2000) 231, hep-th/9904182 (FGHHY) [standard], read from Orion's PDF " +
      (f"(sha256 {hashlib.sha256(open(FGHHY_PDF, 'rb').read()).hexdigest()[:8].upper()})." if os.path.exists(FGHHY_PDF) else "(PDF missing: cited only)."))
    w("")
    w("| d | D = d+1 | κ computed | κ FGHHY | match | reps computed / FGHHY | σ computed / FGHHY | bar on κ | κ_eff = κ′ (bar d/2) | asymptotic status | Witten index | bound state (from index) | index source |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    allmatch, lines, consist = True, [], True
    for dv in D_LIST:
        bar = A_rows[dv]["bar"]
        idx, src = WITTEN[dv]
        if dv == 2:
            kc, reps, sig, keff, status = [], [], [], [], ["no invariant asymptotic solution [standard: Fröhlich–Hoppe CMP 191 (1998) 613, hep-th/9701119; 'simplest model' = SU(2), d = 2 per FGHHY §3]"]
        else:
            out = res[dv][1]
            kc = [o["kappa"] for o in out]; reps = [o["rep"] for o in out]; sig = [int(round(o["sig"])) for o in out]
            keff = [A_rows[dv]["keff"](o["kappa"]) for o in out]
            status = []
            n_clear = sum(1 for o in out if o["kappa"] > bar)
            for o, sg in zip(out, sig):
                if o["kappa"] > bar and sg == 1:
                    status.append(f"κ = {o['kappa']}: normalisable; existence from the index")
                elif o["kappa"] > bar:
                    status.append(f"κ = {o['kappa']}: {'the only state' if n_clear == 1 else 'a state'} clearing the bar is odd under the antipode map, so not a ground state (odd [computed: σ; other two factors standard: FGHHY §4.3])")
                else:
                    status.append(f"κ = {o['kappa']}: not normalisable")
        match = sorted(kc) == sorted(sp.Integer(v) for v in FGHHY_KAPPA[dv])
        rmatch = dv == 2 or sorted(reps) == sorted(FGHHY_REP[dv])
        smatch = dv == 2 or sorted(sig) == sorted(FGHHY_SIGMA[dv])
        allmatch &= match and rmatch and smatch
        n_even_norm = sum(1 for st in status if "existence from the index" in st)
        consist &= (idx >= 1) == (n_even_norm >= 1)
        w(f"| {dv} | {dv + 1} | {sorted(kc)} | {sorted(FGHHY_KAPPA[dv])} | {match} | {sorted(reps)} / {sorted(FGHHY_REP.get(dv, []))} | "
          f"{sorted(sig)} / {sorted(FGHHY_SIGMA.get(dv, []))} | κ > {bar} | {sorted(keff)} (> {A_rows[dv]['barE']}) | {'; '.join(status)} | {idx} | "
          f"{'yes' if idx >= 1 else 'no'} | {src} |")
        lines.append((dv, status, idx))
    w("")
    w("Notes:")
    w("- σ is the factor e^(iπM‖) of FGHHY eq. (32), computed on C. The other two antipode factors (§4.3) are +1 by FGHHY's computation "
      "using eq. (31) [standard]. So the parity of each solution is σ.")
    w("- Θ (eq. 31) is reported in the Stage B table but not graded: its sign depends on the orientation of the γ-matrix basis "
      "(FGHHY: a det = −1 change inverts the branching).")
    w("- κ_eff = κ′ = 8C/s_d is the decay of the effective wave function on R^d. Writing C = l(l + d − 2) for a rank-l symmetric "
      "traceless rep, the singlets give κ_eff = 0 (l = 0, the constant harmonic), and the 5 (d = 5, l = 1) and 44 (d = 9, l = 2) give "
      "κ_eff = d − 2 + l, the decaying harmonic r^(−(d−2+l)) [hive-interpretation].")
    w("- Witten index: the main source is Kac–Smilga hep-th/9908096 eq. (1.25), I_W = 0, 0, 1 for d = 3, 5, 9, built from the principal "
      "term (eq. 1.22) and the deficit (eq. 4.14) [standard]. Yi hep-th/9704098 is cited for the bulk terms 5/4, 1/4, 1/4 only. Yi's "
      "−1/4 defect is conditional: he motivates it but does not derive it (he calls it an outstanding problem).")
    w("- d = 2 [standard: Fröhlich–Hoppe CMP 191 (1998) 613, hep-th/9701119; 'simplest model' = SU(2), d = 2 per FGHHY §3]: no SU(2)-invariant ground state, in line with the non-integer M₁₂ spectrum computed in Stage B.")
    w("")
    return allmatch, consist, lines


def main():
    now = datetime.datetime.now().astimezone(); z = now.strftime("%z")
    w("# RESULTS: Job 6c, κ(d) for the SU(2) matrix models in d = 2, 3, 5, 9 (generated by run.py; do not edit)")
    w("")
    w(f"Generated {now.strftime('%Y-%m-%d %H:%M:%S')} local (UTC{z[:3]}:{z[3:]}). Python {platform.python_version()}, numpy {np.__version__}, "
      f"scipy {scipy.__version__}, sympy {sp.__version__}. No grids.")
    w("Tags: [identity] [computed] [standard] [standard: beyond toy] [hive-interpretation] [assumed input] [post-hoc]. Rules fixed in run.py before the first run.")
    w("Fold-in pass [post-hoc]: run.py rerun once to relabel d = 5 (not a ground state), bracket the transverse exponent, make "
      "Kac–Smilga eq. (1.25) the main index source and tag d = 2. Tolerances, reference values and computations are unchanged.")
    w("")
    A_rows, t3 = stage_a()
    res, b_ok, evr = stage_b(A_rows, t3)
    allmatch, consist, lines = stage_c(A_rows, res)
    w("## Grade (rules fixed before the run)")
    w("")
    g = "PASS" if (allmatch and b_ok) else "FAIL"
    w(f"- κ(d) matches FGHHY at d = 2, 3, 5, 9 (with reps and parities), and the identity checks pass: **{g}** [computed].")
    for dv, status, idx in lines:
        w(f"- d = {dv}: " + "; ".join(status) + f". Witten index {idx} → bound state: {'yes' if idx >= 1 else 'no'} [standard].")
    w(f"- Asymptotics consistent with the index (index ≥ 1 exactly where an even normalisable solution exists): {consist}.")
    w(f"- d = 5: the state clearing the bar is odd under the antipode map, so not a ground state (odd [computed: σ; other two factors "
      f"standard: FGHHY §4.3]); the Witten index ({WITTEN[5][0]}) agrees [standard].")
    w(f"- d = 9: the even solution that clears the bar is labelled 'normalisable; existence from the index', not 'bound state'. FGHHY fix "
      f"only the behaviour far along the valley; only the Witten index (= {WITTEN[9][0]}) settles that a bound state exists [standard: beyond toy].")
    w("")
    w(f"Runtime: {time.time() - T0:.1f} s [computed].")
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
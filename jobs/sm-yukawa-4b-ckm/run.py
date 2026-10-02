#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job 4b: CKM mixing from an aligned soft brane plus a narrow tilted brane on the round sphere (alpha = 1).
Builds on Job Four (C:\\Users\\Akitt\\sm-rugby-yukawa, main 3b2e06a), which is neither imported nor modified.
Writes RESULTS.md only (never hand-edited). Every number in RESULTS.md is printed from a variable.
Run:  $env:PYTHONIOENCODING='utf-8';  python -B run.py
"""
import os, re, sys, time, math, hashlib, datetime, platform
import numpy as np
import scipy
from scipy.special import gammainc
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET_FILE = r"C:\Users\Akitt\open-problems\JOB4B_TARGETS.md"
T0 = time.time()
OUT = []


def w(line=""):
    print(line, flush=True)
    OUT.append(line)


# =====================================================================================
# Inputs and PASS thresholds: FIXED BEFORE THE FIRST RUN (do not tune afterwards)
# =====================================================================================
TH_A1 = 1e-10                                   # A1: max ||V| - |d1(beta)||, and Y = D diag(t) D^T (relative)
A1_BETAS = [0.1, 0.3, 0.64, 1.2]
A1_CASES = [(0.1, 0.03, "soft"), (0.01, 0.3, "soft"), (0.05, 0.2, "tophat")]   # (sigma_u, sigma_d, profile)
A2_EPS = [1e-3, 3e-3]                           # lopsided dipole strength [assumed input]
A2_SIG = [1e-2, 3e-3, 1e-3, 3e-4]
TH_A2_SLOPE, TH_A2_LO = 0.02, 0.03
CP = dict(sd=0.00935, eps=0.06, beta=0.64)      # check point (spec) [assumed input]
CP_EXPECT = dict(helios12=0.134, exact12=0.084) # spec expectations [prediction]
TH_CP = 0.05                                    # Venus's corrected LO forms within 5% of the exact SVD
R3_POINTS = [(0.00935, 0.06, 0.64), (0.00935, 0.02, 0.30), (0.005, 0.05, 0.40),
             (0.02, 0.10, 0.50), (0.00935, 0.06, 0.25), (0.01, 0.03, 0.80)]   # (sigma_d, eps, beta), rank-1 form
TH_R3 = 0.10                                    # relation 3 within 10% of the exact SVD at every point
VENUS_R3, VENUS_R3_TOL = 0.036, 0.07            # spec expectations [prediction]
VENUS_MDMS, VENUS_MDMS_EPS = 0.009, 0.018       # spec expectations [prediction]
ST_ROW, ST_BETAS, ST_FIX = [0.001, 0.01, 0.03], [0.28, 0.64], dict(sd=0.00935, eps=0.06)
ST_FIT1 = 0.01                                  # fit 1: sigma_t fixed
FACTOR = 2.0                                    # grade: PASS if every target within a factor of 2
LB = dict(sig=1e-6, sig_hi=0.5, eps=1e-4, eps_hi=10.0, beta=1e-3, beta_hi=3.0)   # fit bounds [assumed input]
NG, NPSI = 300, 64                              # quadrature: Gauss-Legendre in the brane angle, uniform in psi
KEYS = ["Vus", "Vcb", "Vub", "mu/mc", "mc/mt", "md/ms", "ms/mb"]
LABEL = {"Vus": "|V_us|", "Vcb": "|V_cb|", "Vub": "|V_ub|", "mu/mc": "m_u/m_c", "mc/mt": "m_c/m_t",
         "md/ms": "m_d/m_s", "ms/mb": "m_s/m_b"}


def load_targets():
    raw = open(TARGET_FILE, "rb").read()
    txt = raw.decode("utf-8")
    names = {1: "V_{us}", 2: "V_{cb}", 3: "V_{ub}", 4: "m_u/m_c", 5: "m_c/m_t", 6: "m_d/m_s", 7: "m_s/m_b"}
    T = {}
    for line in txt.splitlines():
        m = re.match(r"^\|\s*(\d)\s*\|\s*([^|]+?)\s*\|\s*([0-9.]+(?:e-?\d+)?)\s*\|", line)
        if m and int(m.group(1)) in names:
            n = int(m.group(1))
            if KEYS[n - 1] in T:
                continue
            assert names[n] in m.group(2), line
            T[KEYS[n - 1]] = float(m.group(3))
    assert len(T) == 7, T
    return T, hashlib.sha256(raw).hexdigest()[:8].upper()


# =====================================================================================
# Model
# =====================================================================================
def prof_int(sig, prof):
    """t_k = ∫_0^1 h(u) b_k(u) du, b_k = 3 C(2,k) u^k (1-u)^(2-k): brane-frame diagonal Yukawas (unnormalised)."""
    if prof == "soft":
        I = [sig ** (n + 1) * math.factorial(n) * gammainc(n + 1, 1.0 / sig) for n in range(3)]
        return np.array([3 * (I[0] - 2 * I[1] + I[2]), 6 * (I[1] - I[2]), 3 * I[2]])
    s = min(sig, 1.0)
    return np.array([3 * (s - s * s + s ** 3 / 3), 3 * s * s - 2 * s ** 3, s ** 3])


def Dmat(beta):
    c, s = math.cos(beta / 2), math.sin(beta / 2)
    r = math.sqrt(2) * c * s
    return np.array([[c * c, -r, s * s], [r, c * c - s * s, -r], [s * s, r, c * c]])


def d1abs(beta):
    cb, sb = math.cos(beta), math.sin(beta) / math.sqrt(2)
    return np.abs(np.array([[(1 + cb) / 2, sb, (1 - cb) / 2], [sb, cb, sb], [(1 - cb) / 2, sb, (1 + cb) / 2]]))


def yd_matrix(sd, eps, beta, st, prof="soft", ref=False):
    if ref:
        A = np.diag([1.0, 2 * sd, 2 * sd * sd])
    else:
        a = prof_int(sd, prof); A = np.diag(a / a[0])
    D = Dmat(beta)
    if st is None:
        Tm = np.outer(D[:, 0], D[:, 0])
    else:
        t = prof_int(st, prof); Tm = D @ np.diag(t / t[0]) @ D.T
    return A + eps * Tm


def observables(Yu, Yd):
    Uu, Su, _ = np.linalg.svd(Yu)
    Ud, Sd, _ = np.linalg.svd(Yd)
    V = np.abs(Uu.T @ Ud)          # rows (t, c, u), columns (b, s, d)
    return {"Vus": V[2, 1], "Vcb": V[1, 0], "Vub": V[2, 0], "mu/mc": Su[2] / Su[1], "mc/mt": Su[1] / Su[0],
            "md/ms": Sd[2] / Sd[1], "ms/mb": Sd[1] / Sd[0], "V": V, "Sd": Sd, "Su": Su}


def predict(su, sd, eps, beta, st, prof="soft", ref=False):
    a = prof_int(su, prof)
    return observables(np.diag(a / a[0]), yd_matrix(sd, eps, beta, st, prof, ref))


def lo_forms(sd, eps, beta, P):
    """Venus's corrected LO forms (physical gap from the exact SVD P) and Helios's originals."""
    vb, vs, vd = Dmat(beta)[:, 0]
    gap = P["ms/mb"] * (1 - P["md/ms"])
    ven = {"Vcb": eps * vb * vs, "Vub": eps * vb * vd, "Vus": eps * vs * vd / gap}
    hel = {"Vcb": eps * vs, "Vub": eps * vd, "Vus": eps * vs * vd / (2 * sd)}
    return ven, hel


def rel3(P):
    return 2 * P["Vub"] ** 2 / (P["Vcb"] * P["ms/mb"]), 2 * P["Vub"] ** 2 / (P["Vcb"] * P["ms/mb"] * (1 - P["md/ms"]))


# ---------------- direct quadrature of the zero modes (brane-centred coordinates) ----------------
_GLX, _GLW = np.polynomial.legendre.leggauss(NG)


def brane_Y_quad(beta, hfun, umax):
    gmax = 2 * math.asin(math.sqrt(min(umax, 1.0)))
    g = 0.5 * gmax * (_GLX + 1); wg = 0.5 * gmax * _GLW * np.sin(g)
    psi = 2 * np.pi * np.arange(NPSI) / NPSI
    G, P = np.meshgrid(g, psi, indexing="ij")
    W = np.outer(wg, np.full(NPSI, 2 * np.pi / NPSI))
    a1, b1 = np.cos(G / 2) * np.exp(-0.5j * P), np.sin(G / 2) * np.exp(0.5j * P)   # brane-frame spinor
    c, s = math.cos(beta / 2), math.sin(beta / 2)
    a, b = c * a1 - s * b1, s * a1 + c * b1                                         # rotated about y by beta
    eta = [math.sqrt(3 / (4 * math.pi)) * a * a, math.sqrt(6 / (4 * math.pi)) * a * b, math.sqrt(3 / (4 * math.pi)) * b * b]
    h = hfun(np.sin(G / 2) ** 2, P)
    Y = np.array([[np.sum(W * h * np.conj(eta[i]) * eta[j]) for j in range(3)] for i in range(3)])
    return Y


def prof_quad(beta, sig, prof):
    if prof == "soft":
        return brane_Y_quad(beta, lambda u, p: np.exp(-u / sig), min(1.0, 60 * sig))
    return brane_Y_quad(beta, lambda u, p: np.ones_like(u), sig)


# =====================================================================================
# Stages
# =====================================================================================
def stage_a1():
    w("## A1: different widths alone still give |V| = |d¹(β)| [identity]")
    w("")
    w(f"Direct 2D quadrature of the zero modes ({NG} Gauss–Legendre nodes in the brane angle × {NPSI} in ψ, brane-centred).")
    w("Up brane at the north tip (width σ_u), down brane tilted by β (width σ_d); V = U_uᵀU_d from the two SVDs.")
    w("")
    w("| profile | σ_u | σ_d | β | max ‖V‖ − ‖d¹(β)‖ | Y_d vs D·diag(t)·Dᵀ (rel.) | Y_u vs diag(t) (rel.) | max Im Y |")
    w("|---|---|---|---|---|---|---|---|")
    worst = 0.0
    for su, sd, prof in A1_CASES:
        Yu = prof_quad(0.0, su, prof)
        eu = np.abs(Yu - np.diag(prof_int(su, prof))).max() / np.abs(Yu).max()
        for bt in A1_BETAS:
            Yd = prof_quad(bt, sd, prof)
            D = Dmat(bt)
            Tf = D @ np.diag(prof_int(sd, prof)) @ D.T
            eT = np.abs(Yd - Tf).max() / np.abs(Yd).max()
            im = max(np.abs(Yu.imag).max(), np.abs(Yd.imag).max())
            V = observables(Yu.real, Yd.real)["V"]
            dV = np.abs(V - d1abs(bt)).max()
            worst = max(worst, dV, eT, eu)
            w(f"| {prof} | {su:g} | {sd:g} | {bt:g} | {dV:.1e} | {eT:.1e} | {eu:.1e} | {im:.1e} |")
    ok = worst < TH_A1
    w("")
    w(f"A1 {'PASS' if ok else 'FAIL'}: worst {worst:.1e} (threshold {TH_A1:g}). The tilted brane is the aligned one rotated, so "
      "U_d = D(β) for any width and profile, and the widths only set the masses [identity].")
    w("")
    return ok


def stage_a2():
    w("## A2: a lopsided brane gives θ₁₂ ≈ θ₂₃ ∝ ε√σ")
    w("")
    w("Lopsided brane [assumed input]: h = exp(−u/σ)(1 + ε cos φ) at the north tip (a dipole distortion; Venus's own definition "
      "was not in the relayed spec). The up brane is axially symmetric, so U_u = 1.")
    w("Leading order [identity]: θ₂₃ = ε√(2πσ)/4 and θ₁₂ = 3ε√(2πσ)/16, so θ₁₂/θ₂₃ → 3/4 (same order, not equal).")
    w("")
    w("| ε | σ | θ₂₃ = ‖V_cb‖ | LO | ratio | θ₁₂ = ‖V_us‖ | LO | ratio | θ₁₂/θ₂₃ | θ₁₃ |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    R = {}
    for eps in A2_EPS:
        for sig in A2_SIG:
            Yd = brane_Y_quad(0.0, lambda u, p: np.exp(-u / sig) * (1 + eps * np.cos(p)), min(1.0, 60 * sig)).real
            P = observables(np.diag([1.0, 0.5, 0.25]), Yd)
            l23, l12 = eps * math.sqrt(2 * math.pi * sig) / 4, 3 * eps * math.sqrt(2 * math.pi * sig) / 16
            R[(eps, sig)] = (P["Vcb"], P["Vus"], l23, l12)
            w(f"| {eps:g} | {sig:g} | {P['Vcb']:.6e} | {l23:.6e} | {P['Vcb'] / l23:.5f} | {P['Vus']:.6e} | {l12:.6e} | "
              f"{P['Vus'] / l12:.5f} | {P['Vus'] / P['Vcb']:.5f} | {P['Vub']:.1e} |")
    e0, e1 = A2_EPS[0], A2_EPS[-1]
    s0, s1 = A2_SIG[-2], A2_SIG[-1]
    sl = lambda y0, y1, x0, x1: math.log(y1 / y0) / math.log(x1 / x0)
    s23 = sl(R[(e0, s0)][0], R[(e0, s1)][0], s0, s1); s12 = sl(R[(e0, s0)][1], R[(e0, s1)][1], s0, s1)
    e23 = sl(R[(e0, s1)][0], R[(e1, s1)][0], e0, e1); e12 = sl(R[(e0, s1)][1], R[(e1, s1)][1], e0, e1)
    v23, v12, l23, l12 = R[(e0, s1)]
    rr = (v12 / v23) / 0.75
    ok = (abs(s23 - 0.5) <= TH_A2_SLOPE and abs(s12 - 0.5) <= TH_A2_SLOPE and abs(e23 - 1) <= TH_A2_SLOPE
          and abs(e12 - 1) <= TH_A2_SLOPE and abs(v23 / l23 - 1) <= TH_A2_LO and abs(v12 / l12 - 1) <= TH_A2_LO
          and abs(rr - 1) <= TH_A2_LO)
    w("")
    w(f"Fitted exponents [computed]: d ln θ/d ln σ (σ = {s0:g} → {s1:g}): θ₂₃ {s23:.4f}, θ₁₂ {s12:.4f}; d ln θ/d ln ε (ε = {e0:g} → {e1:g}): "
      f"θ₂₃ {e23:.4f}, θ₁₂ {e12:.4f}. At ε = {e0:g}, σ = {s1:g}: θ/LO = {v23 / l23:.4f} (θ₂₃), {v12 / l12:.4f} (θ₁₂); "
      f"(θ₁₂/θ₂₃)/(3/4) = {rr:.4f}.")
    w(f"A2 {'PASS' if ok else 'FAIL'} (thresholds: exponents within {TH_A2_SLOPE:g} of 1/2 and 1; LO ratios within {TH_A2_LO:g}). "
      "A single lopsided brane makes θ₁₂ and θ₂₃ comparable, like a tilt, and so cannot give |V_us| ≫ |V_cb| on its own.")
    w("")
    return ok


def stage_cp(T):
    w("## Check point: leading-order forms against the exact 3×3 SVD")
    w("")
    sd, eps, bt = CP["sd"], CP["eps"], CP["beta"]
    P = predict(T["mc/mt"] / 2, sd, eps, bt, None, ref=True)
    ven, hel = lo_forms(sd, eps, bt, P)
    w(f"Rank-1 reference form Y_d = diag(1, 2σ_d, 2σ_d²) + ε v vᵀ at σ_d = {sd:g}, ε = {eps:g}, β = {bt:g} [assumed input]. "
      f"Exact masses: m_s/m_b = {P['ms/mb']:.5f}, m_d/m_s = {P['md/ms']:.5f} [computed].")
    w("")
    w("| angle | exact SVD | Venus corrected | ratio | Helios original | ratio |")
    w("|---|---|---|---|---|---|")
    ok = True
    for k, nm in (("Vcb", "θ₂₃ = ‖V_cb‖"), ("Vub", "θ₁₃ = ‖V_ub‖"), ("Vus", "θ₁₂ = ‖V_us‖")):
        rv, rh = ven[k] / P[k], hel[k] / P[k]
        ok &= abs(rv - 1) <= TH_CP
        w(f"| {nm} | {P[k]:.5f} | {ven[k]:.5f} | {rv:.4f} | {hel[k]:.5f} | {rh:.4f} |")
    w("")
    w("Venus: θ₂₃ = ε cos²(β/2) sinβ/√2, θ₁₃ = ε cos²(β/2) sin²(β/2), θ₁₂ = ε v_s v_d /((m_s − m_d)/m_b) with the physical gap. "
      "Helios: no cos² factor, gap 2σ_d.")
    w(f"Spec expectations [prediction]: Helios θ₁₂ ≈ {CP_EXPECT['helios12']:g} (here {hel['Vus']:.4f}), exact ≈ {CP_EXPECT['exact12']:g} "
      f"(here {P['Vus']:.4f}).")
    full1 = predict(T["mc/mt"] / 2, sd, eps, bt, None)
    full2 = predict(T["mc/mt"] / 2, sd, eps, bt, 0.001)
    w(f"Same knobs in the full model (exact soft integrals) [computed]: rank-1 tilted brane ‖V_us‖, ‖V_cb‖, ‖V_ub‖ = "
      f"{full1['Vus']:.5f}, {full1['Vcb']:.5f}, {full1['Vub']:.6f}; σ_t = 0.001: {full2['Vus']:.5f}, {full2['Vcb']:.5f}, {full2['Vub']:.6f}.")
    w(f"Check point {'PASS' if ok else 'FAIL'}: Venus's corrected forms within {TH_CP:g} of the exact SVD.")
    w("")
    return ok, P


def stage_masses(T, Pcp):
    w("## Masses: soft-law estimates")
    w("")
    sd_est = T["ms/mb"] / 2
    w(f"Down [prediction]: the soft law gives m_s/m_b ≈ 2σ_d and m_d/m_s ≈ σ_d, so m_d/m_s ≈ ½·m_s/m_b = {sd_est:.5f} from the target, "
      f"against the target {T['md/ms']:.4g} (target/estimate = {T['md/ms'] / sd_est:.2f}). Venus expected ≈ {VENUS_MDMS:g}.")
    w(f"With the ε shift (check point, rank-1 reference form, exact SVD) [computed]: m_d/m_s = {Pcp['md/ms']:.4f} "
      f"(target/value = {T['md/ms'] / Pcp['md/ms']:.2f}); Venus expected ≈ {VENUS_MDMS_EPS:g}.")
    su_est = T["mc/mt"] / 2
    w(f"Up [prediction]: m_u/m_c ≈ σ_u ≈ ½·m_c/m_t = {su_est:.4e}, against the target {T['mu/mc']:.4g} "
      f"(target/estimate = {T['mu/mc'] / su_est:.2f}).")
    w("")


def stage_r3(T):
    w("## Relation 3: Venus's parameter-free relation [identity at first order in ε, rank-1 limit]")
    w("")
    pred = 2 * T["Vub"] ** 2 / (T["Vcb"] * T["ms/mb"])
    pred_g = 2 * T["Vub"] ** 2 / (T["Vcb"] * T["ms/mb"] * (1 - T["md/ms"]))
    w("θ₁₃/θ₂₃ = tan(β/2)/√2 and θ₁₂/θ₂₃ ≈ tan²(β/2)·m_b/m_s, so V_us ≈ 2V_ub²/(V_cb·m_s/m_b).")
    w(f"**Prediction from the targets, before any fit [prediction]:** V_us ≈ {pred:.4f} (with the physical gap m_s − m_d: {pred_g:.4f}), "
      f"against the target {T['Vus']:.5f}: low by a factor {T['Vus'] / pred:.2f} ({T['Vus'] / pred_g:.2f}). "
      f"Venus expected ≈ {VENUS_R3:g}. This is the wall for single-brane mixing.")
    w("")
    w("Check against the exact SVD (rank-1 reference form):")
    w("")
    w("| σ_d | ε | β | ‖V_us‖ | ‖V_cb‖ | ‖V_ub‖ | m_s/m_b | (θ₁₃/θ₂₃)/(tan(β/2)/√2) | (θ₁₂/θ₂₃)/(tan²(β/2)m_b/m_s) | V_us / relation | with gap |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    worst = 0.0
    for sd, eps, bt in R3_POINTS:
        P = predict(T["mc/mt"] / 2, sd, eps, bt, None, ref=True)
        ra = (P["Vub"] / P["Vcb"]) / (math.tan(bt / 2) / math.sqrt(2))
        rb = (P["Vus"] / P["Vcb"]) / (math.tan(bt / 2) ** 2 / P["ms/mb"])
        r3, r3g = rel3(P)
        worst = max(worst, abs(P["Vus"] / r3 - 1))
        w(f"| {sd:g} | {eps:g} | {bt:g} | {P['Vus']:.5f} | {P['Vcb']:.5f} | {P['Vub']:.6f} | {P['ms/mb']:.5f} | {ra:.4f} | {rb:.4f} | "
          f"{P['Vus'] / r3:.4f} | {P['Vus'] / r3g:.4f} |")
    ok = worst <= TH_R3
    w("")
    w(f"Relation 3 {'PASS' if ok else 'FAIL'}: worst |V_us/relation − 1| = {worst:.3f} (threshold {TH_R3:g}; Venus found ≲ {VENUS_R3_TOL:g}).")
    w("")
    return ok, pred


def stage_st(T):
    w("## σ_t row: the second tilted mode")
    w("")
    sd, eps = ST_FIX["sd"], ST_FIX["eps"]
    w(f"Full model at σ_d = {sd:g}, ε = {eps:g} [assumed input]. The tilted mode t₁ adds ε·t₁·sinβ cosβ/√2 to Y_sd; it competes with "
      "ε v_s v_d once σ_t ≳ β²/8. 'Y_sd factor' is the exact brane-frame ratio (v_s v_d + τ₁ w_s w_d + τ₂ x_s x_d)/(v_s v_d), τ = t/t₀; "
      "'Venus' is 1 + 2σ_t cosβ/sin²(β/2).")
    w("")
    w("| β | β²/8 | σ_t | ‖V_us‖ | ‖V_cb‖ | ‖V_ub‖ | m_d/m_s | m_s/m_b | V_us / V_us(rank-1) | Y_sd factor | Venus |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    for bt in ST_BETAS:
        P0 = predict(T["mc/mt"] / 2, sd, eps, bt, None)
        D = Dmat(bt)
        for st in [None] + ST_ROW:
            P = predict(T["mc/mt"] / 2, sd, eps, bt, st)
            if st is None:
                fac, ven, lab = 1.0, 1.0, "rank-1"
            else:
                t = prof_int(st, "soft"); tau = t / t[0]
                fac = sum(tau[k] * D[1, k] * D[2, k] for k in range(3)) / (D[1, 0] * D[2, 0])
                ven = 1 + 2 * st * math.cos(bt) / math.sin(bt / 2) ** 2
                lab = f"{st:g}"
            w(f"| {bt:g} | {bt * bt / 8:.4f} | {lab} | {P['Vus']:.5f} | {P['Vcb']:.5f} | {P['Vub']:.6f} | {P['md/ms']:.4f} | {P['ms/mb']:.5f} | "
              f"{P['Vus'] / P0['Vus']:.3f} | {fac:.3f} | {ven:.3f} |")
    w("")


def residuals(x, T, prof, st_fixed):
    su, sd, eps, bt = math.exp(x[0]), math.exp(x[1]), math.exp(x[2]), x[3]
    st = st_fixed if st_fixed is not None else math.exp(x[4])
    P = predict(su, sd, eps, bt, st, prof)
    return np.array([math.log(max(P[k], 1e-300) / T[k]) for k in KEYS])


def do_fit(T, prof, st_fixed):
    lo = [math.log(LB["sig"]), math.log(LB["sig"]), math.log(LB["eps"]), LB["beta"]]
    hi = [math.log(LB["sig_hi"]), math.log(LB["sig_hi"]), math.log(LB["eps_hi"]), LB["beta_hi"]]
    su0 = T["mc/mt"] / 2 if prof == "soft" else T["mc/mt"]
    sts = [None] if st_fixed is not None else [0.001, 0.01, 0.05]
    if st_fixed is None:
        lo.append(math.log(LB["sig"])); hi.append(math.log(LB["sig_hi"]))
    best, nstart = None, 0
    for sd0 in (0.003, 0.01, 0.03):
        for e0 in (0.02, 0.1, 0.5, 2.0):
            for b0 in (0.15, 0.3, 0.6, 1.0, 1.5):
                for st0 in sts:
                    x0 = [math.log(su0), math.log(sd0), math.log(e0), b0] + ([] if st0 is None else [math.log(st0)])
                    r = least_squares(residuals, x0, args=(T, prof, st_fixed), bounds=(lo, hi), xtol=1e-12, ftol=1e-12,
                                      gtol=1e-12, max_nfev=3000)
                    nstart += 1
                    if best is None or r.cost < best.cost:
                        best = r
    x = best.x
    kn = dict(su=math.exp(x[0]), sd=math.exp(x[1]), eps=math.exp(x[2]), beta=x[3],
              st=st_fixed if st_fixed is not None else math.exp(x[4]))
    return kn, best, nstart


def grade(P, T):
    misses = [(k, P[k] / T[k]) for k in KEYS if not (1 / FACTOR <= P[k] / T[k] <= FACTOR)]
    order = P["Vus"] > P["Vcb"] > P["Vub"]
    hier = all(P[k] < 1 for k in ("mu/mc", "mc/mt", "md/ms", "ms/mb"))
    if not (order and hier):
        g = "FAIL"
    else:
        g = "PASS" if not misses else "PARTIAL"
    return g, misses, order, hier


def grade_line(name, P, T):
    g, misses, order, hier = grade(P, T)
    ms = "; ".join(f"{LABEL[k]} at {r:.3g}× target" for k, r in misses) if misses else "none"
    w(f"**{name}: {g}**: ordering V_us > V_cb > V_ub {order}; mass hierarchy {hier}; misses (outside ×{FACTOR:g}): {ms}.")
    return g


def ratio_table(rows, T):
    w("| target | value | " + " | ".join(nm for nm, _ in rows) + " |")
    w("|---|---|" + "---|" * len(rows))
    for k in KEYS:
        w(f"| {LABEL[k]} | {T[k]:.4g} | " + " | ".join(f"{P[k]:.4g} (×{P[k] / T[k]:.3f})" for _, P in rows) + " |")
    w("")


def knob_str(kn, free_st):
    s = f"σ_u = {kn['su']:.5g}, σ_d = {kn['sd']:.5g}, ε = {kn['eps']:.5g}, β = {kn['beta']:.5g}"
    return s + (f", σ_t = {kn['st']:.5g} [tuned]" if free_st else f" [tuned]; σ_t = {kn['st']:g} [assumed input]")


def stage_fits(T):
    w("## Fits: log least-squares against the seven targets [tuned]")
    w("")
    w(f"Residuals ln(prediction/target), unweighted; multi-start (grid of starts) with bounds σ ∈ [{LB['sig']:g}, {LB['sig_hi']:g}], "
      f"ε ∈ [{LB['eps']:g}, {LB['eps_hi']:g}], β ∈ [{LB['beta']:g}, {LB['beta_hi']:g}] [assumed input]. Full model, soft profiles.")
    w("")
    fits = {}
    for name, st_fixed in (("Fit 1 (σ_t fixed)", ST_FIT1), ("Fit 2 (σ_t free)", None)):
        kn, r, ns = do_fit(T, "soft", st_fixed)
        P = predict(kn["su"], kn["sd"], kn["eps"], kn["beta"], kn["st"])
        nk = 4 if st_fixed is not None else 5
        fits[name] = (kn, P, st_fixed)
        w(f"### {name}")
        w("")
        w(f"Knobs: {nk} against {len(KEYS)} targets ({len(KEYS) - nk} more targets than knobs). Best of {ns} starts: {knob_str(kn, st_fixed is None)}.")
        w(f"Σ ln² = {2 * r.cost:.4f}, rms |ln ratio| = {math.sqrt(2 * r.cost / len(KEYS)):.4f} [computed].")
        w("")
        ratio_table([(name, P)], T)
        ven, hel = lo_forms(kn["sd"], kn["eps"], kn["beta"], P)
        r3, r3g = rel3(P)
        w(f"Leading order against the exact SVD at the best fit [computed]: ‖V_cb‖ {P['Vcb']:.5f} (Venus {ven['Vcb']:.5f}, Helios {hel['Vcb']:.5f}); "
          f"‖V_ub‖ {P['Vub']:.6f} (Venus {ven['Vub']:.6f}, Helios {hel['Vub']:.6f}); ‖V_us‖ {P['Vus']:.5f} (Venus {ven['Vus']:.5f}, "
          f"Helios {hel['Vus']:.5f}); relation 3 gives {r3:.5f} (with gap {r3g:.5f}), V_us/relation = {P['Vus'] / r3:.3f}. "
          "The LO forms omit the second tilted mode, so they track the exact SVD only where σ_t ≪ β²/8.")
        w("")
        grade_line(f"{name} grade", P, T)
        w("")
    return fits


def stage_tophat(T, fits):
    w("## Top-hat robustness row (report, not graded)")
    w("")
    w("All three branes switched to the top-hat profile h = 1 for u < σ (law 1 : σ : σ²/3). Re-evaluation keeps the soft best-fit "
      "knobs (σ then means a different width, so this is not like-for-like); the refit is the fair comparison.")
    w("")
    rows, glines = [], []
    for name, (kn, Ps, st_fixed) in fits.items():
        P = predict(kn["su"], kn["sd"], kn["eps"], kn["beta"], kn["st"], "tophat")
        rows.append((f"{name}, re-evaluated", P))
        kt, r, ns = do_fit(T, "tophat", st_fixed)
        Pt = predict(kt["su"], kt["sd"], kt["eps"], kt["beta"], kt["st"], "tophat")
        rows.append((f"{name}, top-hat refit", Pt))
        glines.append((name, P, Pt, kt, r, ns, st_fixed))
    ratio_table(rows, T)
    for name, P, Pt, kt, r, ns, st_fixed in glines:
        w(f"{name}, top-hat refit (best of {ns} starts): {knob_str(kt, st_fixed is None)}; Σ ln² = {2 * r.cost:.4f}.")
        grade_line(f"{name}, top-hat re-evaluated (report)", P, T)
        grade_line(f"{name}, top-hat refit (report)", Pt, T)
        w("")


def main():
    now = datetime.datetime.now().astimezone()
    z = now.strftime("%z")
    w("# RESULTS: Job 4b, CKM from an aligned soft brane plus a narrow tilted brane (generated by run.py; do not edit)")
    w("")
    w(f"Generated {now.strftime('%Y-%m-%d %H:%M:%S')} local (UTC{z[:3]}:{z[3:]}). Python {platform.python_version()}, numpy {np.__version__}, "
      f"scipy {scipy.__version__}.")
    w("Tags: [identity] [computed] [assumed input] [prediction] [standard] [tuned] [post-hoc]. Thresholds fixed in run.py before the first run.")
    w("Round sphere only (α = 1). Generations: k = 0 heaviest; V = U_uᵀU_d with rows (t, c, u), columns (b, s, d). All matrices real, so J = 0.")
    w("")
    T, th = load_targets()
    w(f"Targets parsed from {TARGET_FILE} (sha256 {th}) [standard: PDG 2026 global fit; Huang–Zhou 2021 at M_Z]:")
    w("")
    w("| " + " | ".join(LABEL[k] for k in KEYS) + " |")
    w("|" + "---|" * len(KEYS))
    w("| " + " | ".join(f"{T[k]:.4g}" for k in KEYS) + " |")
    w("")
    a1 = stage_a1()
    a2 = stage_a2()
    cp, Pcp = stage_cp(T)
    stage_masses(T, Pcp)
    r3, pred = stage_r3(T)
    stage_st(T)
    fits = stage_fits(T)
    stage_tophat(T, fits)
    w("## Grade lines")
    w("")
    w(f"- A1 [identity]: {'PASS' if a1 else 'FAIL'}; A2: {'PASS' if a2 else 'FAIL'}; check point: {'PASS' if cp else 'FAIL'}; "
      f"relation 3: {'PASS' if r3 else 'FAIL'}.")
    for name, (kn, P, st_fixed) in fits.items():
        g, misses, _, _ = grade(P, T)
        w(f"- {name}: {g}" + (" (misses: " + ", ".join(LABEL[k] for k, _ in misses) + ")" if misses else ""))
    w(f"- Venus expected PARTIAL at fixed σ_t [prediction].")
    w("")
    w(f"Runtime: {time.time() - T0:.1f} s [computed].")
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
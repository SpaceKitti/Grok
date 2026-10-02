#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job 4c: RS flavour anarchy. Fit 9 bulk masses c (8 free, c_Q3 = c_u3) to quark masses at 1 TeV and median |V_us|, |V_cb|;
then predict |V_ub| and |J| from independent anarchic draws. Writes RESULTS.md only. Every number is printed from a variable.
"""
import os, re, time, hashlib, datetime, platform
import numpy as np
import scipy
from scipy.optimize import least_squares
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = r"C:\Users\Akitt\open-problems\01_sm_from_sphere\JOB_4c_SPEC.md"
RES4B = r"C:\Users\Akitt\sm-yukawa-4b-ckm\RESULTS.md"
T0 = time.time(); OUT = []


def w(s=""):
    print(s, flush=True); OUT.append(s)


def sha8(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:8].upper() if os.path.exists(p) else "MISSING"


# =====================================================================================
# FIXED BEFORE THE FIRST RUN
# =====================================================================================
KL = 35.0                         # Venus: kL = 35 (spec: ln(M_Pl/TeV) ~ 35) [assumed input]
MPL_FULL, MPL_RED, TEV = 1.22e19, 2.435e18, 1.0e3   # GeV, for printing ln(M_Pl/TeV) [standard]
VEV = 246.22                      # GeV [standard]
YSTAR = 1.0                       # graded run; YSTAR_REPORT reported only
YSTAR_REPORT = 3.0
YMIN, YMAX = 1.0 / 3.0, 3.0       # |Y_ij| log-uniform on [1/3, 3] [assumed input]
N_DRAW = 10_000
SEED_A, SEED_B = 40401, 40402     # fit sample, prediction sample
MASS_TOL = 0.10                   # Stage A solvability: medians within 10%
C_LO, C_HI = 0.0, 1.0             # naturalness: every c in 1/2 +- 0.5
Q68 = (0.16, 0.84); Q95 = (0.025, 0.975)
BAND_4B = 2.0                     # 4b tolerance: within x2
SPREAD_REF = 0.3                  # spec: "c's spread over less than about 0.3"
# [assumed input] masses at mu = 1 TeV, Xing-Zhang-Zhou arXiv:0712.1419 Table IV (SM, m_H = 140 GeV), GeV
MASS = {"u": 1.10e-3, "c": 0.532, "t": 150.7, "d": 2.50e-3, "s": 47e-3, "b": 2.43}
MASS_SRC = "Xing–Zhang–Zhou arXiv:0712.1419, Table IV (SM, m_H = 140 GeV), μ = 1 TeV"
# [assumed input] PDG 2026 CKM review, Eq. (12.27) global fit, and J on the line after it
CKM = {"Vus": 0.22517, "Vcb": 0.04189, "Vub": 0.003763, "Vcs": 0.97345, "J": 3.16e-5}
CKM_SRC = {"Vus": "PDG26 Eq. (12.27)", "Vcb": "PDG26 Eq. (12.27), +0.00081/−0.00069", "Vub": "PDG26 Eq. (12.27), +0.000088/−0.000083",
           "Vcs": "PDG26 Eq. (12.27)", "J": "PDG26 §12.4, J = (3.16 +0.13/−0.11)×10⁻⁵"}
# [pre-registered estimate, Venus, /tmp/c4c.py; leading order, kL=35]
VENUS = {"Q": [0.62, 0.56, 0.07], "u": [0.69, 0.54, 0.07], "d": [0.67, 0.62, 0.60], "spread_light": 0.16, "spread_full": 0.62,
         "VusVcb": 0.0092}
START = np.array([0.62, 0.56, 0.07, 0.69, 0.54, 0.67, 0.62, 0.60])   # x = (cQ1, cQ2, c3, cu1, cu2, cd1, cd2, cd3)
NAMES = ["c_Q1", "c_Q2", "c_Q3 = c_u3", "c_u1", "c_u2", "c_d1", "c_d2", "c_d3"]


def F(c, kL=KL):
    """IR-brane zero-mode value, convention c > 1/2 UV/light, c < 1/2 IR/heavy. expm1 form; F^2 -> 1/kL at c = 1/2."""
    c = np.asarray(c, dtype=float); x = 1.0 - 2.0 * c
    small = np.abs(x) < 1e-12
    xs = np.where(small, 1.0, x)
    F2 = np.where(small, 1.0 / kL, xs / (-np.expm1(-xs * kL)))
    return np.sqrt(F2)


def unpack(x):
    cQ = np.array([x[0], x[1], x[2]]); cu = np.array([x[3], x[4], x[2]]); cd = np.array([x[5], x[6], x[7]])
    return cQ, cu, cd


def draws(seed, n=N_DRAW, ystar=YSTAR):
    rng = np.random.default_rng(seed)
    def one():
        mag = np.exp(rng.uniform(np.log(YMIN), np.log(YMAX), size=(n, 3, 3)))
        ph = rng.uniform(0.0, 2 * np.pi, size=(n, 3, 3))
        return ystar * mag * np.exp(1j * ph)
    Yu = one(); Yd = one()
    return Yu, Yd


def observables(x, Yu, Yd, kL=KL):
    cQ, cu, cd = unpack(x)
    FQ, Fu, Fd = F(cQ, kL), F(cu, kL), F(cd, kL)
    pre = VEV / np.sqrt(2.0)
    Mu = pre * FQ[None, :, None] * Yu * Fu[None, None, :]
    Md = pre * FQ[None, :, None] * Yd * Fd[None, None, :]
    Uu, su, _ = np.linalg.svd(Mu); Ud, sd, _ = np.linalg.svd(Md)
    Uu, su = Uu[:, :, ::-1], su[:, ::-1]; Ud, sd = Ud[:, :, ::-1], sd[:, ::-1]     # ascending: (u, c, t), (d, s, b)
    V = np.conj(np.transpose(Uu, (0, 2, 1))) @ Ud
    Vus, Vcb, Vub, Vcs = V[:, 0, 1], V[:, 1, 2], V[:, 0, 2], V[:, 1, 1]
    J = np.imag(Vus * Vcb * np.conj(Vub) * np.conj(Vcs))
    unit = np.abs(np.conj(np.transpose(V, (0, 2, 1))) @ V - np.eye(3)).max()
    return dict(mu=su[:, 0], mc=su[:, 1], mt=su[:, 2], md=sd[:, 0], ms=sd[:, 1], mb=sd[:, 2],
                Vus=np.abs(Vus), Vcb=np.abs(Vcb), Vub=np.abs(Vub), J=J, unit=unit, FQ=FQ, Fu=Fu, Fd=Fd)


TKEYS = ["mu", "mc", "mt", "md", "ms", "mb", "Vus", "Vcb"]
TVALS = np.array([MASS["u"], MASS["c"], MASS["t"], MASS["d"], MASS["s"], MASS["b"], CKM["Vus"], CKM["Vcb"]])


def resid(x, Yu, Yd, kL=KL):
    o = observables(x, Yu, Yd, kL)
    med = np.array([np.median(o[k]) for k in TKEYS])
    return np.log(med / TVALS)


def fit(Yu, Yd, x0, kL=KL):
    r = least_squares(resid, x0, args=(Yu, Yd, kL), method="trf", diff_step=1e-4, xtol=1e-12, ftol=1e-12, gtol=1e-12,
                      max_nfev=4000, bounds=(-1.0, 2.0))
    return r


def quant(a, qs):
    return np.quantile(a, qs)


def stage_b(x, ystar=YSTAR, kL=KL):
    Yu, Yd = draws(SEED_B, ystar=ystar)
    o = observables(x, Yu, Yd, kL)
    lnJ = np.log(np.abs(o["J"]))
    q_ub = quant(o["Vub"], [Q95[0], Q68[0], 0.5, Q68[1], Q95[1]])
    q_J = np.exp(quant(lnJ, [Q95[0], Q68[0], 0.5, Q68[1], Q95[1]]))
    in68_ub = q_ub[1] <= CKM["Vub"] <= q_ub[3]; in95_ub = q_ub[0] <= CKM["Vub"] <= q_ub[4]
    in68_J = q_J[1] <= CKM["J"] <= q_J[3]; in95_J = q_J[0] <= CKM["J"] <= q_J[4]
    if in68_ub and in68_J:
        g = "PASS"
    elif in95_ub and in95_J:
        g = "PARTIAL"
    else:
        g = "FAIL"
    rank_ub = float(np.mean(o["Vub"] < CKM["Vub"])); rank_J = float(np.mean(np.abs(o["J"]) < CKM["J"]))
    return dict(o=o, q_ub=q_ub, q_J=q_J, in68=(in68_ub, in68_J), in95=(in95_ub, in95_J), grade=g, rank=(rank_ub, rank_J))


def main():
    now = datetime.datetime.now().astimezone(); z = now.strftime("%z")
    w("# RESULTS: Job 4c, RS flavour anarchy (generated by run.py; do not edit)")
    w("")
    w(f"Generated {now.strftime('%Y-%m-%d %H:%M:%S')} local (UTC{z[:3]}:{z[3:]}). Python {platform.python_version()}, numpy {np.__version__}, scipy {scipy.__version__}.")
    w("Tags: [standard] [computed] [assumed] [tuned] [post-hoc] [prediction] [hive-interpretation] [standard: beyond toy]. Thresholds and seeds fixed in run.py before the first run.")
    w(f"Spec: {SPEC} (sha256 {sha8(SPEC)}). 4b reference: {RES4B} (sha256 {sha8(RES4B)}).")
    w("")
    w("**Convention (one F(c) for every field):** c > 1/2 means UV-localised and light; c < 1/2 means IR-localised and heavy; the same for Q, u and d. "
      "Sources that flip the sign of c for the singlets map as c → −c for those singlets. "
      "F(c) = sqrt((1 − 2c)/(1 − e^(−(1 − 2c)kL))), coded with expm1, with F² = 1/kL at c = 1/2 [standard: Gherghetta–Pomarol; Huber–Shafi; Agashe–Perez–Soni].")
    w(f"kL = {KL:g} [assumed input]; for reference ln(M_Pl/TeV) = {np.log(MPL_FULL / TEV):.2f} (M_Pl = {MPL_FULL:.3g} GeV), "
      f"{np.log(MPL_RED / TEV):.2f} (reduced, {MPL_RED:.4g} GeV). F(1/2) = {float(F(0.5)):.6f} against 1/sqrt(kL) = {1 / np.sqrt(KL):.6f}; "
      f"F(1/2 ± 1e-9) = {float(F(0.5 - 1e-9)):.6f}, {float(F(0.5 + 1e-9)):.6f} [computed].")
    w(f"M_u = (v/√2) F_Q Y_u F_u, M_d = (v/√2) F_Q Y_d F_d, v = {VEV} GeV; V = U_uL† U_dL; J = Im(V_us V_cb V_ub* V_cs*). "
      f"Anarchy [assumed input]: |Y_ij| log-uniform on [{YMIN:.4g}, {YMAX:g}], phases uniform on [0, 2π), Y* = {YSTAR:g} (graded). "
      f"Leftover freedom fixed by F(c_Q3) = F(c_u3), i.e. c_Q3 = c_u3 (Venus fix 2). Draws: {N_DRAW}; seeds A = {SEED_A}, B = {SEED_B}.")
    w("")
    w("## Inputs [assumed input]")
    w("")
    w("| quantity | value | source |")
    w("|---|---|---|")
    for k, lab in [("u", "m_u"), ("c", "m_c"), ("t", "m_t"), ("d", "m_d"), ("s", "m_s"), ("b", "m_b")]:
        w(f"| {lab}(1 TeV) | {MASS[k]:.4g} GeV | {MASS_SRC} |")
    for k, lab in [("Vus", "|V_us|"), ("Vcb", "|V_cb|"), ("Vub", "|V_ub|"), ("Vcs", "|V_cs|"), ("J", "J")]:
        w(f"| {lab} | {CKM[k]:.5g} | {CKM_SRC[k]} |")
    w("CKM magnitudes are low-energy values; their SM running up to 1 TeV is neglected [standard].")
    w("")

    # ---------------- Stage A ----------------
    w("## Stage A: fit the c's (solvability check, not a prediction) [standard / tuned]")
    w("")
    YuA, YdA = draws(SEED_A)
    r = fit(YuA, YdA, START)
    x = r.x; cQ, cu, cd = unpack(x)
    res = resid(x, YuA, YdA)
    w(f"8 free c's for 8 targets (6 masses, median |V_us|, median |V_cb|) over the Stage A sample. least_squares: status {r.status}, "
      f"nfev {r.nfev}, max |ln(median/target)| = {np.abs(res).max():.2e} [computed].")
    w("")
    w("| field | gen 1 | gen 2 | gen 3 | F(c) gen 1 | F(c) gen 2 | F(c) gen 3 |")
    w("|---|---|---|---|---|---|---|")
    for lab, cc in [("Q", cQ), ("u", cu), ("d", cd)]:
        Fc = F(cc)
        w(f"| c_{lab} | {cc[0]:.4f} | {cc[1]:.4f} | {cc[2]:.4f} | {Fc[0]:.4e} | {Fc[1]:.4e} | {Fc[2]:.4e} |")
    w("")
    oA = observables(x, YuA, YdA)
    w("| target | value | median (Stage A sample) | ratio | within 10% |")
    w("|---|---|---|---|---|")
    okA = True
    for k, tv in zip(TKEYS, TVALS):
        m = float(np.median(oA[k])); rr = m / tv; ok = abs(rr - 1) <= MASS_TOL; okA &= ok
        w(f"| {k} | {tv:.4g} | {m:.4g} | {rr:.4f} | {ok} |")
    w("")
    allc = np.concatenate([cQ, cu, cd])
    in_range = [(C_LO <= v <= C_HI) for v in allc]
    labs = ["c_Q1", "c_Q2", "c_Q3", "c_u1", "c_u2", "c_u3", "c_d1", "c_d2", "c_d3"]
    w(f"Unitarity of V on the sample: max |V†V − 1| = {oA['unit']:.1e} [computed].")
    w("Naturalness test [prediction; range fixed before the run]: every c in [" + f"{C_LO:g}, {C_HI:g}" + "]: " +
      ", ".join(f"{l} {v:.3f} {'in' if ok else 'OUT'}" for l, v, ok in zip(labs, allc, in_range)) + ".")
    gA_solv = "solvable" if okA else "not solved to 10%"
    gA_nat = "PASS" if all(in_range) else "FAIL"
    w(f"**Stage A: {gA_solv} (all 8 medians within {MASS_TOL:.0%}: {okA}); naturalness (every c in ½ ± 0.5): {gA_nat}.** "
      "With 8 c's for 8 targets the fit itself is not a test; only the c range is.")
    VusVcb_LO = CKM["Vus"] * CKM["Vcb"]
    w(f"Leading order [computed]: F_Q1/F_Q2 = {F(cQ[0]) / F(cQ[1]):.4f}, F_Q2/F_Q3 = {F(cQ[1]) / F(cQ[2]):.4f}, F_Q1/F_Q3 = {F(cQ[0]) / F(cQ[2]):.5f}; "
      f"V_us·V_cb from the measured values = {VusVcb_LO:.5f} against |V_ub| = {CKM['Vub']} (ln ratio {np.log(VusVcb_LO / CKM['Vub']):.3f}).")
    w("")
    w("Venus's pre-registered estimate against the fit [pre-registered estimate, Venus, /tmp/c4c.py; leading order, kL=35]:")
    w("")
    w("| c | Venus | fitted | difference |")
    w("|---|---|---|---|")
    vlist = VENUS["Q"] + VENUS["u"] + VENUS["d"]
    for l, v, f_ in zip(labs, vlist, allc):
        w(f"| {l} | {v:.2f} | {f_:.4f} | {f_ - v:+.4f} |")
    light = np.array([cQ[0], cQ[1], cu[0], cu[1], cd[0], cd[1], cd[2]])
    light8 = np.array([cQ[0], cQ[1], cu[0], cu[1], cd[0], cd[1], cd[2]])
    w("")

    # ---------------- Stage B ----------------
    w("## Stage B: predictions from independent draws [prediction]")
    w("")
    B = stage_b(x)
    o = B["o"]
    w(f"{N_DRAW} new (Y_u, Y_d) pairs (seed {SEED_B}), c's frozen at Stage A. Unitarity max |V†V − 1| = {o['unit']:.1e}.")
    w("")
    w("| quantity | measured (source) | q2.5% | q16% | median | q84% | q97.5% | measured inside 68% | inside 95% | fraction of draws below measured |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    w(f"| |V_ub| | {CKM['Vub']} ({CKM_SRC['Vub']}) | " + " | ".join(f"{v:.5f}" for v in B["q_ub"]) + f" | {B['in68'][0]} | {B['in95'][0]} | {B['rank'][0]:.3f} |")
    w(f"| |J| (quantiles of log|J|) | {CKM['J']:.3g} ({CKM_SRC['J']}) | " + " | ".join(f"{v:.3e}" for v in B["q_J"]) + f" | {B['in68'][1]} | {B['in95'][1]} | {B['rank'][1]:.3f} |")
    w("")
    for k in ["Vus", "Vcb"]:
        q = quant(o[k], [Q95[0], Q68[0], 0.5, Q68[1], Q95[1]])
        w(f"Report: |{k}| on the B sample: quantiles " + ", ".join(f"{v:.4f}" for v in q) + f" (target {CKM[k]}, fitted as a median on sample A).")
    w(f"Report: sign of J: fraction J > 0 = {np.mean(o['J'] > 0):.3f} (anarchic phases are symmetric, so ~0.5 is expected); median |J| / (V_us V_cb V_ub measured) = "
      f"{B['q_J'][2] / (CKM['Vus'] * CKM['Vcb'] * CKM['Vub']):.3f}.")
    # 4b seven targets
    txt4b = open(RES4B, encoding="utf-8").read() if os.path.exists(RES4B) else ""
    m4b = re.search(r"\| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \|", txt4b)
    t4b = [float(v) for v in m4b.groups()] if m4b else None
    if t4b:
        ratios = np.stack([o["Vus"] / t4b[0], o["Vcb"] / t4b[1], o["Vub"] / t4b[2], (o["mu"] / o["mc"]) / t4b[3], (o["mc"] / o["mt"]) / t4b[4],
                           (o["md"] / o["ms"]) / t4b[5], (o["ms"] / o["mb"]) / t4b[6]])
        hit = np.all((ratios >= 1 / BAND_4B) & (ratios <= BAND_4B), axis=0)
        per = np.mean((ratios >= 1 / BAND_4B) & (ratios <= BAND_4B), axis=1)
        w(f"4b comparison: fraction of draws hitting all seven 4b targets ({', '.join(f'{v:g}' for v in t4b)}; parsed from 4b RESULTS) within ×{BAND_4B:g}: "
          f"**{hit.mean():.4f}** [computed]. Per target: " + ", ".join(f"{n} {p:.3f}" for n, p in zip(["V_us", "V_cb", "V_ub", "m_u/m_c", "m_c/m_t", "m_d/m_s", "m_s/m_b"], per)) +
          ". Caveat: 4b's mass ratios are at M_Z (Huang–Zhou 2021); here masses are fitted at 1 TeV, so m_c/m_t and m_s/m_b carry a scale offset of order 10%.")
    else:
        w("4b comparison: 4b target row not found in 4b RESULTS.")
    w("")
    w(f"**Stage B grade: {B['grade']}** (PASS: both measured values inside the central 68%; PARTIAL: both inside 95%; FAIL: either outside 95%) [prediction].")
    w("")

    # ---------------- report rows ----------------
    w("## Report-only rows (not graded)")
    w("")
    w("| variant | refit max |ln| | c_Q | c_u | c_d | all c in [0,1] | |V_ub| q16/med/q84 | |J| q16/med/q84 | grade-equivalent |")
    w("|---|---|---|---|---|---|---|---|---|")
    for lab, ys, kl in [(f"Y* = {YSTAR_REPORT:g}", YSTAR_REPORT, KL), (f"kL = ln(M_Pl/TeV) = {np.log(MPL_FULL / TEV):.2f}", YSTAR, float(np.log(MPL_FULL / TEV)))]:
        YuR, YdR = draws(SEED_A, ystar=ys)
        rr = fit(YuR, YdR, x, kL=kl)
        cq, cuu, cdd = unpack(rr.x); BR = stage_b(rr.x, ystar=ys, kL=kl)
        allr = np.concatenate([cq, cuu, cdd])
        w(f"| {lab} | {np.abs(resid(rr.x, YuR, YdR, kl)).max():.1e} | {', '.join(f'{v:.3f}' for v in cq)} | {', '.join(f'{v:.3f}' for v in cuu)} | "
          f"{', '.join(f'{v:.3f}' for v in cdd)} | {bool(np.all((allr >= C_LO) & (allr <= C_HI)))} | "
          f"{BR['q_ub'][1]:.5f} / {BR['q_ub'][2]:.5f} / {BR['q_ub'][3]:.5f} | {BR['q_J'][1]:.2e} / {BR['q_J'][2]:.2e} / {BR['q_J'][3]:.2e} | {BR['grade']} |")
    w("")

    # ---------------- Stage C ----------------
    w("## Stage C: report only")
    w("")
    wall = re.findall(r"Knob-free wall number r_us·r_cb·r_ρ/r_ub² = ([\d.]+)", txt4b)
    rel3 = re.search(r"V_us ≈ ([\d.]+) \(with the physical gap", txt4b)
    ratio_anarchy = B["q_ub"][2] / CKM["Vub"]
    w("**4b comparison** [computed; 4b values parsed from 4b RESULTS, standard: earlier hive result]:")
    w(f"- Anarchy: V_ub ~ V_us·V_cb. Predicted/measured: leading order {VusVcb_LO / CKM['Vub']:.3f}; median of the B sample {ratio_anarchy:.3f} "
      f"(68% band {B['q_ub'][1] / CKM['Vub']:.3f}–{B['q_ub'][3] / CKM['Vub']:.3f}).")
    if rel3:
        v3 = float(rel3.group(1))
        w(f"- 4b rank-1 relation 3: predicted/measured |V_us| = {v3 / CKM['Vus']:.3f} (4b's V_us ≈ {v3}), with no spread to absorb it; J = 0 identically.")
    if len(wall) >= 2:
        w(f"- 4b knob-free wall numbers (1 = no wall): Fit 1 {float(wall[0]):.4f}, Fit 2 {float(wall[1]):.4f}. The anarchy analogue is ln(predicted/measured) for V_ub: "
          f"{np.log(ratio_anarchy):+.3f} (median), which sits inside the order-one spread (68% band in ln: {np.log(B['q_ub'][1] / CKM['Vub']):+.3f} to {np.log(B['q_ub'][3] / CKM['Vub']):+.3f}).")
    sp_l = float(light8.max() - light8.min()); sp_f = float(allc.max() - allc.min())
    w("")
    w(f"**Spread of the c's** [computed]: the light set (c_Q1, c_Q2, c_u1, c_u2, c_d1, c_d2, c_d3) spans {sp_l:.4f} (Venus {VENUS['spread_light']}); "
      f"the full set including the top pair (c_Q3 = c_u3) spans {sp_f:.4f} (Venus {VENUS['spread_full']}). Reference: about {SPREAD_REF}. "
      f"Light set under {SPREAD_REF}: {sp_l < SPREAD_REF}; full set under {SPREAD_REF}: {sp_f < SPREAD_REF}. "
      f"Mass span covered by the light set: ln(m_c/m_u) = {np.log(MASS['c'] / MASS['u']):.2f}, ln(m_b/m_d) = {np.log(MASS['b'] / MASS['d']):.2f}, against kL·(spread) = {KL * sp_l:.2f}.")
    w("")
    # Brockett check
    rng = np.random.default_rng(SEED_A + 7)
    Rm, _ = np.linalg.qr(rng.standard_normal((3, 3)))
    H0 = Rm @ np.diag(cQ) @ Rm.T; Nm = np.diag([1.0, 2.0, 3.0])
    def rhs(t, y):
        Hh = y.reshape(3, 3); K = Hh @ Nm - Nm @ Hh
        return (Hh @ K - K @ Hh).ravel()
    sol = solve_ivp(rhs, (0, 4000.0), H0.ravel(), method="DOP853", rtol=1e-11, atol=1e-13)
    Hend = sol.y[:, -1].reshape(3, 3)
    ev0, ev1 = np.sort(np.linalg.eigvalsh(H0)), np.sort(np.linalg.eigvalsh((Hend + Hend.T) / 2))
    off = np.abs(Hend - np.diag(np.diag(Hend))).max()
    w("**Akitti's Brockett double-bracket c-shifts** [hive-interpretation]: a double-bracket flow dH/dt = [H, [H, N]] on a symmetric bulk-mass matrix "
      "H = R·diag(c)·Rᵀ keeps the spectrum of H and only rotates it, ending diagonal in the eigenbasis of N with the eigenvalues sorted. So it can land on the "
      "Stage A c's only if those values are already the eigenvalues of H at the start: it can align the bulk masses with the brane (removing bulk mixing), "
      "but it cannot create the exponential hierarchy, which comes from kL times order-one differences in c. "
      f"Check [computed]: starting from a random rotation of diag(c_Q fitted), N = diag(1, 2, 3), t = {sol.t[-1]:.0f}: eigenvalue drift "
      f"{np.abs(ev1 - ev0).max():.1e}, final max off-diagonal {off:.1e}, final diagonal " + ", ".join(f"{v:.4f}" for v in np.diag(Hend)) +
      " against the fitted c_Q " + ", ".join(f"{v:.4f}" for v in cQ) + ".")
    w("")
    w("## Scope")
    w("")
    w("Zero modes only. KK-gluon exchange and the ε_K bound, which pushes the KK scale to many TeV in anarchic RS, are not tested "
      "[standard: beyond toy; Csáki–Falkowski–Weiler arXiv:0804.1954]. No running between TeV and the throat, no brane-kinetic terms, Higgs exactly on the IR brane.")
    w("")
    w("## Grade lines")
    w("")
    w(f"- Stage A: {gA_solv}; naturalness (every c in ½ ± 0.5): **{gA_nat}** [prediction].")
    w(f"- Stage B: **{B['grade']}**: |V_ub| inside 68% {B['in68'][0]}, inside 95% {B['in95'][0]}; |J| inside 68% {B['in68'][1]}, inside 95% {B['in95'][1]} [prediction].")
    w("")
    w(f"Runtime: {time.time() - T0:.1f} s [computed].")
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
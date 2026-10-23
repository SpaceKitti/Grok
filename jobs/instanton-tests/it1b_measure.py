"""IT1b grading, fixed-time paired response (Venus spec rev 4, out/diag22b/IT1B_FIXEDTIME_FROZEN.md, sha256 C99963A0)
[hive proposal, untested]. Grading only; never used to regrade diag22.
VERDICT: chi=(X_d-X_0)/d at t=0.6, paired per seed. P1 linearity dX(0.003)/dX(0.0015) in 1.7-2.3.
Noise: |dX| at d=0.0015 > seed-to-seed spread, else UNDECIDED. P2 cal shift <= 5%, P3 control < 0.23 (unchanged).
G1, G2, dp, r_d slope: REPORT-ONLY. Meaning: linear response at t=0.6, reduced model (not a settled state)."""
import numpy as np
T_LO, T_SPLIT, T_HI = 0.1, 0.245, 0.6
T_VERDICT = 0.6
NUM_FLOOR = 1e-12  # float round-off floor only, not a physics cut-off
HALF_TOL = 0.10; LIN = (1.7, 2.3); CAL_MAX = 0.05; CTRL_MAX = 0.23
D_LO, D_HI = 0.0015, 0.003
LABEL = "linear response at t=0.6, reduced model"
MEASURE = "out/diag22b/IT1B_FIXEDTIME_FROZEN.md C99963A0"

def _sel(h, a, b):
    h = np.asarray(h, float); m = (h[:, 0] >= a-1e-12) & (h[:, 0] <= b+1e-12); return h[m]

def x_at(hist, t=T_VERDICT):
    """X at exactly t (recorded point); ValueError if absent or non-finite."""
    h = np.asarray(hist, float); m = np.abs(h[:, 0]-t) < 1e-9
    if not m.any(): raise ValueError(f"no X at t={t}")
    x = float(h[m][-1, 1])
    if not np.isfinite(x): raise ValueError(f"non-finite X at t={t}")
    return x

# ---- report-only (old FD9FD866 / AC3738B0 quantities) ----
def fit_p(hist, a=T_LO, b=T_HI):
    """ln X = ln A - p ln t; returns (p, lnA)."""
    h = _sel(hist, a, b); s, c = np.polyfit(np.log(h[:, 0]), np.log(h[:, 1]), 1); return -s, c

def fit_r(hist_d, hist_0, a=T_LO, b=T_HI):
    """r = ln X_d - ln X_0 = dlnA - dp ln t (same t grid)."""
    hd, h0 = _sel(hist_d, a, b), _sel(hist_0, a, b)
    if hd.shape != h0.shape or not np.allclose(hd[:, 0], h0[:, 0]): raise ValueError("time grids differ")
    s, c = np.polyfit(np.log(hd[:, 0]), np.log(hd[:, 1]) - np.log(h0[:, 1]), 1); return -s, c

def _agree(x, y, tol=HALF_TOL):
    m = max(abs(x), abs(y)); return m > 0 and abs(x-y)/m <= tol

def g1(hist_0):
    p1, _ = fit_p(hist_0, T_LO, T_SPLIT); p2, _ = fit_p(hist_0, T_SPLIT, T_HI)
    return dict(p0_h1=p1, p0_h2=p2, ok=bool(_agree(p1, p2)), role="report-only")

def report_delta(rows_d, rows_0):
    """Report-only: paired log-response slope (old 'dp'), intercept, G2 straightness."""
    seeds = sorted(rows_d); per = {}
    for s in seeds:
        dp, dA = fit_r(rows_d[s], rows_0[s]); dp1, _ = fit_r(rows_d[s], rows_0[s], T_LO, T_SPLIT); dp2, _ = fit_r(rows_d[s], rows_0[s], T_SPLIT, T_HI)
        per[s] = dict(dp=dp, dlnA=dA, dp_h1=dp1, dp_h2=dp2)
    dps = np.array([per[s]["dp"] for s in seeds]); sp_p = max(float(np.ptp(dps)), NUM_FLOOR)
    g2 = all(_agree(per[s]["dp_h1"], per[s]["dp_h2"]) or (abs(per[s]["dp_h1"]) <= sp_p and abs(per[s]["dp_h2"]) <= sp_p) for s in seeds)
    return dict(per_seed=per, paired_log_response=float(dps.mean()), dlnA=float(np.mean([per[s]["dlnA"] for s in seeds])),
                spread=sp_p, G2=bool(g2), role="report-only")

def chi_curve(hist_d, hist_0, d):
    hd, h0 = np.asarray(hist_d, float), np.asarray(hist_0, float)
    if hd.shape != h0.shape or not np.allclose(hd[:, 0], h0[:, 0]): raise ValueError("time grids differ")
    return [(float(t), float((xd-x0)/d)) for (t, xd), (_, x0) in zip(hd, h0)]

# ---- verdict quantities ----
def fixed_time(rows_d, rows_0, d, t=T_VERDICT):
    """Per-seed paired dX = X_d(t)-X_0(t); mean, seed spread (max-min), chi = mean/d."""
    seeds = sorted(rows_d); dX = {s: x_at(rows_d[s], t) - x_at(rows_0[s], t) for s in seeds}
    v = np.array([dX[s] for s in seeds]); m = float(v.mean())
    return dict(t=t, delta=d, dX_per_seed=dX, dX=m, spread=float(np.ptp(v)), chi=m/d, n_seeds=len(seeds))

def grade_it1b(hist0_by_alpha, rows, cal_shift, control):
    """hist0_by_alpha[alpha][seed]; rows[alpha][delta][seed]; delta in (0.0015, 0.003). Verdict per alpha."""
    out = {}
    for al, r in rows.items():
        h0 = hist0_by_alpha[al]
        lo, hi = fixed_time(r[D_LO], h0, D_LO), fixed_time(r[D_HI], h0, D_HI)
        noise_ok = abs(lo["dX"]) > max(lo["spread"], NUM_FLOOR)
        ratio = hi["dX"]/lo["dX"] if lo["dX"] != 0 else None
        P1 = ratio is not None and LIN[0] <= ratio <= LIN[1]; P2 = bool(cal_shift <= CAL_MAX); P3 = bool(control < CTRL_MAX)
        verdict = "UNDECIDED" if not noise_ok else ("PASS" if (P1 and P2 and P3) else "FAIL")
        rep = {}
        try:
            rep = dict(G1=g1(next(iter(h0.values()))), d0015=report_delta(r[D_LO], h0), d003=report_delta(r[D_HI], h0),
                       chi_curve={str(d): {str(s): chi_curve(r[d][s], h0[s], d) for s in r[d]} for d in (D_LO, D_HI)})
        except Exception as e: rep = dict(error=f"report-only failed: {e}")
        out[al] = dict(fixed_time={str(D_LO): lo, str(D_HI): hi}, chi=lo["chi"], chi_003=hi["chi"], lin_ratio=ratio,
                       noise_gate=dict(ok=bool(noise_ok), abs_dX=abs(lo["dX"]), seed_spread=lo["spread"]),
                       P1=bool(P1), P2=P2, P3=P3, verdict=verdict, report_only=rep, label=LABEL, measure=MEASURE)
    return out

# ==== rev 6 (out/diag22b/IT1B_REV6_FROZEN.md, sha256 E360229B) [hive proposal, untested] ====
# grade_it1b above is the superseded C99963A0 grader, kept only so old tests/records stay reproducible; rev 6 grades with grade_rev6.
MEASURE6 = "out/diag22b/IT1B_REV6_FROZEN.md E360229B"
D6_LO, D6_HI = 0.003, 0.006
LIN6 = (0.85, 1.15)

def antithetic(rows_pm, hist_0, d, t=T_VERDICT):
    """rows_pm[+d][seed], rows_pm[-d][seed]; hist_0 = the deterministic X0 history (shared by every seed, same RNG-free baseline).
    L_s = (X(+d)-X(-d))/(2d) per seed (verdict); E_s = (X(+d)+X(-d)-2 X0)/d^2 per seed (REPORT-ONLY). Spread = max-min over seeds."""
    seeds = sorted(rows_pm[d]); x0 = x_at(hist_0, t)
    if sorted(rows_pm[-d]) != seeds: raise ValueError("+d and -d seed sets differ")
    L = {s: (x_at(rows_pm[d][s], t) - x_at(rows_pm[-d][s], t))/(2*d) for s in seeds}
    E = {s: (x_at(rows_pm[d][s], t) + x_at(rows_pm[-d][s], t) - 2*x0)/d**2 for s in seeds}
    v = np.array([L[s] for s in seeds]); e = np.array([E[s] for s in seeds])
    return dict(t=t, delta=d, X0=x0, L_per_seed=L, L=float(v.mean()), spread=float(np.ptp(v)), E_per_seed=E, E=float(e.mean()),
                E_role="report-only", n_seeds=len(seeds))

def grade_rev6(hist0_by_alpha, rows, cal_shift, control):
    """hist0_by_alpha[alpha] = X0 history; rows[alpha][signed d][seed], d in {+-0.003, +-0.006}.
    Noise gate (rev 5 text): |mean_s L| > spread_s(L), else UNDECIDED; applied at the smaller d=0.003 (as rev 4 used the smaller d) and
    reported at 0.006. P1: L_s(0.006)/L_s(0.003) in [0.85, 1.15] for EVERY seed. P2 cal |shift| <= 5%. P3 control < 0.23.
    Verdict: UNDECIDED if the noise gate fails, else PASS iff P1 and P2 and P3, else FAIL. chi = mean L at d=0.003."""
    out = {}
    for al, r in rows.items():
        h0 = hist0_by_alpha[al]
        lo, hi = antithetic(r, h0, D6_LO), antithetic(r, h0, D6_HI)
        noise_ok = abs(lo["L"]) > max(lo["spread"], NUM_FLOOR)
        ratios = {s: (hi["L_per_seed"][s]/lo["L_per_seed"][s] if lo["L_per_seed"][s] != 0 else None) for s in lo["L_per_seed"]}
        P1 = all(q is not None and LIN6[0] <= q <= LIN6[1] for q in ratios.values())
        P2 = bool(abs(cal_shift) <= CAL_MAX); P3 = bool(control < CTRL_MAX)
        verdict = "UNDECIDED" if not noise_ok else ("PASS" if (P1 and P2 and P3) else "FAIL")
        out[al] = dict(antithetic={str(D6_LO): lo, str(D6_HI): hi}, chi=lo["L"], chi_006=hi["L"], lin_ratio_per_seed=ratios,
                       lin_ratio_mean=(hi["L"]/lo["L"] if lo["L"] != 0 else None), lin_band=list(LIN6),
                       noise_gate=dict(ok=bool(noise_ok), abs_L=abs(lo["L"]), seed_spread=lo["spread"], at_delta=D6_LO,
                                       report_006=dict(abs_L=abs(hi["L"]), seed_spread=hi["spread"], ok=bool(abs(hi["L"]) > max(hi["spread"], NUM_FLOOR)))),
                       P1=bool(P1), P2=P2, P3=P3, verdict=verdict, label=LABEL, measure=MEASURE6, tag="[hive proposal, untested]")
    return out

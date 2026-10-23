"""IT1b power-law grading (Venus spec IT1B_POWERLAW_FROZEN.md, AE31015E) [hive proposal, untested].
Grading only; never used to regrade diag22. Helios report-only: dp~0 with dlnA linear in delta => 'time-rescale'."""
import numpy as np
T_LO, T_SPLIT, T_HI = 0.1, 0.245, 0.6
NUM_FLOOR = 1e-12  # float round-off floor only, not a physics cut-off
HALF_TOL = 0.10; LIN = (1.7, 2.3); CAL_MAX = 0.05; CTRL_MAX = 0.23

def _sel(h, a, b):
    h = np.asarray(h, float); m = (h[:, 0] >= a-1e-12) & (h[:, 0] <= b+1e-12); return h[m]

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
    return dict(p0_h1=p1, p0_h2=p2, ok=bool(_agree(p1, p2)))

def grade_delta(rows_d, rows_0):
    """rows_d/rows_0: {seed: hist}. Per-delta G2,G3 summary."""
    seeds = sorted(rows_d); per = {}
    for s in seeds:
        dp, dA = fit_r(rows_d[s], rows_0[s]); dp1, _ = fit_r(rows_d[s], rows_0[s], T_LO, T_SPLIT); dp2, _ = fit_r(rows_d[s], rows_0[s], T_SPLIT, T_HI)
        per[s] = dict(dp=dp, dlnA=dA, dp_h1=dp1, dp_h2=dp2)
    dps = np.array([per[s]["dp"] for s in seeds]); dAs = np.array([per[s]["dlnA"] for s in seeds])
    sp_p = max(float(np.ptp(dps)), NUM_FLOOR); sp_A = max(float(np.ptp(dAs)), NUM_FLOOR)
    g2 = all(_agree(per[s]["dp_h1"], per[s]["dp_h2"]) or (abs(per[s]["dp_h1"]) <= sp_p and abs(per[s]["dp_h2"]) <= sp_p) for s in seeds)
    return dict(per_seed=per, dp=float(dps.mean()), dlnA=float(dAs.mean()), spread_dp=sp_p, spread_dlnA=sp_A,
                G2=bool(g2), G3_dp=bool(abs(dps.mean()) > sp_p), G3_dlnA=bool(abs(dAs.mean()) > sp_A))

def grade_it1b(hist0_by_alpha, rows, cal_shift, control):
    """hist0_by_alpha[alpha][seed]; rows[alpha][delta][seed]; delta in (0.0015, 0.003). Returns verdict per alpha."""
    out = {}
    for al, r in rows.items():
        G1 = g1(next(iter(hist0_by_alpha[al].values())))
        d1, d2 = grade_delta(r[0.0015], hist0_by_alpha[al]), grade_delta(r[0.003], hist0_by_alpha[al])
        if d1["G3_dp"] and d2["G3_dp"]: q, ratio = "dp", d2["dp"]/d1["dp"]
        elif d1["G3_dlnA"] and d2["G3_dlnA"]: q, ratio = "dlnA", d2["dlnA"]/d1["dlnA"]
        else: q, ratio = None, None
        gates = G1["ok"] and d1["G2"] and d2["G2"] and q is not None
        P1 = ratio is not None and LIN[0] <= ratio <= LIN[1]; P2 = cal_shift <= CAL_MAX; P3 = control < CTRL_MAX
        verdict = "UNDECIDED" if not gates else ("PASS" if (P1 and P2 and P3) else "FAIL")
        rescale = (not d1["G3_dp"] and not d2["G3_dp"] and q == "dlnA" and P1)
        out[al] = dict(G1=G1, d0015=d1, d003=d2, lin_quantity=q, lin_ratio=ratio, P1=P1, P2=P2, P3=P3, verdict=verdict,
                       helios_note=("time-rescale [report-only]" if rescale else None))
    return out


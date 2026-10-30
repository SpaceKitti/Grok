import json, time, numpy as np
from cone_v1_4 import *
DR = W_N / 40      # <= w_N/20 everywhere (F-M rule satisfied for all cases)
LO, HI = W_N / 4, W_N   # FLAG: V1_2 window [2w_N, 0.5 r_c] is empty here (2w_N=0.85 > 0.75); tip window used instead
rows = []
cases = [(al, n, False) for al in (0.9, 0.75, 0.5, 1/3) for n in (1, 2)] + [(2.0, 1, True), (2.0, 2, True)]
for al, n, side in cases:
    t = time.time(); s1 = solve(al, n, DR); s2 = solve(al, n, DR / 2)
    p1, p2 = fit_p(s1, LO, HI), fit_p(s2, LO, HI); pp = n / al
    Qs = [Q_lattice(s2, n, al, A) for A in (RHO/3, RHO/4, RHO/5)]
    A2 = np.array([1/9, 1/16, 1/25]); c = np.polyfit(A2, Qs, 1); Q0 = float(c[1])
    row = dict(alpha=al, n=n, side=side, Q_a3=Qs[0], Q_a4=Qs[1], Q_a5=Qs[2], Q0=Q0, Q_pred=n, dQ=Q0 - n,
               a_eq=float(s2["a"][-1]), p_fit=p2, p_fit_coarse=p1, p_pred=pp, p_pass=bool(abs(p2-pp) <= 0.05*pp and abs(p2-p1) < 0.02*pp),
               E_over_pin=s2["E"]/(np.pi*n), E_tip=tip_energy(s2, n, al, W_N), curv=curvature_check(al)[2], conv=[s1["ok"], s2["ok"]])
    if side:
        Qsh = [Q_lattice(s2, n, al, A, frac=0.5) for A in (RHO/3, RHO/4, RHO/5)]; row["Q_sheet0"] = float(np.polyfit(A2, Qsh, 1)[1])
        row["double_cover_ok"] = abs(Q0 - 2*row["Q_sheet0"]) <= 0.02
    if abs(al - 0.5) < 1e-12:   # Z2 cross-check: flat plane winding 2n, read Q/2
        sp = solve(1.0, 2*n, DR/2); Qp = [Q_lattice(sp, 2*n, 1.0, A) for A in (RHO/3, RHO/4, RHO/5)]
        row["Q_Z2"] = float(np.polyfit(A2, Qp, 1)[1]) / 2; row["Z2_ok"] = abs(row["Q_Z2"] - Q0) <= 0.01
        row["kQ_ok"] = abs(2*Q0 - round(2*Q0)) <= 0.04
    row["sec"] = round(time.time() - t, 1); rows.append(row); print(json.dumps(row), flush=True)
main = [r for r in rows if not r["side"]]
for n in (1, 2):
    d = [r["dQ"] for r in main if r["n"] == n]
null = all(abs(r[k] - r["Q_pred"]) <= 0.02 for r in main for k in ("Q_a3", "Q_a4", "Q_a5", "Q0"))
sup = all(abs(r[k] - r["Q_pred"]) > 0.05 for r in main for k in ("Q_a3", "Q_a4", "Q_a5"))
verdict = "NULL" if null else ("SUPPORTED(check smoothness)" if sup else "UNDECIDED")
json.dump(dict(rows=rows, verdict=verdict, dr=DR, fit_window=[LO, HI], Rs=RS, w_N=W_N), open("CONE_RESULTS_V1_4.json", "w"), indent=1)
print("VERDICT", verdict)

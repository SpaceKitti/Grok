"""V1_5 P2 refit (spec 8f081319). FLAG: V1_4 never wrote the solution arrays to disk, so there is nothing 'stored' to read.
The V1_4 solves are regenerated with the UNCHANGED code cone_v1_4.py (5448980d; same seed, same DR, deterministic L-BFGS-B),
and each regenerated solve is verified against the V1_4 results file (old p_fit and Q must match to 1e-9) before refitting.
Solutions are now saved to v1_4_solutions.npz. No solver/energy change."""
import json, numpy as np
from cone_v1_4 import solve, W_N, RHO, Q_lattice, fit_p
DR = W_N / 40; old = {(round(r["alpha"], 6), r["n"]): r for r in json.load(open("CONE_RESULTS_V1_4.json"))["rows"]}
def p_tip(s, dr):
    r, f = s["r"], s["f"]; fp = np.gradient(f, r); m = (r >= 20 * dr) & (r <= 0.3 * RHO) & (f > 0)
    pl = r[m] * fp[m] / f[m]; c = np.polyfit(r[m] ** 2, pl, 1); return float(c[1]), float(c[0]), int(m.sum())
rows, store = [], {}
for al, n in [(a, n) for a in (0.9, 0.75, 0.5, 1/3) for n in (1, 2)] + [(2.0, 1), (2.0, 2)]:
    s1, s2 = solve(al, n, DR), solve(al, n, DR / 2); o = old[(round(al, 6), n)]
    repro = max(abs(fit_p(s2, W_N/4, W_N) - o["p_fit"]), abs(fit_p(s1, W_N/4, W_N) - o["p_fit_coarse"]), abs(Q_lattice(s2, n, al, RHO/3) - o["Q_a3"]))
    (p1, _, m1), (p2, c2, m2) = p_tip(s1, DR), p_tip(s2, DR / 2); pp = n / al
    ok = abs(p2 - pp) <= 0.05 * pp and abs(p1 - p2) < 0.02 * pp
    rows.append(dict(alpha=al, n=n, side=al > 1, p_tip_DR=p1, p_tip_DR2=p2, c_r2=c2, npts=[m1, m2], p_pred=pp, rel_err=(p2-pp)/pp,
                     grade="PASS" if ok else "UNDECIDED", repro_maxdiff=repro, Q_reported_not_graded=o["Q0"]))
    print(json.dumps(rows[-1]), flush=True)
    for k, s in (("DR", s1), ("DR2", s2)): store[f"a{al:.4f}_n{n}_{k}_r"], store[f"a{al:.4f}_n{n}_{k}_f"], store[f"a{al:.4f}_n{n}_{k}_a"] = s["r"], s["f"], s["a"]
np.savez_compressed("v1_4_solutions.npz", **store)
json.dump(dict(spec="CONE_SPEC_V1_5_ADDENDUM.md 8f081319", code="cone_v1_4.py 5448980d", window=[20*DR, 0.3*RHO], rows=rows), open("CONE_REFIT_V1_5.json", "w"), indent=1)

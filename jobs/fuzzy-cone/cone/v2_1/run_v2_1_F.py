import json, datetime, hashlib, numpy as np
from run_v2_1_E import solve, h8
pred = json.load(open("PREDICTIONS_V2_1_F.json"))
rows = []
for p in pred["points"]:
    r = solve(p["theta"], p["N"], p["n"], 1000.0); r["mu_pred"] = p["mu_pred"]
    r["a_ok"] = all(abs(r[k] - p["mu_pred"]) <= 0.02 for k in ("mu_N", "mu_S")); r["in_valid_range"] = r["bradlow"] >= 3.8; rows.append(r)
fits = {}
for t in (0.25, 1.5):
    for n in (1, 2):
        rw = sorted([r for r in rows if r["theta"] == t and r["n"] == n], key=lambda r: r["N"]); N = np.array([r["N"] for r in rw], float)
        f = {}
        for pl in "NS":
            g = np.array([r["gap_" + pl] for r in rw]); c = np.linalg.solve(np.vstack([np.ones(2), 1 / N]).T, g)
            f["gap_" + pl] = dict(g_inf=float(c[0]), c=float(c[1]), sigma=None, note="2 points, 0 dof: sigma not estimable")
        f["b_ok"] = False; fits[f"theta{t}_n{n}"] = f
a = all(r["a_ok"] for r in rows); c = all(r["conv"] for r in rows)
out = dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           specs={"V2_1": h8("../FUZZY_CONE_SPEC_V2_1.md"), "B": "4e265cbd", "C": "86b8052f", "D": h8("../FUZZY_CONE_SPEC_V2_1_ADDENDUM_D.md"), "E": h8("../FUZZY_CONE_SPEC_V2_1_ADDENDUM_E.md"), "F": h8("../FUZZY_CONE_SPEC_V2_1_ADDENDUM_F.md")},
           code=h8("fuzzy_cone_v2_1.py"), continuum=h8("continuum_two_pole.py"), predictions=h8("PREDICTIONS_V2_1_F.json"), runner=h8("run_v2_1_F.py"), runner_lib=h8("run_v2_1_E.py"),
           rows=rows, fits=fits, grades=dict(a=a, b=False, b_note="sigma undefined with 2 N per (theta,n); 3-sigma not demonstrable", c=c),
           F2_round3="PASS" if (a and c and False) else "UNDECIDED (to Akitti)")
json.dump(out, open("RESULT_V2_1_F.json", "w"), indent=1)
for r in rows: print(r["theta"], r["n"], r["N"], round(r["bradlow"], 2), r["conv"], r["nit"], round(r["mu_N"], 4), round(r["mu_S"], 4), round(r["mu_pred"], 4), r["a_ok"], round(r["gap_N"], 4), round(r["gap_S"], 4), r["sec"])
print(json.dumps(fits), out["grades"], out["F2_round3"])

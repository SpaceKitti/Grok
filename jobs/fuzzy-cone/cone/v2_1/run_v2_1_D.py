"""Addendum D (372ebe02) F4 round 2: per-pole mu/(pi|n|), n=1,2, N=31,51,71,101, code 63b69fbc unchanged, fuzzy seed."""
import json, datetime, time, hashlib, sys, numpy as np
from fuzzy_cone_v2_1 import Model, relax, observe
WRAD = float(sys.argv[1]) if len(sys.argv) > 1 else 1000.0
h = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()[:8]
out = dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           specs={"V2_1": "9dbd2f86", "B": "4e265cbd", "C": "86b8052f", "D": h("../FUZZY_CONE_SPEC_V2_1_ADDENDUM_D.md")},
           code="fuzzy_cone_v2_1.py " + h("fuzzy_cone_v2_1.py"), predictions="PREDICTIONS_V2_1_D.json " + h("PREDICTIONS_V2_1_D.json"),
           R=3.0, wrad=WRAD, rows=[])
for n in (1, 2):
    for N in (31, 51, 71, 101):
        t = time.time(); M = Model(N, n, wrad=WRAD); x, E, ok, it = relax(M, M.seed_fuzzy()); o = observe(M, x)
        r = dict(n=n, N=N, conv=ok, nit=it, E_over_2pin=E / (2 * np.pi * n), mu_N=o["profiles"]["north"]["mu"] / (np.pi * n),
                 mu_S=o["profiles"]["south"]["mu"] / (np.pi * n), sec=round(time.time() - t, 1))
        out["rows"].append(r); print(r, flush=True)
grades = {}
for n in (1, 2):
    rows = [r for r in out["rows"] if r["n"] == n]; N = np.array([r["N"] for r in rows], float); conv = all(r["conv"] for r in rows)
    ns = max(abs(r["mu_N"] - r["mu_S"]) for r in rows); g = dict(conv_all=conv, max_NS_diff=ns)
    for pole in ("N", "S"):
        mu = np.array([r["mu_" + pole] for r in rows])
        A1 = np.vstack([np.ones_like(N), 1 / N]).T; c1, *_ = np.linalg.lstsq(A1, mu, rcond=None); res = float(np.max(np.abs(A1 @ c1 - mu)))
        A2 = np.vstack([np.ones_like(N), 1 / N, 1 / N**2]).T; c2, *_ = np.linalg.lstsq(A2, mu, rcond=None)
        inband = abs(c1[0] - 1) <= 0.02; fitok = res <= 0.002 and abs(c2[0] - c1[0]) <= 0.01
        grade = "PASS" if (inband and fitok and ns <= 0.005 and conv) else ("UNDECIDED" if (inband and not fitok and ns <= 0.005 and conv) else "FAIL")
        g[pole] = dict(mu_inf=float(c1[0]), b=float(c1[1]), max_resid=res, fit2=dict(mu_inf=float(c2[0]), b=float(c2[1]), d=float(c2[2])),
                       shift=float(c2[0] - c1[0]), grade=grade)
    g["F4"] = "PASS" if all(g[p]["grade"] == "PASS" for p in "NS") else ("FAIL" if any(g[p]["grade"] == "FAIL" for p in "NS") else "UNDECIDED")
    grades[n] = g
out["grades"] = grades; json.dump(out, open("RESULT_V2_1_D.json", "w"), indent=1); print(json.dumps(grades, indent=1))

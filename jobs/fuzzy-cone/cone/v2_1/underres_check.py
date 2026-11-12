import json, datetime, numpy as np, hashlib
from fuzzy_cone_v2_1 import Model, relax, observe
th, N, n = 2.0, 141, 2; R = float(np.sqrt(th * np.sqrt(N**2 - 1) / 2)); out = dict(theta=th, N=N, n=n, R=R, runs={})
d = np.load("sol_v2_1_E_t2.0_n2_N141.npz"); M = Model(N, n, R=R, wrad=1000.0); o = observe(M, d["x"])
out["runs"]["1000_saved"] = dict(E2pin=float(d["E"]) / (4 * np.pi), radial_resid=o["radial_resid"], Qtot=o["Q_total"], QN=o["Q_cap_N"])
M = Model(N, n, R=R, wrad=10000.0); x, E, ok, it = relax(M, M.seed_fuzzy()); o = observe(M, x)
out["runs"]["10000"] = dict(E2pin=E / (4 * np.pi), conv=ok, nit=it, radial_resid=o["radial_resid"], Qtot=o["Q_total"], QN=o["Q_cap_N"], muN=o["profiles"]["north"]["mu"] / (2 * np.pi))
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat(); json.dump(out, open("UNDERRES_CHECK_E.json", "w"), indent=1); print(json.dumps(out, indent=1))

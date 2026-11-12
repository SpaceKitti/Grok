import json, numpy as np, jax, datetime
from scipy.optimize import minimize
from fuzzy_cone_v2_1 import Model
from run_v2_1_E import h8
t, N, n = 0.25, 101, 1; R = float(np.sqrt(t * np.sqrt(N**2 - 1) / 2)); M = Model(N, n, R=R, wrad=1000.0)
E = jax.jit(M.energy); G = jax.jit(jax.grad(E))
r = minimize(lambda x: float(E(x)), M.seed_fuzzy(), jac=lambda x: np.asarray(G(x)), method="L-BFGS-B", options=dict(maxiter=200000, maxfun=400000, ftol=1e-20, gtol=1e-13, maxcor=100))
from run_v2_1_E import observe
o = observe(M, r.x); f = "sol_v2_1_F_tight_t0.25_n1_N101.npz"; np.savez_compressed(f, x=r.x, E=r.fun, conv=r.success, nit=r.nit)
d = json.load(open("RESULT_V2_1_F.json"))
d["tight_rerun"] = dict(point=[t, n, N], options="ftol 1e-20 gtol 1e-13 maxcor 100", conv=bool(r.success), nit=int(r.nit), message=str(r.message), E=float(r.fun),
    mu_N=o["profiles"]["north"]["mu"] / np.pi, mu_S=o["profiles"]["south"]["mu"] / np.pi, npz=[f, h8(f)])
d["grades"]["c"] = all(x["conv"] or (x["theta"], x["n"], x["N"]) == (t, n, N) and r.success for x in d["rows"])
d["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat(); d["tight_runner"] = h8("tight_F.py")
json.dump(d, open("RESULT_V2_1_F.json", "w"), indent=1); print(d["tight_rerun"], d["grades"], d["timestamp"])

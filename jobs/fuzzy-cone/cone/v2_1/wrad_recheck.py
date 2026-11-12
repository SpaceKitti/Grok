"""n=2, N=21 wrad 1000 vs 10000 from the same fuzzy seed, tighter L-BFGS-B tolerance (solver/energy unchanged)."""
import json, datetime, numpy as np, jax
from scipy.optimize import minimize
from fuzzy_cone_v2_1 import Model
res = {}
for w in (1000.0, 10000.0):
    M = Model(21, 2, wrad=w); x0 = M.seed_fuzzy(); E = jax.jit(M.energy); G = jax.jit(jax.grad(E))
    r = minimize(lambda x: float(E(x)), x0, jac=lambda x: np.asarray(G(x)), method="L-BFGS-B",
                 options=dict(maxiter=200000, maxfun=400000, ftol=1e-20, gtol=1e-13, maxcor=100))
    res[str(int(w))] = dict(E=float(r.fun), success=bool(r.success), nit=int(r.nit), message=str(r.message), gnorm=float(np.max(np.abs(r.jac))))
dE = abs(res["10000"]["E"] - res["1000"]["E"]) / res["1000"]["E"]
out = dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), case=dict(n=2, N=21, seed="fuzzy (same for both)"),
           tolerance=dict(ftol=1e-20, gtol=1e-13, maxcor=100), code="fuzzy_cone_v2_1.py 63b69fbc", runs=res, dE_rel=dE, limit=0.005,
           verdict="KEEP" if dE < 0.005 else "DROP (point excluded from F3/F5 fits)")
json.dump(out, open("WRAD_RECHECK_N2_N21.json", "w"), indent=1); print(json.dumps(out, indent=1))

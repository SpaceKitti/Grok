import json, datetime, hashlib, numpy as np, jax.numpy as jnp
from fuzzy_cone_v2_1 import Model, relax, symbol_diag
from continuum_two_pole import _shoot
from scipy.optimize import brentq
h8 = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
R = 3.0; th = np.linspace(0, np.pi, 2001); H = 5e-4
def cont(n):
    a = brentq(lambda a: _shoot(a, n, R, H).y[1, -1], -10, 10, xtol=1e-13); s = _shoot(a, n, R, H)
    t = np.minimum(th, np.pi - th); t = np.clip(t, 1e-4, np.pi / 2); return 0.5 * (1 - np.exp(np.minimum(s.sol(t)[0], 50)))
out = dict(timestamp=None, specs={"V2_1": h8("../FUZZY_CONE_SPEC_V2_1.md"), "B": "4e265cbd", "C": "86b8052f", "D": h8("../FUZZY_CONE_SPEC_V2_1_ADDENDUM_D.md")},
           code=h8("fuzzy_cone_v2_1.py"), continuum=h8("continuum_two_pole.py"), predictions=h8("PREDICTIONS_V2_1_F1F2.json"), runner=h8("run_v2_1_F1F2.py"),
           rows=[], npz={}, grades={})
for n in (1, 2):
    bc = cont(n); pk = np.max(np.abs(bc))
    for N in (21, 81, 101):
        M = Model(N, n, R=R, wrad=1000.0); x, E, ok, it = relax(M, M.seed_fuzzy())
        X, P, B, K, rad = M.pieces(x); B = np.asarray(B)
        f = f"sol_v2_1_n{n}_N{N}.npz"; np.savez_compressed(f, x=x, B=B, N=N, n=n, R=R, wrad=1000.0, E=E, conv=ok, nit=it); out["npz"][f] = h8(f)
        bs = symbol_diag(M, B, th); err = np.abs(bs - bc) / pk; r = R * th
        out["rows"].append(dict(n=n, N=N, conv=ok, nit=it, E=E, sup_err=float(err.max()), argmax_r_from_N=float(r[err.argmax()]),
                                gap_N=float(err[r <= 3].max()), gap_S=float(err[r >= np.pi * R - 3].max()), err_mid=float(err[(r > 3) & (r < np.pi * R - 3)].max())))
        print(out["rows"][-1], flush=True)
for n in (1, 2):
    rw = [r for r in out["rows"] if r["n"] == n]; N = np.log([r["N"] for r in rw]); g = {}
    sup = [r["sup_err"] for r in rw]
    g["F1"] = dict(sup_err=sup, sup_at_101=sup[-1], decreasing=bool(sup[0] > sup[1] > sup[2]), grade="PASS" if sup[-1] <= 0.01 and sup[0] > sup[1] > sup[2] else "FAIL")
    for p in "NS":
        gp = [r["gap_" + p] for r in rw]; sl = float(np.polyfit(N, np.log(gp), 1)[0])
        g["F2_" + p] = dict(gap=gp, slope=sl, grade="PASS" if gp[0] >= 0.05 and -1.5 <= sl <= -0.5 else ("FAIL" if gp[0] < 0.05 else ("BUG-FLAG (gap not shrinking)" if sl >= 0 else "FAIL")))
    g["all_converged"] = all(r["conv"] for r in rw); out["grades"][n] = g
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("RESULT_V2_1_F1F2.json", "w"), indent=1); print(json.dumps(out["grades"], indent=1))

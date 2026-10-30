"""Pure-gauge comparison (statics): A = 0, A' = i h dh^+ with h = h_v4 (antipode_v4), one (x3,x4) site; fuzzy cap action."""
import json, sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fuzzy_instanton import Model, trprod
import run_it1b as r
from weyl_seed import SeedField
cfg = json.load(open(os.path.join(HERE, "it1b_fuzzy_config_v4.json")))
N, eps, x3, x4 = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]); R = 5.0
mc = r.model_cfg(cfg, 5); mc["gauge"] = None
m = Model(mc, N, 1, R, 1.0); W = m._weyl(); n = W.n
sf = SeedField(R, 1.0, 1e9, 2e9, {"mode": "antipode_v4", "eps": eps})
den = 1 + n[2]; X = np.stack([2 * R * n[0] / den, 2 * R * n[1] / den, np.full(den.shape, x3), np.full(den.shape, x4)])
A = sf._antipode_v4(np.zeros((2, 3) + den.shape), X, (0, 1), eps, R)       # chart mu = 0,1
c = 2 / den; d = -2 / (R * den**2); Xe = R * n
Ae = np.stack([A[0] * c, A[1] * c, A[0] * Xe[0] * d + A[1] * Xe[1] * d])
At = Ae - n[:, None] * (Ae * n[:, None]).sum(0)[None]
Ahat = R * np.cross(At, n[:, None] * np.ones_like(At), axis=0)
B = m._lift(W.quantize(Ahat)) + np.array(m.Lfull); B = 0.5 * (B + B.conj().swapaxes(-1, -2))
cc = m.wcap * m.a**2 / R**4; s = 0.0
for (i, j, kk, e) in [(0, 1, 2, 1.0), (0, 2, 1, -1.0), (1, 2, 0, 1.0)]:
    F = B[i] @ B[j] - B[j] @ B[i] - 1j * e * B[kk]; s += cc * (-trprod(F, F).real)
res = {"N": N, "eps": eps, "x3": x3, "x4": x4, "a_over_rho": m.a, "cap_site_over_8pi2": float(s / (8 * np.pi**2)), "max_Ahat": float(np.abs(Ahat).max())}
json.dump(res, open(os.path.join(HERE, "out", "seed_v4", "puregauge", f"N{N}_eps{eps}_x{x3}_{x4}.json"), "w"), indent=1)
print(json.dumps(res), flush=True)

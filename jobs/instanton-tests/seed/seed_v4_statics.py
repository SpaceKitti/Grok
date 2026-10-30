"""V4 seed statics (SEED_PASS_RULES_V4 73b3cae4): regular gauge + h = G^-s on the antipode cap. Usage: N L eps [a_over_rho]."""
import json, sys, time, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fuzzy_instanton import Model, trprod, lam_of
import run_it1b as r
from grading_it1b import box_fraction
cfg = json.load(open(os.path.join(HERE, "it1b_fuzzy_config_v4.json")))
N, L, eps = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]); aor = float(sys.argv[4]) if len(sys.argv) > 4 else 1 / 3
mc = r.model_cfg(cfg, L); mc["a"] = aor; mc["taper_r0_over_R"], mc["taper_r1_over_R"] = 1e9, 2e9
mc["gauge"] = {"mode": "antipode_v4", "eps": eps}
R = 5.0; m = Model(mc, N, 1, R, 1.0); t = time.time(); B, U = m.seed(1.0); ts = time.time() - t
S, dens, _, _ = m.action_grad(B, U, want_grad=False, per_site=True)
a, w = m.a, m.wcap; d = np.zeros((m.L3, m.L4))
for (i, j, kk, e) in [(0, 1, 2, 1.0), (0, 2, 1, -1.0), (1, 2, 0, 1.0)]:
    F = B[i] @ B[j] - B[j] @ B[i] - 1j * e * B[kk]; d += w * a**2 / R**4 * (-trprod(F, F).real)
k = 8 * np.pi**2; h = (L / 2 - 2) * a; lam = lam_of(R, N)
res = {"N": N, "L": L, "a_over_rho": a, "eps": eps, "h_over_rho": h, "x": lam**2, "S_over_8pi2": float(dens[m.interior].sum() / k),
       "target": box_fraction(h), "cap": float(d[m.interior].sum() / k), "Q": float(m.charge(B, U)), "nsub": mc["nsub"],
       "link_quadrature": "midpoint, nsub sub-steps (2nd order)", "seed_s": ts}
res["cap_over_N2"] = res["cap"] / N**2
p = os.path.join(HERE, "out", "seed_v4", f"N{N}_L{L}_eps{eps}_a{a:.4f}.json"); json.dump(res, open(p, "w"), indent=1)
print(json.dumps(res), flush=True)

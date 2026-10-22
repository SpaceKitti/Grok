# [SCRATCH H5] [hive proposal, untested] Gauge sector at xi = 1, 5/lambda_min, 10/lambda_min (grid 48), plus HP2 5-vs-10 guard (grid 24). Box only.
# mu = lambda_gauge/xi. For an exact pure-gauge direction v = G eps (H v = 0 at a stationary background), lambda_gauge = xi * mu with mu
# an eigenvalue of G^T G, so mu must not depend on xi. RULE (fixed before running): |mu(xi) - mu(xi')|/mu > 1e-6 => flag
# "gauge-physical mixing". HP2 guard: per alpha, 24... (here 8) window eigenvalues equal at 4 s.f. and tracking labels identical.
import sys, os, json; sys.argv = ["x", "--smoke"]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "run.py"), encoding="utf-8").read().replace('if __name__ == "__main__":\n    main()', ''))
from scipy.sparse.linalg import LinearOperator, eigsh
NEV, NG, MIX = 24, 5, 1e-6
def ops(L, x):
    G = L.gauge_sparse(x); GT = G.T.tocsr(); gfun = jax.grad(L.energy); xj = jnp.asarray(x)
    hvp = jax.jit(lambda v: jax.jvp(gfun, (xj,), (v,))[1])
    return G, GT, lambda v, xi: np.asarray(hvp(jnp.asarray(v))) + xi*(G @ (GT @ v))
def lowest(opf, n, xi, nev):
    op = LinearOperator((n, n), dtype=float, matvec=lambda v: opf(np.ravel(v), xi))
    w, V = eigsh(op, k=nev, which="SA", tol=THR["LANCZOS_TOL"], ncv=max(3*nev, 40), maxiter=20000)
    o = np.argsort(w); return w[o], V[:, o]
def gap(w):
    return next((lv for lv in w if abs(lv) > THR["C4_gap_split"]*max(abs(w[0]), 1e-300)), float("nan"))
out = {"tag": "[SCRATCH H5] [hive proposal, untested]", "cases": [], "hp2_guard": []}
mumin = {}
for (n, k, al) in [(1, 2.0, 0.75), (1, 2.0, 1.0), (2, 1.0, 0.5), (2, 1.0, 1.0)]:
    L = ConeLattice(48, 48, 10.0, al, k, n)
    x, E, g, it = L.relax(L.seed([(0.0, 0.0, n)]), 5000)
    G, GT, opf = ops(L, x)
    mu, eps = eigsh((GT @ G).tocsc(), k=NG, sigma=0, which="LM")
    o = np.argsort(mu); mu, eps = mu[o], eps[:, o]
    lmin = float(mu[0]); mumin[(n, k, al)] = lmin
    xis = {"1": 1.0, "5/lmin": 5.0/lmin, "10/lmin": 10.0/lmin}
    # Rayleigh quotients on the pure-gauge directions v = G eps
    mu_eff = {}
    for lab, xi in xis.items():
        r = []
        for j in range(NG):
            v = G @ eps[:, j]; v /= np.linalg.norm(v)
            r.append(float(v @ opf(v, xi))/xi)
        mu_eff[lab] = r
    mix = [j for j in range(NG) if max(abs(mu_eff[a][j]-mu_eff[b][j]) for a in xis for b in xis)/mu[j] > MIX]
    # xi = 1 window: which modes are gauge-dominated, where they sit vs lambda_gap and window top (code xi spectrum)
    w1, V1 = lowest(opf, L.ndof, 1.0, NEV)
    leak1 = np.linalg.norm(GT @ V1, axis=0)
    wc, Vc = lowest(opf, L.ndof, 10.0/lmin, NEV)
    lg, top = float(gap(wc)), float(wc[-1])
    gm = [float(v) for v, l in zip(w1, leak1) if l >= 1e-3]
    rec = dict(n=n, kappa=k, alpha=al, grid=48, max_grad=g, lambda_min_GtG=lmin, mu_GtG=[float(m) for m in mu], mu_eff=mu_eff,
               mixing_flag_modes=mix, xi1_gauge_count_in_window=len(gm), xi1_gauge_eigs=gm, lambda_gap_codexi=lg, window_top=top,
               xi1_gauge_below_gap=sum(1 for v in gm if v < lg), xi1_gauge_below_top=sum(1 for v in gm if v < top))
    out["cases"].append(rec)
    print(f"[SCRATCH H5] n={n} k={k} a={al}: mu_min={lmin:.5e}; mu_eff(1,5,10)[0]={mu_eff['1'][0]:.6e},{mu_eff['5/lmin'][0]:.6e},{mu_eff['10/lmin'][0]:.6e}; mixing={mix}; "
          f"xi=1 gauge in window={len(gm)} eigs={[f'{v:.4e}' for v in gm]}; below gap({lg:.4e})={rec['xi1_gauge_below_gap']}; window top {top:.4e}", flush=True)
for c in out["cases"]:
    c["mu_min_ratio_to_alpha1"] = c["lambda_min_GtG"]/mumin[(c["n"], c["kappa"], 1.0)]
    print(f"  ratio mu_min(alpha={c['alpha']})/mu_min(alpha=1) [n={c['n']},k={c['kappa']}] = {c['mu_min_ratio_to_alpha1']:.5f}")
# HP2 guard, small: n=1, kappa=1, alpha 1 -> 0.5 (3 steps), grid 24, 8 levels
okhp2 = True
res = {}
for f in (5.0, 10.0):
    THR["XI_FACTOR"] = f
    res[f] = _hp2_series((1, 1.0, [1.0, 0.75, 0.5], 24, 24, 8.0, 3000, 8))
for r5, r10 in zip(res[5.0], res[10.0]):
    same = (f"{r5[4]:.3e}" == f"{r10[4]:.3e}") and (r5[6] == r10[6])
    okhp2 &= same
    out["hp2_guard"].append(dict(alpha=r5[2], level=r5[3], lam5=r5[4], lam10=r10[4], ov5=None if np.isnan(r5[5]) else r5[5],
                                 ov10=None if np.isnan(r10[5]) else r10[5], track5=r5[6], track10=r10[6], same=same))
print("HP2_GUARD", "PASS" if okhp2 else "FAIL", f"({len(res[5.0])} level rows)")
out["hp2_guard_pass"] = okhp2
out["mixing_any"] = any(c["mixing_flag_modes"] for c in out["cases"])
os.makedirs("out_scratch", exist_ok=True)
json.dump(out, open("out_scratch/gauge_sector_SCRATCH_hive_proposal.json", "w"), indent=1)
print("MIXING_FLAG", out["mixing_any"])

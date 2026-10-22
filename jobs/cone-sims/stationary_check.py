# [SCRATCH H5] Venus ruling 1 check: polish 4 backgrounds (grid 48) to stationarity, then gauge-sector mixing at xi = 1/5/10,
# the n=2 -3.1e-5 mode, and ruling-2 tau0 counts. Box only. Rules fixed before running:
#  stationary iff |grad|_2 <= min|lambda in 24-window| / 10;  mixing iff mu spread > 1e-6 rel;
#  tau0 = 10 x max|lambda| over the K known zero modes of the alpha=1 control (K = 2n at kappa=1, else 2); alpha<1 count = #(|lambda| <= tau0);
#  undecided iff any eigenvalue in [tau0/3, 3 tau0].
import sys, os, json; sys.argv = ["x", "--smoke"]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "run.py"), encoding="utf-8").read().replace('if __name__ == "__main__":\n    main()', ''))
out = {"tag": "[SCRATCH H5] [hive proposal, untested] gauge sector; ruling-2 tau0 counts", "cases": {}}
order = [(1, 2.0, 1.0), (1, 2.0, 0.75), (2, 1.0, 1.0), (2, 1.0, 0.5)]   # alpha=1 controls first: tau0 fixed before alpha<1
tau0 = {}
for (n, k, al) in order:
    L = ConeLattice(48, 48, 10.0, al, k, n)
    x, E, gmax0, it = L.relax(L.seed([(0.0, 0.0, n)]), 30000)
    g20 = float(np.linalg.norm(np.asarray(jax.grad(L.energy)(x))))
    x, g2, gmax, hist = L.polish(x)
    w, V, xi = L.spectrum(x, 24)
    minlam = float(np.min(np.abs(w)))
    stat = g2 <= minlam/THR["STAT_FACTOR"]
    mu0, eff, mix = L.gauge_sector(x, xi)
    spread = max(abs(eff[a][j]-eff[b][j])/eff["10/lmin"][j] for a in eff for b in eff for j in range(5))
    rec = dict(n=n, kappa=k, alpha=al, lbfgs_iters=it, grad2_after_lbfgs=g20, grad2=g2, gradmax=gmax, polish_hist=hist,
               min_abs_lambda=minlam, stationary=stat, lowest6=[float(v) for v in w[:6]], mu_min=mu0, mu_eff=eff, mixing=mix, mu_spread_rel=spread)
    K = 2*n if k == 1.0 else 2
    if al == 1.0:
        zs = sorted(np.abs(w))[:K]; tau0[(n, k)] = THR["TAU0_FACTOR"]*float(zs[-1]); rec.update(K_known=K, tau0=tau0[(n, k)])
    else:
        t = tau0[(n, k)]; cnt = int(np.sum(np.abs(w) <= t))
        und = [float(v) for v in w if t/THR["UNDECIDED_BAND"] <= abs(v) <= t*THR["UNDECIDED_BAND"]]
        rec.update(tau0=t, count=cnt, undecided=bool(und), band_eigs=und)
    out["cases"][f"n{n}_k{k}_a{al}"] = rec
    print(f"[SCRATCH H5] n={n} k={k} a={al}: lbfgs it={it} |g|2 {g20:.2e} -> polish {g2:.2e} (max {gmax:.2e}); min|lam|={minlam:.3e}; stationary={stat}; "
          f"lowest4={[f'{v:.5e}' for v in w[:4]]}; mu_min={mu0:.6e} spread={spread:.1e} mixing={mix}; "
          + (f"K={K} tau0={rec['tau0']:.3e}" if al == 1.0 else f"tau0={rec['tau0']:.3e} count={rec['count']} undecided={rec['undecided']} band={rec['band_eigs']}"), flush=True)
for key, c in out["cases"].items():
    ref = out["cases"][f"n{c['n']}_k{c['kappa']}_a1.0"]["mu_min"]; c["mu_ratio_report_only"] = c["mu_min"]/ref
os.makedirs("out_scratch", exist_ok=True)
json.dump(out, open("out_scratch/stationary_check_SCRATCH.json", "w"), indent=1)
print("done")

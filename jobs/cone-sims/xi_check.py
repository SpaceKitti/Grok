# [SCRATCH H5] xi = 1 (spec) vs xi = XI_FACTOR/lambda_min(G^T G) (code) gauge-fixing check at grid 48. Not a result.
import sys, os; sys.argv = ["x", "--smoke"]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "run.py"), encoding="utf-8").read().replace('if __name__ == "__main__":\n    main()', ''))
from scipy.sparse.linalg import LinearOperator, eigsh
def spec_xi(L, x, nev, xi):
    G = L.gauge_sparse(x); GT = G.T.tocsr(); gfun = jax.grad(L.energy); xj = jnp.asarray(x)
    hvp = jax.jit(lambda v: jax.jvp(gfun, (xj,), (v,))[1])
    op = LinearOperator((L.ndof, L.ndof), dtype=float, matvec=lambda v: np.asarray(hvp(jnp.asarray(np.ravel(v)))) + xi*(G @ (GT @ np.ravel(v))))
    w, V = eigsh(op, k=nev, which="SA", tol=THR["LANCZOS_TOL"], ncv=max(3*nev, 40), maxiter=20000)
    o = np.argsort(w); w, V = w[o], V[:, o]
    return w, np.linalg.norm(GT @ V, axis=0)/np.linalg.norm(V, axis=0)
NEV = 24
ok_all = True
for (n, k, al) in [(1, 2.0, 0.75), (2, 1.0, 0.5)]:
    L = ConeLattice(48, 48, 10.0, al, k, n)
    x, E, g, it = L.relax(L.seed([(0.0, 0.0, n)]), 5000)
    G = L.gauge_sparse(x); GtG = (G.T @ G).tocsc()
    gmin = float(eigsh(GtG, k=1, sigma=0, which="LM", return_eigenvectors=False)[0])
    w1, l1 = spec_xi(L, x, NEV, 1.0)
    w2, V2, xi2 = L.spectrum(x, NEV)
    phys1 = w1[l1 < 1e-3]                       # modes with negligible gauge component at xi = 1
    m = min(len(phys1), len(w2))
    match = bool(np.all(np.array([f"{a:.4e}" for a in phys1[:m]]) == np.array([f"{b:.4e}" for b in w2[:m]])))
    maxdiff = float(np.max(np.abs(phys1[:m]-w2[:m]))) if m else float("nan")
    cutoff = float(w2[-1])                      # counting window top: highest eigenvalue in the 24-mode window
    gauge_low = gmin                            # lowest pure-gauge eigenvalue of H + 1*G G^T (= lambda_min(G^T G))
    ok = match and gauge_low > cutoff
    ok_all &= ok
    print(f"[SCRATCH H5] n={n} kappa={k} alpha={al} grid=48 |grad|={g:.1e}")
    print(f"  xi=1: {len(phys1)}/{NEV} modes gauge-free in window; gauge-tagged in window: {int(np.sum(l1 >= 1e-3))}")
    print(f"  code xi={xi2:.2f}: lowest 6 = " + ", ".join(f"{v:.4e}" for v in w2[:6]))
    print(f"  xi=1  phys lowest 6 = " + ", ".join(f"{v:.4e}" for v in phys1[:6]))
    print(f"  (a) physical match to printed digits over {m} modes: {match} (max |diff| {maxdiff:.2e})")
    print(f"  (b) lowest gauge eigenvalue at xi=1 = {gauge_low:.4e} vs counting-window top {cutoff:.4e}: {'ABOVE' if gauge_low > cutoff else 'NOT ABOVE'}")
print("XI_CHECK", "PASS" if ok_all else "FAIL")

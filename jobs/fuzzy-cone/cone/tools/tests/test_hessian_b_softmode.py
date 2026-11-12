"""Unit tests for hessian_b_softmode.py on a tiny model (N=5, n=1). Not a result."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hessian_b_softmode as hb
import jax.numpy as jnp
from scipy.optimize import minimize

def setup():
    M = hb.Model(5, 1, R=2.0, wrad=1e4); pm, f, g, hvp = hb.build(M); return M, pm, f, g, hvp

def test_param_roundtrip_and_energy():
    M, pm, f, g, hvp = setup(); rng = np.random.default_rng(0)
    x = M.seed_fuzzy() + 0.05 * rng.standard_normal(M.nX() + 2 * M.Np * M.N)
    y, X, P = pm.x2y(x)
    assert abs(float(f(jnp.asarray(y))) - float(M.energy(jnp.asarray(x)))) < 1e-10
    H = X[1] - M.Lp[1]; assert np.allclose(pm.c2h(pm.h2c(H)), H)

def test_symmetries_null_at_random_point():
    M, pm, f, g, hvp = setup(); rng = np.random.default_rng(1)
    y = 0.05 * rng.standard_normal(pm.dim); y[3 * pm.nh:3 * pm.nh + pm.nP] += M.seed_fuzzy()[M.nX():M.nX() + pm.nP]
    X, P = M.unpack(np.asarray(pm.y2x(jnp.asarray(y), xp=jnp))); X = [np.asarray(v) for v in X]; P = np.asarray(P)
    gr = np.asarray(g(jnp.asarray(y))); G = hb.gauge_matrix(pm, X, P); R = hb.rot_vectors(pm, X, P)
    assert np.abs(gr @ G).max() < 1e-9 * np.linalg.norm(gr) * np.linalg.norm(G, axis=0).max()
    assert np.abs(gr @ R).max() < 1e-9 * np.linalg.norm(gr) * np.linalg.norm(R, axis=0).max()

def test_gauge_and_rotation_null_hessian_at_minimum():
    M, pm, f, g, hvp = setup()
    y0, _, _ = pm.x2y(M.seed_fuzzy()); y0 = y0 + 1e-3 * np.random.default_rng(2).standard_normal(pm.dim)
    r = minimize(lambda y: float(f(jnp.asarray(y))), y0, jac=lambda y: np.asarray(g(jnp.asarray(y))), method='L-BFGS-B',
                 options=dict(maxiter=20000, ftol=1e-18, gtol=1e-12))
    y = r.x; X, P = M.unpack(np.asarray(pm.y2x(jnp.asarray(y)))); X = [np.asarray(v) for v in X]; P = np.asarray(P)
    G = hb.gauge_matrix(pm, X, P); R = hb.rot_vectors(pm, X, P)
    scale = max(abs(float(v @ np.asarray(hvp(jnp.asarray(y), jnp.asarray(v))))) for v in np.eye(pm.dim)[:20])
    for V in (G, R):
        for k in range(V.shape[1]):
            v = V[:, k]; n = np.linalg.norm(v)
            if n < 1e-12: continue
            hv = np.asarray(hvp(jnp.asarray(y), jnp.asarray(v / n)))
            assert np.linalg.norm(hv) < 1e-4 * max(scale, 1.0), (k, np.linalg.norm(hv))

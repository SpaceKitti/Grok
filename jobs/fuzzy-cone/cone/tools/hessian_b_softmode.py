#!/usr/bin/env python3
"""HESSIAN_B_SOFTMODE_FREEZE.md (30408148) runner. Aethon 2026-11-09. Output only, no solves, run once via launch_gated.py.
H1 Hermitian X_a only (orthonormal Frobenius coords of H_a = X_a - L'_a), plus Phi (re, im). Energy = Model.energy (code 63b69fbc).
H2 Gauge slice span{dX_a = i[Lam,X_a], dPhi = i Lam Phi}, orthonormalised by SVD (rank: sigma > 1e-8 sigma_max), projected out.
   Implementation: operator P H P + s_g Q Q^T (Q = gauge basis, s_g = gauge shift) so the gauge slice sits at s_g, far above
   the lowest 40; equivalent to the Hessian on the orthogonal complement. Leakage of every returned mode into Q is reported.
H3 eigsh which='SA', k=40, tol=1e-10, HVP = jax.jvp of jax.grad.
H4 n_neg (lam < -1e-6), n_soft (|lam| <= 1e-6), lam_min_nonzero (lowest lam > 1e-6), rotation overlaps.
   Rotation generators (freeze H4): dX_a = eps_{kab} X_b + i[L'_k, X_a], dPhi = i(L'_k Phi - Phi L_k)."""
import os, sys, json, time, hashlib, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CONE = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(CONE, 'v2_1'))
from fuzzy_cone_v2_1 import Model, observe, EPS
import jax, jax.numpy as jnp
from scipy.sparse.linalg import eigsh, LinearOperator
from scipy.linalg import svd
jax.config.update("jax_enable_x64", True)

FREEZE = os.path.join(CONE, 'HESSIAN_B_SOFTMODE_FREEZE.md')
ROWS = [2.0, 1.2, 1.05]
NPZ = os.path.join(CONE, 'v2_1', 'sol_probeB_r3_S1_b{b:g}_n3_N61_seed0.npz')
OUT = os.path.join(CONE, 'RESULT_HESSIAN_B_SOFTMODE.json')
K_EIG, TOL, ZTOL, RANK_RTOL = 40, 1e-10, 1e-6, 1e-8

def sha8(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:8]
def uk_now():
    from zoneinfo import ZoneInfo; import datetime as dt
    return dt.datetime.now(ZoneInfo('Europe/London')).strftime('%Y-%m-%d %H:%M:%S %Z')

class Param:
    """y = [h_0, h_1, h_2, Re Phi, Im Phi]; h_a orthonormal coords of Hermitian H_a (diag, sqrt2 Re upper, sqrt2 Im upper)."""
    def __init__(s, M):
        s.M = M; Np, N = M.Np, M.N; s.iu = np.triu_indices(Np, 1); s.nh = Np * Np; s.nP = Np * N
        s.dim = 3 * s.nh + 2 * s.nP
    def h2c(s, H, xp=np):
        r2 = np.sqrt(2.0)
        return xp.concatenate([xp.real(xp.diagonal(H)), r2 * xp.real(H[s.iu]), r2 * xp.imag(H[s.iu])])
    def c2h(s, c, xp=np):
        Np = s.M.Np; nu = len(s.iu[0]); d = c[:Np]; re = c[Np:Np + nu] / np.sqrt(2); im = c[Np + nu:] / np.sqrt(2)
        U = xp.zeros((Np, Np), dtype=complex)
        if xp is np: U[s.iu] = re + 1j * im
        else: U = U.at[s.iu].set(re + 1j * im)
        return U + U.conj().T + xp.diag(d.astype(complex))
    def y2x(s, y, xp=jnp):
        parts = []
        for a in range(3):
            H = s.c2h(y[a * s.nh:(a + 1) * s.nh], xp); parts += [xp.real(H).ravel(), xp.imag(H).ravel()]   # A = H (Hermitian)
        parts += [y[3 * s.nh:3 * s.nh + s.nP], y[3 * s.nh + s.nP:]]
        return xp.concatenate(parts)
    def x2y(s, x):
        X, P = s.M.unpack(x); X = [np.asarray(v) for v in X]; P = np.asarray(P)
        return np.concatenate([s.h2c(X[a] - s.M.Lp[a]) for a in range(3)] + [P.real.ravel(), P.imag.ravel()]), X, P
    def tang(s, dX, dP):
        return np.concatenate([s.h2c(dX[a]) for a in range(3)] + [dP.real.ravel(), dP.imag.ravel()])

def gauge_matrix(pm, X, P):
    Np = pm.M.Np; cols = []
    for k in range(Np * Np):
        e = np.zeros(Np * Np); e[k] = 1.0; L = pm.c2h(e)
        cols.append(pm.tang([1j * (L @ Xa - Xa @ L) for Xa in X], 1j * L @ P))
    return np.array(cols).T

def rot_vectors(pm, X, P):
    M = pm.M; R = []
    for k in range(3):
        dX = [sum(EPS[k, a, b] * X[b] for b in range(3)) + 1j * (M.Lp[k] @ X[a] - X[a] @ M.Lp[k]) for a in range(3)]
        R.append(pm.tang(dX, 1j * (M.Lp[k] @ P - P @ M.L[k])))
    return np.array(R).T

def build(M):
    pm = Param(M); f = jax.jit(lambda y: M.energy(pm.y2x(y))); g = jax.jit(jax.grad(f))
    hvp = jax.jit(lambda y, v: jax.jvp(g, (y,), (v,))[1]); return pm, f, g, hvp

def kernel_rank(M, x):
    X, P, *_ = M.pieces(x); P = np.asarray(P); X3 = np.asarray(X[2])
    w, U = np.linalg.eigh(P @ P.conj().T); K = U[:, w < 1e-8]
    lam = np.linalg.eigvalsh(K.conj().T @ X3 @ K) / np.sqrt(M.c)
    return f"{(lam > 0).sum()}/{(lam < 0).sum()}", int(K.shape[1])

def row(b, seed=12345):
    t0 = time.time(); path = NPZ.format(b=b); d = np.load(path)
    M = Model(int(d['N']), int(d['n']), R=float(d['R']), wrad=float(d['wrad'])); pm, f, g, hvp = build(M)
    y0, X, P = pm.x2y(d['x']); y0j = jnp.asarray(y0)
    E_y = float(f(y0j)); E_x = float(M.energy(jnp.asarray(d['x']))); gn = float(np.linalg.norm(np.asarray(g(y0j))))
    G = gauge_matrix(pm, X, P); U, sv, _ = svd(G, full_matrices=False, lapack_driver='gesdd'); del G
    rank = int((sv > RANK_RTOL * sv[0]).sum()); Q = np.ascontiguousarray(U[:, :rank]); del U
    Rv = rot_vectors(pm, X, P); Rp = Rv - Q @ (Q.T @ Rv); rs = np.linalg.svd(Rp, compute_uv=False)
    n_rot = int((rs > RANK_RTOL * np.linalg.norm(Rv, axis=0).max()).sum())
    Rhat, _ = np.linalg.qr(Rp) if n_rot == 3 else (None, None)
    rot_rq = [float(Rhat[:, k] @ np.asarray(hvp(y0j, jnp.asarray(Rhat[:, k])))) for k in range(3)] if Rhat is not None else None
    # gauge shift: above the lowest-40 band; pick 10x a Rayleigh-quotient scale of the projected Hessian on random vectors
    rng = np.random.default_rng(seed); proj = lambda v: v - Q @ (Q.T @ v)
    probe = [proj(rng.standard_normal(pm.dim)) for _ in range(4)]
    rq = [float(v @ np.asarray(hvp(y0j, jnp.asarray(v)))) / float(v @ v) for v in probe]
    s_g = float(max(rq)); nmv = [0]; Qj = jnp.asarray(Q); gr = jax.grad(f)
    @jax.jit
    def _mv(v):
        pv = v - Qj @ (Qj.T @ v); h = jax.jvp(gr, (y0j,), (pv,))[1]
        return h - Qj @ (Qj.T @ h) + s_g * (Qj @ (Qj.T @ v))
    def mv(v):
        nmv[0] += 1; return np.asarray(_mv(jnp.asarray(np.asarray(v).ravel())))
    op = LinearOperator((pm.dim, pm.dim), matvec=mv, dtype=float)
    t1 = time.time()
    lam, V = eigsh(op, k=K_EIG, which='SA', tol=TOL, v0=proj(rng.standard_normal(pm.dim)), ncv=160, maxiter=200000)
    o = np.argsort(lam); lam, V = lam[o], V[:, o]
    gauge_leak = float(np.linalg.norm(Q.T @ V, axis=0).max())
    resid = [float(np.linalg.norm(mv(V[:, i]) - lam[i] * V[:, i])) for i in range(K_EIG)]
    soft = np.abs(lam) <= ZTOL; neg = lam < -ZTOL; pos = lam > ZTOL
    rot_w = (np.linalg.norm(Rhat.T @ V, axis=0) ** 2).tolist() if Rhat is not None else None
    Vs = V[:, soft]
    rot_in_soft = (np.linalg.norm(Vs.T @ Rhat, axis=0) ** 2).tolist() if Rhat is not None else None
    obs = observe(M, d['x']); kr, kd = kernel_rank(M, d['x'])
    return dict(b=b, npz=os.path.basename(path), npz_sha8=sha8(path), N=M.N, n=M.n, Np=M.Np, R=M.R, wrad=M.wrad,
                dim_y=pm.dim, E_saved=float(d['E']), E_hermitian_param=E_y, E_model=E_x, grad_norm_y=gn,
                gauge_slice_rank=rank, gauge_dim=M.Np ** 2, gauge_sv_min_kept_over_max=float(sv[rank - 1] / sv[0]),
                gauge_sv_next_over_max=float(sv[rank] / sv[0]) if rank < len(sv) else None,
                gauge_shift=s_g, gauge_leak_max=gauge_leak, n_rot_after_gauge=n_rot,
                rotation_sv_after_gauge=rs.tolist(), rotation_rayleigh=rot_rq,
                eigenvalues_lowest40=lam.tolist(), eig_residuals=resid, n_matvec=nmv[0],
                n_neg=int(neg.sum()), n_soft=int(soft.sum()), soft_tol=ZTOL, neg_tol=-ZTOL,
                lam_min_nonzero=float(lam[pos][0]) if pos.any() else None,
                rotation_weight_per_mode=rot_w, rotation_weight_in_soft_space=rot_in_soft,
                rotation_overlap_total_soft=float(sum(rot_in_soft)) if rot_in_soft is not None else None,
                validity_projector_rank_G1=kr, kernel_dim=kd, Q_total_output_only=obs['Q_total'],
                eigsh_sec=round(time.time() - t1, 1), row_sec=round(time.time() - t0, 1))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=OUT); a = ap.parse_args()
    assert sha8(FREEZE) == '30408148', 'freeze hash changed'
    res = dict(name='HESSIAN_B_SOFTMODE', freeze=os.path.basename(FREEZE), freeze_sha8=sha8(FREEZE),
               script_sha8=sha8(os.path.abspath(__file__)), model_sha8=sha8(os.path.join(CONE, 'v2_1', 'fuzzy_cone_v2_1.py')),
               started_uk=uk_now(), grading='none (output only); Venus line-checks', rows=[])
    print('START', res['started_uk'], flush=True)
    for b in ROWS:
        r = row(b); res['rows'].append(r)
        print(f"b={b} rank={r['gauge_slice_rank']} n_rot={r['n_rot_after_gauge']} n_neg={r['n_neg']} n_soft={r['n_soft']} "
              f"lam_min_nz={r['lam_min_nonzero']} low={np.round(r['eigenvalues_lowest40'][:8], 8).tolist()} sec={r['row_sec']}", flush=True)
        json.dump(res, open(a.out + '.partial', 'w'), indent=1)
    res['finished_uk'] = uk_now(); json.dump(res, open(a.out, 'w'), indent=1)
    if os.path.exists(a.out + '.partial'): os.remove(a.out + '.partial')
    print('DONE', res['finished_uk'], sha8(a.out), flush=True)

if __name__ == '__main__':
    main()

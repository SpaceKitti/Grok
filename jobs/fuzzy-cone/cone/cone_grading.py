"""CONE_SPEC_V1 (b0a62591) + ADDENDUM_P1 (3150c48b) grading pieces. Aethon, 2026-10-29. Statics only.
C-2 radial-projected charge (Venus V1_2 §8a, prototype ../it1b/venus_v1_2_check_charge.py 0530de3b) with Z_k weight
    w_cap = 4 pi R^2/(k N) (already Model.wcap) + addendum P1 rules and the k-fold cover check.
C-4 tip-exponent fitter (P2) + density finiteness (P6).
C-5 l <= N-1 adjoint-Casimir check (P0) + sphere-term excess (P5).
C-6 curvature/deficit of the realised Z_k cone (P7).
C-7 SU(2)/U(1) split (grade SU(2), report U(1))."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "it1b"))
from fuzzy_instanton import spin_matrices

def dag(X): return np.swapaxes(X.conj(), -1, -2)
_EPS = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]

def _pieces(m, B, U):
    a, R = m.a, m.R; n3, n4 = m.L3 - 1, m.L4 - 1; s0 = (slice(0, n3), slice(0, n4))
    P = U[0][s0] @ U[1][1:, :n4] @ dag(U[0][:n3, 1:]) @ dag(U[1][s0]); F34 = 1j * (P - dag(P)) / (2 * a**2)
    def C(mu, i):
        Ul, Bn = (U[0][s0], B[i][1:, :n4]) if mu == 0 else (U[1][s0], B[i][:n3, 1:])
        return (Ul @ Bn @ dag(Ul) - B[i][s0]) / (a * R)
    return s0, F34, C

def charge_radial_density(m, B, U, part="full"):
    """Venus's radial-projected lattice charge density (identical algebra to venus_v1_2_check_charge.charge_radial).
    part: 'full' | 'su2' | 'u1' (C-7: products split into colour-trace and colour-traceless pieces)."""
    a, R, N = m.a, m.R, m.N; jj = (N - 1) / 2
    nh = [x / np.sqrt(jj * (jj + 1)) for x in m.Lfull]
    s0, F34, C = _pieces(m, B, U)
    proj = {"full": lambda X: X, "su2": su2_part, "u1": u1_part}[part]
    q = 0
    for (i, j, c) in _EPS:
        Ft = -1j * (B[i] @ B[j] - B[j] @ B[i] - 1j * B[c])[s0] / R**2
        q = q + np.einsum("ab,...ba->...", nh[c], proj(Ft) @ proj(F34))
    for (i, j, c) in _EPS:            # Venus prototype: full Levi-Civita sum (both orderings) for the mixed term
        q = q - np.einsum("ab,...ba->...", nh[c], proj(C(0, i)) @ proj(C(1, j)))
        q = q + np.einsum("ab,...ba->...", nh[c], proj(C(0, j)) @ proj(C(1, i)))
    return (m.wcap * a**2 * q.real) / (4 * np.pi**2), m.interior[s0]

def charge_radial(m, B, U, part="full"):
    d, msk = charge_radial_density(m, B, U, part); return float(d[msk].sum())

def u1_part(X):
    """colour trace part: X0 (x) 1, X0 = tr_colour(X)/2 (2N = N (x) 2 ordering, kron(L, I2))."""
    N = X.shape[-1] // 2; Y = X.reshape(X.shape[:-2] + (N, 2, N, 2))
    X0 = 0.5 * (Y[..., :, 0, :, 0] + Y[..., :, 1, :, 1])
    return np.einsum("...ab,ij->...aibj", X0, np.eye(2)).reshape(X.shape)
def su2_part(X): return X - u1_part(X)

def grade_P1(Q20, Q26, n, k, m_hol, Q_pred, tol=0.02):
    """Addendum P1: |Q - Q_pred| <= tol at L26 (finest), sign reported, |Q - Q_pred| shrinks L20 -> L26;
    Q_pred must be a multiple of 1/k with Q_pred = m/k mod 1; prediction-free cover check |kQ - round(kQ)| <= tol*k."""
    assert abs(Q_pred * k - round(Q_pred * k)) < 1e-12, "Q_pred not in Z/k"
    assert abs(((Q_pred - m_hol / k) + 0.5) % 1 - 0.5) < 1e-12, "Q_pred != m/k mod 1"
    out = {"Q_L20": Q20, "Q_L26": Q26, "sign": int(np.sign(Q26)), "Q_pred": Q_pred, "m_hol": m_hol, "k": k}
    out["dev"] = abs(Q26 - Q_pred); out["moves_toward"] = abs(Q26 - Q_pred) < abs(Q20 - Q_pred)
    out["cover_dev"] = abs(k * Q26 - round(k * Q26)); out["cover_ok"] = out["cover_dev"] <= tol * k
    if not out["cover_ok"]: out["grade"] = "FAIL (cover check: construction bug or wrong prediction)"
    elif not out["moves_toward"]: out["grade"] = "FAIL (construction bug: not moving toward Q_pred)"
    else: out["grade"] = "PASS" if out["dev"] <= tol else "FAIL"
    return out

# ---------------- C-4 ----------------
def radial_profile(m, dens2d, nbins=None):
    """Energy density per unit x3x4 area vs plane radius r (sites, interior only). Returns r, e per site."""
    X3, X4 = np.meshgrid(m.x3, m.x4, indexing="ij"); r = np.hypot(X3, X4)
    msk = m.interior
    return r[msk], dens2d[msk] / m.a**2

def fit_tip_exponent(r, e, w_N, r_c, n, alpha, tol=0.05, min_pts=4):
    """P2: log-slope of e(r) on the frozen window [2 w_N, 0.5 r_c] vs 2|n|/alpha - 2."""
    lo, hi = 2 * w_N, 0.5 * r_c; s = (r >= lo) & (r <= hi) & (e > 0)
    target = 2 * abs(n) / alpha - 2
    res = {"window": [lo, hi], "npts": int(s.sum()), "target": target}
    res["n_distinct_r"] = int(len(np.unique(np.round(r[s], 9))))
    if res["n_distinct_r"] < min_pts: res.update(slope=None, grade="UNDECIDED (<4 distinct radii in window)"); return res
    slope = float(np.polyfit(np.log(r[s]), np.log(e[s]), 1)[0])
    res.update(slope=slope, grade="PASS" if abs(slope - target) <= tol else "FAIL"); return res

def grade_P6(maxdens_N21, maxdens_N41):
    ok = np.isfinite(maxdens_N41) and maxdens_N41 <= maxdens_N21 * 1.1
    return {"max21": maxdens_N21, "max41": maxdens_N41, "grade": "PASS" if ok else "FAIL"}

# ---------------- C-5 ----------------
def max_l_content(X, N, tol=1e-12):
    """P0: decompose the N x N orbital blocks of X (2N x 2N, colour blocks separately) into adjoint-Casimir
    eigenspaces of ad(L)^2 (eigenvalue l(l+1)); return the largest l with weight > tol*||X||."""
    L = spin_matrices(N); I = np.eye(N)
    Cas = sum((np.kron(Li, I) - np.kron(I, Li.T)) @ (np.kron(Li, I) - np.kron(I, Li.T)) for Li in L)
    w, V = np.linalg.eigh(Cas); ls = np.rint((-1 + np.sqrt(1 + 4 * np.maximum(w, 0))) / 2).astype(int)
    Y = X.reshape(N, 2, N, 2); lmax = 0; nrm = np.linalg.norm(X) + 1e-300
    for c1 in range(2):
        for c2 in range(2):
            v = Y[:, c1, :, c2].reshape(-1); coef = V.conj().T @ v
            for l in np.unique(ls):
                if np.linalg.norm(coef[ls == l]) > tol * nrm: lmax = max(lmax, int(l))
    return lmax

def sphere_term(m, B):
    """lattice sphere (cap) term per site, same normalisation as Model.action."""
    cc = m.wcap * m.a**2 / m.R**4; d = 0
    for (i, j, kk, e) in [(0, 1, 2, 1.0), (0, 2, 1, -1.0), (1, 2, 0, 1.0)]:
        F = B[i] @ B[j] - B[j] @ B[i] - 1j * e * B[kk]; d = d + cc * (-np.einsum("...ab,...ba->...", F, F).real)
    return d

def grade_P5(E_by_N, tol=0.01):
    Ns = sorted(E_by_N); E = [abs(E_by_N[n]) for n in Ns]
    ok = all(e <= tol for e in E) and all(E[i + 1] <= E[i] * 1.0 + 1e-12 for i in range(len(E) - 1))
    return {"E": dict(zip(Ns, E)), "grade": "PASS" if ok else "FAIL"}

# ---------------- C-6 ----------------
def cone_deficit(m):
    """P7: realised cone = round fuzzy S^2 / Z_k (g = exp(2 pi i L3/k)). Tip total angle = rotation angle of Ad_g on
    the tangent plane (from m.Rot); deficit = 2 pi - angle. Cross-check: fuzzy-trace curvature of the cap
    sum_cap w_cap/R^2 * N = 4 pi/k, split over the 2 tips by Gauss-Bonnet for S^2/Z_k: 2pi*chi_orb = 4 pi/k ->
    each tip deficit = (4 pi - 4 pi/k)/2."""
    th = abs(np.arctan2(m.Rot[0, 1], m.Rot[0, 0]))
    ang = 2 * np.pi if m.k == 1 else th
    d_rot = 2 * np.pi - ang
    curv = m.wcap * m.N / m.R**2
    d_gb = (4 * np.pi - curv) / 2
    target = 2 * np.pi * (1 - 1 / m.k)
    ok = all(abs(d - target) <= 0.01 * max(target, 1e-300) or abs(d - target) < 1e-12 for d in (d_rot, d_gb))
    return {"deficit_rot": d_rot, "deficit_GB": d_gb, "target": target, "grade": "PASS" if ok else "FAIL"}

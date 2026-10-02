"""M-matrix check (Venus/Helios): M = R^{-1} U R in the sheet eigenbasis at the start point.

Normalisation: R columns = right eigenvectors of H_A(0.75 eps_EP), ordered [A, B], each scaled to
unit Euclidean norm (a column scaling; D = R^T R stays diagonal for any column scaling because H_A is
complex-symmetric, so left eigenvectors are plain transposes). Same R as the weight code in drive.py.
U = un-renormalised propagator of H' = H_A + i(a+b)/2 (det U = 1).
"""
from __future__ import annotations

import numpy as np

import drive as D

SX = np.array([[0, 1], [1, 0]], dtype=complex)


def U_loops(s: int, gT: float) -> dict:
    """Propagator after 1 and 2 turns (same integrator and steps as drive.run_drive)."""
    T = gT / D.GAM
    w = 2 * np.pi / T
    n1 = D.steps_per_turn(gT)
    dt = T / n1
    M = np.eye(2, dtype=complex)
    out = {}
    for k in range(n1 * 2):
        M = D.expm2(D.Hp(D.eps_of(w * (k + 0.5) * dt, s)), dt) @ M
        if (k + 1) % n1 == 0:
            out[(k + 1) // n1] = M.copy()
    return out


def classify(M: np.ndarray) -> dict:
    a = np.abs(M)
    s = np.linalg.svd(M, compute_uv=False)
    diag = max(a[0, 1], a[1, 0]) < 0.1 * max(a[0, 0], a[1, 1])
    anti = max(a[0, 0], a[1, 1]) < 0.1 * max(a[0, 1], a[1, 0])
    r = s[1] / s[0]
    kind = "~diagonal" if diag else "~antidiagonal" if anti else ("rank-1-dominated" if r < 0.1 else "mixed (none of the three)")
    return {"s2/s1": float(r), "kind": kind}


def rank1(M: np.ndarray, Dd: np.ndarray, slow: int) -> dict:
    """M ~ sigma1 u w^T with w^T = v1^H (leading SVD pair). ccw output = u; cw output = D^{-1} w."""
    U_, S, Vh = np.linalg.svd(M)
    u = U_[:, 0]
    w = Vh[0, :]
    dw = w / Dd
    fu = np.abs(u) ** 2 / np.sum(np.abs(u) ** 2)
    fd = np.abs(dw) ** 2 / np.sum(np.abs(dw) ** 2)
    return {"sigma": S, "ratio": float(S[0] / S[1]), "u": u, "Dinv_w": dw,
            "frac_u_slow": float(fu[slow]), "frac_Dw_slow": float(fd[slow])}


def weights_col(M: np.ndarray, j: int) -> np.ndarray:
    c = M[:, j]
    return np.abs(c) ** 2 / np.sum(np.abs(c) ** 2)


def m_check(gT: float) -> dict:
    lam, R, Rinv = D.sheet_basis(D.EPS_START)
    slow = int(np.argmax(lam.imag))
    Dg = R.T @ R
    Dd = np.diag(Dg).copy()
    out = {"gT": gT, "D": Dd, "DA_over_DB": complex(Dd[0] / Dd[1]), "offdiag_D": float(abs(Dg[0, 1])),
           "slow": slow, "turns": {}}
    Lp, Lm = U_loops(+1, gT), U_loops(-1, gT)
    for m in (1, 2):
        Up, Um = Lp[m], Lm[m]
        Mp = Rinv @ Up @ R
        Mm = Rinv @ Um @ R
        pred = np.diag(1 / Dd) @ Mp.T @ np.diag(Dd)
        # PT: sigma_x H'(eps)^* sigma_x = H'(conj eps)  =>  U_cw = sigma_x (U_ccw^{-1})^dagger sigma_x
        pt = SX @ np.linalg.inv(Up).conj().T @ SX
        out["turns"][m] = {
            "M_ccw": Mp, "M_cw": Mm,
            "resid_transpose": float(np.linalg.norm(Mm - pred)),
            "resid_PT": float(np.linalg.norm(Um - pt)),
            "abs_AB": float(abs(Mp[0, 1])), "abs_BA": float(abs(Mp[1, 0])),
            "class_ccw": classify(Mp), "class_cw": classify(Mm),
            "w_ccw": {"A": weights_col(Mp, 0), "B": weights_col(Mp, 1)},
            "w_cw": {"A": weights_col(Mm, 0), "B": weights_col(Mm, 1)},
            "det_ccw": complex(np.linalg.det(Mp)), "det_cw": complex(np.linalg.det(Mm)),
            # det U = 1 exactly (H' traceless); losing it means the propagator's dynamic range exceeded double precision
            "precision_ok": bool(abs(np.linalg.det(Mp) - 1) < 1e-6 and abs(np.linalg.det(Mm) - 1) < 1e-6),
            "r1_ccw": rank1(Mp, Dd, slow), "r1_cw": rank1(Mm, Dd, slow),
        }
    return out


# ---------------------------------------------------------------------------
# Log-scaled M (Helios): propagate each start eigenvector R_j separately, renormalising every step
# and keeping a running log of its norm, so M_ij = exp(l_j) (R^{-1} psi_hat_j)_i. Avoids overflow;
# it does NOT remove the loss of the subdominant component to round-off (check det M = 1).
def M_loops_log(s, gT, R, Rinv):
    T = gT / D.GAM
    w = 2 * np.pi / T
    n1 = D.steps_per_turn(gT)
    dt = T / n1
    Psi = R.copy()
    logn = np.zeros(2)
    out = {}
    for k in range(n1 * 2):
        Psi = D.expm2(D.Hp(D.eps_of(w * (k + 0.5) * dt, s)), dt) @ Psi
        nr = np.linalg.norm(Psi, axis=0)
        Psi = Psi / nr
        logn += np.log(nr)
        if (k + 1) % n1 == 0:
            X = Rinv @ Psi
            out[(k + 1) // n1] = {"X": X.copy(), "logn": logn.copy(), "M": X * np.exp(logn)[None, :],
                                  "logdet": complex(np.sum(logn) + np.log(np.linalg.det(X) + 0j))}
    return out


def pt_map(R):
    # PT: psi -> sigma_x psi*. Row i: normalised overlaps |<R_k|PT R_i>| for k = A, B.
    res = []
    for i in range(2):
        p = SX @ R[:, i].conj()
        res.append([abs(np.vdot(R[:, k], p)) / (np.linalg.norm(R[:, k]) * np.linalg.norm(p)) for k in range(2)])
    return res


def m_check_log(gT, name_idx):
    # M check at the current drive start point, log-scaled propagation; name_idx = mode used for 'fractions'.
    lam, R, Rinv = D.sheet_basis(D.EPS_START)
    Dg = R.T @ R
    Dd = np.diag(Dg).copy()
    out = {"gT": gT, "lam": lam, "R": R, "D": Dd, "DA_over_DB": complex(Dd[0] / Dd[1]),
           "offdiag_D": float(abs(Dg[0, 1])), "pt": pt_map(R), "turns": {}}
    Lp, Lm = M_loops_log(+1, gT, R, Rinv), M_loops_log(-1, gT, R, Rinv)
    for m in (1, 2):
        Mp, Mm = Lp[m]["M"], Lm[m]["M"]
        pred = np.diag(1 / Dd) @ Mp.T @ np.diag(Dd)
        Up, Um = R @ Mp @ Rinv, R @ Mm @ Rinv
        adj = np.array([[Up[1, 1], -Up[0, 1]], [-Up[1, 0], Up[0, 0]]])  # = U^{-1} exactly since det U = 1; uses entries only
        pt = SX @ adj.conj().T @ SX
        dp, dm = np.exp(Lp[m]["logdet"]), np.exp(Lm[m]["logdet"])
        r1p, r1m = rank1(Mp, Dd, name_idx), rank1(Mm, Dd, name_idx)
        def ovR(v):
            return [abs(np.vdot(R[:, k], v)) / (np.linalg.norm(R[:, k]) * np.linalg.norm(v)) for k in range(2)]
        out["turns"][m] = {
            "M_ccw": Mp, "M_cw": Mm,
            "rel_resid_transpose": float(np.linalg.norm(Mm - pred) / np.linalg.norm(Mm)),
            "rel_resid_PT": float(np.linalg.norm(Um - pt) / np.linalg.norm(Um)),
            "abs_AA": float(abs(Mp[0, 0])), "abs_BB": float(abs(Mp[1, 1])),
            "abs_AB": float(abs(Mp[0, 1])), "abs_BA": float(abs(Mp[1, 0])),
            "det_ccw": complex(dp), "det_cw": complex(dm),
            "precision_ok": bool(abs(dp - 1) < 1e-6 and abs(dm - 1) < 1e-6),
            "class_ccw": classify(Mp), "class_cw": classify(Mm),
            "w_ccw": {"A": weights_col(Mp, 0), "B": weights_col(Mp, 1)},
            "w_cw": {"A": weights_col(Mm, 0), "B": weights_col(Mm, 1)},
            "r1_ccw": r1p, "r1_cw": r1m,
            # output directions as vectors in the physical basis: u -> R u ; cw output D^{-1} w -> R D^{-1} w
            "ov_u_R": ovR(R @ r1p["u"]), "ov_Dw_R": ovR(R @ r1p["Dinv_w"]), "ov_ucw_R": ovR(R @ r1m["u"]),
        }
    return out

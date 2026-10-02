"""
OBJECT 1 — linearized resistive tearing operator on a Harris sheet.

Ideal-MHD outer region + resistive inner layer. No Hall, no guide field.
Non-Hermitian 2-field operator (ψ flux, u stream) discretized on a sheet-
clustered grid. Even/odd tearing pair lives in the spectrum; a 2×2 Galerkin
reduction is stored as a layer transfer companion, not as the test itself.

Harris: Bx = tanh(z), a = B0 = v_A = 1, η = 1/S.
Δ' a = 2 (1/(k a) - k a); tearing window k a < 1.

Pass only if R_EP, R_Puiseux, and R_conn lock on the same parameter value
AND the Puiseux exponent or EP gap reproduces a known rate scaling.
Otherwise: "spectral decoration, not dictionary" and STOP.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
from scipy import linalg

# ---------------------------------------------------------------------------
# Grid and differentiation
# ---------------------------------------------------------------------------


def clustered_grid(n: int, zmax: float, beta: float) -> tuple[np.ndarray, np.ndarray]:
    """z = zmax * sinh(β ξ)/sinh(β), ξ ∈ [-1, 1]. Dense at the sheet."""
    xi = np.linspace(-1.0, 1.0, n)
    z = zmax * np.sinh(beta * xi) / np.sinh(beta)
    return z, xi


def mapped_dzz(n: int, zmax: float, beta: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Second-order FD on ξ, chain-ruled to d²/dz². Dirichlet rows left intact."""
    z, xi = clustered_grid(n, zmax, beta)
    h = xi[1] - xi[0]
    dz = zmax * beta * np.cosh(beta * xi) / np.sinh(beta)
    d2z = zmax * (beta ** 2) * np.sinh(beta * xi) / np.sinh(beta)

    D1 = np.zeros((n, n))
    D2 = np.zeros((n, n))
    invh = 1.0 / h
    invh2 = 1.0 / h ** 2
    D1[0, 0], D1[0, 1], D1[0, 2] = -1.5 * invh, 2.0 * invh, -0.5 * invh
    D1[-1, -1], D1[-1, -2], D1[-1, -3] = 1.5 * invh, -2.0 * invh, 0.5 * invh
    D2[0, 0], D2[0, 1], D2[0, 2] = invh2, -2.0 * invh2, invh2
    D2[-1, -1], D2[-1, -2], D2[-1, -3] = invh2, -2.0 * invh2, invh2
    for i in range(1, n - 1):
        D1[i, i - 1] = -0.5 * invh
        D1[i, i + 1] = 0.5 * invh
        D2[i, i - 1] = invh2
        D2[i, i] = -2.0 * invh2
        D2[i, i + 1] = invh2

    inv = 1.0 / dz
    Dzz = (inv ** 2)[:, None] * D2 - (d2z * inv ** 3)[:, None] * D1
    return z, Dzz, dz


def layer_resolved(z: np.ndarray, S: float) -> dict:
    dz_min = float(np.min(np.diff(z)))
    delta_sp = S ** (-0.5)
    delta_fkr = S ** (-0.4)
    return {
        "dz_min": dz_min,
        "delta_SP": float(delta_sp),
        "delta_FKR": float(delta_fkr),
        "resolved_SP": bool(dz_min < 0.25 * delta_sp),
        "resolved_FKR": bool(dz_min < 0.25 * delta_fkr),
    }


# ---------------------------------------------------------------------------
# Operator
# ---------------------------------------------------------------------------


def delta_prime(k: float, a: float = 1.0) -> float:
    """Harris-sheet tearing index. Unstable for k a < 1."""
    ka = k * a
    return 2.0 * (1.0 / ka - ka) / a


def fkr_growth(S: float, k: float, a: float = 1.0) -> float:
    """Constant-ψ FKR, γ τ_A ≈ 0.55 (Δ'a)^{4/5} S^{-3/5} (k a)^{2/5}."""
    dp = delta_prime(k, a) * a
    if dp <= 0.0:
        return 0.0
    return 0.55 * (dp ** 0.8) * (S ** -0.6) * ((k * a) ** 0.4)


def coppi_growth(S: float, k: float) -> float:
    """Non-constant-ψ / large-Δ' Coppi scaling ~ S^{-1/3} k^{2/3}."""
    return (S ** (-1.0 / 3.0)) * (k ** (2.0 / 3.0))


def sweet_parker_rate(S: float) -> float:
    return S ** (-0.5)


def plasmoid_max_growth(S: float) -> float:
    """Ideal-tearing / plasmoid branch γ τ_A ~ S^{1/4} (critical sheet only)."""
    return S ** 0.25


def assemble_operator(
    S: float,
    k: float,
    z: np.ndarray,
    Dzz: np.ndarray,
    pm: float = 0.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Standard EVP γ v = A v, v = [ψ_int, u_int], obtained by inverting ∇²
    on the momentum block (Dirichlet, k≠0 ⇒ invertible).

    γ ψ   = η ∇²ψ + F u
    γ ∇²u = -F ∇²ψ + F'' ψ + ν ∇²(∇² u)     (Pm = ν/η, default 1)

    F = k tanh(z), η = 1/S. Viscosity regularises the discrete Alfvén
    pile; it does not replace η and is not a second cut.
    """
    n_full = z.size
    interior = np.arange(1, n_full - 1)
    n = interior.size
    z_i = z[interior]
    I = np.eye(n)
    Lap = Dzz[np.ix_(interior, interior)] - (k ** 2) * I
    F = k * np.tanh(z_i)
    sech2 = 1.0 / np.cosh(z_i) ** 2
    Fpp = k * (-2.0 * sech2 * np.tanh(z_i))
    eta = 1.0 / S
    nu = pm * eta

    A = np.zeros((2 * n, 2 * n))
    A[:n, :n] = eta * Lap
    A[:n, n:] = np.diag(F)
    # u-row: γ u = Lap^{-1} (-F Lap + Fpp) ψ + ν Lap u
    rhs = -np.diag(F) @ Lap + np.diag(Fpp)
    A[n:, :n] = np.linalg.solve(Lap, rhs)
    A[n:, n:] = nu * Lap
    return A, Lap, z_i


@dataclass
class EigenResult:
    S: float
    k: float
    delta_prime: float
    gamma: np.ndarray
    tearing_gamma: complex
    tearing_idx: int
    even_frac: float
    odd_frac: float
    partner_gamma: complex
    gap: float
    petermann: float
    self_orth: float
    defective: bool
    psi: np.ndarray
    u: np.ndarray
    z: np.ndarray
    resolved: dict
    n_finite: int


def _even_odd_fractions(z: np.ndarray, psi: np.ndarray) -> tuple[float, float]:
    psi_e = 0.5 * (psi + psi[::-1])
    psi_o = 0.5 * (psi - psi[::-1])
    nrm = np.linalg.norm(psi) ** 2 + 1e-30
    return float(np.linalg.norm(psi_e) ** 2 / nrm), float(np.linalg.norm(psi_o) ** 2 / nrm)


def _petermann_pair(A: np.ndarray, idx: int, wr: np.ndarray, Vr: np.ndarray) -> tuple[float, float]:
    """Petermann K = 1/|<L_i|R_i>|^2 and |<R_i|R_j>| to nearest physical neighbour."""
    wl, Vl = np.linalg.eig(A.conj().T)
    j = int(np.argmin(np.abs(wl - wr[idx].conj())))
    left = Vl[:, j]
    right = Vr[:, idx]
    ov = np.vdot(left, right)
    nL = np.linalg.norm(left) + 1e-30
    nR = np.linalg.norm(right) + 1e-30
    K = 1.0 / (np.abs(ov / (nL * nR)) ** 2 + 1e-30)
    diffs = np.abs(wr - wr[idx])
    diffs[idx] = np.inf
    # ignore the numerical zero pile when picking a partner
    diffs[np.abs(wr) < 1e-8] = np.inf
    j2 = int(np.argmin(diffs))
    r2 = Vr[:, j2]
    n2 = np.linalg.norm(r2) + 1e-30
    ov_rr = np.abs(np.vdot(right, r2)) / (nR * n2)
    return float(K), float(ov_rr)


def solve_spectrum(
    S: float,
    k: float,
    z: np.ndarray,
    Dzz: np.ndarray,
    n_keep: int = 24,
) -> EigenResult:
    A, Lap, z_i = assemble_operator(S, k, z, Dzz)
    n = z_i.size
    wr, Vr = np.linalg.eig(A)
    finite = np.isfinite(wr) & (np.abs(wr) < 40.0)
    wr_f = wr[finite]
    Vr_f = Vr[:, finite]
    order = np.argsort(-wr_f.real)
    wr_f = wr_f[order]
    Vr_f = Vr_f[:, order]

    # first even-ψ mode in Re-descending order is the tearing mode
    best_i = 0
    for i in range(min(24, wr_f.size)):
        ef, _ = _even_odd_fractions(z_i, Vr_f[:n, i])
        if ef > 0.55:
            best_i = i
            break

    phase = np.angle(Vr_f[int(np.argmax(np.abs(Vr_f[:n, best_i]))), best_i])
    psi = Vr_f[:n, best_i] * np.exp(-1j * phase)
    u = Vr_f[n:, best_i] * np.exp(-1j * phase)
    nrm = np.linalg.norm(psi) + 1e-30
    psi = psi / nrm
    u = u / nrm

    ef, of = _even_odd_fractions(z_i, psi)
    diffs = np.abs(wr_f - wr_f[best_i])
    diffs[best_i] = np.inf
    # Alfvén-continuum regularisation and the γ=0 null-sheet pile are a
    # spectral cut, not a discrete–discrete EP2. Exclude them as partners.
    diffs[np.abs(wr_f) < 1e-5] = np.inf
    diffs[np.abs(wr_f.real) < 1e-5] = np.inf
    if np.all(~np.isfinite(diffs)):
        gap = np.nan
        partner = wr_f[best_i]
        j2 = best_i
    else:
        j2 = int(np.argmin(diffs))
        gap = float(diffs[j2])
        partner = wr_f[j2]
    K, ov_rr = _petermann_pair(A, best_i, wr_f, Vr_f)
    # Discrete–discrete EP2 only. A tearing mode sliding into γ=0 at Δ'→0 is
    # the Alfvén-cut edge, not a Jordan block of two finite eigenvalues.
    partner_finite = bool(np.abs(partner) > 5e-3)
    tearing_finite = bool(np.abs(wr_f[best_i]) > 5e-3)
    defective = bool(
        (K > 80.0)
        and (ov_rr > 0.85)
        and (gap < 0.02)
        and (gap == gap)
        and partner_finite
        and tearing_finite
    )

    return EigenResult(
        S=S,
        k=k,
        delta_prime=delta_prime(k),
        gamma=wr_f[:n_keep],
        tearing_gamma=complex(wr_f[best_i]),
        tearing_idx=int(best_i),
        even_frac=ef,
        odd_frac=of,
        partner_gamma=complex(partner),
        gap=gap,
        petermann=K,
        self_orth=ov_rr,
        defective=defective,
        psi=psi,
        u=u,
        z=z_i,
        resolved=layer_resolved(z, S),
        n_finite=int(wr_f.size),
    )


# ---------------------------------------------------------------------------
# Diagnostics: connectivity, rate, holonomy, Ohmic
# ---------------------------------------------------------------------------


def connectivity_jump(z: np.ndarray, psi: np.ndarray, k: float, amp: float = 0.15) -> dict:
    """
    Finite-amplitude overlay of the linear eigenfunction on the Harris flux.
    Equilibrium is a null *line* (open sheet). Even-ψ tearing splits it into
    an X–O island chain: that is the connectivity jump.
    """
    psi_r = np.real(np.asarray(psi, dtype=complex))
    z_u = np.linspace(-2.5, 2.5, 201)
    period = 2.0 * np.pi / max(k, 1e-6)
    x_u = np.linspace(0.0, period, 201, endpoint=False)
    psi_u = np.interp(z_u, z, psi_r)
    # pin the island phase so ψ_u(0) ≥ 0
    i0 = int(np.argmin(np.abs(z_u)))
    sign = 1.0 if psi_u[i0] >= 0.0 else -1.0
    psi_u = sign * psi_u
    Z, X = np.meshgrid(z_u, x_u, indexing="ij")
    Psi = -np.log(np.cosh(np.clip(Z, -20.0, 20.0))) + amp * psi_u[:, None] * np.cos(k * X)
    dPdz = np.gradient(Psi, z_u, axis=0)
    dPdx = np.gradient(Psi, x_u, axis=1)
    Bx = -dPdz
    Bz = dPdx
    B2 = Bx ** 2 + Bz ** 2
    n_x = 0
    n_o = 0
    nz, nx = B2.shape
    thresh = 4e-3 * float(np.max(B2))
    for iz in range(2, nz - 2):
        for ix in range(nx):
            im = (ix - 1) % nx
            ip = (ix + 1) % nx
            if not (
                B2[iz, ix] <= B2[iz - 1, ix]
                and B2[iz, ix] <= B2[iz + 1, ix]
                and B2[iz, ix] <= B2[iz, im]
                and B2[iz, ix] <= B2[iz, ip]
            ):
                continue
            if B2[iz, ix] > thresh:
                continue
            Pzz = Psi[iz + 1, ix] - 2.0 * Psi[iz, ix] + Psi[iz - 1, ix]
            Pxx = Psi[iz, ip] - 2.0 * Psi[iz, ix] + Psi[iz, im]
            Pxz = 0.25 * (
                Psi[iz + 1, ip] - Psi[iz + 1, im] - Psi[iz - 1, ip] + Psi[iz - 1, im]
            )
            detH = Pxx * Pzz - Pxz ** 2
            if detH < 0.0:
                n_x += 1
            elif detH > 0.0:
                n_o += 1
    jumped = bool(n_x >= 1 and n_o >= 1)
    return {
        "n_X": int(n_x),
        "n_O": int(n_o),
        "R_conn": 1.0 if jumped else 0.0,
        "amp": amp,
        "null_line_split": jumped,
        "psi0": float(psi_u[i0]),
    }


def ohmic_and_holonomy(
    z: np.ndarray,
    psi: np.ndarray,
    k: float,
    S: float,
    Dzz_diag_est: np.ndarray | None = None,
) -> dict:
    """
    R_MHD = Ohmic ∫ η |j_y|^2 dz on the eigenfunction (j_y ~ ∇²ψ).
    R_CS  = |holonomy across the sheet|.
      geometric: enclosed current jump |Bx(+δ)-Bx(-δ)| of the *perturbed* field
      at the X-phase, plus the eigenfunction Δ_num = [ψ'] / ψ(0).
    """
    eta = 1.0 / S
    psi_r = np.real(psi)
    # numerical Laplacian of ψ along z minus k²ψ
    d2 = np.gradient(np.gradient(psi_r, z), z) - k ** 2 * psi_r
    jy = d2  # j_y = ∇²ψ
    ohmic = float(eta * np.trapezoid(jy ** 2, z))
    e_dot_j = ohmic  # E_|| = η j in the layer

    # Δ_num from even ψ: 2 ψ'(0+)/ψ(0)
    i0 = int(np.argmin(np.abs(z)))
    # one-sided derivative using points with z>0
    zp = z > 0
    if np.count_nonzero(zp) > 4 and abs(psi_r[i0]) > 1e-12:
        dpsi = np.gradient(psi_r, z)
        # jump ψ'(0+) - ψ'(0-)
        dplus = dpsi[np.where(zp)[0][0]]
        dminus = dpsi[np.where(z < 0)[0][-1]]
        dnum = (dplus - dminus) / (psi_r[i0] + 1e-16)
    else:
        dnum = np.nan

    # geometric holonomy: current enclosed in |z|<δ, δ = 2 S^{-1/2}
    delta = max(2.0 * S ** (-0.5), 0.15)
    mask = np.abs(z) <= delta
    # unperturbed Harris jump is 2 tanh(δ); perturbed adds  -2 amp ψ'(layer)
    I_enc = float(np.trapezoid(jy[mask], z[mask])) if np.any(mask) else 0.0
    I_eq = 2.0 * np.tanh(delta)  # ∫ sech² dz over ±δ = 2 tanh(δ)
    R_CS = float(np.abs(I_enc))  # eigenfunction holonomy (perturbed)
    R_CS_eq = float(np.abs(I_eq))  # always-on open-sheet holonomy
    return {
        "R_MHD": ohmic,
        "E_dot_J": e_dot_j,
        "Delta_num": float(dnum),
        "R_CS": R_CS,
        "R_CS_eq": R_CS_eq,
        "delta_hol": float(delta),
    }


def rate_scores(gamma: complex, S: float, k: float) -> dict:
    g = float(np.real(gamma))
    g = max(g, 0.0)
    pred_fkr = fkr_growth(S, k)
    pred_sp = sweet_parker_rate(S)
    pred_coppi = coppi_growth(S, k)
    pred_pl = plasmoid_max_growth(S)
    # relative residuals against each branch (only meaningful if g>0)
    def rel(pred):
        if g <= 0.0:
            return np.nan
        return abs(g - pred) / (abs(pred) + abs(g) + 1e-16)

    return {
        "gamma_re": float(np.real(gamma)),
        "gamma_im": float(np.imag(gamma)),
        "pred_FKR": pred_fkr,
        "pred_SP": pred_sp,
        "pred_Coppi": pred_coppi,
        "pred_plasmoid": pred_pl,
        "res_FKR": rel(pred_fkr) if pred_fkr > 0 else np.nan,
        "res_SP": rel(pred_sp),
        "res_Coppi": rel(pred_coppi),
        "res_plasmoid": rel(pred_pl),
        "best_branch": _best_branch(g, pred_fkr, pred_sp, pred_coppi, pred_pl, k),
    }


def _best_branch(g, fkr, sp, coppi, pl, k) -> str:
    if g <= 0:
        return "stable"
    cands = []
    if fkr > 0:
        cands.append(("FKR", abs(g - fkr) / (fkr + g)))
    cands.append(("Sweet-Parker", abs(g - sp) / (sp + g)))
    cands.append(("Coppi", abs(g - coppi) / (coppi + g)))
    # plasmoid S^{1/4} is not a prediction for a fixed-thickness Harris sheet
    if not cands:
        return "none"
    cands.sort(key=lambda t: t[1])
    return cands[0][0]


# ---------------------------------------------------------------------------
# 2×2 Galerkin companion (layer reduction, not the test)
# ---------------------------------------------------------------------------


def galerkin_2x2(S: float, k: float, z: np.ndarray, Dzz: np.ndarray) -> dict:
    """
    Project the 2-field operator onto two even-ψ trial pairs.
    This is the 'small N×N / transfer matrix in the layer' companion.
    """
    Aop, Lap, z_i = assemble_operator(S, k, z, Dzz)
    sech = 1.0 / np.cosh(z_i)
    psi_a = sech
    u_a = np.tanh(z_i) * sech
    psi_b = sech ** 3
    u_b = np.tanh(z_i) * sech ** 3
    Va = np.concatenate([psi_a, u_a])
    Vb = np.concatenate([psi_b, u_b])
    Q = np.column_stack([Va, Vb])
    # L2 Galerkin reduction of the standard operator
    H2 = Q.conj().T @ Aop @ Q
    G2 = Q.conj().T @ Q
    try:
        w = linalg.eigvals(H2, G2)
        A = linalg.solve(G2, H2)
    except linalg.LinAlgError:
        return {"evals": np.array([np.nan, np.nan]), "gap": np.nan, "defective": False}
    gap = float(np.abs(w[0] - w[1])) if w.size == 2 else np.nan
    s = np.linalg.svd(A - np.mean(w) * np.eye(2), compute_uv=False)
    defect = float(s[1] / (s[0] + 1e-16)) if s.size == 2 else 0.0
    return {
        "evals": w,
        "gap": gap,
        "defect": defect,
        "defective": bool(gap < 0.02 and defect > 0.05),
        "H": A,
    }


# ---------------------------------------------------------------------------
# Sweeps, EP hunt, monodromy
# ---------------------------------------------------------------------------


@dataclass
class SweepPoint:
    S: float
    k: float
    Delta_prime: float
    gamma_re: float
    gamma_im: float
    R_EP: float
    R_Puiseux: float
    R_conn: float
    R_rate: float
    R_mono: float
    R_CS: float
    R_MHD: float
    pred_FKR: float
    pred_SP: float
    pred_Hall: float
    pred_plasmoid: float
    best_branch: str
    even_frac: float
    gap: float
    petermann: float
    defective: bool
    n_sheet: int
    Gamma_lo: float
    Gamma_hi: float
    onset: bool
    resolved_SP: bool


def build_grid(n: int = 201, zmax: float = 12.0, beta: float = 5.5):
    z, Dzz, _ = mapped_dzz(n, zmax, beta)
    return z, Dzz


def sweep(
    S_vals: np.ndarray,
    k_vals: np.ndarray,
    z: np.ndarray,
    Dzz: np.ndarray,
) -> list[SweepPoint]:
    rows: list[SweepPoint] = []
    cache: dict[tuple[float, float], EigenResult] = {}
    for S in S_vals:
        for k in k_vals:
            er = solve_spectrum(float(S), float(k), z, Dzz)
            cache[(float(S), float(k))] = er
            conn = connectivity_jump(er.z, er.psi, k, amp=0.12)
            hol = ohmic_and_holonomy(er.z, er.psi, k, S)
            rates = rate_scores(er.tearing_gamma, S, k)
            onset = bool(er.tearing_gamma.real > 0.0 and er.even_frac > 0.55)
            # Hall prediction is Object-2 physics; quoted only as a comparison column
            pred_hall = S ** (-0.25)
            rows.append(
                SweepPoint(
                    S=float(S),
                    k=float(k),
                    Delta_prime=float(er.delta_prime),
                    gamma_re=float(er.tearing_gamma.real),
                    gamma_im=float(er.tearing_gamma.imag),
                    R_EP=np.nan,  # filled after EP hunt
                    R_Puiseux=np.nan,
                    R_conn=float(conn["R_conn"] if onset else 0.0),
                    R_rate=float(max(er.tearing_gamma.real, 0.0)),
                    R_mono=np.nan,
                    R_CS=float(hol["R_CS"]),
                    R_MHD=float(hol["R_MHD"]),
                    pred_FKR=rates["pred_FKR"],
                    pred_SP=rates["pred_SP"],
                    pred_Hall=float(pred_hall),
                    pred_plasmoid=rates["pred_plasmoid"],
                    best_branch=rates["best_branch"],
                    even_frac=er.even_frac,
                    gap=er.gap,
                    petermann=er.petermann,
                    defective=er.defective,
                    n_sheet=0 if abs(er.tearing_gamma.imag) < 1e-6 else 1,
                    Gamma_lo=float(-k),
                    Gamma_hi=float(k),
                    onset=onset,
                    resolved_SP=bool(er.resolved["resolved_SP"]),
                )
            )
    return rows, cache


def hunt_ep(rows: list[SweepPoint], cache: dict) -> dict:
    """
    Nearest defective coalescence to the reconnection threshold.
    Threshold: Δ' = 0 (k=1) and/or first Re(γ)>0 with even parity.
    """
    defective_pts = [r for r in rows if r.defective]
    onset_pts = [r for r in rows if r.onset]
    # smallest gap among points with a finite discrete partner (not the cut)
    gapped = [r for r in rows if r.gap == r.gap and r.gap > 0]
    gaps = sorted(gapped, key=lambda r: r.gap)
    smallest_gap = gaps[0] if gaps else None

    # onset boundary: among each S, the largest k with onset, or k=1
    onset_boundary = []
    S_vals = sorted({r.S for r in rows})
    for S in S_vals:
        sl = [r for r in rows if r.S == S]
        unstable = [r for r in sl if r.onset]
        if unstable:
            onset_boundary.append(max(unstable, key=lambda r: r.k))
        else:
            onset_boundary.append(min(sl, key=lambda r: abs(r.Delta_prime)))

    def dist_to_onset(r: SweepPoint) -> float:
        # log-S / k metric
        best = np.inf
        for o in onset_boundary:
            d = np.sqrt((np.log10(r.S + 1e-12) - np.log10(o.S + 1e-12)) ** 2
                        + (r.k - o.k) ** 2)
            best = min(best, d)
        # also distance to the analytic Δ'=0 line k=1
        d_line = abs(r.k - 1.0)
        return float(min(best, d_line))

    if defective_pts:
        nearest = min(defective_pts, key=dist_to_onset)
        R_EP = dist_to_onset(nearest)
        source = "defective_pair"
    else:
        nearest = smallest_gap
        R_EP = np.nan
        source = "no_discrete_EP2"  # small gaps are Alfvén-cut / grid, not Jordan EP2

    # Puiseux at the candidate: need a local 1D cut. Use k-scan at that S.
    puis = {"exponent": np.nan, "residual": np.nan, "passed": False, "c": np.nan}
    if defective_pts and nearest is not None:
        puis = puiseux_along_k(cache, nearest.S, nearest.k)

    # fill R_EP / R_Puiseux on every row: distance of THAT row's gap-minimum
    # to threshold, plus the global candidate residual
    for r in rows:
        # small only if a defective coalescence sits on the threshold at this point
        if r.defective:
            r.R_EP = dist_to_onset(r)
        else:
            r.R_EP = float("nan") if R_EP != R_EP else float(R_EP) + dist_to_onset(r)
        r.R_Puiseux = float(puis["residual"]) if np.isfinite(puis["residual"]) else np.nan

    return {
        "source": source,
        "nearest": nearest,
        "R_EP_global": float(R_EP) if R_EP == R_EP else np.nan,
        "puiseux": puis,
        "n_defective": len(defective_pts),
        "min_gap": float(smallest_gap.gap) if smallest_gap else np.nan,
        "min_gap_at": (smallest_gap.S, smallest_gap.k) if smallest_gap else None,
        "onset_boundary": [(o.S, o.k, o.gamma_re) for o in onset_boundary],
    }


def puiseux_along_k(cache: dict, S0: float, k0: float) -> dict:
    """Fit |λ - λ0| ~ c |k - k0|^p using tearing eigenvalues at fixed S."""
    pts = [(k, er) for (S, k), er in cache.items() if abs(S - S0) < 1e-12]
    if len(pts) < 5:
        return {"exponent": np.nan, "residual": np.nan, "passed": False, "c": np.nan}
    pts.sort(key=lambda t: t[0])
    ks = np.array([p[0] for p in pts])
    gs = np.array([p[1].tearing_gamma for p in pts])
    # coalescence proxy: minimum |γ - partner| or min |dγ/dk| stall
    gaps = np.array([p[1].gap for p in pts])
    i0 = int(np.argmin(np.abs(ks - k0)))
    lam0 = gs[i0]
    # use a neighbourhood
    d = np.abs(ks - ks[i0])
    mask = (d > 1e-8) & (d < 0.35)
    if np.count_nonzero(mask) < 4:
        return {"exponent": np.nan, "residual": np.nan, "passed": False, "c": np.nan}
    split = np.abs(gs[mask] - lam0)
    logd = np.log(d[mask])
    logs = np.log(np.maximum(split, 1e-16))
    # drop non-positive
    ok = np.isfinite(logs) & np.isfinite(logd)
    if np.count_nonzero(ok) < 4:
        return {"exponent": np.nan, "residual": np.nan, "passed": False, "c": np.nan}
    p, intercept = np.polyfit(logd[ok], logs[ok], 1)
    fit = np.exp(intercept) * d[mask] ** p
    rel = np.max(np.abs(split - fit) / (split + fit + 1e-16))
    return {
        "exponent": float(p),
        "residual": float(rel),
        "passed": bool(abs(p - 0.5) < 0.12 and rel < 0.25),
        "c": float(np.exp(intercept)),
        "n": int(np.count_nonzero(ok)),
    }


def monodromy_around(
    z: np.ndarray,
    Dzz: np.ndarray,
    S0: float,
    k0: float,
    r_logS: float = 0.15,
    r_k: float = 0.08,
    n_theta: int = 48,
    n_loops: float = 2.0,
) -> dict:
    """
    Real 2-parameter loop in (log S, k) around (S0, k0).
    EP2 must swap after 2π and return after 4π. A regular onset (γ through 0)
    does not swap sheets.
    """
    theta = np.linspace(0.0, n_loops * 2.0 * np.pi, n_theta)
    evals = np.zeros((n_theta, 2), dtype=complex)
    overlaps = np.zeros(n_theta, dtype=complex)
    psi0 = None
    for i, th in enumerate(theta):
        S = S0 * (10.0 ** (r_logS * np.cos(th)))
        k = k0 + r_k * np.sin(th)
        k = max(k, 0.15)
        er = solve_spectrum(S, k, z, Dzz)
        # tearing + partner
        evals[i, 0] = er.tearing_gamma
        evals[i, 1] = er.partner_gamma
        if i == 0:
            psi0 = er.psi.copy()
            overlaps[i] = 1.0 + 0j
        else:
            # continue sheets
            prev = evals[i - 1]
            curr = evals[i].copy()
            if abs(curr[0] - prev[0]) + abs(curr[1] - prev[1]) > abs(curr[0] - prev[1]) + abs(curr[1] - prev[0]):
                evals[i] = curr[::-1]
            ov = np.vdot(psi0, er.psi)
            nrm = (np.linalg.norm(psi0) * np.linalg.norm(er.psi) + 1e-30)
            overlaps[i] = ov / nrm
    i2 = int(np.argmin(np.abs(theta - 2.0 * np.pi)))
    i4 = n_theta - 1
    swap_2pi = abs(evals[i2, 0] - evals[0, 1]) + abs(evals[i2, 1] - evals[0, 0])
    stay_2pi = abs(evals[i2, 0] - evals[0, 0]) + abs(evals[i2, 1] - evals[0, 1])
    stay_4pi = abs(evals[i4, 0] - evals[0, 0]) + abs(evals[i4, 1] - evals[0, 1])
    swapped = swap_2pi < stay_2pi
    returned_4pi = stay_4pi < 0.2 * (abs(evals[0, 0]) + abs(evals[0, 1]) + 0.2)
    ep2 = bool(swapped and returned_4pi)
    return {
        "theta": theta,
        "evals": evals,
        "overlaps": overlaps,
        "swapped_at_2pi": swapped,
        "returned_4pi": returned_4pi,
        "ep2_monodromy": ep2,
        "S0": S0,
        "k0": k0,
        "overlap_2pi": complex(overlaps[i2]),
        "overlap_4pi": complex(overlaps[i4]),
        "stay_2pi": float(stay_2pi),
        "swap_2pi": float(swap_2pi),
        "stay_4pi": float(stay_4pi),
    }


def operator_selfcheck(z, Dzz) -> dict:
    """Sanity: unstable at (S=200, k=0.5), stable at (S=200, k=1.3)."""
    er_u = solve_spectrum(200.0, 0.5, z, Dzz)
    er_s = solve_spectrum(200.0, 1.3, z, Dzz)
    ok = (er_u.tearing_gamma.real > 0.0) and (er_s.tearing_gamma.real <= 0.05)
    return {
        "ok": bool(ok),
        "gamma_unstable": complex(er_u.tearing_gamma),
        "even_unstable": er_u.even_frac,
        "gamma_stable": complex(er_s.tearing_gamma),
        "even_stable": er_s.even_frac,
        "resolved": er_u.resolved,
    }


def run_object1(outdir: Path, n: int = 201) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    z, Dzz = build_grid(n=n, zmax=12.0, beta=5.5)
    check = operator_selfcheck(z, Dzz)
    S_vals = np.array([50.0, 100.0, 200.0, 500.0, 1000.0, 2000.0])
    k_vals = np.array([0.30, 0.45, 0.55, 0.70, 0.85, 0.95, 1.00, 1.10, 1.30])
    rows, cache = sweep(S_vals, k_vals, z, Dzz)
    hunt = hunt_ep(rows, cache)

    # monodromy: around nearest candidate if any, else around onset (S=500, k=1)
    if hunt["nearest"] is not None:
        S0, k0 = hunt["nearest"].S, hunt["nearest"].k
    else:
        S0, k0 = 500.0, 1.0
    # also always loop the analytic onset point
    mono_onset = monodromy_around(z, Dzz, 500.0, 1.00, r_logS=0.12, r_k=0.10, n_theta=36)
    mono_cand = monodromy_around(z, Dzz, S0, k0, r_logS=0.12, r_k=0.08, n_theta=36)
    for r in rows:
        # R_mono: 0 if this point's neighbourhood shows EP2 4π, 1 otherwise
        r.R_mono = 0.0 if mono_cand["ep2_monodromy"] else 1.0

    # Galerkin companion on the same grid
    gal_rows = []
    for S in S_vals:
        for k in [0.5, 1.0]:
            gal_rows.append({"S": S, "k": k, **{kk: vv for kk, vv in galerkin_2x2(S, k, z, Dzz).items() if kk != "H"}})

    # persist
    recs = [asdict(r) for r in rows]
    np.savez(
        outdir / "object1_data.npz",
        S=np.array([r.S for r in rows]),
        k=np.array([r.k for r in rows]),
        Delta_prime=np.array([r.Delta_prime for r in rows]),
        gamma_re=np.array([r.gamma_re for r in rows]),
        gamma_im=np.array([r.gamma_im for r in rows]),
        R_EP=np.array([r.R_EP for r in rows]),
        R_Puiseux=np.array([r.R_Puiseux for r in rows]),
        R_conn=np.array([r.R_conn for r in rows]),
        R_rate=np.array([r.R_rate for r in rows]),
        R_mono=np.array([r.R_mono for r in rows]),
        R_CS=np.array([r.R_CS for r in rows]),
        R_MHD=np.array([r.R_MHD for r in rows]),
        gap=np.array([r.gap for r in rows]),
        petermann=np.array([r.petermann for r in rows]),
        even_frac=np.array([r.even_frac for r in rows]),
        pred_FKR=np.array([r.pred_FKR for r in rows]),
        pred_SP=np.array([r.pred_SP for r in rows]),
        pred_Hall=np.array([r.pred_Hall for r in rows]),
        pred_plasmoid=np.array([r.pred_plasmoid for r in rows]),
        z_grid=z,
    )
    # store a representative eigenfunction at an unstable point
    er_ref = cache[(200.0, 0.55)] if (200.0, 0.55) in cache else next(iter(cache.values()))

    # pass condition
    R_EP_g = hunt["R_EP_global"]
    puis = hunt["puiseux"]
    # lock: small R_EP AND small R_Puiseux AND R_conn lights at same (S,k)
    lock = False
    lock_reason = []
    if hunt["n_defective"] == 0:
        lock_reason.append("no defective coalescence in the (S, k) grid")
        lock_reason.append("Puiseux N/A (no discrete EP2 to expand about)")
    else:
        near = hunt["nearest"]
        if R_EP_g is not None and R_EP_g == R_EP_g and R_EP_g < 0.15:
            lock_reason.append(f"EP near onset (R_EP={R_EP_g:.3f})")
        else:
            lock_reason.append(f"EP not at onset (R_EP={R_EP_g})")
        if near is not None and near.onset and near.R_conn > 0.5:
            lock_reason.append("R_conn lights at the EP point")
        else:
            lock_reason.append("R_conn does not light at the EP point")
        if puis.get("passed"):
            lock_reason.append(f"square-root Puiseux p={puis.get('exponent')}")
        else:
            lock_reason.append(
                f"Puiseux not EP2 (p={puis.get('exponent')}, res={puis.get('residual')})"
            )
    if mono_cand["ep2_monodromy"]:
        lock_reason.append("4π monodromy around candidate")
    else:
        lock_reason.append("no 4π EP2 monodromy around candidate")

    # dictionary requires ALL of: small R_EP, small R_Puiseux, R_conn at same value,
    # and exponent/gap matching a rate scaling
    near = hunt["nearest"]
    ep_small = (hunt["n_defective"] > 0) and (R_EP_g == R_EP_g) and (R_EP_g < 0.15)
    puis_small = bool(puis.get("passed"))
    conn_lock = bool(near is not None and near.onset and near.R_conn > 0.5)
    # rate lock: Puiseux p matches 1/2 (SP), 3/5 (FKR), or 1/3 (Coppi)
    p = puis.get("exponent", np.nan)
    rate_lock = False
    if p == p:
        rate_lock = min(abs(p - 0.5), abs(p - 0.6), abs(p - 1.0 / 3.0)) < 0.12
    # also: tearing growth itself matching FKR is NOT an EP dictionary unless EP locks
    lock = bool(ep_small and puis_small and conn_lock and rate_lock)

    # measured γ(S) exponent at ka≈0.55 (FKR 3/5, SP 1/2, Coppi 1/3)
    k_scale = 0.55
    scale_pts = [(r.S, r.gamma_re) for r in rows if abs(r.k - k_scale) < 1e-12 and r.gamma_re > 0]
    scale_fit = {"p": np.nan, "r": np.nan}
    if len(scale_pts) >= 4:
        Ss = np.log([p[0] for p in scale_pts])
        gs = np.log([p[1] for p in scale_pts])
        p, _ = np.polyfit(Ss, gs, 1)
        scale_fit = {"p": float(p), "r": float(np.corrcoef(Ss, gs)[0, 1])}

    if lock:
        verdict = "dictionary"
    elif hunt["n_defective"] > 0 and not conn_lock:
        verdict = "spectral decoration, not dictionary"
    elif check["ok"] and any(r.onset for r in rows) and hunt["n_defective"] == 0:
        verdict = "spectral decoration, not dictionary"
    else:
        verdict = "grid artefact" if not check["ok"] else "spectral decoration, not dictionary"

    return {
        "check": check,
        "rows": rows,
        "cache": cache,
        "hunt": hunt,
        "mono_onset": mono_onset,
        "mono_cand": mono_cand,
        "galerkin": gal_rows,
        "er_ref": er_ref,
        "z": z,
        "Dzz": Dzz,
        "lock": lock,
        "verdict": verdict,
        "lock_reason": lock_reason,
        "S_vals": S_vals,
        "k_vals": k_vals,
        "scale_fit": scale_fit,
    }

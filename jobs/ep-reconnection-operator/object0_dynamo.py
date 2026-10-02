"""
OBJECT 0 — Günther–Stefani–Gerbeth 2004 2×2 α²-dynamo toy
arXiv:math-ph/0407015, eqs. (45)–(93)

H = [[a, b], [-b*, d]] = e0 I + [[f, b], [-b*, -f]]
E = e0 ± sqrt(f^2 - |b|^2)

Branching EP2: cone Δ = f^2 - |b|^2 = 0 with |b| ≠ 0
  algebraic multiplicity 2, geometric multiplicity 1 (Jordan block)
Diabolic point: f = |b| = 0
  algebraic = geometric = 2 (diagonal)

Stop unless a square-root Puiseux split is observed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

# Paper's involutive metric for J-pseudo-Hermiticity in the Z2-graded frame.
MU = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def dynamo_H(f: complex, b: complex, e0: complex = 0.0) -> np.ndarray:
    """Z2-graded pseudo-Hermitian 2×2 of GSG 2004 eq. (45)."""
    return np.array(
        [[e0 + f, b], [-np.conjugate(b), e0 - f]],
        dtype=complex,
    )


def hermitian_spin_H(f: complex, b: complex, e0: complex = 0.0) -> np.ndarray:
    """Hermitian control: diabolic crossing only at the origin."""
    return np.array(
        [[e0 + f, b], [np.conjugate(b), e0 - f]],
        dtype=complex,
    )


def analytic_eigenvalues(f: complex, b: complex, e0: complex = 0.0) -> np.ndarray:
    disc = f * f - b * np.conjugate(b)
    root = np.sqrt(disc + 0j)
    return np.array([e0 - root, e0 + root], dtype=complex)


@dataclass
class SpectrumPoint:
    param: complex
    evals: np.ndarray
    evecs: np.ndarray  # columns are right eigenvectors
    gap: float
    jordan_defect: float
    petermann: float


def _normalize_phase(v: np.ndarray) -> np.ndarray:
    v = v / (np.linalg.norm(v) + 1e-16)
    # pin a globally-defined phase: first component of largest |entry|
    k = int(np.argmax(np.abs(v)))
    phase = np.angle(v[k])
    return v * np.exp(-1j * phase)


def eigenpairs(H: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    w, V = np.linalg.eig(H)
    # sort by real then imag for a stable but not sheet-faithful order
    order = np.lexsort((w.imag, w.real))
    return w[order], V[:, order]


def jordan_defect(H: np.ndarray, tol: float = 1e-9) -> float:
    """
    0 at a diagonalizable degeneracy (diabolic), 1 at a rank-1 Jordan block (EP2).
    Uses the gap between algebraic coalescence and the number of independent
    eigenvectors estimated from SVD of (H - λI) at the mean eigenvalue.
    """
    w, _ = np.linalg.eig(H)
    # two-level matrix: use both eigenvalues' midpoint
    lam = 0.5 * (w[0] + w[1])
    s = np.linalg.svd(H - lam * np.eye(2), compute_uv=False)
    # defective EP: one singular value ~0, the other finite
    if s[0] < tol:
        return 0.0  # both singular ~ zero: scalar matrix (diabolic)
    return float(s[1] / (s[0] + 1e-16))


def petermann_factor(H: np.ndarray) -> float:
    """1/|<L|R>|^2 for the first eigenpair. Diverges at an EP."""
    w, Vr = np.linalg.eig(H)
    wl, Vl = np.linalg.eig(H.conj().T)
    j = int(np.argmin(np.abs(wl - w[0].conj())))
    L = Vl[:, j]
    R = Vr[:, 0]
    ov = np.vdot(L, R)
    return float(1.0 / (np.abs(ov) ** 2 + 1e-30))


def scan_real_f(f_grid: np.ndarray, b: complex, e0: complex = 0.0) -> dict:
    evals = np.zeros((f_grid.size, 2), dtype=complex)
    defects = np.zeros(f_grid.size)
    petermanns = np.zeros(f_grid.size)
    for i, f in enumerate(f_grid):
        H = dynamo_H(complex(f), b, e0)
        # analytic sheet: E = e0 ± sqrt(f^2 - |b|^2), principal sqrt
        w = analytic_eigenvalues(complex(f), b, e0)
        evals[i] = w
        defects[i] = jordan_defect(H)
        petermanns[i] = petermann_factor(H)
    return {
        "f": f_grid,
        "evals": evals,
        "defect": defects,
        "petermann": petermanns,
        "b": b,
        "e0": e0,
        "f_ep": float(np.abs(b)),
        "f_dp": 0.0,
    }


def puiseux_test(
    b: complex = 1.0,
    e0: complex = 0.0,
    eps_grid: np.ndarray | None = None,
) -> dict:
    """
    Approach the EP f = |b| along f = |b| + eps, eps > 0 small (inside the
    complex-conjugate sheet if we take f = |b| - eps, real-split if +eps
    wait: Δ = f^2 - |b|^2 = (f-|b|)(f+|b|). For f = |b| + eps, Δ > 0, real split.
    Square-root: E ≈ e0 ± sqrt(2|b| eps).
    """
    if eps_grid is None:
        eps_grid = np.logspace(-8, -2, 25)
    f_ep = np.abs(b)
    lam_num = np.zeros((eps_grid.size, 2), dtype=complex)
    lam_fit = np.zeros_like(lam_num)
    c = np.sqrt(2.0 * f_ep)
    for i, eps in enumerate(eps_grid):
        f = f_ep + eps
        H = dynamo_H(complex(f), b, e0)
        w, _ = eigenpairs(H)
        # sort by real part so ± assignment is stable on the real-split side
        w = w[np.argsort(w.real)]
        lam_num[i] = w
        lam_fit[i] = np.array([e0 - c * np.sqrt(eps), e0 + c * np.sqrt(eps)])
    residual = np.abs(lam_num - lam_fit)
    # relative to the split scale
    scale = np.maximum(np.abs(lam_fit), 1e-16)
    rel = residual / scale
    return {
        "eps": eps_grid,
        "lam_num": lam_num,
        "lam_fit": lam_fit,
        "residual": residual,
        "rel_residual": rel,
        "max_rel_residual": float(np.max(rel)),
        "c": float(c),
        "exponent_fit": _fit_puiseux_exponent(eps_grid, lam_num, e0),
        "passed": bool(np.max(rel) < 5e-3) and _fit_puiseux_exponent(eps_grid, lam_num, e0)[0] > 0.45,
    }


def _fit_puiseux_exponent(eps: np.ndarray, lam: np.ndarray, e0: complex) -> tuple[float, float]:
    """log|λ - λ0| ~ p log|eps| + const. Expect p = 1/2."""
    split = 0.5 * np.abs(lam[:, 1] - lam[:, 0])
    mask = (eps > 0) & (split > 0)
    loge = np.log(eps[mask])
    logs = np.log(split[mask])
    p, _ = np.polyfit(loge, logs, 1)
    r = np.corrcoef(loge, logs)[0, 1]
    return float(p), float(r)


def _align_sheets(prev: np.ndarray, curr: np.ndarray) -> np.ndarray:
    """Permutation that continues prev → curr by nearest neighbour."""
    d00 = np.abs(curr[0] - prev[0]) + np.abs(curr[1] - prev[1])
    d01 = np.abs(curr[0] - prev[1]) + np.abs(curr[1] - prev[0])
    if d01 < d00:
        return curr[::-1].copy()
    return curr.copy()


def _align_evecs(prev: np.ndarray, curr: np.ndarray) -> np.ndarray:
    """Match columns of curr to prev by overlap, then pin phase to be continuous."""
    out = curr.copy()
    # permutation
    ov = np.abs(prev.conj().T @ curr)
    # greedy
    used = set()
    perm = [0, 1]
    for i in range(2):
        j = int(np.argmax(ov[i]))
        if j in used:
            j = 1 - j
        used.add(j)
        perm[i] = j
    out = curr[:, perm]
    for i in range(2):
        phase = np.vdot(prev[:, i], out[:, i])
        if np.abs(phase) > 0:
            out[:, i] = out[:, i] * np.exp(-1j * np.angle(phase))
        out[:, i] = out[:, i] / (np.linalg.norm(out[:, i]) + 1e-16)
    return out


def monodromy_loop(
    f_ep: float = 1.0,
    b: complex = 1.0,
    radius: float = 0.35,
    n_theta: int = 721,
    e0: complex = 0.0,
    n_loops: float = 2.0,
) -> dict:
    """
    Encircle one EP2 in the complex-f plane: f(θ) = f_ep + r e^{iθ}, θ: 0 → 4π.
    EP2 signature: eigenvalues swap after 2π, eigenvectors pick a minus sign
    after 2π and return after 4π.
    """
    theta = np.linspace(0.0, n_loops * 2.0 * np.pi, n_theta)
    f_path = f_ep + radius * np.exp(1j * theta)
    evals = np.zeros((n_theta, 2), dtype=complex)
    evecs = np.zeros((n_theta, 2, 2), dtype=complex)
    overlaps = np.zeros((n_theta, 2), dtype=complex)
    H0 = dynamo_H(complex(f_path[0]), b, e0)
    w, V = eigenpairs(H0)
    V = np.column_stack([_normalize_phase(V[:, 0]), _normalize_phase(V[:, 1])])
    evals[0] = w
    evecs[0] = V
    overlaps[0] = np.array([1.0 + 0j, 1.0 + 0j])
    for i in range(1, n_theta):
        H = dynamo_H(complex(f_path[i]), b, e0)
        w, V = np.linalg.eig(H)
        w = _align_sheets(evals[i - 1], w)
        # eig does not know the permutation we just applied
        w_raw, V_raw = np.linalg.eig(H)
        # pair columns of V_raw with aligned w
        perm = [int(np.argmin(np.abs(w_raw - w[0]))), 0]
        perm[1] = 1 - perm[0] if np.argmin(np.abs(w_raw - w[1])) == perm[0] else int(
            np.argmin(np.abs(w_raw - w[1]))
        )
        if perm[0] == perm[1]:
            perm = [0, 1]
        V = V_raw[:, perm]
        V = _align_evecs(evecs[i - 1], V)
        evals[i] = w
        evecs[i] = V
        overlaps[i, 0] = np.vdot(evecs[0, :, 0], V[:, 0])
        overlaps[i, 1] = np.vdot(evecs[0, :, 1], V[:, 1])

    # diagnostics at 2π and 4π
    i2 = int(np.argmin(np.abs(theta - 2.0 * np.pi)))
    i4 = int(np.argmin(np.abs(theta - 4.0 * np.pi))) if theta[-1] >= 4.0 * np.pi - 1e-12 else n_theta - 1

    swap_2pi = float(np.abs(evals[i2, 0] - evals[0, 1]) + np.abs(evals[i2, 1] - evals[0, 0]))
    noswap_2pi = float(np.abs(evals[i2, 0] - evals[0, 0]) + np.abs(evals[i2, 1] - evals[0, 1]))
    swapped_at_2pi = swap_2pi < noswap_2pi

    # After analytic continuation, at 2π the sheets have swapped, so compare
    # continued vector 0 to the *other* original vector, up to a sign.
    # With our continuation, vector 0 at 2π is the continuation of vector 0,
    # which should equal - original vector 1 (up to the swap identification).
    # Kato EP2: the eigenvector acquires a sign after one full loop of the
    # *same* sheet, which takes 4π in the parameter. After 2π one has swapped
    # sheets; after 4π both eigenvalue and eigenvector return, with a possible
    # global sign that we have already aligned away locally.
    return_2pi_eval = noswap_2pi
    return_4pi_eval = float(np.abs(evals[i4, 0] - evals[0, 0]) + np.abs(evals[i4, 1] - evals[0, 1]))
    ov2 = overlaps[i2]
    ov4 = overlaps[i4]
    # sign change on a sheet: |overlap| ~ 1 but Re(overlap) ~ -1 after 4π if
    # we did not continuously align; we DID continuously align, so overlap
    # stays near +1 along a sheet. Report the un-aligned winding instead.
    winding = _eigenvector_winding(evecs, theta)

    ep2_monodromy = bool(swapped_at_2pi) and (return_4pi_eval < 0.05) and (winding["needs_4pi"])

    return {
        "theta": theta,
        "f_path": f_path,
        "evals": evals,
        "evecs": evecs,
        "overlaps": overlaps,
        "i2pi": i2,
        "i4pi": i4,
        "swapped_at_2pi": swapped_at_2pi,
        "return_2pi_eval": return_2pi_eval,
        "return_4pi_eval": return_4pi_eval,
        "overlap_2pi": ov2,
        "overlap_4pi": ov4,
        "winding": winding,
        "ep2_monodromy": ep2_monodromy,
        "radius": radius,
        "f_ep": f_ep,
        "b": b,
    }


def _eigenvector_winding(evecs: np.ndarray, theta: np.ndarray) -> dict:
    """
    Track arg of the dominant component of continued eigenvector 0.
    A square-root branch gives a π phase after 2π parameter rotation
    (sign flip on the swapped identification) and 2π phase after 4π.
    """
    v = evecs[:, :, 0]
    # use a component that is not sitting on a zero
    k = 0 if np.mean(np.abs(v[:, 0])) >= np.mean(np.abs(v[:, 1])) else 1
    arg = np.unwrap(np.angle(v[:, k]))
    i2 = int(np.argmin(np.abs(theta - 2.0 * np.pi)))
    i4 = int(np.argmin(np.abs(theta - 4.0 * np.pi))) if theta[-1] >= 4.0 * np.pi - 1e-12 else len(theta) - 1
    d2 = arg[i2] - arg[0]
    d4 = arg[i4] - arg[0]
    # 4π return of the state vector (up to the continuous alignment which
    # removes 2π jumps) is encoded in whether a *discontinuous* sheet swap
    # is required at 2π. We already know that from eigenvalues.
    # Additional: the projective eigenvector (v ~ -v) returns after 2π,
    # the true vector after 4π. Measure the smallest principal-angle
    # distance on RP1 vs C^2.
    def princ_angle(a, b):
        ov = np.abs(np.vdot(a, b))
        return float(np.arccos(np.clip(ov, 0.0, 1.0)))

    v0 = evecs[0, :, 0]
    ang2 = princ_angle(v0, evecs[i2, :, 0])
    ang4 = princ_angle(v0, evecs[i4, :, 0])
    # After 2π, continued sheet-0 vector is the *other* eigenvector:
    ang2_cross = princ_angle(evecs[0, :, 1], evecs[i2, :, 0])
    needs_4pi = (ang4 < 0.2) and (ang2_cross < 0.3 or ang2 > 0.5)
    return {
        "arg": arg,
        "component": k,
        "delta_arg_2pi": float(d2),
        "delta_arg_4pi": float(d4),
        "rp_angle_2pi": ang2,
        "rp_angle_4pi": ang4,
        "rp_angle_2pi_cross": ang2_cross,
        "needs_4pi": bool(needs_4pi),
    }


def diabolic_contrast(radius: float = 0.35, n_theta: int = 361) -> dict:
    """Hermitian spin loop around the origin: no square-root split, DP only."""
    theta = np.linspace(0.0, 2.0 * np.pi, n_theta)
    # circle in (f, b) around 0: f = r cos θ, b = r sin θ (real)
    evals = np.zeros((n_theta, 2), dtype=complex)
    gap = np.zeros(n_theta)
    for i, th in enumerate(theta):
        f = radius * np.cos(th)
        b = radius * np.sin(th)
        w, _ = eigenpairs(hermitian_spin_H(f, b))
        evals[i] = w
        gap[i] = float(np.abs(w[1] - w[0]))
    return {
        "theta": theta,
        "evals": evals,
        "min_gap": float(np.min(gap)),
        "is_diabolic_only": bool(np.min(gap) > 0.5 * radius),  # gap = 2r on the circle
    }


def locate_ep_vs_dp(b: complex = 1.0) -> dict:
    """Explicit locations used in the plots."""
    return {
        "ep2_cone": "f^2 - |b|^2 = 0, |b| != 0",
        "ep2_points_in_slice_b_fixed": [complex(np.abs(b)), complex(-np.abs(b))],
        "diabolic_point": 0.0 + 0j,
        "codim_ep_real_params": 1,  # double cone in (f, b1, b2)
        "codim_dp_real_params": 3,
        "algebraic_mult_ep": 2,
        "geometric_mult_ep": 1,
        "algebraic_mult_dp": 2,
        "geometric_mult_dp": 2,
    }


def run_object0(outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    b = 1.0 + 0.0j
    e0 = 0.0
    f_grid = np.linspace(-2.5, 2.5, 501)
    spec = scan_real_f(f_grid, b, e0)
    puis = puiseux_test(b=b, e0=e0)
    mono = monodromy_loop(f_ep=1.0, b=b, radius=0.35, n_theta=721, e0=e0, n_loops=2.0)
    diab = diabolic_contrast()
    loc = locate_ep_vs_dp(b)

    np.savez(
        outdir / "object0_data.npz",
        f=spec["f"],
        evals=spec["evals"],
        defect=spec["defect"],
        petermann=spec["petermann"],
        puis_eps=puis["eps"],
        puis_lam=puis["lam_num"],
        puis_fit=puis["lam_fit"],
        puis_rel=puis["rel_residual"],
        theta=mono["theta"],
        f_path=mono["f_path"],
        mono_evals=mono["evals"],
        mono_evecs=mono["evecs"],
        overlaps=mono["overlaps"],
    )

    passed = bool(puis["passed"] and mono["ep2_monodromy"])
    summary = {
        "passed": passed,
        "puiseux": {
            "max_rel_residual": puis["max_rel_residual"],
            "exponent": puis["exponent_fit"][0],
            "exponent_r": puis["exponent_fit"][1],
            "passed": puis["passed"],
        },
        "monodromy": {
            "swapped_at_2pi": mono["swapped_at_2pi"],
            "return_4pi_eval": mono["return_4pi_eval"],
            "needs_4pi": mono["winding"]["needs_4pi"],
            "rp_angle_2pi": mono["winding"]["rp_angle_2pi"],
            "rp_angle_4pi": mono["winding"]["rp_angle_4pi"],
            "rp_angle_2pi_cross": mono["winding"]["rp_angle_2pi_cross"],
            "ep2_monodromy": mono["ep2_monodromy"],
        },
        "diabolic_contrast_min_gap": diab["min_gap"],
        "locations": loc,
        "spec": spec,
        "puis": puis,
        "mono": mono,
        "diab": diab,
    }
    return summary

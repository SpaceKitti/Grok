"""
Candidate pair A — two modes that live on the Alfvén cut, not tearing.

The ideal multiplication operator ω_A(x) = ε x on x∈[-1,1] has continuous
spectrum Γ(ε) = [-|ε|, |ε|]. Unique field-line labeling is the assignment
of a real frequency in Γ. Resistivity regularises ∂_xx and couples the
two labels. The two-mode Galerkin of that generator is the candidate
2×2 (GSG recipe applied to the cut, not to a dynamo).

  A = ε x + i η ∂_xx     (Im A < 0: damped),  Dirichlet on [-1,1]

Trial modes: the two lowest Dirichlet sines — the smoothest pair that
can still carry a left/right label imbalance. Off-diagonal = shear
⟨φ1, x φ2⟩. Diagonal = unequal Ohmic damping of n=1,2.

This is NOT the GSG dynamo matrix: the coupling is Hermitian (shear),
the grading is loss-asymmetric. It still allows a Jordan block.
"""

from __future__ import annotations

import numpy as np
from recipe import Checklist, jordan_defect, monodromy_loop, petermann, puiseux_real

ETA = 0.05
OMEGA0 = 0.0  # cut centred at 0


def _sines(x: np.ndarray, n: int) -> np.ndarray:
    return np.sin(n * np.pi * (x + 1.0) / 2.0)


def coupling_v() -> float:
    """⟨φ1, x φ2⟩ on [-1,1]."""
    x = np.linspace(-1.0, 1.0, 4001)
    w = np.trapezoid(_sines(x, 1) * x * _sines(x, 2), x)
    n1 = np.trapezoid(_sines(x, 1) ** 2, x)
    n2 = np.trapezoid(_sines(x, 2) ** 2, x)
    return float(w / np.sqrt(n1 * n2))


def damp_n(n: int, eta: float = ETA) -> float:
    """η (n π / 2)^2  so that iη ∂xx φ_n = -i * this * φ_n."""
    return eta * (n * np.pi / 2.0) ** 2


V = coupling_v()
A_DAMP = damp_n(1)
B_DAMP = damp_n(2)


def H_A(eps: complex, eta: float = ETA) -> np.ndarray:
    """
    2×2 cut operator, pair A.

        [ -i a    ,  ε v ]
        [  ε v    , -i b ]

    a = η(π/2)^2, b = η π^2, v = ⟨φ1, x φ2⟩.
    ε = shear (half-width of Γ). η = resistivity-as-cut-width, held fixed.
    """
    v = coupling_v()
    a = damp_n(1, eta)
    b = damp_n(2, eta)
    return np.array([[-1j * a, eps * v], [eps * v, -1j * b]], dtype=complex)


def Gamma(eps: float) -> tuple[float, float]:
    return (OMEGA0 - abs(eps), OMEGA0 + abs(eps))


def eps_ep_analytic(eta: float = ETA) -> float:
    """|ε v| = |b-a|/2  ⇒  EP2. Take the positive shear."""
    a, b = damp_n(1, eta), damp_n(2, eta)
    return float(abs(b - a) / (2.0 * abs(coupling_v())))


def lam_ep_analytic(eta: float = ETA) -> complex:
    a, b = damp_n(1, eta), damp_n(2, eta)
    return -0.5j * (a + b)


def on_cut(lam: complex, eps: float, eta: float = ETA) -> bool:
    lo, hi = Gamma(eps)
    # regularised cut sits O(η) off the real axis
    return bool((lo - 1e-9) <= lam.real <= (hi + 1e-9) and abs(lam.imag) <= 4.0 * (a_scale := (damp_n(1, eta) + damp_n(2, eta))))


def assemble_N(eps: float, n: int = 81, eta: float = ETA) -> np.ndarray:
    """N×N FD of ε x + i η ∂xx, Dirichlet. Check, not the 2×2 itself."""
    x = np.linspace(-1.0, 1.0, n)
    h = x[1] - x[0]
    interior = slice(1, -1)
    m = n - 2
    D2 = np.zeros((m, m))
    for i in range(m):
        D2[i, i] = -2.0 / h ** 2
        if i > 0:
            D2[i, i - 1] = 1.0 / h ** 2
        if i < m - 1:
            D2[i, i + 1] = 1.0 / h ** 2
    A = np.diag(OMEGA0 + eps * x[interior]) + 1j * eta * D2
    return A, x[interior]


def sweep_A(eps_grid: np.ndarray, eta: float = ETA) -> dict:
    evals = np.zeros((eps_grid.size, 2), dtype=complex)
    defects = np.zeros(eps_grid.size)
    pets = np.zeros(eps_grid.size)
    gaps = np.zeros(eps_grid.size)
    for i, e in enumerate(eps_grid):
        H = H_A(complex(e), eta)
        w = np.linalg.eigvals(H)
        # sort by real part so the two labels stay ordered off the EP
        w = w[np.argsort(w.real + 1e-9 * w.imag)]
        evals[i] = w
        gaps[i] = float(np.abs(w[0] - w[1]))
        defects[i] = jordan_defect(H)
        pets[i] = petermann(H, 0)
    return {
        "eps": eps_grid,
        "evals": evals,
        "gap": gaps,
        "defect": defects,
        "petermann": pets,
        "eta": eta,
        "v": coupling_v(),
        "a": damp_n(1, eta),
        "b": damp_n(2, eta),
    }


def sweep_N(eps_grid: np.ndarray, n: int = 81, eta: float = ETA) -> dict:
    """Track two least-damped N×N modes (closest to the real cut Γ)."""
    evals2 = np.zeros((eps_grid.size, 2), dtype=complex)
    gaps = np.zeros(eps_grid.size)
    for i, e in enumerate(eps_grid):
        A, _ = assemble_N(float(e), n=n, eta=eta)
        w = np.linalg.eigvals(A)
        # least-damped = smallest |Im| (Im is negative)
        order = np.argsort(np.abs(w.imag))
        pair = w[order[:2]]
        pair = pair[np.argsort(pair.real)]
        evals2[i] = pair
        gaps[i] = float(np.abs(pair[0] - pair[1]))
    return {"eps": eps_grid, "evals": evals2, "gap": gaps}


def score_A(eta: float = ETA) -> dict:
    eps_c = eps_ep_analytic(eta)
    lam_c = lam_ep_analytic(eta)
    H_c = H_A(eps_c, eta)
    w = np.linalg.eigvals(H_c)
    gap = float(np.abs(w[0] - w[1]))
    defect = jordan_defect(H_c, lam_c)
    K = petermann(H_c, 0)
    # Jordan: rank-1 at coalescence
    s = np.linalg.svd(H_c - lam_c * np.eye(2), compute_uv=False)
    jordan = bool(gap < 1e-8 and s[1] / (s[0] + 1e-16) > 0.05)
    # geometric multiplicity
    # one singular value ~0, one finite
    geom_one = bool(s[1] < 1e-8 * max(s[0], 1e-16) or (s[1] / (s[0] + 1e-16) > 1e-6 and s[0] > 1e-8))
    # more direct: nullity of (H-λI)
    rank = np.linalg.matrix_rank(H_c - lam_c * np.eye(2), tol=1e-8)
    geom_mult = 2 - rank if rank < 2 else 2
    jordan = bool(geom_mult == 1 and gap < 1e-6)

    puis = puiseux_real(lambda e: H_A(e, eta), eps_c, side=0.3 * eps_c)
    # approach from |ε| > ε_c (real-split side): disc = 4 (ε v)^2 - (a-b)^2 > 0
    puis = puiseux_real(lambda e: H_A(e, eta), eps_c, side=+0.35 * eps_c)

    mono = monodromy_loop(lambda z: H_A(z, eta), z_ep=complex(eps_c), radius=0.25 * eps_c)

    on = on_cut(lam_c, eps_c, eta)
    notes = (
        f"derived 2×2 of εx + iη∂xx on two Dirichlet sines; "
        f"ε_EP={eps_c:.6g}, λ_EP={lam_c}, Γ={Gamma(eps_c)}, "
        f"geom_mult={geom_mult}, rank(H-λI)={rank}"
    )
    chk = Checklist(
        ep2_found=bool(gap < 1e-6 and geom_mult == 1),
        jordan=jordan,
        puiseux_half=bool(puis["passed"]),
        mono_4pi=bool(mono["ep2_monodromy"]),
        on_cut=on,
        exponent=float(puis["exponent"]),
        defect=float(defect),
        petermann=float(K),
        lam_ep=complex(lam_c),
        eps_ep=float(eps_c),
        Gamma=Gamma(eps_c),
        notes=notes,
    )
    return {
        "checklist": chk,
        "puiseux": puis,
        "mono": mono,
        "H_ep": H_c,
        "matrix_form": (
            "H_A(ε) = [[ -i η(π/2)^2,  ε v ], [ ε v,  -i η π^2 ]]  "
            f"with v=⟨φ1,x φ2⟩={coupling_v():.6g}, η={eta}"
        ),
        "v": coupling_v(),
        "eta": eta,
    }

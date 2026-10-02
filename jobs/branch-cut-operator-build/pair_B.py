"""
Candidate pair B — two readings of the same meridian / slit.

Not tearing. Gravity reading of the cut vs MHD dissipation on Γ.

B1  dissipation vs CS defect sitting on the slit (holonomy diagonal = 0)
    H_B1(ε) = [[ -i η,  ε ],
               [  -ε,   0 ]]
    ε = shear (shared with pair A). η = cut-width (same number as pair A).

B2  GSG recipe with the two readings as the Z2 grading:
    MHD = shear/tension label split (diagonal), CS/Landau = cut-width (off-diagonal)
    H_B2(ε) = [[  ε,  η ],
               [ -η, -ε ]]
    This is the 2004 recipe pointed at the slit, not at the dynamo.

Do not claim MHD–QG unless an EP2 of A and of B sit at the same ε
and λ_EP lies on Γ.
"""

from __future__ import annotations

import numpy as np

from recipe import Checklist, jordan_defect, monodromy_loop, petermann, puiseux_real

from pair_A import ETA, Gamma, on_cut


def H_B1(eps: complex, eta: float = ETA) -> np.ndarray:
    return np.array([[-1j * eta, eps], [-eps, 0.0]], dtype=complex)


def H_B2(eps: complex, eta: float = ETA) -> np.ndarray:
    return np.array([[eps, eta], [-eta, -eps]], dtype=complex)


def _score_2x2(H_of, eps_c: float, eta: float, name: str, side: float) -> dict:
    H_c = H_of(eps_c, eta)
    lam = 0.5 * np.sum(np.linalg.eigvals(H_c))
    w = np.linalg.eigvals(H_c)
    gap = float(np.abs(w[0] - w[1]))
    rank = np.linalg.matrix_rank(H_c - lam * np.eye(2), tol=1e-7)
    geom = 2 - rank if rank < 2 else (2 if gap > 1e-6 else 2)
    # if gap tiny and rank 1 → geom 1
    jordan = bool(gap < 1e-6 and rank == 1)
    ep2 = jordan
    puis = {"exponent": float("nan"), "passed": False, "rel_residual": float("nan"), "c": float("nan"),
            "delta": np.array([]), "split": np.array([])}
    mono = {"ep2_monodromy": False, "swapped_at_2pi": False, "return_4pi": float("nan"),
            "needs_4pi": False, "theta": np.array([0.0]), "evals": np.zeros((1, 2), dtype=complex),
            "z_path": np.array([0.0]), "z_ep": 0.0, "radius": 0.0, "evecs": np.zeros((1, 2, 2))}
    if ep2:
        puis = puiseux_real(lambda e: H_of(e, eta), eps_c, side=side)
        mono = monodromy_loop(lambda z: H_of(z, eta), z_ep=complex(eps_c), radius=0.3 * max(abs(eps_c), eta))
    on = on_cut(lam, eps_c, eta) if ep2 else False
    chk = Checklist(
        ep2_found=ep2,
        jordan=jordan,
        puiseux_half=bool(puis["passed"]),
        mono_4pi=bool(mono["ep2_monodromy"]),
        on_cut=bool(on),
        exponent=float(puis["exponent"]) if puis["exponent"] == puis["exponent"] else float("nan"),
        defect=float(jordan_defect(H_c, lam)),
        petermann=float(petermann(H_c, 0)),
        lam_ep=complex(lam),
        eps_ep=float(eps_c),
        Gamma=Gamma(eps_c),
        notes=name,
    )
    return {"checklist": chk, "puiseux": puis, "mono": mono, "H_ep": H_c, "gap": gap, "rank": rank}


def disc_B1(eps: float, eta: float = ETA) -> complex:
    """(a-d)^2 + 4 b12  for H=[[ -iη, ε],[-ε, 0]]. Zero iff EP."""
    a, d, b12 = -1j * eta, 0.0, -eps * eps
    return (a - d) ** 2 + 4.0 * b12


def score_B1(eta: float = ETA) -> dict:
    """
    Real-ε hunt: min |disc| on a grid. Also the analytic condition
    Im disc = 0 and Re disc = 0, which requires η=0 or ε complex.
    """
    grid = np.linspace(-2.0, 2.0, 2001)
    vals = np.array([disc_B1(e, eta) for e in grid])
    i = int(np.argmin(np.abs(vals)))
    eps_star = float(grid[i])
    minabs = float(np.abs(vals[i]))
    # no real root expected for η>0
    found_real = bool(minabs < 1e-6)
    if found_real:
        out = _score_2x2(H_B1, eps_star, eta, "B1 dissipation vs CS@0", side=0.2)
    else:
        # still pack a checklist of failure
        H = H_B1(eps_star, eta)
        w = np.linalg.eigvals(H)
        chk = Checklist(
            ep2_found=False,
            jordan=False,
            puiseux_half=False,
            mono_4pi=False,
            on_cut=False,
            exponent=float("nan"),
            defect=float(jordan_defect(H)),
            petermann=float(petermann(H, 0)),
            lam_ep=complex(0.5 * (w[0] + w[1])),
            eps_ep=float("nan"),
            Gamma=Gamma(eps_star),
            notes=(
                f"B1: no real-ε EP2 (min|disc|={minabs:.3g} at ε={eps_star:.4g}). "
                "Ohmic (−iη) and CS@0 miss each other on real shear; "
                "EP would need η=0 (gravity-only) or complex coupling."
            ),
        )
        out = {
            "checklist": chk,
            "puiseux": {"exponent": float("nan"), "passed": False, "rel_residual": float("nan"),
                        "c": float("nan"), "delta": np.array([]), "split": np.array([])},
            "mono": {"ep2_monodromy": False, "swapped_at_2pi": False, "return_4pi": float("nan"),
                     "needs_4pi": False, "theta": np.array([0.0]),
                     "evals": np.zeros((1, 2), dtype=complex),
                     "z_path": np.array([0.0j]), "z_ep": 0.0, "radius": 0.0,
                     "evecs": np.zeros((1, 2, 2))},
            "H_ep": H,
            "gap": float(np.abs(w[0] - w[1])),
            "rank": int(np.linalg.matrix_rank(H - np.mean(w) * np.eye(2), tol=1e-8)),
        }
    out["min_disc"] = minabs
    out["eps_star"] = eps_star
    out["matrix_form"] = "H_B1(ε) = [[ -i η, ε ], [ -ε, 0 ]]"
    out["disc_grid"] = (grid, vals)
    return out


def score_B2(eta: float = ETA) -> dict:
    eps_c = float(eta)  # |ε| = η
    out = _score_2x2(H_B2, eps_c, eta, "B2 GSG grading (shear vs cut-width)", side=0.35 * eps_c)
    out["matrix_form"] = "H_B2(ε) = [[ ε, η ], [ -η, -ε ]]"
    return out


def sweep_B(H_of, eps_grid: np.ndarray, eta: float = ETA) -> dict:
    evals = np.zeros((eps_grid.size, 2), dtype=complex)
    gaps = np.zeros(eps_grid.size)
    for i, e in enumerate(eps_grid):
        w = np.linalg.eigvals(H_of(complex(e), eta))
        w = w[np.argsort(w.real + 1e-9 * w.imag)]
        evals[i] = w
        gaps[i] = float(np.abs(w[0] - w[1]))
    return {"eps": eps_grid, "evals": evals, "gap": gaps}

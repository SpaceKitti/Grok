r"""Vortices: model import from the Pair A handoff + circulation + physics checks.

All model objects come from C:\Users\Akitt\pairA-qg-handoff (read-only import,
no bytecode written there). Nothing here redefines the model.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HANDOFF = Path(r"C:\Users\Akitt\pairA-qg-handoff")
sys.dont_write_bytecode = True  # do not write __pycache__ into the handoff folder
if str(HANDOFF) not in sys.path:
    sys.path.insert(0, str(HANDOFF))

import seed as _seed  # noqa: E402  (handoff seed.py)
import tracker as _tracker  # noqa: E402  (handoff tracker.py)
import wick_lorentzian as _wick  # noqa: E402  (handoff wick_lorentzian.py)

H_A = _seed.H_A                 # seed.py: H_A(eps) = [[-i a, eps v],[eps v, -i b]]
EPS_EP = float(_seed.EPS_EP)    # seed.py: eps_EP = |a-b|/(2|v|)  (b>a in this handoff)
LAM_EP = complex(_seed.LAM_EP)  # seed.py: -i(a+b)/2
A, B, V = _seed.A, _seed.B, _seed.V
y_of_eps = _seed.y_of_eps       # seed.py: y^2 = 4 v^2 (eps^2 - eps_EP^2)
align_evals = _tracker.align_evals  # tracker.py: nearest-distance pair matching
GAMMA = (-EPS_EP, EPS_EP)       # wick_lorentzian.chart(): real_section_support = [-eps_EP, eps_EP]
GAMMA_STR = _wick.chart()["real_section_support"]


def in_gamma(x: float, tol: float = 1e-12) -> bool:
    return GAMMA[0] - tol <= x <= GAMMA[1] + tol


def eig(eps: complex):
    return np.linalg.eig(H_A(complex(eps)))


def lam_ep_at(core: float) -> complex:
    """lambda_EP evaluated AT the given core: the double eigenvalue = tr H_A(core)/2."""
    return complex(np.trace(H_A(complex(core))) / 2.0)


def circulation(evals: np.ndarray, lam_ep: complex) -> np.ndarray:
    """Unwrapped arg(lambda - lambda_EP) change along a tracked path, per sheet."""
    ph = np.unwrap(np.angle(evals - lam_ep), axis=0)
    return ph - ph[0]


def gap_and_overlap(core: float, r: float, n: int = 721) -> dict:
    th = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    gaps, ovs = [], []
    for t in th:
        w, Vm = eig(core + r * np.exp(1j * t))
        gaps.append(abs(w[0] - w[1]))
        v0, v1 = Vm[:, 0], Vm[:, 1]
        ovs.append(abs(np.vdot(v0, v1)) / (np.linalg.norm(v0) * np.linalg.norm(v1)))
    return {"gap_mean": float(np.mean(gaps)), "overlap_mean": float(np.mean(ovs)),
            "overlap_min": float(np.min(ovs))}


def physics_checks(fracs=(0.25, 0.1, 0.03, 0.01)) -> dict:
    out = {"fracs": list(fracs), "cores": {}}
    for core in (+EPS_EP, -EPS_EP):
        rows = [gap_and_overlap(core, f * EPS_EP) for f in fracs]
        rs = np.array(fracs) * EPS_EP
        g = np.array([x["gap_mean"] for x in rows])
        slope = float(np.polyfit(np.log(rs), np.log(g), 1)[0])
        at = eig(core)
        v0, v1 = at[1][:, 0], at[1][:, 1]
        ov_core = abs(np.vdot(v0, v1)) / (np.linalg.norm(v0) * np.linalg.norm(v1))
        out["cores"][core] = {"rows": rows, "exponent": slope, "overlap_at_core": float(ov_core),
                              "gap_at_core": float(abs(at[0][0] - at[0][1]))}
    # Hermiticity on the real chart
    herm = []
    for e in np.linspace(-EPS_EP, EPS_EP, 11):
        H = H_A(complex(e))
        herm.append(float(np.linalg.norm(H - H.conj().T)))
    H0 = H_A(0.3 + 0j)
    D = H0 - H0.conj().T
    out["herm_norms"] = herm
    out["herm_diff_example"] = D
    out["offdiag_herm"] = float(abs(D[0, 1]) + abs(D[1, 0]))
    out["diag_antiherm"] = (complex(D[0, 0]), complex(D[1, 1]))
    return out

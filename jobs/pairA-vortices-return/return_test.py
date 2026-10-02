"""Return tests T1-T4, with explicit branch cuts for sheet labels A/B."""
from __future__ import annotations

import numpy as np

from vortices import EPS_EP, LAM_EP, V, in_gamma

LIP = 1e-13  # points exactly on a cut are read on the upper lip (eps + i0)


def y_cut_gamma(eps: complex) -> complex:
    """Cut = segment [-eps_EP, +eps_EP] (the handoff's cut Gamma).
    y = 2v sqrt(eps-eps_EP) sqrt(eps+eps_EP), principal sqrts; y^2 = 4v^2(eps^2-eps_EP^2)."""
    e = complex(eps)
    if abs(e.imag) < LIP and abs(e.real) <= EPS_EP:
        e = complex(e.real, LIP)
    return 2.0 * V * np.sqrt(e - EPS_EP) * np.sqrt(e + EPS_EP)


def y_cut_rays(eps: complex) -> complex:
    """Cut = two rays outward: (-inf,-eps_EP] and [+eps_EP,+inf).
    y = 2v i sqrt(eps_EP-eps) sqrt(eps_EP+eps); y^2 = 4v^2(eps^2-eps_EP^2)."""
    e = complex(eps)
    if abs(e.imag) < LIP and abs(e.real) >= EPS_EP:
        e = complex(e.real, LIP)
    return 2.0j * V * np.sqrt(EPS_EP - e) * np.sqrt(EPS_EP + e)


CUTS = {
    "Gamma-segment [-eps_EP,+eps_EP]": y_cut_gamma,
    "outward rays (-inf,-eps_EP] U [+eps_EP,+inf)": y_cut_rays,
}


def sheet_label(lam: complex, eps: complex, yfun) -> str:
    """Sheet A := lambda_EP + y/2, sheet B := lambda_EP - y/2 (for the given cut)."""
    y = yfun(eps)
    dA = abs(lam - (LAM_EP + 0.5 * y))
    dB = abs(lam - (LAM_EP - 0.5 * y))
    return "A" if dA <= dB else "B"


def label_history(tr: dict, yfun, sheet: int = 0) -> dict:
    z, ev = tr["z"], tr["evals"]
    labs = [sheet_label(ev[i, sheet], z[i], yfun) for i in range(z.size)]
    flips = sum(1 for i in range(1, len(labs)) if labs[i] != labs[i - 1])
    return {"start": labs[0], "end": labs[-1], "flips": flips, "swap": labs[0] != labs[-1]}


def returns_to_real_chart(z_end: complex, tol: float = 1e-9) -> dict:
    on_axis = abs(z_end.imag) < tol
    return {"on_real_axis": bool(on_axis), "in_Gamma": bool(on_axis and in_gamma(z_end.real)),
            "eps_end": complex(z_end)}


def loop_report(name: str, tr: dict) -> dict:
    ev = tr["evals"]
    tracked_swap = bool(abs(ev[-1, 0] - ev[0, 1]) < abs(ev[-1, 0] - ev[0, 0]))
    cuts = {k: label_history(tr, f) for k, f in CUTS.items()}
    lam_back = bool(np.max(np.abs(ev[-1] - ev[0])) < 1e-8)
    return {"name": name, "tracked_swap": tracked_swap, "cuts": cuts,
            "cut_independent": all(c["swap"] == tracked_swap for c in cuts.values()),
            "lam_back": lam_back, "chart": returns_to_real_chart(tr["z"][-1]),
            "jump_ratio": tr["jump_ratio"], "start": complex(tr["z"][0])}

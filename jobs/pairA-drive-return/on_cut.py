r"""On-cut path: start on Gamma, go along Gamma, figure-eight around both tips, continuous tracking."""
from __future__ import annotations

import numpy as np

from drive import EPS_EP, EPS_START, in_gamma, sheet_basis  # noqa: F401
from tracks import figure_eight, track  # pairA-vortices-return


def path_from(e0: float, n_line: int = 2000) -> np.ndarray:
    s8, z8 = figure_eight()
    if abs(e0) < 1e-15:
        return z8
    to0 = np.linspace(e0, 0.0, n_line + 1).astype(complex)
    back = np.linspace(0.0, e0, n_line + 1).astype(complex)
    return np.concatenate([to0, z8[1:], back[1:]])


def run_on_cut() -> list:
    out = []
    for e0, name in ((0.0, "eps=0"), (float(EPS_START), "eps=0.75 eps_EP")):
        z = path_from(e0)
        lam0, _, _ = sheet_basis(z[0])
        tr = track(z, first=lam0)
        ev = tr["evals"]
        diff = float(np.max(np.abs(ev[-1] - ev[0])))
        on_line = z[np.abs(z.imag) < 1e-14].real
        out.append({"name": name, "e0": e0, "eps_end": complex(z[-1]), "lam_start": ev[0], "lam_end": ev[-1],
                    "max_diff": diff, "yes": diff < 1e-8 and in_gamma(z[-1].real) and abs(z[-1].imag) < 1e-12,
                    "jump_ratio": tr["jump_ratio"], "n": z.size,
                    "real_segment_in_gamma": bool(np.all([in_gamma(x) for x in on_line]))})
    return out

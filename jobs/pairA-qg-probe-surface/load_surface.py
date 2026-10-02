r"""Load the Pair A surface read-only: handoff (seed, wick_lorentzian, Jhat), drive-return and
vortices-return results. Also: file hashing for the before/after unchanged check.
Nothing here writes into the loaded folders (bytecode writing is disabled before any import).
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

HANDOFF = Path(r"C:\Users\Akitt\pairA-qg-handoff")
DRIVE = Path(r"C:\Users\Akitt\pairA-drive-return")
VORT = Path(r"C:\Users\Akitt\pairA-vortices-return")
LOADED = [HANDOFF, DRIVE, VORT]
EPS_EP_REF = 0.51368066  # Akitti's HAVE value, used only for an agreement check (not as input)


def hash_tree(roots=LOADED) -> dict:
    out = {}
    for root in roots:
        for p in sorted(root.rglob("*")):
            if p.is_file():
                out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def grep(roots, pattern, exts=(".py", ".md", ".txt", ".json")):
    rx = re.compile(pattern, re.IGNORECASE)
    hits = []
    for root in roots:
        for p in sorted(root.rglob("*")):
            if p.is_file() and p.suffix in exts and "__pycache__" not in p.parts:
                for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                    if rx.search(line):
                        hits.append((str(p), i, line.strip()))
    return hits


def load() -> dict:
    """Import the handoff model (read-only) and assert eps_EP = |a-b|/(2|v|)."""
    if str(HANDOFF) not in sys.path:
        sys.path.insert(1, str(HANDOFF))
    import numpy as np
    import seed  # handoff seed.py
    import tracker  # handoff tracker.py
    import wick_lorentzian  # handoff wick_lorentzian.py

    eps = float(seed.EPS_EP)
    formula = abs(seed.A - seed.B) / (2.0 * abs(seed.V))
    assert abs(eps - formula) < 1e-15, (eps, formula)
    assert abs(eps - EPS_EP_REF) < 1e-8, (eps, EPS_EP_REF)
    jz = np.load(HANDOFF / "outputs" / "Jhat.npz")
    chart = wick_lorentzian.chart()
    return {
        "H_A": seed.H_A, "A": seed.A, "B": seed.B, "V": seed.V, "EPS_EP": eps, "LAM_EP": complex(seed.LAM_EP),
        "formula": formula, "align_evals": tracker.align_evals, "chart": chart,
        "GAMMA": (-eps, eps), "Jhat2": jz["Jhat2"], "Jhat4": jz["Jhat4"],
    }


def y_cut_gamma(eps_c: complex, EPS_EP: float, V: float) -> complex:
    """Sheet convention of pairA-vortices-return/return_test.py (Gamma-segment cut, upper lip on the cut):
    sheet A = lam_EP + y/2, sheet B = lam_EP - y/2, y = 2v sqrt(eps-eps_EP) sqrt(eps+eps_EP)."""
    import numpy as np
    e = complex(eps_c)
    if abs(e.imag) < 1e-13 and abs(e.real) <= EPS_EP:
        e = complex(e.real, 1e-13)
    return 2.0 * V * np.sqrt(e - EPS_EP) * np.sqrt(e + EPS_EP)

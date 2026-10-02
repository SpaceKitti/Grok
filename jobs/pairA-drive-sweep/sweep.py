"""Sweep driver: reuses pairA-drive-return/drive.py (read-only import) with per-start loop radius / centre / phase set in memory."""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

DRIVE = Path(r"C:\Users\Akitt\pairA-drive-return")
LOADED = [DRIVE, Path(r"C:\Users\Akitt\pairA-vortices-return"), Path(r"C:\Users\Akitt\pairA-qg-handoff")]
if str(DRIVE) not in sys.path:
    sys.path.insert(1, str(DRIVE))

import drive as D  # noqa: E402

E = D.EPS_EP
FRACS = [0.25, 0.50, 0.75, 1.00, 1.10, 1.25, 1.50]
SPEEDS = {"slow20": 20.0, "slow40": 40.0, "slow100": 100.0}
DIRS = {"ccw": +1, "cw": -1}


def set_loop(start: float, tip: float):
    """in-memory: loop around `tip` passing through the real start point."""
    r = abs(start - tip)
    far = abs(start) > abs(tip)
    phase = 0.0 if (far == (tip > 0)) else np.pi   # start = tip + r e^{i phase}
    assert abs(tip + r * np.exp(1j * phase) - start) < 1e-12
    D.R_LOOP, D.EPS_START, D.PHASE = r, start, phase

    def eps_of(theta, s):
        return tip + r * np.exp(1j * (s * np.asarray(theta) + phase))
    D.eps_of = eps_of
    return r, phase


def start_info(start: float):
    lam, R, _ = D.sheet_basis(complex(start))
    d = lam[0] - lam[1]
    if abs(d.real) < 1e-9 * abs(d):
        kind = "shared frequency (decays differ)"
    elif abs(d.imag) < 1e-9 * abs(d):
        kind = "shared decay (frequencies differ)"
    else:
        kind = "neither"
    return {"lam": lam, "kind": kind, "F": start ** 2 - E ** 2, "slow": int(np.argmax(lam.imag)), "hi": int(np.argmax(lam.real))}


def phys(idx, info):
    if info["kind"].startswith("shared frequency"):
        return "slower-decaying" if idx == info["slow"] else "faster-decaying"
    return "higher-frequency" if idx == info["hi"] else "lower-frequency"


def run_start(start: float, tip: float, conv: bool = True):
    r, phase = set_loop(start, tip)
    info = start_info(start)
    runs = {}
    for sp, gT in SPEEDS.items():
        for dn, s in DIRS.items():
            for st in (0, 1):
                out = D.run_drive(s, gT, st)
                rec = {}
                for m in (1, 2):
                    w = out["marks"][m]["w"]
                    k = int(np.argmax(w))
                    rec[m] = {"win": "AB"[k], "phys": phys(k, info), "w": float(w[k]), "wv": w}
                if conv and sp == "slow40":
                    o2 = D.run_drive(s, gT, st, factor=2)
                    rec["dw"] = max(float(np.max(np.abs(out["marks"][m]["w"] - o2["marks"][m]["w"]))) for m in (1, 2))
                runs[(sp, dn, "AB"[st])] = rec
    return {"r": r, "phase": phase, "info": info, "runs": runs, "min_gap": min_gap(tip, r)}


def min_gap(tip, r, n=4000):
    th = np.linspace(0, 2 * np.pi, n)
    return float(min(abs(np.diff(np.linalg.eigvals(D.H_A(complex(tip + r * np.exp(1j * t)))))[0]) for t in th))


def classify(res):
    runs = res["runs"]
    bad = any(not np.isfinite(runs[k][m]["w"]) for k in runs for m in (1, 2)) or any(runs[k].get("dw", 0) > 1e-3 for k in runs)
    if bad:
        return "FAIL", "numerics (NaN or dt-halving change > 1e-3)"
    ws = all(runs[k][m]["w"] >= 0.9 for k in runs for m in (1, 2))
    same, opp, indep = True, True, True
    for sp in SPEEDS:
        for m in (1, 2):
            for st in "AB":
                a, b = runs[(sp, "ccw", st)][m]["win"], runs[(sp, "cw", st)][m]["win"]
                same &= a == b
                opp &= a != b
            for dn in DIRS:
                indep &= runs[(sp, dn, "A")][m]["win"] == runs[(sp, dn, "B")][m]["win"]
    if ws and same and indep:
        return "D6-like", "ccw = cw for both start sheets, start-sheet independent, all w ≥ 0.9"
    if ws and opp and indep:
        return "D7-like", "ccw ≠ cw for both start sheets, each direction start-sheet independent, all w ≥ 0.9"
    why = []
    if not ws:
        why.append(f"min w = {min(runs[k][m]['w'] for k in runs for m in (1, 2)):.3f} < 0.9")
    if not (same or opp):
        why.append("ccw/cw agree for some cases, differ for others")
    if not indep:
        why.append("winner depends on the start sheet")
    return "MIXED", "; ".join(why)

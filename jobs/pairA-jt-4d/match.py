"""MATCH M1-M5 (each PASS/FAIL, tested)."""
from __future__ import annotations

import numpy as np

from jt2d import EPS_EP, LAM_EP, SHEETS, V, track_y

N = 8000

PROBE = r"C:\Users\Akitt\pairA-qg-probe-surface"
OPERATOR = r"C:\Users\Akitt\pairA-qg-operator"
LOADED = [PROBE, OPERATOR]


def hash_tree():
    import hashlib
    from pathlib import Path
    out = {}
    for root in LOADED:
        for p in sorted(Path(root).rglob("*")):
            if p.is_file():
                out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def d67_map():
    """What D6/D7 are (probe-surface RESULTS.md rows, read-only) and whether they line up with F_JT < 0 / F_JT > 0."""
    import re
    from pathlib import Path
    E = EPS_EP
    rows = {}
    ptxt = (Path(PROBE) / "RESULTS.md").read_text(encoding="utf-8")
    otxt = (Path(OPERATOR) / "RESULTS.md").read_text(encoding="utf-8")
    for did in ("D6", "D7"):
        line = next(l for l in ptxt.splitlines() if l.startswith(f"| {did} |"))
        cells = [c.strip() for c in line.split(" | ")]
        olines = [l for l in otxt.splitlines() if l.startswith(f"| {did} |")]   # spec copy + match row
        m_start = re.search(r"start/end ([0-9.]+) ε_EP", line)
        m_r = re.search(r"r = ([0-9.]+) ε_EP", line)
        rows[did] = {"claim": cells[1], "result": cells[2].strip("*"), "tag": cells[3],
                     "start": float(m_start.group(1)), "r": float(m_r.group(1)),
                     "operator": any("**INHERITED FROM H_A, not from P1**" in l for l in olines)}
    out = {"rows": rows}
    for did, d in rows.items():
        s = d["start"] * E
        Fs = s * s - E * E
        ys = np.sqrt(complex(4 * V ** 2 * Fs))
        # loop centre: both probe loops circle +eps_EP (probe conditions); range of |eps| on the loop
        th = np.linspace(0, 2 * np.pi, 2001)
        z = E + d["r"] * E * np.exp(1j * th)
        Fl = (z ** 2 - E ** 2).real                       # sign of F_JT on the real-axis crossings is what matters
        xr = z[np.abs(z.imag) < 1e-12 * E].real if np.any(np.abs(z.imag) < 1e-12 * E) else np.array([E - d["r"] * E, E + d["r"] * E])
        d.update({"F_start": Fs, "y_start": ys,
                  "phase": "split-decay (same frequency)" if abs(ys.real) < 1e-12 and abs(ys.imag) > 0 else
                           "split-frequency (same decay)" if abs(ys.imag) < 1e-12 and abs(ys.real) > 0 else "mixed",
                  "loop_x": (float((E - d["r"] * E) / E), float((E + d["r"] * E) / E)),
                  "straddles": (E - d["r"] * E) < E < (E + d["r"] * E)})
    start_ok = rows["D6"]["F_start"] < 0 and rows["D7"]["F_start"] > 0
    same_loop = rows["D6"]["r"] == rows["D7"]["r"]
    straddle = rows["D6"]["straddles"] and rows["D7"]["straddles"]
    inherited = rows["D6"]["operator"] and rows["D7"]["operator"]
    out.update({"start_ok": start_ok, "same_loop": same_loop, "straddle": straddle, "inherited": inherited})
    match_ = start_ok and not straddle
    out["verdict"] = "regions match YES" if match_ else "regions match NO"
    out["reason"] = ("D6 and D7 are the same driven loop (r = 0.25 ε_EP around +ε_EP, spanning 0.75–1.25 ε_EP, so it straddles Γ), labelled only by its start point; "
                     "the start points do sit at F_JT < 0 (0.75 ε_EP) and F_JT > 0 (1.25 ε_EP), but that is how D6/D7 are defined, tested at two points, not a region map along the loop"
                     if not match_ else "start points and whole loops lie in F_JT < 0 (D6) and F_JT > 0 (D7)")
    return out


def chirality():
    """Static eigenvalue continuation (branch tracking of y) both ways around each tip: label map for ccw and cw, 1 and 2 turns.
    (M1/M2 run ccw only; this adds the cw direction.)"""
    E, r = EPS_EP, 0.25 * EPS_EP
    res = {}
    for s, nm in ((+1, "+ε_EP"), (-1, "−ε_EP")):
        for d, dn in ((+1, "ccw"), (-1, "cw")):
            for turns in (1, 2):
                t = np.linspace(0, 2 * np.pi * turns, N * turns + 1)
                z = s * E + r * np.exp(1j * d * t)
                y0, y1, _ = track_y(z)
                res[(nm, dn, turns)] = 0 if abs(y1 - y0) < abs(y1 + y0) else 1
    same = all(res[(nm, "ccw", k)] == res[(nm, "cw", k)] for nm in ("+ε_EP", "−ε_EP") for k in (1, 2))
    swap = all(res[(nm, dn, 1)] == 1 and res[(nm, dn, 2)] == 0 for nm in ("+ε_EP", "−ε_EP") for dn in ("ccw", "cw"))
    return {"n": res, "same": same, "swap": swap, "ok": same and swap}


def h_a_check():
    import sympy as sp
    a, b, v, e = sp.symbols("a b v epsilon", real=True)
    return sp.simplify(4 * v ** 2 * (e ** 2 - ((a - b) / (2 * v)) ** 2) - (4 * v ** 2 * e ** 2 - (a - b) ** 2))


def loops():
    E, r = EPS_EP, 0.25 * EPS_EP
    out = {}
    for s, nm in ((+1, "+ε_EP"), (-1, "−ε_EP")):
        for turns in (1, 2):
            t = np.linspace(0, 2 * np.pi * turns, N * turns + 1)
            z = s * E + r * np.exp(1j * t)
            y0, y1, ymin = track_y(z)
            out[(nm, turns)] = {"n": 0 if abs(y1 - y0) < abs(y1 + y0) else 1, "ymin": ymin}
    return out


def run(J):
    E = EPS_EP
    lp = loops()
    rows = []
    m1 = all(lp[(nm, 1)]["n"] == 1 for nm in ("+ε_EP", "−ε_EP"))
    rows.append(("M1", "2π loop around each tip (complex ε, r = 0.25 ε_EP) swaps the A/B branches of y", m1, "[computed]",
                 f"branch tracking of y = ±√(4v²(ε²−ε_EP²)), 8000 steps: n = {lp[('+ε_EP',1)]['n']} at +ε_EP, {lp[('−ε_EP',1)]['n']} at −ε_EP (1 = swap); min |y| on the loop {min(lp[(k,1)]['ymin'] for k in ('+ε_EP','−ε_EP')):.4f} > 0"))
    m2 = all(lp[(nm, 2)]["n"] == 0 for nm in ("+ε_EP", "−ε_EP"))
    rows.append(("M2", "4π loop returns them", m2, "[computed]",
                 f"n = {lp[('+ε_EP',2)]['n']} at +ε_EP, {lp[('−ε_EP',2)]['n']} at −ε_EP (0 = return)"))
    c = J["cones"]
    cs = {k: v[-1][2] for k, v in c.items()}
    smooth_ok = all(abs(cs[(nm, "2π/ε_EP (smooth)")] / (2 * np.pi) - 1) < 1e-4 for nm in ("+ε_EP", "−ε_EP"))
    dbl_ok = all(abs(cs[(nm, "4π/ε_EP (τ_swap)")] / (2 * np.pi) - 2) < 1e-4 for nm in ("+ε_EP", "−ε_EP"))
    one_tip = J["pos_outside"] and J["neg_inside"]    # Euclidean pieces eps > E and eps < -E, separated by the F<0 strip Gamma
    m3 = m1 and m2 and smooth_ok and dbl_ok and one_tip
    rows.append(("M3", "swap/return cover: smooth horizon period 2π/ε_EP vs 4π cone (τ_swap)", m3,
                 "cone angles [computed]; 4π cone [by construction, from τ_swap]; τ ↔ arg(ε−ε_EP) identification [hive-interpretation]",
                 f"cone angle with period 2π/ε_EP = {cs[('+ε_EP','2π/ε_EP (smooth)')]/np.pi:.6f}π / {cs[('−ε_EP','2π/ε_EP (smooth)')]/np.pi:.6f}π (smooth); "
                 f"with τ_swap = 4π/ε_EP = {cs[('+ε_EP','4π/ε_EP (τ_swap)')]/np.pi:.6f}π / {cs[('−ε_EP','4π/ε_EP (τ_swap)')]/np.pi:.6f}π (branched double cover). "
                 "The swap and return need a double cover. The smooth horizon (period 2π/ε_EP) already is one, in z = √(ε−ε_EP) (near the tip, ρ ≈ √(2(ε−ε_EP)/ε_EP), "
                 "z² ∝ (ε−ε_EP)e^{2iε_EPτ}); the 4π cone is [by construction, from τ_swap]. Identifying the τ angle with arg(ε−ε_EP) (4π-cone reading) or arg(ε−ε_EP)/2 "
                 "(smooth reading) is [hive-interpretation]; either way the cover y needs is degree 2 (M1: swap after one turn, M2: return after two). "
                 "The swap lives on the complex ε curve; each real Euclidean JT piece holds only one tip."))
    yb = np.sqrt(complex(4 * V ** 2 * ((1.25 * E) ** 2 - E ** 2)))
    lamA, lamB = LAM_EP + yb / 2, LAM_EP - yb / 2
    m4 = SHEETS["A"] == "WRITE" and SHEETS["B"] == "WRITE" and SHEETS["C"] == "held" and abs(lamA - lamB) > 0
    rows.append(("M4", "A and B lifted (both WRITE; the two sheets of y); C held", m4, "[by construction]",
                 f"A, B = λ_EP ± y/2 (at ε = 1.25 ε_EP: {lamA.real:+.6f}{lamA.imag:+.6f}i, {lamB.real:+.6f}{lamB.imag:+.6f}i); both enter F_JT = y²/(4v²) and the lift. "
                 "C is not in the construction (held, untouched)."))
    m5 = J["res_y2"] < 1e-13
    rows.append(("M5", "F_JT = +y²/(4v²) at machine precision", m5, "[by construction, numerically confirmed]",
                 f"max |F_JT − (λ₊−λ₋)²/(4v²)| = {J['res_y2']:.1e} on 61×21 complex ε in Re ∈ [−3, 3] ε_EP, Im ∈ [−1, 1] ε_EP, with λ± the numerical eigenvalues of the 2×2 stand-in v[[0,1],[ε²−ε_EP²,0]] (λ_EP I dropped: it cancels in the difference). H_A gives the same: (λ₊−λ₋)² = −(a−b)² + 4v²ε² = 4v²(ε²−ε_EP²), with ε_EP = |a−b|/(2|v|), so the stand-in is fair [standard]"
                 f" (sympy: 4v²(ε² − ((a−b)/(2v))²) − (4v²ε² − (a−b)²) = {h_a_check()})."))
    return rows, lp


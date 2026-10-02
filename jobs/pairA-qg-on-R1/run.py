"""pairA-qg-on-R1: mini path integral on the Euclidean R1 section. `python run.py` writes RESULTS.md."""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
except Exception:
    pass

import load_inputs as LI  # noqa: E402

H_BEFORE = LI.hash_tree()

import numpy as np  # noqa: E402

import pathint as P  # noqa: E402


def fmt(z):
    return f"{z.real:+.6f}", f"{z.imag:+.6f}"


def main() -> int:
    r1 = LI.load_r1()
    sf = LI.load_surface()
    E, LAM, V = r1["EPS_EP"], r1["LAM_EP"], r1["V"]
    C = P.Curve(E, LAM, V, sf["y_cut_gamma"])
    # M5-style consistency: y_cut^2 = 4 v^2 F_JT (curve of jt-4d = sheets of probe-surface)
    zs = [complex(x, y) for x in np.linspace(-3 * E, 3 * E, 25) for y in (-0.7 * E, -0.2 * E, 0.3 * E, 0.9 * E)]
    res_curve = max(abs(C.y_cut(z) ** 2 - complex(r1["y2"](z))) for z in zs)

    base_p, base_m = 1.25 * E, -1.25 * E
    PATHS = [("S1", "+ε_EP once (2π)", E, base_p, 1),
             ("S2", "+ε_EP twice (4π)", E, base_p, 2),
             ("S3", "−ε_EP once (2π)", -E, base_m, 1),
             ("S4", "−ε_EP twice (4π)", -E, base_m, 2)]
    rows = []
    for name, desc, tip, base, turns in PATHS:
        for dn, s in (("ccw", +1), ("cw", -1)):
            z, th = P.circle(tip, base, turns, s)
            on, off = P.crossings(z, E)
            for sh in (0, 1):
                a = P.action(C, z, th, sh)
                # deformations with the same base point (stationarity check: delta S under shape changes)
                dS = 0.0
                for zz, tt in (P.ellipse(tip, base, turns, 0.4, s), P.ellipse(tip, base, turns, 2.0, s),
                               P.offcircle(tip, base, turns, -0.1 * (base - tip), s), P.offcircle(tip, base, turns, 0.15 * (base - tip), s)):
                    b = P.action(C, zz, tt, sh)
                    assert b["swap"] == a["swap"]
                    dS = max(dS, abs(b["S"] - a["S"]))
                if turns == 1:
                    ana = P.s1_analytic(C, base, sh)
                else:
                    ana = 0.0   # closed cycle on the double cover, contractible (y holomorphic in sqrt(eps - tip))
                rows.append({"name": name, "desc": desc, "dir": dn, "sheet": "AB"[sh], "turns": turns, "tip": tip, "base": base,
                             "S": a["S"], "ana": ana, "err": abs(a["S"] - ana), "dS": dS, "swap": a["swap"],
                             "end": "AB"[a["end_sheet"]], "gap": a["min_gap"], "jump": a["jump"],
                             "on": on, "off": off, "F_cross": [x * x - E * E for x in on]})
    for r in rows:
        print(f"{r['name']} {r['dir']} from {r['sheet']}: S = {r['S'].real:+.6f} {r['S'].imag:+.6f}i (analytic {r['ana']:+.6f}, |diff| {r['err']:.1e}; "
              f"max |ΔS| over 4 shape deformations {r['dS']:.1e}); Γ crossings {len(r['on'])} at {[round(x / E, 4) for x in r['on']]} ε_EP; "
              f"swap {'YES' if r['swap'] else 'NO'} (ends on {r['end']}); min|y| {r['gap']:.4f}")

    # extra (not requested): loop around BOTH tips, circle r = 2 eps_EP from +2 eps_EP
    extra = []
    for dn, s in (("ccw", +1), ("cw", -1)):
        z, th = P.circle(0.0, 2 * E, 1, s)
        on, off = P.crossings(z, E)
        for sh in (0, 1):
            a = P.action(C, z, th, sh)
            ana = s * (-np.pi * 1j * V * E ** 2) * (1 if sh == 0 else -1) * np.sign(C.y_cut(2 * E).real / V)
            extra.append({"dir": dn, "sheet": "AB"[sh], "S": a["S"], "ana": ana, "swap": a["swap"], "on": on})

    # toy partition sum over the chosen paths (ħ = 1, Euclidean weight e^{-S}) [by construction]
    Z = sum(np.exp(-r["S"]) for r in rows if r["dir"] == "ccw")
    Zswap = sum(np.exp(-r["S"]) for r in rows if r["dir"] == "ccw" and r["swap"])
    Zret = sum(np.exp(-r["S"]) for r in rows if r["dir"] == "ccw" and not r["swap"])

    # D3: 2π swap, 4π return (both tips, both directions, both start sheets)
    d3 = all(r["swap"] == (r["turns"] == 1) for r in rows)
    # D4: A and B continue past each EP (two-detour test from the outside base point into Γ: above vs below)
    d4rows = []
    for tip, base in ((E, base_p), (-E, base_m)):
        a = base - tip
        th = np.linspace(0, np.pi, 10001)
        res = {}
        for side, s in (("above", +1 if tip > 0 else -1), ("below", -1 if tip > 0 else +1)):
            z = tip + a * np.exp(1j * s * th)      # semicircle from base (outside Γ) to the mirror point inside Γ
            res[side] = [P.action(C, z, th, sh) for sh in (0, 1)]
        endpt = tip - a
        pair = {side: [int(np.argmin(np.abs(C.sheets(endpt) - res[side][sh]["lam_end"]))) for sh in (0, 1)] for side in res}
        swapped = pair["above"][0] != pair["below"][0] and pair["above"][1] != pair["below"][1]
        gap = min(res[sd][sh]["min_gap"] for sd in res for sh in (0, 1))
        d4rows.append({"tip": tip, "base": base, "end": endpt, "pair": pair, "swapped": swapped, "gap": gap,
                       "S": {sd: [res[sd][sh]["S"] for sh in (0, 1)] for sd in res}})
    c_held = r1["SHEETS"].get("C") == "held" and r1["SHEETS"].get("A") == "WRITE" and r1["SHEETS"].get("B") == "WRITE"
    d4 = all(d["swapped"] and d["gap"] > 0 for d in d4rows) and c_held and sf["rows"].get("D4", {}).get("result") == "PASS"
    d3_surface = sf["rows"].get("D3", {}).get("result") == "PASS"

    H_AFTER = LI.hash_tree()
    same = H_BEFORE == H_AFTER
    print(f"D3 (2π swap, 4π return): {'PASS' if d3 and d3_surface else 'FAIL'}")
    print(f"D4 (A and B continue past the EPs, C held): {'PASS' if d4 else 'FAIL'}")
    print("D6/D7: inherited from H_A, not from Z")
    print(f"curve check max |y_cut² − 4v²F_JT| = {res_curve:.1e}; Z(ccw, 4 paths × 2 sheets) = {Z:.6f}")
    print(f"loaded folders unchanged (SHA-256 of {len(H_BEFORE)} files): {same}")

    # ---------------- RESULTS.md
    L = ["# pairA-qg-on-R1 — RESULTS", "", "**Signed off 2026-09-25:** Venus (maths) and Helios (physics).", "", "R1 QG toy written", "",
         "this is a path-integral probe on R1, not a full QG theory", "",
         "Reading: **path-integral probe over R1's complexified radial coordinate, base point on the Euclidean section [hive-interpretation]**. The loops are contours in ε continued into the complex plane, never along R1's Euclidean time circle τ, so they are not paths in R1 spacetime.", "",
         "Z is a sum over homotopy classes weighted by periods of λ dε on the spectral curve; the flat saddle families reflect a topological (not dynamical) action [hive-interpretation].", "",
         "No QG Hamiltonian was derived, no JT dual is claimed, no Einstein solution is claimed (R1 = AdS₂×S² is taken as given from pairA-jt-4d as the 4D target; ordinary S², no GoldbergHexa). A and B WRITE, C held.", "",
         "## Set-up", "",
         f"- R1 (from pairA-jt-4d, read-only): AdS₂×S², F_JT = ε² − ε_EP², S² radius r = ε_EP = {E:.8f}, horizons at ±ε_EP. Euclidean section = real ε with F_JT > 0 (|ε| > ε_EP, outside Γ). Quoted: \"{r1['target_line']}\"",
         f"- Sheets: λ_A,B = λ_EP ± y/2, λ_EP = {LAM.imag:+.6f}i, v = {V:+.6f}, y² = 4v²F_JT; y from probe-surface `load_surface.y_cut_gamma` (Γ-segment cut). Consistency with jt-4d's curve: max |y² − 4v²F_JT| = {res_curve:.1e} over 100 complex points [computed].",
         "- Action: **S[path] = ∮ λ(ε) dε** along the path on the tracked Pair A eigenvalue branch (start on sheet A or B at the base point) — **[by construction / hive-interpretation: action choice]**. Akitti gave no action; this standard toy loop action was kept because it is the one built from the files' own data (the sheet eigenvalue λ and the ε-plane), and no other action is written in the loaded folders. Toy weight e^{−S}, ħ = 1 [by construction].",
         "- The λ_EP part integrates to zero on any closed ε path, so S = ±½∮y dε [computed, identity].",
         f"- Base points (outside Γ, on the real axis, F_JT > 0): +1.25 ε_EP for loops around +ε_EP, −1.25 ε_EP for loops around −ε_EP; circles of radius 0.25 ε_EP centred on the tip (same circles as the probe-surface cover loops). ccw = counter-clockwise in the ε plane.",
         "", "## Saddle table", "",
         "'Saddle' is used only with this tag: **[by construction: chosen closed paths]**. They are not solved from δS = 0 as an equation. Stationarity was checked instead: λ(ε) is holomorphic away from the tips, so δS = 0 for every deformation that keeps the base point and does not cross a tip [standard: Cauchy]. Numerically, max |ΔS| over 4 shape deformations (two ellipses, two off-centre circles, same base point) is listed. So each path is stationary, but degenerately so: the whole homotopy class is one flat critical family, not an isolated saddle. S depends only on the base point, the start sheet and the winding [computed].", "",
         "| saddle | loop | direction | start sheet | Re S | Im S | analytic S | max |ΔS| (deformations) | Γ crossings (count, at x/ε_EP; F_JT there) | swap (continuation) | ends on | min |λ_A−λ_B| on path |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        re_, im_ = fmt(r["S"])
        cr = f"{len(r['on'])}: " + ", ".join(f"{x / E:+.4f} (F_JT = {x * x - E * E:+.4f})" for x in r["on"])
        L.append(f"| {r['name']} | {r['desc']} | {r['dir']} | {r['sheet']} | {re_} | {im_} | {r['ana']:+.6f} | {r['dS']:.1e} | {cr} | **{'YES' if r['swap'] else 'NO'}** | {r['end']} | {r['gap']:.4f} |")
    L += ["", f"Numerical vs analytic action: max |S_num − S_analytic| = {max(r['err'] for r in rows):.1e}. Analytic values: once around (S1, S3) the loop collapses onto the real segment between tip and base, so S = −∫_tip^base y_X dx, which is real and the same for ccw and cw. Twice around (S2, S4) is a closed cycle on the double cover, contractible there (y is holomorphic in √(ε − tip)), so S = 0 [computed + standard].", "",
          f"Toy partition sum over the chosen paths (ccw, 4 paths × 2 start sheets, ħ = 1): Z = {Z.real:.6f} {Z.imag:+.6f}i; swap sector (S1, S3) {Zswap.real:.6f}, return sector (S2, S4) {Zret.real:.6f} [by construction: the sum is over the chosen paths only; no measure, no fluctuation determinant].", "",
          "### Γ intersection and the Euclidean section [careful-before-toy]", "",
          "- Every loop around a tip crosses Γ once per turn (at 0.75 ε_EP for +ε_EP, −0.75 ε_EP for −ε_EP), where F_JT = −0.4375 ε_EP² < 0. So each loop enters the F_JT < 0 region, which is the R2 / Lorentzian side, not the Euclidean R1 section. A loop cannot circle a tip while staying in F_JT > 0.",
          "- Apart from those real-axis points, the paths run through complex ε, where F_JT is complex. So the paths are complexified contours: the only real points on each path are the base point (F_JT > 0, on the Euclidean R1 section) and the Γ crossing(s) (F_JT < 0, off it). Calling Z a path integral 'on R1' means: base point on the Euclidean section, contour in R1's radial coordinate ε continued into the complex plane [careful-before-toy].",
          "- No loop runs along the Euclidean time circle τ of R1 (period 2π/ε_EP smooth, 4π/ε_EP = τ_swap); τ does not appear in S. The loops are therefore not paths in R1 spacetime. Relating the ε-winding to the τ angle is the jt-4d [hive-interpretation] and is not used here.",
          "- The gap never closes on any path (min |λ_A − λ_B| > 0), so the continuation is well defined; no path passes through an EP.",
          "", "### Extra (not requested): loop around both tips", "",
          "| loop | direction | start sheet | Re S | Im S | analytic | swap | Γ crossings |", "|---|---|---|---|---|---|---|---|"]
    for x in extra:
        re_, im_ = fmt(x["S"])
        L.append(f"| circle r = 2 ε_EP from +2 ε_EP | {x['dir']} | {x['sheet']} | {re_} | {im_} | {x['ana'].imag:+.6f}i | {'YES' if x['swap'] else 'NO'} | {len(x['on'])} |")
    L += ["", f"This is the only closed path here with non-zero action: ½∮y dε = ∓iπ v ε_EP² (|value| = π|v|ε_EP² = {np.pi * abs(V) * E ** 2:.6f}), purely imaginary, from the ε → ∞ tail of y [computed]. It crosses Γ zero times and returns (no swap), consistent with the probe-surface cover row 'big loop around both'.", "",
          "## Matches", "",
          f"- **D3 (2π swap, 4π return): {'PASS' if d3 and d3_surface else 'FAIL'}** — computed by continuation on all 16 path/direction/sheet cases above (S1, S3 swap; S2, S4 return); probe-surface D3 row: {sf['rows'].get('D3', {}).get('result')}. [computed, known]",
          f"- **D4 (A and B continue past the EPs, C held): {'PASS' if d4 else 'FAIL'}** — two-detour test from the outside base point into Γ (semicircle r = 0.25 ε_EP above vs below each tip):"]
    for d in d4rows:
        L.append(f"  - tip {d['tip'] / E:+.0f} ε_EP: {d['base'] / E:+.2f} → {d['end'] / E:+.2f} ε_EP; A lands on {'AB'[d['pair']['above'][0]]} (above) / {'AB'[d['pair']['below'][0]]} (below); B lands on {'AB'[d['pair']['above'][1]]} / {'AB'[d['pair']['below'][1]]}; pairings swapped: {'YES' if d['swapped'] else 'NO'}; min gap {d['gap']:.4f} > 0; half-path actions (A) above {d['S']['above'][0].real:+.6f}{d['S']['above'][0].imag:+.6f}i, below {d['S']['below'][0].real:+.6f}{d['S']['below'][0].imag:+.6f}i.")
    L += [f"  - only A and B enter Z (the curve y² = 4v²F_JT has two sheets); jt-4d SHEETS = {r1['SHEETS']} (C held: {'YES' if c_held else 'NO'}); probe-surface D4 row: {sf['rows'].get('D4', {}).get('result')}. [computed, equivalent to the 2π swap]",
          "- **D6/D7: inherited from H_A, not from Z.** Z is a sum over sheet paths with a holomorphic action; it has no loss or drive direction, so it cannot produce the D6/D7 behaviour. Those come from the lossy driven H_A evolution (pairA-drive-return).",
          "- Note (not run): the link to the sweep's approach to w → 1 (pairA-drive-sweep) is through the DDP-type time integral Im∫(λ_A − λ_B) dt = ∫ y dε / (iω(ε − tip)) along the driven loop (ε = tip + r e^{iωt}), which scales with 1/ω, i.e. with γT. It is not S1 itself: S1 = ½∮y dε has no 1/ω and no time [standard: Dykhne–Davis–Pechukas; Venus correction].", "",
          "## Tags", "",
          "[standard]: Cauchy/contour deformation, AdS₂×S² form of R1. [by construction]: the action choice, base points, chosen paths ('saddles'), ħ = 1, the finite sum Z. [computed]: actions, analytic cross-checks, deformation invariance, crossings, swap by continuation, D3/D4. [hive-interpretation]: reading Z as a path-integral probe over R1's complexified radial coordinate; the action choice; Z as a sum over homotopy classes weighted by periods. [careful-before-toy]: the loops leave the Euclidean section (they cross Γ into F_JT < 0 and run through complex ε).", "",
          "## Loaded folders (read-only)", "",
          f"- `{LI.JT4D}`: jt2d.py imported (EPS_EP, LAM_EP, V, y2, SHEETS); RESULTS.md R1 lines quoted.",
          f"- `{LI.SURF}`: load_surface.y_cut_gamma imported (sheet convention); RESULTS.md D1–D7 rows read ({', '.join(f'{k} {v['result']}' for k, v in sorted(sf['rows'].items()))}); first line: \"{sf['signed']}\".",
          f"- SHA-256 of every file ({len(H_BEFORE)} files) before any import and after all computations: **{'unchanged' if same else 'CHANGED'}**.", ""]
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("Wrote RESULTS.md")
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())

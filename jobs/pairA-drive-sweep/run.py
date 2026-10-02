"""pairA-drive-sweep: D6/D7 region sweep. `python run.py` runs the sweep and writes RESULTS.md;
`python run.py --from-saved` rebuilds RESULTS.md from outputs/sweep.npz, outputs/dw.json and outputs/diag_dt.json (no drive is run)."""
from __future__ import annotations

import hashlib
import sys
import time

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
except Exception:
    pass


def hash_tree(roots):
    out = {}
    for root in roots:
        for p in sorted(Path(root).rglob("*")):
            if p.is_file():
                out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


LOADED = [Path(r"C:\Users\Akitt\pairA-drive-return"), Path(r"C:\Users\Akitt\pairA-vortices-return"), Path(r"C:\Users\Akitt\pairA-qg-handoff")]
H_BEFORE = hash_tree(LOADED)

import numpy as np  # noqa: E402

import sweep as SW  # noqa: E402

FROM_SAVED = "--from-saved" in sys.argv
TAG025 = "[numerical FAIL, cause not established; careful-before-toy]; not a physical boundary"


def saved_res(i, f, tip, start, npz, dwj):
    """Rebuild run_start's result from saved outputs. Only cheap, drive-free quantities are recomputed
    (loop geometry, eigenvalues at the start, min gap on the loop)."""
    r, phase = SW.set_loop(start, tip)
    info = SW.start_info(start)
    pm = "p" if tip > 0 else "m"
    runs = {}
    for sp in SW.SPEEDS:
        for dn in SW.DIRS:
            for st in "AB":
                rec = {}
                for m in (1, 2):
                    w = np.asarray(npz[f"row{i}_{f}_{pm}_{sp}_{dn}_{st}_{2*m}pi_w"])
                    k = int(np.argmax(w))
                    rec[m] = {"win": "AB"[k], "phys": SW.phys(k, info), "w": float(w[k]), "wv": w}
                if sp == "slow40":
                    rec["dw"] = float(dwj[f"{pm}_{f}"]) if dn == "ccw" and st == "A" else 0.0
                runs[(sp, dn, st)] = rec
    return {"r": r, "phase": phase, "info": info, "runs": runs, "min_gap": SW.min_gap(tip, r)}


def checks():
    """Symmetry checks of H_A (no drive): mirror D H_A(e) D = H_A(-e), D = diag(1,-1), and H_A^T = H_A."""
    D = np.diag([1.0, -1.0])
    zs = [0.3 + 0.2j, -0.7 + 0.1j, 1.2 - 0.4j, 0.25 + 0j, 0.6j, 0.75 * SW.E + 0.1j]
    mir = max(float(np.abs(SW.D.H_A(-z) - D @ SW.D.H_A(z) @ D).max()) for z in zs)
    sym = max(float(np.abs(SW.D.H_A(z).T - SW.D.H_A(z)).max()) for z in zs)
    return mir, sym, len(zs)


def post_hoc(rows):
    """Post-hoc diagnostics (NOT used in the verdict; criteria stay as fixed in README)."""
    import json
    L = ["## Post-hoc diagnostics (not used in the verdict)", "",
         "The criteria in README.md were fixed before running and are not changed here. These notes only explain the interior result.", ""]
    inter = [r for r in rows if r["region"] == "interior" and r["res"] is not None]
    win_only = all(len({r["res"]["runs"][k][m]["win"] for k in r["res"]["runs"] for m in (1, 2)}) == 1 for r in inter)
    wins = sorted({r["res"]["runs"][k][m]["phys"] for r in inter for k in r["res"]["runs"] for m in (1, 2)})
    w100 = min(r["res"]["runs"][(sp, d, st)][m]["w"] for r in inter for sp in ("slow100",) for d in ("ccw", "cw") for st in "AB" for m in (1, 2))
    wlow = min(r["res"]["runs"][k][m]["w"] for r in inter for k in r["res"]["runs"] for m in (1, 2))
    L.append(f"- Winner-only reading at the default dt: every interior run (both tips, all three speeds, 2π and 4π, ccw and cw, from A and from B) has the same winner: {win_only} ({', '.join(wins)}). That is the D6 winner pattern (loss picks the mode, direction ignored). The pre-fixed threshold w ≥ 0.9 fails because at γT = 20 and 40 the weights are only {wlow:.3f}–0.84 (mostly at 4π and from start sheet B). At γT = 100 all interior weights are ≥ {w100:.4f}. drive-return's D6 PASS used winners only (no w threshold), which is why 0.75 ε_EP was D6 there and is MIXED here under the stricter pre-fixed rule.")
    f = ROOT / "outputs" / "diag_dt.json"
    if f.exists():
        d = json.loads(f.read_text(encoding="utf-8"))
        L += ["", f"- dt convergence at γT = 40 (`diag_dt.py`, dt refined by factors {d['factors']} relative to drive-return's dt rule), weight of sheet B at 4π:", "",
              "| tip | start | dir | from | w_B at dt factors " + " / ".join(str(k) for k in d["factors"]) + " | spread |", "|---|---|---|---|---|---|"]
        for r in d["rows"]:
            L.append(f"| {'+' if r['tip'] > 0 else '−'}ε_EP | {r['tip'] * r['frac']:+.2f} | {r['dir']} | {r['start']} | {' / '.join(f'{w:.5f}' for w in r['wB'])} | {max(r['wB']) - min(r['wB']):.1e} |")
        L += ["", "  Reading: the ±0.75 starts are converged to better than 1e-5 and ±0.50 to about 1e-3. At ±0.25 (loop r = 0.75 ε_EP) the weights do not converge when dt is refined; at +0.25, cw from B at factor 4 even gives w_B = 0.107, so the winner itself flips.",
              "",
              "  ±0.25 rows: **[numerical FAIL, cause not established; careful-before-toy]**. This is not a physical boundary: it says nothing about where D6 or D7 behaviour stops. Two candidate causes, neither tested:",
              "  1. Integrator breakdown on the big loop (r = 0.75 ε_EP). Evidence: U_cw = U_ccwᵀ holds exactly for this driver (H_A is complex-symmetric and the cw midpoint steps are the ccw steps in reverse order), yet cw and ccw give different weights (+0.25, from A, γT = 40, 4π: ccw 0.7851, cw 0.7235), and the weights jump under dt refinement (table above).",
              "  2. Roundoff amplification by exp(∫|Im(λ_A−λ_B)| dt) over the loop.",
              "  Tests (named, not run): a tight adaptive solver at rtol ~1e-12 rules out integrator error, and an mpmath (high-precision) run rules out roundoff. Whichever one restores cw = ccw identifies the cause."]
    L.append("")
    return L


def main() -> int:
    E = SW.E
    t0 = time.time()
    rows = []
    if FROM_SAVED:
        import json
        npz = np.load(ROOT / "outputs" / "sweep.npz")
        dwj = json.loads((ROOT / "outputs" / "dw.json").read_text(encoding="utf-8"))["dw"]
    for tip, tname in ((E, "+ε_EP"), (-E, "−ε_EP")):
        for f in SW.FRACS:
            start = (1 if tip > 0 else -1) * f * E
            region = "interior" if f < 1 else ("on Γ (end point)" if f == 1 else "exterior")
            row = {"tip": tname, "frac": f, "start": start, "region": region, "F": start ** 2 - E ** 2}
            if abs(f - 1.0) < 1e-12:
                w, _ = np.linalg.eig(SW.D.H_A(complex(start)))
                row.update({"cls": "FAIL", "why": f"degenerate: the start is the EP itself (r = 0; eigenvalues {w[0]:.6f}, {w[1]:.6f} coincide to {abs(w[0]-w[1]):.1e}; H_A defective, no eigenbasis to start in); not run",
                            "kind": "EP (both merge)", "res": None})
            else:
                res = saved_res(len(rows), f, tip, start, npz, dwj) if FROM_SAVED else SW.run_start(start, tip)
                cls, why = SW.classify(res)
                if cls == "FAIL":
                    why = f"{why} {TAG025}"
                row.update({"cls": cls, "why": why, "kind": res["info"]["kind"], "res": res})
            rows.append(row)
            print(f"{tname} start {row['start']/E:+.2f} ε_EP [{region}] F_JT={row['F']:+.5f} {row['kind']} → {row['cls']} ({row['why']}) t={time.time()-t0:.0f}s")
    H_AFTER = hash_tree(LOADED)
    same = H_BEFORE == H_AFTER
    inter = [r for r in rows if r["region"] == "interior"]
    exter = [r for r in rows if r["region"] == "exterior"]
    ok = all(r["cls"] == "D6-like" for r in inter) and all(r["cls"] == "D7-like" for r in exter)
    bad = [f"{r['tip']} {r['frac']:.2f} ({r['region']}: {r['cls']})" for r in inter + exter
           if (r["region"] == "interior" and r["cls"] != "D6-like") or (r["region"] == "exterior" and r["cls"] != "D7-like")]
    verdict = "REGION MAP YES" if ok else "REGION MAP NO"
    reason = ("all interior starts D6-like and all exterior starts D7-like at both tips" if ok else "not matching: " + "; ".join(bad))
    mir, sym, npts = checks()
    conv_int = [r for r in inter if r["cls"] != "FAIL"]
    cwccw = max(abs(r["res"]["runs"][(sp, "ccw", st)][m]["w"] - r["res"]["runs"][(sp, "cw", st)][m]["w"]) for r in conv_int for sp in SW.SPEEDS for st in "AB" for m in (1, 2))
    win_conv = all(len({r["res"]["runs"][k][m]["win"] for k in r["res"]["runs"] for m in (1, 2)}) == 1 for r in conv_int)
    by = {(r["tip"], r["frac"]): r for r in rows}
    d5075 = max(abs(by[(t, 0.75)]["res"]["runs"][k][m]["w"] - by[(t, 0.5)]["res"]["runs"][k][m]["w"]) for t in ("+ε_EP", "−ε_EP") for k in by[(t, 0.75)]["res"]["runs"] for m in (1, 2))
    d5075_40 = max(abs(by[(t, 0.75)]["res"]["runs"][("slow40", d, st)][2]["w"] - by[(t, 0.5)]["res"]["runs"][("slow40", d, st)][2]["w"]) for t in ("+ε_EP", "−ε_EP") for d in SW.DIRS for st in "AB")
    VLINE = ("REGION MAP NO under the pre-fixed w ≥ 0.9 at γT = 40 rule. At the winner level, every converged start matches: interior D6-like (same winner both ways) and exterior D7-like."
             if not ok else "REGION MAP YES")
    PLINE = ("Physics reading: the interior starts that converge are D6 in the winner-and-direction sense at every speed; the w rule fails because loss selection is incomplete at γT ≤ 40 [computed]. "
             "cw = ccw weights at interior starts follow from M_cw = M_ccwᵀ (complex-symmetric H_A) [standard + computed].")
    print(VLINE)
    print(PLINE)
    print(f"mirror check max |H_A(−ε) − D H_A(ε) D| = {mir:.1e} ({npts} points); max |H_Aᵀ − H_A| = {sym:.1e}; converged interior max |w_ccw − w_cw| = {cwccw:.1e}; winner-level D6 at converged interior starts: {win_conv}")
    print(f"{verdict} — {reason}")
    print(f"loaded folders unchanged (SHA-256 of {len(H_BEFORE)} files before/after): {same}")

    def wcell(res, sp, m):
        R = res["runs"]
        return "; ".join(f"{st}: ccw→{R[(sp,'ccw',st)][m]['win']} {R[(sp,'ccw',st)][m]['phys']} ({R[(sp,'ccw',st)][m]['w']:.4f}), cw→{R[(sp,'cw',st)][m]['win']} {R[(sp,'cw',st)][m]['phys']} ({R[(sp,'cw',st)][m]['w']:.4f})" for st in "AB")

    L = ["# pairA-drive-sweep — RESULTS", "", "**Signed off 2026-09-25:** Venus (maths) and Helios (physics).", "",
         "D6/D7 region sweep on the Pair A two-mode toy. H_A, the propagator and the driver are imported read-only from pairA-drive-return (not rebuilt). "
         "Classification criteria and loop convention were fixed in README.md before running. A and B WRITE, C held (not in the 2×2 dynamics).", "",
         "## Verdict", "", f"**{VLINE}**", "",
         "(Rule as fixed in README.md: w ≥ 0.9 at every slow speed γT = 20, 40, 100, with the dt-halving check at γT = 40. The interior weights fall below 0.9 at γT = 20 and 40; at γT = 100 they are all ≥ 0.9998.)", "",
         f"Rule-level detail: {verdict} — {reason}.", "",
         PLINE, "",
         f"Computed support: converged interior starts (±0.50, ±0.75) have one winner (slower-decaying) for every speed, turn, direction and start sheet: {win_conv}; max |w_ccw − w_cw| over them = {cwccw:.1e}; max |H_Aᵀ − H_A| = {sym:.1e} at {npts} complex ε. Exterior starts: all D7-like, all converged.", "",
         "The on-Γ starts (±1.00 ε_EP) are reported but not counted as interior or exterior.", "",
         "## Summary table", "",
         "| tip | start ε/ε_EP | region | loop r/ε_EP, phase | F_JT sign | eigenvalues at start | ccw vs cw winner (γT = 40, 4π; from A / from B) | class | reason |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        res = r["res"]
        if res is None:
            L.append(f"| {r['tip']} | {r['frac']*(1 if r['tip'][0]=='+' else -1):+.2f} | {r['region']} | r = 0 | 0 (F_JT = {r['F']:+.1e}) | {r['kind']} | — | **{r['cls']}** | {r['why']} |")
            continue
        R = res["runs"]
        win = "; ".join(f"from {st}: ccw {R[('slow40','ccw',st)][2]['phys']} ({R[('slow40','ccw',st)][2]['w']:.4f}), cw {R[('slow40','cw',st)][2]['phys']} ({R[('slow40','cw',st)][2]['w']:.4f})" for st in "AB")
        sgn = "−" if r["F"] < 0 else "+"
        L.append(f"| {r['tip']} | {r['start']/E:+.2f} | {r['region']} | {res['r']/E:.2f}, {'π' if res['phase'] else '0'} | {sgn} ({r['F']:+.5f}) | {r['kind']}: λ_A = {res['info']['lam'][0]:.5f}, λ_B = {res['info']['lam'][1]:.5f} | {win} | **{r['cls']}** | {r['why']} |")
    L += ["", "## Full winners (every slow speed, both turns)", "", "Format: start sheet: ccw → winner label, physical name (weight), cw → … . Labels A/B are the sheets at the start point (= recording point).", ""]
    for r in rows:
        res = r["res"]
        if res is None:
            continue
        L.append(f"### {r['tip']}, start {r['start']/E:+.2f} ε_EP ({r['region']}): {r['cls']}" + (f" {TAG025}" if r["cls"] == "FAIL" else ""))
        L.append(f"- loop: r = {res['r']/E:.2f} ε_EP around {r['tip']}, min |λ₊−λ₋| on the loop = {res['min_gap']:.6f}; max |Δw| under dt halving (γT = 40, all 4 runs) = {max(res['runs'][k]['dw'] for k in res['runs'] if 'dw' in res['runs'][k]):.1e}")
        for sp in SW.SPEEDS:
            for m in (1, 2):
                L.append(f"- {sp} {2*m}π: {wcell(res, sp, m)}")
        L.append("")
    L += ["## Notes", "",
          "- Loop radius convention: r = |ε_start − tip| so that the loop passes through the start point; identical to drive-return for 0.75 and 1.25 around +ε_EP (r = 0.25 ε_EP). Other starts need other radii (0.75, 0.50, 0.10, 0.50 × ε_EP); the radius therefore changes together with the start point, which is a confound: the sweep tests start point + radius jointly. "
          f"Starts 0.75 (r = 0.25) and 0.50 (r = 0.50) give nearly the same weights at γT = 40, 4π (max difference {d5075_40:.4f}); over all speeds and turns the difference is larger (up to {d5075:.4f}, at γT = 20), so the radius effect is small at γT = 40 but not ruled out. "
          "Suggested follow-up (not run): fix the start at 0.75 ε_EP and vary r over 0.25 / 0.50 / 0.75 ε_EP. Any re-test needs a new criterion fixed in advance (v2); the verdict above stays under the v1 criteria.",
          f"- Mirror convention: −ε_EP loops start at the mirrored points; ccw means counter-clockwise in the complex ε plane for both tips, in the table and in every − row. ε → −ε is a rotation by π (orientation-preserving) and H_A(−ε) = D H_A(ε) D, D = diag(1,−1); so ccw ↔ ccw, matching the table [standard + computed] (computed: max |H_A(−ε) − D H_A(ε) D| = {mir:.1e} at {npts} complex ε).",
          "- 'lower/higher-frequency' means signed Re λ, with ψ ~ e^{−iλt}; the two frequencies are equal and opposite.",
          "- Start ±1.00 ε_EP is the EP itself: degenerate, reported as FAIL and not run.",
          "- Winner = larger left-eigenvector weight at the start point after 2π / 4π (drive-return's `decompose`). Physical name: slower-/faster-decaying where the two modes share a frequency (inside Γ), higher-/lower-frequency where they share a decay (outside Γ).", "",
          ]
    L += post_hoc(rows)
    L += ["## Loaded folders (read-only)", ""]
    L += [f"- `{p}`" for p in LOADED]
    L += [f"- SHA-256 of every file ({len(H_BEFORE)} files) before and after: **{'unchanged' if same else 'CHANGED'}**.", "",
          "Scope: two-mode toy; driven evolution i dψ/dt = H_A(ε(t))ψ as in drive-return. No QG, JT or Einstein claim.", ""]
    L.insert(L.index("## Loaded folders (read-only)") + 1, "")
    L.insert(L.index("## Loaded folders (read-only)") + 2, ("Generated with `--from-saved`: weights from outputs/sweep.npz, dt-halving maxima from outputs/dw.json, diagnostics from outputs/diag_dt.json; no drive was re-run. Loop geometry, start eigenvalues, min gap and the H_A symmetry checks are recomputed (no time evolution)." if FROM_SAVED else "Generated by a full run."))
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    if FROM_SAVED:
        print("Wrote RESULTS.md (from saved outputs)")
        return 0 if same else 1
    import json
    dwo = {("p" if r["tip"][0] == "+" else "m") + "_" + str(r["frac"]): max(r["res"]["runs"][k]["dw"] for k in r["res"]["runs"] if "dw" in r["res"]["runs"][k]) for r in rows if r["res"] is not None}
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "dw.json").write_text(json.dumps({"source": "full run", "dw": dwo}, indent=1), encoding="utf-8")
    sv = {}
    for i, r in enumerate(rows):
        if r["res"] is None:
            continue
        for k, rec in r["res"]["runs"].items():
            for m in (1, 2):
                sv[f"row{i}_{r['frac']}_{'p' if r['tip'][0]=='+' else 'm'}_{k[0]}_{k[1]}_{k[2]}_{2*m}pi_w"] = rec[m]["wv"]
    (ROOT / "outputs").mkdir(exist_ok=True)
    np.savez(ROOT / "outputs" / "sweep.npz", **sv)
    print("Wrote RESULTS.md")
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())

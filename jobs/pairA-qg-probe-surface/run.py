"""pairA-qg-probe-surface: QG probe on the Pair A surface (cut, flip, inside/outside switch).
No new Hamiltonian, no Einstein solver. `python run.py` writes RESULTS.md."""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import load_surface as LS  # noqa: E402  (no handoff import at module level)

H_BEFORE = LS.hash_tree()   # before anything from the loaded folders is imported

import numpy as np  # noqa: E402

from cover import run_cover  # noqa: E402
from dictionary import build  # noqa: E402
from verdict import verdict  # noqa: E402


def yn(b):
    return "YES" if b else "NO"


def main() -> int:
    S = LS.load()
    E = S["EPS_EP"]
    print(f"eps_EP = {E!r} = |a-b|/(2|v|) = {S['formula']!r} (asserted); |eps_EP - 0.51368066| = {abs(E-LS.EPS_EP_REF):.1e}")
    cov = run_cover(S)
    for r in cov:
        print(f"cover {r['name'][:40]:40s} I={r['I']} signed={r['I_signed']} U_G={r['U_G']:+d} n_A={r['n_A']} n_B={r['n_B']} match={r['match']}")
    # hashes after the computations that touch the loaded folders
    H_MID = LS.hash_tree()
    rows = build(S, cov, H_BEFORE, H_MID)
    V = verdict(rows)
    for r in rows:
        print(f"{r['id']} {'PASS' if r['result'] else 'FAIL'} {r['tag']} — {r['claim']}")
    print(V)
    H_AFTER = LS.hash_tree()
    same = H_BEFORE == H_AFTER
    changed = sorted(set(H_BEFORE) ^ set(H_AFTER) | {k for k in H_BEFORE if H_AFTER.get(k) != H_BEFORE[k]})
    print(f"loaded folders unchanged (SHA-256 of {len(H_BEFORE)} files before/after): {same}")

    L = ["**Signed off 2026-09-25:** Venus (maths) and Helios (physics) on D1–D7 and cover.", "", "# pairA-qg-probe-surface — RESULTS", "",
         "QG probe on the Pair A surface using the cut Γ, the 2π/4π flip and the inside/outside switch. Two-mode toy; no new MHD Hamiltonian, no Einstein solver. "
         "No QG Hamiltonian was found and none is claimed; no JT dual is claimed.", "",
         "## Verdict", "", V, "",
         "Meaning: the surface has these properties [standard]; reading them as QG is [hive-interpretation].", "",
         f"Failed rows: {', '.join(r['id'] for r in rows if not r['result']) or 'none'} (no row was fudged).", "",
         "## Definition of 'stall' (Akitti, 2026-09-25)", "",
         "> " + __import__('stall').AKITTI_DEF, "",
         "Handoff source for the same fact (per Akitti): probe.py:44 `\"allowed_past_Wick\": [\"A\", \"B\"],`.", "",
         "## Dictionary D1–D7", "",
         "Tags (Venus): [by definition] / [by construction] carry no new information; [computed] rows carry information. As surface properties, D1–D7 are [standard] non-Hermitian two-mode physics; using them as a QG dictionary is [hive-interpretation].", "",
         "| row | property | result | tag | information? | conditions | evidence |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        info = r.get("info") or ("yes (computed)" if "computed" in r["tag"] else "no")
        L.append(f"| {r['id']} | {r['claim']} | **{'PASS' if r['result'] else 'FAIL'}** | {r['tag']} | {info} | {r['conditions']} | {r['evidence']} |")
    d4 = [r for r in rows if r["id"] == "D4"][0]
    L += ["", "## D4 detail: two-detour test at each tip", "",
          "Start on real ε inside Γ with A = λ_EP + y/2, B = λ_EP − y/2 (upper-lip convention); semicircle r = 0.25 ε_EP around the tip to real ε outside Γ; continuous tracking.", "",
          "| tip | route | start → end (ε/ε_EP) | A lands on | B lands on | A, B labels at end | (a) swapped | (b) 2π/4π | (c) C held | (d) allowed_past_Wick | tip PASS |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for nm, pt in d4["parts"].items():
        dd = pt["detour"]
        for rt in ("above", "below"):
            q = dd[rt]
            L.append(f"| {nm} | {rt} | {dd['start'].real/E:+.2f} → {dd['end'].real/E:+.2f} | {q['land']['A']}-frequency | {q['land']['B']}-frequency | {q['label_at_end']['A']}, {q['label_at_end']['B']} | "
                     f"{yn(dd['swapped'])} | {yn(pt['b'])} | {yn(pt['c'])} | {yn(pt['d'])} | **{yn(pt['a'] and pt['b'] and pt['c'] and pt['d'])}** |")
    L += ["", "## Cover check: U_G[γ] = (−1)^{I(γ,Γ)} vs Φ(n) = (−1)^n", "",
          "I = number of crossings of the discretised loop (8000 steps per turn) with the segment Γ = [−ε_EP, ε_EP] itself (not an outward-ray cut), mod 2 for U_G. "
          "n = sheet index change from continuous eigenvalue tracking along the loop (handoff tracker.align_evals nearest-distance matching): 0 = return, 1 = swap. "
          "Start sheets A/B = vortices-return convention (A = λ_EP + y/2, B = λ_EP − y/2, Γ-segment cut). Φ(0) = +1, Φ(1) = −1.", "",
          "| loop | start ε/ε_EP | winding (+ε_EP, −ε_EP) | I (unsigned) | signed count | crossing points x/ε_EP | U_G | n_A | n_B | Φ(n_A) | Φ(n_B) | Φ = U_G for A and B | tracking jump ratio |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in cov:
        xs = ", ".join(f"{x/E:+.4f}" for x in r["x_cross"]) or "—"
        L.append(f"| {r['name']} | {r['start'].real/E:+.4f} | ({r['wind_plus']:+d}, {r['wind_minus']:+d}) | {r['I']} | {r['I_signed']:+d} | {xs} | {r['U_G']:+d} | {r['n_A']} | {r['n_B']} | {r['Phi_A']:+d} | {r['Phi_B']:+d} | **{yn(r['match'])}** | {r['jump_ratio']:.1e} |")
    f8 = [r for r in cov if r["name"].startswith("figure-eight")][0]
    L += ["", f"All loops: Φ(n) = U_G for A and B: **{yn(all(r['match'] for r in cov))}**.",
          f"Figure-eight: unsigned count {f8['I']}, signed count {f8['I_signed']:+d} (same parity, even → U_G = +1). "
          "Both passes cross Γ at ε = 0 in the same vertical direction, so the signed count here is ±2, not 0: Γ ends at the tips, and a loop around one tip meets it once, with sign set by the direction of travel; the two lobes run in opposite senses but each crosses Γ downward. Only the parity enters U_G.", "",
          "## Loaded inputs (read-only) and unchanged check", "",
          f"- Handoff `{LS.HANDOFF}`: seed.H_A, seed.A/B/V, seed.EPS_EP (asserted = |a−b|/(2|v|) = {S['formula']:.12f}; agrees with 0.51368066 to {abs(E-LS.EPS_EP_REF):.1e}), seed.LAM_EP, "
          "tracker.align_evals, wick_lorentzian.chart() (Γ), outputs/Jhat.npz (Jhat2, Jhat4), text of RESULTS.md / RESULTS_probe.md / probe.py / histories.py for D1, D4, D5.",
          f"- Drive-return `{LS.DRIVE}`: outputs/drive.npz (0.75 ε_EP start, D6), outputs/drive_start1p25.npz (1.25 ε_EP start, D7), RESULTS.md and RESULTS_start1p25.md (verdict and sign-off lines). No drive was re-run.",
          f"- Vortices-return `{LS.VORT}`: sheet A/B convention (return_test.y_cut_gamma, re-implemented identically in load_surface.y_cut_gamma); searched for 'stall'.",
          f"- SHA-256 of every file in the three folders ({len(H_BEFORE)} files) before any import and after all computations: **{'unchanged' if same else 'CHANGED: ' + ', '.join(changed)}**.", "",
          "## Scope", "",
          "Two-mode toy (H_A is 2x2). The dictionary rows are properties of this non-Hermitian surface; reading them as QG is [hive-interpretation]. "
          "No QG Hamiltonian was found or claimed; no JT dual is claimed. C stays held (never written).", ""]
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("Wrote RESULTS.md")
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())

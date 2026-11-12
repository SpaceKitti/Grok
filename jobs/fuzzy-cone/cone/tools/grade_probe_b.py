#!/usr/bin/env python3
"""Grade Probe B v2 against Y_JUNCTION_B_V2_FREEZE.md b84a670a (pins Q1–Q6).

Spec text: Y_JUNCTION_SPEC_B_DRAFT_V2.md 8a0ca930.
Uses grade_result.py c188ec50 for the structural gate.
"""
from __future__ import annotations

import json
import os
import sys
import subprocess
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CONE = os.path.abspath(os.path.join(HERE, "..", "fuzz", "cone"))
sys.path.insert(0, HERE)
from ring_projector import sha256_file, uk_now
from probe_b import Q_TOL, RANK_EXPECT


def _shape_label(r) -> str:
    """Per-solve shape tag from peaks + A3 (used for seed agreement / moduli)."""
    a3 = float(r["probe_B"]["A3"])
    pN = int(r["probe_B"]["peaks_north"]["n_peaks"])
    pS = int(r["probe_B"]["peaks_south"]["n_peaks"])
    # "keeps seeded shape" proxies
    if pN >= 3 and pS >= 3 and a3 > 0.1:
        return "THREE-LEG"
    if a3 < 0.02 and pN <= 1 and pS <= 1:
        return "MERGE-LIKE"  # coincident / single peak
    if 0.02 < a3 <= 0.1:
        return "THREE-MODE-RING"
    return "OTHER"


def _seed_verdict_for_cell(rows_seed, grid_err, e_s1, e_s2, shape_s1, shape_s2, s1_three, s2_three):
    """Classify one (b,N,seed) given both starts. Returns label or None if incomplete."""
    # BROKEN/UNDECIDED handled globally; here shape rules only
    # Q1 DEGENERATE: both converge (assumed), |E(S2)-E(S1)|<=grid_err, each keeps seeded shape
    # S1 seeded = coincident → MERGE-LIKE; S2 seeded = three-leg → THREE-LEG
    if (
        abs(e_s2 - e_s1) <= grid_err + 1e-15
        and shape_s1 == "MERGE-LIKE"
        and shape_s2 == "THREE-LEG"
    ):
        return "DEGENERATE"
    # THREE-LEG (spec + Q1): S2 has three peaks & A3>0.1, E(S2)<=E(S1)+grid_err,
    # and S1 (kicked) also splits into three peaks
    if s2_three and shape_s2 == "THREE-LEG" and e_s2 <= e_s1 + grid_err + 1e-15 and s1_three:
        return "THREE-LEG"
    # THREE-MODE RING
    if shape_s2 == "THREE-MODE-RING" and shape_s1 in ("MERGE-LIKE", "THREE-MODE-RING", "OTHER"):
        # require A3 band at this cell; both N checked at aggregation
        return "THREE-MODE-RING"
    # MERGE: S2 relaxes to S1
    if (
        abs(e_s2 - e_s1) <= grid_err + 1e-15
        and shape_s2 == "MERGE-LIKE"
        and shape_s1 == "MERGE-LIKE"
        and float(rows_seed["S2"]["probe_B"]["A3"]) < 0.02
    ):
        return "MERGE"
    return "UNDECIDED"


def grade(sweep: dict) -> dict:
    rows = [r for r in sweep.get("rows", []) if r.get("status") == "ok"]
    broken, undecided = [], []
    q_flags = []

    for r in rows:
        tag = f"{r['start']} b={r['b']} N={r['N']} seed={r['kick_seed']}"
        if not r["convergence"]["converged"]:
            undecided.append(f"{tag} non-converged")
        if r["projector"]["rank_N"] != RANK_EXPECT or r["projector"]["rank_S"] != RANK_EXPECT:
            broken.append(
                f"{tag} rank {r['projector']['rank_N']}/{r['projector']['rank_S']} != {RANK_EXPECT}/{RANK_EXPECT}"
            )
        aq = r["flux"].get("abs_Q_minus_6")
        if aq is None:
            aq = abs(float(r["flux"]["Q_total"]) - 6.0)
        if aq > Q_TOL:
            broken.append(f"{tag} |Q-6|={aq:.4g} > {Q_TOL}")
        elif aq > 1e-2:
            q_flags.append({"tag": tag, "abs_Q_minus_6": aq, "Q_total": r["flux"]["Q_total"]})

    # index: (start,b,N,seed)
    by = {}
    for r in rows:
        by[(r["start"], float(r["b"]), int(r["N"]), int(r["kick_seed"]))] = r

    bs = sorted({float(r["b"]) for r in rows})
    Ns = sorted({int(r["N"]) for r in rows})
    seeds = sorted({int(r["kick_seed"]) for r in rows})
    starts = sorted({r["start"] for r in rows})

    # per-solve detail table
    solves_out = []
    for r in sorted(rows, key=lambda x: (x["b"], x["start"], x["N"], x["kick_seed"])):
        solves_out.append({
            "start": r["start"],
            "b": r["b"],
            "N": r["N"],
            "kick_seed": r["kick_seed"],
            "npz": r.get("npz"),
            "npz_sha8": r.get("npz_sha8"),
            "converged": r["convergence"]["converged"],
            "residual_inf": r["convergence"]["residual_inf"],
            "rank_N": r["projector"]["rank_N"],
            "rank_S": r["projector"]["rank_S"],
            "ev_proj_N": r["projector"].get("ev_proj_N"),
            "ev_proj_S": r["projector"].get("ev_proj_S"),
            "Q_total": r["flux"]["Q_total"],
            "abs_Q_minus_6": r["flux"].get("abs_Q_minus_6", abs(r["flux"]["Q_total"] - 6)),
            "E": r.get("E"),
            "A3": r["probe_B"]["A3"],
            "peaks_N": r["probe_B"]["peaks_north"]["n_peaks"],
            "peaks_S": r["probe_B"]["peaks_south"]["n_peaks"],
            "shape": _shape_label(r),
            "solve_sec": r.get("solve_sec"),
            "timestamp_uk": r.get("timestamp_uk"),
        })

    # Energy gaps S2-S1 per (b,N,seed) and grid errors |E81-E61|
    energy_gaps = []
    grid_errors = {}  # (start,b,seed) -> |E81-E61|
    for b in bs:
        for seed in seeds:
            for start in ("S1", "S2"):
                r61 = by.get((start, b, 61, seed))
                r81 = by.get((start, b, 81, seed))
                if r61 and r81 and r61.get("E") is not None and r81.get("E") is not None:
                    grid_errors[(start, b, seed)] = abs(float(r81["E"]) - float(r61["E"]))
            for N in Ns:
                r1 = by.get(("S1", b, N, seed))
                r2 = by.get(("S2", b, N, seed))
                if r1 and r2 and r1.get("E") is not None and r2.get("E") is not None:
                    energy_gaps.append({
                        "b": b, "N": N, "kick_seed": seed,
                        "E_S1": r1["E"], "E_S2": r2["E"],
                        "delta_E_S2_minus_S1": float(r2["E"]) - float(r1["E"]),
                        "abs_delta_E": abs(float(r2["E"]) - float(r1["E"])),
                    })

    # Per (b, seed): classify using both N (spec: A3/peaks at both N)
    per_b_seed = []
    for b in bs:
        for seed in seeds:
            # grid error: max over starts of |E81-E61|
            ge_list = [grid_errors[k] for k in grid_errors if k[1] == b and k[2] == seed]
            grid_err = max(ge_list) if ge_list else float("inf")

            cell_labels = []
            detail_N = {}
            ok_cell = True
            for N in Ns:
                r1 = by.get(("S1", b, N, seed))
                r2 = by.get(("S2", b, N, seed))
                if not r1 or not r2:
                    ok_cell = False
                    undecided.append(f"b={b} seed={seed} N={N} missing start")
                    continue
                s1 = _shape_label(r1)
                s2 = _shape_label(r2)
                s1_three = r1["probe_B"]["peaks_north"]["n_peaks"] >= 3 and r1["probe_B"]["peaks_south"]["n_peaks"] >= 3
                s2_three = r2["probe_B"]["peaks_north"]["n_peaks"] >= 3 and r2["probe_B"]["peaks_south"]["n_peaks"] >= 3
                lab = _seed_verdict_for_cell(
                    {"S1": r1, "S2": r2}, grid_err, float(r1["E"]), float(r2["E"]),
                    s1, s2, s1_three, s2_three,
                )
                # THREE-MODE RING needs both N in band — mark per N then require all
                if lab == "THREE-MODE-RING":
                    if not (0.02 < float(r2["probe_B"]["A3"]) <= 0.1):
                        lab = "UNDECIDED"
                cell_labels.append(lab)
                detail_N[N] = {
                    "label": lab,
                    "shape_S1": s1, "shape_S2": s2,
                    "E_S1": r1["E"], "E_S2": r2["E"],
                    "A3_S1": r1["probe_B"]["A3"], "A3_S2": r2["probe_B"]["A3"],
                    "peaks_S1": [r1["probe_B"]["peaks_north"]["n_peaks"], r1["probe_B"]["peaks_south"]["n_peaks"]],
                    "peaks_S2": [r2["probe_B"]["peaks_north"]["n_peaks"], r2["probe_B"]["peaks_south"]["n_peaks"]],
                    "s1_three": s1_three, "s2_three": s2_three,
                }
            if not ok_cell or len(cell_labels) < len(Ns):
                seed_label = "UNDECIDED"
            elif all(l == cell_labels[0] for l in cell_labels):
                seed_label = cell_labels[0]
            else:
                seed_label = "UNDECIDED"
                undecided.append(f"b={b} seed={seed} N-labels disagree: {cell_labels}")

            per_b_seed.append({
                "b": b, "kick_seed": seed,
                "grid_error": grid_err if ge_list else None,
                "label": seed_label,
                "by_N": detail_N,
            })

    # Q5: all three seeds must agree per b
    per_b = []
    for b in bs:
        labs = [e["label"] for e in per_b_seed if e["b"] == b]
        if len(labs) < 3:
            vb = "UNDECIDED"
            reason = f"missing seeds: {labs}"
            undecided.append(f"b={b} {reason}")
        elif all(l == labs[0] for l in labs) and labs[0] not in (None,):
            vb = labs[0]
            reason = "all three seeds agree"
        else:
            vb = "UNDECIDED"
            reason = f"seeds disagree: {labs}"
            undecided.append(f"b={b} {reason}")
        # energy gap summary at this b (mean over N,seed)
        gaps = [g for g in energy_gaps if g["b"] == b]
        per_b.append({
            "b": b,
            "verdict": vb,
            "reason": reason,
            "seed_labels": labs,
            "mean_abs_delta_E_S2_S1": (sum(g["abs_delta_E"] for g in gaps) / len(gaps)) if gaps else None,
            "max_abs_delta_E_S2_S1": max((g["abs_delta_E"] for g in gaps), default=None),
        })

    # Overall
    if broken:
        overall = "BROKEN"
    elif len(rows) < 36:
        overall = "UNDECIDED"
        undecided.append(f"only {len(rows)}/36 ok rows")
    elif any(e["verdict"] == "UNDECIDED" for e in per_b) or undecided:
        # if all per_b share a non-UNDECIDED and only undecided were soft notes... still UNDECIDED if any nonconv
        if any(not r["convergence"]["converged"] for r in rows):
            overall = "UNDECIDED"
        elif per_b and all(e["verdict"] == per_b[0]["verdict"] for e in per_b) and per_b[0]["verdict"] != "UNDECIDED":
            overall = per_b[0]["verdict"]
        else:
            overall = "UNDECIDED"
    elif per_b and all(e["verdict"] == per_b[0]["verdict"] for e in per_b):
        overall = per_b[0]["verdict"]
    else:
        overall = "UNDECIDED"
        undecided.append(f"b-verdicts disagree: {[e['verdict'] for e in per_b]}")

    absQs = [s["abs_Q_minus_6"] for s in solves_out]
    return {
        "timestamp_uk": uk_now(),
        "spec_sha8": "8a0ca930",
        "freeze_sha8": "b84a670a",
        "round2_sha8": "1202fa35",
        "grader_sha8": "c188ec50",
        "Q_tol": Q_TOL,
        "rank_expect": RANK_EXPECT,
        "n_rows": len(rows),
        "n_converged": sum(1 for r in rows if r["convergence"]["converged"]),
        "worst_abs_Q_minus_6": max(absQs) if absQs else None,
        "broken_reasons": broken,
        "undecided_reasons": undecided,
        "Q_flags_1e-2_to_3e-2": q_flags,
        "verdict": overall,
        "per_b": per_b,
        "per_b_seed": per_b_seed,
        "energy_gaps_S2_minus_S1": energy_gaps,
        "grid_errors_E81_minus_E61": [
            {"start": k[0], "b": k[1], "kick_seed": k[2], "abs_dE": v}
            for k, v in sorted(grid_errors.items())
        ],
        "solves": solves_out,
        "summary": {
            "all_36": len(rows) == 36,
            "all_converged": all(r["convergence"]["converged"] for r in rows) and len(rows) == 36,
            "all_rank_3": all(
                r["projector"]["rank_N"] == 3 and r["projector"]["rank_S"] == 3 for r in rows
            ),
            "is_BROKEN": overall == "BROKEN",
            "is_DEGENERATE": overall == "DEGENERATE",
            "is_THREE_LEG": overall == "THREE-LEG",
            "is_THREE_MODE_RING": overall == "THREE-MODE-RING",
            "is_MERGE": overall == "MERGE",
            "is_UNDECIDED": overall == "UNDECIDED",
            "seeds_agree_all_b": all(e["verdict"] != "UNDECIDED" or "disagree" not in e.get("reason", "") for e in per_b)
            and per_b and all(e["seed_labels"] and all(s == e["seed_labels"][0] for s in e["seed_labels"]) for e in per_b),
        },
    }


def main():
    sweep_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CONE, "SWEEP_probe_B.json")
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(CONE, "RESULT_PROBE_B.json")
    if not os.path.exists(sweep_path):
        print(json.dumps({"error": "sweep missing", "sweep_path": sweep_path}))
        return 2
    sweep = json.load(open(sweep_path))
    graded = grade(sweep)
    result = {
        "tool": "grade_probe_b.py",
        "sweep_path": os.path.abspath(sweep_path),
        "sweep_sha8": sha256_file(sweep_path)[:8],
        **graded,
    }
    rules = {
        "spec": "Y_JUNCTION_B_V2_FREEZE b84a670a",
        "pass": [
            ["summary.all_36", "==", True],
            ["summary.all_rank_3", "==", True],
        ],
        "fail": [
            ["summary.is_BROKEN", "==", True],
        ],
    }
    rules_path = os.path.join(CONE, "RULES_PROBE_B_V2.json")
    json.dump(rules, open(rules_path, "w"), indent=2)
    json.dump(result, open(out_path, "w"), indent=2)
    line = subprocess.run(
        [sys.executable, os.path.join(HERE, "grade_result.py"), rules_path, out_path],
        capture_output=True, text=True,
    ).stdout.strip()
    result["grade_result_line"] = line
    result["rules_path"] = rules_path
    result["rules_sha8"] = sha256_file(rules_path)[:8]
    json.dump(result, open(out_path, "w"), indent=2)
    print(json.dumps({
        "out": out_path,
        "sha8": sha256_file(out_path)[:8],
        "verdict": result["verdict"],
        "n_converged": result["n_converged"],
        "worst_abs_Q_minus_6": result["worst_abs_Q_minus_6"],
        "grade_result_line": line,
        "timestamp_uk": result["timestamp_uk"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

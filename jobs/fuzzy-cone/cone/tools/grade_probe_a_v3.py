#!/usr/bin/env python3
"""Build RESULT_PROBE_A.json from SWEEP_probe_A_v3.json and grade via grade_result.py.

Applies Spec A v3 + freeze 6e0f1942 + addendum 61f39a62. No refits.
"""
from __future__ import annotations

import json, os, sys, subprocess
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CONE = os.path.abspath(os.path.join(HERE, "..", "fuzz", "cone"))
sys.path.insert(0, HERE)
from ring_projector import sha256_file, uk_now, Q_CAP_RC  # noqa: E402


def _pole_r(row, pole):
    return row["ring"][pole]["r_peak"]  # dimensionless primary


def _pole_f(row, pole):
    return row["ring"][pole]["f"]


def grade_sweep(sweep: dict) -> dict:
    rows = [r for r in sweep.get("rows", []) if r.get("status") == "ok" and not r.get("non_result")]
    by_b = defaultdict(dict)
    for r in rows:
        by_b[float(r["b"])][int(r["N"])] = r

    q_flags = []
    broken_reasons = []
    undecided_reasons = []

    # Global BROKEN / UNDECIDED scans
    for r in rows:
        b, N = r["b"], r["N"]
        tag = f"b={b} N={N}"
        if not r["convergence"]["converged"]:
            undecided_reasons.append(f"{tag} not converged residual={r['convergence']['residual_inf']}")
        if r["projector"]["rank_N"] != 2 or r["projector"]["rank_S"] != 2:
            broken_reasons.append(
                f"{tag} rank {r['projector']['rank_N']}/{r['projector']['rank_S']} != 2/2"
            )
        aq = r["flux"]["abs_Q_minus_4"]
        if aq is not None and aq > 3e-2:
            broken_reasons.append(f"{tag} |Q-4|={aq:.4g} > 3e-2")
        elif aq is not None and aq > 1e-2:
            q_flags.append({"b": b, "N": N, "abs_Q_minus_4": aq, "Q_total": r["flux"]["Q_total"]})
        if r["ring"].get("vertex_outside_any"):
            undecided_reasons.append(f"{tag} vertex outside fit window")

    per_b = []
    yes_bs = []
    nomove_bs = []
    for b in sorted(by_b):
        block = by_b[b]
        entry = {"b": b, "N_present": sorted(block), "poles": {}}
        if set(block) != {41, 61, 81}:
            entry["verdict"] = "UNDECIDED"
            entry["reason"] = f"missing N values: have {sorted(block)}"
            undecided_reasons.append(f"b={b} {entry['reason']}")
            per_b.append(entry)
            continue

        # floor = max f over both poles and all three N (freeze P5)
        floors = []
        for N in (41, 61, 81):
            for pole in ("north", "south"):
                floors.append(_pole_f(block[N], pole))
        floor = max(floors)
        entry["floor_f"] = floor
        entry["f_values"] = floors

        pole_info = {}
        signs = []
        move_flags = []
        nomove_flags = []
        mono_flags = []
        for pole in ("north", "south"):
            r41 = _pole_r(block[41], pole)
            r61 = _pole_r(block[61], pole)
            r81 = _pole_r(block[81], pole)
            delta = r81 - r41
            # monotone 41->61->81 (freeze P2): non-decreasing or non-increasing matching delta sign
            if delta > 0:
                mono = (r61 >= r41 - 1e-15) and (r81 >= r61 - 1e-15)
            elif delta < 0:
                mono = (r61 <= r41 + 1e-15) and (r81 <= r61 + 1e-15)
            else:
                mono = abs(r61 - r41) <= 1e-15 and abs(r81 - r61) <= 1e-15
            gt3 = abs(delta) > 3.0 * floor
            le1 = abs(delta) <= floor
            pole_info[pole] = {
                "r41": r41,
                "r61": r61,
                "r81": r81,
                "delta_r81_minus_r41": delta,
                "monotone": mono,
                "abs_delta": abs(delta),
                "gt_3x_floor": gt3,
                "le_floor": le1,
            }
            signs.append(1 if delta > 0 else (-1 if delta < 0 else 0))
            move_flags.append(gt3 and mono)
            nomove_flags.append(le1)
            mono_flags.append(mono)

        same_sign = signs[0] != 0 and signs[0] == signs[1]
        entry["poles"] = pole_info
        entry["same_sign"] = same_sign
        entry["all_monotone"] = all(mono_flags)

        if broken_reasons:
            entry["verdict"] = "BROKEN_GLOBAL"
        elif any(
            not block[N]["convergence"]["converged"] for N in (41, 61, 81)
        ) or any(block[N]["ring"].get("vertex_outside_any") for N in (41, 61, 81)):
            entry["verdict"] = "UNDECIDED"
        elif all(move_flags) and same_sign:
            entry["verdict"] = "YES"
            yes_bs.append(b)
        elif all(nomove_flags):
            entry["verdict"] = "NO-MOVE"
            nomove_bs.append(b)
        else:
            entry["verdict"] = "UNDECIDED"
            entry["reason"] = "shift neither clearly >3f with monotone same-sign nor <=f"
        per_b.append(entry)

    # Criticality trend (output only): does |delta| grow as b -> 1?
    deltas = []
    for e in per_b:
        if "poles" in e and "north" in e["poles"]:
            d = 0.5 * (
                abs(e["poles"]["north"]["delta_r81_minus_r41"])
                + abs(e["poles"]["south"]["delta_r81_minus_r41"])
            )
            deltas.append((e["b"], d))
    deltas_sorted = sorted(deltas, key=lambda t: t[0])  # ascending b toward 1
    # as b decreases toward 1, does d increase?
    trend = None
    if len(deltas_sorted) >= 2:
        bs = [t[0] for t in deltas_sorted]
        ds = [t[1] for t in deltas_sorted]
        # check if d is non-increasing as b increases (i.e. grows as b->1)
        trend = all(ds[i] >= ds[i + 1] - 1e-15 for i in range(len(ds) - 1))
    criticality_trend = {
        "deltas_by_b": [{"b": b, "mean_abs_delta": d} for b, d in deltas_sorted],
        "abs_delta_grows_as_b_to_1": trend,
        "note": "output only; not graded",
    }

    if broken_reasons:
        overall = "BROKEN"
    elif undecided_reasons or any(e.get("verdict") == "UNDECIDED" for e in per_b):
        overall = "UNDECIDED"
    elif per_b and all(e.get("verdict") == "YES" for e in per_b):
        overall = "YES"
    elif per_b and all(e.get("verdict") == "NO-MOVE" for e in per_b):
        overall = "NO-MOVE"
    else:
        overall = "UNDECIDED"

    # Booleans for grade_result.py
    all_conv = all(r["convergence"]["converged"] for r in rows) and len(rows) == 12
    all_rank2 = all(
        r["projector"]["rank_N"] == 2 and r["projector"]["rank_S"] == 2 for r in rows
    )
    max_abs_Q_m4 = max((r["flux"]["abs_Q_minus_4"] or 0) for r in rows) if rows else None

    return {
        "timestamp_uk": uk_now(),
        "spec_sha8": "8d7f5092",
        "freeze_sha8": "6e0f1942",
        "addendum_sha8": "61f39a62",
        "code_sha8": "63b69fbc",
        "grader_sha8": "c188ec50",
        "Q_cap_rc_rho": Q_CAP_RC,
        "Q_broken_tol": 3e-2,
        "Q_flag_band": [1e-2, 3e-2],
        "n_rows_graded": len(rows),
        "broken_reasons": broken_reasons,
        "undecided_reasons": undecided_reasons,
        "Q_flags_1e-2_to_3e-2": q_flags,
        "per_b": per_b,
        "criticality_trend": criticality_trend,
        "verdict": overall,
        "summary": {
            "all_12_converged": all_conv,
            "all_rank_equals_2": all_rank2,
            "max_abs_Q_minus_4": max_abs_Q_m4,
            "n_Q_flags": len(q_flags),
            "is_BROKEN": overall == "BROKEN",
            "is_YES": overall == "YES",
            "is_NO_MOVE": overall == "NO-MOVE",
            "is_UNDECIDED": overall == "UNDECIDED",
            "not_BROKEN": overall != "BROKEN",
        },
    }


def main():
    sweep_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CONE, "SWEEP_probe_A_v3.json")
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(CONE, "RESULT_PROBE_A.json")
    sweep = json.load(open(sweep_path))
    # exclude non_result dry-check rows from grading set (already filtered)
    graded = grade_sweep(sweep)
    result = {
        "tool": "grade_probe_a_v3.py",
        "sweep_path": os.path.abspath(sweep_path),
        "sweep_sha8": sha256_file(sweep_path)[:8],
        "solves": [
            {
                "b": r.get("b"),
                "N": r.get("N"),
                "n": r.get("n"),
                "npz": r.get("npz"),
                "npz_sha8": r.get("npz_sha8"),
                "non_result": r.get("non_result", False),
                "converged": (r.get("convergence") or {}).get("converged"),
                "residual_inf": (r.get("convergence") or {}).get("residual_inf"),
                "rank_N": (r.get("projector") or {}).get("rank_N"),
                "rank_S": (r.get("projector") or {}).get("rank_S"),
                "eigenvalues_PhiPhiT": (r.get("projector") or {}).get("eigenvalues_PhiPhiT"),
                "Q_total": (r.get("flux") or {}).get("Q_total"),
                "Q_cap_N": (r.get("flux") or {}).get("Q_cap_N"),
                "Q_cap_S": (r.get("flux") or {}).get("Q_cap_S"),
                "Q_cap_rc_rho": Q_CAP_RC,
                "abs_Q_minus_4": (r.get("flux") or {}).get("abs_Q_minus_4"),
                "Q_flag": (r.get("flux") or {}).get("Q_flag_between_1e-2_and_3e-2"),
                "r_peak_N": (r.get("ring") or {}).get("north", {}).get("r_peak"),
                "r_peak_S": (r.get("ring") or {}).get("south", {}).get("r_peak"),
                "r_peak_core_N": (r.get("ring") or {}).get("north", {}).get("r_peak_core"),
                "r_peak_core_S": (r.get("ring") or {}).get("south", {}).get("r_peak_core"),
                "r_sub3_N": (r.get("ring") or {}).get("north", {}).get("r_sub3"),
                "r_sub5_N": (r.get("ring") or {}).get("north", {}).get("r_sub5"),
                "f_N": (r.get("ring") or {}).get("north", {}).get("f"),
                "f_S": (r.get("ring") or {}).get("south", {}).get("f"),
                "solve_sec": r.get("solve_sec"),
                "timestamp_uk": r.get("timestamp_uk"),
            }
            for r in sweep.get("rows", [])
        ],
        **graded,
    }

    # RULES for grade_result: structural + charge/rank; verdict booleans
    rules = {
        "spec": "Probe A v3 freeze 6e0f1942 + addendum 61f39a62",
        "pass": [
            ["summary.all_rank_equals_2", "==", True],
            ["summary.max_abs_Q_minus_4", "abs<=", [0.0, 0.03]],
            ["summary.not_BROKEN", "==", True],
        ],
        "fail": [
            ["summary.is_BROKEN", "==", True],
        ],
    }
    rules_path = os.path.join(CONE, "RULES_PROBE_A_V3.json")
    json.dump(rules, open(rules_path, "w"), indent=2)

    json.dump(result, open(out_path, "w"), indent=2)
    # call grade_result
    grader = os.path.join(HERE, "grade_result.py")
    proc = subprocess.run(
        [sys.executable, grader, rules_path, out_path],
        capture_output=True,
        text=True,
    )
    line = (proc.stdout or "").strip() or (proc.stderr or "").strip()
    result["grade_result_line"] = line
    result["rules_path"] = rules_path
    result["rules_sha8"] = sha256_file(rules_path)[:8]
    json.dump(result, open(out_path, "w"), indent=2)
    print(json.dumps({
        "out": out_path,
        "sha8": sha256_file(out_path)[:8],
        "verdict": result["verdict"],
        "per_b": [(e["b"], e.get("verdict")) for e in result["per_b"]],
        "grade_result_line": line,
        "Q_flags": result["Q_flags_1e-2_to_3e-2"],
        "timestamp_uk": result["timestamp_uk"],
    }, indent=2))


if __name__ == "__main__":
    main()

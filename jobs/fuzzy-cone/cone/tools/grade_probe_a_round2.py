#!/usr/bin/env python3
"""Grade Probe A round-2 diagnostic (1202fa35). Does NOT regrade Probe A."""
from __future__ import annotations
import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
CONE = os.path.abspath(os.path.join(HERE, "..", "fuzz", "cone"))
sys.path.insert(0, HERE)
from ring_projector import sha256_file, uk_now, Q_CAP_RC


def grade(sweep: dict) -> dict:
    rows = [r for r in sweep.get("rows", []) if r.get("status") == "ok" and not r.get("non_result")]
    n_conv = sum(1 for r in rows if r.get("convergence", {}).get("converged"))
    n_total = len(rows)
    absQs = [float(r["flux"]["abs_Q_minus_4"]) for r in rows]
    worst = max(absQs) if absQs else None
    all_conv = n_conv == n_total and n_total == 12

    if not all_conv:
        verdict = "UNDECIDED"
        reason = f"non-converged solves: {n_total - n_conv}/{n_total}"
    elif worst is not None and worst < 1e-2:
        verdict = "CONVERGENCE"
        reason = "all converged and worst |Q-4| < 1e-2; round-1 drift was under-convergence"
    elif worst is not None and worst > 3e-2:
        verdict = "FLUX-NOT-QUANTISED"
        reason = "all converged and worst |Q-4| > 3e-2; fuzzy flux sum not pinned near criticality"
    else:
        verdict = "INTERMEDIATE"
        reason = (
            f"all converged but 1e-2 <= worst |Q-4|={worst:.4g} <= 3e-2 "
            "(addendum buckets this under UNDECIDED/anything else)"
        )

    solves = []
    for r in rows:
        solves.append({
            "b": r.get("b"),
            "N": r.get("N"),
            "n": r.get("n"),
            "npz": r.get("npz"),
            "npz_sha8": r.get("npz_sha8"),
            "converged": r["convergence"]["converged"],
            "residual_inf": r["convergence"]["residual_inf"],
            "nit": (r.get("params") or {}).get("nit"),
            "solver_message": r.get("solver_message"),
            "solver_gtol": r.get("solver_gtol"),
            "solver_ftol": r.get("solver_ftol"),
            "solver_maxiter": r.get("solver_maxiter"),
            "rank_N": r["projector"]["rank_N"],
            "rank_S": r["projector"]["rank_S"],
            "ev_proj_N": r["projector"].get("ev_proj_N"),
            "ev_proj_S": r["projector"].get("ev_proj_S"),
            "eigenvalues_pole_projector_N": r["projector"].get("eigenvalues_pole_projector_N"),
            "eigenvalues_pole_projector_S": r["projector"].get("eigenvalues_pole_projector_S"),
            "Q_total": r["flux"]["Q_total"],
            "abs_Q_minus_4": r["flux"]["abs_Q_minus_4"],
            "Q_cap_N": r["flux"]["Q_cap_N"],
            "Q_cap_S": r["flux"]["Q_cap_S"],
            "Q_cap_rc_rho": Q_CAP_RC,
            "r_peak_N": r["ring"]["north"]["r_peak"],
            "r_peak_S": r["ring"]["south"]["r_peak"],
            "f_N": r["ring"]["north"]["f"],
            "f_S": r["ring"]["south"]["f"],
            "solve_sec": r.get("solve_sec"),
            "timestamp_uk": r.get("timestamp_uk"),
        })

    from collections import defaultdict
    by_b = defaultdict(dict)
    for r in rows:
        by_b[float(r["b"])][int(r["N"])] = r
    ring_outputs = []
    for b in sorted(by_b):
        blk = by_b[b]
        if set(blk) != {41, 61, 81}:
            continue
        ring_outputs.append({
            "b": b,
            "r41_N": blk[41]["ring"]["north"]["r_peak"],
            "r61_N": blk[61]["ring"]["north"]["r_peak"],
            "r81_N": blk[81]["ring"]["north"]["r_peak"],
            "delta_N": blk[81]["ring"]["north"]["r_peak"] - blk[41]["ring"]["north"]["r_peak"],
            "delta_S": blk[81]["ring"]["south"]["r_peak"] - blk[41]["ring"]["south"]["r_peak"],
            "note": "output only; not graded in round-2 diagnostic",
        })

    return {
        "timestamp_uk": uk_now(),
        "diagnostic": True,
        "probe_A_stands": {"path": "RESULT_PROBE_A.json", "sha8": "07d1e838", "verdict": "BROKEN"},
        "round2_sha8": "1202fa35",
        "spec_sha8": "8d7f5092",
        "freeze_sha8": "6e0f1942",
        "addendum1_sha8": "61f39a62",
        "code_sha8": "63b69fbc",
        "grader_sha8": "c188ec50",
        "Q_cap_rc_rho": Q_CAP_RC,
        "n_solves": n_total,
        "n_converged": n_conv,
        "worst_abs_Q_minus_4": worst,
        "verdict": verdict,
        "reason": reason,
        "summary": {
            "all_converged": all_conv,
            "worst_abs_Q_minus_4": worst,
            "is_CONVERGENCE": verdict == "CONVERGENCE",
            "is_FLUX_NOT_QUANTISED": verdict == "FLUX-NOT-QUANTISED",
            "is_INTERMEDIATE": verdict == "INTERMEDIATE",
            "is_UNDECIDED": verdict == "UNDECIDED",
        },
        "ring_shift_output_only": ring_outputs,
        "solves": solves,
    }


def main():
    sweep_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CONE, "SWEEP_probe_A_round2.json")
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(CONE, "RESULT_PROBE_A_ROUND2_DIAG.json")
    sweep = json.load(open(sweep_path))
    result = {
        "tool": "grade_probe_a_round2.py",
        "sweep_path": os.path.abspath(sweep_path),
        "sweep_sha8": sha256_file(sweep_path)[:8],
        **grade(sweep),
    }
    rules = {
        "spec": "PROBE_A_ROUND2_DIAG_ADDENDUM 1202fa35",
        "pass": [["summary.all_converged", "==", True]],
        "fail": [["summary.all_converged", "==", False]],
    }
    rules_path = os.path.join(CONE, "RULES_PROBE_A_ROUND2_DIAG.json")
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
        "worst_abs_Q_minus_4": result["worst_abs_Q_minus_4"],
        "n_converged": result["n_converged"],
        "n_solves": result["n_solves"],
        "grade_result_line": line,
        "timestamp_uk": result["timestamp_uk"],
    }, indent=2))


if __name__ == "__main__":
    main()

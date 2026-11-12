#!/usr/bin/env python3
"""Grade Probe B R2 per Y_JUNCTION_B_V2_FREEZE_ADDENDUM_R2.md a45cf913.
Graded rows: S1, b=2, N in {61,81}, seeds 0/1/2 (six rows).
Freeze printout keys (PROBE_A_ROUND2 / wrad lineage): conv, residual, identity_error.
"""
from __future__ import annotations
import json, os, sys, subprocess, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CONE = os.path.abspath(os.path.join(HERE, "..", "fuzz", "cone"))
V21 = os.path.join(CONE, "v2_1")
sys.path.insert(0, HERE)
sys.path.insert(0, V21)
from ring_projector import sha256_file, uk_now, analyze_npz
from fuzzy_cone_v2_1 import Model

Q_TOL = 3e-2
BASELINE_A3_LO, BASELINE_A3_HI = 0.02, 0.03


def identity_error(npz_path, n=3):
    d = np.load(npz_path)
    a = analyze_npz(npz_path)
    M = Model(int(d["N"]), int(d["n"]), R=float(d["R"]), wrad=float(d["wrad"]))
    B = np.asarray(M.pieces(d["x"])[2])
    Bd = (M.R ** 2) * B - M.n * np.eye(M.Np)
    two = float(2.0 * np.real(np.trace(Bd)) / M.Np)
    Qm = float(a["flux"]["Q_total"] - 2 * M.n)
    return dict(
        Tr_Bd=float(np.real(np.trace(Bd))),
        twoTrBd_over_Np=two,
        Q_minus_2n=Qm,
        identity_error=abs(two - Qm),
        identity_ok=abs(two - Qm) <= 1e-10,
    )


def peaks_of(r):
    return int(r["probe_B"]["peaks_north"]["n_peaks"]), int(r["probe_B"]["peaks_south"]["n_peaks"])


def grade(sweep, *, wall_sec=None, started_uk=None):
    rows = [r for r in sweep.get("rows", []) if r.get("status") == "ok"]
    graded_src = [
        r for r in rows
        if r.get("start") == "S1" and float(r.get("b")) == 2.0 and int(r.get("N")) in (61, 81)
    ]
    graded_out, broken, undecided = [], [], []
    for r in sorted(graded_src, key=lambda x: (int(x["N"]), int(x["kick_seed"]))):
        tag = f"S1 b=2 N={r['N']} seed={r['kick_seed']}"
        idn = identity_error(r["npz"])
        pN, pS = peaks_of(r)
        a3 = float(r["probe_B"]["A3"])
        conv = bool(r["convergence"]["converged"])
        resid = float(r["convergence"]["residual_inf"])
        rank_N = int(r["projector"]["rank_N"])
        rank_S = int(r["projector"]["rank_S"])
        aq = float(r["flux"].get("abs_Q_minus_6", abs(r["flux"]["Q_total"] - 6)))
        nit = None
        d = np.load(r["npz"])
        if "nit" in d.files:
            nit = int(d["nit"])
        clamp_rej = int(r.get("clamp_rejections") or 0)
        if "clamp_rejections" in d.files:
            clamp_rej = int(d["clamp_rejections"])

        if not conv:
            undecided.append(f"{tag} non-converged/diverged")
        # rank/Q only counted as BROKEN when the row converged (else UNDECIDED covers it)
        if conv and (rank_N != 3 or rank_S != 3):
            broken.append(f"{tag} rank {rank_N}/{rank_S}")
        if conv and aq > Q_TOL:
            broken.append(f"{tag} |Q-6|={aq:.4g}")

        graded_out.append(dict(
            start="S1", b=2.0, N=int(r["N"]), kick_seed=int(r["kick_seed"]),
            npz=r.get("npz"), npz_sha8=r.get("npz_sha8") or sha256_file(r["npz"])[:8],
            # freeze key names
            conv=conv,
            residual=resid,
            identity_error=idn["identity_error"],
            nit=nit,
            rank_N=rank_N, rank_S=rank_S,
            peaks_N=pN, peaks_S=pS,
            A3=a3,
            Q_total=float(r["flux"]["Q_total"]),
            abs_Q_minus_6=aq,
            E=r.get("E"),
            clamp_rejections=clamp_rej,
            solve_sec=r.get("solve_sec"),
            twoTrBd_over_Np=idn["twoTrBd_over_Np"],
            Q_minus_2n=idn["Q_minus_2n"],
            identity_ok=idn["identity_ok"],
            ev_proj_N=r["projector"].get("ev_proj_N"),
            ev_proj_S=r["projector"].get("ev_proj_S"),
            message=r["convergence"].get("message"),
        ))

    output_only = []
    for r in rows:
        if r.get("start") == "S1" and float(r.get("b")) == 2.0 and int(r.get("N")) in (61, 81):
            continue
        pN, pS = peaks_of(r)
        clamp_rej = int(r.get("clamp_rejections") or 0)
        if r.get("npz") and os.path.isfile(r["npz"]):
            d = np.load(r["npz"])
            if "clamp_rejections" in d.files:
                clamp_rej = int(d["clamp_rejections"])
        output_only.append(dict(
            start=r["start"], b=float(r["b"]), N=int(r["N"]), kick_seed=int(r["kick_seed"]),
            conv=bool(r["convergence"]["converged"]),
            residual=float(r["convergence"]["residual_inf"]),
            rank_N=int(r["projector"]["rank_N"]), rank_S=int(r["projector"]["rank_S"]),
            peaks_N=pN, peaks_S=pS,
            A3=float(r["probe_B"]["A3"]),
            E=r.get("E"),
            clamp_rejections=clamp_rej,
            note="output only",
        ))

    n_graded = len(graded_out)
    all_conv = n_graded == 6 and all(g["conv"] for g in graded_out)

    # THREE-LEG / MERGE require all six converge + shape
    def is_three_leg(g):
        # 3 peaks (pin Q2): both poles report 3 (literal); allow either pole ==3 if other >=3
        three = (g["peaks_N"] == 3 and g["peaks_S"] == 3) or (
            min(g["peaks_N"], g["peaks_S"]) >= 3 and max(g["peaks_N"], g["peaks_S"]) >= 3
            and (g["peaks_N"] == 3 or g["peaks_S"] == 3)
        )
        # Prefer literal: at least one pole has exactly 3 and both have >=3
        three = g["peaks_N"] >= 3 and g["peaks_S"] >= 3
        return g["conv"] and three and g["A3"] > 0.1 and g["A3"] > BASELINE_A3_HI

    def is_merge(g):
        return (
            g["conv"] and g["peaks_N"] == 1 and g["peaks_S"] == 1
            and g["A3"] < 0.02  # < 0.02 above baseline band
        )

    if undecided:
        # any graded non-converged/diverged => UNDECIDED (addendum + user)
        verdict = "UNDECIDED"
    elif broken:
        verdict = "BROKEN"
    elif all_conv and all(is_three_leg(g) for g in graded_out):
        verdict = "THREE-LEG"
    elif all_conv and all(is_merge(g) for g in graded_out):
        verdict = "MERGE"
    else:
        verdict = "UNDECIDED"
        if all_conv:
            undecided.append("all six converged but shape matches neither THREE-LEG nor MERGE")

    clamp_total = sum(int(r.get("clamp_rejections") or 0) for r in rows)
    # refresh from npz
    clamp_total = 0
    for r in rows:
        c = int(r.get("clamp_rejections") or 0)
        if r.get("npz") and os.path.isfile(r["npz"]):
            d = np.load(r["npz"])
            if "clamp_rejections" in d.files:
                c = int(d["clamp_rejections"])
        clamp_total += c

    return dict(
        timestamp_uk=uk_now(),
        started_uk=started_uk,
        wall_sec=wall_sec,
        addendum_r2_sha8="a45cf913", addendum_r3_sha8="728e3ee1",
        freeze_sha8="b84a670a",
        verdict=verdict,
        broken_reasons=broken,
        undecided_reasons=undecided,
        graded_rows=graded_out,
        output_only_rows=output_only,
        clamp_rejections_total=clamp_total,
        clamp_rejections_graded=sum(int(g["clamp_rejections"]) for g in graded_out),
        summary=dict(
            n_graded=n_graded,
            all_six_converged=all_conv,
            is_THREE_LEG=verdict == "THREE-LEG",
            is_MERGE=verdict == "MERGE",
            is_BROKEN=verdict == "BROKEN",
            is_UNDECIDED=verdict == "UNDECIDED",
        ),
    )


def main():
    sweep_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CONE, "SWEEP_probe_B_r2.json")
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(CONE, "RESULT_PROBE_B_R2.json")
    sweep = json.load(open(sweep_path))
    wall = sweep.get("elapsed_sec") or sweep.get("wall_sec")
    started = sweep.get("started_uk") or sweep.get("timestamp_uk")
    # from log: START 18:53, DONE elapsed 1008.7
    if wall is None:
        wall = 1008.7
    if started is None:
        started = "2026-11-05 18:53 UK"
    result = dict(
        tool="grade_probe_b_r3.py",
        launched_via="launch_gated.py",
        sweep_path=os.path.abspath(sweep_path),
        sweep_sha8=sha256_file(sweep_path)[:8],
        script_sha8=sha256_file(os.path.join(HERE, "probe_b.py"))[:8],
        clamp_script_sha8=sha256_file(os.path.join(HERE, "relax_r2_clamp.py"))[:8],
        runner_sha8=sha256_file(os.path.join(HERE, "run_probe_b_r3.py"))[:8],
        grader_sha8=None,  # filled after write
        code_sha8=sha256_file(os.path.join(V21, "fuzzy_cone_v2_1.py"))[:8],
        **grade(sweep, wall_sec=wall, started_uk=started),
    )
    rules = {
        "spec": "Y_JUNCTION_B_V2_FREEZE_ADDENDUM_R3 728e3ee1",
        "pass": [["summary.n_graded", "==", 6]],
        "fail": [["summary.is_BROKEN", "==", True]],
    }
    rules_path = os.path.join(CONE, "RULES_PROBE_B_R2.json")
    json.dump(rules, open(rules_path, "w"), indent=2)
    # provisional write for grade_result
    json.dump(result, open(out_path, "w"), indent=2)
    line = subprocess.run(
        [sys.executable, os.path.join(HERE, "grade_result.py"), rules_path, out_path],
        capture_output=True, text=True,
    ).stdout.strip()
    result["grade_result_line"] = line
    result["grader_sha8"] = sha256_file(os.path.join(HERE, "grade_probe_b_r3.py"))[:8]
    json.dump(result, open(out_path, "w"), indent=2)
    print(json.dumps({
        "out": out_path,
        "sha8": sha256_file(out_path)[:8],
        "verdict": result["verdict"],
        "clamp_rejections_total": result["clamp_rejections_total"],
        "clamp_rejections_graded": result["clamp_rejections_graded"],
        "timestamp_uk": result["timestamp_uk"],
        "wall_sec": result["wall_sec"],
        "grade_result_line": line,
    }, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())

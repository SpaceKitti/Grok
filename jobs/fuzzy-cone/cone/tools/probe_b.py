#!/usr/bin/env python3
"""Probe B (Y-junction / three-mode ring) tooling.

Frozen: Y_JUNCTION_SPEC_B_DRAFT_V2.md 8a0ca930 + Y_JUNCTION_B_V2_FREEZE.md
(b84a670a). Convergence/printout as PROBE_A_ROUND2_DIAG_ADDENDUM 1202fa35.
Same Q-cap rc=1.5 rho and |Q-6|<=3e-2 (charge BROKEN above 3e-2).
Uses relax_round2 R2 (maxiter x10, tol 100x tighter than round 1).
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V21 = os.path.abspath(os.path.join(HERE, "..", "fuzz", "cone", "v2_1"))
CONE = os.path.abspath(os.path.join(HERE, "..", "fuzz", "cone"))
sys.path.insert(0, HERE)
sys.path.insert(0, V21)

from ring_projector import (  # noqa: E402
    analyze_npz,
    sha256_file,
    uk_now,
    Q_CAP_RC,
    residual_inf,
)
from relax_round2 import relax_r2, R2  # noqa: E402
from relax_r2_clamp import relax_r2_clamped  # noqa: E402
from fuzzy_cone_v2_1 import Model, symbol_diag  # noqa: E402

UK = timezone(timedelta(hours=0), name="Europe/London")
KICK_AMP = 1e-3
Q_TOL = 3e-2  # freeze Q3 / same as Probe A addendum 1 scale for n=3 -> |Q-6|
RANK_EXPECT = 3


def seed_S1(M: Model) -> np.ndarray:
    """Axisymmetric coincident n=3 start (frozen seed_fuzzy)."""
    return M.seed_fuzzy()


def seed_S2(M: Model, theta0: float | None = None, amp: float = 0.35) -> np.ndarray:
    """Three unit strings spaced 120°: ΔL3=±3 content in Φ (frozen formulas only).

    Start from the isometric m→m embedding, then add a C3-breaking admixture on
    the Φ matrix elements with mp − m = ±3, weighted toward the poles.
    """
    Np, N = M.Np, M.N
    P = np.zeros((Np, N), complex)
    # axisymmetric block
    P[M.n : M.n + N, :] = np.eye(N)
    # ΔL3 = ±3 couplings
    mp = np.asarray(M.mp, float)
    m = np.asarray(M.m, float)
    # pole weight: larger |m| (near poles of the smaller spin)
    w = (np.abs(m) / (np.max(np.abs(m)) + 1e-12)) ** 2
    for i, mpi in enumerate(mp):
        for j, mj in enumerate(m):
            dm = mpi - mj
            if abs(abs(dm) - 3.0) < 1e-9:
                # 120° structure: complex phase from azimuthal C3
                # use column phase factors e^{i 2π k/3} encoded as relative i-phase
                P[i, j] += amp * w[j] * (1.0 if dm > 0 else 1.0j)
    # pack into x (X fluctuations zero): real then imag of Phi, matching Model.unpack
    return np.concatenate([np.zeros(M.nX()), np.real(P).ravel(), np.imag(P).ravel()])


def kick(x: np.ndarray, seed: int, amp: float = KICK_AMP) -> np.ndarray:
    rng = np.random.default_rng(int(seed))
    return np.asarray(x, float) + amp * rng.normal(size=np.asarray(x).shape)


def energy_density_matrix(M: Model, x: np.ndarray) -> np.ndarray:
    """Matrix whose L3-basis diagonal is the energy density (B^2/2 + potential).

    A3 uses the |ΔL3|=3 off-diagonal block of this matrix (spec v2).
    """
    X, P, B, K, rad = (
        np.asarray(v) if not isinstance(v, list) else [np.asarray(u) for u in v]
        for v in M.pieces(x)
    )
    # On V_j': B^2/2
    EB = 0.5 * (B @ B)
    # Potential lives on V_j; lift a diagonal contribution via Phi: Phi (1-Phi†Phi)^2 Phi† / 8
    V = np.eye(M.N) - P.conj().T @ P
    pot_j = 0.125 * (V @ V)
    pot_lift = P @ pot_j @ P.conj().T
    return EB + pot_lift


def A3_measure(M: Model, x: np.ndarray) -> float:
    """Frobenius(|ΔL3|=3 block) / Frobenius(diagonal block) of energy-density matrix."""
    Emat = energy_density_matrix(M, x)
    # L3 eigenbasis is the computational basis for X=L' seed; after relax use eigh(X3)
    X = [np.asarray(u) for u in M.unpack(x)[0]]
    w3, U3 = np.linalg.eigh(X[2])
    Em = U3.conj().T @ Emat @ U3
    # assign integer L3 labels by sorting (already eigh ascending)
    # Δ index = 3 in the sorted m basis ≈ 3 steps in the Np grid of spin-j'
    # Use actual mp differences from Model
    mp = np.asarray(M.mp, float)  # j'..-j' order of background; X3 evecs may reorder
    # Better: label columns by eigenvalue of X3 / (approx)
    # For round fuzzy, X3 ≈ L3, eigenvalues ≈ mp. Match each evec to nearest mp.
    labels = []
    for w in w3:
        labels.append(mp[int(np.argmin(np.abs(mp - np.real(w))))])
    labels = np.asarray(labels, float)
    diag = 0.0
    off3 = 0.0
    for i in range(M.Np):
        for j in range(M.Np):
            dm = abs(labels[i] - labels[j])
            val = abs(Em[i, j]) ** 2
            if i == j:
                diag += val
            elif abs(dm - 3.0) < 0.6:  # allow soft match after relax
                off3 += val
    diag = np.sqrt(diag)
    off3 = np.sqrt(off3)
    return float(off3 / diag) if diag > 0 else float("nan")


def coherent_symbol_grid(M: Model, A: np.ndarray, ntheta=64, nphi=64):
    """Spin-j' coherent-state symbol of Hermitian A on a (θ,φ) grid."""
    # extend symbol_diag (phi=0) by rotating with e^{-i φ L3}
    th = np.linspace(0, np.pi, ntheta)
    phi = np.linspace(0, 2 * np.pi, nphi, endpoint=False)
    # For each phi, A_phi = e^{i φ X3} wait: rotate state. Equivalent: A -> U A U† with U=e^{-iφ L3}
    # Using background Lp[2]
    L3 = np.asarray(M.Lp[2])
    out = np.zeros((ntheta, nphi))
    for k, ph in enumerate(phi):
        U = np.diag(np.exp(-1j * ph * np.asarray(M.mp)))  # e^{-i φ L3} in m-basis
        Ap = U @ A @ U.conj().T
        # symbol_diag expects matrix in m=j'..-j' basis — Ap is that if A was
        # After relax A is in X-evolved frame; use U3 to map to approx L3 basis first.
        out[:, k] = symbol_diag(M, Ap, th)
    return th, phi, out


def peak_count_cap(M: Model, x: np.ndarray, pole="north", ngrid=64, frac=0.5) -> dict:
    """Count local maxima of coherent-state energy symbol on a 64x64 cap grid.

    Freeze Q2: peaks above 50% of the cap maximum. Cap = hemisphere toward pole.
    """
    Emat = energy_density_matrix(M, x)
    # put Emat in approximate L3/m basis via X3 evecs
    X = [np.asarray(u) for u in M.unpack(x)[0]]
    w3, U3 = np.linalg.eigh(X[2])
    Em = U3.conj().T @ Emat @ U3
    # reorder Em to Model.mp order roughly by matching eigenvalues to mp
    order = np.argsort(-np.real(w3))  # high x3 first ~ north
    Em = Em[np.ix_(order, order)]
    th, phi, Z = coherent_symbol_grid(M, Em, ntheta=ngrid, nphi=ngrid)
    if pole == "north":
        mask_th = th <= (np.pi / 2)
    else:
        mask_th = th >= (np.pi / 2)
    cap = Z[mask_th, :]
    if cap.size == 0:
        return dict(n_peaks=0, cap_max=0.0, peak_locs=[])
    cap_max = float(np.max(cap))
    thr = frac * cap_max
    # local maxima on periodic-phi grid
    peaks = []
    nt, np_ = cap.shape
    for i in range(nt):
        for j in range(np_):
            v = cap[i, j]
            if v < thr:
                continue
            nbrs = [
                cap[i2 % nt if False else max(0, min(nt - 1, i2)), j2 % np_]
                for i2 in (i - 1, i, i + 1)
                for j2 in (j - 1, j, j + 1)
                if not (i2 == i and j2 == j)
            ]
            # fix i neighbors without wrap on theta
            vals = []
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ii = i + di
                    if ii < 0 or ii >= nt:
                        continue
                    vals.append(cap[ii, (j + dj) % np_])
            if vals and v >= max(vals) - 1e-15:
                th_cap = th[mask_th][i]
                peaks.append(dict(theta=float(th_cap), phi=float(phi[j]), val=float(v)))
    # de-duplicate adjacent peaks (simple angular merge)
    peaks.sort(key=lambda p: -p["val"])
    kept = []
    for p in peaks:
        if all(
            (abs(p["theta"] - q["theta"]) > 0.15 or abs(((p["phi"] - q["phi"] + np.pi) % (2 * np.pi)) - np.pi) > 0.3)
            for q in kept
        ):
            kept.append(p)
    return dict(n_peaks=len(kept), cap_max=cap_max, peak_locs=kept, threshold=thr)


def jobs_B(cfg: dict):
    """36 jobs: S1/S2 × b ∈ {2,1.2,1.05} × N ∈ {61,81} × seeds {0,1,2}."""
    n = int(cfg.get("n", 3))
    bs = cfg.get("b_values", [2.0, 1.2, 1.05])
    Ns = cfg.get("N_values", [61, 81])
    starts = cfg.get("starts", ["S1", "S2"])
    seeds = cfg.get("kick_seeds", [0, 1, 2])
    wrad = float(cfg.get("wrad", 1000.0))
    out_dir = cfg.get("out_dir", V21)
    jobs = []
    for start in starts:
        for b in bs:
            for N in Ns:
                for seed in seeds:
                    R = float(np.sqrt(2.0 * n * b))
                    prefix = cfg.get("npz_prefix", "sol_probeB")
                    fname = f"{prefix}_{start}_b{b:g}_n{n}_N{N}_seed{seed}.npz"
                    jobs.append(dict(
                        start=start, b=float(b), N=int(N), n=n, R=R, wrad=wrad,
                        kick_seed=int(seed), npz=os.path.join(out_dir, fname),
                        step_clamp=bool(cfg.get("step_clamp", False)),
                    ))
    return jobs


def solve_B_job(job, *, overwrite=False):
    from fuzzy_cone_v2_1 import Model
    n, b, N = job["n"], job["b"], job["N"]
    R = float(np.sqrt(2.0 * n * b))
    theta = float(2.0 * R * R / np.sqrt(N * N - 1.0))
    out = job["npz"]
    if os.path.exists(out) and not overwrite:
        prev = np.load(out)
        if not (bool(prev["non_result"]) if "non_result" in prev.files else False):
            return out, None, True
    M = Model(int(N), int(n), R=R, wrad=float(job["wrad"]))
    x0 = seed_S1(M) if job["start"] == "S1" else seed_S2(M)
    x0 = kick(x0, job["kick_seed"])
    t0 = time.time()
    use_clamp = bool(job.get("step_clamp", False))
    if use_clamp:
        x, E, ok, it, resid, msg, n_rej = relax_r2_clamped(M, x0)
    else:
        x, E, ok, it, resid, msg = relax_r2(M, x0)
        n_rej = 0
    solve_sec = round(time.time() - t0, 3)
    B = np.asarray(M.pieces(x)[2])
    meta = dict(
        x=x, B=B, theta=theta, N=int(N), n=int(n), R=R, b=float(b),
        wrad=float(job["wrad"]), E=E, conv=bool(ok), nit=int(it),
        residual=float(resid), non_result=False, gtol=R2["gtol"], ftol=R2["ftol"],
        maxiter=R2["maxiter"], maxfun=R2["maxfun"],
        profile="r2_clamp" if use_clamp else "r2",
        seed_name=job["start"], kick_seed=int(job["kick_seed"]), message=str(msg),
        clamp_rejections=int(n_rej),
    )
    np.savez_compressed(out, **meta)
    return out, solve_sec, False, int(n_rej)


def analyse_B(npz_path: str) -> dict:
    """ring_projector readout + A3 + peak counts (Probe B)."""
    base = analyze_npz(npz_path)
    d = np.load(npz_path)
    M = Model(int(d["N"]), int(d["n"]), R=float(d["R"]), wrad=float(d["wrad"]))
    a3 = A3_measure(M, d["x"])
    peaks_N = peak_count_cap(M, d["x"], "north")
    peaks_S = peak_count_cap(M, d["x"], "south")
    base["probe_B"] = {
        "A3": a3,
        "peaks_north": peaks_N,
        "peaks_south": peaks_S,
        "start": str(d["seed_name"]) if "seed_name" in d.files else None,
        "kick_seed": int(d["kick_seed"]) if "kick_seed" in d.files else None,
        "Q_tol": Q_TOL,
        "rank_expect": RANK_EXPECT,
        "Q_target": 2 * int(d["n"]),
    }
    # n=3 charge fields
    base["flux"]["abs_Q_minus_6"] = float(abs(base["flux"]["Q_total"] - 6.0))
    base["flux"]["Q_broken_gt_3e-2"] = bool(base["flux"]["abs_Q_minus_6"] > Q_TOL)
    base["flux"]["Q_flag_between_1e-2_and_3e-2"] = bool(
        1e-2 < base["flux"]["abs_Q_minus_6"] <= Q_TOL
    )
    return base


def run_probe_B(cfg: dict, *, force=False, dry_run=False, only_first=False) -> dict:
    jobs = jobs_B(cfg)
    if only_first:
        jobs = jobs[:1]
    out_path = cfg.get("sweep_out", os.path.join(CONE, "SWEEP_probe_B.json"))
    table = {
        "tool": "probe_b.py",
        "name": cfg.get("name", "probe_B_v2"),
        "config": cfg,
        "created_uk": uk_now(),
        "rows": [],
        "Q_cap_rc_rho": Q_CAP_RC,
        "Q_tol": Q_TOL,
        "profile": "r2",
        "round2_sha8": "1202fa35",
        "spec_sha8": "8a0ca930",
        "freeze_sha8": cfg.get("freeze_sha8", "b84a670a"),
    }
    if os.path.exists(out_path) and not force:
        table = json.load(open(out_path))
    budget = float(cfg.get("budget_sec", 7200))
    t0 = time.time()
    done = {(r.get("start"), r.get("b"), r.get("N"), r.get("kick_seed"))
            for r in table.get("rows", []) if r.get("status") == "ok"}
    for job in jobs:
        if time.time() - t0 > budget:
            table.setdefault("notes", []).append("budget stop")
            break
        key = (job["start"], job["b"], job["N"], job["kick_seed"])
        if key in done and not force:
            print(f"skip {key}")
            continue
        if dry_run:
            print(f"DRY {key} -> {job['npz']}")
            continue
        try:
            ret = solve_B_job(job, overwrite=force)
            if len(ret) == 4:
                npz, solve_sec, reused, n_rej = ret
            else:
                npz, solve_sec, reused = ret; n_rej = 0
            analysis = analyse_B(npz)
            row = {
                "status": "ok",
                "start": job["start"],
                "b": job["b"],
                "N": job["N"],
                "n": job["n"],
                "kick_seed": job["kick_seed"],
                "npz": npz,
                "npz_sha8": sha256_file(npz)[:8],
                "solve_sec": solve_sec,
                "reused_npz": reused,
                "clamp_rejections": int(n_rej),
                "convergence": analysis["convergence"],
                "projector": {
                    "rank_N": analysis["projector"]["rank_N"],
                    "rank_S": analysis["projector"]["rank_S"],
                    "ev_proj_N": analysis["projector"]["ev_proj_N"],
                    "ev_proj_S": analysis["projector"]["ev_proj_S"],
                    "rank_equals_3": bool(
                        analysis["projector"]["rank_N"] == 3
                        and analysis["projector"]["rank_S"] == 3
                    ),
                },
                "flux": analysis["flux"],
                "E": analysis["params"]["E"],
                "probe_B": analysis["probe_B"],
                "ring": {
                    "r_peak_N": analysis["ring"]["north"]["r_peak"],
                    "r_peak_S": analysis["ring"]["south"]["r_peak"],
                    "f_N": analysis["ring"]["north"]["f"],
                    "f_S": analysis["ring"]["south"]["f"],
                },
                "timestamp_uk": uk_now(),
            }
            # replace prior
            table["rows"] = [
                r for r in table["rows"]
                if not (r.get("start")==job["start"] and r.get("b")==job["b"]
                        and r.get("N")==job["N"] and r.get("kick_seed")==job["kick_seed"])
            ]
            table["rows"].append(row)
            print(
                f"ok {job['start']} b={job['b']} N={job['N']} seed={job['kick_seed']} "
                f"conv={row['convergence']['converged']} rank={row['projector']['rank_N']}/{row['projector']['rank_S']} "
                f"Q={row['flux']['Q_total']:.4f} A3={row['probe_B']['A3']:.4g} "
                f"peaks={row['probe_B']['peaks_north']['n_peaks']}/{row['probe_B']['peaks_south']['n_peaks']} "
                f"evN={row['projector']['ev_proj_N']} evS={row['projector']['ev_proj_S']} "
                f"solve_s={solve_sec}",
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            table["rows"].append(dict(status="error", **{k: job[k] for k in
                ("start","b","N","n","kick_seed","npz")}, error=repr(exc), timestamp_uk=uk_now()))
            print(f"error {key}: {exc!r}", file=sys.stderr)
    table["elapsed_sec"] = round(time.time() - t0, 3)
    table["n_jobs"] = len(jobs_B(cfg))
    table["n_rows_ok"] = sum(1 for r in table["rows"] if r.get("status") == "ok")
    table["updated_uk"] = uk_now()
    if not dry_run:
        json.dump(table, open(out_path, "w"), indent=2)
        table["sha8"] = sha256_file(out_path)[:8]
        json.dump(table, open(out_path, "w"), indent=2)
        print(f"# wrote {out_path} sha8={table['sha8']}", file=sys.stderr)
    return table


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", default=os.path.join(CONE, "SWEEP_PROBE_B_CONFIG.json"))
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--only-first", action="store_true")
    p.add_argument("--smoke-seed", action="store_true", help="build S1/S2+kick only, no solve")
    args = p.parse_args(argv)
    if args.smoke_seed:
        M = Model(21, 3, R=float(np.sqrt(2 * 3 * 2.0)), wrad=1000.0)
        x1 = kick(seed_S1(M), 0)
        x2 = kick(seed_S2(M), 1)
        print("S1 norm", np.linalg.norm(x1), "S2 norm", np.linalg.norm(x2), "nX", M.nX())
        return 0
    cfg = json.load(open(args.config))
    run_probe_B(cfg, force=args.force, dry_run=args.dry_run, only_first=args.only_first)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Wrad side-check as frozen in cone/WRAD_SIDECHECK_FREEZE.md (f3950987).
Launch via: launch_gated.py --spec .../WRAD_SIDECHECK_FREEZE.md -- python run_wrad_sidecheck.py
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CONE = os.path.abspath(os.path.join(HERE, "..", "fuzz", "cone"))
V21 = os.path.join(CONE, "v2_1")
sys.path.insert(0, HERE)
sys.path.insert(0, V21)

from fuzzy_cone_v2_1 import Model
from relax_round2 import relax_r2, R2
from ring_projector import analyze_npz, sha256_file, uk_now

b, n, wrad = 2.0, 2, 1e4
Ns = [41, 61, 81]


def Bd_and_radial(M, x):
    X, P, B, K, rad = (
        np.asarray(v) if not isinstance(v, list) else [np.asarray(u) for u in v]
        for v in M.pieces(x)
    )
    Bd = (M.R ** 2) * B - M.n * np.eye(M.Np)
    TrBd = float(np.real(np.trace(Bd)))
    two = float(2.0 * TrBd / M.Np)
    S = sum(Xa @ Xa for Xa in X) / M.c
    ev = np.real(np.linalg.eigvalsh(S))
    xmax = float(np.max(np.abs(ev - 1.0)))
    return TrBd, two, xmax, float(np.linalg.norm(np.asarray(rad)))


def main():
    rows = []
    t0 = time.time()
    for N in Ns:
        R = float(np.sqrt(2 * n * b))
        theta = float(2.0 * R * R / np.sqrt(N * N - 1.0))
        path = os.path.join(V21, f"sol_wrad_side_b{b:g}_n{n}_N{N}_wrad1e4.npz")
        M = Model(N, n, R=R, wrad=wrad)
        t1 = time.time()
        x, E, ok, it, resid, msg = relax_r2(M, M.seed_fuzzy())
        solve_sec = round(time.time() - t1, 3)
        B = np.asarray(M.pieces(x)[2])
        np.savez_compressed(
            path, x=x, B=B, theta=theta, N=N, n=n, R=R, b=b, wrad=wrad,
            E=E, conv=bool(ok), nit=int(it), residual=float(resid),
            non_result=True, gtol=R2["gtol"], ftol=R2["ftol"],
            maxiter=R2["maxiter"], profile="r2", seed_name="fuzzy", message=str(msg),
            launched_via="launch_gated.py",
        )
        a = analyze_npz(path)
        TrBd, two, xmax, radn = Bd_and_radial(M, x)
        Qm4 = float(a["flux"]["Q_total"] - 4.0)
        row = dict(
            b=b, n=n, N=N, R=R, wrad=wrad,
            npz=path, npz_sha8=sha256_file(path)[:8],
            conv=bool(ok), nit=int(it), residual=float(resid), message=str(msg),
            solve_sec=solve_sec, E=float(E),
            Q_total=float(a["flux"]["Q_total"]),
            Q_minus_4=Qm4, abs_Q_minus_4=abs(Qm4),
            Tr_Bd=TrBd, twoTrBd_over_Np=two,
            identity_2TrBd_eq_Qm4=abs(two - Qm4) <= 1e-10,
            identity_diff=float(two - Qm4),
            rank_N=a["projector"]["rank_N"], rank_S=a["projector"]["rank_S"],
            max_abs_xhat2_minus_1=xmax, radial_resid=radn,
            non_result=True,
        )
        rows.append(row)
        print(
            f"N={N} nit={it} resid={resid:.3e} TrBd={TrBd:.6e} 2TrBd/Np={two:.6e} "
            f"|Q-4|={abs(Qm4):.6e} id_ok={row['identity_2TrBd_eq_Qm4']} "
            f"rank={row['rank_N']}/{row['rank_S']} conv={ok} |xhat^2-1|={xmax:.3e}",
            flush=True,
        )

    ratios = []
    all_ge5 = all_lt2 = True
    any_div = False
    for row in rows:
        N = row["N"]
        ref = os.path.join(V21, f"sol_probeA_r2_b2.0_n2_N{N}.npz")
        a1 = analyze_npz(ref)
        abs1 = float(a1["flux"]["abs_Q_minus_4"])
        abs4 = row["abs_Q_minus_4"]
        ratio = abs1 / abs4 if abs4 > 0 else float("inf")
        ratios.append(dict(
            N=N, abs_Q_minus_4_wrad1e3=abs1, abs_Q_minus_4_wrad1e4=abs4,
            ratio_1e3_over_1e4=ratio,
        ))
        if not row["conv"]:
            any_div = True
        if ratio < 5:
            all_ge5 = False
        if ratio >= 2:
            all_lt2 = False
        print(f"ratio N={N}: |Q-4|_1e3={abs1:.6e} |Q-4|_1e4={abs4:.6e} ratio={ratio:.4g}", flush=True)

    if any_div:
        verdict, reason = "UNDECIDED", "at least one solve did not converge"
    elif not all(r["identity_2TrBd_eq_Qm4"] for r in rows):
        verdict, reason = "UNDECIDED", "identity 2TrBd/Np == Q-4 failed"
    elif all_ge5:
        verdict, reason = "SOFT-CONSTRAINT", "|Q-4| fell by >=5x at all three N"
    elif all_lt2:
        verdict, reason = "NOT-WRAD", "|Q-4| fell by <2x at all three N"
    else:
        verdict, reason = "UNDECIDED", "ratios neither all >=5x nor all <2x"

    result = dict(
        tool="run_wrad_sidecheck.py",
        launched_via="launch_gated.py",
        freeze_sha8="f3950987",
        round2_sha8="1202fa35",
        code_sha8="63b69fbc",
        timestamp_uk=uk_now(),
        solver=R2,
        wrad_side=1e4, wrad_ref=1e3,
        b=b, n=n, Ns=Ns,
        rows=rows, ratios=ratios,
        verdict=verdict, reason=reason,
        summary=dict(
            all_identity_ok=all(r["identity_2TrBd_eq_Qm4"] for r in rows),
            all_converged=all(r["conv"] for r in rows),
            all_ratio_ge_5=all_ge5,
            all_ratio_lt_2=all_lt2,
            is_SOFT_CONSTRAINT=verdict == "SOFT-CONSTRAINT",
            is_NOT_WRAD=verdict == "NOT-WRAD",
            is_UNDECIDED=verdict == "UNDECIDED",
        ),
        elapsed_sec=round(time.time() - t0, 3),
    )
    out = os.path.join(CONE, "RESULT_WRAD_SIDECHECK.json")
    json.dump(result, open(out, "w"), indent=2)
    print(f"WROTE {out} sha8={sha256_file(out)[:8]} verdict={verdict} UK={result['timestamp_uk']}", flush=True)
    return 0 if not any_div else 0  # diagnostic; always exit 0 after write


if __name__ == "__main__":
    raise SystemExit(main())

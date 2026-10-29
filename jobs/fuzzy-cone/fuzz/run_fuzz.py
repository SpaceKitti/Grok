"""CLI driver. Every value comes from the JSON config (--config) or CLI overrides. No defaults for physics.
Usage: python run_fuzz.py --config fuzz_config_v4.json --mode step1|step2|ladder [--lam X] [--lams a,b,c] [--Ns 32,64,128] [--ks 2,3] --out out.json"""
import argparse, json, os, sys, time, hashlib
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from step1_paper import grade_step1
from observables import test_A, test_B_width, a_tip_star
from fuzzy_sphere import lam_N, R_from_lam
from ldos import ldos_width
import grading as G


def ints(s): return [int(x) for x in s.split(",")]
def floats(s): return [float(x) for x in s.split(",")]


def k_label(k, cfg):
    """V4 §5: only k in cfg['exact_k'] (=2, alpha=1/2) is the exact cone; k=1 has no tip; any other k is a reduced model."""
    if k in cfg["exact_k"]:
        return "exact orbifold S2/Z_%d" % k
    if k == 1:
        return "NO TIP (alpha=1)"
    return "REDUCED MODEL (k=%d not the exact hive cone, V4 §5)" % k


def step2(cfg, lam, Ns, ks):
    res = {}
    for k in ks:
        L = [ldos_width(R_from_lam(lam, N), N, k, cfg) for N in Ns]                 # V4 §3 primary
        A = [test_A(lam, N, k, cfg) for N in Ns]                                     # V4 §2 code check
        B = [test_B_width(lam, N, k, cfg) for N in Ns]                               # V4 §3 report-only
        res[str(k)] = {"label": k_label(k, cfg),
                       "B_LDOS_rows": L, "B_LDOS": G.grade_B(L, cfg),
                       "A_codecheck_rows": A, "A_codecheck_grade": G.grade_A(A, cfg),
                       "berezin_twist_codecheck": G.grade_B(B, cfg), "berezin_twist_rows": B,
                       "D": G.grade_D(B, k, cfg)}
    return res


def ladder(cfg, lams, R, Ns, ks):
    """V3 §5 + V4 §7: R fixed, N_j = round(sqrt(4R^2/lam_j^2+1)) (any integer N; actual lam reported).
    w(lam_j) = pole-LDOS width at (R, N_j). Per-rung L-B: LDOS widths over the N-set at fixed lam_j (V4 §1 bands).
    No h=lam/4 grid / floor (V4 §7). L-a is a code check (V4 §2); rungs with N<=20 give 'no a_tip'."""
    out = {}
    for k in ks:
        rungs = []
        for lj in lams:
            Nj = int(round(np.sqrt(4 * R * R / lj**2 + 1)))
            lact = float(lam_N(R, Nj))
            W = ldos_width(R, Nj, k, cfg); A = test_A(lact, Nj, k, cfg)
            LB = G.grade_B([ldos_width(R_from_lam(lj, N), N, k, cfg) for N in Ns], cfg)
            rungs.append({"lam_req": lj, "lam_actual": lact, "N": Nj, "w_over_R": W["w_over_R"],
                          "a_tip": A.get("a_tip"), "L_B_p": LB["p"], "L_B": G.grade_LB(LB["p"], cfg)})
        fit = G.ladder_fit([r["lam_actual"] for r in rungs], [r["w_over_R"] for r in rungs], cfg)
        La = G.grade_La([r["a_tip"] for r in rungs], a_tip_star(k), cfg)
        grades = [fit.get("L_q", "UNDECIDED"), fit.get("L_h", "UNDECIDED")] + [r["L_B"] for r in rungs]
        out[str(k)] = {"label": k_label(k, cfg), "rungs": rungs, "fit": fit, "L_a_codecheck": La,
                       "overall": G.overall(grades)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--mode", required=True, choices=["step1", "step2", "ladder"])
    ap.add_argument("--lam", type=float); ap.add_argument("--lams", type=floats)
    ap.add_argument("--R", type=float); ap.add_argument("--Ns", type=ints); ap.add_argument("--ks", type=ints)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    raw = open(a.config, "rb").read(); cfg = json.loads(raw)
    Ns = a.Ns or cfg["N_set"]; ks = a.ks or cfg["k_set"]
    t0 = time.time()
    rec = {"mode": a.mode, "config": a.config, "config_sha256": hashlib.sha256(raw).hexdigest()[:8],
           "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"), "label": "[hive proposal, untested]"}
    if a.mode == "step1":
        rec["step1"] = grade_step1(cfg["step1"])
    elif a.mode == "step2":
        if a.lam is None: ap.error("--lam required (lambda is set by Akitti; NOT COMPUTED (YET))")
        rec["lam"] = a.lam; rec["step2"] = step2(cfg, a.lam, Ns, ks)
    else:
        if a.lams is None or a.R is None: ap.error("--lams and --R required")
        rec["lams"] = a.lams; rec["R"] = a.R; rec["ladder"] = ladder(cfg, a.lams, a.R, Ns, ks)
    rec["elapsed_s"] = time.time() - t0
    json.dump(rec, open(a.out, "w"), indent=1, default=str)
    print(json.dumps(rec, indent=1, default=str)[:4000])


if __name__ == "__main__":
    main()

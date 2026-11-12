import json, sys, time, datetime, hashlib, numpy as np
from fuzzy_cone_v2_1 import Model, relax, symbol_diag, observe
from continuum_two_pole import _shoot
from scipy.optimize import brentq
import os, functools
h8 = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
th = np.linspace(0, np.pi, 4001)
@functools.lru_cache(None)
def cont(n, R, H):
    a = brentq(lambda a: _shoot(a, n, R, H).y[1, -1], -10, 10, xtol=1e-13); s = _shoot(a, n, R, H)
    t = np.clip(np.minimum(th, np.pi - th), 1e-4, np.pi / 2); return 0.5 * (1 - np.exp(np.minimum(s.sol(t)[0], 50)))
def solve(theta, N, n, wrad, save=True):
    R = float(np.sqrt(theta * np.sqrt(N**2 - 1) / 2)); t0 = time.time()
    M = Model(N, n, R=R, wrad=wrad); f = f"sol_v2_1_E_t{theta}_n{n}_N{N}.npz"
    if save and os.path.exists(f):  # reuse saved solution (same code/settings), no re-solve
        d = np.load(f); x, E, ok, it = d["x"], float(d["E"]), bool(d["conv"]), int(d["nit"]); reused = True
    else:
        x, E, ok, it = relax(M, M.seed_fuzzy()); reused = False
    B = np.asarray(M.pieces(x)[2])
    row = dict(theta=theta, N=N, n=n, R=R, wrad=wrad, bradlow=R**2 / (2 * n), E=E, E_over_2pin=E / (2 * np.pi * n), conv=ok, nit=it, sec=None)
    if save:
        if not reused: np.savez_compressed(f, x=x, B=B, theta=theta, N=N, n=n, R=R, wrad=wrad, E=E, conv=ok, nit=it)
        row["npz"] = [f, h8(f)]
        bc = cont(n, R, 5e-4); bc2 = cont(n, R, 1e-3); pk = np.abs(bc).max(); r = R * th
        bs = symbol_diag(M, B, th); err = np.abs(bs - bc) / pk
        o = observe(M, x)
        def core(b, rr):  # first r from the pole where b drops below 1/4
            i = np.argmax(b < 0.25); return float(rr[i]) if b[i] < 0.25 else None
        row.update(gap_N=float(err[r <= 3].max()), gap_S=float(err[r >= np.pi * R - 3].max()), grid_check=float(np.abs(bc - bc2).max() / pk),
                   mu_N=o["profiles"]["north"]["mu"] / (np.pi * n), mu_S=o["profiles"]["south"]["mu"] / (np.pi * n),
                   core_sym=core(bs, r), core_cont=core(bc, r), core_ref=max(1.0, np.sqrt(theta)),
                   ring_peak_N=o["profiles"]["north"]["r_peak"], ring_peak_S=o["profiles"]["south"]["r_peak"])
    row["reused_npz"] = reused if save else False; row["sec"] = round(time.time() - t0, 1); print(row, flush=True); return row
if __name__ == "__main__":
    if sys.argv[1:] == ["probe"]: solve(2.0, 141, 2, 1000.0); sys.exit()
    rows = []; wchk = []
    for theta in (0.5, 1.0, 2.0):
        for n in (1, 2):
            for N in (61, 101, 141): rows.append(solve(theta, N, n, 1000.0))
            w = solve(theta, 61, n, 10000.0, save=False); base = [r for r in rows if r["theta"] == theta and r["n"] == n and r["N"] == 61][0]
            wchk.append(dict(theta=theta, n=n, N=61, E_1000=base["E"], E_10000=w["E"], conv=w["conv"], dE_rel=abs(w["E"] - base["E"]) / base["E"]))
    G = {}
    for n in (1, 2):
        gi = []
        for theta in (0.5, 1.0, 2.0):
            rw = sorted([r for r in rows if r["theta"] == theta and r["n"] == n], key=lambda r: r["N"]); N = np.array([r["N"] for r in rw], float)
            A = np.vstack([np.ones(3), 1 / N]).T; g = {}
            for key in ("gap", "mu"):
                for p in "NS":
                    y = np.array([r[f"{key}_{p}"] for r in rw]); c, res, *_ = np.linalg.lstsq(A, y, rcond=None)
                    s2 = float(np.sum((A @ c - y)**2)) / 1; cov = s2 * np.linalg.inv(A.T @ A)
                    g[f"{key}_{p}"] = dict(inf=float(c[0]), c=float(c[1]), se=float(np.sqrt(cov[0, 0])), max_resid=float(np.abs(A @ c - y).max()))
            g["i"] = all(g[f"gap_{p}"]["inf"] > 0 and g[f"gap_{p}"]["inf"] > 3 * g[f"gap_{p}"]["se"] for p in "NS")
            g["iii"] = all(abs(g[f"mu_{p}"]["inf"] - 1) <= 0.02 for p in "NS")
            G[f"theta{theta}_n{n}"] = g; gi.append(0.5 * (g["gap_N"]["inf"] + g["gap_S"]["inf"]))
        gi = np.array(gi); inc = bool(gi[0] < gi[1] < gi[2])
        p = float(np.polyfit(np.log([0.5, 1, 2]), np.log(gi), 1)[0]) if (gi > 0).all() else None
        G[f"ii_n{n}"] = dict(g_inf=gi.tolist(), increasing=inc, p=p, ok=bool(inc and p is not None and p > 0))
    iv = all(r["conv"] for r in rows) and all(w["conv"] for w in wchk)
    I = [G[f"theta{t}_n{n}"]["i"] for t in (0.5, 1.0, 2.0) for n in (1, 2)]
    allpass = all(I) and all(G[f"ii_n{n}"]["ok"] for n in (1, 2)) and all(G[f"theta{t}_n{n}"]["iii"] for t in (0.5, 1.0, 2.0) for n in (1, 2)) and iv
    F2 = "PASS" if allpass else ("FAIL" if not any(I) else ("UNDECIDED" if any(I) and not all(I) else "FAIL"))
    out = dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               specs={"V2_1": h8("../FUZZY_CONE_SPEC_V2_1.md"), "B": "4e265cbd", "C": "86b8052f", "D": h8("../FUZZY_CONE_SPEC_V2_1_ADDENDUM_D.md"), "E": h8("../FUZZY_CONE_SPEC_V2_1_ADDENDUM_E.md")},
               code=h8("fuzzy_cone_v2_1.py"), continuum=h8("continuum_two_pole.py"), predictions=h8("PREDICTIONS_V2_1_E.json"), runner=h8("run_v2_1_E.py"),
               rows=rows, wrad_check=wchk, fits=G, iv_all_converged=iv, F2=F2)
    json.dump(out, open("RESULT_V2_1_E.json", "w"), indent=1); print(json.dumps(dict(fits=G, wrad=wchk, F2=F2), indent=1))

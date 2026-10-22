# HP2 reduced-config wrapper [reduced config, single grid, report-only]; imports run.py unchanged (837D0BC9).
# Overrides: Nr=Np=32 (full 64), nev requested 21 (=20 reported levels + eigenvalue 21 for the gap). R=10, iters=5000, 26 alphas, 9 series as in hp2().
import os, sys, time, json, csv, hashlib, numpy as np
sys.argv += ["--full", "--workers", "2"]
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, ROOT)
import run
from scipy.sparse.linalg import LinearOperator, eigsh
D = os.path.dirname(os.path.abspath(__file__)); TAGS = "[reduced config, single grid, report-only]"
N, NEV_REP, NEV_REQ, R, ITERS = 32, 20, 21, 10.0, 5000
NEARZERO = 1e-3   # [assumed] flag if |lambda_20| <= this
ST = {"att": [], "t": None}
def _res(A, w, V):
    try:
        if V is None or np.size(w) == 0: return float("nan")
        V = np.asarray(V).reshape(A.shape[0], -1); w = np.atleast_1d(np.asarray(w, float))[:V.shape[1]]
        return float(max(np.linalg.norm(A.matvec(V[:, j]) - w[j]*V[:, j]) for j in range(len(w))))
    except Exception: return float("nan")
def w_eigsh(A, *a, **k):
    if "sigma" in k: return eigsh(A, *a, **k)          # gauge gmin call, untouched
    c = [0]; f = A.matvec
    def mv(v): c[0] += 1; return f(v)
    A2 = LinearOperator(A.shape, matvec=mv, dtype=A.dtype); t = time.perf_counter()
    try:
        w, V = eigsh(A2, *a, **k); ST["att"].append(dict(ok=True, ncv=k.get("ncv"), mv=c[0], s=time.perf_counter()-t, res=_res(A, w, V), w=sorted(map(float, w)))); return w, V
    except Exception as e:
        ev = getattr(e, "eigenvalues", None); vv = getattr(e, "eigenvectors", None)
        nconv = 0 if ev is None else int(np.size(ev))          # fixed: no truthiness on arrays
        ST["att"].append(dict(ok=False, ncv=k.get("ncv"), mv=c[0], s=time.perf_counter()-t, nconv=nconv,
                              res=_res(A, ev, vv) if nconv else float("nan"), err=type(e).__name__, w=sorted(map(float, np.atleast_1d(ev))) if nconv else [])); raise
def w_log(n, k, al, extra=""):
    now = time.perf_counter(); dt = now - ST["t"]; ST["t"] = now
    rec = dict(n=n, kappa=k, alpha=float(al), solve_wall_s=round(dt, 2), attempts=ST["att"]); ST["att"] = []
    with open(os.path.join(D, "solve_log_%d.jsonl" % os.getpid()), "a") as fh: fh.write(json.dumps(rec) + "\n")
    print(time.strftime("%H:%M:%S"), TAGS, "solve", n, k, round(float(al), 3), "%.1fs" % dt, flush=True)
def series(a):
    run._EIGSH = w_eigsh; run._log_solve = w_log; ST["t"] = time.perf_counter()
    n, k, alphas = a
    rows = run._hp2_series((n, k, alphas, N, N, R, ITERS, NEV_REQ))
    with open(os.path.join(D, "rows_n%d_k%s.json" % (n, k)), "w") as fh: json.dump(rows, fh, default=float)
    return rows
if __name__ == "__main__":
    h = hashlib.sha256(open(os.path.join(ROOT, "spec", "CONE_SIM_SPECS.md"), "rb").read()).hexdigest()[:8].upper()
    rh = hashlib.sha256(open(os.path.join(ROOT, "run.py"), "rb").read()).hexdigest()[:8].upper()
    print(TAGS, f"spec hash file={h} FINAL={run.FINAL_SPEC_HASH} built={run.SPEC_HASH_BUILT} run.py={rh}", flush=True)
    if h != run.FINAL_SPEC_HASH or rh != "837D0BC9": print("REFUSED: hash mismatch"); sys.exit(2)
    alphas = list(np.linspace(1.0, 0.5, 26)); ser = [(n, k) for n in (0, 1, 2) for k in (0.5, 1.0, 2.0)]
    json.dump(dict(tags=TAGS, grid=[N, N], nev_reported=NEV_REP, nev_requested=NEV_REQ, R=R, iters=ITERS, alphas=alphas, series=ser,
                   workers=2, run_py=rh, spec=h, start=time.strftime("%Y-%m-%d %H:%M:%S")), open(os.path.join(D, "config.json"), "w"), indent=1)
    from concurrent.futures import ProcessPoolExecutor, as_completed
    T0 = time.perf_counter(); allrows = []
    with ProcessPoolExecutor(max_workers=2) as ex:
        fs = {ex.submit(series, (n, k, alphas)): (n, k) for (n, k) in ser}
        for f in as_completed(fs):
            allrows += f.result(); print(time.strftime("%H:%M:%S"), TAGS, "series done", fs[f], flush=True)
    hdr = ["n","kappa","alpha","level","lambda","max_overlap_prev","tracking  [hive proposal, untested]","grad2","row_stationarity","tag"]
    allrows.sort(key=lambda r: (r[0], r[1], -r[2], r[3]))
    with open(os.path.join(D, "hp2_flow_reduced.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(hdr); [w.writerow(list(r) + [TAGS]) for r in allrows]
    with open(os.path.join(D, "hp4_richardson_reduced.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["[hive proposal, untested] HP4", "status", "tag"])
        w.writerow(["dmu/dalpha vs 10 x Richardson error", run.NCY + " (error estimate from richardson_k1/); single grid: NOT COMPUTED", TAGS])
    print(time.strftime("%H:%M:%S"), TAGS, "DONE wall_s=%.0f" % (time.perf_counter()-T0), flush=True)



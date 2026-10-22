# HP2 64x64 short check [report-only]; imports run.py unchanged (837D0BC9).
# Same operator as 32/48 checks. Series: n=0,1,2 x kappa=0.5,1,2 x alpha=1,0.5.
import os, sys, time, json, csv, hashlib, numpy as np
sys.argv = sys.argv[:1] + ["--full", "--workers", "1"]
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
import run
from scipy.sparse.linalg import eigsh
D = os.path.dirname(os.path.abspath(__file__))
TAGS = "[64x64 short check, report-only]"
rh = hashlib.sha256(open(os.path.join(ROOT, "run.py"), "rb").read()).hexdigest()[:8].upper()
if rh != "837D0BC9":
    print("REFUSED run.py sha8", rh); sys.exit(2)
N, ITERS, NEV, R = 64, 5000, 21, 10.0
ALPHAS = [1.0, 0.5]
# n=2 kappa=2 and n=0 first so a kill still leaves the requested sectors
SER = [(2, 2.0), (0, 1.0), (0, 2.0), (0, 0.5), (1, 2.0), (1, 1.0), (1, 0.5), (2, 1.0), (2, 0.5)]
ST = {"att": [], "V": None, "t": None}

def w_eigsh(A, *a, **k):
    if "sigma" in k:
        return eigsh(A, *a, **k)
    t = time.perf_counter()
    try:
        w, V = eigsh(A, *a, **k)
        r = float(max(np.linalg.norm(A.matvec(V[:, j]) - w[j]*V[:, j]) for j in range(len(w))))
        ST["att"].append(dict(ok=True, ncv=k.get("ncv"), maxiter=k.get("maxiter"),
                              s=time.perf_counter()-t, res=r))
        ST["V"] = (w, V)
        return w, V
    except Exception as e:
        ev = getattr(e, "eigenvalues", None)
        ST["att"].append(dict(ok=False, ncv=k.get("ncv"), maxiter=k.get("maxiter"),
                              s=time.perf_counter()-t, err=type(e).__name__,
                              nconv=0 if ev is None else int(np.size(ev))))
        raise

def w_log(n, k, al, extra=""):
    now = time.perf_counter(); dt = now - ST["t"]; ST["t"] = now
    if ST["V"] is not None:
        w, V = ST["V"]; o = np.argsort(w)
        np.save(os.path.join(D, "evecs_n%d_k%s_a%.2f.npy" % (n, k, al)), V[:, o])
        np.save(os.path.join(D, "evals_n%d_k%s_a%.2f.npy" % (n, k, al)), w[o])
    ST["V"] = None
    rec = dict(n=n, kappa=k, alpha=float(al), N=N, iters=ITERS,
               solve_wall_s=round(dt, 2), attempts=ST["att"])
    with open(os.path.join(D, "solve_log.jsonl"), "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    ST["att"] = []
    print(time.strftime("%H:%M:%S"), TAGS, "solve", n, k, al, "%.1fs" % dt, flush=True)

run._EIGSH = w_eigsh
run._log_solve = w_log
rows = []
for n, k in SER:
    ST["t"] = time.perf_counter()
    rows += run._hp2_series((n, k, ALPHAS, N, N, R, ITERS, NEV))
    with open(os.path.join(D, "rows.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["n","kappa","alpha","level","lambda","max_overlap_prev","tracking","grad2","row_stationarity","tag"])
        [w.writerow(list(r) + [TAGS]) for r in rows]
json.dump({"N": N, "iters": ITERS, "nev": NEV, "R": R, "alphas": ALPHAS, "series": SER,
           "run_py": rh, "spec": run.SPEC_HASH_BUILT, "tag": TAGS},
          open(os.path.join(D, "config.json"), "w"), indent=1)
print(time.strftime("%H:%M:%S"), TAGS, "DONE n_rows=%d" % len(rows), flush=True)

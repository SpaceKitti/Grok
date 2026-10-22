# scratch timing probe for HP2; imports run.py unchanged (837D0BC9), writes only out\probe\
import os, sys, time, csv, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import run
from scipy.sparse.linalg import LinearOperator, eigsh
from multiprocessing import Pool
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hp2_probe.csv")
LOG = []
def counting_eigsh(A, *a, **k):
    c = [0]
    if isinstance(A, LinearOperator):
        f = A.matvec
        def mv(v): c[0] += 1; return f(v)
        A2 = LinearOperator(A.shape, matvec=mv, dtype=A.dtype)
    else: A2 = A
    kind = "gauge_gmin" if "sigma" in k else "SA"
    att = sum(1 for e in LOG if e[0] == kind) + 1
    t = time.perf_counter(); ok = "ok"
    try: return eigsh(A2, *a, **k)
    except Exception as e:
        ok = "%s nconv=%d" % (type(e).__name__, len(getattr(e, "eigenvalues", []) or [])); raise
    finally: LOG.append((kind, att, k.get("ncv"), k.get("maxiter"), c[0], round(time.perf_counter()-t, 1), ok))
def job(a):
    n, k, al, N, nev, iters = a; LOG.clear(); run._EIGSH = counting_eigsh
    Nr = Np = N; t0 = time.perf_counter()
    L = run.ConeLattice(Nr, Np, 10.0, al, k, n)
    x, E, g, it = L.relax(L.seed([(0.0, 0.0, n)] if n else []), iters); t1 = time.perf_counter()
    x, g2 = run.reach(L, x, run.THR["GRAD_TARGET"]); t2 = time.perf_counter()
    w, V, _ = L.spectrum(x, nev); t3 = time.perf_counter()
    sa = [e for e in LOG if e[0] == "SA"]
    return [N, nev, iters, n, k, round(al, 4), round(t3-t0, 1), round(t1-t0, 1), it, round(t2-t1, 1), round(t3-t2, 1), len(sa),
            ";".join("att%d ncv=%s maxit=%s matvec=%d %.1fs %s" % e[1:] for e in sa), len(w),
            bool(getattr(L, "spectrum_partial", False)), "%.2e" % g2, os.getpid()]
if __name__ == "__main__":
    al = list(np.linspace(1.0, 0.5, 26)); pick = [al[0], al[13], al[25]]
    ser = [(n, k) for n in (0, 1, 2) for k in (0.5, 1.0, 2.0)]
    S3 = [(1, 1.0), (0, 0.5), (2, 2.0)]
    jobs = [(n, k, a, 32, 10, 5000) for (n, k) in S3 for a in pick] \
         + [(n, k, a, 48, 10, 5000) for (n, k) in S3[:2] for a in (pick[0], pick[2])] \
         + [(1, 1.0, pick[0], 32, 20, 5000), (1, 1.0, pick[0], 32, 10, 2000), (1, 1.0, pick[0], 48, 20, 5000), (1, 1.0, pick[0], 64, 10, 5000)]
    with open(P, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["grid","nev","iters","n","kappa","alpha","wall_s","relax_s","relax_it","reach_s","spectrum_s","eigsh_attempts","attempts","nconv","partial","grad2","pid"]); f.flush()
        with Pool(2) as p:
            for r in p.imap_unordered(job, jobs):
                w.writerow(r); f.flush(); print(time.strftime("%H:%M:%S"), r, flush=True)


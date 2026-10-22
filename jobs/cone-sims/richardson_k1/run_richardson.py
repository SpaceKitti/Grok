"""richardson_k1 — C3/HP4 discretisation-error estimate for kappa = 1 profile integrals (Aethon, 15 Oct 2026).
Imports the SIGNED SM1 run-2 solver READ-ONLY (open-problems/01_sm_from_sphere/SM1_inputs_run/run.py, must hash 38C1D32A,
re-hashed after) and never calls its main(); nothing is written in that folder. For every kappa = 1 critical row it repeats the
signed chain's continuation (eps ladder at alpha = 1, then the alpha ladder with the same continue_param) and samples the same
solution at PROFILE N in {200, 400, 800} theta cell centres (profile_rows rule). From the samples (midpoint rule in theta):
  I_T(N) = sum 2 pi R f(theta) eps_m(theta) dtheta   (= int T_tt dA)
  I_K(N) = sum 2 pi R f(theta) K(theta) dtheta       (= int K dA over the smooth part; tips excluded)
Observed order p = log2(|I(200) - I(400)| / |I(400) - I(800)|); Richardson error E = |I(800) - I(400)| / (2^p - 1).
REPORT RULE (fixed before running): E is 'asymptotic' only if 1.5 <= p <= 2.5 (midpoint rule, expected p = 2) [assumed];
otherwise E is reported as 'NOT ASYMPTOTIC' with the conservative fallback E = |I(800) - I(400)|. If the two differences are
below 1e-14 relative (roundoff), p is 'NOT RESOLVED' and E = |I(800)-I(400)| (roundoff floor).
This measures the profile-sampling quadrature error of these integrals, not the BVP solver error (the BVP tolerance is separate).
Check: N = 200 samples must reproduce the signed profiles.csv to its printed precision (max diff reported).
Usage: python -B run_richardson.py [--smoke]
"""
import os, sys, csv, math, time, hashlib, importlib.util, json
from concurrent.futures import ProcessPoolExecutor, as_completed
SIGNED = r"C:\Users\Akitt\open-problems\01_sm_from_sphere\SM1_inputs_run\run.py"
SIGNED_HASH = "38C1D32A"
NS = (200, 400, 800)
P_LO, P_HI = 1.5, 2.5
HERE = os.path.dirname(os.path.abspath(__file__))
SMOKE = "--smoke" in sys.argv

def sha8(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:8].upper()

def load():
    spec = importlib.util.spec_from_file_location("sm1run", SIGNED)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def sample(m, G, s, lw, nN, nS, N):
    np = m.np
    th = math.pi*(np.arange(N)+0.5)/N
    tq = G.t_of_theta(th)
    y = s.sol(tq); h = lw(tq)+y[0]
    sig = np.exp(m.logsig2(tq))
    hp = 2*nN*(1-sig) - 2*nS*sig + y[1]
    ph2 = np.exp(h); f2 = G.f2(tq)
    em = (ph2*hp**2/4 + f2*(1-ph2)**2/4)/f2
    K = G.Kf2(tq)/f2
    f = G.f_theta(th); dth = math.pi/N
    return th, ph2, em, float(np.sum(2*math.pi*G.R*f*em*dth)), float(np.sum(2*math.pi*G.R*f*K*dth))

def chain(job):
    m = load()
    kind, n, eps, nN, nS = job["kind"], job["n"], job["eps"], job["nN"], job["nS"]
    R_n = job.get("R_n"); out = []
    a1 = (1.0, 1.0) if kind == "P12" else 1.0
    try:
        prev = None
        for e in [x for x in m.EPS_LADDER if x <= eps]:
            G, TN, TS = m.make_geo(kind, n, e, a1, R=m.radius(kind, R_n if R_n else n, e, a1))
            prev, lw = m.solve_taubes(G, nN, nS, TN, TS, m.guess_const(n, nN, nS, e) if prev is None else m.clamp(prev))
        sa, pa = prev, a1
        for a in job["ladder"]:
            def crit_at(av, s0):
                G_, TN_, TS_ = m.make_geo(kind, n, eps, av, R=m.radius(kind, R_n if R_n else n, eps, av))
                s_, lw_ = m.solve_taubes(G_, nN, nS, TN_, TS_, m.clamp(s0))
                return s_, lw_, G_, TN_, TS_
            if a == pa and a == a1:
                G, TN, TS = m.make_geo(kind, n, eps, a, R=m.radius(kind, R_n if R_n else n, eps, a))
                sa, lw = m.solve_taubes(G, nN, nS, TN, TS, m.clamp(sa))
            else:
                sa, lw, G, TN, TS = m.continue_param(crit_at, pa, a, sa)
            pa = a
            if sa.status != 0:
                raise RuntimeError("status %d at alpha %s" % (sa.status, a))
            if a not in job["alphas"]: continue
            res = dict(kind=kind, layout=job["layout"], n=n, eps=eps, alpha=a, status="ok")
            for N in NS:
                th, ph2, em, IT, IK = sample(m, G, sa, lw, nN, nS, N)
                res["IT%d" % N], res["IK%d" % N] = IT, IK
                if N == 200: res["ph2_200"], res["em_200"] = ph2.tolist(), em.tolist()
            out.append(res)
    except Exception as ex:
        out.append(dict(kind=kind, layout=job["layout"], n=n, eps=eps, alpha=None, status="FAILED: %s" % ex))
    return out

def rich(I1, I2, I3):
    d1, d2 = abs(I1-I2), abs(I2-I3)
    scale = max(abs(I3), 1e-300)
    if d2 < 1e-14*scale or d1 < 1e-14*scale:
        return "NOT RESOLVED", d2, "roundoff floor"
    p = math.log2(d1/d2)
    if P_LO <= p <= P_HI:
        return p, d2/(2**p-1), "asymptotic"
    return p, d2, "NOT ASYMPTOTIC (fallback |I800-I400|)"

def lab(a):
    return "%g" % a if not isinstance(a, tuple) else "(%g, %g)" % a

def akey(a):
    # normalise alpha labels ("1", "1.0", "(0.8, 0.5)") to a float tuple string
    t = str(a).strip("()").replace(" ", "")
    return ",".join("%g" % float(x) for x in t.split(",") if x)

def main():
    h0 = sha8(SIGNED)
    if h0 != SIGNED_HASH:
        print("STOP: signed run.py hash %s != %s" % (h0, SIGNED_HASH)); sys.exit(2)
    m = load()
    jobs = [j for j in m.build_jobs() if j["layout"] != "1T-sameR"]
    if SMOKE: jobs = jobs[:2]
    prof = {}
    pcsv = os.path.join(os.path.dirname(SIGNED), "profiles.csv")
    for r in csv.DictReader(open(pcsv, encoding="utf-8")):
        prof.setdefault((r["row"], r["layout"], str(int(float(r["n"]))), str(float(r["eps"])), akey(r["alpha"])), []).append(r)
    t0 = time.perf_counter(); rows = []
    with ProcessPoolExecutor(max_workers=2 if SMOKE else 8) as ex:
        for f in as_completed([ex.submit(chain, j) for j in jobs]):
            rows += f.result()
    T = time.perf_counter()-t0
    out = os.path.join(HERE, "out_scratch" if SMOKE else "out"); os.makedirs(out, exist_ok=True)
    tab = []; ps = []
    for r in rows:
        if r["status"] != "ok":
            tab.append([r["kind"], r["layout"], r["n"], r["eps"], "", r["status"]] + [""]*12); continue
        pT, ET, tT = rich(r["IT200"], r["IT400"], r["IT800"])
        pK, EK, tK = rich(r["IK200"], r["IK400"], r["IK800"])
        key = (r["kind"], r["layout"], str(int(r["n"])), str(float(r["eps"])), akey(lab(r["alpha"])))
        ref = prof.get(key); dmax = "NO MATCH IN profiles.csv"
        if ref:
            dmax = max(max(abs(float(x["phi2"])-a), abs(float(x["eps_m"])-b)) for x, a, b in zip(ref, r["ph2_200"], r["em_200"]))
        for p in (pT, pK):
            if not isinstance(p, str): ps.append(p)
        tab.append([r["kind"], r["layout"], r["n"], r["eps"], lab(r["alpha"]), "ok",
                    r["IT200"], r["IT400"], r["IT800"], pT, ET, tT, r["IK200"], r["IK400"], r["IK800"], pK, EK, tK, dmax])
    hdr = ["row","layout","n","eps","alpha","status","IT200","IT400","IT800","p_T","E_T","T_regime","IK200","IK400","IK800","p_K","E_K","K_regime","max|N200 - profiles.csv|"]
    with open(os.path.join(out, "richardson_k1.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(hdr); w.writerows(tab)
    h1 = sha8(SIGNED)
    ok = [t for t in tab if t[5] == "ok"]
    def stat(i):
        v = [t[i] for t in ok if not isinstance(t[i], str)]
        return (min(v), max(v)) if v else ("NONE", "NONE")
    s = dict(scratch=SMOKE, rows=len(tab), ok=len(ok), failed=len(tab)-len(ok), wall_s=T,
             p_T_range=stat(9), p_K_range=stat(15), E_T_max=stat(10)[1], E_K_max=stat(16)[1],
             T_asymptotic=sum(1 for t in ok if t[11] == "asymptotic"), K_asymptotic=sum(1 for t in ok if t[17] == "asymptotic"),
             N200_vs_signed_max=max([t[18] for t in ok if not isinstance(t[18], str)] or ["NONE"]),
             no_match=sum(1 for t in ok if isinstance(t[18], str)), signed_hash_before=h0, signed_hash_after=h1)
    json.dump(s, open(os.path.join(out, "summary.json"), "w"), indent=1, default=str)
    print(("[SCRATCH H5 — not a result] " if SMOKE else "") + json.dumps(s, default=str))
    if h1 != h0: print("WARNING: signed run.py hash changed during run"); sys.exit(3)

if __name__ == "__main__":
    main()

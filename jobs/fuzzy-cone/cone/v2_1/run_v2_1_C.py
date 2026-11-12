import json, datetime, sys, time, numpy as np
sys.path.insert(0, "../v1_4")
from fuzzy_cone_v2_1 import *
import cone_v1_4b as b
R = 3.0
out = dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), spec="FUZZY_CONE_SPEC_V2_1.md 9dbd2f861ff87efdce42f013afbca5a16f2729b72520486d0d53689cbd7f4227", addendum="FUZZY_CONE_SPEC_V2_1_ADDENDUM_B.md 4e265cbd", addendum_C="FUZZY_CONE_SPEC_V2_1_ADDENDUM_C.md 86b8052f", code="fuzzy_cone_v2_1.py 63b69fbc", continuum="continuum_two_pole.py c2c73cb4", wrad=1000.0, convention_flag="Addendum asks E/(2pi|n|) (two poles, total flux 2n); 4b single-vortex gives E/(pi|n|)=1. Both ratios reported; mismatch for Venus to settle.",
           predictions="PREDICTIONS_V2_1_C.json", R=R, bradlow={n: (4*np.pi*R**2)/(4*np.pi*2*n) for n in (1, 2)}, rows=[])
assert out["bradlow"][2] >= 2
for n in (1, 2):
    cont = b.solve(1.0, n, b.W_N / 10); f = lambda r, c=cont: np.interp(r, c["r"], c["f"])
    for N in (21, 41, 81):
        t = time.time(); M = Model(N, n, R)
        xf, Ef, okf, itf = relax(M, M.seed_fuzzy()); xs, Es, oks, its = relax(M, M.seed_smooth(f))
        of, os_ = observe(M, xf), observe(M, xs)
        row = dict(n=n, N=N, E_over_2pin_fuzzy=Ef/(2*np.pi*n), E_over_pin_fuzzy=Ef/(np.pi*n), E_over_2pin_smooth=Es/(2*np.pi*n), conv=[okf, oks], nit=[itf, its],
                   start_maxdiff=float(np.max(np.abs(xf - xs))), fuzzy=of, smooth=os_,
                   mu_over_pin_N=of["profiles"]["north"]["mu"]/(np.pi*n), mu_over_pin_S=of["profiles"]["south"]["mu"]/(np.pi*n), sec=round(time.time()-t, 1))
        out["rows"].append(row)
        print({k: v for k, v in row.items() if k not in ("fuzzy", "smooth")}, {k: v for k, v in of.items() if k != "profiles"},
              {p: (round(of["profiles"][p]["r_peak"], 3), of["profiles"][p]["ring"]) for p in ("north", "south")}, flush=True)
json.dump(out, open("RESULT_V2_1_C.json", "w"), indent=1)

from continuum_two_pole import cap_flux
gr = {}
for n in (1, 2):
    rows = [r for r in out["rows"] if r["n"] == n]; Ns = np.array([r["N"] for r in rows]); Qc = cap_flux(n, h=5e-4)[0]
    Q = np.array([r["fuzzy"]["Q_cap_N"] for r in rows]); c = np.polyfit(1 / Ns, Q, 1); Qinf = float(c[1]); dev = np.abs(Q - Qc)
    f3 = abs(Qinf - Qc) <= 0.02 and bool(np.all(np.diff(dev) < 0)) and all(r["fuzzy"]["rank_N"] == n and r["fuzzy"]["rank_S"] == n for r in rows)
    e = np.array([abs(r["E_over_2pin_fuzzy"] - 1) for r in rows]); f5 = bool(np.all(np.diff(e) < 0))
    mu = rows[-1]["mu_over_pin_N"], rows[-1]["mu_over_pin_S"]; f4 = all(abs(m - 1) <= 0.02 for m in mu)
    st = all(r["start_maxdiff"] <= 1e-6 for r in rows)
    gr[n] = dict(Q_cont=Qc, Q_cap=Q.tolist(), Q_inf=Qinf, F3="PASS" if f3 else "FAIL", F4="PASS" if f4 else "FAIL", mu_N81=mu,
                 F5="PASS" if f5 else "FAIL", E_over_2pin=[r["E_over_2pin_fuzzy"] for r in rows], start="PASS" if st else "FAIL",
                 ring=[(r["N"], r["fuzzy"]["profiles"]["north"]["r_peak"], r["fuzzy"]["profiles"]["north"]["ring"]) for r in rows])
out["grades"] = gr; json.dump(out, open("RESULT_V2_1_C.json", "w"), indent=1); print(json.dumps(gr, indent=1))

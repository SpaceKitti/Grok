import json, datetime, sys, time, numpy as np
sys.path.insert(0, "../v1_4")
from fuzzy_cone_v2_1 import *
import cone_v1_4b as b
R = 3.0
out = dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), spec="FUZZY_CONE_SPEC_V2_1.md 9dbd2f861ff87efdce42f013afbca5a16f2729b72520486d0d53689cbd7f4227", addendum="FUZZY_CONE_SPEC_V2_1_ADDENDUM_B.md 4e265cbd", wrad=1000.0, convention_flag="Addendum asks E/(2pi|n|) (two poles, total flux 2n); 4b single-vortex gives E/(pi|n|)=1. Both ratios reported; mismatch for Venus to settle.",
           predictions="PREDICTIONS_V2_1_SHORT.json", R=R, bradlow={n: (4*np.pi*R**2)/(4*np.pi*2*n) for n in (1, 2)}, rows=[])
assert out["bradlow"][2] >= 2
for n in (1, 2):
    cont = b.solve(1.0, n, b.W_N / 10); f = lambda r, c=cont: np.interp(r, c["r"], c["f"])
    for N in (21, 41):
        t = time.time(); M = Model(N, n, R)
        xf, Ef, okf, itf = relax(M, M.seed_fuzzy()); xs, Es, oks, its = relax(M, M.seed_smooth(f))
        of, os_ = observe(M, xf), observe(M, xs)
        row = dict(n=n, N=N, E_over_2pin_fuzzy=Ef/(2*np.pi*n), E_over_pin_fuzzy=Ef/(np.pi*n), E_over_2pin_smooth=Es/(2*np.pi*n), conv=[okf, oks], nit=[itf, its],
                   start_maxdiff=float(np.max(np.abs(xf - xs))), fuzzy=of, smooth=os_,
                   mu_over_pin_N=of["profiles"]["north"]["mu"]/(np.pi*n), mu_over_pin_S=of["profiles"]["south"]["mu"]/(np.pi*n), sec=round(time.time()-t, 1))
        out["rows"].append(row)
        print({k: v for k, v in row.items() if k not in ("fuzzy", "smooth")}, {k: v for k, v in of.items() if k != "profiles"},
              {p: (round(of["profiles"][p]["r_peak"], 3), of["profiles"][p]["ring"]) for p in ("north", "south")}, flush=True)
json.dump(out, open("RESULT_V2_1_SHORT.json", "w"), indent=1)

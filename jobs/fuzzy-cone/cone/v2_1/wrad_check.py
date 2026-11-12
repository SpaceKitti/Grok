"""wrad x10 check (1000 -> 10000), fuzzy start, all short-test cases; also times one N=81 solve for the rerun estimate."""
import time, json, numpy as np
from fuzzy_cone_v2_1 import Model, relax
out = []
for n in (1, 2):
    for N in (21, 41):
        E = [relax(Model(N, n, wrad=w), Model(N, n, wrad=w).seed_fuzzy())[1] for w in (1000.0, 10000.0)]
        out.append(dict(n=n, N=N, E1000=E[0], E10000=E[1], dE_rel=abs(E[1] - E[0]) / E[0])); print(out[-1], flush=True)
t = time.time(); M = Model(81, 2); r = relax(M, M.seed_fuzzy()); out.append(dict(timing_N81_n2_one_solve_s=time.time() - t, conv=r[2], nit=r[3])); print(out[-1])
json.dump(out, open("WRAD_CHECK_V2_1_C.json", "w"), indent=1)

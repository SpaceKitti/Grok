"""Scratch (H5): does a short flow remove the identity-face jump? B10, alpha=1, eps=1, BPST rho=3a seed."""
import json, time, numpy as np, run
from lattice import Lattice
from kernels import Loops
S8 = 8*np.pi**2; lat = Lattice(*run.BOXES["B10"], alpha=1.0); lp = Loops(lat, 1); U = lp.flat(lat.bpst_links(3.0))
outer = lp.site_r >= lat.r[-3]; rec = []; t0 = time.time(); tt = 0.0
def snap(U, t):
    S, d = lp.action(U, per_site=True); rec.append(dict(t=t, S=S/S8, S_outer2rings=float(d[outer].sum()/S8), rho_r_ge_2a=lp.rho_moment(U), wall=time.time()-t0)); print(rec[-1], flush=True)
snap(U, 0.0)
for blk in range(8):
    U, _ = lp.flow(U, h=0.005, max_steps=10, record=5); tt += 0.05; snap(U, tt)
json.dump(rec, open("out/diag_relax_B10.json", "w"), indent=1)

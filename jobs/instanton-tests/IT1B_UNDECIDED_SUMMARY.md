# IT1b — UNDECIDED (fix loop closed, 1 round spent)
Signed: Venus (maths rows). Helios co-sign pending.
Frozen measure: VENUS_IT1B_POWERLAW_MEASURE.md rev 6 E360229B. Code: run.py D9D6766D, it1b_measure.py 503F7AC6.
Fix tried (untested idea, literature): over-improved flow eps=-1 (Garcia Perez et al. NPB413 1994; de Forcrand et al. NPB499 1997).

Results (C1 calibration, B10, alpha=1, rho=3a, gate |shift|<=5%):
- On tip:  shift -8.68%, flowed rho 2.740 (cal_B10_eps-1.json). FAIL. Wilson was -7.9%.
- Off tip (centre r=4a, OFFTIP_DIAG_FROZEN.md 06243117): shift -11.69%, flowed rho 2.649. Falls outside all three frozen bands (worse than "not the tip"); read as not the tip. Band gap stated, not redrawn.
- 3a/4a mix-up: Helios froze 3a, NanoRibbon approved 4a first; ran at 4a.
Code checks passed: c1=(4-eps)/3, c2=(eps-1)/48 on 2x2 squares, c1+16c2=1, eps in force (FD-checked), eps=1 = Wilson bit-for-bit.
No delta rows ran. Aethon's gap-fills (noise gate at 0.003; P3 on +delta rows; X0 check ||Q|-1|<=0.05) recorded as notes only.

Reading: our flow fails to reproduce a published result (eps=-1 should not shrink rho/a=3). Red flag on lattice/flow, not physics.
Candidates: non-uniform polar spacing (alpha*r*dphi), box faces at R=9.5, flow step.
diag22 and IT1 results using this flow are SUSPECT until the hypercubic reproduction (gates 2037F294) passes.
Not an open problem; no Clay claim.

# Hypercubic repro — boundary fix B1 (Venus proposal; needs Helios co-sign) [hive proposal, untested]
Amends 1A723DCE (kept frozen as is) for the boundary setup only. All G1-G4 thresholds unchanged.
Cause: singular-gauge x/|x| winds, so a periodic wrap puts a seam of non-trivial links (~34-45 instanton actions at t=0).
Choice: NO periodic wrap. Open hypercubic box L=24 with Dirichlet links: the outer 2 layers are set from the exact
REGULAR-gauge BPST (A ~ pure gauge + O(rho^2/r^3) at large r, F ~ rho^4/r^8), held fixed, never flowed.
Twisted BCs rejected: Q=1 on twisted T^4 is not the BPST and is not the paper's object.
Gate B0 (before G1): t=0 action on links touching the clamped layers, minus the continuum BPST action there, <= 1% of 8pi^2.
   If B0 fails, stop and report; no further setup changes in this round.
Q: report interior Q (|x| <= L/2-3) before and after flow; whole-lattice Q not used.
rho_0 as in 1A723DCE: interior rho at t=0, measured the same way as the flowed rho.
Note: a clamped boundary is itself a pressure. Report G2/G3 with the B0 excess beside them.

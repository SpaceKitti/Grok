# OFF-TIP calibration diagnostic (Aethon) - FROZEN 2026-10-23 22:20 BST, before the run. DIAGNOSTIC ONLY, not a pass. [hive proposal, untested]
Context: IT1b closed UNDECIDED (NanoRibbon). Rev 6 C1 (E360229B, tip-centred) shrank -8.68% under eps=-1. Question: is the Wilson-only cone tip (r<2a: no 2x2 loops) the cause?
Setup: identical to rev 6 C1 (run.py it1b-cal): B10 (Mr=10, Lphi=20, M3=M4=20), alpha=1, eps=-1 over-improved flow (5/3 1x1, -1/24 2x2), exact BPST rho=3a,
h=0.002, 300 steps to T=0.6, same calibration (rel_shift = (rho_moment_flowed - rho_moment_unflowed)/rho_moment_unflowed, rho_moment about the BPST centre, rmin=2).
ONLY change: BPST centre (x1,x2,x3,x4) = (4.0a, 0, 0.5a, 0.5a), i.e. r=4a at theta=0 instead of r=0 (tip). x3,x4 unchanged from C1.
Fit: r+rho = 7a < l = 9.5a (outer radial face), so 4a fits; no fallback needed. Note: the outer radial face is then 5.5a from the centre (was 9.5a), so face effects are larger than in C1. r=4a lies between rings 3.5a and 4.5a (not a site); the singular-gauge links have no site at the centre.
Outcome rule (fixed now): |shift| <= 5% OR shift sign reverses (grows) => tip confirmed as the cause. Shrinks by more than 5% => cause is not the tip.
Nothing else runs: no delta rows, no C2. Output: out/diag22b/cal_B10_eps-1_offtip_r4.json.
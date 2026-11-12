# Probe B round 2 freeze addendum (Venus, 2026-11-05 18:56 UK) — round 2 of 3
Amends Y_JUNCTION_B_V2_FREEZE.md b84a670a (unchanged). Decided by NanoRibbon 18:51 UK.
Change C1 (probe script only, not the frozen energy): reject any L-BFGS step that raises |x|_inf by more than 10x; seeds, kicks, wrad=1e3, solver settings otherwise as round 1. Same 36 solves, once. Log how many steps were rejected per solve.
Change C2 (grading): graded row is S1 (coincident, kicked) at b=2, N=61 and 81, seeds 0/1/2.
 - THREE-LEG: all six converge, 3 peaks (pin Q2) and A3 > 0.1 in each, and A3 above the S1 seed baseline (0.02-0.03, RESULT_PROBE_B_A3_BASELINE.json 3e0166fa).
 - MERGE: all six converge, 1 peak, A3 < 0.02 above baseline.
 - BROKEN: rank != 3 at either pole, or |Q_total-6| > 3e-2, in a graded row.
 - UNDECIDED: anything else, incl. any non-converged or diverged graded row.
 S2 rows and b=1.2, 1.05 are output only (A3 fade near b=1 expected from Bradlow saturation, Helios).
Open-problem check: STILL_TO_DO.md has no entry; BPS vortices on S2 have flat moduli above the Bradlow bound [standard: Bradlow CMP 135 (1990) 1; Garcia-Prada BLMS 26 (1994); fuzzy charge as projector index hep-th/9510083]. Not open.
Idea owner: Akitti (Y-junction, post 2117965185126183010); spec Helios (hive proposal).
Grading rule: projector rank 3 at both poles (ev_proj) as validity; shape graded as above; Q_total reported, tolerance as frozen.
Dimension note: 2D (fuzzy S2) stepping stone towards the 4D S2_F x T2 product.

# Probe B v2 freeze (Venus, 2026-11-05 18:22 UK)
Freezes Y_JUNCTION_SPEC_B_DRAFT_V2.md 8a0ca930 (text unchanged) with pins:
Q1 Moduli check: model is at Bradlow/BPS coupling, so separated unit strings feel no force and the minimiser may simply stay where seeded. If both S1 and S2 converge, |E(S2)-E(S1)| <= grid error, and each keeps its seeded shape, verdict = DEGENERATE (flat moduli), not THREE-LEG or MERGE. THREE-LEG then needs S1 (kicked) to also split into three peaks.
Q2 Peak count is graded (THREE-LEG, MERGE): local maxima of the coherent-state symbol on the 64x64 cap grid above 50% of the cap maximum. Not output-only.
Q3 Rank = 3 and |Q_total-6| <= 3e-2 at BOTH poles/whole sphere, rank from ev_proj_N/S > 0.5 (printed).
Q4 Convergence and printout as PROBE_A_ROUND2_DIAG_ADDENDUM 1202fa35 (R1, R2). Non-converged -> UNDECIDED.
Q5 Kick: seeds 0,1,2 each run (36 solves); a verdict needs all three seeds to agree, else UNDECIDED.
Q6 Runs after round 2 finishes regardless of its verdict (NanoRibbon 18:17).
Grade with grade_result.py c188ec50, 1 run, no refits.

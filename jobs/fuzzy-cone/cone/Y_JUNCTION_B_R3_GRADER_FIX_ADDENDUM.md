# Probe B R3 grader-fix addendum (Venus, 2026-11-09 19:55 UK). Not a round, no new solves, no threshold changes.
Amends grading of RESULT_PROBE_B_R3.json af46054e (sweep 7a80eeb6); freezes b84a670a, a45cf913, 728e3ee1 unchanged. Re-grades the saved R3 npz only.
Fixes (grader implemented the frozen rules wrongly):
G1 Rank (pin Q3): per-pole rank = signs of eigenvalues of P_ker x3_hat P_ker on ker(Phi^+) (basis-free; Aethon tools/kernel_x3_check.py 14f6bb10). The old observe() count used an arbitrary basis of a degenerate kernel.
G2 DEGENERATE (pin Q1 as restated in 728e3ee1): checked after BROKEN/UNDECIDED and before THREE-LEG/MERGE. DEGENERATE if, at b=2 and each N in {61,81}, all S1 and S2 rows converge and max|E(S1)-E(S2)| <= grid error, grid error := |E(N=81)-E(N=61)| of S1 seed 0. All three seeds must agree (Q5).
G3 Peaks (pin Q2) literal: exactly 3 at each pole for THREE-LEG (grader had >=3).
Everything else as tools/grade_probe_b_r3.py 7e92a918. New grader: tools/grade_probe_b_r3_fix.py; output RESULT_PROBE_B_R3_REGRADE.json.
Open-problem check: STILL_TO_DO.md has no entry; flat BPS moduli are standard (Bradlow CMP 135 (1990); Garcia-Prada BLMS 26 (1994); fuzzy projector charge hep-th/9510083); whether the fuzzy energy has an exact bound is still being checked by Venus (E < 6pi seen, BPS_CHECK_B_R3.json 4dfcdbcf). Grader fix is not an open problem.
Idea owner: Akitti (Y-junction); spec Helios; grader fix Venus with Aethon's kernel count (hive work).
Grading rule: projector rank 3/3 per pole via G1 for validity; Q_total output only beyond the frozen 3e-2 tolerance; verdict order UNDECIDED > BROKEN > DEGENERATE > THREE-LEG > MERGE > UNDECIDED.
Dimension note: 2D fuzzy S2 stepping stone towards the 4D product.

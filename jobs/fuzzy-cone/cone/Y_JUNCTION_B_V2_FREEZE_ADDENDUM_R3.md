# Probe B round 3 freeze addendum (Venus, 2026-11-05 19:18 UK) — round 3 of 3, final
Amends Y_JUNCTION_B_V2_FREEZE.md b84a670a and ADDENDUM_R2 a45cf913 (both unchanged).
Single change: wrad = 1e4 (was 1e3) for all 36 solves; step clamp from R2 kept; seeds, kicks, solver settings unchanged. Run once. Basis: the runaway is in |x| (radius held by the soft penalty) and WRAD_SIDECHECK 371f1df5 showed the penalty offset scales as 1/wrad.
Grading unchanged from R2 (S1 at b=2, N=61 and 81, seeds 0/1/2; peak rule Q2 still graded, no relaxation after seeing data). DEGENERATE (pin Q1) applies if S1 and S2 end at equal E within grid error.
If not settled: B reported UNDECIDED at cap, no further rounds.
Open-problem check: STILL_TO_DO.md has no entry; abelian BPS vortices on S2 have flat moduli above the Bradlow bound [standard: Bradlow CMP 135 (1990) 1; Garcia-Prada BLMS 26 (1994); fuzzy charge as projector index hep-th/9510083]. Not open.
Idea owner: Akitti (Y-junction, post 2117965185126183010); spec Helios (hive proposal).
Grading rule: projector rank 3 at both poles (ev_proj) as validity; shape graded as in R2; Q_total tolerance as frozen.
Dimension note: 2D (fuzzy S2) stepping stone towards the 4D S2_F x T2 product.

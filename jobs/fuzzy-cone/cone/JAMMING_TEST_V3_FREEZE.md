# Freeze of JAMMING_TEST_SPEC_DRAFT_V3.md (f14647c7), Venus, 2026-11-10 02:50 UK. The draft text is frozen as is; this note adds only what it left open.
Open-problem check: STILL_TO_DO.md jamming entry OPEN; d=3 jamming open (arXiv:1310.2549, van Hecke arXiv:0911.1384); continuum BPS moduli flat for b>1 (Bradlow CMP 135 (1990)); DEAD_ENDS.md grepped, dead routes not reused.
Idea owner: Akitti (jamming criterion); mapping and measures hive proposal (Helios, route A from Venus check 454ed895).
Grading rule: validity = basis-free projector rank 3/3 per pole on every state, else UNDECIDED; Q_total output only.
Dimension note: 2D fuzzy S2 stepping stone; no d=3 claim.

F1 Reading precedence (checked in this order, first match wins): UNDECIDED > SADDLE > JAMMING-LIKE HINT > LATTICE-LOCKED / ROBUST LOCK. Mixed band ratios (some < 1, some >= 1 at one b) = UNDECIDED, as the draft says.
F2 N=61 rows for J1/J2 = the finished Hessian rows (f977e22b, ffb5836f, 9468b5fd; line-checked PASS, VENUS_HESSIAN_B_LINE_CHECK.md d7d42963).
F3 N=81 rows: the saved files v2_1/sol_probeB_r3_S1_b{2,1.2,1.05}_n3_N81_seed0.npz, script 42724a62 unchanged, called through a wrapper that only sets the npz path and the output file (as for the b=1.2/1.05 reruns). One launch per row, no timeouts. Each row's output also prints E and |grad| so convergence can be checked.
F4 J3 waits for the new seed function's hash and a Venus line check; no J3 launch before that.
F5 No fix rounds are used by this freeze. Route B stays parked unless Akitti OKs it.

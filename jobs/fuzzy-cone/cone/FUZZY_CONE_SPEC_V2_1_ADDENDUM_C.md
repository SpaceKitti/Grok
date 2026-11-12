# V2_1 ADDENDUM_C (Venus), 2026-10-30 10:58 UK. Applies to V2_1 9dbd2f86 + ADDENDUM_B 4e265cbd. Replaces only the F3 flux test. Frozen before any rerun.
F3 flux: compare the cap flux inside 1.5ρ against the continuum round-sphere two-pole vortex at the same R. The continuum values are 0.400 (n=1) and 0.525 (n=2) at R=3ρ. Aethon supplies the continuum solver with its hash, plus a resolution check: the values move <0.002 when its grid is doubled.
Pass: fit Q_cap(N) = Q_inf + c/N over N=21,41,81. |Q_inf − Q_cont| ≤ 0.02, and |Q_cap − Q_cont| shrinks monotonically in N.
Cap sampling: integrate the symbol's flux density on a fixed fine θ grid. No whole-shell counting.
Rejected: the equator cap. Each hemisphere holding n follows from symmetry plus the topological total, so that test cannot fail (the V1_4 tautology lesson). Growing R stays an option for later runs only.
F3 rank test unchanged (exact n).

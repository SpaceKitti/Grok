# Probe A round 2 diagnostic addendum (Venus, 2026-11-05 18:18 UK)
Separate diagnostic. Probe A verdict (RESULT_PROBE_A.json 07d1e838, BROKEN) stands and is not regraded.
Base: spec 8d7f5092 + freeze 6e0f1942 + addendum 1 61f39a62, same 12 solves (b in {2,1.5,1.2,1.05}, N in {41,61,81}), run once.
Changes only:
R1 Iteration cap raised (x10 over round 1) and solver tolerance 100x tighter. Every solve must report success=True; any non-converged -> UNDECIDED for that solve and for the diagnostic.
R2 Print ev_proj_N and ev_proj_S (pole projector eigenvalues) per solve; rank = count > 0.5 of these.
Diagnostic rule (frozen now):
- CONVERGENCE: all converged and worst |Q_total-4| < 1e-2 -> round-1 drift was under-convergence.
- FLUX-NOT-QUANTISED: all converged and worst |Q_total-4| > 3e-2 -> fuzzy flux sum not pinned near criticality (fuzzy-sphere property, not a tip leak).
- UNDECIDED: anything else.
Ring shift and trend reported as outputs only. Grade with grade_result.py c188ec50. Round 2 of 3.

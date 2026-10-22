# richardson_k1 — C3/HP4 Richardson discretisation error (κ = 1 profiles)
NanoRibbon go, 15 Oct 2026 ~18:10 BST. Spec context: CONE_SIM_SPECS 736DA1BD (rev 7) C3/HP4 "10× Richardson over ≥3 resolutions (200, 400, 800)", VENUS_CONE_DIFF_REV7 9C476E05 §2 (report observed order).
Signed SM1 run-2 solver used READ-ONLY by import: open-problems\01_sm_from_sphere\SM1_inputs_run\run.py (38C1D32A, hashed before/after). Signed outputs untouched; this job writes only under richardson_k1\out*.
## Method and report rule (fixed BEFORE running)
- Same continuation as the signed chain; same converged solution sampled at N = 200, 400, 800 θ cell centres.
- I_T = ∫T_tt dA, I_K = ∫K dA (smooth part) by midpoint rule from the samples.
- Observed order p = log2(|I200−I400| / |I400−I800|). E = |I800−I400|/(2^p−1) only if 1.5 ≤ p ≤ 2.5 [assumed] ("asymptotic"); else "NOT ASYMPTOTIC" with fallback E = |I800−I400|; differences < 1e-14 rel → "NOT RESOLVED" (roundoff floor).
- What E measures: profile-sampling quadrature error, not BVP solver error.
- Check: N = 200 must reproduce signed profiles.csv (max diff reported).
- C3 tolerance then = 10·E_K, 10·E_T [assumed] (spec rev 7). HP4 [hive proposal, untested] uses 10·E of μ (= I_T).
## Post-run notes (run on TrinityOrb 15 Oct 2026 ~18:16 BST, 8 workers, 40.8 s)
- 308/308 κ = 1 rows ok, 0 failed. Signed run.py 38C1D32A before and after; signed profiles.csv 8FCD0035 unchanged.
- N = 200 reproduces signed profiles.csv to max diff 2.34e-13.
- Observed order p_T ∈ [1.965, 2.112], p_K ∈ [2.00001, 2.00014]: all 308 rows in the asymptotic band (1.5–2.5) for both.
- max E_T = 9.83e-4 (max relative 1.56e-4); max E_K = 1.61e-5 (max relative 1.28e-6).
- Outputs: out/richardson_k1.csv 0DCA572A, out/summary.json 29D8858C.
- Scope: profile-sampling quadrature error only (not BVP solver error).
## Sign-offs
Aethon: ____ Venus: ____ NanoRibbon: ____


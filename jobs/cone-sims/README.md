# cone-sims — built by Aethon, 15 Oct 2026 (BST)
Spec built against: CONE_SIM_SPECS **CA9D5CBC** (rev 15, Venus-confirmed; CHANGES B3B350F0). FINAL_SPEC_HASH = CA9D5CBC. Earlier targets: E9A76637, 736DA1BD, 4FA92781, F204F8A7, 27CC9F84, D200835C.
FROZEN to CA9D5CBC. `run.py --full` checks spec/CONE_SIM_SPECS.md against it. NOT LAUNCHED: waiting for NanoRibbon's go after the cost is posted in Hive.
Gravity: lift gravity is unknown QG. GR appears only as [GR control] rows.

## Predictions (verbatim from E9A76637, copied before any run)
- C1 [prediction] κ < 1: R < 1 (type I, vortices attract); κ > 1: R > 1 (type II) [standard: Jacobs–Rebbi 1979]. (C1 is a READ-OUT, not a test.)
- C2 [prediction] Equal-tension 2-tip rows: football exists, tips antipodal. Unequal 2-tip: no constant-K solution; balance needs curvature (matter) gradients. ≥3 tips: exist iff inequality holds; equal tensions → symmetric arrangement.
- C3 [prediction] Under the frozen exterior, any δ_s ≠ 0 whose energy is not inside ∫T_tt shifts ∫K and is rejected by Akitti's filter. Strain survives only if it is part of T_tt ... Pure shear (traceless, zero energy) leaves δ unchanged.
- C4 [prediction] At κ = 1 exactly 2n real zero modes, all positions, none a scale modulus ... κ ≠ 1: only the 2 overall translations.
- C5 [prediction] relative space looks like a cone of angle π ... smooth in w = z² [standard: Samols 1992]; for α < 1 the moduli space also carries a conical point inherited from the background.
- C7 RESULT RECORDED (Venus V6): Grok's K = −b²κ_c²; G6 FAIL as stated. Not run as a test.
- [hive proposal, untested] HP1–HP4: separate; HP2 prediction: zero-mode count fixed by n alone at every α.

## Thresholds — PLACEHOLDERS tied to the final hash (all [assumed])
C1 |R−1| ≤ 1e-6 (read-out) · normal-state drop max_phi2 < 1e-6 · C2 mesh conv ≤ 1e-4 (reported) · Gauss–Bonnet ≤ 1e-4 rel on finest, ≥3 refinements, observed order — **[solver check only, not a test]** · C3 tolerance: 10·E_K, 10·E_T from richardson_k1/ (observed order ≈ 2, all 308 rows asymptotic) · C4 zero rule |λ|/λ_gap → 0 over ≥3 grids (stale 1e-8..1e-4 band dropped) · C5 angle 1e-3, n = 2 rows only.

## Venus F7F8F08D edits applied
l.103 α-from-μ struck (α_i are inputs only) · C4-b restricted to κ ≠ 1 · C4 l.144 band removed · C5 grades n = 2 only · κ_c used for plane-curve curvature · C1 l.88 / C3 l.124 / G3 GR forms only as [GR control] rows · C3 tolerance pending.

## Status of pieces
C1 implemented (read-out) · C2 2-tip axisymmetric solver + Luo–Tian 3-tip table + GB solver check implemented; general ≥3-tip 2D FEM with Möbius relaxation NOT COMPUTED (YET) · C3 all rows NOT COMPUTED (YET) · vortex-on-cone background BVP implemented; C4/HP2 polar-lattice fluctuation operator implemented (Lanczos/ARPACK on jax Hessian-vector products + background-gauge penalty ξ·GGᵀ with ξ = 10/λ_min(GᵀG) [assumed]; gauge leakage |Gᵀv| reported per mode; [assumed; H3 deviation, accepted: Venus] (spec ξ = 1). xi_check.py (scratch, grid 48): at ξ = 1 gauge modes enter the 24-mode window (lowest 1.005e-1 and 1.597e-2), and for n=2 κ=1 α=0.5 the lowest gauge mode (1.597e-2) sits below λ_gap (2.204e-2), so ξ = 1 is unusable for counting; physical modes agree with the code's ξ to ≤ 1.9e-9 / 1.5e-8 abs; near-zero cutoff on |λ|/λ_gap is a PLACEHOLDER pending final hash; λ_gap rule = first |λ| > 100× lowest [assumed]); C5 n=2 κ=1 moduli metric implemented (F(d) from gauge-orthogonal tangent, inherited-angle estimate CRUDE), α<1 rows marked graded, α=1 reported only · C7 symbolic recorded · HP1/HP3/HP4 NOT COMPUTED (YET). INSTANTON_TESTS not built (on hold).

## Post-run notes
(blank — no graded run)

## Sign-offs
Aethon: ____ Venus: ____ Helios: ____ NanoRibbon (go): ____

## Known limits (disclosed)
Cone tip r=0 is not a lattice site (central disc flux only). Finite box with fixed outer ring: translations are near-zero, not exact. C5 separation: quadratic penalty on the gauge-invariant moment M = Σ(1−|Φ|²)r²cos2φ dA. FROZEN 15 Oct ~18:45 BST: weight 10, target = the product-ansatz seed's M at d [assumed]; tuned ONLY on the α = 1 control (24×24, R = 8, 2000 its), against the unconstrained coincident E_ref = 6.2639 (2π = 6.2832). Tries (E/E_ref at d=2, d=4; moment miss): w=1e3 seed 1.0532, 1.0397 (stiff, unrelaxed); w=10 seed 1.0001, 1.0000 (≤1.6e-5) ← chosen; w=0.1 seed 0.9997, 0.9990 (miss ~1e-3); w=1e3 pre-relaxed target 1.0272, 1.0287; w=10 pre 0.9996, 0.9979; w=0.1 pre 0.9995, 0.9978. Known weakness: F(d) not monotone in the smoke rows. C4/HP2 grids 48/64/80/96 (Lanczos).

## Run options
`--workers N` (default 1): C4 cases and HP2 series in N processes. Graded launch HELD (instanton run first, RAM clash); cone run will pin to a new Helios hash.

## Venus guard (xi_guard.py DC3CF39D, scratch H5, box, grid 48, 15 Oct ~18:50 BST)
Penalty 5/λ_min vs 10/λ_min, cases (n=1, κ=2, α=0.75) and (n=2, κ=1, α=0.5): near-zero count 7 = 7 and 4 = 4; all 24 window modes match to 4 s.f. (max |diff| 7.3e-12); gauge leak ≤ 5.0e-7. XI_GUARD PASS. Note: the placeholder λ_gap rule (100× lowest) counts 7 'near-zero' modes in case 1 (up to 1.07e-1); the counting rule itself still needs fixing before C4 counts are read.

## Gauge sector [hive proposal, untested] (rev 11) — REPORT-ONLY, never graded, never in the near-zero count
run.py writes a GAUGE-SECTOR column block in c4_modes.csv: μ_min(GᵀG), μ_eff = λ_gauge/ξ on pure-gauge directions at ξ = 1, 5/λ_min, 10/λ_min, a mixing flag (spread > 1e-6 relative [assumed]), and μ_min(α)/μ_min(α=1) on the same grid. The rev-10 guard (5 vs 10 /λ_min, grid 48) runs before C4 in run.py; fail ⇒ C4/HP2 count rows report-only.
Scratch evidence (gauge_sector.py, box, grid 48; out_scratch/gauge_sector_SCRATCH_hive_proposal.json):
| case | μ_min | μ_eff ξ=1 / 5 / 10 | ξ=1 gauge in window | below λ_gap | μ(α)/μ(1) |
|---|---|---|---|---|---|
| n=1 κ=2 α=0.75 | 1.00509e-1 | 1.005107e-1 / 1.005094e-1 / 1.005094e-1 | 5 | 3 (λ_gap 1.2527e-1) | 0.68480 |
| n=1 κ=2 α=1 | 1.46773e-1 | 1.467435e-1 / 1.467719e-1 / 1.467723e-1 | 5 | 0 (λ_gap 5.9092e-2) | 1 |
| n=2 κ=1 α=0.5 | 1.59707e-2 | 1.597679e-2 / 1.597072e-2 / 1.597071e-2 | 5 | 1 (λ_gap 2.2037e-2) | 0.36838 |
| n=2 κ=1 α=1 | 4.33535e-2 | 4.335359e-2 / 4.335346e-2 / 4.335346e-2 | 5 | 1 (λ_gap 4.5660e-2) | 1 |
MIXING FLAG: raised in all four cases (spread 1e-6–2e-4 relative, largest at ξ = 1). Likely cause: the background is not exactly stationary (|grad| 1e-3–4.5e-3), so H·(Gε) ≠ 0; the penalty runs agree with each other to ≤ 3e-7 relative. Not established — flagged, not explained away.
HP2 guard (5 vs 10, n=1 κ=1, α = 1/0.75/0.5, grid 24, 8 levels): 24/24 rows identical at 4 s.f. with identical tracking labels — PASS.
Correction: my earlier note that the n=1 ξ=1 lowest gauge mode sat "above λ_gap (4.73e-2)" used the wrong gap; with run.py's placeholder rule λ_gap = 1.2527e-1 and 3 gauge modes sit below it.

## Rev 12–15 rules implemented (Venus/Helios)
- Stationarity: every background is L-BFGS-relaxed then Newton–Krylov polished (MINRES on H + ξGGᵀ). |grad|₂ reported on every C4/HP2 row; a row is 'row ok' only if |grad|₂ ≤ |λ|/10 (non-zero modes) or ≤ τ₀/10 (counted modes), else report-only.
- τ₀ (100×-lowest rule retired): α = 1 control on the same grid, known zero-mode count K (2n at κ = 1, else 2), relaxed by 10× gradient cuts until a cut changes the largest zero-mode |λ| by < 2×, or to the solver floor ('stopped at solver floor', tagged [floor-limited], floor reported next to each count). τ₀ = 10× that |λ|, frozen before α < 1 rows; control count ≠ K ⇒ τ₀ NOT COMPUTED (YET), counts report-only. α < 1: count |λ| ≤ τ₀; any eigenvalue in [τ₀/3, 3τ₀] ⇒ undecided.
- ~~Levels-off fail test (rev 15, gradient cuts)~~ SUPERSEDED by the rev 16 grid-refinement fall test (rev 17 CA9D5CBC, CHANGES EBA72AF3, pinned; per-grid control must reproduce K or that grid's τ₀ is NOT COMPUTED (YET) and the fall test is not applied). τ₀ is set per grid from that grid's own α = 1 control (48/64/80/96). On the finest grid, each counted mode needs fitted order p_i ≥ 0.5·p_c (least-squares slope of −log|λ| vs log N over all grids; p_c the same for the control's zmax) AND total fall |λ|₄₈/|λ|₉₆ ≥ 2 (whole span, not per step). Any control zmax ≤ 10 × 1e-13 ⇒ undecided. Failures go in c4_candidate_lifted_modes.csv; summary in c4_grid_fall_test.csv. Negative α < 1 modes are tagged [hive proposal, untested].
- Graded/report-only switch for floor-limited counts: removed (Venus).
## Stationary-point scratch results (stationary_check.py, box, grid 48; out_scratch/stationary_check_SCRATCH.json) [SCRATCH H5]
| case | |grad|₂ after L-BFGS → polish | lowest |λ| | mixing at stationary point | τ₀ / count |
|---|---|---|---|---|
| n=1 κ=2 α=1 (control) | 8.58e-7 → 2.08e-13 | ±5.35e-5 (×2) | no (spread 2.4e-15) | K=2, τ₀ = 5.348e-4 |
| n=1 κ=2 α=0.75 | 1.34e-6 → 3.16e-14 | −1.103e-3 (×2) | no (5.2e-15) | count 0, UNDECIDED (−1.103e-3 within 3× of τ₀) |
| n=2 κ=1 α=1 (control) | 1.26e-6 → 7.77e-14 | −4.40e-5 (×2), −4.22e-5 (×2) | no (3.0e-15) | K=4, τ₀ = 4.403e-4 |
| n=2 κ=1 α=0.5 | 2.03e-6 → 2.12e-13 | −1.945e-5 (×2), −1.734e-5 (×2) | no (2.8e-14) | count 4, not undecided |
The earlier mixing flag came from incomplete relaxation; it is gone at the stationary point. μ(α)/μ(1) at stationarity (report-only): 0.68399, 0.36829. The n=2 −3.104e-5 mode is −1.945e-5 / −1.734e-5 (two pairs) at the stationary point.
RESOLVED (rev 16): the two-cut gradient test was always undecided because eigenvalues don't move at stationarity; replaced by the grid-refinement fall test above. Scratch smoke (12/16/20, H5): control p_c = 3.750 (zmax 3.748e-3, 1.269e-3, 5.522e-4). α=0.75 modes −9.67e-3, −5.26e-3, −3.38e-3 give p = 2.06 and total fall 2.86, which would pass. In the smoke the finest grid is undecided by the 3τ₀ band, so the test reports 'not applied'. The pass, lifted and near-floor paths were unit-checked on these numbers.

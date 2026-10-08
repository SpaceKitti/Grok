# SM1 Part A: input-free stages (JOB_SM1A)

**Status: Venus pre-run maths PASS on 712EF4A8, with her four build edits (E1-E4) and her answers to A2-A9 and Q16 folded in below, each tagged [Venus]. Next: Aethon builds. Does not depend on Akitti's inputs or AKITTI_POSTS_OCT1-8, but the candidate list may gain rows after the posts are folded in.**

Helios, 2026-10-08. Split from the parent draft `JOB_SM1_FILTER_SPEC.md` (SHA-256 prefix 3D19F785, kept unchanged). Part B (`JOB_SM1B_SPEC.md`: scoring against Akitti's residuals) is HELD and uses this part's outputs as its inputs.

Framework: `AKITTI_FRAMEWORK_2026-10-08.md`, SHA-256 prefix 6CD5F259 (box `/workspace/lift/`, TrinityOrb `open-problems\`). It is Akitti's own construction, followed as written. **No Akitti input is filled with a guess anywhere in Part A.** The only place her numbers can enter is the single α_ext slot in 0.2, and Part A runs without it.

Tags: [Akitti] her words or construction; [Venus] Venus's convention or check; [standard] textbook or published; [identity] follows by algebra; [computed] printed by an existing run, cited by file and line; [assumed] a toy input; [hive-interpretation]; [Grok-suggested]; [open] not computed anywhere yet; [GR control] a GR reference line, never the lift's gravity. Pronouns: Akitti is she/her. Question numbers Q1-Q16 refer to Part B §5 (`JOB_SM1B_SPEC.md`); section 3 was carried over from the parent and keeps its Q references.

## 0. What Part A does

Part A builds everything that needs no input from Akitti:
- the inventory check;
- the candidate table, with each candidate's zero-mode spectrum, chiral assignment and anomaly data;
- the missing zero-mode counts;
- the α < 1 replacement for the round-sphere 3j (Clebsch–Gordan) table;
- the written-out 4D (I₆) and 6D (I₈, with the Green–Schwarz factorisation) anomaly polynomials per candidate.

It does not score anything against ∫R dA, ∫T_tt dA or the MHD trace; that is Part B. Part A grades only builds and counts, never physics.

### 0.1 Her construction, for reference (verbatim source: framework lines 7-18) [Akitti]
- Exterior, frozen, r > r_c: ds²⊥ = dr² + α² r² dφ², φ ~ φ + 2π, 0 < α ≤ 1, with α = 1 − 4Gμ (so 2π(1 − α) = 8πGμ). G and μ are her measured exterior inputs. The MHD fields Ψ (velocity, magnetic field, density) are known on r = r_c.
- A candidate interior (g_core, T_core, Ψ_core) for r ≤ r_c is kept only if
  - ∫_{D_rc} R[g_core] dA = 2π(1 − α),
  - ∫_{D_rc} T_tt dA = μ,
  - Π(Ψ_core) = Ψ|_{r_c},
  - with C¹ matching at r = r_c.
- Any wrapping, flux or zero-mode assignment that shifts either integral is discarded.
- The lift's gravity is unknown quantum gravity [Akitti]. The scorer never uses an Einstein equation to get one integral from the other.


### 0.2 The single α_ext slot (the only Akitti input Part A can use; absent today)
- `SM1_INPUTS.md` may hold one line `alpha_ext = <value>   [Akitti: <source>]`. run.py reads only this line, and only if it carries an `[Akitti: …]` source tag.
- If the line is absent or untagged, run.py runs on the assumed grid α ∈ {1, 0.8, 0.6, 0.5} [assumed] (Job Four's grid) and prints "α_ext absent: grid-only run".
- If the line is present, run.py adds α_ext as one more column in every α-dependent output, with no code change, and labels every output by its α.
- Today the line does not exist, so the graded Part A run is the grid-only run. No other SM1_INPUTS field is read into any computation; Stage 0 only reports whether each one is present.

## 1. Conventions

### 1.1 Curvature [Venus]
- R = 2K in 2D. The tip deficit is ∫K dA = 2π(1 − α), equivalently ∫R dA = 4π(1 − α) [standard].
- Akitti's R is read as K; her equation is kept as written. (Part A computes no curvature integrals; this is here so the two parts use one convention.)

### 1.2 n conventions [Venus]
Every zero-mode count states its own n convention.

| count | formula | what n means | source (file, line) |
|---|---|---|---|
| Dirac zero modes on round S², U(1) field of charge x = 1 | \|n\| = \|2q\| | n = flux quanta seen by a charge-1 field, (1/2π)∫F; Wu–Yang monopole charge q = xn/2 | Job Two README (9189C7C8) lines 29, 49, 54; RESULTS (FEF2BA79) lines 14-24 |
| Dirac zero modes on the fuzzy sphere (U1) | \|n\| | n = "number of strings, i.e. the monopole charge" (README line 17). Its round-sphere target λ² = (j + ½)² − n²/4 means Wu–Yang q = n/2, the same as Job Two's n at x = 1 | U1 README (0D584792) lines 17, 57-59; RESULTS (232B3059) line 139 |
| Dirac zero modes on the rugby ball (Job Four) | 3 at n = 3 | q = xn/2 = 3/2, the same as Job Two | Job Four README (D28E4934) lines 14-16; RESULTS (BBABA152) lines 104-111 |
| Scalar lowest-Landau-level states (B0 toy) | n + 1 | n = vortex number = flux quanta, B = n/(2R²), q = n/2, l = n/2, so 2l + 1 = n + 1 | B0 README (D0F1A74C) line 15; JOB_LIFT_SPEC (77D663CE) line 86 (N_Φ = 2q; "the toy's n + 1") |
| g = 2 spin-1 lowest level (Ridgway–Weinberg / LNW) | 2n − 1 | n = SU(2) monopole charge, q = n, so the W sees N_Φ = 2q = 2n flux quanta | JOB_LIFT_SPEC (77D663CE) line 85 (count) and line 86 (N_Φ − 1 form) |

(Venus's note placed the scalar n + 1 at LIFT line 85; in file 77D663CE it is on line 86, and line 85 is the spin-1 2n − 1 line.)

**Declared convention, used everywhere in Parts A and B** (confirmed by Venus, A7, including the N_Φ = 2n_RW conversion [Venus]).
- N_Φ = the number of flux quanta the field in question sees = |x| × (1/2π)∫F = 2|q| (Wu–Yang).
- Counts are always computed from N_Φ: Dirac zero modes = N_Φ; scalar lowest level = N_Φ + 1; g = 2 spin-1 lowest level = N_Φ − 1 [standard; identity once converted].
- Conversions on read: the n of Job Two, U1, Job Four and B0 gives N_Φ = |x|·n; an SU(2) monopole charge n_RW gives N_Φ = 2n_RW.
- The flux label n in candidate IDs (S7-S9, R3-R5) is Job Two's n (charge-1 field).
- run.py stores `n_convention` per source and per candidate, converts on read, and stops with an error if any count is formed from an unconverted n.
- Cross-check row [identity]: Job Two's A_z Higgs (x = +2, q = 3, so N_Φ = 6) has spin-weight-shifted lowest level j = 2 with 5 modes (RESULTS lines 198-200). That is N_Φ − 1 = 5, the spin-1 formula. The ALT Higgs (x = 0, N_Φ = 0) has 1 constant mode (RESULTS_alt line 94) = N_Φ + 1.

## 2. STEP A: inventory

Canonical copies are GitHub main (SpaceKitti/Grok, HEAD d740078 when read) and TrinityOrb. Their hashes agree for every SM folder checked (`C:\Users\Akitt\sm-zero-modes-S2`, `sm-rugby-yukawa`, `sm-yukawa-4b-ckm`, `Job4c_rs_anarchy`; `open-problems\U1_fuzzy_sphere_strings`, `open-problems\Bradlow_cap\B0_taubes_base`). Some box copies are older and must not be used as sources: `/workspace/smS2final/RESULTS_alt.md` 2EEF1B88 (pre-wording regeneration; main is 38A2B07C), `/workspace/smS2final/run.py` 8B13816B and README 78EE0C20 (older), and `/workspace/rugby/RESULTS.md` 35CFD24F (main is BBABA152). Line numbers below refer to the main/TrinityOrb files.

"α?" means the dataset has a real conical tip with α < 1 (not just a round sphere). "CG?" means it has a Clebsch–Gordan / 3j table for the zero modes.

| # | dataset (main path) | what it computes | files and hashes (commit) | α? | CG? |
|---|---|---|---|---|---|
| D1 | Job Two, `jobs/sm-zero-modes-S2` | 6D Weyl fields on round S² with U(1)_X flux: zero-mode counts and chirality (n = −4..4), anomaly scan for hypercharges, U(1)_X mixed anomalies, 6D irreducible counts, Yukawa triple overlaps, Higgs spectra; main model, alt model and final (= alt) | README 9189C7C8, RESULTS FEF2BA79, RESULTS_alt 38A2B07C, RESULTS_final 78C1BC24, anomalies.py EFE2723B, monopole.py 99AC267B, overlaps.py 3BFD8603, run.py DCE6413E (f972004) | **No.** Round, smooth S² by construction (RESULTS line 214; README lines 23-24) | **Yes.** Exact triple overlap = product of two 3j symbols (README line 101), sympy wigner_3j against quadrature (RESULTS lines 137-144), Yukawa matrices (RESULTS lines 153-187; RESULTS_alt lines 52-56) |
| D2 | Job Four, `jobs/sm-rugby-yukawa` | alt-model fields on a rugby ball ds² = R²(dθ² + α² sin²θ dφ²); zero-mode count at α = 1, 0.8, 0.6, 0.5; tip exponents; brane-Higgs Yukawa ratios; tilt mixing at α = 1 | README D28E4934, RESULTS BBABA152, run.py 8FA69F08, ratios.png 630FB985 (f972004) | **Yes, as an [assumed] input.** Deficit 2π(1 − α) at both tips (README lines 22-24; RESULTS lines 104-111). α is not derived from a brane action, and there's no back-reaction beyond the deficit (README lines 92-94) | **Partly.** Imports Job Two's monopole.py (Wigner small-d). At α = 1 the j = 1 triplet and d¹(β) are used (RESULTS lines 147-155). At α < 1 SU(2) drops to U(1) (README line 97), and no 3j triple-overlap table exists (only diagonal axial overlaps, RESULTS lines 25-30) |
| D3 | Job 4b, `jobs/sm-yukawa-4b-ckm` | CKM fits with an aligned soft brane plus a tilted narrow brane | README BC001743, RESULTS 9E8D0411, run.py C70AD870 (c480249) | **No.** Round, α = 1 (README line 1 and line 29) | j = 1 rotation D(β) only (README lines 29-40), no 3j table |
| D4 | Job 4c, `jobs/job4c-rs-anarchy` | Akitti's warped-throat flavour (RS anarchy) | README DAB95C99, RESULTS 066D9B4E, run.py C16D5DD9 (4775ac5); spec EAE66844 (`open-problems\01_sm_from_sphere\`, same bytes as `/workspace/JOB_4c_SPEC.md`) | **No.** 5D interval, no S² (README lines 17-19) | No |
| D5 | Job U1, `jobs/u1-fuzzy-sphere-strings` | Ginsparg–Wilson Dirac operator on the N-state fuzzy sphere with n strings: zero modes = \|n\|, chirality +1, index n, rungs = N − n, sector gone at n = N | README 0D584792, RESULTS 232B3059, run.py 851363FB (e84e1a8); same bytes on the box `/workspace/u1/job/` and in `open-problems\U1_fuzzy_sphere_strings\` | **No.** Round fuzzy sphere | d¹(β) check on the n = 3 zero modes (RESULTS line 178), no triple-overlap table |
| D6 | B0, `jobs/b0-taubes-base` | n Abelian-Higgs vortices on a round sphere near the Bradlow cap: energy πn, LLL levels, amplitude-mode gap table | RESULTS AE4E8FFB, README D0F1A74C, run.py 15F2B139, grade E58EFC2F (53e938d, 02e4b43); box `/workspace/b0/graded_RESULTS.md` same bytes | **No.** Round (RESULTS line 8) | No (level counts 2l + 1 only, RESULTS line 80) |
| D7 | B1 outline, `open-problems\Bradlow_cap\JOB_B1_SM_ZEROMODES_SPEC.md` | fermion zero modes at the Bradlow cap (outline only; never specced or run) | AFF0FB0D (TrinityOrb; box `/workspace/bradlow_out/`) | No data | No data |
| D8 | B2, `jobs/b2-vacuum-pressure` | vortex-gas pressure at the Bradlow cap (2D pressure on the sphere, not T_zz) | README 8FEAA480, RESULTS 1EAF64BD (1edf458) | No | No |
| D9 | Job 5d, `jobs/5d-rugby-ball-flux` | Salam–Sezgin/ABPQ rugby ball with branes: N = nαg/g₁ and the flux cap | RESULTS 12E53647, README BDCC8DAE, run.py FF91D4B9 (03e939d) | **Yes, as a parameter.** ε = 4G₆T, α = 1 − ε (RESULTS line 10) [standard: ABPQ §4; GR control] | No (no fermions) |
| D10 | Job 5b, `jobs/radion-5b-tension-casimir` | radion potential with rugby tension and Casimir term | README 9FBE7862 on main (TrinityOrb copy 8767634D differs), RESULTS 6146CF25, run.py 586C6BC8 (7dea7cb) | **Yes, as a parameter.** Tension only relabels the flux: V_α(x; n) = αV₁(x; n/α) (README lines 17, 38) [identity] | No |
| D11 | Job 5c, A1, radion-onshell-filter | flux-share and radion filters, axion | 5c RESULTS F02E9CA9; A1 RESULTS F9F57321; onshell RESULTS 345FB29A | No (5c leaves out brane tension, README line 60) | No |
| D12 | Betti–Berry, `jobs/betti-berry-vacuum-filter` | percolation on the Goldberg lattice GP(m,0) | goldberg.py 404800FA (lines 1-6: 12 pentagons + 10(m² − 1) hexagons), README D779A5BD (line 119) | Lattice disclinations only. Each pentagon in a hexagonal lattice carries a deficit of π/3 [standard; not computed in that job]. No flux and no zero modes | No |
| D13 | Pair A / qg-* / lift-l1 | old lift (cut Hamiltonian, branched double cover = cone excess) and the L1 GR control | various | Excess, not deficit; L1 is GR control | Not SM data |

**Inventory summary.**
- Only D2 (Job Four) puts the SM zero modes on a surface with a real conical tip, and there α is an [assumed] grid (1, 0.8, 0.6, 0.5), not Akitti's measured α.
- D9 and D10 carry α but have no fermions.
- D1, D3 and D5 carry CG data (3j or d¹) but are round.
- **No dataset has both α < 1 and a full Clebsch–Gordan (3j) table.** At α < 1 the round-sphere 3j table no longer applies, because SU(2) drops to U(1). Computing the α < 1 overlap table at Akitti's α is a stage of this job [open].
- D4 (Akitti's own warped throat) and D12 (lattice) are not S² zero-mode data with a deficit. Whether they count is question Q13/Q14.
- Not found anywhere: a brane action or tension value for the rugby tips; any value of G, μ, r_c or Ψ|r_c; any definition of Π; any MHD field on an S² or cone; any occupied-zero-mode (current-carrying) calculation; any full 6D anomaly polynomial I_8 (only irreducible counts exist).

## 3. STEP B: candidates

A candidate is (geometry, flux n, fermion chiral assignment, Higgs assignment, ν^c in/out). Brane-profile shape (top-hat, soft, delta, width σ, tilt β) changes only the Yukawa pattern, not the zero-mode content or the integrals (the profile shape doesn't enter ∫T_tt, only the total tension does). So profiles are recorded as sub-variants, not separate candidates. One exception, kept as a flag: a strictly point-like brane exactly on a conical tip couples to none of the three modes (D2 RESULTS line 114) [computed; boundary-condition choice].

Field content shorthand (D1):
- **ALT**: Q, L at Γ₇ = −1, x = +1; u, d, e, ν at Γ₇ = +1, x = +1; constant scalar Higgs x = 0. Akitti chose this one (D1 README line 234; RESULTS_final line 6).
- **MAIN**: all fermions Γ₇ = −1; singlets x = −1; Higgs is the gauge-field component A_z (D1 RESULTS lines 148-161, 195).

### 3.1 Family S: round S² (α = 1), data D1

| id | assignment | zero-mode spectrum (cited) | chiral assignment (cited) | 4D anomalies (cited) | 6D anomaly data (cited) |
|---|---|---|---|---|---|
| S1 | ALT + ν^c, n = 3 (Akitti's chosen model) | 3 copies each of Q, u^c, d^c, L, e^c, ν^c (RESULTS_alt lines 28-35); Higgs: one constant doublet, M² = μ_H² [assumed], tower l(l+1)/R² (RESULTS_alt lines 92-98); first fermion KK level 2/R, 5 per field (RESULTS_final line 26) | Q, L left; u, d, e, ν right (RESULTS_alt lines 30-35) | SM gauge anomalies cancel with SM hypercharges (RESULTS_alt lines 41-46). U(1)_X over 3 generations: SU(3)²X 0, SU(2)²X 12, Y²X −6, YX² 0, X³ 0, grav²X 0 (RESULTS_alt lines 65-72; RESULTS_final line 54). Gauged SO(3)_KK adds none (RESULTS_final line 57) | tr R⁴: 8 vs 8 Weyl, net N₊ − N₋ = 0 (RESULTS_alt lines 80-84); tr F⁴_SU(3) 2 vs 2 is a build-reproduction count only, not an anomaly condition (E2 [Venus]); reducible part left to Green–Schwarz [standard, not computed] |
| S2 | ALT without ν^c, n = 3 | as S1 without ν^c | as S1 | as S1, except X³ = grav²X = 3 over 3 generations (RESULTS_alt lines 71-72) | tr R⁴ net −1 (RESULTS_alt line 83): irreducible gravitational anomaly left over; a consistency-gate reject in Part B (Q16 [Venus]); S2 + ν^c = S1 |
| S3 | MAIN + ν^c, Higgs A (H_u, H_d at x = +2, j = 2), n = 3 | 3 copies each (RESULTS lines 218-225); Higgs: 5 tachyonic modes per doublet, M²R² = −3 (RESULTS lines 198-203) | doublets left, singlets right (RESULTS lines 220-225) | SM: as S1 (RESULTS lines 62-85). U(1)_X: SU(3)²X 12, SU(2)²X 12, Y²X 10, YX² 0, X³ 48, grav²X 48 (RESULTS lines 108-115) | tr R⁴: all 16 Weyl at Γ₇ = −1, so net N₊ − N₋ = −16 (the file's 16, RESULTS line 122, is the magnitude; E1 [Venus]); consistency-gate reject in Part B (Q16 [Venus]) |
| S4 | MAIN without ν^c, Higgs A, n = 3 | as S3 without ν^c | as S3 | as S3, with X³ = grav²X = 45 (RESULTS lines 114-115) | tr R⁴ net −15 (file magnitude 15, RESULTS line 122; E1 [Venus]); consistency-gate reject in Part B (Q16 [Venus]) |
| S5 | MAIN fermions with singlets at x = +1 (Assignment B), neutral Higgs | 3 copies each, all σ₃ = +1 | **all left-handed**; the Yukawa vanishes by Lorentz symmetry (RESULTS lines 163-166) | not computed for this chirality [open] (the scan assumed SM chirality) | not computed [open] |
| S6 | MAIN + ν^c, Higgs C (j = 3) | fermions as S3; Higgs j = 3 level with 7 modes, M²R² = +3 (RESULTS lines 198-203) | as S3 | as S3 | as S3; Yukawa rank 0 (RESULTS lines 174-188) |
| S7 | ALT + ν^c, n = 1 | 1 copy per field (charge-1 count table, RESULTS lines 14-24, row n = 1) | as S1 | per generation: SU(2)²X 4, Y²X −2, the rest 0 (RESULTS_alt lines 67-72, per-generation column); totals = per generation × 1 [identity] | per generation the same as S1 (the counts are per generation) |
| S8 | ALT + ν^c, n = 2 | 2 copies (row n = 2) | as S1 | per generation × 2 [identity] | as S1 |
| S9 | ALT + ν^c, n = 4 | 4 copies (row n = 4) | as S1 | per generation × 4 [identity] | as S1 |

Notes:
- Negative n gives the mirror orientation with all chiralities flipped (RESULTS lines 16-19); it isn't listed separately.
- Correction to the brief: Job Two does **not** find H − V + 29T = 273 for this toy. It says that condition is for 6D (1,0) supergravity and is **not assumed** here (README line 190; RESULTS line 122). The U(1)_X Green–Schwarz statement is [standard, not computed] (README line 189).

### 3.2 Family R: rugby ball with tip deficit, data D2 (+ D1 code)

All use ALT content and a brane Higgs at the north tip. The job evaluates them at **Akitti's α_ext = 1 − 4Gμ** (an input, Q4). D2's grid α = 0.8, 0.6, 0.5 serves as validation points.

| id | assignment | zero-mode spectrum | chiral assignment | 4D anomalies | 6D anomaly data |
|---|---|---|---|---|---|
| R1 | ALT + ν^c, n = 3, α = α_ext | 3 modes per field at every tested α (m = 1/2, 3/2, 5/2; regularity, normalisability and finite differences agree; RESULTS lines 104-111). Tip exponents p_N = 2m/α − 1, p_S = 2(3 − m)/α − 1 (RESULTS line 112) [identity]. Count at α_ext itself: recompute [open, Stage 1] | as S1: the count lives in the σ₃ = +1 slot, same as α = 1 (RESULTS line 106 onward; σ₃ = −1 count 0) | Same content as S1, so the same 4D numbers [identity: 4D anomalies depend only on the zero-mode content]. Whether the tips add brane-localised anomaly inflow is [open] | Bulk counts as S1 [identity: local]; tip contributions [open] |
| R2 | ALT without ν^c, n = 3, α_ext | as R1 without ν^c | as R1 | as S2 | as S2 (tr R⁴ net −1; consistency-gate reject in Part B, Q16 [Venus]; R2 + ν^c = R1) |
| R3 | ALT + ν^c, n = 1, α_ext | [open]: D2 only ran n = 3; the index theorem says n modes [standard], to be computed | [open] | per generation × 1 [identity] | as S1 per generation |
| R4 | ALT + ν^c, n = 2, α_ext | [open] | [open] | × 2 | as S1 |
| R5 | ALT + ν^c, n = 4, α_ext | [open] | [open] | × 4 | as S1 |
| R6 | MAIN + ν^c, Higgs A, n = 3, α_ext | [open]: not computed on the rugby ball | [open] | as S3 if the content is unchanged | as S3 |

Sub-variant flags for R1-R6 (Yukawa only, not scored): soft or top-hat width σ, with slopes Y_k/Y_0 ~ σ^(k/α) (RESULTS lines 130-141); a delta brane on the tip couples to nothing (RESULTS line 114); a brane carrying its own flux or tension would shift the tip exponent (D2 README line 126) [open].

### 3.3 Family B: Bradlow cap (D6/D7)

| id | assignment | zero-mode spectrum | chiral | 4D anomalies | 6D |
|---|---|---|---|---|---|
| B1 | a unit-charge Dirac fermion in flux n (so N_Φ = n) on B0's vortex background (round sphere), as in the B1 outline | [open] (outline only; draft prediction "count stays n", AFF0FB0D) | [open] | [open] (no SM charges assigned) | [open] |

B0's own zero modes are bosonic vortex moduli (one complex mode per sector k = −n..−1, RESULTS line 6), not fermions.

### 3.4 Data that are not candidates
- U1 (D5): it checks zero-mode counting on a regulated (lattice-like) sphere. It has no SM charges and no α, so it's used as a cross-check of the counts in Stage 1 (count = |n|, RESULTS line 139).
- 4b (D3): same zero modes as D2 at α = 1, so no new assignment.
- 5d/5b (D9/D10): no fermions. They are used only as [GR control] rows for how tension and flux enter (the tension sets the deficit, N = nαg/g₁; RESULTS lines 10-18).
- Goldberg lattice (D12), 4c (D4): see Q13/Q14.

**Candidate count: 16** (S1-S9, R1-R6, B1). Of these, 9 have their spectrum, chirality and 4D anomalies fully on file (S1-S4, S6-S9), and 2 are on file except for the count at α_ext and the tip terms (R1, R2). The other 5 (S5, R3-R6, B1) need [open] computations first.

**Part A note on family R.** In Part A every R row is computed only on the assumed grid α ∈ {1, 0.8, 0.6, 0.5} [assumed]. Read "α = α_ext" above as "α on the grid, plus α_ext when the 0.2 slot holds it". Gate decisions (round versus tipped, etc.) belong to Part B.

## 4. Stages (Part A)

Proposed folder: `C:\Users\Akitt\open-problems\01_sm_from_sphere\SM1_filter\`. Sources are imported read-only with no bytecode, and every source is hashed before and after the run.

### Stage 0: inventory check and input-presence print (graded, build)
- Hash every source listed in section 2 (main/TrinityOrb copies) and compare with the table. Stop on any mismatch.
- Print which `SM1_INPUTS.md` fields are present: α_ext, G, μ (and uncertainties), r_c, r_c/R, Ψ|r_c, pressure, Π, T_b, the gauge normalisation, τ. Print presence only (present / absent / present but untagged). No value except α_ext (0.2) is used anywhere in Part A.

### Stage 1: candidate table → `CANDIDATES.md` (graded, build)
- For S1-S9: recompute counts, chiralities, the hypercharge scan, the U(1)_X sums and the 6D irreducible counts with Job Two's `monopole.py` and `anomalies.py`, and compare each with the cited line in section 3.
- For R1 and R2: reproduce Job Four's grid counts with Job Four's solver.
- One row per candidate, holding: geometry and α; N_Φ per field with its n convention; zero-mode counts per field; 4D chirality; hypercharges; U(1)_X sums; 6D irreducible counts; status of each entry ([computed] with file and line, or [open] → filled in Stage 1b).

### Stage 1b: input-free computations
Count statement [standard]: the index (net chiral count) equals the first Chern number N_Φ, so it doesn't depend on α when no flux sits at the tips.
- **Section form for all spins (E4 [Venus]):** ψ_s = (α sin θ)^(−s) tan(θ/2)^((m − q)/α) sin(θ)^(q/α), with m ∈ ℤ + s.
  - s = 0 is the scalar, s = ½ is Job Four's spinor (README line 31), and s = 1 is A_z.
  - It solves the first-order equation for every s. α drops out of the spin-connection term because the rugby ball's spin connection is α cos θ dφ.
  - At α = 1 these are the spin-weighted harmonics with j = q − s, so C-d's 5 and 1 test them.
- **Tip behaviour (A5, confirmed by Venus) [identity]:** |ψ_s|² ~ θ^(2m/α − 2s) at the north tip and ~ u^(2(N_Φ − m)/α − 2s) at the south tip. Job Four's p_N and p_S (RESULTS line 112) are the s = ½ case.
- For 0 < α ≤ 1, "bounded" and "normalisable" pick the same set of m, so the counts are N_Φ + 1 (s = 0), N_Φ (s = ½) and N_Φ − 1 (s = 1) at every α. **Counts are α-independent for α ≤ 1.** The grid run checks this as a build test.
- For α > 1 the two tests disagree and a boundary condition is needed. Akitti's α ≤ 1 avoids that, but the old lift's excess cone (α > 1) is in that range [Venus].
- A tip brane with tension alone doesn't change the count. A tip flux δ shifts m → m − δ at that tip, and the count changes only when δ crosses a threshold; fractional δ may need a boundary condition. Report-only [open] (A3 [Venus]).

| item | what | runs fully now? | needs a re-run when α_ext exists? |
|---|---|---|---|
| 1b-1 | S-family recompute (S1-S9) | **yes** (round, no α) | no |
| 1b-2 | S5 4D and 6D anomalies (all-left-handed content), with Job Two's anomaly code | **yes** | no |
| 1b-3 | R1/R2 counts, m values, tip exponents (n = 3) | **grid only** | counts: no (α-independent for α ≤ 1, A5 [Venus]); tip exponents and wavefunctions: yes (they carry α) |
| 1b-4 | R3-R5 counts at n = 1, 2, 4 (three methods: regularity, normalisability, finite-difference D² as in Job Four) | **grid only** | counts: no (A5 [Venus]); tip exponents: yes |
| 1b-5 | R6: MAIN content on the rugby ball (singlets at x = −1, so their modes are in the σ₃ = −1 slot) | **grid only** | counts: no (A5 [Venus]); tip exponents: yes; R6's Higgs spectrum on the rugby ball stays [open] |
| 1b-6 | B1: a minimally coupled unit-charge Dirac fermion in flux n (N_Φ = n) on B0's computed backgrounds (B0's ε grid, B0 units, round), count and 4D chirality [identity: index theorem; independent of φ] (A8 [Venus]) | **yes** (round, no α) | no |
| 1b-7 | U1 cross-check: the fuzzy-sphere count = \|n\| (RESULTS line 139), converted to N_Φ | **yes** | no |
| 1b-8 | α < 1 triple-overlap table → `OVERLAPS_ALPHA.md` (below) | **grid only** (α = 1 is the round check) | yes |
| 1b-9 | I₆ write-up per candidate → `ANOMALIES.md` | **yes** | no (A2 [Venus]: a bare deficit adds no anomaly; no candidate has tip chiral fields) |
| 1b-10 | I₈ write-up and Green–Schwarz factorisation per candidate → `ANOMALIES.md` | **yes** | no (A2 [Venus]) |

Optional report-only variants (never graded) [Venus]:
- Jackiw–Rossi (Majorana) zero modes for B1 (A8).
- A gaugino variant of I₈ (A9): one adjoint Weyl fermion per generator, with chirality opposite to the matter. It shifts tr R⁴ and the adjoint tr F⁴, using the E1 sign convention.
- Tip-flux δ shifts of the count (A3).

**1b-8, the α < 1 triple-overlap table.**
- On the rugby ball SU(2) drops to U(1) (Job Four README line 97), so the round-sphere 3j table no longer applies.
- The replacement is the table of fusion overlaps C_α(N₁, m₁; N₂, m₂ → N₃, m₃) = ∫ ψ^(N₁)_{m₁} ψ^(N₂)_{m₂} conj(ψ^(N₃)_{m₃}) dA, for the zero-mode and lowest-level sections the candidates use (charges closing, N₃ = N₁ + N₂ in the declared convention).
- Selection rules: m₃ = m₁ + m₂ [identity: axial symmetry; Job Four RESULTS lines 25-32], **and** spin-weight closure s₁ + s₂ = s₃, counting the conjugate (E4 [Venus]).
- Sections are the E4 forms ψ_s above (s = 0, ½, 1) [Venus], which answers A6.
- Rows needed by the candidates:
  - (a) ALT fermion–fermion–constant-Higgs (the Gram check);
  - (b) the MAIN-A closure Q_L = 1, Q_H = 2, Q_R = −1 (Job Two RESULTS lines 150-159) at α < 1;
  - (c) the general table for N_Φ ≤ 4 needed by S7-S9 and R3-R5.

**1b-9/1b-10, anomalies.**
- **I₆ and the map from Job Two's T = 1 tables (E3 [Venus], answers A1):** I₆ = (1/(2π)³)[…], summed over left-handed Weyl fields. Right-handed fields enter as their conjugates, with all charges flipped. Y is SM-normalised (Q = T₃ + Y, no √(3/5)). F = F_SU(3) + F_SU(2) + Y F_Y + X F_X. The coefficients are:
  - ½ × the table value on tr_□F²_SU(N) F_X (T = 1 means T(r)/T(□));
  - (1/6)ΣX³ on F_X³;
  - ½ΣY²X and ½ΣYX² on the mixed U(1) terms;
  - −(1/24)ΣX on p₁ F_X, with p₁ = −(1/8π²) tr R².
  Every coefficient is the exact rational from Stage 1 after this map.
- I₈ is the 6D polynomial for the 6D Weyl content split by Γ₇, built from [Â(R) tr e^{iF/2π}]₈ [standard: Alvarez-Gaumé–Witten 1984; Green–Schwarz–West 1985]. Sign convention (E1 [Venus]): net = N₊ − N₋, the 6D Weyl count at Γ₇ = +1 minus the count at Γ₇ = −1.
- **Only tr R⁴ is a real irreducible condition in this toy (E2 [Venus]).** For SU(2) and SU(3), tr_□F⁴ = ½(tr_□F²)² [identity; Venus checked it on random su(2)/su(3) elements; it fails for su(4)]. So tr F⁴ for these groups is reducible, and everything except tr R⁴ belongs to the reducible / Green–Schwarz part.
- Graded: the tr R⁴ net N₊ − N₋ must reproduce the file counts with E1 signs: S1 0 (RESULTS_alt line 82), S2 −1 (RESULTS_alt line 83), S3 −16 and S4 −15 (RESULTS line 122 gives the magnitudes 16 and 15). The others are computed new [open → computed here].
- The tr F⁴_SU(3) "2 vs 2" (RESULTS_alt line 84) is kept as a build-reproduction check only. It is not labelled an anomaly condition (E2 [Venus]).
- Reducing I₈ to I₆ on the rugby ball uses ∫K dA = 4πα + 2·2π(1 − α) = 4π, including the tips' delta-curvature, and flux N_Φ. So the reduced I₆ doesn't depend on α. Leaving out the tip delta-curvature would fake a tip inflow (A2 [Venus]) [identity].
- Report-only: when the irreducible parts vanish, test with exact sympy whether the remainder factorises, I₈ = X₄ ∧ X̃₄. Print the factors, or "no factorisation".
- Field content: spin-½ matter only; no gravitino, tensors or gaugini in the graded run, because Job Two isn't supersymmetric (README line 219) (A9 [Venus]). The gaugino variant above is optional and report-only.
- A bare deficit adds no anomaly [identity]. Only a tip brane carrying its own chiral fields adds terms, and none of the 16 candidates has one (A2 [Venus]). H − V + 29T = 273 is the 6D (1,0) supergravity condition [standard], not a Job Two result (README line 190) (A4 [Venus]).

## 5. Pass rules (fixed in advance; not changed after the run)
- **C-a:** S-family recomputed counts, chiralities, hypercharge survivors, U(1)_X sums and 6D counts equal the cited file values exactly (integers and rationals, sympy Rational).
- **C-b:** at n = 3 on the grid, the R1/R2 count and m values equal Job Four RESULTS lines 106-109 exactly, and the three methods agree.
- **C-c:** for n = 1, 2, 4 (R3-R5), R6 and B1, the count equals N_Φ and the three methods agree. Any disagreement is printed as FAIL with the numbers. Nothing is tuned. For B1 this is a build check (index theorem), not physics (A8 [Venus]).
- **C-d:** every count is formed from N_Φ in the declared convention (1.2). The two Higgs cross-check rows reproduce Job Two's 5 (s = 1, N_Φ − 1) and 1 (s = 0, N_Φ + 1), which also tests the E4 sections at α = 1 [Venus].
- **O-a:** at α = 1 the overlaps reproduce Job Two's exact wigner_3j values (RESULTS lines 137-144) to 1e-12 absolute.
- **O-b:** at α < 1, quadrature against closed-form integrals agrees to 1e-9 relative (Job Four's 1D-solve tolerance, README line 74).
- **O-c:** entries that break the m rule are ≤ 1e-12.
- **O-d:** the constant-Higgs Gram row gives 1/sqrt(4πα) at every grid α (Job Four RESULTS lines 16-19) to 1e-12.
- **A-a:** I₆ coefficients are exact rationals equal to the Stage 1 sums, compared after the E3 map [Venus].
- **A-b:** the tr R⁴ net N₊ − N₋ reproduces S1 0, S2 −1, S3 −16, S4 −15 (E1 [Venus]). tr F⁴_SU(3) 2 vs 2 is a build-reproduction check only, not an anomaly condition (E2 [Venus]). The factorisation result is report-only.
- **Build PASS** = all graded items pass. Part A grades builds and counts only, never physics.

## 6. Files (in `SM1_filter\`)
- `README.md`: written before the run, with no computed numbers. It restates the pass rules and the n convention.
- `run.py`: the only code. It reads the 0.2 slot and nothing else from `SM1_INPUTS.md`.
- Generated, never hand-edited: `CANDIDATES.md` (Stage 1 plus 1b counts), `OVERLAPS_ALPHA.md` (1b-8), `ANOMALIES.md` (1b-9, 1b-10).
- Part B reads these three files as its inputs.

**Re-run list once α_ext exists** (no code change; only the 0.2 line is added):
- Re-run: the α_ext column of `OVERLAPS_ALPHA.md` (1b-8; overlaps depend on α), and the tip exponents and wavefunctions in the R rows of `CANDIDATES.md` (1b-3, 1b-4, 1b-5).
- Not re-run: the R-row counts (α-independent for α ≤ 1, A5 [Venus]); `ANOMALIES.md` (A2 [Venus]); the S family, B1 and the U1 check.

## 7. Venus's pre-run check: edits and answers [Venus]
Venus passed the maths of 712EF4A8 before the run, with four build edits, all folded in above:
- E1: the tr R⁴ sign convention N₊ − N₋, so S3 is −16 and S4 is −15.
- E2: tr F⁴ for SU(2) and SU(3) is reducible.
- E3: the I₆ map.
- E4: one section form for all spins, with spin-weight closure.

Her answers:
- **A1** (I₆ normalisation): answered by E3.
- **A2** (tip inflow): a bare deficit adds no anomaly [identity]. Reducing I₈ uses ∫K dA = 4πα + 2·2π(1 − α) = 4π and flux N_Φ, so the reduced I₆ is α-independent provided the tips' delta-curvature is included; leaving it out fakes a tip inflow. Only a tip brane with its own chiral fields adds terms, and none of the 16 candidates has one. So I₆ and I₈ need no re-run for her α.
- **A3** (tip brane with flux or tension): tension alone doesn't change the count. A tip flux δ shifts m → m − δ at that tip, and the count changes only when δ crosses a threshold; fractional δ may need a boundary condition. Report-only [open].
- **A4:** confirmed. 273 is the 6D (1,0) supergravity condition [standard], not a Job Two result.
- **A5:** confirmed [identity]. |ψ_s|² ~ θ^(2m/α − 2s) at the north tip and ~ u^(2(N_Φ − m)/α − 2s) at the south. For 0 < α ≤ 1, bounded and normalisable give the same set, so the counts are N_Φ + 1, N_Φ and N_Φ − 1 at every α (Job Four's p_N and p_S are the s = ½ case). For α > 1 they disagree and a boundary condition is needed; her α ≤ 1 avoids that, but the old lift's excess cone is in it.
- **A6:** answered by E4.
- **A7:** confirmed: the table, N_Φ = 2|q|, and the counts Dirac N_Φ, scalar N_Φ + 1, spin-1 N_Φ − 1, including the 2n_RW conversion.
- **A8:** keep the minimally coupled Dirac fermion. 1b-6 is tagged [identity: index theorem; independent of φ], and C-c for B1 is a build check, not physics. Jackiw–Rossi (Majorana) is report-only and optional.
- **A9:** no gaugini in the graded run (Job Two isn't supersymmetric, README line 219). Optional report-only variant: one adjoint Weyl fermion per generator, opposite chirality to the matter, shifting tr R⁴ and the adjoint tr F⁴, with the E1 sign convention.
- **Q16:** an uncancelled irreducible tr R⁴ is a REJECT at a consistency gate (applied in Part B), not a T_tt flag, because Green–Schwarz can't remove it [standard]. A completion with extra matter would be a new candidate row with its own T_tt [open]. S2 + ν^c = S1, and R2 + ν^c = R1. Part A only computes and reports the tr R⁴ net; Part B applies the gate.

No Part A open points remain for Venus's pre-run check.

# IT1b on the fuzzy cone — plan V4 (Venus, 2026-10-29) — HIVE PROPOSAL, UNTESTED — STATUS: FROZEN
PAPER ONLY. No code, no runs. Continues IT1b (not a separate project), per Akitti via NanoRibbon.
Signed: Venus. Helios co-sign of V4: PENDING. Helios co-signed V3 (IT1B_FUZZY_V3_HELIOS_COSIGN.md d791b25f). NanoRibbon: pending. Base: V3 1dbf2ec0 (copied below unchanged except this header). §9 replaces the NOT ADOPTED list (§0b); all pass/fail bands are frozen and unchanged.

## 0. Built on Akitti's notes
- AKITTI_FRAMEWORK_2026-10-08 [Akitti]: transverse cone for r>r_c with a FINITE core r≤r_c, α=1−4Gμ, C¹ matching. → the tip is a core region, not a point.
- AKITTI_POSTS_OCT22-28 ~1182–1189 [Akitti account]: cone singularity resolved by fuzziness ("same shape", not identical).
- Akitti post 24 Oct 15:24 [Akitti]: instanton size-locking calibration, ρ=3a, 5% band, over-improved flow did not help.
- CONE_TIP_NOTE [Akitti]: "the cone is a clue".
- AKITTI_POSTS_OCT22-28 ~161 (research update, her account): point-like core b.c. is a choice; "a finite-radius core is the next thing to try".
- Hive inputs: IT1B_FIX2_CLAMP_SPEC_V2 ADDF9A3B, IT1B_FIX2_LOOP1, D4_V2, IT1B_UNDECIDED_SUMMARY, FUZZ_PLAN_V6 770dd81b. GROK_BUILD_TASK_IT1B_FIX2.md: NOT FOUND on the box (lives on TrinityOrb it1b_confirm\); its content is not used here.

## 0b. Standard assumptions that contradict her notes — NOT ADOPTED, need her okay
Kept as open choices O1–O5; the plan runs nothing until she picks.
- O1 Sharp cone tip (lattice node at r=0, IT1b). Her framework has a finite core; her fuzzy-cone post wants it fuzzy. Options: (a) fuzzy cap as the core [default proposal], (b) sharp tip as control only.
- O2 Singular-gauge BPST seed (gauge singularity on the tip node, D4 candidate d). Her notes do not specify a gauge. Options: regular gauge / singular gauge as control.
- O3 α=1 (no deficit) in calibration. Her framework has α=1−4Gμ<1. On the fuzzy side only k=2 (α=½) is exact; α=1 has no tip. Choice of α needs her okay.
- O4 Fuzziness scale tied to lattice (λ ~ a) vs to physics (her fuzzy-cone post: G_N). Hive default λ ladder from V6; physical λ open.
- O5 Euclidean flow time as "size flow". Standard; her notes do not define the flow. Kept as the hive's measuring tool only.

## 1. Questions
Q1. Does fuzziness remove IT1b's leftover bulk tip excess X (D2a: X(1/3)=+0.122; D4b: nsub×64 no movement, dΔ/dρ=+0.0087; untested hint of a core effect)?
Q2. Does the instanton's action/size flow change as λ shrinks?

## 2. Setup (reduced model, labelled)
- Transverse plane (r,φ) of IT1b replaced by the cap of fuzzy S²/Z_k with radius R ≫ ρ; x3,x4 as IT1b. SU(2) gauge field in matrix form on the cap. **REDUCED MODEL** for every k≠2 and for any cap-times-plane product; k=2 is the only exact orbifold.
- λ_j = 2R/√(N_j²−1). Ladder from V6 A1: k=2 N_j=2^j(N_0−1)+1, N_0 odd; k=3 N_j=3·2^j+1 (k=3 report-only). ≥4 rungs else UNDECIDED.
- Widths: spectral cutoff R/N ~ λ (primary, p=−1); coherent-state √(Rλ) secondary (V6 A3).
- Seed per O2 choice; ρ=3 in units fixed so ρ/λ_0 = 3 at rung 0 (matches IT1b ρ=3a) — subject to O4.
- Excess defined exactly as D4_V2: E=ρ dΔ/dρ, Δ=S(ε=−1)−S(ε=+1), X=E−E_pred, E_pred=−2(0.4x+0.2857x²), x=(λ/ρ)².

## 3. Caveats (frozen)
- Lemma 1 (V5): the tip coherent state sees only m=0, so anything evaluated exactly AT the tip is k-blind (classically too). Tip-centred diagonal quantities may not be used to claim a k- or cone-effect; use twisted traces (V5 §2) or rings r≥2λ.
- Cutoff-only: the fuzzy Laplacian spectrum is the classical one cut at l≤N−1. Any effect reproduced by the commutative truncated-harmonic control (G-C below) within 10% is labelled "spectral cutoff only" and is NOT physical smoothing.
- Lattice→fuzzy is a change of regulator; a PASS on Q1 shows the fuzzy regulator has no tip excess, not that quantum gravity smooths the tip.

## 4. Frozen gates (in order; earlier fail stops)
- G0 (code): commutators [X^i,X^j]=i(λ)ε X^k and ΣX²=R² to 1e−12; P_k projector idempotent to 1e−12.
- G1 (literature reproduction, BPST): k=1 (no tip, full fuzzy sphere cap), largest rung: S/8π² = 1 within 1% and |Q−1| ≤ 0.02. FAIL >3%. Between UNDECIDED. (Known: fuzzy-sphere YM reduces to commutative YM as N→∞, Steinacker–Szabo hep-th/0701041.)
- G2 (continuum IT1b limit): extrapolated E(λ→0) at k=1 matches E_pred(x→0)=0 within 0.01 absolute; FAIL >0.03.
- G-C (control, always reported): same measurements on commutative truncated harmonics l≤N−1 (no noncommutativity).
- Q1 bands (k=2 primary, regular-gauge seed unless O2 chosen otherwise):
  - REMOVES: |X| at the largest rung ≤ 0.02 AND fit |X| ∝ λ^q gives q ≥ 1.5.
  - DOES NOT REMOVE: |X| ≥ 0.08 at all rungs (within ~35% of D2a's 0.122) OR q < 0.5.
  - Otherwise UNDECIDED. If fuzzy and G-C agree within 10%: label "cutoff only".
- Q2 bands: size-flow ratio r(λ)=ρ(t=0.6ρ²)/ρ0 at ε=−1.
  - CHANGES: |r(λ_max rung) − r(λ_min rung)| ≥ 0.03 and monotone across ≥4 rungs.
  - NO CHANGE: spread ≤ 0.01 across all rungs.
  - Otherwise UNDECIDED. IT1b reference r=0.913 (tip) is reported alongside; action S(t)/8π² every 5 steps reported.
- Fewer than 4 valid rungs: UNDECIDED. Fix-loop cap 3 rounds; spec issues/code bugs not rounds.

## 5. Open-problem status
Fuzzy-sphere YM and its instantons are known (Steinacker–Szabo hep-th/0701041, 0708.4365); orbifold instantons known for C²/Z_n (Kronheimer–Nakajima). 4D BPST instantons on a fuzzy S²/Z_k cone: no paper found in a quick search — UNCHECKED, not claimed open.

## 6. Unresolved
O1–O5 need Akitti. Helios: physics of cap×plane reduced model, choice of E_pred on the fuzzy regulator (is −2(0.4x+0.2857x²) with x=(λ/ρ)² valid? UNCHECKED), H-cost estimate. GROK_BUILD_TASK file not on box.

## 7. V2 AMENDMENTS (pre-result; no results exist; not a fix-loop round)
### H1 — fuzzy baseline replaces lattice E_pred
- E_pred = −2(0.4x+0.2857x²) is a Wilson-lattice O(a²),O(a⁴) artefact form. DROPPED as baseline; reported as reference only.
- Baseline: E_pred_fuzzy(x) = c1·x + c2·x², x=(λ/ρ)², fitted at k=1 (no tip). Also fit with a free c0·√x term (the λ¹ term); if |c0| > 2σ, report it and use the 3-term form.
- Anti-circularity (Venus, frozen): the k=1 data are used ONCE, to fix c1,c2(,c0). They are never a pass target for Q1. The fit is made on all rungs except the finest; G2 is graded only on the held-out finest k=1 rung: |E_1(finest) − E_pred_fuzzy(finest)| ≤ 0.01 PASS, > 0.03 FAIL, between UNDECIDED. (A residual on the fitted rungs would pass almost automatically with 2–3 parameters on ≤4 points; it is reported, not graded.) After G2, c1,c2(,c0) are refitted on all k=1 rungs and frozen before any k=2 number is read.
- Q1: X_2 = E_2 − E_pred_fuzzy on k=2 rungs; Q1 bands of §4 unchanged, applied to X_2. Fit |X_2| ∝ λ^q on k=2 data only.
### H2 — cap×plane model validity
- Local model valid only for R ≥ 10ρ. V1 line "ρ/λ_0 = 3 at rung 0" is WITHDRAWN (it is incompatible: see ladder below).
- G1 run at R=10ρ and R=20ρ (k=1, finest rung). Curvature shift δ(R) = S/8π² − 1. Frozen check G1-R: δ(10ρ)/δ(20ρ) ∈ [3, 5] (4 ± 25%) PASS; else FAIL (flag: cap model not in its local regime). The 1% G1 band applies at R=20ρ; at R=10ρ it is reported. Note: Helios wrote "else UNDECIDED"; this file follows NanoRibbon/parent brief "else FAIL/flag" — Helios to confirm.
- Topological charge Q computed with the fuzzy trace on the cap. REDUCED MODEL label stays (k≠2 and any product).
### Ladder fix (Venus, approx-as-exact guard, found in this check)
- With R=10ρ (ρ=1): λ=2R/√(N²−1) gives N=7→λ=2.89, x=8.3; N=49→x=0.17. The x-series is not valid at x≫1, so the Helios example ladder N=7..49 leaves only 1 usable rung (fewer than 4 → UNDECIDED by construction).
- Frozen rule: only rungs with x ≤ 0.25 (λ ≤ ρ/2) enter any fit or band. Proposed ladder (A1 rule, N0 odd): R=10ρ: N0=41 → 41, 81, 161, 321 (x = 0.24, 0.061, 0.015, 0.004). R=20ρ (G1-R only, finest rung): N=321, x=0.016. N0 choice needs Helios's okay; ≥4 valid rungs else UNDECIDED.
### H3 — note
- G0 commutator [X^i,X^j]=iλε^{ijk}X^k with λ=2R/√(N²−1): consistent with V6 A1. OK.
### H4 — cost
- Cost ∝ L²·N³·steps. Helios ladder 7→49: (49/7)³ = 343× rung 0. With the ladder fix 41→321: (321/41)³ ≈ 480× rung 0, and rung 0 itself ≈ (41/7)³ ≈ 200× Helios's rung 0. Absolute time: NOT COMPUTED (YET) — timed rung-0 smoke on TrinityOrb after Akitti's go-ahead; if the rung-3 projection > 4 h, report before launching rung 3.
### Unchanged
- O1–O5 remain NOT ADOPTED until Akitti okays. Her open problems stay OPEN. Lemma-1 and cutoff-only caveats stand.
### Venus maths check of H1–H4
- Dims: x, E, δ, X dimensionless; λ, ρ, R lengths. OK. Signs: δ sign not assumed; ratio test uses magnitudes of same sign (opposite signs = FAIL). Approx-as-exact: x-series validity cut added above; 343 = 7³ exact. Circularity: handled by held-out G2 and k=2-only Q1.

## 8. V3 AMENDMENTS (pre-result; no results exist; not a fix-loop round). Supersede §2, §4, §7 where they conflict.
### 8.1 Ladder
- x ≤ 0.25 rule (§7) kept.
- k=2 ladder (this plan only; supersedes V6 A1 doubling here): √2-geometric, odd N = 41, 57, 81, 113. x=(λ/ρ)² at R=10ρ, λ=2R/√(N²−1): 0.238, 0.123, 0.061, 0.031 (Venus verified). λ span 113/41 ≈ 2.76.
- If the Q1 q fit is UNDECIDED solely for lack of λ span, add N=161 (x=0.015) as a 5th rung. Not a new fix-loop round.
- k=3 report-only: N = 40, 58, 79, 112 (all ≡ 1 mod 3). x at R=10ρ: 0.250, 0.119, 0.064, 0.032 — shifted from the k=2 x values, so k=3 is not compared rung-by-rung with k=2. Note (Venus): N=40 gives x = 0.2502, just above the 0.25 cut; it is reported but excluded from any k=3 fit.
- R stays 10ρ and 20ρ (G1-R). At R=20ρ, finest rung N=113: x = 0.125.
- Cost: rung 3 ≈ (113/41)³ ≈ 21× rung 0.
- WITHDRAWN: V2 §7 N0=41 doubling ladder (41,81,161,321) and its 480× / 200× figures.
### 8.2 G1-R band (replaces §7 wording)
- Ratio δ(10ρ)/δ(20ρ): PASS in [3, 5]; UNDECIDED in [2, 3) or (5, 6]; FAIL + flag outside [2, 6] (including opposite signs).
### 8.3 Run time
- NOT COMPUTED (YET). IT1b lattice timings are not a valid basis (different regulator and cost law).
- Timed rung-0 smoke on TrinityOrb after Akitti's go-ahead: N=41, R=10ρ, a few hundred flow steps. Project the full run by N³; if > 4 h, report to Akitti before launch.
### 8.4 Unchanged
- O1–O5 NOT ADOPTED; her open problems stay OPEN; Lemma-1 and cutoff-only caveats; held-out G2 and k=2-only Q1 (anti-circularity); REDUCED MODEL labels.

## Helios co-sign note on V3 (d791b25f)
- k=3 N=40 (x=0.2502): reported, excluded from any fit. Agreed.
- R=20ρ rungs feed only G1-R (no Q1/Q2/G2 use).

## 9. Setup choices (decided by Venus + Helios from Akitti's notes) — replaces §0b NOT ADOPTED list
Hive decisions resting on her notes (hive proposal); per the brief relayed to Venus they need no further input from her. No band changes.
- O1 (Akitti's own decision, as relayed): the tip is a fuzzy core. A sharp tip is used only as an internal control, never as the model. Reason: her bulk-cone fuzziness post (24 Oct) and her 8 Oct framework's finite core.
- O2: regular-gauge (smooth) seed. Reason: her 8 Oct framework has a finite core with a smooth (C¹) join. The singular-gauge seed is kept only as a control, to separate seed error from tip error.
- O3: main case k=2, the exact fuzzy cone with a real deficit. Reason: her "the cone is a clue" posts and the deficit in her 8 Oct framework. α=1 (k=1) is only the no-tip baseline for the c1,c2 fit.
- O4: λ is tied to her finite-G_N fuzziness, not the grid; the λ ladder samples that physical scale. Reason: her bulk-cone post (fuzziness at finite G_N). Label: "λ stands for her fuzziness scale; the mapping to G_N is not computed."
- O5: gradient-flow time is a measuring probe only, labelled as such. Reason: her notes do not define a flow; her 24 Oct calibration post uses flow only to measure size. The reported "size flow" is ρ(t)/ρ0 versus λ at a fixed probe time (t=0.6ρ², §4).

# IT1b on the fuzzy cone — plan (Venus, 2026-10-29) — HIVE PROPOSAL, UNTESTED
PAPER ONLY. No code, no runs. Continues IT1b (not a separate project), per Akitti via NanoRibbon.
Signed: Venus. Co-sign: Helios (pending), NanoRibbon (pending). Frozen before any result; changes = new file + new hash.

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

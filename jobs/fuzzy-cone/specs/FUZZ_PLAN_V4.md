# FUZZ_PLAN_V4
**POST-SMOKE CHANGE, derived from maths only, frozen before any ladder rung runs. Signed: Venus. Co-sign: Helios, NanoRibbon (pending).**
Built from FUZZ_PLAN_V4_POSTSMOKE_PROPOSAL.md (2BBF8CE0) plus Helios's agreed points. V3 411C6529, V2 239CDA17 and the proposal are left untouched.
Disclosure: smoke numbers (p≈−0.5) existed before this file was written. Every change below is justified from the maths alone.

## 1. Width model and test B bands
On fuzzy S²_N near a pole, [X,Y]≈iλR, so θ ≈ R²·2/N ≈ Rλ (a local Moyal plane). The minimal length is √θ = √(Rλ), so w/R ~ √(λ/R) ~ N^{−1/2}. The old band [−1.2,−0.8] assumed w~λ (Venus spec slip).
Model p* = −1/2. **PASS** p∈[−0.6,−0.4]. **FAIL** p outside [−0.75,−0.25], or local slopes steepening by >0.3. **UNDECIDED** anywhere in between. These bands apply per rung.

## 2. Test A relabelled
Test A is a code/reproduction check, not evidence. The spectrum is the classical S²/Z_k spectrum cut at l≤N−1, so e(N)~1/N is guaranteed. It is not counted as a finding.

## 3. Primary B proxy: pole LDOS
K_N(t;pole) = Σ_{l≤N−1} |⟨pole|ψ_l⟩|² exp(−t·l(l+1)/R²), where |pole⟩ is the coherent state at the tip. It is compared with the classical cone K_∞(t;pole).
t* is the first t where |K_N/K_∞ − 1| crosses **0.10** (threshold frozen). The width is w = √t*.
Expected: t* ~ Rλ, so w/R ~ N^{−1/2}. Fit p from w/R ∝ N^p and grade it with §1.
Secondary, report-only: the coherent-state (Berezin) symbol of the Laplacian. The old Berezin twisted-projector proxy gives p=−1/2 analytically, so it is a code check only.

## 4. R2 and R5 (paper reproduction)
Reproduce these at the paper's own example value h_L=1/2, as the paper does. Record the general form √(h_L/h_H). Report eq75's 0.494 vs 1/2 separately as the paper's internal mismatch, not ours.

## 5. Cone angle
Only k=2 (α=1/2) is an exact orbifold. α=1 has no tip. Any other angle is a **reduced model**.

## 6. D(N)
Grade D_raw = ∫_cap P dA·N/(4πR²) against the per-tip value (1/12)(k−1/k). PASS ≤5%, FAIL >15% at N=128, UNDECIDED in between.

## 7. Ladder depth
Drop h=λ/4 and the floor λ≥3h; neither applies to the matrix model. The depth limit is matrix size N, which TrinityOrb has to be able to afford. Any integer N is allowed. The V3 ladder fit rules (L-q, L-h, at least 4 rungs) stand. L-a is a code check per §2. Rungs with N≤20 are reported as "no a_tip".

## 8. Code bugs (not rounds)
- grade_La([]) must return UNDECIDED, not crash.
- R4 is a setup echo of its target and is not a check.
- The R2/R5 formulas must use p_L, p_R.
Fixes are made only once Akitti allows. The code must move to TrinityOrb before any run.

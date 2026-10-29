# VENUS_FUZZ_CODE_CHECK — not-a-toy line check of /workspace/lift/fuzz  [hive proposal, untested]
Checked 2026-10-29 against FUZZ_PLAN_V3.md 411C6529, FUZZ_PLAN_V2.md 239CDA17, VENUS_FUZZY_CONE_SPEC.md 9d50c331.
No sims. Only tiny checks (<1 s: test_A / test_B_width at N=32,64,128, k=2,3; fuzz/ files unedited).

## File hashes (sha256, first 8)
fuzzy_sphere.py ac567a36 | observables.py 7a32cba0 | grading.py dbad1675 | run_fuzz.py 6ee907f2
step1_paper.py 73f982c7 | tests/test_fuzz.py 0213321d | fuzz_config_v2.json 4dfde651 | README.md 823da020

## VERDICT: CHANGES NEEDED (code is algebraically correct; two tests can't fail as built, one crash, one band set for the wrong model)

## Line check: correct
- spin_matrices / X_matrices: [X^i,X^j]=iλ_N ε X^k, ΣX²=R², λ_N=2R/√(N²−1). Matches spec §1. ✓
- invariant_mask: ad(L3) eigenvalue m_a−m_b ≡ 0 mod k. ✓  The spectrum l(l+1)/R², l≤N−1, with m≡0 mod k: ✓ (tested numerically).
- coherent_twist_overlap: |⟨n|e^{iφL3}|n⟩|² = |cos²+sin²e^{iφ}|^{2(N−1)} = (1−sin²θ sin²(φ/2))^{N−1}. ✓
- R9 algebra: at A=p0B, h x²+h_L x+h_L=0, so Im x·√h → √h_L exactly. ✓  R8: ⟨h+n⟩ = h(1+q)/(1−q) = h coth ε. ✓
- R1–R7 values reproduce the targets (π/3, 2.717, 1, π, 2.8018, 0.4456, 0.4939). ✓
- Ladder: N_j=round(√(4R²/λ_j²+1)), λ_actual reported and used in the fit. ✓

## Aethon's 7 points
1. Eq numbering + R9 h_L=1/2 — ACCEPT as a documentation fix (plan 67–81 → paper (4.42)–(4.48)); record the general target Im x = √(h_L/h_H)·p0, with p0/√(2h_H) as the h_L=1/2 case. The code's maths is right. Helios: confirm from the PDF that the paper's example uses h_L=1/2.
2. Tip-term reading — ACCEPT. Constant term = (1/12π)∫_smooth K + Σ_tips (1/12)(1/α−α) = 1/(3k) + 2·(1/12)(k−1/k) = (k²+1)/(6k). Subtracting 1/(3k) is the right way to isolate a_tip*. BUT (not-a-toy) the fuzzy spectrum on A_k is EXACTLY the commutative S²/Z_k spectrum truncated at l≤N−1. So test A only measures truncation, which is Euler–Maclaurin and can't fail: e(N)≈1.3/N (k=2: 0.041, 0.020, 0.010; k=3: 0.048, 0.023, 0.011). Test A checks the code, not physics. It should be relabelled "pre-gate / code check", not counted as evidence that fuzziness smooths the tip.
3. Curvature proxy for B — ACCEPT as a localisation proxy, REJECT as a "curvature" proxy. P depends only on (N,k,θ), not on λ or R, so P = (1/k)Σ_s(1−sin²θ sin²(πs/k))^{N−1} ≈ Gaussian with width θ ~ 1/√N. That makes w/R ∝ N^{−1/2} analytically, so the measured p is a theorem, not a test. It also means the per-rung L-B grades in ladder mode are identical on every rung, so they are not independent evidence. Helios to choose: keep it labelled "coherent-state resolution" (analytic), or use a real curvature proxy (Berezin symbol of Δ, or LDOS near the pole).
4. D(N) normalisation — RESOLVED by hand: ∫_cap P dA·N/(4πR²) → (1/4k)Σ_{s=1}^{k−1} 1/sin²(πs/k) = (1/12)(k−1/k), the PER-TIP heat-kernel tip coefficient, not the deficit δ = 2π(1−1/k). Numbers: k=2 0.1270, 0.1260, 0.1255 → 0.125; k=3 0.2270, 0.2246, 0.2234 → 0.2222. Proposal: grade D_raw against (1/12)(k−1/k) with the 5%/15% bands (the V2 wording "within 5% of δ" compares the wrong quantity). This is post-smoke too, so it goes in V4, not V3.
5. Coherent-state width ~√(Rλ) — TRUE, from the maths alone. Near the pole [X,Y]=iλZ≈iλR, which is Moyal with θ_nc=Rλ, so the minimal length is √(Rλ) and w/R ~ √(λ/R) ~ N^{−1/2}. MY SPEC SLIP: VENUS_FUZZY_CONE_SPEC D2/C-b said the width goes as λ ~ R/N. λ is the radial shell spacing on fuzzy R³ (L2 limit), not the in-sphere localisation length. So the frozen band [−1.2,−0.8] tests the wrong model. POST-SMOKE CHANGE proposed in FUZZ_PLAN_V4_POSTSMOKE_PROPOSAL.md. It doesn't edit V3. Helios must weigh in.
6. N integer — ACCEPT, with no extra constraint. Any integer N≥1 (N=2j+1, half-integer j allowed). For even N, g^k = −1 on states, but the adjoint action has order k, so A_k is fine for every N, k. Ladder rounding is handled and reported. V3's h=λ/4 grid and its floor λ≥3h mean nothing in a matrix model, so they should be marked N/A.
7. Test A empty for N≤20 — CORRECT. lo=10λ² < hi=N²λ²/40 iff N>20. N_set {32,64,128} is unaffected. BUG: in ladder mode, if every rung has N_j≤20, grade_La([]) raises ValueError (I reproduced this). It must return UNDECIDED, and there should be a rule that rungs with N_j≤20 count as "no a_tip".

## Other checks
- Hard-coded/tautological: R2 and R5 are fixed formulas that ignore p_L, p_R (valid only at p=1/2; the comment says so; OK if config p=1/2 is asserted). R4 = config phi_hat_2 = target, so R4 can't fail. Mark it "setup echo, not a reproduction".
- Dimensions/signs: no errors found. w/R and D_raw are dimensionless. a_tip* is positive for k>1.
- Approx shown as exact: R9 "Im x = 1/√2" is leading order in 1/h_H; the exact value is √(4hh_L−h_L²)/(2h). The code states this. Coherent overlap is exact; the Gaussian width is my approximation (stated).
- grade_A plateau definition (max−min)/|median| is reasonable; not specified in V2. Accept.

## Needs Helios (physics)
Point 1 (h_L in the paper), 3 (which proxy), 5 (accept V4 band and the √(Rλ) model), 2 (accept A as a code pre-gate), and the hive cone angle (still NOT COMPUTED (YET)).

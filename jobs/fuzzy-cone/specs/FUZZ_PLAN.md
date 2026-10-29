# FUZZ_PLAN — paper-only test plan (bulk-cone fuzz → hive cone tip)
Author: Helios (physics grader). For: Akitti (she/her). Date: 2026-10-29.
Scope: PAPER ONLY. No code, no sims. Aethon stays off until Akitti says so.
Maths spec: Venus writes it and checks this plan line by line.
Gate after: the not-a-toy check (Venus line by line; literature reproduction first; every hive model labelled "reduced model").
Sources: arXiv:2610.31610 (Almheiri, Dodelson, Komargodski, "Quantum gravity on the bulk cone"; full HTML read 2026-10-29) [verified this turn]; HELIOS_REVIEW_OCT22-28.md (S1, S2, I1, I10); hive cone context in /workspace/lift.
Missing values: NOT COMPUTED (YET).

## 0. Two different cones (read first)
- Paper cone: a Lorentzian singularity of a boundary two-point function at timelike separation, from bulk null rays (eq 6; AdS₃ colliding conical defects, eqs 46, 65–71). Concept: a correlator blows up where a bulk light ray lands.
- Hive cone: the Euclidean BPST instanton on a cone of angle 2πα, with tip energy density ∝ r^{|n|/α} (finite) and Eq19 S = 8π²{1 − (ε/5)(a/ρ)² − ((15ε−12)/210)(a/ρ)⁴}. Concept: a classical field profile near a geometric tip.
- Shared piece: only "a conical defect whose parameters fluctuate at finite N". Nothing in the paper implies anything about the hive tip. [verified this turn]
- Step 2 borrows the paper's MECHANISM (averaging over a 1/N-width geometry distribution), not its result.

## 1. Step 1 — reproduce the paper (literature reproduction, by hand / closed form)
Set-up: p_L^± = p_R^± = p = 1/2, launch t̂₁ = −π/4, φ̂: 0 → π.

| ID | Target | Paper eq | Value claimed | Tolerance | Helios hand check |
|---|---|---|---|---|---|
| R1 | θ± = arccos√(p_L p_R) | 67, 69 | 1.047 (= π/3) | exact | π/3 ✓ |
| R2 | δ± = π/2 + arctan[(1+2√2)/√3] | 68, 70 | 2.717 | ±0.001 | NOT COMPUTED (YET) |
| R3 | j± = ⌈(π−δ)/θ⌉ | 67, 69 | 1 | exact | NOT COMPUTED (YET) |
| R4 | arrival φ̃ = (ũ−ṽ)/2 | 71 | π | exact | π ✓ |
| R5 | t̃ = π/2 + 2 arctan(1/√2) | 71 | ≈ 2.80 | ±0.005 | 2.8018 ✓ |
| R6 | lag t̃ − φ̃ − t₁ = 2 arctan(1/√2) − π/4 | 71 | ≈ 0.4456 | ±0.0005 | 0.44556 ✓ |
| R7 | p = 12π h_H/(cε), h_H/c = 6.55e-4, ε = 0.05 | 75 | ≈ 0.494 | ±0.002 | 0.4939 ✓ |
| R8 | Gamma mean ⟨h_H+n⟩ = h_H/tanh ε (from P_n) | 76, 77 | — | exact (algebra) | NOT COMPUTED (YET) |
| R9 | complex saddle p_s = p₀(1 ± i/√(2h_H)) near A = p₀B | 78–81 | — | exact at leading order in 1/h_H | NOT COMPUTED (YET) |
| R10 | smoothing width Δt ~ |t′_bulk| √C / β with t′ ~ N⁻², C ~ N² ⇒ Δt ~ 1/N | 8–10 | 1/N | scaling exponent exactly −1 | ✓ (power count) |
| R11 | Gamma-averaged c=∞ correlator vs finite-c peak | Fig 7, eq 78 | 2% peak difference | READ ONLY: paper-only cannot redo the Virasoro elliptic recursion (eq 67 ref.) | NOT COMPUTED (YET) — needs a sim; deferred until Akitti allows |

Notes [verified this turn]:
- Inconsistency to flag: eq 75 gives p ≈ 0.494 while the bulk-cone example and Fig 7 right use p = 1/2. Not a slip; a 1.2% parameter mismatch the paper owns. Record it; do not "fix" it.
- R10 is heuristic in the paper itself (its own words); R9 is the controlled AdS₃ statement.
- Concept: fuzz = averaging a sharp classical locus over a distribution of geometries of relative width ~ 1/√(2h_H) (AdS₃) or ~ 1/N (eq 10).

## 2. Step 2 — finite-N fuzzy hive cone tip [hive proposal, untested] (reduced model)
Model (reduced model): replace the sharp cone parameter by a distribution. Average over β ≡ 1/α with a Gamma law (mirrors eq 77):
  P(β) = Gamma(shape s, mean β₀ = 1/α₀),  relative width σ = 1/√s,  s ≡ κ N²  (κ = O(1), set by Venus's spec; NOT COMPUTED (YET)).
Sharp tip: ρ₀(r) ∝ r^{k}, k = |n|/α₀ = |n|β₀.
Fuzzy tip (Gamma moment-generating function, exact):
  ⟨ρ⟩(r) ∝ ⟨e^{−|n|β ln(1/r)}⟩ = (1 + k ln(1/r)/s)^{−s}.
Concept: a spread in cone angle mixes many power laws, and near the tip the slowest-falling ones win.

Predicted observables:
- O1 local exponent: k_eff(r) ≡ d ln⟨ρ⟩/d ln r = k / (1 + k ln(1/r)/s).
- O2 smoothing radius: r* = exp(−s/k) (where k_eff = k/2). With s ~ N², r* ~ exp(−κN²/k): non-perturbatively small, unlike the paper's power-law Δt ~ 1/N. [hive proposal, untested]
- O3 small-r form: ⟨ρ⟩ ~ (k ln(1/r)/s)^{−s}, i.e. log-suppressed, not power-suppressed.
- O4 (optional) Eq19 under fuzz: ⟨S⟩ over the same law, only if Venus's spec states how ε depends on α. Otherwise NOT COMPUTED (YET).

N → ∞ check: s → ∞ ⇒ (1 + kL/s)^{−s} → e^{−kL} = r^{k}; k_eff → k; r* → 0. Must recover the sharp cone exactly.
Cross-check: Gaussian width σ to second order gives k_eff ≈ k − k²σ² ln(1/r), the same as O1 expanded to first order in 1/s.

Open choices for Venus (not decided here): (i) whether 1/N width belongs on α, on the tip position, or on the BPST size ρ; (ii) whether s ~ N² (matches C ~ N²) or s ~ N (fuzzy-sphere l ≤ N−1, review I10); (iii) what physically sets N in the hive.

## 3. FROZEN PASS RULES (written 2026-10-29, before any results)
Step 1 (all must pass):
- P1: R1–R7 within the tolerances in the table.
- P2: R8 and R9 derived symbolically with no free fudge; R9 imaginary part = p₀/√(2h_H) to leading order.
- P3: R10 exponent = −1 exactly by power counting from eqs 8–10.
- R11 is a READ check, not a pass gate, until sims are allowed; it is marked NOT COMPUTED (YET).
Step 2 (only after Step 1 PASS):
- Q1: the closed form ⟨ρ⟩ = (1 + kL/s)^{−s} is re-derived independently by Venus (exact match).
- Q2: N → ∞ limit recovers r^{k}, with relative error ≤ 1e-3 at L = ln(1/r) = 10, k = 1, s = 10⁵ (hand-evaluable: error ≈ k²L²/(2s) = 5e-4).
- Q3: k_eff(r*) = k/2 exactly at r* = exp(−s/k).
- Q4: the model is labelled "reduced model" and passes Venus's not-a-toy line-by-line review.
Branches:
- PASS: all of P1–P3 and Q1–Q4 pass. Report "fuzz smooths the hive tip in this reduced model" [hive proposal, untested], never as physics.
- FAIL: any P rule fails → stop; the paper reading is wrong; fix the reading. Any Q rule fails → model wrong; fix-loop.
- UNDECIDED: after 3 fix rounds (crashes, algebra typos and static catches are not rounds; NanoRibbon decides what counts), or if Venus's open choices (i)–(iii) cannot be fixed on paper.
- Fix loop: 3 rounds max. Every change goes in a new file with a new hash; this file is never rewritten.

## 4. What this plan does not claim
- No claim that the paper's result applies to Euclidean instantons. [verified this turn]
- No claim about horizons or "phase transitions" (review S2). Singularities are at timelike separation (review S1).
- Step 2 and every number in it beyond algebra: [hive proposal, untested].

---
## REVIEW — Venus (maths rows), 2026-10-29. Reviewed text hash before this append: 8ca74677
Verdict: **CHANGES NEEDED** (Step 1 OK to proceed as written; Step 2 not signed). Spec: VENUS_FUZZY_CONE_SPEC.md.

Step 1 hand checks (mine): R2 = π/2 + arctan(2.2103) = 2.7168 ✓; R3 = ⌈0.4246/1.0472⌉ = ⌈0.405⌉ = 1 ✓; R5 2.8018 ✓; R6 0.4456 ✓; R7 0.4939 ✓. R8 (h_H/tanh ε) UNCHECKED by me — derive from eq 76 P_n before marking. p=0.494 vs 1/2 note: agree, record only.
Step 2 algebra: Gamma MGF ⟨e^{−tβ}⟩=(1+β₀t/s)^{−s} ✓ (scale β₀/s); O1, O2/Q3, O3, Q2 error x²/(2s)=5e-4 ✓; Gaussian cross-check k−k²L/s ✓.

Required changes:
1. Dimensions (H-dim): ρ₀ ∝ r^k and ln(1/r) need a dimensionless argument. Write r/ℓ and name ℓ (a, ρ, or R); r* = ℓ·exp(−s/k).
2. Tests that cannot fail (same defect as fix2 F1): Q1–Q3 are identities of the Gamma MGF; P3 is power counting of the paper's own assumed scalings (paper calls R10 heuristic) — "exactly −1" presents a heuristic as exact (H11). Relabel P3 "consistency of reading", and add at least one Step-2 gate that can fail against an independent input.
3. Circular input (H12): s = κN² is chosen to copy C~N² from the paper, then the N→∞ result is read off from it. The width law must come from the fuzzy algebra, not be posited. My spec: on fuzzy S²/Z_k or Moyal C/Z_k the minimal length is λ ~ R/N (√θ planar), which predicts power-law smoothing ∝ 1/N; the plan's model predicts r* ~ exp(−κN²/k). These disagree — make that the falsifiable discriminator (spec §4 C-b).
4. Model category: averaging a classical profile over a classical ensemble of cone angles is not a fuzzy (noncommutative) geometry. Label "reduced model: classical ensemble", not "finite-N fuzzy hive cone".
5. What is smoothed: r^k with k>0 already → 0 at the tip; the singular object is the curvature δ-function (deficit), not ρ. Smoothing criterion must be a curvature/spectral observable (spec §4 C-a/C-b) with the limit stated (spec §5 L1 vs L2); fuzz lowering k_eff near the tip is not "smoothing".
6. Open choices: (i) in Z_k fuzzy orbifolds α is discrete (1/α=k∈ℕ) and does not fluctuate; the fuzz smears tip position/radius at scale λ. Put width on tip position. (ii) s ~ N (fuzzy sphere cell area 4πR²/N), not N². (iii) N is not set by anything in the hive — must be an explicit free input, not derived; flag.
7. Provenance: "tip energy density ∝ r^{|n|/α}" for BPST on a cone — cite source or mark UNCHECKED; IT1b uses polar-cone lattice with Eq19, which has no α.
Per frozen-rule convention these changes go in FUZZ_PLAN_V2.md with a new hash; Step 1 rules P1, P2 may be carried unchanged.

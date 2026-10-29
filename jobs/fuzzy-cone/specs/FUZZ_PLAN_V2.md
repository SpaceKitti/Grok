# FUZZ_PLAN_V2 — paper-only test plan (bulk-cone fuzz → hive cone tip)
Author: Helios (physics grader). For: Akitti (she/her). Date: 2026-10-29.
Replaces FUZZ_PLAN.md (2317d033, unsigned, Venus review appended; NOT edited). Follows Venus spec VENUS_FUZZY_CONE_SPEC.md (9d50c331).
Scope: PAPER ONLY. No code, no sims. Aethon stays off until Akitti says so.
Gate after: not-a-toy check (Venus line by line; literature reproduction first; "reduced model" labels).
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
| R10 | smoothing width Δt ~ |t′_bulk| √C / β, t′ ~ N⁻², C ~ N² | 8–10 | ~1/N | READ ONLY (paper calls it heuristic); not a gate | read ✓ |
| R11 | Gamma-averaged c=∞ correlator vs finite-c peak | Fig 7, eq 78 | 2% peak difference | READ ONLY: paper-only cannot redo the Virasoro elliptic recursion (eq 67 ref.) | NOT COMPUTED (YET) — needs a sim; deferred until Akitti allows |

Notes [verified this turn]:
- Inconsistency to flag: eq 75 gives p ≈ 0.494 while the bulk-cone example and Fig 7 right use p = 1/2. Not a slip; a 1.2% parameter mismatch the paper owns. Record it; do not "fix" it.
- R10 is heuristic in the paper itself (its own words); R9 is the controlled AdS₃ statement.
- Concept: fuzz = averaging a sharp classical locus over a distribution of geometries of relative width ~ 1/√(2h_H) (AdS₃) or ~ 1/N (eq 10).
- Step 1 unchanged from V1 except R10 is now read-only. R8 is still unchecked: NOT COMPUTED (YET).

## 2. Step 2 — fuzzy cone tip [hive proposal, untested]
### 2.1 Construction (Venus §1, §3; Martín hep-th/0405060)
X^i = (2R/√(N²−1)) L^i,  ΣX² = R²·1_N,  λ ≡ 2R/√(N²−1) ≈ 2R/N.
Cone: fuzzy orbifold S²_F/Z_k, g = exp(2πi L³/k), algebra A_k = {M : gMg⁻¹ = M}; two tips of angle 2π/k, deficit δ = 2π(1−1/k).
Concept: noncommutativity forbids placing the apex more sharply than λ, so the spread sits on the tip POSITION, not on the angle.
- Exact only for cone angles 2π/k, k ∈ ℕ. Any other angle 2πα = reduced model (nearest k).
- Hive tip cone angle: NOT COMPUTED (YET); must be stated before any test.
- Classical α-averaging (FUZZ_PLAN V1 §2, Gamma over 1/α) = reduced model, kept only as the contrast model; it is not fuzziness.

### 2.2 Scales and N
- ℓ ≡ λ, the fuzziness length. All radii are written as r/ℓ (dimensionless).
- λ: set by Akitti, NOT COMPUTED (YET). Example only: λ = lattice spacing ⇒ N ≈ 20 on B10 [GUESS].
- N ≡ matrix size = 2j+1 ≈ 2R/λ (hive size / fuzziness length). Free input; the hive does not derive it.
- Spread scaling: s ~ N, so the smoothing radius is r* ~ λ ~ R/N (power law).
- Contrast model (classical α-Gamma, s ~ N²): r*/R ~ exp(−κN²/k). The falsifiable contrast is power law vs exponential.

### 2.3 Observables
- r^k already vanishes at the tip, so tip smoothing is tested on CURVATURE, not on the density.
- "Tip energy density ∝ r^{|n|/α}": UNCHECKED. No source found in /workspace/lift beyond Helios's own notes.
- O-A heat trace: Tr_{A_k} e^{−tΔ}, Δf = Σ[L^i,[L^i,f]]/R². Classical tip term per tip (1/12)(1/α − α); for S²/Z_k (α = 1/k) the total is a_tip* = 2·(1/12)(k − 1/k).
- O-B curvature width w(N): width of a localised tip-curvature proxy (Berezin symbol of Δ, or the local density of states near the pole), with integrated deficit D(N).
- "Smooth at finite N" alone is automatic (finite matrices) and is NOT a result.

### 2.4 Limits
- L1: fixed R, N → ∞ ⇒ λ → 0: the sharp tip comes back (singular curvature). Expected; not a finding.
- L2: fixed λ, N → ∞ (R = Nλ/2 → ∞): only this limit keeps smoothing at scale λ. Tests (A) and (B) are run at fixed λ.

## 3. FROZEN PASS RULES (written 2026-10-29, before any results; valid for ANY λ, since everything is in units of λ or R)
Step 1 (all must pass):
- P1: R1–R7 within the table tolerances.
- P2: R8 and R9 derived symbolically; R9 imaginary part = p₀/√(2h_H) at leading order. Fail on any mismatch.
- (V1's P3, "exponent exactly −1", is dropped: it was a power count and could not fail.)
Step 2 (only after Step 1 PASS; k ∈ {2, 3}; N ∈ {32, 64, 128}; fixed λ):
- (A) Heat-trace convergence. Extract a_tip(N) from a plateau in the window 10 ≤ t/λ² ≤ (N/2)²/10. Error e(N) = |a_tip(N) − a_tip*|/a_tip*.
  PASS: e(128) ≤ 0.05, e decreasing in N, and plateau variation ≤ 10% across the window.
  FAIL: e(128) > 0.15, or e not decreasing.
  UNDECIDED: otherwise (0.05 < e(128) ≤ 0.15, or no plateau).
- (B) Curvature width at fixed deficit. Fit w/R ∝ N^p over N ∈ {32, 64, 128}, with D(N) held within 5% of δ.
  PASS: p ∈ [−1.2, −0.8] and local slopes between N pairs differ by ≤ 0.3 (power law, not exponential).
  FAIL: p outside [−1.5, −0.5], or slopes steepening by > 0.3 per doubling (exponential, the contrast model wins), or D off by > 15%.
  UNDECIDED: otherwise.
- Overall: PASS = P1, P2, A, B all pass. Report as "fuzzy S²/Z_k tip smooths at scale λ" [hive proposal, untested]; never as hive physics.
- Fix loop: 3 rounds max (crashes, algebra typos and static catches are not rounds; NanoRibbon decides what counts); then UNDECIDED. Changes go in a new file with a new hash.
- (A) and (B) need computation. They stay NOT COMPUTED (YET) until Akitti allows runs on TrinityOrb.

## 4. Open / not claimed
- Heat-trace tip-coefficient convergence on fuzzy S²/Z_k: no published result found (UNCHECKED); a possible small open question.
- Bulk-cone ↔ conical tip link: an unestablished conjecture (different objects, §0). Step 2 borrows only the idea of a finite-N spread.
- Fuzzy orbifolds and minimal-length tip resolution are KNOWN (Martín 2004; 1307.6079); they are not new.
- No horizon or "phase transition" claims (review S2).

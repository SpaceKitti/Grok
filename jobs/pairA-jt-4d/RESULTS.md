# pairA-jt-4d — RESULTS

**Signed off 2026-09-25:** Venus (maths) and Helios (physics).
Revision 2026-09-25 (D6/D7 map, R2 χ-forward labels, GoldbergHexa note): signed off by Venus (maths) and Helios (physics).

Akitti's build toward JT (AdS₂ sign) and a 4D metric, on the Pair A eigenvalue curve y² = 4v²(ε² − ε_EP²), λ± = λ_EP ± y/2. Two-mode toy.

**no JT dual claimed; no Einstein solution claimed** (R1 geometry is a known Einstein–Maxwell–Λ solution [standard]; not derived from Pair A). No QG Hamiltonian is derived here.

Inputs (numbers only for all geometry; the D6/D7 map reads two RESULTS.md files read-only, see below) [by construction]: ε_EP = 0.51368066, λ_EP = −0.308425i, v = −0.360253, τ_swap = 4π/ε_EP = 24.46339057, Γ = [−ε_EP, ε_EP]; sheets A WRITE, B WRITE, C held. Swap test: branch tracking of y directly (no matrix); the 2×2 stand-in v[[0,1],[ε²−ε_EP²,0]] is used only for the independent F_JT = y²/(4v²) residual (M5).

## Summary

**R1 (AdS2 x S2, r = eps_EP) is the 4D target. R2 is not a target (kept as information only).**

- R sign: 2D JT R = -2 [computed] (negative, AdS₂ sign); 4D R1 R = −2 + 2/ε_EP² = +5.579553 [computed] (positive for ε_EP < 1: the S² curvature 2/ε_EP² = 7.579553 outweighs the AdS₂ −2); 4D R2 R = -2*(6*epsilon**2 - 3*epsilon_EP**2 + 1)/((epsilon - epsilon_EP)*(epsilon + epsilon_EP)) [computed] (at ε = 0: +1.579553; diverges at ±ε_EP).
- F_JT > 0 region vs Γ [computed]: F_JT < 0 on the interior of Γ, F_JT = 0 at ±ε_EP, F_JT > 0 outside Γ — the opposite of pairA-qg-operator's P2 (F = ε_EP² − ε², Euclidean inside Γ).
- Swap cover [computed]: 2π loop swaps (M1), 4π loop returns (M2); smooth horizon period 2π/ε_EP gives cone angle 2π; τ_swap = 4π/ε_EP gives 4π → **swap/return needs a degree-2 cover: the smooth period already gives one; 4π cone [by construction]** (M3).
- A B C [by construction]: A WRITE, B WRITE (the two sheets of y, both lifted); C held — not in the construction.

## JT 2D (jt2d.py)

F_JT = ε² − ε_EP², ds² = dε²/F_JT + F_JT dτ².

- R [computed]: symbolic (sympy, full Christoffel/Riemann) R = -2; formula −F'' = -2; numerical (finite differences, 13 points in [−3, 3] ε_EP) -2.00000001 … -1.99999997. Sign: **negative (AdS₂)** [standard for this F].
- Zeros: ε = -0.51368066, +0.51368066 (= ±ε_EP). F_JT < 0 at every grid point inside Γ: True; F_JT > 0 at every grid point outside Γ: True (6001-point grid on [−3, 3] ε_EP).
- F_JT = +y²/(4v²): residual 2.6e-15 [computed] — the opposite sign of P2's F = −y²/(4v²).
- Horizon: F′(±ε_EP) = ±2ε_EP, surface gravity κ = |F′|/2 = 0.51368066 = ε_EP; smooth period 2π/κ = 2π/ε_EP = 12.231695 [standard].
- Cone angle at each tip (circumference / proper radius, 1e-6 from the tip) [computed]: period 2π/ε_EP → 2.000001π (+ε_EP), 2.000001π (−ε_EP): smooth; period 4π/ε_EP → 4.000003π, 4.000003π: branched double cover (conical excess). Local polar form ε = ε_EP cosh ρ: ds² = dρ² + ε_EP² sinh²ρ dτ² (residuals 4.4e-16, 4.7e-15), so the angle is ε_EP × period exactly.
- Topology [computed]: the Euclidean region F_JT > 0 is two disconnected pieces, ε > ε_EP and ε < −ε_EP, each containing exactly one tip, each noncompact (hyperbolic cigar / disk, K = R/2 = −1). Unlike P2's sphere (which held both tips), no Euclidean piece here contains both tips.
- Gauss–Bonnet on the cut-off disk ρ ≤ ρ₀ (one piece) [identity; computed numerically]:

| period | ρ₀ | bulk ∫K dA | boundary ∫k_g ds | tip cone term 2π − θ | total (= 2πχ, χ = 1) |
|---|---|---|---|---|---|
| 2π/ε_EP (smooth) | 1 | -3.4123 | 9.6955 | +0.000000 | 6.283185 |
| 2π/ε_EP (smooth) | 3 | -56.9738 | 63.2570 | +0.000000 | 6.283185 |
| 2π/ε_EP (smooth) | 6 | -1261.1335 | 1267.4167 | +0.000000 | 6.283185 |
| 2π/ε_EP (smooth) | 10 | -69191.9001 | 69198.1833 | +0.000000 | 6.283185 |
| 4π/ε_EP (τ_swap) | 1 | -6.8246 | 19.3909 | -6.283185 | 6.283185 |
| 4π/ε_EP (τ_swap) | 3 | -113.9476 | 126.5140 | -6.283185 | 6.283185 |
| 4π/ε_EP (τ_swap) | 6 | -2522.2671 | 2534.8334 | -6.283185 | 6.283185 |
| 4π/ε_EP (τ_swap) | 10 | -138383.8002 | 138396.3665 | -6.283185 | 6.283185 |

  [identity; computed numerically]: bulk −ε_EP P(cosh ρ₀ − 1) + boundary ε_EP P cosh ρ₀ + cone (2π − ε_EP P) = 2π for every ρ₀ and P. The bulk term is negative and diverges as the cut-off is removed; the real point is that the −2π cone term is required at τ_swap.

## 4D lift (lift4d.py)

Ansatz [by construction]: ds² = −F_JT dt² + dε²/F_JT + r(ε)² (dθ² + sin²θ dφ²), F_JT = ε² − ε_EP².
Ordinary S^2 (standard theta, phi) is used; GoldbergHexa (Akitti's custom probe lattice) not needed.

R1 (AdS2 x S2, r = eps_EP) is the 4D target. R2 is not a target (kept as information only).

- **R1**: r = ε_EP (constant): ds² = −(ε² − ε_EP²) dt² + dε²/(ε² − ε_EP²) + ε_EP² dΩ₂² — AdS₂ × S² product [standard form].
  - R = -2*(epsilon_EP - 1)*(epsilon_EP + 1)/epsilon_EP**2 = −2 + 2/ε_EP² = 5.579553 [computed] (expected 5.579553); Kretschmann = 4*(epsilon_EP**4 + 1)/epsilon_EP**4 = 61.449616, constant.
  - Exists as a real Lorentzian metric for all real ε ≠ ±ε_EP (outside Γ t is timelike; inside Γ, F_JT < 0, so ε is timelike and t spacelike); ε = ±ε_EP are Killing horizons (coordinate singularities, curvature constant).
  - Euclidean section (t = −iτ): F_JT dτ² + dε²/F_JT + ε_EP² dΩ₂², real Euclidean only where F_JT > 0 (outside Γ). The (τ, ε) plane is the JT cigar: smooth at ε = ±ε_EP with period 2π/ε_EP = 12.231695 (cone 2π); with τ_swap = 4π/ε_EP it has a 4π cone (double cover). [computed, from the 2D cone angles above]
- **R2**: r = ε_EP sin χ, ε = ε_EP cos χ, i.e. r² = ε_EP² − ε²: ds² = −(ε² − ε_EP²) dt² + dε²/(ε² − ε_EP²) + (ε_EP² − ε²) dΩ₂².
  - r is real only for |ε| ≤ ε_EP (inside Γ). There F_JT < 0: ε is timelike, t spacelike; the metric is real Lorentzian for |ε| < ε_EP. Outside Γ r² = ε_EP² − ε² < 0 (sin of an imaginary χ): no real metric. No real Euclidean section either (Euclidean needs F_JT > 0, i.e. outside Γ, where r² < 0).
  - R = -2*(6*epsilon**2 - 3*epsilon_EP**2 + 1)/((epsilon - epsilon_EP)*(epsilon + epsilon_EP)) [computed]; at ε = 0: 1.579553. Kretschmann = 4*(6*epsilon**4 - 6*epsilon**2*epsilon_EP**2 + 2*epsilon**2 + 3*epsilon_EP**4 + 1)/((epsilon - epsilon_EP)**2*(epsilon + epsilon_EP)**2).
  - R2 is a Kantowski–Sachs cosmology inside Γ: with ε = ε_EP cosχ, ds² = −dχ² + ε_EP² sin²χ (dt² + dΩ₂²); χ is forward time, χ: 0 → π, so ε = ε_EP cos χ runs from +ε_EP down to −ε_EP; Big Bang at +ε_EP (χ = 0), Big Crunch at −ε_EP (χ = π) [by construction: χ-forward convention; time-reversal (χ → π−χ) swaps them]; the metric is symmetric under χ → π−χ, so with the other time orientation the Bang is at −ε_EP (spacelike curvature singularities, R ≈ (3ε_EP²+1)/(ε_EP² δ), Kretschmann ∝ 1/(ε_EP−ε)^2.00) [computed]. The bolt test does not apply to a time singularity. (Symbolic check: dε²/F = -1·dχ², −F − ε_EP² sin²χ = 0, r² − ε_EP² sin²χ = 0. Log-log fit for δ = 1e-3 … 1e-7: Kretschmann exponent 2.0000 at +ε_EP, 2.0000 at −ε_EP; R exponent 1.0001; R·δ at δ = 1e-7 = 6.789775 vs (3ε_EP²+1)/ε_EP² = 6.789776. Consistency check of the χ-forward convention (not a derivation) [by construction: χ-forward convention; time-reversal (χ → π−χ) swaps them]: ε(χ=0) = +1.000000000000 ε_EP labelled Bang, ε(χ=π) = -1.000000000000 ε_EP labelled Crunch, dε/dχ = -epsilon_EP*sin(chi), max on (0, π) = -8.069e-04 ≤ 0: PASS; symmetry χ → π−χ: ε_EP² sin²(π−χ) − ε_EP² sin²χ = 0, ε(π−χ) + ε(χ) = 0 [computed]. arrow = chi forward; labels match chi.) Near the Big Bang tip +ε_EP (ε = ε_EP(1 − δ)):

| δ | R | Kretschmann |
|---|---|---|
| 1e-01 | 5.947133e+01 | 2.501766e+03 |
| 1e-02 | 6.703896e+02 | 2.492270e+05 |
| 1e-03 | 6.781173e+03 | 2.493977e+07 |
| 1e-04 | 6.788916e+04 | 2.494174e+09 |
| 1e-06 | 6.789768e+06 | 2.494195e+13 |

  Limits: R → oo, Kretschmann → oo as ε → ε_EP (∝ 1/(ε_EP − ε) and 1/(ε_EP − ε)²). **R2 is singular at ±ε_EP: spacelike curvature singularities (Big Bang at +ε_EP, χ = 0; Big Crunch at −ε_EP, χ = π), not bolts.**
- Einstein tensor G_ab (coordinates t, ε, θ, φ) — **information only; Einstein not the goal**:
  - R1: diag(epsilon**2/epsilon_EP**2 - 1, -1/(epsilon_EP**2*(epsilon**2 - epsilon_EP**2)), epsilon_EP**2, epsilon_EP**2*sin(theta)**2)
  - R2: diag(-3*epsilon**2 + 2*epsilon_EP**2 - 1, (3*epsilon**2 + 1)/(epsilon**2 - epsilon_EP**2)**2, -3*epsilon**2 + 2*epsilon_EP**2, (-3*epsilon**2 + 2*epsilon_EP**2)*sin(theta)**2)
  - R1 mixed components G^a_b = diag(-1/epsilon_EP**2, -1/epsilon_EP**2, 1, 1).
  - R1 = AdS₂×S² is an exact Einstein–Maxwell–Λ solution (Bertotti–Robinson/Nariai family; the near-horizon geometry of an extremal charged black hole with Λ>0) [standard, computed from G_ab]: Λ = (1 - epsilon_EP**2)/(2*epsilon_EP**2) = 1.394888, E² = (epsilon_EP**2 + 1)/(2*epsilon_EP**2) = 2.394888 (residual of G^a_b + Λδ^a_b − E² diag(−1,−1,1,1), all 16 components: 0.0e+00) (convention: G_ab + Λg_ab = 8πT_ab, G=1, T^a_b = (E²/8π) diag(−1,−1,1,1); Λ is convention-independent). This describes the geometry only; no Einstein claim tied to Pair A. That ε_EP = |a−b|/(2|v|) sets the S² radius is [hive-interpretation].
  - R2 is not a vacuum (G = 0) or pure-Λ (G = −Λg) solution; no matter model is proposed for it.

Where each exists:

| ansatz | real Lorentzian | real Euclidean (t = −iτ) | curvature at ±ε_EP |
|---|---|---|---|
| R1 (r = ε_EP) | all ε ≠ ±ε_EP (horizons at ±ε_EP) | outside Γ (F_JT > 0); smooth tip for period 2π/ε_EP, 4π cone for 4π/ε_EP | finite, constant (R = 5.5796) |
| R2 (r² = ε_EP² − ε²) | inside Γ only (|ε| < ε_EP), Kantowski–Sachs cosmology | none | divergent (Big Bang at +ε_EP, χ = 0; Big Crunch at −ε_EP, χ = π) |

## Match (match.py)

| id | test | result | tag | evidence |
|---|---|---|---|---|
| M1 | 2π loop around each tip (complex ε, r = 0.25 ε_EP) swaps the A/B branches of y | **PASS** | [computed] | branch tracking of y = ±√(4v²(ε²−ε_EP²)), 8000 steps: n = 1 at +ε_EP, 1 at −ε_EP (1 = swap); min |y| on the loop 0.2448 > 0 |
| M2 | 4π loop returns them | **PASS** | [computed] | n = 0 at +ε_EP, 0 at −ε_EP (0 = return) |
| M3 | swap/return cover: smooth horizon period 2π/ε_EP vs 4π cone (τ_swap) | **PASS** | cone angles [computed]; 4π cone [by construction, from τ_swap]; τ ↔ arg(ε−ε_EP) identification [hive-interpretation] | cone angle with period 2π/ε_EP = 2.000001π / 2.000001π (smooth); with τ_swap = 4π/ε_EP = 4.000003π / 4.000003π (branched double cover). The swap and return need a double cover. The smooth horizon (period 2π/ε_EP) already is one, in z = √(ε−ε_EP) (near the tip, ρ ≈ √(2(ε−ε_EP)/ε_EP), z² ∝ (ε−ε_EP)e^{2iε_EPτ}); the 4π cone is [by construction, from τ_swap]. Identifying the τ angle with arg(ε−ε_EP) (4π-cone reading) or arg(ε−ε_EP)/2 (smooth reading) is [hive-interpretation]; either way the cover y needs is degree 2 (M1: swap after one turn, M2: return after two). The swap lives on the complex ε curve; each real Euclidean JT piece holds only one tip. |
| M4 | A and B lifted (both WRITE; the two sheets of y); C held | **PASS** | [by construction] | A, B = λ_EP ± y/2 (at ε = 1.25 ε_EP: +0.138791-0.308425i, -0.138791-0.308425i); both enter F_JT = y²/(4v²) and the lift. C is not in the construction (held, untouched). |
| M5 | F_JT = +y²/(4v²) at machine precision | **PASS** | [by construction, numerically confirmed] | max |F_JT − (λ₊−λ₋)²/(4v²)| = 2.6e-15 on 61×21 complex ε in Re ∈ [−3, 3] ε_EP, Im ∈ [−1, 1] ε_EP, with λ± the numerical eigenvalues of the 2×2 stand-in v[[0,1],[ε²−ε_EP²,0]] (λ_EP I dropped: it cancels in the difference). H_A gives the same: (λ₊−λ₋)² = −(a−b)² + 4v²ε² = 4v²(ε²−ε_EP²), with ε_EP = |a−b|/(2|v|), so the stand-in is fair [standard] (sympy: 4v²(ε² − ((a−b)/(2v))²) − (4v²ε² − (a−b)²) = 0). |

swap/return needs a degree-2 cover: the smooth period already gives one; 4π cone [by construction]

## D6/D7 map onto F_JT

What D6 and D7 are (pairA-qg-probe-surface RESULTS.md, read-only):

- D6: "loop starting inside Γ at 0.75ε_EP: the direction of travel is ignored (loss picks the mode)" — probe PASS [computed]; loop r = 0.25 ε_EP around +ε_EP, start/end 0.75 ε_EP. pairA-qg-operator: INHERITED FROM H_A, not from P1: YES.
- D7: "loop starting outside Γ at 1.25ε_EP, slow drive (γT≳20): the direction picks the mode (cw and ccw pick opposite modes)" — probe PASS [computed]; loop r = 0.25 ε_EP around +ε_EP, start/end 1.25 ε_EP. pairA-qg-operator: INHERITED FROM H_A, not from P1: YES.

| row | start ε/ε_EP | F_JT at start | phase at start (y at start) | loop ε range on the real axis (ε/ε_EP) | loop straddles Γ |
|---|---|---|---|---|---|
| D6 | 0.75 | -0.115442 | split-decay (same frequency) (y = +0.000000+0.244805i) | 0.75 – 1.25 | YES |
| D7 | 1.25 | +0.148426 | split-frequency (same decay) (y = +0.277582+0.000000i) | 0.75 – 1.25 | YES |

**regions match NO** — D6 and D7 are the same driven loop (r = 0.25 ε_EP around +ε_EP, spanning 0.75–1.25 ε_EP, so it straddles Γ), labelled only by its start point; the start points do sit at F_JT < 0 (0.75 ε_EP) and F_JT > 0 (1.25 ε_EP), but that is how D6/D7 are defined, tested at two points, not a region map along the loop. [by construction]: D6/D7 are defined by their start point; [computed]: F_JT sign at the start points (negative at 0.75, positive at 1.25 ε_EP), the decay/frequency split there (F_JT = y²/(4v²) < 0 ⇔ y imaginary ⇔ same frequency, different decay: loss picks the mode, D6; F_JT > 0 ⇔ y real ⇔ same decay, different frequency: direction picks the mode, D7), and the loop range 0.75–1.25 ε_EP straddling Γ; [hive-interpretation]: reading D6/D7 as whole F_JT regions. No start points other than 0.75 and 1.25 ε_EP were tested (no drive re-run).

**chirality inherited from H_A, not from F_JT** — F_JT and y² depend only on position, so the static geometry is identical for cw and ccw loops [standard]. The monodromy is a swap, which is its own inverse, so cw and ccw give the same label map [computed: M1/M2 monodromy same both ways]; the D7 direction pick therefore comes from the time-dependent lossy evolution i∂_tψ = H_A(ε(t))ψ, not from F_JT. (pairA-qg-operator D6/D7: INHERITED FROM H_A, not from P1.)

cw/ccw static continuation [computed]: +ε_EP: ccw 1/0, cw 1/0; −ε_EP: ccw 1/0, cw 1/0 (n after 1/2 turns; 1 = swap, 0 = return); same label map both ways: YES; swap then return: YES.

arrow = chi forward; labels match chi — R2: χ forward (0 → π), ε(χ=0) = +ε_EP = Big Bang, ε(χ=π) = −ε_EP = Big Crunch, dε/dχ ≤ 0 [by construction: χ-forward convention; time-reversal (χ → π−χ) swaps them]; the metric is symmetric under χ → π−χ, so with the other orientation the Bang is at −ε_EP. The automated check is a consistency check of the convention, not a derivation.

## Sheets

A: WRITE (lifted). B: WRITE (lifted). C: held — C is not in the construction.

## Tags and scope

[standard]: AdS₂ curvature of F = ε² − ε_EP², surface gravity / smooth period, AdS₂ × S² form. [by construction]: inputs, ansatz, A/B/C status. [computed]: R values, cone angles, Gauss–Bonnet, residuals, branch tracking. [hive-interpretation]: identifying the τ angle with arg(ε−ε_EP) or arg(ε−ε_EP)/2; ε_EP setting the S² radius. [by construction, numerically confirmed]: F_JT = y²/(4v²) (M5). [identity; computed numerically]: Gauss–Bonnet table. [standard, computed from G_ab]: R1 Einstein–Maxwell–Λ. [careful-before-toy]: R2 exists only inside Γ, as a Kantowski–Sachs cosmology (χ forward: Big Bang at +ε_EP, Big Crunch at −ε_EP); R2 is not a target. [by construction: χ-forward convention; time-reversal (χ → π−χ) swaps them]: the arrow and the Bang/Crunch assignment (the metric is symmetric under χ → π−χ). Ordinary S^2 (standard theta, phi) is used; GoldbergHexa (Akitti's custom probe lattice) not needed. D6/D7 map: [by construction] (D6/D7 are defined by start point) + [computed] (F_JT sign and decay/frequency split at the start points, loop range); reading D6/D7 as F_JT regions is [hive-interpretation]. Chirality: static geometry identical for cw/ccw [standard]; cw/ccw label map [computed]; D7 direction pick from H_A's lossy time evolution.
no JT dual claimed; no Einstein solution claimed (R1 geometry is a known Einstein–Maxwell–Λ solution [standard]; not derived from Pair A). No QG Hamiltonian derived. Two-mode toy; geometry uses no files from other folders.

## Loaded folders (read-only, D6/D7 map only)

- `C:\Users\Akitt\pairA-qg-probe-surface` (RESULTS.md D6/D7 rows) and `C:\Users\Akitt\pairA-qg-operator` (RESULTS.md D6/D7 rows).
- SHA-256 of every file in both folders (15 files) before and after: **unchanged**.


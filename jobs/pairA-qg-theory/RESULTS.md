# pairA-qg-theory — RESULTS

**Signed off 2026-09-25:** Venus (maths) and Helios (physics).

Layered audit of a QG-theory stack on Pair A / R1, graded against the criteria fixed in README.md before running. No claim that QG is solved, no JT dual, no Einstein solution derived from Pair A. Ordinary S², no GoldbergHexa. A and B WRITE, C held.

## Grades

| layer | grade | one-line reason |
|---|---|---|
| L1 gravity Hamiltonian | **PARTIAL** | spectrum matches (max eig err 3.6e-16), but route (a) is H_A itself [by construction] and route (b) is an ε-independent unitary similarity of H_A, so no route is independent of H_A |
| L2 action on R1 | **PARTIAL** | S_R1 (reduced Einstein–Maxwell–Λ) written, sourced, and R1 is stationary for it; its on-shell value on the Euclidean piece has no constant relation to ∮λ dε, which stays a choice |
| L3 dissipation | **PARTIAL** | D6-like at 0.75 and D7-like at 1.25 reproduced from H_QG in this folder, but the loss is H_A's (no independent gravity-side origin) |
| L4 Hilbert / measure | **PARTIAL** | C² fiber plus flat √g measure dε on both sides; ε is only a parameter ([H_QG, ε̂] = 0), the biorthogonal norm vanishes at the tips, and outside-Γ states are not normalizable |
| L5 predictions | **PARTIAL** | 1 genuine prediction, of the H_A layer; 0 from the gravity layers (L1, L2, L4, L6). The rest are by construction, identities, fits or standard |
| L6 r from the action | **PARTIAL** | CONSISTENT (circular: couplings chosen from ε_EP): r0 = 1/√(1+2Λ) = ε_EP only because Λ was set from ε_EP |

Signed inputs found: probe-surface SURFACE READY with D1–D7 PASS: True; qg-on-R1 D3/D4 PASS: True; jt-4d R1 numbers: True; drive-return sign-offs: True.

## Numbers (from the handoff seed.py)

- a = 0.12337, b = 0.49348: diagonal damping rates of H_A = [[−i a, vε], [vε, −i b]] (the loss rates of the two uncoupled modes); v = -0.360253. ε_EP = |b−a|/(2|v|) = 0.5136806633, λ_EP = −i(a+b)/2 = -0.308425i; max deviation from the HAVE numbers 3.3e-09 (ε_EP rounding).

## L1 — gravity Hamiltonian

- Route (a): H_QG = λ_EP·1 + i(b−a)/2 σ_z + vε σ_x, the non-Hermitian sector written in this folder. It equals H_A identically (max |H_QG − H_A| = 5.6e-17), so the spectrum match is automatic **[by construction]**.
- Route (b): H_QG = λ_EP·1 + v[[ε, ε_EP], [−ε_EP, −ε]], chosen because (H_QG − λ_EP)² = v²F_JT·1 (residual 1.1e-16). It is a Dirac-type square root of the redshift function F_JT = g_ττ; calling it gravitational is [hive-interpretation].
- Independence test: a constant S with S(H_A − λ_EP)S⁻¹ = H_b − λ_EP exists (null-space residual 6.9e-17, checked at 25 random complex ε: 6.8e-16; cond S = 1.000000, i.e. unitary up to scale). **(b) is the same matrix in new coordinates, not independent of H_A** [computed].
- The map explicitly **[standard, exact]**: H_A − λ_EP = v(−iε_EPσ_z + εσ_x) (residual 2.8e-17); route (b) − λ_EP = v(εσ_z + iε_EPσ_y) (residual 2.8e-17). The rotation σ_x → σ_z, σ_y → −σ_x, σ_z → −σ_y is proper (det O = +1), and it is implemented by S = ½[1 − i(σ_x − σ_y + σ_z)] = exp(−i(π/3) n·σ), n = (1, −1, 1)/√3 (a 120° rotation), S = [[+0.5-0.5i, +0.5-0.5i], [-0.5-0.5i, +0.5+0.5i]], det S = 1.000000, |SS† − 1| = 0.0e+00; Pauli-map residual 0.0e+00. **S H_A S† = route (b): max residual 1.6e-16** over the 451-point grid.

| route | max eig err vs H_A (451 complex ε) | EPs found (real axis) | Re Δλ inside Γ | Im Δλ outside Γ | mean − λ_EP | +ε_EP 2π / 4π (n_A, n_B) | −ε_EP 2π / 4π | reducible to H_A |
|---|---|---|---|---|---|---|---|---|
| (a) | 3.6e-16 | -0.5136806633, +0.5136806633 | 3.5e-18 | 4.4e-16 | 1.2e-16 | [1, 1] / [0, 0] | [1, 1] / [0, 0] | yes (literally H_A) |
| (b) | 7.0e-16 | -0.5136806633, +0.5136806633 | 6.2e-16 | 4.4e-16 | 1.5e-16 | [1, 1] / [0, 0] | [1, 1] / [0, 0] | yes (constant similarity) |

**Max eig err = 3.6e-16** (route (a); (b) 7.0e-16). Route (a) earns the spectral match, but by construction. Neither route is independent of H_A, so **L1 = PARTIAL**.

## L2 — action on R1 spacetime

S_R1 = spherically reduced Einstein–Maxwell–Λ action (Euclidean, G = 1, magnetic charge Q), from I₄ = −(1/16π)∫√g(R − 2Λ − F²) − (1/8π)∮√γK with ds² = g_ab dx^a dx^b + r²dΩ²:
I[g, r] = −¼∫d²x √g [r²R₂ + 2(∇r)² + 2 − 2Λr² − 2Q²/r²] − ½∮√γ r²K. Source: standard spherical reduction to 2D dilaton gravity (Grumiller–Kummer–Vassilevich, Phys. Rep. 369 (2002) 327); the Bertotti–Robinson AdS₂×S² family [standard].
Couplings from pairA-jt-4d: Λ = 1.394888, E² = Q²/r⁴ = 2.394888, so Q² = 0.16674703 (Q is itself set at r = ε_EP).

- R1 is stationary for S_R1: the reduced Euler–Lagrange equations (sympy, gauge f dτ² + h dx², r(x)) on f = x² − c, h = 1/f, r = ε_EP have residual 8.6e-16 at the jt-4d couplings (R₂ = -2). This is the allowed check only [computed]; it is not a derivation from Pair A.
- Loops around an EP must cross Γ: the circle about +ε_EP through the base b crosses Γ at +0.9000 ε_EP (b = 1.10), +0.7500 ε_EP (b = 1.25), +0.5000 ε_EP (b = 1.50), +0.0000 ε_EP (b = 2.00). Those points have F_JT < 0, the Lorentzian / R2 side [careful-before-toy].
- Restricted action: by Cauchy, the once-around ∮λ dε from b collapses onto the real segment [ε_EP, b], which lies entirely in the Euclidean piece (F_JT > 0). S_R1 is evaluated on-shell on the same piece, [ε_EP, b] × τ-circle.

| b/ε_EP | S1 = ∮λ dε (analytic) | S1 numeric | S_R1 bulk (β = 2π/ε_EP) | GH at b | S_R1 total (smooth) | S_R1 total (β = 4π/ε_EP, with cone term) |
|---|---|---|---|---|---|---|
| 1.10 | 0.005752513 | 0.005752513 | 0.082897 | -0.911862 | -0.828965217 | -0.828965217 |
| 1.25 | 0.023227977 | 0.023227977 | 0.207241 | -1.036207 | -0.828965217 | -0.828965217 |
| 1.50 | 0.067931885 | 0.067931885 | 0.414483 | -1.243448 | -0.828965217 | -0.828965217 |
| 2.00 | 0.204105711 | 0.204105711 | 0.828965 | -1.657930 | -0.828965217 | -0.828965217 |

- Fit S_R1 = c·S1 + k over the four b: total (smooth): c = -2.6e-15, k = -0.828965. The total is constant (= −π r0² = −A/4), while S1 varies, so c = 0 **[identity]**: the total ½βr²(b − ε_EP) − ½βr²b = −½r²βε_EP is b-independent by exact algebra. Bulk only: c = 3.6057, residual 5.75e-02 > 1e-8, because the bulk is linear in b and S1 is not.
- **No constant relation exists between S_R1 on the Euclidean piece and ∮λ dε.** ∮λ dε stays **[by construction: action choice]** in the Z toy.
- On-shell S_R1 = −A/4 is a geometric entropy (I = −S at fixed Q) [standard]; ∮λ dε is a base-point-dependent period of the spectral curve; no constant relation is the correct physics.
- Cone convention (used once, in the β = 4π/ε_EP column): ∫√g R ⊃ 2(2π−θ)δ, with θ = ε_EP β the cone angle at the tip.
- The action is β-independent with the cone term [standard] (−½r²βε_EP − ½r²(2π − ε_EPβ) = −πr², the same −0.828965 in both columns), so the 4π/ε_EP identification gets no support from S_R1; it stays [hive-interpretation].
- Extra (not graded): the loop around both tips (no Γ crossing) has |½∮y dε| = π|v|ε_EP² = 0.298637, and the smooth on-shell S_R1 total is −π r0² = -0.828965. Their ratio |v| is constant only because both are ∝ ε_EP², which uses the r0 = ε_EP chart choice [hive-interpretation; not counted]. Handoff history A: Im I = -0.29862325 (≈ π|v|ε_EP²; |Δ| = 1.4e-05).

**L2 = PARTIAL.**

## L3 — dissipation on the gravity side

**L3 = H_A embedded in H_QG (honest)**

Loss operator = anti-Hermitian part of H_QG(a) = −i(a+b)/2·1 − i(a−b)/2·σ_z, identical to H_A's (max difference 5.6e-17). Driven loop i dψ/dt = H_QG(ε(t))ψ, written in loss_qg.py (no H_A or drive.py call at runtime): r = 0.25 ε_EP around +ε_EP, γT = 20, 40, 100, 2 turns, left-eigenvector weights (drive-return convention).

| start ε/ε_EP | γT | turn | ccw from A | ccw from B | cw from A | cw from B |
|---|---|---|---|---|---|---|
| 0.75 | 20 | 2π | B slower-decaying (0.98925) | B slower-decaying (0.78232) | B slower-decaying (0.98925) | B slower-decaying (0.78232) |
| 0.75 | 20 | 4π | B slower-decaying (0.76639) | B slower-decaying (0.67704) | B slower-decaying (0.76639) | B slower-decaying (0.67704) |
| 0.75 | 40 | 2π | B slower-decaying (0.99960) | B slower-decaying (0.80317) | B slower-decaying (0.99960) | B slower-decaying (0.80317) |
| 0.75 | 40 | 4π | B slower-decaying (0.80639) | B slower-decaying (0.69513) | B slower-decaying (0.80639) | B slower-decaying (0.69513) |
| 0.75 | 100 | 2π | B slower-decaying (0.99982) | B slower-decaying (0.99982) | B slower-decaying (0.99982) | B slower-decaying (0.99982) |
| 0.75 | 100 | 4π | B slower-decaying (0.99982) | B slower-decaying (0.99982) | B slower-decaying (0.99982) | B slower-decaying (0.99982) |
| 1.25 | 20 | 2π | A lower-frequency (0.99699) | A lower-frequency (0.99699) | B higher-frequency (0.99699) | B higher-frequency (0.99699) |
| 1.25 | 20 | 4π | A lower-frequency (0.99699) | A lower-frequency (0.99699) | B higher-frequency (0.99699) | B higher-frequency (0.99699) |
| 1.25 | 40 | 2π | A lower-frequency (0.99937) | A lower-frequency (0.99937) | B higher-frequency (0.99937) | B higher-frequency (0.99937) |
| 1.25 | 40 | 4π | A lower-frequency (0.99937) | A lower-frequency (0.99937) | B higher-frequency (0.99937) | B higher-frequency (0.99937) |
| 1.25 | 100 | 2π | A lower-frequency (0.99991) | A lower-frequency (0.99991) | B higher-frequency (0.99991) | B higher-frequency (0.99991) |
| 1.25 | 100 | 4π | A lower-frequency (0.99991) | A lower-frequency (0.99991) | B higher-frequency (0.99991) | B higher-frequency (0.99991) |

- **From H_QG: start 0.75 ε_EP (inside Γ) → D6-like** (slower-decaying mode = sheet B wins, direction ignored). **Start 1.25 ε_EP (outside Γ) → D7-like** (ccw → lower-frequency, cw → higher-frequency).
- Cross-check against pairA-drive-return (outputs/drive.npz, drive_start1p25.npz; 48 weight vectors): max |Δw| = 3.1e-07. Route (b) dynamics at γT = 40 vs route (a): max |Δw| = 1.2e-07 (same physics in a new basis).
- **L3 = PARTIAL**: reproduced, but the loss has no gravity-side origin independent of H_A.

## L4 — Hilbert space / measure

- Fiber: C², dimension 2 (the two modes A, B; C held, not included).
- Measure on ε-space: √|g| of the R1 2D metric in (τ, ε), Euclidean outside Γ (ds² = dε²/F + F dτ²) and in (t, ε), Lorentzian inside Γ (ds² = −F dt² + dε²/F). √|g| = 1 on both sides (checked: 1.000000–1.000000), so dμ = dε dτ (flat in ε) [standard, computed]. No DeWitt minisuperspace measure was built.
- Tips: √|g| stays 1, but the chart degenerates: d = 1e-02: g_εε = 1.885e+02, g_ττ = 5.304e-03, proper distance to the tip = 1.4130e-01; d = 1e-04: g_εε = 1.895e+04, g_ττ = 5.278e-05, proper distance to the tip = 1.4142e-02; d = 1e-06: g_εε = 1.895e+06, g_ττ = 5.277e-07, proper distance to the tip = 1.4142e-03. This is a horizon (coordinate) degeneration with finite proper distance [standard].
- Density: ρ(ε) = ψ̃(ε)ᵀψ(ε) × dμ with the biorthogonal (c-product) pairing, since H_QG is complex-symmetric (max |H − Hᵀ| = 0.0e+00), so left eigenvectors = right eigenvectorsᵀ. The alternative metric operator η = (RR†)⁻¹ is noted. Normalizable: inside Γ (length 1.027361) yes; outside Γ (infinite ε-length) constant fiber densities are **not** normalizable.
- Non-Hermitian inner product at the tips: d = 1e-02: |RᵀR| = 1.945e-01, cond η = 1.037e+02; d = 1e-04: |RᵀR| = 1.973e-02, cond η = 1.027e+04; d = 1e-06: |RᵀR| = 1.973e-03, cond η = 1.027e+06; d = 1e-08: |RᵀR| = 1.973e-04, cond η = 1.027e+08. |RᵀR| ~ d^0.499 → 0 (self-orthogonality) and cond η ~ d^-0.999 → ∞. The inner product breaks at ±ε_EP.
- H_QG acts pointwise in ε: on a grid, [H_QG, ε̂] = 0.0e+00. ε is a parameter, not a quantized coordinate (no kinetic term).
- **L4 = PARTIAL** (more than 2 states: C² ⊗ functions of ε, but ε is not dynamical and the inner product fails at the tips).

## L5 — predictions not fitted

| item | quantity | result | status |
|---|---|---|---|
| P-rate | inside start 0.75 ε_EP: winner = slower-decaying at every γT; purity vs γT | γT 20 2π from A: w = 0.98925 (drive-return 0.98925, drive-sweep 0.98925); γT 20 2π from B: w = 0.78232 (drive-return 0.78232, drive-sweep 0.78232); γT 40 2π from A: w = 0.99960 (drive-return 0.99960, drive-sweep 0.99960); γT 40 2π from B: w = 0.80317 (drive-return 0.80317, drive-sweep 0.80317); γT 100 2π from A: w = 0.99982 (drive-return 0.99982, drive-sweep 0.99982); γT 100 2π from B: w = 0.99982 (drive-return 0.99982, drive-sweep 0.99982) | PREDICTED? no: [by construction] H_QG loss = H_A, so this reproduces drive-return; not an independent prediction |
| P-period | Euclidean τ period on R1 | κ = F'(ε_EP)/2 = 0.51368066 (numerical); smooth β = 2π/κ = 12.231695 vs 2π/ε_EP = 12.231695; τ_swap = 4π/ε_EP = 24.463390; T_H = 0.081755 | [standard; direct consequence of the input F_JT]; 4π/ε_EP is [by construction / hive-interpretation]. Not counted as genuine PREDICTED |
| P-gap | |λ_A−λ_B| ∝ |ε−ε_EP|^p | real, outside: p = 0.5016, real, inside: p = 0.4983, complex ray 45°: p = 0.5012 | FITTED exponent; value 1/2 is [by construction] (y² ∝ F_JT, simple zero). Not genuine |
| P-S | |S1| on one loop vs 2|v|∫√(x²−ε_EP²)dx | b = 1.10 ε_EP: 0.005752513 vs 0.005752513 (|Δ| 6.0e-18); b = 1.25 ε_EP: 0.023227977 vs 0.023227977 (|Δ| 2.7e-17); b = 1.50 ε_EP: 0.067931885 vs 0.067931885 (|Δ| 3.7e-17); b = 2.00 ε_EP: 0.204105711 vs 0.204105711 (|Δ| 8.3e-17) | [identity; computed numerically] (Cauchy collapse). Not genuine |
| P-adiab | (1−w) ∝ (γT)^p at the 1.25 ε_EP start, predicted p = −2 (standard adiabatic theorem: abrupt start/stop of the drive gives a first-order non-adiabatic amplitude ∝ 1/(γT)); fixed in README before running, tolerance ±0.3. At 1.25 ε_EP the spectrum is real after removing the common decay −i(a+b)/2 (PT-unbroken; non-normal, not Hermitian) | **asymptotic exponent p = -2.04 (γT 100→200; -2.0418)**; local exponents 20→40: -2.26, 40→100: -2.10, 100→200: -2.04 (approaching −2 from the steep side); 1−w = 3.013e-03 (γT 20), 6.287e-04 (γT 40), 9.175e-05 (γT 100), 2.228e-05 (γT 200); fit over all 4 points -2.1269 | PREDICTED (exponent not fitted; compared with the in-folder simulation): PASS. Genuine, but H_A-level adiabatic physics, not gravity-side. Caveat: start and stop kicks may interfere (1/T² with an oscillation); four points cannot rule this out; a dense γT scan is a possible upgrade [toy-ready?], not run |
| P-Nariai | second constant-r branch of S_R1 with jt-4d couplings | r² = 0.263868, R₂ = -2.000000 (AdS2 x S2 (Bertotti-Robinson type)); r² = 0.453036, R₂ = +1.164888 (dS2 x S2 (Nariai type)) | [standard: charged Nariai branch; exists for any ε_EP < 1 by construction of the couplings; no Pair A counterpart]. Not counted. It matches neither P2 (R = +2, pairA-qg-operator) nor the jt-4d R2 (Kantowski–Sachs inside Γ) |

**1 genuine prediction, of the H_A layer; 0 from the gravity layers (L1, L2, L4, L6).** The criterion requires ≥ 2, so **L5 = PARTIAL**.

## L6 — r(ε) from the action

- Varying r in S_R1 (reduced equations above, R1 metric): constraint Λr⁴ − r² + Q² = 0 and r-equation −4Λr + 4Q²/r³ − 4r = 0 ⇒ **r0 = 1/√(1+2Λ)**, Q² = (1+Λ)/(1+2Λ)² [computed, sympy]. At the jt-4d Λ: r0 = 0.5136806633 = ε_EP = 0.5136806633 **[identity, given Λ(ε_EP)]**, not [computed].
- Closed forms with s = ε_EP² [identity]: Λ = (1−s)/(2s) (|Δ| 0.0e+00); Q² = s(1+s)/2 (|Δ| 0.0e+00); discriminant 1 − 4ΛQ² = s² (|Δ| 6.9e-17). Roots: r² = s (R1, AdS₂×S², cold extremal; |Δ| 5.6e-16) and r_N² = s(1+s)/(1−s) = 0.453036 (charged Nariai dS₂×S², R₂ = 2(1−s)/(1+s) = 1.164888). Numerically: r_N² = 0.453036 (|Δ| 6.7e-16; ≈ 0.45304 ✓), R₂ = 1.164888 (|Δ| 4.2e-15; ≈ 1.16489 ✓).
- The equations do not fix the horizon constant c in F = x² − c (c-independent: True). For constant r, the horizon position ±ε_EP is gauge (AdS₂ with any c is locally the same) [standard].
- With (Λ, Q²) given and the 2D curvature left free, the constant-r solutions are: r = 0.513680663 (r² = 0.263867824), R₂ = -2.000000: AdS2 x S2 (Bertotti-Robinson type); r = 0.673079163 (r² = 0.453035560), R₂ = +1.164888: dS2 x S2 (Nariai type). The AdS₂ branch is R1.
- Λ = (1 − ε_EP²)/(2ε_EP²) and E² = (ε_EP² + 1)/(2ε_EP²) were chosen from ε_EP in pairA-jt-4d (and the unit AdS₂ radius comes from the unit coefficient in F_JT), so recovering r = ε_EP is circular.
- **CONSISTENT (circular: couplings chosen from ε_EP)** → **L6 = PARTIAL**. r = ε_EP stays the working chart.

## Summary lines

- L1 PARTIAL; L2 PARTIAL; L3 PARTIAL; L4 PARTIAL; L5 PARTIAL; L6 PARTIAL.
- max eig err = 3.6e-16 (route (a), [by construction]).
- From H_QG: 0.75 ε_EP → D6-like; 1.25 ε_EP → D7-like.
- r derived: no, CONSISTENT (circular: couplings chosen from ε_EP).

## Tags

[standard]: spherical reduction, Bertotti–Robinson/Nariai branches, surface gravity/period, −A/4 on-shell form, adiabatic theorem, horizon degeneration. [by construction]: route (a) spectrum match; L3 loss = H_A's; the 4π/ε_EP period; the square-root gap. [identity; computed numerically]: P-S; y² = 4v²F_JT; (H_b − λ_EP)² = v²F_JT. [identity]: L2 fit c = 0; the closed forms of Λ, Q², the discriminant and the roots. [identity, given Λ(ε_EP)]: r0 = ε_EP. [standard, exact]: the SU(2) map S H_A S† = route (b). [standard]: charged Nariai branch; β-independence of the action with the cone term; I = −S. [computed]: all numbers, the similarity test, the reduced equations, the fits. [hive-interpretation]: calling route (b) or the loss 'gravitational'; the big-loop ratio. [careful-before-toy]: EP loops leave the Euclidean section; R1 stationarity is a check, not a derivation from Pair A.

## Loaded folders (read-only)

- `C:\Users\Akitt\pairA-qg-handoff`
- `C:\Users\Akitt\pairA-qg-probe-surface`
- `C:\Users\Akitt\pairA-jt-4d`
- `C:\Users\Akitt\pairA-qg-on-R1`
- `C:\Users\Akitt\pairA-drive-return`
- `C:\Users\Akitt\pairA-drive-sweep`
- SHA-256 of every file (69 files) before any import and after all computations: **unchanged**.

THEORY STACK: (none)

NOT A FULL QG THEORY UNLESS L1 L2 L3 L4 are HAVE


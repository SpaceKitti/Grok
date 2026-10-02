# Job Six: membrane power counting and the x²y² toy — RESULTS

Written only by run.py. Tags: [computed] [identity] [assumed] [assumed input] [standard] [post-hoc]
[finite-size] [grid-step] [prediction] [hive-interpretation].
Python 3.14.7, numpy 2.5.2, scipy 1.18.1, sympy 1.14.0.

Model [assumed input]: H_s = p_x² + p_y² + x²y² + s(xσ3 + yσ1), p = -i∂, box [-L, L]², Dirichlet walls,
s ∈ [0.0, 0.5, 1.0], L ∈ [4, 6, 8, 10, 12], h = 0.08; grading thresholds fixed in run.py before the run.

## Stage A: p-brane power counting [standard]

Derived symbolically with sympy for general p [computed]:
- [T] = p + 1,  [φ] = [T]/2 + [X] = p/2 - 1/2
- NG quartic coupling g₄ of (∂φ)⁴: [g₄] = -[T] = -p - 1; check d - 4([φ]+1) = -p - 1  (agree)
- Polyakov/σ-model coupling g_σ = R/T of φ²(∂φ)²: [g_σ] = 2 - [T] = 1 - p; check d - (4[φ]+2) = 1 - p  (agree)
- Weyl weight of sqrt(-γ)γ^ab: p - 1  (Weyl invariance iff 0)

| p | d = p+1 | [φ] | [g₄] NG (∂φ)⁴ | [g_σ] Polyakov φ²(∂φ)² | Weyl weight | renormalisable | Weyl-invariant |
|---|---|---|---|---|---|---|---|
| 1 | 2 | 0 | -2 | 0 | 0 | yes | yes |
| 2 | 3 | 1/2 | -3 | -1 | 1 | no | no |
| 3 | 4 | 1 | -4 | -2 | 2 | no | no |
| 5 | 6 | 2 | -6 | -4 | 4 | no | no |

Reading: [φ] = (p-1)/2 vanishes only for the string. For p = 1 the static-gauge NG quartic
coupling has dimension -2, but the classically equivalent Polyakov form is a 2D σ-model whose
coupling is marginal (dimension 0) and which is Weyl invariant: renormalisable [standard]. For p ≥ 2
every interaction coupling has negative mass dimension (-(p+1) in NG, 1-p in the σ-model form) and
the Weyl weight p-1 ≠ 0 (Polyakov then needs a cosmological term (p-1)√-γ): non-renormalisable by
power counting and no Weyl invariance [standard].

## Stage B.0: structural identities [identity]

- dWLN (1.5) ↔ H_1: constant spin rotation U with U(xσ3+yσ1)U† = xσ1-yσ2 = [[0,x+iy],[x-iy,0]]:
  null-space singular value 1.4e-16, |U†U-1| = 5.8e-16, max mapping error = 4.4e-16.
  So H_{s=1} is unitarily equivalent to the de Wit–Lüscher–Nicolai model, same spectrum [identity].
- Parity P = σ1⊗(x→-x) commutes with H_s; the two sectors K± are mapped into each other by y → -y,
  so spec(H) = spec(K+) counted twice. Checked on a small grid (L=3, h=0.15) [identity]:
  s = 0.5: max |E_full(pairs) - E_K+|, |E_K- - E_K+| = 1.3e-14;  full H lowest 4: 0.914754, 0.914754, 2.186706, 2.186706
  s = 1.0: max |E_full(pairs) - E_K+|, |E_K- - E_K+| = 2.8e-14;  full H lowest 4: 0.398622, 0.398622, 1.462592, 1.462592
  All later levels are K+ levels; each is a doublet of H.
Operator identity: H_s = (1-s)H_0 + sH_1 [identity].
After the fixed spin rotation, H_1 = Q^2 with Q = σ1 p_x + σ3 p_y + σ2 xy,
and Q^2 = p^2 + x^2y^2 + yσ3 - xσ1, the supersymmetric structure of dWLN eq. (1.5) [identity].
Thus H_1 ≥ 0, and min-max gives E_k(H_s) ≥ (1-s)E_k(H_0); Simon's result makes every s < 1 discrete [standard].

## Stage B.1: valley identity check [identity]

Transverse problem h_y(x) = p_y² + x²y² + s(xσ3 + yσ1) on y ∈ [-3.2, 3.2], h_y = 0.005, 4th-order FD.
Prediction: lowest eigenvalue → (1-s)|x| (oscillator zero point |x| minus spin -s|x|). The yσ1 term
adds a second-order shift -s²/(4(1+s)x²) (hand-derived perturbation theory, shown for comparison, not graded).

| s | x | E_num | (1-s)|x| | E_num - (1-s)|x| | (E_num - (1-s)|x|)·x² | PT: -s²/(4(1+s)) |
|---|---|---|---|---|---|---|
| 0.0 | 4 | 4.00000000 | 4.0000 | -8.367e-10 | -0.00000 | -0.00000 |
| 0.0 | 8 | 7.99999999 | 8.0000 | -6.671e-09 | -0.00000 | -0.00000 |
| 0.0 | 12 | 11.99999998 | 12.0000 | -2.250e-08 | -0.00000 | -0.00000 |
| 0.0 | 16 | 15.99999995 | 16.0000 | -5.333e-08 | -0.00001 | -0.00000 |
| 0.5 | 4 | 1.99739555 | 2.0000 | -2.604e-03 | -0.04167 | -0.04167 |
| 0.5 | 8 | 3.99934894 | 4.0000 | -6.511e-04 | -0.04167 | -0.04167 |
| 0.5 | 12 | 5.99971062 | 6.0000 | -2.894e-04 | -0.04167 | -0.04167 |
| 0.5 | 16 | 7.99983719 | 8.0000 | -1.628e-04 | -0.04168 | -0.04167 |
| 1.0 | 4 | -0.00781632 | 0.0000 | -7.816e-03 | -0.12506 | -0.12500 |
| 1.0 | 8 | -0.00195325 | 0.0000 | -1.953e-03 | -0.12501 | -0.12500 |
| 1.0 | 12 | -0.00086809 | 0.0000 | -8.681e-04 | -0.12501 | -0.12500 |
| 1.0 | 16 | -0.00048834 | 0.0000 | -4.883e-04 | -0.12501 | -0.12500 |

Identity check (relative residual at x = 16 below 0.0001, residual shrinking with x for s > 0): PASS [identity].

## Stage B.2: main scan (lowest levels against box size)

Grid step h = 0.08 in x and y; 4th-order FD; levels of the parity sector K+ (each a doublet of H).
Valley width at the box edge is ~ L^(-1/2); h·√L is printed as the [grid-step] ratio (want ≪ 1).

### s = 0.0

| L | n per axis | h·√L | E1 | E2 | E3 | E4 | E5 | E6 |
|---|---|---|---|---|---|---|---|---|
| 4 | 99 | 0.160 | 1.109388 | 2.396672 | 2.396672 | 3.145267 | 3.696940 | 4.525804 |
| 6 | 149 | 0.196 | 1.108222 | 2.378661 | 2.378661 | 3.056411 | 3.516253 | 4.100080 |
| 8 | 199 | 0.226 | 1.108222 | 2.378632 | 2.378632 | 3.056066 | 3.514932 | 4.093446 |
| 10 | 249 | 0.253 | 1.108222 | 2.378632 | 2.378632 | 3.056065 | 3.514931 | 4.093438 |
| 12 | 299 | 0.277 | 1.108222 | 2.378632 | 2.378632 | 3.056065 | 3.514931 | 4.093438 |

Fitted slope d lnE/d lnL over all L [computed]: E1: -0.001, E2: -0.006, E3: -0.006, E4: -0.024, E5: -0.042, E6: -0.084
Local slope between L = 10 and 12 [computed]: E1: -0.0000, E2: -0.0000, E3: -0.0000, E4: -0.0000, E5: -0.0000, E6: -0.0000
Relative change L=10→12 [computed]: E1: 2.8e-15, E2: 8.2e-14, E3: 8.2e-14, E4: 2.5e-12, E5: 2.0e-11, E6: 2.8e-10
Grade s = 0.0: PASS — prediction 'discrete spectrum, converged in L' [prediction, Simon 1983]; max relative change of E1–E3 between L = 10 and 12 is 8.2e-14 (PASS < 0.001, PARTIAL < 0.01).

### s = 0.5

| L | n per axis | h·√L | E1 | E2 | E3 | E4 | E5 | E6 |
|---|---|---|---|---|---|---|---|---|
| 4 | 99 | 0.160 | 0.846239 | 1.810992 | 2.306014 | 3.177965 | 3.353596 | 4.409148 |
| 6 | 149 | 0.196 | 0.835857 | 1.685412 | 2.095425 | 2.725362 | 2.831993 | 3.501627 |
| 8 | 199 | 0.226 | 0.835795 | 1.682375 | 2.083575 | 2.655488 | 2.763669 | 3.314669 |
| 10 | 249 | 0.253 | 0.835795 | 1.682361 | 2.083466 | 2.653686 | 2.761477 | 3.298670 |
| 12 | 299 | 0.277 | 0.835795 | 1.682361 | 2.083466 | 2.653678 | 2.761465 | 3.298449 |

Fitted slope d lnE/d lnL over all L [computed]: E1: -0.010, E2: -0.061, E3: -0.086, E4: -0.157, E5: -0.168, E6: -0.257
Local slope between L = 10 and 12 [computed]: E1: -0.0000, E2: -0.0000, E3: -0.0000, E4: -0.0000, E5: -0.0000, E6: -0.0004
Relative change L=10→12 [computed]: E1: 5.3e-11, E2: 1.1e-08, E3: 1.1e-07, E4: 3.1e-06, E5: 4.3e-06, E6: 6.7e-05
Grade s = 0.5: PASS — prediction 'discrete spectrum, converged in L' [prediction, Simon 1983]; max relative change of E1–E3 between L = 10 and 12 is 1.1e-07 (PASS < 0.001, PARTIAL < 0.01).

### s = 1.0

| L | n per axis | h·√L | E1 | E2 | E3 | E4 | E5 | E6 |
|---|---|---|---|---|---|---|---|---|
| 4 | 99 | 0.160 | 0.203993 | 0.794055 | 1.679978 | 2.588180 | 3.204018 | 3.862498 |
| 6 | 149 | 0.196 | 0.082417 | 0.327606 | 0.728448 | 1.268877 | 1.911047 | 2.558369 |
| 8 | 199 | 0.226 | 0.044195 | 0.176409 | 0.395312 | 0.698204 | 1.080216 | 1.532062 |
| 10 | 249 | 0.253 | 0.027458 | 0.109808 | 0.246734 | 0.437459 | 0.680756 | 0.974673 |
| 12 | 299 | 0.277 | 0.018650 | 0.074728 | 0.168233 | 0.298833 | 0.466079 | 0.669344 |

Fitted slope d lnE/d lnL over all L [computed]: E1: -2.177, E2: -2.151, E3: -2.098, E4: -1.976, E5: -1.776, E6: -1.613
Local slope between L = 10 and 12 [computed]: E1: -2.1215, E2: -2.1110, E3: -2.1005, E4: -2.0903, E5: -2.0779, E6: -2.0612
All six levels fall monotonically with L: True [computed]. Minimum level over the scan: 0.018650 (H = Q² ≥ 0, so no negative level is expected).
Ratios E_k/E_1 at L = 12 [computed]: 1.000, 4.007, 9.021, 16.023, 24.991, 35.890  (1D box: k² = 1, 4, 9, 16, 25, 36)
Effective 1D box length ℓ_k = kπ/√E_k at L = 12 [computed]: 23.00, 22.98, 22.98, 22.99, 23.01, 23.04  vs full valley length 2L = 24 [hive-interpretation: free motion along one whole valley line].
Grade s = 1: PASS — prediction 'continuum: levels fall like 1/L²'; local slope of E1 between L = 10 and 12 is -2.122 (PASS window (-2.3, -1.7)); the slope sits slightly below -2 because ℓ_eff ≈ 2L - const [finite-size].

## Domain monotonicity and positivity checks [computed]

- monotonicity s = 0.0, E1: PASS; ΔE for successive L = -1.17e-03, -4.51e-07, -2.78e-11, -3.11e-15.
- monotonicity s = 0.0, E2: PASS; ΔE for successive L = -1.80e-02, -2.97e-05, -5.63e-09, -1.95e-13.
- monotonicity s = 0.0, E3: PASS; ΔE for successive L = -1.80e-02, -2.97e-05, -5.63e-09, -1.96e-13.
- monotonicity s = 0.0, E4: PASS; ΔE for successive L = -8.89e-02, -3.45e-04, -1.28e-07, -7.56e-12.
- monotonicity s = 0.0, E5: PASS; ΔE for successive L = -1.81e-01, -1.32e-03, -7.97e-07, -6.95e-11.
- monotonicity s = 0.0, E6: PASS; ΔE for successive L = -4.26e-01, -6.63e-03, -7.82e-06, -1.14e-09.
- monotonicity s = 0.5, E1: PASS; ΔE for successive L = -1.04e-02, -6.17e-05, -9.22e-08, -4.41e-11.
- monotonicity s = 0.5, E2: PASS; ΔE for successive L = -1.26e-01, -3.04e-03, -1.45e-05, -1.80e-08.
- monotonicity s = 0.5, E3: PASS; ΔE for successive L = -2.11e-01, -1.18e-02, -1.09e-04, -2.25e-07.
- monotonicity s = 0.5, E4: PASS; ΔE for successive L = -4.53e-01, -6.99e-02, -1.80e-03, -8.32e-06.
- monotonicity s = 0.5, E5: PASS; ΔE for successive L = -5.22e-01, -6.83e-02, -2.19e-03, -1.20e-05.
- monotonicity s = 0.5, E6: PASS; ΔE for successive L = -9.08e-01, -1.87e-01, -1.60e-02, -2.20e-04.
- monotonicity s = 1.0, E1: PASS; ΔE for successive L = -1.22e-01, -3.82e-02, -1.67e-02, -8.81e-03.
- monotonicity s = 1.0, E2: PASS; ΔE for successive L = -4.66e-01, -1.51e-01, -6.66e-02, -3.51e-02.
- monotonicity s = 1.0, E3: PASS; ΔE for successive L = -9.52e-01, -3.33e-01, -1.49e-01, -7.85e-02.
- monotonicity s = 1.0, E4: PASS; ΔE for successive L = -1.32e+00, -5.71e-01, -2.61e-01, -1.39e-01.
- monotonicity s = 1.0, E5: PASS; ΔE for successive L = -1.29e+00, -8.31e-01, -3.99e-01, -2.15e-01.
- monotonicity s = 1.0, E6: PASS; ΔE for successive L = -1.30e+00, -1.03e+00, -5.57e-01, -3.05e-01.
Domain monotonicity (every s and every level falls or stays as L grows): PASS [computed].
- positivity s = 1, L = 4: lowest box level E1 = 0.20399338; PASS (tolerance −1e-08).
- positivity s = 1, L = 6: lowest box level E1 = 0.08241652; PASS (tolerance −1e-08).
- positivity s = 1, L = 8: lowest box level E1 = 0.04419507; PASS (tolerance −1e-08).
- positivity s = 1, L = 10: lowest box level E1 = 0.02745784; PASS (tolerance −1e-08).
- positivity s = 1, L = 12: lowest box level E1 = 0.01865003; PASS (tolerance −1e-08).
H_1 = Q² positivity check over all scanned boxes: PASS [computed; grid tolerance].

All six s = ½ levels lie below the matching s = 0 levels (weaker wall (1-s)|x| = |x|/2) [computed, ungraded, post-hoc]: L=4: False, L=6: True, L=8: True, L=10: True, L=12: True.
Where it fails is the squeezed small box (L = 4: E4 = 3.178 at s = ½ vs 3.145 at s = 0) [finite-size, computed]; reported per L after the first run showed the all-L form failing at L = 4 [post-hoc].
The difference H_{1/2} − H_0 = ½(xσ3 + yσ1) has no fixed sign, so this ordering is not forced [post-hoc].
E(s=½)/E(s=0) at L = 12 [computed]: 0.754, 0.707, 0.876, 0.868, 0.786, 0.806  (a pure 1D valley wall would give (1/2)^(2/3) = 0.630 [hive-interpretation]).

## Stage B.3: grid convergence at L = 12 [grid-step]

h = 0.08 (h·√L = 0.277) vs h = 0.06 (h·√L = 0.208); Richardson estimate assumes the 4th-order error ∝ h⁴.

| s | level | E(h=0.08) | E(h=0.06) | difference | Richardson E(h→0) | rel. error of h=0.08 |
|---|---|---|---|---|---|---|
| 0.0 | E1 | 1.108222 | 1.108223 | +9.15e-07 | 1.108223 | 1.2e-06 |
| 0.0 | E2 | 2.378632 | 2.378636 | +4.17e-06 | 2.378638 | 2.6e-06 |
| 0.0 | E3 | 2.378632 | 2.378636 | +4.17e-06 | 2.378638 | 2.6e-06 |
| 0.0 | E4 | 3.056065 | 3.056076 | +1.08e-05 | 3.056081 | 5.2e-06 |
| 0.0 | E5 | 3.514931 | 3.514943 | +1.22e-05 | 3.514949 | 5.1e-06 |
| 0.0 | E6 | 4.093438 | 4.093459 | +2.15e-05 | 4.093469 | 7.7e-06 |
| 0.5 | E1 | 0.835795 | 0.835797 | +1.84e-06 | 0.835798 | 3.2e-06 |
| 0.5 | E2 | 1.682361 | 1.682372 | +1.06e-05 | 1.682376 | 9.2e-06 |
| 0.5 | E3 | 2.083466 | 2.083482 | +1.58e-05 | 2.083489 | 1.1e-05 |
| 0.5 | E4 | 2.653678 | 2.653712 | +3.40e-05 | 2.653728 | 1.9e-05 |
| 0.5 | E5 | 2.761465 | 2.761494 | +2.97e-05 | 2.761508 | 1.6e-05 |
| 0.5 | E6 | 3.298449 | 3.298501 | +5.17e-05 | 3.298525 | 2.3e-05 |
| 1.0 | E1 | 0.018650 | 0.018727 | +7.68e-05 | 0.018762 | 6.0e-03 |
| 1.0 | E2 | 0.074728 | 0.074914 | +1.86e-04 | 0.075001 | 3.6e-03 |
| 1.0 | E3 | 0.168233 | 0.168459 | +2.26e-04 | 0.168564 | 2.0e-03 |
| 1.0 | E4 | 0.298833 | 0.299072 | +2.38e-04 | 0.299182 | 1.2e-03 |
| 1.0 | E5 | 0.466079 | 0.466323 | +2.44e-04 | 0.466436 | 7.6e-04 |
| 1.0 | E6 | 0.669344 | 0.669590 | +2.46e-04 | 0.669704 | 5.4e-04 |

Worst relative grid error of the h = 0.08 levels at L = 12 [grid-step]: s=0.0: 7.7e-06, s=0.5: 2.3e-05, s=1.0: 6.0e-03

Transverse zero-point cancellation on the scan grid at the box edge, s = 1 [grid-step]:

| L = x | lowest h_y at h = 0.08 | at h = 0.005 | grid error | E1(L) of the 2D scan | error / E1 |
|---|---|---|---|---|---|
| 4 | -0.007870 | -0.007816 | -5.40e-05 | 0.203993 | -2.6e-04 |
| 6 | -0.003655 | -0.003473 | -1.82e-04 | 0.082417 | -2.2e-03 |
| 8 | -0.002383 | -0.001953 | -4.30e-04 | 0.044195 | -9.7e-03 |
| 10 | -0.002087 | -0.001250 | -8.37e-04 | 0.027458 | -3.0e-02 |
| 12 | -0.002309 | -0.000868 | -1.44e-03 | 0.018650 | -7.7e-02 |

Reading [grid-step]: the transverse grid error grows like h⁴|x|³ and is largest at the wall, so the edge column
is a worst case. The 2D levels average it over the valley with weight |ψ|², and the ground mode peaks at the centre;
the measured 2D grid error of E1 at L = 12 (table above, 0.60%) is the relevant number. It lowers the levels
more at larger L; the resulting local E1 slope between L = 10 and 12 is -2.122 [computed].

Plot: x2y2_levels.png (left: s = 0, ½ lowest three levels vs L; right: s = 1 log-log with an L⁻² guide).

## Summary

- Stage A table: derived symbolically; p = 1 renormalisable and Weyl invariant, p = 2, 3, 5 neither [standard].
- Structural identities (dWLN equivalence, parity doubling): PASS [identity].
- Valley identity (1-s)|x|: PASS [identity].
- s = 0.0: PASS
- s = 0.5: PASS
- s = 1.0: PASS

Runtime: 167 s [computed].

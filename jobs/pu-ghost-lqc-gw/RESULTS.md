# Job Seven: Pais–Uhlenbeck ghost and a GW mode through the LQC bounce — RESULTS

Written only by run.py; every number below is printed from a variable. Tags: [computed] [identity] [assumed]
[assumed input] [standard] [post-hoc] [finite-size] [grid-step] [prediction] [hive-interpretation].
Python 3.14.7, numpy 2.5.2, scipy 1.18.1, sympy 1.14.0.
PASS thresholds are fixed in the parameter block of run.py before the first run. The G5 fold-in thresholds and the
G5b sign rule were added after the Venus/Helios review and fixed before the fold-in run; G1–G4 and L1–L4 are unchanged.

# Part G: the Pais–Uhlenbeck oscillator (ghost)

L = ½[q̈² − (ω₁²+ω₂²)q̇² + ω₁²ω₂²q²] − (λ/4)q⁴  ⇒  q⁽⁴⁾ + (ω₁²+ω₂²)q̈ + ω₁²ω₂²q = λq³.
Ostrogradsky: x = q̇, p_x = q̈, p_q = −(ω₁²+ω₂²)q̇ − q⃛,  H = p_q x + p_x²/2 + (ω₁²+ω₂²)x²/2 − ω₁²ω₂²q²/2 + λq⁴/4.
Main frequencies [assumed input]: ω₁ = 1, ω₂ = 0.6180339887 (golden ratio, away from the 1:1, 1:2, 1:3 resonances).

## G1: free PU splits into two oscillators of opposite energy sign [identity]

Canonical map (Smilga 2009, eq. 4), checked with sympy for symbolic ω₁ > ω₂:
  {X1,P1} = 1, {X2,P2} = 1, {X1,X2} = 0, {P1,P2} = 0, {X1,P2} = 0, {X2,P1} = 0
  H − [½(P₁²+ω₁²X₁²) − ½(P₂²+ω₂²X₂²)] = 0   ⇒  E = E₁ − E₂ (exact).
  The map carries 1/√(ω₁²−ω₂²): it is singular at ω₁ = ω₂, where the split fails (see G2) [identity].
  Unbounded below: the state q = q̈ = 0, q̇ = 1, q⃛ = M has H = −M − (ω₁²+ω₂²)/2: M=10: H=-10.691, M=100: H=-100.691, M=1000: H=-1000.691 [identity].

Numerical free check (50 random starts, |u| = 0.5, RK4 dt = 0.01, t ≤ 600) [computed]:
  max |H − (E₁ − E₂)| at t = 0: 8.3e-17;  max rel. drift E₁: 8.3e-10, E₂: 4.6e-11;  max R(t)/R(0) = 4.370 (bounded).
G1 PASS (thresholds: drift < 1e-06, R/R0 < 50).

## G2: equal frequencies ω₁ = ω₂ = 1, EXCLUDED from the split (flagged) [identity]

The characteristic roots are a double pair ±i; the free solution with q(0)=1 is q = cos t + (t/2) sin t (secular).
RK4 vs exact, t ≤ 600: max |error| / max |q| = 5.0e-08. Envelope max|q| grows from 33.78 (t≈60) to 294.52 (t≈580); log-log slope = 0.957 (linear growth).
G2 PASS (thresholds: rel. error < 1e-06, slope in (0.9, 1.1)).

## G3: interacting PU, L → L − (λ/4)q⁴ (Smilga's quartic) [computed]

Sampling and threshold [assumed input]:
- q_* = ω₁ω₂/√|λ| (the only nonlinear scale). Normalised state u = (q, q̇/ω̄, q̈/ω̄², q⃛/ω̄³), ω̄ = √(ω₁ω₂).
- 200 starts per amplitude, directions uniform on the 3-sphere (seed 7), |u| = A·q_*; A ∈ [0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0]. The same directions are reused for every group.
- Runaway: R(t) = |u(t)| ≥ 10 q_* before t_max = 300 (also reported at 600; R ≥ 100 q_* recorded as a threshold check). RK4, dt = 0.01.
- Integration cost: main batch 70 s, dt/2 batch 9 s [computed].

| A = |u|/q_* | runaway fraction t ≤ 300 | t ≤ 600 | R ≥ 100 q_* by t ≤ 600 |
|---|---|---|---|
| 0.02 | 0.000 (0/200) | 0.000 | 0.000 |
| 0.05 | 0.000 (0/200) | 0.000 | 0.000 |
| 0.1 | 0.000 (0/200) | 0.000 | 0.000 |
| 0.15 | 0.000 (0/200) | 0.000 | 0.000 |
| 0.2 | 0.000 (0/200) | 0.000 | 0.000 |
| 0.3 | 0.040 (8/200) | 0.045 | 0.045 |
| 0.4 | 0.455 (91/200) | 0.480 | 0.480 |
| 0.6 | 0.795 (159/200) | 0.825 | 0.825 |
| 0.8 | 0.925 (185/200) | 0.925 | 0.925 |
| 1 | 0.965 (193/200) | 0.965 | 0.965 |
| 1.5 | 0.995 (199/200) | 0.995 | 0.995 |
| 2 | 0.980 (196/200) | 0.980 | 0.980 |
| 3 | 1.000 (200/200) | 1.000 | 1.000 |

Stable island: no runaway for any A ≤ 0.2 (t ≤ 300). Runaway first appears at A = 0.3; 50 % at A ≈ 0.426 (t ≤ 300), 0.412 (t ≤ 600) [computed].

Runaway fraction (t ≤ 300) against λ and physical amplitude |u| = a. The λ-collapse is an [identity]: with q = Q/√λ every term of L
scales by 1/λ, so the motion depends only on a√λ, i.e. on the column A = a√λ/(ω₁ω₂) = a/q_*(λ) (threshold check in G5a):

| a | λ = 0.1 (A) | λ = 1 (A) | λ = 10 (A) |
|---|---|---|---|
| 0.02 | 0.000 (0.0102) | 0.000 (0.0324) | 0.000 (0.102) |
| 0.05 | 0.000 (0.0256) | 0.000 (0.0809) | 0.000 (0.256) |
| 0.1 | 0.000 (0.0512) | 0.000 (0.162) | 0.670 (0.512) |
| 0.2 | 0.000 (0.102) | 0.085 (0.324) | 0.965 (1.02) |
| 0.5 | 0.000 (0.256) | 0.930 (0.809) | 1.000 (2.56) |
| 1 | 0.670 (0.512) | 1.000 (1.62) | 1.000 (5.12) |
| 2 | 0.965 (1.02) | 1.000 (3.24) | 1.000 (10.2) |

Scaling identity q → q_*·Q removes λ [identity]; runaway counts at equal A: A=0.3: λ=1 → 8, λ=0.25 → 8; A=0.3: λ=1 → 8, λ=4 → 8; A=1: λ=1 → 193, λ=0.25 → 193; A=1: λ=1 → 193, λ=4 → 193.
Energy drift |ΔH|/E_abs at t = 600 [computed]: survivors with max R ≤ 2 q_*: max 1.2e-08 (1353 trajectories); all survivors: max 1.2e-08 (1357).
Step halving (dt vs dt/2, t ≤ 300) [computed]: A=0.3: 0.040 vs 0.040; A=0.6: 0.795 vs 0.800; A=1: 0.965 vs 0.965; A=1.5: 0.995 vs 0.995.
G3 PASS: island (f = 0 for A ≤ 0.1): True; f ≥ 0.5 at A = 3: True (f = 1.000); drift < 1e-06: True; dt/2 within 0.02: True; scaling ±1: True.

λ = −1 (report only; Smilga: the wrong sign is malicious; extended with a no-ghost control in G5b) [computed]:
  unequal frequencies, sphere starts: A=0.02: 0.000 (t≤300), 0.000 (t≤600); A=0.05: 0.000 (t≤300), 0.000 (t≤600); A=0.1: 0.000 (t≤300), 0.000 (t≤600); A=0.2: 0.545 (t≤300), 0.545 (t≤600); A=0.3: 0.825 (t≤300), 0.825 (t≤600).
  equal frequencies, q(0) = c: c=0.02: runaway at t = 34.0; c=0.05: runaway at t = 21.6; c=0.1: runaway at t = 15.2; c=0.2: runaway at t = 10.0.

## G4: comparison with Smilga, NPB 706 (2005) 598, eqs. (6)–(7) (equal frequencies, flagged) [computed]

Model: L = ½(q̈ + Ω²q)² − (α/4)q⁴, Ω = α = 1, q(0) = c, q̇ = q̈ = q⃛ = 0; c grid 0.2…0.45 step 0.0025.
Smallest runaway c: 0.3 (t ≤ 300; 3 larger c survive), 0.3 (t ≤ 600; 0 larger c survive). Smilga: c_crit ≈ 0.3 Ω²/√α.
G4 PASS (window (0.25, 0.35) on the t ≤ 600 value).
Same one-parameter start q(0) = c q_* at the main (unequal) frequencies: smallest runaway c = 0.39 (t ≤ 300; c up to 3) [computed, report only].

## G5: review fold-ins (Venus maths, Helios physics); thresholds fixed in run.py before the fold-in run [computed]

### G5a: the runaway threshold scales like q_* = ω₁ω₂/√|λ|

With q = Q/√λ every term of L = ½[q̈² − (ω₁²+ω₂²)q̇² + ω₁²ω₂²q²] − (λ/4)q⁴ scales by 1/λ, so the motion depends only on a√λ
(a = |u|) [identity]. Numerical check at the λ values already scanned: same start directions, physical amplitudes
a = A·ω₁ω₂/√λ for A ∈ [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6], runaway by t ≤ 300; A₅₀ by linear interpolation of the fraction:

| λ | A=0.25 | A=0.3 | A=0.35 | A=0.4 | A=0.45 | A=0.5 | A=0.6 | A₅₀ | a₅₀ (physical) | a₅₀·√λ |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.000 | 0.040 | 0.235 | 0.455 | 0.570 | 0.655 | 0.795 | 0.4196 | 0.8200 | 0.2593 |
| 0.25 | 0.000 | 0.040 | 0.235 | 0.455 | 0.570 | 0.655 | 0.795 | 0.4196 | 0.5186 | 0.2593 |
| 1 | 0.000 | 0.040 | 0.235 | 0.455 | 0.570 | 0.655 | 0.795 | 0.4196 | 0.2593 | 0.2593 |
| 4 | 0.000 | 0.040 | 0.235 | 0.455 | 0.570 | 0.655 | 0.795 | 0.4196 | 0.1297 | 0.2593 |
| 10 | 0.000 | 0.040 | 0.235 | 0.455 | 0.570 | 0.655 | 0.795 | 0.4196 | 0.0820 | 0.2593 |

a₅₀·√λ spans [0.259306, 0.259306]; max |A₅₀(λ) − A₅₀(1)| = 0.0e+00; fitted d ln a₅₀ / d ln λ = -0.500000 (a 1/√λ threshold gives −1/2).
G5a PASS (thresholds: max |A₅₀(λ) − A₅₀(1)| ≤ 0.01, |slope + 1/2| ≤ 0.01).

### G5b: the sign of λ against a no-ghost control at the same scaled amplitudes

Ghost: H = ½(P₁²+ω₁²X₁²) − ½(P₂²+ω₂²X₂²) + λq⁴/4 in Smilga's normal-mode variables (the G1 map), q = (ω₁X₂ − P₁)/(ω₁√(ω₁²−ω₂²)).
No-ghost control [assumed]: the same H with +½(P₂²+ω₂²X₂²) (both modes positive energy), the same quartic λq⁴/4 in the same q,
the same starts (G3 sphere directions, seed 7, 200 per amplitude, mapped by the same map) and both signs of λ, |λ| = 1.
Runaway criterion (fixed before the run, as in G3): |u| ≥ 10 q_* by t ≤ 300 (t ≤ 600 shown as a check), u recovered by the inverse map; RK4, dt = 0.01.
For λ > 0 the control H is bounded below, so it cannot run away [identity]. For λ < 0 the quartic is unbounded below even
without a ghost, so only runaway beyond the matching control, Δ = f_ghost − f_control, counts as ghost runaway.
Sign rule (fixed before the run): the sign of λ matters if max over A ≤ 0.5 of |Δ(λ>0) − Δ(λ<0)| ≥ 0.25 at t ≤ 300.
Map checks at t = 0 [identity]: round trip u → (X, P) → u, max rel. error 3.6e-16; |H_normal-mode − H_Ostrogradsky| / max E_abs = 4.5e-16. Batch: 8000 trajectories to t = 600 in 94 s.

S [post-hoc; Venus review request, not a grade]: the share of the control's survivors that the ghost adds to the runaway, S = (f_ghost − f_control)/(1 − f_control), printed as n/a where f_control = 1. For λ > 0 the control never runs away, so S(λ>0) = Δ(λ>0).

Runaway fraction by t ≤ 300 against the scaled amplitude A = |u|√|λ|/(ω₁ω₂):

| system | A=0.05 | A=0.1 | A=0.15 | A=0.2 | A=0.25 | A=0.3 | A=0.35 | A=0.4 | A=0.45 | A=0.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| ghost, λ > 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.040 | 0.235 | 0.455 | 0.570 | 0.655 |
| ghost, λ < 0 | 0.000 | 0.000 | 0.195 | 0.545 | 0.750 | 0.825 | 0.875 | 0.930 | 0.945 | 0.955 |
| no-ghost control, λ > 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| no-ghost control, λ < 0 | 0.000 | 0.000 | 0.015 | 0.380 | 0.575 | 0.735 | 0.810 | 0.875 | 0.910 | 0.935 |
| Δ(λ>0) = ghost − control | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.040 | +0.235 | +0.455 | +0.570 | +0.655 |
| Δ(λ<0) = ghost − control | +0.000 | +0.000 | +0.180 | +0.165 | +0.175 | +0.090 | +0.065 | +0.055 | +0.035 | +0.020 |
| abs(Δ(λ>0) − Δ(λ<0)) | 0.000 | 0.000 | 0.180 | 0.165 | 0.175 | 0.050 | 0.170 | 0.400 | 0.535 | 0.635 |
| S(λ>0) = Δ/(1 − f_control) [post-hoc] | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.040 | 0.235 | 0.455 | 0.570 | 0.655 |
| S(λ<0) = Δ/(1 − f_control) [post-hoc] | 0.000 | 0.000 | 0.183 | 0.266 | 0.412 | 0.340 | 0.342 | 0.440 | 0.389 | 0.308 |
| S(λ>0) − S(λ<0) [post-hoc] | +0.000 | +0.000 | -0.183 | -0.266 | -0.412 | -0.300 | -0.107 | +0.015 | +0.181 | +0.347 |
| control survivors, λ < 0 (S denominator, of 200) | 200 | 200 | 197 | 124 | 85 | 53 | 38 | 25 | 18 | 13 |

Runaway fraction by t ≤ 600 against the scaled amplitude A = |u|√|λ|/(ω₁ω₂):

| system | A=0.05 | A=0.1 | A=0.15 | A=0.2 | A=0.25 | A=0.3 | A=0.35 | A=0.4 | A=0.45 | A=0.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| ghost, λ > 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.045 | 0.285 | 0.480 | 0.605 | 0.670 |
| ghost, λ < 0 | 0.000 | 0.000 | 0.195 | 0.545 | 0.750 | 0.825 | 0.875 | 0.930 | 0.945 | 0.955 |
| no-ghost control, λ > 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| no-ghost control, λ < 0 | 0.000 | 0.000 | 0.015 | 0.380 | 0.575 | 0.735 | 0.810 | 0.880 | 0.910 | 0.935 |
| Δ(λ>0) = ghost − control | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.045 | +0.285 | +0.480 | +0.605 | +0.670 |
| Δ(λ<0) = ghost − control | +0.000 | +0.000 | +0.180 | +0.165 | +0.175 | +0.090 | +0.065 | +0.050 | +0.035 | +0.020 |
| abs(Δ(λ>0) − Δ(λ<0)) | 0.000 | 0.000 | 0.180 | 0.165 | 0.175 | 0.045 | 0.220 | 0.430 | 0.570 | 0.650 |
| S(λ>0) = Δ/(1 − f_control) [post-hoc] | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.045 | 0.285 | 0.480 | 0.605 | 0.670 |
| S(λ<0) = Δ/(1 − f_control) [post-hoc] | 0.000 | 0.000 | 0.183 | 0.266 | 0.412 | 0.340 | 0.342 | 0.417 | 0.389 | 0.308 |
| S(λ>0) − S(λ<0) [post-hoc] | +0.000 | +0.000 | -0.183 | -0.266 | -0.412 | -0.295 | -0.057 | +0.063 | +0.216 | +0.362 |
| control survivors, λ < 0 (S denominator, of 200) | 200 | 200 | 197 | 124 | 85 | 53 | 38 | 24 | 18 | 13 |

Which sign has the larger ghost excess, at the sampled A only [post-hoc; computed from the tables above]:
- t ≤ 300, raw Δ: equal at A in [0.05, 0.1]; larger for λ<0 at A in [0.15, 0.3]; larger for λ>0 at A ≥ 0.35 (to the grid maximum A = 0.5).
- t ≤ 300, share S: equal at A in [0.05, 0.1]; larger for λ<0 at A in [0.15, 0.35]; larger for λ>0 at A ≥ 0.4 (to the grid maximum A = 0.5).
- t ≤ 600, raw Δ: equal at A in [0.05, 0.1]; larger for λ<0 at A in [0.15, 0.3]; larger for λ>0 at A ≥ 0.35 (to the grid maximum A = 0.5).
- t ≤ 600, share S: equal at A in [0.05, 0.1]; larger for λ<0 at A in [0.15, 0.35]; larger for λ>0 at A ≥ 0.4 (to the grid maximum A = 0.5).
Same ranges at t ≤ 300 and t ≤ 600: raw Δ True; S True. Both statements are limited to the sampled grid [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]: a crossover lies between neighbouring grid points [finite-size].

Max |Δ(λ>0) − Δ(λ<0)| at t ≤ 300: 0.635 at A = 0.5 (Δ(λ>0) = +0.655, Δ(λ<0) = +0.020); at t ≤ 600: 0.650 at A = 0.5. Uncorrected max |f_ghost(λ>0) − f_ghost(λ<0)| = 0.785 at A = 0.3.
Controls: no-ghost λ > 0 never runs away up to t = 600: True. Ghost in normal-mode vs q variables (same starts, overlapping A, t ≤ 300): max |Δf| = 0.000 over 10 pairs (threshold 0.03).
Energy drift |ΔH|/E_abs of survivors at t = 600: ghost max 9.0e-10 (2379), control max 6.2e-09 (2952).
G5b controls PASS; sign test PASS (the sign of λ matters beyond the no-ghost control).

**Part G verdict: PASS** (PASS = G1–G4; PARTIAL = G1, G2 pass but G3 or G4 fails; FAIL = G1 or G2 fails; the G5 fold-ins are reported separately and do not enter it).

# Part L: a tensor mode through the effective LQC bounce

Units [assumed input]: 8πG = 1, ρ_c = 1, a_B = 1, so 24πGρ_c = 3·(8πG)ρ_c = 3 and k_B = a_B√(8πGρ_c) = 1.
Background [standard]: a(t) = (1 + 24πGρ_c t²)^{1/6} = (1 + 3t²)^{1/6} (massless scalar, ρ = ρ_c a⁻⁶).

## L1: background and a''/a [identity]

- Effective Friedmann H² − (8πG/3)ρ(1 − ρ/ρ_c) for this a(t): 0 (sympy).
- a''/a = d(aȧ)/dt = (1 − t²)(1 + 3t²)^(−5/3); sympy residual 0. Value at the bounce: 1 = k_B².
- η(t) = t·₂F₁(1/6, 1/2; 3/2; −3t²) vs quadrature at t ∈ [0.5, 2.0, 10.0, 100.0, 10000.0]: max rel. difference 5.7e-16.
- Numerical a''/a by 5-point differences in η (h = 0.01) at η ∈ [0.0, 0.4, 0.8, 1.5, 3.0, 10.0, 50.0]: max |error| 5.2e-08.
- Late time: a''/a → −1/(4η²) (a ∝ η^(1/2)). Nearest complex singularity: t = ±i/√3, η_s = ±i·0.646777 [computed].
- Venus's closed form Im η_s = (1/√3)(√π/2)Γ(5/6)/Γ(4/3) = 0.646777389807 (math.gamma); Beta-function value 0.646777389807; difference 6.7e-16 [identity].
L1 PASS (thresholds: η rel. diff < 1e-10, FD error < 1e-06).

## L2–L3: Bogoliubov coefficients, Wronskian and start/end convergence [computed]

v'' + (k² − a''/a)v = 0 integrated in t (dv/dt = v'/a, dv'/dt = −(k² − a''/a)v/a), DOP853, rtol = 1e-12.
Start at η_i = −X/k in the first-order adiabatic vacuum v = e^(−i∫ω)/√(2ω), v' = (−iω − ω'/2ω)v, ω² = k² − a''/a;
end at η_f = +X/k and project on the same late-time adiabatic modes. X = 200; convergence column X = 400.

| k/k_B | |β|² (X=200) | |β|² (X=400) | rel. change | |α|²−|β|²−1 (X=200) | (X=400) |
|---|---|---|---|---|---|
| 0.1 | 3.650273e+00 | 3.650273e+00 | 1.6e-10 | -4.2e-12 | -7.5e-12 |
| 0.1259 | 3.093499e+00 | 3.093499e+00 | 1.7e-10 | -4.4e-12 | -7.1e-12 |
| 0.1585 | 2.578301e+00 | 2.578301e+00 | 1.7e-10 | -4.3e-12 | -7.5e-12 |
| 0.1995 | 2.105564e+00 | 2.105564e+00 | 1.7e-10 | -4.8e-12 | -7.5e-12 |
| 0.2512 | 1.676758e+00 | 1.676758e+00 | 1.8e-10 | -4.0e-12 | -7.4e-12 |
| 0.3162 | 1.294001e+00 | 1.294001e+00 | 1.9e-10 | -3.8e-12 | -6.2e-12 |
| 0.3981 | 9.599596e-01 | 9.599596e-01 | 2.0e-10 | -3.8e-12 | -7.1e-12 |
| 0.5012 | 6.774618e-01 | 6.774618e-01 | 2.3e-10 | -4.2e-12 | -8.1e-12 |
| 0.631 | 4.487192e-01 | 4.487192e-01 | 2.7e-10 | -3.2e-12 | -6.6e-12 |
| 0.7943 | 2.741589e-01 | 2.741589e-01 | 3.5e-10 | -3.0e-12 | -6.4e-12 |
| 1 | 1.511312e-01 | 1.511312e-01 | 4.7e-10 | -3.0e-12 | -6.4e-12 |
| 1.259 | 7.307910e-02 | 7.307910e-02 | 6.8e-10 | -3.1e-12 | -6.3e-12 |
| 1.585 | 2.990923e-02 | 2.990923e-02 | 1.1e-09 | -3.2e-12 | -6.5e-12 |
| 1.995 | 9.903341e-03 | 9.903341e-03 | 1.9e-09 | -3.4e-12 | -6.7e-12 |
| 2.512 | 2.506090e-03 | 2.506090e-03 | 3.9e-09 | -3.5e-12 | -6.7e-12 |
| 3.162 | 4.511480e-04 | 4.511480e-04 | 9.3e-09 | -3.5e-12 | -6.7e-12 |
| 3.981 | 5.279415e-05 | 5.279415e-05 | 2.7e-08 | -3.4e-12 | -6.7e-12 |
| 5.012 | 3.585487e-06 | 3.585487e-06 | 1.0e-07 | -3.4e-12 | -6.7e-12 |
| 6.31 | 1.225397e-07 | 1.225397e-07 | 5.6e-07 | -3.4e-12 | -6.6e-12 |
| 7.943 | 1.761515e-09 | 1.761523e-09 | 4.7e-06 | -3.4e-12 | -6.6e-12 |
| 10 | 8.499395e-12 | 8.499959e-12 | 6.6e-05 | -3.3e-12 | -6.6e-12 |

Mode integrations: 42 in 33 s [computed].
L2 PASS: max ||α|²−|β|²−1| = 8.1e-12 (threshold 1e-08).
L3 PASS: max rel. change X = 200 → 400 over the 20 k with |β|² > 1e-10: 4.7e-06 (threshold 0.001); otherwise [finite-size].

## L4: spectrum shape against the prediction [computed]

- k ≤ 0.3 k_B: min |β|² = 1.68 (need ≥ 0.1): True.
- k ≥ 3 k_B: max |β|² = 0.000451 (need < 0.001); decreasing for k ≥ k_B: True.
- Small-k power law: d ln|β|²/d ln k over k ≤ 0.3 = -0.843.
- Local log-log slopes d ln|β|²/d ln k between neighbouring k: -0.72, -0.79, -0.88, -0.99, -1.13, -1.30, -1.51, -1.79, -2.14, -2.59, -3.16, -3.88, -4.80, -5.97, -7.45, -9.32, -11.68, -14.66, -18.42, -23.16.
- Large-k fits over k ≥ 3 k_B (ln|β|²): exponential b − c·k: c = 2.6007, rms 9.76e-03; b − c·k + p ln k: c = 2.5758, p = -0.151, rms 7.35e-04; pure power law: slope -15.29, rms 9.92e-01.
- Large-k fall-off [standard] (Dykhne, Sov. Phys. JETP 14 (1962) 941; Davis & Pechukas, J. Chem. Phys. 64 (1976) 3129, doi 10.1063/1.432648): |β|² ~ exp(−4k·Im η_s), η_s the nearest complex singularity of a''/a.
  Im η_s = 0.646777, 4·Im η_s = 2.5871; fitted c = 2.6007 (exponential; rel. diff 5.3e-03), 2.5758 (with ln k term; rel. diff 4.4e-03).

**Part L verdict: PASS** (PASS = L1–L4; PARTIAL = L1, L2 pass but L3 or L4 fails; FAIL = L1 or L2 fails).

Plots: pu_runaway.png (runaway fraction vs A, with the λ-table rescaled onto it), lqc_beta.png (|β_k|² vs k/k_B).

## Summary

- Part G (PU ghost): PASS
- Part L (LQC tensor mode): PASS
- Review fold-ins (G5, reported separately): G5a PASS; G5b controls PASS; sign test PASS (the sign of λ matters beyond the no-ghost control)

Runtime: 215 s [computed].

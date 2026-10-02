# pairA-qg-loss — RESULTS

**Signed off 2026-09-25:** Venus (maths) and Helios (physics).

Gravity-side [hive-interpretation] loss test on the Pair A curve. No folder was loaded; the numbers are hard-coded (ε_EP = 0.51368066, λ_EP = −0.308425i, v = −0.360253; source: pairA-qg-handoff / pairA-jt-4d as given by Akitti). H_A is not imported; a and b appear only inside the copy check. No claim of QG, a JT dual, or an Einstein solution. A and B WRITE, C held.

## Verdict

- **Loss term: T1: Im V = eta_g * F_JT (T2 = eta_g (eps^2/eps_EP^2 - 1) is T1 with eta_g -> eta_g/eps_EP^2: rescaling only; T3 not used)**.
- **Sign note.** With ψ ~ e^{−iλt}, Im V = η_g F_JT is **loss inside Γ (F_JT < 0) and gain outside (F_JT > 0)**. Every use of 'loss' in this file means this sign-changing term.
- Placements: P0 = iη_g F_JT·1 (scalar), and P1 = iη_g F_JT σ_z. σ_z is the direction that multiplies ε in the curve part, so vε → vε + iη_g F_JT: an imaginary shift of the dilaton-like variable. Both placements vanish at ±ε_EP.
- **Copy of H_A:** P0 YES for η_g > 0 (strict NO, but dynamical copy YES: the scalar drops out of the normalised dynamics); P1 NO for η_g > 0 (strict and dynamical NO). At η_g = 0 both placements reduce to the curve part, which **is** a copy (YES).
- **D6/D7 from H_try (P1):** D6-like at 0.75 and D7-like at 1.25 for η_g ∈ [0.001, 0.003, 0.01] (longest consecutive run [0.001, 0.003, 0.01], 1.00 decades).
- **GRADE: PARTIAL**
  HAVE (weak) by the pre-fixed letter; clean window 0.52 decades once eta_g=0.001 (dt check fail) is excluded; D6 inherited from the eta_g=0 rotated H_A
- Pre-fixed letter grade computed by the README rule: HAVE (window [0.001, 0.003, 0.01], 1.00 decades by the grid).
- **η_g = 0.001 dt refinement** (P1, γ_g T = 40, both directions): dt/4 Δw (dt/4 vs dt/8) = 1.3e-03, **not** below 1e-3. The letter window is therefore **not** cleanly one decade. Per start: 0.75 ccw: dt vs dt/2 8.9e-04, dt/2 vs dt/4 1.1e-03, dt/4 vs dt/8 1.3e-03; 0.75 cw: dt vs dt/2 1.6e-03, dt/2 vs dt/4 1.6e-03, dt/4 vs dt/8 1.2e-03; 1.25 ccw: dt vs dt/2 1.6e-08, dt/2 vs dt/4 4.0e-09, dt/4 vs dt/8 1.0e-09; 1.25 cw: dt vs dt/2 1.6e-08, dt/2 vs dt/4 4.0e-09, dt/4 vs dt/8 1.0e-09. At 1.25 ε_EP the differences fall as dt² (step-size error). At 0.75 ε_EP they do not fall: this is a rounding floor, because a 10⁻¹⁵ scalar perturbation (P0, η_g = 10⁻¹⁵ vs 0) already shifts the 0.75 ε_EP, γ_g T = 40 weights by 5.8e-04 [computed: floating-point floor, amplified exponentially along the loop at 0.75 ε_EP, γ_gT = 40; not integrator step error] A 1e-15 scalar moving w by 5.8e-04 is a gain of about 1e11 (5.8e-04/1e-15 ≈ 6e+11); this comes from the exponential gain along the loop (the losing mode is suppressed by e^{-Δγ t} and must regrow, carrying its rounding with it: stability-loss delay), not from the eigenvector condition number, which is O(1) at 0.25 ε_EP from the tip. With this setup the η_g = 0.001 row cannot be pushed under the 1e-3 rule at any dt, because the floor does not depend on dt. The grade stays PARTIAL either way: the question was whether the loss causes D6, and it does not.

**Caveat attached to the grade.** The curve part H_curve = λ_EP·1 + v[[ε, ε_EP], [−ε_EP, −ε]] is itself H_A in a rotated basis (constant SU(2); copy test YES at η_g = 0). Inside Γ its eigenvalue split is already purely imaginary, so the mode selection for D6 is already present before any loss is added. Where D6/D7 hold at small η_g they are **inherited from H_curve**: the winners are the same as at η_g = 0 (weights differ by at most the Δw listed below). The new term does not change the winners there and is not the mechanism. Also, the inputs (λ_EP, ε_EP, v) fix a and b up to a swap, so 'not using a, b' is nominal.

**Physics reading (Helios).** P1 = dissipative (imaginary) coupling in H_A's basis (curve sigma_z maps to H_A sigma_x under the constant SU(2) rotation; curve sigma_y maps to H_A sigma_z, the loss-contrast direction). It is the wrong direction to cause D6, which is selection by loss contrast, so it can only destroy D6 [standard + computed]. Check: under S^-1 X S with S = ½[1 − i(σx − σy + σz)], σ_z → σ_x and σ_y → −sigma_z [computed]. The sign (curve σ_y → −σ_z) does not matter, because only squares enter the discriminant and the copy test.

**Mechanism.** Transpose identity kept; the PT property that makes the inside-Γ split purely imaginary is broken by the imaginary coupling [computed]. H_try^T = σ_z H_try σ_z holds at every η_g (max residual 0.0e+00 over both placements, all η_g, 5 sample ε) [identity + computed]. Inside-Γ split at ε = 0.75 ε_EP (|Re Δλ|, |Im Δλ|): η_g = 0: (5.6e-17, 2.4e-01); η_g = 0.001: (2.6e-04, 2.4e-01); η_g = 0.003: (7.9e-04, 2.4e-01); η_g = 0.01: (2.6e-03, 2.4e-01); η_g = 0.03: (7.8e-03, 2.5e-01); η_g = 0.1: (2.6e-02, 2.5e-01); η_g = 0.3: (7.3e-02, 2.6e-01); η_g = 1: (1.7e-01, 3.8e-01); η_g = 3: (2.5e-01, 7.8e-01); η_g = 10: (2.7e-01, 2.3e+00) [computed].

The premise 'a scalar loss must make D6 fail' does not hold here. The scalar term cannot select a mode, but the selection comes from H_curve, so P0 gives exactly the η_g = 0 (H_A-like) winners. P0 is therefore a dynamical copy, not a new mechanism. For P0 the 'max Δw vs η_g = 0' should be exactly 0 [identity: c(ε)·1 commutes and drops out of the normalised dynamics]. The listed 4.9e-4 to 1.1e-3 are numerical error, the same size as the dt-halving column: they come entirely from the 0.75 ε_EP, γ_g T = 40 runs (1.25 ε_EP gives ~1e-16), where the rounding floor quoted above dominates [computed: floating-point floor, amplified exponentially along the loop at 0.75 ε_EP, γ_gT = 40; not integrator step error].

## Scan table

| placement | η_g | EPs (discriminant roots) | ±ε_EP kept | EPs inside the drive loop | loop 2π / 4π (continuation) | copy strict (s_min) | dynamical copy (s_min) | spectrum err vs H_A | γ_g | 0.75 ε_EP | 1.25 ε_EP | max Δw vs η_g = 0 | dt-halving Δw |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P0 scalar | 0 | +0.513681+0.000000i, -0.513681+0.000000i | yes | 1 | [1, 1] / [0, 0] | YES (1.4e-09) | YES (1.4e-09) | 2.1e-05 | 0.12240 | **D6-like** | **D7-like** | 0.0e+00 | 9.1e-04 |
| P0 scalar | 0.1 | +0.513681+0.000000i, -0.513681-0.000000i | yes | 1 | [1, 1] / [0, 0] | NO (1.5e-01) | YES (1.4e-09) | 2.4e-01 | 0.12240 | **D6-like** | **D7-like** | 4.9e-04 | 8.5e-04 |
| P0 scalar | 1 | +0.513681+0.000000i, -0.513681-0.000000i | yes | 1 | [1, 1] / [0, 0] | NO (5.4e-01) | YES (1.4e-09) | 2.4e+00 | 0.12240 | **D6-like** | **D7-like** | 1.1e-03 | 8.8e-04 |
| P0 scalar | 10 | +0.513681-0.000000i, -0.513681+0.000000i | yes | 1 | [1, 1] / [0, 0] | NO (6.2e-01) | YES (1.4e-09) | 2.4e+01 | 0.12240 | **D6-like** | **D7-like** | 6.3e-04 | 2.1e-03 |
| P1 sigma_z | 0 | +0.513681+0.000000i, -0.513681+0.000000i | yes | 1 | [1, 1] / [0, 0] | YES (1.4e-09) | YES (1.4e-09) | 2.1e-05 | 0.12240 | **D6-like** | **D7-like** | 0.0e+00 | 9.1e-04 |
| P1 sigma_z | 0.001 | -0.513680-360.253000i, +0.513680-360.253000i, -0.513681-0.000000i, +0.513681+0.000000i | yes | 1 | [1, 1] / [0, 0] | NO (1.4e-03) | NO (1.4e-03) | 2.5e-03 | 0.12240 | **D6-like** | **D7-like** | 1.6e-02 | 1.6e-03 |
| P1 sigma_z | 0.003 | -0.513681-120.084333i, +0.513681-120.084333i, -0.513681-0.000000i, +0.513681-0.000000i | yes | 1 | [1, 1] / [0, 0] | NO (4.2e-03) | NO (4.2e-03) | 7.6e-03 | 0.12240 | **D6-like** | **D7-like** | 4.6e-02 | 3.7e-04 |
| P1 sigma_z | 0.01 | -0.513681-36.025300i, +0.513681-36.025300i, -0.513681+0.000000i, +0.513681+0.000000i | yes | 1 | [1, 1] / [0, 0] | NO (1.4e-02) | NO (1.4e-02) | 2.5e-02 | 0.12242 | **D6-like** | **D7-like** | 1.6e-01 | 6.9e-04 |
| P1 sigma_z | 0.03 | +0.513681-12.008433i, -0.513681-12.008433i, +0.513681+0.000000i, -0.513681+0.000000i | yes | 1 | [1, 1] / [0, 0] | NO (4.2e-02) | NO (4.2e-02) | 7.6e-02 | 0.12252 | **NO** | **D7-like** | 2.6e-01 | 7.6e-04 |
| P1 sigma_z | 0.1 | +0.513681-3.602530i, -0.513681-3.602530i, +0.513681+0.000000i, -0.513681-0.000000i | yes | 1 | [1, 1] / [0, 0] | NO (1.3e-01) | NO (1.3e-01) | 2.5e-01 | 0.12369 | **NO** | **D7-like** | 3.1e-01 | 7.4e-06 |
| P1 sigma_z | 0.3 | +0.513681-1.200843i, -0.513681-1.200843i, +0.513681+0.000000i, -0.513681-0.000000i | yes | 1 | [1, 1] / [0, 0] | NO (3.3e-01) | NO (3.3e-01) | 7.5e-01 | 0.13280 | **NO** | **D7-like** | 3.1e-01 | 1.4e-07 |
| P1 sigma_z | 1 | +0.513681-0.360253i, +0.513681+0.000000i, -0.513681-0.360253i, -0.513681-0.000000i | yes | 1 | [1, 1] / [0, 0] | NO (5.4e-01) | NO (5.4e-01) | 2.5e+00 | 0.21089 | **NO** | **D7-like** | 3.1e-01 | 1.3e-08 |
| P1 sigma_z | 3 | +0.513681-0.120084i, +0.513681+0.000000i, -0.513681-0.120084i, -0.513681-0.000000i | yes | 2 | [0, 0] / [0, 0] | NO (6.1e-01) | NO (6.1e-01) | 7.3e+00 | 0.47933 | **D7-like** | **D7-like** | 3.1e-01 | 8.6e-09 |
| P1 sigma_z | 10 | +0.513681-0.036025i, +0.513681+0.000000i, -0.513681-0.036025i, -0.513681-0.000000i | yes | 2 | [0, 0] / [0, 0] | NO (6.2e-01) | NO (6.2e-01) | 2.4e+01 | 1.49610 | **D7-like** | **D7-like** | 3.1e-01 | 2.9e-09 |

## EP-location report

- The discriminant of H_try(P1) is ∝ (vε + iη_g F_JT)² − v²ε_EP² = (ε − ε_EP)(ε + ε_EP)[v + iη_g(ε + ε_EP)][v + iη_g(ε − ε_EP)] [identity].
- Its roots are **±ε_EP (kept, since the loss vanishes there) plus two new EPs at ±ε_EP + i v/η_g** (Im < 0 for η_g > 0, since v < 0) [identity; numerically confirmed in the per-η_g list]. For η_g → 0 the new EPs go to infinity. The loop r = 0.25 ε_EP encloses the new EP near +ε_EP once |v|/η_g < 0.25 ε_EP, i.e. η_g > 2.8053 [identity; checked against the computed in-loop counts on the grid: consistent].
- Every EP (old and new) shows a 2π swap and a 4π return on small circles (table in the per-η_g EP list below). For P0 the spectrum's EPs are exactly ±ε_EP for all η_g.
- When the loop encloses two EPs, the loop itself returns after 2π (monodromy of two square-root points), shown in the 'loop 2π / 4π' column.

### Per-η_g EP list (P1)

- η_g = 0: +0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop yes); -0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop no)
- η_g = 0.001: -0.513680-360.253000i (2π [1, 1], 4π [0, 0], in loop no); +0.513680-360.253000i (2π [1, 1], 4π [0, 0], in loop no); -0.513681-0.000000i (2π [1, 1], 4π [0, 0], in loop no); +0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop yes)
- η_g = 0.003: -0.513681-120.084333i (2π [1, 1], 4π [0, 0], in loop no); +0.513681-120.084333i (2π [1, 1], 4π [0, 0], in loop no); -0.513681-0.000000i (2π [1, 1], 4π [0, 0], in loop no); +0.513681-0.000000i (2π [1, 1], 4π [0, 0], in loop yes)
- η_g = 0.01: -0.513681-36.025300i (2π [1, 1], 4π [0, 0], in loop no); +0.513681-36.025300i (2π [1, 1], 4π [0, 0], in loop no); -0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop no); +0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop yes)
- η_g = 0.03: +0.513681-12.008433i (2π [1, 1], 4π [0, 0], in loop no); -0.513681-12.008433i (2π [1, 1], 4π [0, 0], in loop no); +0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop yes); -0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop no)
- η_g = 0.1: +0.513681-3.602530i (2π [1, 1], 4π [0, 0], in loop no); -0.513681-3.602530i (2π [1, 1], 4π [0, 0], in loop no); +0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop yes); -0.513681-0.000000i (2π [1, 1], 4π [0, 0], in loop no)
- η_g = 0.3: +0.513681-1.200843i (2π [1, 1], 4π [0, 0], in loop no); -0.513681-1.200843i (2π [1, 1], 4π [0, 0], in loop no); +0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop yes); -0.513681-0.000000i (2π [1, 1], 4π [0, 0], in loop no)
- η_g = 1: +0.513681-0.360253i (2π [1, 1], 4π [0, 0], in loop no); +0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop yes); -0.513681-0.360253i (2π [1, 1], 4π [0, 0], in loop no); -0.513681-0.000000i (2π [1, 1], 4π [0, 0], in loop no)
- η_g = 3: +0.513681-0.120084i (2π [1, 1], 4π [0, 0], in loop yes); +0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop yes); -0.513681-0.120084i (2π [1, 1], 4π [0, 0], in loop no); -0.513681-0.000000i (2π [1, 1], 4π [0, 0], in loop no)
- η_g = 10: +0.513681-0.036025i (2π [1, 1], 4π [0, 0], in loop yes); +0.513681+0.000000i (2π [1, 1], 4π [0, 0], in loop yes); -0.513681-0.036025i (2π [1, 1], 4π [0, 0], in loop no); -0.513681-0.000000i (2π [1, 1], 4π [0, 0], in loop no)

## Weights (P1, selected η_g)

Winner index 0 = slower-decaying (or higher-frequency if the decays are equal) at the start/end point. Weight = left-eigenvector weight of the winner.

| η_g | start | γ_g T | turn | ccw from 0 | ccw from 1 | cw from 0 | cw from 1 | class |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.75 | 40 | 2π | slower-decaying (0.7998) | slower-decaying (1.0000) | slower-decaying (0.8003) | slower-decaying (1.0000) | D6-like |
| 0 | 0.75 | 40 | 4π | slower-decaying (0.6922) | slower-decaying (0.8006) | slower-decaying (0.6923) | slower-decaying (0.8006) | D6-like |
| 0 | 0.75 | 100 | 2π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | D6-like |
| 0 | 0.75 | 100 | 4π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | D6-like |
| 0 | 1.25 | 40 | 2π | lower-frequency (0.9997) | lower-frequency (0.9997) | higher-frequency (0.9997) | higher-frequency (0.9997) | D7-like |
| 0 | 1.25 | 40 | 4π | lower-frequency (0.9997) | lower-frequency (0.9997) | higher-frequency (0.9997) | higher-frequency (0.9997) | D7-like |
| 0 | 1.25 | 100 | 2π | lower-frequency (1.0000) | lower-frequency (1.0000) | higher-frequency (1.0000) | higher-frequency (1.0000) | D7-like |
| 0 | 1.25 | 100 | 4π | lower-frequency (1.0000) | lower-frequency (1.0000) | higher-frequency (1.0000) | higher-frequency (1.0000) | D7-like |
| 0.001 | 0.75 | 40 | 2π | slower-decaying (0.7893) | slower-decaying (1.0000) | slower-decaying (0.8118) | slower-decaying (1.0000) | D6-like |
| 0.001 | 0.75 | 40 | 4π | slower-decaying (0.6786) | slower-decaying (0.7894) | slower-decaying (0.7079) | slower-decaying (0.8117) | D6-like |
| 0.001 | 0.75 | 100 | 2π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | D6-like |
| 0.001 | 0.75 | 100 | 4π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | D6-like |
| 0.001 | 1.25 | 40 | 2π | slower-decaying (0.9997) | slower-decaying (0.9997) | faster-decaying (0.9997) | faster-decaying (0.9997) | D7-like |
| 0.001 | 1.25 | 40 | 4π | slower-decaying (0.9997) | slower-decaying (0.9997) | faster-decaying (0.9997) | faster-decaying (0.9997) | D7-like |
| 0.001 | 1.25 | 100 | 2π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.001 | 1.25 | 100 | 4π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.003 | 0.75 | 40 | 2π | slower-decaying (0.7648) | slower-decaying (1.0000) | slower-decaying (0.8314) | slower-decaying (1.0000) | D6-like |
| 0.003 | 0.75 | 40 | 4π | slower-decaying (0.6458) | slower-decaying (0.7651) | slower-decaying (0.7345) | slower-decaying (0.8316) | D6-like |
| 0.003 | 0.75 | 100 | 2π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | D6-like |
| 0.003 | 0.75 | 100 | 4π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | D6-like |
| 0.003 | 1.25 | 40 | 2π | slower-decaying (0.9997) | slower-decaying (0.9997) | faster-decaying (0.9997) | faster-decaying (0.9997) | D7-like |
| 0.003 | 1.25 | 40 | 4π | slower-decaying (0.9997) | slower-decaying (0.9997) | faster-decaying (0.9997) | faster-decaying (0.9997) | D7-like |
| 0.003 | 1.25 | 100 | 2π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.003 | 1.25 | 100 | 4π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.01 | 0.75 | 40 | 2π | slower-decaying (0.6658) | slower-decaying (0.9995) | slower-decaying (0.8894) | slower-decaying (0.9999) | D6-like |
| 0.01 | 0.75 | 40 | 4π | slower-decaying (0.5280) | slower-decaying (0.6664) | slower-decaying (0.8188) | slower-decaying (0.8898) | D6-like |
| 0.01 | 0.75 | 100 | 2π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | D6-like |
| 0.01 | 0.75 | 100 | 4π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | D6-like |
| 0.01 | 1.25 | 40 | 2π | slower-decaying (0.9997) | slower-decaying (0.9997) | faster-decaying (0.9997) | faster-decaying (0.9997) | D7-like |
| 0.01 | 1.25 | 40 | 4π | slower-decaying (0.9997) | slower-decaying (0.9997) | faster-decaying (0.9997) | faster-decaying (0.9997) | D7-like |
| 0.01 | 1.25 | 100 | 2π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.01 | 1.25 | 100 | 4π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.03 | 0.75 | 40 | 2π | faster-decaying (0.6684) | slower-decaying (0.9755) | slower-decaying (0.9699) | slower-decaying (0.9996) | NO |
| 0.03 | 0.75 | 40 | 4π | faster-decaying (0.7818) | faster-decaying (0.6694) | slower-decaying (0.9477) | slower-decaying (0.9698) | NO |
| 0.03 | 0.75 | 100 | 2π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | NO |
| 0.03 | 0.75 | 100 | 4π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | NO |
| 0.03 | 1.25 | 40 | 2π | slower-decaying (0.9997) | slower-decaying (0.9997) | faster-decaying (0.9997) | faster-decaying (0.9997) | D7-like |
| 0.03 | 1.25 | 40 | 4π | slower-decaying (0.9997) | slower-decaying (0.9997) | faster-decaying (0.9997) | faster-decaying (0.9997) | D7-like |
| 0.03 | 1.25 | 100 | 2π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.03 | 1.25 | 100 | 4π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.1 | 0.75 | 40 | 2π | faster-decaying (0.9952) | faster-decaying (0.9948) | slower-decaying (0.9995) | slower-decaying (0.9995) | NO |
| 0.1 | 0.75 | 40 | 4π | faster-decaying (0.9971) | faster-decaying (0.9967) | slower-decaying (0.9991) | slower-decaying (0.9992) | NO |
| 0.1 | 0.75 | 100 | 2π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | NO |
| 0.1 | 0.75 | 100 | 4π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | NO |
| 0.1 | 1.25 | 40 | 2π | slower-decaying (0.9997) | slower-decaying (0.9997) | faster-decaying (0.9997) | faster-decaying (0.9997) | D7-like |
| 0.1 | 1.25 | 40 | 4π | slower-decaying (0.9997) | slower-decaying (0.9997) | faster-decaying (0.9997) | faster-decaying (0.9997) | D7-like |
| 0.1 | 1.25 | 100 | 2π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.1 | 1.25 | 100 | 4π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.3 | 0.75 | 40 | 2π | faster-decaying (0.9996) | faster-decaying (0.9996) | slower-decaying (0.9996) | slower-decaying (0.9996) | NO |
| 0.3 | 0.75 | 40 | 4π | faster-decaying (0.9996) | faster-decaying (0.9996) | slower-decaying (0.9996) | slower-decaying (0.9996) | NO |
| 0.3 | 0.75 | 100 | 2π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | NO |
| 0.3 | 0.75 | 100 | 4π | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | NO |
| 0.3 | 1.25 | 40 | 2π | slower-decaying (0.9998) | slower-decaying (0.9998) | faster-decaying (0.9998) | faster-decaying (0.9998) | D7-like |
| 0.3 | 1.25 | 40 | 4π | slower-decaying (0.9998) | slower-decaying (0.9998) | faster-decaying (0.9998) | faster-decaying (0.9998) | D7-like |
| 0.3 | 1.25 | 100 | 2π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 0.3 | 1.25 | 100 | 4π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 1 | 0.75 | 40 | 2π | faster-decaying (0.9996) | faster-decaying (0.9996) | slower-decaying (0.9996) | slower-decaying (0.9996) | NO |
| 1 | 0.75 | 40 | 4π | faster-decaying (0.9996) | faster-decaying (0.9996) | slower-decaying (0.9996) | slower-decaying (0.9996) | NO |
| 1 | 0.75 | 100 | 2π | slower-decaying (0.9998) | slower-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | NO |
| 1 | 0.75 | 100 | 4π | slower-decaying (0.9999) | slower-decaying (0.9998) | slower-decaying (0.9999) | slower-decaying (0.9999) | NO |
| 1 | 1.25 | 40 | 2π | slower-decaying (0.9998) | slower-decaying (0.9998) | faster-decaying (0.9998) | faster-decaying (0.9998) | D7-like |
| 1 | 1.25 | 40 | 4π | slower-decaying (0.9998) | slower-decaying (0.9998) | faster-decaying (0.9998) | faster-decaying (0.9998) | D7-like |
| 1 | 1.25 | 100 | 2π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 1 | 1.25 | 100 | 4π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 3 | 0.75 | 40 | 2π | faster-decaying (0.9997) | faster-decaying (0.9997) | slower-decaying (0.9997) | slower-decaying (0.9997) | D7-like |
| 3 | 0.75 | 40 | 4π | faster-decaying (0.9997) | faster-decaying (0.9997) | slower-decaying (0.9997) | slower-decaying (0.9997) | D7-like |
| 3 | 0.75 | 100 | 2π | faster-decaying (0.9888) | faster-decaying (0.9975) | slower-decaying (1.0000) | slower-decaying (1.0000) | D7-like |
| 3 | 0.75 | 100 | 4π | faster-decaying (0.9945) | faster-decaying (0.9954) | slower-decaying (1.0000) | slower-decaying (1.0000) | D7-like |
| 3 | 1.25 | 40 | 2π | slower-decaying (0.9998) | slower-decaying (0.9998) | faster-decaying (0.9998) | faster-decaying (0.9998) | D7-like |
| 3 | 1.25 | 40 | 4π | slower-decaying (0.9998) | slower-decaying (0.9998) | faster-decaying (0.9998) | faster-decaying (0.9998) | D7-like |
| 3 | 1.25 | 100 | 2π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 3 | 1.25 | 100 | 4π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 10 | 0.75 | 40 | 2π | faster-decaying (0.9998) | faster-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | D7-like |
| 10 | 0.75 | 40 | 4π | faster-decaying (0.9999) | faster-decaying (0.9999) | slower-decaying (0.9999) | slower-decaying (0.9999) | D7-like |
| 10 | 0.75 | 100 | 2π | faster-decaying (1.0000) | faster-decaying (1.0000) | slower-decaying (1.0000) | slower-decaying (1.0000) | D7-like |
| 10 | 0.75 | 100 | 4π | faster-decaying (1.0000) | faster-decaying (1.0000) | slower-decaying (1.0000) | slower-decaying (1.0000) | D7-like |
| 10 | 1.25 | 40 | 2π | slower-decaying (0.9999) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 10 | 1.25 | 40 | 4π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 10 | 1.25 | 100 | 2π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |
| 10 | 1.25 | 100 | 4π | slower-decaying (1.0000) | slower-decaying (1.0000) | faster-decaying (1.0000) | faster-decaying (1.0000) | D7-like |

## Copy test details

- Strict: the smallest relative singular value of the stacked system S H_try(ε_k) − H_A(αε_k + β) S = 0 over 6 complex ε_k, minimised over complex α, β (Nelder–Mead, 5 starts). Copy if ≤ 1e-8. At a single ε any two matrices with the same eigenvalues are similar, which is why the constant-S test is the meaningful one.
- Dynamical: the same test on the traceless parts (removes any c(ε)·1, which does not affect normalised dynamics).
- η_g = 0: s_min ≈ 1.4e-9, the rounding level of the given ε_EP (0.51368066 vs |b−a|/(2|v|) = 0.5136806633). The spectrum error of about 2e-5 is the √-amplified rounding near the EPs. Copy YES.
- P1, η_g > 0: copy NO [identity]. A constant S preserves the spectrum, and P1's discriminant is quartic in ε while H_A(αε + β)'s is quadratic, so no S and no affine reparametrisation can work; η_g does not recreate a and b. The numerical s_min values agree [computed].
- P0, η_g > 0: dynamical copy YES [identity], because c(ε)·1 commutes with everything and drops out of the traceless part. Strict NO only because the trace differs [computed].

## Caveats

- The mode selection is inherited from H_curve (≡ H_A up to a constant rotation) wherever D6/D7 hold at small η_g; see 'max Δw vs η_g = 0'.
- γ_g (Venus): at η_g = 0, γ_g = |v| ε_EP √(0.25·1.75) = 0.12240 (numeric 0.12240), the smallest split on the loop (at ε = 0.75 ε_EP, where the split is purely imaginary, so it is also the max |Im| gap used as the definition). Since |a−b|/2 = |v| ε_EP, γ_g/(|a−b|/2) = √7/4 = 0.661438 exactly [identity]. This is a definitional ratio, not a physical difference; γ_g T = 40 corresponds to drive-return's γT = 40·4/√7.
- For η_g > 0 the 1.25 ε_EP winners switch from frequency to decay ordering, and the equal-frequency/equal-decay regions no longer lie on the real axis. 'D7-like' at 1.25 ε_EP is a real chirality but not a like-for-like comparison with drive-return (Helios).
- dt-halving changes are listed per row. At 0.75 ε_EP, γ_g T = 40 they sit at a ~1e-3 rounding floor (see the verdict) [computed: floating-point floor, amplified exponentially along the loop at 0.75 ε_EP, γ_gT = 40; not integrator step error], so values near 1e-3 there do not measure step-size error. At 1.25 ε_EP they are step-size error.
- New EPs at ±ε_EP + iv/η_g move into the drive loop for η_g > 2.8, which changes the loop's monodromy. D6/D7 there are not comparable to the H_A case.
- [by construction]: H_curve; the placements; γ_g. [computed]: EPs, copy tests, weights. [identity]: the factorisation of the discriminant, the EP locations, the γ_g ratio, P1 copy NO, P0 dynamical copy YES. [hive-interpretation]: calling iη_g F_JT σ_z 'gravity-side' (an imaginary dilaton shift).

## Post-hoc notes (criteria as fixed in README; the final grade PARTIAL follows the Venus/Helios sign-off)

- The HAVE window [0.001, 0.003, 0.01] is exactly one decade by the grid. Its lowest point (η_g = 0.001) fails the dt-halving check (Δw = 1.6e-03 > 1e-3). Using only rows with dt-halving Δw ≤ 1e-3, the window is [0.003, 0.01] = 0.52 decades, which is under one decade and would be flagged. The robustness claim therefore rests on a numerically marginal point (see the dt refinement in the verdict).
- Inside the window the winner weights differ from η_g = 0 (the H_A-equivalent curve part) by at most 1.6e-01; the winners are unchanged from η_g = 0, and the shift grows steadily towards the D6 flip at η_g = 0.03. D6/D7 in the window are inherited from H_curve, not produced by the new loss.
- Once the loss is strong enough to change the weights (η_g ≥ 0.03), D6 fails at 0.75 ε_EP. At γ_g T = 40, ccw and cw pick different modes inside Γ (ccw → faster-decaying, cw → slower-decaying at η_g = 0.1), while at γ_g T = 100 both pick the slower-decaying mode. That is chirality inside Γ at moderate speed [computed; mechanism: inside-Γ split no longer purely imaginary, so equal-frequency is lost].
- For η_g ≥ 3 the new EP at ε_EP + iv/η_g lies inside the drive loop. The loop then encloses two EPs, returns after 2π, and both starts are D7-like.
- Physics reading: the new σ_z term does not supply the D6 mechanism; wherever it is strong enough to matter it destroys D6. So HAVE holds only weakly by the letter of the rule, and a gravity-side loss that *causes* D6 has not been found; hence PARTIAL [hive-interpretation of the computed table].

## Offered next run (not started)

- Loss-contrast placement: a term ∝ F_JT on curve σ_y (= H_A σ_z). It keeps the EPs at ±ε_EP and tests 'gravity-side loss causes D6' on the right footing. 'Gravity-side' is [hive-interpretation].

No folders were loaded (nothing to SHA-check); only this folder was written.


# pairA-qg-loss-sz

Follow-up to pairA-qg-loss (the loss-contrast placement Helios offered). No folders are loaded; the numbers come from the job spec only: a = 0.12337, b = 0.49348, v = −0.360253, ε_EP = 0.51368066, λ_EP = −0.308425i, F_JT = ε² − ε_EP². No git. No claim of QG, a JT dual, or an Einstein solution. Gravity-side is hive language [hive-interpretation].

## Operator (H_A basis)

- H_A = −i(a+b)/2·1 + vε σ_x − i(a−b)/2 σ_z.
- Real curve part: H_real = λ_EP·1 + vε σ_x − i(a−b)/2 σ_z. Since λ_EP = −i(a+b)/2, **H_real is H_A itself (the η_g = 0 point)** [by construction].
- H_try(ε) = H_real(ε) + iη_g F_JT(ε) σ_z. The extra term is diagonal contrast: +iη_g F on entry 11 and −iη_g F on entry 22. Equivalently, H_A with ε-dependent rates a → a − η_g F and b → b + η_g F. The trace, and so λ_EP, is unchanged.
- The previous coupling term (curve σ_z, which is H_A σ_x) is not used.
- η_g grid: {0, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.2, 0.3, 0.35, |v|/(2ε_EP) (computed), 0.4, 1, 3}. η_g is never set from a or b.

## EPs

- Discriminant D(ε) = (tr² − 4 det)/4 = v²ε² − (κ + η_g F)², with κ = (b − a)/2 > 0.
- With κ = |v|ε_EP this factorises as (ε − ε_EP)(ε + ε_EP)[η_g(ε + ε_EP) − |v|][η_g(ε − ε_EP) + |v|] (up to sign) [identity].
- Roots: ±ε_EP and ±(|v|/η_g − ε_EP).
- For each η_g the run reports: the numerical roots, the distinct count and the count with multiplicity, whether ±ε_EP are kept, the 2π swap and 4π return on small circles, and the Jordan structure at the root next to +ε_EP.

## Copy check

- A copy means a constant (ε-independent) S with S H_try(ε) S⁻¹ = H_A(αε + β) for all ε.
- The test: the smallest relative singular value of the stacked linear system over 6 complex sample ε, minimised over complex α and β (Nelder–Mead, 5 starts). Copy if ≤ 1e-8.
- "Dynamical" copy: the same test on the traceless parts. A scalar c(ε)·1 does not matter for normalised dynamics.
- At a single ε any two 2×2 matrices with the same eigenvalues are similar. That is why only the constant-S test is meaningful.

## Drive protocol (as in pairA-drive-return / pairA-qg-loss)

- Loop: ε = ε_EP + 0.25 ε_EP e^{i(sθ + φ₀)}, starting at 0.75 ε_EP (φ₀ = π) and at 1.25 ε_EP (φ₀ = 0).
- Directions: ccw (s = +1) and cw (s = −1). Start modes 0 and 1. Weights are read after 1 and 2 turns (2π and 4π).
- Primary speed: γT = 40 and 100, with γ = |a − b|/2 (the same speed as drive-return). dt = 0.01/γ, exact 2×2 exponential at the midpoint, renormalised every step.
- Secondary (not used in the grade): γ_g T = 40 and 100, with γ_g = ½ max |Im Δλ| on the loop.
  - The literal "min imaginary split" is 0 wherever the split is real.
  - At η_g = 0, γ_g equals ½ the smallest |Δλ| on the loop, as in pairA-qg-loss.
- Mode labels at the start point: index 0 is the slower-decaying mode, or the higher-frequency mode if the decays are equal. Weight = left-eigenvector weight.
  - Physical winner: the dominant H_A-basis component of the winner's right eigenvector (1 = the −ia site, 2 = the −ib site).
- D6-like: for every speed and turn, ccw and cw pick the same winner and it is index 0 (slower-decaying), for both start modes.
- D7-like: for every speed and turn, ccw and cw pick different winners, and each direction's winner does not depend on the start mode. Otherwise NO.
- Phase at a start point: "broken" if the split is purely imaginary (the decays differ), "unbroken" if it is real. H_A has 0.75 ε_EP broken and 1.25 ε_EP unbroken.
- Checks:
  - dt-halving at γT = 40, start mode 0, both directions.
  - Rounding probe: add 1e-15·i·1 at η_g = 0, start at 0.75 ε_EP, γT = 40.

## Grade rules (fixed before running)

- **Excluded rows.** The grade may not rest on these:
  - (E1) a new EP ±(|v|/η_g − ε_EP) lies inside the drive loop or within 0.1 ε_EP of the loop circle;
  - (E2) the phase structure differs from H_A's (0.75 ε_EP must be broken and 1.25 ε_EP unbroken).
- **Floor(η_g)** = max(the dt-halving Δw of that row, the dt-halving Δw at η_g = 0, the rounding-probe Δw).
- **Caused** (an eligible row with η_g > 0) requires both:
  - the 0.75 ε_EP class is D6-like; and
  - either (a) the physical winner differs from the η_g = 0 run in some 0.75 ε_EP run, or (b) the purity P = min over direction and start mode of the 0.75 ε_EP winner weight, at some (γT, turn), exceeds the η_g = 0 value by more than 10 × Floor(η_g).
- **HAVE:** some eligible η_g > 0 row is not a copy (strict and dynamical both NO) and is caused. Flag it if it holds only at a single grid point rather than at least 2 consecutive eligible points.
- **PARTIAL:** not a copy, but no eligible row is caused, so D6 still comes only from the real H_A part.
- **MISSING:** every η_g > 0 row is a copy (H_A was pasted).

## Tags

[identity], [computed], [by construction], [hive-interpretation].

## Files

H_try.py (operator, discriminant, EPs, copy check), drive_test.py (drive protocol), run.py (writes RESULTS.md and stops).

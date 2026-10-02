# pairA-qg-loss-sz — RESULTS

**Signed off 2026-09-26:** Venus (maths) and Helios (physics).

Loss-contrast placement (the follow-up Helios offered after pairA-qg-loss). No folder was loaded; the numbers are from the job spec only (a = 0.12337, b = 0.49348, v = −0.360253, ε_EP = 0.51368066, λ_EP = −0.308425i, F_JT = ε² − ε_EP²). No claim of QG, a JT dual, or an Einstein solution.

gravity-side is hive language [hive-interpretation]

## Verdict

**GRADE (letter): HAVE, single grid point; GRADE (physics): PARTIAL, D6 inherited**

- Original-rule letter result (README rule as fixed; the README's scalar probe cancels exactly, so the traceless probe at η_g = 0, γT = 40 is used in its place, Δw = 2.3e-07): **HAVE** (FLAG: single grid point). Rows meeting the HAVE rule: [0.2]. Eligible rows (not E1/E2): ['0.001', '0.003', '0.01', '0.03', '0.1', '0.2'].
- **post-hoc Hive-amended floor (not the pre-fixed rule):** floor(η_g) = max over γT = 40 and 100 of (dt-halving Δw, random traceless 1e-15 probe Δw), on the row and on η_g = 0. Letter grade recomputed: **PARTIAL** (rows meeting HAVE: none). η_g = 0.2 **does not pass**: amended floor 4.0e-02, so 10 × floor = 4.0e-01 against its largest purity rise +8.2e-03.
- **Trigger of the letter HAVE** [threshold artifact risk]: the +0.008 rise at η_g = 0.2 (γT = 40, 2π) is purification timing / non-adiabatic wobble, winner unchanged, non-monotonic (0.8032, 0.7901, 0.8114).
- **Copy of H_A:** YES at η_g = 0 (H_try(0) − H_A = 5.6e-17: H_real **is** H_A [by construction]). NO for every η_g > 0, strict and dynamical [identity: a constant S and an affine ε map preserve the degree of the discriminant, which is quartic in ε for η_g > 0 and quadratic for H_A(αε + β); computed s_min in the table]. The scalar part does not matter (the dynamical test drops it). **Not a constant basis change, but the same family as H_A**: H_try = H_A with ε-dependent rates a → a − η_g F_JT and b → b + η_g F_JT [identity; numeric residual 2.2e-16].

## Basis form of the extra term (H_A basis)

- H_real = `Matrix([
[ -I*a, eps*v],
[eps*v,  -I*b]])` = H_A [by construction].
- H_try = `Matrix([
[I*(-a + eta_g*(eps**2 - eps_EP**2)),                               eps*v],
[                              eps*v, I*(-b - eta_g*(eps**2 - eps_EP**2))]])`.
- H_try − H_A(a → a − η_g F, b → b + η_g F) = `Matrix([
[0, 0],
[0, 0]])` [identity]. The trace is unchanged, so λ_EP = −i(a+b)/2 is unchanged.
- The extra term iη_g F_JT σ_z is **diagonal contrast**: +iη_g F on entry 11 and −iη_g F on entry 22, and nothing off-diagonal.
- Sample ε = 0.3, η_g = 0.1: H_try − H_A = diag(0.000000-0.017387j, 0.000000+0.017387j); off-diagonal 0.0e+00 [computed]. F_JT(0.3) = -0.173868.
- Sign: with ψ ~ e^{−iλt}, entry 11 has rate a − η_g F. Inside Γ (F < 0) the −ia site loses more and the −ib site less, so the effective contrast κ + η_g F falls. Outside Γ (F > 0) the contrast rises.

## EPs vs η_g

- D(ε) = (tr² − 4 det)/4 = v²ε² − (κ + η_g F)², κ = (b − a)/2 = 0.185055 > 0 [identity; sympy residual 0, numeric 2.7e-15].
- With κ = |v|ε_EP: D = −(ε − ε_EP)(ε + ε_EP)[η_g(ε + ε_EP) − |v|][η_g(ε − ε_EP) + |v|] [identity; sympy residual 0]. Roots: **±ε_EP (kept at every η_g) and new real EPs at ±(|v|/η_g − ε_EP)**, exactly (not only 'about').
- Rounding: the spec's ε_EP = 0.51368066 vs κ/|v| = 0.5136806633 (3.3e-10 apart), so D(±ε_EP) = v²ε_EP² − κ² = 4.4e-10 rather than 0. D(±ε_EP) does not depend on η_g, because F_JT(±ε_EP) = 0; 'kept' is tested this way (|D(±ε_EP)| < 1e-9). Near the coalescence the square root amplifies the rounding: at η_g* the double root splits into a pair about 5.8e-05 off the real axis, and at η_g = 0.35 the near-pair roots move by about 1e-6. Roots within 0.001 are counted as one (near-)coalesced EP. With the exact ε_EP = κ/|v| (check only), the η_g* roots next to +ε_EP are 6.1e-09 from it, a double root up to numerical root-finding [computed].
- **Coalescence:** at eta_g* = |v|/(2 eps_EP) = 0.35065852 each new EP merges with an old tip (D proportional to (eps -/+ eps_EP)^2): non-generic EP2, defective, no branch point, trivial monodromy [identity + computed; see the row].
- **Second non-generic point (Venus):** at η_g = |v|/ε_EP = 0.7013 the two new EPs meet at ε = 0, outside the loop (D ∝ ε²(ε² − ε_EP²)). This explains the phase swap between η_g = 0.4 and 1 [identity]. Computed roots there: -0.513681+0.000000i, +0.513681+0.000000i, -0.000000+0.000000i ×2; small-circle 2π swap / 4π return: -0.513681+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0]; -0.000000+0.000000i: [0, 0]/[0, 0] [computed].
- New-EP enclosure (E1, fixed rule: inside the loop or within 0.1 ε_EP of it): |v|/η_g − ε_EP is inside the loop for η_g ∈ (0.3117, 0.4008), and ε_EP − |v|/η_g is inside for η_g > 2.8053 [identity]. Rows flagged E1 are listed below.
- Phase at the start points (E2): 0.75 ε_EP stays broken only for η_g < 0.4008 (it becomes unbroken when the new EP crosses 0.75 ε_EP, and broken again with flipped contrast for η_g > 2.8053). 1.25 ε_EP becomes broken for η_g > 0.3117 [identity].

| η_g | n_EP distinct | n_EP with mult | roots (×mult) | ±ε_EP kept | all real | closed-form err | E1 (new EP in/near loop) | small-circle 2π swap / 4π return | Jordan at +ε_EP (|eig|, ‖M‖, mult) | loop 2π / 4π |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2 | 2 | -0.513681+0.000000i, +0.513681+0.000000i | yes | yes | 3.3e-09 | no | -0.513681+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0] | (2.7e-09, 0.37, 1) | [1, 1] / [0, 0] |
| 0.001 | 4 | 4 | -359.739319+0.000000i, +359.739319+0.000000i, -0.513681+0.000000i, +0.513681+0.000000i | yes | yes | 3.3e-09 | no (+359.7393: dist 359.0972, -359.7393: dist 360.1246) | -359.739319+0.000000i: [1, 1]/[0, 0]; +359.739319+0.000000i: [1, 1]/[0, 0]; -0.513681+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0] | (9.2e-09, 0.37, 1) | [1, 1] / [0, 0] |
| 0.003 | 4 | 4 | -119.570653+0.000000i, +119.570653+0.000000i, -0.513681+0.000000i, +0.513681+0.000000i | yes | yes | 3.3e-09 | no (+119.5707: dist 118.9286, -119.5707: dist 119.9559) | -119.570653+0.000000i: [1, 1]/[0, 0]; +119.570653+0.000000i: [1, 1]/[0, 0]; -0.513681+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0] | (7.3e-09, 0.37, 1) | [1, 1] / [0, 0] |
| 0.01 | 4 | 4 | -35.511619+0.000000i, +35.511619+0.000000i, -0.513681+0.000000i, +0.513681+0.000000i | yes | yes | 3.4e-09 | no (+35.5116: dist 34.8695, -35.5116: dist 35.8969) | -35.511619+0.000000i: [1, 1]/[0, 0]; +35.511619+0.000000i: [1, 1]/[0, 0]; -0.513681+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0] | (5.6e-09, 0.37, 1) | [1, 1] / [0, 0] |
| 0.03 | 4 | 4 | -11.494753+0.000000i, +11.494753+0.000000i, -0.513681+0.000000i, +0.513681+0.000000i | yes | yes | 3.6e-09 | no (+11.4948: dist 10.8527, -11.4948: dist 11.8800) | -11.494753+0.000000i: [1, 1]/[0, 0]; +11.494753+0.000000i: [1, 1]/[0, 0]; -0.513681+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0] | (1.9e-09, 0.37, 1) | [1, 1] / [0, 0] |
| 0.1 | 4 | 4 | +3.088849+0.000000i, -3.088849+0.000000i, -0.513681+0.000000i, +0.513681+0.000000i | yes | yes | 4.6e-09 | no (+3.0888: dist 2.4467, -3.0888: dist 3.4741) | +3.088849+0.000000i: [1, 1]/[0, 0]; -3.088849+0.000000i: [1, 1]/[0, 0]; -0.513681+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0] | (4.0e-09, 0.37, 1) | [1, 1] / [0, 0] |
| 0.2 | 4 | 4 | -1.287584+0.000000i, +1.287584+0.000000i, -0.513681+0.000000i, +0.513681+0.000000i | yes | yes | 7.7e-09 | no (+1.2876: dist 0.6455, -1.2876: dist 1.6728) | -1.287584+0.000000i: [1, 1]/[0, 0]; +1.287584+0.000000i: [1, 1]/[0, 0]; -0.513681+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0] | (3.2e-09, 0.37, 1) | [1, 1] / [0, 0] |
| 0.3 | 4 | 4 | -0.687163+0.000000i, -0.513681+0.000000i, +0.687163+0.000000i, +0.513681+0.000000i | yes | yes | 2.3e-08 | **YES** (+0.6872: dist 0.0451, -0.6872: dist 1.0724) | -0.687163+0.000000i: [1, 1]/[0, 0]; -0.513681+0.000000i: [1, 1]/[0, 0]; +0.687163+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0] | (2.8e-09, 0.37, 1) | [1, 1] / [0, 0] |
| 0.35 | 4 | 4 | -0.515612+0.000000i, -0.513682+0.000000i, +0.515612+0.000000i, +0.513682+0.000000i | yes | yes | 1.8e-06 | **YES** (+0.5156: inside, -0.5156: dist 0.9009) | -0.515612+0.000000i: [1, 1]/[0, 0]; -0.513682+0.000000i: [1, 1]/[0, 0]; +0.515612+0.000000i: [1, 1]/[0, 0]; +0.513682+0.000000i: [1, 1]/[0, 0] | (2.7e-09, 0.37, 1) | [0, 0] / [0, 0] |
| 0.350659 (=|v|/(2ε_EP)) | 2 | 4 | -0.513681+0.000000i ×2, +0.513681+0.000000i ×2 | yes | no | 5.8e-05 | **YES** (+0.5137: inside, -0.5137: dist 0.8989) | -0.513681+0.000000i: [0, 0]/[0, 0]; +0.513681+0.000000i: [0, 0]/[0, 0] | (5.2e-09, 0.37, 2) | [0, 0] / [0, 0] |
| 0.4 | 4 | 4 | -0.513681+0.000000i, -0.386952+0.000000i, +0.513681+0.000000i, +0.386952+0.000000i | yes | yes | 2.4e-08 | **YES** (+0.3870: inside, -0.3870: dist 0.7722) | -0.513681+0.000000i: [1, 1]/[0, 0]; -0.386952+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0]; +0.386952+0.000000i: [1, 1]/[0, 0] | (1.9e-13, 0.37, 1) | [0, 0] / [0, 0] |
| 1 | 4 | 4 | -0.513681+0.000000i, +0.513681+0.000000i, -0.153428+0.000000i, +0.153428+0.000000i | yes | yes | 1.8e-09 | no (-0.1534: dist 0.5387, +0.1534: dist 0.2318) | -0.513681+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0]; -0.153428+0.000000i: [1, 1]/[0, 0]; +0.153428+0.000000i: [1, 1]/[0, 0] | (5.7e-09, 0.37, 1) | [1, 1] / [0, 0] |
| 3 | 4 | 4 | -0.513681+0.000000i, -0.393596+0.000000i, +0.513681+0.000000i, +0.393596+0.000000i | yes | yes | 4.4e-10 | **YES** (-0.3936: dist 0.7789, +0.3936: inside) | -0.513681+0.000000i: [1, 1]/[0, 0]; -0.393596+0.000000i: [1, 1]/[0, 0]; +0.513681+0.000000i: [1, 1]/[0, 0]; +0.393596+0.000000i: [1, 1]/[0, 0] | (9.7e-09, 0.37, 1) | [0, 0] / [0, 0] |

## D6/D7 table vs η_g (primary: γ = |a − b|/2, γT = 40 and 100)

γ = 0.185055. dt = 0.01/γ. The rounding probe is a random traceless 1e-15 matrix (fixed seed, 3 draws, max taken); a scalar probe cancels exactly in the propagator. The floors per speed are in the next table. The 'floor' column here is the original-rule floor [computed].

| η_g | copy strict / dyn (s_min) | E1 | phase 0.75 / 1.25 | **0.75 ε_EP** | **1.25 ε_EP** | eligible | dt-halving Δw | floor | 0.75 physical winner changed vs η_g = 0 | max ΔP (0.75 purity vs η_g = 0) | purity climb > 10×floor | caused | γ_g | secondary (γ_g T) 0.75 / 1.25 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | YES / YES (5.0e-17 / 5.4e-17) | no | broken / unbroken | **D6-like** | **D7-like** | no | 5.2e-08 | 2.3e-07 | no | +0.00e+00 | no | no | 0.12240 | D6-like / D7-like |
| 0.001 | NO / NO (1.5e-03 / 1.5e-03) | no | broken / unbroken | **D6-like** | **D7-like** | yes | 1.9e-07 | 2.3e-07 | no | -2.58e-04 | no | no | 0.12223 | D6-like / D7-like |
| 0.003 | NO / NO (4.6e-03 / 4.6e-03) | no | broken / unbroken | **D6-like** | **D7-like** | yes | 1.1e-07 | 2.3e-07 | no | -7.82e-04 | no | no | 0.12188 | D6-like / D7-like |
| 0.01 | NO / NO (1.5e-02 / 1.5e-02) | no | broken / unbroken | **D6-like** | **D7-like** | yes | 4.2e-08 | 2.3e-07 | no | -2.70e-03 | no | no | 0.12065 | D6-like / D7-like |
| 0.03 | NO / NO (4.6e-02 / 4.6e-02) | no | broken / unbroken | **D6-like** | **D7-like** | yes | 1.3e-07 | 2.3e-07 | no | -8.40e-03 | no | no | 0.11710 | D6-like / D7-like |
| 0.1 | NO / NO (1.5e-01 / 1.5e-01) | no | broken / unbroken | **D6-like** | **D7-like** | yes | 8.7e-08 | 2.3e-07 | no | -1.31e-02 | no | no | 0.10413 | D6-like / D7-like |
| 0.2 | NO / NO (2.7e-01 / 2.7e-01) | no | broken / unbroken | **D6-like** | **D7-like** | yes | 5.7e-08 | 2.3e-07 | no | -3.22e-01 | YES | YES | 0.08349 | D6-like / D7-like |
| 0.3 | NO / NO (3.7e-01 / 3.7e-01) | YES | broken / unbroken | **D6-like** | **D7-like** | no | 3.3e-08 | 2.3e-07 | no | -2.98e-01 | YES | no | 0.05800 | D6-like / D7-like |
| 0.35 | NO / NO (4.1e-01 / 4.1e-01) | YES | broken / broken | **D6-like** | **D6-like** | no | 5.8e-08 | 2.3e-07 | no | -3.82e-01 | no | no | 0.05160 | D6-like / D6-like |
| 0.350659 (=|v|/(2ε_EP)) | NO / NO (4.1e-01 / 4.1e-01) | YES | broken / broken | **D6-like** | **D6-like** | no | 5.7e-08 | 2.3e-07 | no | -3.87e-01 | no | no | 0.05205 | D6-like / D6-like |
| 0.4 | NO / NO (4.5e-01 / 4.5e-01) | YES | broken / broken | **D6-like** | **D6-like** | no | 3.9e-08 | 2.3e-07 | no | -5.00e-01 | no | no | 0.07896 | NO / D6-like |
| 1 | NO / NO (5.6e-01 / 5.6e-01) | no | unbroken / broken | **D7-like** | **D6-like** | no | 2.3e-06 | 2.3e-06 | no | +3.03e-01 | YES | no | 0.24021 | D7-like / D6-like |
| 3 | NO / NO (6.0e-01 / 6.0e-01) | YES | broken / broken | **NO** | **D6-like** | no | 1.4e-06 | 1.4e-06 | YES | -5.00e-01 | no | no | 0.58635 | NO / NO |

## Winners and purity

- **Winners-change line:** 0.75 ε_EP winners at η_g = 0: [('slower-decaying', 1)] (label, physical site). Small η_g (≤ 0.01): unchanged. Largest eligible η_g (≥ 0.1: ['0.1', '0.2']): unchanged. Non-eligible rows: η_g = 0.3: [('slower-decaying', 1)]; η_g = 0.35: [('slower-decaying', 1)]; η_g = 0.350659 (=|v|/(2ε_EP)): [('slower-decaying', 1)]; η_g = 0.4: [('slower-decaying', 1)]; η_g = 1: [('higher-frequency', 1), ('lower-frequency', 1)]; η_g = 3: [('faster-decaying', 1), ('slower-decaying', 2)] [computed].
- **Purity:** max |ΔP| at 0.75 ε_EP on eligible rows: η_g = 0.001: -2.58e-04 (amended floor 7.6e-07); η_g = 0.003: -7.82e-04 (amended floor 4.0e-07); η_g = 0.01: -2.70e-03 (amended floor 9.5e-07); η_g = 0.03: -8.40e-03 (amended floor 4.5e-06); η_g = 0.1: -1.31e-02 (amended floor 3.7e-04); η_g = 0.2: -3.22e-01 (amended floor 4.0e-02) [computed].
- **Largest clean purity drop** (a drop exceeding 10 × the amended floor, which covers both speeds): ΔP = -1.31e-02 at η_g = 0.1, γT = 40, 2π [computed].
- **η_g = 0.2, γT = 100** [numerical, cause not established]: the cw and ccw weights differ at the 1e-2 level (max 1.4e-02). The row is rounding-dominated (dt-halving 4.0e-02, probe up to 2.1e-02) and is not evidence either way. An optional high-precision re-run is offered, not done.

### Floors per speed (0.75 ε_EP; dt-halving at start mode 0, both directions; probe over 3 draws × both directions × both start modes)

| η_g | dt-halving γT = 40 | dt-halving γT = 100 | probe γT = 40 | probe γT = 100 | amended floor (incl. η_g = 0) | purity climb > 10×amended floor | caused (amended) |
|---|---|---|---|---|---|---|---|
| 0 | 5.2e-08 | 3.7e-07 | 2.3e-07 | 3.3e-07 | 3.7e-07 | (baseline) | (baseline) |
| 0.001 | 1.9e-07 | 7.6e-07 | 1.2e-07 | 6.3e-07 | 7.6e-07 | no | no |
| 0.003 | 1.1e-07 | 3.4e-07 | 1.6e-07 | 4.0e-07 | 4.0e-07 | no | no |
| 0.01 | 4.2e-08 | 2.9e-07 | 6.5e-08 | 9.5e-07 | 9.5e-07 | no | no |
| 0.03 | 1.3e-07 | 7.9e-07 | 3.8e-08 | 4.5e-06 | 4.5e-06 | no | no |
| 0.1 | 8.7e-08 | 3.7e-04 | 9.4e-09 | 2.4e-04 | 3.7e-04 | no | no |
| 0.2 | 5.7e-08 | 4.0e-02 | 5.7e-10 | 2.1e-02 | 4.0e-02 | no | no |

### Weights (primary speeds)

| η_g | start | γT | turn | ccw from 0 | ccw from 1 | cw from 0 | cw from 1 | class |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.75 | 40 | 2π | slower-decaying [site 1] (0.8032) | slower-decaying [site 1] (0.9996) | slower-decaying [site 1] (0.8032) | slower-decaying [site 1] (0.9996) | D6-like |
| 0 | 0.75 | 40 | 4π | slower-decaying [site 1] (0.6951) | slower-decaying [site 1] (0.8064) | slower-decaying [site 1] (0.6951) | slower-decaying [site 1] (0.8064) | D6-like |
| 0 | 0.75 | 100 | 2π | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | D6-like |
| 0 | 0.75 | 100 | 4π | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | D6-like |
| 0 | 1.25 | 40 | 2π | lower-frequency [site 2] (0.9994) | lower-frequency [site 2] (0.9994) | higher-frequency [site 2] (0.9994) | higher-frequency [site 2] (0.9994) | D7-like |
| 0 | 1.25 | 40 | 4π | lower-frequency [site 1] (0.9994) | lower-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | D7-like |
| 0 | 1.25 | 100 | 2π | lower-frequency [site 2] (0.9999) | lower-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | D7-like |
| 0 | 1.25 | 100 | 4π | lower-frequency [site 1] (0.9999) | lower-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | D7-like |
| 0.001 | 0.75 | 40 | 2π | slower-decaying [site 1] (0.8029) | slower-decaying [site 1] (0.9997) | slower-decaying [site 1] (0.8029) | slower-decaying [site 1] (0.9997) | D6-like |
| 0.001 | 0.75 | 40 | 4π | slower-decaying [site 1] (0.6949) | slower-decaying [site 1] (0.8059) | slower-decaying [site 1] (0.6949) | slower-decaying [site 1] (0.8059) | D6-like |
| 0.001 | 0.75 | 100 | 2π | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | D6-like |
| 0.001 | 0.75 | 100 | 4π | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | D6-like |
| 0.001 | 1.25 | 40 | 2π | lower-frequency [site 1] (0.9994) | lower-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | D7-like |
| 0.001 | 1.25 | 40 | 4π | lower-frequency [site 1] (0.9994) | lower-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | D7-like |
| 0.001 | 1.25 | 100 | 2π | lower-frequency [site 1] (0.9999) | lower-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | D7-like |
| 0.001 | 1.25 | 100 | 4π | lower-frequency [site 1] (0.9999) | lower-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | D7-like |
| 0.003 | 0.75 | 40 | 2π | slower-decaying [site 1] (0.8024) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.8024) | slower-decaying [site 1] (0.9998) | D6-like |
| 0.003 | 0.75 | 40 | 4π | slower-decaying [site 1] (0.6944) | slower-decaying [site 1] (0.8048) | slower-decaying [site 1] (0.6944) | slower-decaying [site 1] (0.8048) | D6-like |
| 0.003 | 0.75 | 100 | 2π | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | D6-like |
| 0.003 | 0.75 | 100 | 4π | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | D6-like |
| 0.003 | 1.25 | 40 | 2π | lower-frequency [site 1] (0.9994) | lower-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | D7-like |
| 0.003 | 1.25 | 40 | 4π | lower-frequency [site 2] (0.9994) | lower-frequency [site 2] (0.9994) | higher-frequency [site 2] (0.9994) | higher-frequency [site 2] (0.9994) | D7-like |
| 0.003 | 1.25 | 100 | 2π | lower-frequency [site 1] (0.9999) | lower-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | D7-like |
| 0.003 | 1.25 | 100 | 4π | lower-frequency [site 2] (0.9999) | lower-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | D7-like |
| 0.01 | 0.75 | 40 | 2π | slower-decaying [site 1] (0.8005) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (0.8005) | slower-decaying [site 1] (1.0000) | D6-like |
| 0.01 | 0.75 | 40 | 4π | slower-decaying [site 1] (0.6927) | slower-decaying [site 1] (0.8009) | slower-decaying [site 1] (0.6927) | slower-decaying [site 1] (0.8009) | D6-like |
| 0.01 | 0.75 | 100 | 2π | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | D6-like |
| 0.01 | 0.75 | 100 | 4π | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | D6-like |
| 0.01 | 1.25 | 40 | 2π | lower-frequency [site 1] (0.9994) | lower-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | D7-like |
| 0.01 | 1.25 | 40 | 4π | lower-frequency [site 1] (0.9994) | lower-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | higher-frequency [site 1] (0.9994) | D7-like |
| 0.01 | 1.25 | 100 | 2π | lower-frequency [site 1] (0.9999) | lower-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | D7-like |
| 0.01 | 1.25 | 100 | 4π | lower-frequency [site 1] (0.9999) | lower-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | D7-like |
| 0.03 | 0.75 | 40 | 2π | slower-decaying [site 1] (0.7948) | slower-decaying [site 1] (0.9990) | slower-decaying [site 1] (0.7948) | slower-decaying [site 1] (0.9990) | D6-like |
| 0.03 | 0.75 | 40 | 4π | slower-decaying [site 1] (0.6877) | slower-decaying [site 1] (0.7897) | slower-decaying [site 1] (0.6877) | slower-decaying [site 1] (0.7897) | D6-like |
| 0.03 | 0.75 | 100 | 2π | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | D6-like |
| 0.03 | 0.75 | 100 | 4π | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.9998) | D6-like |
| 0.03 | 1.25 | 40 | 2π | lower-frequency [site 2] (0.9993) | lower-frequency [site 2] (0.9993) | higher-frequency [site 2] (0.9993) | higher-frequency [site 2] (0.9993) | D7-like |
| 0.03 | 1.25 | 40 | 4π | lower-frequency [site 2] (0.9993) | lower-frequency [site 2] (0.9993) | higher-frequency [site 2] (0.9993) | higher-frequency [site 2] (0.9993) | D7-like |
| 0.03 | 1.25 | 100 | 2π | lower-frequency [site 2] (0.9999) | lower-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | D7-like |
| 0.03 | 1.25 | 100 | 4π | lower-frequency [site 2] (0.9999) | lower-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | D7-like |
| 0.1 | 0.75 | 40 | 2π | slower-decaying [site 1] (0.7901) | slower-decaying [site 1] (0.9964) | slower-decaying [site 1] (0.7901) | slower-decaying [site 1] (0.9964) | D6-like |
| 0.1 | 0.75 | 40 | 4π | slower-decaying [site 1] (0.6837) | slower-decaying [site 1] (0.7808) | slower-decaying [site 1] (0.6837) | slower-decaying [site 1] (0.7808) | D6-like |
| 0.1 | 0.75 | 100 | 2π | slower-decaying [site 1] (0.9995) | slower-decaying [site 1] (0.9995) | slower-decaying [site 1] (0.9994) | slower-decaying [site 1] (0.9996) | D6-like |
| 0.1 | 0.75 | 100 | 4π | slower-decaying [site 1] (0.9997) | slower-decaying [site 1] (0.9996) | slower-decaying [site 1] (0.9997) | slower-decaying [site 1] (0.9997) | D6-like |
| 0.1 | 1.25 | 40 | 2π | lower-frequency [site 2] (0.9992) | lower-frequency [site 2] (0.9992) | higher-frequency [site 2] (0.9992) | higher-frequency [site 2] (0.9992) | D7-like |
| 0.1 | 1.25 | 40 | 4π | lower-frequency [site 1] (0.9992) | lower-frequency [site 1] (0.9992) | higher-frequency [site 1] (0.9992) | higher-frequency [site 1] (0.9992) | D7-like |
| 0.1 | 1.25 | 100 | 2π | lower-frequency [site 2] (0.9999) | lower-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | D7-like |
| 0.1 | 1.25 | 100 | 4π | lower-frequency [site 1] (0.9999) | lower-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | D7-like |
| 0.2 | 0.75 | 40 | 2π | slower-decaying [site 1] (0.8114) | slower-decaying [site 1] (0.9946) | slower-decaying [site 1] (0.8114) | slower-decaying [site 1] (0.9946) | D6-like |
| 0.2 | 0.75 | 40 | 4π | slower-decaying [site 1] (0.7026) | slower-decaying [site 1] (0.8234) | slower-decaying [site 1] (0.7026) | slower-decaying [site 1] (0.8234) | D6-like |
| 0.2 | 0.75 | 100 | 2π | slower-decaying [site 1] (0.7864) | slower-decaying [site 1] (0.9993) | slower-decaying [site 1] (0.7873) | slower-decaying [site 1] (0.9993) | D6-like |
| 0.2 | 0.75 | 100 | 4π | slower-decaying [site 1] (0.6923) | slower-decaying [site 1] (0.7862) | slower-decaying [site 1] (0.6778) | slower-decaying [site 1] (0.7941) | D6-like |
| 0.2 | 1.25 | 40 | 2π | lower-frequency [site 2] (0.9990) | lower-frequency [site 2] (0.9990) | higher-frequency [site 2] (0.9990) | higher-frequency [site 2] (0.9990) | D7-like |
| 0.2 | 1.25 | 40 | 4π | lower-frequency [site 1] (0.9990) | lower-frequency [site 1] (0.9990) | higher-frequency [site 1] (0.9990) | higher-frequency [site 1] (0.9990) | D7-like |
| 0.2 | 1.25 | 100 | 2π | lower-frequency [site 2] (0.9999) | lower-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | higher-frequency [site 2] (0.9999) | D7-like |
| 0.2 | 1.25 | 100 | 4π | lower-frequency [site 1] (0.9999) | lower-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | higher-frequency [site 1] (0.9999) | D7-like |
| 0.3 | 0.75 | 40 | 2π | slower-decaying [site 1] (0.8182) | slower-decaying [site 1] (0.9854) | slower-decaying [site 1] (0.8182) | slower-decaying [site 1] (0.9854) | D6-like |
| 0.3 | 0.75 | 40 | 4π | slower-decaying [site 1] (0.7090) | slower-decaying [site 1] (0.8383) | slower-decaying [site 1] (0.7090) | slower-decaying [site 1] (0.8383) | D6-like |
| 0.3 | 0.75 | 100 | 2π | slower-decaying [site 1] (0.8105) | slower-decaying [site 1] (0.9954) | slower-decaying [site 1] (0.8105) | slower-decaying [site 1] (0.9954) | D6-like |
| 0.3 | 0.75 | 100 | 4π | slower-decaying [site 1] (0.7018) | slower-decaying [site 1] (0.8216) | slower-decaying [site 1] (0.7018) | slower-decaying [site 1] (0.8216) | D6-like |
| 0.3 | 1.25 | 40 | 2π | lower-frequency [site 2] (0.9985) | lower-frequency [site 2] (0.9985) | higher-frequency [site 2] (0.9985) | higher-frequency [site 2] (0.9985) | D7-like |
| 0.3 | 1.25 | 40 | 4π | lower-frequency [site 2] (0.9985) | lower-frequency [site 2] (0.9985) | higher-frequency [site 2] (0.9985) | higher-frequency [site 2] (0.9985) | D7-like |
| 0.3 | 1.25 | 100 | 2π | lower-frequency [site 2] (0.9978) | lower-frequency [site 2] (0.9978) | higher-frequency [site 2] (0.9978) | higher-frequency [site 2] (0.9978) | D7-like |
| 0.3 | 1.25 | 100 | 4π | lower-frequency [site 2] (0.9978) | lower-frequency [site 2] (0.9978) | higher-frequency [site 2] (0.9978) | higher-frequency [site 2] (0.9978) | D7-like |
| 0.35 | 0.75 | 40 | 2π | slower-decaying [site 1] (0.6373) | slower-decaying [site 1] (0.6874) | slower-decaying [site 1] (0.6373) | slower-decaying [site 1] (0.6874) | D6-like |
| 0.35 | 0.75 | 40 | 4π | slower-decaying [site 1] (0.5748) | slower-decaying [site 1] (0.5879) | slower-decaying [site 1] (0.5748) | slower-decaying [site 1] (0.5879) | D6-like |
| 0.35 | 0.75 | 100 | 2π | slower-decaying [site 1] (0.7048) | slower-decaying [site 1] (0.8286) | slower-decaying [site 1] (0.7048) | slower-decaying [site 1] (0.8286) | D6-like |
| 0.35 | 0.75 | 100 | 4π | slower-decaying [site 1] (0.6183) | slower-decaying [site 1] (0.6540) | slower-decaying [site 1] (0.6183) | slower-decaying [site 1] (0.6540) | D6-like |
| 0.35 | 1.25 | 40 | 2π | slower-decaying [site 1] (0.6681) | slower-decaying [site 1] (0.7475) | slower-decaying [site 1] (0.6681) | slower-decaying [site 1] (0.7475) | D6-like |
| 0.35 | 1.25 | 40 | 4π | slower-decaying [site 1] (0.5939) | slower-decaying [site 1] (0.6153) | slower-decaying [site 1] (0.5939) | slower-decaying [site 1] (0.6153) | D6-like |
| 0.35 | 1.25 | 100 | 2π | slower-decaying [site 1] (0.6790) | slower-decaying [site 1] (0.7706) | slower-decaying [site 1] (0.6790) | slower-decaying [site 1] (0.7706) | D6-like |
| 0.35 | 1.25 | 100 | 4π | slower-decaying [site 1] (0.6010) | slower-decaying [site 1] (0.6261) | slower-decaying [site 1] (0.6010) | slower-decaying [site 1] (0.6261) | D6-like |
| 0.350659 (=|v|/(2ε_EP)) | 0.75 | 40 | 2π | slower-decaying [site 1] (0.6330) | slower-decaying [site 1] (0.6795) | slower-decaying [site 1] (0.6330) | slower-decaying [site 1] (0.6795) | D6-like |
| 0.350659 (=|v|/(2ε_EP)) | 0.75 | 40 | 4π | slower-decaying [site 1] (0.5722) | slower-decaying [site 1] (0.5843) | slower-decaying [site 1] (0.5722) | slower-decaying [site 1] (0.5843) | D6-like |
| 0.350659 (=|v|/(2ε_EP)) | 0.75 | 100 | 2π | slower-decaying [site 1] (0.6966) | slower-decaying [site 1] (0.8097) | slower-decaying [site 1] (0.6966) | slower-decaying [site 1] (0.8097) | D6-like |
| 0.350659 (=|v|/(2ε_EP)) | 0.75 | 100 | 4π | slower-decaying [site 1] (0.6127) | slower-decaying [site 1] (0.6447) | slower-decaying [site 1] (0.6127) | slower-decaying [site 1] (0.6447) | D6-like |
| 0.350659 (=|v|/(2ε_EP)) | 1.25 | 40 | 2π | slower-decaying [site 1] (0.6735) | slower-decaying [site 1] (0.7588) | slower-decaying [site 1] (0.6735) | slower-decaying [site 1] (0.7588) | D6-like |
| 0.350659 (=|v|/(2ε_EP)) | 1.25 | 40 | 4π | slower-decaying [site 1] (0.5974) | slower-decaying [site 1] (0.6206) | slower-decaying [site 1] (0.5974) | slower-decaying [site 1] (0.6206) | D6-like |
| 0.350659 (=|v|/(2ε_EP)) | 1.25 | 100 | 2π | slower-decaying [site 1] (0.6893) | slower-decaying [site 1] (0.7932) | slower-decaying [site 1] (0.6893) | slower-decaying [site 1] (0.7932) | D6-like |
| 0.350659 (=|v|/(2ε_EP)) | 1.25 | 100 | 4π | slower-decaying [site 1] (0.6078) | slower-decaying [site 1] (0.6368) | slower-decaying [site 1] (0.6078) | slower-decaying [site 1] (0.6368) | D6-like |
| 0.4 | 0.75 | 40 | 2π | slower-decaying [site 1] (0.5041) | slower-decaying [site 1] (0.5041) | slower-decaying [site 1] (0.5041) | slower-decaying [site 1] (0.5041) | D6-like |
| 0.4 | 0.75 | 40 | 4π | slower-decaying [site 1] (0.5021) | slower-decaying [site 1] (0.5021) | slower-decaying [site 1] (0.5021) | slower-decaying [site 1] (0.5021) | D6-like |
| 0.4 | 0.75 | 100 | 2π | slower-decaying [site 1] (0.5000) | slower-decaying [site 1] (0.5000) | slower-decaying [site 1] (0.5000) | slower-decaying [site 1] (0.5000) | D6-like |
| 0.4 | 0.75 | 100 | 4π | slower-decaying [site 1] (0.5000) | slower-decaying [site 1] (0.5000) | slower-decaying [site 1] (0.5000) | slower-decaying [site 1] (0.5000) | D6-like |
| 0.4 | 1.25 | 40 | 2π | slower-decaying [site 1] (0.7951) | slower-decaying [site 1] (0.9991) | slower-decaying [site 1] (0.7951) | slower-decaying [site 1] (0.9991) | D6-like |
| 0.4 | 1.25 | 40 | 4π | slower-decaying [site 1] (0.6880) | slower-decaying [site 1] (0.7902) | slower-decaying [site 1] (0.6880) | slower-decaying [site 1] (0.7902) | D6-like |
| 0.4 | 1.25 | 100 | 2π | slower-decaying [site 1] (0.8006) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (0.8006) | slower-decaying [site 1] (1.0000) | D6-like |
| 0.4 | 1.25 | 100 | 4π | slower-decaying [site 1] (0.6929) | slower-decaying [site 1] (0.8012) | slower-decaying [site 1] (0.6929) | slower-decaying [site 1] (0.8012) | D6-like |
| 1 | 0.75 | 40 | 2π | lower-frequency [site 1] (0.9982) | lower-frequency [site 1] (0.9982) | higher-frequency [site 1] (0.9982) | higher-frequency [site 1] (0.9982) | D7-like |
| 1 | 0.75 | 40 | 4π | lower-frequency [site 1] (0.9982) | lower-frequency [site 1] (0.9982) | higher-frequency [site 1] (0.9982) | higher-frequency [site 1] (0.9982) | D7-like |
| 1 | 0.75 | 100 | 2π | lower-frequency [site 1] (0.9997) | lower-frequency [site 1] (0.9997) | higher-frequency [site 1] (0.9997) | higher-frequency [site 1] (0.9997) | D7-like |
| 1 | 0.75 | 100 | 4π | lower-frequency [site 1] (0.9997) | lower-frequency [site 1] (0.9997) | higher-frequency [site 1] (0.9997) | higher-frequency [site 1] (0.9997) | D7-like |
| 1 | 1.25 | 40 | 2π | slower-decaying [site 1] (0.7979) | slower-decaying [site 1] (0.9998) | slower-decaying [site 1] (0.7979) | slower-decaying [site 1] (0.9998) | D6-like |
| 1 | 1.25 | 40 | 4π | slower-decaying [site 1] (0.6904) | slower-decaying [site 1] (0.7957) | slower-decaying [site 1] (0.6904) | slower-decaying [site 1] (0.7957) | D6-like |
| 1 | 1.25 | 100 | 2π | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | D6-like |
| 1 | 1.25 | 100 | 4π | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | D6-like |
| 3 | 0.75 | 40 | 2π | faster-decaying [site 1] (0.5000) | faster-decaying [site 1] (0.5000) | slower-decaying [site 2] (0.5000) | slower-decaying [site 2] (0.5000) | NO |
| 3 | 0.75 | 40 | 4π | slower-decaying [site 2] (0.5000) | slower-decaying [site 2] (0.5000) | slower-decaying [site 2] (0.5000) | slower-decaying [site 2] (0.5000) | NO |
| 3 | 0.75 | 100 | 2π | faster-decaying [site 1] (0.5000) | slower-decaying [site 2] (0.5000) | slower-decaying [site 2] (0.5000) | slower-decaying [site 2] (0.5000) | NO |
| 3 | 0.75 | 100 | 4π | slower-decaying [site 2] (0.5000) | slower-decaying [site 2] (0.5000) | slower-decaying [site 2] (0.5000) | faster-decaying [site 1] (0.5000) | NO |
| 3 | 1.25 | 40 | 2π | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | D6-like |
| 3 | 1.25 | 40 | 4π | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | D6-like |
| 3 | 1.25 | 100 | 2π | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | D6-like |
| 3 | 1.25 | 100 | 4π | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | slower-decaying [site 1] (1.0000) | D6-like |

## Physics note

- The extra term keeps the PT-type symmetry (real coupling, imaginary diagonal): σ_x K maps the traceless part of H_try(ε) to itself for real ε (residual 5.6e-17), unlike the coupling term in pairA-qg-loss. H_try is also complex-symmetric (H^T = H, residual 0.0e+00) [identity + computed].
- So D6 direction-independence should survive. Check: on the eligible rows the 0.75 ε_EP class is D6-like on every row [computed].
- Inside Γ, F < 0 lowers the effective contrast κ + η_g F; outside, it raises it. The new EPs mark where κ + η_g F = ±|v|ε.
- **Mechanism:** Loss contrast keeps both D6 supports (transpose identity and PT) [identity]; it lowers the inside-Gamma contrast kappa + eta_g F, so selection slows and purity drops [computed]; D6 is inherited from H_A, not caused by the term. Largest clean drop: ΔP = -1.31e-02 (η_g = 0.1, γT = 40, 2π).

## Caveats

- H_real is H_A exactly, so any D6 at small η_g is H_A's own D6. The rule asks whether the new term changes winners or raises the purity above the floor on clean rows.
- Rows with E1 or E2 are listed but not used for the grade: there a new EP sits in or near the loop, or the start points have a different phase from H_A.
- At η_g* the merged EP has trivial monodromy, so the drive loop encloses no net branch point there.
- γ_g (secondary) is ½ max |Im Δλ| on the loop. The literal 'min imaginary split' is 0 wherever the split is real; at η_g = 0 this γ_g equals ½ the smallest |Δλ| on the loop.
- Tags: [by construction] H_real = H_A, the placement, γ; [identity] the rate-shift form, the discriminant and its factorisation, the EP locations and thresholds, copy NO for η_g > 0; [computed] roots, monodromy, copy residuals, weights, classes, floors; [hive-interpretation] 'gravity-side'.

No folders were loaded (nothing to SHA-check); only this folder was written.


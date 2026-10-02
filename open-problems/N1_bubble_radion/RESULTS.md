# Job N1: bubble versus radion

Generated: 2026-10-02 20:54:54 GMT Summer Time (BST/local time)
Tags: [computed] [identity] [standard] [assumed] [tuned] [post-hoc] [hive-interpretation].
Inputs read-only: UNIFYING_THREAD sha256 CDE3C256 (expected CDE3C256); STILL_TO_DO sha256 1AEC133B (expected 1AEC133B).
Radion source read-only: run.py sha256 586C6BC8; RESULTS.md sha256 6146CF25.

## Conventions [assumed]

Bubble static potential: U_b(r) = 4π p∞ r³/3 + 4πσ r² + gas work, with p∞ = -1 (liquid under tension), σ = 1, and gas normalisation G = 1.
For κ > 1 the gas term is +4πG r^[3(1−κ)]/[3(κ−1)]; at κ = 1 it is −4πG log(r/r₀), not a power [identity].
Radion potential: V(R) = 4πΛ₆/R − 4π/R² + (π/2)n²/R³ + C/R⁴, with n = 3, C = −3 and Λ₆ in [0.259398, 0.283357] [computed inherited input].
Allowed map tested exactly as fixed: R = c r^α with α ≠ 0 monotone and c > 0, plus a positive constant energy rescale; no r^β multiplier [assumed rule].

## Term powers and signs [computed]

Radion powers/signs: Λ₆/R (+), curvature/R² (−), flux/R³ (+), Casimir/R⁴ (−).

κ = 1.0 (isothermal) [standard]:
Best power candidate: α = -1.000000, matching 2/3 powers and 0/3 signs [computed].
| bubble term | r power | mapped R power | radion candidate | sign match |
|---|---:|---:|---|---|
| ambient pressure | 3.000000 | -3.000000 | flux | NO |
| surface tension | 2.000000 | -2.000000 | curvature | NO |
| gas | log | log | none | — |
The α = −1 pair sends ambient r³ → flux R⁻³ and surface r² → curvature R⁻²; both signs disagree. The κ=1.0 gas term remains logarithmic and has no radion candidate.

κ = 1.4 (adiabatic air) [standard]:
Best power candidate: α = -1.000000, matching 2/3 powers and 0/3 signs [computed].
| bubble term | r power | mapped R power | radion candidate | sign match |
|---|---:|---:|---|---|
| ambient pressure | 3.000000 | -3.000000 | flux | NO |
| surface tension | 2.000000 | -2.000000 | curvature | NO |
| gas | -1.200000 | 1.200000 | none | — |
The α = −1 pair sends ambient r³ → flux R⁻³ and surface r² → curvature R⁻²; both signs disagree. The κ=1.4 gas term maps to a positive power and has no radion candidate.

## Blake threshold versus radion fold [computed]

κ = 1.0: Blake fold radius r_B = 1.224744871; critical ambient pressure p∞,B = -1.088662108 (negative, tension) [computed].
κ = 1.4: Blake fold radius r_B = 1.260937410; critical ambient pressure p∞,B = -1.208473563 (negative, tension) [computed].
Radion C = -3.0, n = 3 stationary-point fold: R_fold = 2.877147747, Λ₆,fold = 0.327519186; supplied dS window is 0.259398–0.283357 [computed].
Threshold coincidence is not a valid PASS comparison: the complete allowed term/sign map already fails. A positive energy rescale cannot repair powers or signs [identity].

## Knobs and grade [computed]

Formal map knobs are α and κ, so two exponents could be fitted while one of the bubble's three terms remains as an overconstraint. The rule pins κ to 1 or 1.4; choosing κ by hand would be [tuned], leaving only α as a continuous knob.
Blake requires p∞ < 0. Under the only two-power candidate α = −1, the tension term lands on the positive flux sign at R⁻³, not on a negative radion term. The negative curvature and attractive Casimir terms have the needed sign, but their powers do not complete the map; Casimir is the radion collapse side [computed; prediction].
Spec ambiguity resolved [post-hoc]: the files state the allowed map and grade but do not print a bubble potential convention or map orientation. This run uses the standard integrated Rayleigh–Plesset static potential above and allows α < 0 because monotone was not restricted to increasing; restricting α > 0 only makes the power mismatch stronger.
Overall Job N1 grade: FAIL — physical κ choices have no complete power-and-sign map under R = c r^α and a positive energy rescale [computed].

## Read-only audit [computed]

UNIFYING_THREAD.md, STILL_TO_DO.md and Job 5b sources unchanged [computed].

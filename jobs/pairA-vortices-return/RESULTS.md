# pairA-vortices-return — RESULTS

Model: handoff `C:\Users\Akitt\pairA-qg-handoff` (seed.H_A, 2x2). eps_EP = 0.513680663312, lambda_EP = (-0-0.308425j).
lambda_EP evaluated at each core: +core -0.308425j, -core -0.308425j (identical: tr H_A/2 = -i(a+b)/2 does not depend on eps).
Gamma (real chart, handoff wick_lorentzian.chart): Γ=[-ε_EP, ε_EP] = [-0.513681, 0.513681]. C held (not used).

## Gamma check for the start point 1.25 eps_EP

eps_EP + r = 1.25 eps_EP = 0.642100829. Inside Gamma? **NO**

**WARNING — THE REQUESTED LOOP DOES NOT START ON THE REAL CHART.** In this handoff Gamma is the segment [-eps_EP, +eps_EP] between the two tips, so 1.25 eps_EP is on the real axis but OUTSIDE Gamma (it lies on the real sheets |eps|>eps_EP, where lambda-lambda_EP is real). The handoff's own Jhat loop (gauge_J.run_strip) uses this same start. To still test a real-chart start, T4 also runs loops starting at 0.75 eps_EP, -0.75 eps_EP and 0 (all inside Gamma).

Note: This NO comes straight from the formula and is not a failed return. For real ε inside Γ (|ε|<ε_EP), the square root √(ε²v²−(a−b)²/4) is imaginary, so λ−λ_EP is purely imaginary; outside Γ it is real. 'Re ε in Γ' and 'Im(λ−λ_EP)=0' can both hold only at the cores. The handoff's 1.25ε_EP start sits in the other (real-gap) phase.

## Circulation  Δarg(λ − λ_EP(core)), continuous tracking, r = 0.25 eps_EP

| core | 1 turn (0→2π) sheet0 / sheet1 | 2 turns (0→4π) sheet0 / sheet1 |
|---|---|---|
| +eps_EP | +1.000000π / +1.000000π | +2.000000π / +2.000000π |
| −eps_EP | +1.000000π / +1.000000π | +2.000000π / +2.000000π |

Half-turn circulation (π per turn, 2π per two turns) at both cores: **YES**. Tracking jump ratio (max step / local gap) 4.36e-04 (+core), 4.36e-04 (−core): no sheet jumps.

## Return tests (main loop eps = eps_EP + r e^{iθ}, θ 0→4π, 8001 points)

- **T1** labels back at 4π: **YES** (swap at 2π = True; back at 4π = True; handoff Jhat.npz ||Jhat4−I|| = 9.78e-16, ||Jhat2−I|| = 2.000, ||Jhat2²−I|| = 8.86e-16; recomputed ||Jhat4−I|| = 9.78e-16). Expected; already known.
- **T2** ε back on real axis at 4π: **YES** (ε(4π) = 0.642100829-6.3e-17i). **Passes by construction** — ε is moved by hand and returns to eps_EP + r at 2π and 4π. Says nothing about the vortices. Note: that point is on the real axis but NOT in Gamma.
- **T3** λ back to its start value at 4π: **YES** (max |λ(4π)−λ(0)| = 2.0e-16). **Passes by construction**: λ± − λ_EP ≈ ±c√(ε−ε_EP), so two turns return λ — same fact as the known 4π label return. Brief's stricter real-chart form (Re ε in Gamma and Im(λ−λ_EP)=0): **NO** — the start ε is outside Gamma. Also note: on Gamma's interior λ−λ_EP is purely IMAGINARY in this model (e.g. ε=0.5 eps_EP: 0.000000+0.160262j, 0.000000-0.160262j); Im(λ−λ_EP)=0 holds on the outer real sheets |ε|>eps_EP, not on Gamma.
  - T3 strict note: This NO comes straight from the formula and is not a failed return. For real ε inside Γ (|ε|<ε_EP), the square root √(ε²v²−(a−b)²/4) is imaginary, so λ−λ_EP is purely imaginary; outside Γ it is real. 'Re ε in Γ' and 'Im(λ−λ_EP)=0' can both hold only at the cores. The handoff's 1.25ε_EP start sits in the other (real-gap) phase.
- **T4** (the real test): **YES**

Branch cuts used for sheet labels (A := λ_EP + y/2, B := λ_EP − y/2, y² = 4v²(ε²−eps_EP²)):
1. Gamma-segment [−eps_EP, +eps_EP] (the handoff cut): y = 2v√(ε−eps_EP)√(ε+eps_EP); points on the cut read on the upper lip ε+i0.
2. Outward rays (−∞,−eps_EP] ∪ [+eps_EP,+∞): y = 2iv√(eps_EP−ε)√(eps_EP+ε).

T4 is branch-cut independent: whether labels swap is the monodromy of the continuously tracked path; the cut only sets where the label jump is drawn. The two-cut run is a bug check (both cuts must agree with the tracked swap).

| loop | tracked swap | cut 1 swap (flips) | cut 2 swap (flips) | λ back | ends at ε | on real axis | in Gamma |
|---|---|---|---|---|---|---|---|
| +core only (1 turn, start 1.25 eps_EP) | True | True (1) | True (1) | False | 0.642101-3.1e-17i | True | False |
| +core only (1 turn, start 0.75 eps_EP in Gamma) | True | True (1) | True (1) | False | 0.385260+4.7e-17i | True | True |
| -core only (1 turn, start -0.75 eps_EP in Gamma) | True | True (1) | True (1) | False | -0.385260-3.1e-17i | True | True |
| figure-eight (+core ccw, -core cw, start 0) | False | False (2) | False (2) | True | 0.000000+1.3e-16i | True | True |
| big loop around both (radius 2 eps_EP, start 2 eps_EP) | False | False (0) | False (2) | True | 1.027361-2.5e-16i | True | False |

Figure-eight per-lobe circulation (each lobe with its own core's λ_EP): lobe 1 (+core, anticlockwise) +1.000000π / +1.000000π; lobe 2 (−core, clockwise) -1.000000π / -1.000000π.
Cut-independence bug check passed for all loops: **YES**.

## Physics checks

- H_A is 2x2: only one eigenvalue pair exists, so the same two sheets (A, B) meet at both cores.
- Gap scaling |λ+ − λ−| (mean over circle) and eigenvector overlap |<v+|v−>|/(|v+||v−|):

| core | r/eps_EP | mean gap | mean overlap |
|---|---|---|---|
| +0.513681 | 0.25 | 2.619634e-01 | 0.777174 |
| +0.513681 | 0.1 | 1.655441e-01 | 0.904711 |
| +0.513681 | 0.03 | 9.065934e-02 | 0.970442 |
| +0.513681 | 0.01 | 5.234154e-02 | 0.990050 |
| -0.513681 | 0.25 | 2.619634e-01 | 0.777174 |
| -0.513681 | 0.1 | 1.655441e-01 | 0.904711 |
| -0.513681 | 0.03 | 9.065934e-02 | 0.970442 |
| -0.513681 | 0.01 | 5.234154e-02 | 0.990050 |

Core +0.513681: fitted gap exponent **0.5003** (EP ⇒ 1/2, ordinary crossing ⇒ 1); at the core gap = 6.8e-09, overlap = 1.000000 (→1: eigenvectors coalesce).

Core -0.513681: fitted gap exponent **0.5003** (EP ⇒ 1/2, ordinary crossing ⇒ 1); at the core gap = 6.8e-09, overlap = 1.000000 (→1: eigenvectors coalesce).

- Hermiticity on the real chart: ||H − H†|| = 1.017335 for every sampled real ε in Gamma (constant). Off-diagonal part of H − H† = 0.0e+00 (coupling εv is real-symmetric). Diagonal of H − H† = 0.00000-0.24674j, 0.00000-0.98696j: the non-Hermitian terms are the diagonal −i a, −i b (both loss/damping, unequal rates; no gain). H_A is NOT Hermitian for real ε.

## Verdict

**vortices return to real axis: YES**

Labels and λ return to their start values after ONE figure-eight pass (one 2π trip), whereas a one-core loop needs 4π. ε returning is by construction, since any closed loop ends where it started. Mechanism: once around one core swaps the two eigenvalues; the figure-eight's opposite-sense lobes (+π, −π) undo the swap.

Scope [careful-before-toy]: This is a statement about the eigenvalue sheets of H_A with ε moved by hand (quasi-static monodromy). It does not carry over to a state driven around the loop in time. That would mean solving i dψ/dt = H_A(ε(t))ψ, and with losses such a driven run typically ends on one mode that depends on which way you go around, not on the label swap (a known lossy-EP effect). "Vortex" here means arg(λ−λ_EP) winding by π per loop around a core [hive-interpretation], not a flow vortex. Physics picture (Helios): H_A + i(a+b)/2 = [[−iγ, εv],[εv, +iγ]] with γ=(a−b)/2. Both rates are losses, so the system is passive. Inside Γ the two modes share a frequency and decay at different rates; outside Γ they share a decay rate and have different frequencies.

Plot: outputs/tracks_vs_theta.png (Re/Im ε and Re/Im λ vs θ for the main loop).

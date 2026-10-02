# Job B0 spec: vortices on a round sphere (shared base run for B1–B4)

Status: FULL SPEC, draft for Venus. Not locked. Written 2026-10-02 about 22:00 BST from UNIFYING_THREAD.md (9F0867FE), "Next jobs", plus the Venus/Orion fixes of 21:49–21:53.

## Goal
Akitti's link [Akitti, L12, post 2105917997588365696, 8:09 AM Oct 2]: "once too many strings form on the outside of the bubble , mathematical divergences (infinities) and conceptual holes happen in 4 different topics of physics." B0 grades nothing about his idea by itself. It builds the one picture B1–B4 share [hive-interpretation]: strings ending on the bubble show up as n vortices on its skin, and "too many" is the Bradlow cap, the point where the vortices no longer fit.

## Model (normalisation locked by Venus/Orion)
- L = ½|Dφ|² + ¼F² + (e²/8)(|φ|² − v²)², D = ∂ − ieA. *In words: a charged "Higgs" field φ lives on the skin with a magnetic field, and the last term makes φ want to have size v.*
- Vortex (BPS) equations: (D₁ + iD₂)φ = 0 and B = (e/2)(v² − |φ|²). *In words: the magnetic field is strongest where the Higgs is weakest, which is inside each vortex core.*
- ∫B = 2πn/e. *In words: n strings carry n units of magnetic flux.*
- Integrating B gives A ≥ A_B = 4πn/(e²v²) [identity; Bradlow 1990; Manton–Nasir eq. (2.10) "4πN ≤ A"]. *In words: each vortex needs at least 4π of skin.*
- Units: e = v = 1, sphere radius R, A = 4πR², distance from the cap ε = A/A_B − 1.

## Setup: one ODE (the cheap case)
Put all n vortices at the north pole. Write log|φ|² = 2n·log sin(θ/2) + u(θ), with θ the angle from the pole. Then
u'' + cot θ·u' = n − R² + R²·sin^{2n}(θ/2)·e^u, with u'(0) = u'(π) = 0.
*In words: one smooth function along a line from pole to pole fixes the whole n-vortex.* [Plane version: Taubes 1980, standard. Sphere reduction derived by us by hand, so tag it to check, Venus.] Solve it with scipy `solve_bvp` or by shooting on u(0). Fluctuations split into angular sectors k (relative angular momentum k = m − n). This setup is enough for B0 and for 02's gap column.

Areas: ε = 0.01, 0.02, 0.05, 0.1 (near the cap), plus 1 and 4 (far). Take n = 1, 2, 3.

## What to compute
1. Profiles |φ|²(θ) and B(θ), plus max|φ|².
2. **Symmetric phase** (φ = 0, uniform B): the spectrum of −D². The LLL mass² is μ²(A) = eB − e²v²/2 = (e²v²/2)(A_B/A − 1), with eB = 2πn/A [computed, Venus]. *In words: this is the mass² of the n+1 lowest Higgs modes when the Higgs is switched off; a negative value means they want to grow.*
3. **Vortex branch:** the full (δφ, δA) fluctuation operator in background gauge, one sector k at a time, as a finite-difference matrix. Remove the gauge zero mode. Count the zero modes. In the vortex's own sector (k = 0), the lowest non-zero eigenvalue is the amplitude mode, gap² = m_gap².

## Controls (known results)
- **C1 [identity]:** ∫|φ|² = A − 4πn, and energy = πn for every A > A_B (relative error below 10⁻⁶).
- **C2 [standard: Wu–Yang monopole harmonics; Haldane 1983]:** −D² eigenvalues are [l(l+1) − (n/2)²]/R², l = n/2, n/2+1, …, each with 2l+1 states. So the LLL sits at eB with n+1 states.
- **C3 [standard: Manton–Sutcliffe ch. 7]:** n complex position zero modes (2n real) on the vortex branch, spread over sectors k = −n…−1. No others.

## Pre-registered near-cap checks
- **P1 (Venus's argument):** gap² / ((A − A_B)/A_B) → e²v² = 1 as A → A_B, run at at least 3 areas. *In words: the one massive mode that keeps the vortex gas honest gets soft in direct proportion to the distance from the cap.* Our independent hand check agrees [hive-interpretation, Venus to check]. Project φ onto the LLL, φ = c·ψ, and let B relax. That gives E(c) = ½μ²|c|² + |c|⁴/(8A) + const, with no arrangement dependence at this order. Its minimum, |c|² = A − A_B, matches C1. Its depth, (A − A_B)²/(8A), matches the exact energy gap between the symmetric phase and the vortex. Its curvature is 2|μ²|, so the ratio is A_B/A, which tends to 1.
- **P2 [computed by us from Baptista–Manton eq. (7) with all zeros at one pole; to check]:** max|φ|² / (1 − A_B/A) → n+1.
- **P3 [identity, print only]:** the symmetric phase lies above the vortex by ΔE = πnv²(A − A_B)²/(2A·A_B). 02 uses this.

## Pass rule (fixed before the run)
- **PASS:** C1–C3 hold, and a straight-line fit of the P1 ratio over the 3 smallest ε extrapolates to 1 within 3%.
- **PARTIAL:** the controls pass but P1 misses. Venus's argument has then missed a mixing term, and 02 must use the measured gap.
- **FAIL:** a control fails. Then the code is wrong, and nothing downstream runs.

**Prediction:** PASS. P2 holds too.

## Report only
- **Spread-out control:** k vortices at the north pole and n − k at the south (still one ODE, with sin^{2k}(θ/2)cos^{2(n−k)}(θ/2)). The leading gap ratio should match P1 [to check, Venus]. Baptista–Manton's main text doesn't settle this. It gives the moduli metric 2π(R² − N)·(Fubini–Study) (§4), not the gap.
- **Far from the cap:** the profile should approach the plane n-vortex (same code, plane ODE).

## Cost
Laptop Python (numpy/scipy). One BVP plus a few sparse eigenproblems on about 2000 points per area. Minutes in total.

## Refs
- Bradlow, Commun. Math. Phys. 135 (1990) 1 [standard; cited in MN ref. 2].
- Manton–Nasir, CMP 199 (1999) 591, hep-th/9807017, eqs. (2.8)–(2.10) [checked in PDF].
- Baptista–Manton, J. Math. Phys. 44 (2003) 3495, hep-th/0208001, eqs. (4)–(8) and §4 [checked in PDF; Orion verified the ref].
- García Lara–Speight, arXiv:2210.00966 [cited by Manton–Wang; not read].
- Taubes, CMP 72 (1980) 277 [cited in MN ref. 14; not read].
- Manton–Sutcliffe, *Topological Solitons*, CUP 2004, ch. 7 [standard; chapter number from Venus, not checked].
- Haldane, PRL 51 (1983) 605 [standard, from memory; to check].

# FUZZ_PLAN_V4_POSTSMOKE_PROPOSAL — POST-SMOKE CHANGE (proposal, unsigned; needs Helios + NanoRibbon)
Supersedes nothing until signed. V3 411C6529 and V2 239CDA17 are untouched.
Disclosure: smoke numbers (p≈−0.5) existed before this file. The justification below is mathematical only.

## Change B1 (test B exponent band)
Maths: near a pole of fuzzy S²_N, [X,Y]=iλZ ≈ iλR, i.e. a Moyal plane with θ_nc = Rλ. Minimal localisation length = √(Rλ) (coherent states, cell area 4πR²/N). So w/R ~ √(λ/R) ~ N^{−1/2}. The old band [−1.2,−0.8] encoded a width ~λ (Venus spec slip, D2/C-b).
New: model p* = −1/2. PASS p∈[−0.6,−0.4]; FAIL p outside [−0.75,−0.25] or local slopes steepening by >0.3; else UNDECIDED. (Same relative widths as V2: ±20% pass, ±50% fail.)
Caveat, which must be printed with any result: with the Berezin twisted-projector proxy (README A2) p=−1/2 is ANALYTIC, so B is a code check, not evidence. Evidence needs an independent curvature proxy (Helios to choose).
## Change B2 (D check)
Grade D_raw = ∫_cap P dA·N/(4πR²) against (1/12)(k−1/k) (the per-tip limit, derived analytically), with PASS ≤5% and FAIL >15% at N=128. It replaces "within 5% of δ".
## Change A1 (relabel)
Test A becomes a code pre-gate. The fuzzy spectrum is the truncated commutative one, so e(N)~1/N is guaranteed. It is not counted as a finding.
## Change L1
grade_La with no rungs → UNDECIDED. Rungs with N_j≤20 are reported as "no a_tip". V3 grid h and the floor λ≥3h are marked N/A for the matrix model.

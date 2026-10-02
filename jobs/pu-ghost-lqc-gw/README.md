# Job Seven: Pais–Uhlenbeck ghost and a gravitational-wave mode through the LQC bounce

Folder: `C:\Users\Akitt\pu-ghost-lqc-gw\` (TrinityOrb). Files: `run.py`, `RESULTS.md` (written only by
`run.py`), `pu_runaway.png` and `lqc_beta.png` (written by `run.py`), and this README. No git; Ledger pushes.

Run: `$env:PYTHONIOENCODING='utf-8'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py` (a few minutes).

**This README deliberately contains no computed numbers.** Every result, and the verdict for each part, is
printed from variables in `RESULTS.md`. The only numbers below are inputs, thresholds and literature values.

## Spec sources

- The NanoRibbon job text (Akitti's go).
- The pack `C:\Users\Akitt\open-problems\04_stelle_ghosts_lqc_bounce\README.md`, which was read. It has **no
  Helios spec**, so nothing was sharpened from it. It supplies the Stelle 1977/1978 and Agullo–Ashtekar–Nelson
  references. Orion's `X_NOTES.md` there was not opened.
- The fold-in requests from Venus (maths) and Helios (physics) after their PASS grades, relayed by NanoRibbon:
  G5, the λ-collapse [identity] tag, the Part L [standard] tag, and the scope lines below.
- **Conflict to report:** the spec says to exclude ω₁ = ω₂. But Smilga's benign-ghost example (NPB 706, eq. 6),
  L = ½(q̈ + Ω²q)² − (α/4)q⁴, *is* the equal-frequency PU oscillator. Resolution: the free split identity and the
  main ghost scan use unequal frequencies (ω₂/ω₁ = golden ratio). The equal-frequency case appears in two places
  only, both explicitly flagged: as the secular-growth demonstration (G2), and as the literature comparison with
  Smilga's own model (G4).

## What each toy is and isn't

- **Part G is** the one-variable fourth-order oscillator of Pais & Uhlenbeck. Ostrogradsky's Hamiltonian splits
  exactly into two oscillators with energies of opposite sign. It is the standard mechanical stand-in for the
  massive spin-2 ghost of Stelle's quadratic gravity: Stelle 1978's abstract states that "the massive spin-two
  part of the field has negative energy". **It is not** quadratic gravity. It has no gauge symmetry, no field
  modes or continuum, no coupling to matter, and none of Stelle's renormalisability structure.
- Which mode is the ghost depends on the overall sign of L. Flipping the sign leaves the equations of motion
  unchanged and only relabels which oscillator is "negative" [identity]. With the sign used here, the
  lower-frequency mode carries negative energy. Stelle's massive spin-2 corresponds to the opposite labelling,
  which has the same dynamics.
- **Part L is** a single tensor Fourier mode, v = a h, on the *effective* LQC background for a massless scalar
  (the Ashtekar–Pawlowski–Singh bounce, smooth at ρ = ρ_c). **It is not** a quantum-gravity calculation. There
  is no quantum backreaction and no dressed-metric quantum correction to a. The wave equation has the dressed-metric/hybrid form,
  but with the effective a in place of the dressed ã (Agullo–Ashtekar–Nelson go further);
  no inflation after the bounce, no scalar perturbations, and no modification of the tensor equation by
  holonomy corrections. Only the background is "LQC".
- **Scope, beyond the toy [standard: beyond toy]:**
  - (a) Two modes are not a field. Stelle's ghost can trade energy with infinitely many graviton modes. So the stable
    island here does not show that the real theory is stable, and it says nothing about quantum unitarity.
  - (b) Part L uses the dressed-metric/hybrid wave equation, χ'' + (k² − a''/a)χ = 0 (Agullo–Ashtekar–Nelson eq. 34,
    with their mean-field replacement ã → a). The pattern matches Agullo–Ashtekar–Nelson dressed-metric results. The
    deformed-algebra LQC approach instead changes the tensor wave speed near the bounce to c² = 1 − 2ρ/ρ_c, which goes
    negative there and could change |β_k|². That is not tested here. It is listed as a next idea in
    `open-problems\STILL_TO_DO.md`.

## Method summary

- **G1 [identity]:** sympy checks that Smilga's canonical map (SIGMA 2009, eq. 4) has the right Poisson brackets
  and turns H into E₁ − E₂ exactly. Numerically, E₁ and E₂ are conserved separately and the free motion stays
  bounded. H is shown to be unbounded below on an explicit family of states.
- **G2:** ω₁ = ω₂ is flagged and excluded. The free solution grows linearly (cos t + (t/2) sin t), checked
  against RK4, and the canonical map carries 1/√(ω₁²−ω₂²).
- **G3:** L → L − (λ/4)q⁴, which is Smilga's quartic (his positive α is our positive λ). It is integrated with
  vectorised RK4 (dt = 0.01), with an energy-drift check, a dt/2 check and a λ-scaling identity check. The
  λ-collapse is an [identity]: with q = Q/√λ every term of L scales by 1/λ, so the motion depends only on a√λ.
  - **[assumed input] sampling:** 200 starts per amplitude, directions uniform on the 3-sphere in the
    normalised state u = (q, q̇/ω̄, q̈/ω̄², q⃛/ω̄³), |u| = A·q_* with q_* = ω₁ω₂/√|λ|, and 13 amplitudes from
    0.02 to 3. The same directions are reused everywhere (seed 7).
  - **Runaway:** |u| ≥ 10 q_* before t_max = 300, also reported at t = 600 and with a 100 q_* threshold.
- **G4:** Smilga's own model and starting condition, q(0) = c, other derivatives zero, scanned in c.
- **G5 (review fold-in):**
  - **G5a** checks that the half-runaway amplitude scales like q_* ∝ 1/√λ at the λ values already scanned
    (0.1, 0.25, 1, 4, 10), with the same starts. Thresholds: A₅₀ spread ≤ 0.01, and the log-log slope of a₅₀
    against λ within 0.01 of −1/2.
  - **G5b** compares λ = ±1 at the same scaled amplitudes A√|λ| from 0.05 to 0.5, for the ghost and for a no-ghost
    control [assumed]. The control is the same Hamiltonian in Smilga's normal-mode variables with the sign of E₂
    flipped to +, the same quartic in the same q, the same starts, seed and runaway criterion, and both signs of λ.
    Only runaway beyond the matching control counts as ghost runaway.
  - **G5b sign rule** (fixed before the fold-in run): the sign of λ matters if |Δ(λ>0) − Δ(λ<0)| ≥ 0.25 at any
    scaled amplitude ≤ 0.5 by t = 300, where Δ = f_ghost − f_control.
  - **G5b checks:** the λ > 0 control must never run away (its H is bounded below), and the ghost in normal-mode
    variables must match the q-variable runs within 0.03.
- **L:** units 8πG = ρ_c = a_B = 1, so k_B = 1.
  - a''/a = (1 − t²)(1 + 3t²)^(−5/3) is derived with sympy and checked by finite differences in η, with
    η(t) = t·₂F₁(1/6, 1/2; 3/2; −3t²) checked against quadrature.
  - Each mode starts in the first-order adiabatic vacuum at η = −X/k and is integrated in t (DOP853, rtol
    1e-12) to η = +X/k, then projected onto the late-time adiabatic modes. X = 200 is the main run and X = 400
    is the convergence column.
  - 21 values of k/k_B are used, log-spaced from 0.1 to 10.
- **All G1–G4 and L1–L4 PASS thresholds were fixed in run.py's parameter block before the first run and are
  unchanged.** The G5 thresholds and the sign rule were added in the fold-in pass and fixed before the fold-in run.
  That fold-in run is the one reported in RESULTS.md, and nothing was tuned afterwards.

## Literature checks (comparison numbers are printed in RESULTS.md)

- **Smilga, NPB 706 (2005) 598, §2** (read via arXiv hep-th/0407231). For eq. (6) he states that the eq. (7)
  "admits benign regular orbits in the vicinity of the stationary point" and that "Only fluctuations of large
  enough amplitude go astray". For q(0) = c he finds "the threshold amplitude is c_crit ≈ 0.3 Ω²/√α". He also
  says "the positive sign of α is crucial for such a restricted stability", and that for the opposite sign "the
  vacuum is always unstable with respect to small fluctuations". G4 tests the threshold directly. The λ = −1
  report lines test the sign statement in both the equal-frequency and the unequal-frequency cases. G5b extends
  this with a no-ghost control, because for λ < 0 the quartic is unbounded below even without a ghost. A copy of
  the paper is now in the pack (`NPB706_598_Smilga_benign_vs_malicious_ghosts.pdf`).
- **Smilga, SIGMA 5 (2009) 017, §4** (arXiv:0808.0139). For generic interactions "there is an island of stability
  around the perturbative vacuum … Generically, however, the trajectories go astray reaching infinity in finite
  time". G3 is the unequal-frequency version of exactly this statement.
- **Stelle 1978** (GRG 9, 353; the PDF has a text layer): the abstract quote above is the link to the ghost.
  **Stelle 1977** (PRD 16, 953) is a scan with no text layer. It is cited as the renormalisability reference
  only and was not quoted.
- **Agullo–Ashtekar–Nelson 2013:** the introduction says they "study the dynamics of quantum fields representing
  scalar and tensor perturbations on quantum cosmological space-times". This is the pack's LQC
  tensor-perturbation reference. Our Part L is the much cruder effective-background version.
- **Dykhne 1962; Davis & Pechukas 1976** [standard]. For an analytic time dependence in the adiabatic limit, the
  transition amplitude is "localized to the vicinity of a complex crossing", "independent of the nonadiabatic
  coupling and given by a simple formula of A. M. Dykhne" (Davis & Pechukas, abstract). For the mode equation this
  gives |β_k|² ~ exp(−4k·Im η_s), with η_s the nearest complex singularity of a''/a. Venus's closed form is
  Im η_s = (1/√3)(√π/2)Γ(5/6)/Γ(4/3). RESULTS.md prints it, computed with math.gamma, next to the fitted rate.
  Dykhne's paper itself was not read; it is cited as Davis & Pechukas cite it.

## Caveats

- The runaway criterion, the horizons t = 300/600, the amplitude grid and the sphere sampling are all
  [assumed input]. A slow escape beyond t = 600 would be missed. The t ≤ 600 column and the 100 q_* column
  are the sensitivity checks [finite-size].
- "Stable island" here means no escape within t ≤ 600 for the sampled starts. It is numerical evidence, not a
  KAM/Nekhoroshev proof. Low-order resonances (1:2, 1:3) are known to be dangerous for opposite-signature
  oscillators. They are avoided by the golden-ratio choice but not studied [hive-interpretation].
- The quartic interaction is Smilga's simplest choice. Other couplings (his q²q̇² term, or his special benign
  normal-mode potentials of 2009) can behave differently. Quantum behaviour (collapse, unitarity) is not addressed.
- Part L: the "adiabatic vacuum" is first-order WKB. Its residual non-adiabaticity at |kη| = X sets a floor on
  how small a |β|² can be trusted, which is why the convergence test uses only |β|² above 1e-10.
- The large-k fall-off exp(−4k·Im η_s) is tagged [standard] (Dykhne; Davis & Pechukas). It is printed as a check
  next to the fitted rate and is not graded. The fits use only k ≥ 3 k_B.
- The G5b no-ghost control is one choice [assumed]. Because q = (ω₁X₂ − P₁)/(ω₁√(ω₁²−ω₂²)) contains P₁, the
  canonical rotation (X₁, P₁) → (−P₁/ω₁, ω₁X₁), which keeps E₁, turns the control into two ordinary oscillators
  coupled by a quartic in a sum of their positions [identity]. A different control coupling could give different
  numbers. [hive-interpretation] With the control subtracted, much of the λ < 0 runaway at the larger scaled
  amplitudes also happens without the ghost; see the G5b table.
- The background is classical-effective. Near ρ_c the effective equations are an approximation to the quantum
  dynamics (APS show that sharply peaked states follow them).

## Tag key

[computed] produced by `run.py`; [identity] exact algebraic statement checked symbolically or to round-off;
[assumed] modelling choice; [assumed input] parameter set by hand; [standard] textbook/literature result;
[post-hoc] changed or added after seeing a result (here only the G5 fold-ins, requested in review, with their
thresholds fixed before the fold-in run); [finite-size] artefact of finite horizons or start
times; [grid-step] step-size effect; [prediction] expectation stated before the run; [hive-interpretation] our
reading, not a theorem; [standard: beyond toy] a standard statement about the real theory that the toy does not test.

## References

- A. Pais and G. E. Uhlenbeck, "On field theories with non-localized action", Phys. Rev. 79 (1950) 145.
- M. Ostrogradsky, Mem. Acad. St. Petersbourg VI 4 (1850) 385.
- A. V. Smilga, "Benign vs. malicious ghosts in higher-derivative theories", Nucl. Phys. B 706 (2005) 598,
  arXiv:hep-th/0407231.
- A. V. Smilga, "Comments on the dynamics of the Pais–Uhlenbeck oscillator", SIGMA 5 (2009) 017,
  arXiv:0808.0139 (source of the canonical map used in G1).
- K. S. Stelle, "Renormalization of higher-derivative quantum gravity", Phys. Rev. D 16 (1977) 953.
- K. S. Stelle, "Classical gravity with higher derivatives", Gen. Rel. Grav. 9 (1978) 353.
- A. Ashtekar, T. Pawlowski and P. Singh, "Quantum nature of the big bang", Phys. Rev. Lett. 96 (2006) 141301;
  "Quantum nature of the big bang: improved dynamics", Phys. Rev. D 74 (2006) 084003, arXiv:gr-qc/0607039.
- A. Ashtekar and P. Singh, "Loop quantum cosmology: a status report", arXiv:1108.0893 (pack; effective Friedmann equation).
- I. Agullo, A. Ashtekar and W. Nelson, "An extension of the quantum theory of cosmological perturbations to the
  Planck era", Phys. Rev. D 87 (2013) 043507, arXiv:1211.1354 (pack; LQC tensor perturbations).
- A. M. Dykhne, Sov. Phys. JETP 14 (1962) 941.
- J. P. Davis and P. Pechukas, "Nonadiabatic transitions induced by a time-dependent Hamiltonian in the
  semiclassical/adiabatic limit: The two-state case", J. Chem. Phys. 64 (1976) 3129, doi:10.1063/1.432648.

## Post-run / sign-off

- Post-run (2 Oct 2026): the first run of run.py used thresholds fixed beforehand, with no [post-hoc] changes. Pre-run fixes, made before any physics output existed: a brentq tolerance bug, printing parameters
  from variables instead of typed labels, and defining the island as the contiguous run of zero-runaway amplitudes from
  the smallest one.
- Fold-in pass (2 Oct 2026, after the Venus and Helios PASS grades): the folder was backed up to %TEMP%, only run.py
  was edited, and it was re-run once. Added: G5a, G5b, the λ-collapse [identity] tag, the Part L fall-off tag upgrade
  from [hive-interpretation] to [standard] with Venus's closed form, and the scope lines above.
  - Every earlier computed number in RESULTS.md reproduced unchanged, and no earlier threshold changed.
  - [post-hoc]: the G5 checks were added after the review, with their thresholds and the sign rule fixed before the
    fold-in run. No re-grade was requested.
- Venus (maths): PASS (maths), graded 19:21 BST.
- Helios (physics): PASS (physics, as a toy), graded 19:28 BST.
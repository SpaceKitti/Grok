# Job 6b: does the supersymmetric x²y² toy H = Q² have a zero-energy bound state?

Folder: `C:\Users\Akitt\membrane-6b-boundstate\` (TrinityOrb). Files: `run.py`, `RESULTS.md` (written only by `run.py`,
never hand-edited), and this README. No git; Ledger pushes.

Run: `$env:PYTHONIOENCODING='utf-8'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py` (a few minutes; sparse
shift-invert `eigsh`).

This README was written before the first run and contains no computed numbers. The only numbers below are inputs,
rules and literature values. Every result is printed from variables in `RESULTS.md`.

## Spec sources

- Helios's Job 6b spec, relayed by NanoRibbon (Akitti's go).
- Builds on Job Six, `C:\Users\Akitt\membrane-x2y2\` (main 05e6347). That folder is neither imported nor modified here.
  The model is Job Six's s = 1 point, H₁ = p² + x²y² + xσ₃ + yσ₁ [assumed input].
  Job Six's findings used as background [standard: earlier hive result]:
  - the valley wall (1 − s)|x| vanishes at s = 1;
  - the s = 1 levels fall like 1/L² on a k² ladder.
- Literature: Fröhlich, Graf, Hasler, Hoppe and Yau (FGHHY), Nucl. Phys. B 567 (2000) 231, hep-th/9904182. The PDF is
  Orion's copy in `C:\Users\Akitt\open-problems\03_membrane_renormalization\` and was read before writing run.py
  (Theorem, Remarks, Section 4.6, Appendix 2).

## Model and conventions

- H = Q², with Q = −σ₃p_x + σ₁p_y + σ₂xy and p = −i∂.
  - `run.py` checks Q² = H₁ symbolically [identity].
  - It also checks that Q is FGHHY's Appendix-2 supercharge conjugated by y → −y, so the two models are unitarily
    equivalent [identity].
- Spec notation: f ~ |x|^(−γ). In FGHHY's notation, Ψ = x^(−κ)(Ψ₀ + …), so γ = κ.

## Stages

**Stage A (sympy) [identity / computed, leading order]:**
- n = 0: solve Q₀Ψ₀ = 0 in the valley (large x, small y). This gives the transverse Gaussian and selects the fermion
  state, and checks that the oscillator zero point cancels against the fermion term.
- n = 1: the solvability condition fixes κ. This is cross-checked by an independent ansatz with a first correction,
  and the residual order is computed.
- Normalisability with the transverse width included: ∫|Ψ|²dy ∝ x^p, so the zero mode is normalisable along the
  valley iff p < −1. run.py prints the result.
- "Leading order" means the n = 0 kernel plus the n = 1 condition of the formal series in x^(−3/2).

**Stage B (numerics):**
- **B.0 identities:**
  - Q_h is hermitian and has an exact ± spectrum.
  - The parity P = σ₁⊗(x → −x) reduction is checked.
  - A real antisymmetric matrix of odd size has a forced zero eigenvalue. This lattice artefact is shown on Job Six's
    odd vertex grid, so the scans use cell-centred grids of even size.
- **B.1:** the transverse lattice "mass" δ(x) left over by the discretised zero-point cancellation [grid-step].
- **B.2 (primary):** Q discretised directly with Job Six's 4th-order stencil family. This is the 4th-order central
  first derivative.
  - Settings: h = 0.08 on the box [−L, L]², for L = 8, 10, 12, 14, 16.
  - Output: singular values σ = √E from shift-invert `eigsh`, exponents fitted against L, a ladder comparison, and
    per-level diagnostics (doubler content, wall weight, central weight). The doubler content tracks fermion
    doubling, which a first-order lattice operator has.
  - A grid check at L = 8 with h = 0.064.
- **B.3 (cross-check, report):** Job Six's own discretisation of H = Q², a 4th-order Laplacian with Dirichlet walls.
  The same criterion is applied.

**Stage C:** FGHHY comparison, with page and equation references printed by run.py.

## Rules (fixed in run.py before the first run)

- **Ladder established:** the median over the lowest 4 levels of σ_k(16)/σ_k(8) lies in [0.40, 0.625]. That is a drop
  by 1.6–2.5×; a 1/L ladder gives 0.5.
- **Bound-state candidate:** the ladder is established, and either:
  - some level among the lowest 6 has |σ_k(16)/σ_k(8) − 1| < 10% (the spec's example), or
  - σ₁/σ₂ < 0.2 at every L (an off-ladder level near zero).
- **Verdict:**
  - 'Bound state found' needs Stage A normalisable AND a Stage B candidate.
  - 'No bound state' [standard: beyond toy] needs all of: Stage A non-normalisable; no candidate on an established
    ladder; the direct Q_h and the Job Six discretisations agreeing; Stage A agreeing with FGHHY (same κ and same
    normalisability); and the B.0 identities passing.
  - Anything else is 'inconclusive', and the failing conditions are named.

## Caveats

- A finite box always has a discrete spectrum. The continuum is inferred from the 1/L scaling.
- An eigenvalue embedded in the continuum (E > 0) with no avoided crossing, or a zero mode not of the power-series
  form, is not excluded by this job. The question addressed is the threshold E = 0.
- The direct Q_h has fermion doublers (D also vanishes at k = π/h, group speed 5/3). Each doubler copy is again a
  supersymmetric x²y² model, so its levels also fall like 1/L. Hard walls mix the components, so the Q_h box ladder
  interleaves several 1/L ladders. The Job Six cross-check has no doublers but carries a negative h⁴|x|³ grid bias that
  grows with L [grid-step].
- FGHHY's Appendix 2 is formal: no L² solution of the asymptotic form exists. Their main theorem concerns the SU(2)
  matrix models (d = 2, 3, 5, 9), not this toy.

## Tag key

[identity] exact statement checked symbolically or to machine precision; [computed] produced by run.py; [assumed input]
set by hand; [standard] literature result; [standard: beyond toy] literature result about models beyond this toy, or a
conclusion backed by them; [grid-step] discretisation effect; [finite-size] box artefact; [hive-interpretation] our
reading; [post-hoc] changed after seeing a result; [prediction] stated before the run; [lattice artefact: doubler index]
the forced zero eigenvalue of an odd-size real antisymmetric lattice operator (added in the second pass).

## References

- J. Fröhlich, G. M. Graf, D. Hasler, J. Hoppe and S.-T. Yau, "Asymptotic form of zero energy wave functions in
  supersymmetric matrix models", Nucl. Phys. B 567 (2000) 231, arXiv:hep-th/9904182 (PDF read: Theorem, Remarks 1–2,
  §4.6, Appendix 2).
- B. de Wit, M. Lüscher and H. Nicolai, "The supermembrane is unstable", Nucl. Phys. B 320 (1989) 135 (spectrum
  [0, ∞); via Job Six).
- B. Simon, Ann. Phys. 146 (1983) 209 (bosonic x²y², discrete spectrum; via Job Six).
- S. Sethi and M. Stern, Commun. Math. Phys. 194 (1998) 675, hep-th/9705046; P. Yi, Nucl. Phys. B 505 (1997) 307,
  hep-th/9704098 (the d = 9 SU(2) threshold bound state; Witten index 1, 0, 0 at d = 9, 5, 3) [standard: beyond toy].
- V. G. Kac and A. V. Smilga, "Normalized vacuum states in N = 4 supersymmetric Yang–Mills quantum mechanics with any
  gauge group", hep-th/9908096 (second source for the d = 9 index) [standard: beyond toy].
- G. Moore, N. Nekrasov and S. Shatashvili, "D-particle bound states and generalized instantons", hep-th/9803265
  (allowed dimensions d = 2, 3, 5, 9 only) [standard: beyond toy].
- Job 6c: `C:\Users\Akitt\membrane-6c-kappa-d\` (κ(d) for the SU(2) models).
- Job Six: `C:\Users\Akitt\membrane-x2y2\` (main 05e6347).

## Post-run

run.py was run once (the RESULTS.md header gives the time). Code and rules were not changed after the run. All numbers
are in `RESULTS.md`; this section adds none of its own.

- **Stage A:** every identity passes, and κ = γ = −1/4 is found by two independent routes. The asymptotic zero mode is
  not normalisable, because the transverse-integrated density is constant along the valley. This matches FGHHY
  Appendix 2 exactly.
- **Stage B:** both discretisations show a clean 1/L fall, with no non-falling and no near-zero off-ladder level.
  - The B.0 identities and the ± pairing pass.
  - Stage B candidate: none in either discretisation.
- **Verdict:** No bound state [standard: beyond toy], by the pre-fixed rule.
- **[post-hoc] B.1 expectation wrong:**
  - The README and the run.py text expected a small grid mass δ(x) scaling like h⁴. In fact δ sits at roundoff level:
    the lattice transverse operator keeps an exact zero mode, up to exponentially small box leakage.
  - So the "ratio" column of the B.1 table carries no information. The grid does not spoil the zero-point
    cancellation for Q_h.
- **[post-hoc, hive-interpretation] Q_h ladder shape:**
  - The direct Q_h ladder runs over odd integers (σ_k/σ₁ = 1, 3, 5, …; E ratios (2m − 1)², i.e. half-integer k), and
    every level carries the same doubler fraction.
  - This is read as a single standing wave that mixes the physical and doubler components through wall reflections.
    Its effective length is about (1 + 3/5)·2L, with the doubler group speed 5/3. That explains why ℓ_k = kπ/σ_k does
    not equal 2L for Q_h.
  - Job Six's H discretisation gives the plain k² ladder, with ℓ close to 2L. Both scale as 1/L, which is what the
    criterion tests.
- **Grid:** the grid check at L = 8 shows a uniform small shift of all levels, consistent with an O(h) shift of the
  effective wall position [grid-step].
- **Scope (as stated before the run):** E > 0 embedded eigenvalues and zero modes outside the asymptotic power-series
  form are not excluded.
- **Wall [standard: beyond toy] [post-hoc, added after Job 6c]:** the 2-variable toy is exhausted; a bound state
  appears only in the d = 9 SU(2) model. Witten index 1 (d = 9), 0 (d = 5), 0 (d = 3) [Yi hep-th/9704098; d = 9 also
  Kac–Smilga hep-th/9908096]; allowed dimensions d = 2, 3, 5, 9 [Moore–Nekrasov–Shatashvili hep-th/9803265]. Yi's
  index values rest on a defect term he motivates but does not derive; Kac–Smilga compute it. See Job 6c.
- **Second pass [post-hoc]:** run.py was rerun once to add two printouts. Parameters, seeds and verdict rules did not
  change. RESULTS.md was regenerated by run.py, never hand-edited. A backup of the folder before the pass is in
  `%TEMP%\membrane-6b-backup-20261002-2051\`.
  - (a) Stage A now prints the next-to-leading-order balance term by term. This is the lower component at order
    x^(−κ−1), where the longitudinal p_x term enters as a 1/x correction, so γ = κ can be checked from the page.
  - (b) Stage B.0 tags the odd-grid zero as [lattice artefact: doubler index].
  - A diff against the backup shows every other line unchanged except the timestamp and runtime.
  - The first attempt stopped at a new assert in Stage A (a variable used before assignment) before RESULTS was written.
    It was fixed by comparing with the solver output directly. The second attempt was interrupted externally, also
    before RESULTS was written. The third attempt completed.
- **Process note:** a typo in the editing script emptied this README while the Post-run section was being added. The
  file was rewritten from the same pre-run text, with only this Post-run section added. RESULTS.md and run.py were
  not touched.

## Sign-off

- Venus (maths): PASS
- Helios (physics): PASS as a toy
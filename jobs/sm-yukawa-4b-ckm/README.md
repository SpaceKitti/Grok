# Job 4b: CKM mixing from an aligned soft brane plus a narrow tilted brane (round sphere, α = 1)

Folder: `C:\Users\Akitt\sm-yukawa-4b-ckm\` (TrinityOrb). Files: `run.py`, `RESULTS.md` (written only by `run.py`,
never hand-edited), and this README. No git; Ledger pushes.

Run: `$env:PYTHONIOENCODING='utf-8'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py` (seconds).

This README was written before the first run and contains no computed numbers. The only numbers below are
inputs, thresholds and spec expectations. Every result is printed from variables in `RESULTS.md`.

## Spec sources

- Helios's Job 4b spec, plus Venus's milling (19:30) and Helios's notes (19:35), relayed by NanoRibbon (Akitti's go).
- Builds on Job Four, `C:\Users\Akitt\sm-rugby-yukawa\` (on main at 3b2e06a). That folder is neither imported nor
  modified here. Its facts are used as [standard] inputs:
  - the three zero modes form a j = 1 triplet, with Bernstein densities 3·C(2,k)·u^k(1−u)^(2−k);
  - a soft brane h = exp(−u/σ) gives Y_k/Y_0 = 1 : 2σ : 2σ² at leading order;
  - a tilted brane gives |V| = |d¹(β)|.
- Targets: Orion's `C:\Users\Akitt\open-problems\JOB4B_TARGETS.md`, primary set. run.py parses it, so no target is
  typed into the code. CKM magnitudes come from the PDG 2026 global fit; mass ratios from Huang–Zhou 2021,
  Table 2, at μ = M_Z.
- **Conflict to report:** the spec's reference list says "PDG 2022", but Orion's target file uses the PDG 2026
  global fit. The 2026 values are used and cited.
- **Not seen:** Venus's 19:30 milling text itself. The "lopsided brane" of A2 is therefore defined here [assumed
  input]: a soft brane at the north tip with a dipole distortion, h = exp(−u/σ)(1 + ε cos φ).

## Conventions

- Round sphere only (α = 1). The zero modes are η_k = √(3·C(2,k)/4π)·a^(2−k)·b^k, where (a, b) is the point's
  spinor, with |a| = cos(θ/2) and |b| = sin(θ/2) [standard; lowest Landau level].
- k = 0 peaks at the north tip and is the heaviest (third) generation. In mass order, index 1 = heaviest and
  index 3 = lightest. The CKM is V = U_uᵀ U_d from the two SVDs, with up rows (t, c, u) and down columns (b, s, d),
  so |V_us| = |V[u, s]|, |V_cb| = |V[c, b]| and |V_ub| = |V[u, b]|.
- A brane centred at polar angle β gives Y = D(β)·diag(t₀, t₁, t₂)·D(β)ᵀ. Here t_k = ∫ h·b_k du are the
  brane-frame integrals, and D(β) is the j = 1 rotation in this basis. Its heavy column is
  v = (cos²(β/2), sin β/√2, sin²(β/2)) [identity; checked numerically in A1].
- Up sector: a soft brane of width σ_u at the north tip, Y_u = diag(a(σ_u))/a₀.
- Down sector: Y_d = diag(a(σ_d))/a₀ + ε·D·diag(t(σ_t))/t₀·Dᵀ. The tilted brane couples through a second Higgs
  [assumed input], so ε is an independent strength.
  - Rank-1 reference form: Y_d = diag(1, 2σ_d, 2σ_d²) + ε·v vᵀ.
  - The full finite-σ_t version keeps the second tilted mode, t₁/t₀ ≈ 2σ_t.
  - "Exact" means the exact soft integrals (incomplete gamma functions) followed by an exact 3×3 SVD.
- Everything is real, so the Jarlskog invariant is J = 0: **there is no CP violation in this real model.**

## Stages (what run.py prints)

1. **A1 [identity]:** two different widths alone (an up brane at the tip, a down brane tilted by β) still give
   |V| = |d¹(β)|. This is checked by direct 2D quadrature of the zero modes in brane-centred coordinates, for soft
   and top-hat profiles. The same quadrature checks Y = D·diag(t)·Dᵀ.
2. **A2:** the lopsided brane above gives θ₁₂ and θ₂₃ ∝ ε√σ. At leading order [identity]:
   - θ₂₃ = ε·√(2πσ)/4
   - θ₁₂ = 3ε·√(2πσ)/16
   So θ₁₂/θ₂₃ → 3/4 (same order, not equal). Both the scaling exponents and the leading-order forms are checked.
3. **Formula comparison at the check point** σ_d = 0.00935, ε = 0.06, β = 0.64, on the rank-1 reference form:
   - Venus's corrected forms: θ₂₃ = ε·cos²(β/2)·sin β/√2, θ₁₃ = ε·cos²(β/2)·sin²(β/2), and
     θ₁₂ = ε·v_s·v_d/((m_s − m_d)/m_b), with the physical gap taken from the exact SVD.
   - Helios's original forms: no cos² factor, and a gap of 2σ_d.
   - Spec expectations [prediction]: Helios's θ₁₂ ≈ 0.134, the exact value ≈ 0.084, and the physical-gap form
     within a few percent.
4. **Masses:**
   - Down: the soft-law estimate m_d/m_s ≈ σ_d ≈ ½·m_s/m_b from the targets. Venus expects about 0.009 against
     0.050, lifted to about 0.018 by the ε shift [prediction].
   - Up: the analogue m_u/m_c ≈ ½·m_c/m_t.
5. **Relation 3, Venus's parameter-free relation** [identity at first order in ε, rank-1 limit]:
   - θ₁₃/θ₂₃ = tan(β/2)/√2
   - θ₁₂/θ₂₃ ≈ tan²(β/2)·m_b/m_s
   - Together: V_us ≈ 2V_ub²/(V_cb·m_s/m_b).
   It is printed from the targets as a [prediction] before any fit; Venus expects about 0.036 against 0.225. It is
   then checked against the exact SVD at several points (Venus: within about 7%).
6. **σ_t row:** σ_t ∈ {0.001, 0.01, 0.03} at fixed σ_d = 0.00935 and ε = 0.06, at β = 0.28 and β = 0.64. The second
   tilted mode adds ε·t₁·sin β·cos β/√2 to Y_sd, which competes with ε·v_s·v_d once σ_t ≳ β²/8. Venus expects
   σ_t = 0.01 to roughly double V_us at β ≈ 0.25–0.3 [prediction].
7. **Fits:** log least-squares (unweighted residuals ln(prediction/target)) against the seven targets, with
   multi-start, run twice:
   - Fit 1: σ_t fixed at 0.01; 4 knobs (σ_u, σ_d, ε, β) [tuned].
   - Fit 2: σ_t free, openly the fifth knob [tuned] (Helios).
   - The knob count against the 7 targets is printed for each. The leading-order forms and relation 3 are compared
     with the exact SVD at each best fit.
8. **Top-hat robustness row:** the top-hat profile h = 1 for u < σ (law 1 : σ : σ²/3). It is used both to
   re-evaluate the soft best-fit knobs and to refit both versions. It is a report and is not graded.

## PASS thresholds (fixed in run.py before the first run)

- A1: max ‖|V| − |d¹(β)|‖ < 1e-10; Y = D·diag(t)·Dᵀ to a relative 1e-10.
- A2: fitted exponents within 0.02 of 1/2 (in σ) and 1 (in ε); at the smallest σ and ε, both angles within 3% of
  their leading-order forms and θ₁₂/θ₂₃ within 3% of 3/4.
- Check point: each of Venus's corrected forms within 5% of the exact SVD. Helios's originals are reported only.
- Relation 3: within 10% of the exact SVD at every rank-1 test point.
- **Fit grade** (applied to each fit):
  - PASS if all seven targets are within a factor of 2.
  - PARTIAL if V_us > V_cb > V_ub and the mass hierarchy is right (all four ratios below 1), but some target
    misses; every miss is named.
  - FAIL if the ordering or the hierarchy is wrong.
  - Venus expects PARTIAL at fixed σ_t [prediction].

## Caveats

- Toy bookkeeping. Brane profiles, widths, the tilt and the second Higgs are put in by hand [assumed input]. There is
  no brane action and no back-reaction. Only ratios within a sector are meaningful.
- Round sphere only. On the rugby ball the tilt no longer acts as d¹(β) (Job Four, [standard]).
- The up brane sits at the tip and is diagonal in this basis, so σ_u affects only the two up mass ratios, not the
  CKM [identity].
- The targets are at μ = M_Z. The toy has no scale of its own, so fitting at M_Z is a choice [assumed input].
- J = 0: the real model has no CP phase. A complex brane coupling or a relative phase between the two down branes
  would be needed.
- The fits are unweighted in log space, with no experimental errors. "Within a factor of 2" is a coarse toy grade.

## Tag key

[identity] exact algebraic statement checked numerically; [computed] produced by run.py; [assumed input] set by hand;
[prediction] stated before the run, or computed from the targets before any fit; [standard] literature result or
earlier hive result; [tuned] fitted knob; [post-hoc] changed after seeing a result.

## References

- Particle Data Group (2026), Review "12. CKM Quark-Mixing Matrix", global fit (via Orion's JOB4B_TARGETS.md; the
  spec named PDG 2022).
- G.-y. Huang and S. Zhou, Phys. Rev. D 103 (2021) 016010, arXiv:2009.04851 (mass ratios at M_Z).
- Z.-z. Xing, H. Zhang and S. Zhou, Phys. Rev. D 77 (2008) 113016, arXiv:0712.1419.
- C. D. Froggatt and H. B. Nielsen, "Hierarchy of quark masses, Cabibbo angles and CP violation", Nucl. Phys. B 147
  (1979) 277.
- N. Arkani-Hamed and M. Schmaltz, "Hierarchies without symmetries from extra dimensions", Phys. Rev. D 61 (2000)
  033005, arXiv:hep-ph/9903417.
- Job Four: `C:\Users\Akitt\sm-rugby-yukawa\` (main 3b2e06a), for the j = 1 triplet, the soft law and |V| = |d¹(β)|.

## Post-run

run.py was run once (RESULTS.md header gives the time). Thresholds and code were not changed after the run. All
numbers are in `RESULTS.md`. This section adds no numbers of its own.

- **Pre-run smoke test (disclosed):** before the run, one interactive call checked only the D(β)-vs-quadrature
  identity at a single point. Nothing was written and nothing was changed as a result.
- **A1, A2, relation 3:** PASS, as graded in RESULTS. The relation-3 prediction from the targets came out as Venus
  expected: single-brane mixing sits well below |V_us| (the wall).
- **Check point: FAIL against the 5% threshold fixed before the run.** θ₂₃ and θ₁₃ of Venus's corrected forms pass,
  but θ₁₂ with the physical gap misses 5%. Helios's θ₁₂ and the exact θ₁₂ match the spec's expectations. Relation 3
  still holds better than its θ₁₂ ingredient, because the errors partly cancel [post-hoc observation].
- **Masses:** the soft-law m_d/m_s estimate and its ε-shifted value both match Venus's expectations (see RESULTS).
  The up-sector analogue m_u/m_c ≈ ½·m_c/m_t lands close to its target.
- **σ_t row:** the exact Y_sd factor tracks Venus's 1 + 2σ_t·cos β/sin²(β/2). At β = 0.28, σ_t = 0.01 roughly doubles
  V_us, as Venus said.
- **Fit 1 (σ_t fixed): PARTIAL**, as Venus expected. The named miss is in RESULTS.
- **Fit 2 (σ_t free): PASS.** [post-hoc caveat] At the best fit, σ_d sits at its lower bound (1e-6, an input), so
  the aligned soft brane only supplies m_b. m_s, m_d and the mixing then come from a wide tilted brane at σ_t ≫ β²/8,
  far outside the rank-1 regime. The leading-order forms and relation 3 do not describe this point (see the LO lines
  in RESULTS). In effect the model has changed: a pointlike aligned brane plus a wide tilted brane. Only four knobs
  are active there. This should be read as "the two-brane system can reach the targets once the tilted brane is
  wide", not as a confirmation of the narrow-brane picture.
- **Top-hat row (report):** the refits give the same pattern as the soft fits, PARTIAL at fixed σ_t and PASS at free
  σ_t, again with σ_d at its bound. Re-evaluating the soft knobs with a top-hat profile mainly moves the mass ratios,
  because σ means a different width there.
- J = 0 throughout (real model): no CP violation.

## Sign-off

- Venus (maths): ____
- Helios (physics): ____
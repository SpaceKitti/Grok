# Job 6c: κ(d) for the SU(2) matrix models in d = 2, 3, 5, 9

Folder: `C:\Users\Akitt\membrane-6c-kappa-d\`. Files: `run.py` (the only code), `RESULTS.md` (written only by run.py, never hand-edited), this README.
This README holds no computed numbers. Every number from the run is in RESULTS.md.

## Spec
- `C:\Users\Akitt\open-problems\STILL_TO_DO.md`, line 74 (Job 6c): redo Job 6b's valley balance for the SU(2) matrix models in d = 2, 3, 5, 9, and derive κ(d) against the normalisability bar. Sympy only, no grids.
- Steering from NanoRibbon (for Akitti cat), Venus and Helios:
  - PASS = the computed κ(d) match FGHHY's values at d = 2, 3, 5, 9.
  - The final yes/no on a bound state comes from the Witten index, printed as a separate column.
  - d = 5 (fold-in wording): the only state clearing the bar is odd under the antipode map, so not a ground state. Tagged odd [computed: σ; other two factors standard: FGHHY §4.3]; only the factor σ is computed here.
  - Venus: derive the bar per d, state whether FGHHY's κ includes the measure and transverse factors, and reconcile the bar κ > d/2 with FGHHY's 3/2.
  - Sources (fold-in): Kac–Smilga eq. (1.25) is the main source for the Witten index at d = 9, 5, 3. Yi is cited for the bulk terms only, with a note that his −1/4 defect is conditional. Moore–Nekrasov–Shatashvili is used only for the list of allowed dimensions. Staudacher is dropped. d = 2 is tagged [standard: Fröhlich–Hoppe CMP 191 (1998) 613, hep-th/9701119; 'simplest model' = SU(2), d = 2 per FGHHY §3].
  - Wording: at d = 9 the solution is labelled "normalisable; existence from the index", not "bound state". FGHHY fix only the behaviour far along the valley, and only the Witten index settles that a bound state exists.

## Method (all in run.py)
- **Stage A, sympy [identity]:**
  - The radial measure far along the valley is the orbit factor r² × the E-sphere factor r^(d−1) × the transverse Gaussian factor r^(−(d−1)). This gives the bar on FGHHY's κ for every d.
  - FGHHY's κ already includes the measure and transverse factors. Removing them gives the effective exponent κ_eff = κ − 1 + (d−1)/2 on R^d, whose bar is d/2. The equivalence of the two bars is checked symbolically. This is the reconciliation of κ > d/2 with κ > 3/2.
  - The 6b toy is redone as a special case, along with the −1/4-per-direction oscillator term.
- **Stage B, Clifford algebra [computed]:**
  - FGHHY's γ-matrices (eq. 27) are built from the left multiplications of C, H, O, with integer entries.
  - The Spin(d−1) generators, the Casimir, the chirality Θ and the antipode parity σ (eq. 32) are computed on the Clifford module.
  - Spin(d−1)-singlet fermion states are found by null space, and rep dimensions by Krylov closure.
  - κ′ is read from eq. (40) and cross-checked against 8C/s_d. Then κ = 1 + κ′ − (d−1)/2.
  - Term (i) (eq. 39) is checked on the full fermion Fock space for d = 3 and 5.
  - For d = 2, the M₁₂ spectrum is computed. A non-integer spectrum means no invariant asymptotic state.
  - The allowed-dimension check s_d = 2(d−1) is run for d = 2…10.
- **Stage C, table:** for each d, the table shows:
  - κ computed vs FGHHY, reps and σ vs FGHHY;
  - the bar and κ_eff;
  - the asymptotic status;
  - the Witten index with its source, and bound state yes/no from the index.

## Rules fixed in code before the first run
Tolerances (ID_TOL, NULL_TOL, RAT_TOL), the FGHHY reference values (κ, reps, σ), the Witten index values and sources, and the grading rules are all fixed at the top of run.py:
- PASS iff all κ, reps and σ match FGHHY and the identity checks pass.
- Per solution:
  - κ > bar and even → "normalisable; existence from the index";
  - κ > bar and odd → "not a ground state", tagged odd [computed: σ; other two factors standard: FGHHY §4.3] (fold-in relabel);
  - κ ≤ bar → "not normalisable".
- Bound state yes/no comes only from the Witten index.

run.py was run once, then once more as the fold-in pass (see Post-run).

## Caveats
- Term (i) of eq. (39) is checked on the full Fock space only for d = 3 and 5. For d = 9 (256-dimensional module, 2^24-state Fock space) it is taken from FGHHY [standard].
- Θ's sign depends on the orientation of the γ-matrix basis. It is reported, not graded.
- Witten index:
  - Main source: Kac–Smilga eq. (1.25), which gives the index for d = 3, 5, 9 from the principal term and the deficit, both computed there.
  - Yi is cited for the bulk terms only. His −1/4 defect is motivated but not derived (he calls it an outstanding problem), so it is conditional.
  - d = 2: [standard: Fröhlich–Hoppe CMP 191 (1998) 613, hep-th/9701119; 'simplest model' = SU(2), d = 2 per FGHHY §3], no SU(2)-invariant ground state.
- numpy is used for exact-integer Clifford matrices. No grids or discretisation anywhere.
- The harmonic reading of κ_eff is [hive-interpretation].

## Tags
[identity] symbolic or algebraic identity checked in code · [computed] number produced by run.py · [standard] taken from the literature · [standard: beyond toy] a result outside what the 2-variable toy can reach · [hive-interpretation] our reading, not in the sources · [assumed input] input not derived here · [post-hoc] added after seeing the run.

## References
- J. Fröhlich, G. M. Graf, D. Hasler, J. Hoppe, S.-T. Yau, "Asymptotic form of zero energy wave functions in supersymmetric matrix models", Nucl. Phys. B 567 (2000) 231, hep-th/9904182 (FGHHY below). Read from Orion's PDF in `open-problems\03_membrane_renormalization\`.
- P. Yi, "Witten index and threshold bound states of D-branes", hep-th/9704098.
- V. G. Kac, A. V. Smilga, "Normalized vacuum states in N = 4 supersymmetric Yang–Mills quantum mechanics with any gauge group", hep-th/9908096.
- G. Moore, N. Nekrasov, S. Shatashvili, "D-particle bound states and generalized instantons", hep-th/9803265 (allowed dimensions only).
- J. Fröhlich, J. Hoppe, "On zero-mass ground states in super-membrane matrix models", Commun. Math. Phys. 191 (1998) 613, hep-th/9701119 (d = 2 entry; FGHHY §3 identify its 'simplest model' as SU(2), d = 2).
- E. Witten, "Bound states of strings and p-branes", Nucl. Phys. B 460 (1996) 335, hep-th/9510135 (§3.2: one D0 bound state per n is needed to match the Kaluza–Klein spectrum of 11D supergravity).
- T. Banks, W. Fischler, S. H. Shenker, L. Susskind, "M theory as a matrix model: a conjecture", Phys. Rev. D 55 (1997) 5112, hep-th/9610043 (the threshold bound state carries the supergraviton multiplet).
- Job 6b: `C:\Users\Akitt\membrane-6b-boundstate\` (the valley balance redone here).

## Physics note (Helios)
- The toy reproduces the known answer but does not prove existence at d = 9. Term (i) at d = 9 and the existence of the bound state come from the papers (FGHHY, and the Witten index from Kac–Smilga). The result is a reproduction, not a prediction.
- The d = 9 state is the one matrix theory reads as the 11D graviton [standard: Witten hep-th/9510135; BFSS hep-th/9610043; verified by Orion].

## Post-run
- run.py was run once on 2 Oct 2026 (BST) and exited cleanly. No code changes after the run. All numbers are in RESULTS.md.
- Outcome: see RESULTS.md, "Grade". The overall PASS/FAIL line, the per-d lines and the index-consistency check are there. The κ(d), rep and σ comparison with FGHHY is in the Stage C table. The bar derivation and the reconciliation of the two conventions are in Stage A.
- Wording follows the steering. At d = 9 the solution is labelled "normalisable; existence from the index", not "bound state".
- **Fold-in pass [post-hoc]:** run.py was rerun once (2 Oct 2026, BST). RESULTS.md was regenerated by run.py, never hand-edited. A backup of the folder before the pass is in `%TEMP%\membrane-6c-backup-20261002-2056\`. Changes:
  - (1) d = 5 relabelled: the only state clearing the bar is odd under the antipode map, so not a ground state. Tagged odd [computed: σ; other two factors standard: FGHHY §4.3]. The grade lines match, and the first pass's label no longer appears in RESULTS.
  - (2) The transverse exponent in the Stage A measure line is bracketed, so it now prints as −(d − 1). This fixes the cosmetic defect of the first pass.
  - (3) Kac–Smilga eq. (1.25) is now the main index source. Yi is cited for the bulk terms only, with the conditional-defect note.
  - (4) d = 2 is tagged [standard: Fröhlich–Hoppe CMP 191 (1998) 613, hep-th/9701119; 'simplest model' = SU(2), d = 2 per FGHHY §3].
  - A diff against the backup shows every κ, rep, σ, κ_eff and identity result unchanged. Only these labels and sources, the timestamp and the runtime differ.
- Caveats from above still stand: term (i) for d = 9 is [standard], Yi's defect is conditional, and Θ is ungraded.

## Sign-off
- Venus (maths): PASS
- Helios (physics): PASS as a reproduction
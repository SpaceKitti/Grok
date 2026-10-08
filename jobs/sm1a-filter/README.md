# SM1 Part A: input-free stages (SM1_filter)

Spec: `JOB_SM1A_SPEC.md`, SHA-256 prefix **04B9AA05** (Venus passed this hash; it replaces 712EF4A8). Problem 1 (Standard-Model attachment) only. This README was written before the graded run and holds no number computed by it; results are in `RESULTS.md`, `CANDIDATES.md`, `OVERLAPS_ALPHA.md` and `ANOMALIES.md`, which only `run.py` writes.

## What Part A does

Part A builds and counts; it scores nothing and grades no physics. It is input-free: none of Akitti's inputs (μ, G, r_c, Ψ, Π) is used or filled in, and her construction is only quoted. The only `SM1_INPUTS.md` value `run.py` may use is α_ext (spec 0.2), and only when the line carries an `[Akitti: …]` tag. That file does not exist today, so this is a grid-only run on α ∈ {1, 4/5, 3/5, 1/2} [assumed]. Part B (1ADF2904) is HELD and is not built; Q12 is untouched. The lift's gravity is unknown quantum gravity [Akitti]; nothing here uses an Einstein equation, and GR appears only as labelled [GR control] rows in the source datasets.

Stages (spec section 4):
- Stage 0: hash every source in spec section 2 and stop on any mismatch; print which `SM1_INPUTS.md` fields are present (presence only).
- Stage 1: the 16-row candidate table (S1-S9, R1-R6, B1) → `CANDIDATES.md`, with S1-S9 recomputed using Job Two's `monopole.py` and `anomalies.py` and R1/R2 using Job Four's solver.
- Stage 1b: S5's anomalies; R3-R5 and R6 on the rugby ball; B1 on B0's backgrounds; the U1 cross-check; the per-count table; the E4 section counts; the overlap table → `OVERLAPS_ALPHA.md`; I₆ and I₈ → `ANOMALIES.md`.

Counts and anomalies do not depend on α for α ≤ 1 (A2, A5 [Venus]). Only tip exponents, wavefunctions and overlaps carry α.

## n convention (spec 1.2, A7 [Venus])

N_Φ = |x|·(1/2π)∫F = 2|q|. Counts: Dirac N_Φ, scalar lowest level N_Φ + 1, g = 2 spin-1 lowest level N_Φ − 1. Conversions on read: Job Two, Job Four and B0 give N_Φ = |x|·n; U1 gives N_Φ = n; an RW charge gives N_Φ = 2n_RW. In `run.py` every count is formed from an `NPhi` object that only `convert()` can build; a raw integer raises `ConventionError`, and C-d tests that hard stop.

## How Venus's edits E1-E4 are handled

- **E1:** tr R⁴ net = N₊ − N₋ (6D Weyl components at Γ₇ = +1 minus those at Γ₇ = −1). The file magnitudes for MAIN (RESULTS line 122) are read and given the E1 sign.
- **E2:** tr F⁴ for SU(2) and SU(3) is written as ½(tr F²)² inside I₈, so only tr R⁴ is irreducible. The tr F⁴_SU(3) "2 vs 2" count is a build-reproduction check inside C-a, never an anomaly condition. The identity is also checked on random su(2), su(3) and su(4) elements (report-only).
- **E3:** I₆ is expanded independently with sympy from (1/6) tr F³ − (1/24) p₁ tr F over the 4D left-handed zero modes, with right-handed fields entering as conjugates with all charges flipped and Y SM-normalised. Each coefficient is compared exactly with Job Two's `anomalies.py` sums after the E3 map (½ on tr F²·F_X, 1/6 on F_X³, ½ on the mixed U(1) terms, −1/24 on p₁ F_X; likewise for the SM U(1)_Y terms).
- **E4:** all overlaps use ψ_s = (α sin θ)^(−s) tan(θ/2)^((m−q)/α) sin(θ)^(q/α) e^{imφ}, m ∈ ℤ + s, with spin-weight closure s₁ + s₂ = s₃ as well as m₃ = m₁ + m₂. Build interpretation, disclosed: a section of negative charge is taken as conj(ψ_{−q,−s,−m}), because the E4 form with q < 0 has no regular modes. At α = 1 the map to Job Two's monopole harmonics (charge Q = q − s, m_J = m − q, a constant unit phase) is checked at two angles inside O-a.

Venus's answers A2-A9 and Q16 are applied as written in spec section 7. No gaugini are in the graded run (A9). Part A only reports the tr R⁴ net; Part B applies the Q16 gate.

## Build choices (disclosed)

- **S5 content:** S5 includes ν^c, and its 4D content is all left-handed (no conjugation).
- **S6:** S6 is S3's fermion content. Its Higgs C (j = 3, 7 modes) is cited, not recomputed.
- **Job Four's run.py:** it is imported as a module, so its module level runs (it hashes Job Two's folder and imports its `monopole.py`) but `main()` does not. Its global q is set per case and restored afterwards.
- **B0's run.py:** this file runs its whole job at import. So `run.py` takes only B0's background functions and constants from it by AST and re-implements B0's continuation loop (B0 lines 249-263).
- **B1** is a minimally coupled unit-charge Dirac fermion in flux n on B0's computed backgrounds (A8: [identity: index theorem; independent of φ]; a build check). It uses three methods:
  - regularity (tip slopes);
  - normalisability (∫ to 20 vs to 40 in t);
  - finite differences of R²D² with eigenvalues below 0.5 counted.
- **B1 finite differences [post-hoc, development]:** the FD uses the same operator as Job Two/Job Four, but on a grid uniform in t = ln tan(θ/2), t ∈ [−40, 40], step 0.01, with Dirichlet ends.
  - **Why:** the box scratch run showed that the θ-uniform grid (N = 2000, as Job Four) undercounts B1 at n = 3 at the largest ε. The mode with |ψ|² ~ θ⁰ at the north pole sits at the Hardy-critical point, and its FD eigenvalue error there falls only like 1/ln N, which matters when the vortex flux is concentrated at that pole.
  - The θ-grid count is kept as a report-only column. The threshold 0.5 is unchanged.
- **R family:** Job Four's own `Mode` and `fd_rugby` (N = 2000, τ = 0.5), unchanged.
- **Optional report-only variants:**
  - the tip-flux δ shift (A3);
  - the tr R⁴ shift from a gaugino variant (A9);
  - the factorisation test.
  - Jackiw-Rossi is not run.

## Thresholds (fixed before the graded run)

| item | value |
|---|---|
| FD zero-mode threshold on R²D² | 0.5 (Job Two / Job Four) |
| FD grids | N = 4000 (S family, Job Two); N = 2000 (R family, Job Four); B1 t-grid [−40, 40], step 0.01 |
| regularity / normalisability | tip exponent ≥ −1e-6; abs(ln Z(40) − ln Z(20)) < 1e-8 (Job Four) |
| O-a | 1e-12 absolute |
| O-b | 1e-9 relative |
| O-c | 1e-12 absolute |
| O-d | 1e-12 absolute |
| C-a, C-b, C-c, C-d, A-a, A-b | exact (integers, sympy Rational) |
| quadrature | Gauss-Legendre in t, 2000 nodes on [−40, 40]; check grid 4000; mpmath 40 digits for closed forms |
| α grid | 1, 4/5, 3/5, 1/2 [assumed] |

## Pass rules (spec section 5, restated)

- **C-a:** S-family recomputed counts, chiralities, hypercharge survivors, U(1)_X sums and 6D counts equal the cited file values exactly.
- **C-b:** at n = 3 on the grid, the R1/R2 count and m values equal Job Four RESULTS lines 106-109 exactly, and the three methods agree.
- **C-c:** for n = 1, 2, 4 (R3-R5), R6 and B1, the count equals N_Φ and the three methods agree. Any disagreement is printed as FAIL with the numbers. Nothing is tuned. For B1 this is a build check (A8).
- **C-d:** every count is formed from N_Φ in the declared convention. The Higgs rows reproduce Job Two's 5 (s = 1) and 1 (s = 0). The E4 counts N_Φ + 1 − 2s hold at every grid α.
- **O-a:** at α = 1 the overlaps reproduce Job Two's exact wigner_3j values (RESULTS lines 137-144) to 1e-12 absolute.
- **O-b:** at every α, quadrature agrees with the closed form to 1e-9 relative.
- **O-c:** entries that break the m rule are ≤ 1e-12.
- **O-d:** the constant-Higgs Gram row gives 1/√(4πα) at every grid α to 1e-12 (Job Four RESULTS lines 16-19).
- **A-a:** I₆ coefficients are exact rationals equal to the Stage 1 sums after the E3 map.
- **A-b:** the tr R⁴ net reproduces S1 0, S2 −1, S3 −16 and S4 −15 (E1). The tr F⁴_SU(3) count and the factorisation are not anomaly conditions (the count is a build check inside C-a; the factorisation is report-only).
- **Audit:** every source and this folder's inputs are unchanged by the run.
- **Build PASS** = every graded item passes.

## Honest prediction (before the graded run)

- I expect Build PASS.
- Every count should equal N_Φ (Dirac), N_Φ + 1 (scalar) or N_Φ − 1 (spin-1) at every grid α.
- The tr R⁴ nets should be as the spec states for S1-S4. The ALT + ν^c rows should be zero, S2 and R2 should equal S2's value, and the MAIN-content rows and S5 should be nonzero.
- S5's SM gauge sums should not vanish, since all its fields are left-handed.
- The α < 1 overlaps should differ from their α = 1 values, apart from the constant-Higgs Gram row.
- The B1 count should stay n at every ε.

## Development disclosure

Box scratch runs were done on a mock tree on the box that mirrors the TrinityOrb paths, with source copies whose hashes match. The only post-hoc change after a scratch run, other than formatting and bug fixes, is the B1 FD grid above, tagged [post-hoc, development]. No tolerance or pass rule was changed. The single graded run is on TrinityOrb.

## Post-run notes

Added 2026-10-08 (BST) after Venus's maths grade and Helios's physics grade, both PASS with notes. Everything here is report-only. No graded output was regenerated or hand-edited: run.py 803FD2DA, RESULTS 7148A1DC, CANDIDATES DAD867CE, OVERLAPS_ALPHA D93AC9BD and ANOMALIES B55D5D1F are unchanged. This README was 12CEC48F before these notes. The text above this section is the pre-run README, left as written. Errata to it are listed here as notes, not edited into it.

**(1) I₈ cross-term sign: a convention mismatch in the spec.** ANOMALIES prints I₈ with −(1/96) tr R² tr F². The spec cites the anti-Hermitian form [Â tr e^{iF/2π}]₈ (spec line 214), but the E3 map that I₆ uses treats F as real (spec lines 208–212). For real F the correct sign is **+(1/96)**. So every term linear in r2 = tr R² at ANOMALIES lines 280–308 flips sign. The corrected terms are:
- ALT + ν^c (line 280): fY² r2/48 − r2 t2/24. The corrected second factor (line 283) gives I₈ = −(2 t2 − fY²)(24 fX² + 3 fY² + r2 + 2 t2 + 6 t3)/48.
- ALT without ν^c (line 287): −fX² r2/96 + fY² r2/48 − r2 t2/24.
- MAIN + ν^c (line 294) and S5 + ν^c (line 308): −fX² r2/6 − 5 fY² r2/144 − r2 t2/24 − r2 t3/24.
- MAIN without ν^c (line 301): −5 fX² r2/32 − 5 fY² r2/144 − r2 t2/24 − r2 t3/24.

Wrapping the 6D anomaly on the flux sphere has to give back the 4D anomaly:

$$I_6 = -n\,\frac{\partial I_8}{\partial F_X}\bigg|_{\mathrm{tr}R^2 \to -2p_1}$$

Reduction-check result (note 2):
- With +(1/96), this reproduces the graded I₆ for all 15 S/R candidates.
- With −(1/96), it fails in the p₁ F_X term for S2, S3, S4, S5, S6, R2 and R6. Venus's note named S2–S5; S6, R2 and R6 fail too because they share S3's or S2's content.
- It holds either way for the ALT + ν^c rows, because their mixed gravitational–X sum is zero.

Unaffected: the tr R⁴ nets, I₆ (A-a, A-b) and every factorises yes/no answer. ALT + ν^c still factorises. The other contents still have tr R⁴ left over.

**(2) The I₈ → I₆ reduction (Venus's hole 2) is now run as a report-only check.** `I8_REDUCTION_CHECK.py` (1FAC9593) writes `I8_REDUCTION_CHECK.md` (2694D622). Its stdout is in %TEMP%\i8_reduction_stdout.txt on TrinityOrb. It takes run.py's own content, I₆, I₈ and factorisation code by AST and does not import or run run.py. It also checks that run.py's code reproduces the printed I₆ and I₈, and it does.

**(3) The B1 grid change (disclosure 1).** The count of 3 is the A8 index (the flux is 3), fixed before any grid was chosen. The FD column is only a build check. `B1_TGRID_CONVERGENCE.py` (9A5F3330) writes `B1_TGRID_CONVERGENCE.md` (DC8F40C7). Its stdout is in %TEMP%\b1_tgrid_stdout.txt, with the first version's in b1_tgrid_stdout_v1.txt. It covers n = 3, ε = 4 and reproduces the graded row: flux 3, t-grid FD 3 and 0, θ-grid 2 and 0.

The m = ½ mode sits exactly on the critical inverse-square point of its pole potential. So on either grid its eigenvalue goes to zero only logarithmically. On the t grid the step size hardly matters, and what is left is set by the end cut T. Venus and Helios asked for a scan in T, so that is the main table (step 0.01, window [−T, T]):

| T | m = ½ eigenvalue | T × that eigenvalue | count below 0.5 |
|---|---|---|---|
| 20 | 0.3788 | 7.58 | 3 |
| 40 (graded) | 0.1821 | 7.28 | 3 |
| 80 | 0.0893 | 7.15 | 3 |
| 160 | 0.0444 | 7.10 | 3 |

The leftover eigenvalue falls like C/T with C close to 7, as Venus predicted. The count is 3 at every T. This corrects the pre-run wording: the t grid doesn't remove the slow logarithmic error. It behaves like a θ grid with ln N of about T, and that's why it clears 0.5 easily.

Side by side on Venus's N ladder, with the 0.5 cut-off. The t grid keeps the window [−40, 40] and uses spacing 80/(N+1):

| N | θ grid: m = ½ eigenvalue | θ-grid count | t grid: m = ½ eigenvalue | t-grid count |
|---|---|---|---|---|
| 2000 | 0.8324 | 2 | 0.1822 | 3 |
| 4000 | 0.7695 | 2 | 0.1821 | 3 |
| 8000 | 0.7154 | 2 | 0.1821 | 3 |
| 16000 | 0.6684 | 2 | 0.1821 | 3 |
| 32000 | 0.6271 | 2 | 0.1821 | 3 |

- The θ grid undercounts (2) at every N on the ladder. Before this, the θ sequence was only in chat; now it comes from a run file.
- Venus's fit a/(ln N + c) matches it with a ≈ 7.05 and c ≈ 0.87. On that fit the θ grid would need about N ≈ 6 × 10⁵ points (5.6 × 10⁵) to drop below 0.5. A θ-grid run at that size: **NOT COMPUTED (YET)**.
- The window check at step 0.01 gives 3 on [−30, 30], [−40, 40] and [−50, 50].

**(4) Wording errata.**
- **S5's tr R⁴ net of −16** comes from all 16 of its 6D Weyl components sitting at Γ₇ = −1. It doesn't come from their 4D left-handedness. S3, S6 and R6 have 4D right-handed singlets and the same −16, because tr R⁴ counts 6D chirality.
- **B1 is n/a in the SM 4D anomaly check, not a fail.** It has no SM charges, and CANDIDATES line 400 already says so. My Hive wrap's "S5 and B1 don't cancel" should read "S5 doesn't; B1 is n/a".
- **Gaugino variant (A9):** the ±13 gaugini have the opposite chirality to the matter. For MAIN-content rows (matter at Γ₇ = −1) that means +13: S3, S5, S6 and R6 go from −16 to −3, and S4 from −15 to −2 (report-only). ALT has matter at both chiralities, so the sign there isn't fixed. The adjoint tr F⁴ shift: **NOT COMPUTED (YET)**.
- **README line 7** cites Part B as 1ADF2904. That hash is superseded (Venus graded against BE912C18, and Helios is adding S5 to its Q16 list).
- **O-a** cites Job Two RESULTS lines 139–144, while the spec's O-a rule says 137–144. They are the same rows; the two header lines are left out.

**(5) CANDIDATES line 400, "Survivor counts", is a tally of Part A properties, not a survivor list.** No candidate survives or is selected in Part A, and Part A applies no gate. The string will be reworded in run.py at the next re-run. There is no re-run now, and output files are not hand-edited.

**(6) Tip flux (report-only, A3).** δ = ¼ gives 2 bounded vs 3 normalisable modes only at α = 1, 4/5 and 3/5. At α = ½ it gives 3 vs 3 (CANDIDATES lines 385–388, checked against the graded file). At α = ½ the m = ½ north exponent sits exactly on the bounded edge. My wrap's unqualified "2 vs 3" is corrected to this.

**(7) RESULTS line 7 erratum.** It lists the FD grid as "N = … 2000 R family and B1", which reads as if B1's count used N = 2000 or the θ grid. B1's graded count used the t grid (step 0.01 on [−40, 40]; README line 54; run.py lines 53–54). N = 2000 is only B1's report-only θ column.

## Sign-off

Venus (maths): PASS with notes. Grade VENUS_GRADE_NOTES.md E6754653; signed against README B655B422, 2026-10-08 16:19 BST.

Helios (physics): PASS with notes. Grade SM1A_HELIOS_GRADE.md F9CB456F; signed against README B655B422, 2026-10-08 16:21 BST.

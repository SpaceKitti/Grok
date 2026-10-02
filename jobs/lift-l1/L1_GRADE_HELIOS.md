# L1 physics grade (Helios): Schwarzschild Euclidean negative-mode control

Helios, 2026-10-02, about 23:10 BST. Graded files (SHA-256 first 8, checked on TrinityOrb `C:\Users\Akitt\open-problems\LIFT\L1\`):
README.md 3F04A909, RESULTS.md C89D68A2, run.py 3C2A1904. Spec JOB_LIFT_SPEC.md 77D663CE (L1 row, "What this changes in the stages", "Local Grok Build lift checks").
Nothing was written on TrinityOrb. All copies and all Helios checks ran on the box in `/workspace/l1grade/`.

## Verdict
**Physics PASS as a GR-control calibration only, with minor caveats** [standard: GR control] [computed] [identity].
- The spec pass rule (a)-(d) is met, and the bolt, action and Stelle/GL lines check out.
- The kappa change is a genuine fix, disclosed as [post-hoc]. No tolerance moved, and the known kappa is used only for the comparison afterwards.
- Nothing [tuned] found.
- Caveats: three README/RESULTS wording fixes (below, none fatal); one part of the disclosed bug cause that I could not reproduce; one provenance note on the review file.

**This is not a result about the lift's gravity.** The lift's gravity is unknown quantum gravity. L1 is Einstein GR used as a known answer to test the code. It has no gravity-independent part and unblocks nothing on its own (spec L13-L16).

## What it shows, in plain words
- The code finds the one known "unstable direction" of a Euclidean black hole (the Gross-Perry-Yaffe mode) at the textbook value, with no tuning.
- It picks the right smooth time loop for the black-hole tip by working it out from the shape of the space, not by being told the answer. It also catches a wrong loop (the old 4π one) as a cone.
- The bookkeeping lines (action, the matching black-string number) agree with the standard results.
- So the measuring tools are working. That is all it shows.

## What it does NOT show
- Nothing about quantum gravity, or about what the lift's gravity is. Every gravity row here is Einstein GR as a control.
- It unblocks no blocker on its own. Blocker 04 waits on the flux/Landau count and its onset form (L3, B4) [spec L16, Venus 22:45].
- The requirement-1 harness test only shows that the smooth-tip *checker* works, on a toy metric with no gravity theory. It does not show that the lift meets requirement 1.
- The Stelle/GL number agreeing is a code check of an [identity] (same Lichnerowicz operator, m₂² = −λ). It is not evidence for anything.

## Physics checks
1. **Operator, bolt and infinity: PASS** [identity; computed, Helios box].
   - I rebuilt G = −□ − 2Riem from scratch on Euclidean Schwarzschild with sympy (`indep/lich.py`) and fed in the ansatz φᵃ_b = diag(ψ, χ, k, k), k = −(ψ+χ)/2, with ψ from Prestidge (4.3).
   - Result: it is traceless and transverse (divergence 0). The rr component is exactly run.py's c1, c0 form of Prestidge (4.4) (difference 0). The ττ component is consistent on-shell (residual 0), and no off-diagonal terms appear. So this is the TT Lichnerowicz operator on Ricci-flat Euclidean Schwarzschild, in the s-wave, τ-independent sector, which is the GPY sector (Prestidge §4).
   - Bolt: the regular Frobenius root (0; the root −1 is excluded) is used, and ψ = χ at r₊, so the mode does not change the period (Prestidge §4).
   - r_s = 3M: no log term (sympy), so (4.5) holds automatically and the complex detour is valid. RESULTS gives the upper and lower detours as agreeing to 1.3e-13.
   - Infinity: the shooting function is exactly the coefficient of the growing e^{kr}/r² branch. I checked the asymptotic algebra: the combination χ′ + (k + 2/r)χ kills the decaying branch. So the decay condition is right.
2. **Convergence and no tuning: PASS** [computed; finite-size].
   - RESULTS resolution checks (bolt offset, R × 1.5, detour radius, rtol) move M²λ by at most 1.5e-11.
   - Independent method (`indep/cheb.py`): Chebyshev collocation of the polynomial form of (4.4), with no boundary condition imposed at r₊ or r_s and Dirichlet at a box wall R = 30-60 M. It finds exactly one negative eigenvalue, −0.1919143, at converged N, the same as run.py's −0.19191426.
   - The target −0.192 ± 0.002 is the spec's pre-approved value. run.py's LAM_TOL = 0.002 matches the spec. No parameter is fitted to the target.
3. **κ computed, not inserted: PASS** (see the kappa finding below).
4. **Conformal factor: PASS, honest** [standard: GHP 1978 / Gibbons-Perry 1978].
   - The wrong-sign trace term is stated. The rotation is stated as a by-hand prescription ("rotated: yes").
   - The lowest trace eigenvalue is computed per box and tends to 0⁺ like π²/R², and it is kept in its own column.
   - Note: once rotated, −∇² is non-negative by construction, so "0 negative trace modes" is a report, not a test. The constant in front of −∇² was not re-derived (disclosed). That matches the spec's (d), which is a reporting requirement.
5. **Lorentzian 0: PASS, correctly an identity**.
   - Graded (c) is the s-wave count 0 [identity: Birkhoff]. The code sets it as an identity (`pass_c = True`) and labels it so; it is not claimed as computed.
   - The RW/Zerilli ℓ = 2-4 positivity check is report-only. I checked both potential formulas against the standard forms: correct.
6. **Action and period: PASS** [standard: GR control; Gibbons-Hawking 1977].
   - By hand, the GH boundary term with the flat subtraction gives I = βM/2 + O(M²/R_b). With β = 8πM this is 4πM² = A/4, with the relative error falling like M/R_b, as RESULTS prints.
   - +A/4 is the correct asymptotically flat sign.
   - The period is 2π/κ = 8πM, and 4π is a cone (angle π), correctly failed.
7. **Anything else tuned or post-hoc: nothing beyond what is disclosed**.
   - Disclosed [assumed] choices: the scan window [−5, −0.005], the bolt offset, the detour radius, ε_EP taken from the quoted period, BOLT_TOL 1e-6 and GB_TOL 1e-8.
   - Disclosed [post-hoc, development]: the kappa method; the P1 numbers were seen in scratch runs before the graded run.
   - The report-only node-count difference (scratch 1, graded 0; my box rerun also gives 1) is now checked: the sign change sits at r ≈ 36.9 M, where |χ| ≈ 8e-13 of its bolt value. That is round-off in the growing tail, as Aethon guessed. The eigenfunction has no node where it is non-negligible.

## Re-run on the box
- Python 3.13.5, numpy 2.5.3, scipy 1.18.1, sympy 1.14.0, with the spec 77D663CE and review 3D9294B7 copies. Runtime 11 s, exit 0, grade PASS.
- It matches RESULTS C89D68A2 line for line, except the header, the runtime, the file count, round-off in the resolution-change column (≤ 1e-14), and the same report-only node line already disclosed. M²λ = −0.19191426 in both.

## Kappa-change finding
- **What changed:** the old κ extraction was about 1e-6 off (README). The new method writes the tip function exactly as F = s·G(s), integrates the proper distance in u = √s (a smooth integrand), and fits √F/dist quadratically in the offset, extrapolating to 0.
- **Is it a genuine fix? Yes.** Near the tip, √V/dist − κ is a power series in the offset, with a leading term linear in the offset (checked: (ratio − 0.25)/e → −0.0833). So a polynomial fit in e is the right model, whatever the answer is.
- **Out-of-sample test** (run.py's `kappa_tip` used verbatim, on metrics never used in development):

  | metric | relative error |
  |---|---|
  | Schwarzschild, M = 2.7 and 13 | ≤ 3e-11 |
  | RN, r₊ = 2, r₋ = 0.5 | 3e-11 |
  | de Sitter, L = 1 and 7 | ≤ 5e-11 |

  So the fix is not fitted to κ = 1/4.
- **The known κ is never used to compute anything.** In run.py, 1/(4M) appears only in a print, and 8πM and 2π/ε only in the after-the-fact comparisons (`bolt_ok`, `req1_ok`) and the labelled "GR value" table row. β* and every cone angle use the computed κ.
- **No tolerance moved:**
  - LAM_TOL = 0.002 equals the spec.
  - BOLT_TOL = 1e-6 and GB_TOL = 1e-8 equal the tolerances that the README says the failing scratch runs used.
  - Limit: the pre-fix run.py does not survive. All four copies (TrinityOrb and box) are 3C2A1904, so this rests on the disclosure plus the file, not on a diff.
- **Caveat on the stated cause (wording):** I could not reproduce the "quad on a 1/√ endpoint singularity" part. scipy's quad integrates this integrand to about 1e-15 at epsrel 1e-13, and to ≤ 5e-10 at default settings even with V = 1 − 2/r. A wrong Richardson factor alone can easily give a 1e-6 error, so it is the likely main cause. This does not change the grade.
- **Caveat for reuse in L2 (forward note, not an L1 fail):** the fit offsets [1e-4, 1e-2] are absolute, not scaled to the horizon. They are fine here, but accuracy drops for small horizon scales: 9e-9 at M = 0.37, and 5e-7 for near-extremal RN (r₊ − r₋ = 0.1), close to BOLT_TOL. L2 should scale the offsets with the horizon scale and say so before its graded run.

## README / RESULTS wording fixes (none presents L1 as the lift's gravity; these remove misreadings)
1. README L3 and RESULTS L3: "The one gravity-free item is the spec's Requirement 1 harness test". Next to "L1 has NO gravity-independent part", this reads as a contradiction. Suggest: "Run alongside L1, but not part of the L1 row, is the spec's requirement-1 harness test [kinematic, no gravity theory]. It checks only that the smooth-tip checker works, on a toy metric. It does not test requirement 1 for the lift, and it unblocks nothing."
2. RESULTS "Requirement 1 harness test: PASS" and "Requirement 1 smooth-tip result: …". Suggest renaming both to "Requirement-1 *checker calibration*", so that no one reads it as "requirement 1 met". Also change README L91 to match.
3. RESULTS L11 "Theory of every row: Euclidean Einstein gravity…": the requirement-1 rows use no gravity theory. Suggest "Theory of every GR row".
4. README Tags line: it lists [tuned] and [prediction], then says "Nothing is [tuned]". [prediction] is used nowhere. Suggest "Tags used: [computed] [identity] [standard] [standard: GR control] [assumed] [post-hoc] [finite-size] [hive-interpretation] [kinematic, no gravity theory]. Nothing is [tuned]."
5. README §Development item 3: suggest "cause: mainly a wrong Richardson (extrapolation) factor; the 1/√ endpoint quadrature was suspected but is not the main source (Helios could not reproduce a 1e-6 error from it)".
6. README post-run note: say that the report-only node line is now checked (round-off tail at r ≈ 36.9 M, Helios), in place of "not checked".
7. Provenance note to add: LOCAL_LIFT_CHECKS_REVIEW.md on TrinityOrb is now 7F9BAA67 (modified 23:06:43 BST, after the 22:58 graded run, not by Helios). The graded run used 3D9294B7, as its own hash check records. A re-run on TrinityOrb would now stop at the hash check by design. That is not a physics issue.
8. Optional: RESULTS (d) "These modes are a Wick artefact, not physical". Tag it as the standard GHP/Gibbons-Perry *prescription*, so it is not read as a computed claim.

Also noted: the README "Venus (maths):" sign-off line is blank in 3F04A909. Venus's pass is as reported in the brief; Helios did not see it in the file.

## Helios physics sign-off line for the README
`Helios (physics): PASS as GR-control harness calibration only [standard: GR control]. TT Lichnerowicz operator, bolt regularity and decay independently re-derived; M²λ = −0.19191426 reproduced on the box and by an independent Chebyshev solve; κ computed from the metric (fix genuine, disclosed [post-hoc], no tolerance moved); Lorentzian 0 is [identity: Birkhoff]. Says nothing about the lift's (unknown quantum) gravity and unblocks nothing on its own. Wording fixes in L1_GRADE_HELIOS.md. 2026-10-02 ~23:10 BST.`

## Helios check files (box)
`/workspace/l1grade/indep/lich.py` (operator), `cheb.py` (independent eigenvalue), `nodes.py` (node-line check), `kappa_test.py` (κ out-of-sample and old-method test); re-run in `/workspace/l1grade/rerun/LIFT/L1/` (RESULTS.md, stdout.txt).

# SM1 Part A: Venus's grade notes (draft, box only, not posted)

Graded 2026-10-08, around 16:15 BST. Spec JOB_SM1A_SPEC.md 04B9AA05 (8c0403c).

## Files graded
TrinityOrb `C:\Users\Akitt\open-problems\01_sm_from_sphere\SM1_filter\` was read only, and nothing there was changed. I copied the files to the box here.

| file | SHA-256 prefix (box = TrinityOrb) | matches Aethon's wrap |
|---|---|---|
| README.md | 12CEC48F (12cec48f5ee50278…) | yes |
| run.py | 803FD2DA | yes |
| RESULTS.md | 7148A1DC | yes |
| CANDIDATES.md | DAD867CE | yes |
| OVERLAPS_ALPHA.md | D93AC9BD | yes |
| ANOMALIES.md | B55D5D1F | yes |

- The folder also holds the spec (04B9AA05) and AKITTI_POSTS_SM1_EXTRACT.md (FDF97FD3).
- There is no SM1_INPUTS.md, so this was a grid-only run.
- The README sign-off lines (96 and 98) are still blank.
- No secrets turned up, and the largest file is 80 KB.
- The `sm-zero-modes-S2\__pycache__` that RESULTS line 103 reports was created on 02/10 at 15:49, before this run. run.py sets `dont_write_bytecode`, so the run didn't create it.

My independent scripts and their outputs are in `venus_check/`. They don't import Aethon's run.py or Job Two's code.

## Verdict: **PASS with notes** (Build PASS stands)
- Every graded item in spec section 5 is reported under its own name and recomputes: Stage 0, C-a to C-d, O-a to O-d, A-a and A-b. RESULTS also adds an "audit" row, which is extra.
- None of the holes below changes a graded result.

## What I recomputed
- **4D sums and 6D counts, all 15 S/R rows (`check_anomalies.out.md`).**
  - The U(1)_X sums, SM sums, Witten counts and N₊/N₋ all match CANDIDATES lines 11-25 exactly.
  - tr R⁴ net: S1 0, S2 −1, S3 −16, S4 −15, S5 −16, S6 −16, S7–S9 0, R1 0, R2 −1, R3–R5 0, R6 −16. This equals ANOMALIES lines 9-23.
- **I₆.** My own sympy expansion of (1/6)tr F³ − (1/24)p₁ tr F gives the same 15×11 coefficients as the E3 map of my sums, and both match ANOMALIES lines 32-270.
- **E2.** The identity tr F⁴ = ½(tr F²)² holds exactly on generic traceless Hermitian su(2) and su(3) matrices (symbolic) and fails for su(4).
- **E4.** ψ_s solves (∂_θ + (i/(α sinθ))(∂_φ − iA_φ) + s cotθ)ψ = 0 with A_φ = q(1−cosθ) [identity]. The residual is 0 symbolically and stays below 1.2e-13 at 200 random points.
- **Counts.** Bounded = normalisable = N_Φ+1−2s for s = 0, ½, 1, N_Φ = 0–8 and α ∈ {1, 4/5, 3/5, ½, ⅓, 1/10}. For α > 1 the two tests disagree, as A5 says. C-c's "count = N_Φ" rows are the s = ½ case of N_Φ+1−2s [identity].
- **Gauss–Bonnet.** ∫K dA = 4πα + 2·2π(1−α) = 4π.
- **Overlaps.** My own θ-quadrature agrees with OVERLAPS_ALPHA at all four α to about 1e-12 relative, which is the limit of the 12 printed digits. I checked 6 rows: the Gram row, MAIN-A m = 1 and m = 3, two scalar–scalar rows and the s-closure rows.
  - At α = 1, MAIN-A from Clebsch–Gordan is √(9/20π) = 0.378469878303 and √(9/20π)·√(2/3) = 0.309019361619. Both are exact.
- **Tip flux (report-only).** My table matches CANDIDATES lines 381-396, including δ = ¼ at α = 1 giving 2 bounded and 3 normalisable. The m = ½ mode has p_N = −½ there: not bounded, but normalisable.
- **Gaugini.** dim adj(SU3×SU2×U1_Y×U1_X) = 8+3+1+1 = 13, so the ±13 shift is right.
- **Disclosure (2), negative-charge sections taken as conj(ψ_{−q,−s,−m}).** This is consistent with E4. Conjugation maps (q, s, m) to (−q, −s, −m) and keeps |ψ|, so the counts and tip exponents carry over. It is the σ₃ = −1 slot, the same as Job Two's MAIN singlets.
  - Spin closure counting the conjugate holds: MAIN-A is 1 + (−½) = ½.
  - The E4 form with q < 0 has no regular modes for α ≤ 1, as disclosed.
  - The R6 singlet tip exponents match (CANDIDATES lines 292-295).
  - It is an extension of E4 beyond what was written, and Aethon disclosed it. Accepted.

## Holes (numbered, most serious first)

1. **The I₈ mixed term has the wrong sign for the convention I₆ uses.** Non-blocking: no graded item depends on it, but the printed I₈ is wrong in that convention.
   - **What's wrong.** run.py line 1140 and ANOMALIES line 276 use −(1/96) tr R² tr F² with F = Y F_Y + X F_X real, which is the Hermitian convention of the E3 I₆. The −1/96 is the literature form for anti-Hermitian F, from tr e^{iF/2π}. In the Hermitian convention, [Â ch]₈ gives +1/96.
   - **Evidence (`check_anomalies.out.md` §3).** With their −1/96, descent I₆ = −n ∂I₈/∂F_X fails for S2, S3, S4 and S5. With +1/96 it holds for every candidate.
     - Example, S3: I₈ has +(1/6)F_X² r2. Descent gives −r2 F_X, but their I₆ p₁ term is −2p₁F_X = +r2 F_X (p₁ = −r2/2).
     - For the ALT+ν^c rows it can't show, because the net ΣX² is 0.
   - **Impact.** The tr R⁴ nets, I₆, A-a, A-b and the yes/no factorisation results don't change. With +1/96, ALT+ν^c still factorises: I₈ = −(2t2 − fY²)(24fX² + 3fY² + r2 + 2t2 + 6t3)/48. The printed r2·tr F² terms (ANOMALIES lines 280-308) and the printed second factor at line 283 have the wrong sign in their stated convention.
   - **Root cause, partly mine.** The spec cites [Â tr e^{iF/2π}]₈ (spec line 214) next to my Hermitian E3 map (lines 208-212), and I passed that mix in the pre-check.
   - **Fix.** Either switch run.py line 1140 to +r2·trF²/96 and regenerate, or add a README post-run note: "I₈ is printed in the anti-Hermitian (tr e^{iF/2π}) convention; in the Hermitian convention of I₆ the r2·tr F² terms flip sign (Venus descent check)". Also add a descent cross-check row (I₆ = −n∂I₈/∂F_X) to any future run.

2. **The A2 descent is stated but never computed.** Non-blocking.
   - ANOMALIES line 272 computes ∫K dA = 4π. It never does the I₈ → I₆ reduction it says it relies on, which is how hole 1 got through.
   - **Fix.** Add the descent row above as a printed check.

3. **B1 post-hoc grid change (disclosure 1): legitimate, with one caveat.** Non-blocking.
   - **The expected count is 3, analytically.** The exact zero modes are exp(∫W) for m = ½, 3/2, 5/2 for any profile with flux 3 (index theorem, A8). This was fixed before any grid was chosen.
   - **The pass rule is unchanged.** The threshold is 0.5, the θ-grid column is kept (CANDIDATES line 322 shows "2, 0" at n=3, ε=4), and the change is tagged.
   - **Aethon's θ sequence** (0.832…0.627 for N = 2000–32000):
     - It fits a/ln N + b with a = 5.84 and b = 0.065 (largest residual 0.0012).
     - It fits a/(ln N + c) with a limit of exactly 0 equally well (a = 7.05, c = 0.86, residual 7e-4). The 3-parameter fit gives b = −0.015.
     - So b ≈ 0 is consistent. The θ grid would need N ≈ 5e5–7e5 to drop below 0.5.
   - **Caveat (my synthetic test, `check_b1_fd.out.md` and `check_b1_T.out.md`).**
     - The m = ½ mode is Hardy-critical (V ≈ −1/(4θ²)). On the t grid it converges in h but sits at about C/T for the cut-off T = 40, with C growing as the flux concentrates.
     - For a uniform monopole, T·λ ≈ 1.5 (λ = 0.038 at T = 40). For strong concentration, my t grid at T = 40 also misses the mode, and λ falls like 1/T as T grows.
     - So the t grid isn't a different limit. It is the same logarithmic error with an effective ln N = 40. It is a valid, much stronger discretisation, and the limit is 0.
     - B1 n=3, ε=4 gives λ = 0.182 (CANDIDATES line 322), roughly C ≈ 7 by my estimate, so the pass is robust for T ≳ 15.
   - **Fix (README post-run note, no re-grade).** Print a T scan (T = 20, 40, 80) of the largest zero eigenvalue for n=3, ε=4 to show it falls like 1/T toward 0.

4. **S5's tr R⁴ net of −16 needs the right reason.** Non-blocking; it's wording.
   - The −16 is correct and new (spec line 112 had it [open], item 1b-2).
   - It comes from all 16 6D Weyl components sitting at Γ₇ = −1 (MAIN content). It does not come from their 4D left-handedness.
   - S3, S6 and R6 have 4D right-handed singlets and the same −16. tr R⁴ is a 6D chirality count.
   - **Fix.** Use this wording in the wrap and in Part B.

5. **Part B's Q16 list is missing S5.** Fix this in Part B, not Part A.
   - JOB_SM1B_SPEC.md (now BE912C18) line 148 lists the consistency-gate rejects as S2, S3, S4, S6, R2 and R6. S5 (−16) is not there.
   - S5 is still rejected at Gate SM (line 138), so the outcome doesn't change.
   - **Fix.** Helios adds S5 to the line 148 Q16 list.
   - Q12 is untouched in Part A, which is right. R6 doesn't inherit the S3 tachyon: its rugby-ball Higgs spectrum is [open] (CANDIDATES line 270). R6 is a Q16 reject anyway.
   - Part B (not graded here) lists S6 under Q12 even though Higgs C is M²R² = +3. That only holds because the j = 2 tachyonic level of the same A_z field is present, and Part B should say so.

6. **Gaugino variant not applied per A9.** Report-only, cosmetic.
   - ANOMALIES line 313 gives ±13 without applying A9's "opposite chirality to the matter".
   - For MAIN content (matter at Γ₇ = −1) that means +13, so S3/S5/S6/R6 would go to −3 and S4 to −2. ALT has matter at both chiralities, so the sign there is ambiguous.
   - **Fix.** One line in post-run notes.

7. **Stale or inconsistent text.** Cosmetic.
   - (a) README line 7 says "Part B (1ADF2904)". Part B is now BE912C18.
   - (b) RESULTS line 7 says the FD grid is "N = … 2000 R family and B1". The graded B1 FD is the t grid (h = 0.01, T = 40), as README line 54 says.
   - (c) O-a cites Job Two RESULTS lines 139-144, but spec rule O-a says 137-144. These are the same rows, with header lines left out.
   - (d) Aethon's Hive wrap says "S5 and B1 fail" the SM 4D anomalies. B1 is n/a, with no SM content, and CANDIDATES line 400 already says so correctly.
   - **Fix.** README post-run notes and wrap wording only.

## Hive-equation-audit sweep
- **Dimensions:** clean. B1 uses R²·B on the unit θ sphere, consistently in both grids.
- **Signs:** hole 1. The E1 sign, the 4D chirality γ₅ = −Γ₇σ₃ and the descent orientation (−n) are consistent.
- **Code validity:** clean. Job Four's q global is restored in a `finally` block, and there is a hard stop on an unconverted n.
- **Types and shapes:** clean.
- **Placeholders:** Jackiw–Rossi wasn't run and the gaugino tr F⁴ wasn't expanded. Both are disclosed and optional.
- **Numerical stability:** hole 3 (Hardy-critical m = ½). Also, the bounded test sits exactly at p = 0 for m = ½ at α = 1, with tolerance −1e-6. It's fine (the computed value is −0.0), but marginal by construction.
- **Approximation presented as exact:** hole 2, where descent is asserted rather than computed.
- **Copy-paste:** hole 7.

## Claim tags and Akitti attributions
- **Tags.** [computed], [identity], [assumed] (the α grid), [standard] and [open] are used correctly.
- **GR.** None is used. D9 appears only as [GR control]. No Einstein equation appears.
- **Akitti attributions.** Only "the lift's gravity is unknown quantum gravity [Akitti]" (framework) and "Akitti's chosen model" for S1 (Job Two README line 234, a hive file). None of her numbers is used.
- **Provisional survivor classes** from post 2106801517357351243 (chiral spin-2 magnetoroton, lattice chiral edge modes, TT helicity ±2): they appear nowhere and are not graded.

## Blocking vs non-blocking
- **Blocking:** none.
- **Non-blocking, fix before the next run or in README post-run notes:** 1, 2, 3 (T scan).
- **Wording:** 4, 6, 7.
- **Part B spec:** 5.

## NOT COMPUTABLE here
- **The B1 n=3, ε=4 T scan on B0's actual background.** I didn't rebuild B0's background; my evidence is a synthetic profile. Aethon can run it from run.py's own functions.
- **The U1 113-sector cross-check.** I didn't recompute it. It is taken as cited from U1 RESULTS line 139.
- **Anything at α_ext.** There is no SM1_INPUTS.md. α_ext has to come from hive run files or her public posts, and none gives it today.

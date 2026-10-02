# Job B0: n vortices on a round sphere (Taubes base run for the Bradlow-cap line)

Folder: `C:\Users\Akitt\open-problems\Bradlow_cap\B0_taubes_base\`. Files: `run.py` (the whole job), `RESULTS.md` (written only by `run.py`), `README.md` (this file).
Spec: `..\JOB_B0_TAUBES_BASE_SPEC.md` (Helios; Venus PASS about 22:05 BST). Posted hash B5ABA965 = the **SHA-256 prefix** of the spec file (CRC32 is 9DE59B6C, which does not match). The spec was not edited. `run.py` hashes every file in `Bradlow_cap\` before and after the run and prints whether anything changed. B1, B2, B3 and B4 were **not** built.

Run (TrinityOrb, PowerShell): `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONDONTWRITEBYTECODE='1'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py`

## Model and normalisation (spec, locked at e = v = 1)
L = ½|Dφ|² + ¼F² + ⅛(|φ|² − 1)², BPS: (D₁ + iD₂)φ = 0, B = ½(1 − |φ|²); A_B = 4πn; R² = A/4π = n(1 + ε), ε = δ = (A − A_B)/A_B. Sphere vortices: Manton 1993, Nucl. Phys. B 400, 624 [standard; sphere source]; Bradlow 1990 and Manton–Nasir CMP 199 (1999) 591 for the bound A ≥ 4πn [standard].

## What run.py does
1. **Background [computed].** All n vortices at the north pole. h = log|φ|² = 2n log sin(θ/2) + u. The spec ODE (L17), u'' + cotθ u' = n − R² + R² sin^{2n}(θ/2) e^u, u'(0) = u'(π) = 0, is solved in the cylinder coordinate t = log tan(θ/2), where it reads u_tt = sech²t (n − R² + R² sin^{2n}(θ/2) e^u) (the L17 form times sin²θ; sympy identity printed). solve_bvp, tol 1e-10, t ∈ [−14, 14], u'(±14) = 0 [assumed]. Near the cap (ε ≤ 0.1) the start is Venus's constant u₀ = log[(n+1)(1 − A_B/A)]; ε = 1 and 4 are reached by continuation through ε = 0.1, 0.2, 0.5, 1, 2, 4 [assumed]. Venus's θ-form is also checked directly (finite-difference residual of L17 in θ).
2. **C1 [identity]:** ∫|φ|² = A − 4πn and E = πn, relative error < 1e-6.
3. **Profiles:** |φ|², B at five angles, max|φ|².
4. **C2 [standard: Wu–Yang; Haldane 1983]:** −D² for uniform B = n/(2R²), per angular sector m, finite differences in t; levels l = n/2 … n/2+3 compared with [l(l+1) − (n/2)²]/R² (tolerance 1e-3 [assumed]) and the states per level counted (2l+1). μ² = eB − ½ = ½(A_B/A − 1) printed and sympy-checked.
5. **Vortex fluctuations, per sector k = m − n [computed].** Second variation in background gauge. Writing P = D_tφ + iD_ϕφ and Q = F − (Ω²/2)(1 − |φ|²) (Ω = R sech t, the conformal factor), E − πn = ∫ ½|P|² + Q²/(2Ω²). The background-gauge Hessian is K = ∫ |δP|² + (δQ² + G²)/Ω², with G = div a − Ω² Im(φ̄η). With α = a_t + i a_ϕ, (δP, (G + iδQ)/Ω) is complex-linear in (η, α), so K is a sum of squares. In sector k, with η ∝ e^{i(n+k)ϕ} and α = iΩβ e^{ikϕ}, it becomes real: P = η' − (k + h'/2)η + Ωfβ, S = β' + (k − tanh t)β + Ωfη, K = ∫P² + S², M = ∫Ω²(η² + β²). ω² are the generalised eigenvalues of (K, M); each is one complex (two real) mode. Discretisation: staggered sum of squares, h = 0.01, t ∈ [−10, 10] (2001 nodes), Dirichlet unless the field is allowed to be non-zero at that pole (η at N iff n + k = 0, at S iff k = 0; β at N iff k = −1, at S iff k = 1). Lowest 6 eigenvalues per sector, k = −n−2 … 2. Zero mode means ω² < 1e-5 [assumed: discretisation leaves ~1e-8, the smallest physical gap is ~1e-2].
   - **"Remove the gauge zero mode":** in background gauge every pure-gauge direction gets ω² > 0 from the G² term, so there is no gauge zero mode left to remove. The constant gauge rotation (η = iφ) is the J-partner of the amplitude direction (η = φ), which is physical (G = 0) and is the P1 mode. All modes of the real k = 0 problem satisfy G = 0 exactly (η real, a_t = 0), so gap² is a physical eigenvalue. The run prints the overlap of the k = 0 mode with η = φ.
   - **C3 [standard: Manton–Sutcliffe ch. 7]:** exactly one zero mode in each of k = −n … −1, none elsewhere in the scanned window.
6. **P1 [prediction]:** ratio = gap²/δ. Straight-line fit over ε = 0.01, 0.02, 0.05; PASS if |intercept − 1| ≤ 0.03 for every n. The fitted slope is printed (Venus: leading order ratio = A_B/A, slope ≈ −1), with the 4-point near-cap slope and A_B/A beside each ratio. Resolution check of the ε = 0.01 gap at h = 0.005 [finite-size].
7. **P2** [computed by us from Baptista–Manton eq. (7) with all zeros at one pole; to check — tag as in the spec]: max|φ|²/(1 − A_B/A), with a linear extrapolation over the 3 smallest ε; print only.
8. **P3 [identity, print only]:** E_sym − E_vortex against (A − A_B)²/(8A); sympy shows (πn/2)(A_B/A + A/A_B) − πn = πn(A − A_B)²/(2A·A_B) = (A − A_B)²/(8A).
9. **Report only.** (a) Spread-out control: p vortices at N, n − p at S, (n, p) = (2,1), (3,1), (3,2), at the 3 smallest ε, same k = 0 gap and fit. Start u₀ = log[(1 − A_B/A)/B(p+1, n−p+1)], the same C1-normalised constant (B = Euler beta) [assumed]. (b) Far from the cap (ε = 1, 4): |φ|² against geodesic distance from the pole vs the plane n-vortex (plane ODE in log r, r ≤ 14).

Pass rule (spec, coded before the run): PASS = C1–C3 hold and P1 passes; PARTIAL = controls pass and P1 misses (job 02 then uses the measured gap); FAIL = a control fails.

## Choices and ambiguities resolved (executor)
- The spec gives no folder or file names, so I chose `B0_taubes_base\` with run.py / RESULTS.md / README.md.
- The hash check: CRC32 did not match; the SHA-256 prefix did.
- Coordinate t = log tan(θ/2) instead of θ (same ODE times sin²θ). It puts both poles at infinity, where the BCs u'(±T) = 0 are smooth.
- Background gauge removes gauge modes (see 5); nothing is projected out by hand.
- The continuation path for ε = 1, 4 and the spread-control start guess are not in the spec.
- Before the graded run, the solver was smoke-tested on the box (Linux) at a **non-graded** area ε = 0.3 only. It checked C1, C2 and the zero-mode counts in k ≠ 0; the k = 0 gap was not computed. Then TrinityOrb went offline (about 22:24 BST), and the parent agent allowed scratch runs on the box while waiting. I ran the **full** run.py there twice as non-graded scratch runs (Linux, Python 3 with numpy/scipy/sympy). They wrote to a scratch copy, never to this folder. So the P1 numbers were seen before the graded run. Between the scratch runs and the graded run, the only change to run.py was one printed sentence: the θ-form residual line now prints its finite-difference step, which it had said it would and did not. No threshold, parameter or numerical code changed. The graded run is the single run on TrinityOrb recorded in RESULTS.md.

## Tags
[computed] [identity] [standard] [assumed] [tuned] [post-hoc] [prediction] [finite-size], as used in RESULTS.md. Nothing in this job is [tuned].

## Refs (as in the spec)
- Manton, Nucl. Phys. B 400 (1993) 624 [sphere source, per Akitti's instruction; not re-read].
- Bradlow, CMP 135 (1990) 1. Manton–Nasir, CMP 199 (1999) 591, hep-th/9807017, eqs. (2.8)–(2.10).
- Baptista–Manton, J. Math. Phys. 44 (2003) 3495, hep-th/0208001: used only as the spec uses it (P2 via its eq. (7); the near-Bradlow CP^n picture behind the spread-out control).
- Taubes, CMP 72 (1980) 277. Manton–Sutcliffe, *Topological Solitons*, ch. 7. Haldane, PRL 51 (1983) 605. García Lara–Speight, arXiv:2210.00966 (not used).

## Post-run notes
- **Graded run:** one run on TrinityOrb, 22:33:34–22:33:56 BST, exit 0, no crash and no rerun. Runtime printed by the script: 20 s. Python 3.14.7, numpy 2.5.2, scipy 1.18.1, sympy 1.14.0. Spec hash re-checked just before the run: SHA-256 prefix B5ABA965. The audit shows that every file present in `Bradlow_cap\` when the run started was unchanged by it. Six PDFs (PRD/PRL papers) were added to `Bradlow_cap\` at 22:33:51–22:34:01 BST. They came from elsewhere (not this job), so they are not in the audit.
- **Comparison with the box scratch runs:** the graded RESULTS matches the box scratch run line for line, apart from the timestamp and runtime lines.
- **Grade by the fixed rule: PASS.** C1, C2 and C3 all pass. P1 intercepts are 0.999206 (n = 1), 0.998277 (n = 2) and 0.996034 (n = 3), all within 0.4% of 1 (the threshold is 3%).
- **P1 slope [computed; Venus to read]:** the 3-point slopes are −1.09 (n = 1), −1.60 (n = 2) and −2.34 (n = 3). The 4-point near-cap slopes are −1.04, −1.49 and −2.09. Venus expected about −1, which holds for n = 1 only. For n = 2 and 3 the ratio falls faster than A_B/A: ratio − A_B/A at ε = 0.01 is −1.6e-3, −7.5e-3 and −1.7e-2 for n = 1, 2, 3. So there is an O(ε) correction beyond the leading order that grows with n. It does not change the intercept or the grade. The overlap of the k = 0 mode with η = φ also falls with n (0.998, 0.992, 0.983 at ε = 0.01), which fits mixing with other LLL directions at next order [post-hoc reading, not a check].
- **Spread-out control (report only):** the intercepts are 0.9993 for (n, p) = (2, 1) and 0.9991 for (3, 1) and (3, 2), so the leading ratio matches P1 as Venus expected. The slopes do depend on the arrangement: −1.00 for (2, 1) against −1.60 with both vortices at one pole, and −1.21 for (3, 1) and (3, 2) against −2.34. So the arrangement-independence holds at leading order only [post-hoc]. As expected, (3, 1) and (3, 2) agree to every printed digit, since they are mirror images.
- **P2:** linear extrapolations are 1.9998, 2.9980 and 3.9935 against n + 1 = 2, 3, 4. **P3:** agrees to about 1e-11 at every area. **C1:** relative errors ≤ 5e-12.
- **Far from the cap (report only):** the largest |φ|² gap to the plane vortex over d ≤ 2 shrinks with R, from 0.20 to 0.06 (n = 1), 0.14 to 0.05 (n = 2) and 0.07 to 0.03 (n = 3) going from ε = 1 to ε = 4. That is the expected approach. Curvature corrections at R ≈ 1.4–3.9 are still visible.
- **Resolution check [finite-size]:** halving h changes the ε = 0.01 gap² by at most 3.2e-6 (relative).

## Sign-off
Venus (maths): 
Helios (physics): 

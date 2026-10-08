# SM1 Part A: Helios physics grade

Helios, 2026-10-08 (BST). This is the physics grade of Aethon's graded run of `JOB_SM1A_SPEC.md` (04B9AA05). Venus grades the maths separately. I edited no run file, spec or README on TrinityOrb, and I sent no messages.

Tags: [standard] textbook or published; [identity] follows by algebra; [computed] printed by the run (file and line given); [Helios check] my own independent computation on the box (scripts in `/workspace/lift/helios_sm1a_check/`); [open] not done. Missing values are labelled **NOT COMPUTED (YET)**, meaning not done yet or not recorded (Akitti's wording rule, 16:12). The run outputs say "absent" for missing inputs (RESULTS lines 63-79). Under the new rule those read as NOT COMPUTED (YET).

## Files graded (SHA-256, first 8 hex)

| file | expected | TrinityOrb (`open-problems\01_sm_from_sphere\SM1_filter\`) | box copy (`/workspace/lift/sm1a_results/`) |
|---|---|---|---|
| run.py | 803FD2DA | 803FD2DA | 803FD2DA |
| README.md | 12CEC48F | 12CEC48F | 12CEC48F |
| RESULTS.md | 7148A1DC | 7148A1DC | 7148A1DC |
| CANDIDATES.md | DAD867CE | DAD867CE | DAD867CE |
| OVERLAPS_ALPHA.md | D93AC9BD | D93AC9BD | D93AC9BD |
| ANOMALIES.md | B55D5D1F | B55D5D1F | B55D5D1F |
| JOB_SM1A_SPEC.md | 04B9AA05 | 04B9AA05 | 04B9AA05 |

All match. The box copies are byte-identical to TrinityOrb, and line numbers below refer to them.

My check scripts: `ov_check.py` DDE07B43, `tipexp_check.py` 0AA3D629, `hardy_check.py` A915495D, `hardy_check2.py` 4B52411B.

---

## (a) Hashes, and whether the outputs match Aethon's claims: **PASS-with-notes**

All six hashes match. Every graded claim matches the files:

| claim | file evidence | match |
|---|---|---|
| C-a 181/181 | RESULTS line 87; CANDIDATES lines 34-214 (181 rows, all YES) | yes |
| C-b R1/R2 = Job Four | CANDIDATES lines 224-227 | yes |
| C-c 34/34, three methods | CANDIDATES lines 235-268 (12 R3-R5 + 4 R6 + 18 B1) | yes |
| C-d Higgs 5 and 1; E4 N_Φ+1−2s at every α | CANDIDATES lines 345-346, 352-373 | yes |
| U1 113/113 | RESULTS line 91 | yes |
| A-a 15 S/R candidates | RESULTS line 94; ANOMALIES lines 32-270 | yes |
| A-b S1 0, S2 −1, S3 −16, S4 −15 | ANOMALIES line 26 | yes |
| tr R⁴ net table | ANOMALIES lines 9-24; RESULTS line 95 | yes |
| overlaps 112 per α; MAIN-A 2.8e-16 at α = 1 | OVERLAPS_ALPHA lines 11-40 (30) + 46-56 (11) + 62-132 (71) = 112; line 149 (2.776e-16, report-only) | yes |
| worst O-b 5.8e-14, O-c 8.6e-18, O-d 2.3e-14 | OVERLAPS_ALPHA line 151; RESULTS line 93 | yes |
| timing | RESULTS line 3 (generated 16:03:02 BST) + line 122 (187.0 s) = 16:06:09 BST, which equals the outputs' mtime on TrinityOrb | consistent |

Places where a number or wording disagrees (none changes a grade):
1. **"SM 4D anomalies cancel for 14 of 16 (S5 and B1 don't)."** The file says 14 cancel, S5 doesn't, and B1 is **n/a** because it has no SM charges (CANDIDATES line 400). B1 doesn't fail. It isn't assessed.
2. **"Tip flux δ = ¼ gives counts 2 vs 3."** That's true at α = 1, 4/5 and 3/5. At α = 1/2 the counts are **3 vs 3** (CANDIDATES lines 385-388). That's correct physics: at α = ½ the m = ½ north exponent (m − δ)/α − s = 0 sits on the bounded edge. Report-only.
3. **RESULTS line 7** says the FD grid is "2000 R family and B1". B1's graded FD is the t-grid (step 0.01 on [−40, 40]; README line 54; run.py lines 53-54). N = 2000 is only B1's report-only θ column. This is a wording slip.
4. **README line 7** cites Part B as 1ADF2904. That hash is stale (Part B has moved on), but it's harmless.
5. Aethon's θ-grid eigenvalue sequence 0.832 → 0.627 (N = 2000 → 32000) appears **only in chat**, not in any run file. I treat it as unverified, though it's consistent with my model (see (c)).
6. RESULTS line 103 lists `C:\Users\Akitt\sm-zero-modes-S2\__pycache__`. Its .pyc files are dated **2026-10-02 15:49** on TrinityOrb, so they predate this run. The run wrote no bytecode. Sources were 43/43 unchanged (RESULTS lines 59, 101).
7. Exit code 0 can't be verified from the files (there's no log). The outputs are complete and the timing is consistent.

## (b) Physics of the counts: **PASS-with-notes**

- **Dirac count = N_Φ** [standard: Atiyah–Singer on S², index = c₁ = (1/2π)∫F]. All modes sit in one 2D chirality slot because bulk curvature is positive (Lichnerowicz vanishing) [standard]. That holds on the rugby ball too, since its bulk curvature is still positive. Evidence: the "other slot 0" columns (CANDIDATES lines 50-214, 235-268) [computed].
- **Spin-weighted counts N_Φ + 1 − 2s** [identity]. I redid the algebra myself. For the E4 section, |ψ_s|² ~ θ^(2m/α − 2s) at the north tip and u^(2(N_Φ−m)/α − 2s) at the south tip, with m ∈ ℤ + s.
  - Bounded means m ≥ sα. Normalisable means m > α(s − 1).
  - For 0 < α ≤ 1 these select the same lattice points: m ≥ 0 (s = 0), m ≥ ½ (s = ½) and m ≥ 1 (s = 1), and the same at the south tip. So the counts are N_Φ + 1, N_Φ and N_Φ − 1 for every α ≤ 1. Matches CANDIDATES lines 354-373 [computed].
- **No α dependence for α ≤ 1** (A5) [identity, as above]. Physically, a bare deficit with no tip holonomy adds nothing to the index. The tip-exponent table (CANDIDATES lines 276-295) matches p_N = 2m/α − 1 and p_S = 2(N_Φ − m)/α − 1 to ≤ 1.05e-13. I checked one row by hand: n = 3, α = 3/5, m = 5/2 gives p_N = 7.3333 and p_S = 0.6667 (line 286).
- **Conventions N_Φ = 2|q|** [standard: Wu–Yang]. The scalar lowest Landau level has 2q + 1 = N_Φ + 1 states [standard]. The g = 2 spin-1 lowest level has 2q − 1 = N_Φ − 1 states [standard: Randjbar-Daemi–Salam–Strathdee; Nielsen–Olesen]. These are [identity] once converted, and the per-count table reproduces every source (CANDIDATES lines 328-346), including A_z 5 = N_Φ − 1 and ALT 1 = N_Φ + 1. The hard stop on an unconverted n fires (line 348).

Notes:
- **B1.** The B1 rows carry flux exactly n (CANDIDATES lines 305-322, "flux" column 1.0000000000 / 2.0… / 3.0…). So N_Φ = n is confirmed on B0's backgrounds, not just assumed.
- **N1: the s = 0 and s = 1 numbers are not protected zero modes.** They're lowest-level degeneracies. A scalar mass or potential lifts the N_Φ + 1 level as a whole, and the g = 2 spin-1 level is tachyonic in Job Two (S3's Higgs, M²R² = −3; spec line 110). Only the Dirac N_Φ is an index. Part B must not read the s = 0 or s = 1 counts as massless 4D fields.
- **N2: A5 covers only α ≤ 1.** The old lift's excess cone (α > 1) is outside A5, and there bounded and normalisable disagree, so a boundary condition is needed. NOT COMPUTED (YET) in Part A, correctly.

## (c) Disclosure 1 (B1's FD grid change): **PASS-with-notes. It's legitimate.**

**The physics is expected.** For m = ½ in the σ₃ = +1 slot at α = 1, with W ≈ m/θ near the pole, the potential is V = W² + W′ → (m² − m)/θ² = −1/(4θ²). That's exactly the Hardy-critical inverse-square potential (Bessel ν = 0). The zero mode goes as u ~ θ^½, i.e. |ψ|² ~ θ⁰, which is bounded and normalisable, so the mode itself is unambiguous. But Dirichlet FD at the critical constant converges only like 1/ln N [standard numerical behaviour at the Hardy constant].
- The same effect is already visible in Job Four's own α = 1 row. The largest FD zero eigenvalue is 0.1665 at α = 1, against 0.0537 at α = 4/5, 0.0032 at 3/5 and 0.0000 at 1/2 (CANDIDATES lines 224-227) [computed]. For α < 1, p_N = 2m/α − 1 > 0 moves m = ½ off the critical point.
- When B0's vortex flux concentrates at the north pole (large ε), the mode localises in the small core. The error then scales like 1/(ℓ² ln(ℓ/h)) in R²D² units, which is why only n = 3, ε = 4 failed on the θ grid (line 322, θ column "2, 0").

**[Helios check] model test.** This is not B0's background. It's a unit-charge Dirac fermion on the round unit sphere with flux 3 concentrated in a cap of size a at the north pole; the exact zero mode has eigenvalue 0.

| grid | a = 1 | a = 0.3 |
|---|---|---|
| θ, N = 2000 / 8000 / 32000 | λ = 0.2424 / 0.2099 / 0.1851 (λ·ln N = 1.84 → 1.92) | λ = 1.6535 / 1.4177 / 1.2402 (λ·ln N = 12.6 → 12.9) |
| t (h = 0.01), T = 10 / 20 / 40 / 80 | λ = 0.2394 / 0.1137 / 0.0554 / 0.0274 | λ = 1.6313 / 0.7446 / 0.3560 / 0.1742 |
| t, T = 40, h = 0.02 / 0.005 | 0.0555 / 0.0554 | 0.3561 / 0.3560 |

- The θ grid confirms λ ∝ 1/ln N, and a concentrated core makes it much worse.
- On the t grid, λ doesn't depend on the step h but does go like λ ∝ 1/T. The t grid doesn't remove the critical log. It moves the Dirichlet cut to θ ≈ 2e^(−T), so T = 40 acts like a θ grid with ln N ≈ 40. Aethon's chat claim that it "converges at ordinary speed" is right only for the step size. The residual is set by the end cut.
- This fits the run itself. Extrapolating Aethon's chat θ sequence as C/(ln N + c) predicts about 0.17 at the t-grid's effective cut, and the file prints 0.1821 for n = 3, ε = 4 (CANDIDATES line 322).

**It's a valid change of variables, not tuning.** I read run.py lines 831-862.
- With c = cosh t and dθ = dt/c, −d²/dθ² + V becomes the symmetric generalised problem A u = λ M u, where A = −(c u′)′ + V/c and M = diag(1/c).
- W = (m − A_φ)c and W′ = −R²B + (m − A_φ) tanh t · c², which is the exact transcription of the θ-form in lines 874-875 [identity; I checked it term by term].
- The eigenvalues are the same as for the θ operator, so the 0.5 threshold (line 41) means the same thing. The ends are still Dirichlet. The count uses Sylvester inertia of A − 0.5M (line 858).
- The pass rule and threshold are unchanged, and the θ column is kept.
- The spec doesn't fix B1's FD grid (spec line 186). The R family's FD "as in Job Four" (spec line 184) was not touched (run.py line 716).
- The count of 3 was fixed by the index theorem (A8) before any grid was chosen, and the regular and normalisable methods give 3 on their own.

Notes:
- **N3.** The real margin is 0.1821 vs 0.5 at n = 3, ε = 4. That's set by T = 40, not by h, and a more concentrated background could cross 0.5 again. If anyone wants a convergence table (Aethon offered one), it should be report-only and vary **T** (20, 40, 80, expecting λ·T roughly constant), not h or N.
- Disclosure 1 should read "its eigenvalue error falls like 1/ln N on the θ grid and like 1/T on the t grid". As written, the second part is missing (README line 40; CANDIDATES line 301).

## (d) Disclosure 2 (negative charge = conj(ψ_{−q,−s,−m})): **PASS-with-notes**

- Complex conjugation sends charge q → −q, spin weight s → −s and J_z eigenvalue m → −m [standard: conj(ₛY_jm) = (−1)^(m+s) ₋ₛY_j,−m; for Wu–Yang monopole harmonics, conj(Y_q,l,m) = (−1)^(q+m) Y_−q,l,−m]. So conj(ψ_{−q,−s,−m}) is a section with labels (q, s, m), which is the right object.
- The E4 form with q < 0 has no regular modes: it would need m ≥ sα and m ≤ 2q − sα < 0 at once [identity]. So conjugation is needed, not optional.
- Physically, negative-charge zero modes are antiholomorphic and live in the σ₃ = −1 slot. That matches R6's singlets in σ₃ = −1 (CANDIDATES lines 247-250, 270) and their mirrored tip exponents (lines 292-295) [computed].
- The radial factors are real, so conjugation only flips the φ phase. It commutes with the α deformation, and nothing new appears at α < 1.
- At α = 1 the convention is checked against Job Two's independent monopole harmonics, including the rows with negative charge (q₃ = −1). They agree to ≤ 2.2e-16 (OVERLAPS_ALPHA lines 142-147) [computed].
- **N4.** The (−1)^(…) phase is dropped and absorbed into a fitted unit constant (OVERLAPS_ALPHA line 138). Magnitudes are convention-free, but the **signs of overlaps involving a negative-charge section depend on the phase convention**. Part B may use only rephasing-invariant combinations of them (|C|, or invariants like Jarlskog).

## (e) tr R⁴ and the anomaly table: **PASS-with-notes**

**Are A-b's N₊ − N₋ and Part B's gate quantity different? No. They're the same quantity.**
- Both are the 6D Weyl-component count at Γ₇ = +1 minus the count at Γ₇ = −1, weighted by gauge dimension (spec line 214; ANOMALIES line 5). That's the coefficient of the irreducible tr R⁴ in I₈ [standard: Alvarez-Gaumé–Witten].
- A-b is the **graded reproduction** of that column for S1-S4 against Job Two's files (ANOMALIES line 26). The Part B gate applies the **same column** to all 16 rows (ANOMALIES lines 9-24; JOB_SM1B_SPEC line 137).
- What it is **not**:
  - the 4D chiral index of the zero modes (N_L − N_R, set by Γ₇ × σ₃ and N_Φ);
  - the 4D grav²Y sum;
  - the U(1)_X grav²X sum. For S3 that sum is 48 (CANDIDATES line 13), while tr R⁴ net is −16.
- tr R⁴ net is a property of the 6D Γ₇ assignment alone. It doesn't depend on flux, α or the number of generations, and it is checked by I₈'s r4 coefficients: −1/5760 (S2), −16/5760 = −1/360 (MAIN + ν^c), −15/5760 = −1/384 (S4) (ANOMALIES lines 287, 294, 301).
- **S1 vs S3 makes the difference clear.** They have identical 4D SM chirality and both cancel the 4D SM anomalies (CANDIDATES lines 11, 13). ALT gets right-handed singlets by flipping Γ₇, giving 8 vs 8 and a net of 0. MAIN keeps all 16 at Γ₇ = −1 and gets right-handed singlets from x = −1 (the σ₃ = −1 slot), giving 0 vs 16 and a net of −16.

**Consistency of the numbers.**
- S3 −16 and S4 −15 equal A-b exactly (ANOMALIES lines 11-12, 26).
- **S5 = −16** (line 13) is consistent. S5 is MAIN's fermions with every field at Γ₇ = −1, including ν^c (README line 31), so N₋ = 16. Only its 2D slot (x = +1) differs, which changes 4D chirality, not tr R⁴. Its 4D SM sums 2, 0, −4/3, 0, 12 (RESULTS line 88) are right for the content as labelled; I recomputed SU3²Y = 2, Y³ = −4/3 and SU3³ = 12 by hand. One caution: that holds with u, d, e kept as colour 3 with SM Y while left-handed. It's a build choice, not a hypercharge re-scan (README line 31).
- Gaugino ±13 = 8 + 3 + 1 + 1 adjoint Weyl fields (ANOMALIES line 313) [identity]. Report-only.

**N5: Part B's Q16 list is missing S5.** `JOB_SM1B_SPEC.md` (box copy BE912C18), lines 118 and 148, lists S2, S3, S4, S6, R2 and R6. The run gives **S5 −16** too (ANOMALIES line 13). The generic gate rule in line 137 would reject S5 anyway, but the explicit list should read S2, S3, S4, **S5**, S6, R2, R6. (S5 is also rejected at Gate SM, line 148.)

**N6: tr R⁴ is not the only irreducible term.** E2 (ANOMALIES line 276: "only tr R⁴ is irreducible") misses one. For SU(3) × U(1), **tr F³_SU(3) ∧ F_U(1)** can't appear in any X₄ ∧ X̃₄, because tr F³ is a 6-form. So Green–Schwarz can't cancel it [standard: 6D anomaly condition Σ x_R E_R = 0; Erler 1994].
- I recomputed the coefficients [Helios check, matches the files]:
  - ALT: 0 (line 280, no c3 term);
  - MAIN: c3·fY = −1/9 (lines 294, 301);
  - S5: c3·fY = −1/9 and c3·fX = −2/3 (line 308).
- No verdict changes, since every candidate carrying it (S3, S4, S5, S6, R6) already has tr R⁴ ≠ 0. But Part B's gate should test the tr R⁴ net **and** these c3·F_U(1) coefficients.

**N7: Gate assumptions to record in Part B.**
- The tr R⁴ requirement needs only 6D diffeomorphism invariance, not an Einstein equation, so it fits "the lift's gravity is unknown QG".
- It does assume that the unknown gravity sector adds **no chiral fields** (gravitino, (anti-)self-dual tensors), which would shift tr R⁴. The ANOMALIES line 5 caveat covers matter only.
- 6D global anomalies (π₆(SU(2)) = ℤ₁₂, π₆(SU(3)) = ℤ₆) [standard: Bershadsky–Vafa 1997] are NOT COMPUTED (YET) anywhere.

## (f) Overlaps' α dependence comes only from the tip exponents: **PASS**

- **[Helios check] direct θ-quadrature (mpmath)**, independent of the run's t-variable and Beta-function code. I checked 8 entries at all 4 α: rows 11, 46, 49, 63, 82, 97, 123 and 130. All agree with OVERLAPS_ALPHA to 12 digits, for example:
  - row 46 (MAIN-A) at α = 1/2: 0.590397503571;
  - row 82 at α = 4/5: 0.13671875;
  - row 123 at α = 3/5: 0.372166398909.
- **[identity, checked numerically]** In t = ln tan(θ/2), each E4 radial factor is e^(At)·sech^B(t), with A = (p_N − p_S)/4 and B = (p_N + p_S)/4. So it is fixed completely by the two tip exponents of |ψ|². I rebuilt rows 46, 82 and 130 at all 4 α from (p_N, p_S) alone on the α = 1 measure, times 1/√α, and reproduced the file values exactly.
- So C_α = α^(−½) × G(tip exponents). The only other α dependence is the area normalisation 1/√(4πα), which the Gram rows isolate: C·√α = 0.28209479 = 1/(2√π) at every α (lines 11-40).
- At α = 1 the table reproduces Job Two (lines 142-147).
- This holds **because the profile is the constant-curvature rugby ball, f(θ) = α sin θ**. For any other core shape it would not. See (g).

## (g) GR discipline: **PASS-with-notes**

- No Einstein equation is used anywhere. run.py mentions no tension, G or μ except the hash of the 5b folder name (line 133) and the disclaimer (line 161). The text says it outright (README line 7; RESULTS line 5).
- The one curvature statement is Gauss–Bonnet: ∫K dA = 4πα + 2·2π(1 − α) = 4π (ANOMALIES line 272) [identity]. That isn't GR.
- D9 and 5d are hashed but not imported (RESULTS lines 45-47, 83).
- B0's backgrounds are gauge-Higgs fields on a fixed round sphere.
- **N8.** OVERLAPS_ALPHA and the R-family tip exponents are computed on the **constant-curvature rugby profile**. That's the Salam–Sezgin/ABPQ shape, i.e. what 6D Einstein–Maxwell would give with tip tensions. α is tagged [assumed] (CANDIDATES line 5; README line 62), but the **shape** isn't labelled in OVERLAPS_ALPHA (lines 3-5).
- Part B must read OVERLAPS_ALPHA as overlaps on an assumed toy profile, or as a [GR control] shape, never as the core's own wavefunction overlaps. Per Venus, the core shape stays "[open: f(θ) from hive runs]", i.e. NOT COMPUTED (YET). The counts are unaffected, because they don't depend on f.

## (h) Nothing presented as a survivor: **PASS-with-notes (one required fix)**

- Part A uses no inputs. Every `SM1_INPUTS.md` field is "absent" (RESULTS lines 63-77), which under the new rule reads NOT COMPUTED (YET). The run is grid-only (line 79), and nothing is scored against ∫R dA, ∫T_tt dA or the MHD trace.
- **Breach: CANDIDATES line 400** is headed **"Survivor counts (information only; Part A applies no gate)"**. It lists which rows have tr R⁴ = 0 and which cancel the 4D anomalies.
  - It's labelled no-gate and scores nothing against her integrals, so I don't fail the run.
  - But it is presented as survivors, and it anticipates Part B's gates.
  - **Required before my sign-off:** a README Post-run note saying that line 400 is a tally of Part A properties, not a survivor list, and that no candidate survives or is selected in Part A. The string in run.py should also be reworded at the next (α_ext) re-run. Output files must not be hand-edited, and no re-run is needed now.
- "Hypercharge scan survivors" (CANDIDATES lines 47, 68, …, 216) is Job Two's term for hypercharge assignments that pass its anomaly scan, not candidate survival. That's acceptable.

---

## Overall verdict: **PASS-with-notes (physics)**

The build PASS is confirmed: every graded number matches its file, and my independent overlap and anomaly-coefficient checks agree. The counts are physically right: Dirac N_Φ [standard], N_Φ + 1 − 2s [identity] and α-independence for α ≤ 1 [identity]. Disclosure 1 is legitimate: the slow convergence is the expected Hardy-critical effect, and the t-grid is an exact change of variables. Disclosure 2 is consistent with charge conjugation. No GR is used as the core's gravity.

**Required before the Helios sign-off line is filled:** N-h, a README Post-run note on CANDIDATES line 400 ("Survivor counts" is not a survivor list).

**Carry into Part B (none changes a Part A grade):**
- N5: add S5 (−16) to the explicit Q16 list.
- N6: also gate on the tr F³_SU(3)·F_U(1) coefficients.
- N7: state the no-chiral-gravity-sector assumption. 6D global anomalies are NOT COMPUTED (YET).
- N8: OVERLAPS_ALPHA is on the assumed constant-curvature profile, not the core. f(θ) from hive runs is NOT COMPUTED (YET).
- N4: use only phase-invariant overlap combinations.
- N1: the s = 0 and s = 1 counts are level degeneracies, not protected massless modes.
- N2: α > 1 is outside A5.
- N3: any B1 convergence check should vary T, not h or N, and is report-only.

Wording fixes, optional and needing no re-run: (a)1 and (a)2 (Aethon's chat summary), (a)3 (RESULTS line 7), (a)4 (README line 7), and the 1/T wording in disclosure 1.

Helios (physics): PASS-with-notes, to be signed once the N-h Post-run note exists.

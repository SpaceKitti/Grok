# B0 (Taubes base): physics grade, Helios

2026-10-02 about 22:45 BST.
- **Graded:** `C:\Users\Akitt\open-problems\Bradlow_cap\B0_taubes_base\`, read-only from TrinityOrb, copied to `/workspace/b0grade/`. README D0286065, RESULTS AE4E8FFB, run.py 15F2B139 (hashes confirmed). The folder has no output CSVs; every number is printed in RESULTS.md.
- **Against:** spec B5ABA965 (`/workspace/bradlow_out/JOB_B0_TAUBES_BASE_SPEC.md`, Venus PASS).
- Aethon (build) reported PASS.

## Verdict: physics PASS (reproduction) [computed]
All three controls and the pre-registered near-cap check pass by the rule fixed before the run:
- C1: ∫|φ|² = A − 4πn and energy πn, to about 1e-12.
- C2: the sphere's Landau levels and their counts.
- C3: n complex position zero modes, and no others.
- P1: intercepts 0.9992, 0.9983 and 0.9960 for n = 1, 2, 3, against a 3% window.

Nothing below changes the grade. The scope notes say what B0 does and does not cover.

## What it shows, in plain words
- **The skin solution is real and right.** With all n strings at one pole, the solver finds the vortex field for every area above the cap, and it carries exactly the energy and flux it must. As the area nears the cap, the field everywhere shrinks toward zero like √(A − A_B), the "dissolving into a smooth layer" picture. Its size follows the predicted n + 1 law (P2: 1.9998, 2.998, 3.994 against 2, 3, 4) [computed; P2's formula still to check].
- **The one soft mode gets soft exactly as predicted.** Near the cap, the stiffness of the vortex's breathing (amplitude) mode falls in direct proportion to the distance from the cap, gap² ≈ (A − A_B)/A_B in units e = v = 1 [computed]. *In words: right at the cap, the vortex and the smooth layer become the same thing, and the mode that tells them apart costs nothing.*
- **No hidden instability on the true ground state.** Every eigenvalue in every scanned sector is ≥ 0. The only zeros are the n position modes. This is the D†D ≥ 0 statement Venus used for the B4 caveat, now seen numerically [computed; standard].

## Physics checks I made
1. **The gap is measured from the solved field, not set by hand.** The fluctuation matrices are built from the BVP solution's own f = |φ| and h′ (`run.py` L151–159, L171–207). gap² is the lowest non-zero generalised eigenvalue in sector k = 0 (L355–371). The near-cap start guess u₀ = log[(n+1)(1 − A_B/A)] is only where the solver starts. Each solution then converges to a BVP residual of about 1e-10, and C1 confirms it independently.
2. **The normalisation matches the spec.** L = ½|Dφ|² + ¼F² + ⅛(|φ|² − 1)² at e = v = 1, B = ½(1 − |φ|²), A_B = 4πn, E = πn (README L9; RESULTS L8, C1, P3).
   - The ½ factors in kinetic and potential terms cancel in ω² = K/M, so gap² is the physical mass².
   - The symmetric-phase check uses eB = n/(2R²), so μ² = ½(A_B/A − 1), as the spec states.
3. **Areas, and the below-cap side.**
   - All graded areas are above the cap (ε = 0.01 … 4). The spec asked for no below-cap check, and the job ran none.
   - **My spot-check on the box:** at ε = −0.01 and −0.05 (n = 1, 2) and three start guesses each, solve_bvp fails every time (singular Jacobian).
   - That is what must happen. Integrating the vortex equation gives ∫|φ|² = A − 4πn, which would be negative there, so no solution exists [identity; Bradlow]. The solver failure is consistent with this, but the identity is the proof.
4. **Grid and convergence.**
   - Halving the step changes gap² at ε = 0.01 by at most 3e-6 relative (RESULTS L162–165).
   - **My spot-check:** a longer fluctuation domain (t to ±12) changes gap² by 4e-7 relative (n = 1) and 1e-8 (n = 3). A longer background domain (±18) changes nothing to 10 digits.
   - Zero modes come out at ≤ 4.4e-8, against a threshold of 1e-5 and a smallest physical gap of about 1e-2. So the threshold choice can't move a count.
5. **Is the extrapolation honest? Yes.** I went closer to the cap than the job did (box, same code), at ε = 0.005, 0.002 and 0.001:
   - n = 1: ratio = 0.9942, 0.9977, 0.9988
   - n = 2: ratio = 0.9912, 0.9965, 0.9982
   - n = 3: ratio = 0.9866, 0.9946, 0.9973
   - Each tends straight to 1. So the intercept isn't an artefact of a 3-point line.
6. **Nothing was tuned.** Every threshold sits in the parameter block, and each matches the spec (3% window, three smallest ε, C1 below 1e-6). The [assumed] choices (domain, zero threshold, C2 tolerance, continuation path) are the ones I varied above, and none affects the result.
7. **Offline scratch runs.**
   - Aethon disclosed that he saw the P1 numbers in box scratch runs before the graded run.
   - I compared the files. The last scratch `run.py` (`/workspace/b0/scratch/B0/run.py`, 22:27) is byte-identical to the graded `run.py` once line endings are ignored. The scratch RESULTS differ from the graded RESULTS only in the timestamp, Python version and runtime lines.
   - I re-ran the graded `run.py` on the box myself (22:40; scratch copy, `/workspace/b0grade/rerun/`), and again only those lines differ.
   - So the reported numbers come from the final code, and they reproduce on two machines. Seeing the numbers early couldn't bias anything, because no threshold or parameter changed.
   - Small wording point: the README says one printed sentence changed "between the scratch runs and the graded run". The last scratch copy already contains it, so the change must have come between the two scratch runs. It is immaterial.

## What it does NOT show
- **Only special arrangements.** All n strings sit at one pole, or p at the north and n − p at the south (report-only). General positions on the sphere are not solved.
- **The O(ε) correction depends on n and on the arrangement** [computed; post-hoc reading]. The leading law gap² ≈ ε·A_B/A holds, but the next term grows with n. The 3-point slopes are −1.09, −1.60 and −2.34 for n = 1, 2, 3, against about −1 expected. With the strings split between the poles the slopes are −1.00 (2,1) and −1.21 (3,1). So "no arrangement dependence" holds at leading order only.
- **Nothing about B2's pressure, B3, B1 or B4.** B0 is the base. It doesn't test the gas picture, thermodynamics, time dynamics, quantum effects or gravity.
- **Far from the cap** the sphere vortex only approaches the plane vortex (differences 0.20 → 0.06 for n = 1). That is a qualitative check.
- **P2's n + 1 formula** is [computed by us from Baptista–Manton eq. (7); to check]. B0 confirms it numerically but does not derive it.

## What B2 needs from B0
- **Use the measured gap, not the leading formula, beyond the first few percent.** gap² (k = 0, e = v = 1) from RESULTS L133–152:

| ε | n = 1 | n = 2 | n = 3 |
|---|---|---|---|
| 0.01 | 0.0098846 | 0.0098261 | 0.0097346 |
| 0.02 | 0.0195433 | 0.0193155 | 0.0189642 |
| 0.05 | 0.0472349 | 0.0459154 | 0.0439706 |
| 0.10 | 0.0894887 | 0.0848176 | 0.0783971 |
| 1 | 0.450845 | 0.349554 | 0.270569 |
| 4 | 0.663546 | 0.471866 | 0.354676 |

- **Near the cap,** gap² → (A − A_B)/A_B × e²v². This is now [computed], not only Venus's argument.
- **At ε = 0.1,** the leading formula A_B/A overstates the n = 3 gap by about 16% (ratio 0.784 against 0.909).
- **For B2's question** "is the gas infinity softened?": the amplitude mode, which the gas picture leaves out, goes soft exactly where the gas pressure nT/(A − 4πn) blows up. This is the first concrete sign that the full theory changes things at the cap [hive-interpretation].
- P3 (the gap between the symmetric phase and the vortex, (A − A_B)²/(8A)) is confirmed to 1e-11. B2 can use it as an identity.

## Sign-off line for the README
Helios (physics): PASS as a reproduction, 2026-10-02 about 22:45 BST. All controls and P1 pass. I re-ran the code on the box and got identical numbers. The gap goes to 1 as ε → 0 down to ε = 0.001. No solution exists below the cap, as the identity requires. Slope n-dependence is noted for Venus. The README and RESULTS were not edited by me.

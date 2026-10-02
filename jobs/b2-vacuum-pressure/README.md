# Job B2: does the vortex-gas pressure really blow up at the Bradlow cap? (folder 02, vacuum)

Folder: `C:\Users\Akitt\open-problems\Bradlow_cap\02_vacuum\`. Files: `run.py` (the whole job), `RESULTS.md` (written only by `run.py`), `README.md` (this file).
Spec: `..\JOB_B2_VACUUM_PRESSURE_SPEC.md` (Helios; cleared by Venus; GitHub main 07c9d97). Posted hash 3A069F08 = the SHA-256 prefix (CRC32 is D6529F00). The spec was not edited. L19 (Helios/Venus, tag-only fix after the run): The factor of 2 between M22's total curvature and the scaled-FS value is exact for every N on the sphere (M22 eq. (14), g = 0). The 2 + 2/N in RESULTS A1 comes from comparing with M22's large-N form (15), which run.py labels 'eq. (15) at g = 0'. [identity; tag-only fix]
Input: `..\B0_taubes_base\RESULTS.md` (SHA-256 prefix AE4E8FFB, checked by run.py, which stops on a mismatch). It is read-only, and its hash is re-checked after the run.

Run (TrinityOrb, PowerShell): `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONDONTWRITEBYTECODE='1'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py`

**A PASS here reproduces known results. It is not evidence for Akitti's link.** The spec says the grade is "PASS by construction (reproduction + scale ordering)": ΔE ~ ε², so T/ΔE must cross 1 before the cap, and P_MW → 0 is MW's own result. The new information is ε*(T), which breakdown scale comes first, and the finite pressure P(ε*) where the gas description ends.

## Convention
H = ½ħ²Δ on the moduli space (MW eq. (4) = M22 eq. (6)). Dissolving-limit metric g = (A − 4πN)·G_FS on CP^N (MW eq. (2)). e = v = 1, A_B = 4πN, ε = A/A_B − 1. N = 1, 2, 3.

## What run.py does
**Stage A, controls**
- **A1 [identity; sympy]:**
  - MN (3.23) → (4.7): Vol = (A − 4πN)^N/N! gives P = NT/(A − 4πN) exactly on the sphere.
  - M22 (16) → (19) → (20): the algebra is reproduced with M22's printed coefficient. That is c = 1/12 in MW's z. It is labelled **"misprinted, for reference" (MW fn. 1)** and is never used as a cross-check.
  - The corrected coefficient comes from the scaled Fubini–Study heat kernel: (t/6)R with t = ħ²/2T and R = 4N(N+1)/(A − 4πN) gives c = (N+1)/(6N). The plain-unit form 2cħ²N²/(A − 4πN)² is checked too.
  - The spec's "where the 2 sits" ratio R·Vol / M22 (15) = 2(N+1)/N → 2.
- **A2 [computed]:**
  - The exact MW sum is Z = Σ_{k≥0} g_k e^{−zk(1+k/N)}, with MW (5)–(7), the ground state k = 0 included, and up to 2·10⁵ terms (the tail weight is printed).
  - The reduced pressure is P̃ = P/(NT/(A − 4πN)) = (z/N)⟨k(1 + k/N)⟩.
  - The small-z slope c comes from a quadratic fit of (1 − P̃)/z over z = 1e-4…1e-2. It must be within 1e-3 (relative) of (N+1)/(6N) for N = 1, 2, 3.
  - The large-N trend toward 1/6 is shown for N = 10, 100 and 1000.
- **A3 [computed]:**
  - The exact sum at N = 10⁵ (MW's figure value) is compared with MW eq. (36) in its three regimes (z = 0.25…2 high, 8–16 intermediate, 30 and 35 low).
  - Criterion [assumed]: the error must be at most |last retained term| + (3+z)/N·|leading| + z/(4N). The last piece is MW's own finite-N crossover term, eq. (34).

**Stage B, B0's area ladder** (ε = 0.01, 0.02, 0.05, 0.1, 1, 4), with T ∈ {0.01, 0.1, 1} and ħ ∈ {0.1, 1}. Columns:
- P_class and P_MW (the exact sum). P_MW is printed via logs, so the values far below 1e-300 at low T stay finite.
- z.
- m_gap² **measured in B0**, beside Venus's ε = e²v²(A − A_B)/A_B, labelled "leading order, reference".
- ΔE = (A − A_B)²/(8A), and m_gap²(A − A_B)/(8ΔE).
- T/ΔE (classical validity).
- ħm_gap/ΔE (quantum validity), from the B0 gap, with the leading-order version beside it as reference.
- T/(ħm_gap) (report only).
- (ħ²λ₁/2)/(ħm_gap), the moduli step (quantum gas only).

**ε*(T)**
- ε*(T) is the first ladder area, going from ε = 4 toward the cap, where the governing column is ≥ 1.
- The governing column is T/ΔE if T ≥ ħm_gap, else ħm_gap/ΔE. That is the spec's "T/(ħm_gap) says which applies".
- Each scale also gets its own ladder ε* and a log-log interpolated ε* [assumed]. "Breaks first" is the scale with the largest ε*.
- P(ε*) is P_class for the classical gas and P_MW for the quantum gas, with both printed.

**Stage C, report only**
- The classical melting point is solved exactly: A* − A_B = 4T + √(16T² + 8TA_B).
- Leading estimate: P(ε*) = N√(T/8A*), which is exact at A*. The version with A_B in place of A* is also printed.
- Torus: P = (N−1)T/(A − 4πN) + T/A, from MN (3.24). Shah–Manton was not read.

**Pass rule** (coded before the graded run):
- PASS if Stage A reproduces (including the c = (N+1)/6N slope) and B0's P1 passed.
- PARTIAL if B0's P1 was PARTIAL.
- FAIL if Stage A fails.

run.py reads B0's grade and P1 lines from B0's RESULTS.

## Gap source (Venus 22:38)
The gaps are **read from B0's RESULTS.md** (P1 table, gap² to 8 decimals). B0's solver was not imported or rerun, and B0's files are untouched.
- Per Venus at 22:38, every quantum column (ħm_gap/ΔE, T/(ħm_gap), and the moduli-step ratio) uses B0's **measured** gap.
- The measured gap carries the n-dependent correction B0 found: slopes −1.09, −1.60 and −2.34 for n = 1, 2, 3. Venus attributes it to sextic/higher-Landau-level mixing.
- The leading-order formula gap² = ε appears only in columns labelled "leading order, reference".
- B0's gap is for all N vortices at one pole. The gas averages over arrangements, and B0's spread-out control matched only at leading order. So the ε-dependence of the gap columns away from the cap is for the coincident configuration [assumed].

## Caveats
- Manton–Wang keep only the moduli and never compute the amplitude gap. So the gap columns (ħm_gap/ΔE, T/(ħm_gap), moduli step vs gap) **cannot be checked against MW directly**.
- Baptista–Manton warn that the validity proof of the moduli approximation "does not extend automatically" to this regime.
- P_MW uses the dissolving-limit (Fubini–Study) metric. That is MW's model for ε ≪ 1 only; at ε = 1 and 4 it is an extrapolation [assumed].
- The ladder is coarse (six areas), so ladder ε* values often tie. The interpolated ε* separates them [assumed]. The classical one is cross-checked against the exact root. Log-log interpolation is within about 7% of exact crossings and errs high in the 0.1–1 bracket [computed, Helios check].

## Choices and ambiguities resolved (executor)
- **Folder name:** the spec says "folder 02, vacuum", so I used `02_vacuum\`.
- **k = 0:** included in MW's sum (the ground state, g₀ = 1). MW write "k ∈ Z+", but their low-T series (26)/(30) begins with the k = 0 term 1, so the ground state is in their sum.
- **P = T∂lnZ/∂A:** depends on A only through z (MW (21)–(22)).
- **"Governing column":** read as max(T, ħm_gap)/ΔE, per T/(ħm_gap).
- **"Crosses 1":** a column ≥ 1 at a ladder area. All three columns are monotone along the ladder (run.py checks this). Crossing 1 is an order-of-magnitude marker (energies, not free energies) [assumed].
- **Scratch runs (disclosed):** I ran the full run.py several times on the box (Linux, Python 3) as non-graded scratch runs. They used a scratch copy of the spec and of B0's graded RESULTS, never this folder. Changes made after scratch runs:
  1. The A3 criterion first lacked the z/(4N) term, and z = 16 failed by 4e-5. That is exactly MW's eq. (34) finite-N term, so I added it. z/(4N) added after the z = 16 scratch miss [post-hoc]; independently confirmed by N-scaling of the residual (Venus) [computed].
  2. The torus sympy line was fixed; it did not simplify.
  3. The leading-estimate table now uses A_B; with A* it was trivially exact.
  4. The grade line wording was fixed.
  5. Interpolated ε* columns were added.

  No threshold changed after the code was frozen for the graded run.

## Tags
[computed] [identity] [standard] [assumed] [post-hoc] [prediction] [finite-size] [hive-interpretation], as used in RESULTS.md and this README. Nothing is [tuned].

## Refs (as in the spec)
- Manton, NPB 400 (1993) 624 (original sphere volume; not read).
- Manton–Nasir, hep-th/9807017, eqs. (2.10), (3.23), (3.24), (4.7).
- Manton, arXiv:2204.01389 (J. Phys. A 55 (2022) 325001), eqs. (6), (15), (16), (19), (20); its 1/12 is superseded by MW fn. 1.
- Manton–Wang, arXiv:2212.06016, eqs. (2), (4)–(7), (21)–(22), (25), (34), (36) and fn. 1. The text was re-read from the arXiv PDF for this build.
- Baptista–Manton, hep-th/0208001.
- Shah–Manton, JMP 35 (1994) 1171 (not read).

## Post-run notes
- **Graded run:** one run on TrinityOrb, 22:44:21–22:44:42 BST, exit 0, with no crash and no rerun. Runtime printed by the script: 19 s. Spec hash 3A069F08 and B0 RESULTS hash AE4E8FFB were both re-checked just before the run and by run.py. All 18 audited files (top-level `Bradlow_cap\` files plus B0's folder) were unchanged by the run.
- **Comparison with the box scratch run:** the graded RESULTS matches the last scratch run line for line, apart from the header, runtime and audit-count lines.
- **Grade by the fixed rule: PASS.** This is PASS by construction (reproduction + scale ordering). It reproduces known results and is **not** evidence for Akitti's link.
  - A1: every sympy residual is 0.
  - A2: c fitted = 0.3333333334, 0.2499999999 and 0.2222222222 for N = 1, 2, 3 (relative error ≤ 4e-10). The trend is 6c = 1.1, 1.01 and 1.001 at N = 10, 100, 1000 → MW's 1/6.
  - A3: all 9 test points are within the allowance.
  - B0 P1: PASS.
- **Measured gap (Venus 22:38):** every gap column uses B0's measured gap² from B0's RESULTS (read, not recomputed). Venus ruled that the n-dependent correction B0 found (P1 slopes −1.09, −1.60 and −2.34; sextic/higher-Landau-level mixing) is real, so the quantum columns should carry it. The leading-order gap² = ε is printed only in columns labelled "leading order, reference". Near the cap the two agree to within the B0 ratio: m_gap²(A − A_B)/(8ΔE) = 0.998, 0.992 and 0.983 at ε = 0.01 for N = 1, 2, 3. Away from the cap the measured gap lies far below the leading formula (e.g. gap² = 0.355 against ε = 4 at N = 3, ε = 4), and m_gap²(A − A_B)/(8ΔE) falls to 0.83, 0.59 and 0.44 at ε = 4.
- **Gap table used (parent / Helios, 22:45):** the graded run used **B0's RESULTS.md** (`..\B0_taubes_base\RESULTS.md`, SHA-256 prefix AE4E8FFB, CRC32 B5DA1D2C), from the P1 table at 8 decimals. Helios's B0 physics grade, `..\B0_taubes_base\B0_GRADE_HELIOS.md` (SHA-256 prefix E58EFC2F, 22:43:40 BST), has a measured gap table that is the same data rounded to 6–7 significant figures. I checked it against B0's RESULTS after the run, outside run.py: all 18 entries agree to within 4.0e-6 relative, which is only rounding. So using Helios's table instead would change nothing at the printed precision. Neither file was edited; both are in run.py's before/after audit, since Helios's file was already there when the run started. Helios notes that the leading formula is too high at ε = 0.1 for n = 3. In the A_B/A form it is 0.0909 against the measured 0.0784, about 16% high. The spec's ε form used in this job's reference column gives 0.1, about 28% high. So the leading formula appears only as the column labelled "leading order, reference".
- **ε*(T) and which scale breaks first [computed; interpolated values assumed]:**
  - At **T = 1** classical melting breaks first for every N and ħ. The exact ε* is 1.18, 0.75 and 0.58 for N = 1, 2, 3.
  - At **T = 0.01** the quantum scales break first: the quantum gap for N = 1 and 2, the moduli step for N = 3. Ladder ε* is 0.1 (0.05 for N = 3, ħ = 0.1). The interpolated quantum-gap ε* is 0.17, 0.10 and 0.076 at ħ = 0.1, and 0.89, 0.51 and 0.36 at ħ = 1. The classical crossing would only come at 0.083, 0.058 and 0.047.
  - At **T = 0.1** it depends on ħ: classical melting first at ħ = 0.1; the quantum gap (N = 1, 2) or the moduli step (N = 3) first at ħ = 1.
  - At leading order the quantum-gap and moduli-step columns tie exactly for N = 3 (ratio 4/(N+1)). 'Moduli step first' depends on the stacked-configuration gap [assumed]. (Helios grade, B2_GRADE_HELIOS.md.) So read N = 3 where quantum scales govern as "quantum gap and moduli step break together, within the arrangement uncertainty", not as a clear winner.
- **P(ε*) [computed]:**
  - The classical gas ends at a finite pressure, P(ε*) = N√(T/8A*) exactly. That is 9.6e-3, 1.4e-2 and 1.7e-2 at T = 0.01 and 6.8e-2, 0.107 and 0.137 at T = 1, for N = 1, 2, 3. The leading A_B version, N√(T/8A_B), exceeds the exact value by 2% (N = 3, T = 0.01) up to 48% (N = 1, T = 1).
  - Where the quantum gas governs, it is frozen at ε*: P_MW ≪ P_class, e.g. 4.4e-138 against 8.0e-3 at N = 1, T = 0.01, ħ = 1.
  - So on both routes the gas-picture divergence NT/(A − 4πN) is never reached inside the gas's own validity range. This agrees with the spec's prediction, by construction.
- **Interpretation [hive-interpretation]:** the cap blow-up of NT/(A − 4πN) marks where the string/gas description breaks down, not a physical infinity; it is never reached inside the gas picture's validity. **B2 is not evidence for Akitti's link.**
- **Caveat repeated:** the gap columns cannot be checked against Manton–Wang, who never compute the amplitude gap.
- README wording/tag fixes per B2_GRADE_HELIOS.md (7C120916) items 1–6 and sign-offs added about 23:07 BST; no numbers or code changed.

## Sign-off
Venus (maths): PASS, 2026-10-02 about 22:52 BST. A1–A3 reproduce MW/MN/heat-kernel identities; the z/(4N) allowance is MW (34)'s finite-N term, confirmed by N-scaling (N = 10⁴–10⁷); gap columns use B0's measured gaps; reproduction only.
Helios (physics): PASS (reproduction + scale ordering), 2026-10-02 about 23:05 BST. I re-ran run.py on the box and got identical RESULTS. The measured B0 gaps, c = (N+1)/6N and B0's normalisation are all used correctly. The z/(4N) allowance is MW eq. (34)'s finite-N term [post-hoc, confirmed]. The N = 3 low-T ordering is a leading-order tie, decided by the stacked-gap assumption. The gas breaks down at finite pressure before the blow-up. The README and RESULTS were not edited by me.

# Job U1: strings on the fuzzy sphere (`u1-fuzzy-sphere-strings`)

Folder: `C:\Users\Akitt\open-problems\U1_fuzzy_sphere_strings\` (TrinityOrb). Files: `run.py`, `RESULTS.md` (written only
by `run.py`), this README, and the two reference PDFs filed by Orion. No git is used here; Ledger pushes.

Run: `$env:PYTHONIOENCODING='utf-8'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py` (a couple of minutes, dense eigensolves of dimension ≤ ~1000, no time-stepping).

This README quotes no computed numbers. Every result is printed from variables in `RESULTS.md`. The only numbers here are inputs,
thresholds and formulas.

## Question (Helios's spec)

On the fuzzy sphere, does the number of zero modes equal the number of strings n? And do the levels drift once n crowds the
resolution N?

- N = 2L+1 is the matrix size of the base fuzzy sphere. Venus reads it as the brane count / resolution.
- n is the number of strings, i.e. the monopole charge.

## Sources

- Helios's spec, with Venus's notes and additions (relayed by NanoRibbon; Helios agreed to Venus's additions).
- The folder did not exist and had no PDFs. Both papers were read from arXiv on the agent box: Aoki–Iso–Nagao
  hep-th/0312199v2 (AIN) and Grosse–Klimčík–Prešnajder hep-th/9510083v2 (GKP).
- No PDF was copied into this folder by `run.py` or by me. Orion has since filed both PDFs here (see the "Filed PDF:" lines in References).

## Construction (AIN as written; for Venus to check against the paper)

**Base fuzzy sphere.** x_i = α L_i, with L_i spin L, (2L+1)-dimensional (AIN 2.1). Wave functions are matrices. L^L and L^R
are the left and right actions (2.5).

**Operators** (AIN §2.2):

- a = 1/(L + 1/2) (2.18).
- Γ^R = a(σ·L^R − 1/2) (2.16).
- H = a(σ·A + 1/2) (2.19), with A_i = L_i + ρa_i acting from the left (2.11).
- Γ̂ = H/√H² (2.17).
- D_GW = −a⁻¹ Γ^R (1 − Γ^R Γ̂) (2.23).
- The GW relation Γ^R D_GW + D_GW Γ̂ = 0 (2.27) holds.
- Index = (n₊ − n₋) = ½ Tr(Γ^R + Γ̂) (2.28).
- Identity used [identity]: because (Γ^R)² = 1, D_GW = a⁻¹(Γ̂ − Γ^R), so D_GW is Hermitian. `run.py` checks this.

**Charge-n sector as a projective module.** AIN §3.3 eqs. 3.40–3.43 take a_i = (1/ρ) 1 ⊗ T_i with isospin T. Then
A_i = L_i ⊗ 1 + 1 ⊗ T_i satisfies su(2) and splits into blocks L^(a) = L + T + 1 − a. The projector P^(a) (3.43) picks one block.
Its topological charge is ½ Tr P^(a)(Γ^R + Γ̂) = 2(L − L^(a)) (3.37).

- The charge-n sector is the block L' = L − n/2, taking T = n/2 and the lowest block.
- On that block Γ̂ = (σ·L' + 1/2)/(L' + 1/2) (3.30).
- Fermions there are spinor-valued (2L'+1)×(2L+1) matrices: A acts from the left as spin L', and L acts from the right as spin L.
- This is GKP's space Ĥ_MN of (M+1)×(N+1) matrices with winding κ = M − N (GKP eqs. 41, 44 and the conclusion), with M = 2L' and GKP's N = 2L.

**Two checks that this is the paper's operator** [computed]:

1. The reduced block is cross-checked against the literal construction at small N. The literal version uses the full V_L ⊗ V_T
   space, Γ̂ by eigendecomposition, P^(a) from (3.43), and D_GW from (2.23) restricted to the range of P^(a).
2. The GW relation, Γ² = 1, H = Γ^R + a D_GKP (2.20) and [D_GW, J] = 0 are checked numerically. Here J = L'^L − L^R + σ/2.

**Round-sphere targets [standard; sympy].** For the charge-n Dirac operator on the unit S² (Wu–Yang monopole harmonics),
the level j = (n−1)/2 + k has λ² = (j+1/2)² − n²/4 = k(k+|n|) and degeneracy |n| + 2k per sign. The k = 0 level is the
|n|-fold zero-mode multiplet with j = (|n|−1)/2.

## Construction choices Venus should check

1. **N = 2L+1** (matrix size), so x = n/N. GKP's "N" is the integer 2L, not the matrix size.
2. **Sign convention.** The block L' = L − n/2 has AIN index +n, with zero modes of chirality Γ^R = +1. This follows AIN's
   sign at (3.39), where the block L − 1/2 gives +1. In GKP's convention the same block has winding κ = 2L' − 2L = −n.
   The opposite block L' = L + n/2 is reported too, with index −n.
3. **The normalisation a = 1/(L+½) uses the base spin L**, as written in (2.18). It is not the module spin L'. This choice
   matters for Stage B; see the Post-run section. Γ^R must keep this a for (Γ^R)² = 1. Only the prefactor of D_GW could be
   changed: AIN's general form (A.1) allows any invertible O(a) prefactor f(a, Γ). The run uses the prefactor as written.
4. **D_GW on the block.** D_GW is restricted to the block, i.e. it is (2.23) multiplied by P^(a). AIN's footnote 1 says that
   the index theorem holds for this operator, but "the meaning of this Dirac operator is not clear".
5. **Stage C, T > L.** AIN's list L^(a) = L + T + 1 − a assumes T ≤ L. For n ≥ N, `run.py` uses the irreps actually present
   in A_i, which run from |L − T| to L + T.
6. **D_GKP is a comparison only.** It is AIN's (2.8), D_GKP = σ·(A − L^R) + 1, restricted to the block. This is not GKP's
   own monopole spinor construction, which `run.py` does not reproduce.
7. **Tolerances [assumed input].** A zero mode is |λ| < 1e-8. Eigenvalues within 1e-7 are grouped as one level.

## Stages and fixed thresholds (in `run.py` before the first run)

**Stage A [standard], graded.** Covers N = 4..20 and n = 0..6, with n < N only.

- The zero modes of D_GW are counted directly, and the index ½Tr(Γ^R + Γ̂) is computed alongside.
- PASS needs exactly |n| zero modes in every sector.
- J² is printed on the zero modes, to show they form one spin-(|n|−1)/2 multiplet.
- Venus's note: the n = 3 zero modes form j = 1. `run.py` compares their rotation matrix with Wigner d¹(β) from sympy [standard].
- Reported only: the opposite orientation, the literal-construction cross-check, and D_GKP's zero-mode count (which grades
  only D_GKP).

**Stage B [prediction], graded.** Compares the lowest three nonzero levels with λ_k = √(k(k+|n|)) and checks degeneracy
|n| + 2k. It prints δ_k = |λ_k^fuzzy/λ_k^round − 1|.

- The scan covers n = 0..N−1 at N = 8, 12, 16 and 20 (Venus's addition b).
- n* comes from linear interpolation in n between the neighbouring integers that bracket δ₁ = 0.1 (first crossing), and
  x* = n*/N. The bracketing pair is printed (Venus's addition a).
- δ₁ at n = 0 is printed as the finite-N floor (Venus's addition c).
- PASS if max(x*)/min(x*) − 1 ≤ 0.20 over the four N.
- The scalings n/N² and k/N are printed only and never graded.
- **Fold-in (after review).** The drift is tagged [identity: prefactor convention]. Next to the AIN-as-written columns, `RESULTS.md`
  adds a column with a prefactor built from both spins (Venus): the geometric mean a_gm = √(a·a_s) of the base-spin normalisation
  a = 1/(L+½) and the charge-sector normalisation a_s = 1/(L'+½), with D = −a_gm⁻¹ Γ^R(1 − Γ^R Γ̂). Γ^R and Γ̂ are unchanged.
  With this prefactor the drift is zero. The AIN-as-written columns and the x* table are kept unchanged.
- **Rungs (Venus).** `RESULTS.md` also counts the distinct positive levels per (N, n) and checks the count against N − n in code.

**Stage C, reported only.** What happens at n = N−1, N and N+1 ("too many strings for the bubble"), for the charge +n block,
the opposite block and the literal isospin construction.

**Grade.** PASS = A exact and B collapses. PARTIAL = A exact with no clean collapse. FAIL = A wrong with D_GW.

## Notes

- **Bonus [standard].** The Stage B targets λ² = k(k+|n|), with degeneracy |n|+2k, are also the angular levels of a charged
  spin-½ particle on the S² of a magnetically charged black-hole horizon (near-horizon AdS₂ × S²). There the flux through
  S² plays the role of n.
- **Venus.** N = brane count/resolution, n = number of strings, and the n = 3 zero modes give j = 1, which links to d¹(β).
- **Scope [standard].** The zero-mode count is topological: it is the index and cannot change under small deformations. The number
  and position of the excited levels depend on the cutoff (rungs = N − n) and on the prefactor convention.
- **Helios's reading [standard; Orion verifying].** An N-state fuzzy sphere is the lowest Landau level of a charge-(N−1) monopole
  (Haldane, PRL 51 (1983) 605). Linking that to Akitti's bubble, where each string spends one unit of a fixed flux budget, is [assumed].

## Process disclosure

- Before writing `run.py`, a small prototype on the agent box checked the construction (zero-mode counts and conventions).
  It also showed the uniform-rescaling pattern reported in Stage B. That pattern is therefore tagged [post-hoc] in `RESULTS.md`.
- Helios set the thresholds, and they did not change.
- One early execution of `run.py` on the agent box, before Venus's additions were baked in, was interrupted. Its output was
  deleted without being read.
- The graded run is the single TrinityOrb run recorded in `RESULTS.md`.

## Tag key

- [computed]: produced by `run.py`.
- [identity]: exact algebra, checked numerically to round-off.
- [standard]: textbook or literature result.
- [prediction]: graded expectation.
- [finite-size]: effect of finite N.
- [assumed] / [assumed input]: a modelling choice or parameter.
- [post-hoc]: noticed or added after seeing a result.

## References

- H. Aoki, S. Iso and K. Nagao, "Ginsparg-Wilson relation and 't Hooft-Polyakov monopole on fuzzy 2-sphere", Nucl. Phys. B 684 (2004) 162, arXiv:hep-th/0312199.
  Filed PDF: `NPB684_162_Aoki_Iso_Nagao_GW_monopole_fuzzy_sphere.pdf`
- H. Grosse, C. Klimčík and P. Prešnajder, "Topologically nontrivial field configurations in noncommutative geometry", Commun. Math. Phys. 178 (1996) 507, arXiv:hep-th/9510083.
  Filed PDF: `CMP178_507_Grosse_Klimcik_Presnajder_topological_fuzzy_sphere.pdf`
- T. T. Wu and C. N. Yang, "Dirac monopole without strings: monopole harmonics", Nucl. Phys. B 107 (1976) 365.
- F. D. M. Haldane, "Fractional quantization of the Hall effect: a hierarchy of incompressible quantum fluid states", Phys. Rev. Lett. 51 (1983) 605 [standard; Orion verifying].

## Post-run (2 Oct 2026)

- [computed] **Stage A: PASS.** Every sector has exactly |n| zero modes, all of chirality +1, and the GW index equals n.
  J² on the zero modes is j(j+1) with j = (n−1)/2 to round-off: one multiplet. The n = 3 zero modes rotate exactly with d¹(β).
  The literal AIN construction matches the reduced block to round-off.
  - D_GKP on the same block has no exact zero modes for n ≥ 1 (reported only; it grades only itself).
  - The opposite block gives |n| zero modes of chirality −1 and index −n.
- [computed] **Stage B: PASS.** x* agrees across the four N far inside the 20% band. The finite-N floor δ₁(n = 0) is at
  round-off.
- [post-hoc] **What the drift is.** The drift is a **uniform rescaling**. Every positive level is
  λ_k = √(k(k+n)·N/(N−n)) to round-off, so δ_k is the same for every k and is exactly 1/√(1 − n/N) − 1. The level ratios are
  exactly the round ones. So yes, the levels drift when n crowds N, but only through one overall factor
  √(N/(N−n)) = √((2L+1)/(2L'+1)). That factor is AIN's choice a = 1/(L+½) (choice 3 above). With a prefactor of D_GW built
  from both spins, the drift would disappear.
  - The Stage B collapse is real, but it measures this normalisation rather than a reshuffling of levels.
  - The small spread in x* comes only from interpolating on the integer-n grid.
  - The closed form is numerical, not proved.
- [computed] **Stage C.**
  - In the charge +n block, the largest charge that exists is n = N−1 (L' = 0). There the N−1 zero modes plus a single
    cutoff level (|λ| = 2/a, degeneracy N+1) fill the whole space, and no smooth levels are left.
  - For n = N and N+1 the block does not exist (L' < 0).
  - In the literal isospin construction, the lowest block of A_i has index 2(N−1) − n. That means the index turns back down
    instead of growing: too many strings for the bubble.
  - The opposite orientation (charge −n) exists for every n.
- **Overall grade: PASS** (A exact, B collapses), as printed in `RESULTS.md` under the fixed rule.
- **Fold-in (2 Oct 2026, after review).** The folder was backed up to %TEMP%. `run.py` was edited and re-run once; `RESULTS.md`
  was regenerated by it and not hand-edited. This README was updated, and Orion's "Filed PDF:" lines are kept.
  - Added: the [identity: prefactor convention] tag on the drift; the both-spin (geometric-mean) prefactor column, whose drift is
    zero to round-off; the rungs = N − n check, which holds in every computed sector; and the scope and Haldane lines.
  - Every Stage A, Stage C and AIN-as-written Stage B number reproduced unchanged. Only the runtime line differs. No threshold changed.
  - Review outcome: Stage B is void as a prediction, because the drift it measured is a prefactor convention. So the physics grade
    is PARTIAL by Helios's rule, fixed beforehand (Stage A exact, Stage B void). The mechanical grade printed by `run.py` under the
    original rule is still PASS. `RESULTS.md` prints both.

## Sign-off

- Venus (maths): **PASS** (maths), 2 Oct 2026.
- Helios (physics): **PARTIAL** (physics; Stage A exact, Stage B void as a prediction, by the rule fixed beforehand), 2 Oct 2026.

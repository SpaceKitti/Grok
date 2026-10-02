# Job 6d spec: the mass-deformed membrane (BMN mass terms + Myers term on the 6b valley toy)

Status: FULL SPEC. Venus gave 2072F32D a pre-run maths PASS at about 23:10 BST, and her edits E1–E4 are folded in here (Helios, about 23:14 BST). Her checks are in `/workspace/6d/venus/` (chk.py, hess.py). Sources for Orion to verify where marked. Aethon builds it; queued after N1, A1 and 4c (STILL_TO_DO 2B89A550, Problem 3, "Next idea, Job 6d").
Suggested folder: `C:\Users\Akitt\Grok-jobs-push\jobs\membrane-6d-mass-deformed\` (same naming as 6b/6c) [suggested].

## Why this job
- Serves **open problem 03 (membranes)**. Job Six and 6b showed the mechanism behind the membrane's trouble. With supersymmetry the membrane can slide out along flat valleys for free, so its spectrum is a continuum starting at zero (de Wit–Lüscher–Nicolai, dWLN) [standard; 6b computed]. 6c closed the bound-state question at toy level.
- 6d asks the reverse question: what removes the valleys?
  - The plane-wave (BMN) matrix model adds mass terms and a Myers term.
  - Then the flat directions are lifted and the spectrum becomes discrete.
  - The ground states are fuzzy spheres, labelled by how the N branes split into groups (the partitions of N) [standard: BMN hep-th/0202021 §5].
- That fuzzy sphere is the object of Job U1. U1's base sphere x_i = αL_i is 6d's vacuum X_i = (μ/3)J_i with α = μ/3.
- *In plain words:* 6b's membrane could leak away along "gutters" in its energy landscape. 6d tilts the landscape into a bowl, so the gutters fill in. The membrane then has only a few resting shapes, which are little spheres, and a ladder of energy steps above them. The steps get closer together as the tilt is removed, until they merge back into 6b's continuum.
- **Lift link, one line [hive-interpretation]:** BMN's vacua are counted by p(N), the ways N branes share out into spheres. Their sphere radius grows with μN (BMN (5.5)). So this is a matrix-model version of lift requirement 4 (the crowding threshold, A against N). An S² carrying N units becomes the ground state rather than something that breaks up. The count is gravity-free, but the S² here is a matrix-model sphere, not the lift's r = 0 S².

## Units and conventions (fixed)
- ħ = 1 and l_p = 1. Use **R = 1 in DSV's (4.1)**, which is the same as **2R = 1 in BMN's (5.2)** (BMN footnote 8: 2R_BMN = R_BFSS).
- Scalars: X^i with i = 1, 2, 3 (the SO(3) directions) and X^a with a = 4…9 (the SO(6) directions). N×N Hermitian matrices.
- Mass terms ½(μ/3)²X^i² and ½(μ/6)²X^a², i.e. the μ²/9 and μ²/36 of the plane-wave metric (BMN (5.1)).
- Myers term **+i(μ/3)ε_ijk Tr X^iX^jX^k** in V. BMN write −i(μ/3)… in the action S, so it comes with a + sign in V.
- With these signs the vacuum is X^i = +(μ/3)J^i with [J^i, J^j] = iε_ijk J^k (BMN (5.4) at 2R = 1; DSV §4.2).
- su(2) generators: spin-j matrices, with τ = σ/2 for spin ½.

## The model
### Full matrix model (Stages A and B; classical and quadratic only)
The bosonic potential is (DSV (4.1) at R = 1; BMN (5.2) at 2R = 1):

V = Tr[ ½(μ/3)²(X^i)² + ½(μ/6)²(X^a)² + i(μ/3)ε_ijk X^iX^jX^k − ¼[X^i,X^j]² − ¼[X^a,X^b]² − ½[X^a,X^i]² ]

It is a sum of squares (DSV §4.2) [standard]:

V = ½Tr[ ((μ/3)X^i + iε_ijk X^jX^k)² + ½(i[X^a,X^b])² + (i[X^a,X^i])² + (μ/6)²(X^a)² ].
- I checked the SO(6) factors by hand: ½·½(i[a,b])² = −¼[a,b]² and ½(i[a,i])² = −½[a,i]², which matches the line above.
- Stage A1 re-checks this.

Fermion mass operator about a vacuum, for Stage B2: V_ψ = ψ†(¼ψ + ⅓σ^i J^i∘ψ), where J∘B = J_k B − B J_l on the block (k, l). This is DSV §5.3 [standard], with 4 copies from the SU(4) index.

### Toy (Stage C): the 3-variable diagonal truncation of the SU(2) model
- **Truncation:** set X^i = √2 q_i τ_i (no sum) and X^a = 0.
- **Why it changes from 6b [identity, to check in A4]:** 6b's toy has two variables, and the Myers term ε_ijk Tr X^iX^jX^k vanishes identically with fewer than three non-zero matrices. So 6d must keep three. This is the smallest change that can carry a fuzzy sphere.
- **Result (Helios sympy pre-check; A3 re-derives it):**
  - Kinetic term: ½q̇².
  - V = ½|∇W|², with W = (μ/6)(q₁² + q₂² + q₃²) − √2 q₁q₂q₃.
- **At μ = 0:** |∇W|² = 2(q₁²q₂² + q₂²q₃² + q₃²q₁²). That is the 3-variable version of Job Six/6b's x²y² valley potential, with flat valleys along each axis.
- **Consistent truncation [identity, check in A4]:** the ansatz is the fixed set of the combined rotations "gauge rotation by π about axis k × SO(3)_R rotation by π about axis k". So the equations of motion of every off-diagonal and X^a component vanish on it, and Gauss's law holds automatically.
- **Residual gauge:** V₄ = {flip the signs of two of the q's}. Physical states must be V₄-invariant, with fermions transforming like the q's.
- **Fermion stand-in [assumed]:** the Witten-type supercharge for W. 6b used a 2-state stand-in in the same spirit.
  - H_toy = ½(p² + |∇W|²) + Σ_ij (∂_i∂_jW) ψ_i†ψ_j − ½ΔW, with {ψ_i, ψ_j†} = δ_ij.
  - ΔW = μ.
  - Sectors F = 0, 1, 2, 3 (sizes 1, 3, 3, 1).
  - Along a valley at μ = 0, the F = 1 sector cancels the transverse zero-point energy exactly, as in dWLN/6b. Check: transverse frequencies √2|q₁| twice against a Hessian eigenvalue −√2|q₁|.
- **Dropped, and so stated in the README:**
  - the Jacobian (measure) of the diagonal truncation (Job Six dropped it too);
  - the six SO(6) directions;
  - BMN's real 16-component fermions with mass μ/4.
- **So the toy is not BMN.** Its fermions have the "standard" SUSY algebra, not BMN's SU(2|4). Expect tunnelling between the toy's vacua that the full theory forbids (see C3).

## Known before it runs (from the pre-check; classical only, no spectra computed)
- Critical points of W:
  - the trivial vacuum q = 0, with Hessian (μ/3)·1;
  - four points q = (√2μ/6)(±1, ±1, ±1) with an even number of minus signs, all with W = μ³/108 and Hessian eigenvalues (μ/3)(−1, 2, 2).
- The four points are one V₄ orbit, which is the N = 2 irreducible fuzzy sphere X^i = (μ/3)τ_i. So there are 2 gauge classes = p(2) [identity].
- Frequencies μ/3 and 2μ/3 about the fuzzy point are the DSV N = 2 entries α_{j=0} = μ/3 and β_{j=2} = 2μ/3 [standard: DSV Table 1].
- Pre-check script: `/workspace/6d/precheck/identities.py` (box). Aethon must re-derive all of this in run.py.

## Stages
### Stage A: identities (sympy) [identity]
- **A1 (perfect square):** check Tr[½((μ/3)X^i + iε_ijk X^jX^k)²] = Tr[½(μ/3)²X^i² + i(μ/3)ε_ijk X^iX^jX^k − ¼[X^i,X^j]²].
  - Symbolically in the toy.
  - Numerically for random Hermitian X with N = 2, 3, 4.
  - Check the SO(6) squares against DSV §4.2 as well.
- **A2 (vacua and count):** for every partition of N, for N = 1…5, build X^i = (μ/3)·⊕_k J^(N_k) with X^a = 0.
  - Check [X^i, X^j] = i(μ/3)ε_ijk X^k and V = 0 exactly (sympy, rational μ).
  - The number of vacua must be p(N) = 1, 2, 3, 5, 7.
  - The trivial vacuum (all N_k = 1) has E = 0.
  - *In words:* every way of splitting N branes into spheres costs exactly zero energy.
- **A3 (toy):**
  - V_toy = ½|∇W|².
  - H_toy = ½{Q, Q†} for the stated Q, with H_toy ≥ 0.
  - ΔW = μ.
  - All solutions of ∇W = 0 are the five points above. W and the Hessian take the values above.
  - At μ = 0 the toy reduces to the 3-variable valley model.
- **A4 (truncation):** the off-diagonal and X^a equations of motion vanish on the ansatz, Gauss's law holds, and the Myers term is non-zero only with three non-zero matrices.

### Stage B: fluctuation spectrum about every vacuum (numpy, N = 2, 3, 4, all partitions) [computed vs standard]
- **B1 (bosons):** diagonalise the Hessian of the full V (all 9N² real components) at each vacuum. Masses = √(Hessian eigenvalues).
  - **Exact Hessian required [Venus E2]:** build it as an exact quadratic form (sympy, or the analytic second variation). Do not use finite differences: Venus's FD check had about 1e-5 noise on the zero modes, which cannot meet the 1e-9 tolerance.
  - Count an eigenvalue as a zero mode when |eigenvalue| ≤ 1e-10 μ² (fixed now).
  - Venus has already matched the full Hessian against DSV Table 1 at N = 2 and 3, zero modes included [computed, Venus]. So B1 there is a reproduction check of the code.
  - Match DSV Table 1 (irreducible) and Table 2 (reducible): SO(6) masses 1/6 + j/3, and SO(3) masses (j+1)/3 and j/3, in units of μ, with the stated spin ranges and degeneracies.
  - Zero modes = gauge-orbit dimension = N² − dim(commutant of the J's) (DSV §5.3).
  - Trivial vacuum: μ/3 (×3N²) and μ/6 (×6N²) (BMN p. 16 text).
- **B2 (fermions):** eigenvalues of DSV's V_ψ at each vacuum, against DSV Tables 1–2 (1/4 + j/3 and 1/12 + j/3), with degeneracies. Trivial vacuum: all μ/4.
- **B3 (zero-point cancellation):** at every vacuum, Σ (degeneracy × mass) over bosons = Σ (degeneracy × mass) over fermions, using DSV's Table 1/2 degeneracies as listed (real bosons; complex fermions) [Venus E1]. Any overall ½ is common to both sides, so it is left out.
  - For the irreducible vacuum, both sums equal (2/9)μN(8N² + 1) (DSV after Table 1) [standard; 2/9 confirmed by Venus's sympy sum, computed].
  - *In words:* the quantum jitter of the bosons and of the fermions cancel exactly, so the fuzzy spheres and the trivial vacuum stay at zero energy at this order.

### Stage C: the valley becomes a gapped ladder (one small (μ, L) grid; toy only) [computed]
- **Discretisation:** 6b's 4th-order central stencil family on a cell-centred grid in [−L, L]³, with Dirichlet walls. The grid is symmetric, so the V₄ flips are exact.
- **Sectors:** the F = 1 sector (3 components; this carries the valleys), plus F = 0 (scalar; the trivial-vacuum state).
- Classify every eigenvector by its V₄ character and keep the V₄-invariant ones.
- **Solver:** Aethon's choice (shift-invert eigsh if it fits in memory, else Lanczos 'SA' or LOBPCG). Print the residuals ‖Hv − Ev‖.
- **C1 (μ = 0 control, 6b reproduced in 3 variables):** h = 0.2, L = 3, 4, 5. Lowest 4 V₄-invariant F = 1 levels.
  - They must fall like L⁻², with the fitted log-log slope of each in [−2.3, −1.7] (Job Six's window). Report the k² pattern.
  - A level that does not fall is reported as a flag. That would be news, because 6c found no d = 3 bound state.
- **C2 (μ > 0):** μ ∈ {2, 3, 4, 6} at L = 4, h = 0.2.
  - Report the lowest 6 V₄-invariant F = 1 levels and the lowest 3 F = 0 levels.
  - Box check: μ = 2 at L = 5. Grid check: μ = 3 at h = 0.16.
  - **Gap Δ(μ)** = the median of the consecutive spacings among the lowest 4 V₄-invariant F = 1 levels (fixed now).
- **C3 (report only): the vacuum energies.** Report the lowest F = 0 and F = 1 levels against μ.
  - **Toy ground states [Venus E3]:** after V₄, the toy keeps two perturbative ground states. One is F = 0, on the trivial vacuum (Morse index 0). The other is F = 1, on the fuzzy orbit (one negative Hessian direction). They contribute with opposite signs, so the toy's Witten index is 0. The diagonal gradient-flow line joins them, so tunnelling lifts them together.
  - Expected lifting: E₀ ~ e^(−2·μ³/108). The factor 2 is there because the tunnelling amplitude goes like e^(−ΔW), and the energy shift is its square [prediction, semiclassical; Venus].
  - At μ = 2 this is only about e^(−0.15). So across most of C2 there is no suppression, and E₀ of order Δ is expected.
  - In full BMN both vacua are exactly zero-energy, protected by SU(2|4) [standard: DSV §4.1, "fully supersymmetric if and only if it has zero energy"].
  - So C3 is not graded. A non-zero toy E₀ at small μ is a toy artefact, not a BMN failure.
- **C0 (report only, the literal 6b operator):** 6b's H₁ = p² + x²y² + xσ₃ + yσ₁ plus (μ/3)²(x² + y²), with 6b's own code and grid (L = 8, 10, 12; h = 0.08), for μ ∈ {0, 0.5, 1, 2}.
  - In 2 variables there is no Myers term, and the mass breaks 6b's supersymmetry.
  - Leading Born–Oppenheimer (BO) expectation: spacing → 2μ/3 in 6b's units (H = p² + …) [prediction, BO].
  - This is the closest literal "6b valley turned into a ladder".

### Stage D: prediction (fixed now, before any run) [prediction]
- **D1:** Δ(μ) shrinks toward 0 as μ → 0, recovering 6b's continuum.
  - On the C2 points, Δ must increase monotonically with μ.
  - The fitted log-log slope of Δ against μ must be in [0.8, 1.2] (gap ∝ μ).
  - Δ(2)/Δ(6) must be in [0.25, 0.45] (linear gives 1/3).
- **D2 (coefficient, report-only flag):** Δ ≈ μ/3, the BMN SO(3) mass, is expected in both simple limits [prediction; both confirmed by Venus]. Flag "agrees" if Δ/(μ/3) is within 20%. Not graded.
  - **Limit 1, valley BO (small μ, roughly μ ≲ 1).** It needs √2s ≫ μ/3 at the valley width s ~ √(3/μ). The transverse zero-point (√2s ± μ/3) cancels against the F = 1 fermion term, leaving a constant −μ/6. So the valley potential is ½(μ/3)²s², with spacing μ/3.
  - **Limit 2, harmonic about the critical points (large μ, μ³/108 ≫ 1).** The Hessian frequencies are μ/3 and 2μ/3.
  - **Regime note [Venus E4]:** C2's μ = 2–6 sits in the crossover between the two limits. So D1 is a real test, not a guaranteed pass. The D1 windows stay as fixed.
  - **Optional report-only point:** μ = 1 at L = 6, h = 0.2, which is inside the valley-BO regime. It doesn't enter the grade.
- *In plain words:* the steps of the ladder are as wide as the bowl is steep, so flattening the bowl closes the steps up into a continuum.

## Pass rule (fixed before the run)
- **PASS:**
  - A: every sympy residual is exactly 0, and numeric residuals are ≤ 1e-12.
  - B: every mass matches DSV to ≤ 1e-9 relative, the degeneracies and zero-mode counts are exact, and B3 holds to ≤ 1e-9.
  - C1: the μ = 0 slopes are in the window.
  - C2: converged, meaning box and grid changes of the lowest 4 levels are ≤ 3%.
  - D1: all three conditions hold.
- **PARTIAL:** A and B pass, but C is not converged by the 3% rule or the C1 control fails. The numerics are then inconclusive; name the failing check.
- **FAIL:**
  - A or B fails. These are known results, so the code is wrong.
  - Or C is converged and D1 fails. That falsifies the prediction in this toy, and should be written up as such.
- Thresholds may not change after the first graded run. Any scratch run is disclosed, as in B2.

## What a PASS shows, and what it does not
- **Shows:**
  - The hive's toy reproduces the known BMN facts [standard]: the vacua are fuzzy spheres counted by p(N) at zero energy, and the fluctuation masses are DSV's.
  - In the smallest truncation that can carry a Myers term, the flat-valley continuum of 6b becomes a discrete ladder whose spacing shrinks to zero with μ [computed, toy].
- **Does not show:**
  - Anything new about BMN. Stages A–B are a reproduction.
  - That full BMN quantum vacua are exact. That is DSV's symmetry argument, not tested here; the toy's fermions are a stand-in.
  - Large N, or the membrane's continuum limit.
  - A finite quantum membrane in flat space. At μ = 0 the continuum returns, and problem 03 stays open.
  - Anything about gravity or the lift.
- The lift link is [hive-interpretation] only.

## Budget
Tiny.
- Stages A and B: seconds (N ≤ 4 gives dense matrices of size ≤ 144).
- Stage C: about 8 sparse eigensolves of ≤ about 4e5 unknowns.
- Target total runtime ≤ 5 min on TrinityOrb. If it is over, drop C's h to 0.25 and report it as [grid-step].

## Refs (verification status)
- D. Berenstein, J. Maldacena, H. Nastase, hep-th/0202021, §5: eqs. (5.1)–(5.5), the mass and Myers terms, vacua labelled by partitions (pp. 15–17); App. B (B.27) for fermion mass μ/4. **[verified: arXiv PDF read on box by Helios]**
- K. Dasgupta, M. M. Sheikh-Jabbari, M. Van Raamsdonk, hep-th/0205185: eq. (4.1) action, §4.2 sum-of-squares potential and vacua, §5.2 Table 1, §5.3 Table 2 and V_ψ, zero-point sentence after Table 1. **[verified: arXiv PDF read on box]**
- R. C. Myers, "Dielectric-Branes", hep-th/9910053, §6 (dielectric D0-branes). **[ID and title verified; content not read; Orion to confirm the section]**
- B. de Wit, M. Lüscher, H. Nicolai, "The supermembrane is unstable", Nucl. Phys. B 320 (1989) 135 (pre-arXiv, no ID). Spectrum [0, ∞), §1 eqs. (1.5)–(1.11). **[on disk in `03_membrane_renormalization\`; read by Job Six]**
- E. Witten, "Supersymmetry and Morse theory", J. Diff. Geom. 17 (1982) 661 (fermion stand-in and the critical-point picture of SUSY ground states). **[not verified; Orion to verify]**
- E. Witten, "Dynamical breaking of supersymmetry", Nucl. Phys. B 188 (1981) 513 (SUSY quantum mechanics). **[not verified; Orion to verify]**
- Background, already in the hive: FGHHY hep-th/9904182 (6b); Kac–Smilga hep-th/9908096 and Yi hep-th/9704098 (6c); BFSS hep-th/9610043; B. Simon, Ann. Phys. 146 (1983) 209 (Job Six).
- Hive inputs read for this spec: STILL_TO_DO.md 2B89A550 (Problem 3); Job Six README 9B2CB3FD; 6b README 7D4929F2 and RESULTS 20A6261E; 6c README 40C8DA8B; U1 README 0D584792. Box copies are byte-identical to TrinityOrb (hashes checked).

## Venus's pre-run answers (2072F32D, about 23:10 BST), now folded in
1. **SO(6) factors:** right. The perfect square holds for random Hermitian N = 2, 3, 4 (residual ≤ 1e-13) [computed, Venus].
2. **Zero-point factor:** 2/9 is right. Σ deg·mass gives (2/9)N(8N² + 1) on both sides [computed, Venus]. The B3 wording was fixed (E1).
3. **Spacings:** μ/3 for the toy and 2μ/3 for C0 in 6b units, both right at leading BO. C0's y-mass leaves a small μ²/(18|x|) residue.
4. **Gauge projection:** V₄ with vector-like fermion signs is right. The residual gauge is pure adjoint rotation by π, and the fermions are adjoint.
5. **Jacobian:** dropped for the graded run, so 6b stays comparable. With X^a = 0 the diagonal form is an exact SVD slice for SU(2)_gauge × SO(3)_R, with Jacobian ∏|q_i² − q_j²| [identity, Venus]. A report-only bosonic Jacobian variant is allowed but optional.

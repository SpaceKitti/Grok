# pairA-drive-return — RESULTS

Signed off: Venus (maths), Helios (physics), 2026-09-25

Scope: two-mode toy (H_A is 2x2, from the Pair A handoff). Driven Schrödinger evolution i dψ/dt = H_A(ε(t))ψ; no field/MHD dynamics. C held.

Model: seed.H_A, ε_EP = 0.513680663, λ_EP = (-0-0.308425j), γ = |a−b|/2 = 0.185055, r = 0.25 ε_EP = 0.128420166.
Loop: ε(t) = ε_EP + r e^{i(±ωt+π)}. Start/end point ε = 0.75 ε_EP = 0.385260497 (inside Γ = [−ε_EP, ε_EP]: YES).
At the start/end point: sheet A λ = 0.000000-0.430827j (faster-decaying), sheet B λ = 0.000000-0.186023j (slower-decaying). Sheet A = λ_EP + y/2, B = λ_EP − y/2, Γ-segment cut read on the upper lip (vortices-return convention).
Shared decay −i(a+b)/2 removed (H' = H_A + i(a+b)/2); ψ renormalised every step. Weights: w± = |c±|²/Σ|c|² with c = R⁻¹ψ, i.e. c± = <L±|ψ>/<L±|R±>; R columns = right eigenvectors at the recording point, unit Euclidean norm. Plain normalised-overlap weights shown for comparison only.

## Speeds, integrator, convergence

- γT per loop (T = 2π/|ω|): fast γT = 1 (T = 5.4038, ω/min-gap = 4.7496), slow20 γT = 20 (T = 108.0760, ω/min-gap = 0.2375), slow40 γT = 40 (T = 216.1520, ω/min-gap = 0.1187), slow100 γT = 100 (T = 540.3799, ω/min-gap = 0.0475); min |λ+−λ−| on the loop = 0.244805.
- Integrator: ψ ← exp(−i H'(t_mid) dt) ψ (exact 2x2 exponential), steps per turn = max(2000, γT/0.01): fast 2000 (γdt = 0.0005), slow20 2000 (γdt = 0.0100), slow40 4000 (γdt = 0.0100), slow100 10000 (γdt = 0.0100).
- Convergence (dt halved once, all 16 runs, 2π and 4π): max |Δw| = 3.78e-07.

## Drive table (winner = larger left-eigenvector weight at the recording point ε = 0.75 ε_EP)

| direction | speed | start sheet | winner at 2π (w) [tracked label] | winner at 4π (w) [tracked label] | back on Γ at 4π |
|---|---|---|---|---|---|
| ccw (+w) | fast (γT=1) | A (faster-decaying) | A faster-decaying (w=0.73826) [B] | B slower-decaying (w=0.89652) [A] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 10/90), not a pure mode |
| ccw (+w) | fast (γT=1) | B (slower-decaying) | B slower-decaying (w=0.93122) [A] | B slower-decaying (w=0.84555) [B] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 15/85), not a pure mode |
| cw (-w) | fast (γT=1) | A (faster-decaying) | A faster-decaying (w=0.73826) [B] | B slower-decaying (w=0.89652) [A] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 10/90), not a pure mode |
| cw (-w) | fast (γT=1) | B (slower-decaying) | B slower-decaying (w=0.93122) [A] | B slower-decaying (w=0.84555) [B] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 15/85), not a pure mode |
| ccw (+w) | slow20 (γT=20) | A (faster-decaying) | B slower-decaying (w=0.98925) [B] | B slower-decaying (w=0.76639) [A] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 23/77), not a pure mode |
| ccw (+w) | slow20 (γT=20) | B (slower-decaying) | B slower-decaying (w=0.78232) [A] | B slower-decaying (w=0.67704) [B] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 32/68), not a pure mode |
| cw (-w) | slow20 (γT=20) | A (faster-decaying) | B slower-decaying (w=0.98925) [B] | B slower-decaying (w=0.76639) [A] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 23/77), not a pure mode |
| cw (-w) | slow20 (γT=20) | B (slower-decaying) | B slower-decaying (w=0.78232) [A] | B slower-decaying (w=0.67704) [B] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 32/68), not a pure mode |
| ccw (+w) | slow40 (γT=40) | A (faster-decaying) | B slower-decaying (w=0.99960) [B] | B slower-decaying (w=0.80639) [A] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 19/81), not a pure mode |
| ccw (+w) | slow40 (γT=40) | B (slower-decaying) | B slower-decaying (w=0.80317) [A] | B slower-decaying (w=0.69513) [B] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 30/70), not a pure mode |
| cw (-w) | slow40 (γT=40) | A (faster-decaying) | B slower-decaying (w=0.99960) [B] | B slower-decaying (w=0.80639) [A] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 19/81), not a pure mode |
| cw (-w) | slow40 (γT=40) | B (slower-decaying) | B slower-decaying (w=0.80317) [A] | B slower-decaying (w=0.69513) [B] | NO — ε is back on Γ (by construction) but the state is a fixed mix (A/B ≈ 30/70), not a pure mode |
| ccw (+w) | slow100 (γT=100) | A (faster-decaying) | B slower-decaying (w=0.99982) [B] | B slower-decaying (w=0.99982) [A] | NO — ε back on Γ (by construction) but the state is a pure mode on the OTHER sheet (B) |
| ccw (+w) | slow100 (γT=100) | B (slower-decaying) | B slower-decaying (w=0.99982) [A] | B slower-decaying (w=0.99982) [B] | YES (ε back on Γ by construction; pure start-sheet mode) |
| cw (-w) | slow100 (γT=100) | A (faster-decaying) | B slower-decaying (w=0.99982) [B] | B slower-decaying (w=0.99982) [A] | NO — ε back on Γ (by construction) but the state is a pure mode on the OTHER sheet (B) |
| cw (-w) | slow100 (γT=100) | B (slower-decaying) | B slower-decaying (w=0.99982) [A] | B slower-decaying (w=0.99982) [B] | YES (ε back on Γ by construction; pure start-sheet mode) |

Start point for all runs: ε = 0.75 ε_EP (inside Γ). [tracked label] = where continuous eigenvalue tracking takes the start sheet (swap at 2π, return at 4π).

Plain normalised-overlap weights (w_A, w_B) for comparison:

| direction | speed | start | 2π plain | 4π plain | 2π left (w_A, w_B) | 4π left (w_A, w_B) |
|---|---|---|---|---|---|---|
| ccw (+w) | fast | A | 0.8818, 0.1182 | 0.2407, 0.7593 | 0.73826, 0.26174 | 0.10348, 0.89652 |
| ccw (+w) | fast | B | 0.4181, 0.5819 | 0.4424, 0.5576 | 0.06878, 0.93122 | 0.15445, 0.84555 |
| cw (-w) | fast | A | 0.8818, 0.1182 | 0.2407, 0.7593 | 0.73826, 0.26174 | 0.10348, 0.89652 |
| cw (-w) | fast | B | 0.4181, 0.5819 | 0.4424, 0.5576 | 0.06878, 0.93122 | 0.15445, 0.84555 |
| ccw (+w) | slow20 | A | 0.3749, 0.6251 | 0.4463, 0.5537 | 0.01075, 0.98925 | 0.23361, 0.76639 |
| ccw (+w) | slow20 | B | 0.4427, 0.5573 | 0.4654, 0.5346 | 0.21768, 0.78232 | 0.32296, 0.67704 |
| cw (-w) | slow20 | A | 0.3749, 0.6251 | 0.4463, 0.5537 | 0.01075, 0.98925 | 0.23361, 0.76639 |
| cw (-w) | slow20 | B | 0.4427, 0.5573 | 0.4654, 0.5346 | 0.21768, 0.78232 | 0.32296, 0.67704 |
| ccw (+w) | slow40 | A | 0.3651, 0.6349 | 0.1880, 0.8120 | 0.00040, 0.99960 | 0.19361, 0.80639 |
| ccw (+w) | slow40 | B | 0.1861, 0.8139 | 0.1482, 0.8518 | 0.19683, 0.80317 | 0.30487, 0.69513 |
| cw (-w) | slow40 | A | 0.3651, 0.6349 | 0.1880, 0.8120 | 0.00040, 0.99960 | 0.19361, 0.80639 |
| cw (-w) | slow40 | B | 0.1861, 0.8139 | 0.1482, 0.8518 | 0.19683, 0.80317 | 0.30487, 0.69513 |
| ccw (+w) | slow100 | A | 0.3600, 0.6400 | 0.3600, 0.6400 | 0.00018, 0.99982 | 0.00018, 0.99982 |
| ccw (+w) | slow100 | B | 0.3600, 0.6400 | 0.3600, 0.6400 | 0.00018, 0.99982 | 0.00018, 0.99982 |
| cw (-w) | slow100 | A | 0.3600, 0.6400 | 0.3600, 0.6400 | 0.00018, 0.99982 | 0.00018, 0.99982 |
| cw (-w) | slow100 | B | 0.3600, 0.6400 | 0.3600, 0.6400 | 0.00018, 0.99982 | 0.00018, 0.99982 |

**By construction:** ε is back on Γ at 2π and 4π by construction (the loop is phase-shifted to start and end at 0.75 ε_EP). 'Back on Γ at 4π' = YES only if, in addition, the final state is a single-sheet state (w > 0.99) on its start sheet.

## M-matrix check (Venus)

M = R⁻¹ U R, U = un-renormalised propagator of H' (det U = 1), R = right eigenvectors at ε = 0.75 ε_EP, columns [A, B], unit Euclidean norm (a column scaling, so D = RᵀR stays diagonal). Start on sheet j reads column j of M. Venus: M_cw = D⁻¹ M_ccwᵀ D, so cw from A reads row A of M_ccw.

D = diag(+0.661438+0.000000i, +0.661438+0.000000i); D_A/D_B = +1.000000+0.000000i; |off-diagonal of RᵀR| = 1.7e-16.

| speed | turn | M_ccw | M_cw | det M_ccw (exact 1) | ‖M_cw − D⁻¹M_ccwᵀD‖ | \|M_AB\|, \|M_BA\| | σ1, σ2 (ccw) | σ1/σ2 | class (ccw) | u (ccw output): slow frac | D⁻¹w from M_ccw: slow frac | u_cw (cw output, direct): slow frac |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fast (γT=1) | 2π | [[+0.626793+0.000000i, -0.078159+0.364931i], [+0.078159+0.364931i, +1.373207+0.000000i]] | [[+0.626793-0.000000i, +0.078159+0.364931i], [-0.078159+0.364931i, +1.373207-0.000000i]] | +1.000000+0.000000i | 2.3e-15 | 0.373207, 0.373207 | 1.441, 0.6942 | 2.075 | mixed (none of the three) | 0.96844 | 0.96844 | 0.96844 |
| fast (γT=1) | 4π | [[+0.253586+0.000000i, -0.156318+0.729862i], [+0.156318+0.729862i, +1.746414-0.000000i]] | [[+0.253586-0.000000i, +0.156318+0.729862i], [-0.156318+0.729862i, +1.746414+0.000000i]] | +1.000000+0.000000i | 2.9e-14 | 0.746414, 0.746414 | 1.994, 0.5014 | 3.977 | mixed (none of the three) | 0.90069 | 0.90069 | 0.90069 |
| slow20 (γT=20) | 2π | [[-0.116347-0.000000i, -0.979321+0.535873i], [+0.979321+0.535873i, +2.116347+0.000000i]] | [[-0.116347-0.000000i, +0.979321+0.535873i], [-0.979321+0.535873i, +2.116347+0.000000i]] | +1.000000+0.000000i | 1.6e-11 | 1.116347, 1.116347 | 2.615, 0.3824 | 6.839 | mixed (none of the three) | 0.83361 | 0.83361 | 0.83361 |
| slow20 (γT=20) | 4π | [[-1.232693-0.000000i, -1.958642+1.071747i], [+1.958642+1.071747i, +3.232693-0.000000i]] | [[-1.232693+0.000000i, +1.958642+1.071747i], [-1.958642+1.071747i, +3.232693+0.000000i]] | +1.000000+0.000000i | 7.0e-11 | 2.232693, 2.232693 | 4.679, 0.2137 | 21.89 | rank-1-dominated | 0.70438 | 0.70438 | 0.70438 |
| slow40 (γT=40) | 2π | [[+0.019622-0.000000i, +0.288602-0.936937i], [-0.288602-0.936937i, +1.980378+0.000000i]] | [[+0.019622+0.000000i, -0.288602-0.936937i], [+0.288602-0.936937i, +1.980378-0.000000i]] | +1.000000+0.000000i | 1.2e-07 | 0.980378, 0.980378 | 2.381, 0.42 | 5.668 | mixed (none of the three) | 0.85704 | 0.85704 | 0.85704 |
| slow40 (γT=40) | 4π | [[-0.960757-0.000000i, +0.577203-1.873874i], [-0.577203-1.873874i, +2.960756-0.000000i]] | [[-0.960757+0.000000i, -0.577203-1.873874i], [+0.577203-1.873874i, +2.960755+0.000000i]] | +1.000000+0.000000i | 6.5e-07 | 1.960756, 1.960757 | 4.162, 0.2403 | 17.32 | rank-1-dominated | 0.72717 | 0.72717 | 0.72717 |
| slow100 (γT=100) ⚠ | 2π | [[-1999.726658+382.033474i, -368.693723-3820.940758i], [+147071.250226-30166.669313i, +31075.501859+281377.801078i]] | [[-2102.436378-2251.509287i, +2991.364396-4172.252073i], [-152777.614439-168116.859393i, +224811.523593-304662.833150i]] | -148945.218008+21464.962047i | 6.7e+05 | 3838.687711, 150133.209452 | 3.205e+05, 0.4696 | 6.825e+05 | rank-1-dominated | 0.99982 | 0.78048 | 0.99982 |
| slow100 (γT=100) ⚠ | 4π | [[-323307246.097671-162109442.537611i, +568591846.416408-665151282.150037i], [+24012245684.641026+11628963206.341974i, -41260576284.678955+49634281765.224197i]] | [[+21890786.772340+46645600.105930i, -175559653.319368+726637213.092224i], [+1555437735.834621+3449756920.239384i, -13655812490.427284+53380387019.862267i]] | -2157858490809658.250000+1248413777642094.500000i | 3.9e+10 | 875055950.186648, 26679968667.035892 | 6.985e+10, 3.569e+04 | 1.957e+06 | rank-1-dominated | 0.99982 | 0.85407 | 0.99982 |

Note (Helios): σ1/σ2 does not grow steadily with loop time (21.9 at γT=20, 17.3 at γT=40). This is physical, not a bug: the loss contrast partly cancels around the loop because the decay gap changes sign across the cut.

|M| entries and cw singular values:

| speed | turn | \|M_ccw\| | \|M_cw\| | σ1, σ2 (cw) | ‖U_cw − σx U_ccw^{−†} σx‖ |
|---|---|---|---|---|---|
| fast | 2π | [[0.626793, 0.373207], [0.373207, 1.373207]] | [[0.626793, 0.373207], [0.373207, 1.373207]] | 1.4406, 0.6942 | 4.9e-15 |
| fast | 4π | [[0.253586, 0.746414], [0.746414, 1.746414]] | [[0.253586, 0.746414], [0.746414, 1.746414]] | 1.9943, 0.5014 | 1.1e-13 |
| slow20 | 2π | [[0.116347, 1.116347], [1.116347, 2.116347]] | [[0.116347, 1.116347], [1.116347, 2.116347]] | 2.6151, 0.3824 | 4.7e-11 |
| slow20 | 4π | [[1.232693, 2.232693], [2.232693, 3.232693]] | [[1.232693, 2.232693], [2.232693, 3.232693]] | 4.6791, 0.2137 | 7.1e-10 |
| slow40 | 2π | [[0.019622, 0.980378], [0.980378, 1.980378]] | [[0.019622, 0.980378], [0.980378, 1.980378]] | 2.3808, 0.4200 | 1.3e-07 |
| slow40 | 4π | [[0.960757, 1.960756], [1.960757, 2.960756]] | [[0.960757, 1.960756], [1.960756, 2.960755]] | 4.1618, 0.2403 | 5.9e-07 |
| slow100 | 2π | [[2035.892011, 3838.687711], [150133.209452, 283088.597007]] | [[3080.508528, 5133.804468], [227165.749808, 378628.661149]] | 441587.8015, 0.5167 | 4.0e+05 |
| slow100 | 4π | [[361672568.408381, 875055950.186648], [26679968667.035892, 64544535645.501999]] | [[51526872.161566, 747544534.676062], [3784205247.974514, 55099427702.690247]] | 55234306552.4467, 207394.0539 | 8.1e+10 |

Rank-1 fit: M ≈ σ1 u wᵀ (leading SVD pair, wᵀ = v1ᴴ). ccw output direction = u; cw output direction = D⁻¹w. Chiral would mean u ≠ D⁻¹w. 'slow frac' = weight of the slower-decaying mode (sheet B).

⚠ Precision limit: slow100 2π, slow100 4π: det M ≠ 1 (see table), i.e. the un-renormalised propagator's dynamic range (σ1/σ2 = σ1² with det = 1; σ1 ≈ 3e5 at 2π, ≈ 7e10 at 4π) exceeds double precision, so the individual M entries, the identity residuals and D⁻¹w from M_ccw's row are NOT reliable there. The output directions u (the attractor of each direction's own propagation) and the renormalised drive-table weights are reliable (dt-halving converged). For these cases compare u (ccw output) with u_cw (cw output from the direct cw propagation, which equals D⁻¹w in exact arithmetic). An optional fix without mpmath: propagate the two basis vectors separately, renormalising each step with a running log of the norms, to get M in log-scaled form. Not done; the weights at γT=100 are already dt-converged.

**Why the weights are identical in both directions (computed, not assumed; residuals over the precision-OK cases γT = 1, 20, 40):**
1. D_A/D_B = +1.000000+0.000000i (|D_A| = |D_B|), so Venus's identity M_cw = D⁻¹M_ccwᵀD reduces to M_cw = M_ccwᵀ (max residual 6.5e-07).
2. |M_AB| = |M_BA| (max relative difference 1.1e-07). This comes from a second symmetry: H' is PT-symmetric, σx H'(ε)* σx = H'(ε̄), which gives U_cw = σx (U_ccw⁻¹)† σx (max residual 5.9e-07); combined with U_cw = U_ccwᵀ it fixes the off-diagonal moduli of M to be equal.
3. cw from sheet j reads row j of M_ccw, ccw reads column j; with (1) and (2) the row and the column have identical moduli, so the weights are identical. M_ccw is not diagonal or antidiagonal here; the equality is from the two symmetries, not from adiabaticity. It holds for this start point (real ε inside Γ); other start points were not run. At γT = 100 the identities cannot be checked in double precision, but both directions' output directions u agree (table) and the drive-table weights are identical.
4. Old weight code: correct. Drive-table weights agree with the M-column weights to 1.5e-06; no old number changed.

## Checks

- Sanity run γT = 0.01, start A (ccw): fidelity |<ψ₀|ψ_end>|/norms = 0.99999683 at 2π, 0.99998716 at 4π (expect ≈ 1).
- Fixed ε = 0.75 ε_EP, mixed start (R_A + R_B): ΔΓ = Im λ_slow − Im λ_fast = 0.244805; slower-decaying mode = sheet B.

| γt | w_fast/w_slow measured | expected (initial ratio)·e^{−2ΔΓt} | rel. error |
|---|---|---|---|
| 1 | 7.095203e-02 | 7.095203e-02 | 1.8e-14 |
| 2 | 5.034190e-03 | 5.034190e-03 | 3.7e-14 |
| 5 | 1.798142e-06 | 1.798142e-06 | 9.8e-14 |
| 10 | 3.233315e-12 | 3.233315e-12 | 1.9e-13 |

## On-cut path (on_cut.py)

Start on Γ, go along Γ to ε = 0, figure-eight around both tips (+ε_EP anticlockwise, −ε_EP clockwise, as in vortices-return), back along Γ; continuous eigenvalue tracking.

| start | λ at start | λ at end | max \|Δλ\| | λ on Γ at the end (returns to start value) |
|---|---|---|---|---|
| eps=0 | -0.000000-0.493480j, -0.000000-0.123370j | -0.000000-0.493480j, -0.000000-0.123370j | 0.0e+00 | **YES** |
| eps=0.75 eps_EP | 0.000000-0.430827j, 0.000000-0.186023j | 0.000000-0.430827j, 0.000000-0.186023j | 0.0e+00 | **YES** |

Expected YES (Venus): this is a setup check, already known from pairA-vortices-return, not a new result.

## Missing mechanism

Definition (fixed before running, Helios/Orion): **YES** only if ccw and cw give DIFFERENT physical winners (slower- vs faster-decaying mode at the recording point) for the same start sheet; if both directions give the same winner (e.g. both slower-decaying = passive drift baseline) → **NO**. Primary: the slowest runs, γT = 40 and γT = 100, at 4π.

Per speed / time: fast 2π NO, 4π NO; slow20 2π NO, 4π NO; slow40 2π NO, 4π NO; slow100 2π NO, 4π NO.
Secondary (earlier wording: winner depends on direction and not on start sheet): fast 2π NO, 4π NO; slow20 2π NO, 4π NO; slow40 2π NO, 4π NO; slow100 2π NO, 4π NO.
Driven winner equals tracked label (state follows the sheet swap): fast 2π NO, 4π NO; slow20 2π NO, 4π NO; slow40 2π NO, 4π NO; slow100 2π NO, 4π NO.

**missing mechanism: NO**

Reason: at γT = 40 and 100 both directions end on the same physical mode at 4π (slow40: slower-decaying, slow100: slower-decaying); in the rank-1 fit the ccw output u and the cw output (D⁻¹w; taken from the direct cw propagation) both lean to the slower-decaying mode (slow fractions ccw, cw at 4π: slow40 0.727, 0.727, slow100 1.000, 1.000) — the physical non-chiral NO (passive drift toward the slower-decaying mode), with the directions made equal by the transpose + PT symmetries at this start point.

Scope: two-mode toy; one start point (0.75 ε_EP on the real axis). The start point can change which direction flips (Milburn et al.); other start points were not run.

Plot: outputs/weights_vs_theta.png (w_A vs θ for every run; w_B = 1 − w_A).

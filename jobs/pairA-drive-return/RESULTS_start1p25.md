**Signed off 2026-09-25:** Venus (maths) and Helios (physics).

# pairA-drive-return — RESULTS, start point 1.25 ε_EP

Companion to the signed-off RESULTS.md (start 0.75 ε_EP), which is unchanged. Produced by `python run.py --start 1.25`.

Scope: two-mode toy (H_A is 2x2, from the Pair A handoff). Driven Schrödinger evolution i dψ/dt = H_A(ε(t))ψ; no field/MHD dynamics. C held.

Loop: ε(t) = ε_EP + r e^{±iωt} (no π shift), r = 0.25 ε_EP. Start/end ε = 1.25 ε_EP = 0.642100829: on the real axis, **inside Γ: NO** (Γ = [−ε_EP, ε_EP]). The loop crosses Γ at θ = π (ε = 0.75 ε_EP).
Eigenvalues at the start point: λ_A = -0.138791-0.308425i, λ_B = +0.138791-0.308425i (λ − λ_EP = -0.138791+0.000000j, 0.138791-0.000000j); eigenvalues of H' = H_A + i(a+b)/2: -0.138791+0i, +0.138791-1.66533e-16i (real ±: same decay rate, different frequency).
Sheet labels at 1.25 ε_EP (vortices-return convention continued off Γ): A = λ_EP + y/2, B = λ_EP − y/2, y = 2v√(ε−ε_EP)√(ε+ε_EP) with principal roots (Γ-segment cut). Here ε > ε_EP is real, so both roots are real and positive and y = 2v·√(ε²−ε_EP²) < 0 (v < 0): sheet A = lower-frequency mode (Re λ_A < Re λ_B), sheet B = higher-frequency mode.
Physical naming: winners are named by FREQUENCY (higher- vs lower-Re λ mode at the recording point), since the decay rates are equal here. Weights: left-eigenvector weights w± = |c±|²/Σ|c|², c = R⁻¹ψ (R = unit-norm right eigenvectors at the recording point).

## Speeds, integrator, convergence

- γT per loop: fast 1 (T = 5.4038), mid5 5 (T = 27.0190), slow20 20 (T = 108.0760), slow40 40 (T = 216.1520), slow100 100 (T = 540.3799); γ = |a−b|/2 = 0.185055; min |λ+−λ−| on the loop = 0.244805. (γT = 5 added for comparison with Venus's reference.)
- Integrator: ψ ← exp(−i H'(t_mid) dt) ψ (exact 2x2 exponential), steps per turn = max(2000, γT/0.01) (γdt ≤ 0.01), ψ renormalised every step.
- Convergence (dt halved once, all 20 runs, 2π and 4π): max |Δw| = 1.03e-07.

## Drive table (winner = larger left-eigenvector weight at the recording point ε = 1.25 ε_EP)

| direction | speed | start sheet | winner at 2π (w) [tracked label] | winner at 4π (w) [tracked label] | back at start / on Γ at 4π |
|---|---|---|---|---|---|
| ccw (+w) | fast (γT=1) | A (lower-frequency) | A lower-frequency (w=0.94027) [B] | A lower-frequency (w=0.83721) [A] | ε back at start (by construction) but NOT on Γ; state: mix A/B ≈ 84/16, not a pure mode |
| ccw (+w) | fast (γT=1) | B (higher-frequency) | B higher-frequency (w=0.85856) [A] | B higher-frequency (w=0.66479) [B] | ε back at start (by construction) but NOT on Γ; state: mix A/B ≈ 34/66, not a pure mode |
| cw (-w) | fast (γT=1) | A (lower-frequency) | A lower-frequency (w=0.85856) [B] | A lower-frequency (w=0.66479) [A] | ε back at start (by construction) but NOT on Γ; state: mix A/B ≈ 66/34, not a pure mode |
| cw (-w) | fast (γT=1) | B (higher-frequency) | B higher-frequency (w=0.94027) [A] | B higher-frequency (w=0.83721) [B] | ε back at start (by construction) but NOT on Γ; state: mix A/B ≈ 16/84, not a pure mode |
| ccw (+w) | mid5 (γT=5) | A (lower-frequency) | A lower-frequency (w=0.92008) [B] | A lower-frequency (w=0.91014) [A] | ε back at start (by construction) but NOT on Γ; state: mix A/B ≈ 91/9, not a pure mode |
| ccw (+w) | mid5 (γT=5) | B (higher-frequency) | A lower-frequency (w=0.89031) [A] | A lower-frequency (w=0.90221) [B] | ε back at start (by construction) but NOT on Γ; state: mix A/B ≈ 90/10, not a pure mode |
| cw (-w) | mid5 (γT=5) | A (lower-frequency) | B higher-frequency (w=0.89031) [B] | B higher-frequency (w=0.90221) [A] | ε back at start (by construction) but NOT on Γ; state: mix A/B ≈ 10/90, not a pure mode |
| cw (-w) | mid5 (γT=5) | B (higher-frequency) | B higher-frequency (w=0.92008) [A] | B higher-frequency (w=0.91014) [B] | ε back at start (by construction) but NOT on Γ; state: mix A/B ≈ 9/91, not a pure mode |
| ccw (+w) | slow20 (γT=20) | A (lower-frequency) | A lower-frequency (w=0.99699) [B] | A lower-frequency (w=0.99699) [A] | ε back at start (by construction) but NOT on Γ; state: pure lower-frequency mode (A, w=0.99699) |
| ccw (+w) | slow20 (γT=20) | B (higher-frequency) | A lower-frequency (w=0.99699) [A] | A lower-frequency (w=0.99699) [B] | ε back at start (by construction) but NOT on Γ; state: pure lower-frequency mode (A, w=0.99699) |
| cw (-w) | slow20 (γT=20) | A (lower-frequency) | B higher-frequency (w=0.99699) [B] | B higher-frequency (w=0.99699) [A] | ε back at start (by construction) but NOT on Γ; state: pure higher-frequency mode (B, w=0.99699) |
| cw (-w) | slow20 (γT=20) | B (higher-frequency) | B higher-frequency (w=0.99699) [A] | B higher-frequency (w=0.99699) [B] | ε back at start (by construction) but NOT on Γ; state: pure higher-frequency mode (B, w=0.99699) |
| ccw (+w) | slow40 (γT=40) | A (lower-frequency) | A lower-frequency (w=0.99937) [B] | A lower-frequency (w=0.99937) [A] | ε back at start (by construction) but NOT on Γ; state: pure lower-frequency mode (A, w=0.99937) |
| ccw (+w) | slow40 (γT=40) | B (higher-frequency) | A lower-frequency (w=0.99937) [A] | A lower-frequency (w=0.99937) [B] | ε back at start (by construction) but NOT on Γ; state: pure lower-frequency mode (A, w=0.99937) |
| cw (-w) | slow40 (γT=40) | A (lower-frequency) | B higher-frequency (w=0.99937) [B] | B higher-frequency (w=0.99937) [A] | ε back at start (by construction) but NOT on Γ; state: pure higher-frequency mode (B, w=0.99937) |
| cw (-w) | slow40 (γT=40) | B (higher-frequency) | B higher-frequency (w=0.99937) [A] | B higher-frequency (w=0.99937) [B] | ε back at start (by construction) but NOT on Γ; state: pure higher-frequency mode (B, w=0.99937) |
| ccw (+w) | slow100 (γT=100) | A (lower-frequency) | A lower-frequency (w=0.99991) [B] | A lower-frequency (w=0.99991) [A] | ε back at start (by construction) but NOT on Γ; state: pure lower-frequency mode (A, w=0.99991) |
| ccw (+w) | slow100 (γT=100) | B (higher-frequency) | A lower-frequency (w=0.99991) [A] | A lower-frequency (w=0.99991) [B] | ε back at start (by construction) but NOT on Γ; state: pure lower-frequency mode (A, w=0.99991) |
| cw (-w) | slow100 (γT=100) | A (lower-frequency) | B higher-frequency (w=0.99991) [B] | B higher-frequency (w=0.99991) [A] | ε back at start (by construction) but NOT on Γ; state: pure higher-frequency mode (B, w=0.99991) |
| cw (-w) | slow100 (γT=100) | B (higher-frequency) | B higher-frequency (w=0.99991) [A] | B higher-frequency (w=0.99991) [B] | ε back at start (by construction) but NOT on Γ; state: pure higher-frequency mode (B, w=0.99991) |

Left-eigenvector weights (w_A, w_B) and plain normalised-overlap weights:

| direction | speed | start | 2π left | 4π left | 2π plain | 4π plain |
|---|---|---|---|---|---|---|
| ccw (+w) | fast | A | 0.94027, 0.05973 | 0.83721, 0.16279 | 0.5842, 0.4158 | 0.5528, 0.4472 |
| ccw (+w) | fast | B | 0.14144, 0.85856 | 0.33521, 0.66479 | 0.4354, 0.5646 | 0.4761, 0.5239 |
| cw (-w) | fast | A | 0.85856, 0.14144 | 0.66479, 0.33521 | 0.5646, 0.4354 | 0.5239, 0.4761 |
| cw (-w) | fast | B | 0.05973, 0.94027 | 0.16279, 0.83721 | 0.4158, 0.5842 | 0.4472, 0.5528 |
| ccw (+w) | mid5 | A | 0.92008, 0.07992 | 0.91014, 0.08986 | 0.5621, 0.4379 | 0.5583, 0.4417 |
| ccw (+w) | mid5 | B | 0.89031, 0.10969 | 0.90221, 0.09779 | 0.5550, 0.4450 | 0.5564, 0.4436 |
| cw (-w) | mid5 | A | 0.10969, 0.89031 | 0.09779, 0.90221 | 0.4450, 0.5550 | 0.4436, 0.5564 |
| cw (-w) | mid5 | B | 0.07992, 0.92008 | 0.08986, 0.91014 | 0.4379, 0.5621 | 0.4417, 0.5583 |
| ccw (+w) | slow20 | A | 0.99699, 0.00301 | 0.99699, 0.00301 | 0.5986, 0.4014 | 0.5986, 0.4014 |
| ccw (+w) | slow20 | B | 0.99699, 0.00301 | 0.99699, 0.00301 | 0.5986, 0.4014 | 0.5986, 0.4014 |
| cw (-w) | slow20 | A | 0.00301, 0.99699 | 0.00301, 0.99699 | 0.4014, 0.5986 | 0.4014, 0.5986 |
| cw (-w) | slow20 | B | 0.00301, 0.99699 | 0.00301, 0.99699 | 0.4014, 0.5986 | 0.4014, 0.5986 |
| ccw (+w) | slow40 | A | 0.99937, 0.00063 | 0.99937, 0.00063 | 0.6045, 0.3955 | 0.6045, 0.3955 |
| ccw (+w) | slow40 | B | 0.99937, 0.00063 | 0.99937, 0.00063 | 0.6045, 0.3955 | 0.6045, 0.3955 |
| cw (-w) | slow40 | A | 0.00063, 0.99937 | 0.00063, 0.99937 | 0.3955, 0.6045 | 0.3955, 0.6045 |
| cw (-w) | slow40 | B | 0.00063, 0.99937 | 0.00063, 0.99937 | 0.3955, 0.6045 | 0.3955, 0.6045 |
| ccw (+w) | slow100 | A | 0.99991, 0.00009 | 0.99991, 0.00009 | 0.6077, 0.3923 | 0.6077, 0.3923 |
| ccw (+w) | slow100 | B | 0.99991, 0.00009 | 0.99991, 0.00009 | 0.6077, 0.3923 | 0.6077, 0.3923 |
| cw (-w) | slow100 | A | 0.00009, 0.99991 | 0.00009, 0.99991 | 0.3923, 0.6077 | 0.3923, 0.6077 |
| cw (-w) | slow100 | B | 0.00009, 0.99991 | 0.00009, 0.99991 | 0.3923, 0.6077 | 0.3923, 0.6077 |

**By construction:** ε returns to its start 1.25 ε_EP at 2π and 4π (closed loop). That point is OUTSIDE Γ, so the state is never 'back on Γ' here; the table reports only whether it is a pure mode and which one.

γT = 40 winner depends on the start sheet: **NO**.

## M-matrix check (log-scaled propagation)

M = R⁻¹ U R (R = unit-norm right eigenvectors at the start point, columns [A, B]; D = RᵀR diagonal). Each start eigenvector is propagated separately with per-step renormalisation and a running log of its norm (Helios), so M is assembled without overflow. PT check uses U⁻¹ = adj(U) (exact for det U = 1), so it needs only the entries.

D = diag(+0.36+0.48i, +0.36-0.48i); D_A/D_B = -0.28+0.96i (|D_A/D_B| = 1.000000); |off-diag RᵀR| = 5.9e-16.

| speed | turn | M_ccw | M_cw | rel ‖M_cw − D⁻¹M_ccwᵀD‖ | \|M_AA\|/\|M_BB\| | \|M_AB\|/\|M_BA\| | σ1, σ2 (ccw, computed) | σ1/σ2 | det M_ccw (exact 1) | rel PT residual | u: hi-freq frac | D⁻¹w: hi-freq frac |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fast (γT=1) | 2π | [[+1+0.337583i, +0.257036-0.342714i], [+0.159613+0.212818i, +1-0.337583i]] | [[+1+0.337583i, +0.159613-0.212818i], [+0.257036+0.342714i, +1-0.337583i]] | 6.2e-15 | 1.000000 | 1.61036 | 1.406, 0.711 | 1.98 | +1+3.88578e-16i | 2.8e-15 | 0.46165 | 0.53835 |
| fast (γT=1) | 4π | [[+1+0.675165i, +0.514071-0.685428i], [+0.319227+0.425636i, +1-0.675165i]] | [[+1+0.675165i, +0.319227-0.425636i], [+0.514071+0.685428i, +1-0.675165i]] | 1.1e-14 | 1.000000 | 1.61036 | 1.912, 0.523 | 3.66 | +1-1.22125e-15i | 4.9e-15 | 0.43332 | 0.56668 |
| mid5 (γT=5) | 2π | [[+1+2.28853i, +4.26916-5.69221i], [+0.441644+0.588858i, +1-2.28853i]] | [[+1+2.28853i, +0.441644-0.588858i], [+4.26916+5.69221i, +1-2.28853i]] | 4.2e-15 | 1.000000 | 9.66652 | 7.977, 0.125 | 63.6 | +1+4.42424e-14i | 2.5e-15 | 0.10632 | 0.89368 |
| mid5 (γT=5) | 4π | [[+1+4.57705i, +8.53832-11.3844i], [+0.883288+1.17772i, +1-4.57705i]] | [[+1+4.57705i, +0.883288-1.17772i], [+8.53832+11.3844i, +1-4.57705i]] | 1.9e-14 | 1.000000 | 9.66652 | 15.77, 0.0634 | 249 | +1+5.46202e-13i | 1.3e-14 | 0.09701 | 0.90299 |
| slow20 (γT=20) | 2π | [[+1+498.835i, +5444.33-7259.1i], [+16.4541+21.9387i, +1-498.835i]] | [[+1+498.835i, +16.4541-21.9387i], [+5444.33+7259.1i, +1-498.835i]] | 1.4e-14 | 1.000000 | 330.881 | 9101, 0.00011 | 8.28e+07 | +1-3.91847e-09i | 9.0e-15 | 0.00301 | 0.99699 |
| slow20 (γT=20) | 4π | [[+1+997.671i, +10888.7-14518.2i], [+32.9081+43.8775i, +1-997.671i]] | [[+1+997.671i, +32.9081-43.8775i], [+10888.7+14518.2i, +1-997.671i]] | 5.8e-12 | 1.000000 | 330.881 | 1.82e+04, 5.49e-05 | 3.31e+08 | +1-2.49465e-08i | 9.8e-13 | 0.00301 | 0.99699 |
| slow40 (γT=40) | 2π | [[+1+2.3097e+06i, +5.5254e+07-7.3672e+07i], [+34757.7+46343.6i, +1-2.3097e+06i]] | [[+1+2.3097e+06i, +34757.7-46343.6i], [+5.5254e+07+7.3672e+07i, +1-2.3097e+06i]] | 1.6e-14 | 1.000000 | 1589.69 | 9.215e+07, 1.77e-08 | 5.21e+15 | +1.60958+0.270269i | 1.2e-14 | 0.00063 | 0.99937 |
| slow40 (γT=40) | 4π | [[+0.512437+4.6194e+06i, +1.10508e+08-1.47344e+08i], [+69515.3+92687.1i, +0.60181-4.6194e+06i]] | [[+1.39144+4.6194e+06i, +69515.3-92687.1i], [+1.10508e+08+1.47344e+08i, +0.441682-4.6194e+06i]] | 3.2e-08 | 1.000000 | 1589.69 | 1.843e+08, 5.01e-09 | 3.68e+16 | +0.90341-0.165625i | 1.7e-07 | 0.00063 | 0.99937 |
| slow100 (γT=100) | 2π | [[-31073.5+8.41674e+17i, +5.27206e+19-7.02941e+19i], [+4.83738e+15+6.44983e+15i, -58981.1-8.41674e+17i]] | [[-127792+8.41674e+17i, +4.83738e+15-6.44983e+15i], [+5.27206e+19+7.02941e+19i, +108475-8.41674e+17i]] | 5.0e-14 | 1.000000 | 10898.6 | 8.788e+19, 1.82e+03 | 4.82e+16 | +1.38328e+22-1.59465e+23i | 4.8e-14 | 0.00009 | 0.99991 |
| slow100 (γT=100) | 4π | [[-1.3363e+23+2.03615e+23i, +8.28687e+24-1.72104e+25i], [+1.46226e+20+2.32834e+21i, -3.5411e+22-1.79513e+23i]] | [[+8.60232e+22+8.57642e+22i, -4.59575e+20-5.10298e+20i], [+1.25565e+25+1.77447e+24i, -7.03462e+22-1.38318e+22i]] | 8.8e-01 | 1.331071 | 8187.84 | 1.91e+25, 5.01e+08 | 3.81e+16 | +8.52149e+33-4.35832e+33i | 1.3e+00 | 0.00009 | 0.99984 |

'hi-freq frac' = weight of the higher-frequency mode. ccw output = u; cw output = D⁻¹w.

⚠ Precision: slow40 2π, slow40 4π, slow100 2π, slow100 4π: det M ≠ 1. Since det U = 1 exactly, σ2 = 1/σ1 and σ1/σ2 = σ1²; once σ1² approaches 1/eps ≈ 4.5e15 (σ1 ≈ 9e7 at γT = 40), the subdominant singular value is lost to round-off even with log-scaled propagation (log scaling prevents overflow, not cancellation). In those rows the computed σ2, σ1/σ2 and det are NOT reliable; the M entries, the ratios |M_AA|/|M_BB| and |M_AB|/|M_BA|, u and D⁻¹w come from the dominant part and are reliable as long as the transpose residual stays small. The drive-table weights are reliable in any case (renormalised ψ; dt-halving converged).

⚠ Entries unreliable (relative transpose residual > 1e-6, i.e. round-off has reached the dominant part too): slow100 4π. Do not use the M entries or ratios in these rows.

Output directions at γT = 40 as overlaps |<R_k|v>|/norms with the right eigenvectors (R_A, R_B are not orthogonal here, |<R_A|R_B>|/norms = 0.800000):

- 2π: ccw output u → (R_A 0.999891, R_B 0.808764); cw output D⁻¹w (from M_ccw) → (R_A 0.808764, R_B 0.999891); cw output from the direct cw propagation → (R_A 0.808764, R_B 0.999891).
- 4π: ccw output u → (R_A 0.999891, R_B 0.808764); cw output D⁻¹w (from M_ccw) → (R_A 0.808764, R_B 0.999891); cw output from the direct cw propagation → (R_A 0.808764, R_B 0.999891).

Final states at 4π, γT = 40, overlap with (R_A, R_B), both start sheets (labelling-artifact test):

- ccw (+w) start A: (0.999891, 0.808764) → A lower-frequency
- ccw (+w) start B: (0.999891, 0.808764) → A lower-frequency
- cw (-w) start A: (0.808764, 0.999891) → B higher-frequency
- cw (-w) start B: (0.808764, 0.999891) → B higher-frequency

u and D⁻¹w land on DIFFERENT eigenvectors at γT = 40: **YES** (ccw → R_A, cw → R_B).

PT map ψ → σx ψ* on the eigenvectors, normalised overlaps |<R_k|PT R_i>| (row i = A, B; columns k = A, B):
- at 1.25 ε_EP: A → (1.000000, 0.800000), B → (0.800000, 1.000000)
- at 0.75 ε_EP (contrast): A → (0.750000, 1.000000), B → (1.000000, 0.750000)
PT maps each eigenvector to itself at 1.25 ε_EP: **YES** (Helios predicted yes outside Γ); at 0.75 ε_EP it maps A↔B: YES. With PT eigenvectors mapped to themselves the PT relation constrains |M_AA| = |M_BB| instead of |M_AB| = |M_BA|, which is what the table shows.

## Checks

- Sanity run γT = 0.01, start A (ccw): fidelity = 0.99999801 at 2π, 0.99999204 at 4π.
- Fixed ε = 1.25 ε_EP, mixed start: ΔΓ = difference of Im λ = 1.67e-16 (equal decay rates), so the weight ratio should stay constant:

| γt | ratio measured | expected (initial ratio)·e^{−2ΔΓt} | rel. error |
|---|---|---|---|
| 1 | 1.000000e+00 | 1.000000e+00 | 3.1e-15 |
| 2 | 1.000000e+00 | 1.000000e+00 | 5.8e-15 |
| 5 | 1.000000e+00 | 1.000000e+00 | 9.8e-15 |
| 10 | 1.000000e+00 | 1.000000e+00 | 2.0e-14 |

## a↔b swap check (σx relabelling)

a = 0.49348, b = 0.12337 (swapped in memory only; handoff files untouched), same v, start 1.25 ε_EP, γT = 40 and 100. With the shared decay removed, a↔b is γ → −γ, a basis relabelling by σx; the eigenvalues depend on γ² and are unchanged. Expected: the winning FREQUENCY per direction is unchanged and the winning state is the σx image of the old one. Eigenvalues after the swap: λ_A = -0.138791-0.308425i, λ_B = +0.138791-0.308425i.

| speed | direction | start | winner 4π (swapped) | winner 4π (original) | same frequency (2π and 4π) | ‖<ψ_swap|σx ψ_orig>‖ | ‖<ψ_swap|σx ψ_orig*>‖ | ‖<ψ_swap|ψ_orig>‖ |
|---|---|---|---|---|---|---|---|---|
| slow40 | ccw (+w) | A | A lower-frequency (w=0.99937) | A lower-frequency (w=0.99937) | YES | 1.000000 | 0.576140 | 0.576140 |
| slow40 | ccw (+w) | B | A lower-frequency (w=0.99937) | A lower-frequency (w=0.99937) | YES | 1.000000 | 0.576140 | 0.576140 |
| slow40 | cw (-w) | A | B higher-frequency (w=0.99937) | B higher-frequency (w=0.99937) | YES | 1.000000 | 0.576140 | 0.576140 |
| slow40 | cw (-w) | B | B higher-frequency (w=0.99937) | B higher-frequency (w=0.99937) | YES | 1.000000 | 0.576140 | 0.576140 |
| slow100 | ccw (+w) | A | A lower-frequency (w=0.99991) | A lower-frequency (w=0.99991) | YES | 1.000000 | 0.590835 | 0.590835 |
| slow100 | ccw (+w) | B | A lower-frequency (w=0.99991) | A lower-frequency (w=0.99991) | YES | 1.000000 | 0.590835 | 0.590835 |
| slow100 | cw (-w) | A | B higher-frequency (w=0.99991) | B higher-frequency (w=0.99991) | YES | 1.000000 | 0.590835 | 0.590835 |
| slow100 | cw (-w) | B | B higher-frequency (w=0.99991) | B higher-frequency (w=0.99991) | YES | 1.000000 | 0.590835 | 0.590835 |

Winning frequency per direction unchanged after the swap: **YES**. (Start sheets are relabelled by the swap too, so rows are matched by sheet label.) v → −v is the same situation via σz (not run).

## Missing mechanism

Definition (same as RESULTS.md): **YES** only if ccw and cw give DIFFERENT physical winners (here: higher- vs lower-frequency mode) for the same start sheet; NO if they are the same. Full chiral conversion = YES and independent of the start sheet. Primary: γT = 40 and 100 at 4π.

Per speed / time: fast 2π NO, 4π NO; mid5 2π YES, 4π YES; slow20 2π YES, 4π YES; slow40 2π YES, 4π YES; slow100 2π YES, 4π YES.
Full chiral (start-sheet independent): fast 2π NO, 4π NO; mid5 2π YES, 4π YES; slow20 2π YES, 4π YES; slow40 2π YES, 4π YES; slow100 2π YES, 4π YES.
Driven winner equals tracked label: fast 2π NO, 4π YES; mid5 2π NO, 4π NO; slow20 2π NO, 4π NO; slow40 2π NO, 4π NO; slow100 2π NO, 4π NO.

**missing mechanism (start 1.25 ε_EP): YES**

Reason: γT = 40: ccw → lower-frequency, cw → higher-frequency; γT = 100: ccw → lower-frequency, cw → higher-frequency at 4π, from either start sheet — the winner is set by the direction, not by the start sheet.

**Verdict (Helios wording):** the toy already has the mechanism; whether it shows depends on the start point. Inside Γ (0.75 ε_EP, RESULTS.md) the winner is direction-independent; outside Γ (1.25 ε_EP, this file) it is direction-dependent. Both come from the same H_A with nothing added. The earlier 'missing mechanism: NO' in RESULTS.md stands; this run shows where the effect lives, not something that was missing.

## Comparison with Venus's independent integrator (pattern only)

Venus's reference used sample values a = 1, b = 2, v = 1 (not the handoff values), so only the pattern is compared; mode labels can be mirrored by sign(v) and the a/b order. Her pattern at 1.25 ε_EP: γT = 40 → ccw ends on one frequency mode (~99.94%) from either start sheet, cw on the other, at 2π and 4π; γT = 5 → same lean, ~90/10; |M_AA| = |M_BB|; |M_AB|/|M_BA| ~ 0.1 (γT = 5), ~6e-4 (γT = 40); transpose holds to ~1e-7.

This run: γT = 40 → ccw lower-frequency (w = 0.99937 from A, 0.99937 from B), cw higher-frequency (w = 0.99937, 0.99937), same at 2π; γT = 5 → w ≈ 0.910/0.902 (ccw from A/B), 0.902/0.910 (cw). |M_AA|/|M_BB| = 1.000000 (γT=5), 1.000000 (γT=40); |M_AB|/|M_BA| = 9.667 (γT=5), 1590 (γT=40), i.e. the inverse of her ratios (labels mirrored: 1/9.667 = 0.103, 1/1590 = 0.00063); transpose residual 3.2e-08 (relative, γT=40, 4π). Pattern agrees; digits are not expected to match (different a, b, v).

## Literature (expected only, not checked)

Expected from EP-encircling work in C:\Users\Akitt\Grok\pdf\ (Milburn et al. 1410.1882, quasiadiabatic dynamics; Hassan et al. 1706.09938, exact driven 2x2; Doppler et al. 1603.02325, mode switching): for slow loops in passive/lossy two-mode systems the final mode is fixed by the encircling direction rather than the start state (chiral switching), and the start point can change whether and how this shows. The papers were not read or compared quantitatively here; no agreement is claimed.

Scope: two-mode toy; two start points so far (0.75 ε_EP in RESULTS.md, 1.25 ε_EP here).
Plot: outputs/weights_vs_theta_start1p25.png (w_A vs θ, all runs; w_B = 1 − w_A).

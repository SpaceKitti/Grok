# pairA-qg-loss: a gravity-side loss that is not a copy of H_A, and a D6/D7 test with it

Run: `python run.py` (Grok\.venv python, PYTHONIOENCODING=utf-8). It writes RESULTS.md and stops. No folder is loaded or imported: the numbers are hard-coded, with their source named in `loss_term.py`.

No claim of QG, a JT dual, or an Einstein solution. A and B WRITE, C held.

## Inputs (numbers only)
Hard-coded:
- ε_EP = 0.51368066
- λ_EP = −0.308425i
- v = −0.360253
- Γ = [−ε_EP, ε_EP]
- F_JT = ε² − ε_EP²

Source: pairA-qg-handoff / pairA-jt-4d values as given by Akitti.

H_A is not imported, and a and b (0.12337, 0.49348) are not used in the construction. They appear only inside `H_try.copy_test`, in a locally defined H_A that is clearly marked.

Caveat, stated up front: the three input numbers already fix a and b up to a swap, because λ_EP = −i(a+b)/2 and ε_EP = |b−a|/(2|v|). So "not using a, b" is nominal. Any operator built from (λ_EP, ε_EP, v) can re-encode H_A, which is why the copy test is needed.

## Loss term
- **T1:** Im V = η_g F_JT = η_g(ε² − ε_EP²).
- **T2:** η_g(ε²/ε_EP² − 1). This is T1 with η_g → η_g/ε_EP², i.e. a rescaling only.
- **T3:** boundary flux. Not used.

η_g is a new coupling, scanned on a log grid and never set from a or b.

## Operator
H_try(ε) = H_curve(ε) + i η_g F_JT(ε) M, with H_curve(ε) = λ_EP·1 + v[[ε, ε_EP], [−ε_EP, −ε]].
- H_curve has zeros of its discriminant at ±ε_EP, and y² = 4v²(ε² − ε_EP²).
- Placement P0: M = 1 (scalar). It shifts both eigenvalues equally, so it cannot select a mode.
- Placement P1: M = σ_z, the same matrix direction that multiplies ε in H_curve. The loss then acts as an imaginary shift of the dilaton-like variable, vε → vε + iη_g F_JT, which splits the modes.
- A diagonal loss on one mode, iη_g F diag(1, 0) = (iη_g F/2)(1 + σ_z), is P1 with η_g/2 plus a scalar. So it adds nothing new and is not run separately.
- The loss term vanishes at ±ε_EP in both placements.

## Spectrum report
For each placement and η_g, the report covers:
- the zeros of the discriminant (EPs), which are the roots of a polynomial in ε;
- whether ±ε_EP survive;
- any new EPs;
- 2π swap / 4π return around each EP by continuation;
- which EPs the r = 0.25 ε_EP drive loop encloses.

## Copy test
- **YES = copy:** there is a constant (ε-independent) invertible S with S H_try(ε) S⁻¹ = H_A(ε) for all ε, possibly after an affine reparametrisation ε → αε + β, with H_A = [[−ia, vε], [vε, −ib]] defined locally.
  - At a single ε, any two 2×2 matrices with the same eigenvalues are similar, which is why only the constant-S test is meaningful.
  - Numerically: the smallest singular value of the stacked linear system S P_k − Q_k S = 0 over 6 sample ε values (relative), minimised over complex α, β with several starts. Copy if it is ≤ 1e-8 and S is invertible.
- **Dynamical copy** (extra, stricter): the same test on the traceless parts, H − tr(H)/2. An ε-dependent scalar c(ε)·1 changes only the norm, not the normalised dynamics or the winners. So a dynamical copy has the same D6/D7 physics as H_A even if the strict test says NO.
- **Spectrum test:** max |eig(H_try) − eig(H_A)| over a complex ε grid, for every η_g scanned. If the spectra match at some η_g, the report checks whether H_try reduces to H_A there.
- Output: YES (FAIL, still a copy) or NO (continue), per placement and η_g.

## Drive test
- Loop: ε(θ) = ε_EP + r e^{i(sθ + φ₀)}, r = 0.25 ε_EP around +ε_EP. φ₀ = π for the start at 0.75 ε_EP and φ₀ = 0 for 1.25 ε_EP. Two turns; s = +1 ccw, −1 cw.
- The ±ε_EP EPs are kept by construction (the loss vanishes there). New EPs are reported, not driven.
- Time scale: γ_g = ½ max over the loop of |Im(λ₁ − λ₂)| of H_try itself. T = γ_g T / γ_g with γ_g T = 40 and 100.
- Integration: exact 2×2 midpoint propagator, ≥ 2000 steps per turn and γ_g dt ≤ 0.01, normalised each step. A dt-halving check is run at γ_g T = 40.
- Weights: left-eigenvector (biorthogonal) weights at the start/end point. Modes are named slower/faster-decaying when the decays differ, and higher/lower-frequency otherwise.
- **D6-like:** for both start modes, the ccw and cw winners are equal and equal the slower-decaying mode, at both speeds and both turns.
- **D7-like:** for both start modes, ccw ≠ cw, and each direction's winner is independent of the start mode, at both speeds and both turns.
- **NO:** anything else.
- η_g grid: P0 at {0, 0.1, 1, 10}; P1 at {0, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 1, 3, 10}.

## Grade (fixed before running)
- **HAVE:** a placement with copy test NO (strict) **and** dynamical copy NO, D6-like at 0.75 **and** D7-like at 1.25.
  - Robust if it holds on a run of consecutive η_g > 0 grid points spanning at least one decade.
  - Otherwise it is flagged "single tuned value".
- **PARTIAL:** not a copy, but D6/D7 fail for every η_g > 0.
- **MISSING:** H_A had to be pasted, or every placement is a copy / dynamical copy.
- Extra flag (does not change the grade): the curve part H_curve is itself a constant-SU(2) rotation of H_A. So wherever D6/D7 hold at small η_g, they are inherited from H_curve, and the loss only perturbs them. This is judged by comparing weights with η_g = 0.

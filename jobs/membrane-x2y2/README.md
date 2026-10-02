# Job Six: membrane power counting and the x²y² toy

Folder: `C:\Users\Akitt\membrane-x2y2\` (TrinityOrb). Files: `run.py`, `RESULTS.md` (written only by
`run.py`), `x2y2_levels.png` (written by `run.py`), and this README. No git; Ledger pushes.

Run: `$env:PYTHONIOENCODING='utf-8'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py`
(about 2.7 min; sparse shift-invert `eigsh`, largest grid 399² per spinor sector).

## Spec summary

- **Stage A [standard]:** power counting for p-branes, p = 1, 2, 3, 5. `run.py` derives [T] = p+1,
  [φ] = (p−1)/2, the NG quartic coupling [g₄] = −(p+1), the Polyakov/σ-model coupling [g_σ] = 1−p and the
  Weyl weight p−1 with sympy, checking each of the two couplings two independent ways. Only p = 1 is
  renormalisable (Polyakov form) and Weyl invariant.
- **Stage B:** H_s = p_x² + p_y² + x²y² + s(xσ₃ + yσ₁) on [−L, L]², Dirichlet walls, 4th-order finite
  differences, s = 0, ½, 1. The steps are: an identity check of the valley wall (1−s)|x|; the lowest 6 levels
  for L = 4…12 (h = 0.08); a grid-convergence check at L = 12 (h = 0.08 vs 0.06); and a grade for each s.
- **Cost-saving identity:** P = σ₁⊗(x→−x) commutes with H_s, and the two sectors are unitarily equivalent
  (by y→−y). So only one scalar sector K₊ is diagonalised, and every level is a doublet of H. This is
  checked against the full 2-component H on a small grid in `run.py` [identity].

## What this toy is and isn't

- It **is** a 2-matrix caricature of the light-cone supermembrane matrix model. x²y² is the commutator
  potential −Tr[X,Y]² of two SU(2) matrices restricted to one direction each. Its classical valleys (the
  axes) are the toy version of the membrane's string-like flat directions. The s-term is a 2-state
  stand-in for the fermions. At s = 1, H₁ is unitarily equivalent (constant spin rotation, checked in
  `run.py`) to the supersymmetric model H = ½{Q, Q*} of de Wit–Lüscher–Nicolai, eq. (1.5).
- It **is not** the supermembrane. The true regularised supermembrane is the SU(N) matrix model of
  de Wit–Hoppe–Nicolai (9 bosonic N×N matrices + 16 real fermionic ones), with valleys along commuting
  matrices and a gauge constraint. Nothing here is a statement about large N, about bound states inside
  the continuum, or about the M-theory interpretation.
- s is an interpolation parameter [assumed input]. Only s = 1 is supersymmetric (H₁ = Q² ≥ 0). s = 0 is
  the bosonic membrane caricature (Simon's H₁), and s = ½ is a non-supersymmetric half-cancellation.
- **Scope [standard: beyond toy]:** this is a two-variable cartoon of the SU(2) membrane matrix model, not the
  full nine-dimensional model. It shows how a continuum can appear, but cannot establish the real model's single
  bound state at zero energy; both Sethi & Stern, *D-brane bound states redux*, Commun. Math. Phys. 194 (1998) 675,
  `hep-th/9705046`, and Yi, *Witten index and threshold bound states of D-branes*, Nucl. Phys. B 505 (1997) 307,
  `hep-th/9704098`, prove that SU(2) threshold bound state [standard: beyond toy].

## Results (from RESULTS.md; numbers are not re-derived here)

- **Valley identity [identity]: PASS.** The transverse ground level → (1−s)|x|. The residual is exactly the
  second-order shift −s²/(4(1+s)x²) from the yσ₁ term (residual·x² = −0.04167 at s = ½ and −0.1250 at
  s = 1 for x = 4…16).
- **s = 0: PASS.** Levels converge in L (relative change L = 10→12 below 3e-10 for all six). E₁ = 1.108222, and
  E₂ = E₃ = 2.378632 are degenerate by the x↔y symmetry.
- **s = ½: PASS.** Converged (relative change of E₁–E₃ ≤ 1.1e-7, E₆ 6.7e-5). E₁ = 0.835795 lies below the s = 0
  value (weaker wall).
- **s = 1: PASS.** All six levels fall monotonically. The local slope d lnE₁/d lnL between L = 10 and 12 is
  −2.12 (window −2.3…−1.7), and the fitted slopes over L = 4…12 are −2.18 … −1.61 (the higher levels leave the
  valley regime at small L). E_k/E₁ = 1, 4.01, 9.02, 16.0, 25.0, 35.9 ≈ k², and ℓ_k = kπ/√E_k ≈ 23.0 for all k
  at L = 12. So the low states are a free particle in a 1D box running the whole length of one valley line
  (2L = 24, minus ≈1 of end/junction correction) [hive-interpretation]. The slope sits a little below −2
  because ℓ_eff ≈ 2L − const [finite-size].
- **Grid [grid-step]:** at L = 12 the worst relative error of the h = 0.08 levels (Richardson, h⁴) is
  7.7e-6 (s = 0), 2.3e-5 (s = ½) and 6.0e-3 (s = 1, E₁). h·√L = 0.28 at L = 12, so the "Δy ≪ L^{-1/2}" requirement is
  met only moderately; s = 1 is the sensitive case because the answer is a small difference of large
  zero-point terms.
- **s = 1 scope [standard: beyond toy; hive-interpretation]:** a finite-box scan cannot detect levels embedded
  inside the continuum, as dWLN say, "cannot at present rule out". In matrix theory this continuum is read as the
  membrane breaking up into separate pieces (BFSS 1996, `hep-th/9610043`), not as a broken theory.

## Literature checks

**de Wit, Lüscher & Nicolai (1989), Section 1 (Introduction), pp. 136–139, eqs. (1.3)–(1.13).** Their toy is
H = ½{Q, Q*} = [[−Δ + x²y², x + iy], [x − iy, −Δ + x²y²]] (eq. 1.5), which is our s = 1. Quotes:

> "It has been known for some time that the associated bosonic hamilton operator H_B = −Δ + x²y²
> nevertheless has a purely discrete spectrum [7]. One way to see this starts from the operator
> inequality H_B ≥ |x| (1.6), which one obtains by regarding H_B as a harmonic oscillator in the
> variable y at fixed x." (p. 137)

> "… whereas the system looked like a harmonic oscillator in the vicinity of the potential valleys
> before, it now looks like a supersymmetric harmonic oscillator, and since the ground state energy of
> this oscillator vanishes, it does not give rise to a confining force (the bound analogous to the
> inequality (1.6) becomes trivial)." (p. 138)

> "This is just enough to cancel the bosonic zero-point energy associated with the oscillations of the
> y-coordinate about the bottom of the potential valley" (p. 138, after eq. 1.9: Ψ†HΨ = H_B − x).
> "Eq. (1.11) also implies that the spectrum of H is the whole interval [0, ∞)." (p. 139)

Check: our valley identity is their eqs. (1.6)/(1.9) with the spin cancellation scaled by s, and the
numbers confirm it. Their Gaussian (1.10), exp(−½|x|y²), is the transverse ground state we diagonalise.
Our extra observation is that the off-diagonal yσ₁ piece leaves a −1/(8x²) tail at s = 1 [computed].
This vanishes along the valley, consistent with their (1.11). They also caution (p. 135) that they
"cannot at present rule out the existence of discrete eigenvalues within the continuum or at its lower
end", and a finite-box scan cannot settle that either. Their p. 137 remark that "all higher p-branes
suffer from such potential instabilities", while strings are confined by the oscillator potential,
matches Stage A's p = 1 vs p ≥ 2 split.

**B. Simon (1983), Section 1 and Section 2 ("First proof: zero point oscillator motion"), pp. 210–212.**
The PDF is a scan, and the OCR drops the displayed formulas of §2, so the inequalities below are
re-typed from the surrounding text and the eq. (5) fragment:

> "The simplest example of this genre is the two dimensional Hamiltonian H₁ = −∂²/∂x² − ∂²/∂y² + x²y² …
> Both H₁ and H₂ have discrete spectrum with infinite classical phase space volumes." (§1, p. 210)

> §2: "Thus, treating y as c-number, [−∂²/∂y² + x²y² ≥ |x|] … Using symmetry in x and y and adding, we see
> that H₁ ≥ ½(−Δ + |x| + |y|) ≡ H₃ (5). Since H₃ has discrete spectrum, so does H₁." (pp. 211–212)

Check: this is exactly our s = 0 valley check (the lowest transverse level is |x|; §5 gives all of them,
ε_j(x) = (2j+1)|x|, matching (2j+1)|x| from the oscillator). Simon's §2 remark that N(E) grows like
E^{3/2} ln E rather than E³ is not tested here. The "note added in proof" (Rellich 1948) states the general
criterion: discrete spectrum if the lowest transverse eigenvalue → ∞ along every direction. That is the
(1−s)|x| → ∞ condition for s < 1.

**s = ½ discreteness, one line [identity]:** H_s = (1−s)·(H₀⊗1) + s·H₁, and H₁ = Q² ≥ 0 (dWLN). So
H_s ≥ (1−s) H₀⊗1, and by min–max E_k(s) ≥ (1−s)E_k(0), which gives a discrete spectrum for every s < 1 by
Simon. Consistency with RESULTS: E(½)/E(0) at L = 12 is 0.707–0.876 ≥ 0.5 [computed].

## Caveats

- A finite Dirichlet box always has a discrete spectrum. The s = 1 "continuum" is inferred from the
  1/L² scaling and the k² pattern, not seen directly [finite-size].
- Grid: 4th-order FD at h = 0.08. The transverse grid error grows like h⁴|x|³ and is largest at the wall
  (7.7% of E₁ at x = L = 12 in the 1D edge table). The 2D level error that matters is ~0.6% for E₁ at s = 1,
  biasing the slope by roughly −0.01 [grid-step].
- Grading thresholds (converge < 1e-3, slope window −2.3…−1.7) were fixed in `run.py` before the first run.
- [post-hoc]: the ungraded "s = ½ levels below s = 0 levels" line was first coded as "at every L". It
  failed only at L = 4 (E₄: 3.178 vs 3.145, a squeezed-box effect [finite-size]), so it is now printed per L.
  The comparison is now emitted from the computed level arrays rather than typed into `run.py`.
- The Born–Oppenheimer comparison (1/2)^{2/3} = 0.630 for the s = ½/s = 0 ratio is a rough 1D-valley
  picture only [hive-interpretation]. The low states are not deep in the valleys.
- Stage A is perturbative power counting only. It says nothing about non-perturbative completions.

## Tag key

[computed] produced by `run.py`; [identity] exact algebraic statement checked to machine precision;
[assumed] modelling choice; [assumed input] parameter set by hand (s, L, h); [standard] textbook result;
[post-hoc] changed after seeing a result; [finite-size] box-size artefact; [grid-step] discretisation
effect; [prediction] expectation stated before the run; [hive-interpretation] our reading, not a theorem.

## References

- B. de Wit, M. Lüscher and H. Nicolai, "The supermembrane is unstable", Nucl. Phys. B320 (1989) 135.
  PDF: `C:\Users\Akitt\Grok\pdf\NPB320_135_deWit_Luscher_Nicolai_supermembrane_unstable.pdf` (§1 read).
- B. Simon, "Some quantum operators with discrete spectrum but classically continuous spectrum",
  Ann. Phys. 146 (1983) 209. PDF: `C:\Users\Akitt\open-problems\03_membrane_renormalization\AnnPhys146_209_Simon_discrete_spectrum_x2y2.pdf`
  (§§1, 2, 5 and the note added in proof skimmed).
- B. de Wit, J. Hoppe and H. Nicolai, "On the quantum mechanics of supermembranes", Nucl. Phys. B305
  [FS23] (1988) 545: the SU(N) matrix regularisation that this toy caricatures (on disk; not re-read).
- E. Bergshoeff, E. Sezgin and P. K. Townsend, "Supermembranes and eleven-dimensional supergravity",
  Phys. Lett. B189 (1987) 75: the supermembrane action behind the p = 2 row of Stage A (on disk; not re-read).
- F. Rellich (1948), cited by Simon's note added in proof for the general valley criterion.
- F. Sethi and M. Stern, "D-brane bound states redux," Commun. Math. Phys. 194 (1998) 675, hep-th/9705046 [standard: beyond toy].
- P. Yi, "Witten index and threshold bound states of D-branes," Nucl. Phys. B 505 (1997) 307, hep-th/9704098 [standard: beyond toy].
- T. Banks, W. Fischler, S. H. Shenker and L. Susskind, "M Theory As A Matrix Model: A Conjecture," arXiv:`hep-th/9610043` [hive-interpretation].
- Context: `C:\Users\Akitt\open-problems\03_membrane_renormalization\README.md` (read only).

## Post-run / sign-off

- Post-run fold-in (2 Oct 2026): `run.py` now prints the H_s interpolation, rotated Q² identity, min–max/Simon note,
  H₁ positivity at every L, and domain monotonicity per s and per level; the weaker-wall comparison remains ungraded
  and [post-hoc], with its indefinite-sign caveat. Typed-in comparison values and other typed result prose were
  replaced by values formatted from computed arrays.
- Post-run identity [identity]: H_s = (1−s)H₀ + sH₁; after the fixed spin rotation H₁ = Q² with
  Q = σ₁p_x + σ₃p_y + σ₂xy and Q² = p² + x²y² + yσ₃ − xσ₁. Thus H₁ ≥ 0,
  E_k(H_s) ≥ (1−s)E_k(H₀), and Simon gives discreteness for every s < 1.
- Post-run checks [computed]: H₁ positivity passes at L = 4, 6, 8, 10, 12; domain monotonicity passes for
  every s ∈ {0, ½, 1} and every one of the six levels. The ungraded [post-hoc] comparison retains
  H_{1/2} − H₀ = ½(xσ₃ + yσ₁), which has no fixed sign and therefore forces no ordering.
- Post-run scope lines: the two-variable/cartoon limitation, the real-model zero-energy bound-state references, the
  dWLN embedded-continuum caveat, and the BFSS breakup [hive-interpretation] are recorded above.
- Signed off 2026-10-02: Venus PASS (maths); Helios PASS (physics, toy).
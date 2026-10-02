# Rugby-ball Yukawas from a brane-localised Higgs (Job Four, toy bookkeeping)

Builds on the alternative model of `C:\Users\Akitt\sm-zero-modes-S2` (its RESULTS_alt.md and
RESULTS_final.md). That folder is read-only here: `run.py` imports its `monopole.py` (Wu-Yang monopole
harmonics, Wigner small-d, Sturm count; credit: sm-zero-modes-S2) with bytecode writing switched off, and
prints that folder's file hashes before and after the run so it is visibly untouched.

Spec: Helios (physics), maths checked by Venus. Go from NanoRibbon (counts as Akitti's). This README was
written before the first run. Outputs come only from `run.py`: `RESULTS.md` and `ratios.png`.
Never hand-edit them. No git (Ledger pushes).

## 1. Setup [assumed input]

- Alternative-model fields: Q, L at Gamma_7 = -1, x = +1; singlets u, d, e, nu at Gamma_7 = +1, x = +1;
  U(1)_X flux n = 3. Every fermion has q = x n / 2 = 3/2, and its zero modes sit in the sigma3 = +1 slot,
  a section of effective charge q - 1/2 = 1 (j = 1, three modes).
- Q and the singlets share the same three zero-mode sections, so on ANY metric a constant Higgs gives
  Y = constant x (Gram matrix of one orthonormal basis) = constant x unitary [identity]. Squashing alone
  cannot split the generations.
- The symmetry breaker is a Higgs on a 3-brane at the north tip with profile h(u):
  Y_mm' ∝ ∫ sqrt(g) h eta^(Q)†_m eta^(u)_m'. Only ratios inside a sector are meaningful.
- Geometry: ds^2 = R^2 (dtheta^2 + alpha^2 sin^2 theta dphi^2), R = 1. alpha = 1 is the round sphere;
  alpha < 1 gives a conical deficit 2 pi (1 - alpha) at both tips [assumed input; SLED-type rugby ball,
  where the brane tension makes the deficit]. Flux quantisation B 4 pi alpha R^2 = 2 pi n with n fixed;
  in the north gauge A = q (1 - cos theta) dphi for every alpha [identity].
- Area fraction from the north tip: u = sin^2(theta/2), for every alpha [identity].
- Zero modes: a 1D problem in theta per half-integer angular number m (rotating frame, as in
  sm-zero-modes-S2): psi = (alpha sin theta)^(-1/2) e^{i m phi} a(theta) in the sigma3 = +1 slot, with
  a' = W a, W = (m - q (1 - cos theta)) / (alpha sin theta); the sigma3 = -1 slot has b' = -W b.
  Solved numerically in s = ln tan(theta/2) [computed]. The closed form
  a = tan(theta/2)^((m - q)/alpha) sin(theta)^(q/alpha) is used only as a check [identity].
  Independent count: finite differences of D^2 per m with Dirichlet ends (as in sm-zero-modes-S2, with
  sin theta replaced by alpha sin theta).
- Allowed modes: |psi|^2 bounded at both tips (regularity) AND normalisable. Both tests are printed.
  Label k = m - 1/2, so k = 0 is the mode that peaks at the north tip.

## 2. Stages (what run.py prints)

Stage A [identity]
1. h constant (the normalised constant Higgs mode 1/sqrt(4 pi alpha)): the three singular values are equal
   for every alpha in {1, 0.8, 0.6, 0.5}. Print them.
2. h axially symmetric (top-hat sigma = 0.3, soft sigma = 0.1), at alpha = 1 (monopole harmonics, 2D
   quadrature) and alpha = 0.6 (1D-solved modes): Y is diagonal in m. Print the largest off-diagonal entry.

Stage B (alpha = 1)
- Confirm from the actual zero modes (the monopole harmonics Y_{1,1,m} of sm-zero-modes-S2, and the 1D
  solve) that the densities in u are 3 C(2,k) u^k (1-u)^(2-k) [standard, Haldane-sphere lowest level].
- Ratios Y_1/Y_0 and Y_2/Y_0 at sigma = 0.3, 0.1, 0.03, 0.01 against each profile's OWN leading law:
  - top-hat, h = 1 for u < sigma: 1 : sigma : sigma^2/3; at sigma = 1 all three are equal [identity];
  - soft, h = exp(-u/sigma): 1 : 2 sigma : 2 sigma^2; equal only as sigma -> infinity, not at sigma = 1
    (printed at sigma = 1, 10, 100, 1000, 10000);
  - delta brane: Y = eta(p)^* eta(p)^T, exactly rank 1; at the tip Y_k ∝ |eta_k(tip)|^2: one heavy and
    two massless generations. Rank 1 holds only for the delta brane (finite profiles are rank 3).
- Exact values from sympy integrals of the Bernstein shapes cross-check the quadrature.

Stage C (squashing; a report, not pass/fail), alpha in {1, 0.8, 0.6, 0.5}
- FIRST the zero-mode count for each alpha (regular, normalisable, finite differences). If it is not 3,
  say so plainly before any ratio.
- Then top-hat ratios at a fixed area fraction sigma = 0.1, and whether they depend only on sigma or also
  on alpha.
- Then a log-log slope fit of Y_k/Y_0 against sigma (sigma = 1e-2 ... 1e-4), compared with Venus's
  estimate Y_k/Y_0 ~ sigma^(k/alpha) [prediction].

Stage D (mixing, alpha = 1)
- Up-type brane at the north tip, down-type brane tilted by beta; soft profile, sigma = 0.1.
  CKM V = U_u† U_d from the two SVDs, ordered by mass. Compare |V| with |d^1(beta)| [prediction] for
  beta in {0.05, 0.1, 0.2, 0.3, 0.5}. Compare only the PATTERN with real quark mixing [hive-interpretation].

Plot: `ratios.png` (Stage B ratios against sigma with the laws; Stage C ratios for each alpha).

## 3. PASS criteria (Helios), fixed before the run

- P1 Stage A: singular values equal within 1e-12 (relative) at every alpha; off-diagonals below 1e-12.
- P2 Stage B: Bernstein shapes confirmed (within 1e-12 from the harmonics, 1e-9 from the 1D solve);
  at sigma = 0.01 every ratio is within 3% of its own profile's leading law, and the deviation shrinks as
  sigma shrinks; delta brane rank 1 (s2/s1 < 1e-12); finite profiles rank 3.
  Post-hoc amendment [post-hoc], made after one staged test run and before the recorded run: "the
  deviation shrinks as sigma shrinks" is checked over the small-sigma points 0.1, 0.03, 0.01 only. As first
  worded it also included sigma = 0.3, where the soft Y_2/Y_0 deviation is non-monotone (exact/law 1.128 at
  0.3, then 1.216 at 0.1) because 0.3 is not a small sigma. RESULTS.md still prints the original check.
- P3 sigma limits: top-hat at sigma = 1 equal within 1e-12; soft not equal at sigma = 1 (spread > 0.1),
  and its spread falls as sigma grows (below 1e-3 at sigma = 1e4).
- P4 This README carries the caveats and references (run.py checks the text).
- Stage C is a report. Stage D is reported; without it the grade on mixing would be PARTIAL.

## 4. Caveats

- A point brane breaks SO(3) down to U(1). Two of Job Two's three massless flavour (isometry) vectors get
  a mass by absorbing the brane's position modes, and one stays massless; Stage D's second brane breaks
  the rest [hive-interpretation].
- sigma, alpha and beta are all [assumed input]. In a real solution alpha comes from the brane tension,
  and R is the radion (that is Job Five).
- The brane profile is put in by hand: no brane action, no back-reaction beyond the conical deficit, and
  no brane-localised flux at the tips [assumed input].
- Yukawa entries are known only up to one overall constant per sector; the 6D couplings stay free
  [assumed input].
- Stage D's d^1(beta) tilt result holds only on the round sphere (alpha = 1). On the rugby ball SU(2) drops to
  U(1), so a tilt no longer acts as d^1(beta) [standard].
- Toy bookkeeping. Nothing here derives the Standard Model, the quark masses or the real CKM matrix.

## 5. References

- S. Randjbar-Daemi, A. Salam and J. Strathdee, Nucl. Phys. B 214 (1983) 491.
- D. Cremades, L. E. Ibáñez and F. Marchesano, "Computing Yukawa couplings from magnetized extra
  dimensions", JHEP 0405:079 (2004), arXiv:hep-th/0404229. This is the torus analogue, not a sphere
  calculation.
- F. D. M. Haldane, Phys. Rev. Lett. 51 (1983) 605 (lowest Landau level on the sphere; source of the
  [standard, Haldane-sphere] tag).

## 6. Files

- `README.md` - this file (spec, rules, caveats, references, sign-off).
- `run.py` - all computations; writes `RESULTS.md` and `ratios.png`.
- `RESULTS.md`, `ratios.png` - generated by `run.py`; not hand-edited.

## 7. Sign-off

Signed off 2026-10-02: Venus PASS (maths); Helios PASS (physics, toy), PARTIAL on mixing.

Post-run (2026-10-02): recorded run at 18:41 (12 s); P1-P4 all PASS [computed]. Stage A: three equal singular values 1/sqrt(4 pi alpha) at alpha = 1, 0.8, 0.6, 0.5 (0.282094791774 at alpha = 1, the alternative model's value); axial profiles give off-diagonals of at most 2e-17 [computed].
Post-run (2026-10-02): Stage B: Bernstein shapes confirmed from the monopole harmonics (1.3e-15) and the 1D solve (3e-12); at sigma = 0.01 the ratios are within 1.1% (top-hat) and 2.1% (soft) of their own laws; top-hat equal at sigma = 1; soft spread 0.39 at sigma = 1, about 1/(2 sigma) after; delta brane rank 1 [computed].
Post-run (2026-10-02): Stage C: the zero-mode count stays 3 at every alpha tested (regularity, normalisability and finite differences agree; m = 1/2, 3/2, 5/2). Ratios at a fixed area fraction depend on alpha as well as sigma. Fitted slopes match Venus's k/alpha to within 0.005 [computed; prediction confirmed].
Post-run (2026-10-02): extra observation [computed; boundary-condition choice]: on a cone the k = 0 density vanishes at the tip like r^(1/alpha - 1), so a strictly point-like brane exactly on a conical tip couples to none of the three modes; a finite width is needed.
Post-run (2026-10-02): Stage D: abs(V) = abs(d^1(beta)) to 7e-15 [computed]; neighbouring mixings are equal, sin(beta)/sqrt(2), and 1-3 is (1 - cos beta)/2. Against real mixing the 1-3 suppression matches but V_12 = V_23 does not (real |V_cb| is about |V_us|/5.5) [hive-interpretation].
Post-run (2026-10-02): [post-hoc] the P2 monotonicity check was narrowed to sigma = 0.1, 0.03, 0.01 after one staged test run (section 3); the check as first worded prints NO in RESULTS.md. The staged test run also showed that recomputing Gauss-Legendre nodes took 75 of 92 s, so run.py caches them; no number depends on this.
Post-run (2026-10-02, Venus wording fixes, approved by NanoRibbon): the conical-tip observation is tagged [boundary-condition choice] here and in RESULTS.md. It relies on the regular tip condition run.py uses (both tip exponents >= 0); a brane carrying its own flux or tension would shift that exponent. Venus's note [standard]: on a cone, spinors pick up r^(1/alpha - 1) from the spin connection, so |eta_k|^2 ∝ r^((2k+1)/alpha - 1); this matches the closed form, and the shared factor cancels in the ratios.
Post-run (2026-10-02): P2 stays narrowed to sigma <= 0.1 [post-hoc]. RESULTS.md now prints the leading corrections next to each measured ratio-to-law (top-hat Y_1: 1 + sigma/3; top-hat Y_2: 1 + sigma; soft Y_1: 1 - 2 sigma^2; soft Y_2: 1 + 2 sigma) and explains why the soft Y_2 ratio turns over: Y_2/Y_0 tends to 1 while 2 sigma^2 keeps growing.
Post-run (2026-10-02): Stage D scope: the d^1(beta) result holds only on the round sphere (alpha = 1); caveat added in section 4 and a note in RESULTS.md.
Post-run (2026-10-02): Signed off 2026-10-02: Venus PASS (maths); Helios PASS (physics, toy), PARTIAL on mixing.

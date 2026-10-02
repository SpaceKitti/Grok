# SM-like zero modes on a smooth S^2 bolt (toy bookkeeping)

This file was written **before** `run.py` was run. The setup, the checks and the
expectations are fixed here first. `RESULTS.md` is written only by `run.py` and is
never edited by hand.

**What this is.** A 6D toy, 4D spacetime times a round two-sphere, with a magnetic
flux through the sphere. We count fermion zero modes, filter hypercharges by anomaly
cancellation, and compute overlap integrals that play the role of Yukawa couplings.

**What this is not.** It does not derive the Standard Model, and no quantum-gravity
result follows from it. Every choice of field content and charge below is an input.

Tags: [computed] = produced by `run.py`; [identity] = follows from algebra;
[assumed] = an input we chose; [by construction] = true because of how the setup is
built; [standard] = textbook fact; [standard, expected] = textbook result we expect the
run to reproduce; [schematic] = a toy stand-in for a real calculation; [not checked] =
not computed here.

## 1. Assumed inputs and conventions

### Geometry and flux
- Space is M4 x S^2, with S^2 round and radius R = 1. [assumed]
- The S^2 is smooth [by construction]. It is **not** the branched Pair A double cover
  from the earlier job. A GoldbergHexa lattice version is deferred; it would only be
  useful later as a fermion-doubling check.
- There is a background U(1)_X magnetic flux with (1/2 pi) * integral of F over S^2 = n,
  n an integer (Dirac quantisation). [assumed background]
- A field of U(1)_X charge x feels the monopole charge q = x n / 2. [identity, from the definitions]

### Wu-Yang two-patch convention (fixed here)
- Covariant derivative D = d - i A on a field of monopole charge q.
- North patch (all of S^2 except the south pole): A_N = q (1 - cos theta) dphi.
- South patch (all of S^2 except the north pole): A_S = -q (1 + cos theta) dphi.
- On the overlap, A_N - A_S = 2q dphi, so fields glue by psi_N = e^{i 2 q phi} psi_S.
  This phase is single-valued only if 2q is an integer, which is Dirac quantisation. [identity]
- The flux is then (1/2 pi) * (loop integral of A_N - A_S around the equator) = 2q = n
  for a charge-1 field. [identity]

### Monopole harmonics (our normalisation)

$$Y^{N}_{q,l,m}(\theta,\phi)=\sqrt{\tfrac{2l+1}{4\pi}}\;d^{\,l}_{m,-q}(\theta)\,e^{i(m+q)\phi},\qquad Y^{S}_{q,l,m}=e^{-2iq\phi}\,Y^{N}_{q,l,m}$$

In words: a monopole harmonic is a Wigner rotation function with the monopole charge
as its second index, written in each patch's gauge. Here l = |q|, |q|+1, ... and
m = -l..l. [standard; Wu-Yang 1976, written in Wigner-d form]

### Dirac operator and chirality
- On S^2 with flux, the Dirac operator has |n| zero modes for a charge-1 field, all of
  one 2D chirality fixed by sign(n). With no flux there are none: the curvature of
  the round sphere makes the squared Dirac operator strictly positive (Lichnerowicz).
  [standard; Randjbar-Daemi, Salam, Strathdee 1983]
- The zero modes are the lowest-Landau-level harmonics with j = |q| - 1/2, so there
  are 2j + 1 = |2q| of them. Their wavefunctions are Y_{Q,j,m} with effective charge
  Q = q - sign(q)/2, so |Q| = j (the half unit is the spin connection). [standard]
- 4D chirality convention [assumed]: the 6D chirality is Gamma7 = gamma5 x sigma3,
  6D Weyl fermions have Gamma7 = -1, and gamma5 = -1 means 4D left-handed.
  So **a 2D zero mode with sigma3 = +1 is 4D left-handed**, and one with sigma3 = -1 is
  4D right-handed. [identity, given the convention]
- **The chiral projector comes from the flux sign.** A 6D Weyl field with x n > 0 has
  only sigma3 = +1 zero modes, so only 4D left-handed modes. With x n < 0 it has only
  right-handed ones. We are not adding a projector by hand: putting the SU(2)_L doublets
  at x n > 0 makes only left-handed doublets appear. [standard; checked in check 1]

### Field content and U(1)_X charges [assumed]
- One 6D Weyl field per SM-like multiplet: Q_L (3,2), L_L (1,2) with x = +1; u_R (3,1),
  d_R (3,1), e_R (1,1) and optional nu_R (1,1) with x = -1.
- The flux n is **not** set by hand: run.py picks the smallest n > 0 that gives 3 zero
  modes for a charge-1 field, using its own computed count table (check 2).
- The target "3 copies" is the input; the flux that delivers it is computed.

## 2. Checks that run.py must print

**Check 1: flux is needed; count table.** For n = -4..4 (charge-1 field), count zero
modes and their 2D chirality three ways:
  (a) the lowest-Landau-level formula 2j+1 with j = |q| - 1/2 (none if n = 0);
  (b) diagonalising the truncated Dirac matrix in a monopole-harmonic basis. Its 2x2
      blocks use the standard eigenvalue sqrt((l+1/2)^2 - q^2) [standard], so (b) is a
      bookkeeping check, not an independent one;
  (c) **independent numerics:** a finite-difference discretisation of the explicit
      Dirac differential operator in theta (north gauge, rotating frame, regular
      boundary conditions), counting eigenvalues of D^2 below 0.5 per half-integer m.
      This uses no harmonics and no eigenvalue formula. A convergence table with grid
      size is printed for the zero-mode eigenvalues.

**Check 2: three copies.** The flux for 3 copies is read off the computed table.

**Check 3: anomaly filter.** Fields are written as 4D left-handed: Q(3,2), u^c(3bar,1),
d^c(3bar,1), L(1,2), e^c(1,1), optionally nu^c(1,1). With Y_Q = 1/6 fixed, scan every
other Y over k/6, k = -6..6. Keep only assignments where these cancel **exactly**
(integer arithmetic, re-checked with sympy Rational):
SU(3)^2 U(1), SU(2)^2 U(1), U(1)^3, grav^2 U(1), and SU(3)^3 (which cancels for any Y,
because each generation has two colour triplets and two antitriplets; it is printed).
Also print the Witten SU(2) global anomaly check: the number of doublets per generation,
3 colours + 1 = 4, must be even. Print all sums as exact fractions for the survivors.
Also computed: the mixed anomalies of the extra U(1)_X with the zero-mode content.
These are expected **not** to cancel. That is printed as a finding, not hidden.

**Check 4: Yukawas from triple overlaps.** The overlap of three monopole harmonics,

$$\int_{S^2}\overline{Y}_{q_1 l_1 m_1}Y_{q_2 l_2 m_2}Y_{q_3 l_3 m_3}\,d\Omega=(-1)^{m_1+q_1}\sqrt{\tfrac{(2l_1+1)(2l_2+1)(2l_3+1)}{4\pi}}\begin{pmatrix}l_1&l_2&l_3\\-m_1&m_2&m_3\end{pmatrix}\begin{pmatrix}l_1&l_2&l_3\\q_1&-q_2&-q_3\end{pmatrix}$$

In words: the overlap is a product of two 3j symbols; the second one carries the
charges, so the overlap vanishes unless charges add up and m's add up.
[identity, derived from the Wigner-D triple integral in our convention]. It is computed
with sympy `wigner_3j` and checked by numerical quadrature on the two Wu-Yang patches
(north hemisphere in the north gauge, south hemisphere in the south gauge).
Closure rule: -Q_L + Q_H + Q_R = 0 for the effective charges, and m_L = m_H + m_R.

Flux assignments for the Yukawa test [assumed flux assignment], all at n = 3:
- **A (main):** doublets x = +1 (Q = +1, 3 left-handed modes); singlets x = -1 (Q = -1,
  3 right-handed modes); Higgs doublets with x = +2 (q = 3). The Higgs is treated as an
  internal gauge-field-like component whose spin weight shifts its wavefunction charge
  by one unit, so Q_H = q_H - 1 = 2 and it has 5 lowest modes. With that, both the bare
  charges (-3/2 + 3 - 3/2 = 0) and the wavefunction charges (-1 + 2 - 1 = 0) close.
  [assumed, schematic] Two Higgs doublets are used, H_d (Y = +1/2) for down and lepton
  and H_u (Y = -1/2) for up. Why two is checked: run.py shows that one Higgs plus its
  conjugate cannot close the up sector with 3 right-handed modes.
- **B (alternative):** neutral scalar Higgs (x = 0, Q = 0, 1 mode); singlets at x = +1,
  the same sign as the doublets. The charges close, but the singlets are then 4D
  left-handed too, so the 4D coupling (left-bar)(Higgs)(left) vanishes by Lorentz
  symmetry [identity]. The matrix is printed only as bookkeeping.
- **C (alternative):** as A, but the Higgs taken from the next Landau level (j = 3,
  7 modes). The 3j triangle rule (j_H <= j_L + j_R = 2) should kill every entry.
- For every Higgs mode, run.py prints the 3x3 matrix (rows: doublet m, columns:
  singlet m), its rank, and its singular-value ratios. The up, down and lepton sectors
  share the same flux charges in A, so their matrices are expected to be the same up to
  an overall coupling [assumed = 1]. All of this is [schematic; depends on flux
  assignment].
- **Plain warning:** on a round S^2, rotation symmetry (m conservation) fixes the
  sparsity pattern of every matrix. Any realistic hierarchy needs extra [assumed] input
  (Wilson lines, a deformed metric, localised sources, a chosen Higgs vev profile). The
  2D spinor/vector index structure of the coupling is only modelled through the
  effective charge Q. [schematic]

**Check 5:** the smooth-S^2 note above.

**Check 6: final table.** For each surviving mode: multiplet, SU(3)xSU(2)xU(1)_Y rep,
Y as an exact fraction, U(1)_X charge, flux charge q, number of zero modes, and 4D
chirality. Then the coupling ratios and ranks.

## 3. Pre-registered expectations (before the run)
- Check 1: no zero modes at n = 0; |n| zero modes otherwise, all with chirality
  sign(n); (a), (b) and (c) agree. [standard, expected]
- Check 2: 3 copies at n = 3. [standard, expected]
- Check 3: without nu^c, only the SM hypercharges survive, up to swapping the names u^c
  and d^c. With nu^c, the SM line plus the B-L direction survives (a one-parameter
  family on the grid). SU(3)^3 = 0 for every Y; Witten count = 4 (even).
  [standard, expected] The U(1)_X mixed anomalies do not cancel. [expected]
- Check 4: exact and quadrature overlaps agree. In A, the m_H = 0 mode gives a rank-3
  diagonal matrix, m_H = +-1 give rank 2, m_H = +-2 give rank 1. B gives a rank-3
  identity-like matrix (but forbidden by 4D chirality). C gives rank 0.
  [expected from the 3j selection rules]

## 4. What is NOT checked [not checked]
- 6D gauge, gravitational and mixed anomalies (these need a Green-Schwarz mechanism or
  extra matter). Not computed.
- Any cure for the 4D U(1)_X anomalies (Green-Schwarz, a massive U(1)_X). Not computed.
- SU(2)^3: it vanishes identically for SU(2) [standard], so it isn't scanned.
- Other global anomalies beyond Witten's SU(2) check.
- Higgs mass, potential, stability (lowest Landau levels of charged vector components
  are known to be tachyonic), vacuum expectation value, and electroweak breaking.
- Stabilisation of the sphere's radius, backreaction of the flux, and the KK tower
  beyond the zero modes.
- Real Yukawa values (overall 6D couplings set to 1), RG running, and any fit to masses.

## 5. Files
- `README.md` - this file (written before the run).
- `monopole.py` - Wu-Yang harmonics, the harmonic-basis Dirac matrix, and the
  finite-difference Dirac check.
- `anomalies.py` - the exact hypercharge scan and the anomaly sums.
- `overlaps.py` - triple overlaps (sympy 3j and quadrature) and Yukawa matrices.
- `run.py` - runs every check and writes `RESULTS.md`.
- `RESULTS.md` - generated; never hand-edited.

No git, no GitHub.

Post-run (2026-10-02): Venus [standard]: B-L line Y = a Y_SM + b (B-L) with a + 2b = 1; equivalently Y_a = a Y_SM + (1-a)/2 (B-L), with grid a = 1, 2/3, 1/3, 0 and one pure (B-L)/2 row. With nu^c, anomalies alone cannot fix hypercharge; the Yukawa/Higgs charge choice picks a = 1.
Post-run (2026-10-02): FD edge-mode convergence is logarithmic, with eigenvalue x ln N printed per grid as a borderline inverse-square-pole diagnostic; the n = 0 level has the same bias (1.089 versus 1), and counts are unaffected.
Post-run (2026-10-02): Check 1 to Check 4 map: m_phi = m_J + q in the north patch (e.g. 1/2 = -1 + 3/2).
Post-run (2026-10-02): T = 1 normalisation (common T(R) = 1/2 factored out).
Post-run (2026-10-02): Assignment C rank 0 [identity: triangle rule, j_H <= j_L + j_R = 2].
Post-run (2026-10-02): The flux sits only in U(1)_X and no SM gauge boson carries X, so there is no Nielsen-Olesen tachyon in the W/gluon sector [standard].
Post-run (2026-10-02): In 6D a scalar Yukawa between Weyl fermions of the SAME 6D chirality vanishes identically because Gamma^0 anticommutes with Gamma_7 [identity]. All fermions have Gamma_7 = -1, so the Higgs must be A_z (spin weight 1), i.e. gauge-Higgs unification; the charge is spin-shifted.
Post-run (2026-10-02): Tachyon [computed + standard: RSS 1983]: M^2 R^2 = j(j+1) - q^2 with j >= |q| - 1; at the lowest level M^2 = -|q|/R^2 exactly, with no curvature correction. For q = 3, j = 2 gives -3/R^2 with 5 modes, j = 3 gives +3/R^2, and the other helicity starts at (3q+2)/R^2 = 11/R^2 > 0. [standard: tachyonic Higgs = EWSB at the compactification scale]
Post-run (2026-10-02): H_u and H_d [requires gauge-Higgs embedding, not specified]; a doublet in A_M needs e.g. SU(3)_w or G2, and SU(3)_w gives tree-level sin^2 theta_W = 3/4.
Post-run (2026-10-02): Yukawa = gauge coupling x 3j overlap, so identical up, down and lepton matrices are a structural prediction with no tree-level flavour hierarchy; there are 5 degenerate tachyonic doublets per Higgs, and only m_H = 0 preserves the S^2 U(1) rotation.
Post-run (2026-10-02): H_u/H_d hypercharge labels are opposite to the MSSM convention but internally consistent with psi_bar_L H psi_R.
Post-run (2026-10-02): Green-Schwarz precision [standard, not computed]: the 4D U(1)_X anomalies reduce from the 6D anomaly polynomial on integral F_X = n, scale with n, and are cancelled by B wedge F_X; the B_mu_nu axion is eaten, U(1)_X becomes a massive Z' near compactification, survives as a global x-closure selection rule, and its couplings to WW~, GG~ and BB~ require generalised Chern-Simons terms.
Post-run (2026-10-02): Anomalies NOT checked now begins with irreducible 6D anomalies: net 15 Weyl (16 with nu^c) for tr R^4 in the all-Gamma_7 = -1 model, needing extra matter or tensors; n_H - n_V + 29 n_T = 273 is for 6D (1,0) supergravity, not assumed for this toy. Background stability (radion, flux sector) [not checked].
Post-run (2026-10-02): Alternative model (Helios), not run unless Akitti asks: singlets Gamma_7 = +1, x = +1; scalar Yukawa allowed; neutral scalar Higgs x = 0, j = 0, no tachyon makes Assignment B Lorentz-allowed (rank 3, equal singular values). Per-generation X anomalies with nu^c (T = 1): SU(3)^2X = 0, SU(2)^2X = 4, Y^2X = -2, YX^2 = 0, X^3 = grav^2X = 0 (both 1 without nu^c); over three generations, 12 and -6. Irreducible 6D tr R^4 and tr F^4_SU(3) cancel (8 vs 8 Weyl, 2 vs 2 triplets), leaving reducible parts for GS. NOTES ONLY; not run.
Post-run (2026-10-02): Fermion content, chirality and SM hypercharges follow from n = 3 flux [computed]; with one 6D chirality the Higgs must be a gauge-field component, which is tachyonic (EWSB at 1/R) and gives universal, hierarchy-free Yukawas [standard + computed]; U(1)_X needs 6D GS and becomes a massive Z′ [standard, not checked].

## Alternative model (Helios, approved by Akitti 2026-10-02), pre-fixed rules

Written before the alternative run. Run it with `python run.py --model alt`. Its output
goes ONLY to `RESULTS_alt.md`. The default model and its `RESULTS.md` are unchanged.
The alternative mode runs no new finite-difference sweeps: it reuses the exact
harmonic-basis counts, the anomaly scan and the exact 3j overlaps. Spec and pass criteria,
word for word:

SETUP: same S^2 as Job Two, U(1)_X flux n = 3, and no flux in the SM gauge fields.
- Q and L: Gamma_7 = -1, x = +1.
- Singlets u, d, e, nu: Gamma_7 = +1, x = +1. Their 4D zero modes are right-handed, so their left-handed conjugates carry X = -1.
- Higgs: an ordinary 6D scalar doublet with x = 0, which sees no flux. Its zero mode is the constant j = 0 mode, and its potential (mu^2 < 0) is [assumed input].

PASS CRITERIA (print before any results):
1. Each field has three copies with the correct 4D chirality.
2. The anomaly filter still returns the SM hypercharges.
3. The Yukawa overlap ∫_{S^2} psibar_Q H psi_u is nonzero now that the fermions have opposite 6D chirality. Report its rank and its three singular values. Prediction (Venus's corrected wording, use this verbatim): 'The coupling uses psibar_Q, which is complex-conjugated, so the modes pair as m_Q = m_u. With a constant Higgs Y_H = 1/sqrt(4 pi), the overlap is the orthonormality of two identical j = 1 sections: ∫ psibar_{Q,m} H psi_{u,m′} = (1/sqrt(4 pi)) delta_{m m′}. So the prediction is a diagonal matrix with entries 1/(2 sqrt(pi)), rank 3 and three exactly equal singular values [identity].' It's a check, not a target. Real masses come out, but all three generations are identical; splitting them needs something that breaks the round sphere's symmetry, which isn't part of this run. Also do the down and lepton matrices.
4. Print the per-generation 4D anomaly table, then the totals over three generations (T = 1 normalisation, exact fractions): SU(3)^2X = 0, SU(2)^2X = 4 (12), Y^2X = -2 (-6), YX^2 = 0, X^3 = grav^2X = 0 (these two need nu^c; print the without-nu^c values too, expected 1 each).
5. The irreducible 6D anomalies cancel: tr R^4 has 8 Weyl fields at Gamma_7 = -1 (Q 6, L 2) against 8 at +1 (u, d, e, nu), and tr F^4_SU(3) has 2 triplets against 2. Compute the counts. Anything left over goes to Green-Schwarz, which makes Z' massive [standard, not computed].
6. The Higgs has no flux tachyon: x = 0 gives the lowest M^2 R^2 = 0 at tree level (j = 0). Print the scalar spectrum l(l+1) for the first few levels.
Final: a PASS/FAIL table for criteria 1-6, plus a short reading line.

Notes fixed with these rules:
- 4D chirality uses the same convention as the default model: Gamma_7 = gamma5 x sigma3, and gamma5 = -1 is
  left-handed. [assumed convention]
- Criterion 5 counts only spin-1/2 fields; no gravitino or (anti-)self-dual tensors are assumed. [assumed]
- How the default model's output was checked to be unchanged: run the default model to a scratch file
  (`--out`), compare it with a backup of `RESULTS.md` taken first, ignoring only the "Generated:" timestamp
  line, then delete the scratch file. `RESULTS.md` itself is never rewritten.

Post-run (2026-10-02): Venus, item 6: criterion 6 is named "Higgs has no FLUX tachyon". The constant j = 0 mode has M^2 = mu^2, whose sign stays [assumed input]; the l(l+1)/R^2 tower is the flux-free KK spectrum on top of mu^2.
Post-run (2026-10-02): Helios, note 1, degenerate generations [standard]: the three generations are the j = 1 triplet of the sphere's SO(3) (a rotation combined with a gauge transformation, because of the flux), so SO(3) is an exact flavour symmetry and forces the three equal singular values. The metric side also gives flavour-changing KK vectors at about 1/R. Splitting the generations needs SO(3) breaking (a squashed sphere, a rugby ball with conical tips, or a localised source): a separate later step, not computed here.
Post-run (2026-10-02): Helios, note 2, units [standard]: in 6D, [y_6] = -1 (a length), because [psibar psi H] = 5 + 2 = 7 against an action density of dimension 6. With unit-normalised harmonics on a radius-R sphere, y_4 = y_6 * (1/(2 sqrt(pi))) * (1/R). The overlap fixes the coupling ratios, not their overall size; the up, down and lepton 6D couplings are free [assumed input].
Post-run (2026-10-02): Venus hand-checked item 4, per generation with left-handed charges: SU(3)^2X 2-1-1 = 0, SU(2)^2X 3+1 = 4, Y^2X = -2, YX^2 = 0, X^3 = grav^2X 8-8 = 0 (8-7 = 1 without nu^c); totals 12 and -6. Cross-referenced in RESULTS_alt.md.
Signed off 2026-10-02: main model (RESULTS.md) Venus PASS (maths), Helios PARTIAL (fermion table sound; Yukawa sector needs a gauge–Higgs embedding). Alternative model (RESULTS_alt.md) Venus PASS (maths, items 3–4 hand-checked), Helios PASS (toy physics).

## Final model (`--model final`), NanoRibbon go 2026-10-02 (counts as Akitti's)

Written before the final run. Run it with `python run.py --model final`. Its output goes ONLY to
`RESULTS_final.md`. `RESULTS.md` and `RESULTS_alt.md` are not rewritten and stay byte-identical as the
audit trail. No new physics and no new Higgs model: Akitti chose the alternative model at 15:58 and it
passed, so this mode presents that model as THE single final answer. It recomputes the numbers with the
same functions (exact harmonic-basis counts, exact 3j overlaps, anomaly sums) and checks them against
`RESULTS_alt.md`, read-only. No gauge-Higgs code is added.

RESULTS_final.md contains:
(a) one finite table of surviving 4D modes: fermions with chirality and charges, the Higgs constant mode,
    and the lowest KK levels;
(b) one coupling-ratio table for up, down and lepton: all diagonal 1/(2 sqrt(pi)), so the ratios between
    generations are 1 : 1 : 1 [identity]; the ratios between sectors are free 6D inputs [assumed input];
    y_4 = y_6 / (2 sqrt(pi) R) [standard];
(c) a plain statement that the generations come out degenerate (an SO(3) triplet), so any mass hierarchy
    needs an [assumed] symmetry-breaking input;
(d) a plain note that U(1)_X needs Green-Schwarz, giving a massive Z' [standard, not computed];
(e) a 'Final answer' section: RESULTS.md is the main model (A_z Higgs, tachyonic, Helios PARTIAL) and is
    superseded; RESULTS_alt.md is the source; RESULTS_final.md is THE final answer.

Self-checks printed as PASS/FAIL: (a) 3 copies each with the expected 4D chirality, first fermion KK gap
sqrt(|n| + 1)/R; (b) overlaps diagonal 1/(2 sqrt(pi)), rank 3, two-patch quadrature agrees within 1e-12;
(c) the three singular values equal within 1e-12; (d) U(1)_X anomaly totals 0, 12, -6, 0, 0, 0 with nu^c;
(e) agreement with RESULTS_alt.md (six PASS, same singular values, same anomaly totals).

File added: `RESULTS_final.md` - generated by `run.py --model final`; not hand-edited.
Post-run (2026-10-02): final run done; self-checks (a)-(e) all PASS [computed]. RESULTS.md (FEF2BA7974F75028, 15:49:52) and RESULTS_alt.md (2EEF1B88083A4FBC, 16:10:57) were not rewritten [computed: hashes printed in RESULTS_final.md and re-checked after the run].
Post-run (2026-10-02): THE final answer for this folder is RESULTS_final.md, which presents the alternative model; RESULTS.md (main model: A_z Higgs, tachyonic, Helios PARTIAL) is superseded and kept as the audit trail; RESULTS_alt.md is the source of every number [post-hoc presentation; no number changed].
Post-run (2026-10-02): coupling ratios: generations 1 : 1 : 1 in up, down and lepton [identity]; sectors y6_u : y6_d : y6_e, free [assumed input]; y_4 = y_6 / (2 sqrt(pi) R) [standard]. The generations are an SO(3) triplet, so any hierarchy needs an [assumed] SO(3)-breaking input. U(1)_X needs Green-Schwarz, giving a massive Z' [standard, not computed].
Post-run (2026-10-02, Venus/Helios re-grade): the isometry vectors (a mix of the metric and the U(1)_X field along the Killing vectors) are MASSLESS at tree level [standard, RSS 1983: Randjbar-Daemi, Salam & Strathdee]. So the generation SO(3) is a gauged flavour symmetry, and on the round sphere the degeneracy is exact. Squashing would break SO(3) to U(1) and give two of the three vectors a mass of order the squashing scale [standard]. This replaces the earlier 'flavour-changing KK vectors at about 1/R' wording (the Helios note 1 Post-run line above, the RESULTS_alt.md reading section, and RESULTS_final.md rows 9/15 and section (c)).
Post-run (2026-10-02): the Z' scale is [assumed]; it depends on the Green-Schwarz coupling. The 'near 1/R' wording is removed from RESULTS_final.md. RESULTS.md (the superseded main model) keeps its old wording unchanged as the audit trail.
Post-run (2026-10-02): gauged SO(3) anomaly check (Helios's bonus check) [computed, printed in RESULTS_final.md section (d)]: every fermion sits in the same j = 1 triplet, so the SU(2)_KK x U(1) anomalies reduce to the gravitational sums: Sum Y = 0 and Sum X = 8 - 8 = 0 per generation (needs nu^c), so SU(2)_KK^2 Y = SU(2)_KK^2 X = 0. No cubic SU(2) anomaly and no Witten anomaly (integer isospin) [standard]. Gauging adds no new anomaly.
Post-run (2026-10-02): RESULTS_alt.md and RESULTS_final.md regenerated through run.py (--model alt, --model final) for this wording only; RESULTS.md not rewritten [post-hoc wording; numbers checked unchanged by diff against the 17:27 backup].
Post-run (2026-10-02, Venus correction): the gauged SO(3) anomaly line is weighted by the triplet index T(3) = 2 (doublet normalised to 1/2), not by the dimension 3, summing over 4D left-handed fields counted once: A[SU(2)_KK^2 Y] = T(3) * Sum Y = 2 x 0 = 0; A[SU(2)_KK^2 X] = T(3) * Sum X = 2 * (8 * (+1) + 8 * (-1)) = 0, +1 group Q (6), L (2), -1 group u^c (3), d^c (3), e^c (1), nu^c (1), so it needs nu^c. One-vertex SU(2)_KK anomalies vanish (traceless generators), no cubic SU(2) anomaly, no Witten anomaly (integer isospin) [computed; Venus confirmed]. Only --model final re-run for this.
Post-run (2026-10-02): added a References section at the end of this file with the RSS 1983 citation (given by Orion, confirmed by Helios). It is the source for the [standard, RSS 1983] tag in RESULTS_final.md and RESULTS_alt.md. README only; no RESULTS file or run.py changed.

## References

- S. Randjbar-Daemi, A. Salam and J. Strathdee, "Spontaneous compactification in six-dimensional Einstein–Maxwell theory", Nucl. Phys. B 214 (1983) 491. This is the source for the [standard, RSS 1983] tag in RESULTS_final.md and RESULTS_alt.md.

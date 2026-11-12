# VENUS audit: Helios finite-d marginality note + Addendum 1 + buckler closing-count note (2026-11-10, ~10:30 UK)
Role: Venus (maths checker). Categories I own: 1 dimensions (algebra side), 2 signs, 7 approximation presented as exact, H2 circular inputs, H3 conventions, H4 re-grade after change, H10 tallies read as results, H11 stale reasons, H12 one symbol with two meanings, H14 comparisons that fail by construction. H15 (paper claims checked against the page) is done here too because the brief asks for it.
Scope: research and maths only. I ran no sims, changed no construction, froze nothing, sent no messages and touched no git. The authors' files are unchanged.
Open-problem check: STILL_TO_DO.md:205 + arXiv:1202.0259, 1302.3990, 1411.3975, 2011.10899 (finite-d jamming theory gap is OPEN; the note is listed there as working and ungraded, with the speculative response-decay bound not established). I grepped DEAD_ENDS.md before starting. The only jamming lines were the b-control spec, J1 n_stiff and (added by Helios during this audit) the s4 buckler-geometry line. None covers the Wyart/LDW closures.
Idea owner: the question comes from Akitti's post 2119613243593302457 item 1, which is Grok text she pasted, so it is tagged as possibly hallucinated (H6). The derivations audited are hive proposals (Helios). The corrections are a hive audit (Venus).
Grading rule: n/a. This is a maths audit, not a run spec, so no projector-rank grading applies and nothing here is a gate.
Dimension note: general d, target 3D (d=3); 2D results cited only as literature. Gaps are used as lengths (Wyart: r - sigma0) in note s3 and s6, and as dimensionless h=(r-sigma)/sigma in 1411.3975 and CHB21. The algebra is consistent either way as long as the closing rates c are dimensionless (dh = s c, with s a length). In LDW, a0 absorbs this.

## Versions read (H4). Files changed while I was auditing.
| file | sha8 read first | sha8 audited (final) | change seen |
|---|---|---|---|
| HELIOS_FINITE_D_MARGINALITY_NOTE.md | 817d1354 (10:14) | 5f1384a0 (mtime 10:18:09) | adds a 2-line "SEE ADDENDUM 1" header; title time changed from ~11:40 to ~10:05; body otherwise identical by my side-by-side read, so body lines shift by +2 |
| HELIOS_FINITE_D_MARGINALITY_NOTE_ADDENDUM_1.md | b853a27f (10:19) | 500f984c | adds a 2-line "SEE ALSO closing-count note" header (eta = lambda; rms correction); body identical by my read, so lines shift by +2 |
| HELIOS_BUCKLER_CLOSING_COUNT_NOTE.md | 3c46f4b5 | 3c46f4b5 | none |
Line numbers below refer to the FINAL hashes. Any later edit needs re-grading before anyone relies on it.
I did not audit ORION_JAMMING_*_2026-11-10.md. I read papers directly instead.

## Verdict
- The Wyart 2012 bound gamma >= 1/(2+theta) is reproduced correctly, and so are LDW 2013 Eqs. 20, 23 and 24. The CONDITIONAL label is right.
- Main note s6b (decaying-response generalised bound) is REJECTED as a constraint. The algebra is right, but it omits a force-response correlation that is forced by virtual work. Once that correlation is included, the a-dependence cancels exactly. "Observed saturation REQUIRES a=0" is false in any case.
- 6a "iff", s5 "closures hold at d=inf" and the s4 geometric reconstruction (already withdrawn by the author) are overclaims and are corrected below.
- Addendum 1: the LDW sourcing and the lambda(=eta) algebra are correct. But the MK "contradiction" is overstated. CHB21's LP jamming certifies FIRST-ORDER jamming only, so it does not exclude LDW's second-order, finite-s instability. The C rms argument is wrong (the author conceded this in the closing-count note).
- Closing-count note: s1-s5 are correct as exact or conditional statements, subject to the caveats below. It is the trustworthy framework of the three files. Nothing in any of the three files derives theta_l, eta, zeta, mu, or MK's theta_l=0.

## Findings, in severity order (silent-failure risks first)

1. **[HIGH, rejects s6b] Main note L44-47 (s6b): the force is treated as independent of the response decay.**
   - Quote: "s* ~ f N^{2a/d - 1}" with f_min taken from P(f) ~ f^theta, while c and s_c carry the response decay N^{-a/d}.
   - Why it fails: by virtual work (Wyart 1202.0259 Eqs. 5-6, p3: p dV = s f_<12> at first order; LDW 1302.3990 Eq. 7, p3-4: f_alpha = -sum_i F_i . V*_i^(alpha)), a contact's force IS the first-order coupling of its floppy mode to the boundary or box. LDW write this as f/f_typ = b W (Eq. 10, p4), with b the far-field amplitude.
   - s6b is exactly LDW's Eq. 18 with b = N^{-a/d}: c ~ b^2 = N^{-2a/d} matches s6b's C ~ N^{1-2a/d}, and s† ~ h_min/b matches s6b's s_c ~ N^{-1/(1-gamma)+a/d}. But s6b draws f from P(f) independently of b.
   - With f = bW: kappa ~ W b^2 N^{gamma/(1-gamma)}/(1/N + b^2), which equals W N^{gamma/(1-gamma)} for b^2 >> 1/N. b drops out, and the bound returns to gamma >= 1/(2+theta_W) (LDW Eq. 24).
   - Sympy (tools/venus_fd_marginality_checks.py): the log_N kappa exponent has no u=a/d dependence with f=bW, and retains u with independent f.
   - Correction: s6b's a-correction is an artefact of the omitted f-response correlation. It is not a finite-d bound. A decaying response could change the extended bound only through (i) W correlating with the decay, or (ii) blocking or energy not being captured by one far-field amplitude. Neither is derived. s6b should be withdrawn by an addendum, and I have added a DEAD_ENDS line.

2. **[HIGH] Main note L47: "Observed saturation in d=2,3 therefore REQUIRES a = 0".**
   - This is wrong even inside s6b's own (flawed) model. The bound is an inequality. For a > 0, the a-bound lies below 1/(2+theta), so an observed gamma = 1/(2+theta_e) would be strictly stable (non-marginal), not forbidden.
   - The correct statement is: "if the s6b bound were the operative one, observed gamma=1/(2+theta_e) would be MARGINAL only if a=0".
   - "Vanishes at d=inf for fixed a, matching mean-field exactness" is also not a check. a/d appears only because N = L^d, the correction is a power of L, and nothing says a is d-independent.
   - The s6b regime boundaries are not treated either. C ~ s^2 <f> sum r^{-2a} is far-field for 2a<d, ~ ln N at 2a=d, and near-field O(1) for 2a>d (which is LDW's mode-2 c ~ 1/N). The closing count int r^{d-1-a(1-gamma)} dr is far-field for a(1-gamma)<d (always true inside 2a<d), ~ ln N at equality (s_c ~ (ln N)^{-1/(1-gamma)}), and near-field O(1) beyond (s_c = O(1), no N scaling). Sympy confirms the three integral regimes.
   - One symbol, two quantities (H12): s6b's a is used for (i) the gap-direction closing rate, (ii) the perpendicular motion entering C, and (iii) absolute displacement in "B -> 0". Wyart's property (c) (relative motion ~ absolute motion) is exactly what fails for a decaying response, so these can have different exponents.
   - It is also inconsistent to use theta_e for contacts whose modes decay (B -> 0). Those are LDW's small-b class, not the extended class.

3. **[HIGH] Addendum L33-34 (B): "MK packings are certified jammed (LP + rattler removal)... Hence at least one of L1-L3 is false in MK, or theta_l,MK=0 is pre-asymptotic."**
   - The page: CHB21 2011.10899 p4, Sec. II.B, says the sequential LP converges when "neither particle displacements nor size increases are possible" under the LINEARISED non-overlap constraint. Rattlers are removed and a single self-stress is kept.
   - That certifies first-order (linear) jamming. LDW/Wyart instability is second order: pdOmega = s f - s^2 c N<f>/a0 rises first and only turns negative beyond s*. A packing with kappa_alpha < 1 is still first-order jammed, with a finite barrier.
   - So a third option is missing: (iii) MK packings from this protocol are simply NOT stable in LDW's finite-opening sense. LDW stability is a marginality or protocol hypothesis (Wyart p4 avalanche argument), not a consequence of jamming.
   - CHB21 p15 says only "apparently violated". This is my reasoning from the pages, labelled [AUDITOR ARGUMENT], not a page claim.
   - Also, the N^{+0.149} count of unstable bucklers (arithmetic correct: 1 - 1/(2(1-0.41269)) = 0.14866) is asymptotic, with unknown O(1) prefactors. At N ~ 10^3-10^4 it is a few per packing at most, so it is not a finite-N contradiction (H10).

4. **[HIGH, already conceded by author] Addendum L47 (C): "that moment is finite whenever <zeta^2> = 1. So it does not change lambda."**
   - Lyapunov/Hoelder gives only <zeta^{1-gamma}> <= <zeta^2>^{(1-gamma)/2}, an UPPER bound.
   - Counterexample: zeta = N^x on a fraction N^{-2x} of pairs and 0 elsewhere has <zeta^2> = 1 but <zeta^{1-gamma}> ~ N^{-x(1+gamma)} -> 0. That changes the exponent (sympy).
   - "Heterogeneity changes only prefactors" needs an ADDED hypothesis: an N-independent positive lower bound on the conditional moment over APPROACHING pairs, with gaps independent of zeta.
   - Closing-count note s4 (L43-46) corrects this correctly. Its Hoelder exponents p=2/(1-gamma), q=2/(1+gamma) check out.
   - Consequence: Addendum C's "which assumption differs: L3" does not follow. Closing-count s5 L58 says the same.

5. **[MEDIUM] Addendum L15-16 (A): "stability iff kappa_alpha > 1 (Eq. 18) ... This statement uses no spatial assumption"; label "[EXACT to O(s^2)]".**
   - kappa is the quadratic-truncation diagnostic. s* is the zero of the truncated quadratic, and it is reliable only if O(s^3) is negligible at s ~ s*, s†.
   - kappa tests one floppy mode against one new contact. It is not global nonlinear stability.
   - LDW p5 state only "if kappa < 1 the packing is unstable". The converse (kappa>1 => stable) is not claimed. Call it a necessary-type, quadratic, local diagnostic.
   - s† itself is defined by the true nonlinear path. The first-order s† = min h/|u| needs signed approaching rates (u<0 in Addendum E, c>0 in the closing-count note; both conventions are internally consistent).
   - For MK, the contact vectors and gaps must use the shifted distance D(ri,rj) = |ri - rj + A_ij| (CHB21 p5), not Euclidean r_ij.

6. **[MEDIUM] Main note L43 (6a): "gamma_x = gamma iff (h, c) are asymptotically independent with N-independent <|c|^{1-gamma}>".**
   - Independence is SUFFICIENT, not necessary. The necessary and sufficient statement is: P(h <= X|c|, c approaching) ~ X^{1-gamma} as X -> 0, uniformly enough in c, with an N-independent, non-zero conditional moment. Dependent (h, c) whose conditional small-h exponent is still gamma, with bounded amplitude, also gives gamma_x = gamma.
   - The closing-count note s3 L40 states the right version (gamma_cond belongs to the conditional density, not bulk g).
   - Sign and definition are correct: x = h/|c| for c<0 (approaching) under dh = s c. Note that the brief's shorthand "min h/c" needs |c| or the sign convention c = -dh/ds (as in the closing-count note).
   - Also first order only: pairs with |c| <~ s q/... close by curvature (closing-count Caveat 3). Rattlers must be excluded because their motion is undetermined by the floppy mode.

7. **[MEDIUM] Main note L40 (s5): "In d=inf these hold (no neighbour correlations; saturation is a theorem there)".**
   - Overclaim. The d=inf result is a replica/fullRSB computation of exponents plus the a+b=1 identity (2606.03300). It is not a proof that Wyart's real-space closures (i)-(iii) hold.
   - The d=inf theory has no real-space floppy modes in which (ii) or (iii) could even be stated. Rewrite as "the d=inf exponents satisfy the saturated relation".

8. **[MEDIUM] Main note L27: Parisi-Zamponi labelled [THEOREM].**
   - Checked on the page: 2606.03300 v1 (2 Jun 2026) proves a+b=1 within the CKPUZ scaling fullRSB equations. That gives alpha = 1/(2+theta), where alpha is THEIR gap exponent, the note's gamma (H3/H12). See p1-2, Eqs. (2)-(4).
   - It takes as given (p4, s1.3) the scaling equations, b=(1+c)/2, the marginal-stability identities [7, Eqs. 193, 199], and the existence and uniqueness of the fullRSB profile and of the matching region. The proof was AI-assisted and checked by the authors (p2).
   - Relabel: "[PROOF CLAIMED, preprint v1, conditional on the stated taken-as-given items; d=inf only]". It proves an identity within the d=inf theory (equivalence of the two marginalities there, p2), not saturation of the finite-d bound.

9. **[MEDIUM] Main note L32 (s4 geometric reconstruction).**
   - The reconstruction (offset y -> h ~ y^2 with g(h) inherited, giving theta_l = 1-2gamma) assumes its conclusion: P(y) ~ y^{1-2gamma} is just the change of variables of the assumed gap law.
   - LDW obtain theta_l = 1-2gamma as SATURATION of the mode-2 stability bound (Eq. 23, p6), not from geometry. LDW Fig. 3c (p4) gives f = 2 f0 sin(theta) and b ~ sin(theta).
   - Already withdrawn by the author (Addendum D1, DEAD_ENDS line). I agree, and that DEAD_ENDS line suffices.

10. **[MEDIUM] Addendum L38 (C): "h_min ~ N^{-1/(1-gamma)} (verified for MK via Fig. 6 collapse)" and L28 "gamma_MK = gamma by finite-size collapse".**
    - Partly supported. CHB21 p11 and Fig. 6 caption (p12): the collapse in h~ = N^{1/(1-gamma)} h with the MF gamma is good. That does support the h_min scaling variable.
    - But the local slopes over 1e-3 < h~ < 1e3 are "not that predicted by MF theory", and "systems orders of magnitude larger would be needed" (p11-12). Below h~ ~ 1 the cdf is linear (the extra-contact effect).
    - Qualify as "supported by FSS collapse; pure power law not reached".
    - Separately, Addendum L34 says "no finite-size scaling for f_l is offered". CHB21 p13 do compare N and report "no clear finite N signature" for f_l, with left-tail dispersion in 7(a) and 7(d). Qualify the pre-asymptotic hedge accordingly. The 7(a),(d) -> 7(a),(b) typo reading at p13 is correct per the Fig. 7 caption.

11. **[LOW-MEDIUM] Closing-count note: what its caveats must carry. The algebra is correct, but the scope needs stating.**
    - (1) Campbell identity and {s_c<=s} = {N_close>0}: exact for the first-order s_c.
    - (3) Union bound and Cauchy-Schwarz lower bound: exact.
    - (4) EN/(1+(1+chi)EN): exact given E[N(N-1)] <= (1+chi)(EN)^2.
    - Caveats to carry:
      - (a) EN(s_*)=1 sets the closing SCALE only under regular (power-law) scaling of EN(s). Otherwise s_* is just a quantile-type lower scale (s2(i) is exact).
      - (b) chi_bar = O(1) gives P(s_c <= s_*) >= 1/(2+chi_bar), an ORDER-ONE probability, not high probability. Even as EN -> infinity the bound tends to 1/(1+chi_bar).
      - (c) s2 L31 "stable in EVERY realization" is stronger than LDW Eq. 22 (probability of an unstable contact <= 1/N). With stability at probability 1-eps, the conclusion becomes EN >= 1-eps. The exponent statement is unchanged.
      - (d) s5 conditions on the extreme-force buckler. Selection on f_min can bias rho_N(.|alpha) (extreme-value conditioning). Assumption (a) must say that the conditional law is unchanged by that selection.
      - (e) Caveat 3's curvature extension is itself a quadratic truncation. The exact closing region is {exists s'<=s: h_p(s') <= 0} along the TRUE nonlinear floppy path. The quadratic form is exact only where higher terms are negligible over the actual closure region. For MK, use shifted-distance geometry.
    - (6) algebra checked: N^zeta b_min^{1-gamma_c+mu} >~ 1 with b_min ~ N^{-1/(1+theta_l)} gives zeta(1+theta_l) >= 1-gamma_c+mu. LDW values give Eq. 23. The Addendum map eta = mu/(1-gamma) reproduces (1-gamma)(1+eta) <= 1+theta_l. All correct.
    - On MK specifically: CHB21 p12 note MK is effectively fully connected (shifts drawn from the whole volume). Candidate closing pairs are therefore not geometrically limited to O(N) neighbours in the conditional measure, which is one reason zeta and gamma_cond must be measured, not assumed. [auditor remark]

12. **[LOW] Closing-count s6 (EMT integral).**
    - Checked on the page: 1402.3834 SI p7, Eq. [A.18]: A1 = (z0/d) 2 pi^{d/2}/(Gamma(d/2)(2pi)^d) x {Lambda^{d-2}/(d-2), d>=3; (1/2) log(1/delta z), d=2}.
    - The note's radial integral and prefactors (1/2pi, 1/(2pi^2)) are correct. The reading q*^2 ~ delta z is consistent with (1/2)log(1/delta z) = log(Lambda/q*) at Lambda=1.
    - L65's general-d line omits the S_d/(2pi)^d prefactor (cosmetic).
    - Scope is correct as stated: this is a factor inside DeGiuli et al.'s tensor EMT, not a jamming d_c proof, and silent on rho_N and theta_l.

13. **[LOW] Citation and page slips (H15).**
    - Main note L11 "1411.3975 (p5)": the "remains thus far unanswered" quote is on p4 of arXiv v2.
    - L14 "one-loop RG gives no stable fixed point below 6": 1410.4523 abstract (p1) adds "except for a tiny region of the 1RSB breaking parameter".
    - L33 theta_e=0.42313 comes from 4-digit gamma. The paper gives 0.42311 (1411.3975 p1). Rounding, not an error.
    - L33 theta_eff is the pdf's local exponent, while 1411.3975 Fig. 1 plots the cdf G. The "equal amplitudes" is an assumption, and the "explains why theta_f grows" argument is 1411.3975's own (p4), so it should be attributed there.
    - L58 "CPA (PRE 111 045508)": abstract only (paywalled). That is a CPA for randomly diluted elastic networks / rigidity transitions. It does not address gamma or theta, so cite it as such.
    - L58 2006.09592 ✓ (p1: "no first-principles theory of jammed systems at finite dimensions exists"; one prefactor derived exactly).
    - Addendum symbol lambda collides with the hive's parked lambda coupling (H12). It is now renamed eta in the closing-count note L6, but Addendum body 500f984c still says lambda. eta is a response exponent, not a model coupling.

14. **[CLEAN] Signs.** pdOmega/pdV signs: the quadratic term is destabilising because f_ij > 0 and the projections are squared (Wyart Eq. 7-8, p3; LDW Eq. 15-16, p5). Approaching-pair conventions are consistent within each file. No printed sign errors were found.
15. **[CLEAN] Dimensions.** Clean on the algebra side, given dimensionless c and the a0 or sigma0 normalisation.
16. **[CLEAN] H2 (circularity).** No circular input apart from item 9 (s4, withdrawn) and the general point that theta_l = 1-2gamma is a saturation statement (Addendum L35, correct).
17. **[CLEAN] H11/H14.** No graded tolerances, so not applicable.

## Trustworthy derivation (what can be relied on)
**Wyart 1202.0259, pp. 2-3.** N hard frictionless spheres, isostatic (z=2d), rigid-wall box at pressure p. Opening contact <12> by s defines a unique floppy mode. Then:
- Second order, Eqs. 3-8: p dV = s f_12 - C + o(s^2), with C = sum f_ij [(dR_j - dR_i).n_perp]^2/sigma0 = A N <f> s^2/sigma0.
- The zero crossing is s* = f_12 sigma0/(A <f> N) (Eq. 9).
- P(f) ~ f^theta/<f>^{1+theta} and int_0^{f_min} P = 1/N_c give f_min ~ <f> N^{-1/(1+theta)} (Eq. 10), so s*_min/sigma0 ~ N^{-(2+theta)/(1+theta)} (Eq. 11).
- int_{sigma0}^{sigma0+h_min} g = 1/N_c with g ~ (r-sigma0)^{-gamma} (gamma<1) gives s_c ~ h_min ~ N^{-1/(1-gamma)} (Eq. 12).
- s_c < s*_min gives 1/(1-gamma) >= (2+theta)/(1+theta), i.e. gamma >= 1/(2+theta) (Eq. 13). With B(f) ~ f^delta: gamma >= (1-delta/2)/(2+theta-delta/2). Sympy reproduces both.

Hypotheses actually used:
- H-iso: exact isostaticity; one floppy mode per opened contact; hard spheres; no rattlers in the network.
- H-a (extended): B = lim <sum dR^2/(N s^2)> > 0 (Eq. 1), and the constant A is O(1) and N-independent for the weakest contacts, i.e. no correlation between f_12 and A beyond B(f) ~ f^delta.
- H-c: the relative displacement of adjacent particles is ~ the displacement of either one, so every nearby pair moves O(s).
- H-extreme-f: forces are independent enough for the typical-minimum estimate ("I expect to be approximatively true", under Eq. 10).
- H-extreme-h: s_c ~ h_min, which needs (h, closing rate) independence (6a / closing-count s3) and approaching pairs to be an O(1) fraction.
- H-trunc: the o(s^2) truncation is valid up to s* (fine as s* -> 0 for fixed geometry).
- H-scale: comparing typical extreme values fixes exponents only. Equality is undecided by the argument, which is why it reads ">=".
- Property (d) (force response of order F everywhere) is used only in the avalanche argument (p4), not in the bound. Main note L19 lists it as a bound assumption, which is harmless but imprecise.
- The force-response correlation is implicit: virtual work (Eq. 5) ties f_12 to the mode's boundary coupling. In LDW it is f = bW, and it is what makes s6b fail.

**LDW 1302.3990, pp. 3-6.**
- kappa_alpha = f_alpha a0/(c_alpha s† N <f>) (Eq. 18); c ~ 1/N + b^2; s† ~ h_min/b; f ~ bW with P(b,W) ~ P(b)P(W) (Eq. 12; independence checked numerically in their App. A, p8, for 3D binary spheres).
- These give kappa ~ W b^2 N^{gamma/(1-gamma)}/(1/N + b^2) (Eq. 20), mode 1: gamma >= 1/(2+theta') (Eq. 24) and mode 2: gamma >= (1-theta)/2 (Eq. 23). Sympy confirms all three.
- Their measured b uses medians of relative displacements (App. B, Eq. B4). Any reuse in Addendum E must use the same definition.

**Closing-count note s1-s5.** These are correct as exact or conditional statements with caveats 11(a)-(e). Equation (6), zeta(1+theta_l) >= 1-gamma_cond+mu, is a valid NECESSARY condition under its assumptions (a)-(e) plus the unbiased-selection condition. It recovers LDW Eq. 23. It does not single out L3.

## Still unverified (not computed yet; not "not computable")
- Not derived anywhere: theta_l, theta_e, eta, zeta, gamma_cond, mu, chi_bar, or MK's theta_l = 0. Also whether MK packings satisfy kappa > 1 at all, and whether CHB21's MK theta_l = 0 is asymptotic.
- Whether a decaying extended response can alter the extended bound once f = bW is respected. This needs W to correlate with the decay, which is not derived.
- How relevant second-order (curvature) closures are for small-c pairs.
- The 1/d (M-layer) programme of s6d for the EXTENDED closures. No jamming application was found, and bucklers are non-perturbative in 1/d (1411.3975 p4, "cannot be perturbatively detected", an inference there).
- Open status: in the sources I read, no controlled finite-d derivation of the closures exists. 1411.3975 p4 (2015) calls it "unanswered". Sartor et al. 2021 p1 say "no first-principles theory ... at finite dimensions exists". Hexner-Urbani-Zamponi 2019 (abstract) and Ikeda 2020 (abstract) give numerical evidence for d_u <~ 2. Thornton et al. 2025 (abstract) is a CPA for diluted networks. This is a coverage statement, not a theorem that none exists, and my search was not exhaustive (stopped once sufficient, per steering).

## Concrete next analysis (analytic, no sim, no new model)
1. Add an addendum to the main note that (i) withdraws s6b with the f = bW cancellation of item 1, and (ii) restates 6a and s5 per items 6-7. A one-page derivation is enough.
2. In the closing-count framework, write the mode-1 (extended) analogue of (6). Keep f = bW explicit, and allow M_N(b, W) and a W-decay correlation. Determine algebraically the minimal correlation structure that could move gamma off 1/(2+theta_e). This turns "why saturation survives in finite d" into a statement about one conditional measure rho_N(h, c, W | alpha).
3. Before any measurement spec, Helios should state precisely which stability notion MK/CHB21 packings satisfy: first-order LP jamming (item 3), the quadratic kappa diagnostic, or nonlinear stability. Any later measurement then compares like with like (H14). Addendum E's measurement list is reasonable once it uses LDW's median-based b (App. B, Eq. B4), MK shifted-distance contact vectors, signed approaching rates, and second-order closure checks. It is NOT launched or frozen here.

## Papers used and how much of each I read (for Orion's PAPER_LOG, relay if authorised)
- Wyart, arXiv:1202.0259 v2 (PRL 109, 125502): full text pp. 1-4, Eqs. 1-14 and refs.
- Lerner, Düring, Wyart, arXiv:1302.3990 (Soft Matter 9, 8252): pp. 3-8, Eqs. 7-24, Figs. 3-5, App. A mention, App. B data and median b.
- Charbonneau, Corwin, Parisi, Zamponi, arXiv:1411.3975 v2 (PRL 114, 125504): pp. 1-4 full main text plus App. A start.
- Charbonneau et al., arXiv:2011.10899 v3 (PRE 104, 014102): pp. 2, 4-5 (Sec. II.A-B, MK def.), 11-15 (Fig. 6, Fig. 7, Secs. V-VI, Table I).
- Parisi, Zamponi, arXiv:2606.03300 v1: pp. 1-4 (abstract, s1.1-1.3).
- DeGiuli, Lerner, Brito, Wyart, arXiv:1402.3834 v3 (PNAS): p1 abstract, p4 extended/localised text, SI p7 Eqs. A.17-A.18 only.
- Urbani, Biroli, arXiv:1410.4523: abstract p1 and the p2 quote only.
- Charbonneau, Yaida, arXiv:1607.04217: pp. 1-4 (d <~ 5.05 statement) only.
- Charbonneau, Hu, Raju, Sethna, Yaida, arXiv:1808.02767: abstract p1 only.
- Sartor, Ridout, Corwin, arXiv:2006.09592: abstract and p1 only.
- Müller, Wyart, arXiv:1406.7669: downloaded, not read.
- Abstracts only (web): Thornton-Cohen-Sethna-Liarte PRE 111 045508 (2025); Hexner-Urbani-Zamponi arXiv:1902.00630; Ikeda arXiv:2002.07557; Angelini-Palazzi-Parisi-Rizzo arXiv:2502.21089.
- Local copies of the papers are in lift/pdf_arxiv/venus_fd/ (new subfolder; PDFs + pdftotext).

Checks script: lift/tools/venus_fd_marginality_checks.py (algebra only).

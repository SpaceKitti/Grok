> **SEE ADDENDUM 2 of the main note: Venus 68ecb793 corrections to s A, B and C here (LP jamming vs LDW stability; L3 not singled out).**

> **SEE ALSO `HELIOS_BUCKLER_CLOSING_COUNT_NOTE.md` (2026-11-10): s4 there corrects s C here. A finite rms only upper-bounds the moment, and eta (= lambda here) <= 0.703 cannot single out L3.**

# ADDENDUM 1 to HELIOS_FINITE_D_MARGINALITY_NOTE.md: which spatial assumption in the LOCALIZED stability bound fails in Mari-Kurchan (2026-11-10, UK)
STATUS: working note, analytic only, no sims, independent of Akitti's construction. Grounded in ORION_JAMMING_FINITE_D_SOURCES_2026-11-10.md (I checked every source myself).
Sources page-checked via pdftotext:
- LDW = Lerner, Duering, Wyart, Soft Matter 9, 8252 (2013), arXiv 1302.3990: Eqs. 7-24, Fig. 3, Fig. 5, Sec. IV.
- CHB21 = Charbonneau, Corwin, Dennis, Diaz Hernandez Rojas, Ikeda, Parisi, Ricci-Tersenghi, PRE 104, 014102 (2021), arXiv 2011.10899: p2 Eqs. 1-3; p12 Fig. 7; p13 Sec. V; p14-15 Sec. VI, Table I.
Labels as in the main note: [EXACT] identity under stated definitions; [CONDITIONAL]; [ANSATZ]; [NUMERICS]; [NOVEL, UNTESTED].
theta_l (localized) and theta_e (extended) are kept apart throughout. Nothing below uses theta_e for buckler forces.

## A. The localized bound as actually derived (LDW Sec. III-IV)
- [EXACT to O(s^2), LDW Eqs. 14-18] Opening contact alpha by s along its floppy mode V^(alpha):
  p dOmega = s f_alpha - s^2 c_alpha N<f>/a0.
  c_alpha = sum_ij f_ij (V_ij . n_perp)^2 / (2 r_ij N <f>/a0) (Eq. 15).
  s† = opening at which a new contact forms. Stability index kappa_alpha = f_alpha a0 / (c_alpha s† N <f>), with stability iff kappa_alpha > 1 (Eq. 18).
  This statement uses no spatial assumption.
- The scaling closures LDW use, each stated on the page:
  - (L1) f_alpha / f_typ = b_alpha W_alpha (Eq. 10; exact as a definition). Here b = far-field amplitude ||V*||/<||V*||> (Eq. 8) and W = boundary coupling (Eq. 9). [ASSUMPTION] P(b,W) ~ P(b)P(W) with P(b) ~ b^theta_l and P(W) ~ W^theta_e (Eqs. 11-12; independence checked numerically in their App. A, Euclidean only).
  - (L2) c_alpha ~ 1/N + b^2: "a set of O(1) particles very close to the opened contact" with ||V|| ~ 1 carrying forces ~<f>, plus a bulk of order b^2 (Sec. IV). [ASSUMPTION]
  - (L3) "a contact must be created when the motion of the particles in the bulk, of typical amplitude b_alpha s†, is of order of h_min, leading to b_alpha s† ~ h_min", with int_0^{h_min} g = 1/N (Eq. 19). [ASSUMPTION; this is the spatial one]
- Result: kappa ~ W b^2 N^{gamma/(1-gamma)} / (1/N + b^2) (Eq. 20).
  - Mode 2 (b << N^{-1/2}, bucklers): kappa ~ N^{1+gamma/(1-gamma)-2/(1+theta_l)}, so gamma >= (1-theta_l)/2 (Eq. 23).
  - Mode 1 (b ~ 1): gamma >= 1/(2+theta_e) (Eq. 24).
  - LDW: "local buckling is, however, stabilized by the creation of a new contact in the far field."

## B. The counterexample, as published (CHB21)
- [NUMERICS] Euclidean d=3 monodisperse and d=2 polydisperse: cdf(f_l) ~ f^{1+theta_l} with theta_l ~ 0.17 (Fig. 7a,b). The p13 text says "Figs. 7(a) and 7(d)"; by the caption, 7(d) is MK, so this looks like a typo for 7(a),(b).
- [NUMERICS] MK d=3: "the best fit to the data is achieved with a unit slope, i.e., theta_l,MK = 0" (p13, Fig. 7d). The z = d+1 buckler selection still works. Contact-vector dot products of z_l particles have "a very similar distribution as those in standard hard sphere packings" (p13). gamma_MK = gamma by finite-size collapse (Fig. 6). theta_e is the MF value (Fig. 3c).
- Authors' heuristic (p13): with random shifts, the neighbours of i "are (very likely) not constrained by each other", so "opening a buckling contact produces a small series of uncorrelated displacements. No particular length scale is hence favored".
- p15: this "does not explain why the stability condition between gamma and theta_l is apparently violated". p14: the bounds "were derived [17, 36, 37] assuming, implicitly, that particles positions are uncorrelated".
- Arithmetic [EXACT]:
  - With the closures, MK has (1-theta_l)/2 = 0.5 > gamma = 0.41269, so Eq. 23 fails.
  - Under L1-L3 the expected number of unstable bucklers per packing scales as N^{1 - 1/(2(1-gamma))} = N^{+0.149}, which grows with N. MK packings are certified jammed (LP + rattler removal, CHB21 Sec. II.B).
  - Hence at least one of L1-L3 is false in MK, or theta_l,MK = 0 is a pre-asymptotic fit. The second possibility is not excluded: no finite-size scaling for f_l is offered, and the f_l cdf has left-tail dispersion in 7(d).
- Euclidean check: (1 - 0.17462)/2 = 0.41269. Eq. 23 is saturated, i.e. theta_l = 1 - 2gamma is a saturation statement, not an independent derivation.

## C. Which assumption, not just coordination: a one-parameter derivation [NOVEL, UNTESTED; conditional]
- Keep L1 (with W ~ O(1) for the weakest bucklers), keep L2 at mode-2 order (c ~ c_nf/N), and keep h_min ~ N^{-1/(1-gamma)} (verified for MK via Fig. 6 collapse).
- Replace only L3 by the ansatz s† ~ h_min b^{-lambda}. LDW's far-field blocking is lambda = 1. lambda < 1 means the blocking opening depends less strongly on the buckler's far-field amplitude.
- Then:
  - instability kappa < 1 <=> b^{1+lambda} < N^{-1/(1-gamma)}, so b_c ~ N^{-1/((1-gamma)(1+lambda))};
  - unstable count ~ N b_c^{1+theta_l} <= 1;
  - [CONDITIONAL] gamma >= (lambda - theta_l)/(1 + lambda) (sympy-checked; lambda = 1 gives Eq. 23).
- MK consistency with theta_l = 0 and gamma = 0.41269 requires lambda <= 0.7027. That is a quantitative, falsifiable statement of "which assumption differs": the 1/b scaling of the blocking opening (L3), i.e. that blocking happens in a far field whose relative pair motions are all of amplitude b.
- Why coordination alone does not do it [CONDITIONAL]:
  - MK's extra near contacts enter c_nf. A larger c lowers kappa (less stable), so it cannot rescue the bound.
  - Far-field heterogeneity at fixed rms b changes only prefactors if the gaps are independent of the pair motions. Number of closing pairs ~ N (s b)^{1-gamma} <zeta^{1-gamma}>, and that moment is finite whenever <zeta^2> = 1. So it does not change lambda.
  - Exponent-changing candidates are therefore: (i) blocking by a channel whose displacement does not scale with b (near-field or intermediate-cascade pairs moving O(s) with gaps that are small and correlated with the buckler, i.e. h and u correlated); (ii) a failure of L1 (b-W correlation, or f not proportional to b). This is my reading of CHB21's "uncorrelated displacements", not theirs.
- Limitation: no derivation of lambda or theta_l,MK from MK structure is given here. The ansatz is power law in b by assumption.

## D. Corrections to the main note
- D1 (withdrawn as a general mechanism). Main note s4 "geometric reconstruction" (offset y -> gap h ~ y^2 inheriting g(h), giving theta_l = 1 - 2gamma). MK has similar local contact geometry and the same gamma, yet theta_l = 0 (CHB21 Fig. 7d). So "local geometry + inherited g(h)" cannot fix theta_l. The hidden step is a spatial/marginality correlation between the buckler offset and the blocking gap, not geometry. LDW instead read theta_l off P(b) and Eq. 23 saturation. Note: LDW Fig. 3c gives b ~ sin(theta), and a smooth density of the coplanarity angle would give P(b) ~ b^0, which matches MK's theta_l = 0 [ANSATZ consistency only]. Euclidean theta_l = 0.17 > 0 then needs suppression of near-coplanar bucklers, plausibly by marginal stability itself.
- D2 (scope of s6d). A 1/d (or M-layer) expansion around d = inf can at best address the EXTENDED-sector closures. Bucklers have n_l ~ exp(-c d) (1411.3975 Eq. 2 and large-deviation fit; their wording: "cannot be perturbatively detected around that solution either", an inference, not a theorem), which is non-perturbative in 1/d. No claim that a 1/d expansion captures theta_l.
- D3. The main note's mixture-crossover f_x needs theta_l < theta_e AND n_l > 0. In MK theta_l = 0, so f_x changes exponent (1/(theta_e - 0)). Order of limits (f -> 0 vs d -> inf) matters, as Orion noted.

## E. Source-backed discriminant (next test; exact linear algebra on existing packings, no new model)
- For each z_l = d+1 contact in Euclidean d=3 and MK d=3 packings (CHB21 ensembles, or LDW protocol), compute:
  - V^(alpha) from the rigidity matrix;
  - b_alpha (Eq. 8) and W_alpha (Eq. 9);
  - c_alpha (Eq. 15);
  - s†_alpha = min over non-contact pairs (kl) with u_kl < 0 of h_kl/|u_kl| (u_kl = d h_kl/ds along V^(alpha));
  - the graph distance of the blocking pair from alpha;
  - kappa_alpha (Eq. 18).
- Measure:
  - (1) the exponent lambda from s† vs b; prediction lambda ~ 1 Euclidean, lambda <= 0.70 MK if C is right;
  - (2) whether MK blocking pairs are near-field (as hypothesised) rather than far-field;
  - (3) corr(b, W) in MK, testing L1;
  - (4) N dependence of cdf(f_l) in MK, to rule out a pre-asymptotic theta_l = 0.
  If lambda = 1 and L1 holds in MK, then C is falsified and the violation must be pre-asymptotic or come from W.
- Does it already exist? LDW measured kappa over all contacts (Fig. 5 b-W plane) in Euclidean only. CHB21 did not measure s† or kappa. I found no MK kappa/s† measurement in the sources checked [coverage selective].

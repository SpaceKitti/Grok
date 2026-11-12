> **SEE ADDENDUM 2 (2026-11-10): `HELIOS_FINITE_D_MARGINALITY_NOTE_ADDENDUM_2.md` applies Venus audit 68ecb793. s6b is WITHDRAWN as a bound (f=bW cancels a). Also relabels 6a, s5, s3 and Parisi-Zamponi.**

> **SEE ADDENDUM 1 (2026-11-10): `HELIOS_FINITE_D_MARGINALITY_NOTE_ADDENDUM_1.md` grounds the localized bound in LDW 2013 eqs 13-24 and the Mari-Kurchan counterexample (2011.10899). It withdraws the s4 buckler-geometry reconstruction as a general mechanism and restricts s6d to extended-sector closures.**

# HELIOS working note: the d=inf -> d=3 jamming gap through extended vs localized marginal stability (2026-11-10 ~10:05 UK)
STATUS: working note, analytic only, no sims. INDEPENDENT of Akitti's construction (scope correction from NanoRibbon, 10 Nov: the idea that her construction should address the gap was NanoRibbon's, not hers). HELIOS_JAMMING_3D_GAP_NOTE.md and ADDENDUM_1 are context only; nothing here is a gate on her construction.
Open-problem check: STILL_TO_DO.md:205 jamming OPEN; 1202.0259, 1411.3975, 1310.2549, 2606.03300, 1410.4523, 1607.04217, 1808.02767, cond-mat/0508415, 2006.09592, PRE 111 045508.
Idea owner: question = Akitti post 2119613243593302457 item 1 (Grok text she pasted, tagged possibly hallucinated). Lead choice and derivations = hive proposal (Helios).
Dimension note: general d; physical target d=3.
Labels: [THEOREM] = proved under stated hypotheses; [CONDITIONAL] = derived under stated assumptions, not proved; [NUMERICS] = observed; [HYPOTHESIS] = working hypothesis; [NOVEL, UNTESTED] = mine, not checked against literature (may duplicate known work).

## 1. Why this lead
1410.4523 (Urbani-Biroli) separates two finite-d questions: "how the Gardner transition and its critical properties change from infinite dimension down to three, and ... how the soft modes of the symmetry broken phase change". It also says jamming exponents "are not exponents related to a phase transition". So the jamming exponents hinge on the second question: marginal stability of the contact network. 1411.3975 (p5) names the unresolved step: "why long-wavelength fluctuations do not renormalize the properties of jamming criticality ... remains thus far unanswered". The marginal-stability inequalities are the one place where a finite-d closure is explicit and checkable, so I take that route.

## 2. Gardner vs jamming (kept separate)
- Gardner: a landscape transition at finite pressure inside the glass (replicon -> 0). Finite-d status by method: one-loop RG gives no stable fixed point below 6 (1410.4523). Two-loop RG gives a strong-coupling stable fixed point for d<6, robust for d <~ 5.05 after Borel resummation with three-loop input (1607.04217, PRL 118 215701). A possible limit cycle follows, "debate persists" (1808.02767). [UNSETTLED]
- Jamming: the p -> inf endpoint. Its exponents (gamma, theta_e, theta_l, kappa) are controlled by isostaticity + marginal stability. They can be robust even if Gardner criticality is modified. [HYPOTHESIS, consistent with NUMERICS 1411.3975]

## 3. The conditional constraint, reproduced (Wyart 1202.0259, PRL 109 125502)
Setting: N frictionless hard spheres, isostatic, pressure p, diameter sigma0. Opening contact <12> (force f) by s defines a floppy mode dR(s).
Assumptions as stated on the page: (a) floppy modes are extended, B = lim <sum_i dR_i^2/(N s^2)> > 0 (Eq. 1); (b) B(f) ~ f^delta for weak contacts (delta = 0 default); (c) relative motion of nearby pairs ~ s; (d) force responses random. Forces "treated as independent variables" (stated under Eq. 10).
Derivation:
  p dV(s) = s f - C,  C = sum_{<ij> != <12>} f_ij [(dR_j - dR_i).n_perp]^2 / sigma0 = s^2 A N <f>/sigma0      (Eq. 6-8)
  denser state reachable if s exceeds s* ~ f sigma0 /(<f> N)                                                  (Eq. 9)
  P(f) ~ f^theta: int_0^{f_min} P = 1/N  =>  f_min ~ <f> N^{-1/(1+theta)}  =>  s*_min/sigma0 ~ N^{-(2+theta)/(1+theta)}   (Eq. 10-11)
  g(r) ~ (r - sigma0)^{-gamma}: int g = 1/N  =>  s_c ~ h_min ~ N^{-1/(1-gamma)}                                (Eq. 12)
  stability s_c < s*_min  =>  gamma >= 1/(2+theta)                                                             (Eq. 13) [CONDITIONAL]
  with delta != 0: gamma >= (1 - delta/2)/(2 + theta - delta/2)  (stated after Eq. 13).
Saturation gamma = 1/(2+theta_e) is PROVED only inside the d->inf fullRSB scaling solution: a+b=1 gives alpha = 1/(2+theta) (Parisi-Zamponi 2606.03300; they take existence of the fullRSB profile and of the scaling regime as given) [THEOREM, d=inf, under those hypotheses].

## 4. Localized (buckler) sector and the two-exponent force law
- Relations quoted in 1411.3975 p1 (refs [1,14-16]): theta_l = 1 - 2 gamma, theta_e = theta_l/gamma [CONDITIONAL; primary derivations not re-checked on page here].
- Algebra check: saturation gamma = 1/(2+theta_e) gives theta_e = 1/gamma - 2 = (1-2gamma)/gamma = theta_l/gamma. Identical. With gamma = 0.41269: theta_e = 0.42313, theta_l = 0.17462, theta_e - theta_l = 0.24851.
- Geometric reconstruction of theta_l [reconstruction, consistent with the quoted relation; not taken from the page]: a buckler has d nearly coplanar strong contacts offset by y out of plane. Force balance gives a weak force f_w ~ <f> y/sigma0. The offset enters distances at second order, so it acts like a gap h ~ y^2/sigma0. If h inherits g(h) ~ h^{-gamma}, then P(f_w) = g(h) dh/df_w ~ f_w^{-2gamma} f_w = f_w^{1-2gamma}, i.e. theta_l = 1 - 2gamma.
- Mixture (1411.3975 Eq. 2): P(f) = n_l P_l + (1 - n_l) P_e, with n_l = (d+1) P_c(d+1)/2d decaying exponentially in d [NUMERICS + argument there]. Derived: with equal amplitudes the crossover force is f_x = (n_l/(1-n_l))^{1/(theta_e - theta_l)} = (n_l/(1-n_l))^{4.02}. So n_l = 0.1 gives f_x ~ 1.4e-4 <f>; n_l = 0.01 gives ~ 1e-8. Effective exponent theta_eff(f) = [n_l theta_l f^theta_l + (1-n_l) theta_e f^theta_e] / [n_l f^theta_l + (1-n_l) f^theta_e]. This explains why "theta_f grows steadily with d" (1411.3975 Fig. 1) without any change of gamma [CONDITIONAL]. The d=inf solution has n_l = 0, and 1411.3975 notes the buckler contribution "cannot be perturbatively detected around that solution".

## 5. The precise unresolved step
Wyart's bound uses three factorisation closures:
 (i) forces independent (extreme value f_min);
 (ii) gaps independent of the floppy-mode response (s_c ~ h_min, every nearby pair moves O(s));
 (iii) uniform extended participation, which sets C ~ s^2 N <f>.
In d=inf these hold (no neighbour correlations; saturation is a theorem there). In finite d the gaps h_kl, the response coefficients c_kl (with dh_kl = s c_kl) and the weak forces all come from the SAME contact network, so (ii)-(iii) are hypotheses. Numerics (1411.3975: theta_e and gamma at d=inf values in d=2-4, after removing bucklers and rattlers) say saturation survives. No derivation explains why. That is the gap at the level of marginal stability.

## 6. Analytical route [NOVEL, UNTESTED]
6a. Replace g(h) by the mode-projected gap. For the mode opened at a weak contact define x_kl = h_kl/|c_kl| for c_kl < 0 (pairs that approach). Then s_c = min x_kl, and the bound as derived constrains the exponent gamma_x of the small-x density, not gamma: gamma_x >= 1/(2+theta). gamma_x = gamma iff (h, c) are asymptotically independent with N-independent <|c|^{1-gamma}>. That is exactly closure (ii).
6b. Spatially decaying response. Suppose |c(r)| ~ r^{-a} at distance r from the opened contact (a = 0 is Wyart's extended case). Then the closing-pair count is n(s) ~ s^{1-gamma} N^{1 - a(1-gamma)/d}, so s_c ~ N^{-1/(1-gamma) + a/d}. Also C ~ s^2 <f> N^{1-2a/d} (2a < d), so s* ~ f N^{2a/d - 1}. Stability:
  1/(1-gamma) > (2+theta)/(1+theta) - a/d
  => gamma >= [1 - (a/d)(1+theta)] / [2 + theta - (a/d)(1+theta)]  =  1/(2+theta) - (a/d)(1+theta)^2/(2+theta)^2 + O((a/d)^2)
  (sympy check done). The correction is O(a/d), so it vanishes at d=inf for fixed a, matching mean-field exactness there. Observed saturation in d=2,3 therefore REQUIRES a = 0 (or cancellation between 6a and 6b effects). 2a < d with a > 0 means B -> 0, so this is the spatial version of Wyart's delta generalisation.
6c. Measurable missing ingredients (packing data, exact linear algebra on the rigidity matrix, no new physics model):
  (1) gamma_x vs gamma, from x_kl for floppy modes of the weakest extended contacts;
  (2) the response profile exponent a and participation scaling B(N) for weak vs typical contacts (B ~ f^delta, so delta too);
  (3) the joint density of (f, h) for the SAME particle's neighbourhood (tests closure (i)-(ii) locally);
  (4) n_l(d) and the amplitudes A_l, A_e, to make the crossover f_x quantitative.
  Prediction if saturation is structural: gamma_x = gamma, a = 0, delta = 0 for extended contacts in d=2,3. Any measured a > 0 or gamma_x != gamma with unchanged gamma would mean saturation holds for a different reason (compensation), and the factorised argument is not the mechanism.
6d. Analytical step after that: compute <|c|^{1-gamma}> and the h-c covariance at leading order in an expansion around d=inf (neighbour correlations O(1/d)). The M-layer/Bethe-type loop expansion exists for spin glasses in a field (2502.21089). For jamming I found no applied version. Adapting it to the contact network would give the first controlled 1/d correction to closures (ii)-(iii) [HYPOTHESIS that this is tractable].

## 7. What is NOT claimed
- Not claimed that finite-d jamming is unsolved in general: existence, isostaticity and exponents are well supported numerically (0911.1384, 1204.4915, 1209.0705, 1411.3975, 2006.09592).
- Not claimed that no controlled finite-d theory exists anywhere; only none found in the sources checked (to June 2026). CPA (PRE 111 045508, 2025) gives d_upper = 2 within an approximation. 2006.09592 derives one finite-d prefactor exactly.
- No link to the fuzzy-cone construction is asserted.

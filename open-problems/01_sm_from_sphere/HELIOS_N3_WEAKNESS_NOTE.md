# Helios note: does our S² have the paper's weakness, and what could fix it (N3, arXiv:2610.08939)

Helios, physics rows (units, placeholder inputs, toy-vs-new-physics, H1, H7, H8, H9, H13). Status: untested proposal inside problem 1. For Venus pre-check.
Revised 2026-10-08, about 16:58 BST, after Venus's pre-check (`VENUS_N3_NOTE_PRECHECK.md` 4D247037, HOLD; previous version 55D26152). Not sent anywhere. Goal (Akitti 16:37 via NanoRibbon): find whatever fixes the weakness our S² likely has; she isn't tied to n2 [Akitti, via NanoRibbon 16:37].
Sources (all on the box, `/workspace/lift/` unless stated):
- framework `AKITTI_FRAMEWORK_2026-10-08.md` 6CD5F259 ("L" = its line, where cited as framework).
- posts `AKITTI_POSTS_OCT1-8.md` F1C6CC26, L4352-4459 (post 2108092102886211700, Oct 8 08:08 BST).
- Orion's check `N3_2610.08939_CHECK.md` C30ED955; paper text `papers/2610.08939.txt` (PDF 69D94C6B; "p." = printed page; every quote and page checked by Orion, 16:47 BST).
- D1 `/workspace/oldlift/jobs/sm-zero-modes-S2/`: RESULTS.md FEF2BA79 (= SpaceKitti/Grok@1fe72c2), RESULTS_final.md 78C1BC24 (added in 67c711a), run.py DCE6413E.
- B0 SpaceKitti/Grok@1fe72c2:jobs/b0-taubes-base/RESULTS.md AE4E8FFB. Job Five RESULTS 345FB29A @ f982965.
- Part B 3037E19D; inputs spec DB7ECF85; SM1_INPUTS E0D7D41D; Venus's check 4D247037 (scripts in `venus_n3_check/`).
Symbols [Venus N5, B3]:
- κ is our abelian-Higgs coupling (inputs spec); the paper's curvature sign of Σ is κ_Σ (H12).
- α is the framework's cone parameter (0 < α ≤ 1). Her post's α is a different object, the flag-ratio target, written α_flag here.
- n1, n2 have four meanings: (A) B0 vortex numbers, one per abelian-Higgs sector (§2(ii)); (B) D1-type U(1) fluxes in q = xn/2 (§2(iii)); (C) her post's «flag fluxes \(n_1,n_2\)» (L4390); (D) the paper's flux quanta (flag n1, n2 in Sec. 3; p₁, p₂ on Σ, p.22 eq. (4.9)). (A) and (B) coincide only for a unit-charge abelian-Higgs scalar on the same U(1).
- ε has three meanings: ε_B0 = B0's area excess (A = 4πn(1 + ε_B0)); ε_post = her post's ε; ϵ = the paper's (p.3).
- q is D1's Wu–Yang charge: D = d − iA, A_N = q(1 − cos θ)dφ, eF₁₂ = q/R², 2q ∈ ℤ, q = xn/2 [Venus §A].

## §0 Premises (one line each)
- n2 on our S² tip is a hive idea from her post as Grok wrote it: «The upgrade adjoins a second integer charge \(n_2\) to the same tip» (L4380) [from her posts; untested; 2108092102886211700] [possibly Grok-written].
- The paper's Sec. 4 S² solutions already carry two fluxes: p.22 eq. (4.9) «Z ∋ pi ≡ (1/2π)∫Σ 2mFi = 4mR² fi (g − 1)», i = 1, 2 [H1 control: paper sugra; quoted via Orion C30ED955].
- All non-SUSY ones are perturbatively unstable: p.19 «Unfortunately, we will find them all to be perturbatively unstable.»; p.24 after eq. (4.14) «this always has an eigenvalue ≤ −4, with equality only on the supersymmetric locus (4.4).»; p.25 «this mode violates the BF bound in all the non-supersymmetric solutions» [H1 control: paper sugra].
- The working two-flux construction is the flag manifold F6 (Sec. 3), not an S²; the paper never deforms the S² (Orion C30ED955 §(a)) [H1 control: paper sugra].
- Paper sugra is an H1 control only. Our core gravity is unknown QG [Akitti]; no paper equation enters a core computation.
- Sign: p.3 below eq. (2.4) «σ = σcrit (1 − ϵ)»; eq. (2.5) «ρΛ = σcrit ϵ»; «positive when ϵ > 0» [H1 control: paper sugra].
  - Her post's «\mu=\mu_{\mathrm{crit}}(1+\epsilon)» (L4382; ε here is ε_post) [from her posts; untested; possibly Grok-written; contradicted by p.3] is the opposite sign and a different object.
  - Her μ = Σ t_a is the string pile-up tension, L4378; the paper's σ is a  5d brane tension [from her posts; untested; 2108092102886211700] [possibly Grok-written]. 
  - Not carried across, not flipped.
- "ε_post set by how close n1/n2 is to α_flag" (L4458): NOT COMPUTED (YET) in the toy. The paper's ϵ ∼ δ² is a scaling around the flag model's algebraic n12, p.16 eq. (3.33) «|n12(p1) − n1+/n2+| < δ², δ⁻¹ ∼ n2+» and «ϵ ∼ δ²» [H1 control: paper sugra]. We have no n12 analogue [open].
- α_flag stays symbolic. Her post's α is the flag-ratio target: L4366 «where \(\alpha\) is the irrational value fixed by the homogeneous metric and the calibration»; L4391 «irrational \(\alpha\) | extremality target» [from her posts; untested; 2108092102886211700]. α_flag = √2 is «schematic stand-in for the paper's irrational» in her post's code (L4424) [possibly Grok-written]; the paper's targets are n12(p1) ≃ 0.795888, n12(p2) ≃ −0.891851 (p.16) [H1 control: paper sugra].
- α_flag is a ratio target, not the cone angle: no cone constraint (α = 1 − 4Gμ, 0 < α ≤ 1) applies to it [Venus B3]. The cone α is unchanged.

## §1 Does our toy have the weakness? Two kinds of mode, kept strictly apart [Venus]
- (a) FIELD mode on a fixed round sphere. D1 RESULTS:197 «Tachyon formula [computed + standard: RSS 1983]: M^2 R^2 = j(j+1) - q^2 with j >= |q| - 1. At the lowest level M^2 = -|q|/R^2 exactly»; RESULTS:200 «| 3 | 2 | -3 | 5 | lowest level |»; RESULTS:203 «q = 3 gives j = 2 with M^2 = -3/R^2 and 5 modes, j = 3 with +3/R^2» [hive-run: sm-zero-modes-S2 (D1), SpaceKitti/Grok@1fe72c2:jobs/sm-zero-modes-S2/RESULTS.md:197-203]. The table is hand-entered at run.py:295 (`tachyon_rows = [...]`), not code output [typed from formula] [Venus N7].
  - Confirmed independently [Venus, VENUS_N3_NOTE_PRECHECK.md 4D247037; scripts in venus_n3_check/]: both helicities have M²R² = j(j+1) − q², with j ≥ ||q| − 1| (aligned) and j ≥ |q| + 1 (other). The lowest level is −|q| exactly; the Ricci +1 cancels the spin-connection shift, and the spin-term sign (c = +2) is fixed by gauge invariance.
  - D1:197's "j ≥ |q| − 1" holds only for |q| ≥ 1. There is a tachyon if and only if |q| ≥ 1; at |q| = 1/2 the lowest level is +1/2 [Venus §A].
  - The j = |q| level (2|q| + 1 states; for q = 3, +3/R², 7 modes) is pure gauge: the Goldstones eaten by the massive charged 4D vectors [Venus §A].
  - **The field tachyon is a property of the rejected MAIN branch only** (S3, S4, S6, rejected by Rule S1 and tr R⁴; Part B 3037E19D §2.2(d), (e)) [Venus N2].
  - D1's final answer is ALT: RESULTS_final.md:10 «Higgs: an ordinary 6D scalar doublet with x = 0, so it sees no flux; its potential (mu^2 < 0) is [assumed input]»; :77 «the Higgs has no flux tachyon» [hive-run: sm-zero-modes-S2 (D1), RESULTS_final.md:10,77]. So the field-mode weakness is absent from the surviving (ALT-type) candidates at tree level [Venus N2].
- (b) GEOMETRY mode (breathing/shape of the S² with flux): this is the paper's instability (scalars of the reduction, p.24 eq. (4.14)) [H1 control: paper sugra]. In our toy, under the lift's (unknown QG) gravity: NOT COMPUTED (YET) in any hive run. It can't be computed in-toy without a gravity theory for R; only a [GR control] row is possible.
  - The breathing (radion) mode has been computed only as a [GR control]: Job Five «V(x) = aΛ_6/x − b/x² + cn²/x³ with a = 4*pi, b = 4*pi*M_6**4, c = pi/(2*g_6**2)» (x = R², i.e. V(R) = R⁻⁴(aΛ6 R² − b + c n²/R²) [identity]) and «Flat stationary point | x*=2cn²/b; Λ_6=b²/(4acn²); V''(x*)=b/x*^4=2cn²/x*^5: True [identity]», so V'' > 0 at the flat vacuum (b > 0) [Λ₆ tuned to the flat point] [GR control; hive-run: radion-onshell-filter (Job Five), SpaceKitti/Grok@f982965:jobs/radion-onshell-filter/RESULTS.md:19,30], with the radius normalisation [assumed]. Maths re-verified [Venus N9]. Shape modes (non-breathing) of the S²: NOT COMPUTED (YET).
  - Parked problem-2 item (Dilaton wall): STILL_TO_DO.md:146 (AF8451F4) «In de Sitter the dilaton and breathing mode are tachyonic, so dS is unstable [standard: Guo-Pang-Sezgin arXiv 2510.11794]» (Salam–Sezgin, dilaton free). Not a problem-1 item.
- Our toy has no AdS factor, so the test is plain M² < 0. Do not import the BF bound or the "eigenvalue ≤ −4" threshold [Venus].
- (c) Hierarchy: paper flag model R⁻¹ ∼ Λ4^(1/4) (p.2), Sec. 4 «Λ4 ∼ R−2» (p.23) [H1 control: paper sugra]. Our toy computes no Λ4: NOT COMPUTED (YET). Not a problem-1 item.

## §2 What n2 means in the toy, and the two integral tests
- (i) ∫K dA: with the frozen exterior and a fixed background geometry, adding a gauge flux does not change ∫K over the core disk; Gauss–Bonnet with fixed boundary turning gives ∫_D K dA = 2π(1 − α) (Part B §1.3) [identity] [by construction; not a test] [Venus N3]. This is the total including the tip's delta; per Part B §1.3 the smooth part is 0 on tip rows and the full 2π(1 − α) only on tipless rows [Venus H3, 17:01]. With backreaction: NOT COMPUTED (YET).
- (ii) Set-up A, two decoupled abelian-Higgs sectors (n1, n2 = meaning (A)). ∫T_tt = μ: a second flux adds magnetic and gradient energy, so μ shifts unless compensated [standard].
  - Each sector's Bogomolny bound is E_i ≥ π|n_i|, saturated independently (BPS or anti-BPS), so μ = π(|n1| + |n2|) at κ1 = κ2 = 1, with each sector above its own Bradlow bound A > 4π|n_i| on the fixed S² [identity: Bogomolny; Venus B2; units of B0, e = v = 1]. Example (Venus): (n1, n2) = (4, −1) has n1 + n2 = 3 but μ = 5π.
  - So only assignments keeping |n1| + |n2| fixed keep μ fixed [identity at κ1 = κ2 = 1]. Off-critical: NOT COMPUTED (YET); it would come from the inputs-run κ scan, κ ∈ {0.25, 0.5, 1, 2, 4} (inputs spec DB7ECF85 §3b).
  - Same-U(1) case (her «second integer charge \(n_2\) to the same tip», L4380, read as a second unit of the same U(1)): μ = π|n1 + n2| at κ = 1, n2 is identically a retuning of n, and the Bradlow condition is A > 4π|n1 + n2| [identity; Venus B2]. Her table calls n1, n2 «flag fluxes» (L4390), which favours two U(1)s [Venus B2].
  - In set-up A, D1's gauge-Higgs field A_z has zero U(1)_2 charge (x2 = 0), so n2 cannot touch the field tachyon at all [Venus N4].
- (iii) Set-up B, one field charged under both U(1)s (n1, n2 = meaning (B)): q_eff = (x1 n1 + x2 n2)/2 [standard: monopole charges of commuting U(1)s add]. For A_z, x2 is set by the gauge-Higgs embedding (a root of G), not free [Venus N4].
  - A spin-0 charged scalar on S² with monopole charge q has Wu–Yang monopole harmonics: lowest −D² eigenvalue |q|/R² (positive), degeneracy 2|q| + 1 [standard: Wu–Yang 1976]. So flux alone gives a scalar no tachyon.
  - D1's MAIN Higgs is not spin 0: it is «an internal gauge-field component A_z (spin weight 1), i.e. gauge-Higgs unification» (D1 RESULTS:195) [hive-run: sm-zero-modes-S2 (D1), RESULTS.md:195]. Its 5 modes = 2j + 1 at j = |q| − 1 = 2, i.e. 2|q| − 1 for q = 3 [identity]; not the spin-0 count 2|q| + 1 = 7, which is the pure-gauge j = 3 level [Venus §A].
  - **Tachyon-free if and only if |q_eff| ≤ 1/2** [identity: Venus §A]. In the tachyon-free cases the lightest physical A_z mode is (3|q_eff| + 2)/R² ≥ 2/R², so no light gauge-Higgs scalar is left [identity on the round S², tree level; Venus B1(a)].
  - Per-U(1) gauge invariance of the Yukawa coupling makes q_eff linear and closed: q_H,eff = q_L,eff − q_R,eff (D1's closure, RESULTS:150) [Venus B1(b)].
  - In MAIN all fermions have Γ₇ = −1; three chiral generations need |q_L,eff| = |q_R,eff| = 3/2, with q_L,eff = +3/2 (4D left) and q_R,eff = −3/2 (4D right), hence **|q_H,eff| = 3 whatever n2 is** [Venus B1(c), (d)]. The other choice q_L,eff = q_R,eff gives q_H,eff = 0, but both fermions are then 4D left and the Yukawa vanishes by Lorentz symmetry (D1 Assignment B, RESULTS:163–167) [hive-run: sm-zero-modes-S2 (D1)].
  - So, at tree level on the round S² in the gauge-Higgs case, n2 cannot remove the tachyon and keep three generations with an allowed Yukawa [Venus B1]. This answers the former "Higgs's role" open item.
  - Count range: the formula N_Φ + 1 − 2s (Part B 3037E19D line 137) is the aligned lowest-level degeneracy only for N_Φ ≥ 2s − 1 (at N_Φ = 0, spin 1 it gives −1; the true count is 0) [Venus N6].
  - On a conical tip: NOT COMPUTED (YET). None of this says anything about the geometry mode (§1(b)).

## §3 How it plugs into problem 1
- New SM1_INPUTS slots (proposal; not added; only if n2 is revisited outside the gauge-Higgs case): `n2`, `kappa2` (second coupling), `charges_U1_2` (each field's charge under U(1)_2). All NOT COMPUTED (YET).
- The inputs-run κ scan would extend to (κ1, κ2) or to two decoupled sectors [assumed; needs a spec revision and Venus's check].
- Former run 1 (monopole-harmonic table) is answered analytically [Venus §D; round S², D1 normalisation]:

| q_eff | spin 0 lowest M²R² (count) | A_z aligned lowest (count) | lowest physical A_z | tachyon? |
|---|---|---|---|---|
| 0 | 0 (1) | +2 (3) | +2 (3) | no, and no light A_z |
| 1/2 | +1/2 (2) | +1/2 (2), pure gauge | +7/2 (4) | no, and no light A_z |
| 1 | +1 (3) | −1 (1) | −1 (1) | yes |
| 3/2 | +3/2 (4) | −3/2 (2) | −3/2 (2) | yes |
| 3 | +3 (7) | −3 (5) | −3 (5) | yes (D1) |

- Run 2, critical two-sector vortex check μ = π(|n1| + |n2|) against B0 (RESULTS:73): regression only (two copies of B0; it can fail only through a coding error) [Venus N3] [proposal].
- Framework L18: «Any wrapping, flux, or zero-mode assignment that shifts either integral is discarded.»; L26: the Betti–Berry spike is applied «only after the integral test has pruned the wrappings and fluxes» [Akitti]. So any n2 assignment that moves ∫K or ∫T_tt is discarded before the spike filter.

## §4 Ranked candidates
| rank | candidate | targets | keeps ∫K, ∫T_tt? | cost in toy | inside problem 1? | status |
|---|---|---|---|---|---|---|
| withdrawn | second charge n2 | field mode (via q_eff) | ∫K by construction [Venus N3]; ∫T_tt only if \|n1\| + \|n2\| fixed, at κ1 = κ2 = 1 [identity] | — | yes | WITHDRAWN as a fix: closed at tree level on the round S² for the gauge-Higgs Higgs [Venus B1]; x2 = 0 in set-up A [Venus N4]; the tachyon is in rejected MAIN only [Venus N2]. Origin [from her posts; untested; 2108092102886211700] |
| 1 (check, not a fix) | vortex-sector stability check (κ = 1) | vortex fluctuations: at BPS the operator is non-negative (2n zero modes); for κ > 1 the n ≥ 2 vortices have splitting modes (type II) [standard: Jacobs & Rebbi 1979; Weinberg 1979] | yes (μ topological at κ = 1) [standard] | free: already in the scan | yes | Does not remove D1's tachyon: κ does not appear in D1's operator [identity on D1's background; Venus N1]. Analogy to the paper's SUSY locus (p.24 after eq. (4.14)) [hive-interpretation] |
| — | flag manifold F6, n1/n2 near an algebraic number (Sec. 3) | geometry mode (in the paper) | changes the internal space | outside toy | no: leaves our S² framework; parked | [H1 control: paper sugra]; see caveats below |
| — | higher genus, κ_Σ = −1, g ≥ 2 | geometry mode (in the paper) | changes topology | outside toy | no; parked | [H1 control: paper sugra]; moduli: p.2 «We restrict to Σ = S 2 in order to avoid moduli» |
- Flag caveats, quoted [H1 control: paper sugra]:
  - p.18 «Not all solutions satisfy the BF-bound there, in particular those close to the tip of the boomerang»
  - p.19 for F6 «the answer is not currently known»
  - p.25 «zero-mode instabilities are absent in the flag manifold construction, but a full KK analysis would of course be needed»
  - p.17 fn. 10 «a weakness of our derivation is the use of the probe approximation»
- Higher-genus caveats, quoted: the stable window is for the minimal-sugra, single-gauge-field variant only (the paper's κ = κ_Σ here):
  - p.22 «These now exist only for κ = −1, X ∈ (2−1/5 , 1)» (p.22 confirmed by Orion)
  - p.24 eq. (4.15) «Now there is no instability for X⁵ ≤ (5+√5)/8» and «they only make sense for κ = −1, g ≥ 2» [H1 control: paper sugra]. The maximal-sugra family «always» has an eigenvalue ≤ −4 (p.24).
- Ranking: field mode — no fix is needed for the surviving ALT-type candidates at tree level [Venus N2]; n2 is withdrawn [Venus B1]; the κ = 1 item stays as a free vortex-sector check [Venus N1]; flag and higher genus are parked.
- Geometry mode: no fix can be ranked until it is computed. The only cheap proxy is a [GR control] breathing-mode row of the flux-stabilised S² (e.g. the RSS radion (6D Einstein–Maxwell + Λ6, RSS 1983), Job Five, SpaceKitti/Grok@f982965:jobs/radion-onshell-filter/RESULTS.md:19,30 (RESULTS 345FB29A)) [GR control]; it is clearly not the lift's gravity.

## §5 Not computed (yet), queued, and out of scope
- NOT COMPUTED (YET): the geometry (shape) mode of our S² under the lift's gravity; any toy ε_post or n12 analogue; n2, κ2, U(1)_2 charges; μ off-critical with two sectors; ∫K with backreaction; the field mode on a conical tip; Λ4 in the toy.
- Queued for the next Part B pass (not edited now; no verdict moves) [Venus §A]: Part B 3037E19D lines 160 and 263 call the pure-gauge j = |q| level (j = 3, +3, 7 modes) "Higgs C". Suggested wording: «Higgs C (j = 3, +3, 7 modes) is the pure-gauge level eaten by the massive charged vectors; S6 is rejected on the j = 2 tachyon (−3, 5 modes) and on tr R⁴.» D1 Assignment C has the same issue. S6 stays rejected.
- Out of scope (not problem 1): M5 probes and nucleation; dark-bubble cosmology and the Λ4 hierarchy; flag-manifold physics; massive-IIA uplifts.
- Paper page (H15): the minimal-sugra κ_Σ = −1 sentence is on p.22 (confirmed by Orion).

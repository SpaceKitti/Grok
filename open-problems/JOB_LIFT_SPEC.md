# Job LIFT: from the flat toy to 3D/4D quantum gravity (spec, DRAFT for Venus)

Helios, 2026-10-02 about 22:30 BST. Asked for by Akitti via NanoRibbon (22:12, 22:14, 22:16). Venus checked it at 22:19, 22:25 and 22:25b; Orion checked the refs. Every edit from those checks is in here.

## Why the four problems come first [Akitti, via NanoRibbon]
- Akitti, 22:14, his exact words: "the whole issue is the r=0 basically and going from s^2->r^2 string to brane".
- 22:16: the lift to 3D/4D quantum gravity can't be built yet. All four open problems happen at the same step, the string → brane handoff at r = 0, where the flat plane (R²) meets the sphere (S²). **So the four problems block the lift.** Grok pointed this out to him.
- Remnant idea [Grok-suggested]: "quantum planck bounces at the r=0 (between s^2->r^2) might leave quantum gravity geometric remnants".
- **L1–L4 below are not the lift.** They are tests run at the blockers.

## The lift's gravity is unknown quantum gravity [Akitti, 22:41, via NanoRibbon]
- Akitti: the gravity in the lift is **quantum gravity, and it is unknown**. Einstein GR must never stand in for it. Earlier Grok kept doing that, and it is wrong.
- So **every GR or known-theory row in this spec is a labelled REFERENCE/CONTROL row**: L1 (Euclidean Einstein), L2 (Einstein–Maxwell), L3 (Einstein–Yang–Mills–Higgs), and Stelle and LQC in L4. None of them is the lift's gravity, and none of them, passing or failing, says what the lift's gravity is.
- **What the control rows are for:** (i) to calibrate the code against known answers; (ii) to give the classical-limit counts that any candidate quantum gravity has to reproduce, or explicitly depart from, at the bolt; (iii) to separate results that depend only on the flux and topology on the S² (Landau-level counts, the area-bound form, smoothness of the tip) from results that depend on which gravity theory is chosen.
- **Only gravity-independent results can unblock a problem for the lift.** A result that holds only in GR is a reference value, not an unblocking result. Where the table below says "unblocked by", it means the gravity-independent part of the result, with the GR row as its control [hive-interpretation].
- **L1 and L2 have no gravity-independent part.** They are harness calibration only. Blocker 04 is unblocked by the flux/Landau count and its onset form (L3, B4) [Venus 22:45].

**Theory-free lift requirements** (what any candidate quantum gravity must satisfy at the r = 0 S² → R² handoff; Venus 22:45)
1. **Smooth cap at r = 0.** The Euclidean time period is 2π/κ, so the tip of the R² has no cone [kinematic; holds in any metric theory].
2. **Flux is conserved through the handoff.** N = (1/2π)∫_{S²} F does not change from S² to R² [identity: the first Chern number].
3. **Mode count on the S².** For the g = 2 spin-1 field, 2n − 1 modes (complex), from index counting on the S² [identity]. For the scalar, n + 1.
4. **The crowding threshold, A against N_Φ, is the open test.** How the sphere's area A compares with the flux count N_Φ, and what the unknown quantum gravity does past that threshold, is the question the lift's gravity must answer. All four blockers sit at that threshold [open].


His saved words (all [Akitti account], all checked word for word against AKITTI_LINK_POST.md C796580D by `check_lift_quotes.py`):
- L47: "Yes. In the hive the \(\mathbb{R}^2\to S^2\) handoff *is* the deathface."
- L82: "The \(S^{2}\) bolt is then the wrapping cycle of a D2 / Euclidean instanton / charged 0-brane that the Lin–Shiu fragmentation already licenses."
- L3301: "GoldbergHexa-\(S^2\) / bolt is assembled from the edge, not by Wick-rotating through the wall."
- L1924: "The square-root vanishing is the geometric signature that the real Lorentzian solution has run out of room."

## The geometry, in plain words
- **Euclidean black hole = R² × S²** [standard: Gibbons–Hawking 1977]. The R² is a "cigar": imaginary time wrapped around the radial direction. The cigar's tip is the **bolt**, which is the horizon sphere, area 4πr_h². For the tip to be smooth, the time loop must have one fixed length. That length gives the Hawking temperature.
- **There are two different "r = 0"s. This is the key point.**
  - The origin of the Euclidean R² is the bolt, which sits at Schwarzschild radius r = r_h.
  - The Lorentzian r = 0 is the singularity inside the horizon.
  - The Euclidean section never reaches the Lorentzian r = 0. The gap between them is where the Wick picture stops [hive-interpretation; this fits L3301].
- A vortex wrapped on the bolt is a string turning into a 2-surface on S², as in L82 [standard object: Dowker–Gregory–Traschen 1992; the link to L82 is hive-interpretation]. Its discrete Z_N charge is standard "quantum hair", which is the closest standard thing to a remnant [standard: Coleman–Preskill–Wilczek 1992].
- Strings that pierce the horizon are our Bradlow toy living on the horizon [standard object: Achúcarro–Gregory–Kuijken 1995]. Whether the Bradlow cap carries over to a horizon is [hive-interpretation, to check].

## Blocker table [hive-interpretation for the whole mapping]
| Folder | What it blocks | What would unblock it | Tests that probe it |
|---|---|---|---|
| 04 Stelle / bounce | There is no finite, ghost-free treatment of the r = 0 bounce or of the Euclidean negative mode. So the lift's path integral isn't well defined. | The flux/Landau-level count on the S² and its onset form (L3, B4); requirements 3 and 4 above. L1 and L2 are harness calibration only, and the L-rows are GR/known-theory controls, not the answer | B4 / B4L, L1, L2 (L4 report-only) |
| 03 membranes | The wrapped string → brane has no finite quantum theory. | A finite count of the modes of the brane wrapped on the bolt [to write] | B3, L3 |
| 02 vacuum | The vacuum energy at the handoff isn't fixed, so the Euclidean action and the entropy can't predict anything. | A fixed vacuum term at the bolt, e.g. the Λ > 0 Nariai S²×S² case [standard object: Ginsparg–Perry 1983; to write] | B0, B2 |
| 01 SM | The families and zero modes on the bolt S² aren't derived, so nothing matches the Standard Model. | The zero-mode count on a bolt with flux n [to write] | B1, U1 |

## The L1–L3 count table: REFERENCE/CONTROL rows only (known theories, not the lift's gravity)
Each entry is (Euclidean negative modes, Lorentzian growing modes). Conformal-factor modes are counted separately (see L1). **Units of the count:** L1 and L2 count real gravity modes. L3 counts complex modes: 2n − 1 complex modes are 2(2n − 1) real growing directions. (The toy's n + 1 is also a complex count.)

| Row (all control rows) | Theory | Count | Source |
|---|---|---|---|
| L1 Schwarzschild | Euclidean Einstein (Einstein–Maxwell with Q = 0) | **(1, 0)** locked, real modes | GPY 1982 / Prestidge / Reall; Lorentzian stability [standard] |
| L2 RN with flux, past C_Q = 0 | Einstein–Maxwell, magnetic, canonical (fixed charge) | **(1, 0) → (0, 0)** at C_Q = 0, real modes | Monteiro–Santos 2009 |
| L3 RN in broken SU(2), small horizon | Lorentzian Einstein–Yang–Mills–Higgs (EYMH) | **(·, 0) → (·, 2n−1)** below the LNW onset, complex modes (= 2(2n−1) real) | LNW 1992, Ridgway–Weinberg 1995 |

**The table is not one continuous family.** L1 and L2 are pure Einstein–Maxwell. L3 is a different theory, with the SU(2) broken, so it has a massive charged W. Read the table as three separate checks at the same horizon, not as a single flow.

### L1, first runnable step: the Gross–Perry–Yaffe negative mode
- **What:** the one s-wave transverse-traceless negative mode of Euclidean Schwarzschild, solved as a radial ODE. Use Prestidge's master ODE (4.4) with the ansatz (4.1)–(4.3) and his boundary conditions (regular at the bolt, regular where rV′ − 2V = 0, normalisable), then shoot.
- **Target:** M²λ_neg ≈ −0.192 (Prestidge eq. 5.12, with G = 1; operator −∇² − 2Riem on TT modes). Reall eq. (1.7) gives λ = −0.19 M⁻². Both cite GPY; GPY itself was not read.
- **Count locked at (E, L) = (1, 0)** [Venus]. The GPY mode is thermodynamic: it is the negative specific heat. Lorentzian Schwarzschild is stable [standard].
- **Conformal factor:** count its modes separately, using the Gibbons–Perry rotation of the conformal factor [standard: Gibbons–Perry NPB 146 (1978) 90; the problem itself: GHP NPB 138 (1978) 141]. In words, the size mode has the wrong sign in Euclidean gravity, and it gets rotated by hand. Those modes are a Wick artefact, not physical.
- **Conformal column, what it holds:** (i) the wrong-sign trace (conformal) kinetic term, and whether it was rotated (yes/no); (ii) the lowest eigenvalue of the trace operator.
- **Optional Gregory–Laflamme cross-check (report-only) [checked in full text, Reall §1; verified by Orion]:** Reall gives λ = −μ*². With r₊ = 2 (M = 1), λ = −0.19 and μ* = 0.44. So μ*r₊ ≈ 0.88, and λr₊² ≈ −0.77 = −0.192 × 4. That is the black-string threshold. In words: the same number that makes the black hole thermally unstable sets where a black string starts to ripple.
- **Pass rule (fixed now; tolerance approved by Venus):** PASS if (a) the eigenvalue is M²λ = −0.192 within ±0.002, (b) exactly one negative TT s-wave mode is found, (c) the Lorentzian check finds no growing mode, and (d) conformal modes are reported in their own column. Otherwise FAIL (code or algebra). This is a reproduction.
- **Cost:** a 1D shooting ODE. Seconds to minutes.

### L2: magnetic RN (folder 04, with flux added)
- **What:** run the same count against Q/M and r_h for a magnetically charged RN hole in the canonical (fixed-charge) ensemble.
- **Target [checked in full text, Monteiro–Santos 0812.1767]:** the Euclidean count goes 1 → 0 exactly where the specific heat at fixed charge C_Q changes sign, at |Q|/M = √3/2, i.e. at r₊ = √3|Q|, M = 2|Q|/√3 (G = 1, Gaussian Q) [computed, Venus]. The Lorentzian count stays 0.
- **Normalisation caveat:** MS use Kol's Kaluza–Klein method. Their eigenvalue (eq. 63) is not the GPY number. MS say the "negative eigenvalue in [30] is quantitatively different from the one in [6]", but whether one exists "must be the same". **So compare the count and the zero crossing, not the Q = 0 value against L1.**
- **Pass rule:** the count goes 1 → 0 at C_Q = 0 within the scan step; the Lorentzian count is 0 throughout.

### L3: broken gauge theory on the horizon (the bridge to B4)
- **What LNW show [checked in full text, hep-th/9111045]:**
  - Eq. (22): the W's magnetic-moment term eF·(a×a) competes with its mass term ½e²v²a².
  - Eq. (23): the hole is stable if r_H > √n/(ev).
  - Eq. (24): there is a growing mode if r_H < c√n/(ev). Its shape is a_θ ∝ sinⁿ⁻¹θ, a_φ ∝ sinⁿθ.
  - For n > 1 the new fields are "localized about isolated points on the horizon". LNW guess these grow into lumps that "break off as unit monopoles".
  - **Plainly: LNW is a classical result in real (Lorentzian) time on a black hole. It is not the r = 0 bounce.**
- **Mode count; the count's source is Ridgway–Weinberg §3 [checked in full text, gr-qc/9503035 §3–4]:**
  - The W magnetic charge is Q_M = q/e. The unstable modes start at J_min = q − 1, and "there is but a single monopole vector spherical harmonic" for each J_z. So the lowest multiplet has 2q − 1 modes.
  - Each mode is a polynomial in the sphere coordinate z, with "exactly 2(q − 1) zeros" on S², which spread out "as evenly as possible".
  - For the SU(2) monopole of charge n, q = n, so the count is **2n − 1** [checked, Venus]. At n = 1 that is one spherical mode, as in LNW.
- **Landau-level reading [standard, Ambjørn–Olesen W condensate; refs unopened].** Let N_Φ be the number of flux quanta the condensing field sees (N_Φ = 2q). A charged scalar's lowest Landau level then has N_Φ + 1 states, which is the toy's n + 1. The g = 2 spin-1 lowest level has N_Φ − 1 states. The RW multiplet is exactly that spin-1 level [Orion; consistent with the RW polynomial form].
- **Same onset area, opposite sides [computed, Venus]:**
  - **Toy:** μ² = −e²v²/2 + eB with eB = 2πn/A. The symmetric saddle has tachyons for A > 4πn/(e²v²), the sparse big-bubble side. Below that area no vortex solution exists.
  - **LNW:** ω² = m_W² − eB with eB = 4πn/A and m_W = ev. So the horizon is **unstable for A below 4πn/(e²v²), opposite to the Bradlow toy.**
  - In words: in both, a magnetic energy competes with a mass. But in the toy the Higgs condenses when the field is weak, and in LNW the W condenses when the field is strong. **They mirror each other: unstable on opposite sides of the onset.**
  - **Flux convention, per flux quantum N_Φ [Venus 22:34]:**
    - Toy: N_Φ = n, onset eB = e²v²/2, so A = 4πN_Φ/(e²v²).
    - LNW: N_Φ = 2n, onset eB = m_W² = e²v², so A = 2πN_Φ/(e²v²).
    - So "same onset area 4πn/(e²v²)" holds only when each side uses its own n. Per flux quantum the two differ by a factor of 2. The mirror still stands.
  - In the toy, crowding just smooths things out. In LNW, crowding breaks the horizon into lumps that leave as monopoles. So LNW is the closer match to Akitti's "too many strings" [hive-interpretation].
- **The tie to B4:** this is B4's count with gravity added, tied to the number of strings on the sphere [hive-interpretation].
- **Prediction (fixed):** Lorentzian count = 2n − 1 complex modes (2(2n − 1) real) just below the LNW onset, and 0 above it. **Overtones (report-only):** deeper below onset, radial overtones could add modes. The count should then be a multiple of 2n − 1 [assumed; check against RW §3].
- **Report-only output, c:** measure LNW's onset constant c, where r_H,onset = c√n/(ev). The flat-space estimate gives c = 1, which is LNW's eq. (23) bound. The true onset depends on the horizon redshift: c lies in (0.32, 1]. c → 1 as M → M_crit, and c > 0.32 is a variational lower bound for M ≫ M_crit (LNW, checked in the text by Venus). Here LNW's M_crit is the extremal mass, where their T_H (eq. 26) vanishes; it is not L2's C_Q = 0 crossing. **c = 1 is a reference value only, not a prediction.** Whether c equals the Bradlow constant exactly, or only up to an order-one factor, is an L3 output. **The comparison must state its convention (per N_Φ and per mass²).** Otherwise "c = 1 matches" hides the factor of 2 above.
- **Also in L3:** Abelian-Higgs probe vortices on the bolt S² (Bradlow on the horizon, after AGK) and the DGT wrapping vortex. Both are report-only until Venus locks a rule.

### L4: report only
- An AOS-type bounce in the Lorentzian interior [standard object: Ashtekar–Olmedo–Singh 1806.00648]. Also Planck stars and white-hole remnants (Rovelli–Vidotto 2014; Bianchi et al. 2018).
- Any remnant [Grok-suggested].
- The two r = 0s compared side by side.
- The Stelle wall: non-Schwarzschild black holes in higher-derivative gravity (Lü–Perkins–Pope–Stelle 2015; Stelle 1977).
- No pass rule. Any match here would be [tuned] without stated dynamics.
- Stelle and LQC are named here as **reference candidates only**. Neither is assumed to be the lift's quantum gravity [Akitti 22:41].

## Earlier lift work (SpaceKitti/Grok jobs/)
Full review: `OLD_LIFT_REVIEW.md`. The old line lifted "Pair A", a 2×2 MHD matrix with an exceptional point at ε_EP ≈ 0.514, to a 4D chart. It stopped at "THEORY STACK: (none)" (qg-theory) and "Overall: NOT HAVE" (qg-radial). The reason: the gravity side never got dynamics of its own, and ε_EP is an MHD box number.
- **pairA-qg-handoff** (no sign-off): names the EP tips "r = 0 bolts", period 4π/ε_EP; the WRITE / NOT-SELECTED scores are hard-coded. Status: history only. **Superseded:** the new "r = 0" is a real bolt or singularity of a solved metric.
- **pairA-qg-lift-4d** (no sign-off): "bolt PASS" is circular (τ defined as 4π/ε_EP, then checked), and its own code prints "2π-polar FAIL". **Superseded** by the smoothness rule below.
- **pairA-qg-lift-ode** (no sign-off): its "regular" profiles fail the full Einstein + Λ equations, except r = 1 [computed, box]. That one is Euclidean Nariai S²×S² [standard]. **Kept only as** a Λ > 0 control idea for blocker 02.
- **pairA-jt-4d** (signed off 09-25): M1–M5 PASS. R1 = AdS₂×S² is a standard Einstein–Maxwell–Λ solution, with couplings chosen from ε_EP. It found that the smooth period is 2π/ε_EP and that 4π is a conical excess. **Reused:** its cone-angle / Gauss–Bonnet and G_ab-residual code as the bolt and geometry harness for L1/L2.
- **pairA-qg-on-R1** (signed off 09-25): D3 and D4 PASS, as a contour sum in complex ε with no measure or determinant. Not a gravity path integral, and it has no negative modes. **Not used;** L1 supplies what it lacked.
- **pairA-qg-theory** (signed off 09-25): L1–L6 all PARTIAL; r = ε_EP is circular. **Reused:** the reduced Einstein–Maxwell–Λ action with the boundary term as an on-shell-action check in L1/L2 (blocker 02). Note: qg-theory's on-shell −A/4 is the sign for compact spaces such as Euclidean dS/Nariai (no mass term). It is NOT the sign for asymptotically flat black holes, so the sign below supersedes it [Venus 22:40].
- **pairA-qg-radial** (signed off 09-26): NOT HAVE; no LPPS shooting solve done. **Reused:** the LPPS bifurcation m₂r_h ≈ 0.876, which is the same threshold as Reall's μ*r₊ ≈ 0.88 tied to the GPY mode. This is an exact identity, not a coincidence [identity, Venus 22:40]: Stelle's massive spin-2 mode on Schwarzschild obeys the same Lichnerowicz equation as the GPY mode, with m₂² playing the role of −λ. It feeds the L1 GL cross-check and the L4 Stelle item.
- **mhd-qg-cut-connection** (no sign-off): C1–C4 PASS, "Named type only. Not a theorem." Its Z₂ holonomy is at most a cartoon of discrete hair [hive-interpretation, weak]. **Not used.**

**What this changes in the stages:**
- **L1 and L2, bolt rule (new):** the Euclidean period is the smooth one, 2π/κ. A 4π (or any other) period is a conical defect and fails the bolt check. This was added because the old lift-4d graded a 4π cone as a bolt PASS.
- **L1/L2, report-only extra:** the on-shell Euclidean action (with the Gibbons–Hawking boundary term and flat-space subtraction) is printed against I = βM/2 = +A/4 = 4πM² for Schwarzschild (L1) [standard, Gibbons–Hawking 1977], and against I = βM − S for magnetic RN at fixed charge (L2) [standard]. The −A/4 and −S forms hold only for compact spaces with no mass term, such as dS [Venus 22:40].
- **L4, Stelle item:** the point where the non-Schwarzschild branch meets Schwarzschild, m₂r_h ≈ 0.876 (Lü–Perkins–Pope–Stelle, PRL 114 (2015) 171601, arXiv 1502.01028, eq. 9, with m₂ = 1; verified by Orion. LPPS is cited for the 0.876 only. It does not mention GL, GPY or negative modes, so the identity reasoning is Venus's), is set by L1's eigenvalue, as an exact identity (the same Lichnerowicz operator, m₂² = −λ) [identity, Venus 22:40; Reall §1 for the GPY–GL side]. L4 reports the numerical agreement as a check on code, not as evidence.
- Nothing else changes. L3 is untouched by the old work.

## Weak evidence, kept as weak
Above A_B, the vortex amplitude and the gap both scale as √(A − A_B). That fits L1924's "square-root vanishing". But 1/2 is the exponent of any pitchfork, so it is [hive-interpretation], weak. Also, the branch point is in the area A, not in the frequency.

## References (status)
- Gross–Perry–Yaffe, PRD 25 (1982) 330 [verified via INSPIRE; not read]
- Gibbons–Hawking–Perry, NPB 138 (1978) 141 [verified via INSPIRE; not read]
- Gibbons–Perry, "Quantizing Gravitational Instantons", NPB 146 (1978) 90 [verified via INSPIRE; not read]
- Gibbons–Hawking, PRD 15 (1977) 2752 [verified via INSPIRE; not read]
- Prestidge, PRD 61 (2000) 084002, hep-th/9907163 [checked in full text]
- Reall, PRD 64 (2001) 044005, hep-th/0104071 [checked in full text]
- Monteiro–Santos, PRD 79 (2009) 064006, arXiv 0812.1767 [checked in full text]
- Lee–Nair–Weinberg, PRL 68 (1992) 1100, hep-th/9111045 [checked in full text]
- Lee–Nair–Weinberg, PRD 45 (1992) 2751, hep-th/9112008 [checked in full text]
- Ridgway–Weinberg, PRD 52 (1995) 3440, gr-qc/9503035 [checked in full text]
- Dowker–Gregory–Traschen, PRD 45 (1992) 2762, hep-th/9112065 [verified via INSPIRE]
- Coleman–Preskill–Wilczek, NPB 378 (1992) 175, hep-th/9201059 [verified via INSPIRE]
- Achúcarro–Gregory–Kuijken, PRD 52 (1995) 5729, gr-qc/9505039 [verified via INSPIRE]
- Ginsparg–Perry, NPB 222 (1983) 245 [verified via INSPIRE; not read]
- Ashtekar–Olmedo–Singh, 1806.00648 [checked in full text; journal not verified]
- Rovelli–Vidotto, IJMPD 23 (2014) 1442026, 1401.6562; Bianchi et al., CQG 35 (2018) 225003, 1802.04264 [verified via INSPIRE]
- Lü–Perkins–Pope–Stelle, PRL 114 (2015) 171601, 1502.01028; Stelle, PRD 16 (1977) 953 [verified via INSPIRE]
- Ambjørn–Olesen (W condensate), candidates: PLB 214 (1988) 565; NPB 315 (1989) 606; IJMPA 5 (1990) 4525 [unopened]
- Allen, PRD 30 (1984) 1153 (cited by Prestidge) [not read]

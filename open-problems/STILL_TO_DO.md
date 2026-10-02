# Still to do on the four open problems

Kept by Helios. I update it every time a job lands, and Ledger pushes it with each job. A problem is marked "out of ideas" only once Venus, Aethon, Orion and Helios all agree.

**Common thread (from Akitti's link post, see `UNIFYING_THREAD.md`):** all four problems are read as a sphere carrying n units of flux ("strings"), where things break once n is too big for the sphere [assumed]. The link is firm for the SM on the physics side (n = number of families, by the index theorem), but that's Hive's mapping [assumed mapping]: Akitti's own SM posts use a warped throat instead. It's firm for membranes (fuzzy sphere, where the integer is the brane count N, not n), medium for vacuum selection, and weak for Stelle/LQC. Job U1 (fuzzy-sphere string count): done, maths PASS (Venus), physics PARTIAL (Helios). The n string zero modes are exact at every size [standard], but the "too many strings" collapse is a count, not a shift: the ladder stays exactly round with only N - n rungs, and the sector vanishes at n = N [computed]. The apparent level drift was just the radius convention [identity]. Reading: an N-state fuzzy sphere is the lowest Landau level of a charge N - 1 monopole, so strings use up the bubble's own flux budget [standard: Haldane 1983; tie is hive-interpretation]. Two more threads are now written up in `UNIFYING_THREAD.md`, negative modes (around Akitti's Aug 8 anchor article) and axions, each with a cheap test (Jobs N1 and A1 below).

Last updated: 2026-10-02, 20:30 BST.

Problems 1 and 2 don't have folders here yet. Their titles below are Helios's own grouping of Jobs One to Five, and Akitti can rename them.

---

## Problem 1: The Standard Model's particles from a curled-up sphere (generations, masses, mixing)

**Status:** open, ideas left.

**Tried so far**
- Job One (gap pass): PASS.
- Job Two (RSS sphere and the generation symmetry): PASS. The generation symmetry is a gauged flavour symmetry, not a 1/R effect. The Z' scale is put in by hand.
- Job Four (Yukawa couplings on a rugby ball): PASS as a toy. The rugby ball's squashing, set by the brane tension, controls how steep the mass ladder is.

**Walls hit**
- A brane that's a single point couples to nothing, so its width has to be put in by hand [boundary-condition choice].
- A single tilted brane makes the 1-2 and 2-3 quark mixings equal. In nature they aren't.
- Job 4b wall: a single narrow brane ties four quantities together (V_us, V_cb, V_ub, m_s/m_b) and comes out about 6 times low. Only a wide, smooth profile gets past it, which is no longer the narrow-brane picture.
- There's no CP-violating phase: J = 0.

**Still to do or try**
- Job 4b (sm-yukawa-4b-ckm): done. Maths PASS (Venus), physics PARTIAL (Helios). Fit 1 (4 knobs) misses V_cb at about half, and only reaches V_us by spending the factor-of-2 slack. Venus's knob-free wall number is about 1/5.3 against the predicted 1/6.2, so the single narrow brane does not beat its wall. Fit 2 (5 knobs) hits all 7 targets, but only with the aligned brane shrunk to a point and the tilted brane so wide (about 13 degrees, Helios's estimate) that it's really a smooth profile spread over the sphere [post-hoc]. The up-quark pair is a genuine knob-free hit. Fold-in (RESULTS 9E8D0411, cleared by Venus): the corrected check point passes (1-2 angle within 0.24%, 2-3 and 1-3 within 2-4%); at Fit 2 the two brane profiles barely overlap (0.0086) and the tilted brane is wide (width over spacing 0.63), so Fit 2 sits outside the narrow-brane approximation [post-hoc].
- Idea, not specced yet: find a source of CP violation, such as a complex brane profile, after 4b lands.
- **Next job (triggered, since 4b hit the rank-1 wall): Job 4c, Akitti's own warped-throat flavour picture** (from Akitti's SM posts, found by Orion; Helios specs it after U1; PDFs in `01_sm_from_sphere\`). Quarks live in a warped extra dimension, and each zero mode's value at the IR end goes like f(c) ~ e^((1/2 - c)kL) for c > 1/2. So hierarchies come from exponentials of O(1) numbers, the warped cousin of Job Four's power law. With O(1) random Yukawas the mixing goes like V_ij ~ f_Qi/f_Qj, which forces V_ub ~ V_us V_cb [standard: RS flavour anarchy, Agashe-Perez-Soni hep-ph/0408134]. That gives about 0.0094 against the measured 0.0038, within the O(1) spread (Venus's estimate), whereas 4b's single-brane relation predicts V_us about 6x low. Akitti's c-shifts from Brockett double-bracket flow stay in as [hive-interpretation]. Sources: Gherghetta-Pomarol hep-ph/0003129 (bulk-fermion profiles), Huber-Shafi hep-ph/0010195 (masses and mixings from O(1) c values). This idea comes from Akitti, not from Hive.

---

## Problem 2: Choosing the vacuum (why three generations, and why a small positive vacuum energy)

**Status:** open, ideas left.

**Tried so far**
- Job Three (Betti/Berry vacuum filter): PARTIAL. The machinery works, but the filter selects nothing.
- Job Five (radion settled at its minimum): PASS as a toy, PARTIAL on selection. Its exactly flat vacuum is the known RSS 1983 solution [standard].

**Walls hit**
- Job Three: the slow downhill roll stops at the first barrier by construction. The count of frozen vacua depends on the grid, and nothing suppresses the vacuum energy.
- Job Five: whether the three-generation match is a slowly expanding (dS) vacuum depends on the radius scale we chose. It's dS only for scales between roughly 0.74 and 0.957, and not at scale 1 [assumed input].

**Still to do or try**
- Why 5b matters [identity, Helios]: brane tension just relabels the flux (n becomes n/alpha), so it keeps the same blind spot and can't pick n even in principle. The Casimir term falls off at a different power of the radius, so it breaks the blind spot. Casimir is the only part of 5b that could select n.
- Job 5b (radion-5b-tension-casimir): done, fold-in RESULTS 6146CF25. In the one-universe scan only n = 3 survives (n = 1-10) anywhere in the Casimir window. Of the two barriers, the outer one (towards blowing up) is far lower, so it controls tunnelling. A natural Casimir size would need about 2000 light fields. Tension is PARTIAL (it can only relabel n, so it never reaches the band). Casimir is PARTIAL under the rule fixed beforehand: it makes three generations a dS survivor, and it is the first ingredient that actually tells n apart, but only with a Casimir strength about 2000 times its natural size [tuned]. The radius is the only thing allowed to move, and tunnelling through either barrier is not checked yet.
- Next ideas: (a) work out the Casimir sign and size for real field content from Kantowski-Milton, to see what number of fields makes it natural; (b) scan every n at one fixed vacuum energy and Casimir strength, which is the real "one universe" selection test; (c) add the second field that the SLED models carry (the dilaton).
- Superseded line from the 5b spec: lift the vacuum with brane tension (predicted to fail) or with the one-loop Casimir energy. The Casimir strength is taken as a constant and its log R piece is ignored [assumed input].
- Job 5c (vacuum-flux-share): done. PARTIAL for the flux share (the widest dS stretch is about 2.8%, under the 5% bar) and FAIL for the curvature-inclusive share (an identity: it can never reach a band). Wall [identity]: the filter only sees the flux strength in 6D units, a single number, so every n survives somewhere if the 6D vacuum energy is rescaled to match. Three generations come out alone only for hand-picked stretches of vacuum energy [post-hoc].
  - Known before it lands [identity]: the flux share depends only on n divided by its largest allowed value, and that largest value moves with the 6D vacuum energy. Any number of generations can be made the survivor by shifting the 6D vacuum energy, so 5c can at best say "three generations for this vacuum energy". The only thing that could single out three is if Job Three's bands differ from one n to another. 5c checks that.
- Next idea (not specced yet): fix the 6D vacuum energy from outside the model, for example from Job Two's KK gap or from the measured 4D vacuum energy.
- Next idea, Job A1 (not specced yet), "does an S2 axion see n?": add the axion that a 2-form on the sphere gives to the radion potential, and run 5b's Part K rescaling test on it. PASS if it breaks the rescaling blind spot with a natural-sized coefficient, PARTIAL if only when tuned, FAIL if blind [assumed input until derived]. Sympy plus one rerun.
- Next idea, Job N1 (not specced yet), "bubble vs radion": map the cavitation bubble's static potential (ambient pressure, surface tension, gas) term by term onto the radion's, and test whether the Blake threshold lands on the radion's no-minimum edge, with 5b's Casimir as the collapse side [prediction]. PASS if signs match and thresholds coincide, PARTIAL if only the powers match, FAIL if the powers don't match. Algebra only.

---

## Problem 3: Making sense of quantum membranes (open problem 3)

**Status:** open, ideas left.

**Tried so far**
- Job Six (membrane x^2 y^2 toy): PASS as a toy. Power counting shows strings are the only renormalisable case. Without supersymmetry the toy membrane is trapped, with separate energy levels (Simon). With supersymmetry it can slide out along the valleys for free, so its energies form a continuum starting at zero (dWLN).

**Walls hit**
- The toy has two variables, while the real model has nine directions. The real model has exactly one zero-energy bound state (Sethi-Stern, Yi), and the toy can't show it [standard: beyond toy].
- Growing the box can't detect a bound state at zero energy, or levels hidden inside the continuum.
- No renormalisable way to quantise membranes is known. Matrix theory reinterprets the problem rather than solving it.

**Still to do or try**
- Job 6b (membrane-6b-boundstate): done, maths PASS (Venus), physics PASS as a toy (Helios). No bound state: along the valley the zero-energy solution grows like x^(1/4), so it can't be normalised (needs decay faster than x^(-1/4)), exactly as in Froehlich-Graf-Hasler-Hoppe-Yau Appendix 2 (hep-th/9904182) [standard]. The box spectrum shows no level below the continuum ladder [computed]. Wall: the 2-variable toy is exhausted here; a bound state only appears in the 9-direction SU(2) model [standard: beyond toy].
- Next idea, Job 6c (not specced yet): redo 6b's valley balance for the SU(2) matrix model in d directions (d = 2, 3, 5, 9, the only cases with supersymmetry, from Yang-Mills in 3, 4, 6 and 10 dimensions) and derive the decay exponent kappa(d) against the normalisability bar. PASS if kappa(d) matches FGHHY's values. The asymptotics alone do not decide d = 5 (it passes the bar but has no bound state, which FGHHY rule out by symmetry), so the final yes or no is the Witten index, 0, 0, 0, 1 [standard: Moore-Nekrasov-Shatashvili hep-th/9803265, Kac-Smilga hep-th/9908096, Staudacher hep-th/0006234; Orion to verify]. Sympy only, no grids.

---

## Problem 4: Stelle's ghost and the loop-quantum-cosmology bounce (open problem 4)

**Status:** open, ideas left.

**Tried so far**
- Job Seven (pu-ghost-lqc-gw): PASS as a toy from Venus and Helios. Fold-in done (RESULTS E265D109), on main as 5331e11. Its no-ghost control shows the ghost's extra runaway depends on amplitude: at high amplitude it's larger for positive coupling, at low amplitude for negative. Aethon is adding the conditional-share line.
  - Part G: a toy with a ghost (Pais-Uhlenbeck) plus a small push between its modes has a stable "safe island" at small amplitude, where the ghost is benign, and runs away above it. This matches Smilga's benign-ghost picture.
  - Part L: a gravitational wave passing through the LQC bounce gets strongly kicked (order-one particle production) for wavelengths about the bounce size or longer. Short waves pass through almost untouched, with the effect falling off exponentially. That falloff is the standard smooth-background result (Dykhne-Davis-Pechukas).

**Walls hit**
- The ghost toy has only two modes. Stelle's ghost is a field with infinitely many modes that can trade energy with gravitons, so a safe island in the toy doesn't show that the real theory is stable, and says nothing about quantum unitarity [standard: beyond toy].
- Part L uses one specific way of carrying waves through the bounce (dressed-metric / hybrid style). Other LQC approaches, such as the "deformed algebra" one, change the wave equation near the bounce, and the answer could change with them.
- The bounce here is the effective, homogeneous one. Waves don't feed back on the background.

**Still to do or try**
- Idea (not specced yet): rerun Part L with the deformed-algebra wave speed, where the speed squared is 1 - 2 rho/rho_c, so it turns negative near the bounce. Cheap, because it's one function change. Near the bounce the wave equation turns into a growth equation, so expect short waves to be amplified, not suppressed (as Venus points out). Pass test: match the sign and slope of the short-wave behaviour in Linsefors-Cailleteau-Barrau-Grain (arXiv 1212.2852), using the tensor equation from Cailleteau-Barrau-Grain-Vidotto (arXiv 1206.6736).
- Idea (not specced yet): chain several ghost toys together, as a small step towards a field, and see whether the safe island shrinks as more modes are added. For contrast: Deffayet-Mukohyama-Vikman (arXiv 2108.06294) have a ghost model that is stable for every starting condition.
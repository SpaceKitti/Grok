# Still to do on the four open problems

Kept by Helios. I update it every time a job lands, and Ledger pushes it with each job. A problem is marked "out of ideas" only once Venus, Aethon, Orion and Helios all agree.

**Common thread (from Akitti's link post, see `UNIFYING_THREAD.md`):** all four problems are read as a sphere carrying n units of flux ("strings"), where things break once n is too big for the sphere [assumed]. The link is firm for the SM on the physics side (n = number of families, by the index theorem), but that's Hive's mapping [assumed mapping]: Akitti's own SM posts use a warped throat instead. It's firm for membranes (fuzzy sphere, where the integer is the brane count N, not n), medium for vacuum selection, and weak for Stelle/LQC. Cheap test: Job U1, the fuzzy-sphere string count (not run yet).

Last updated: 2026-10-02, 19:56 BST.

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
- There's no CP-violating phase: J = 0.

**Still to do or try**
- Job 4b (spec sent): use different brane widths for up and down quarks plus one lopsided brane, and fit 7 measured targets with 4 knobs.
- Idea, not specced yet: find a source of CP violation, such as a complex brane profile, after 4b lands.
- **Next idea if 4b hits the rank-1 wall: Akitti's own warped-throat flavour picture** (from Akitti's SM posts, found by Orion; not specced yet). Quarks live in a warped extra dimension, and each zero mode's value at the IR end goes like f(c) ~ e^((1/2 - c)kL) for c > 1/2. So hierarchies come from exponentials of O(1) numbers, the warped cousin of Job Four's power law. With O(1) random Yukawas the mixing goes like V_ij ~ f_Qi/f_Qj, which forces V_ub ~ V_us V_cb [standard: RS flavour anarchy, Agashe-Perez-Soni hep-ph/0408134]. That gives about 0.0094 against the measured 0.0038, within the O(1) spread (Venus's estimate), whereas 4b's single-brane relation predicts V_us about 6x low. Akitti's c-shifts from Brockett double-bracket flow stay in as [hive-interpretation]. Sources: Gherghetta-Pomarol hep-ph/0003129 (bulk-fermion profiles), Huber-Shafi hep-ph/0010195 (masses and mixings from O(1) c values). This idea comes from Akitti, not from Hive.

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
- Job 5b (radion-5b-tension-casimir): done. Tension is PARTIAL (it can only relabel n, so it never reaches the band). Casimir is PARTIAL under the rule fixed beforehand: it makes three generations a dS survivor, and it is the first ingredient that actually tells n apart, but only with a Casimir strength about 2000 times its natural size [tuned]. The radius is the only thing allowed to move, and tunnelling through either barrier is not checked yet.
- Next ideas: (a) work out the Casimir sign and size for real field content from Kantowski-Milton, to see what number of fields makes it natural; (b) scan every n at one fixed vacuum energy and Casimir strength, which is the real "one universe" selection test; (c) add the second field that the SLED models carry (the dilaton).
- Superseded line from the 5b spec: lift the vacuum with brane tension (predicted to fail) or with the one-loop Casimir energy. The Casimir strength is taken as a constant and its log R piece is ignored [assumed input].
- Job 5c (vacuum-flux-share): done. PARTIAL for the flux share (the widest dS stretch is about 2.8%, under the 5% bar) and FAIL for the curvature-inclusive share (an identity: it can never reach a band). Wall [identity]: the filter only sees the flux strength in 6D units, a single number, so every n survives somewhere if the 6D vacuum energy is rescaled to match. Three generations come out alone only for hand-picked stretches of vacuum energy [post-hoc].
  - Known before it lands [identity]: the flux share depends only on n divided by its largest allowed value, and that largest value moves with the 6D vacuum energy. Any number of generations can be made the survivor by shifting the 6D vacuum energy, so 5c can at best say "three generations for this vacuum energy". The only thing that could single out three is if Job Three's bands differ from one n to another. 5c checks that.
- Next idea (not specced yet): fix the 6D vacuum energy from outside the model, for example from Job Two's KK gap or from the measured 4D vacuum energy.

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
- Job 6b (new, idea from Venus, Aethon and Orion): test directly whether the toy has a zero-energy bound state, by solving Q psi = 0 along the valley and comparing with Froehlich-Graf-Hasler-Hoppe-Yau (hep-th/9904182).

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
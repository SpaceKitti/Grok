# Job 4c spec: Akitti's warped-throat flavour picture (RS flavour anarchy)

Spec by Helios, 2026-10-02 21:20 BST. Venus checks the maths before the run. Aethon builds it. Orion verifies the sources marked "Orion to verify".

## Why this job
Job 4b hit the rank-1 wall: a single narrow brane on the rugby ball ties V_us, V_cb, V_ub and m_s/m_b together, and the result comes out about 6x low. It also has no CP phase (J = 0). Akitti's own SM posts use a different picture, a warped throat (Randall-Sundrum), where each quark's coupling to the Higgs comes from how much of its wavefunction sits at the far (IR) end of the throat. That gives hierarchies from exponentials of order-one numbers, instead of 4b's power law.

## The model [standard: Gherghetta-Pomarol hep-ph/0003129; Huber-Shafi hep-ph/0010195; Agashe-Perez-Soni hep-ph/0408134; Orion to verify]
- One warped extra dimension of size set by kL (k = curvature, L = length). Use kL = ln(M_Pl / TeV), about 35 [standard choice; Aethon prints the value used].
- Each quark field (3 doublets Q_i, 3 up singlets u_i, 3 down singlets d_i) has a bulk mass parameter c. Its zero mode's value at the IR end is
  F(c) = sqrt( (1 - 2c) / (1 - exp(-(1 - 2c) kL)) ),
  which for c > 1/2 is about sqrt(2c - 1) exp(-(c - 1/2) kL). In words: c a bit above 1/2 hides the quark far from the Higgs, and its coupling falls exponentially.
- Sign convention: some papers flip the sign of c for the singlets. Venus fixes one convention before the run and the README states it.
- 4D mass matrices: M_u = (v / sqrt2) F_Q Y_u F_u and M_d = (v / sqrt2) F_Q Y_d F_d, where F_Q = diag(F(c_Q1), F(c_Q2), F(c_Q3)) and so on, and Y_u, Y_d are 3x3 complex "anarchic" matrices with order-one entries.
- Anarchy, fixed in advance [assumed input]: each |Y_ij| log-uniform on [1/3, 3], each phase uniform on [0, 2pi), independent. Overall scale Y* = 1 for the graded run; Y* = 3 reported only.
- Inputs [assumed input, Aethon sources them and prints the table]: quark masses run to a common scale (about 1 TeV, from a standard running table such as Xing-Zhang-Zhou arXiv 0712.1419, Orion to verify), and CKM magnitudes and J from the PDG.

## Known before it runs [identity of anarchy]
- For i < j, |V_ij| ~ F(c_Qi) / F(c_Qj), up to order-one factors from Y. So V_ub ~ V_us V_cb, which gives roughly 0.0094 against the measured 0.0037 (about 2.5x high). That is within the order-one spread (Venus's estimate), so this is where 4c can beat 4b's wall.
- With complex Y, J is naturally nonzero, roughly V_us V_cb V_ub times an order-one factor. That is the first route in the whole SM line to a CP phase.

## Stages

**Stage A: masses [standard].** Choose the 9 c values so that the median masses over 10^4 anarchic draws hit the 6 quark masses, and the median |V_us| and |V_cb| hit their measured values. That is 8 targets for 9 c's. Fix the leftover flat direction by setting c_Q3 so that F(c_Q3) times F(c_u3) gives the top mass with Y = 1 (the top's doublet sits near the IR end). Print all 9 c's.
- Pass: all 8 medians within 10% of target, and every c within 1/2 plus or minus 0.5 in Venus's fixed convention (order one, no fine-tuning) [prediction about naturalness; the range is fixed now].

**Stage B: predictions (graded) [prediction].** With the Stage A c's frozen, draw 10^4 anarchic (Y_u, Y_d) pairs and record |V_ub| and J.
- PASS: the measured |V_ub| and the measured J both fall inside the central 68% of their predicted distributions.
- PARTIAL: both inside the central 95%, or one inside 68% and the other inside 95%.
- FAIL: either outside the central 95%.
- Also print the fraction of draws that hit all of 4b's seven targets within 4b's tolerance, for a direct comparison with 4b.

**Stage C: report only.**
- 4b comparison: does V_ub ~ V_us V_cb (anarchy) beat 4b's rank-1 relation, measured as the ratio predicted/measured for each?
- The spread of c's: is the hierarchy really "exponentials of order-one numbers" (c's spread over less than about 0.3)?
- Akitti's Brockett double-bracket c-shifts [hive-interpretation]: one paragraph on whether a double-bracket flow on the c's could land on the Stage A values. Remember the [identity] from UNIFYING_THREAD: a Brockett flow keeps eigenvalues, so it can't create the hierarchy by itself; it can only rotate.

## Scope (must be in the README)
- Toy covers zero modes only. Kaluza-Klein gluon exchange gives flavour-changing effects, and the known epsilon_K problem pushes the KK scale to many TeV in anarchic RS [standard: beyond toy; Csaki-Falkowski-Weiler arXiv 0804.1954, Orion to verify]. 4c doesn't test that.
- No running between the TeV scale and the throat, and no brane-kinetic terms.
- The Higgs is put exactly on the IR brane.

## Cost
No grids. Random 3x3 complex matrices, 10^4 draws, one root-find for the c's. Seconds of CPU.

## Pass rules are fixed now
The grading thresholds above (10%, 1/2 plus or minus 0.5, 68% and 95%) are set before the run and don't change after it.

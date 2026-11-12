# Probe A v3: ring vs projector towards criticality (new solves, no new physics)
Idea: Akitti's (via NanoRibbon, 2026-11-05 17:05 UK). Spec: Helios, 2026-11-05 17:15 UK.
Replaces v2 (915cde8d). Keeps Venus's four fixes and adds the new-solve sweep NanoRibbon asked for at 17:09.

**Model.** Unchanged: FUZZY_CONE_SPEC_V2_1 9dbd2f86 + ADDENDUM_B 4e265cbd, solved with fuzzy_cone_v2_1.py as frozen. n = 2 at each pole.

**Criticality.** The Bradlow ratio is b = R²/(2n), which matches the saved rows: 4.5 for n = 1 and 2.25 for n = 2 at R = 3. Solutions exist only for b > 1. Since R² = θN, the tip parameter and b are linked.

**Sweep, 12 solves.**
- b ∈ {2.0, 1.5, 1.2, 1.05}, setting R² = 4b.
- N ∈ {41, 61, 81}, so θ = R²/N.
- At fixed b, N alone sets the fuzz level.
- At about 10 s per N = 81 solve, the whole sweep takes a few minutes.

**Per solve.**
- Converged flag.
- rank_N, rank_S, Q_cap_N, Q_cap_S, Q_total.
- r_peak at both poles from a 3-point parabola fit to the energy-ring maximum, in units of R (r_peak/R) and also raw.
- Fit floor f = |3-point vertex − 5-point quartic vertex|.

**Verdict, frozen before any numbers are read.**
- **BROKEN:** rank ≠ 2 at either pole, or |Q_total − 4| > 1e-2, in any converged solve.
- **YES:** not BROKEN, and at every b the change in r_peak/R across N is greater than 3 × max f, with the same sign at both poles.
- **NO-MOVE:** not BROKEN, and the change is ≤ max f at every b.
- **UNDECIDED:** anything else, any solve that didn't converge, or a vertex outside its fit points.
- **Criticality trend, output only:** whether the size of the shift grows as b → 1.

**Note.** Changing N at fixed R is the tip change itself. So the earlier "grid error" between different N is the effect being tested, not noise. The noise floor is the fit floor f.

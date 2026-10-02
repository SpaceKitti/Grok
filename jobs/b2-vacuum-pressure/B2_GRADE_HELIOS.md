# B2 (vacuum pressure at the Bradlow cap, folder 02): physics grade, Helios

2026-10-02, about 23:05 BST.
- **Graded:** `C:\Users\Akitt\open-problems\Bradlow_cap\02_vacuum\` (the folder is `02_vacuum`, not `B2_*`). I read it on TrinityOrb without writing anything and copied it to `/workspace/b2grade/02_vacuum/`. Hashes confirmed: README 4C355920, RESULTS 1EAF64BD, run.py 27105171. There are no other output files; every number is printed in RESULTS.md.
- **Against:** spec `JOB_B2_VACUUM_PRESSURE_SPEC.md` 3A069F08 (in `Bradlow_cap\` on TrinityOrb; same bytes as `/workspace/bradlow/`). B0 inputs: B0 RESULTS AE4E8FFB, and my B0 grade `B0_GRADE_HELIOS.md` E58EFC2F.
- Aethon (build): PASS. Venus (maths): PASS (Hive 22:52). Orion checked the source of the z/(4N) term (MW p. 8).

## Verdict: physics PASS (reproduction + scale ordering), with caveats [computed]
- The grade comes from the rule fixed before the run, and it is PASS by construction, as the spec said it would be.
- Stage A reproduces the known results. A1: every sympy residual is exactly 0. A2: c = (N+1)/6N for N = 1, 2, 3, and the trend tends to MW's 1/6. A3: the exact sum agrees with MW eq. (36) at N = 10⁵.
- B0 P1 passed.
- **The caveats do not change the grade.** They change how firmly one row of the scale ordering can be read (N = 3 at low T, below), and they add wording fixes to the README.
- **Re-run:** I ran the graded run.py on the box (scratch copy under `/workspace/b2grade/rerun/`, same spec and B0 RESULTS bytes). It took 6 s. RESULTS matches the graded file line for line, apart from the timestamp, Python version, audit count and runtime lines [computed].

## Physics checks
1. **The measured gap table is used** [computed]. All 18 gap² values in B2's Stage B match the table in B0_GRADE_HELIOS.md to within rounding (largest relative difference 4e-6; my check, `/workspace/b2grade/checks/`). They are read from B0's RESULTS, not recomputed. The leading formula appears only in columns labelled "leading order, reference".
2. **The normalisation matches B0** [identity]. L = ½|Dφ|² + ¼F² + (e²/8)(|φ|² − v²)² at e = v = 1, with A_B = 4πN.
   - I re-derived ΔE = (A − A_B)²/(8A) by hand: it is the uniform-field (φ = 0) energy minus the BPS energy πNv².
   - MW's moduli metric uses (A − 4πN), the same cap.
   - The CP^N degeneracies coded in run.py are the standard SU(N+1) ones (2k+1 at N = 1, and N(N+2) at k = 1). The levels give exactly MW's exponent z·k(1 + k/N).
3. **c = (N+1)/6N, not 1/12** [computed; identity]. The heat-kernel line uses the scaled Fubini–Study curvature 4N(N+1)/(A − 4πN) and gives (N+1)/6N. The exact spectrum sum then recovers it to about 1e-10. M22's 1/12 is printed only as "misprinted, for reference".
4. **The validity columns are computed and the ordering of scales makes sense** [computed].
   - *Hot (T = 1):* classical melting comes first for every N and ħ. The exact melting points are ε* = 1.18, 0.75 and 0.58 for N = 1, 2, 3. Physically, the thermal energy outgrows the energy that keeps the strings condensed (ΔE) before any quantum scale matters. This needs no gap, so it doesn't depend on the gap assumption.
   - *Cold (T = 0.01):* a quantum scale comes first. For N = 1 and 2 it is the amplitude gap (ħ·m_gap/ΔE); for N = 3 the run reports the moduli step. Physically, zero-point energy outruns ΔE before thermal energy does. That is the right order for a cold system.
   - *T = 0.1:* the order depends on ħ, as it should. That temperature sits between the two regimes.
5. **ε*(T) follows √(8TA)-type scaling** [computed; identity]. At low T the exact melting point and the leading √(8TA_B) estimate agree to a few per cent. At T = 1 the leading estimate is off by up to about half, as expected: the exact root A − A_B = 4T + √(16T² + 8TA_B) carries a 4T term that only matters when T is not small. P(ε*) = N√(T/8A*) is exact at the exact root [identity].
6. **Nothing is tuned.** Every threshold is in the parameter block and matches the spec. The one post-hoc item is the A3 allowance (next section).

## The large-N allowance
- **What it is:** the A3 tolerance includes the term z/(4N). That is the finite-N correction in MW eq. (34), P̃ = z e^(−z/2) − z/(4N). I read it in MW's text on the box too (2212.06016, p. 8).
- **History:** Aethon added it after a scratch run in which the z = 16 test point missed by about 4e-5. He disclosed this.
- **Does it change a verdict?**
  - Inside A3, yes. Without it, A3 fails at z = 16, the run's own Stage A would read FAIL, and so would the coded grade.
  - Against the spec, no. The spec asks only to "check the large-N trend toward MW (36)" and sets no number for it. The actual reproduction test is A2's c = (N+1)/6N slope, which passes by a huge margin.
  - So the allowance never decided the physics.
- **Not tuning.** Venus showed that the z = 16 miss is exactly −z/(4N) by checking how it changes with N. My own quick look before the 22:52 update agrees (residual × N ≈ −4 = −z/4 at z = 16, for N from 2.5e4 to 4e5). I am not re-deriving it.
- **Keep it, tagged.** Use Venus's tag: "[post-hoc] added after the z = 16 scratch miss; independently confirmed by N-scaling (Venus) [computed]".
- **Side note:** the other allowance term, (3+z)/N·|leading|, is [assumed] and never decides a test point. Every point passes without it [computed].

## Physical fairness of the two [assumed] choices
**(a) The coincident-configuration gap.**
- B0 measured the gap only with all N strings stacked at one pole. The gas mostly samples spread-out arrangements.
- Near the cap this hardly matters, because every arrangement has the same leading law, gap² ≈ (A − A_B)/A [computed, B0].
- It matters slowly further out. B0's split-pole runs sit closer to the leading law than the stacked ones. So the gap of a typical arrangement is probably between the stacked value and the leading formula [assumed].
- **Effect on ε*:** I swapped the measured stacked gap for the leading-law gap. The quantum-gap ε* moves by at most about 15% (N = 3, ħ = 1) [computed].
- **One ordering is fragile: N = 3 at low T.**
  - The ratio of the quantum-gap column to the moduli-step column is 4A·m_gap² / ((N+1)(A − A_B)). With the leading-law gap this is 4/(N+1), whatever T and ħ are [identity, leading order].
  - So for N = 1 and 2 the quantum gap always breaks first, and that result is robust.
  - For N = 3 the two scales tie exactly at leading order. The report "moduli step first" comes entirely from the stacked gap being a little lower than the leading law.
  - Read N = 3, low T, as **"quantum gap and moduli step break together, within the arrangement uncertainty"**, not as a clear winner.
  - For N ≥ 4 the leading law would put the moduli step first [prediction, untested].

**(b) The log-log interpolation.**
- Near the cap each column is close to a power of ε: T/ΔE goes like ε⁻², and the other two like ε^(−3/2). So straight-line interpolation on log-log axes is the natural choice.
- I checked it against exact crossings: the true root for the classical column, and a root-find on the leading-gap quantum and step columns. Interpolation lands within about 7% and errs a little high. The worst case is the wide 0.1-to-1 bracket.
- This changes no "breaks first" verdict [computed]. It is fair as an estimate. The coarse ladder, not the method, limits the precision.

**(c) The "crosses 1" threshold.** The point where a column reaches 1 is an order-of-magnitude marker. It compares energies, not free energies, so the entropy of the competing smooth phase is ignored [assumed]. ε* is a scale, not a sharp transition point.

## What it shows, in plain words
- **The famous infinity is never reached inside the region where the gas picture is valid.** Squeeze N strings onto a sphere near the smallest allowed area, and the simple gas formula says the pressure goes to infinity, like hard discs that run out of room [standard]. B2 checks where the gas picture itself stops working. It stops before the infinity, at a finite pressure [computed].
  - *Hot:* the strings melt into a smooth layer first. At the melting point the pressure is N√(T/8A*). It grows like the square root of temperature, and it is finite.
  - *Cold:* quantum effects freeze the gas into its ground state first, and the pressure in the gas model drops toward zero instead of blowing up (Manton–Wang's own result).
  - Both ways, the formula's infinity sits beyond the edge of its own validity.
- **What this means for "too many strings"** [hive-interpretation]. Akitti's line was: "once too many strings form … mathematical divergences (infinities) … happen". In this toy, crowding strings toward the limit doesn't produce a real infinity. It produces a change of description: the strings stop being separate strings. They dissolve into a smooth layer, or they freeze. The divergence marks the point where the string description breaks, not a physical infinity. That fits Akitti's vacuum-post wording ("critical occupancy", L1155) better than an infinity. It is a reading, not a result, and B2 is not evidence for Akitti's link.

## What it does NOT show
- **What happens after the breakdown.** B2 finds where the gas picture ends. It doesn't compute the pressure of the melted or frozen phase. That needs the full field theory at finite temperature, with the amplitude mode included.
- **A true phase transition.** ε* is an energy-scale crossing, not a computed transition, and it has no order or latent heat (see (c)).
- **General arrangements.** The gap columns use only the stacked configuration (see (a)).
- **Far from the cap.** P_MW uses the dissolving-limit metric, so at ε = 1 and 4 it is an extrapolation (README says so).
- **Anything about gravity, the bubble, or B1, B3 and B4.**

## Fixes for the README (tag and wording only; no rerun needed)
1. **Venus's L19 note is not yet in the README.** The README only says the L19 fix "is deferred". RESULTS A1 prints the ratio R·Vol / M22 (15) = 2 + 2/N "→ 2 as N → ∞". I checked M22's text on the box (2204.01389, eqs. (14)–(15)):
   - Eq. (14) at g = 0 gives 2N(N+1)π^N(A − 4πN)^(N−1)/N!, so the factor-of-2 relation to the scaled Fubini–Study value is **exact for every N on the sphere**.
   - Eq. (15) is M22's thermodynamic-limit simplification (N + 1 → N). Comparing against (15) is what produces 2 + 2/N.
   - Suggested README line: "The factor of 2 between M22's total curvature and the scaled-FS value is exact for every N on the sphere (M22 eq. (14), g = 0). The 2 + 2/N in RESULTS A1 comes from comparing with M22's large-N form (15), which run.py labels 'eq. (15) at g = 0'. [identity; tag-only fix]".
2. **A3 allowance tag:** replace "[post-hoc, during development]" with Venus's tag (above).
3. **N = 3, low T:** add "At leading order the quantum-gap and moduli-step columns tie exactly for N = 3 (ratio 4/(N+1)). 'Moduli step first' depends on the stacked-configuration gap [assumed]."
4. **Interpolated ε*:** add "log-log interpolation is within about 7% of exact crossings and errs high in the 0.1–1 bracket [computed, Helios check]".
5. **Validity threshold:** add "crossing 1 is an order-of-magnitude marker (energies, not free energies) [assumed]".
6. **Minor:** the Tags line lists [tuned] among the tags used and then says "Nothing is [tuned]". Drop [tuned] from the list.

## Sign-off line for the README
Helios (physics): PASS (reproduction + scale ordering), 2026-10-02 about 23:05 BST. I re-ran run.py on the box and got identical RESULTS. The measured B0 gaps, c = (N+1)/6N and B0's normalisation are all used correctly. The z/(4N) allowance is MW eq. (34)'s finite-N term [post-hoc, confirmed]. The N = 3 low-T ordering is a leading-order tie, decided by the stacked-gap assumption. The gas breaks down at finite pressure before the blow-up. The README and RESULTS were not edited by me.

## Helios check files (box)
`/workspace/b2grade/rerun/` (re-run), `/workspace/b2grade/checks/a3_allowance.py` and `.out`, `/workspace/b2grade/checks/gap_interp_sensitivity.py` and `.out`.

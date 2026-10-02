# pairA-qg-radial

Question: does any standard gravity family give a radial equation whose root lands on Pair A's tip, with no Pair A input and no tuned scale? r = eps_EP is a match test, not an input. No folders are loaded. No git. No claim that Pair A is a quantum-gravity result, has a JT dual, or is an Einstein solution. Gravity-side is hive language [hive-interpretation].

## Pipeline and firewall (fixed before any computation)

1. `inputs.py`: every constant carries a fixing rule, one of 'Planck units', 'extremality', 'standard value from <named source>', or 'free'. Each 'free' counts as a free scale.
   - Forbidden-input scan: each input value v (and |v|, 1/|v|, v², √|v|, 2|v|, |v|/2) is compared, at relative tolerance 1e-6, against the Pair A numbers (a, b, |v|, |λ_EP|, the derived tip (b−a)/(2|v|), the derived Nariai r_N² and R₂) and their simple combinations (pairwise sums, differences, products and ratios; halves, doubles, squares, square roots and reciprocals).
   - The tip enters `inputs.py` only as the combination (b − a)/(2|v|), never as the target literal.
   - Any hit stops the run.
2. `families.py`: the equations, as sympy expressions and printed strings.
3. `roots.py`: ALL roots (real and complex), each marked physical or unphysical, with no knowledge of the target. Neutral conventions for free scales: each is set to 1 in its own units (Planck units G = c = ħ = 4πε₀ = 1), except the Liouville V amplitude, set to −1 so that a real horizon exists.
4. The raw roots are written to RESULTS.md first (section 'Raw roots'), before any matching.
5. `match.py` (the ONLY file containing the target 0.51368066) runs after roots.py. It reports:
   - the relative error of the closest physical root;
   - whether the zeros form a ± pair or exist only for r > 0;
   - what value of a free scale WOULD hit the target, as information only [PARTIAL, by construction]. Nothing is tuned.
6. Extra roots are always logged and discussed; they never lower a grade.

## Grade rules (pre-fixed)

Per family (or per model inside a family):
- **HAVE:** no forbidden inputs, zero free scales tuned, a physical root within 1e-6 relative of the target, and the ± pair present or derived.
- **PARTIAL [by construction]:** exactly one free scale tuned to hit the target (reported as hypothetical here, not actually tuned), or a match that needs a declared choice. As run with the neutral convention it misses; the hypothetical value is shown.
- **PARTIAL (no match):** clean (no forbidden input and no free scale available), but misses by more than 1e-6.
- **MISSING:** needs a forbidden input to close (for example the location of the zero is an integration constant that only F_JT or eps_EP could fix), or has no finite physical root.
- Overall: **RADIAL EQUATION FROM GRAVITY: HAVE only if some family is HAVE with no tuned scale.**

## Families

1. Einstein–Maxwell–Λ: f(r) = 1 − 2M/r + Q²/r² − Λr²/3. Horizons, the extremal (cold) condition and the Nariai condition.
2. Stelle / quadratic gravity: the non-Schwarzschild branch (Lü–Perkins–Pope–Stelle 2015). A full numerical shooting solve is not done. The characteristic radii used are the Yukawa radius 1/m₂ and the bifurcation radius m₂r_h ≈ 0.876, plus the zeros of Stelle's linearised metric. This is stated clearly as a limitation.
3. 2D dilaton gravity, Killing norm ξ = 0 from the standard general solution: CGHS, spherically reduced 4D Einstein (SRG), and Liouville (U = const, V ∝ exponential).
4. R1-like product chart AdS₂ × S² in Einstein–Maxwell–Λ, with ε as the radial coordinate of the 2D factor. Field equations solved along ε for r(ε).

Tags: [standard], [computed], [identity], [by construction], [hive-interpretation].

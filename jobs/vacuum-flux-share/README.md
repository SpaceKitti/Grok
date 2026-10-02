# Job 5c: vacuum flux share filter

New standalone folder, approved through NanoRibbon (Akitti's go) and specced by Helios. It is algebra on top of Job Five; there are no heavy runs and no new percolation.
`RESULTS.md` is written **only** by `run.py`. No git is used. Every number in `RESULTS.md` is printed from a variable in `run.py`; this README deliberately quotes no computed numbers.

Read-only inputs (hash-audited before and after the run in `RESULTS.md`):
- Job Five: `C:\Users\Akitt\radion-onshell-filter\` (`run.py`, `RESULTS.md`, `README.md`)
- Job Three: `C:\Users\Akitt\betti-berry-vacuum-filter\` (its `RESULTS.md` band table and `run.py` source), including Orion's X files (`X_POSTS_verbatim.md`, `X_NOTES.md`, `X_WINDOW_DEFS.md`), which are never modified.

## What changed from Job Five

Job Five reduced 6D Einstein-Maxwell on a round S^2 to the breathing-mode potential
`V(x) = a Lambda_6/x - b/x^2 + c n^2/x^3`, with `x = R^2`, `a = 4 pi`, `b = 4 pi M_6^4` and `c = pi/(2 g_6^2)` [assumed input: Job Five's reduction convention].
It then fed Job Three's filter with `p = n/(3R^2)` times a radius scale `s` [assumed input], so the n = 3 dS hit depended on `s`.

Job 5c removes `s`. It uses Venus's dimensionless on-shell quantity, the flux share of the vacuum energy:

    p_flux = (B^2/2) / (B^2/2 + Lambda_6),   B = n / (2 g_6 R^2)

`B` is Job Five's convention: Job Five sets `F_thetaphi = n sin(theta)/2`, so the orthonormal field is `n/(2R^2)`. With the `1/(4 g_6^2)` normalisation, the flux energy density is `B^2/2` with `B = n/(2 g_6 R^2)`. `run.py` checks this against Job Five's flux term with sympy.
`p_flux` is evaluated only at Job Five's stable minimum (on-shell) and only for `Lambda_6 > 0`, because for `Lambda_6 < 0` the "share" leaves [0, 1] and its denominator can vanish.

**New mapping [hive-interpretation].** Job Three's `p` is a face-occupancy (filling) fraction in its Betti/percolation model. Reading it as the flux share of the vacuum energy is a new identification, not a derivation.

## Band-reuse case (Helios's catch)

`run.py` reads Job Three's source read-only. Job Three's residual `rho_res` comes from `rho_at(p)`, a function of the occupancy `p` alone on the fixed m = 16 Goldberg sphere. Its window bands come from `rho_window_bands()`, which takes no flux argument. The flux `n` entered Job Three **only** through the separate `p = n/(3R^2)` map, which turned the p-bands into per-n R-bands.

So **the case is "intrinsic"**: the survival bands are fixed intervals of Job Three's own `p`, the **same for every n**, and independent of how `p` was obtained. Job 5c reuses those p-bands unchanged with the new `p_flux` [hive-interpretation]. It does **not** reuse Job Three's per-n R-bands, which belonged to the old map. No band was recomputed and no percolation was run.
The primary band edges are Job Three's own code-derived table (`Analytic R-bands ... p_lo/p_hi from rho(p)`) [computed in Job Three; finite-size: m = 16]. Job Five's slightly different linear-interpolation edges are printed as a cross-check.

## Stages

- **Stage 0 [identity].** At the exactly flat RSS point, `Lambda_6 = B^2/2`, so `p_flux = 1/2` for every n. `run.py` prints this for n = 1-6, whether 1/2 lies in each n's band, and the distances to the band edges. Venus's RSS unit map (`M_6^4 = 1/(8 pi G)`, `g_6 = e`) [standard: RSS 1983] is verified with sympy for the flat radius and the tuned `Lambda_6`.
- **Stage 1 [computed].** `p_on(n, Lambda_6)` along the stable root for n = 1-6 and `0 < Lambda_6 < Lambda_max(n) = b^2/(3 a c n^2)`. It reports exact window edges in closed form, a fine-grid cross-check, the dS/AdS split from `V_min = (b x - 2 c n^2)/x^3`, and which n survive at each fixed `Lambda_6`.
- **Scaling identity (Helios).** `p_on` depends only on `n/n_max`, with `n_max^2 = b^2/(3 a c Lambda_6)`. `run.py` prints the k-family `Lambda_6^(k) = (3/k)^2 Lambda_6^(3)` for k = 1-6 at the n = 3 window edges and spot points. It checks each against **n = k's own band**.
- **Robustness [assumed input: choice of denominator].** Leaving the curvature energy out of the denominator is a choice. `run.py` also grades `p_curv = (B^2/2)/(B^2/2 + Lambda_6 + |curvature term|)`, built from the same three terms of `V`. A signed curvature term would make the denominator the total vacuum energy, which vanishes at the flat point, so the absolute value is used.

## Walls

- **Flat point [by construction].** `p_flux = 1/2` for every n at the RSS flat point, so the flat point alone cannot select n.
- **Scaling [identity].** Because `p_on` is a function of `n/n_max` only, and Job Three's bands do not depend on n, `n -> k n` with `Lambda_6 -> Lambda_6/k^2` maps survivors onto survivors exactly. The filter therefore cannot select n on its own. Any "n = 3" statement is conditional on `Lambda_6`.
- **The filter only sees `Lambda_6 n^2` [identity] (Helios).** Under `n -> k n`, `Lambda_6 -> Lambda_6/k^2`, `x -> k^2 x`, every term of the potential picks up the same factor, so the whole potential is multiplied by `k^-4` (sympy-checked in Stage 0). No ratio built from it, including `p_flux` and `p_curv`, can pick n. Brane tension only relabels n (Helios: `V_alpha(x; n) = alpha V_1(x; n/alpha)`) [assumed input: not re-derived here]. A Casimir term `C/x^4` scales as `k^-8` instead, so it could break the degeneracy; that is being tested in Job 5b, not here.
- **Negative Lambda_6.** The share leaves [0, 1] and has a pole, so it is excluded.
- **Robustness.** `RESULTS.md` shows the range that `p_curv` can reach on-shell; if that misses Job Three's bands, nothing survives under that version.

## Grades (fixed in `run.py` before the first run)

- **PASS:** only n = 3 survives, over a dS stretch of `Lambda_6` at least 5% wide (relative width = width/midpoint, `(hi - lo)/((hi + lo)/2)`), with no `s` anywhere. The grade uses width/midpoint only; `RESULTS.md` also prints width/lower edge, `(hi - lo)/lo`, next to it for reference (Venus).
- **PARTIAL:** several n survive.
- **FAIL:** no n survives.
- A single surviving n that misses the PASS conditions falls outside the fixed scheme and is reported as UNGRADED.
- Both `p` versions are graded. Next to the grades, `RESULTS.md` gives the conditional statement "n = 3 alone for `Lambda_6` in [...]" [post-hoc], with a printed line showing that even the post-hoc "n = 3 alone" dS stretch is below the PASS width, on either width measure [computed].
- `RESULTS.md` also has an all-n check of that statement (Venus) [identity; computed]. By scaling (`u = (n/n_max)^2` is proportional to `Lambda_6 n^2`), another n's band-1 window overlaps n = 3's only if `9/n^2` lies in a ratio interval computed from the band-1 edges; only n = 3 does. Band 2 of any n >= 1 stays below n = 3's band 1. An analytic cut-off shows that n beyond a computed bound cannot reach any n = 3 window, and a direct check runs over n = 1-1000.

**Remaining assumption.** Uniqueness cannot PASS from inside this run. Because of the scaling identity, something outside the run has to fix `Lambda_6`, for example a KK-gap requirement or a measured 4D vacuum energy `Lambda_4`. Until then, the most this toy can say is "n = 3 for `Lambda_6` in a window".

## Caveats

Only the breathing mode is included. Shape modes, flux tunnelling, one-loop/Casimir terms and brane tension are omitted, as in Job Five [assumed input]. "Stable" means classically stable in R only [standard]. Job Three's bands are finite-size (m = 16) and depend on its assumed residual window [finite-size; assumed input].

## Tag key

- [computed]: evaluated by `run.py`.
- [identity]: exact algebra, checked with sympy.
- [assumed]: a modelling choice.
- [assumed input]: an input value or convention taken as given.
- [by construction]: true because of how the quantity is defined.
- [standard]: textbook or literature result.
- [post-hoc]: chosen or stated after seeing results.
- [finite-size]: depends on the finite lattice size.
- [tuned]: holds only at a fine-tuned parameter value.
- [prediction]: an output that could be checked.
- [hive-interpretation]: a hive reading or identification, not derived.

## Reference

- S. Randjbar-Daemi, A. Salam and J. Strathdee, "Spontaneous compactification in six-dimensional Einstein-Maxwell theory," Nuclear Physics B 214 (1983) 491 [standard].

## Post-run notes (2026-10-02)

- [computed] The band-reuse case is **intrinsic**, as the source reading above said. `RESULTS.md` confirms that every source check holds.
- [computed] `p_flux` grade: **PARTIAL**. Every n in the scan survives in its own `Lambda_6` windows, and the n = 3 dS stretch is narrower than the fixed width threshold. `p_curv` grade: **FAIL**. Its on-shell range never reaches Job Three's bands.
- [identity] The k-family check holds exactly: `p_on` at `(k, (3/k)^2 Lambda_6)` equals `p_on` at `(3, Lambda_6)` to round-off, and band membership matches for every k. The filter cannot select n by itself.
- [post-hoc] The conditional "n = 3 alone for `Lambda_6` in [...]" intervals are printed in `RESULTS.md` next to the grades. Uniqueness still depends on something outside the run fixing `Lambda_6`.
- [computed] The first run had a misleading diagnostic: the V-form check was normalised by `|V|`, which blows up next to the flat point. It now uses the sum of the term magnitudes, and `run.py` was re-run. Grades, thresholds and windows did not change, and `RESULTS.md` comes from the second run only.

- [computed; identity] **Post-run (fold-in, 2026-10-02, after sign-off).** This was a single fold-in pass of Venus's and Helios's notes: `run.py` was edited and re-run, and `RESULTS.md` was regenerated by it, not edited by hand. Thresholds and grades are unchanged: `p_flux` is **PARTIAL** and `p_curv` is **FAIL**. Added: width/lower edge next to width/midpoint; the line saying the post-hoc "n = 3 alone" dS stretch is below the PASS width; the all-n check; and the sympy check that scaling multiplies the potential by `k^-4`. All-n result: the band-1 "n = 3 alone" stretch (its AdS part and its dS part) holds for **every n >= 1** [identity]. The band-2 AdS "n = 3 alone" piece from the n = 1-6 scan does **not** survive intact. Band-1 windows of larger n (listed in `RESULTS.md`) cover most of it, leaving two thin AdS slivers [computed]. The dS "n = 3 alone" stretch is unchanged. It is the only dS piece, and it is still below the PASS width [computed].

## Sign-off

- Venus (maths): **PASS** (maths), 2026-10-02 19:33 BST.
- Helios (physics): **PASS** (physics; grade PARTIAL for `p_flux` and FAIL for `p_curv`, as computed), 2026-10-02 19:35 BST.
- Post-run: the fold-in pass above (Venus's width wording and all-n check, Helios's scaling line) came after both sign-offs. No re-grade.

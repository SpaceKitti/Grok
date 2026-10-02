# Job 5d spec: do branes lift the flux cap? (rugby ball, Salam–Sezgin)

Status: FINAL, locked 2026-10-02 21:40 BST by Helios on NanoRibbon's go. Build after 4c (Aethon). Pass rule and prediction are Venus's (Hive, 21:32), copied word for word in meaning and fixed before any code runs.

## Question
On Problem 2's sphere, Salam–Sezgin with the dilaton free allows only one unit of flux. Can two branes at the poles (the "rugby ball") make three units come out on their own, or only if we set something by hand?

## Naming (must be in the README)
- Hive's flux count, read as the family count [assumed mapping], is ABPQ's **N**.
- ABPQ's **n = ±1** is only a sign, fixed by the bulk field equations.
- ε = 4 G₆ T is the wedge removed (as a fraction of a turn), and α = 1 − ε.

## Sources [standard]
- ABPQ, hep-th/0304256, §4 (eqs. 4.1–4.8): the two-brane rugby ball in 6D supergravity. Positive tension removes a wedge, eq. 4.6 is the flux rule, and eq. 4.8 adds brane-localised flux Q±.
- Carroll–Guica hep-th/0302067 and Navarro JCAP 09 (2003) 004: the non-supergravity forerunners (cross-check only).
- GGP hep-th/0307238 (PLB 595 (2004) 498): the uniqueness theorem for the smooth vacuum, with one negative-tension cone. Context only, not the source of the rugby ball.

## The rules being tested
Bulk field, unchanged by the branes:
$$F=\frac{n}{2g_1}\sin\theta\,d\theta\wedge d\phi,\qquad n=\pm1,\qquad r^2e^{\phi}=\frac{1}{4g_1^2}.$$
Flux quantisation (eq. 4.6):
$$\frac{g}{g_1}=\frac{N}{n(1-\varepsilon)}.$$
With brane flux (eq. 4.8):
$$\frac{Q_+-Q_-}{2\pi}+\frac{n}{g_1}=\frac{N}{g(1-\varepsilon)}.$$
What it means: the branes leave the field strength alone but cut area out of the sphere, so positive tension means **less** total flux fits.

## Stages
**Stage A [identity], reproduction.** In sympy, integrate F over the cut sphere (area 4πα r²) and recover 4.6. Add ΔQ = Q₊ − Q₋ and recover 4.8. Print the limits:
- ε = 0 and ΔQ = 0 gives N = ±g/g₁, so the supersymmetric case g = g₁ gives |N| = 1. This is the existing cap.
- With T > 0 and ΔQ = 0, |N| ≤ g/g₁. Positive tension can only lower the cap.

**Stage B, the three ways to reach N = 3.** For each route, solve for the knob at N = 2, 3 and 4 and print it:
- (a) g = g₁ and ΔQ = 0: α = N, so ε = 1 − N and T = (1 − N)/(4G₆). N = 3 means T = −1/(2G₆), a negative tension of Planck size.
- (b) T > 0 (0 < ε < 1) and ΔQ = 0: g/g₁ = N/α. That's a ratio chosen by hand, above 3 for N = 3.
- (c) g = g₁ and T > 0, the **brane-flux route (ABPQ eq. 4.8)**: g₁ΔQ/2π = N/α − n. The brane flux is chosen by hand. This is the only route ABPQ say may keep g = g₁ and bulk supersymmetry, since Q₊ = Q₋ rules out g = g₁ once ε ≠ 0.

For each route, also print whether the map from knob to N is smooth and one-to-one (linear in N). If it is, nothing in the model prefers 3 over 2 or 4.

**Stage C, report only (not graded).**
- Route (a): negative-tension objects do exist in string theory (orientifold planes) [standard: beyond toy], but their tension is set by the string scale, not by G₆ of this compactification. Print the ratio a real such object would need, |T|·2G₆ = 1, and say plainly that nothing here supplies it.
- Route (c): print whether ΔQ is quantised in ABPQ. If a source shows brane flux comes in fixed units, list the discrete N values it would allow [hive-interpretation].
- Reuse the 5b note: tension only relabels the flux count, so it has the same blind spot (STILL_TO_DO line 52).

## Pass rule (fixed before the run, Venus 21:32)
5d **PASSes only if some route makes N = 3 preferred over N = 2 and N = 4 without any input set by hand to give 3.** Otherwise it's a FAIL (tuned).

## Pre-registered prediction (Venus 21:32, endorsed by Helios)
**FAIL (tuned) on all three routes.** Each one is linear in N with a continuous knob, so the brane relabels N but doesn't select it. This matches the 5b identity. Venus's earlier dS-bound guess, 4 − 3(nα)² ≥ 0, is **withdrawn** (it rested on the inverted rule) and must not be printed.

## If it fails (wall to log in STILL_TO_DO)
The next idea is the uneaten-axion route with a four-form source (STILL_TO_DO line 48). That is the one live way to revive A1's mechanism on this sphere.

## Cost
Sympy only, plus three short printed tables. Seconds of CPU, no grid scan.

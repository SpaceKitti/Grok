# pairA-qg-on-R1 — RESULTS

**Signed off 2026-09-25:** Venus (maths) and Helios (physics).

R1 QG toy written

this is a path-integral probe on R1, not a full QG theory

Reading: **path-integral probe over R1's complexified radial coordinate, base point on the Euclidean section [hive-interpretation]**. The loops are contours in ε continued into the complex plane, never along R1's Euclidean time circle τ, so they are not paths in R1 spacetime.

Z is a sum over homotopy classes weighted by periods of λ dε on the spectral curve; the flat saddle families reflect a topological (not dynamical) action [hive-interpretation].

No QG Hamiltonian was derived, no JT dual is claimed, no Einstein solution is claimed (R1 = AdS₂×S² is taken as given from pairA-jt-4d as the 4D target; ordinary S², no GoldbergHexa). A and B WRITE, C held.

## Set-up

- R1 (from pairA-jt-4d, read-only): AdS₂×S², F_JT = ε² − ε_EP², S² radius r = ε_EP = 0.51368066, horizons at ±ε_EP. Euclidean section = real ε with F_JT > 0 (|ε| > ε_EP, outside Γ). Quoted: "**R1 (AdS2 x S2, r = eps_EP) is the 4D target. R2 is not a target (kept as information only).**"
- Sheets: λ_A,B = λ_EP ± y/2, λ_EP = -0.308425i, v = -0.360253, y² = 4v²F_JT; y from probe-surface `load_surface.y_cut_gamma` (Γ-segment cut). Consistency with jt-4d's curve: max |y² − 4v²F_JT| = 4.4e-16 over 100 complex points [computed].
- Action: **S[path] = ∮ λ(ε) dε** along the path on the tracked Pair A eigenvalue branch (start on sheet A or B at the base point) — **[by construction / hive-interpretation: action choice]**. Akitti gave no action; this standard toy loop action was kept because it is the one built from the files' own data (the sheet eigenvalue λ and the ε-plane), and no other action is written in the loaded folders. Toy weight e^{−S}, ħ = 1 [by construction].
- The λ_EP part integrates to zero on any closed ε path, so S = ±½∮y dε [computed, identity].
- Base points (outside Γ, on the real axis, F_JT > 0): +1.25 ε_EP for loops around +ε_EP, −1.25 ε_EP for loops around −ε_EP; circles of radius 0.25 ε_EP centred on the tip (same circles as the probe-surface cover loops). ccw = counter-clockwise in the ε plane.

## Saddle table

'Saddle' is used only with this tag: **[by construction: chosen closed paths]**. They are not solved from δS = 0 as an equation. Stationarity was checked instead: λ(ε) is holomorphic away from the tips, so δS = 0 for every deformation that keeps the base point and does not cross a tip [standard: Cauchy]. Numerically, max |ΔS| over 4 shape deformations (two ellipses, two off-centre circles, same base point) is listed. So each path is stationary, but degenerately so: the whole homotopy class is one flat critical family, not an isolated saddle. S depends only on the base point, the start sheet and the winding [computed].

| saddle | loop | direction | start sheet | Re S | Im S | analytic S | max |ΔS| (deformations) | Γ crossings (count, at x/ε_EP; F_JT there) | swap (continuation) | ends on | min |λ_A−λ_B| on path |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | +ε_EP once (2π) | ccw | A | +0.023228 | -0.000000 | +0.023228 | 4.1e-13 | 1: +0.7500 (F_JT = -0.1154) | **YES** | B | 0.2448 |
| S1 | +ε_EP once (2π) | ccw | B | -0.023228 | -0.000000 | -0.023228 | 4.1e-13 | 1: +0.7500 (F_JT = -0.1154) | **YES** | A | 0.2448 |
| S1 | +ε_EP once (2π) | cw | A | +0.023228 | -0.000000 | +0.023228 | 4.1e-13 | 1: +0.7500 (F_JT = -0.1154) | **YES** | B | 0.2448 |
| S1 | +ε_EP once (2π) | cw | B | -0.023228 | -0.000000 | -0.023228 | 4.1e-13 | 1: +0.7500 (F_JT = -0.1154) | **YES** | A | 0.2448 |
| S2 | +ε_EP twice (4π) | ccw | A | +0.000000 | -0.000000 | +0.000000 | 4.5e-13 | 2: +0.7500 (F_JT = -0.1154), +0.7500 (F_JT = -0.1154) | **NO** | A | 0.2448 |
| S2 | +ε_EP twice (4π) | ccw | B | +0.000000 | +0.000000 | +0.000000 | 4.5e-13 | 2: +0.7500 (F_JT = -0.1154), +0.7500 (F_JT = -0.1154) | **NO** | B | 0.2448 |
| S2 | +ε_EP twice (4π) | cw | A | -0.000000 | +0.000000 | +0.000000 | 4.5e-13 | 2: +0.7500 (F_JT = -0.1154), +0.7500 (F_JT = -0.1154) | **NO** | A | 0.2448 |
| S2 | +ε_EP twice (4π) | cw | B | -0.000000 | -0.000000 | +0.000000 | 4.5e-13 | 2: +0.7500 (F_JT = -0.1154), +0.7500 (F_JT = -0.1154) | **NO** | B | 0.2448 |
| S3 | −ε_EP once (2π) | ccw | A | +0.023228 | +0.000000 | +0.023228 | 1.2e-12 | 1: -0.7500 (F_JT = -0.1154) | **YES** | B | 0.2448 |
| S3 | −ε_EP once (2π) | ccw | B | -0.023228 | +0.000000 | -0.023228 | 1.2e-12 | 1: -0.7500 (F_JT = -0.1154) | **YES** | A | 0.2448 |
| S3 | −ε_EP once (2π) | cw | A | +0.023228 | +0.000000 | +0.023228 | 1.2e-12 | 1: -0.7500 (F_JT = -0.1154) | **YES** | B | 0.2448 |
| S3 | −ε_EP once (2π) | cw | B | -0.023228 | +0.000000 | -0.023228 | 1.2e-12 | 1: -0.7500 (F_JT = -0.1154) | **YES** | A | 0.2448 |
| S4 | −ε_EP twice (4π) | ccw | A | -0.000000 | -0.000000 | +0.000000 | 1.3e-12 | 2: -0.7500 (F_JT = -0.1154), -0.7500 (F_JT = -0.1154) | **NO** | A | 0.2448 |
| S4 | −ε_EP twice (4π) | ccw | B | -0.000000 | +0.000000 | +0.000000 | 1.3e-12 | 2: -0.7500 (F_JT = -0.1154), -0.7500 (F_JT = -0.1154) | **NO** | B | 0.2448 |
| S4 | −ε_EP twice (4π) | cw | A | +0.000000 | +0.000000 | +0.000000 | 1.3e-12 | 2: -0.7500 (F_JT = -0.1154), -0.7500 (F_JT = -0.1154) | **NO** | A | 0.2448 |
| S4 | −ε_EP twice (4π) | cw | B | +0.000000 | -0.000000 | +0.000000 | 1.3e-12 | 2: -0.7500 (F_JT = -0.1154), -0.7500 (F_JT = -0.1154) | **NO** | B | 0.2448 |

Numerical vs analytic action: max |S_num − S_analytic| = 3.8e-10. Analytic values: once around (S1, S3) the loop collapses onto the real segment between tip and base, so S = −∫_tip^base y_X dx, which is real and the same for ccw and cw. Twice around (S2, S4) is a closed cycle on the double cover, contractible there (y is holomorphic in √(ε − tip)), so S = 0 [computed + standard].

Toy partition sum over the chosen paths (ccw, 4 paths × 2 start sheets, ħ = 1): Z = 8.001079 -0.000000i; swap sector (S1, S3) 4.001079, return sector (S2, S4) 4.000000 [by construction: the sum is over the chosen paths only; no measure, no fluctuation determinant].

### Γ intersection and the Euclidean section [careful-before-toy]

- Every loop around a tip crosses Γ once per turn (at 0.75 ε_EP for +ε_EP, −0.75 ε_EP for −ε_EP), where F_JT = −0.4375 ε_EP² < 0. So each loop enters the F_JT < 0 region, which is the R2 / Lorentzian side, not the Euclidean R1 section. A loop cannot circle a tip while staying in F_JT > 0.
- Apart from those real-axis points, the paths run through complex ε, where F_JT is complex. So the paths are complexified contours: the only real points on each path are the base point (F_JT > 0, on the Euclidean R1 section) and the Γ crossing(s) (F_JT < 0, off it). Calling Z a path integral 'on R1' means: base point on the Euclidean section, contour in R1's radial coordinate ε continued into the complex plane [careful-before-toy].
- No loop runs along the Euclidean time circle τ of R1 (period 2π/ε_EP smooth, 4π/ε_EP = τ_swap); τ does not appear in S. The loops are therefore not paths in R1 spacetime. Relating the ε-winding to the τ angle is the jt-4d [hive-interpretation] and is not used here.
- The gap never closes on any path (min |λ_A − λ_B| > 0), so the continuation is well defined; no path passes through an EP.

### Extra (not requested): loop around both tips

| loop | direction | start sheet | Re S | Im S | analytic | swap | Γ crossings |
|---|---|---|---|---|---|---|---|
| circle r = 2 ε_EP from +2 ε_EP | ccw | A | +0.000000 | +0.298637 | +0.298637i | NO | 0 |
| circle r = 2 ε_EP from +2 ε_EP | ccw | B | +0.000000 | -0.298637 | -0.298637i | NO | 0 |
| circle r = 2 ε_EP from +2 ε_EP | cw | A | -0.000000 | -0.298637 | -0.298637i | NO | 0 |
| circle r = 2 ε_EP from +2 ε_EP | cw | B | -0.000000 | +0.298637 | +0.298637i | NO | 0 |

This is the only closed path here with non-zero action: ½∮y dε = ∓iπ v ε_EP² (|value| = π|v|ε_EP² = 0.298637), purely imaginary, from the ε → ∞ tail of y [computed]. It crosses Γ zero times and returns (no swap), consistent with the probe-surface cover row 'big loop around both'.

## Matches

- **D3 (2π swap, 4π return): PASS** — computed by continuation on all 16 path/direction/sheet cases above (S1, S3 swap; S2, S4 return); probe-surface D3 row: PASS. [computed, known]
- **D4 (A and B continue past the EPs, C held): PASS** — two-detour test from the outside base point into Γ (semicircle r = 0.25 ε_EP above vs below each tip):
  - tip +1 ε_EP: +1.25 → +0.75 ε_EP; A lands on A (above) / B (below); B lands on B / A; pairings swapped: YES; min gap 0.2448 > 0; half-path actions (A) above +0.011614+0.089989i, below +0.011614+0.068443i.
  - tip -1 ε_EP: -1.25 → -0.75 ε_EP; A lands on A (above) / B (below); B lands on B / A; pairings swapped: YES; min gap 0.2448 > 0; half-path actions (A) above +0.011614-0.089989i, below +0.011614-0.068443i.
  - only A and B enter Z (the curve y² = 4v²F_JT has two sheets); jt-4d SHEETS = {'A': 'WRITE', 'B': 'WRITE', 'C': 'held'} (C held: YES); probe-surface D4 row: PASS. [computed, equivalent to the 2π swap]
- **D6/D7: inherited from H_A, not from Z.** Z is a sum over sheet paths with a holomorphic action; it has no loss or drive direction, so it cannot produce the D6/D7 behaviour. Those come from the lossy driven H_A evolution (pairA-drive-return).
- Note (not run): the link to the sweep's approach to w → 1 (pairA-drive-sweep) is through the DDP-type time integral Im∫(λ_A − λ_B) dt = ∫ y dε / (iω(ε − tip)) along the driven loop (ε = tip + r e^{iωt}), which scales with 1/ω, i.e. with γT. It is not S1 itself: S1 = ½∮y dε has no 1/ω and no time [standard: Dykhne–Davis–Pechukas; Venus correction].

## Tags

[standard]: Cauchy/contour deformation, AdS₂×S² form of R1. [by construction]: the action choice, base points, chosen paths ('saddles'), ħ = 1, the finite sum Z. [computed]: actions, analytic cross-checks, deformation invariance, crossings, swap by continuation, D3/D4. [hive-interpretation]: reading Z as a path-integral probe over R1's complexified radial coordinate; the action choice; Z as a sum over homotopy classes weighted by periods. [careful-before-toy]: the loops leave the Euclidean section (they cross Γ into F_JT < 0 and run through complex ε).

## Loaded folders (read-only)

- `C:\Users\Akitt\pairA-jt-4d`: jt2d.py imported (EPS_EP, LAM_EP, V, y2, SHEETS); RESULTS.md R1 lines quoted.
- `C:\Users\Akitt\pairA-qg-probe-surface`: load_surface.y_cut_gamma imported (sheet convention); RESULTS.md D1–D7 rows read (D1 PASS, D2 PASS, D3 PASS, D4 PASS, D5 PASS, D6 PASS, D7 PASS); first line: "**Signed off 2026-09-25:** Venus (maths) and Helios (physics) on D1–D7 and cover.".
- SHA-256 of every file (14 files) before any import and after all computations: **unchanged**.


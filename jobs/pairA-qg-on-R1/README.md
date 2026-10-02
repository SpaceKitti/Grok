# pairA-qg-on-R1: mini path integral on R1

**Signed off 2026-09-25:** Venus (maths) and Helios (physics).

Reading: path-integral probe over R1's complexified radial coordinate, base point on the Euclidean section [hive-interpretation]. The loops are contours in ε continued into the complex plane, never along R1's Euclidean time circle τ, so they are not paths in R1 spacetime.

Question: write a toy path integral Z on the Euclidean R1 section (AdS₂×S², F_JT = ε² − ε_EP² > 0, outside Γ). Then check whether its chosen closed paths reproduce D3 (2π swap, 4π return) and D4 (A and B continue past the EPs, C held) of the signed-off probe surface.

Run: `python run.py` (Grok\.venv python, PYTHONIOENCODING=utf-8). It writes RESULTS.md, which contains the lines 'R1 QG toy written' and 'this is a path-integral probe on R1, not a full QG theory'.

## Loaded, read-only (SHA-256 of every file before any import and after all computations)
- `C:\Users\Akitt\pairA-jt-4d`: `jt2d.py` is imported for the R1 numbers (ε_EP = 0.51368066, λ_EP = −0.308425i, v = −0.360253, y² = 4v²F_JT, sheet status A/B WRITE, C held). The R1 target line and region row are quoted from RESULTS.md. R1: AdS₂×S², S² radius r = ε_EP, horizons at ±ε_EP, ordinary S² (no GoldbergHexa). This job does no Einstein solve and makes no Einstein claim.
- `C:\Users\Akitt\pairA-qg-probe-surface`: `load_surface.y_cut_gamma` is imported (sheet convention A = λ_EP + y/2, B = λ_EP − y/2, Γ-segment cut). The D1–D7 rows are read from RESULTS.md.
- Bytecode writing is disabled, so no __pycache__ lands in the loaded folders.

## Action [by construction / hive-interpretation: action choice]
S[path] = ∫ λ(ε) dε along the path, with λ the Pair A eigenvalue on the branch being tracked (continuous continuation from sheet A or B at the base point). Toy weight e^{−S}, ħ = 1. Akitti gave no action. No other action is written in the loaded folders, so this standard toy loop action is kept; it uses only the files' own data (the sheet eigenvalue and the ε plane).

## Paths ("saddles" only with the tag [by construction: chosen closed paths])
- Base points: real ε outside Γ, +1.25 ε_EP for the +ε_EP loops and −1.25 ε_EP for the −ε_EP loops. Circles of radius 0.25 ε_EP centred on the tip (the same circles as the probe-surface cover loops).
- S1: +ε_EP once. S2: +ε_EP twice. S3: −ε_EP once. S4: −ε_EP twice. Each is run ccw and cw, starting from sheet A and from sheet B.
- Stationarity is checked, not assumed: S is recomputed on 4 deformed paths with the same base point (two ellipses, two off-centre circles). λ is holomorphic off the tips, so δS should vanish (Cauchy). That makes each path a degenerate critical family, not an isolated saddle.
- Analytic cross-checks: for once around, S = −∫_tip^base y_X dx (real, direction independent); for twice around, S = 0.
- Extra, not requested: one loop around both tips.

## Printed per path
Re S, Im S, the analytic value, max |ΔS| under the deformations, the Γ crossings (count, position, F_JT there), swap YES/NO by continuation, the end sheet, and the minimum gap.

[careful-before-toy]: every loop around a tip crosses Γ into F_JT < 0 and runs through complex ε. It therefore leaves the Euclidean section; only the base point is on it.

## Matches
- D3 PASS if S1 and S3 swap and S2 and S4 return, for all directions and start sheets, and the probe-surface D3 row is PASS.
- D4 PASS if two conditions hold. (a) At each tip, the semicircle from the outside base point into Γ above the tip and the one below it give swapped pairings, with the gap open. (b) Only A and B enter Z, jt-4d has C held, and the probe-surface D4 row is PASS.
- 'D6/D7: inherited from H_A, not from Z' is printed: Z has no loss or drive direction.

## Files
- `load_inputs.py`: read-only loaders and hashing.
- `pathint.py`: curve, branch tracking, action, paths, crossings, analytic values.
- `run.py`: runs everything and writes RESULTS.md.

Scope: toy. No QG Hamiltonian derived, no JT dual, no Einstein solution. A and B WRITE, C held.

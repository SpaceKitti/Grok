# IT1b power-law measure (Venus, maths) — FROZEN 2026-10-23 12:45 BST, before any IT1b rows exist
[hive proposal, untested]. Applies only to new IT1b runs. Not to be used to regrade diag22.

Model: X_0(t) ~ A_0 t^(-p_0); X_d(t) ~ A_d t^(-p_d).
Observable: r_d(t) = ln X_d(t) - ln X_0(t) (same seed, same t) = dlnA - dp * ln t.
Fit window: t in [0.1, 0.6], least squares of r_d against ln t. Slope = -dp, intercept = dlnA.

Gates (all must pass, else row UNDECIDED, no retune):
G1 (REPORT-ONLY from rev 3, 13:40 BST, after the short check showed p0 = 0.0301 vs 0.0415, so X0 is not a single power law; it no longer gates the verdict) power law holds: p_0 fitted on [0.1, 0.245] and on [0.245, 0.6] (geometric halves) agree within 10%.
G2 r_d is straight in ln t: same slope dp on both halves within 10% (or both within seed spread of 0).
G3 signal above noise: |dp| (and |dlnA|) larger than the spread across the 2 seeds; else UNDECIDED.
Pass (old cut-offs, unchanged):
P1 linearity: dp(0.003)/dp(0.0015) in 1.7-2.3 (use dlnA instead if dp fails G3 at both d).
P2 calibration shift <= 5%.
P3 main control < 0.23 on the SAME statistic as diag22 (the paired shift at alpha=0.5, computed by the unchanged diag22 function at t=0.6). NOT dp: dp is an exponent, different units. (rev 2, 12:52 BST, before any IT1b rows)
Short run: single point t=0.6, X_0=2.9027 (same seed), reproduced within 2%, plus the 136-test suite. Code-change check only.

rev 3 (13:40 BST, before any delta rows exist): G2 on r_d (paired, model-free) is the settling gate. Because X0 is not a single power law, the slope of r_d vs ln t is reported as the 'paired log-response', NOT as an exponent shift dp. P1 uses that slope (or the intercept fallback). Window, cut-offs and the other gates are unchanged. G1 stays logged for both alpha.

rev 4 (13:45 BST, before any delta rows exist; IT1b's one fix round). Merged with Helios's proposal:
VERDICT: chi(t)=(X_d(t)-X_0(t))/d at t=0.6 (fixed-time paired response). Linearity dX(0.003)/dX(0.0015) in 1.7-2.3.
Noise: |dX| at d=0.0015 > seed spread, else UNDECIDED. P2, P3 unchanged. G1, G2, dp, r_d slope: report-only.
Meaning: linear response at t=0.6 of a reduced model, not a settled state.
BPST pre-step (alpha=1 only): S/8pi^2 = |Q| = 1 (checked: int 48 rho^4/(r^2+rho^2)^4 d^4x = 8 pi^2).
Finite box truncates the tail: fraction outside radius R = rho^4(3R^2+rho^2)/(R^2+rho^2)^3. For a 1% cut at rho=3 this needs R >= 12.5.
Pass: S/8pi^2 within 1% of 1 after h->0 fit across >=2 lattice spacings, with box half-width >= 12.5 (else compare to 1 - tail(R) and label it).

rev 5 PROPOSAL (21:20 BST, IT1b fix round, not yet co-signed by Helios; no rows exist) [hive proposal, untested]
Diagnosis from diag22 (t=0.6): seed spread of dX scales with delta (a=1: 0.0010 -> 0.0019; a=0.5: 0.0019 -> 0.0038).
So the "noise" is the seed-dependent LINEAR response (random perturbation direction), not a floor. A bigger delta alone cannot beat it.
The seed-mean dX is then dominated by the even (delta^2) part, which is why linearity failed (0.55, 1.46).
(a) Antithetic pairs: for each seed, run +delta and -delta.
  odd  L_s(d) = (X(+d) - X(-d)) / (2d)   (linear response, per seed)
  even E_s(d) = (X(+d) + X(-d) - 2 X0) / d^2
  Linearity per seed: L_s(2d)/L_s(d) in [0.85, 1.15] (same as old 1.7-2.3 on dX). Noise gate: |mean_s L| > spread_s(L), else UNDECIDED. Even part report-only.
  delta in {0.003, 0.006}, 2 seeds, alpha in {1, 0.5}: 16 rows + 2 baselines.
(b) Calibration 7.9%: the Wilson-flow O(a^2) lattice term changes the BPST size at rho/a=3. Standard fix: over-improved flow, eps=-1
  (Garcia Perez, Gonzalez-Arroyo, Snippe, van Baal 1994; de Forcrand, Garcia Perez, Stamatescu 1997), which removes O(a^2) so an instanton keeps its size. Cut-off stays rel_shift <= 5%.
  Calibration is recomputed first (one short row); if it is still > 5%, stop before the delta rows.

rev 6 FROZEN (21:25 BST, co-signed by Helios, before any delta rows exist). Rev 5 plus Helios's conditions:
1. X(+d), X(-d) and X0 share one seed and one RNG stream (X0 is deterministic, so this costs nothing).
2. If -d is not a physical perturbation, report it and fall back to same-seed d in {0.003, 0.006} with dX(0.006)/dX(0.003) in 1.7-2.3.
3. Under eps=-1: re-check the BPST pre-step, calibration (<=5%) and X0 before any delta row runs. Stop if any of them fails.
BPST pre-step (Wilson action): S0=0.98739 lies inside [0.97682, 1] (cube >= ball), so it PASSES.

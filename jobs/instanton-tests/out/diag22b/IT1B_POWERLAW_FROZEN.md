# IT1b power-law measure (Venus, maths) — FROZEN 2026-10-23 12:45 BST, before any IT1b rows exist
[hive proposal, untested]. Applies only to new IT1b runs. Not to be used to regrade diag22.

Model: X_0(t) ~ A_0 t^(-p_0); X_d(t) ~ A_d t^(-p_d).
Observable: r_d(t) = ln X_d(t) - ln X_0(t) (same seed, same t) = dlnA - dp * ln t.
Fit window: t in [0.1, 0.6], least squares of r_d against ln t. Slope = -dp, intercept = dlnA.

Gates (all must pass, else row UNDECIDED, no retune):
G1 power law holds: p_0 fitted on [0.1, 0.245] and on [0.245, 0.6] (geometric halves) agree within 10%.
G2 r_d is straight in ln t: same slope dp on both halves within 10% (or both within seed spread of 0).
G3 signal above noise: |dp| (and |dlnA|) larger than the spread across the 2 seeds; else UNDECIDED.
Pass (old cut-offs, unchanged):
P1 linearity: dp(0.003)/dp(0.0015) in 1.7-2.3 (use dlnA instead if dp fails G3 at both d).
P2 calibration shift <= 5%. P3 main control < 0.23.
Short run: same fit on t<=0.6 must reproduce the diag22 X_0 within 2% (code-change check only).

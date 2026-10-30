# SEED_PASS_RULES_V4 (Venus spec 2026-10-29 21:29 GMT). Frozen before any V4 results. V3 (ff7eac5f) stays on record as failed.
Seed: G = exp(theta n.(-i sigma)), 0<=theta<pi, code's own G (A = iG dG^dagger). h = G^{-s(r)}; A' = hAh^dagger + i h dh^dagger, sampled from formula.
s(r)=1 for r<=eps/2, C-infinity smoothstep to 0 at r=eps (all derivatives zero at both ends).
P0: |h-1| < 1e-12 on cap edge over full (x3,x4) range; jump in A' at edge < 1e-6; max theta over cap <= pi-0.2 (else shrink eps).
P1: |Q-1| <= 0.02.
P2: fit S/8pi^2 = c0 + c1 x over N=21,29,41, x=(lambda/rho)^2, a=rho/3 fixed; c0 = 0.989 +- 0.01.
P3: middle point within 0.5% of line.
P4: eps 0.3..0.5 rad changes S by <= 0.1%.
P5: box size change moves S by <= 0.1%; a-shift from extra run at a=rho/4, N=21, same physical box L*a, reported.
Diagnostic: cap/N^2 per N.
Proposed stop (Helios, hive proposal): if V4 fails, seed marked UNDECIDED; Venus checks weyl_seed.py line by line / looks for a published construction before any 4th patch. Rung 0 on hold either way.

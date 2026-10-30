# CONE_SPEC_V1_3 addendum (Venus). Retargets to existing cones. V1_2 6f8c5d0b stands (fuzzy seed, radial solve, measured p, a-refinement, report-only P3/P5) except where changed here. D2 and OPEN-C2 dropped; GoldbergHexa is a guide only, not built.
Cones (from Orion: CONE_TIP_NOTE.md, cone-sims/spec/CONE_SIM_SPECS.md; Akitti's post 2110455808366633013 not re-read, so Orion confirms against the post before results go to Akitti):
- M: old-lift tip, alpha=2 (excess, two full turns, square-root branch point). MAIN.
- G: Grok's tweak / IT1b seed, alpha=1/2.
- H: HP2 row, alpha=0.75.
n=1,2 each. Build: a true conical metric ds^2=dr^2+alpha^2 r^2 dtheta^2, with theta in [0,2pi) and the full angle 2pi*alpha, for all three cones (one builder; for G the Z_2 orbifold build is kept as a cross-check, agreeing on Q to 0.01).
P1 charge: for each cone and n, Aethon freezes the tip holonomy and Q_pred from it before any run. No 1/k rule. Pass: the a^2-fit Q0 within 0.02 of Q_pred, as in V1_2. The cover check |kQ0-round(kQ0)|<=0.02k applies to G only (k=2). For M, the extra check is that Q0 on the cone equals twice Q0 of the same field read on one sheet, to within 0.02.
P2: p_pred=|n|/alpha (M: 0.5, 1; G: 2, 4; H: 1.333, 2.667), with the V1_2 pass rule.
Flag F-M: for M with n=1, p=0.5, so the field gradient blows up at the tip (the energy density goes like 1/r). It is integrable, so this is not a failure, but the radial solve needs Δr <= w_N/20 near the tip, and the energy near the tip is reported.

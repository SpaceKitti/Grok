# CONE_SPEC_V1_5 addendum (Venus). Frozen before any refit. Applies to P2 for the existing V1_4 solutions (same code 5448980d), plus a fix list for the next build.
P2 refit (no re-solve needed; uses the stored s1 at DR and s2 at DR/2):
- Local exponent p_loc(r) = r f'(r)/f(r), with central differences.
- Fit p_loc = p_tip + c r^2 on r in [20*DR, 0.3*rho] (DR = w_N/40). The window is fixed by the grid and rho only, chosen now, before any refit is seen.
- Pass: |p_tip - |n|/alpha| <= 0.05 |n|/alpha AND |p_tip(DR) - p_tip(DR/2)| < 0.02 |n|/alpha. Otherwise UNDECIDED. No window change after results.
- Report p_tip for all 10 rows, side rows labelled.
Q: the V1_4 Q null is withdrawn as a test (Q = n*a_eq by construction). Q is reported, not graded. Double-cover and Z2 checks are dropped as tautological.
Required before any next build (not graded now):
F1. The energy goes to the self-dual form 0.5B^2+0.5|Dpsi|^2+(1/8)(1-f^2)^2, with check E/(pi|n|) -> 1.
F2. Fuzzification must survive the solve: the tip has to carry the fuzzy-sphere structure itself (matrix / finite-N shells), not just seed a classical minimiser. OPEN, and the spec goes to Helios and Aethon.
F3. A real charge test needs a tip-local measurement (flux within r <= w_N, or the tension route). OPEN.
Akitti line: the tip field is a classical abelian vortex standing in for her instanton, and the cones were not yet fuzzified.

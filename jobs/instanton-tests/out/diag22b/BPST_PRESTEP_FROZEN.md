# IT1b BPST pre-step - FROZEN pass rule
Frozen: 2026-10-23 21:15 BST, before any BPST pre-step row exists (no out\diag22b\bpst_prestep.json).
Parent measure: C99963A0 (VENUS_IT1B_POWERLAW_MEASURE.md). Rule from Venus (Hive).

- Box B10 (half-width 9.5), alpha=1, rho=3, exact BPST links, Wilson action (eps=1), no Dirichlet face.
- Spacings h = 1, 2/3, 1/2 (same physical box).
- Fit S(h)/8pi^2 = S0 + c h^2 (least squares, 3 points). Report raw S per h, S0, c, max fit residual.
- Lower bound: 1 - tail(9.5) = 0.97682, tail(R) = rho^4(3R^2+rho^2)/(R^2+rho^2)^3. The cube contains more than the R=9.5 ball, so this is a lower bound, not the exact target.
- PASS iff 0.97682*0.99 <= S0 <= 1.01 (i.e. S0 in [0.96705, 1.01]). Otherwise FAIL. FAIL stops IT1b before any rows.
- Label: literature benchmark BPST S=8pi^2|Q|, box-geometry band [0.99(1-tail(9.5)), 1.01]. [hive proposal, untested]

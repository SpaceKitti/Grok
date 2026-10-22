# instanton-tests (Aethon, solver/code)
Spec: spec/INSTANTON_TESTS.md rev 12, sha256 prefix 5DD76953 (FINAL_SPEC_HASH in run.py; refuses any other hash). rev 12 HOLD is coded: graded mode refuses.
Also: spec/CHANGES_60C9EBD4.md (the live CHANGES file has since moved to B3B350F0 with cone-spec entries), VENUS_CONE_DIFF_REV10 F657E190.
Files: run.py (only entry point for outputs), lattice.py (geometry, BPST seed, smoke action), kernels.py (flat-loop action, gradient, RK3 flow + target-rho stop, clover F/Q, self-duality shells, gauge-fixed Hessian + Lanczos with 3.3 GB guard, generic seed, seed bootstrap), tests.py (unit tests), diag_faces.py / diag_relax.py (scratch face diagnosis), out/.
Run: `$env:PYTHONIOENCODING='utf-8'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py smoke`

## Built
- Polar lattice: one r=0 tip site, no zero-length links, rings at (n+1/2)a (so 10.5a / 12.5a exist), L_phi=20, alpha*20 angular sites (wedge glued), identity Dirichlet faces.
- S(eps) per plane: (4-eps)/3 1x1 + (eps-1)/48 2x2, prefactor = complementary/own lengths (xi only in prefactors), Wilson 1x1 only where any corner has r<2a.
- Fixed before any run (in code): alphas, eps rows {1,0,-1,-0.25}, k_Delta=3, windows 0.3/0.4, a-series rho/a 3/4/5, off-tip B16 d0=10.5a rho=4.2a, B20 d0=12.5a rho=5a (B12 report-only, out of order estimate), per-eps p_a {1:2, -1:2, 0:4, -0.25:2} gate, IT2 tau=3E_a, IT3 0.02/0.1/20%, IT4 B10/B12/B16 rho=3a, 30 vectors, p=4, residual>1sigma => report-only, B10 9% in quadrature, predictions 6 / control 8. IT4 waits if free RAM < 3.3 GB.
- Grading logic: 3-point Richardson, off-tip E_a with the eps's p_a, E = sqrt(E_a^2 + sigma^2/8), IT4 weighted fit + residual rule.

## NOT COMPUTED (YET) — graded mode refuses
Cartesian wedge row; p_box (frozen only from relaxed fields; the seed's 2.7-3.0 is a face-jump artefact); rho-estimator calibration (BPST rho=3a reads 4.0-4.1a with the r>=2a cut); a stable flow step (spec 0.01 unstable; 0.005 unstable on B10 at t~0.4); Lanczos cost at B10+ (tiny-box eigsh 51 s; B10 would be hours in numpy).
Tip gauge copies: the tip is one site by construction, so there are no copies; its gauge direction is projected with the other interior sites.

## Post-run notes (scratch smoke, H5 — not graded, not a test)
See out/smoke_scratch.json and out_smoke_console.txt. Summary in Aethon's report to the room.
- Peak-RSS probe returned 0 on Windows (ctypes struct bug); process peak NOT COMPUTED (YET).
- Face diagnosis (scratch, out/diag_faces_*.json): the excess is the identity-face jump on the UNRELAXED singular-gauge seed, not a code bug and not the physical box cost. Jump/8pi^2 = 0.099/0.056/0.023/0.011 (B10..B20) scales as l^-3.0 and grows as a->0 on an independent Cartesian box (0.171 at a=1 -> 0.274 at a=0.5). Without the face reset, lattice - continuum-in-box = -0.0166 on every box (eq. 19 at eps=1: -0.022). A short flow halves the jump on B10 (outer rings 0.083 -> 0.040 by t=0.35).
- Unit tests: 35/35 on the box (tests.py).

## Sign-offs
- Venus (maths): ____________
- Helios (physics): ____________
- Akitti (launch graded rows): ____________

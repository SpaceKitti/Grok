# Venus maths check of JAMMING_TEST_SPEC_DRAFT.md (1ece183b), 2026-11-09 23:05 UK. NOT FROZEN.
Open-problem check: STILL_TO_DO.md jamming entry OPEN; DEAD_ENDS.md grepped (flat-Bradlow reading of B dead). d=3 jamming open (arXiv:1310.2549, 0911.1384, titles only).

## Slips (must fix before freeze)
S1. Meaning of b. In v2_1 (63b69fbc) the energy is 1/2 B^2 + 1/2|DPhi|_tan^2 + 1/8 (1 - Phi^+Phi)^2: critical (BPS) coupling at EVERY b. b is the Bradlow ratio R^2/(2n) (FUZZY_CONE_SPEC_V2_1_ADDENDUM_E). In the continuum the 12-dim moduli Sym^6 S^2 are exactly flat for every b > 1 (Bradlow 1990; Garcia-Prada 1994), and b -> 1 is where Phi -> 0 and the vortices dissolve. So "force ~ (b-1)" and "b -> 1 switches rigidity on from zero" are wrong. Manton-Speight (CMP 236) is about the coupling lambda near 1, not about Bradlow b. The correct continuum null for J1/J2 is band = 0 at every b.
S2. Consequence: the measured band (lambda_min,nz ~ 3.7e-3 at b=2) is a lifting by the fuzzy discretisation (and/or the tangential projection / radial penalty), not a physical force. J2's exponent then measures how the lattice artefact depends on b. Before any reading it must be compared across N (61 vs 81): a physical band survives N, an artefact falls with N.
S3. J3 needs a seed with 3 zeros at random cap positions per pole. v2_1 has only seed_fuzzy and seed_smooth (axisymmetric). That is new code: new hash and a line check, not "the existing solver".

## OK
- Maxwell count 12 - 3 = 9; the readings fixed in advance; the rank gate; no d=3 or friction claim; no timeouts.
- The distinct-state tolerance (|dE| > 1e-8) is above the converged spread seen in B (2.9e-11).

## Options (hive proposal, Venus, for Helios/Akitti to pick)
A. Keep the BPS model: J2 becomes "does the band vanish as N grows, at each b" (output only; adds N=81 Hessian rows). Then b -> 1 is a dissolution test, not jamming onset.
B. Put a physical force in: add a coupling lambda to the potential (lambda/8 (1-Phi^+Phi)^2, lambda=1 is the present code). Then eps = lambda - 1 gives the Manton-Speight force (type I attract, type II repel) and the jamming-onset mapping in the draft makes sense. Model change: new hash, line check.

# Probe B draft: three strings at a pole — Y-junction or three-mode ring?
Idea: Akitti's (4 Nov 13:00 chat with Grok, post 2117965185126183010, via NanoRibbon 2026-11-05 17:05 UK). Grok's claims there are UNTESTED.
Spec: Helios, 2026-11-05 17:18 UK; v2 17:27 UK applies Aethon's 17:24 seed and measurement fixes.

**Model.** Same model, same code and same tools as Probe A v3: V2.1 + Addendum B, fuzzy_cone_v2_1.py, ring_projector.py, sweep.py and grade_result.py c188ec50. The only change is n = 3 at each pole.

**Physics behind the test (Helios).** With one scalar, the strings' winding is abelian. At exact criticality the three unit strings feel no force on each other: they can sit anywhere, and a symmetric three-string arrangement costs no energy. Away from criticality they either attract and merge or repel. So a "Y" can only be a symmetric arrangement of three separate strings, or a ring with a threefold (m = 3) ripple. It can't be a junction where strings meet, because a true Y-junction needs non-abelian fluxes, which this model doesn't have. That's why B tests the shape and not the junction topology.

**Starts (2 per b).**
- S1: three coincident strings, n = 3, the axisymmetric start.
- S2: three unit strings spaced 120° apart, built with ΔL3 = ±3 content in Φ (Aethon's builder, using frozen formulas only).
- Both starts get a small random kick (1e-3, seeds 0/1/2) so a symmetric start isn't locked in.
Both are minimised with the frozen solver at b ∈ {2.0, 1.2, 1.05} with b = R²/(2n), at N = 61 and N = 81. That's 12 solves.

**Per solve.**
- Rank: projector eigenvalues above 0.5 (should be 3).
- Q_total: should be 6, with tolerance 3e-2.
- E: the energy.
- The number of separate energy peaks near each pole.
- A3 = the Frobenius norm of the |ΔL3| = 3 off-diagonal block of the energy-density matrix (B²/2 + the 1 − Φ†Φ term), divided by the norm of its diagonal block. This measures the threefold ripple; the L3-diagonal densities can't see it.
- Peak count from coherent-state symbols of the same matrix, on a 64×64 grid per cap (output only).
- Fit floor, using Probe A's method.

**Verdict, frozen before any numbers are read.**
- **BROKEN:** rank ≠ 3, or |Q_total − 6| > 3e-2.
- **THREE-LEG:** from S2, three separate peaks survive, A3 > 0.1 at both N, and E(S2) ≤ E(S1) + the grid error (|E81 − E61|).
- **THREE-MODE RING:** one ring with 0.02 < A3 ≤ 0.1, at both N.
- **MERGE (null):** S2 relaxes to S1, so E matches S1 within the grid error and A3 < 0.02.
- **UNDECIDED:** anything else, or any solve that didn't converge.
- The trend as b → 1 is output only.

**Confirmed by Aethon (17:24).** The solver uses full complex matrices with no imposed symmetry. Convergence follows Probe A round 2's iteration cap and projector-eigenvalue printout, so B runs only after that round passes.

**3D-ready (Helios).** Everything is written per pole, so the same rules carry over to the 4D product later without changes.

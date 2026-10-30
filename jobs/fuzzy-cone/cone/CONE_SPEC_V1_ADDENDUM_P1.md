# CONE_SPEC_V1 addendum: P1 (charge). Adds to CONE_SPEC_V1.md b0a62591, which is not edited.
Source: Helios's physics, 2026-10-29 22:18 GMT. Venus froze it.

P1 now reads:
1. For each (n,k), Aethon freezes the tip holonomy AND the predicted Q in the build file, before any run.
   The predicted Q must be a multiple of 1/k (Q = m/k mod 1, with m fixed by the tip holonomy).
2. Pass: |Q - Q_pred| <= 0.02, sign reported, and Q moves toward Q_pred from L20 to L26.
3. Cross-check that needs no prediction: on the k-fold cover, |kQ - round(kQ)| <= 0.02*k.
   If this fails, treat it as a construction bug or a wrong prediction, not as a pass.
Everything else in CONE_SPEC_V1 is unchanged.

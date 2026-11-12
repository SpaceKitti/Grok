# ADDENDUM_F: F2 round 3 (final). Derived NC energy bound. Frozen 2026-10-30 12:45 UK, Venus. Co-sign: Helios (conditions met).

## Derivation (from the code's own energy, fuzzy_cone_v2_1.py lines 40-49)
- In the code, B lives on V_N' with weight w' = 4πR²/N'. The potential uses Φ†Φ on V_N with weight w = 4πR²/N.
- Φ is N'×N with N' = N + 2n. For k ≥ 1, Tr_N (Φ†Φ)^k = Tr_N' (ΦΦ†)^k. This gives
  Tr_N (1 − Φ†Φ)² = Tr_N' (1 − ΦΦ†)² − 2n.
- The Bogomolny completion pairs B with (1 − ΦΦ†) on V_N'. Its square uses Tr_N'(1−ΦΦ†)², which carries 2n more units than the potential the code evaluates. The 2n zero modes of ΦΦ† (the n-projector at each pole) cost potential energy in the bound but nothing in E.
- Hence E ≥ 2π|n| − (1/8)·w·2n. This is a lower bound on the energy, not an exact formula.
- With R² = θ√(N²−1)/2, the shift in the ratio is w/(8π) = R²/(2N). The prediction is

  **μ/(π|n|) = 1 − θ·√(N²−1)/(4N)**, which is about 1 − θ/4. It does not depend on n.

  Corrections are O(n/N), from w' ≠ w.
- This coefficient comes from the derivation, not from the round-2 fit (Helios's condition 1). It goes to 1 as θ→0 (Helios's condition 2).

## Valid range
- The formula is a bound that is expected to saturate only while vortices are BPS. Use it only for 0 < θ ≤ 2 with Bradlow R²/(2n) ≥ 3.8.
- At θ ≥ 4 the bound becomes ≤ 0 and is trivial, so it makes no claim there.

## Test (Aethon, ≤ 30 min, lean)
- θ ∈ {0.25, 1.5}, n ∈ {1, 2}, N ∈ {61, 101}, R = √(θ√(N²−1)/2), with the same code (63b69fbc) and nothing else changed.
- PASS needs all of:
  (a) |μ/(π|n|) − prediction| ≤ 0.02 at every point;
  (b) g_inf > 0 at the 3σ level, as in E(i);
  (c) every solve converged.
- If any of these fails, the result is UNDECIDED and goes to Akitti. This is round 3 of 3, with no refit.

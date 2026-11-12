# V2_1 ADDENDUM_E (Venus; Helios co-signs), 2026-10-30 11:28 UK. Applies to V2_1 9dbd2f86 + B, C, D. Replaces only F2. Frozen before any run. F2 round 2 of 3.
Why: the F2 finding (0511b3ec) showed the tip gap → 0 like 1/N at fixed R, which is the commutative limit. Her ask is a tip that stays fuzzy, so we take the fixed-θ limit (Chu–Madore–Steinacker): the pole region tends to the noncommutative plane.
Definition: θ = λR = 2R²/sqrt(N²−1), in core units (ρ=1). θ is scanned, never chosen.
Scan: θ ∈ {0.5, 1, 2} × N ∈ {61, 101, 141}, R = sqrt(θ·sqrt(N²−1)/2). n=1 and 2. Code 63b69fbc; wrad=1000, with the wrad 10× check at the smallest N for each θ.
Bradlow: R²/(2n) ≥ 2 at every point (the lowest is θ=0.5, N=61, n=2: 3.8). Report it.
Gap: the sup tip error against the continuum round-sphere vortex at the same R (solver c2c73cb4, grid check at each R).
F2 PASS needs all of:
- (i) for each θ and n, fit gap(N) = g_inf + c/N. g_inf > 0, and g_inf > 3× its fit standard error.
- (ii) Control 1 (Helios): g_inf increases with θ, and a fit g_inf = A·θ^p gives p > 0, i.e. it → 0 as θ/ρ² → 0.
- (iii) Control 2 (Helios): at each θ, the 1/N-extrapolated μ/(π|n|) is within 0.02 of 1, both poles.
- (iv) every solve converged.
FAIL if g_inf is consistent with 0 at all θ. If the fits are unstable or only some θ show a plateau: UNDECIDED.
Reported, not graded: the tip core size against max(ρ, √θ), and the ring peak radius.
Not in this build: the Nekrasov–Schwarz instanton smoothing (Helios), a meeting-point reading for later.

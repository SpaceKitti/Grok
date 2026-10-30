# FUZZY_CONE_SPEC_V1 (Venus, physics from Helios's two outlines 2026-10-30). Frozen before any build. [hive proposal, untested]
Object: her picture is a 2D surface (S^2) with a deficit cone at each pole. The tip cross-sections are circles, so the fuzzy-native tip is the noncommutative (NC) plane quotiented to a cone, NOT a stack of fuzzy S^2 shells.
Milling note on the shell-stack outline: a stack of fuzzy S^2 shells is a cone over S^2, i.e. a 3D cone, and the monopole projector is a 3D object. That build is kept OPEN as the 3D comparison (it is the natural home of the instanton on a cone over CP^2 / S^3), not the main build. The formula N(r)^2-1=(2 alpha r/lambda)^2 is correct (lambda = 2R/sqrt(N^2-1) with R = alpha r). Note that alpha then only rescales r unless the link matrices carry the radial spacing lambda/(2 alpha).
Build (main):
B1. Hilbert space: oscillator states |m>, with angular momentum restricted to l in (1/alpha)Z>=0 (alpha=1/k gives the Z_k orbifold, keeping m = 0 mod k). Truncate at m_max = M, with M in {64,128,256}.
B2. Field: a matrix Phi and gauge field in the Fock basis. Energy: the self-dual NC abelian-Higgs functional (same normalisation as cone_v1_4b e0bb1cd9, operator form). The minimisation runs over matrices; no continuum profile appears anywhere.
B3. Seed: shift operator S_n on the cone's restricted spectrum, Phi = v S_n.
B4. Same cones as V1_4: alpha in {0.9, 0.75, 0.5, 1/3}, n=1,2, plus alpha=2 as a side comparison. Fuzziness lambda in {lambda0, lambda0/2}.
Pass rules:
P-F1 (control): as lambda -> 0 at fixed alpha, the symbol of Phi outside a few lambda approaches the V1_4b continuum solution within 1% (sup norm on r in [5 lambda, 3 rho]).
P-F2 (fuzzy tip survives): at lambda0, the tip action within r <= 3 lambda differs from the continuum value by more than 5%, and the difference changes when lambda is halved. If the tip matches the classical vortex, the row FAILS.
P-F3 (charge): Q = rank(1 - S S^dagger) is read in the tip block only. It is a build check (it must equal n exactly; any other value is a construction bug), NOT a test of the angle.
P-F4 (angle test, the real one): p is read from the decay of <m|Phi|m+n'> over the lowest restricted states (the fuzzy spectrum), fitted for log|Phi_m| vs log m on m in [1, 8]. Prediction: p = |n|/alpha. Pass within 5%, and stable to 2% from M=128 to 256. Otherwise UNDECIDED.
P-F5: E/(pi|n|) -> 1 as lambda -> 0.
Not graded: the tension route (separate spec, now unblocked by the 4b fix).
Refit V1_5 (a3e41946): accepted. Nine points in the coarse window is enough for the 2-parameter fit. alpha=1/3, n=2 stays UNDECIDED.

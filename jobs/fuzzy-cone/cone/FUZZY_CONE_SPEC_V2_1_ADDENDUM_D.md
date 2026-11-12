# V2_1 ADDENDUM_D (Venus), 2026-10-30 11:10 UK. Applies to V2_1 9dbd2f86 + B 4e265cbd + C 86b8052f. Replaces only F4. Frozen before any rerun. F4 round 2 of 3.
F4: per-pole μ/(π|n|), n=1 and 2, both poles, on the new set N ∈ {31, 51, 71, 101}. Code 63b69fbc unchanged; wrad=1000 unless the (c) rerun says otherwise.
Fit μ(N) = μ_inf + b/N by least squares over all 4 N.
PASS needs all of:
- |μ_inf − 1| ≤ 0.02;
- max fit residual ≤ 0.002;
- a fit with an added d/N² term moves μ_inf by ≤ 0.01;
- north and south agree to 0.005 at each N;
- every solve converged.
FAIL is anything else. If the fit checks (residual or stability) fail while μ_inf is in band, the result is UNDECIDED, not PASS.
Report μ_inf, b and both fits per n and pole. Old N values (21/41/81) are not used in this grade.

# pairA-qg-radial — RESULTS

**Signed off 2026-09-26:** Venus (maths) and Helios (physics).

Does a standard gravity family give a radial equation whose root lands on Pair A's tip, with no Pair A input and no tuned scale? No folders loaded. Conventions: Planck units G = c = ħ = 4πε₀ = 1; each free scale is set to 1 in its own units (the Liouville V amplitude is set to −1 so that a real horizon exists) [by construction].

Firewall: every input carries a fixing rule (rule problems: 0), and the forbidden-input scan found **0** hits against 102 Pair A numbers and combinations (re-scan after computing the extremal Q: 0 hits) [computed]. The target appears only in match.py, which is imported after this section was built.

**Global caveat:** eps is a dimensionless drive parameter; every gravity root is a length, so the comparison needs a unit (Planck units here, itself a convention). Even an exact hit would be [by construction: unit choice].

## Raw roots (computed before any matching)

### F1 Einstein–Maxwell–Λ

Equation: f(r) = `-Lambda*r**2/3 - 2*M/r + Q**2/r**2 + 1` = 0, i.e. r² f = `-Lambda*r**4/3 - 2*M*r + Q**2 + r**2` = 0 [standard].
Extremal / Nariai conditions: f = f' = 0  <=>  Lambda r^4 - r^2 + Q^2 = 0 and M = r - (2/3) Lambda r^3 (cold branch: r^2 = (1 - sqrt(1 - 4 Lambda Q^2))/(2 Lambda); charged-Nariai branch: '+' sign; Q = 0 Nariai: 9 Lambda M^2 = 1, r_N = 1/sqrt(Lambda)) [standard + identity].

| input | value | fixing rule |
|---|---|---|
| G | 1.0 | Planck units |
| c | 1.0 | Planck units |
| hbar | 1.0 | Planck units |
| 4pi_eps0 | 1.0 | Planck units |
| LAMBDA | 2.88813701678764e-122 | standard value from Planck 2018 results VI (A&A 641, A6): Lambda = 1.1056e-52 m^-2, times l_P^2 (CODATA 2018 l_P = 1.616255e-35 m) |
| F1_M | 1.0 | free |
| F1_Q | computed: 1.0 | extremality |

Free scales: **1** (each 'free' set to its neutral convention).

| root | multiplicity | physical | label | note |
|---|---|---|---|---|
| 1.0 | 2 | yes | extremal horizon (inner = outer, cold) |  |
| -1.01918196725e+61 | 1 | no | r < 0 root of r^2 f |  |
| 1.01918196725e+61 | 1 | yes | cosmological horizon |  |

- Checks: polynomial relative residual 6.39e-402; deflation remainders 1.07e-401; cold-branch formula vs extremal root 3.16e-281 [computed].
- Extremal Q = 1.0 (from M and Λ). Nariai at this Λ: Q = 0 needs M_N = 1/(3√Λ) = 1.96142e+60, r_N = 1/√Λ = 5.88425e+60; charged Nariai for this Q has r_N = 5.88425e+60 with **M = Q²/r_N + Λr_N³/3 = 1.96142e+60** (≈ r_N/3 = 1.96142e+60; cross-check r_N − (2/3)Λr_N³ = 1.96142e+60). Not realised at M = 1 [computed].
- Helios: at r ~ 1 Planck length, Λ's effect is ~1e-122, so F1 is Reissner–Nordström in practice (extremal Q = M). The only real scale is M, which is free, so PARTIAL [by construction]. Planck 2018 Λ is the honest external choice [standard].

### F2 Stelle / quadratic gravity

Convention (Lu-Perkins-Pope-Stelle 2015): L = R - beta_W C^2 + alpha R^2 in G = 1 units, massive spin-2 m2 = 1/sqrt(2 beta_W) (beta_W > 0 non-tachyonic). The spec's '+beta C^2' is beta = -beta_W. Static black holes have R = 0, so alpha drops out [standard].
Equation used: linearised static metric h(r) = `-2*M/r + 4*M*exp(-m_2*r)/(3*r) + 1` = 0 (Stelle 1978, α = 0), m₂ = 1/√(2β_W) [standard]. **A full numerical LPPS shooting solve was not done**: the non-Schwarzschild branch is represented by its characteristic radii (the Yukawa radius 1/m₂ and the bifurcation radius 0.876/m₂) and by the zeros of the linearised h. Zeros: r = 2M + W_k(z)/m₂, z = −(4m₂M/3)e^{−2m₂M} = -0.2292126554 [identity], with infinitely many complex branches (k = −3…3 listed).
Whether β in mass-scale units is theory-fixed: **free** (a coupling of the theory; nothing in the theory fixes it) [standard].
Dimensional argument [identity]: with G = 1 and α = 0 the only scales are M (a length) and m₂ = 1/√(2β_W) (an inverse length), so r_h = g(m₂M)/m₂. Also, r = 2M solves the full Stelle equations for every β_W (Ricci-flat metrics solve quadratic gravity) [standard], so M alone can place a root anywhere, and a full LPPS solve could only reproduce PARTIAL [by construction]. The LPPS branch only exists near m₂r_h ≲ 0.876 [standard].

| input | value | fixing rule |
|---|---|---|
| G | 1.0 | Planck units |
| c | 1.0 | Planck units |
| hbar | 1.0 | Planck units |
| 4pi_eps0 | 1.0 | Planck units |
| F2_BETA_W | 1.0 | free |
| F2_M | 1.0 | free |
| F2_ALPHA_R2 | 0.0 | standard value from Lu-Perkins-Pope-Stelle 2015 (PRL 114, 171601): static black holes have R = 0, so the R^2 coupling does not enter |
| F2_GL | 0.876 | standard value from Gregory-Laflamme 1993 (PRL 70, 2837) / Lu-Perkins-Pope-Stelle 2015: Schwarzschild static zero mode (non-Schwarzschild branch bifurcation) at m2 r_h ~ 0.876 |

Free scales: **2** (each 'free' set to its neutral convention).

| root | multiplicity | physical | label | note |
|---|---|---|---|---|
| 1.41421356237 | 1 | yes | Yukawa radius 1/m2 = sqrt(2 beta_W) (linearised scale, not a zero of h) | characteristic radius |
| 1.23885108064 | 1 | yes | bifurcation radius r_h = 0.876/m2 (non-Schwarzschild branch meets Schwarzschild) | characteristic radius |
| -3.86052975474 - 19.58171791i | 1 | no | zero of linearised h (Lambert W branch k = -3) | complex |
| -3.06307098778 - 10.4702224992i | 1 | no | zero of linearised h (Lambert W branch k = -2) | complex |
| -1.26771255245 | 1 | no | zero of linearised h (Lambert W branch k = -1) |  |
| -3.06307098778 + 10.4702224992i | 1 | no | zero of linearised h (Lambert W branch k = 1) | complex |
| -3.86052975474 + 19.58171791i | 1 | no | zero of linearised h (Lambert W branch k = 2) | complex |
| -4.36832542839 + 28.5685627005i | 1 | no | zero of linearised h (Lambert W branch k = 3) | complex |

Linearised zero, listed separately (not on a par with the roots above):

| root | multiplicity | physical | label | note |
|---|---|---|---|---|
| 1.5564173849 | 1 | yes | zero of linearised h (Lambert W branch k = 0) | [indicative only; outside linear validity] (m2 r = 1.1) |

- Checks: max |h| at the Lambert-W zeros 7.13e-401 [computed]. Caveat: the linearised h is not reliable at r ~ 2M (strong field); its zero is indicative only.

### F3 2D dilaton gravity (Killing norm ξ = 0)

General solution: ξ(X) = e^{Q(X)}(w(X) − C), with Q = ∫U dX and w = −2∫e^{Q}V dX, for S = ∫√−g [XR − U(X)(∇X)² − 2V(X)] [standard form, Grumiller–Kummer–Vassilevich 2002 review; normalisation by construction so that SRG gives 1 − 2C/r].

#### F3a dilaton: SRG

U = `-1/(2*X)`, V = `-1/4` (parameters: 0 in U, 0 in V, plus the mass Casimir C). Coordinate: X = r^2/4.
ξ(X) = `-C/sqrt(X) + 1`; in r: `-2*C/Abs(r) + 1` [computed]. |ξ| at the real root: 0.0e+00.
Root set by: C (= M) only.

| input | value | fixing rule |
|---|---|---|
| G | 1.0 | Planck units |
| c | 1.0 | Planck units |
| hbar | 1.0 | Planck units |
| 4pi_eps0 | 1.0 | Planck units |
| F3_SRG_C | 1.0 | free |

Free scales: **1** (each 'free' set to its neutral convention).

| root | multiplicity | physical | label | note |
|---|---|---|---|---|
| 2.0 | 1 | yes | horizon r_h = 2C (X_h = C^2) |  |

#### F3b dilaton: CGHS

U = `-1/X`, V = `-2*X*lambda**2` (parameters: 0 in U, 1 in V, plus the mass Casimir C). Coordinate: X = exp(2 lambda r) (linear dilaton).
ξ(X) = `-C/X + 4*lambda**2` [computed]. |ξ| at the real root: 0.0e+00.
Root set by: λ and C (X_h = C/(4λ²)).

| input | value | fixing rule |
|---|---|---|
| G | 1.0 | Planck units |
| c | 1.0 | Planck units |
| hbar | 1.0 | Planck units |
| 4pi_eps0 | 1.0 | Planck units |
| F3_CGHS_LAMBDA | 1.0 | free |
| F3_CGHS_C | 1.0 | free |

Free scales: **2** (each 'free' set to its neutral convention).

| root | multiplicity | physical | label | note |
|---|---|---|---|---|
| -0.69314718056 | 1 | yes | horizon, r = ln(X_h)/(2 lambda), X_h = C/(4 lambda^2) |  |
| -0.69314718056 - 6.28318530718i | 1 | no | log-branch copy k = -2 (same X_h; coordinate artefact) | complex |
| -0.69314718056 - 3.14159265359i | 1 | no | log-branch copy k = -1 (same X_h; coordinate artefact) | complex |
| -0.69314718056 + 3.14159265359i | 1 | no | log-branch copy k = 1 (same X_h; coordinate artefact) | complex |
| -0.69314718056 + 6.28318530718i | 1 | no | log-branch copy k = 2 (same X_h; coordinate artefact) | complex |

#### F3c dilaton: Liouville

U = `p`, V = `q*exp(X*s)` (parameters: 1 in U, 2 in V, plus the mass Casimir C). Coordinate: X itself (no areal radius).
ξ(X) = `Piecewise(((-C*(p + s) - 2*q*exp(X*(p + s)))*exp(X*p)/(p + s), Ne(p, -s)), ((-C - 2*X*q)*exp(X*p), True))` [computed]. |ξ| at the real root: 0.0e+00.
Root set by: p, q, s and C (e^{(p+s)X_h} = −C(p+s)/(2q)). V amplitude −1: the same sign as SRG and CGHS in this action convention, and it allows a real Killing horizon; a consistent convention [by construction]. Caveat: X is the dilaton, not an areal radius, so comparing X_h with eps_EP depends even more on the coordinate.

| input | value | fixing rule |
|---|---|---|
| G | 1.0 | Planck units |
| c | 1.0 | Planck units |
| hbar | 1.0 | Planck units |
| 4pi_eps0 | 1.0 | Planck units |
| F3_LIOU_P | 1.0 | free |
| F3_LIOU_Q | -1.0 | free |
| F3_LIOU_S | 1.0 | free |
| F3_LIOU_C | 1.0 | free |

Free scales: **4** (each 'free' set to its neutral convention).

| root | multiplicity | physical | label | note |
|---|---|---|---|---|
| 0.0 - 6.28318530718i | 1 | no | zero of xi(X), branch k = -2 | complex (xi is entire in X: infinitely many) |
| 0.0 - 3.14159265359i | 1 | no | zero of xi(X), branch k = -1 | complex (xi is entire in X: infinitely many) |
| 0.0 | 1 | yes | zero of xi(X), branch k = 0 |  |
| 0.0 + 3.14159265359i | 1 | no | zero of xi(X), branch k = 1 | complex (xi is entire in X: infinitely many) |
| 0.0 + 6.28318530718i | 1 | no | zero of xi(X), branch k = 2 | complex (xi is entire in X: infinitely many) |

### F4 R1-like product chart AdS₂ × S² (Einstein–Maxwell–Λ, ε as the radial coordinate)

Ansatz: ds² = −h(ε)dt² + dε²/h(ε) + r(ε)² dΩ², electric field F_tε = Q/r² (Maxwell solved). Equations E^μ_ν = G^μ_ν + Λδ^μ_ν − 8πT^μ_ν = 0 [standard].
- Normalisation check: RNdS (r = ε, h = f) gives residuals [0, 0, 0] [computed].
- E^t_t − E^ε_ε = G^t_t − G^ε_ε = `2*h(epsilon)*Derivative(r(epsilon), (epsilon, 2))/r(epsilon)` [computed]. G^t_t − G^eps_eps = +2h r''/r (mostly-plus) [sign corrected; r'' = 0 unaffected], so **r'' = 0** along ε: r = αε + r₀. α ≠ 0 is F1 again (r = ε after a shift). r = const [by construction of the AdS2xS2 ansatz; alpha != 0 is F1].
- Product (r = r₀): `Lambda + Q**2/r_0**4 - 1/r_0**2` = 0 and `Lambda - Q**2/r_0**4 + Derivative(h(epsilon), (epsilon, 2))/2` = 0, so Λr₀⁴ − r₀² + Q² = 0 (the same quartic as F1's extremal condition [identity]) and h'' = 2(Q²/r₀⁴ − Λ) = 2/l². General solution h = ε²/l² + c₁ε + c₀. After the ε-shift isometry, h = (ε² − ε_h²)/l², with **ε_h a free integration constant** (the AdS₂ black-hole temperature) [computed + standard].
- r(ε) has no zeros at all: it is constant. The zeros of h sit at ±ε_h, a ± pair by construction, but their location is not fixed by the field equations. l² = 1.0 on the AdS₂ branch [computed].
- **Rescaling check (sympy):** under ε = ε_h u, t = τ/ε_h the metric becomes g_ττ = `(1 - u**2)/l**2`, g_uu = `l**2/(u**2 - 1)`, F_τu = `E_0`. ε_h removed: **True**. Zeros of h at u = [-1, 1] [computed].

| input | value | fixing rule |
|---|---|---|
| G | 1.0 | Planck units |
| c | 1.0 | Planck units |
| hbar | 1.0 | Planck units |
| 4pi_eps0 | 1.0 | Planck units |
| LAMBDA | 2.88813701678764e-122 | standard value from Planck 2018 results VI (A&A 641, A6): Lambda = 1.1056e-52 m^-2, times l_P^2 (CODATA 2018 l_P = 1.616255e-35 m) |
| F4_Q | 1.0 | free |
| F4_EPS_H | 1.0 | free |

Free scales: **2** (each 'free' set to its neutral convention).

r₀ roots:

| root | multiplicity | physical | label | note |
|---|---|---|---|---|
| 1.0 | 1 | yes | r0 root: AdS2 x S2 (Bertotti-Robinson-like), 1/l^2 = 1.0 |  |
| -1.0 | 1 | no | r0 root: AdS2 x S2 (Bertotti-Robinson-like), 1/l^2 = 1.0 | r0 < 0 |
| 5.88424983147e+60 | 1 | no | r0 root: dS2 x S2 (charged Nariai), 1/l^2 = -2.888137e-122 |  |
| -5.88424983147e+60 | 1 | no | r0 root: dS2 x S2 (charged Nariai), 1/l^2 = -2.888137e-122 | r0 < 0 |

zeros of h(ε) (neutral ε_h = 1):

| root | multiplicity | physical | label | note |
|---|---|---|---|---|
| 1.0 | 1 | yes | zero of h(eps) = (eps^2 - eps_h^2)/l^2 at +eps_h (eps_h = integration constant, neutral 1) | location = integration constant |
| -1.0 | 1 | yes | zero of h(eps) at -eps_h | location = integration constant |

## Match test (match.py, run after the raw roots above)

r = eps_EP is a match test, not an input. Relative error of the closest physical root to 0.51368066 (taken from match.py), with the free scales at their neutral convention. Hypothetical values that WOULD hit are information only; nothing was tuned.

| family | free scales | closest physical root | rel. error | closest over all roots | ± pair? | L6-type r² ≈ 0.453 root? | tag | grade |
|---|---|---|---|---|---|---|---|---|
| F1 Einstein-Maxwell-Lambda | 1 | 1.0 | 0.9467 | 1.0 (0.947) | only r > 0 (r^2 f has the odd term -2Mr; a +- pair would need M = 0) | no | [by construction] | **PARTIAL [by construction]** |
| F2 Stelle (quadratic gravity) | 2 | 1.238851081 | 1.412 | 1.2388511 (1.41) | only r > 0 | no | [by construction] | **PARTIAL [by construction]** |
| F3a dilaton: SRG | 1 | 2.0 | 2.893 | 2.0 (2.89) | only r > 0 | no | [by construction] | **PARTIAL [by construction]** |
| F3b dilaton: CGHS | 2 | -0.6931471806 | 2.349 | -0.69314718 (2.35) | single real root (linear-dilaton r on the whole line; no +- pair) | no | [by construction] | **PARTIAL [by construction]** |
| F3c dilaton: Liouville | 4 | 0.0 | 1.0 | 0.0 (1.0) | single real root in X; no +- pair | no | [by construction] | **PARTIAL [by construction]** |
| F4 AdS2 x S2 product chart | 2 | 1.0 | 0.9467 | 1.0 (0.947) | +- pair present (h = (eps^2 - eps_h^2)/l^2 after the eps-shift isometry) [by construction of the AdS2 black-hole chart] | no | [computed] | **MISSING** |

### Hypothetical placements (information only, not tuned) [PARTIAL, by construction]

- **F1 Einstein-Maxwell-Lambda:** M = 0.51368066 (with Q by extremality, Q = 0.51368066) would put the extremal horizon at the target: one free scale placed [PARTIAL, by construction; hypothetical, not tuned].
- **F2 Stelle (quadratic gravity):** beta_W = 0.1319339102 would put the Yukawa radius 1/m2 at the target; beta_W = 0.1719286376 would put the bifurcation radius there; the linearised-horizon zero depends on beta_W and M together (a declared choice) [PARTIAL, by construction; hypothetical, not tuned].
- **F3a dilaton: SRG:** C = M = 0.25684033 would put r_h = 2M at the target: one free scale [PARTIAL, by construction; hypothetical, not tuned].
- **F3b dilaton: CGHS:** with lambda = 1 declared, C = 4 lambda^2 exp(2 lambda r_h) = 11.17473784 would put r_h at the target (two free scales: a declared choice) [PARTIAL, by construction; hypothetical, not tuned].
- **F3c dilaton: Liouville:** with p = s = 1, q = -1 declared, C = -2 q exp((p+s) X_h)/(p+s) = 2.793684461 would put X_h at the target (four free parameters: declared choices) [PARTIAL, by construction; hypothetical, not tuned].
- **F4 AdS2 x S2 product chart:** F4: the +-eps_h pair exists by construction of the AdS2 black-hole chart, but eps_h is removable by a coordinate rescaling (diffeomorphism) eps = eps_h u, t = tau/eps_h [standard], so gravity cannot fix its location: MISSING. Only eps_h>0 (black-hole patch) vs eps_h=0 (Poincare patch) is physical; the pair always sits at u = +-1 in the chart's own units, so matching it to +-eps_EP is exactly the unit choice in the global caveat. [sympy check: eps_h removed = True]

## Extra roots (logged, never hidden)

- F1: besides the extremal (double) horizon, a cosmological horizon at r ≈ √(3/Λ) ~ 1e61 and a negative root of r²f at about −1e61 (unphysical). No Nariai root is realised at M = 1, and nothing near r² ≈ 0.453. Pair A has a single ± pair; F1 has three distinct roots (four with multiplicity) and no ± pair.
- F2: two characteristic radii, plus the linearised-h zeros: one physical real zero (k = 0), one negative real zero (k = −1, unphysical), and infinitely many complex Lambert-W zeros (k = ±1, ±2, …; seven branches listed).
- F3: SRG has one root. CGHS has one root in X; the complex r-copies are log-branch artefacts of X = e^{2λr}. Liouville has one real root and infinitely many complex ones, X_k = X_0 + 2πik/(p+s).
- F4: four r₀ roots: one physical AdS₂ × S² (r₀ = +1), its negative (unphysical), and a charged-Nariai dS₂ × S² pair at |r₀| ≈ 1/√Λ (dS₂, not AdS₂: the extra Nariai-type root, at ~6e60, not at 0.453). h(ε) has the ± pair ±ε_h.

- F2's linearised zero (listed separately) has relative error 2.03 (r = 1.5564174) [indicative only; outside linear validity].

## Side observations (notes only; not inputs)

- π² note: a = π²/80 = 0.123370055 and b = π²/20 = 0.4934802201 match the given a = 0.12337 and b = 0.49348 to all 5 digits given (relative differences 4.5e-7 and 4.5e-7), and b = 4a exactly (4 × 0.12337 = 0.49348). So eps_EP = (b − a)/(2|v|) = 3π²/(160|v|) (relative difference from the match target: 4.5e-7, computed after matching). A ratio of 4 with π² fits the n = 1 and n = 2 decay rates of a diffusing box (γ_n ~ n²π²) [confirmed by Akitti 2026-09-26: Dirichlet slab, eta=0.05, L=2, n=1,2 modes]. Not used anywhere as an input.
- v = <sine_1|x|sine_2> on the L=2 Dirichlet slab = -16L/(9 pi^2) = -32/(9 pi^2) [confirmed by Akitti 2026-09-26; post-hoc]; the whole Pair A triple (a, b, v) is the 2-mode Galerkin of A = eps x + i eta d_xx; eps_EP = 27 pi^4/5120 is fixed by eta, L only. Sympy check [computed]: (2/L)∫₀^L x sin(πx/L) sin(2πx/L) dx = `-16*L/(9*pi**2)` (equals −16L/(9π²): True); with x − L/2: `-16*L/(9*pi**2)`; at L = 2: -0.360253097395 (|value| vs 0.360253: relative difference 2.7e-07). 27π⁴/5120 = 0.513680753500 (relative difference from the match target: 1.8e-7; identity check (3π²/80)/(2·32/(9π²)) − 27π⁴/5120 = 0).
- General form [identity, given the 2-mode Galerkin]: eps_EP = kappa/|v| = (3 eta pi^2/(2L^2)) / (16L/(9 pi^2)) = 27 eta pi^4/(32 L^3), which gives 27 pi^4/5120 at eta = 0.05, L = 2. Sympy [computed]: κ = (b − a)/2 = 3ηπ²/(2L²): True; κ/|v| = `27*pi**4*eta/(32*L**3)`, equals 27ηπ⁴/(32L³): True; at η = 1/20, L = 2 equals 27π⁴/5120: True. The tip is where the linear drive eps x just matches the diffusion contrast between the two modes; it moves in proportion to eta and falls as 1/L^3.
- Post-hoc (2026-09-26): eps_EP = 3pi^2/(160|v|) is an MHD box number (eta, L, v); gravity families with generic couplings cannot produce it without feeding the box in, consistent with NOT HAVE. The source of v is still open.

- Footnote: |v| = 1/2 (8/(3pi))^2 [numerical coincidence: holds only at L = 2, where 16L/(9 pi^2) = 1/2 (8/(3pi))^2; on L = pi the real coupling is 16/(9 pi)]. Sympy: ½(8/(3π))² − 32/(9π²) = 0; 16L/(9π²) at L = π = `16/(9*pi)` [computed].

## Summary

- F1 Einstein-Maxwell-Lambda: **PARTIAL [by construction]**
- F2 Stelle (quadratic gravity): **PARTIAL [by construction]**
- F3a dilaton: SRG: **PARTIAL [by construction]**
- F3b dilaton: CGHS: **PARTIAL [by construction]**
- F3c dilaton: Liouville: **PARTIAL [by construction]**
- F4 AdS2 x S2 product chart: **MISSING**

**Overall: NOT HAVE**: no family is HAVE; the best outcome is PARTIAL [by construction] (one free scale can always be placed), and F4 is MISSING (the ±eps_h pair exists by construction, but eps_h is removable by a coordinate rescaling, so gravity cannot fix its location) [computed].

## Conventions chosen

- Planck units G = c = ħ = 4πε₀ = 1; Λ from Planck 2018 times l_P².
- F1: Q fixed by extremality (cold branch) for the given M and Λ; M free = 1.
- F2: LPPS sign convention (L = R − β_W C² + αR², m₂ = 1/√(2β_W)); the spec's +βC² is β = −β_W. α drops out for static black holes. Linearised metric used instead of a full shooting solve.
- F3: GKV-type action and general solution; U, V normalised so that SRG gives 1 − 2C/r; CGHS radial coordinate from X = e^{2λr}; Liouville V amplitude −1.
- F4: ε_h (integration constant) set to 1 as the neutral value; the chart's ε origin fixed by the shift isometry.

## Final lines

RADIAL EQUATION FROM GRAVITY: HAVE only if some family is HAVE with no tuned scale.
r = eps_EP is a match test, not an input.
No claim that Pair A is a quantum-gravity result, that it has a JT dual, or that it is an Einstein solution. The standard solutions used here are textbook solutions of their own theories; matching or not matching a number says nothing about Pair A's physics.
gravity-side is hive language [hive-interpretation]


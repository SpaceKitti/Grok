# CONE_SPEC_V1 — Akitti's fuzzy cone with an instanton attached, built cone-first (Venus, 2026-10-29 ~22:25 GMT)
FROZEN before any code or results. Never edited; changes go in a new file (V1_1 ...). Statics only, first.
History: the A/B/C seed work is stopped. SEED_AB_SPEC_V1_2.md (d361b4b9) stays frozen as history.
Working rule (Akitti): study the object itself first; textbook physics is a check only.
Tags: [Akitti] hers · [paper] · [standard] textbook check · [hive proposal] = UNCHECKED/GUESS · OPEN = kept, not dropped · [Venus-checked] = small algebra done here.

## 0. What this rests on (one woven source, not ranked)
Her notes and posts:
- X 2110455808366633013 (14 Oct). The post text is only an emoji. Its 4 images are chat screenshots (read today; image 1 viewed directly):
  "the cone singularity you found at the poles ... a point where the configuration can't be continuously deformed back to vacuum";
  "your cone singularity sitting at the poles of the sphere is the geometric signature of an instanton trying to form";
  "look at how the cone angle relates to the instanton number. If the singularity's opening angle matches a known instanton charge,
  you've found a real connection". Remaining images (ADHM / Atiyah–Hitchin, Groisser, conical-deficit tension paper) are taken from
  Aethon's SEED_A_DRAFT_V1 §1 reading, not re-viewed by me.
- X 2110480278460465169 (14 Oct). The text is only links. Infographic viewed directly: sphere with cone tips at BOTH poles, angles
  2pi - delta_±; "cone singularity = topological defect"; "cone angle encodes instanton number"; "deficit angles from stacked strings
  (tension or strain) -> force-balance equation"; "opening angle = 2pi - delta, instanton charge k in Z, match => real self-dual
  connection"; ADHM -> Atiyah–Hitchin; Groisser 1990 (vertex = small-instanton limit); Bakas (Toda); "delta = delta_t (tension) + delta_s
  (strain); force balance holds for combined source".
- X 2108616007984046199 (9 Oct): "stacked moire blanket" (image: stacked hopfion cells). Text read.
- X 2108946150795481569 (10 Oct): long note on the rolling-tachyon array, the c=1 dual H = p^2/2 - q^2/2 + mu, and Krylov in the
  synthetic layer (text read via the x tools; the quoted post 2108919688851812480 was not fetched).
- AKITTI_FRAMEWORK_2026-10-08: transverse cone ds^2 = dr^2 + alpha^2 r^2 dphi^2 for r > r_c, 0 < alpha <= 1; curvature at the tip
  int R dA = 2pi(1-alpha); FINITE core r <= r_c, C^1 matching; alpha = 1 - 4G mu (string tension).
- CONE_TIP_NOTE.md: "the cone is a clue" [Akitti]. The rest of that note is Helios's: excess vs deficit, replica/orbifold readings.
- AKITTI_POSTS_OCT22-28.md: "finite N automatically smears any classical cone tip" (l. 1954, 1978); the tip is resolved by fuzziness;
  the cone singularity is a primary simulation target (2114179948600566231).
- HIVE_CONSTRUCTIONS.md, Meeting points (29 Oct): GoldbergHexa pentagons x spherical-crystal scars; fuzzy cone tip x ADK.
Papers / maths:
- Almheiri–Dodelson–Komargodski arXiv:2610.31610 (abstract fetched today): the bulk-cone singularity "is smoothed out at finite G_N ...
  a consequence of the fuzziness of the bulk solution in quantum gravity". Their "bulk cone" is a light-ray singularity in a
  correlator; the AdS3 colliding shocks are conical defects. Link to her cone: meeting point, OPEN (not identical objects).
- GoldbergHexa: 12 pentagons as soft cones, alpha = 5/6 each. [Venus-checked] 12 x 2pi(1 - 5/6) = 4pi = 2pi·chi(S^2), so Gauss–Bonnet closes.
  The "k = 6/5 tip link" (exponent 1/alpha = 6/5, §2) is a [hive proposal].
- Fuzzy sphere / fuzzy projectors (hep-th/9811169, 0905.2338): fuzzy-native building blocks. Coherent-state pole projector
  P_0 = |j,j><j,j| with symbol width 2R/sqrt(N+1) (V1_2 §8e) [hive proposal as tip].

Flagged departures from her notes (standard assumptions brought in):
D1 Pure Yang–Mills / abelian-Higgs dynamics on the tip; she names no Lagrangian. [standard]
D2 Cone realised on the fuzzy sphere as a Z_k orbifold cap (alpha = 1/k, existing Model k-twist). Her alpha is continuous and set by tension; integer 1/k is only a subset. GoldbergHexa's 5/6 is NOT of this form (OPEN-C2).
D3 alpha FIXED as input (geometry not dynamical); her alpha = 1 - 4G mu with force balance is not solved here (OPEN-A5).
D4 Hive chart/lattice conventions (lambda = 2R/sqrt(N^2-1), a = rho/3, x = (lambda/rho)^2, Hermitian A with U ~ exp(-i a A)).
D5 Round sphere away from the tips.
Any switch from her construction to a published one is flagged to Akitti first.

## 1. The object (cone-first)
A fuzzy sphere S^2_F (N = 2j+1) whose pole is a cone of total angle 2pi·alpha (deficit delta = 2pi(1-alpha)), with a charge-n winding
attached AT the tip. In her words, "an instanton trying to form" at the cone. The tip is fuzzy by default: no point singularity, and the smearing scale is set by N.
Default: the north tip carries the object, and the south tip (if present, D2) is its mirror. Her infographic has both tips. Two-tip runs are a side variant (OPEN-C3).

## 2. Central question (former A3): cone angle <-> charge
Checks (Helios's claim, verified by Venus, cone_algebra_check.py b9486389):
- Metric dr^2 + alpha^2 r^2 dphi^2, winding phi ~ f(r) e^{i n phi}. The regular harmonic solution is f = r^{|n|/alpha} (Laplace residual 0).
  Energy density = 2 n^2 r^{2|n|/alpha - 2}/alpha^2: finite at r -> 0 for every n != 0 and alpha <= 1. ✓ (Helios's "theta -> alpha theta"
  means proper angle = alpha·phi; the claim holds in that reading.)
- NEW [Venus-checked]: the core gradient energy for r < 1 is EXACTLY |n|, independent of alpha (2D Dirichlet energy is conformally
  invariant). So the cone angle is INVISIBLE in the total energy of a harmonic winding and shows up only in the tip EXPONENT |n|/alpha.
  Any "angle encodes number" readout must therefore be read off the tip profile, not the action alone.
- Gauss–Bonnet fixes the total deficit by topology (4pi on S^2) whatever the charge. So the angle cannot encode n through topology
  alone. Any link must come through tension: delta_T = 8 pi G mu_n, with mu_n = |n| mu_1 at critical coupling [standard; GR reference]
  -> delta linear in |n|. [hive proposal, UNCHECKED]
Frozen predictions to test (statics):
- PRED-1 (exponent law): the tip profile exponent is p = |n|/alpha, measured outside the fuzzy width w_N = 2R/sqrt(N+1) and inside r_c.
- PRED-2 (fuzzy tip): inside w_N the exponent law is smeared and the density stays finite and smooth at every N. The sharp tip (side only) shows the bare law down to the lattice.
- PRED-3 (charge on the cone): Q is fixed by the construction and frozen per (n, k) before results. On a Z_k orbifold, fractional values
  in Z/k are allowed [standard: orbifold instantons]. Q_pred is written into Aethon's build file and checked by Venus before any run.
- PRED-4 (angle readout) [hive proposal]: at fixed n, the action is alpha-independent at leading order (conformal check above), and p carries alpha.
  "Match" in her sense = measured p equal to |n|/alpha. The tension-based delta(n) stays OPEN-A5 (needs dynamical geometry).

## 3. Seeds (statics first)
Default fuzzy tip [hive proposal]: winding built from fuzzy-native objects only: the monopole/coherent-state projectors on the Z_k cap
(P_0 = |j,j><j,j| as the tip-localized block, plus the P_± family), with plane/tip-angle dependence e^{i n phi}. NO sampled continuum
field on S^2_F (R0). Profile f(r) inside r_c with C^1 matching to r^{|n|/alpha} outside [Akitti framework core].
Sharp tip (side comparison only, never graded): the same winding with the core removed (f = bare power law down to the lattice).
Runs (frozen): k = 1, 2, 3 (alpha = 1, 1/2, 1/3); n = 1, 2; N = 21, 29, 41; L20 and L26 at a = rho/3; one a = rho/4 L27 run (L·a = 6.75 rho).
GoldbergHexa alpha = 5/6: side, only after a non-Z_k fuzzy cone exists (OPEN-C2).

## 4. Frozen pass rules (one set for every graded run)
P0 Construction: S^2 factor fuzzy-native; max angular content l <= N-1 (adjoint-Casimir check, tol 1e-12); Q_pred and target T frozen in files (name + hash) before grading.
P1 Charge: radial-projected charge routine (V1_2 §8a; prototype ../it1b/venus_v1_2_check_charge.py 0530de3b, extended to the Z_k weight w_cap = 4 pi R^2/(kN)).
   ||Q| - |Q_pred|| <= 0.02; sign reported; |Q| moves toward |Q_pred| from L20 to L26 (else construction bug, not a pass).
P2 Exponent: fitted log-slope of the energy density on w_N < r < r_c equals 2|n|/alpha - 2 within 0.05 at N = 41; fit window frozen as
   [2 w_N, 0.5 r_c]. UNDECIDED if the window holds < 4 lattice/fuzzy points.
P3 Action: S/(8 pi^2 T) = c0 + c1 x over N = 21, 29, 41; c0 = 1 +- 0.01; middle point within 0.5% of the line. T = boxed continuum
   action of the same seed's own profile on the same cone, frozen before grading (Gauss–Legendre, node doubling < 1e-6).
P4 Lattice: L20 -> L26 changes S/T by <= 0.1%; a = rho/4 vs rho/3 <= 1%.
P5 Sphere-term excess: lattice minus continuum sphere term of the same seed, |E| <= 0.01, not growing with N (the V4 catcher).
P6 Tip: fuzzy tip graded; sharp tip side only. Fuzzy-tip density finite at every N (max density at N = 41 <= that at N = 21 x (1 + 0.1)).
P7 Curvature bookkeeping: integrated curvature of the realised cone equals 2pi(1-alpha) at the tip within 1% (input check on the geometry, not on the field).
Stop rules: code bugs and seed-construction fixes are not rounds; fix loop capped at 3 rounds; a failure after round 3 is UNDECIDED. Statics pass before any flow or time evolution.
OPEN, not claimed: fuzzy S^2 x S^2 ADHM recovery.

## 5. What Aethon must code (each with file name + hash; Venus checks before grading)
C-1 Build file: the fuzzy cone seed on the Z_k cap (default fuzzy tip and the sharp side variant), with Q_pred(n,k) and the r_c choice frozen.
C-2 Radial-projected charge routine in grading, including the Z_k weight; regression: it must reproduce 0.9327 on the V4 N21 L20 seed.
C-3 Continuum boxed target integrator T(n, alpha, h) for the seed's own profile.
C-4 Tip-exponent fitter (P2) and density-finiteness check (P6).
C-5 Sphere-term continuum baseline (P5) and the l <= N-1 Casimir check (P0).
C-6 Curvature/deficit measure for the realised cone (P7).
C-7 SU(2)/U(1) split: grade SU(2), report U(1) (as V1_2).

## 6. OPEN items (kept, none dropped)
OPEN-A1 U(2N) vs SU(2) grading detail · A2 r_c value (her framework gives finite r_c, no number) · A3 = §2 (now central) · A4 hopfion-moiré
stack / cells (2108616007984046199) · A5 delta = delta_T + delta_s with force balance, alpha = 1 - 4G mu (dynamical geometry) · A6 R/x
conventions · A7 non-symmetric pole-localized fuzzy instanton (this spec's seed is its first attempt) · A8 Q sign/normalisation on cones
(P1 extends the V1_2 check) · tachyon-instanton array along imaginary time (2108946150795481569; spacing map to the lattice) · r_c (as A2) ·
C2 non-Z_k cone (GoldbergHexa 5/6, k = 6/5 link) · C3 two-tip runs (both poles, as in her infographic) · C4 ADK bulk-cone <-> her cone
(meeting point only) · C5 ADHM / Atiyah–Hitchin / Groisser readings from her images · fuzzy S^2 x S^2 ADHM recovery.

## 7. Note for Akitti (plain words)
This plan starts from your cone itself: a fuzzy cone tip at the pole with an instanton attached, and it asks your question directly,
how the cone angle and the charge are tied. A quick check already shows the angle hides from the total energy and shows up in how
sharply the field rises at the tip, so that is what we'll measure. Everything you listed that isn't built yet stays in, marked open.

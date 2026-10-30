# CONE_BUILD_V1 — Aethon build file for CONE_SPEC_V1 (b0a62591) + ADDENDUM_P1 (3150c48b). 2026-10-29 ~22:45 GMT
FROZEN before any graded run. No P0–P7 batch has been run. Changes go in CONE_BUILD_V1_1.md.
Predictions machine copy: CONE_PREDICTIONS_V1.json (hash in the file list at the end of this note's report).

## 0. What this rests on
- [Akitti] X 2110455808366633013 (cone at the poles = instanton trying to form; cone angle <-> instanton number), X 2110480278460465169
  (infographic: tips at both poles, 2pi - delta, delta = delta_t + delta_s), X 2108616007984046199 (moiré stack), X 2108946150795481569 (tachyon array).
- [Akitti] AKITTI_FRAMEWORK_2026-10-08 via spec §0: cone ds^2 = dr^2 + alpha^2 r^2 dphi^2, finite core r <= r_c, C^1 matching.
- [Akitti] /workspace/grok-push/open-problems/CONE_TIP_NOTE.md ("the cone is a clue"); /workspace/lift/AKITTI_POSTS_OCT22-28.md
  ("finite N automatically smears any classical cone tip"); /workspace/lift/HIVE_CONSTRUCTIONS.md meeting points (GoldbergHexa; fuzzy tip x ADK).
- [paper] Almheiri–Dodelson–Komargodski arXiv:2610.31610 (fuzziness smooths the bulk-cone singularity) — meeting point only (OPEN-C4).
- [paper] fuzzy sphere/projectors hep-th/9811169, 0905.2338: monopole projectors P_+- = (1 +- Lam)/2, Lam = (2L.sigma+1)/N.
- Reused from it1b: Model (Z_k twist, action, wcap), Venus's radial-projected charge (venus_v1_2_check_charge.py 0530de3b),
  the exact fuzzy pure-gauge form g L g^+ (V1_2).
I did not re-read the X posts myself this turn; I take them from Venus's spec §0.

## 1. Seed (C-1, cone_seed.py) — cone-first, fuzzy-native on S^2_F
g = P_+ + e^{i n theta} P_-;  B_i = L_i + F(r)(g L_i g^+ - L_i);  U_mu = exp(-i n Phi_mu P_-), Phi_mu = int_link F dtheta (exact, P_- projector).
Tip law: u = (r/r_c)^p, p = |n|/alpha; fuzzy tip (graded) u -> u r^2/(r^2 + w_N^2), w_N = 2R/sqrt(N+1); sharp tip (side) w = 0. F = 1 - e^{-u}.
Cone = Z_k cap of the fuzzy sphere (D2, alpha = 1/k). Seed is exactly Z_k invariant (tested, < 1e-12). R = rho = 1 (V1_2 carry-over, flagged).
SMOOTH-START FLAG: F(r) is a smooth function of the PLANE radius chosen by hand (not fuzzy on S^2_F — the S^2 factor stays fuzzy-native).
The exponent p = |n|/alpha is therefore BUILT IN, so P2 tests the construction, not dynamics (PRED-1 is a consistency check until flow).

## 2. r_c  [hive proposal, UNCHECKED]
r_c = 1.5 rho. Reasoning: (a) the charge needs F ~ 1 inside the box (half-width 3 rho at L20, 4.33 rho at L26); with r_c = 1.5 the
k=1,n=1 seed reaches F(edge) = 0.91 at L26 and Q_su2 = 0.999 at N=21 (smaller r_c -> steep p = 4, 6 tips under-resolved at a = rho/3:
k3 n2 gives kQ = 1.70 at r_c = 1.5 but only 1.10 at r_c = 0.5, N = 15);
(b) it sits between the V4 gauge-switch radii r_a = 1.5 rho and r_g = 3 rho. Her framework gives no number (OPEN-A2 stays OPEN).
Cost: the P2 window [2 w_N, 0.5 r_c] = [0.62, 0.75] rho at N = 41 holds one lattice radius -> P2 will be UNDECIDED (blocker B-P2).

## 3. FROZEN predictions (before any run)
P1 (addendum): tip holonomy m = n mod k; Q_pred = n/k (in Z/k, = m/k mod 1); cover check kQ = n (|kQ - round(kQ)| <= 0.02k). Graded on the SU(2) part (C-7), U(1) reported.
| n | k | alpha | m | Q_pred | kQ (cover) | p = |n|/alpha | P2 slope 2p-2 |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 1   | 0 | 1   | 1 | 1 | 0  |
| 2 | 1 | 1   | 0 | 2   | 2 | 2 | 2  |
| 1 | 2 | 1/2 | 1 | 1/2 | 1 | 2 | 2  |
| 2 | 2 | 1/2 | 0 | 1   | 2 | 4 | 6  |
| 1 | 3 | 1/3 | 1 | 1/3 | 1 | 3 | 4  |
| 2 | 3 | 1/3 | 2 | 2/3 | 2 | 6 | 10 |
Sign: +1 for sgn = +1 (theta -> -theta flips Q exactly, tested). Reason for Q_pred = n/k: the winding n sits at the fixed point of the
Z_k cap and the cap weight is 4 pi R^2/(kN), so the k-fold cover carries the full charge n [standard: orbifold instantons, hive reading].

## 4. D2 flag (for Akitti)
This build's cone is the stand-in alpha = 1/k (Z_k orbifold cap). Her GoldbergHexa cones are alpha = 5/6 (12 pentagons, 4 pi total, Gauss–Bonnet
closes); 5/6 is not 1/k, so it needs a new non-orbifold fuzzy cone (OPEN-C2, k = 6/5 link stays a hive proposal). Nothing here tests 5/6.

## 5. OPEN, kept (none dropped)
A1 U(2N) vs SU(2) · A2 = r_c (proposal above) · A3 angle<->charge (central) · A4 hopfion-moiré stack · A5 delta = delta_T + delta_s, alpha = 1 - 4G mu ·
A6 R/x conventions · A7 non-symmetric pole-localized instanton · A8 Q sign/normalisation on cones · tachyon-instanton array (2108946150795481569) ·
C2 GoldbergHexa 5/6 · C3 two-tip runs · C4 ADK meeting point · C5 ADHM/Atiyah–Hitchin/Groisser · fuzzy S^2 x S^2 ADHM recovery.

## 6. Known blockers before grading
B-T  C-3: continuum target T integrator is built (Gauss–Legendre, node doubling 1e-6) but the full 4D continuum density of this seed
     (sphere + mixed terms from the symbols of P_+- and g) is not derived; only the cone Dirichlet part is. P3/P5 need Venus to mill it.
B-F  Far field: g L g^+ is an exact fuzzy pure gauge, but F = 1 - e^{-u} only reaches 1 exponentially; inside the box it is not exactly pure gauge.
B-P2 P2 window too narrow at R = rho, r_c = 1.5 (see §2).
B-Q  Smallest-N sanity (N = 21): k=1 n=1 passes-level (Q_su2 0.952 -> 0.999 L20->L26); k>=2 rows do NOT move L20 -> L26
     (box already saturated) so "moves toward" fails by construction; k3 n2 kQ = 1.70 vs 2 (tip p = 6 under-resolved at a = rho/3).
B-N  k = 3 at N = 21, 29, 41 (spec) vs it1b's N = 1 mod 3 rule (22, 28, 40); kept as the spec says, flagged.

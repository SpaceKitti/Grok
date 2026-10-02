# Betti-Berry vacuum filter: toy run

This file was written **before** `run.py` was run. The rules, the assumed inputs and
the pass/fail logic are fixed here first. `RESULTS.md` is written only by `run.py`
and is never edited by hand.

**What this is.** A toy test of the idea in Akitti's X post: a slowly rolling field
stops in a local minimum, percolation on a Goldberg sphere sets a Betti number, and
the residual energy is read off from that Betti number plus a Berry term. Vacua whose
residue lands in an assumed window are kept.

**What this is not.** It is not a solution to vacuum selection or to the cosmological
constant problem. Every number that decides which vacua survive is an assumed input
below, so **the selection is only as meaningful as those inputs**. No quantum-gravity
claim is made.

Tags: [computed] = produced by run.py; [identity] = follows from algebra; [assumed] /
[assumed input] = chosen here; [by construction] = true because of how the setup is
built; [standard] = textbook fact; [from Akitti's post] = quoted from
X_POSTS_verbatim.md; [finite-size] = an effect of the finite sphere;
[computed from lattice choice] = follows from the lattice we picked.

## 0. Foreign input files (read only, never modified)

These two files were already in this folder, placed by Orion. They are inputs, not
outputs of this job. run.py records their SHA-256 hashes before and after the run
to show they were not changed.

| file | mtime (UTC+1) | size (bytes) | SHA-256 (first 16 hex) | role |
|---|---|---|---|---|
| X_NOTES.md | 2026-10-02 15:21:38 | 4768 | 58117031B7A6B39D | another bot's notes, compiled before the posts were read; formulas unverified |
| X_POSTS_verbatim.md | 2026-10-02 15:34:04 | 6394 | D9915B9C81FAEEEA | Akitti's two X posts, verbatim; the authority for the formulas |

## 1. Formulas taken from the posts [from Akitti's post]

From post 1 (status 2105755883904831888):

$$V(\phi)\approx\Lambda_0+g\phi+\varepsilon_V\left[\cos\frac{2\pi\phi}{f}+\beta\cos\frac{2\pi\alpha\phi}{f}\right]$$

In words: a steady downhill slope plus two wiggles whose periods don't line up,
because alpha is irrational. Alpha is "golden-ratio or similar" in the post.

$$\rho_{\rm res}\sim\frac{\varepsilon_V}{L^{d}}\,b_k(\mathcal{C})+\text{Berry monopole contribution}$$

In words: the leftover energy is the wiggle energy spread over the locking scale,
times a Betti number of the occupied complex, plus a Berry term.

### Differences between the posts, X_NOTES.md and this job
- **Symbol:** the post writes epsilon. Here it is renamed eps_V (Venus) so it can't be
  confused with Pair A's drive epsilon. Same quantity.
- **"Approximately" vs "equals":** the post writes V ≈ ...; we use it as an exact toy
  formula. [assumed]
- **X_NOTES.md** gives the same two formulas, but from a task brief, not a post, and
  marks them unverified. The posts confirm both. Nothing else in X_NOTES.md (the MHD
  "scar-floor" trigger 1e-8, the Pair A bolt numbers, the references) is used here.
- **Lattice:** post 1 talks about "Menger-sponge or Poincaré-ball voxels". This job uses
  a GoldbergHexa sphere instead, as the spec asks (post 2 mentions the "GoldbergHexa
  hive", but not for this filter). [assumed]
- **What the posts leave unset:** k (which Betti number), L and d, the Berry monopole
  term, the structure-formation window, the percolation threshold, and the map from
  phi to occupancy. All of these are assumed inputs below.
- **Not used:** post 2 (the LQC bounce, the scar-floor ~0.041, the death-face residual).
  It doesn't enter this filter.

## 2. Assumed inputs (all values fixed here)

**Units [assumed]:** dimensionless toy units with an explicit scale. Energies are in
units of E_*, an arbitrary toy energy scale. The field phi is in units of f, so f = 1.
L is in lattice units (face spacing), so rho_res is in units of E_* per lattice cell.

| input | value | tag |
|---|---|---|
| eps_V (an energy) | 1 E_* | [assumed input] |
| alpha | (1 + sqrt 5)/2 = 1.6180339887 | [from Akitti's post: irrational, golden ratio or similar] |
| f | 1 | [assumed input] |
| Lambda_0 | 100 E_* (only enters V(phi_stop), not rho_res) | [assumed input] |
| beta scan | 0, 0.5, 1.0 | [assumed input] |
| g scan | 1, 5, 9, 12, 20 E_*/f | [assumed input] |
| scanned phi range | [-20, 0] | [assumed input] |
| starting points phi_0 | 0, -7, -14 | [assumed input] |
| dynamics | overdamped gradient flow dphi/dt = -V'(phi), RK4 | [assumed dynamics] |
| occupancy map | p(phi) = clip(-phi/20, 0, 1): occupancy grows linearly as phi rolls down from 0 to -20 | [assumed input] |
| lattice | Goldberg polyhedra GP(m,0), m = 4, 8, 16 (162, 642, 2562 faces); rho_res uses m = 16 | [assumed input] |
| random seeds | 300 per p for the Betti curves, 300 per candidate vacuum, master seed 20261002 | [assumed input] |
| k | 1: b_1 of the largest occupied cluster (the "occupied cluster" C) | [assumed input] |
| d, L | d = 2 (the complex is 2-dimensional); L = sqrt(N_faces), so L^d = N_faces | [assumed input] |
| Berry term | see section 5 | [assumed input] |
| window | 0.010 <= rho_res <= 0.030 E_* per lattice cell | [assumed input] |

## 3. Rules fixed before the run

**Rule 1: stopping condition first (Helios).** For every (g, beta), before any
rho_res, print PASS/FAIL of

$$g<\frac{2\pi\,\varepsilon_V\,(1+\alpha\beta)}{f}$$

In words: the slope must be smaller than the steepest possible uphill slope of the
wiggles, or the field can never stop. [standard] This is an upper bound. In a
finite range, the two wiggles never quite line up, so run.py also prints the actual
largest uphill slope of the wiggles, max of -dV_wiggle/dphi over the scanned range, and
whether any local minimum exists there. If the bound FAILS, print **"field never
settles; Betti filter has nothing to act on"** and skip rho_res for that set. If the
bound passes but there is no local minimum in the range, also skip rho_res, and say so.

**Rule 2: rolling.** From each phi_0, follow the overdamped flow until it stops. Record
phi_stop, the first local minimum reached. Cross-check it against the first zero of V'
found on a fine grid in the direction of motion. If the flow leaves [-20, 0] first,
record "leaves range".

**Rule 3: percolation.** No existing GoldbergHexa implementation was found under
C:\Users\Akitt. A read-only search turned up only text mentions in
pairA-jt-4d, pairA-qg-lift-4d, pairA-qg-on-R1, pairA-qg-theory (and copies under
Grok-jobs-push) and sm-zero-modes-S2, and none of them builds the lattice. So
`goldberg.py` builds GP(m,0) itself, as the dual of the class-I geodesic icosahedron.
- Each face is occupied independently with probability p (face-site percolation).
  Faces are adjacent when they share an edge. Face adjacency on a hex tiling is the
  triangular lattice, so in the infinite lattice p_c = 1/2 exactly. [computed from
  lattice choice; standard]
- The Goldberg sphere is finite, with 12 pentagon defects. So any jump near p_c is
  expected to be a **smeared** step whose position moves with size. [finite-size]
- **Which b_1.** b_1 here is that of the 2D complex: the union of the closed occupied
  faces. Three faces meet at every Goldberg vertex and touch pairwise along edges, so
  the small triangles of three mutually touching faces are filled in. b_1 is computed
  two ways that must agree:
  (i) Alexander duality on the sphere: b_1 = (components of the complement) - 1;
  (ii) the Euler characteristic of the induced sub-triangulation, chi = V - E + T, with
  b_1 = b_0 + b_2 - chi.
  Also printed, for contrast only, is the dual-graph cycle count E - V + components.
  It counts every filled triangle as a "cycle", so it is not the homology.
- For each size, print the mean b_0 and b_1 per face of the whole occupied set, the
  share of faces in the largest cluster, and b_1 of the largest cluster, all against p.
  The jump location is the p where the mean b_1 of the largest cluster rises most
  steeply (also given for the largest-cluster share), with a width.
- Exact check [identity]: for independent occupation, the mean Euler characteristic is
  N p - (3N-6) p^2 + (2N-4) p^3, which equals 1 at p = 1/2 for any size.

**Rule 4: Berry monopole term** [assumed input; not given in the posts]. Each new cycle
(each hole of the largest cluster, except the largest complement piece, which plays the
role of "outside") is threaded by a monopole of strength q_B = 1/2. Its Berry phase is
gamma_c = q_B * Omega_c, where Omega_c = 4 pi A_c / N is the solid angle of the hole and
A_c its size in faces (equal-area approximation [assumed]). The contribution is

$$\rho_{\rm Berry}=\frac{\varepsilon_V}{L^{d}}\;c_B\sum_{c}\bigl(1-\cos\gamma_c\bigr),\qquad c_B=1$$

In words: each threaded hole adds an Aharonov-Bohm-like energy that grows with the
phase it encloses. [assumed input]

**Rule 5: window and freezing.**
- rho_res = (eps_V / L^d) * mean b_1(C) + mean rho_Berry, averaged over seeds, at
  p(phi_stop), on the m = 16 sphere.
- In-window: 0.010 <= rho_res <= 0.030. [assumed input]
- **Frozen = YES** only if the vacuum is actually reached by the roll from some phi_0
  AND it is in the window. A reached vacuum outside the window is "not populated
  (filtered out)".
- In this toy, the field stops because of ordinary barriers. The Betti filter only
  labels which stops are kept; it doesn't stop the field. [by construction]
- Every local minimum in the range is also listed, with reached yes/no.

**Rule 6:** this job doesn't read or write C:\Users\Akitt\sm-zero-modes-S2 or
pairA-lambda-on-gamma. The Job Two table is untouched.

## 4. Expectations written before the run
- Bound: PASS for g = 1, 5 at beta = 0; for g = 1, 5, 9 at beta = 0.5; for g = 1, 5, 9, 12
  at beta = 1. FAIL otherwise. [identity, from the bound values 6.28, 11.37, 16.45]
- When the bound only barely passes, the actual max slope in the finite range may sit
  below g, so there may be no minima even with PASS. [expected, not certain]
- The Betti-jump location approaches 1/2 as m grows, with a width that shrinks.
  [standard, expected; finite-size]

## 5. Files
- `README.md` - this file (written before the run).
- `potential.py` - V(phi), the bound, minima, overdamped roll.
- `goldberg.py` - GP(m,0) built here (no existing implementation found).
- `percolation.py` - occupation, b_0 and b_1 (two ways), the largest cluster, the
  Berry sum.
- `run.py` - runs everything, writes `RESULTS.md` and `betti_vs_p.png`.
- `RESULTS.md` - generated; never hand-edited.
- `X_NOTES.md`, `X_POSTS_verbatim.md` - foreign inputs, read only.

No git.

Post-run (2026-10-02): b_1 behavior [identity: Alexander duality + self-matching]: on S^2, b_1(X) = b_0(S^2 \ X) - 1, and the GP(m,0) face graph is a self-matching triangulation, so <b_1>(p) = <b_0>(1-p) - 1 and <chi>(1/2) = 1 (up to 2^-N). The pre-registered b_1 expectation failed because b_1 was the wrong observable, not because of a bug; only the largest-cluster share (or torus wrapping cycles) jumps at p_c.
Post-run (2026-10-02): The share of b_1 on the largest cluster is retained as a [post-hoc] diagnostic, and fails at GP(4,0).
Post-run (2026-10-02): Verdict: 0 frozen vacua [assumed-input dependent; depends on phi0 choice]. The barriers do the selecting, the Betti filter only labels stops, and Lambda_0 is not cancelled.
Post-run (2026-10-02): Berry vacua use GP(16,0), N = 2562. The sum runs over holes; each hole uses its real size A_c counted in faces: γ_c = 2πA_c/N; the FACES are treated as equal-area, and the (1 - cos γ) form is [assumed input].
Post-run (2026-10-02): Stopping [by construction, no backreaction]: overdamped flow from rest ends at the nearest downhill minimum (phi_stop about phi0 - 0.5). In the real relaxion barriers switch on with the Higgs vev and select the stop (Graham-Kaplan-Rajendran 2015, arXiv:1504.07551) [standard]; this toy has fixed barriers.
Post-run (2026-10-02): Frozen count [depends on phi0 choice]: in-window minima lie near phi = -10.3 to -10.8 and -19.5 to -19.6 (p = 0.51-0.54 and 0.97-0.98), while starts 0, -7 and -14 never reach them.
Post-run (2026-10-02): b_1 is extensive [computed]: at p = 0.8, b_1 per face is printed for m = 4, 8 and 16; rho_res is about eps_V*b_1/N, of order 0.1 eps_V in the middle range, with no parametric topological suppression.
Post-run (2026-10-02): The Berry term is 1e-5 to 1e-8 of rho_res and moves no vacuum [computed; still assumed input].
Post-run (2026-10-02): **Signed off 2026-10-02:** Venus (maths PASS) and Helios (physics, PARTIAL: calculations sound; filter selects nothing; stopping by construction).

Post-run (2026-10-02): At m = 16, the computed duality table is <b_0>(0.1)=0.0723 vs <b_1>(0.9)=0.0718, <b_0>(0.2)=0.0960 vs <b_1>(0.8)=0.0962, and <b_0>(0.3)=0.0847 vs <b_1>(0.7)=0.0844; exact <chi>(1/2) = 1.
Post-run (2026-10-02): Berry scaling at p = 0.7 is 7.871e-04, 8.536e-05, 6.911e-06 for m = 4, 8, 16, with fitted N exponent -1.7151 [computed scaling].
Post-run (2026-10-02): b_1 per face at p = 0.8 is 0.0907, 0.0944, 0.0962 for m = 4, 8, 16 [computed].

Post-run (2026-10-02): b_0(p) - b_1(1-p) = 1 per pattern exactly, which is 1/N ≈ 0.0004 per face at m=16, so the ~0.0005 gap is expected [identity], plus seed noise.
Post-run (2026-10-02): Berry local slopes are m=4→8: -1.61 and m=8→16: -1.82; the gap from -2 is [finite-size]. Small-angle rho_B ≈ (2π²ε_V/N³)·ΣA_c² → N⁻² because p=0.7 has empty density 0.3 < 1/2 and finite holes; dropping the largest complement piece at small m flattens the fit.
Post-run (2026-10-02): Berry wording fix: each hole uses its real size A_c counted in faces, γ_c = 2πA_c/N; the FACES, not the holes, are treated as equal-area.

Post-run (2026-10-02): NanoRibbon go accepted as Akitti approval. [post-hoc] run.py now prints a parameter scan over occupancy-map scale, window centre/half-width, and phi_0 starts; the fixed default remains 0 frozen vacua.
Post-run (2026-10-02): [post-hoc] surviving_vacua(vacua, rho_window, spectrum_filter) plus --vacua-json is the Job Two spectrum hook; barriers select stops and the Betti/Berry filter only labels them.
Post-run (2026-10-02): [post-hoc] Job Two RESULTS_final.md was read in read-only mode; the hook needs vacua carrying rho_res, field_content, and spectrum, and the final grid applies the n=3/three-generation compatibility predicate.
Post-run (2026-10-02): [post-hoc] Added an explicit assumed Job Two alt-model map p(n,R)=clip((|n|/3)(1/R)^2,0,1), with raw m=16 b1 and rho_res reported over a small (n,R) grid; no Job Two file was changed.
Post-run (2026-10-02): [post-hoc] Empty-default diagnosis records barrier stopping, the phi_0 grid, extensive raw b1, and the negligible Berry term separately; future intensive b1/face or largest-cluster-share use remains an option rather than a default change.
Post-run (2026-10-02): [post-hoc] Read-only Job Two RESULTS_final.md is now available: n=3 with x=+/-1 gives three generations; the Higgs is an unfluxed scalar with constant mode and l(l+1)/R^2 tower; KK, Yukawa, SO(3), and anomaly-scaling data are carried into the assumed (n,R) grid metadata.
Post-run (2026-10-02): [post-hoc] Read-only X_WINDOW_DEFS.md confirms 0.010-0.030, clip(-phi/20), and phi_0 are assumed rather than Akitti-defined; borrowed p_c values 0.5/0.7055/0.38 and scar floor ~0.041 are cross-checked, and the optional CSK theta-lock is not used.
Post-run (2026-10-02): [post-hoc] Bridge wording fix adds the p=n/(3R^2) [identity] degeneracy, code-derived analytic R-bands, and Venus band comparisons.
Post-run (2026-10-02): [post-hoc] The Job Two rho-count is explicitly tagged [grid-step]; p_c=1/2 survivors are tagged [finite-size], and n=3 spectrum selection is marked [by construction].
Post-run (2026-10-02): [post-hoc] Bridge wording now identifies n/R^2 with the assumed S2 magnetic-field-strength map, marks the R grid as an off-shell coupling scan, and records radion fixing/stability caveats.
Post-run (2026-10-02): [post-hoc] Cosmetic wording: the computed n=3 narrow band supersedes Venus's hand estimate because the latter came from rounded rows.

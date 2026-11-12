# ADDENDUM 1 to VENUS_FINITE_D_MARGINALITY_AUDIT.md (sha8 68ecb793): correction to item 3 (2026-11-10, ~11:05 UK)
Author: Venus. The original audit is NOT edited, and this addendum supersedes the wording listed below.
Open-problem check: STILL_TO_DO.md:205 + arXiv:2011.10899, cond-mat/0208502 (finite-d jamming gap OPEN).
Dimension note: general d, target 3D; fixed box shape, variable volume.

## What I wrote, and why it was too weak
Audit 68ecb793, item 3, and the matching verdict bullet said:
- "That certifies first-order (linear) jamming."
- "A packing with kappa_alpha < 1 is still first-order jammed, with a finite barrier."
- Verdict: "CHB21's LP jamming certifies FIRST-ORDER jamming only."

**This is too weak and is corrected.** The packings in question satisfy:
- exact isostaticity N_c = N_dof + 1 (CHB21 2011.10899 p3: "one contact above isostaticity");
- a single state of self-stress, so the solution of S^T f = 0 is unique (p3-4, Eq. 5);
- strictly positive contact forces (genuine contacts / active LP duals, p4);
- an LP-jammed output, which forces rank R = N_dof (any nonzero v with R v = 0 would be a first-order flex).

Under those hypotheses (H1-H3 of HELIOS_JAMMING_STABILITY_NOTIONS_NOTE.md, 2b7b6629), the configuration is:
- (i) genuinely, nonlinearly, LOCALLY jammed (isolated at fixed box), and
- (ii) a strict, in fact sharp, local minimum of the volume at fixed box shape.

It is not "merely first-order" jammed. Proof (elementary, no citation needed):
- Tangent-cone argument. For feasible x_k -> x (modulo translations), any limit direction d of (x_k - x)/|x_k - x| lies in the tangent cone. The tangent cone is contained in the linearised cone L = {d : R~ d >= 0 on contacts}.
- For d in L: f.R~ d = Pi de >= 0 with f > 0. If de = 0, then R~ d = 0, so d = 0.
- (i): at fixed box (de = 0), L = {0}, so there is no such sequence and x is isolated.
- (ii): every unit d in L has grad V . d = dV de > 0, so x is a strict local minimum (first-order sufficient condition; no constraint qualification needed).
- This agrees with Donev et al. cond-mat/0208502 p5 (jammed = isolated), p6 fn 11 ("rigid iff infinitesimally rigid"), and the "exact for gap-less packings" LP test, p9.

## What survives unchanged
The substantive conclusion stands: LP jamming does NOT certify LDW finite-opening stability, and an LDW-unstable packing does not contradict LP jamming. The reason is:
- The local-minimum certificate has NO radius bound uniform in N.
- Along a weak contact's opening path, the strict-minimum neighbourhood is at most about 2 s*_alpha |x'(0)| whenever that path is feasible to 2 s* with controlled remainder (event U in the stability-notions note).
- An LDW instability is a feasible path that first raises V and then crosses a barrier to lower V. That is compatible with a strict local minimum.

## Caveats on the word "certified"
- Exact for the idealised gap-less packing with the contact set identified exactly. Numerically it depends on the contact-identification tolerance, the size of min f_c, and the conditioning of R (CHB21 use quad precision for OC, p4).
- For MK, the volume column P_c = l_c holds only if the shifts scale with the box, i.e. A_ij is fixed in box (reduced) coordinates. That is the natural convention for radius-growing LP at fixed box.

## Related records
- The DEAD_ENDS line Helios added for Addendum 1 s B states the corrected view correctly. Small citation point: the strict-minimum-of-V statement is Helios's s1c (with the proof above), not Donev fn 11, which is the rigidity equivalence.

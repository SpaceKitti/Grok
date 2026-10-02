# Pair A: can a loop in eps put lambda back onto Gamma?

This file was written **before** `run.py` was run. The rules below are fixed
here first. `RESULTS.md` is written only by `run.py` and is never edited by hand.

Tags used: [computed] = number produced by `run.py`; [identity] = follows from
algebra; [assumed] = taken from the handoff, not re-derived here;
[by construction] = true because of how the test is defined; [standard] =
textbook fact.

Nothing here is a quantum-gravity result, and none is claimed. This is a 2x2
matrix exercise.

## 1. Assumed inputs (from the handoff, not re-derived)

The handoff matrix (no new Hamiltonian is built):

$$H_A(\varepsilon)=\begin{pmatrix}-i a & v\varepsilon\\ v\varepsilon & -i b\end{pmatrix}$$

- a = 0.12337 (handoff says = pi^2/80): decay rate of sine mode n=1 on a
  Dirichlet slab with eta = 0.05, L = 2. [assumed]
- b = 0.49348 (handoff says = pi^2/20): same for n=2. [assumed]
- v = -0.360253 (handoff says = <sine1|x|sine2> = -32/(9 pi^2)). [assumed]
- kappa = (b - a)/2 = 0.185055. [assumed formula; value is plain arithmetic]
- eps_EP = kappa/|v| = 0.51368066 (the two exceptional points sit at +eps_EP
  and -eps_EP). [assumed]
- lambda_EP = -0.308425 i. [assumed]
- Gamma = the real segment [-eps_EP, +eps_EP] of the eps-plane, treated as an
  ordinary branch cut. [assumed]

The code uses the handoff decimals as given. `run.py` also checks them against
pi^2/80, pi^2/20 and -32/(9 pi^2), and reports the tiny rounding gap. [computed]

## 2. The eigenvalue formula (identity)

$$\lambda_\pm=-\tfrac{i(a+b)}{2}\pm\sqrt{v^2\varepsilon^2-\kappa^2}$$

In words: the two eigenvalues sit symmetrically about a fixed centre, and they
meet (the exceptional point) exactly where the square root is zero, i.e. at
eps = +eps_EP or -eps_EP. [identity] `run.py` checks this against numpy's
eigenvalues at every tracked step. [computed]

## 3. Shifted eigenvalue mu, and the ON-Gamma test (Helios's spec, fixed now)

- mu = lambda - tr(H)/2, where tr(H)/2 = -i(a+b)/2. So mu = +-sqrt(v^2 eps^2 - kappa^2). [identity]
- Note: the full model also has a common eps*L/2 term on the diagonal. It is
  **not** in H_A here, so it is not in tr/2 either. A common diagonal term
  shifts both eigenvalues equally and would cancel out of mu if it were put
  into both H and tr/2. [identity] We simply leave it out, as the handoff does. [assumed]
- **ON-Gamma** (for one eigenvalue) means:
  |Re mu| <= 1e-9 * kappa  AND  |Im mu| <= kappa.
- For real eps inside Gamma, the square root is purely imaginary with size at
  most kappa, so lambda lies on the imaginary segment from -i a to -i b. Both
  eigenvalues are on it. They meet at the centre lambda_EP only at the tips of
  Gamma (eps = +-eps_EP). [identity]
- Endpoint check, plainly [identity]: for any eps on Gamma,

$$\lambda-\lambda_{EP}=\pm\, i\,|v|\sqrt{\varepsilon_{EP}^2-\varepsilon^2}$$

  In words: on Gamma, both sheets (both signs) land on the same imaginary
  segment, just at mirror-image heights. So the statement "lambda ends on the
  cut spectrum" only repeats the statement "eps ends on Gamma"; it carries no
  extra information about which sheet you are on. (Here lambda - lambda_EP is
  the same thing as mu, because lambda_EP = tr/2.) `run.py` checks this
  formula numerically along P1. [computed]
- Consequence (written down before the run): mu is purely imaginary with
  |Im mu| <= kappa exactly when v^2 eps^2 is real and between 0 and kappa^2,
  i.e. exactly when eps itself is a real number in Gamma. So ON-Gamma depends
  only on where eps is, not on which branch you are on. [identity]

## 4. What is reported for each path

1. eps0 (the start point) and whether it is strictly inside Gamma
   (|Im eps0| <= 1e-12 and |Re eps0| < eps_EP).
2. Nearest-neighbour eigenvalue tracking. Step sizes are adaptive: a step is
   accepted only if neither eigenvalue moves more than 1% of the local gap
   (the gap = distance between the two eigenvalues, the smaller of its value
   before and after the step). Otherwise the step is halved.
   Branch names at the start: **branch A** = the "+" root, mu = +sqrt(v^2 eps0^2 - kappa^2)
   with the usual (principal) square root; **branch B** = the "-" root. For eps0
   inside Gamma, A is the one with Im mu > 0 (toward -i a); for eps0 outside
   Gamma on the real axis (P3b), A is the one with Re mu > 0.
   We follow the eigenvalue that starts on branch A and report which branch it
   is on when the path returns to eps0.
3. SWAP yes/no: yes if the followed eigenvalue comes back on the other branch.
4. ON-Gamma at the start and at return, printing |Re mu| and |Im mu|/kappa.
4b. **SAME-POINT** (added from Venus, a stricter test that does see a swap):
   does the followed lambda come back to the very same complex number it
   started at, i.e. |lambda(T) - lambda(0)| <= 1e-8 * kappa? Checked at
   T = 2 pi and T = 4 pi. Kept as its own column, separate from SWAP and
   ON-Gamma. It does not change the verdict rule.
5. Smallest distance from the path to +eps_EP and to -eps_EP. A path counts as
   touching an EP if that distance is below 1e-6 * eps_EP.
6. Winding numbers of the path around +eps_EP and around -eps_EP, computed by
   adding up the change in angle along the path and dividing by 2 pi.

Time runs over t in [0, 4 pi]: one lap is 2 pi, two laps in total. At t = 2 pi
and t = 4 pi we report eps, ON-Gamma, the branch label (2 pi: SWAP, 4 pi:
back to start branch or not).

## 5. Paths (formulas fixed now)

- **P1** (real): eps(t) = 0.5 * eps_EP * sin(t). Starts at eps0 = 0, stays on
  Gamma the whole time, returns.
- **P2** (figure-eight, a lemniscate of Gerono):
  eps(t) = R sin(t) + i h sin(t) cos(t), with R = 1.5 eps_EP and h = eps_EP.
  It starts at eps0 = 0. For t in (0, pi) it makes the right lobe, which goes
  around +eps_EP clockwise (winding -1); for t in (pi, 2 pi) it makes the left
  lobe around -eps_EP counter-clockwise (winding +1). So the windings are
  opposite. [identity, to be verified numerically] It crosses the real axis
  inside Gamma only at eps = 0; it also crosses the real axis at eps = +-R,
  which lie outside Gamma. `run.py` lists every real-axis crossing.
- **P3** (control; earlier T3 result was NO): circle around +eps_EP only,
  eps(t) = eps_EP - 0.25 eps_EP e^{i t}, radius 0.25 eps_EP, starting at
  eps0 = 0.75 eps_EP and going counter-clockwise (winding +1 around +eps_EP,
  0 around -eps_EP).
- **P3b** (added from Venus): the same one-tip circle, but starting OUTSIDE
  Gamma: eps(t) = eps_EP + 0.25 eps_EP e^{i t}, centre eps_EP, radius
  0.25 eps_EP, eps0 = 1.25 eps_EP, counter-clockwise (winding +1 around
  +eps_EP, 0 around -eps_EP).

## 6. Pre-registered expectation [identity, not computed]

- P1: no swap; ON-Gamma yes at start and return.
- P2: no net swap after a full lap; ON-Gamma yes at both ends.
- P3: swap yes on each lap (back to the start branch after two laps);
  ON-Gamma yes at both ends.
- P3b (Venus): ON-Gamma NO at the start (eps0 is outside Gamma, so mu is
  real and nonzero); swap at 2 pi; back to the start branch at 4 pi; ON-Gamma
  NO at return too.
- SAME-POINT: P1 and P2 yes at 2 pi and 4 pi; P3 and P3b no at 2 pi (the
  swapped value is the mirror point), yes at 4 pi.

Background fact: going once around a square-root branch point swaps the two
roots; going around it twice, or around both branch points once each, swaps
them back. [standard]

## 7. Verdict rule (fixed now)

- **YES** needs a path where ON-Gamma is NO at the start and YES at return,
  and the change is caused by SWAP = yes.
- If ON-Gamma holds at both ends whatever the swap does, the verdict is **NO**.
  [by construction: both branches share the segment inside Gamma, so a swap
  cannot move an eigenvalue onto or off Gamma.]
- SWAP, ON-Gamma and SAME-POINT are kept as separate columns. The rule
  above is Helios's and is unchanged by the additions (endpoint identity,
  SAME-POINT, P3b).
- RESULTS.md also prints a rounding diagnostic (how close |Im mu|/kappa is
  to 1 at the segment ends). It is information only; the ON-Gamma test used
  for the verdict is exactly the one in section 3.
- The last line of RESULTS.md is exactly one of
  `lambda restored onto Gamma: YES (path ...)` or
  `lambda restored onto Gamma: NO (paths ...)`.

## 8. Files

- `README.md` - this file (rules, written before the run).
- `paths.py` - the handoff numbers, H_A, and the four path formulas.
- `run.py` - tracking, tests, writes `RESULTS.md` and `paths.png`.
- `RESULTS.md` - generated by `run.py`; not hand-edited.
- `paths.png` - picture of the four paths, Gamma and the two EPs.

No git, no GitHub.

Post-run (2026-10-02): Helios rule fix, post-run, boundary identity: eps = 0 maps exactly to the segment endpoints -ia, -ib.
Post-run (2026-10-02): ON-Gamma is decided primarily from eps [post-hoc]: Im eps = 0 within 1e-12 and |eps| <= eps_EP; the lambda test is the secondary consistency check.
Post-run (2026-10-02): Lambda secondary tolerance [post-hoc]: |Re mu| <= 1e-9*kappa and |Im mu| <= kappa*(1 + 1e-12); any eps-versus-lambda disagreement is flagged.
Post-run (2026-10-02): P2, P3 and P3b [requires complex drive: gradient with a loss/gain part].
Post-run (2026-10-02): Gamma (real |eps| < kappa/|v|) is the physical PT-broken window, where a real drive below threshold leaves both modes at one frequency with two decay rates [identity].
Post-run (2026-10-02): No real-eps path can encircle a tip. Complex eps means eps x -> (eps_r + i eps_i) x, a linearly varying damping across the slab [standard: complex Bloch-Torrey gradient].
Post-run (2026-10-02): So 'a path that can hit Gamma' (real drive) and 'a path that flips' (complex drive) are different physical controls.
Post-run (2026-10-02): P3b at t = pi sits inside Gamma (eps = 0.75 eps_EP) with lambda on the segment; this comes from eps's position, not from the swap.
Post-run (2026-10-02): eps = 0 -> lambda = -ia, -ib; eps -> +-eps_EP -> lambda_EP [identity].
Post-run (2026-10-02): lambda on Gamma is fixed by where eps ends, not by the sheet [identity]; the flip is visible only in SWAP/SAME-POINT; NO is by construction.
Post-run (2026-10-02): Final verdict line: lambda restored onto Gamma: NO [identity: on-Gamma is a function of eps; closed loops return to eps(0)]; SWAP and SAME-POINT carry the flip (P3, P3b: 2pi swap, 4pi return).
Post-run (2026-10-02, follow-up to c985021): the spec wants exactly one verdict line, so run.py now ends RESULTS.md with a single plain line of the form `λ restored onto Γ: NO — <path>` (or `λ restored onto Γ: YES — path ...`). This replaces the two forms listed in section 7 [post-hoc: wording only; the verdict rule is unchanged].
Post-run (2026-10-02): the line just above the verdict carries the tags: on-Γ is a function of ε and closed loops return to ε(0) [identity]; the loop names and the flipping loops (P3, P3b) are read from the per-path table [computed]. Re-run check: no number in RESULTS.md moved; only the Generated line and the verdict lines changed [computed].

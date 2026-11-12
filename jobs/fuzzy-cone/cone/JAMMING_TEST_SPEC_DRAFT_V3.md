# Jamming test in the fuzzy-cone toy, DRAFT V3 (Helios, 2026-11-10 02:40 UK). Route A of Venus check 454ed895. Supersedes 1ece183b and V2 147ac769 (route B lambda term parked: not from Akitti's construction, no-ad-hoc rule). For Venus to freeze. Not run.
Open-problem check: STILL_TO_DO.md jamming entry OPEN (added 9 Nov); N1 negative-modes thread nearest. Literature: d=3 jamming open, exact only at d=inf (arXiv:1310.2549; van Hecke arXiv:0911.1384; O'Hern et al. cond-mat/0304421 for contact counting; Wyart-Nagel-Witten cond-mat/0409687 for excess soft modes). Continuum BPS vortex moduli flat for every b>1 (Bradlow CMP 135 (1990); Garcia-Prada BLMS 26 (1994)). DEAD_ENDS.md grepped: b-as-coupling null (1ece183b) and flat-Bradlow reading of B R3 are dead; not reused.
Idea owner: Akitti (jamming = soft modes / negative eigenvalues at a threshold before locking, posts 2119595984288116749, 2119613243593302457; the cubic lock-in = crystal-like order, NOT jamming, Akitti 9 Nov via NanoRibbon). Mapping and measures: hive proposal (Helios; route A Venus).
Grading rule: validity first: basis-free projector rank lambda(P_ker x3 P_ker) = 3/3 per pole on every state, else that row is UNDECIDED. Q_total output only.
Dimension note: 2D fuzzy S2 stepping stone. No d=3 jamming claim; frictionless; d=3 vs d=inf gap noted, not tested.

## Object, question and tie to the centre pole
Unchanged v2_1 BPS model, code 63b69fbc, n=3 strings per pole, b = Bradlow ratio R^2/2n. No new coupling.
In the continuum the 6 vortex positions (Sym^6 S2, 12 dims) cost nothing to move at every b>1 [standard]. So any stiffness we see on the fuzzy sphere comes from the discretisation (finite N), the tangential projection or the radial penalty, i.e. the "contacts" that lock the cluster are made by the fuzzy geometry itself.
Question: does the per-pole cluster lock because the fuzzy sphere is a lattice (crystal-like, stiffness tied to N), and does that locking soften as b -> 1 where the vortices dissolve? This reads the rigidity of the cone tip's charge arrangement at each pole, which is the main goal.

## Measures (all output; frozen before any result)
J1 Maxwell band. Hessian with freeze 30408148 settings (H1-H3). Band = 9 lowest nonzero eigenvalues above the 3 rotation modes; report them, gap ratio lambda_10/lambda_9, n_stiff (# > 1e-6), n_neg.
J2 N-scaling. Rows: N in {61, 81} at b in {2, 1.2, 1.05} (N=61 rows = the Hessian run now in progress, untouched; N=81 rows new, same script 42724a62 with N changed only). Report band_k(81)/band_k(61) per k and b. Continuum null [standard]: band -> 0 as N grows.
J3 Disordered starts (new seed function: new hash + Venus line check before launch). At b=2, N=61: 1 triad seed + 20 seeds with 3 zeros per pole at uniform random cap positions (numpy seeds 0..19). Relax, no timeout. Report number of distinct final states (|dE|>1e-8 or |dA3|>1e-4), each with E, A3, per-pole rank, n_neg, lambda_min_nonzero.

## Readings (decided now)
- LATTICE-LOCKED (crystal-like, artefact-driven): band falls with N (ratio < 1 for all 9 modes at a given b) and J3 gives one state. Lock-in filed under crystal-like order, set by the fuzzy lattice; not jamming.
- ROBUST LOCK: band does not fall with N (ratio >= 1) and J3 gives one state. Flags a real lifting term to explain; not jamming.
- JAMMING-LIKE HINT: J3 gives >= 2 distinct states, each with n_neg = 0 and band lambda_1 smaller than the triad state's. 2D hint only.
- SADDLE: any relaxed state with n_neg > 0 (Akitti's isolated negative eigenvalues); report b, N, and overlap with vortex moves.
- UNDECIDED: rank gate fails, non-convergence, or mixed signs across modes. Fix loop 3 rounds, then UNDECIDED.
- b-trend (output only): band vs b at each N; softening toward b=1 reads as dissolving, not jamming onset.

## Run order
N=61 Hessian rows: let them finish, untouched. N=81 rows and J3 only after Venus freezes this and line-checks the seed function; launch via preflight.py + launch_gated.py; no timeouts.

## Parked
Route B (coupling (lambda/8)(1-Phi^dag Phi)^2, eps=lambda-1) = hive proposal, held: only if Akitti OKs a coupling that is not in her construction.

# SM1_INPUTS.md: inputs for SM1 Part B, from hive runs and public sources only

Helios, 2026-10-08, about 16:30 BST. This file is read by SM1 Part A (only the `alpha_ext` slot, and only with an `[Akitti: ...]` tag, so nothing here changes a Part A run) and by Part B, which is HELD.

**Where values may come from (Akitti's rules, relayed by NanoRibbon at 16:06 and after):**
- None of her work comes from her own simulations. The cone on the strings and its tension were reported to her by the hive's bots, so every cone input has to come from **our own run files**.
- A value exists only if it is in one of these:
  - her public X posts (stand-ins: `AKITTI_POSTS_OCT1-8.md` F1C6CC26 and the QUOTED file);
  - local files (TrinityOrb or the box);
  - GitHub SpaceKitti/Grok, including older commits.
- If none of these has a value, it is **NOT COMPUTED (YET)**. It is never guessed and never sent to Akitti as a question.
- Placeholders in her posts (μ = 0.05, α = 0.8, mhd_trace {v: 0, B: 0, ρ: 1}, tol = 1e-8) are flagged POSSIBLY GROK-HALLUCINATED (extract FDF97FD3 §2). They are **not inputs**.

**What was searched:**
- Box: /workspace/lift, /workspace/6d, /workspace/oldlift (clone of SpaceKitti/Grok), b0, b2, l1, l1fix, l1grade, rugby, job5c, job7, u1, smS2final, sm1 and the MHD code (chive_ns, worktree-mhd).
- TrinityOrb (read-only): C:\Users\Akitt\open-problems\ and its subfolders, and every job folder in C:\Users\Akitt (pairA-*, qg-*, sm-*, radion-*, vacuum-*, membrane-*, mhd-qg-*, Grok-jobs-push).
- GitHub SpaceKitti/Grok: fetched read-only to main 1fe72c2 (120 commits). `git log -G` searched the whole history of jobs/ and open-problems/ for deficit, conical, Gμ, cone angle, string tension, r_c and matching circle. Only two paths were ever removed from the repo, `chive_ns` and `worktree-mhd/ns`; both still exist as local copies on the box (/workspace/oldlift), and neither turned up a cone.
- Posts: extract FDF97FD3 found 0 input values.

Source tags: `[hive-run: job, file, line]` for local files; `[hive-run: job, SpaceKitti/Grok@<commit>:<path>:<line>]` for GitHub. Where a box or TrinityOrb copy has the same SHA-256 as main, both are given.

## Slots (Part A spec 0.2 format, retagged [hive-run: ...])

```
alpha_ext = NOT COMPUTED (YET) [hive-run: none; no run produced an exterior cone angle from a tension]
G = NOT COMPUTED (YET) [hive-run: none]
sigma_G = NOT COMPUTED (YET) [hive-run: none]
mu = NOT COMPUTED (YET) [hive-run: none]
sigma_mu = NOT COMPUTED (YET) [hive-run: none]
r_c = NOT COMPUTED (YET) [hive-run: none]
r_c/R = NOT COMPUTED (YET) [hive-run: none]
Psi_rc = NOT COMPUTED (YET) [hive-run: none]
pressure = NOT COMPUTED (YET) [hive-run: none]
Pi = NOT COMPUTED (YET) [definition, not a value; Part B scores both the pointwise and the circle-totals versions]
T_b = NOT COMPUTED (YET) [hive-run: none]
gauge_norm = NOT COMPUTED (YET) [hive-run: none]
tau = NOT COMPUTED (YET) [hive-run: none; no run quotes an uncertainty]
f_theta_core = NOT COMPUTED (YET) [hive-run: none; no run produced a core profile]
tips = NOT COMPUTED (YET) [hive-run: none for a string core; see the table for the 2-tip excess cone]
```

## What the runs do contain, value by value

"INPUT PARAMETER" means the run assumed the value; it is not a result. "GR control" values are references only, never the core's gravity.

| wanted | value found | source | status |
|---|---|---|---|
| α (exterior cone angle) | none from a tension. Only cone actually measured: total angle 3.999997π ≈ 4π at each of two tips, so α = β/2π = 2, an **excess** (deficit −2π per tip) | [hive-run: pairA-qg-operator, SpaceKitti/Grok@1fe72c2:jobs/pairA-qg-operator/RESULTS.md:18 and :111] (box copy 3656A65A, same; TrinityOrb C:\Users\Akitt\pairA-qg-operator\RESULTS.md, hash 209A1EA7 because of text encoding, same lines 18/111); re-measured in [hive-run: pairA-jt-4d, SpaceKitti/Grok@1fe72c2:jobs/pairA-jt-4d/RESULTS.md:29] (4.000003π) and [hive-run: lift-l1, SpaceKitti/Grok@1fe72c2:jobs/lift-l1/RESULTS.md:73] (12.566371 = 4π per tip, C89D68A2) | **Not an α_ext.** Set by construction: the period τ_E = 4π/ε_EP was put in by hand from the handoff (qg-operator RESULTS:18, "[by construction, given τ_E = 4π/ε_EP from the handoff]"). It's a kinematic measurement on the spectral curve of a 2×2 MHD matrix, with no strings, no tension and no field equation. Neither GR nor QG. |
| α grid (Job Four) | 1, 0.8, 0.6, 0.5 | [hive-run: sm-rugby-yukawa, SpaceKitti/Grok@1fe72c2:jobs/sm-rugby-yukawa/run.py:44]; README:22-24 ("[assumed input; SLED-type rugby ball, where the brane tension makes the deficit]") | INPUT PARAMETER |
| α grid (Job 5b) | 1, 0.8, 0.6, 0.5, 1.5 | [hive-run: radion-5b-tension-casimir, SpaceKitti/Grok@1fe72c2:jobs/radion-5b-tension-casimir/run.py:20]; RESULTS:26-30 | INPUT PARAMETER (1.5 labelled "unphysical: negative tension") |
| α grid (SM1 Part A run) | 1, 4/5, 3/5, 1/2 | [hive-run: SM1 Part A, open-problems\01_sm_from_sphere\SM1_filter\RESULTS.md (7148A1DC), "grid-only run (alpha in {1, 4/5, 3/5, 1/2} [assumed])"] | INPUT PARAMETER |
| α, ε from Job 5d route (a) | α = 3, ε = −2 | [hive-run: 5d-rugby-ball-flux, SpaceKitti/Grok@1fe72c2:jobs/5d-rugby-ball-flux/RESULTS.md:25-26] (box copy 12E53647, same) | GR control (ABPQ 6D Einstein–Maxwell, with the deficit formula assumed at RESULTS:10). Computed only for the tuned N = 3 condition. An excess, graded FAIL [tuned]. Not an input. |
| μ (tension) and G convention | no μ. Job 5d uses ε = 4G₆T (G₆ the 6D Newton constant; deficit 2πε = 8πG₆T), symbolic; route (a) gives T = −1/(2G₆) | [hive-run: 5d-rugby-ball-flux, SpaceKitti/Grok@1fe72c2:jobs/5d-rugby-ball-flux/RESULTS.md:10] ("[assumed input from ABPQ §4]") and :25-26 | GR control; T is negative and tuned. NOT COMPUTED (YET) as μ. |
| tension-like energy (nearest computed number) | vortex energy = πn (n = 1, 2, 3; e = v = 1), to 1e-12 | [hive-run: B0, SpaceKitti/Grok@1fe72c2:jobs/b0-taubes-base/RESULTS.md:73] (and rows 31-48; box b0/graded_RESULTS.md AE4E8FFB, same) | Computed (Bogomolny value), but these vortices sit on a **round** S² with no deficit and no G. No unit map to an exterior μ exists. Not μ, and not T_b. |
| r_c and R | no r_c. R = 1 in Jobs Two and Four (convention; Job Four README:22); B0 R² = n(1 + ε) for the chosen ε grid (B0 RESULTS:8); Pair A S² radius r = ε_EP = 0.513681 | Job Four README:22; [hive-run: B0, SpaceKitti/Grok@1fe72c2:jobs/b0-taubes-base/RESULTS.md:8]; [hive-run: pairA-qg-theory, SpaceKitti/Grok@1fe72c2:jobs/pairA-qg-theory/RESULTS.md:16, 118-119] ("circular: couplings chosen from ε_EP") | R values are conventions or INPUT PARAMETERs; Pair A's r is circular. **r_c: no run produced one.** |
| Ψ on the matching circle (v, B, ρ, p) | none. No run has a matching circle. The MHD code (chive_ns) has no cone. B0 prints a U(1) field B = (1 − \|φ\|²)/2 on the round S² (RESULTS:52-71), which is not an MHD field and not on r = r_c | B0 RESULTS:52-71 | NOT COMPUTED (YET) |
| core shape f(θ) | none for a core. Job Four f = Rα sin θ (constant curvature, equal tips, assumed, README:22). qg-operator: unit sphere f = sin ρ with φ over 4π (RESULTS:112), from the hand-set period. L1: Schwarzschild cigar | Job Four README:22; qg-operator RESULTS:112; [hive-run: lift-l1, SpaceKitti/Grok@1fe72c2:jobs/lift-l1/RESULTS.md:62] | Job Four f is an INPUT PARAMETER geometry; qg-operator's is by construction; L1 is a GR control. NOT COMPUTED (YET) for the core. |
| brane tension T_b normalisation | none. Job Four: "no brane action" (README:93-94). Job 5b: tension only relabels the flux, V_α(x; n) = αV₁(x; n/α) (README:17, 38). Job 5d: symbolic T with ε = 4G₆T | Job Four README:93-94; [hive-run: radion-5b-tension-casimir, SpaceKitti/Grok@1fe72c2:jobs/radion-5b-tension-casimir/README.md:17, 38]; 5d RESULTS:10 | NOT COMPUTED (YET) (5d is a GR control) |
| number of tips and equality | qg-operator / jt-4d / L1: **2 tips, equal** (3.999997π and 3.999997π), equal because one period serves both. Job Four: 2 equal tips, assumed | qg-operator RESULTS:18; Job Four README:23 | For the excess cone, equal by construction. For a string core no run gives a number of tips. NOT COMPUTED (YET). |

## Where "the cone formed" actually rests

- **The only hive run output where a cone formed is `pairA-qg-operator` RESULTS.md line 18** (also line 111). It was run 09-25 on TrinityOrb and pushed to SpaceKitti/Grok in 757af61 (2026-10-02 15:27 BST); it is unchanged at 1fe72c2.
  - It says that with τ_E = 4π/ε_EP "each tip is a conical point with total angle 3.999997π (+ε_EP) and 3.999997π (−ε_EP), i.e. 4π: conical excess, a double-cover branch point."
  - It was re-measured in pairA-jt-4d RESULTS:29 and lift-l1 RESULTS:73, and written up in CONE_TIP_NOTE.md 4EAAEAA9 §1-§3.
- **What it is:**
  - an **excess** of one full turn at each of the two exceptional-point tips of the 2×2 Pair A MHD matrix;
  - it exists only because the period 4π/ε_EP was put in by hand ("[by construction, given τ_E = 4π/ε_EP from the handoff]");
  - it's the n = 2 branched double cover of the round S² [identity, CONE_TIP_NOTE §4b].
- **What it is not:**
  - not a deficit;
  - not caused by strings or by tension;
  - not a solution of any field equation.
- **"Strings with tension make a deficit cone"** appears in hive files only as:
  - known GR reference physics (CONE_TIP_NOTE §4a, §6a: Vilenkin 1981);
  - a bot suggestion marked "[Grok-suggested] … Untested" (CONE_TIP_NOTE §5);
  - an assumed input in Job Four (README:22-24), Job 5b (run.py:20) and Job 5d (RESULTS:10, ABPQ, GR control).
- **No hive run computed a tension that produced a cone.**

## Summary

- Values found from hive runs, posts or SpaceKitti/Grok: **0 usable inputs**. Every slot above is NOT COMPUTED (YET).
- What does exist:
  - the 2-tip 4π excess cone (by construction, Pair A);
  - assumed α grids (Job Four, Job 5b, Part A);
  - GR-control formulas and tuned values (Job 5d);
  - a round-sphere vortex energy πn (B0) with no unit map to μ.

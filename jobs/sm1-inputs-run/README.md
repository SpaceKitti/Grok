# SM1-INPUTS-RUN: tensioned vortices at a conical tip (second graded run: RUN on 2026-10-08, exit 0; graded by Venus; Helios sign-off open)

- **Spec:** `01_sm_from_sphere/SM1_filter/JOB_SM1_INPUTS_RUN_SPEC.md`, SHA-256 prefix **C9683FDD** (389 lines; Helios ruling + node cap, §3b; Venus passed it). The first graded run used DB7ECF85.
- **Inputs sheet:** `SM1_filter/SM1_INPUTS.md`, **E0D7D41D**. Read-only; this run does not edit it.
- **run.py for the second graded run:** **38C1D32A** (2322 lines). Earlier versions are kept, not used: 235D00E5 (graded run 1, crashed; dev/run_235D.py and %TEMP%\run_235D.py), B11D43D5 (v2, HELD by Venus; dev/run_B11D.py).
- **Diffs:** dev/run_v2.diff (235D00E5 → B11D43D5, C3DE65C5); dev/run_v3_vs_B11D.diff (B11D43D5 → 38C1D32A, 8D84EEEC).
- **Not built:** Part B (JOB_SM1B_SPEC.md 6611EE3B) is HELD. The MHD core job is not built.
- **Hashes:** the first 8 hex characters of SHA-256, uppercase.
- **Status:** the second graded run was launched on TrinityOrb at 21:50:16 BST and finished at 23:33:07 BST with exit code 0. The outputs in this folder (RESULTS.md 84E12441 and the files listed under Outputs) come from it. As printed, the critical stage and stage NC are FAIL and SM1_INPUTS_FILLED.md holds no values, so every slot stays NOT COMPUTED (YET). See "Post-run notes (graded run 2)" below.

## Numerical settings for the second graded run (H3)

- **Mesh-node cap:** `MAX_NODES = 100000` on both solve_bvp calls (Taubes and stage NC). 235D00E5 used 3 000 000, which caused the out-of-memory crash. The cap is a numerical setting, not a graded tolerance. BVP tol stays at 1e-10 (read from B0). No threshold, tolerance, grid or prediction differs from DB7ECF85.
- **Workers:** `N_WORKERS = 8` (TrinityOrb has 15.4 GB RAM; 235D00E5 used 16).
- **Largest converged node count:** 12300 in the box node-count re-run of P1 1T n = 4, ε = 1 (C-GR 1T n = 4, ε = 1: 12248), counting every converged solve including continuation substeps and the G4/NC4 re-solves, at the TrinityOrb smoke's settings (κ = 0.5 and 4); 12211 in the box forced smokes (smoke grid). All against MAX_NODES = 100000. RESULTS prints the graded run's own value next to MAX_NODES.
- **Normal-state fill (spec C9683FDD §3b):** 32 rows, 16 per κ, at (ε, κ) = (1, 0.25) and (1, 0.5): P0 1T n = 1–4; P1 1T α = 1, n = 1–4; C-GR 1T α = 1, n = 1–4; C-GR 2T α = 1, n = 2, 4; P2 2T α = 1, n = 2, 4. They are filled as the exact normal state with no BVP call, tagged "[normal state: exact solution, linearly stable for B > κ/2, marginal at B = κ/2; whether a vortex branch coexists (κ < 1, subcritical) is NOT COMPUTED (YET)] [by construction; not a test] [Venus 20:44]", and counted in the tally column "n/a (normal state)". A code assert checks that the list has 32 rows, 16 per κ, and equals the smooth-tipless B ≥ κ/2 rows over the 70 chains. Filled rows feed no vortex-side slot: μ_matter, μ_i, s_c, r_c, Φ_i, T_b, w, G_req and Δ_bg for their sets are NOT COMPUTED (YET). Cone-tip rows and P12 always run the BVP.
- **Error boundary (per κ path; Venus):**
  - The critical-stage α ladder is one path. At each α, every κ path (1 → 0.5 → 0.25 and 1 → 2 → 4) starts only from that α's κ = 1 solution.
  - A row whose solve does not converge (solve_bvp status ≠ 0, including the cap) is "failed directly". Every row that would start from it is "failed upstream (row X)". Both are NOT COMPUTED (YET) and count as FAILED; nothing is dropped and the totals do not change. Rows on other paths carry on.
  - A non-converged check re-solve (G4 1.5 × T, NC4 2 × nodes or 1.5 × T) fails only its own check; nothing starts from it (Venus N6).
  - C0 covers critical-stage solves only (ε ladder, α continuation, G4 re-solve). Stage-NC failures are counted by NC0 and the stage-NC tally (passed / FAILED incl. not converged (cap hit) / n/a (normal state)), so a κ-path stall cannot fail the critical stage (Venus B1).
  - "Never retried" means: after the pre-registered continuation fallback (bisection of a failed step, depth 4, already in 235D00E5) is used up, the row is not solved again (Venus N7).
  - Each chain prints its name when it starts and every failed row with its error; RESULTS lists every failed row with its label.

## Run command (PowerShell, TrinityOrb, from this folder) — used for graded run 2

```powershell
$env:PYTHONIOENCODING='utf-8'; & 'C:\Users\Akitt\Grok\.venv\Scripts\python.exe' -B run.py
```

Before launch, spec C9683FDD was copied to `SM1_filter` and run.py 38C1D32A to this folder (replacing DB7ECF85 and 235D00E5; backups in %TEMP%\sm1_stage2_backup\), so the H4 re-hash would pass. Staged and re-hashed on TrinityOrb before launch; RESULTS shows all 9 sources matching. Run 2 was started with this command from %TEMP%\sm1_graded2_launch.ps1 (keep-awake, output to %TEMP%\sm1_graded2.log).

## Outputs (written only by run.py; run 2's outputs are in this folder, hashes in the post-run notes)

| file | contents |
|---|---|
| `RESULTS.md` | Symbol map (line 1), inventory, fixed settings, run log (cap, workers, largest converged node count, failed rows), G1–G7 with C0, row tables, consistency curve, stage NC (NC0–NC7, tally), PREDICTION vs outcome, audit, grade. |
| `profiles.csv` | Critical stage profiles per row. |
| `per_tip.csv` | μ_i(s) and Φ_i(s) on the secondary grid s ∈ {2, 4, 6, 8} per tip. **This is the secondary-grid Φ_i file the MHD core job needs.** |
| `consistency_curve.csv` | G_req(α) per row and κ; failed rows and filled normal-state rows are listed as NOT COMPUTED (YET). Exception (H10, run 2): the 24 BVP-solved normal-state entries at (ε, κ) = (1, 0.25) carry a G_req in 48 rows; see the post-run notes. |
| `nc_scan.csv` | Stage NC per row and κ; failed rows listed with their label; filled normal-state rows carry no vortex value. Exception (H10, run 2): the 24 BVP-solved normal-state entries at (ε, κ) = (1, 0.25) carry μ and w values under the generic vortex tag; see the post-run notes. |
| `SM1_INPUTS_FILLED.md` | Same slots as SM1_INPUTS.md, with RESULTS line tags. |

## Symbol map

| symbol | meaning |
|---|---|
| code `u` | spec χ(t), the Taubes function (B0's name). |
| `u_flow` | the velocity; NOT COMPUTED (YET) here. Never a bare u. |
| κ | λ/e², the coupling (κ = 1 is critical) |
| β | plasma beta only (unused) |
| η → code `P2_SHAPE` = 0.5 | the P2 shape parameter |
| s_c | s_c,δ, the proper core radius from the tip |
| r_c | f(θ_c)/α_i, a definition (circumference match), never a copy of s_c. |

No chive names (`chi`, `eta_*`, `lambda_in`) are used in run.py; RESULTS' audit prints the tokenizer check.

## Graded run 1 (crash record, kept as a disclosure)

run.py 235D00E5 on spec DB7ECF85, started 18:30:25 BST on TrinityOrb with 16 workers and max_nodes = 3 000 000. It ran out of memory (workers at 29–42 GB virtual) and exited with code 1 at 20:32:09 BST after 2 h 02 min, with 0/90 tasks done and no output written. Full record: **README_crash1.md (E5B5D76C)**; console log dev/graded_run_console.log. The second run is NanoRibbon's go-ahead (counted as Akitti's) with Venus-approved code-only changes.

## Disclosures (H5): every scratch, dev and profiling run

1. Box prototypes before run.py (dev/geo.py, taubes.py, nc.py, mini.py, t1–t5.py; graded-type settings). Solver design only.
2. Box smoke #1 (17:32, killed under load), TrinityOrb smoke in %TEMP%\sm1smoke (about 17:46–18:07, killed), box smokes #2 (18:07) and #3 (18:20), profiling on the box (prof.py, prof2.py, g4diag.py, 18:03–18:18) and on TrinityOrb (prof.py). Details in README_crash1.md.
3. Graded run 1 (crashed; above).
4. v2 development smokes on the box (/tmp mirror, SM1_SMOKE settings), about 20:45–21:02: intermediate versions (/tmp/smoke_v2a.log, /tmp/smoke_v2b.log, killed when the code changed); B11D43D5 normal smoke (602 s; tally 156/0/16 of 172) and forced chain cap-hit smoke (607 s; 143/13/16 of 172).
5. TrinityOrb memory smoke, B11D43D5, %TEMP%\sm1smoke (not the run folder), 20:50:38–21:02:08 BST: the five n = 4, ε = 1 chains at κ = 0.5 and 4. P0, P1 and C-GR 1T converged; P2 2T and C-GR 2T hit the cap at κ = 0.5, α = 0.9 (max |φ|² → 2e-7 and 6e-7). Peak total private memory 4.94 GB; peak working set 1.51 GB. Logs dev/mem_smoke_v2_out.log, dev/mem_smoke_v2_samples.log.
6. Box single-chain re-runs of P2 2T and C-GR 2T n = 4, ε = 1 (21:03–21:04; the first attempt failed on a driver path error): same cap hits, max RSS 0.53 / 0.54 GB.
7. v3 development: two box smokes on an early v3 (3628CE1B, 21:09, killed when Venus's notes arrived); forced smokes on 85F86FE2 and on 46CBC2DE (21:12, the first killed after seconds for a wording fix; the 46CBC2DE pair completed and showed a forced NC4 re-solve not being counted, fixed in 38C1D32A); a B11D43D5 regression smoke at the same settings (dev/smoke_v3_regress_B11D.py, log dev/smoke_v3_regress_B11D.log; every computed value identical to 38C1D32A's); final forced-stall smokes A and B on 38C1D32A (dev/smoke_v3_forced.py; logs dev/smoke_v3_forcedA.log, dev/smoke_v3_forcedB.log); node-count re-runs of P1 1T and C-GR 1T n = 4, ε = 1 on the box with 46CBC2DE (its solves are the same as 38C1D32A's; the later edits are reporting only) (dev/nodecount_v3.py; logs dev/nodecount_v3_P1.log, dev/nodecount_v3_CGR.log). All report-only, at non-graded or partial settings, none in the run folder.
8. Code changes after graded run 1 (all code-only; none touches a threshold, tolerance, grid or prediction): see dev/run_v2.diff and dev/run_v3_vs_B11D.diff.

## Spec ambiguities, H14 flags and Venus's pre-run notes

Unchanged from README_crash1.md (P12 report-only; NC7 same-R; negative-control profile flag; G4 μ_i at n_i = 0 tips; B0 ≤ 5e-12 erratum; r_c as a definition; NC6 different-R note). The ε = 1, κ = 0.5 flag is now resolved by spec C9683FDD §3b (normal-state fill for smooth tipless rows; cone-tip rows run the BVP under the cap).

## Audit

Sign-off:

Venus (maths): ____

Helios (physics): ____

## Post-run notes (graded run 2)

**Run.** run.py 38C1D32A on spec C9683FDD, launched on TrinityOrb at 21:50:16 BST (8 workers, MAX_NODES = 100000). The exit file appeared at 23:33:07 BST with exit code 0. RESULTS prints a runtime of 6168 s. No traceback and no REPORT ERROR in the log.

**Hashes** (SHA-256 prefix; the same on TrinityOrb and the box mirror):

| file | hash |
|---|---|
| RESULTS.md | 84E12441 |
| profiles.csv | 8FCD0035 |
| per_tip.csv | B3E611CA |
| consistency_curve.csv | BF37C674 |
| nc_scan.csv | C8333CB4 |
| SM1_INPUTS_FILLED.md | DB9D99A5 |
| console log (dev/graded_run2_console.log, from %TEMP%\sm1_graded2.log) | 67EEE52D |

run.py is still 38C1D32A after the run, and README_crash1.md is still E5B5D76C. RESULTS reports all 9 sources unchanged after the run. Run 1's log (dev/graded_run_console.log) is kept as it was.

**Verdicts and tally, as printed in RESULTS.md:**

- C0 (critical-stage convergence): PASS. 0 of 320 rows failed; 0 G4 1.5 x T re-solves not converged.
- Critical stage: FAIL, on G4 only (mu_i relative change, both tips; worst 5.877e+00 against 1e-08). Every other critical-stage check passed.
- NC0 (flat-plane references): PASS, 0 of 20 failed.
- NC0 (graded stage-NC entries): FAIL. 72 of 1112 graded entries (36 failed directly, 36 upstream, 0 NC4 re-solve); 37 of 640 kappa paths broken.
- NC1-neg (negative control): FAIL ("profile (s_c,delta) background-dependent at kappa = 1").
- Stage NC: FAIL ("critical stage failed; no stage-NC value is used").
  - H11 note: this printed reason (RESULTS lines 990 and 1617) names only the critical stage. NC0 (graded entries) and NC1-neg also failed on their own, as listed here. The spec asks for the reason to name the check that fired.
- Stage-NC row tally: passed 1008, FAILED (incl. not converged (cap hit)) 72, n/a (normal state) 32, total 1112.
  - **H10 correction (Venus):** the printed 1008 passed includes the 24 BVP-solved normal-state entries at (ε, κ) = (1, 0.25). They supply 144 values across NC2 (both rows), NC3, NC4 μ, NC4 s_c and NC5. They were counted as passes by construction: NC2, NC3, NC4 μ and NC5 hold for any solution, and NC4 s_c does not apply (no s_c, counted as a zero change). They test no vortex. **The real vortex passes are 984.**
  - Those 24 entries still carry vortex labels in report-only output: the μ and w values in nc_scan.csv; the μ-table cells at RESULTS lines 1268, 1288, 1308, 1448 and 1488 (α < 1 cells showing 0.50000000 with no normal-state tag); and 48 G_req rows in consistency_curve.csv (24 entries × 2 readings). These numbers are the normal-state energy, μ/(πn) = 0.5. They must not be quoted as vortex μ, w or G_req. The code fix (R2-7: tag them "normal state (BVP)", give them n/a, write no μ_i, w or G_req) is queued for run 3.
- SM1_INPUTS_FILLED.md written with values: NO (every slot NOT COMPUTED (YET)).

**Prediction against outcome:**

- mu_matter = pi n everywhere (Bogomolny): HIT [identity; tests numerics] (max |mu/(pi n) - 1| = 1.1e-12 over 308 rows).
- No s_c,delta before the midpoint at eps = 1 and 4 (Bradlow regime): HIT (at eps > 4, s_c,delta exists at 200 of 200 vortex tips).
- G_req = (1 - alpha)/(4 pi n), a straight line: HIT [identity; tests numerics] (max difference 2.207e-15).
- At eps = 99 each 2T tip carries pi n/2: HIT (max relative deviation 1.034e-12).
- C-GR eps = 99, mu(2T, n) = 2 mu(1T, n/2) on the same sphere: HIT (worst 1.160e-09).
- P1 rows approach the exact-cone value: report-only (max relative difference 3.243e-03 at eps = 99).
- w = -1: HIT [identity; tests numerics] (max |w + 1| = 4.9e-13).

**H14 flags for Venus and Helios (not rulings):**

1. G4 at the tips with no vortex (n_i = 0): RESULTS line 449. Vortex tips pass (worst 1.218e-12); the n_i = 0 tips, where mu_i is only the exponential tail, give the worst 5.877e+00. RESULTS notes that under a vortex-tips-only reading the critical stage would pass.
2. NC1-neg: RESULTS line 992. The mu part of the negative control passes; the profile flag is 'yes' in 24 of 24 groups, so a literal 'both no' control cannot pass on these grids.
3. Aethon's observation, not a ruling: all 36 graded cap hits are at eps = 1, kappa = 0.5, where B = kappa/2, on alpha < 1 rows (alpha 0.9 to 0.5). Their last max|phi|^2 ranges from 7.498e-09 to 4.083e-05. The spec (C9683FDD, line 265) leaves the branch point of cone-tip rows [open].

**Other notes:**

- The 37th broken kappa path is the report-only P12 2T-unequal n=2 eps=1 path (RESULTS lines 257-258). It is not in the 72.
- 24 stage-NC entries at (eps, kappa) = (1, 0.25) were solved by the BVP (not filled) and converged to the normal state, max|phi|^2 < 1e-6 (RESULTS line 994). RESULTS calls the observation report-only, but the entries are counted inside the 1008 passed; see the H10 correction above.
- Largest node count in any converged solve: 34974 (CGR 1T n=2 eps=1), against the cap of 100000.

**Disclosures (H5):**

- A read-only memory sampler ran on TrinityOrb during the run (every 5 s; log dev/graded_run2_memwatch.log). It was not part of the run. Peak total private memory 8.59 GB, in single-sample spikes; peak working set 2.43 GB; minimum free RAM 4.14 GB.
- The watcher was interrupted twice and resumed. This had no effect on the run.
- No scratch runs during the run, and no post-hoc changes to run.py, the spec, the inputs or the outputs.
- The smoke runs before launch are listed above; their logs are dev/smoke_v3_*.log.

**Venus's rulings on run 2 (VENUS_SM1_RUN2_GRADE.md 45B5A784), in brief:**

- G4: the literal FAIL stands. Its n_i = 0 part fails by construction (H14).
- NC1-neg: the literal FAIL stands. Its profile half fails by construction (H14).
- The 36 cap hits stay FAILED (Helios and Venus).
- R2-8 (H10): an absent s_c is counted as a zero change, which inflates NC4 s_c (549 of 1008 values) and G4 s_c (400 of 800 values). No verdict changes (real worst values 8.9e-8 and 6.9e-8); the fix is to count them as n/a.
- Next step: NanoRibbon chose option (b), a re-run as run 3 under an amended G4 (G4') written into the spec before launch. Run 2 stays on record as printed.

**Deferred:** Venus's R2-1 to R2-6 wait for the next code touch. R2-7 (the 24 normal-state BVP entries) is queued for run 3. R2-8's fix (count an absent s_c as n/a) is Venus's recommendation for the next code touch.

Sign-off (graded run 2):

Venus (maths): graded; printed record accurate; H10 correction (984) applied; VENUS_SM1_RUN2_GRADE.md 45B5A784

Helios (physics): ____

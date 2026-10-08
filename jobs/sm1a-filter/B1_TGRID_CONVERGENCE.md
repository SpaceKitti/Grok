# B1 t-grid convergence table: REPORT-ONLY

**REPORT-ONLY. Outside the graded SM1 Part A run. Requested by Venus on 2026-10-08 to close README disclosure 1. It does not change any graded output.** Written by `B1_TGRID_CONVERGENCE.py`, which copies run.py's B1 code and does not import or run run.py. Run at 2026-10-08 16:16:55 GMT Summer Time on TrinityOrb, Python 3.14.7, numpy 2.5.2, scipy 1.18.1.

Graded hashes (SHA-256, first 8 hex), checked by the script before and after this run:

| file | graded | before | after |
|---|---|---|---|
| run.py | 803FD2DA | 803FD2DA | 803FD2DA |
| README.md | 12CEC48F | 12CEC48F | 12CEC48F |
| RESULTS.md | 7148A1DC | 7148A1DC | 7148A1DC |
| CANDIDATES.md | DAD867CE | DAD867CE | DAD867CE |
| OVERLAPS_ALPHA.md | D93AC9BD | D93AC9BD | D93AC9BD |
| ANOMALIES.md | B55D5D1F | B55D5D1F | B55D5D1F |

All unchanged: YES.

## What this checks

Case: B1 at n = 3, eps = 4, the case where the graded run's theta-grid column undercounted. The analytic count is the index N_Phi = 3, fixed beforehand in A8. Both grids use the same operator R^2 D^2 = -u'' + (W^2 +- W') u with Dirichlet ends, the same 11 m values (m = -3.5 to 6.5) and both sigma3 signs, and the same rule: count eigenvalues below 0.5. The theta grid has N interior points, spacing pi/(N+1). The t grid has N interior points uniform in t = ln tan(theta/2) on [-40, 40], spacing 80/(N+1); the window is kept at [-40, 40] at every N. Nothing was tuned after seeing results.

Prediction written before the run: t-grid count 3 at every N on the ladder, at the graded step and at every window. theta-grid count 2 at every N on the ladder (the graded run gave 2 at N = 2000), with the third eigenvalue above 0.5 and falling slowly (box scratch numbers 0.832, 0.770, 0.715, 0.668, 0.627).

Prediction for the cut-off scan: (v2, written before the v2 run) Venus and Helios: the leftover m = 1/2 eigenvalue goes like C/T with C about 7 (0.1821 at T = 40), so the count stays 3 at every T in the scan and T times that eigenvalue stays near 7.

Version note: the first version of this script (v1) ran once at 16:13 BST with the N ladder and the window check only. This version (v2) adds the cut-off scan and the fit below, at Venus's and Helios's request. The v1 rows are recomputed here and are deterministic; v1's stdout is kept at %TEMP%\b1_tgrid_stdout_v1.txt on TrinityOrb.

## Main table: cut-off scan in T (t grid, step 0.01, window [-T, T])

On the t grid the step size barely matters; what is left is set by where the grid ends (theta about 2 e^-T at the north pole). The m = 1/2 mode sits exactly at the critical point of its pole potential, so its eigenvalue goes to 0 only like C/T. The count of 3 is the A8 index, fixed in advance; this table shows the FD count agrees with it at every cut-off.

| T | interior points | lowest eigs | m = 1/2 eig | T x (m = 1/2 eig) | count<0.5 |
|---|---|---|---|---|---|
| 20 | 3999 | -0.0000, 0.0140, 0.3788, 1.3956, 1.4737 | 0.3788 | 7.576 | 3 |
| 40 | 7999 | -0.0000, 0.0069, 0.1821, 1.3956, 1.4337 | 0.1821 | 7.283 | 3 |
| 80 | 15999 | -0.0000, 0.0034, 0.0893, 1.3956, 1.4144 | 0.0893 | 7.147 | 3 |
| 160 | 31999 | -0.0000, 0.0017, 0.0444, 1.3956, 1.4050 | 0.0444 | 7.098 | 3 |

## Side-by-side table: theta grid and t grid on Venus's N ladder

Lowest 5 eigenvalues pooled over every (m, sigma3) sector, smallest first.

| N | theta-grid lowest eigs | theta-grid count<0.5 | t spacing | t-grid lowest eigs | t-grid count<0.5 |
|---|---|---|---|---|---|
| 2000 | -0.0000, 0.0292, 0.8324, 1.3956, 1.5616 | 2 | 0.03998 | -0.0007, 0.0067, 0.1822, 1.3952, 1.4337 | 3 |
| 4000 | -0.0000, 0.0272, 0.7695, 1.3956, 1.5497 | 2 | 0.019995 | -0.0002, 0.0069, 0.1821, 1.3955, 1.4337 | 3 |
| 8000 | -0.0000, 0.0255, 0.7154, 1.3956, 1.5394 | 2 | 0.00999875 | -0.0000, 0.0069, 0.1821, 1.3956, 1.4337 | 3 |
| 16000 | -0.0000, 0.0239, 0.6684, 1.3956, 1.5304 | 2 | 0.00499969 | -0.0000, 0.0069, 0.1821, 1.3956, 1.4337 | 3 |
| 32000 | -0.0000, 0.0226, 0.6271, 1.3956, 1.5225 | 2 | 0.00249992 | -0.0000, 0.0069, 0.1821, 1.3956, 1.4337 | 3 |
| graded row: 7999 (step 0.01) | **NOT COMPUTED (YET)** (t-grid row only) | **NOT COMPUTED (YET)** | 0.01 | -0.0000, 0.0069, 0.1821, 1.3956, 1.4337 | 3 |

Graded row: run.py's own grid, 7999 interior points plus the 2 Dirichlet ends (8001 nodes). Every count above has sigma3 = -1 count 0 throughout.

Fit of the theta-grid m = 1/2 eigenvalue to a/(ln N + c) (Venus's form, report-only): a = 7.051, c = 0.870, largest residual 5.7e-05. On that fit the theta grid would need about N = 5.6e+05 points before this mode drops below 0.5.

## Window check (t grid, step 0.01)

| window | interior points | lowest eigs | count<0.5 |
|---|---|---|---|
| [-30, 30] | 5999 | -0.0000, 0.0093, 0.2459, 1.3956, 1.4468 | 3 |
| [-40, 40] | 7999 | -0.0000, 0.0069, 0.1821, 1.3956, 1.4337 | 3 |
| [-50, 50] | 9999 | -0.0000, 0.0055, 0.1445, 1.3956, 1.4259 | 3 |

## Detail: eigenvalues with their sector

- N = 2000, theta grid (h = 0.00157001): -0.000022 (m=1.5, s3=+1), 0.029247 (m=2.5, s3=+1), 0.832407 (m=0.5, s3=+1), 1.395597 (m=3.5, s3=+1), 1.561553 (m=3.5, s3=-1)
- N = 2000, t grid (h = 0.03998): -0.000720 (m=1.5, s3=+1), 0.006657 (m=2.5, s3=+1), 0.182197 (m=0.5, s3=+1), 1.395234 (m=3.5, s3=+1), 1.433704 (m=3.5, s3=-1)
- N = 4000, theta grid (h = 0.000785202): -0.000006 (m=1.5, s3=+1), 0.027229 (m=2.5, s3=+1), 0.769540 (m=0.5, s3=+1), 1.395598 (m=3.5, s3=+1), 1.549695 (m=3.5, s3=-1)
- N = 4000, t grid (h = 0.019995): -0.000180 (m=1.5, s3=+1), 0.006854 (m=2.5, s3=+1), 0.182096 (m=0.5, s3=+1), 1.395508 (m=3.5, s3=+1), 1.433710 (m=3.5, s3=-1)
- N = 8000, theta grid (h = 0.00039265): -0.000002 (m=1.5, s3=+1), 0.025470 (m=2.5, s3=+1), 0.715430 (m=0.5, s3=+1), 1.395598 (m=3.5, s3=+1), 1.539412 (m=3.5, s3=-1)
- N = 8000, t grid (h = 0.00999875): -0.000045 (m=1.5, s3=+1), 0.006903 (m=2.5, s3=+1), 0.182071 (m=0.5, s3=+1), 1.395576 (m=3.5, s3=+1), 1.433711 (m=3.5, s3=-1)
- N = 16000, theta grid (h = 0.000196337): -0.000001 (m=1.5, s3=+1), 0.023923 (m=2.5, s3=+1), 0.668384 (m=0.5, s3=+1), 1.395599 (m=3.5, s3=+1), 1.530410 (m=3.5, s3=-1)
- N = 16000, t grid (h = 0.00499969): -0.000012 (m=1.5, s3=+1), 0.006915 (m=2.5, s3=+1), 0.182064 (m=0.5, s3=+1), 1.395593 (m=3.5, s3=+1), 1.433712 (m=3.5, s3=-1)
- N = 32000, theta grid (h = 9.81717e-05): -0.000000 (m=1.5, s3=+1), 0.022554 (m=2.5, s3=+1), 0.627114 (m=0.5, s3=+1), 1.395599 (m=3.5, s3=+1), 1.522467 (m=3.5, s3=-1)
- N = 32000, t grid (h = 0.00249992): -0.000003 (m=1.5, s3=+1), 0.006918 (m=2.5, s3=+1), 0.182063 (m=0.5, s3=+1), 1.395597 (m=3.5, s3=+1), 1.433712 (m=3.5, s3=-1)
- graded t grid (h = 0.01): -0.000045 (m=1.5, s3=+1), 0.006903 (m=2.5, s3=+1), 0.182071 (m=0.5, s3=+1), 1.395576 (m=3.5, s3=+1), 1.433711 (m=3.5, s3=-1)
- window [-30, 30]: -0.000045 (m=1.5, s3=+1), 0.009252 (m=2.5, s3=+1), 0.245947 (m=0.5, s3=+1), 1.395576 (m=3.5, s3=+1), 1.446821 (m=3.5, s3=-1)
- window [-40, 40]: -0.000045 (m=1.5, s3=+1), 0.006903 (m=2.5, s3=+1), 0.182071 (m=0.5, s3=+1), 1.395576 (m=3.5, s3=+1), 1.433711 (m=3.5, s3=-1)
- window [-50, 50]: -0.000045 (m=1.5, s3=+1), 0.005503 (m=2.5, s3=+1), 0.144536 (m=0.5, s3=+1), 1.395576 (m=3.5, s3=+1), 1.425946 (m=3.5, s3=-1)
- T scan [-20, 20]: -0.000045 (m=1.5, s3=+1), 0.014020 (m=2.5, s3=+1), 0.378794 (m=0.5, s3=+1), 1.395576 (m=3.5, s3=+1), 1.473672 (m=3.5, s3=-1)
- T scan [-40, 40]: -0.000045 (m=1.5, s3=+1), 0.006903 (m=2.5, s3=+1), 0.182071 (m=0.5, s3=+1), 1.395576 (m=3.5, s3=+1), 1.433711 (m=3.5, s3=-1)
- T scan [-80, 80]: -0.000045 (m=1.5, s3=+1), 0.003420 (m=2.5, s3=+1), 0.089331 (m=0.5, s3=+1), 1.395576 (m=3.5, s3=+1), 1.414439 (m=3.5, s3=-1)
- T scan [-160, 160]: -0.000045 (m=1.5, s3=+1), 0.001701 (m=2.5, s3=+1), 0.044362 (m=0.5, s3=+1), 1.395576 (m=3.5, s3=+1), 1.404989 (m=3.5, s3=-1)

Cross-check: in every grid, the number of listed eigenvalues below 0.5 equals the Sturm count: YES.

## Reproduction of the graded B1 row (CANDIDATES.md, n = 3, eps = 4)

| item | graded file | this script | same |
|---|---|---|---|
| flux | 3.0000000000 | 3.0000000000 | YES |
| FD sigma3=+1 | 3 | 3 | YES |
| FD sigma3=-1 | 0 | 0 | YES |
| theta-grid FD (+1, -1) at N = 2000 | 2, 0 | 2, 0 | YES |

Background: BVP success True, C1 relative error 1.381e-12, max |phi|^2 0.999516. Total time 55 s.


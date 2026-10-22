# diag21 time estimate (2026-10-19)

Measured 2 t_f α=1 pick-rows (`out/timing_rev21/`): B10 760.4 s (0.211 h), B12 2058.3 s (0.572 h).
α=0.5 wall taken as 0.50× α=1 (angular sites = α L_φ). An IT1 row is 2T of flow, so wall scales as T/t_f times a 2 t_f pick-row.
find-T is a single B12 flow, stop at 10% window settle or 6 t_f. T/t_f copied to B10. No pick, no B14.

## Jobs

| stage | jobs | flow |
|-------|------|------|
| find-T B12 | 1 | up to 6 t_f (early-stop when windows settle) |
| cal B10, B12 | 2 | 1 t_f each |
| IT1 rows | 16 (2 boxes × (3 seeds × 2 α + 2 δ=0)) | 2T each |
| linearity B10 α=1 δ=0.002 | 3 | 2T each |
| grade | 1 | instant |

δ=0.001 tagged `[deviation] smallest rev 21 candidate; Venus reviews post-hoc`. `--outdir diag21`. Live `out/it1/` and `out/delta_frozen.json` unused.

## Hours

| stage | T = t_f (find-T 2 t_f) | T = 2 t_f (find-T 4 t_f) | T = 3 t_f cap (find-T 6 t_f) |
|-------|------------------------|--------------------------|------------------------------|
| find-T B12 | 0.57 | 1.14 | 1.72 |
| cal B10+B12 | 0.39 | 0.39 | 0.39 |
| IT1 16 rows | 4.70 | 9.40 | 14.10 |
| linearity 3 rows | 0.63 | 1.27 | 1.90 |
| **total** | **6.3** | **12.2** | **18.1** |

Expected: **12.2 h** (T = 2 t_f; rev 20 B12 1.5–2 t_f window was ~20–23% below 1–1.5 t_f, so T > t_f is likely). Design cap ~16 h; hard cap 6 t_f of find-T ⇒ T ≤ 3 t_f ⇒ 18.1 h if settle never fires.

Launch gate ≤ 18 h: expected 12.2 h passes. Launch `chain.ps1 -Diag21` (sleep held, `--outdir diag21`).

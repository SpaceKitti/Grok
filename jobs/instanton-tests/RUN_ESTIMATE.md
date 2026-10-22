# Rev 21 run estimate (2026-10-19)

Measured one unperturbed α=1 pick-row per box (2 t_f, `it1_pick_row` seed=−1, `out/timing_rev21/`). Full chain not started.

## Measured 2 t_f row (α=1)

| box | t_f | steps (pre+drift) | wall_s | hours |
|-----|-----|-------------------|--------|-------|
| B10 | 0.100 | 50+50 | 760.4 | 0.211 |
| B12 | 0.144 | 72+72 | 2058.3 | 0.572 |
| B14 | 0.196 | 98+98 | 4591.9 | 1.276 |

Rev 20 mixed-α / α=1 wall from saved `out/it1` rows: B10 0.80, B12 0.78. IT1 estimate uses 0.79 on the measured α=1 times. Pick, find-T, and cal are α=1.

## Job counts

| stage | jobs |
|-------|------|
| pick | 19 B10 + 19 B12 = 38 (1 base + 3×6 draws), α=1, 2 t_f |
| freeze | 1 (instant) |
| find-T | 1 per box × 3, δ=0 α=1, flow to 8 t_f (4× a 2 t_f row) |
| cal | 1 per box × 3, flow t_f (½× a 2 t_f row) |
| IT1 6+6 | 41 per box × 3 = 123 (plus 3 cal already counted) |
| grade | 1 (instant) |

IT1 row length is 2 T. T is found per box on δ=0 α=1 so the [T, 1.5 T] vs [1.5 T, 2 T] window drift is <10%, capped at 4 t_f. If the t_f windows already settle, T = t_f and an IT1 row matches the measured 2 t_f row.

## Hours per stage

| stage | T = t_f | T = 2 t_f | T = 4 t_f (cap) |
|-------|---------|-----------|-----------------|
| pick B10+B12 | 14.87 | 14.87 | 14.87 |
| freeze | 0.00 | 0.00 | 0.00 |
| find-T B10+B12+B14 | 8.23 | 8.23 | 8.23 |
| cal B10+B12+B14 | 1.03 | 1.03 | 1.03 |
| IT1 B10 | 6.83 | 13.67 | 27.33 |
| IT1 B12 | 18.53 | 37.05 | 74.10 |
| IT1 B14 | 41.33 | 82.66 | 165.31 |
| grade | 0.00 | 0.00 | 0.00 |
| **total** | **90.8** | **157.5** | **290.9** |

Pick / find-T / cal do not scale with the chosen T (find-T always scans to 4 t_f). IT1 scales ~ T / t_f. The T = t_f column is a lower bound; B12’s rev 20 1.5–2 t_f window was ~20–23% below 1–1.5 t_f, so T > t_f is likely on B12 and maybe B14.

IT1 α=1-only upper bound at T = t_f (no 0.79 mix): 8.66 + 23.44 + 52.30 = 84.4 h for IT1, 108.5 h total.

## Smoke chain (tiny, `--steps 1 --outdir smoke_rev21`)

Completed 2026-10-19 11:52, wall 6815 s (1.89 h). Freeze correctly printed NO_DELTA and continued with `--delta 0.001`. 123/123 IT1 rows + B14 cal + grade in `out/smoke_rev21/`. Live `out/it1/` and `out/delta_frozen.json` (δ=0.005) were not overwritten.

## Tests

110/110 (`python -B tests.py`). Existing 101 plus rev 21 checks (candidates, B14, linearity, window pair / choose T, 3-grid order, freeze 0.002).

# HP2 truncation-check hive handoff

Operator: `C:\Users\Akitt\Grok\jobs\cone-sims\run.py` sha8 837D0BC9, spec CA9D5CBC.
Tag: [report-only]. Do not grade. Do not start `--full`.

## This run (64×64)

`C:\Users\Akitt\Grok\jobs\cone-sims\out\hp2_check_64_nev20\`

Completed solves: n=2 κ=2 α=1.0, n=2 κ=2 α=0.5, n=0 κ=1 α=1.0.
Later series stopped (n=0 ARPACK too slow).

| file | what |
|---|---|
| REPORT.md | short verdict for bots |
| MANIFEST.md | this list |
| check.py | 64×64 driver |
| analyse.py | ratios + radial profiles |
| rows.csv | eigenvalues written |
| config.json | not written (job stopped before end) |
| solve_log.jsonl | per-solve wall times |
| run.log / run.err | stdout/stderr |
| evals_n2_k2.0_a1.00.npy | 21 evals, no-cone |
| evecs_n2_k2.0_a1.00.npy | 16384×21 |
| evals_n2_k2.0_a0.50.npy | cone α=0.5 |
| evecs_n2_k2.0_a0.50.npy | |
| evals_n0_k1.0_a1.00.npy | n=0 cluster |
| evecs_n0_k1.0_a1.00.npy | |
| key_ratios.csv | 32/48/64 λ_min table |
| mode_localization.csv | r50 + tip weights |
| lambda_min_ratios.csv | full dump |
| profiles\ | radial CSV/NPZ per grid |

## Prior grids

- 48×48: `C:\Users\Akitt\Grok\jobs\cone-sims\out\hp2_check_48_nev20\`
- 32×32 reduced (n=0 cluster, many α): `C:\Users\Akitt\Grok\jobs\cone-sims\out\hp2_reduced_32_nev20\`
- 32×32 10k-iter n=2 κ=2 evecs: `C:\Users\Akitt\Grok\jobs\cone-sims\out\hp2_iter10k\`
- 32 vs 48 analyser: `C:\Users\Akitt\Grok\jobs\cone-sims\out\hp2_check_analyse.py`

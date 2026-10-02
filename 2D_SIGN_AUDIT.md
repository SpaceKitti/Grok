# 2D sign audit: old `_u_from_vort_2d` returned -u (top-level chive_ns)

> **INVENTORY ONLY.** Nothing was re-run, no code was changed, and no git writes were made to produce this file.
> It lists what *may* be affected. **Helios decides what, if anything, gets re-run.**
> Compiled 2026-10-02 (BST) from read-only file searches and `git log` / `git show`.

## The bug

- Old line in `chive_ns/grid.py::_u_from_vort_2d`: `psi_hat = -vort_hat / grid["k2"]`, so u -> omega -> u returned **-u** (2D Taylor-Green round trip: max error 2.000 x max|u|; after the fix it is 1.3e-14).
- Venus's note: 2D vorticity inversion sign fixed: the old code returned -u from omega, which reversed the 2D velocity whenever it was rebuilt from vorticity (and anti-aligned 2D induction against the Lorentz force in MHD); 3D was unaffected.
- In the top-level tree the old sign has been there since `251e7ee` (2026-08-14, "Refactor grid.py for early-May vorticity updates").
- Fixed only on `origin/grokbot` in `b83f1d7` (2026-10-02 18:31 BST). Still has the old sign: `origin/main`, `origin/aethon/runnable-mhd` (open PR #1), `origin/venus/hive-textbook`, `origin/aethon/mhd-patches`, and the stale local `grokbot` ref.
- `_u_from_vort_3d` is untouched, so **every 3D path is unaffected**.

## Where 2D rebuilds u from omega (top-level `chive_ns/`)

| File:line | What it does |
|---|---|
| `vorticity.py:148` `_rhs_2d` | Advection `u . grad(omega)` uses the rebuilt u. Called by `ns_vorticity_rhs` / `ns_vorticity_step` (2D) |
| `vorticity.py:217-218` `_coupled_step_2d` | 2D clay step: omega advection (via `_rhs_2d`) **and** the Oldroyd-B tau update use the rebuilt u |
| `driver.py:83, 117` | Per-snapshot `velocity_from_vorticity` -> `field_diagnostics` / `stress_diagnostics` |
| `driver.py:251` | Final `u_hat` returned by `run_framework` |
| `grid.py:95` | `velocity_from_vorticity` dispatches 2D to `_u_from_vort_2d` |
| `mhd.py:12` | Imports `_u_from_vort_2d` but never calls it. The 2D Lorentz/induction functions take `u_hat` from the caller |

Note: `run_framework`'s **default is `dim=2`** (N=32, `ic="smooth"`, Euler, dt=0.005, scar forcing on). Any call that doesn't pass `dim=3` runs the affected 2D path.

## Scripts that import the top-level `chive_ns`

There are 8 scripts in `examples/`; each runs `sys.path.insert(parents[1])` and imports the top-level package. The venv's editable install also points at `C:\Users\Akitt\Grok\chive_ns`. All 8 were added in `cfaf055` (2026-08-14 18:23 BST), and **all 8 pass `dim=3`**:
`compare_ns_clay.py`, `compare_scars.py`, `compare_tubes.py`, `compare_tubes_scars.py`, `confirm_mild_clay.py`, `run_3d_highres.py`, `study_hires_nu.py`, `sweep_clay_mild.py`. (`interactive_toy.py` is a 2-byte placeholder in this tree.)
The `worktree-mhd/ns/examples/*` scripts insert their own `ns/` parent, so they use the worktree copy and are out of scope here.

## Inventory

Labels: **affected** = the output depends on the direction of u, or the run is time-evolved with the rebuilt u. **sign-invariant** = only quadratic-in-u quantities from a single rebuild, with no time evolution. **unclear** = there isn't enough evidence to tell.

| # | Entry | Label | Reason |
|---|---|---|---|
| A1 | `vorticity._rhs_2d` / `ns_vorticity_step` (2D NS) | **affected** | Advects omega with -u every step, so the whole 2D NS evolution is wrong (energies included) |
| A2 | `vorticity._coupled_step_2d` (2D clay / Oldroyd-B) | **affected** | Both omega advection and the tau stretching/advection are driven by -u every step |
| A3 | Any `run_framework(dim=2, ...)` run, including the default call | **affected** | Time-evolved through A1/A2; reported E/Z histories come from a wrongly evolved flow |
| A4 | 2D clay snapshot `stress_diagnostics(tau_hat, u_hat)` (`driver.py:117-118`) | **affected** | Stress-work-type terms are linear in u, so they flip sign even in a single snapshot |
| S1 | 2D `field_diagnostics` at t=0 only (energy, enstrophy, max abs(omega), max div u) | **sign-invariant** | A single rebuild with quadratic or absolute-value quantities; there is no time evolution before t=0 |
| U1 | `mhd.py` 2D path (`_lorentz_vort_2d`, `_induction_2d`, `induction_rhs`) | **unclear** | Not reachable from the top-level driver (no `mode="mhd"` here). Affected only if a caller passes a 2D u rebuilt from omega; no such caller was found |
| U2 | `live.py::_live_2d`, `residual.py` 2D | **unclear** | They take `u_hat` from the caller; no top-level 2D caller was found, so no outputs to tag |
| U3 | "original 2D scar runs" (docstring, `vorticity.py:204-205`) | **unclear** | No saved logs, CSVs or summaries anywhere under `Grok\`. If they ran on this code after 2026-08-14 they are affected |
| U4 | `open/03_hive_map.txt:22` "A2 2D textbook OT peel" (HAVE-style claim) | **unclear** | Came from `worktree-mhd` (its own `chive_ns`). The worktree fixed the sign in `04636a6` (2026-09-01 19:19 BST) and A2 was parked in `439d9da` (2026-09-03 10:27 BST), so it is *probably* unaffected; Helios should confirm |
| U5 | `worktree-mhd` 2D runs between `c18c01c` (2026-08-31 19:23 BST) and `04636a6` (2026-09-01 19:19 BST) | **unclear** | The worktree had the old sign in that window. Out of scope for the top-level tree; listed so Helios can check |

### Not affected (3D only; outside the three labels)

| Entry | Reason |
|---|---|
| The 8 `examples/*.py` scripts above | All pass `dim=3`, so they use `_u_from_vort_3d` only |
| `examples/mhd_dissipation.csv` + `.png`, `examples/mhd_n48/mhd_dissipation.csv` + `.png` | Added in `552e2b9` (2026-08-30 00:07 BST). Produced by `aethon/runnable-mhd:examples/mhd_dissipation.py` with `dim=3`, `ic="tubes"` |
| `examples/smoke_monitors.csv` + `.png` | Added in `552e2b9`. Produced by `aethon/runnable-mhd:examples/smoke_plot.py` (`interactive_toy.py` is an alias) with `dim=3`, `ic="tubes"`, N=32 |
| About 40 hive note files that mention "2D" (`MHD*/`, `Lorentz/`, `Merge/`, `dissipation/`, `converged/`, `open/`) | Paper or X-framework text; apart from U4, none cite a top-level toy run |

**Counts: affected 4, sign-invariant 1, unclear 5.** No saved 2D result from the top-level `chive_ns` was found anywhere under `C:\Users\Akitt\Grok\`.

## Nested `ns/` clone (deliberately not fixed)

`C:\Users\Akitt\Grok\ns\chive_ns\grid.py` **still has the old sign** (`psi_hat = -vort_hat / grid["k2"]`). It was left unchanged on purpose, per NanoRibbon, because the clone has uncommitted local edits (on `main`, 8 commits behind). Anything run from `ns/` in 2D has the same bug.

## Side note (Venus, not fixed)

`k2 = kx**2 + ky**2 (+ kz**2) + 1e-12` (`grid.py:20, 25`): at k = 0, psi_hat = omega_hat/1e-12 is multiplied by k = 0, so the mean flow is dropped. That's harmless while the mean velocity is zero.
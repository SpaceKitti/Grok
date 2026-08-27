# C*Hive (`chive_ns`)

Small JAX spectral fluid solver. What actually runs is the Python package
`chive_ns/`. The folders `MHD/`, `MHD2/`, and `dissipation/` are research-note
dumps (hypotheses, paper maps, hive memos). They are **not** the simulator.

## What works today

- **Spectral Navier–Stokes** on a periodic box (the Clay torus), vorticity
  formulation, 2/3-rule dealiasing, RK2. 3D includes vortex stretching.
- **Oldroyd-B “clay”** extra-stress coupled to that vorticity stepper
  (`mode="clay"`).
- **Incompressible MHD** (`mode="mhd"`): same Fourier grid, induction equation
  for **B**, Lorentz force `curl(J × B)` on vorticity. 3D only. Guide-field
  orientation and η dials follow hypotheses in `MHD2/02` — treat them as
  starting points, not settled physics.
- Diagnostics: kinetic energy, enstrophy, max |ω|, BKM integral, helicity,
  and (MHD) magnetic energy, max |J|, div B residual, magnetic / cross helicity.

Initial conditions: smooth random, Taylor–Green, or Crow-perturbed
anti-parallel vortex tubes (`ic="tubes"`).

## Install

From a clone of this repo (Python 3.10+):

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

This pulls `jax`, `jaxlib`, `numpy`, and `matplotlib`. CPU JAX is enough for
the smokes below. A GPU JAX build is optional if you already use one.

You can also run examples without installing by staying at the repo root
(they add the parent path automatically).

## Smoke commands

Short CPU-friendly checks. First JAX compile of a 3D kernel takes a bit;
the step counts are tiny on purpose.

```bash
# Crow tubes, NS vs MHD (N=32)
python examples/compare_tubes_mhd.py

# Short run → CSV + PNG of energy, max |ω|, BKM (+ magnetic energy)
python examples/smoke_plot.py
python examples/interactive_toy.py          # same viz smoke
```

Heavier (not smokes): `examples/compare_tubes.py` and
`examples/compare_ns_clay.py` are N=64 reference comparisons.

## Modes (`run_framework`)

```python
from chive_ns import run_framework

ns   = run_framework(mode="vorticity", dim=3, N=32, steps=20, ic="tubes", force_on=False)
clay = run_framework(mode="clay",      dim=3, N=32, steps=20, ic="taylor_green", force_on=False)
mhd  = run_framework(mode="mhd",       dim=3, N=32, steps=20, ic="tubes", force_on=False,
                     mhd_params=dict(eta=1e-3, B0=0.08, b_guide="z"))
```

Safe MHD smoke defaults (from `MHD2/02`, hypotheses only): `b_guide="z"`
(spanwise / reconnection-plane), `η=1e-3`, `B0=0.08`, no clay coupling.

## Layout

| Path | Role |
|------|------|
| `chive_ns/` | Installable solver |
| `examples/` | Scripts, including smokes |
| `MHD/`, `MHD2/`, `dissipation/` | Research notes, not imported |

## MHD caveats

- 3D only; clay+MHD in one stepper is not wired yet.
- `div B` is projected every step; `max_divB` should stay at round-off.
- Low-N (32/48) current sheets are under-resolved — Ohmic ramps may be
  numerical. That is a known follow-up, not a bug in the smoke.

# Job N1: bubble versus radion

Folder: `C:\Users\Akitt\open-problems\N1_bubble_radion\`. No git. `run.py` generates `RESULTS.md`; source files are read-only.

Run: `$env:PYTHONIOENCODING='utf-8'; C:\Users\Akitt\Grok\.venv\Scripts\python.exe -B run.py`

## Scope

This is the cheap negative-modes-thread test from `UNIFYING_THREAD.md`: compare the conventional integrated Rayleigh–Plesset bubble static potential with Job 5b's radion potential. The only allowed map is `R = c r^α` with `c > 0`, `α ≠ 0`, plus a positive constant energy rescale. No multiplication by `r^β` is used.

The gas index is tested only at κ = 1 (isothermal; logarithmic gas term) and κ = 1.4 (adiabatic air). The run counts α and κ as the formal two algebraic knobs, while noting that κ is pinned physically and is not a free fitted knob.

## Post-run

- The standard integrated bubble potential was used because the supplied spec fixes the allowed map and pass rules but does not print a bubble-potential convention. α < 0 was allowed because “monotone” was not stated to mean increasing; restricting α > 0 only strengthens the failure.
- No complete power-and-sign map exists. The best κ = 1.4 candidate is α = −1: ambient r³ → flux R⁻³ and surface r² → curvature R⁻², but both signs disagree; the gas term maps to a positive power. κ = 1 has a logarithm.
- Blake requires negative ambient pressure, p∞ < 0. Under α = −1 it would land on the positive flux sign, so no radion term carries both the required sign and matched power. The negative curvature and C < 0 Casimir terms have the sign, with Casimir the collapse-side analogue, but the powers do not complete the map.
- Overall grade: FAIL under the fixed rule “FAIL if the powers do not match.”

## Sign-off

- Venus (maths): ______________________________
- Helios (physics): ____________________________

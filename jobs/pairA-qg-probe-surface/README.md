# pairA-qg-probe-surface

A QG probe on the Pair A surface, using the cut Γ, the 2π/4π flip and the inside/outside switch. It is built only from loaded, signed-off results.
- No new MHD Hamiltonian and no Einstein solver.
- No QG Hamiltonian is claimed, and no JT dual is claimed.
- C is held.

Run: `cd C:\Users\Akitt\pairA-qg-probe-surface; python run.py`. This writes RESULTS.md; use the venv Python `C:\Users\Akitt\Grok\.venv\Scripts\python.exe` if needed.

## Akitti's HAVE
- H_A (Pair A), Γ = [−ε_EP, ε_EP], with ε_EP = |a−b|/(2|v|) = 0.51368066 (loaded from the handoff and asserted, not hardcoded).
- Histories: A WRITE, B WRITE, C held.
- Jhat4 = I; 2π swap, 4π return.
- Loop starting inside Γ: the direction is ignored and loss picks the mode.
- Loop starting outside Γ, slow drive: the direction picks the mode.
- Circulation (Venus's correction): half a turn at each tip. That is π per loop around one tip and 2π for a loop around both. (This is what "circulations 1/2 + 1/2 at each EP" means.)

## Loaded (read-only; SHA-256 of every file checked before and after)
- `C:\Users\Akitt\pairA-qg-handoff\`: model (`seed.py`), Γ (`wick_lorentzian.py`), Jhat (`outputs/Jhat.npz`), histories and probe text.
- `C:\Users\Akitt\pairA-drive-return\`: `outputs/drive.npz` (start at 0.75 ε_EP) and `outputs/drive_start1p25.npz` (start at 1.25 ε_EP), plus RESULTS.md and RESULTS_start1p25.md.
- `C:\Users\Akitt\pairA-vortices-return\`: the sheet A/B convention.

## Files
- `load_surface.py`: loads the model and asserts ε_EP; file hashing; text search.
- `cover.py`: U_G[γ] = (−1)^{I(γ,Γ)}, with I counted as crossings of Γ itself, checked against Φ(n) = (−1)^n from eigenvalue tracking.
- `dictionary.py`: rows D1–D7, each tagged [by definition], [by construction] or [computed].
- `verdict.py`: prints exactly one verdict line.
- `run.py`: runs everything and writes RESULTS.md.

Crossing-count note (Venus): loops that start and end on Γ itself (figure-eight at ε=0, single-tip loops at 0.75 ε_EP) count leaving and returning as ONE crossing, not two or zero; cover.py already does this, as the Φ(n)=U_G match on all six loops shows. The figure-eight signed count is ±2 (both passes cross ε=0 the same way; its crossings at ±2ε_EP are outside Γ); parity is even either way.

## Definition of 'stall' (Akitti, 2026-09-25)

> stall = both EPs (±ε_EP). Real / Wick / Lorentzian chart dies there. D4 test: A and B are the two sheets that continue past those tips (labels swap on a 2π loop around a tip, return at 4π). C stays held. Use allowed_past_Wick: [A,B] as the same fact.

Definition sources for D4: Akitti's line above, together with handoff probe.py:44 `"allowed_past_Wick": ["A", "B"],` (the same fact, per Akitti). D4 is implemented in `stall.py` (Helios's two-detour test at each tip) and `dictionary.py`; tagged [computed] (definition supplied by Akitti). Added after the Venus/Helios sign-off; D4 pending Hive check.

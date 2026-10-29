# Hypercubic (square-lattice) reproduction check

Code and frozen specs only. Pushed from the shared box while TrinityOrb is offline, at Akitti's request (she asked to push what we can now).

## Verdicts (as relayed by NanoRibbon)
Against gates `specs/HYPERCUBIC_REPRO_GATES_FINAL.md` (1A723DCE) and boundary fix `specs/HYPERCUBIC_BOUNDARY_FIX_B1.md` (2BA983A1):

- G0: pass
- B0: pass
- G1: pass (static)
- G3: pass (rho ratio 0.9987)
- G2: pass (rho ratio 1.0022)
- G4: pass (rho ratio 1.0022452, h=0.001, 600 steps). Caveat from Helios: at these step sizes G4 cannot really fail, so it is a weak check.

## Notes
- Interior topological charge Q = -0.886 (L=24), about 7% under the ball fraction; likely clover O(a^2) error at rho=3a. This is a note, not a gate.
- `run_flow.py` produced G2/G3/G4 and imports `kernels.py` and `lattice.py`, which are not in this push.
- `run_G0.py` is the original periodic-box G0 script, written against the superseded spec FDF44325 (not included); the B1 open-box G0/B0/G1 rerun was done by `run_B1.py`.

## Results pending
The result JSONs (`out/B1.json`, `out/G0.json`, `out/G2.json`, `out/G3.json`, `out/G4.json`) are still on TrinityOrb and will be pushed when it is back online.

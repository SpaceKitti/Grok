# Hypercubic (square-lattice) reproduction check

Code, frozen specs, helpers and results. Code/specs first pushed in 0fe8ac5 while TrinityOrb was offline; results and helpers added once TrinityOrb was back online.

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
- `run_flow.py` produced G2/G3/G4 and imports them via `hc_open` -> `hc_kernel` -> `kernels.py` / `lattice.py` (both included).
- `run_G0.py` is the original periodic-box G0 script, written against the superseded spec FDF44325 (not included); the B1 open-box G0/B0/G1 rerun was done by `run_B1.py`.

## Results (`out/`)
- `out/B1.json` (sha256 bc5f9b24): B1 open-box rerun, G0/B0/G1 pass
- `out/G0.json` (0f75bada): G0 pass
- `out/G2.json` (76d757d2): G2 pass, ratio 1.0022
- `out/G3.json` (1f0c8015): G3 pass, ratio 0.9987
- `out/G4.json` (a331343b): G4 pass, ratio 1.0022452 (600/600 steps, finished on TrinityOrb 25 Oct 22:07:52 GMT). Helios caveat: G4 can't really fail at these step sizes.

Helpers: `kernels.py` (f07c0646), `lattice.py` (35e9e049).

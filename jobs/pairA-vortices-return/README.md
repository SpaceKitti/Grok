# pairA-vortices-return

Tests whether the dual vortices at the two tips (±ε_EP) of Pair A bring a path back to the real chart.
Tracks the path (ε, λ±) continuously, not just labels. C held fixed (not used).

Run:
```
cd C:\Users\Akitt\pairA-vortices-return
python run.py        # or C:\Users\Akitt\Grok\.venv\Scripts\python.exe run.py (numpy 2.5.2, matplotlib 3.11.1)
```

## Inputs — all taken from C:\Users\Akitt\pairA-qg-handoff (imported read-only, no bytecode written there)

| object | source (file / function) |
|---|---|
| H_A(ε) = [[−i a, ε v],[ε v, −i b]], a=0.12337, b=0.49348, v=−0.360253 | `seed.py` : `H_A`, constants `A`,`B`,`V` |
| λ± (eigenvalues of H_A) | `numpy.linalg.eig(seed.H_A(ε))`, as in `tracker.py`/`gauge_J.py`; λ± − λ_EP = ±y/2, y² = 4v²(ε²−ε_EP²) (`seed.y_of_eps`) |
| ε_EP = \|a−b\|/(2\|v\|) = 0.51368066… (b>a in this handoff) (EPs at ±ε_EP) | `seed.py` : `EPS_EP` (check `seed.ep_condition`); tips also in `r0_bolts.py`, `jump_on_cut.jordan_at` |
| λ_EP = −i(a+b)/2 | `seed.py` : `LAM_EP`; here re-evaluated at each core as tr H_A(core)/2 (`vortices.lam_ep_at`) |
| Γ = [−ε_EP, ε_EP] (real chart / real-section support) | `wick_lorentzian.py` : `chart()["real_section_support"]`; also `probe.probe2`, RESULTS.md "real-section support = Γ" |
| Jhat2, Jhat4 | `outputs/Jhat.npz` (keys `Jhat2`,`Jhat4`), produced by `gauge_J.run_strip()` (loop ε_EP+0.25ε_EP e^{iθ}, 0→4π); re-run here as a check |
| sheet tracking rule | `tracker.py` : `align_evals` (nearest-distance pair matching) |
| sheets A, B | handoff `histories.py` A = upper lip of Γ (Im I = −0.2986), B = conjugate/lower lip (Im I = +0.2986). Here: sheet A := λ_EP + y/2, sheet B := λ_EP − y/2 with the handoff cut on Γ, y = 2v√(ε−ε_EP)√(ε+ε_EP); on the upper lip y = 2iv√(ε_EP²−ε²), whose ∫ over Γ is iπvε_EP² = −0.2986i = history A. |

## Files
- `vortices.py` — imports the model from the handoff; circulation Δarg(λ−λ_EP(core)); physics checks (gap exponent, eigenvector overlap, Hermiticity).
- `tracks.py` — continuous tracking along ε paths (4000 steps per turn); circle and figure-eight paths.
- `return_test.py` — branch-cut label functions (Γ segment; outward rays), loop reports for T4.
- `run.py` — runs everything, writes `outputs/tracks.npz`, `outputs/tracks_vs_theta.png`, `RESULTS.md`.

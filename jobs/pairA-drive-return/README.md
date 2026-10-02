# pairA-drive-return

Two-mode toy: drive a state in time around the +ε_EP tip of Pair A (i dψ/dt = H_A(ε(t))ψ), and run a path that starts on Γ and does the figure-eight. Question: does anything return onto the cut? C held.

Run: `cd C:\Users\Akitt\pairA-drive-return; python run.py`  (Python 3.14, numpy 2.5.2, matplotlib 3.11.1).

## Inputs (imported read-only; nothing written to these folders, bytecode disabled)
| object | source |
|---|---|
| H_A(ε) = [[−ia, εv],[εv, −ib]], a, b, v | `C:\Users\Akitt\pairA-qg-handoff\seed.py` (`H_A`, `A`, `B`, `V`) via `pairA-vortices-return\vortices.py` |
| ε_EP = \|a−b\|/(2\|v\|) (b>a here), λ_EP = −i(a+b)/2 | handoff `seed.EPS_EP`, `seed.LAM_EP` |
| Γ = [−ε_EP, ε_EP] | handoff `wick_lorentzian.chart()` via `vortices.GAMMA`, `vortices.in_gamma` |
| sheet A = λ_EP + y/2, sheet B = λ_EP − y/2, Γ-segment cut (upper-lip reading) | `C:\Users\Akitt\pairA-vortices-return\return_test.py` (`y_cut_gamma`) |
| continuous eigenvalue tracking, figure-eight path | `pairA-vortices-return\tracks.py` (`track`, `figure_eight`) |

## Files
- `drive.py`: loop ε(t) = ε_EP + r e^{i(±ωt+π)} (r = 0.25 ε_EP; start/end 0.75 ε_EP inside Γ). Uses an exact 2x2 exponential with midpoint H', where H' = H_A + i(a+b)/2 has the shared decay removed. ψ is renormalised every step. Weights come from the left and right eigenvectors, c = R⁻¹ψ. Also contains the fixed-ε relaxation check and the γT = 0.01 sanity run.
- `on_cut.py`: path starting on Γ (ε = 0 and ε = 0.75 ε_EP), along Γ, figure-eight around both tips, back along Γ.
- `run.py`: 8 driven runs (±ω × γT ∈ {40, 1} × start A/B) plus a dt-halving convergence check. Writes `outputs/drive.npz`, `outputs/weights_vs_theta.png`, `RESULTS.md`.

## References (C:\Users\Akitt\Grok\pdf\)
- 1410.1882: Milburn et al., quasiadiabatic dynamics near EPs (`1410.1882_Milburn_quasiadiabatic_dynamics_near_EPs.pdf`)
- 1706.09938: Hassan et al., exact driven 2x2 evolution when encircling an EP (`1706.09938_Hassan_EP_encircling_exact_evolution_polarization.pdf`)
- 1603.02325: Doppler et al., EP encircling / mode switching (`1603.02325_Doppler_EP_encircling_mode_switching.pdf`)

These are cited as background only. The results here were NOT checked against these papers, and no agreement is claimed.

Start-point option: `python run.py --start 1.25` runs the loop from 1.25 ε_EP (outside Γ) and writes `RESULTS_start1p25.md`, `outputs/drive_start1p25.npz`, `outputs/drive_start1p25_swapab.npz`, `outputs/weights_vs_theta_start1p25.png` (code: `start_other.py`); plain `python run.py` (default 0.75) reproduces the signed-off `RESULTS.md`.

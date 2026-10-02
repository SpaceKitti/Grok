# pairA-drive-sweep — D6/D7 region sweep

**Signed off 2026-09-25:** Venus (maths) and Helios (physics).

Question: do the D6 behaviour (loss picks the mode, direction ignored) and the D7 behaviour (direction picks the mode, cw and ccw opposite) line up with inside Γ (F_JT = ε² − ε_EP² < 0) and outside Γ (F_JT > 0) for all start points, not just 0.75 and 1.25 ε_EP?

Run: `python run.py` (Grok\.venv python, PYTHONIOENCODING=utf-8). Writes RESULTS.md and outputs/sweep.npz.

## Loaded, read-only (SHA-256 of every file before and after)
- C:\Users\Akitt\pairA-drive-return — `drive.py` imported as is: H_A (via its imports), the exact 2×2 propagator `expm2`, `run_drive`, `sheet_basis`, `decompose`, the shared-decay shift and the step rule (γ dt ≤ 0.01, ≥ 2000 steps per turn). H_A is NOT rebuilt.
- C:\Users\Akitt\pairA-vortices-return and C:\Users\Akitt\pairA-qg-handoff — imported indirectly by drive.py (H_A, sheet convention, tracking).
- Only in-memory module attributes of drive.py are set per start point (loop radius, centre, phase); no file is changed.

## Loop convention (fixed before running)
- ε(θ) = p + r e^{i(sθ + φ₀)}, s = +1 ccw, s = −1 cw (counter-clockwise in the complex ε plane), p = +ε_EP or −ε_EP (the encircled tip).
- The loop passes through the start point on the real axis: r = |ε_start − p|, φ₀ = 0 if ε_start is on the far side of the tip (|ε_start| > ε_EP), φ₀ = π if on the near side (|ε_start| < ε_EP). For starts 0.75 and 1.25 ε_EP around +ε_EP this is exactly drive-return's loop (r = 0.25 ε_EP, φ₀ = π / 0). Other starts need a different radius (the loop must pass through the start and circle the tip): 0.25 → r = 0.75, 0.50 → 0.50, 1.10 → 0.10, 1.50 → 0.50 (× ε_EP). No loop around one tip reaches the other tip (r < 2 ε_EP).
- Mirror convention for −ε_EP: start points −0.25, −0.50, −0.75, −1.00, −1.10, −1.25, −1.50 × ε_EP, loop around −ε_EP, same orientation convention (ccw = counter-clockwise in the ε plane). Corrected 2026-09-25 (Venus/Helios): ε → −ε is a rotation by π (orientation-preserving) and H_A(−ε) = D H_A(ε) D, D = diag(1,−1); so ccw ↔ ccw, matching the table [standard + computed]. (The earlier note here said the mirror reverses orientation; that was wrong.)
- Start 1.00 × ε_EP (on Γ's end point) IS the EP: r = 0, H_A is defective there (no eigenbasis to start in). It is reported as FAIL (degenerate) and not run. The on-Γ row counts as neither interior nor exterior.
- Drive speeds: slow γT = 20, 40, 100 (as D7: γT ≳ 20), T = γT/γ, γ = |a−b|/2; 2 turns; start in the pure eigenvector of sheet A or B at the start point.

## Quantities per start
- F_JT sign at the start point.
- Shared frequency vs shared decay: from the H_A eigenvalues at the start, |ΔRe λ| vs |ΔIm λ| (shared frequency if |ΔRe λ| < 1e-9·|Δλ|; shared decay if |ΔIm λ| < 1e-9·|Δλ|; else neither).
- Winner at 2π and 4π = eigenvector (at the start point, which is also the recording point) with the larger left-eigenvector weight (drive-return's `decompose`), named physically: slower-/faster-decaying when decays differ, higher-/lower-frequency when frequencies differ.

## Classification (fixed before running)
For each start point, over all slow speeds γT ∈ {20, 40, 100}, both turns (2π, 4π), both start sheets (A, B):
- **D6-like** (loss picks, direction ignored): ccw and cw give the same winner for every start sheet, the winner is the same for both start sheets, and every winner weight w ≥ 0.9.
- **D7-like** (direction picks): ccw and cw give different winners for every start sheet, each direction's winner is the same for both start sheets, and every winner weight w ≥ 0.9.
- **MIXED**: any other pattern (including w < 0.9 anywhere).
- **FAIL**: the run cannot be done or is numerically invalid (degenerate start at the EP, NaN, or dt-halving at γT = 40 changes a weight by more than 1e-3).

## Verdict (fixed before running)
'REGION MAP YES' if all six interior starts (±0.25, ±0.50, ±0.75) are D6-like and all six exterior starts (±1.10, ±1.25, ±1.50) are D7-like; otherwise 'REGION MAP NO' with the reason. The on-Γ starts (±1.00) are reported but not counted.

Scope: two-mode toy; A and B WRITE, C held (C is not in H_A's 2×2 dynamics). No GoldbergHexa; nothing about S² enters here.

## Added after the first run (post hoc; the criteria above are unchanged)
- `diag_dt.py`: dt-convergence diagnostic for the interior starts at γT = 40 (dt refined ×1, ×2, ×4, ×8). It writes outputs/diag_dt.json, and run.py adds it to RESULTS.md under 'Post-hoc diagnostics (not used in the verdict)'. Run it before run.py to include it.

- `python run.py --from-saved`: rebuilds RESULTS.md from outputs/sweep.npz, outputs/dw.json (per-start dt-halving maxima; for the 2026-09-25 run extracted from its RESULTS.md) and outputs/diag_dt.json without running any drive.

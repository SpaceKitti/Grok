**Signed off 2026-09-25:** Venus (maths) and Helios (physics) on D1–D7 and cover.

# pairA-qg-probe-surface — RESULTS

QG probe on the Pair A surface using the cut Γ, the 2π/4π flip and the inside/outside switch. Two-mode toy; no new MHD Hamiltonian, no Einstein solver. No QG Hamiltonian was found and none is claimed; no JT dual is claimed.

## Verdict

SURFACE READY — QG probe may use D1–D7

Meaning: the surface has these properties [standard]; reading them as QG is [hive-interpretation].

Failed rows: none (no row was fudged).

## Definition of 'stall' (Akitti, 2026-09-25)

> stall = both EPs (±ε_EP). Real / Wick / Lorentzian chart dies there. D4 test: A and B are the two sheets that continue past those tips (labels swap on a 2π loop around a tip, return at 4π). C stays held. Use allowed_past_Wick: [A,B] as the same fact.

Handoff source for the same fact (per Akitti): probe.py:44 `"allowed_past_Wick": ["A", "B"],`.

## Dictionary D1–D7

Tags (Venus): [by definition] / [by construction] carry no new information; [computed] rows carry information. As surface properties, D1–D7 are [standard] non-Hermitian two-mode physics; using them as a QG dictionary is [hive-interpretation].

| row | property | result | tag | information? | conditions | evidence |
|---|---|---|---|---|---|---|
| D1 | real chart only on Γ | **PASS** | [by definition] | no | 'real chart' = the handoff's chart, which the handoff places on Γ = [−ε_EP, ε_EP] | handoff: probe.py:43 `"real_chart_support": "Γ only",`; probe.py:79 `lines.append(f"real chart support: {p2['real_chart_support']}")`; run.py:52 `print(f"  real-section support = {w['real_section_support']}")`; wick_lorentzian.py:1 `"""Layer W — Lorentzian/real chart only on Γ. Dies at ±ε_EP."""`; wick_lorentzian.py:26 `"real_section_support": "Γ=[-ε_EP, ε_EP]",`. Computed fact (not hidden): for real ε inside Γ, λ−λ_EP is purely imaginary (max |Re| = 1.3e-16 over 21 points); outside Γ it is real (max |Im| = 1.7e-16 over 20 points). Real eigenvalue differences live OUTSIDE Γ; inside Γ the two modes share a frequency and differ in decay. |
| D2 | dies at both EPs | **PASS** | [computed] | yes (computed) | circles r = 0.25, 0.1, 0.03, 0.01 ε_EP around each EP; gap = mean |λ+−λ−| on the circle; overlap = normalised |<v+|v−>| | +ε_EP: gap exponent 0.5003, overlap 0.7772, 0.9047, 0.9704, 0.9900 → 1.000000 at the EP (gap 6.8e-09); −ε_EP: exponent 0.5003, overlap 0.7772, 0.9047, 0.9704, 0.9900 → 1.000000 (gap 6.8e-09). r^(1/2) and merging eigenvectors at both EPs. |
| D3 | 4π return of labels | **PASS** | [computed, known] | yes (computed) | continuous eigenvalue tracking on circles r = 0.25 ε_EP around each EP (this run); handoff Jhat from outputs/Jhat.npz | one turn: swap (n=1) at +ε_EP and −ε_EP for A and B; two turns: return (n=0); handoff ‖Jhat4−I‖ = 9.8e-16, ‖Jhat2−I‖ = 2.000. Known result (2π swap, 4π return), re-confirmed. |
| D4 | A and B allowed past the stall (stall = both EPs ±ε_EP, Akitti 2026-09-25) | **PASS** | [computed, equivalent to 2π swap] (definition supplied by Akitti) | no (same fact as the one-tip 2π swap, read along an open path) | at each tip: (a) Helios two-detour test, semicircles r = 0.25 ε_EP just above / just below the tip from ±0.75 to ±1.25 ε_EP, continuous tracking (handoff align_evals, 8000 steps), PASS only if the pairings are swapped; (b) 2π swap / 4π return from the cover loops and handoff Jhat; (c) only A and B continue, C files unchanged (SHA-256); (d) probe.py:44 allowed_past_Wick [A, B] cited as the same fact | Definition (Akitti, 2026-09-25, verbatim): "stall = both EPs (±ε_EP). Real / Wick / Lorentzian chart dies there. D4 test: A and B are the two sheets that continue past those tips (labels swap on a 2π loop around a tip, return at 4π). C stays held. Use allowed_past_Wick: [A,B] as the same fact." Handoff definition source, same fact per Akitti: probe.py:44 `"allowed_past_Wick": ["A", "B"],`; probe.py:89 `lines.append(f"allowed past Wick: {', '.join(p2['allowed_pas`. +ε_EP: (a) start +0.75 ε_EP (inside Γ) → end +1.25 ε_EP (outside Γ), semicircle r = 0.25 ε_EP; above (Im ε>0): A → lower-frequency mode, B → higher (labels at the end point: A stays A, B stays B); below (Im ε<0): A → higher, B → lower (A arrives on sheet B, B on sheet A); pairings swapped: YES; above ∘ reversed below = one closed loop around the tip (winding -1); end modes Re λ = +0.138791 (higher), -0.138791 (lower), |Im(λA−λB)| at end 1.7e-16; tracking jump ratio 1.2e-04. (b) 2π loop: n_A = 1, n_B = 1 (swap); 4π: n_A = 0, n_B = 0 (return). (c) only the two sheets A, B of the 2x2 H_A are continued; C files unchanged: YES. (d) probe.py:44 allowed_past_Wick [A, B] cited above: YES. −ε_EP: (a) start -0.75 ε_EP (inside Γ) → end -1.25 ε_EP (outside Γ), semicircle r = 0.25 ε_EP; above (Im ε>0): A → higher-frequency mode, B → lower (labels at the end point: A stays A, B stays B); below (Im ε<0): A → lower, B → higher (A arrives on sheet B, B on sheet A); pairings swapped: YES; above ∘ reversed below = one closed loop around the tip (winding +1); end modes Re λ = +0.138791 (higher), -0.138791 (lower), |Im(λA−λB)| at end 5.6e-17; tracking jump ratio 1.2e-04. (b) 2π loop: n_A = 1, n_B = 1 (swap); 4π: n_A = 0, n_B = 0 (return). (c) only the two sheets A, B of the 2x2 H_A are continued; C files unchanged: YES. (d) probe.py:44 allowed_past_Wick [A, B] cited above: YES. Route dependence: the route that stays on the upper lip (above) keeps the start labels (A ends as sheet A, B as sheet B); the route below crosses to the other lip and the labels arrive swapped, so which outside-Γ mode A lands on is set by the side of the tip it passes, and the two answers differ by exactly one 2π loop around the tip. Handoff ‖Jhat4−I‖ = 9.8e-16, ‖Jhat2−I‖ = 2.000. C-related files (6) unchanged: YES. Note (Venus): which pairing counts as 'A continues to A' is a choice set by the cut; the only choice-independent fact is that the two detours disagree by exactly one swap. The gap stays open along both detours (they never touch the tip): min |λA−λB| over all four detours = 0.244805 (at +ε_EP: 0.244805, at −ε_EP: 0.244805; > 0), and that is what makes 'allowed past' true. The results at the two tips mirror each other (going above −ε_EP behaves like going below +ε_EP) because of the ε → −ε symmetry of H_A (σz); expected, not an error (computed: max ‖σz H_A(ε) σz − H_A(−ε)‖ = 0.0e+00 at 4 complex ε). Scope [careful-before-toy]: D4 is about the eigenvalue sheets with ε moved by hand. A driven state taken past a tip is covered by D6 and D7, where the direction of travel and the loss decide the outcome, not the sheet label. All parts (a)–(d) pass at both tips. |
| D5 | C held | **PASS** | [by construction] | no | this probe never writes C or any handoff file; checked by SHA-256 before/after | C-related handoff files (6): RESULTS.md, RESULTS_probe.md, histories.py, summary.json, probe.py, run.py — unchanged: YES. Handoff status: C imaginary cap NOT-SELECTED, 'held: C' (RESULTS_probe.md). |
| D6 | loop starting inside Γ at 0.75ε_EP: the direction of travel is ignored (loss picks the mode) | **PASS** | [computed] | yes (computed) | loop r = 0.25 ε_EP around +ε_EP, start/end 0.75 ε_EP (inside Γ), γT = 1, 20, 40, 100; left-eigenvector weights. The loop straddles the tip (it also passes 1.25 ε_EP outside Γ); no driven loop lies entirely inside or outside Γ | drive-return outputs/drive.npz: fast: 2π ccw/cw from A → A/A, from B → B/B, 4π ccw/cw from A → B/B, from B → B/B; slow20: 2π ccw/cw from A → B/B, from B → B/B, 4π ccw/cw from A → B/B, from B → B/B; slow40: 2π ccw/cw from A → B/B, from B → B/B, 4π ccw/cw from A → B/B, from B → B/B; slow100: 2π ccw/cw from A → B/B, from B → B/B, 4π ccw/cw from A → B/B, from B → B/B. Slower-decaying mode at 0.75 ε_EP = sheet B. RESULTS.md: **missing mechanism: NO** — Signed off: Venus (maths), Helios (physics), 2026-09-25 |
| D7 | loop starting outside Γ at 1.25ε_EP, slow drive (γT≳20): the direction picks the mode (cw and ccw pick opposite modes) | **PASS** | [computed] | yes (computed) | r = 0.25 ε_EP, start/end 1.25 ε_EP (outside Γ), slow drive: the direction picks the mode cleanly from about γT ≈ 20 (w = 0.99699 at γT = 20, 0.99937 at 40, 0.99991 at 100), only partially at γT = 5 (a lean of about 91/9), and not at γT = 1. The loop straddles the tip (it crosses Γ at 0.75 ε_EP); no driven loop lies entirely inside or outside Γ | drive-return outputs/drive_start1p25.npz (winners from start A/B): fast: 2π ccw → A/B (w 0.94027), cw → A/B, 4π ccw → A/B (w 0.83721), cw → A/B [direction-dependent: NO]; mid5: 2π ccw → A/A (w 0.92008), cw → B/B, 4π ccw → A/A (w 0.91014), cw → B/B [direction-dependent: YES]; slow20: 2π ccw → A/A (w 0.99699), cw → B/B, 4π ccw → A/A (w 0.99699), cw → B/B [direction-dependent: YES]; slow40: 2π ccw → A/A (w 0.99937), cw → B/B, 4π ccw → A/A (w 0.99937), cw → B/B [direction-dependent: YES]; slow100: 2π ccw → A/A (w 0.99991), cw → B/B, 4π ccw → A/A (w 0.99991), cw → B/B [direction-dependent: YES]. Higher-frequency mode at 1.25 ε_EP = sheet B. RESULTS_start1p25.md: **missing mechanism (start 1.25 ε_EP): YES** — **Signed off 2026-09-25:** Venus (maths) and Helios (physics). |

## D4 detail: two-detour test at each tip

Start on real ε inside Γ with A = λ_EP + y/2, B = λ_EP − y/2 (upper-lip convention); semicircle r = 0.25 ε_EP around the tip to real ε outside Γ; continuous tracking.

| tip | route | start → end (ε/ε_EP) | A lands on | B lands on | A, B labels at end | (a) swapped | (b) 2π/4π | (c) C held | (d) allowed_past_Wick | tip PASS |
|---|---|---|---|---|---|---|---|---|---|---|
| +ε_EP | above | +0.75 → +1.25 | lower-frequency | higher-frequency | A, B | YES | YES | YES | YES | **YES** |
| +ε_EP | below | +0.75 → +1.25 | higher-frequency | lower-frequency | B, A | YES | YES | YES | YES | **YES** |
| −ε_EP | above | -0.75 → -1.25 | higher-frequency | lower-frequency | A, B | YES | YES | YES | YES | **YES** |
| −ε_EP | below | -0.75 → -1.25 | lower-frequency | higher-frequency | B, A | YES | YES | YES | YES | **YES** |

## Cover check: U_G[γ] = (−1)^{I(γ,Γ)} vs Φ(n) = (−1)^n

I = number of crossings of the discretised loop (8000 steps per turn) with the segment Γ = [−ε_EP, ε_EP] itself (not an outward-ray cut), mod 2 for U_G. n = sheet index change from continuous eigenvalue tracking along the loop (handoff tracker.align_evals nearest-distance matching): 0 = return, 1 = swap. Start sheets A/B = vortices-return convention (A = λ_EP + y/2, B = λ_EP − y/2, Γ-segment cut). Φ(0) = +1, Φ(1) = −1.

| loop | start ε/ε_EP | winding (+ε_EP, −ε_EP) | I (unsigned) | signed count | crossing points x/ε_EP | U_G | n_A | n_B | Φ(n_A) | Φ(n_B) | Φ = U_G for A and B | tracking jump ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| +EP once (circle r=0.25 eps_EP, start 1.25 eps_EP, ccw) | +1.2500 | (+1, +0) | 1 | -1 | +0.7500 | -1 | 1 | 1 | -1 | -1 | **YES** | 2.5e-04 |
| -EP once (circle r=0.25 eps_EP, start -1.25 eps_EP, ccw) | -1.2500 | (+0, +1) | 1 | +1 | -0.7500 | -1 | 1 | 1 | -1 | -1 | **YES** | 2.5e-04 |
| +EP twice (same circle, 4pi) | +1.2500 | (+2, +0) | 2 | -2 | +0.7500, +0.7500 | +1 | 0 | 0 | +1 | +1 | **YES** | 2.5e-04 |
| -EP twice (same circle, 4pi) | -1.2500 | (+0, +2) | 2 | +2 | -0.7500, -0.7500 | +1 | 0 | 0 | +1 | +1 | **YES** | 2.5e-04 |
| figure-eight (lemniscate, foci +-eps_EP, lobes opposite senses, start sqrt2 eps_EP) | +1.4142 | (+1, -1) | 2 | -2 | -0.0000, +0.0000 | +1 | 0 | 0 | +1 | +1 | **YES** | 7.9e-04 |
| big loop around both (circle r=2 eps_EP, start 2 eps_EP) | +2.0000 | (+1, +1) | 0 | +0 | — | +1 | 0 | 0 | +1 | +1 | **YES** | 5.2e-04 |

All loops: Φ(n) = U_G for A and B: **YES**.
Figure-eight: unsigned count 2, signed count -2 (same parity, even → U_G = +1). Both passes cross Γ at ε = 0 in the same vertical direction, so the signed count here is ±2, not 0: Γ ends at the tips, and a loop around one tip meets it once, with sign set by the direction of travel; the two lobes run in opposite senses but each crosses Γ downward. Only the parity enters U_G.

## Loaded inputs (read-only) and unchanged check

- Handoff `C:\Users\Akitt\pairA-qg-handoff`: seed.H_A, seed.A/B/V, seed.EPS_EP (asserted = |a−b|/(2|v|) = 0.513680663312; agrees with 0.51368066 to 3.3e-09), seed.LAM_EP, tracker.align_evals, wick_lorentzian.chart() (Γ), outputs/Jhat.npz (Jhat2, Jhat4), text of RESULTS.md / RESULTS_probe.md / probe.py / histories.py for D1, D4, D5.
- Drive-return `C:\Users\Akitt\pairA-drive-return`: outputs/drive.npz (0.75 ε_EP start, D6), outputs/drive_start1p25.npz (1.25 ε_EP start, D7), RESULTS.md and RESULTS_start1p25.md (verdict and sign-off lines). No drive was re-run.
- Vortices-return `C:\Users\Akitt\pairA-vortices-return`: sheet A/B convention (return_test.y_cut_gamma, re-implemented identically in load_surface.y_cut_gamma); searched for 'stall'.
- SHA-256 of every file in the three folders (57 files) before any import and after all computations: **unchanged**.

## Scope

Two-mode toy (H_A is 2x2). The dictionary rows are properties of this non-Hermitian surface; reading them as QG is [hive-interpretation]. No QG Hamiltonian was found or claimed; no JT dual is claimed. C stays held (never written).


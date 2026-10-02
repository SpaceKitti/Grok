# pairA-drive-sweep — RESULTS

**Signed off 2026-09-25:** Venus (maths) and Helios (physics).

D6/D7 region sweep on the Pair A two-mode toy. H_A, the propagator and the driver are imported read-only from pairA-drive-return (not rebuilt). Classification criteria and loop convention were fixed in README.md before running. A and B WRITE, C held (not in the 2×2 dynamics).

## Verdict

**REGION MAP NO under the pre-fixed w ≥ 0.9 at γT = 40 rule. At the winner level, every converged start matches: interior D6-like (same winner both ways) and exterior D7-like.**

(Rule as fixed in README.md: w ≥ 0.9 at every slow speed γT = 20, 40, 100, with the dt-halving check at γT = 40. The interior weights fall below 0.9 at γT = 20 and 40; at γT = 100 they are all ≥ 0.9998.)

Rule-level detail: REGION MAP NO — not matching: +ε_EP 0.25 (interior: FAIL); +ε_EP 0.50 (interior: MIXED); +ε_EP 0.75 (interior: MIXED); −ε_EP 0.25 (interior: FAIL); −ε_EP 0.50 (interior: MIXED); −ε_EP 0.75 (interior: MIXED).

Physics reading: the interior starts that converge are D6 in the winner-and-direction sense at every speed; the w rule fails because loss selection is incomplete at γT ≤ 40 [computed]. cw = ccw weights at interior starts follow from M_cw = M_ccwᵀ (complex-symmetric H_A) [standard + computed].

Computed support: converged interior starts (±0.50, ±0.75) have one winner (slower-decaying) for every speed, turn, direction and start sheet: True; max |w_ccw − w_cw| over them = 8.5e-05; max |H_Aᵀ − H_A| = 0.0e+00 at 6 complex ε. Exterior starts: all D7-like, all converged.

The on-Γ starts (±1.00 ε_EP) are reported but not counted as interior or exterior.

## Summary table

| tip | start ε/ε_EP | region | loop r/ε_EP, phase | F_JT sign | eigenvalues at start | ccw vs cw winner (γT = 40, 4π; from A / from B) | class | reason |
|---|---|---|---|---|---|---|---|---|
| +ε_EP | +0.25 | interior | 0.75, π | − (-0.24738) | shared frequency (decays differ): λ_A = 0.00000-0.48760j, λ_B = 0.00000-0.12925j | from A: ccw slower-decaying (0.7851), cw slower-decaying (0.7235); from B: ccw slower-decaying (0.6986), cw slower-decaying (0.6363) | **FAIL** | numerics (NaN or dt-halving change > 1e-3) [numerical FAIL, cause not established; careful-before-toy]; not a physical boundary |
| +ε_EP | +0.50 | interior | 0.50, π | − (-0.19790) | shared frequency (decays differ): λ_A = 0.00000-0.46869j, λ_B = 0.00000-0.14816j | from A: ccw slower-decaying (0.8139), cw slower-decaying (0.8139); from B: ccw slower-decaying (0.6984), cw slower-decaying (0.6984) | **MIXED** | min w = 0.698 < 0.9 |
| +ε_EP | +0.75 | interior | 0.25, π | − (-0.11544) | shared frequency (decays differ): λ_A = 0.00000-0.43083j, λ_B = 0.00000-0.18602j | from A: ccw slower-decaying (0.8064), cw slower-decaying (0.8064); from B: ccw slower-decaying (0.6951), cw slower-decaying (0.6951) | **MIXED** | min w = 0.677 < 0.9 |
| +ε_EP | +1.00 | on Γ (end point) | r = 0 | 0 (F_JT = +0.0e+00) | EP (both merge) | — | **FAIL** | degenerate: the start is the EP itself (r = 0; eigenvalues -0.000000-0.308425j, 0.000000-0.308425j coincide to 6.8e-09; H_A defective, no eigenbasis to start in); not run |
| +ε_EP | +1.10 | exterior | 0.10, 0 | + (+0.05541) | shared decay (frequencies differ): λ_A = -0.08480-0.30843j, λ_B = 0.08480-0.30842j | from A: ccw lower-frequency (0.9979), cw higher-frequency (0.9979); from B: ccw lower-frequency (0.9979), cw higher-frequency (0.9979) | **D7-like** | ccw ≠ cw for both start sheets, each direction start-sheet independent, all w ≥ 0.9 |
| +ε_EP | +1.25 | exterior | 0.25, 0 | + (+0.14843) | shared decay (frequencies differ): λ_A = -0.13879-0.30843j, λ_B = 0.13879-0.30843j | from A: ccw lower-frequency (0.9994), cw higher-frequency (0.9994); from B: ccw lower-frequency (0.9994), cw higher-frequency (0.9994) | **D7-like** | ccw ≠ cw for both start sheets, each direction start-sheet independent, all w ≥ 0.9 |
| +ε_EP | +1.50 | exterior | 0.50, 0 | + (+0.32983) | shared decay (frequencies differ): λ_A = -0.20690-0.30842j, λ_B = 0.20690-0.30843j | from A: ccw lower-frequency (0.9998), cw higher-frequency (0.9998); from B: ccw lower-frequency (0.9998), cw higher-frequency (0.9998) | **D7-like** | ccw ≠ cw for both start sheets, each direction start-sheet independent, all w ≥ 0.9 |
| −ε_EP | -0.25 | interior | 0.75, 0 | − (-0.24738) | shared frequency (decays differ): λ_A = 0.00000-0.48760j, λ_B = 0.00000-0.12925j | from A: ccw slower-decaying (0.8443), cw slower-decaying (0.8443); from B: ccw slower-decaying (0.6909), cw slower-decaying (0.6909) | **FAIL** | numerics (NaN or dt-halving change > 1e-3) [numerical FAIL, cause not established; careful-before-toy]; not a physical boundary |
| −ε_EP | -0.50 | interior | 0.50, 0 | − (-0.19790) | shared frequency (decays differ): λ_A = 0.00000-0.46869j, λ_B = 0.00000-0.14816j | from A: ccw slower-decaying (0.8139), cw slower-decaying (0.8139); from B: ccw slower-decaying (0.6986), cw slower-decaying (0.6986) | **MIXED** | min w = 0.699 < 0.9 |
| −ε_EP | -0.75 | interior | 0.25, 0 | − (-0.11544) | shared frequency (decays differ): λ_A = 0.00000-0.43083j, λ_B = 0.00000-0.18602j | from A: ccw slower-decaying (0.8064), cw slower-decaying (0.8064); from B: ccw slower-decaying (0.6951), cw slower-decaying (0.6951) | **MIXED** | min w = 0.677 < 0.9 |
| −ε_EP | -1.00 | on Γ (end point) | r = 0 | 0 (F_JT = +0.0e+00) | EP (both merge) | — | **FAIL** | degenerate: the start is the EP itself (r = 0; eigenvalues -0.000000-0.308425j, 0.000000-0.308425j coincide to 6.8e-09; H_A defective, no eigenbasis to start in); not run |
| −ε_EP | -1.10 | exterior | 0.10, π | + (+0.05541) | shared decay (frequencies differ): λ_A = 0.08480-0.30842j, λ_B = -0.08480-0.30843j | from A: ccw lower-frequency (0.9979), cw higher-frequency (0.9979); from B: ccw lower-frequency (0.9979), cw higher-frequency (0.9979) | **D7-like** | ccw ≠ cw for both start sheets, each direction start-sheet independent, all w ≥ 0.9 |
| −ε_EP | -1.25 | exterior | 0.25, π | + (+0.14843) | shared decay (frequencies differ): λ_A = 0.13879-0.30843j, λ_B = -0.13879-0.30843j | from A: ccw lower-frequency (0.9994), cw higher-frequency (0.9994); from B: ccw lower-frequency (0.9994), cw higher-frequency (0.9994) | **D7-like** | ccw ≠ cw for both start sheets, each direction start-sheet independent, all w ≥ 0.9 |
| −ε_EP | -1.50 | exterior | 0.50, π | + (+0.32983) | shared decay (frequencies differ): λ_A = 0.20690-0.30843j, λ_B = -0.20690-0.30842j | from A: ccw lower-frequency (0.9998), cw higher-frequency (0.9998); from B: ccw lower-frequency (0.9998), cw higher-frequency (0.9998) | **D7-like** | ccw ≠ cw for both start sheets, each direction start-sheet independent, all w ≥ 0.9 |

## Full winners (every slow speed, both turns)

Format: start sheet: ccw → winner label, physical name (weight), cw → … . Labels A/B are the sheets at the start point (= recording point).

### +ε_EP, start +0.25 ε_EP (interior): FAIL [numerical FAIL, cause not established; careful-before-toy]; not a physical boundary
- loop: r = 0.75 ε_EP around +ε_EP, min |λ₊−λ₋| on the loop = 0.358358; max |Δw| under dt halving (γT = 40, all 4 runs) = 3.1e-01
- slow20 2π: A: ccw→B slower-decaying (0.9963), cw→B slower-decaying (0.9963); B: ccw→B slower-decaying (0.7899), cw→B slower-decaying (0.7899)
- slow20 4π: A: ccw→B slower-decaying (0.7804), cw→B slower-decaying (0.7804); B: ccw→B slower-decaying (0.6835), cw→B slower-decaying (0.6835)
- slow40 2π: A: ccw→B slower-decaying (0.9982), cw→B slower-decaying (0.9982); B: ccw→B slower-decaying (0.8238), cw→B slower-decaying (0.8118)
- slow40 4π: A: ccw→B slower-decaying (0.7851), cw→B slower-decaying (0.7235); B: ccw→B slower-decaying (0.6986), cw→B slower-decaying (0.6363)
- slow100 2π: A: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998); B: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998)
- slow100 4π: A: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998); B: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998)

### +ε_EP, start +0.50 ε_EP (interior): MIXED
- loop: r = 0.50 ε_EP around +ε_EP, min |λ₊−λ₋| on the loop = 0.320525; max |Δw| under dt halving (γT = 40, all 4 runs) = 1.6e-04
- slow20 2π: A: ccw→B slower-decaying (0.9868), cw→B slower-decaying (0.9868); B: ccw→B slower-decaying (0.8174), cw→B slower-decaying (0.8174)
- slow20 4π: A: ccw→B slower-decaying (0.8365), cw→B slower-decaying (0.8365); B: ccw→B slower-decaying (0.7082), cw→B slower-decaying (0.7082)
- slow40 2π: A: ccw→B slower-decaying (0.9981), cw→B slower-decaying (0.9981); B: ccw→B slower-decaying (0.8067), cw→B slower-decaying (0.8068)
- slow40 4π: A: ccw→B slower-decaying (0.8139), cw→B slower-decaying (0.8139); B: ccw→B slower-decaying (0.6984), cw→B slower-decaying (0.6984)
- slow100 2π: A: ccw→B slower-decaying (0.9999), cw→B slower-decaying (0.9999); B: ccw→B slower-decaying (0.9999), cw→B slower-decaying (0.9999)
- slow100 4π: A: ccw→B slower-decaying (0.9999), cw→B slower-decaying (0.9999); B: ccw→B slower-decaying (0.9999), cw→B slower-decaying (0.9999)

### +ε_EP, start +0.75 ε_EP (interior): MIXED
- loop: r = 0.25 ε_EP around +ε_EP, min |λ₊−λ₋| on the loop = 0.244805; max |Δw| under dt halving (γT = 40, all 4 runs) = 1.2e-07
- slow20 2π: A: ccw→B slower-decaying (0.9893), cw→B slower-decaying (0.9893); B: ccw→B slower-decaying (0.7823), cw→B slower-decaying (0.7823)
- slow20 4π: A: ccw→B slower-decaying (0.7664), cw→B slower-decaying (0.7664); B: ccw→B slower-decaying (0.6770), cw→B slower-decaying (0.6770)
- slow40 2π: A: ccw→B slower-decaying (0.9996), cw→B slower-decaying (0.9996); B: ccw→B slower-decaying (0.8032), cw→B slower-decaying (0.8032)
- slow40 4π: A: ccw→B slower-decaying (0.8064), cw→B slower-decaying (0.8064); B: ccw→B slower-decaying (0.6951), cw→B slower-decaying (0.6951)
- slow100 2π: A: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998); B: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998)
- slow100 4π: A: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998); B: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998)

### +ε_EP, start +1.10 ε_EP (exterior): D7-like
- loop: r = 0.10 ε_EP around +ε_EP, min |λ₊−λ₋| on the loop = 0.161327; max |Δw| under dt halving (γT = 40, all 4 runs) = 2.0e-08
- slow20 2π: A: ccw→A lower-frequency (0.9887), cw→B higher-frequency (0.9887); B: ccw→A lower-frequency (0.9887), cw→B higher-frequency (0.9887)
- slow20 4π: A: ccw→A lower-frequency (0.9887), cw→B higher-frequency (0.9887); B: ccw→A lower-frequency (0.9887), cw→B higher-frequency (0.9887)
- slow40 2π: A: ccw→A lower-frequency (0.9979), cw→B higher-frequency (0.9979); B: ccw→A lower-frequency (0.9979), cw→B higher-frequency (0.9979)
- slow40 4π: A: ccw→A lower-frequency (0.9979), cw→B higher-frequency (0.9979); B: ccw→A lower-frequency (0.9979), cw→B higher-frequency (0.9979)
- slow100 2π: A: ccw→A lower-frequency (0.9997), cw→B higher-frequency (0.9997); B: ccw→A lower-frequency (0.9997), cw→B higher-frequency (0.9997)
- slow100 4π: A: ccw→A lower-frequency (0.9997), cw→B higher-frequency (0.9997); B: ccw→A lower-frequency (0.9997), cw→B higher-frequency (0.9997)

### +ε_EP, start +1.25 ε_EP (exterior): D7-like
- loop: r = 0.25 ε_EP around +ε_EP, min |λ₊−λ₋| on the loop = 0.244805; max |Δw| under dt halving (γT = 40, all 4 runs) = 1.7e-08
- slow20 2π: A: ccw→A lower-frequency (0.9970), cw→B higher-frequency (0.9970); B: ccw→A lower-frequency (0.9970), cw→B higher-frequency (0.9970)
- slow20 4π: A: ccw→A lower-frequency (0.9970), cw→B higher-frequency (0.9970); B: ccw→A lower-frequency (0.9970), cw→B higher-frequency (0.9970)
- slow40 2π: A: ccw→A lower-frequency (0.9994), cw→B higher-frequency (0.9994); B: ccw→A lower-frequency (0.9994), cw→B higher-frequency (0.9994)
- slow40 4π: A: ccw→A lower-frequency (0.9994), cw→B higher-frequency (0.9994); B: ccw→A lower-frequency (0.9994), cw→B higher-frequency (0.9994)
- slow100 2π: A: ccw→A lower-frequency (0.9999), cw→B higher-frequency (0.9999); B: ccw→A lower-frequency (0.9999), cw→B higher-frequency (0.9999)
- slow100 4π: A: ccw→A lower-frequency (0.9999), cw→B higher-frequency (0.9999); B: ccw→A lower-frequency (0.9999), cw→B higher-frequency (0.9999)

### +ε_EP, start +1.50 ε_EP (exterior): D7-like
- loop: r = 0.50 ε_EP around +ε_EP, min |λ₊−λ₋| on the loop = 0.320525; max |Δw| under dt halving (γT = 40, all 4 runs) = 1.3e-08
- slow20 2π: A: ccw→A lower-frequency (0.9990), cw→B higher-frequency (0.9990); B: ccw→A lower-frequency (0.9990), cw→B higher-frequency (0.9990)
- slow20 4π: A: ccw→A lower-frequency (0.9990), cw→B higher-frequency (0.9990); B: ccw→A lower-frequency (0.9990), cw→B higher-frequency (0.9990)
- slow40 2π: A: ccw→A lower-frequency (0.9998), cw→B higher-frequency (0.9998); B: ccw→A lower-frequency (0.9998), cw→B higher-frequency (0.9998)
- slow40 4π: A: ccw→A lower-frequency (0.9998), cw→B higher-frequency (0.9998); B: ccw→A lower-frequency (0.9998), cw→B higher-frequency (0.9998)
- slow100 2π: A: ccw→A lower-frequency (1.0000), cw→B higher-frequency (1.0000); B: ccw→A lower-frequency (1.0000), cw→B higher-frequency (1.0000)
- slow100 4π: A: ccw→A lower-frequency (1.0000), cw→B higher-frequency (1.0000); B: ccw→A lower-frequency (1.0000), cw→B higher-frequency (1.0000)

### −ε_EP, start -0.25 ε_EP (interior): FAIL [numerical FAIL, cause not established; careful-before-toy]; not a physical boundary
- loop: r = 0.75 ε_EP around −ε_EP, min |λ₊−λ₋| on the loop = 0.358357; max |Δw| under dt halving (γT = 40, all 4 runs) = 6.0e-02
- slow20 2π: A: ccw→B slower-decaying (0.9963), cw→B slower-decaying (0.9963); B: ccw→B slower-decaying (0.7899), cw→B slower-decaying (0.7899)
- slow20 4π: A: ccw→B slower-decaying (0.7804), cw→B slower-decaying (0.7804); B: ccw→B slower-decaying (0.6835), cw→B slower-decaying (0.6835)
- slow40 2π: A: ccw→B slower-decaying (0.9982), cw→B slower-decaying (0.9982); B: ccw→B slower-decaying (0.7979), cw→B slower-decaying (0.7979)
- slow40 4π: A: ccw→B slower-decaying (0.8443), cw→B slower-decaying (0.8443); B: ccw→B slower-decaying (0.6909), cw→B slower-decaying (0.6909)
- slow100 2π: A: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998); B: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998)
- slow100 4π: A: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998); B: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998)

### −ε_EP, start -0.50 ε_EP (interior): MIXED
- loop: r = 0.50 ε_EP around −ε_EP, min |λ₊−λ₋| on the loop = 0.320525; max |Δw| under dt halving (γT = 40, all 4 runs) = 4.0e-04
- slow20 2π: A: ccw→B slower-decaying (0.9868), cw→B slower-decaying (0.9868); B: ccw→B slower-decaying (0.8174), cw→B slower-decaying (0.8174)
- slow20 4π: A: ccw→B slower-decaying (0.8365), cw→B slower-decaying (0.8365); B: ccw→B slower-decaying (0.7082), cw→B slower-decaying (0.7082)
- slow40 2π: A: ccw→B slower-decaying (0.9981), cw→B slower-decaying (0.9981); B: ccw→B slower-decaying (0.8067), cw→B slower-decaying (0.8067)
- slow40 4π: A: ccw→B slower-decaying (0.8139), cw→B slower-decaying (0.8139); B: ccw→B slower-decaying (0.6986), cw→B slower-decaying (0.6986)
- slow100 2π: A: ccw→B slower-decaying (0.9999), cw→B slower-decaying (0.9999); B: ccw→B slower-decaying (0.9999), cw→B slower-decaying (0.9999)
- slow100 4π: A: ccw→B slower-decaying (0.9999), cw→B slower-decaying (0.9999); B: ccw→B slower-decaying (0.9999), cw→B slower-decaying (0.9999)

### −ε_EP, start -0.75 ε_EP (interior): MIXED
- loop: r = 0.25 ε_EP around −ε_EP, min |λ₊−λ₋| on the loop = 0.244805; max |Δw| under dt halving (γT = 40, all 4 runs) = 2.1e-08
- slow20 2π: A: ccw→B slower-decaying (0.9893), cw→B slower-decaying (0.9893); B: ccw→B slower-decaying (0.7823), cw→B slower-decaying (0.7823)
- slow20 4π: A: ccw→B slower-decaying (0.7664), cw→B slower-decaying (0.7664); B: ccw→B slower-decaying (0.6770), cw→B slower-decaying (0.6770)
- slow40 2π: A: ccw→B slower-decaying (0.9996), cw→B slower-decaying (0.9996); B: ccw→B slower-decaying (0.8032), cw→B slower-decaying (0.8032)
- slow40 4π: A: ccw→B slower-decaying (0.8064), cw→B slower-decaying (0.8064); B: ccw→B slower-decaying (0.6951), cw→B slower-decaying (0.6951)
- slow100 2π: A: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998); B: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998)
- slow100 4π: A: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998); B: ccw→B slower-decaying (0.9998), cw→B slower-decaying (0.9998)

### −ε_EP, start -1.10 ε_EP (exterior): D7-like
- loop: r = 0.10 ε_EP around −ε_EP, min |λ₊−λ₋| on the loop = 0.161327; max |Δw| under dt halving (γT = 40, all 4 runs) = 2.0e-08
- slow20 2π: A: ccw→B lower-frequency (0.9887), cw→A higher-frequency (0.9887); B: ccw→B lower-frequency (0.9887), cw→A higher-frequency (0.9887)
- slow20 4π: A: ccw→B lower-frequency (0.9887), cw→A higher-frequency (0.9887); B: ccw→B lower-frequency (0.9887), cw→A higher-frequency (0.9887)
- slow40 2π: A: ccw→B lower-frequency (0.9979), cw→A higher-frequency (0.9979); B: ccw→B lower-frequency (0.9979), cw→A higher-frequency (0.9979)
- slow40 4π: A: ccw→B lower-frequency (0.9979), cw→A higher-frequency (0.9979); B: ccw→B lower-frequency (0.9979), cw→A higher-frequency (0.9979)
- slow100 2π: A: ccw→B lower-frequency (0.9997), cw→A higher-frequency (0.9997); B: ccw→B lower-frequency (0.9997), cw→A higher-frequency (0.9997)
- slow100 4π: A: ccw→B lower-frequency (0.9997), cw→A higher-frequency (0.9997); B: ccw→B lower-frequency (0.9997), cw→A higher-frequency (0.9997)

### −ε_EP, start -1.25 ε_EP (exterior): D7-like
- loop: r = 0.25 ε_EP around −ε_EP, min |λ₊−λ₋| on the loop = 0.244805; max |Δw| under dt halving (γT = 40, all 4 runs) = 1.7e-08
- slow20 2π: A: ccw→B lower-frequency (0.9970), cw→A higher-frequency (0.9970); B: ccw→B lower-frequency (0.9970), cw→A higher-frequency (0.9970)
- slow20 4π: A: ccw→B lower-frequency (0.9970), cw→A higher-frequency (0.9970); B: ccw→B lower-frequency (0.9970), cw→A higher-frequency (0.9970)
- slow40 2π: A: ccw→B lower-frequency (0.9994), cw→A higher-frequency (0.9994); B: ccw→B lower-frequency (0.9994), cw→A higher-frequency (0.9994)
- slow40 4π: A: ccw→B lower-frequency (0.9994), cw→A higher-frequency (0.9994); B: ccw→B lower-frequency (0.9994), cw→A higher-frequency (0.9994)
- slow100 2π: A: ccw→B lower-frequency (0.9999), cw→A higher-frequency (0.9999); B: ccw→B lower-frequency (0.9999), cw→A higher-frequency (0.9999)
- slow100 4π: A: ccw→B lower-frequency (0.9999), cw→A higher-frequency (0.9999); B: ccw→B lower-frequency (0.9999), cw→A higher-frequency (0.9999)

### −ε_EP, start -1.50 ε_EP (exterior): D7-like
- loop: r = 0.50 ε_EP around −ε_EP, min |λ₊−λ₋| on the loop = 0.320525; max |Δw| under dt halving (γT = 40, all 4 runs) = 1.3e-08
- slow20 2π: A: ccw→B lower-frequency (0.9990), cw→A higher-frequency (0.9990); B: ccw→B lower-frequency (0.9990), cw→A higher-frequency (0.9990)
- slow20 4π: A: ccw→B lower-frequency (0.9990), cw→A higher-frequency (0.9990); B: ccw→B lower-frequency (0.9990), cw→A higher-frequency (0.9990)
- slow40 2π: A: ccw→B lower-frequency (0.9998), cw→A higher-frequency (0.9998); B: ccw→B lower-frequency (0.9998), cw→A higher-frequency (0.9998)
- slow40 4π: A: ccw→B lower-frequency (0.9998), cw→A higher-frequency (0.9998); B: ccw→B lower-frequency (0.9998), cw→A higher-frequency (0.9998)
- slow100 2π: A: ccw→B lower-frequency (1.0000), cw→A higher-frequency (1.0000); B: ccw→B lower-frequency (1.0000), cw→A higher-frequency (1.0000)
- slow100 4π: A: ccw→B lower-frequency (1.0000), cw→A higher-frequency (1.0000); B: ccw→B lower-frequency (1.0000), cw→A higher-frequency (1.0000)

## Notes

- Loop radius convention: r = |ε_start − tip| so that the loop passes through the start point; identical to drive-return for 0.75 and 1.25 around +ε_EP (r = 0.25 ε_EP). Other starts need other radii (0.75, 0.50, 0.10, 0.50 × ε_EP); the radius therefore changes together with the start point, which is a confound: the sweep tests start point + radius jointly. Starts 0.75 (r = 0.25) and 0.50 (r = 0.50) give nearly the same weights at γT = 40, 4π (max difference 0.0075); over all speeds and turns the difference is larger (up to 0.0701, at γT = 20), so the radius effect is small at γT = 40 but not ruled out. Suggested follow-up (not run): fix the start at 0.75 ε_EP and vary r over 0.25 / 0.50 / 0.75 ε_EP. Any re-test needs a new criterion fixed in advance (v2); the verdict above stays under the v1 criteria.
- Mirror convention: −ε_EP loops start at the mirrored points; ccw means counter-clockwise in the complex ε plane for both tips, in the table and in every − row. ε → −ε is a rotation by π (orientation-preserving) and H_A(−ε) = D H_A(ε) D, D = diag(1,−1); so ccw ↔ ccw, matching the table [standard + computed] (computed: max |H_A(−ε) − D H_A(ε) D| = 0.0e+00 at 6 complex ε).
- 'lower/higher-frequency' means signed Re λ, with ψ ~ e^{−iλt}; the two frequencies are equal and opposite.
- Start ±1.00 ε_EP is the EP itself: degenerate, reported as FAIL and not run.
- Winner = larger left-eigenvector weight at the start point after 2π / 4π (drive-return's `decompose`). Physical name: slower-/faster-decaying where the two modes share a frequency (inside Γ), higher-/lower-frequency where they share a decay (outside Γ).

## Post-hoc diagnostics (not used in the verdict)

The criteria in README.md were fixed before running and are not changed here. These notes only explain the interior result.

- Winner-only reading at the default dt: every interior run (both tips, all three speeds, 2π and 4π, ccw and cw, from A and from B) has the same winner: True (slower-decaying). That is the D6 winner pattern (loss picks the mode, direction ignored). The pre-fixed threshold w ≥ 0.9 fails because at γT = 20 and 40 the weights are only 0.636–0.84 (mostly at 4π and from start sheet B). At γT = 100 all interior weights are ≥ 0.9998. drive-return's D6 PASS used winners only (no w threshold), which is why 0.75 ε_EP was D6 there and is MIXED here under the stricter pre-fixed rule.

- dt convergence at γT = 40 (`diag_dt.py`, dt refined by factors [1, 2, 4, 8] relative to drive-return's dt rule), weight of sheet B at 4π:

| tip | start | dir | from | w_B at dt factors 1 / 2 / 4 / 8 | spread |
|---|---|---|---|---|---|
| +ε_EP | +0.25 | ccw | A | 0.78507 / 0.65643 / 0.59582 / 0.91855 | 3.2e-01 |
| +ε_EP | +0.25 | ccw | B | 0.69857 / 0.68705 / 0.46560 / 0.71477 | 2.5e-01 |
| +ε_EP | +0.25 | cw | A | 0.72347 / 0.63305 / 0.61087 / 0.69243 | 1.1e-01 |
| +ε_EP | +0.25 | cw | B | 0.63627 / 0.32816 / 0.10684 / 0.56852 | 5.3e-01 |
| +ε_EP | +0.50 | ccw | A | 0.81386 / 0.81387 / 0.81387 / 0.81360 | 2.7e-04 |
| +ε_EP | +0.50 | ccw | B | 0.69844 / 0.69830 / 0.69764 / 0.69855 | 9.1e-04 |
| +ε_EP | +0.50 | cw | A | 0.81389 / 0.81376 / 0.81377 / 0.81376 | 1.3e-04 |
| +ε_EP | +0.50 | cw | B | 0.69835 / 0.69843 / 0.69808 / 0.69820 | 3.5e-04 |
| +ε_EP | +0.75 | ccw | A | 0.80639 / 0.80639 / 0.80639 / 0.80639 | 1.2e-07 |
| +ε_EP | +0.75 | ccw | B | 0.69513 / 0.69513 / 0.69513 / 0.69513 | 3.7e-07 |
| +ε_EP | +0.75 | cw | A | 0.80639 / 0.80639 / 0.80639 / 0.80639 | 2.1e-07 |
| +ε_EP | +0.75 | cw | B | 0.69513 / 0.69513 / 0.69513 / 0.69513 | 1.1e-07 |
| −ε_EP | -0.25 | ccw | A | 0.84429 / 0.78444 / 0.76898 / 0.88583 | 1.2e-01 |
| −ε_EP | -0.25 | ccw | B | 0.69092 / 0.71683 / 0.76140 / 0.80280 | 1.1e-01 |
| −ε_EP | -0.25 | cw | A | 0.84429 / 0.78444 / 0.65276 / 0.83512 | 1.9e-01 |
| −ε_EP | -0.25 | cw | B | 0.69092 / 0.71683 / 0.76140 / 0.80280 | 1.1e-01 |
| −ε_EP | -0.50 | ccw | A | 0.81385 / 0.81400 / 0.81381 / 0.81399 | 1.9e-04 |
| −ε_EP | -0.50 | ccw | B | 0.69862 / 0.69822 / 0.69792 / 0.69842 | 7.0e-04 |
| −ε_EP | -0.50 | cw | A | 0.81389 / 0.81375 / 0.81377 / 0.81371 | 1.7e-04 |
| −ε_EP | -0.50 | cw | B | 0.69862 / 0.69822 / 0.69792 / 0.69842 | 7.0e-04 |
| −ε_EP | -0.75 | ccw | A | 0.80639 / 0.80639 / 0.80639 / 0.80639 | 2.5e-07 |
| −ε_EP | -0.75 | ccw | B | 0.69513 / 0.69513 / 0.69513 / 0.69513 | 1.9e-07 |
| −ε_EP | -0.75 | cw | A | 0.80639 / 0.80639 / 0.80639 / 0.80639 | 6.5e-08 |
| −ε_EP | -0.75 | cw | B | 0.69513 / 0.69513 / 0.69513 / 0.69513 | 1.9e-07 |

  Reading: the ±0.75 starts are converged to better than 1e-5 and ±0.50 to about 1e-3. At ±0.25 (loop r = 0.75 ε_EP) the weights do not converge when dt is refined; at +0.25, cw from B at factor 4 even gives w_B = 0.107, so the winner itself flips.

  ±0.25 rows: **[numerical FAIL, cause not established; careful-before-toy]**. This is not a physical boundary: it says nothing about where D6 or D7 behaviour stops. Two candidate causes, neither tested:
  1. Integrator breakdown on the big loop (r = 0.75 ε_EP). Evidence: U_cw = U_ccwᵀ holds exactly for this driver (H_A is complex-symmetric and the cw midpoint steps are the ccw steps in reverse order), yet cw and ccw give different weights (+0.25, from A, γT = 40, 4π: ccw 0.7851, cw 0.7235), and the weights jump under dt refinement (table above).
  2. Roundoff amplification by exp(∫|Im(λ_A−λ_B)| dt) over the loop.
  Tests (named, not run): a tight adaptive solver at rtol ~1e-12 rules out integrator error, and an mpmath (high-precision) run rules out roundoff. Whichever one restores cw = ccw identifies the cause.

## Loaded folders (read-only)

Generated with `--from-saved`: weights from outputs/sweep.npz, dt-halving maxima from outputs/dw.json, diagnostics from outputs/diag_dt.json; no drive was re-run. Loop geometry, start eigenvalues, min gap and the H_A symmetry checks are recomputed (no time evolution).

- `C:\Users\Akitt\pairA-drive-return`
- `C:\Users\Akitt\pairA-vortices-return`
- `C:\Users\Akitt\pairA-qg-handoff`
- SHA-256 of every file (57 files) before and after: **unchanged**.

Scope: two-mode toy; driven evolution i dψ/dt = H_A(ε(t))ψ as in drive-return. No QG, JT or Einstein claim.


# Job B2 spec: does the vortex-gas pressure really blow up at the cap? (folder 02, vacuum)

Status: FULL SPEC, draft for Venus, not locked. Runs after B0. Revised 2026-10-02 about 22:15 BST after Venus's 22:05 and 22:09 notes.

## Goal
Akitti [L12]: "once too many strings form on the outside of the bubble , mathematical divergences (infinities) … happen". The vortex gas gives a literal infinity at the cap [standard]. But the gas picture itself fails there, because the vortices dissolve (Manton–Wang). **The classical divergence is not a physical infinity unless the near-cap result keeps it.** B2 asks what really happens. Reading this as vacuum selection is [hive-interpretation]. Akitti's vacuum post says "critical occupancy" (L1155) and never says strings.

## Convention (one throughout)
- Quantum Hamiltonian H = ½ħ²Δ on the moduli space (Manton–Wang eq. (4); the same in Manton 2204.01389 eq. (6)).
- Dissolving-limit metric g = (A − 4πN)·G_FS on CP^N (MW eq. (2)).
- Area A of the round sphere, units e = v = 1.
- ε = A/A_B − 1 (Venus's δ).

## Equations
- **Classical gas.** Vol(moduli) = (A − 4πN)^N/N! [standard: Manton NPB 400 (1993) 624, the original; restated in MN eq. (3.23); π^N depends on convention and cancels in P]. *In words: the room the N strings have to move in shrinks to zero at the cap.*
- **Pressure.** P = NT/(A − 4πN) [MN eq. (4.7); exact on the sphere, since Z ∝ (A − 4πN)^N]. *In words: the strings act like hard discs of area 4π, and their pressure goes to infinity when the discs cover the sphere.*
- **Quantum gas near the cap.** Levels λ_k = 4k(N+k)/(A − 4πN) with degeneracy g_k, and z = (ħ²/2πT)·4πN/(A − 4πN) (MW eqs. (5), (7)). *In words: as the cap nears, the quantum steps between string states grow without limit.* At fixed T the gas freezes, and in MW's low-T regime P → 0 (MW eq. (36)).
- **First quantum correction.** P = NT/(A − 4πN)·(1 − c·z + …), with c = (N+1)/(6N) for finite N [computed, Venus, from MW's exact spectrum]. This tends to MW's printed 1/6 at large N (eq. (36)). *In words: quantum effects lower the pressure, by an amount that grows faster than the blow-up.* In plain units the correction is 2c·ħ²N²/(A − 4πN)² [from MW eq. (7)]. Use c = (N+1)/6N for N = 1–3, not 1/6.
- **Reconciliation note.** MW footnote 1 (p. 5): "In [6] the term z/6 appeared incorrectly as z/12; this resulted from misunderstanding factors of 2 in formulae for the total scalar curvature." Their [6] is Manton 2204.01389. So M22's −ħ²N²/(6(A − 4πN)²) (its eq. (19)) is the known misprint. It is printed once, and it is **not** a cross-check. Where the 2 sits [our arithmetic, Venus to check]: both papers use the same H = ½ħ²Δ (M22 eq. (6), MW eq. (4)), so the Hamiltonian isn't the cause. M22's total curvature, eq. (15), has 2N²π^N/N!·(A−4πN)^{N−1}. The scaled Fubini–Study value, R·Vol = [4N(N+1)/(A−4πN)]·π^N(A−4πN)^N/N!, is twice that at large N.

## What to compute (N = 1, 2, 3 from B0)
**Stage A, controls (known results).**
1. Sympy: (3.23) → (4.7).
2. Sum MW's Z = Σ g_k exp(−ħ²λ_k/2T) exactly, and get P = T ∂ln Z/∂A. Fit the small-z slope and check it against c = (N+1)/(6N). Check the large-N trend toward MW (36).
3. Print M22's 1/12 form beside it, labelled "misprinted, for reference" (MW fn. 1).

**Stage B, the near-cap rows.** On B0's area ladder, for T in {0.01, 0.1, 1} and ħ in {0.1, 1}, print:
- P_class and P_MW (exact sum);
- m_gap² from B0, next to Venus's e²v²(A − A_B)/A_B;
- ΔE = (A − A_B)²/(8A), the exact symmetric-minus-vortex energy (B0 P3). Note that m_gap²·|c₀|² = 8ΔE [Venus];
- **classical validity: T/ΔE**, which governs the classical gas [Venus];
- **quantum validity: ħ·m_gap/ΔE**, which governs the quantum gas [Venus];
- T/(ħ·m_gap), report only: it says which of the two applies;
- moduli step ħ²λ₁/2 against ħ·m_gap: whether truncating to the moduli is consistent. This matters only for the quantum gas.

From these, read off ε*(T), the first area where the governing column crosses 1. Record which scale breaks first, and P(ε*).

**Stage C, report only.**
- Torus: Shah–Manton, JMP 35 (1994) 1171.
- Leading classical estimate: melting at A − A_B ≈ √(8TA), so P(ε*) ≈ N√(T/8A) [correct at classical leading order, Venus].

## Pass rule (fixed before the run)
**PASS by construction (reproduction + scale ordering).** This comes out by construction:
- ΔE goes to zero like ε², so T/ΔE crosses 1 before the cap at every T > 0 [identity, given B0 P3];
- P_MW → 0 is MW's own result.

So B2's grade is really B0 P1's grade:
- **PASS** if Stage A reproduces (including the c = (N+1)/6N slope) and B0 P1 passed.
- **PARTIAL** if B0 P1 was PARTIAL (B2 then uses the measured gap).
- **FAIL** if Stage A fails, which means the code is wrong.

**A PASS reproduces known results. It is not evidence for Akitti's link.** The new information is:
- ε*(T);
- which breakdown scale comes first at each T (classical melting, the quantum gap, or the moduli step);
- the finite pressure P(ε*) where the gas description ends.

## Prediction (locked by Venus)
**PASS by construction (reproduction + scale ordering).** In the gas approximation P diverges. In the full theory it is softened, and the strings melt rather than jam.

Caveat: MW keep only the moduli and never compute the amplitude gap, so they can't check the gap columns. Baptista–Manton warn that the proof that the moduli approximation is valid "does not extend automatically" to this regime.

## Cost
Sympy plus numpy. Sums of about 10³ terms per row. Seconds, once B0 has run.

## Refs
- Manton, NPB 400 (1993) 624 [standard; cited in MN ref. 7, MW ref. 5; not read].
- Manton–Nasir, hep-th/9807017, eqs. (2.10), (3.23), (4.7) [checked in PDF].
- Manton, arXiv:2204.01389 (J. Phys. A 55 (2022) 325001 per MW ref. 6), eqs. (6), (16), (19), (20) [checked in PDF; the 1/12 is superseded by MW fn. 1].
- Manton–Wang, arXiv:2212.06016, eqs. (2), (4), (5), (7), (36) and fn. 1 [checked in PDF].
- Baptista–Manton, hep-th/0208001 [checked in PDF].
- Shah–Manton, JMP 35 (1994) 1171 [cited in MN ref. 12; not read].

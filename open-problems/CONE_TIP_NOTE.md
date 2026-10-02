# The cone at the old lift's tip, a short research note

Helios, 2026-10-02, about 23:00 BST. Written at Akitti's request, passed on by NanoRibbon. Waiting on Venus's check.

**Akitti's view:** the cone is a clue [Akitti]. Nothing else in this note is his.

**Ground rule:** the lift's gravity is unknown quantum gravity. Nothing below uses Einstein gravity (GR) as the lift's gravity. Where GR appears, it is a labelled reference only.

**Tags:**
- [standard] is known physics or maths from the literature.
- [computed] was checked by a bot.
- [hive-interpretation] and [Grok-suggested] are bot guesses.

## 1. Where the cone showed up

- **Job:** Grok Build's `pairA-qg-operator`, run 09-25 on TrinityOrb. It is the same as `jobs/pairA-qg-operator` on GitHub.
- **File and line:** `RESULTS.md:18` says: "with τ_E = 4π/ε_EP the P2 geometry is **not** a smooth Euclidean horizon."
- The job flagged the cone itself. It came back to light in `LOCAL_LIFT_CHECKS_REVIEW.md` (3D9294B7), and Venus re-derived it in her 77D663CE check.
- The same period had already been put in by hand in `pairA-qg-lift-4d` (09-23). That job's "bolt PASS" checks the period against itself, so it is circular (see `OLD_LIFT_REVIEW.md`).

## 2. What the smoothness test measures, and how far off it was

**The picture.** Near a tip, the cap looks like a flat disc. One direction runs outward from the tip. The other is the "time" circle, the Euclidean time τ, going round it. Take the circle's length at a small distance r from the tip and divide by r. That ratio is the *total angle* at the tip [standard].
- An ordinary smooth point has a total angle of one full turn (2π).
- Anything else is a cone point.

**The test.** The total angle is fixed by how long the time circle is, called the period, and by how fast the circle shrinks at the tip.
- The smooth choice is period = 2π divided by that shrink rate (the κ in requirement 1).
- For the old lift's shape, the smooth period is 2π/ε_EP. With it, the cap closes up into an ordinary round sphere [computed; Venus re-derived it].

**The miss.** The old lift used *twice* the smooth period, 4π/ε_EP. So:
- Each of the two tips has a total angle of **two full turns** instead of one.
- That is an **excess** of one full turn at each tip, not a deficit. The tip is not a pointy cone missing a wedge. It is a point where the surface wraps round itself twice, like a two-storey spiral car park.
- The cap's area comes out double that of a smooth sphere.
- The bookkeeping still balances. The curvature of the doubled surface plus the two tip corrections adds up to the total a sphere must have (Gauss–Bonnet with χ = 2) [computed, box and Venus].
- So the shape is still a sphere in topology. It just isn't smooth at the tips.

This is pure geometry and uses no gravity theory [kinematic].

## 3. What in the old lift causes it

- **Where the doubled period comes from.** The old lift's "r = 0 tips" are not gravity objects. They are the two branch points ±ε_EP of a 2×2 MHD matrix, its exceptional points, relabelled as bolts (`OLD_LIFT_REVIEW.md`).
- **What a branch point does.** Near one, the two eigenvalues behave like a square root [standard]. Go round the point once, and the two eigenvalues swap places. Only after going round **twice** is everything back where it started (the "2π swap / 4π return" in the old jobs) [standard, computed in pairA-*].
- **How that became the period.** The old lift took "you must go round twice to come back" and made it the length of the time circle. That is exactly the doubled period, so the two full turns at each tip are that square root's two sheets showing through [hive-interpretation, but the arithmetic is direct].
- **What's missing.** Nothing in the old lift has its own rule for setting the time-circle period. In any real geometry, *something* has to choose that period: a field equation, a temperature, or a regularity condition. The old lift had none, so the matrix's going-round-twice number filled the gap.
- In short, the cone is what the relabelled matrix leaves behind when no theory sets the period [hive-interpretation].
- **Topology cross-check.** The curve y² ∝ ε² − ε_EP² is a sphere branched at exactly those two points (genus 0, Riemann–Hurwitz) [computed in pairA-qg-operator]. So "two sheets glued at two branch points" is the whole story of where the extra turn lives.

## 4. What cones at a tip usually mean (reference, known literature)

These are known meanings of tip cones in other settings. None of them is claimed to be what happens in the lift.

**a) Missing wedge (deficit, total angle less than a full turn): something sits at the tip.**
- In 2+1-dimensional gravity, a point particle makes a cone with a missing wedge, sized by its mass (Deser–Jackiw–'t Hooft 1984) [standard; GR reference only].
- A straight cosmic string does the same in the plane around it, sized by its tension (Vilenkin 1981) [standard; GR reference only].
- More generally, any thin defect with positive tension at the tip gives a deficit.
- **This is not our case.** The old lift has an excess, not a deficit.

**b) Extra turns (excess, total angle a whole number of turns).**
- **The replica trick.** Gluing n copies of a disc at one point gives a total angle of n full turns. This is how entanglement and Rényi entropies are computed in ordinary quantum field theory, with no gravity needed (Calabrese–Cardy 2004) [standard].
- With n = 2, you get exactly two turns. The old lift's surface is **exactly the n = 2 replica (branched double cover) of the round S², with the two twist points at the tips** [identity, computed Venus].
  - The check: the area is twice a sphere's, there is a two-turn tip at each branch point, and the Riemann–Hurwitz count gives χ = 2, matching the Gauss–Bonnet bookkeeping above.
  - This identifies the *geometry* only. Reading it *physically* as a replica is still [hive-interpretation].
- In 2D field theory, the branch points of such a double cover carry "twist operators" [standard].
- **Excess angles in gravity.** Excess angles also come from defects with negative tension [standard; GR reference only].

**c) Wrong period at a horizon (off-shell cones).**
- In the Euclidean picture of a horizon, the smooth period is set by the temperature. Picking a different period leaves a cone at the tip [standard; GR reference].
- Such "conical" geometries are used on purpose to compute horizon entropy: Susskind–Uglum 1994, Callan–Wilczek 1994, Fursaev–Solodukhin 1995, and Lewkowycz–Maldacena 2013 for the replica version with gravity [standard; GR references only].
- In Lewkowycz–Maldacena, the bulk replica solutions are themselves smooth. The cone appears only in the off-shell step as n → 1 [standard].
- They mean "not in equilibrium", or "a counting device", rather than a physical object at the tip.

**d) Orbifold points.**
- Folding the plane by a symmetry (quotient by Z_n) gives a tip with a total angle of 1/n of a turn: a deficit with a fixed, quantised size [standard].
- String theory treats such points as allowed, often with extra "twisted" states living at the tip (Dixon–Harvey–Vafa–Witten 1985) [standard].
- An integer excess, as here, is the opposite direction: a branched cover, not a quotient.

## 5. Bot guesses (not established, not Akitti's)

- **[hive-interpretation]** The old lift's tip is case (b), two sheets glued at the tip, not case (a), something sitting at the tip. If the cone is a clue, the clue may be "the tip is where two copies meet" rather than "a string ends here".
- **[Grok-suggested]** In the hive's string picture, a deficit cone is what a single tensioned string at the tip would leave. The old lift shows the opposite sign. A future lift that *does* put flux or strings at the tip would be testable here: check whether the tip angle moves toward a deficit as strings are added. This would tie to requirement 4 (crowding A vs N_Φ). Untested.
  - **Condition:** this is only meaningful in a candidate where strings carry tension that couples to the tip geometry. In the flux-only toy, the angle is set by the period, not by N.
  - Flux alone makes no cone. A candidate that sets its own period just shifts κ and the period, and the tip stays smooth. Magnetic RN in the control row does this [GR reference].
  - A deficit needs a tensioned object sitting *at* the tip, like a vortex piercing a Euclidean horizon. Known analogue: Achúcarro–Gregory–Kuijken, PRD 52 (1995) 5729, gr-qc/9505039 [GR reference].
- **[hive-interpretation]** Requirement 1 still demands a smooth tip. Read through (c), any cone in a candidate lift means its period wasn't set by its own physics. So the cone is a useful failure test whatever the unknown quantum gravity is.
- **[open]** Whether the unknown quantum gravity permits or needs tip cones (as orbifold or replica-type points) is not known. No result here depends on it.

## References (checked by Orion on INSPIRE, 2026-10-02)
- Deser, Jackiw, 't Hooft, "Three-dimensional Einstein gravity: dynamics of flat space", Ann. Phys. 152 (1984) 220
- Vilenkin, "Gravitational field of vacuum domain walls and strings", PRD 23 (1981) 852
- Calabrese, Cardy, hep-th/0405152, J. Stat. Mech. (2004) P06002
- Susskind, Uglum, hep-th/9401070, PRD 50 (1994) 2700
- Callan, Wilczek, "On geometric entropy", hep-th/9401072, PLB 333 (1994) 55
- Fursaev, Solodukhin, hep-th/9501127, PRD 52 (1995) 2133
- Lewkowycz, Maldacena, 1304.4926, JHEP 08 (2013) 090
- Dixon, Harvey, Vafa, Witten, "Strings on orbifolds", NPB 261 (1985) 678 (part II: NPB 274 (1986) 285)
- Achúcarro, Gregory, Kuijken, "Abelian Higgs hair for black holes", gr-qc/9505039, PRD 52 (1995) 5729

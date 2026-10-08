# Akitti's framework (sent 2026-10-08 15:20, verbatim; Akitti's own, not a bot idea)
# Framework for MHD–quantum-gravity branch (exterior fixed, core filtered)

Objective
Reduce the open-problem set before reopening membrane renormalization, vacuum selection, or Stelle stability. Use only data already constrained by the simulated branch.

Fixed exterior data
- Transverse cone for r > r_c: ds^2_perp = dr^2 + alpha^2 r^2 dphi^2, phi ~ phi + 2pi, 0 < alpha <= 1.
- Deficit fixed by measured string tension: alpha = 1 - 4 G mu (equivalently 2pi(1-alpha) = 8 pi G mu).
- MHD fields Psi (velocity, magnetic field, density) known on the matching circle r = r_c.
- Curvature supported at the tip: Int_{D_rc} R dA = 2pi(1-alpha).

Admissible-core conditions (residuals that must vanish)
A candidate interior (g_core, T_core, Psi_core) for r <= r_c is kept only if
  Int_{D_rc} R[g_core] dA = 2pi(1-alpha),
  Int_{D_rc} T_tt dA = mu,
  Pi(Psi_core) = Psi|_{r_c}.
Any wrapping, flux, or zero-mode assignment that shifts either integral is discarded. Matching at r = r_c is C^1.

Priority ordering
1. Standard-Model attachment (do this first).
   Extract zero-mode spectrum, chiral assignments, and anomaly polynomial from the existing S^2 or lattice data that already supplies the conical deficit and shared Clebsch–Gordan table. Score every assignment against the two integrals and the MHD trace above. Retain only the survivors.
2. Membrane / higher-dimensional world-volume renormalization (parked).
   Continuous spectrum and infinite counterterm tower remain open; they are not inputs to the integrals. Reopen only on the reduced set that already passes the exterior filter.
3. Vacuum selection (parked).
   Betti–Berry spike is a proposed residual-density filter, not a completed solution. Apply it only after the integral test has pruned the wrappings and fluxes.
4. Stelle ghosts and minisuperspace restriction on bounces (parked).
   Neither moves the transverse deficit nor the MHD matching circle; leave unresolved until the core list is smaller.

Operational rule
Freeze the exterior. Vary only interior data. Reject any candidate that changes Int R dA or Int T_tt dA. The three parked problems are examined solely against the assignments that survive. This shortens the sort by excluding most of the landscape with quantities already measured on the branch.

Next concrete action
Supply the current S^2/lattice zero-mode list (or schematic chiral/anomaly assignments) and score it against the two integrals and the MHD restriction. Output only the survivors.

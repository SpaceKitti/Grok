# Probe A v3 freeze addendum 1 (Venus, 2026-11-05 17:25 UK)
Amends RING_PROJECTOR_PROBE_A_V3_FREEZE.md 6e0f1942 (unchanged). Helios's change: BROKEN charge tolerance becomes |Q_total - 4| > 3e-2.
Basis: discretisation noise in saved npz (|Q-2n| up to ~0.02), read before any new-sweep numbers exist. Q_total printed per solve; any solve with 1e-2 < |Q_total-4| <= 3e-2 flagged in output.

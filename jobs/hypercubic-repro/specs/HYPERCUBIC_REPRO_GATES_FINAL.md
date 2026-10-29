# Hypercubic reproduction gates — FINAL (Helios + Venus) [hive proposal, untested]
Do not edit. Any change = new file name + new hash.
Purpose: not-a-toy reproduction of over-improved flow (Garcia Perez et al. NPB413 1994; de Forcrand et al. NPB499 1997).
Code: /workspace/hypercubic hc_kernel.py 305F518F, test_hc.py 01451299; flow/coefficients from run.py D9D6766D, kernels.py F07C0646, lattice.py 35E9E049.
Weights c1=(4-eps)/3, c2=(eps-1)/48 on 2x2 squares. 1 round (run > 2-3 h).
Setup: periodic hypercubic L=24, one singular-gauge BPST, rho=3a, centred. Singular gauge only makes the seam small, not zero.
Outer 2 link layers held fixed, never flowed. rho and S measured only inside |x| <= L/2-3.
Record: boundary/seam action at t=0, Q before and after flow. Twisted BCs only if t=0 boundary excess > 1%.
rho_0 = interior rho at t=0, measured the same way as the flowed rho.

G0: eps=1 action and force match plain Wilson to 1e-12 (done at L=4: report). Must pass before G1 counts.
G1 static (no flow), eps in {1,-1}: interior S/8pi^2 vs Eq.(19) x (1 - continuum tail outside the ball), within 1%.
   Box error bar = |G1(L=24) - G1(L=20)|, static only (no flow at L=20).
G2 flow eps=-1 to T=0.6: rho_flowed/rho_0 >= 0.95. Growth (>1) passes. Report signed shift.
G3 flow eps=1 to T=0.6: rho_flowed/rho_0 < 1.
G4 half step, eps=-1: |rho_flowed/rho_0 - 1| moves by <= 0.01 absolute vs G2.
Reading: all pass -> flow fine, polar grid/box is the IT1b cause. G1 fails -> stop. G2 fails -> read t=0 boundary excess first, then flow step.
Every row reported. No retuning after results exist.

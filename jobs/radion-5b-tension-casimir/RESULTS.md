# Job 5b: rugby-ball tension and Casimir radion filter

Generated: 2026-10-02 19:54:53 GMT Summer Time (BST/local time)
One-universe scan flag: no n != 3 survivor at the three C = -3 window points [computed].
Unit normalisation: s = 1 only [assumed input]; Job Five dS window 0.739 ≤ s ≤ 0.957 [computed inherited input].
Job Three comparison: n = 3 own bands [assumed input]; testing against n's own band, not n_e = n/alpha.
Job Three n = 3 bands [computed read-only]: band 1 = 0.485797–0.542667; band 2 = 0.966397–0.989419
Job Five source hashes before run [computed, read-only]: RESULTS.md 345fb29a14414c748da40198f509f1ce58e1061a20839e9d364a38a1781eeea0; run.py d65d2002fca944ba227dab705af693a8cb6e8100f554ebb07cc9367421798c81.
Job Three source hashes before run [computed, read-only]: RESULTS.md 18723401c5fca77a76413abdcbcd952455fa23e167d3310016ea2b69d54a40f8; run.py dc51f7a3c93deede7e73d8f13c9938f007b80ce3795cbde7cd258001ae495c15.

## Stage A — identities and conventions [identity]

Tension identity [standard]: area = 4παx, smooth curvature integral = 8πα; tip delta is cancelled by tension (Carroll–Guica, hep-th/0302067).
With b → αb and B = n/(2gαR²), flux energy is c n²/(αx), and V_J,α(x;n) = α V_J,1(x;n/α) [identity].
Symbolic tension identity check: True [identity].
Einstein-frame convention used for the reported primary V: round-sphere Weyl factor, prefactor α [assumed input].
The alternate fixed-physical-M₄² convention has prefactor 1/α; both are positive, so stationary points, dS/AdS sign, barrier and p are unchanged [identity].
V_min = (b x − 2 c n_e²)/x³; p = n_e/(3x). The dS range is p ∈ [8/(9 n_e), 4/(3 n_e)), with the upper end open at the merger inflection [identity].

## Stage T — rugby-ball tension scan

[prediction] For α < 1, n_e = n/α > n, so p < 4/(3n) = 0.444444 and misses both n = 3 bands. Overlap needs n_e ≈ 1.64–2.74, hence α ≈ 1.09–1.83 [prediction].
T scan Λ6 range [assumed input]: 0.020–0.800; each α is tested on 40 computed points.
| α | n_e | tension | representative dS Λ6 | x_min | V_min (primary) | barrier | p | band | m² round α | m² fixed-M₄² 1/α | coverage |
|---:|---:|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1.000 | 3.000000 | positive tension | 0.240000 | 2.350459 | +9.721646e-02 | 1.218236e-01 | 0.425449 | none | 9.914741e-01 | 9.914741e-01 | 0.0% |
| 0.800 | 3.750000 | positive tension | 0.160000 | 3.779471 | +4.913113e-02 | 2.977015e-02 | 0.330734 | none | 2.781941e-01 | 4.346783e-01 | 0.0% |
| 0.600 | 5.000000 | positive tension | 0.100000 | 7.500000 | +2.234021e-02 | 1.787217e-03 | 0.222222 | none | 3.351032e-02 | 9.308423e-02 | 0.0% |
| 0.500 | 6.000000 | positive tension | 0.060000 | 9.401835 | +3.038015e-03 | 3.806988e-03 | 0.212724 | none | 3.098357e-02 | 1.239343e-01 | 0.0% |
| 1.500 | 2.000000 | unphysical: negative tension | 0.640000 | 1.250000 | +2.412743e+00 | 8.936086e-02 | 0.533333 | band 1 | 2.412743e+00 | 1.072330e+00 | 2.6% |
Tension scan checks [computed]: dS minima and barriers exist on the listed representative rows; only α > 1 can overlap an n = 3 band, and it is tagged unphysical [standard: beyond toy].
Part T grade: PARTIAL — physical α ≤ 1 has dS/barrier points but p misses both n = 3 bands; any overlap is only the negative-tension α > 1 row [computed; prediction].
No α or Λ6 point is treated as an exact-flat adjustment; exact flatness would be a [tuned] special case, not used here [computed].

## Stage C — Casimir scan

Potential: V(x) + C/x⁴ with V from the s = 1, n = 3 normalisation [assumed input].
Casimir grid Λ6 = 0.020–0.300 (15 points), C = -3, -1, 0, 1, 3 [assumed input].
Naturalness reference: C_nat = N/(4π)^3 with N = 1.000, so C_nat = 5.039302e-04; N-equivalent = |C|/C_nat [assumed input].
Each point: minimum location, V_min sign, barrier height, p, tested n = 3 band, and Casimir naturalness [computed].
| Λ6 | C | x_min | V_min | sign | barrier height | p_flux | band | p_with_C | band variant | C/C_nat | N-equivalent |
|---:|---:|---:|---:|---|---:|---:|---|---:|---|---:|---:|
| 0.020000 | -3.000000 | 1.352877 | -1.866246e+00 | AdS | 1.867518e+00 | 0.968487 | band 2 | -2.356068 | none | 5.953e+03 | 5.953e+03 |
| 0.040000 | -3.000000 | 1.379422 | -1.682254e+00 | AdS | 1.687399e+00 | 0.936632 | none | -2.995949 | none | 5.953e+03 | 5.953e+03 |
| 0.060000 | -3.000000 | 1.407800 | -1.501884e+00 | AdS | 1.513605e+00 | 0.904403 | none | -4.170015 | none | 5.953e+03 | 5.953e+03 |
| 0.080000 | -3.000000 | 1.438275 | -1.325241e+00 | AdS | 1.346347e+00 | 0.871761 | none | -7.042644 | none | 5.953e+03 | 5.953e+03 |
| 0.100000 | -3.000000 | 1.471169 | -1.152441e+00 | AdS | 1.185867e+00 | 0.838655 | none | -25.184030 | none | 5.953e+03 | 5.953e+03 |
| 0.120000 | -3.000000 | 1.506888 | -9.836176e-01 | AdS | 1.032435e+00 | 0.805017 | none | 14.741949 | none | 5.953e+03 | 5.953e+03 |
| 0.140000 | -3.000000 | 1.545947 | -8.189240e-01 | AdS | 8.863632e-01 | 0.770763 | none | 5.505561 | none | 5.953e+03 | 5.953e+03 |
| 0.160000 | -3.000000 | 1.589022 | -6.585382e-01 | AdS | 7.480127e-01 | 0.735776 | none | 3.300322 | none | 5.953e+03 | 5.953e+03 |
| 0.180000 | -3.000000 | 1.637016 | -5.026709e-01 | AdS | 6.178102e-01 | 0.699902 | none | 2.305844 | none | 5.953e+03 | 5.953e+03 |
| 0.200000 | -3.000000 | 1.691185 | -3.515760e-01 | AdS | 4.962689e-01 | 0.662926 | none | 1.735817 | none | 5.953e+03 | 5.953e+03 |
| 0.220000 | -3.000000 | 1.753350 | -2.055673e-01 | AdS | 3.840214e-01 | 0.624538 | none | 1.362842 | none | 5.953e+03 | 5.953e+03 |
| 0.240000 | -3.000000 | 1.826315 | -6.504545e-02 | AdS | 2.818741e-01 | 0.584263 | none | 1.096420 | none | 5.953e+03 | 5.953e+03 |
| 0.260000 | -3.000000 | 1.914759 | +6.945322e-02 | dS | 1.909045e-01 | 0.541324 | band 1 | 0.892875 | none | 5.953e+03 | 5.953e+03 |
| 0.280000 | -3.000000 | 2.027536 | +1.971593e-01 | dS | 1.126562e-01 | 0.494277 | band 1 | 0.727549 | none | 5.953e+03 | 5.953e+03 |
| 0.300000 | -3.000000 | 2.185468 | +3.168284e-01 | dS | 4.962292e-02 | 0.439817 | none | 0.582969 | none | 5.953e+03 | 5.953e+03 |
| 0.020000 | -1.000000 | 1.615038 | -1.453178e+00 | AdS | 1.454449e+00 | 0.955684 | none | 1.417265 | none | 1.984e+03 | 1.984e+03 |
| 0.040000 | -1.000000 | 1.644851 | -1.298963e+00 | AdS | 1.304109e+00 | 0.912245 | none | 1.302673 | none | 1.984e+03 | 1.984e+03 |
| 0.060000 | -1.000000 | 1.676959 | -1.147620e+00 | AdS | 1.159343e+00 | 0.869578 | none | 1.199185 | none | 1.984e+03 | 1.984e+03 |
| 0.080000 | -1.000000 | 1.711720 | -9.992606e-01 | AdS | 1.020374e+00 | 0.827572 | none | 1.104999 | none | 1.984e+03 | 1.984e+03 |
| 0.100000 | -1.000000 | 1.749585 | -8.540101e-01 | AdS | 8.874548e-01 | 0.786106 | none | 1.018635 | none | 1.984e+03 | 1.984e+03 |
| 0.120000 | -1.000000 | 1.791132 | -7.120125e-01 | AdS | 7.608720e-01 | 0.745044 | none | 0.938851 | none | 1.984e+03 | 1.984e+03 |
| 0.140000 | -1.000000 | 1.837117 | -5.734348e-01 | AdS | 6.409595e-01 | 0.704225 | none | 0.864584 | none | 1.984e+03 | 1.984e+03 |
| 0.160000 | -1.000000 | 1.888559 | -4.384731e-01 | AdS | 5.281100e-01 | 0.663457 | none | 0.794890 | none | 1.984e+03 | 1.984e+03 |
| 0.180000 | -1.000000 | 1.946883 | -3.073635e-01 | AdS | 4.227956e-01 | 0.622488 | none | 0.728893 | none | 1.984e+03 | 1.984e+03 |
| 0.200000 | -1.000000 | 2.014171 | -1.803970e-01 | AdS | 3.255983e-01 | 0.580982 | none | 0.665727 | none | 1.984e+03 | 1.984e+03 |
| 0.220000 | -1.000000 | 2.093656 | -5.794521e-02 | AdS | 2.372614e-01 | 0.538446 | band 1 | 0.604445 | none | 1.984e+03 | 1.984e+03 |
| 0.240000 | -1.000000 | 2.190813 | +5.949368e-02 | dS | 1.587813e-01 | 0.494089 | band 1 | 0.543854 | none | 1.984e+03 | 1.984e+03 |
| 0.260000 | -1.000000 | 2.316221 | +1.712001e-01 | dS | 9.159722e-02 | 0.446452 | none | 0.482114 | none | 1.984e+03 | 1.984e+03 |
| 0.280000 | -1.000000 | 2.495776 | +2.759913e-01 | dS | 3.807479e-02 | 0.392110 | none | 0.415352 | none | 1.984e+03 | 1.984e+03 |
| 0.300000 | -1.000000 | 2.850249 | +3.712122e-01 | dS | 3.524182e-03 | 0.315818 | none | 0.327122 | none | 1.984e+03 | 1.984e+03 |
| 0.020000 | +0.000000 | 1.716980 | -1.323297e+00 | AdS | 1.324568e+00 | 0.950201 | none | 0.950201 | none | 0.000e+00 | 0.000e+00 |
| 0.040000 | +0.000000 | 1.748656 | -1.178237e+00 | AdS | 1.183383e+00 | 0.901940 | none | 0.901940 | none | 0.000e+00 | 0.000e+00 |
| 0.060000 | +0.000000 | 1.782857 | -1.035880e+00 | AdS | 1.047604e+00 | 0.855049 | none | 0.855049 | none | 0.000e+00 | 0.000e+00 |
| 0.080000 | +0.000000 | 1.819995 | -8.963389e-01 | AdS | 9.174562e-01 | 0.809358 | none | 0.809358 | none | 0.000e+00 | 0.000e+00 |
| 0.100000 | +0.000000 | 1.860590 | -7.597408e-01 | AdS | 7.931948e-01 | 0.764693 | none | 0.764693 | none | 0.000e+00 | 0.000e+00 |
| 0.120000 | +0.000000 | 1.905313 | -6.262325e-01 | AdS | 6.751130e-01 | 0.720865 | none | 0.720865 | none | 0.000e+00 | 0.000e+00 |
| 0.140000 | +0.000000 | 1.955057 | -4.959851e-01 | AdS | 5.635530e-01 | 0.677664 | none | 0.677664 | none | 0.000e+00 | 0.000e+00 |
| 0.160000 | +0.000000 | 2.011044 | -3.692017e-01 | AdS | 4.589209e-01 | 0.634844 | none | 0.634844 | none | 0.000e+00 | 0.000e+00 |
| 0.180000 | +0.000000 | 2.075010 | -2.461289e-01 | AdS | 3.617100e-01 | 0.592099 | none | 0.592099 | none | 0.000e+00 | 0.000e+00 |
| 0.200000 | +0.000000 | 2.149561 | -1.270752e-01 | AdS | 2.725374e-01 | 0.549015 | none | 0.549015 | none | 0.000e+00 | 0.000e+00 |
| 0.220000 | +0.000000 | 2.238888 | -1.244210e-02 | AdS | 1.922060e-01 | 0.504988 | band 1 | 0.504988 | band 1 | 0.000e+00 | 0.000e+00 |
| 0.240000 | +0.000000 | 2.350459 | +9.721646e-02 | dS | 1.218236e-01 | 0.459012 | none | 0.459012 | none | 0.000e+00 | 0.000e+00 |
| 0.260000 | +0.000000 | 2.500000 | +2.010619e-01 | dS | 6.306744e-02 | 0.409091 | none | 0.409091 | none | 0.000e+00 | 0.000e+00 |
| 0.280000 | +0.000000 | 2.733854 | +2.975763e-01 | dS | 1.897340e-02 | 0.349628 | none | 0.349628 | none | 0.000e+00 | 0.000e+00 |
| 0.300000 | +0.000000 | none | none | none | none | none | none | none | none | 0.000e+00 | 0.000e+00 |
| 0.020000 | +1.000000 | 1.808214 | -1.219636e+00 | AdS | 1.220907e+00 | 0.945066 | none | 0.751886 | none | 1.984e+03 | 1.984e+03 |
| 0.040000 | +1.000000 | 1.841756 | -1.081901e+00 | AdS | 1.087047e+00 | 0.892374 | none | 0.723246 | none | 1.984e+03 | 1.984e+03 |
| 0.060000 | +1.000000 | 1.878057 | -9.467501e-01 | AdS | 9.584748e-01 | 0.841672 | none | 0.694382 | none | 1.984e+03 | 1.984e+03 |
| 0.080000 | +1.000000 | 1.917583 | -8.142954e-01 | AdS | 8.354162e-01 | 0.792717 | none | 0.665239 | none | 1.984e+03 | 1.984e+03 |
| 0.100000 | +1.000000 | 1.960924 | -6.846668e-01 | AdS | 7.181300e-01 | 0.745269 | none | 0.635742 | none | 1.984e+03 | 1.984e+03 |
| 0.120000 | +1.000000 | 2.008857 | -5.580135e-01 | AdS | 6.069151e-01 | 0.699079 | none | 0.605796 | none | 1.984e+03 | 1.984e+03 |
| 0.140000 | +1.000000 | 2.062419 | -4.345110e-01 | AdS | 5.021222e-01 | 0.653880 | none | 0.575272 | none | 1.984e+03 | 1.984e+03 |
| 0.160000 | +1.000000 | 2.123054 | -3.143694e-01 | AdS | 4.041715e-01 | 0.609367 | none | 0.543994 | none | 1.984e+03 | 1.984e+03 |
| 0.180000 | +1.000000 | 2.192854 | -1.978463e-01 | AdS | 3.135784e-01 | 0.565171 | none | 0.511710 | band 1 | 1.984e+03 | 1.984e+03 |
| 0.200000 | +1.000000 | 2.275036 | -8.526879e-02 | AdS | 2.309967e-01 | 0.520795 | band 1 | 0.478039 | none | 1.984e+03 | 1.984e+03 |
| 0.220000 | +1.000000 | 2.374963 | +2.292914e-02 | dS | 1.572946e-01 | 0.475506 | none | 0.442358 | none | 1.984e+03 | 1.984e+03 |
| 0.240000 | +1.000000 | 2.502733 | +1.261299e-01 | dS | 9.370711e-02 | 0.428036 | none | 0.403525 | none | 1.984e+03 | 1.984e+03 |
| 0.260000 | +1.000000 | 2.681840 | +2.233468e-01 | dS | 4.220788e-02 | 0.375627 | none | 0.358963 | none | 1.984e+03 | 1.984e+03 |
| 0.280000 | +1.000000 | 3.003113 | +3.125420e-01 | dS | 6.872178e-03 | 0.308200 | none | 0.299114 | none | 1.984e+03 | 1.984e+03 |
| 0.300000 | +1.000000 | none | none | none | none | none | none | none | none | 1.984e+03 | 1.984e+03 |
| 0.020000 | +3.000000 | 1.968779 | -1.062129e+00 | AdS | 1.063400e+00 | 0.935534 | none | 0.569189 | none | 5.953e+03 | 5.953e+03 |
| 0.040000 | +3.000000 | 2.005999 | -9.356486e-01 | AdS | 9.407950e-01 | 0.874832 | none | 0.553783 | none | 5.953e+03 | 5.953e+03 |
| 0.060000 | +3.000000 | 2.046452 | -8.115894e-01 | AdS | 8.233162e-01 | 0.817422 | none | 0.537605 | band 1 | 5.953e+03 | 5.953e+03 |
| 0.080000 | +3.000000 | 2.090718 | -6.900672e-01 | AdS | 7.111950e-01 | 0.762873 | none | 0.520589 | band 1 | 5.953e+03 | 5.953e+03 |
| 0.100000 | +3.000000 | 2.139544 | -5.712150e-01 | AdS | 6.046968e-01 | 0.710781 | none | 0.502653 | band 1 | 5.953e+03 | 5.953e+03 |
| 0.120000 | +3.000000 | 2.193930 | -4.551879e-01 | AdS | 5.041319e-01 | 0.660754 | none | 0.483690 | none | 5.953e+03 | 5.953e+03 |
| 0.140000 | +3.000000 | 2.255241 | -3.421706e-01 | AdS | 4.098694e-01 | 0.612393 | none | 0.463555 | none | 5.953e+03 | 5.953e+03 |
| 0.160000 | +3.000000 | 2.325434 | -2.323879e-01 | AdS | 3.223581e-01 | 0.565263 | none | 0.442044 | none | 5.953e+03 | 5.953e+03 |
| 0.180000 | +3.000000 | 2.407452 | -1.261211e-01 | AdS | 2.421608e-01 | 0.518852 | band 1 | 0.418860 | none | 5.953e+03 | 5.953e+03 |
| 0.200000 | +3.000000 | 2.506056 | -2.373773e-02 | AdS | 1.700123e-01 | 0.472478 | none | 0.393529 | none | 5.953e+03 | 5.953e+03 |
| 0.220000 | +3.000000 | 2.629805 | +7.425297e-02 | dS | 1.069304e-01 | 0.425091 | none | 0.365227 | none | 5.953e+03 | 5.953e+03 |
| 0.240000 | +3.000000 | 2.796977 | +1.670747e-01 | dS | 5.446756e-02 | 0.374683 | none | 0.332248 | none | 5.953e+03 | 5.953e+03 |
| 0.260000 | +3.000000 | 3.063147 | +2.533010e-01 | dS | 1.547664e-02 | 0.315608 | none | 0.289629 | none | 5.953e+03 | 5.953e+03 |
| 0.280000 | +3.000000 | none | none | none | none | none | none | none | none | 5.953e+03 | 5.953e+03 |
| 0.300000 | +3.000000 | none | none | none | none | none | none | none | none | 5.953e+03 | 5.953e+03 |
C = 0 closed-form 5c check: max |x_numeric − x_closed| = 1.554e-15 [identity].
Variant row [assumed input]: p_with_C = (B²/2)/(B²/2 + Λ6 + C/x⁴); the main p_flux rows keep Casimir outside the denominator [identity].

C = -3.000000 grid-step qualifying points [computed]: 2; old coverage = 7.1% [grid-step].
Exact C = -3.000000 qualifying interval(s) [computed]: 0.259397739–0.283356695; coverage = 8.557% of the scanned Λ6 range.
Coverage denominators [computed]: width = 0.023958956; width/scanned range = 0.085568; width/midpoint = 0.088287; width/lower edge = 0.092364.
Fine C scan [computed]: C = -1.000000 is the smallest |C| with a qualifying interval, interval(s) 0.229755073–0.243608395; |C|/C_nat(N=1) = 1.984e+03.
Casimir sign convention [assumed input]: C < 0 is attractive Casimir; the successful points are therefore attractive.
Part C grade: PARTIAL [tuned] — window passes the 5% coverage rule, but |C|/C_nat = 1.984e+03 for N = 1; about 1984 light fields would be needed for naturalness [tuned].
Reading a surviving band as a candidate is a [hive-interpretation], not a full vacuum-selection claim [standard: beyond toy].

## One-universe scan — fixed (Λ6, C), n = 1…10

At each fixed point only n varies; C = -3.000000 is attractive. A survivor requires dS, both barriers, and p_flux in a band [computed].
| Λ6 | n | minimum | sign | barrier? | p_flux | band |
|---:|---:|---|---|---|---:|---|
| 0.259397739 | 1 | NO | none | NO | none | none |
| 0.259397739 | 2 | NO | none | NO | none | none |
| 0.259397739 | 3 | YES | dS | YES | 0.542667000 | band 1 |
| 0.259397739 | 4 | NO | none | NO | none | none |
| 0.259397739 | 5 | NO | none | NO | none | none |
| 0.259397739 | 6 | NO | none | NO | none | none |
| 0.259397739 | 7 | NO | none | NO | none | none |
| 0.259397739 | 8 | NO | none | NO | none | none |
| 0.259397739 | 9 | NO | none | NO | none | none |
| 0.259397739 | 10 | NO | none | NO | none | none |
Survivors at Λ6 = 0.259397739: n=3 [computed].
| 0.271377217 | 1 | NO | none | NO | none | none |
| 0.271377217 | 2 | NO | none | NO | none | none |
| 0.271377217 | 3 | YES | dS | YES | 0.515206357 | band 1 |
| 0.271377217 | 4 | NO | none | NO | none | none |
| 0.271377217 | 5 | NO | none | NO | none | none |
| 0.271377217 | 6 | NO | none | NO | none | none |
| 0.271377217 | 7 | NO | none | NO | none | none |
| 0.271377217 | 8 | NO | none | NO | none | none |
| 0.271377217 | 9 | NO | none | NO | none | none |
| 0.271377217 | 10 | NO | none | NO | none | none |
Survivors at Λ6 = 0.271377217: n=3 [computed].
| 0.283356695 | 1 | NO | none | NO | none | none |
| 0.283356695 | 2 | NO | none | NO | none | none |
| 0.283356695 | 3 | YES | dS | YES | 0.485797000 | band 1 |
| 0.283356695 | 4 | NO | none | NO | none | none |
| 0.283356695 | 5 | NO | none | NO | none | none |
| 0.283356695 | 6 | NO | none | NO | none | none |
| 0.283356695 | 7 | NO | none | NO | none | none |
| 0.283356695 | 8 | NO | none | NO | none | none |
| 0.283356695 | 9 | NO | none | NO | none | none |
| 0.283356695 | 10 | NO | none | NO | none | none |
Survivors at Λ6 = 0.283356695: n=3 [computed].

## Two-barrier heights at the C = -3 dS interval [identity]

| Λ6 | x_in | ΔV_in | x_min | x_out | ΔV_out | lower barrier |
|---:|---:|---:|---:|---:|---:|---|
| 0.259397739 | 0.353661802 | 3.651092684e+01 | 1.911801210 | 5.444704433 | 1.934674443e-01 | out |
| 0.271377217 | 0.353404891 | 3.685923878e+01 | 1.975046936 | 5.041363604 | 1.447036044e-01 | out |
| 0.283356695 | 0.353149204 | 3.721050621e+01 | 2.049978994 | 4.655113360 | 1.009239961e-01 | out |
For C < 0, V→−∞ as x→0; the dS minimum lies between two maxima [identity].

## Stage K — k-family Casimir degeneracy check

Without C, n→k n, Λ6→Λ6/k², x→k²x multiplies the potential by k⁻⁴, leaving p invariant [identity]. Fixed C scales as k⁻⁸ and should break that degeneracy [identity].
The restoring control is C→k⁴C under n→k n; for the absolute-n table relative to base n=3 this is C→C·(k/3)^4 [identity]. A literal C/k⁴ row is retained as a breaks-more illustration.
| base Λ6 | base C | k | p(n=3) | p fixed C | fixed dS+barrier | fixed band | p literal C/k⁴ | p correct C·(k/3)^4 |
|---:|---:|---:|---:|---:|---|---|---:|---:|
| 0.259398 | -3.000000 | 1 | 0.542667000 | none | NO | none | none | 0.542667000 |
| 0.259398 | -3.000000 | 2 | 0.542667000 | none | NO | none | 0.445946619 | 0.542667000 |
| 0.259398 | -3.000000 | 3 | 0.542667000 | 0.542667000 | YES | band 1 | 0.411988873 | 0.542667000 |
| 0.259398 | -3.000000 | 4 | 0.542667000 | 0.445946619 | YES | none | 0.410817087 | 0.542667000 |
| 0.259398 | -3.000000 | 5 | 0.542667000 | 0.424632427 | YES | none | 0.410708815 | 0.542667000 |
| 0.259398 | -3.000000 | 6 | 0.542667000 | 0.417333887 | YES | none | 0.410692067 | 0.542667000 |
| 0.271377 | -3.000000 | 1 | 0.515206357 | none | NO | none | none | 0.515206357 |
| 0.271377 | -3.000000 | 2 | 0.515206357 | none | NO | none | 0.414649387 | 0.515206357 |
| 0.271377 | -3.000000 | 3 | 0.515206357 | 0.515206357 | YES | band 1 | 0.378592030 | 0.515206357 |
| 0.271377 | -3.000000 | 4 | 0.515206357 | 0.414649387 | YES | none | 0.377334356 | 0.515206357 |
| 0.271377 | -3.000000 | 5 | 0.515206357 | 0.392097607 | YES | none | 0.377218091 | 0.515206357 |
| 0.271377 | -3.000000 | 6 | 0.515206357 | 0.384315291 | YES | none | 0.377200107 | 0.515206357 |
| 0.283357 | -3.000000 | 1 | 0.485797000 | none | NO | none | none | 0.485797000 |
| 0.283357 | -3.000000 | 2 | 0.485797000 | none | NO | none | 0.379452580 | 0.485797000 |
| 0.283357 | -3.000000 | 3 | 0.485797000 | 0.485797000 | YES | band 1 | 0.339128191 | 0.485797000 |
| 0.283357 | -3.000000 | 4 | 0.485797000 | 0.379452580 | YES | none | 0.337671963 | 0.485797000 |
| 0.283357 | -3.000000 | 5 | 0.485797000 | 0.354512459 | YES | none | 0.337537109 | 0.485797000 |
| 0.283357 | -3.000000 | 6 | 0.485797000 | 0.345700409 | YES | none | 0.337516246 | 0.485797000 |
Part K largest |Δp| fixed C: 1.401e-01; literal C/k⁴ control: 1.483e-01; restoring C·(k/3)^4 control: 1.277e-15 [computed].
Part K verdict: fixed C sees n [computed]; the restoring k⁴C control matches to machine precision, while literal C/k⁴ breaks more for the absolute-n convention [identity].

Breaking-strength check uses multiplier q = 2 at base Λ6 = 0.001000, C = -0.010000 [assumed input]. ε_C = (C/x⁴)/(c n²/x³) = C/(c n² x), expected to scale as Cb/(c²n⁴) [identity].
| base n | q | p(base) | p(qn, Λ/q², C) | Δp fixed C | ε_C at base root |
|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 0.999744867 | 0.999720370 | -2.450e-05 | -3.564e-02 |
| 2 | 2 | 0.998881787 | 0.998875819 | -5.968e-06 | -2.127e-03 |
| 3 | 2 | 0.997473703 | 0.997471058 | -2.644e-06 | -4.191e-04 |
| 4 | 2 | 0.995508312 | 0.995506829 | -1.483e-06 | -1.325e-04 |
| 6 | 2 | 0.989909639 | 0.989908985 | -6.543e-07 | -2.611e-05 |
Largest |Δp| over available base-n rows: 2.450e-05 [computed].
Part K base-n breaking check: Δp is printed for n = 1, 2, 3, 4, 6; ε_C carries the expected small-n enhancement [computed].

## Summary

- Part T: PARTIAL [computed; prediction was physical non-overlap].
- Part C: PARTIAL [tuned] [tuned; physics-grader relabel, threshold unchanged].
- Part K: first n-sensitive ingredient [computed].
- Overall: Part T PARTIAL, Part C PARTIAL [tuned], Part K first n-sensitive ingredient [computed].
- Band convention: n = 3 own Job Three bands, not n_e = n/alpha [assumed input].
- All numbers above are generated from variables; source trees were read-only [computed].
Read-only source audit: Job Five and Job Three inputs unchanged [computed].

# Cut-crossing probe

New folder. Hive not opened. Pair A not rebuilt.
No letter is copied from $n_{\mathrm{MHD}}$ or $da=\pi\delta_\Gamma$.
$\Gamma=[-0.513681,0.513681]$. $\gamma_{\mathrm{cross}}$: $x=0.25$, $y=+0.05\to-0.05$. $\gamma_{\mathrm{miss}}$: $x=1.2$, same length.
Main number: jump across the segment, not flux of a closed loop.

## P0 pair A labels

```
P0  pair A principal sqrt
    disc(ε)=(ε v)^2−((b−a)/2)^2
    letter=√disc  (principal branch)
    γ_cross: +0.25±i0.05,  γ_miss: +1.20±i0.05
```
J_on=0.32593, J_off=0.0398527, ratio=8.1784. n(before,after) on=(1, -1) off=(0, 0). defined without MHD jump: **no**. verdict: **sees the wall**.

## P1 CS

```
P1  U(1)_k CS, k=8, vacuum A_ℓ=0
    S_CS=(k/4π)∫ A dA,  eom F=0
    J=|∫_γ A·dl|
```
J_on=0, J_off=0, ratio=0.0000. defined without MHD jump: **yes**. verdict: **misses the wall**.

## P2 foam

```
P2  BF defect g_*=exp(2πi/3) on scanned face f
    J=|g_*-1| if dual(f) meets the path, else 0
    scan faces on a 21×21 grid over [-2,2]²
```
J_on=1.73205, J_off=0, ratio=17320508075688772.0000. P_site=(0.20000000000000018+0j). defined without MHD jump: **yes**. verdict: **inserted**.

## P3 holo

```
P3  3-layer bulk, χ=βx on the boundary, β=1/3
    J=|χ(x+iδ)−χ(x−iδ)|   (smooth field, no slit inserted)
```
J_on=0, J_off=0, ratio=0.0000. defined without MHD jump: **yes**. verdict: **misses the wall**.

## P4 worldsheet

```
P4  Nambu length of the probe segment
    S=∫ds=2δ for both γ_cross and γ_miss
    no wall weight in the action
```
J_on=0.1, J_off=0.1, ratio=1.0000. defined without MHD jump: **yes**. verdict: **global junk**.

## P5 hybrid

```
P5  hybrid  J_h = hypot(J_P1_CS, J_P3_holo)
    same γ_cross / γ_miss
    not exp(iπ n_MHD)
```
J_on=0, J_off=0, ratio=0.0000. defined without MHD jump: **yes**. verdict: **misses the wall**.

## P6 uniform U(1) control

```
P6  uniform U(1), B=1
    A=(−By/2, Bx/2)
    J=|∫_γ A|=|B x δ|
```
J_on=0.0125, J_off=0.06, ratio=0.2083. defined without MHD jump: **yes**. verdict: **global junk**.

## Table

| family | J_on | J_off | ratio | defined without MHD jump? | verdict |
| --- | --- | --- | --- | --- | --- |
| P0 pair A labels | 0.32593 | 0.0398527 | 8.1784 | no | **sees the wall** |
| P1 CS | 0 | 0 | 0.0000 | yes | **misses the wall** |
| P2 foam | 1.73205 | 0 | 17320508075688772.0000 | yes | **inserted** |
| P3 holo | 0 | 0 | 0.0000 | yes | **misses the wall** |
| P4 worldsheet | 0.1 | 0.1 | 1.0000 | yes | **global junk** |
| P5 hybrid | 0 | 0 | 0.0000 | yes | **misses the wall** |
| P6 uniform U(1) control | 0.0125 | 0.06 | 0.2083 | yes | **global junk** |

## One sentence

**wall-probe works; no named letter sees the wall**

Not a theorem. No Qin, leapfrog, Hall 3×3, dynamo phenomenology.

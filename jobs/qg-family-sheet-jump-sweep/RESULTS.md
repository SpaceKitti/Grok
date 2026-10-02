# QG family sheet-jump sweep

New folder. Hive not opened. Tearing not rerun. Pair A not rebuilt.
No letter is $U=\exp(i\pi n_{\mathrm{MHD}})$ or $da=\pi\delta_\Gamma$.

Locked MHD: pair A, $\varepsilon_{\mathrm{EP}}=0.513681$, $\Delta n(2\pi)=1$, $\Delta n(4\pi)=2$.
Same loop family around $+\varepsilon_{\mathrm{EP}}$; control centre $+1.2i$.

## F1 CS

```
F1  U(1)_k Chern–Simons, k=8 (fixed)
    S_CS = (k/4π) ∑_p A_∂p ∧ F_p
    eom F_p = 0  (no δ_Γ source)
    vacuum A_ℓ = 0
    U_CS[γ] = ∏_{ℓ∈γ} exp(i A_ℓ)
```

defined without MHD jump: **yes**. S1 FAIL (on/off=0.0000 (on=0, off=0)). S2 FAIL (U(2π)=1.0000+0.0000j |U+1|=2.000; U(4π)=1.0000+0.0000j |U-1|=0.000). S3 FAIL (|ΔU|_at n-jump / |ΔU|_quiet = 0.0000). S4 FAIL (drop=0.0000  |U-1|_on=0.0000 |_off=0.0000). verdict: **misses Γ**.

## F2 foam

```
F2  BF / spin-foam on a 9×9 face lattice over [-2,2]²
    S_BF = ∑_f Tr(B_f F_f)
    defect g_* = exp(2πi/3) on face (i,j)=(0,0) at (-1.778,-1.778)
    foam rule: unique face of max graph-distance from the origin
    (NOT pasted onto Γ)
    U_BF[γ] = g_*^{winding around that face}
```

defined without MHD jump: **yes**. S1 FAIL (on/off=0.0000 (on=0, off=0.02221)). S2 FAIL (U(2π)=1.0000+0.0000j |U+1|=2.000; U(4π)=1.0000+0.0000j |U-1|=0.000). S3 FAIL (|ΔU|_at n-jump / |ΔU|_quiet = 1.2106). S4 FAIL (drop=0.0000  |U-1|_on=0.0000 |_off=0.0000). verdict: **misses Γ**.

## F3 holo

```
F3  3-layer discrete bulk
    ds² = dr² + (1+r)² dx²    r=0,1,2
    ω_x^{rx} = 1/(1+r)         (Levi-Civita of the warp)
    radial links A_r = 0
    IR identification at r=0; χ(x) = β x,  β=1/3
    U_3[γ] = exp(i[χ(x_γ)−χ(x_0)])   geodesic monodromy through IR
```

defined without MHD jump: **yes**. S1 FAIL (on/off=0.0000 (on=0, off=0)). S2 FAIL (U(2π)=1.0000+0.0000j |U+1|=2.000; U(4π)=1.0000+0.0000j |U-1|=0.000). S3 FAIL (|ΔU|_at n-jump / |ΔU|_quiet = 0.0271). S4 FAIL (drop=0.0000  |U-1|_on=0.0000 |_off=0.0000). verdict: **misses Γ**.

## F4 hybrid

```
F4  hybrid on one meridian
    U_F4[γ] = U_F1_CS[γ] × U_F3_holo[γ]
    F1 vacuum A=0  and  F3 IR geodesic χ=βx
    not exp(i π n_MHD)
```

defined without MHD jump: **yes**. S1 FAIL (on/off=0.0000 (on=0, off=0)). S2 FAIL (U(2π)=1.0000+0.0000j |U+1|=2.000; U(4π)=1.0000+0.0000j |U-1|=0.000). S3 FAIL (|ΔU|_at n-jump / |ΔU|_quiet = 0.0271). S4 FAIL (drop=0.0000  |U-1|_on=0.0000 |_off=0.0000). verdict: **misses Γ**.

## F5 uniform U(1) control

```
F5  uniform U(1)  (independent-check G1, copied)
    A_x = −(B/2) y ,  A_y = +(B/2) x ,  B=1
    U[γ] = exp(i B Area)
```

defined without MHD jump: **yes**. S1 FAIL (on/off=1.0000 (on=0.0003979, off=0.0003979)). S2 FAIL (U(2π)=0.9987+0.0518j |U+1|=1.999; U(4π)=0.9946+0.1034j |U-1|=0.104). S3 FAIL (|ΔU|_at n-jump / |ΔU|_quiet = 1.9229). S4 FAIL (drop=1.0000  |U-1|_on=0.0518 |_off=0.0518). verdict: **global junk**.

## Table

| family | defined without MHD jump? | S1 | S2 | S3 | S4 | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| F1 CS | yes | FAIL | FAIL | FAIL | FAIL | **misses Γ** |
| F2 foam | yes | FAIL | FAIL | FAIL | FAIL | **misses Γ** |
| F3 holo | yes | FAIL | FAIL | FAIL | FAIL | **misses Γ** |
| F4 hybrid | yes | FAIL | FAIL | FAIL | FAIL | **misses Γ** |
| F5 uniform U(1) control | yes | FAIL | FAIL | FAIL | FAIL | **global junk** |

## One sentence

**no family jumps with the MHD sheet**

Not quantum gravity solved. No Qin, leapfrog, Hall 3×3, dynamo phenomenology.

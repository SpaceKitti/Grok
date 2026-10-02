# QG defect-scan sweep

New folder. Hive not opened. Tearing not rerun. Pair A not rebuilt.
No letter is $\exp(i\pi n_{\mathrm{MHD}})$ or $da=\pi\delta_\Gamma$.
Locked MHD: $\varepsilon_{\mathrm{EP}}=0.513681$, $\Delta n(2\pi)=1$, $\Delta n(4\pi)=2$.
Defect/source/pinch is scanned. Γ is a score mask only.

## T1 CS puncture

```
T1  U(1)_k CS, k=8, one puncture
    S_CS = (k/4π)∫ A dA  +  q ∫_{z_p} A
    q = 2π/3  (not π, not fitted)
    F = q δ(z−z_p)  at scanned z_p
    U[γ] = exp(i q W(γ, z_p))
```

P_site(on-loop)=0.5000+0.0000j; P_site(off-loop)=0.0000+1.2000j. defined without MHD jump: **yes**. S1 FAIL (P=0.5000+0.0000j, n_tie=5, max_on/max_off=1.0000). S2 FAIL (U(2π)=-0.5000+0.8660j |U+1|=1.000; U(4π)=-0.5000-0.8660j |U-1|=1.732). S3 FAIL (|ΔU|_jump / |ΔU|_quiet = 0.9023). S4 PASS (drop=17320508075688770.0000 |U-1|_on=1.7321 |_off=0.0000). verdict: **misses Γ**.

## T2 foam

```
T2  BF / spin-foam, one defect
    S_BF = ∑_f Tr(B_f F_f)
    g_* = exp(2πi/3) on scanned face f
    scan starts from a full 2d face grid (on / near / far from Γ)
    U[γ] = g_*^{W(γ, centre(f))}
```

P_site(on-loop)=0.5000+0.0000j; P_site(off-loop)=0.0000+1.2000j. defined without MHD jump: **yes**. S1 FAIL (P=0.5000+0.0000j, n_tie=5, max_on/max_off=1.0000). S2 FAIL (U(2π)=-0.5000+0.8660j |U+1|=1.000; U(4π)=-0.5000-0.8660j |U-1|=1.732). S3 FAIL (|ΔU|_jump / |ΔU|_quiet = 0.9023). S4 PASS (drop=17320508075688770.0000 |U-1|_on=1.7321 |_off=0.0000). verdict: **misses Γ**.

## T3 holo

```
T3  3-layer bulk, ds²=dr²+(1+r)² dx²
    membrane = radial line at scanned boundary site x_p
    scan x_p on the boundary line (includes Γ and |x|>ε_EP)
    α=2π/5 (not π)
    U[γ] = exp(i α W(γ, x_p))
```

P_site(on-loop)=0.5000+0.0000j; P_site(off-loop)=0.0000+0.0000j. defined without MHD jump: **yes**. S1 FAIL (P=0.5000+0.0000j, n_tie=3, max_on/max_off=1.0000). S2 FAIL (U(2π)=0.3090+0.9511j |U+1|=1.618; U(4π)=-0.8090+0.5878j |U-1|=1.902). S3 FAIL (|ΔU|_jump / |ΔU|_quiet = 0.9023). S4 PASS (drop=11755705045849462.0000 |U-1|_on=1.1756 |_off=0.0000). verdict: **misses Γ**.

## T4 worldsheet

```
T4  worldsheet / Nambu cone + wrapping
    S_N(p) = π R * hypot(R, |p−z_γ|)
    L(p) = |W(γ,p)| exp(−S_N / R²)
    scan pinch p on the 2d mesh
```

P_site(on-loop)=0.5000+0.0000j; P_site(off-loop)=0.0000+1.2000j. defined without MHD jump: **yes**. S1 FAIL (P=0.5000+0.0000j, n_tie=1, max_on/max_off=1.8700). S2 FAIL (U(2π)=-0.5000+0.8660j |U+1|=1.000; U(4π)=-0.5000-0.8660j |U-1|=1.732). S3 FAIL (|ΔU|_jump / |ΔU|_quiet = 0.9023). S4 PASS (drop=17320508075688772.0000 |U-1|_on=1.7321 |_off=0.0000). verdict: **misses Γ**.

## T5 hybrid

```
T5  hybrid on one meridian
    U_h[γ; x] = U_T1_CS(q=2π/3; z=x) × U_T3_holo(α=2π/5; x)
    scan x on the boundary line
    not exp(i π n_MHD)
```

P_site(on-loop)=0.5000+0.0000j; P_site(off-loop)=0.0000+0.0000j. defined without MHD jump: **yes**. S1 FAIL (P=0.5000+0.0000j, n_tie=3, max_on/max_off=1.0000). S2 FAIL (U(2π)=-0.9781-0.2079j |U+1|=0.209; U(4π)=0.9135+0.4067j |U-1|=0.416). S3 FAIL (|ΔU|_jump / |ΔU|_quiet = 0.9023). S4 PASS (drop=19890437907365468.0000 |U-1|_on=1.9890 |_off=0.0000). verdict: **misses Γ**.

## T6 uniform U(1) control

```
T6  uniform U(1), no defect  (control)
    A_x=−(B/2)y, A_y=+(B/2)x, B=1
    U[γ]=exp(i B Area)  independent of any site
```

P_site(on-loop)=uniform / none; P_site(off-loop)=uniform / none. defined without MHD jump: **yes**. S1 FAIL (P=uniform, max_on/max_off=1.0000 (flat)). S2 FAIL (U(2π)=0.9987+0.0518j |U+1|=1.999; U(4π)=0.9946+0.1034j |U-1|=0.104). S3 FAIL (|ΔU|_jump / |ΔU|_quiet = 1.9325). S4 FAIL (drop=1.0000 |U-1|_on=0.0518 |_off=0.0518). verdict: **global junk**.

## Table

| family | P_site | defined without MHD jump? | S1 | S2 | S3 | S4 | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 CS puncture | 0.5000+0.0000j | yes | FAIL | FAIL | FAIL | PASS | **misses Γ** |
| T2 foam | 0.5000+0.0000j | yes | FAIL | FAIL | FAIL | PASS | **misses Γ** |
| T3 holo | 0.5000+0.0000j | yes | FAIL | FAIL | FAIL | PASS | **misses Γ** |
| T4 worldsheet | 0.5000+0.0000j | yes | FAIL | FAIL | FAIL | PASS | **misses Γ** |
| T5 hybrid | 0.5000+0.0000j | yes | FAIL | FAIL | FAIL | PASS | **misses Γ** |
| T6 uniform U(1) control | uniform / none | yes | FAIL | FAIL | FAIL | FAIL | **global junk** |

## One sentence

**no scan prefers Γ without insertion**

Not a QG theorem. No Qin, leapfrog, Hall 3×3, dynamo phenomenology.

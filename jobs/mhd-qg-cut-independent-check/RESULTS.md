# Independent gravity letter on Γ

New folder. Hive not opened. Tearing not rerun. Pair A not rebuilt.
The dictionary $U_G=(-1)^{I(\gamma,\Gamma)}$, $da=\pi\delta_\Gamma$ is locked as tautological and is **not** used here.

## Gravity letter (Option G1)

Lattice $U(1)$ connection on a Cartesian mesh in the plane. Symmetric gauge of a **uniform** background field $B$. $F=dA=B$ (constant). No $\delta_\Gamma$. No pair A. No $I(\gamma,\Gamma)$. No $\mathrm{Arg}/\mathrm{atan2}$ branch cut.

```
A_x = − (B/2) y
A_y = + (B/2) x
F_xy = B
θ_{n,x̂} = A_x(n+x̂/2) Δx ,   U_ℓ = exp(i θ_ℓ)
U_□ = exp(i B Δx Δy)
U[γ] = ∏_{ℓ∈γ} U_ℓ
B = 1.0   # O(1), not fitted to U(2π)=−1
```

Option G2 was not used.

## MHD letter (reused, not rebuilt)

```
H_A(ε) = [[ -i a, ε v ], [ ε v, -i b ]]
v = -0.360253, η = 0.05, ε_EP = 0.513681
```
Used only to continue $n_{\mathrm{MHD}}$ around $+\varepsilon_{\mathrm{EP}}$ and to **score** I1–I4 against $\Gamma=[-\varepsilon_{\mathrm{EP}},\varepsilon_{\mathrm{EP}}]$. Not an input to $A$.

## Table I1–I4

| test | formula | number | pass |
| --- | --- | --- | --- |
| I1 support | $\overline{|F|/2\pi}_{\mathrm{on}\,\Gamma}\ /\ \overline{|F|/2\pi}_{\mathrm{off}\,\Gamma}$ | on=0.000397887, off=0.000397887, ratio=1.0000 (need >3 to peak on Γ) | **FAIL** |
| I2 sheet | $U(2\pi)\stackrel{?}{=}-1,\ U(4\pi)\stackrel{?}{=}+1$ | U(2π)=0.9987+0.0518j  |U+1|=1.9993; U(4π)=0.9946+0.1034j  |U-1|=0.1036; enclosed flux Bπr²=0.0518 rad (not fitted) | **FAIL** |
| I3 map | $\max|U-\exp(i\pi n_{\mathrm{MHD}})|\ \mathrm{at}\ (0,2\pi,4\pi)$ | max|U−Φ_hand|=1.9993 (need <0.2); corr(Arg U, n_MHD)=0.866, corr(Arg U, θ)=0.697 | **FAIL** |
| I4 control | $|U-1|_{\mathrm{loop\ on\ endpoint}}\ /\ |U-1|_{\mathrm{loop\ off\ }\Gamma}$ | shift drop-ratio=1.0000 (need >3); |U-1|_on=0.0518, |U-1|_off=0.0518; scramble CS on/off=1.0368 | **FAIL** |

- I1 support: CS density of uniform-B lattice. Γ used only as a mask after A is built.
- I2 sheet: Same loop family as pair-A endpoint continuation. A is uniform B, not π-flux.
- I3 map: Hand map Φ(n)=e^{iπ n} is the locked tautology. Here U comes from uniform-B holonomy.
- I4 control: Same radius, centre moved to +1.2i (off the real slit). If drop≈1 the letter is global (area law), not a cut connection. Scramble: random compact U(1) links on the same mesh.

## One sentence

**independent gravity letter does not land on Γ**

G1 could be defined (uniform $B$, no cut in $A$). It is global area-law junk: CS density is flat, $U(2\pi)\neq-1$, shifting the loop off $\Gamma$ does not drop the signal. The tautological cover is still the only letter that sat on $\Gamma$, and it was inserted by hand.

Not a theorem. No Qin, leapfrog, Hall 3×3, dynamo, or black hole.

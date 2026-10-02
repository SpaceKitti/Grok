# EP–reconnection operator  —  Object 0 then Object 1

New session, new folder. Dynamo control + tearing operator + scoring table only.
Source control: Günther–Stefani–Gerbeth, arXiv:math-ph/0407015.

## (A) Object 0 — 2×2 α²-dynamo toy

- Square-root Puiseux: **PASS**  (fitted exponent $p=0.5001$, $r=1.0000$, max rel residual $2.497\times 10^{-3}$).
- EP$_2$ 4π monodromy: **PASS**  (eigenvalue sheets swap at $2\pi$, return at $4\pi$; eval return distance $7.9\times 10^{-16}$).
- Diabolic contrast (Hermitian loop around the origin): min gap $0.70=2r$ (no branching).
- Locations: branching EP$_2$ on the cone $f^2-|b|^2=0$, $|b|\neq 0$ (algebraic multiplicity 2, geometric 1, Jordan block). Diabolic point at the origin (algebraic = geometric = 2).
- Object 0 overall: **PASS**. Proceed to Object 1.

Figure: `outputs/A_dynamo_spectrum_monodromy.png`.

## (B) Object 1 — Harris tearing / reconnection operator

Linearized incompressible resistive MHD on $B_x=\tanh z$, no Hall, no guide field. Inner layer resolved: $dz_\min=6.0\times 10^{-3}$ vs $\delta_\mathrm{SP}(S=200)=7.1\times 10^{-2}$.

- Operator self-check: **PASS**. $\gamma(S=200,ka=0.5)=+0.0288$ (even $\psi$), $\gamma(S=200,ka=1.3)\approx 0$ (stable). Unstable window is $ka<1$ i.e. $\Delta'>0$.
- Discrete EP$_2$ hunt: **none**. $n_\mathrm{defective}=0$. $R_\mathrm{EP}=\mathrm{nan}$. The $10^{-5}$ gaps at $ka>1$ are Alfvén-continuum discretisation (grid artefact on the spectral cut $\Gamma=[-k,k]$, not a Jordan block).
- Puiseux about an EP$_2$: **N/A** (no discrete coalescence to expand about).
- Monodromy around onset $(S,k)=(500,1)$ and around the smallest-gap point: **no 4π EP$_2$**. The tearing growth simply turns on and off as the loop crosses $\Delta'=0$.
- $R_\mathrm{conn}$: **lights on $\Delta'>0$** (even-$\psi$ eigenfunction splits the Harris null line into an X–O island chain at finite amplitude). It does **not** light on an EP, because there is no EP.
- Rate: FKR is the best match on the unstable grid. Measured $\gamma\sim S^{-0.46}$ at $ka=0.55$ over $S=50$–$2000$ (moderate-$S$; the large-$S$ constant-$\psi$ FKR exponent is $-3/5$). This scaling is inner-layer asymptotics, not an EP$_2$ gap.
- Lock: **FAIL**. No defective coalescence, no Puiseux, no 4π monodromy. $R_\mathrm{conn}$ and the FKR rate sit on the $\Delta'>0$ window; they do not sit on an EP.

Figures: `outputs/B_tearing_spectrum.png`, `outputs/B_tearing_monodromy.png`.

## (C) Scoring table

`outputs/C_scoring_table.csv` and `outputs/C_scoring_table.md`.

Columns: $(S,\Delta',R_\mathrm{EP},R_\mathrm{Puiseux},R_\mathrm{conn},\mathrm{rate},\mathrm{FKR}/\mathrm{SP}/\mathrm{Hall}/\mathrm{plasmoid})$, plus $\gamma$, gap, Petermann, $R_\mathrm{CS}$, $R_\mathrm{MHD}$, $n_\mathrm{sheet}$, $\Gamma_\mathrm{lo}$, $\Gamma_\mathrm{hi}$.

$R_\mathrm{EP}$ and $R_\mathrm{Puiseux}$ are nan on the whole grid (no discrete EP$_2$). $R_\mathrm{conn}=1$ iff $\Delta'>0$ and the even tearing mode is unstable. $R_\mathrm{mono}=1$ (no 4π EP$_2$). Hall is a comparison column only; the operator has no Hall term.

## (D) One sentence

**spectral decoration, not dictionary**

Tearing onset is a discrete mode peeling off the resistive regularisation of the Alfvén continuum (the spectral cut $\Gamma$), with FKR inner-layer scaling. That is not an EP$_2$ of branching type, and it does not make Riemann-EP = X-point a theorem.

## (E) Object 2

Object 1 did not lock. Object 2 is **not** run. No Hall, no guide field, no 3×3 spine-fan Hamiltonian.

## (F) $R_\mathrm{CS}$ vs $R_\mathrm{MHD}$ overlay

Figure: `outputs/F_RCS_RMHD_overlay.png`.

- Mean $R_\mathrm{CS}$ on/off $R_\mathrm{conn}$: $0.082$ / $0.129$.
- Mean $R_\mathrm{MHD}$ on/off $R_\mathrm{conn}$: $2.8\times 10^{-4}$ / $2.4\times 10^{-3}$.
- Neither lights on the $R_\mathrm{conn}$ interval (both are larger on the stable side, where the selected even eigenfunction is a damped continuum mode). Keep CS orthogonal. No black-hole or spin-foam theorem.

Hive-slot 0-forms (not written into any Qin $\nabla\cdot u$ or leapfrog): `n_sheet`, `Gamma_lo`, `Gamma_hi`, `R_EP`, `R_conn` in the CSV. The live support is the open Harris sheet; $\Gamma=[-k,k]$ is the Alfvén continuum interval; the K-neutral hex is not used here.

# MHD patches (`aethon/mhd-patches`)

Tiny B-E smoke (not a campaign). PowerShell:

```powershell
$env:PYTHONPATH = "C:\Users\Akitt\Grok\worktree-mhd\ns"
& "C:\Users\Akitt\Grok\.venv\Scripts\python.exe" "C:\Users\Akitt\Grok\worktree-mhd\ns\examples\test_mhd_solver.py"
```

- **GLM:** `mhd_params` `glm_ch=0` is the Qin projector (Dedner off). `glm_ch>0` enables Dedner psi; use `glm_cr=0.18`.
- **OT:** `ic="ot"` sets `b_guide="ot"` and uses `generate_u_ot`.
- **Alfvén:** `ic="alfven"` sets `b_guide="alfven"`: uniform guide plus a small transverse δv=-δb wiggle at v_A=|B0|.
- **cmhd:** mode="cmhd" evolves primitive u (dt u = ... -nabla p/rho + (J x B)/rho + nu lap u). Qin/Helmholtz/project_div_free off on u so sound lives; mode="mhd" stays projected vorticity. Continuity + Russell e_int (gamma=5/3) stay. CFL uses max(|u|+c_s+|v_A|) with c_s=sqrt(gamma p/rho). Sound-wave smoke: 1D acoustic phase speed ~ c_s. No rho pin/floor. No nabla p on the vorticity RHS.
- **Brio–Wu:** `ic="brio_wu"` on mode="cmhd" is a 1D MHD Riemann problem on the periodic torus (stop before wrap). Spectral; Gibbs ringing expected (rho may go negative — that is the scheme, not a continuity leak). gamma=2 is test-local via mhd_params/ic_params; Hive GAMMA_DEFAULT stays 5/3. No WENO/TVD, no rho pin/floor. Success is waves exist, no NaN — not a plot match. Do not interpret smear vs ribbon. Alfvén on mode="mhd" is unchanged.
- **I_leak:** mill (mode=mhd) stays `(e_tot+e_glm-that[0])+I_nu+I_eta+I_tau`. cmhd only: `I_leak=Delta(<1/2 rho |u|^2> + E_int + E_mag + e_glm)` (heat already in E_int; do not add int(eps_nu+eps_eta)). Field names: `I_leak`, `e_tot`, `e_kin`, `max_div_b`, `flux_x_half`, `flux_y_half`, `rec_rate_flux`, `E_rec`, `e_glm`, `max_psi`.
- **Hall:** `mode="hall"` is the same incompressible vorticity path as `mode="mhd"` (Qin/GLM kept). Ohm is `E = -u x B + eta J + (d_i/n) J x B` with `n=1` default; Faraday is `dt B = -curl E` (plus Dedner if `glm_ch!=0`). `d_i=0` matches `mode="mhd"`. Hall is dispersive, not heat (`I_leak` mill unchanged) and not a momentum body force. 2D with `d_i>0` stores Bz (2.5D) so whistlers can live. Smoke: `examples/test_hall.py`.
- **twofluid:** `mode="twofluid"` clones the hall path and adds electron pressure in Ohm (no electron inertia). Quasi-neutral `n_i = n_e = n`, `u_e = u_i - (d_i/n) J`, `E = -u_e x B - grad(p_e)/n + eta J`, `p_e = n T_e` with `T_e` const (default 0). Continuity on `n` (cmhd tracer, no pin/floor). `T_e=0` recovers Hall Ohm (same `d_i`, `n`). Ion Lorentz stays `J x B` (not a Hall body force). 2.5D Bz when `d_i>0` as in hall. `I_leak` mill unchanged. Smoke: `examples/test_twofluid.py`.
- Branch is `aethon/mhd-patches`. Do not merge to main unless asked.

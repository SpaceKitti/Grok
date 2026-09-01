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
- **I_leak:** includes `e_glm` when GLM is on (`glm_ch!=0`). Field names: `I_leak`, `e_tot`, `max_div_b`, `flux_x_half`, `flux_y_half`, `rec_rate_flux`, `E_rec`, `e_glm`, `max_psi`.
- Branch is `aethon/mhd-patches`. Do not merge to main unless asked.

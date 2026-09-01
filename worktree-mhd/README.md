# MHD patches (`aethon/mhd-patches`)

Tiny B-E smoke (not a campaign). PowerShell:

```powershell
$env:PYTHONPATH = "C:\Users\Akitt\Grok\worktree-mhd\ns"
& "C:\Users\Akitt\Grok\.venv\Scripts\python.exe" "C:\Users\Akitt\Grok\worktree-mhd\ns\examples\test_mhd_solver.py"
```

- **GLM:** `mhd_params` `glm_ch=0` is the Qin projector (Dedner off). `glm_ch>0` enables Dedner psi; use `glm_cr=0.18`.
- **OT:** `ic="ot"` sets `b_guide="ot"` and uses `generate_u_ot`.
- **I_leak field names:** `I_leak`, `e_tot`, `max_div_b`, `flux_x_half`, `flux_y_half`, `rec_rate_flux`, `E_rec`, `e_glm`, `max_psi`.
- Branch is `aethon/mhd-patches`. Do not merge to main unless asked.

"""Few-step MHD patch proofs. No campaigns."""
import os, sys
sys.path.insert(0, r"C:\Users\Akitt\Grok\worktree-mhd\ns")
os.environ.setdefault("JAX_PLATFORMS", "cpu")

import numpy as np
from chive_ns import run_framework, generate_u_ot, generate_b0, make_grid, project_div_free
import jax.numpy as jnp

def arr(x):
    return np.asarray(x)

results = []

def report(name, ok, detail):
    tag = "PASS" if ok else "FAIL"
    line = f"{tag} {name}: {detail}"
    print(line)
    results.append((name, ok, detail))

# 1) Energy identity, hydro off, force_on=False, eta_h=0
mp = dict(eta_hyper=0.0, glm_ch=0.0, B0=0.08, eta_mag=1e-3)
out = run_framework(
    N=16, dim=2, steps=8, mode="mhd", magnetic=True, viscoelastic=False,
    force_on=False, dt=0.002, diag_every=1, nu=0.001, mhd_params=mp, seed=0,
)
e0 = float(arr(out["e_tot"])[0])
ileak = arr(out["I_leak"])
ratio = abs(float(ileak[-1])) / (abs(e0) + 1e-30)
report("energy identity 2D", ratio < 1e-4, f"I_leak/E0={ratio:.3e} I_leak={float(ileak[-1]):.3e}")

out3 = run_framework(
    N=8, dim=3, steps=4, mode="mhd", magnetic=True, viscoelastic=False,
    force_on=False, dt=0.001, diag_every=1, nu=0.001, mhd_params=mp, seed=0,
    ic="taylor_green",
)
e03 = float(arr(out3["e_tot"])[0])
ileak3 = arr(out3["I_leak"])
ratio3 = abs(float(ileak3[-1])) / (abs(e03) + 1e-30)
report("energy identity 3D", ratio3 < 1e-4, f"I_leak/E0={ratio3:.3e} I_leak={float(ileak3[-1]):.3e}")

# 2) Reconnected flux monitor
fx = arr(out["flux_x_half"])
fy = arr(out["flux_y_half"])
ok2 = np.isfinite(fx).all() and np.isfinite(fy).all() and fx.shape[0] >= 2
report("reconnected flux", ok2, f"flux_x={float(fx[-1]):.4e} flux_y={float(fy[-1]):.4e} n={fx.shape[0]}")

# 3) Reconnection rate
rr = arr(out["rec_rate_flux"])
er = arr(out["E_rec"])
ok3 = np.isfinite(rr).all() and np.isfinite(er).all() and rr.shape == fx.shape
report("reconnection rate", ok3, f"rec_rate={float(rr[-1]):.4e} E_rec={float(er[-1]):.4e}")

# 4) Orszag-Tang matching u
g = make_grid(16, L=1.0, dim=2)
u = generate_u_ot(g, U0=1.0)
Bhat = generate_b0(g, B0=1.0, kind="ot")
B = jnp.fft.ifftn(Bhat, axes=range(1, 3)).real
u_hat = project_div_free(jnp.fft.fftn(u, axes=range(1, 3)), g)
div_u = float(jnp.max(jnp.abs(jnp.fft.ifftn(jnp.sum(g["k_stack"] * u_hat, axis=0)).real)))
div_b = float(jnp.max(jnp.abs(jnp.fft.ifftn(jnp.sum(g["k_stack"] * Bhat, axis=0)).real)))
# same trig skeleton: ux ~ -sin(2pi y), Bx ~ -sin(2pi y)
ux = np.asarray(u[0]); Bx = np.asarray(B[0])
corr = float(np.corrcoef(ux.ravel(), Bx.ravel())[0, 1])
out_ot = run_framework(
    N=16, dim=2, steps=4, mode="mhd", magnetic=True, viscoelastic=False,
    force_on=False, dt=0.002, diag_every=1, nu=0.001, ic="ot",
    mhd_params=dict(eta_hyper=0.0, glm_ch=0.0, B0=0.08, eta_mag=1e-3, ot_u0=1.0),
    seed=0,
)
ok4 = corr > 0.99 and div_u < 1e-10 and div_b < 1e-10 and out_ot["mhd_params"]["b_guide"] == "ot"
report("OT matching u", ok4, f"corr(u,B)={corr:.4f} div_u={div_u:.2e} div_b={div_b:.2e} b_guide={out_ot['mhd_params']['b_guide']}")

# 5) Dedner GLM. Projected OT has divB~0 so psi stays roundoff; seed a
# compressible magnetic mode and step the coupled GLM rhs.
from chive_ns.mhd import zero_psi_hat, glm_psi_rhs, zero_b_hat
from chive_ns.clay import zero_tau_hat
from chive_ns.vorticity import coupled_mhd_step
from chive_ns.grid import vorticity_from_velocity

g = make_grid(16, L=1.0, dim=2)
Bhat = generate_b0(g, B0=0.08, kind="ot")
B = np.array(jnp.fft.ifftn(Bhat, axes=(1, 2)).real, copy=True)
x = np.linspace(0.0, 1.0, 16, endpoint=False)
X, Y = np.meshgrid(x, x, indexing="ij")
B[0] = B[0] + 0.01 * np.cos(2.0 * np.pi * X)
Bhat = jnp.fft.fftn(jnp.asarray(B), axes=(1, 2))  # keep the divergence
psi0 = zero_psi_hat(g)
dpsi0 = glm_psi_rhs(psi0, Bhat, g, 1.0, 0.18)
dpsi_amp = float(jnp.max(jnp.abs(dpsi0)))
u = generate_u_ot(g, U0=1.0)
u_hat = project_div_free(jnp.fft.fftn(u, axes=(1, 2)), g)
omega = vorticity_from_velocity(u_hat, g)
tau = zero_tau_hat(g, dtype=omega.dtype)
psi = psi0
B_s = Bhat
for _ in range(8):
    omega, tau, B_s, psi = coupled_mhd_step(
        omega, tau, B_s, g, 0.001, 0.002, 0.0, "rk2", 0.0,
        0.0, 0.6, 0.085, 0.13, 1e-4, 0.0, 0.0, 0.0, None,
        1e-3, 0.0, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        psi, 1.0, 0.18)
psi_amp = float(jnp.max(jnp.abs(jnp.fft.ifftn(psi).real)))
divb = float(jnp.max(jnp.abs(jnp.fft.ifftn(1j * jnp.sum(g["k_stack"] * B_s, axis=0)).real)))
out_glm = run_framework(
    N=16, dim=2, steps=4, mode="mhd", magnetic=True, viscoelastic=False,
    force_on=False, dt=0.002, diag_every=1, nu=0.001, ic="ot",
    mhd_params=dict(eta_hyper=0.0, glm_ch=1.0, glm_cr=0.18, B0=0.08, eta_mag=1e-3),
    seed=0,
)
wired = "psi_hat" in out_glm and "e_glm" in out_glm and "max_psi" in out_glm
ok5 = dpsi_amp > 1e-8 and psi_amp > 1e-8 and np.isfinite(divb) and wired
report("Dedner GLM", ok5, f"dpsi0={dpsi_amp:.3e} max_psi={psi_amp:.3e} max_div_b={divb:.3e} wired={wired} psi_hat={out_glm['psi_hat'].shape}")

# glm_ch=0 still closes energy identity after GLM wiring
ratio_off = ratio  # already measured
report("GLM off identity", ratio < 1e-4, f"same as energy identity 2D I_leak/E0={ratio:.3e}")

failed = [r for r in results if not r[1]]
print("---")
print(f"{len(results)-len(failed)}/{len(results)} passed")
if failed:
    sys.exit(1)

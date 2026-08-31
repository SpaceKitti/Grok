"""Smoke the hybrid residual + regulariser dials on a tiny 3D clay run."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import (
    run_framework, hybrid_asgs_residual, live_diagnostics_and_feedback,
    DEFAULT_CLAY, make_grid, generate_taylor_green, project_div_free,
    vorticity_from_velocity, zero_tau_hat,
)
import jax.numpy as jnp


def main():
    print("DEFAULT_CLAY", DEFAULT_CLAY, flush=True)
    out = run_framework(
        dim=3, N=16, steps=20, ic="taylor_green", mode="clay",
        force_on=False, nu=5e-4, dt=0.002, diag_every=10, scheme="rk2",
    )
    print(f"E {float(out['energy'][0]):.5f}->{float(out['energy'][-1]):.5f}  "
          f"dE={(float(out['energy'][0])-float(out['energy'][-1]))/float(out['energy'][0]):.2%}  "
          f"max|w| {float(out['max_vort'][0]):.3f}->{float(out['max_vort'][-1]):.3f}  "
          f"work {float(out['work'][-1]):.3e}  lam {float(out['lambda_kin'][-1]):.3f}  "
          f"sheet {float(out['sheet_order'][-1]):.3f}  "
          f"I_bkm_w {float(out['I_bkm_w'][-1]):.3f}  "
          f"div {float(out['max_div'].max()):.2e}", flush=True)

    grid = make_grid(16, 1.0, 3)
    u = generate_taylor_green(grid)
    u_hat = project_div_free(jnp.fft.fftn(u, axes=(1, 2, 3)), grid)
    tau_hat = zero_tau_hat(grid)
    R = hybrid_asgs_residual(u_hat, tau_hat, grid, 5e-4, 0.003, 0.6)
    print("residual max|R_con|", float(jnp.max(jnp.abs(R["R_con"]))),
          "lambda_kin", float(R["lambda_kin"]), flush=True)

    live = live_diagnostics_and_feedback(
        u_hat, tau_hat, grid, 5e-4, 0.003, 0.6, 0.002)
    print("live T* / sheet / Gamma", float(live["Tstar"]),
          float(live["sheet_order"]), float(live["Gamma"]), flush=True)


if __name__ == "__main__":
    main()

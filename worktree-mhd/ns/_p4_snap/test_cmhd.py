"""Tiny cmhd smoke: uniform RHS=0, 3b bump advection, patch-4 energy.

Helmholtz-on; not acoustics. No mean-pin and no floor in the solver.
Uniform smoke is the RHS=0 check and is not sufficient alone.
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
import jax.numpy as jnp
from chive_ns import (
    run_framework, make_grid, project_div_free,
    bump_rho_hat, continuity_step, density_diagnostics,
)


def _arr(x):
    return np.asarray(x)


def _uniform_smoke():
    out = run_framework(
        N=16, dim=2, steps=8, dt=5e-4, diag_every=8, scheme="rk2",
        mode="cmhd", force_on=False, viscoelastic=False,
        mhd_params=dict(eta_hyper=0.0, glm_ch=0.0),
    )
    rho = np.fft.ifftn(_arr(out["rho_hat"])).real
    max_rho_m1 = float(np.max(np.abs(rho - 1.0)))
    hist_m1 = float(np.max(np.abs(_arr(out["max_abs_rho_m1"]))))
    max_drho = float(np.max(np.abs(_arr(out["max_drho_dt"]))))
    mean_rho = float(np.mean(rho))
    leftover = mean_rho - 1.0
    print(
        f"cmhd uniform rho: max|rho-1|={max_rho_m1:.6e} "
        f"hist max|rho-1|={hist_m1:.6e} max|d_t rho|={max_drho:.6e} "
        f"mean_rho={mean_rho:.16f} <rho>-1={leftover:.6e}",
        flush=True,
    )
    ok = (
        out.get("rho_hat") is not None
        and np.isfinite(max_rho_m1)
        and max_rho_m1 < 1e-12
        and hist_m1 < 1e-12
        and max_drho < 1e-12
    )
    if not ok:
        print(
            f"FAIL cmhd uniform rho leftover too large: "
            f"max|rho-1|={max_rho_m1:.3e} max|d_t rho|={max_drho:.3e}",
            flush=True,
        )
        return False
    print("SMOKE CMHD uniform RHS=0 OK", flush=True)
    return True


def _bump_advection():
    """rho = 1+eps sin(2 pi x/L) advected by uniform solenoidal u=(U,0)."""
    N, L = 32, 1.0
    eps, U = 0.01, 0.4
    dt, steps = 0.005, 50
    T = steps * dt
    grid = make_grid(N, L=L, dim=2)
    rho_hat = bump_rho_hat(grid, eps=eps)
    u = np.zeros((2, N, N), dtype=np.float64)
    u[0] = U
    u_hat = project_div_free(jnp.fft.fftn(jnp.asarray(u), axes=(1, 2)), grid)
    rho0 = np.fft.ifftn(_arr(rho_hat)).real
    for _ in range(steps):
        rho_hat = continuity_step(rho_hat, u_hat, grid, dt, "rk2")
    rho = np.fft.ifftn(_arr(rho_hat)).real
    d = density_diagnostics(rho_hat, u_hat, grid)
    mean_rho = float(_arr(d["mean_rho"]))
    leftover = mean_rho - 1.0
    min_rho = float(_arr(d["min_rho"]))
    max_delta = float(np.max(np.abs(rho - rho0)))
    x = np.linspace(0.0, L, N, endpoint=False)
    Xg = np.meshgrid(x, x, indexing="ij")[0]
    expected = 1.0 + eps * np.sin(2.0 * np.pi * (Xg - U * T) / L)
    corr = float(np.corrcoef(rho.ravel(), expected.ravel())[0, 1])
    prof = rho.mean(axis=1) - 1.0
    phase = float(np.angle(np.fft.fft(prof)[1]))
    phase0 = float(np.angle(np.fft.fft((rho0.mean(axis=1) - 1.0))[1]))
    dphi = float(np.unwrap(np.array([phase0, phase]))[1] - phase0)
    dphi_exp = -2.0 * np.pi * U * T / L
    print(
        f"cmhd bump advect: <rho>-1={leftover:.6e} min_rho={min_rho:.8f} "
        f"max|rho-rho0|={max_delta:.6e} corr={corr:.6f} "
        f"dphi={dphi:.6f} dphi_exp={dphi_exp:.6f} T={T:.4f} U={U}",
        flush=True,
    )
    failed = []
    if not (min_rho > 0.0):
        failed.append(f"min_rho={min_rho}")
    if abs(leftover) >= 1e-12:
        failed.append(f"<rho>-1={leftover}")
    if max_delta <= 1e-3:
        failed.append(f"bump did not move max|rho-rho0|={max_delta}")
    if not (corr > 0.99):
        failed.append(f"shape corr={corr}")
    if abs(dphi - dphi_exp) >= 0.05:
        failed.append(f"phase dphi={dphi} vs {dphi_exp}")
    if failed:
        print("FAIL cmhd bump: " + ", ".join(failed), flush=True)
        return False
    print("SMOKE CMHD bump advects OK", flush=True)
    return True


def _no_backreaction():
    common = dict(
        N=16, dim=2, steps=8, dt=5e-4, diag_every=8, scheme="rk2",
        mode="cmhd", force_on=False, viscoelastic=False, seed=0,
        mhd_params=dict(eta_hyper=0.0, glm_ch=0.0),
    )
    out0 = run_framework(**common)
    outb = run_framework(ic_params=dict(rho_eps=0.01), **common)
    u0 = _arr(out0["u_hat"])
    ub = _arr(outb["u_hat"])
    du = float(np.max(np.abs(ub - u0)))
    rho = np.fft.ifftn(_arr(outb["rho_hat"])).real
    leftover = float(np.mean(rho) - 1.0)
    min_rho = float(np.min(rho))
    print(
        f"cmhd no back-reaction: max|u_bump-u_uni|={du:.6e} "
        f"<rho>-1={leftover:.6e} min_rho={min_rho:.8f}",
        flush=True,
    )
    if du >= 1e-14:
        print(f"FAIL cmhd bump back-reacted on u: {du:.3e}", flush=True)
        return False
    if not (min_rho > 0.0):
        print(f"FAIL cmhd coupled bump min_rho={min_rho}", flush=True)
        return False
    print("SMOKE CMHD no back-reaction OK", flush=True)
    return True


def _energy_smoke():
    gamma = 5.0 / 3.0
    p0 = 1.0
    out = run_framework(
        N=16, dim=2, steps=8, dt=5e-4, diag_every=1, scheme="rk2",
        mode="cmhd", force_on=False, viscoelastic=False,
        mhd_params=dict(eta_hyper=0.0, glm_ch=0.0, gamma=gamma, p0=p0),
    )
    e = _arr(out["mean_e_int"])
    t = _arr(out["time"])
    Q = _arr(out["mean_Q"])
    dE = float(e[-1] - e[0])
    IQ = float(np.sum(0.5 * (Q[1:] + Q[:-1]) * np.diff(t))) if t.size > 1 else 0.0
    IQ2 = float(_arr(out["I_nu"])[-1] + _arr(out["I_eta"])[-1])
    gamma_hist = float(_arr(out["gamma"])[-1])
    p = np.fft.ifftn(_arr(out["p_hat"])).real
    leftover_p = float(np.mean(p)) - p0
    print(
        f"cmhd energy: Delta E_int={dE:.6e} int_Q={IQ:.6e} "
        f"I_nu+I_eta={IQ2:.6e} gamma={gamma_hist:.12f} "
        f"mean_p={float(np.mean(p)):.16f} leftover_p={leftover_p:.6e}",
        flush=True,
    )
    failed = []
    if abs(gamma_hist - gamma) >= 1e-12:
        failed.append(f"gamma={gamma_hist}")
    scale = max(abs(dE), abs(IQ), 1e-16)
    if abs(dE - IQ) / scale >= 0.05:
        failed.append(f"Delta E_int={dE} vs int_Q={IQ}")
    if failed:
        print("FAIL cmhd energy: " + ", ".join(failed), flush=True)
        return False
    print("SMOKE CMHD energy Q OK", flush=True)
    return True


def main():
    failed = []
    if not _uniform_smoke():
        failed.append("uniform")
    if not _bump_advection():
        failed.append("bump")
    if not _no_backreaction():
        failed.append("back-reaction")
    if not _energy_smoke():
        failed.append("energy")
    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE CMHD OK", flush=True)


if __name__ == "__main__":
    main()

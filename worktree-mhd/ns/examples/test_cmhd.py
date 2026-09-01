"""Tiny cmhd smoke: 1D sound at c_s, rest RHS=0, bump advection, Russell energy.

Primitive u; Qin/Helmholtz off on cmhd. No mean-pin and no floor in the solver.
FIRST TEST is a 1D sound wave at c_s (not Brio-Wu, not Alfven).
mode=mhd stays Qin-projected.
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
    bump_rho_hat, bump_p_hat, continuity_step, density_diagnostics,
    sound_wave_fields, GAMMA_DEFAULT, coupled_cmhd_step,
    uniform_rho_hat, uniform_p_hat, max_abs_div_u,
    zero_tau_hat, zero_b_hat,
)


def _arr(x):
    return np.asarray(x)


def _sound_wave():
    """1D traveling acoustic wave on a 1D-like 2D grid. v_phase / c_s ~ 1."""
    gamma = float(GAMMA_DEFAULT)
    p0, rho0, eps = 1.0, 1.0, 1e-3
    N, L = 16, 1.0
    dt, steps = 0.005, 40
    T = steps * dt
    cs = float(np.sqrt(gamma * p0 / rho0))
    out = run_framework(
        N=N, dim=2, steps=steps, dt=dt, diag_every=steps, scheme="rk2",
        mode="cmhd", ic="sound", force_on=False, viscoelastic=False, nu=0.0,
        ic_params=dict(sound_eps=eps, rho0=rho0),
        mhd_params=dict(
            B0=0.0, eta_mag=0.0, eta_hyper=0.0, glm_ch=0.0,
            gamma=gamma, p0=p0,
        ),
    )
    grid = make_grid(N, L=L, dim=2)
    _u0, rho0f, _p0f, cs_f = sound_wave_fields(
        grid, eps=eps, rho0=rho0, p0=p0, gamma=gamma)
    rho0_phys = _arr(rho0f)
    rho = np.fft.ifftn(_arr(out["rho_hat"])).real
    max_div = float(_arr(max_abs_div_u(out["u_hat"], out["grid"])))

    def _phase_x(field):
        prof = np.mean(np.asarray(field), axis=1)
        return float(np.angle(np.fft.fft(prof)[1]))

    phi0 = _phase_x(rho0_phys)
    phi1 = _phase_x(rho)
    dphi = float(np.unwrap(np.array([phi0, phi1]))[1] - phi0)
    k = 2.0 * np.pi / L
    v_phase = -dphi / (k * T + 1e-30)
    ratio = v_phase / (cs + 1e-30)
    amp0 = float(np.max(np.abs(rho0_phys - rho0)))
    amp1 = float(np.max(np.abs(rho - rho0)))
    print(
        f"cmhd sound: v_phase={v_phase:.6f} c_s={cs:.6f} v_phase/c_s={ratio:.6f} "
        f"dphi={dphi:.6f} T={T:.4f} max_div={max_div:.6e} "
        f"amp0={amp0:.6e} amp1={amp1:.6e} cs_f={float(cs_f):.6f}",
        flush=True,
    )
    failed = []
    if abs(ratio - 1.0) >= 0.1:
        failed.append(f"v_phase/c_s={ratio}")
    if max_div <= 1e-8:
        failed.append(f"Qin still on? max_div={max_div}")
    if amp1 < 0.5 * amp0:
        failed.append(f"wave died amp1={amp1} amp0={amp0}")
    if failed:
        print("FAIL cmhd sound: " + ", ".join(failed), flush=True)
        return False
    print("SMOKE CMHD sound wave OK", flush=True)
    return True


def _rest_state(grid):
    N, dim = int(grid["N"]), int(grid["dim"])
    u = jnp.zeros((dim,) + (N,) * dim, dtype=jnp.float64)
    u_hat = jnp.fft.fftn(u, axes=range(1, dim + 1))
    tau = zero_tau_hat(grid, dtype=jnp.complex128)
    B = zero_b_hat(grid, dtype=jnp.complex128)
    rho = uniform_rho_hat(grid, rho0=1.0)
    return u_hat, tau, B, rho


def _uniform_smoke():
    """Rest + uniform rho/p: continuity and momentum RHS stay ~0."""
    grid = make_grid(16, L=1.0, dim=2)
    u_hat, tau, B, rho = _rest_state(grid)
    p = uniform_p_hat(grid, p0=1.0)
    dt, steps = 5e-4, 8
    for _ in range(steps):
        u_hat, tau, B, _psi, rho, p = coupled_cmhd_step(
            u_hat, tau, B, rho, p, grid, 0.001, dt,
            0, "rk2", 0.0,
            0.0, 0.6, 0.085, 0.13, 1e-4, 0.0, 0.0, 0.0, None,
            1e-3, 0.0, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            None, 0.0, 0.18, 5.0 / 3.0)
    rho_x = np.fft.ifftn(_arr(rho)).real
    u = np.fft.ifftn(_arr(u_hat), axes=(1, 2)).real
    max_rho_m1 = float(np.max(np.abs(rho_x - 1.0)))
    max_u = float(np.max(np.abs(u)))
    divu = float(_arr(max_abs_div_u(u_hat, grid)))
    mean_rho = float(np.mean(rho_x))
    leftover = mean_rho - 1.0
    print(
        f"cmhd uniform rest: max|rho-1|={max_rho_m1:.6e} max|u|={max_u:.6e} "
        f"max|div u|={divu:.6e} mean_rho={mean_rho:.16f} <rho>-1={leftover:.6e}",
        flush=True,
    )
    ok = (
        np.isfinite(max_rho_m1) and max_rho_m1 < 1e-12
        and max_u < 1e-12 and divu < 1e-12
    )
    if not ok:
        print(
            f"FAIL cmhd uniform rest leftover too large: "
            f"max|rho-1|={max_rho_m1:.3e} max|u|={max_u:.3e} max|div u|={divu:.3e}",
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


def _energy_smoke():
    gamma = 5.0 / 3.0
    p0 = 1.0
    out = run_framework(
        N=16, dim=2, steps=8, dt=5e-4, diag_every=1, scheme="rk2",
        mode="cmhd", force_on=False, viscoelastic=False,
        ic_params=dict(u_scale=0.0),
        mhd_params=dict(eta_hyper=0.0, glm_ch=0.0, gamma=gamma, p0=p0, B0=0.0),
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


def _pressure_bump_acoustics():
    """Rest + p bump: Helmholtz-off must produce nonzero div u (acoustics seed)."""
    grid = make_grid(16, L=1.0, dim=2)
    u_hat, tau, B, rho = _rest_state(grid)
    p = bump_p_hat(grid, eps=0.01, p0=1.0)
    dt, steps = 5e-4, 4
    for _ in range(steps):
        u_hat, tau, B, _psi, rho, p = coupled_cmhd_step(
            u_hat, tau, B, rho, p, grid, 0.001, dt,
            0, "rk2", 0.0,
            0.0, 0.6, 0.085, 0.13, 1e-4, 0.0, 0.0, 0.0, None,
            1e-3, 0.0, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            None, 0.0, 0.18, 5.0 / 3.0)
    div_cmhd = float(_arr(max_abs_div_u(u_hat, grid)))
    u_proj = project_div_free(u_hat, grid)
    div_proj = float(_arr(max_abs_div_u(u_proj, grid)))
    out_mhd = run_framework(
        N=16, dim=2, steps=8, dt=5e-4, diag_every=8, scheme="rk2",
        mode="mhd", force_on=False, viscoelastic=False,
        mhd_params=dict(eta_hyper=0.0, glm_ch=0.0),
    )
    div_mhd = float(_arr(max_abs_div_u(out_mhd["u_hat"], out_mhd["grid"])))
    print(
        f"cmhd pressure bump: max|div u|={div_cmhd:.6e} "
        f"after Qin on same u={div_proj:.6e} "
        f"mode=mhd max|div u|={div_mhd:.6e}",
        flush=True,
    )
    failed = []
    if not (div_cmhd > 1e-8):
        failed.append(f"cmhd max|div u| still roundoff {div_cmhd}")
    if not (div_proj < 1e-10):
        failed.append(f"Qin on cmhd u not killed {div_proj}")
    if not (div_mhd < 1e-10):
        failed.append(f"mode=mhd still projected? max|div u|={div_mhd}")
    if failed:
        print("FAIL cmhd acoustics: " + ", ".join(failed), flush=True)
        return False
    print("SMOKE CMHD pressure-bump acoustics OK", flush=True)
    return True


def main():
    failed = []
    if not _sound_wave():
        failed.append("sound")
    if not _uniform_smoke():
        failed.append("uniform")
    if not _bump_advection():
        failed.append("bump")
    if not _energy_smoke():
        failed.append("energy")
    if not _pressure_bump_acoustics():
        failed.append("acoustics")
    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE CMHD OK", flush=True)


if __name__ == "__main__":
    main()

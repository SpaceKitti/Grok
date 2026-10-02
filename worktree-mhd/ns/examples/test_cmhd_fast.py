"""G2: 1D perpendicular fast magnetosonic on mode=cmhd only.

v_phase vs sqrt(c_s^2 + v_A^2). Short N, few periods. mode=mhd untouched.
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import run_framework, make_grid, GAMMA_DEFAULT, magnetosonic_fields


def _arr(x):
    return np.asarray(x)


def main():
    gamma = float(GAMMA_DEFAULT)
    p0, rho0, B0, eps = 1.0, 1.0, 1.0, 1e-3
    N, L = 16, 1.0
    cs = float(np.sqrt(gamma * p0 / rho0))
    vA = float(B0 / np.sqrt(rho0))
    vf = float(np.sqrt(cs * cs + vA * vA))
    # 0.4 period so two-point phase unwrap stays inside (-π, π).
    T_period = L / vf
    dt = 0.005
    steps = max(8, int(round(0.4 * T_period / dt)))
    T = steps * dt
    out = run_framework(
        N=N, dim=2, steps=steps, dt=dt, diag_every=steps, scheme="rk2",
        mode="cmhd", ic="magnetosonic", force_on=False, viscoelastic=False,
        nu=0.0,
        ic_params=dict(sound_eps=eps, rho0=rho0),
        mhd_params=dict(
            B0=B0, eta_mag=0.0, eta_hyper=0.0, glm_ch=0.0,
            gamma=gamma, p0=p0,
        ),
    )
    grid = make_grid(N, L=L, dim=2)
    _u0, rho0f, _p0f, _B0f, vf_f, cs_f, vA_f = magnetosonic_fields(
        grid, eps=eps, rho0=rho0, p0=p0, B0=B0, gamma=gamma)
    rho0_phys = _arr(rho0f)
    rho = np.fft.ifftn(_arr(out["rho_hat"])).real

    def _phase_x(field):
        prof = np.mean(np.asarray(field), axis=1)
        return float(np.angle(np.fft.fft(prof)[1]))

    phi0 = _phase_x(rho0_phys)
    phi1 = _phase_x(rho)
    dphi = float(np.unwrap(np.array([phi0, phi1]))[1] - phi0)
    k = 2.0 * np.pi / L
    v_phase = -dphi / (k * T + 1e-30)
    ratio = v_phase / (vf + 1e-30)
    e0 = float(_arr(out["e_kin"])[0] + _arr(out["e_int"])[0]
               + _arr(out["e_mag_tot"])[0] + _arr(out["e_glm"])[0])
    ileak = float(_arr(out["I_leak"])[-1])
    leak_ratio = abs(ileak) / (abs(e0) + 1e-30)
    min_rho = float(np.min(rho))
    print(
        f"cmhd fast: v_phase={v_phase:.6f} sqrt(c_s^2+v_A^2)={vf:.6f} "
        f"ratio={ratio:.6f} I_leak/E0={leak_ratio:.6e} min_rho={min_rho:.6e} "
        f"c_s={cs:.6f} v_A={vA:.6f} T={T:.4f} periods={T / T_period:.2f} "
        f"N={N} steps={steps} vf_f={float(vf_f):.6f} cs_f={float(cs_f):.6f} "
        f"vA_f={float(vA_f):.6f} mode={out.get('ic')}",
        flush=True,
    )
    failed = []
    if abs(ratio - 1.0) >= 0.1:
        failed.append(f"ratio={ratio}")
    if not np.isfinite(min_rho):
        failed.append("min_rho not finite")
    if failed:
        print("FAIL cmhd fast: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE CMHD G2 fast OK", flush=True)


if __name__ == "__main__":
    main()

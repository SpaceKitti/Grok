"""Tiny Brio-Wu smoke: cmhd 1D MHD Riemann on a periodic torus.

Paper gamma=2 is test-local via mhd_params. Hive GAMMA_DEFAULT stays 5/3.
Stop before wrap. Spectral Gibbs ringing expected (rho may go negative).
Success is waves exist, no NaN — not a plot match. No WENO/TVD, no floor.
mode=mhd / Alfven untouched. Primitive cmhd stepper.
"""
import os
import sys
from pathlib import Path

os.environ.setdefault('JAX_PLATFORMS', 'cpu')
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update('jax_enable_x64', True)

import numpy as np
from chive_ns import (
    run_framework, make_grid, GAMMA_DEFAULT,
    brio_wu_wrap_time, primitive_cmhd_step,
)


def _arr(x):
    return np.asarray(x)


def main():
    N, dt, steps = 64, 0.001, 20
    T = steps * dt
    gamma = 2.0
    hive_gamma = float(GAMMA_DEFAULT)
    grid = make_grid(N, L=1.0, dim=2)
    t_wrap = float(_arr(brio_wu_wrap_time(grid, gamma=gamma)))
    out = run_framework(
        N=N, dim=2, steps=steps, dt=dt, diag_every=steps, scheme='rk2',
        mode='cmhd', ic='brio_wu', force_on=False, viscoelastic=False, nu=0.001,
        ic_params=dict(gamma=gamma),
        mhd_params=dict(
            eta_mag=1.0e-3, eta_hyper=0.0, glm_ch=0.0,
            gamma=gamma,
        ),
    )
    rho = np.fft.ifftn(_arr(out['rho_hat'])).real
    p = np.fft.ifftn(_arr(out['p_hat'])).real
    u = np.fft.ifftn(_arr(out['u_hat']), axes=(1, 2)).real
    B = np.fft.ifftn(_arr(out['B_hat']), axes=(1, 2)).real
    gamma_hist = float(_arr(out['gamma'])[-1])
    min_rho, max_rho = float(np.min(rho)), float(np.max(rho))
    min_p, max_p = float(np.min(p)), float(np.max(p))
    max_u = float(np.max(np.abs(u)))
    finite = all(np.isfinite(a).all() for a in (rho, p, u, B))
    nan_yes = (not finite) or (not np.isfinite(gamma_hist))
    before_wrap = T < t_wrap
    waves = max_u > 1e-8
    print(
        f'cmhd brio_wu: crash=no NaN={"yes" if nan_yes else "no"} '
        f'gamma_test={gamma:.12f} gamma_hist={gamma_hist:.12f} '
        f'GAMMA_DEFAULT={hive_gamma:.12f} N={N} Ny={N} (1D-like) '
        f't={T:.6f} t_wrap={t_wrap:.6f} before_wrap={before_wrap} '
        f'min/max rho={min_rho:.6e}/{max_rho:.6e} '
        f'min/max p={min_p:.6e}/{max_p:.6e} max|u|={max_u:.6e} '
        f'ic={out.get("ic")} stepper=primitive_cmhd_step',
        flush=True,
    )
    print(
        '  (spectral Gibbs ringing expected; rho may go negative; '
        'do not interpret smear vs ribbon)',
        flush=True,
    )
    failed = []
    if abs(hive_gamma - 5.0 / 3.0) >= 1e-12:
        failed.append(f'Hive GAMMA_DEFAULT changed {hive_gamma}')
    if abs(gamma_hist - gamma) >= 1e-12:
        failed.append(f'gamma_hist={gamma_hist} not test-local 2')
    if out.get('ic') != 'brio_wu':
        failed.append(f'ic={out.get("ic")}')
    if nan_yes:
        failed.append('NaN')
    if not before_wrap:
        failed.append(f't={T} not before wrap t_wrap={t_wrap}')
    if not waves:
        failed.append(f'waves missing max|u|={max_u}')
    if primitive_cmhd_step is None:
        failed.append('primitive_cmhd_step missing')
    if failed:
        print('FAIL cmhd brio_wu: ' + ', '.join(failed), flush=True)
        return False
    print('SMOKE CMHD Brio-Wu OK (waves exist, no NaN, before wrap)', flush=True)
    return True


if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)

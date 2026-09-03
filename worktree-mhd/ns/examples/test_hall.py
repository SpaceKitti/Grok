"""Tiny Hall-MHD smoke: Alfven off vs on. Stage 1 only. No Crow / 0% / B0."""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import run_framework, generate_u_alfven, make_grid


def _arr(x):
    return np.asarray(x)


def _finite(out, keys):
    bad = []
    for k in keys:
        v = _arr(out[k])
        if not np.all(np.isfinite(v)):
            bad.append(k)
    return bad


def _phase_ratio(out, amp, B0, N, L, dt, steps):
    u = np.fft.ifftn(np.asarray(out["u_hat"]), axes=(1, 2)).real
    grid0 = make_grid(N, L=L, dim=2)
    u0 = np.asarray(generate_u_alfven(grid0, amp=amp))

    def _phase_y(fx):
        profile = np.mean(np.asarray(fx), axis=0)
        return float(np.angle(np.fft.fft(profile)[1]))

    phi0 = _phase_y(u0[0])
    phi1 = _phase_y(u[0])
    dphi = float(np.unwrap(np.array([phi0, phi1]))[1] - phi0)
    T = steps * dt
    k = 2.0 * np.pi / L
    v_A = abs(B0)
    v_phase = -dphi / (k * T + 1e-30)
    return v_phase, v_A, v_phase / (v_A + 1e-30)


def _leak(out):
    e0 = float(_arr(out["e_tot"])[0])
    ileak = float(_arr(out["I_leak"])[-1])
    return abs(ileak) / (abs(e0) + 1e-30), ileak, e0


def main():
    failed = []

    def check(name, ok, detail):
        tag = "PASS" if ok else "FAIL"
        print(f"{tag} {name}: {detail}", flush=True)
        if not ok:
            failed.append(name)

    B0 = 1.0
    amp = 0.05
    L = 1.0
    N = 16
    dt = 0.01
    steps = 20
    keys = ("energy", "e_tot", "I_leak", "max_div_b", "e_mag_tot")
    common = dict(
        N=N, dim=2, steps=steps, dt=dt, diag_every=steps, scheme="rk2",
        ic="alfven", force_on=False, viscoelastic=False, nu=1e-4,
    )
    mp0 = dict(B0=B0, alfven_amp=amp, eta_mag=1e-4, glm_ch=0.0, eta_hyper=0.0, d_i=0.0)

    out_mhd = run_framework(mode="mhd", mhd_params=dict(mp0), **common)
    out_h0 = run_framework(mode="hall", mhd_params=dict(mp0), **common)

    bad_m = _finite(out_mhd, keys)
    bad_h0 = _finite(out_h0, keys)
    check("mhd no NaN", not bad_m, f"bad={bad_m}")
    check("hall d_i=0 no NaN", not bad_h0, f"bad={bad_h0}")

    vp_m, va_m, r_m = _phase_ratio(out_mhd, amp, B0, N, L, dt, steps)
    vp_h0, va_h0, r_h0 = _phase_ratio(out_h0, amp, B0, N, L, dt, steps)
    print(
        f"d_i=0  mhd:  v_phase={vp_m:.6f} v_A={va_m:.6f} v_phase/v_A={r_m:.6f}",
        flush=True,
    )
    print(
        f"d_i=0  hall: v_phase={vp_h0:.6f} v_A={va_h0:.6f} v_phase/v_A={r_h0:.6f}",
        flush=True,
    )
    check("mhd Alfven phase", abs(r_m - 1.0) < 0.1, f"ratio={r_m:.6f}")
    check("hall d_i=0 Alfven phase", abs(r_h0 - 1.0) < 0.1, f"ratio={r_h0:.6f}")
    check("hall d_i=0 matches mhd phase", abs(r_h0 - r_m) < 1e-8, f"dh={abs(r_h0-r_m):.3e}")

    # Hall on: whistlers expected; do not demand the same v_A.
    dt_h = 5e-4
    steps_h = 40
    common_h = dict(common, steps=steps_h, dt=dt_h, diag_every=steps_h)
    out_h = run_framework(
        mode="hall",
        mhd_params=dict(mp0, d_i=0.05, n_hall=1.0),
        **common_h,
    )
    bad_h = _finite(out_h, keys)
    check("hall d_i=0.05 no NaN", not bad_h, f"bad={bad_h}")
    r_h, ileak_h, e0_h = _leak(out_h)
    div_h = float(_arr(out_h["max_div_b"])[-1])
    div0 = float(_arr(out_h["max_div_b"])[0])
    print(
        f"d_i=0.05 hall: I_leak/E0={r_h:.6e} I_leak={ileak_h:.6e} E0={e0_h:.6e} "
        f"max|divB|[-1]={div_h:.6e} max|divB|[0]={div0:.6e} dt={dt_h}",
        flush=True,
    )
    check("hall d_i=0.05 I_leak finite", np.isfinite(ileak_h) and np.isfinite(e0_h),
          f"I_leak={ileak_h:.3e} E0={e0_h:.3e}")
    check("hall d_i=0.05 divB not exploded", np.isfinite(div_h) and abs(div_h) < 1e-3,
          f"max|divB|={div_h:.3e}")

    r_mhd, ileak_m, e0_m = _leak(out_mhd)
    r_h0l, ileak_h0, e0_h0 = _leak(out_h0)
    div_m = float(_arr(out_mhd["max_div_b"])[-1])
    div_h0 = float(_arr(out_h0["max_div_b"])[-1])

    print(
        "HAVE hall | "
        f"mhd crash=0 nan={int(bool(bad_m))} vph/vA={r_m:.6f} I_leak/E0={r_mhd:.3e} max|divB|={div_m:.3e} | "
        f"hall_di0 crash=0 nan={int(bool(bad_h0))} vph/vA={r_h0:.6f} I_leak/E0={r_h0l:.3e} max|divB|={div_h0:.3e} | "
        f"hall_di=0.05 crash=0 nan={int(bool(bad_h))} I_leak/E0={r_h:.3e} I_leak={ileak_h:.3e} E0={e0_h:.3e} max|divB|={div_h:.3e}",
        flush=True,
    )

    if failed:
        print("FAILED: " + ", ".join(failed), flush=True)
        sys.exit(1)
    print("SMOKE HALL OK", flush=True)


if __name__ == "__main__":
    main()

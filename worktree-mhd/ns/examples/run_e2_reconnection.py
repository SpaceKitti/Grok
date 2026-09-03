"""E2c mill: Harris n ~ sech^2 peel, hall vs twofluid (Te>0). Not Crow, not SP.

n = n_bg + n1 sech^2((y - L/2)/delta) with n_bg=0.25, n1=0.75 (no floor).
Same thick Harris + edge seed as examples/test_harris_meter.py.
Phi = <Bx>_{y<L/2} * (L/2); rate_norm = rec_rate_flux * (L/2) / (v_A B0).
v_A = B0 / sqrt(n_bg)  (Harris lobe / background density; printed).
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import (
    make_grid, run_framework, split_guide_fields, cfl_dt_mhd, generate_harris_n,
)


def _arr(x):
    return np.asarray(x, dtype=float)


def _phi_from_mean_bx(flux_x_half, L):
    """Phi = <Bx>_{y<L/2} * (L/2). mill flux_x_half is the mean, not the integral."""
    return _arr(flux_x_half) * (0.5 * float(L))


def _rate_norm(rec_rate_flux, L, v_A, B0):
    """-dPhi/dt /(v_A B0) = rec_rate_flux * (L/2) / (v_A B0)."""
    return _arr(rec_rate_flux) * (0.5 * float(L)) / (float(v_A) * float(B0) + 1e-30)


def _print_table(label, t, phi, rec, rnorm, jmax):
    print(f"--- {label} ---", flush=True)
    print(
        f"{'t':>10} {'Phi':>14} {'rec_rate_flux':>16} {'rate_norm':>14} {'max|J|':>14}",
        flush=True,
    )
    for i in range(t.size):
        print(
            f"{t[i]:10.4f} {phi[i]:14.6e} {rec[i]:16.6e} {rnorm[i]:14.6e} {jmax[i]:14.6e}",
            flush=True,
        )


def _phi_transfers(phi):
    p0, p1 = float(phi[0]), float(phi[-1])
    sign_change = (p0 * p1) < 0.0
    dropped = abs(p1) < 0.5 * abs(p0)
    return sign_change, dropped, p0, p1


def _run_one(mode, mhd_params, N, steps, dt, diag_every, nu):
    return run_framework(
        N=N, dim=2, steps=steps, dt=dt, diag_every=diag_every, scheme="rk2",
        mode=mode, ic="smooth", force_on=False, viscoelastic=False, nu=nu,
        ic_params=dict(u_scale=0.0),
        mhd_params=mhd_params,
    )


def main():
    # Prior E2: N=32, t=0.60, delta=0.20 >> delta_SP, edge seed. Forming sheet.
    N = 32
    L = 1.0
    T_END = 0.60
    DELTA = 0.20
    EDGE = 0.05
    D_I = 0.05
    T_E = 0.01
    B0 = 1.0
    N_BG = 0.25
    N1 = 0.75
    NU = 1e-3
    ETA = 1e-3
    CFL = 0.4

    print(
        f"E2c Harris n = n_bg + n1 sech^2((y-L/2)/delta)  "
        f"n_bg={N_BG} n1={N1} delta={DELTA} (NO floor)",
        flush=True,
    )
    print(f"E2c Te knob T_e={T_E} (NOT 0; Te=0 would make twofluid==hall at uniform n)", flush=True)
    print(
        f"Harris IC: harris=True harris_n=True harris_width={DELTA} harris_edge={EDGE} "
        f"b_guide=x B0={B0} (same forming sheet as test_harris_meter)",
        flush=True,
    )

    mp_base = dict(
        B0=B0, b_guide="x", harris=True, harris_width=DELTA,
        harris_edge=EDGE, harris_n=True, n_bg=N_BG, harris_n1=N1,
        eta_mag=ETA, eta_hyper=0.0, hyper_kcut=0.0,
        glm_ch=0.0, freeze_ext=0.0, d_i=D_I, T_e=0.0,
    )

    grid = make_grid(N, L=L, dim=2)
    L_grid = float(grid["L"])
    n_real = np.asarray(generate_harris_n(grid, n_bg=N_BG, n1=N1, width=DELTA))
    n_min = float(n_real.min())
    n_max = float(n_real.max())
    n_mean = float(n_real.mean())
    print(
        f"n on grid: min={n_min:.6e} max={n_max:.6e} mean={n_mean:.6e} "
        f"(min n > 0; no floor applied)",
        flush=True,
    )
    if n_min <= 0.0:
        raise SystemExit("E2c abort: min n <= 0; would need a floor (forbidden)")

    B_hat, B_ext_hat, _ = split_guide_fields(grid, mp_base)
    B = np.fft.ifftn(np.asarray(B_hat) + np.asarray(B_ext_hat), axes=(1, 2)).real
    u0 = np.zeros((2, N, N), dtype=float)
    # CFL helper assumes n=1; Hall ~ d_i/n and lobe v_A = B0/sqrt(n_bg).
    # Pass d_i/n_bg so the Hall CFL uses the lobe 1/n (does not rewrite mhd RHS).
    dt = float(cfl_dt_mhd(
        u0, B, float(grid["dx"]), NU, ETA, cfl=CFL, d_i=D_I / max(N_BG, 1e-30)))
    diag_every = max(1, int(np.ceil(T_END / dt)) // 10)
    steps = diag_every * 10
    print(
        f"N={N} L={L_grid} dx={float(grid['dx']):.6e} dt={dt:.6e} "
        f"steps={steps} t_end={steps * dt:.4f} diag_every={diag_every}",
        flush=True,
    )
    print(
        "Phi definition: mill flux_x_half = mean(Btot[0][:, :N//2]) = <Bx>_{y<L/2}; "
        "Phi = flux_x_half * (L/2); rec_rate_flux = -d<Bx>/dt; "
        "rate_norm = rec_rate_flux * (L/2) / (v_A B0)",
        flush=True,
    )

    # v_A from Harris lobe / background density, not mean n and not invented 0.1.
    v_A = B0 / np.sqrt(N_BG)
    print(
        f"v_A definition: v_A = B0/sqrt(n_bg) = {v_A:.6e}  "
        f"(Harris lobe/background density n_bg={N_BG}; "
        f"NOT B0/sqrt(mean n)={B0/np.sqrt(n_mean):.6e}; NOT 0.1)",
        flush=True,
    )
    print(
        f"B0={B0}  n_bg={N_BG}  n1={N1}  v_A={v_A:.6e}  L={L_grid}  "
        f"delta={DELTA}  d_i={D_I}  T_e={T_E}",
        flush=True,
    )

    mp_hall = dict(mp_base)
    mp_tf = dict(mp_base, T_e=T_E)

    print("RUN mode=hall d_i=%.4f harris_n=True (frozen spatial n in Ohm)" % D_I, flush=True)
    out_h = _run_one("hall", mp_hall, N, steps, dt, diag_every, NU)
    print("RUN mode=twofluid d_i=%.4f T_e=%.4f harris_n=True (n_i=n_e IC)" % (D_I, T_E), flush=True)
    out_t = _run_one("twofluid", mp_tf, N, steps, dt, diag_every, NU)

    if "mean_n_i" in out_t:
        n_hist = _arr(out_t["mean_n_i"])
        min_hist = _arr(out_t["min_n_i"]) if "min_n_i" in out_t else n_hist
        if n_hist.size:
            print(
                f"twofluid mean n_i[0]={float(n_hist[0]):.6e} mean n_i[-1]={float(n_hist[-1]):.6e} "
                f"min n_i[0]={float(min_hist[0]):.6e} min n_i[-1]={float(min_hist[-1]):.6e} "
                f"(no floor)",
                flush=True,
            )

    t_h = _arr(out_h["time"])
    phi_h = _phi_from_mean_bx(out_h["flux_x_half"], L_grid)
    rec_h = _arr(out_h["rec_rate_flux"])
    rn_h = _rate_norm(rec_h, L_grid, v_A, B0)
    j_h = _arr(out_h["max_j"])

    t_t = _arr(out_t["time"])
    phi_t = _phi_from_mean_bx(out_t["flux_x_half"], L_grid)
    rec_t = _arr(out_t["rec_rate_flux"])
    rn_t = _rate_norm(rec_t, L_grid, v_A, B0)
    j_t = _arr(out_t["max_j"])

    _print_table("hall", t_h, phi_h, rec_h, rn_h, j_h)
    _print_table("twofluid", t_t, phi_t, rec_t, rn_t, j_t)

    peak_h = float(np.max(rn_h))
    peak_t = float(np.max(rn_t))
    min_h = float(np.min(rn_h))
    min_t = float(np.min(rn_t))
    abspeak_h = float(np.max(np.abs(rn_h)))
    abspeak_t = float(np.max(np.abs(rn_t)))
    sc_h, drop_h, p0_h, p1_h = _phi_transfers(phi_h)
    sc_t, drop_t, p0_t, p1_t = _phi_transfers(phi_t)
    dphi = float(np.max(np.abs(phi_h - phi_t)))
    drec = float(np.max(np.abs(rec_h - rec_t)))
    drn = float(np.max(np.abs(rn_h - rn_t)))
    dj = float(np.max(np.abs(j_h - j_t)))
    print(
        f"max|hall-twofluid| Phi={dphi:.3e} rec_rate_flux={drec:.3e} "
        f"rate_norm={drn:.3e} max|J|={dj:.3e} "
        "(Harris n => grad p_e = Te grad n != 0 on twofluid)",
        flush=True,
    )

    print("=== E2c comparison (Harris n sech2 peel; not Sweet-Parker; not universal 0.1) ===", flush=True)
    print(
        f"{'mode':<10} {'peak_rate_norm':>16} {'min_rate_norm':>16} {'max|rate_norm|':>16} "
        f"{'Phi0':>14} {'Phi_end':>14} {'sign_change':>12} {'|Phi| dropped':>14}",
        flush=True,
    )
    print(
        f"{'hall':<10} {peak_h:16.6e} {min_h:16.6e} {abspeak_h:16.6e} "
        f"{p0_h:14.6e} {p1_h:14.6e} {str(sc_h):>12} {str(drop_h):>14}",
        flush=True,
    )
    print(
        f"{'twofluid':<10} {peak_t:16.6e} {min_t:16.6e} {abspeak_t:16.6e} "
        f"{p0_t:14.6e} {p1_t:14.6e} {str(sc_t):>12} {str(drop_t):>14}",
        flush=True,
    )
    print(
        "HAVE E2c Harris n sech2 peel "
        f"(hall vs twofluid; Te={T_E}>0; no floor).",
        flush=True,
    )


if __name__ == "__main__":
    main()

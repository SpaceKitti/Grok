"""E2 mill: forming Harris sheet, hall vs twofluid (Te>0). Not Crow, not SP.

Same thick Harris + edge seed as examples/test_harris_meter.py.
flux_x_half in the mill is mean <Bx> on y<L/2 (mhd.py _mhd_diag_2d).
rec_rate_flux is -d<Bx>/dt (diagnostics.millennium_series).
Phi = <Bx>_{y<L/2} * (L/2); rate_norm = -dPhi/dt / (v_A B0)
     = rec_rate_flux * (L/2) / (v_A B0).
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import make_grid, run_framework, split_guide_fields, cfl_dt_mhd


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
    N_DENSITY = 1.0
    NU = 1e-3
    ETA = 1e-3
    CFL = 0.4

    print(f"E2 Te knob T_e={T_E} (NOT 0; Te=0 would make twofluid==hall)", flush=True)
    print(
        f"Harris IC: harris=True harris_width={DELTA} harris_edge={EDGE} "
        f"b_guide=x B0={B0} (same forming sheet as test_harris_meter)",
        flush=True,
    )

    mp_base = dict(
        B0=B0, b_guide="x", harris=True, harris_width=DELTA,
        harris_edge=EDGE, eta_mag=ETA, eta_hyper=0.0, hyper_kcut=0.0,
        glm_ch=0.0, freeze_ext=0.0, d_i=D_I, n_hall=N_DENSITY, n=N_DENSITY,
    )

    grid = make_grid(N, L=L, dim=2)
    L_grid = float(grid["L"])
    B_hat, B_ext_hat, _ = split_guide_fields(grid, mp_base)
    B = np.fft.ifftn(np.asarray(B_hat) + np.asarray(B_ext_hat), axes=(1, 2)).real
    u0 = np.zeros((2, N, N), dtype=float)
    dt = float(cfl_dt_mhd(u0, B, float(grid["dx"]), NU, ETA, cfl=CFL, d_i=D_I))
    # Exact chunks so rec_rate_flux is not a one-sided spike on a remainder dt.
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

    mp_hall = dict(mp_base)
    mp_tf = dict(mp_base, T_e=T_E)

    print("RUN mode=hall d_i=%.4f" % D_I, flush=True)
    out_h = _run_one("hall", mp_hall, N, steps, dt, diag_every, NU)
    print("RUN mode=twofluid d_i=%.4f T_e=%.4f" % (D_I, T_E), flush=True)
    out_t = _run_one("twofluid", mp_tf, N, steps, dt, diag_every, NU)

    n_h = N_DENSITY
    n_t = N_DENSITY
    if "mean_n_i" in out_t:
        n_hist = _arr(out_t["mean_n_i"])
        if n_hist.size:
            n_t = float(n_hist[0])
            print(
                f"twofluid mean n_i[0]={n_t:.6e} mean n_i[-1]={float(n_hist[-1]):.6e} "
                f"(n=1 default unless mean n is not 1)",
                flush=True,
            )
    vA_h = B0 / np.sqrt(n_h)
    vA_t = B0 / np.sqrt(n_t if n_t > 0.0 else 1.0)
    print(
        f"B0={B0} (Harris amplitude)  n_hall={n_h} v_A_hall={vA_h:.6e}  "
        f"n_twofluid={n_t} v_A_twofluid={vA_t:.6e}  L={L_grid}  delta={DELTA}  "
        f"d_i={D_I}  T_e={T_E}",
        flush=True,
    )

    t_h = _arr(out_h["time"])
    phi_h = _phi_from_mean_bx(out_h["flux_x_half"], L_grid)
    rec_h = _arr(out_h["rec_rate_flux"])
    rn_h = _rate_norm(rec_h, L_grid, vA_h, B0)
    j_h = _arr(out_h["max_j"])

    t_t = _arr(out_t["time"])
    phi_t = _phi_from_mean_bx(out_t["flux_x_half"], L_grid)
    rec_t = _arr(out_t["rec_rate_flux"])
    rn_t = _rate_norm(rec_t, L_grid, vA_t, B0)
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
        "(uniform n=1 => grad p_e = Te grad n ~ 0 on this IC)",
        flush=True,
    )

    print("=== E2 comparison (forming Harris; not Sweet-Parker; not universal 0.1) ===", flush=True)
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
        "HAVE E2 hall vs twofluid reconnection "
        f"(thick Harris; Te={T_E}>0; rate_norm=-dPhi/(vA B0)).",
        flush=True,
    )


if __name__ == "__main__":
    main()

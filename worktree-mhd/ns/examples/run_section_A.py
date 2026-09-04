"""Section A study: 3D textbook-B OT regularity / current sheets (A1-A4).

Orion short-list #1. Not a smoke.

Re-run from:
  cd C:\\Users\\Akitt\\Grok\\worktree-mhd\\ns
  python .\\examples\\run_section_A.py

Default (no flags) = original HAVE matrix:
  N=32, t_end=1.5, sample 0.1, nu_fac=4
  1) mhd default  2) mhd default/4
  3) hall d_i=0.05 default  4) hall d_i=0.2 default
  writes examples/section_A_out.txt

Crank matrix:
  python .\\examples\\run_section_A.py --crank
  python .\\examples\\run_section_A.py --crank --N 32 --t-end 2 --nu-fac 8 --d-i 0.2
  Tries N=64; drops ALL runs to N=32 on OOM or if hall will not finish overnight.
  t_end=2.0, sample 0.1, nu_fac=8
  1) mhd default nu,eta (1e-3 / 1e-3)
  2) mhd default/8 (1.25e-4)
  3) hall d_i=0.2 default nu,eta
  4) hall d_i=0.2 default/8  (skip if run 2 or 3 NaN)
  writes examples/section_A_crank_out.txt

CLI: --N, --t-end, --nu-fac, --d-i (one or more), --out, --crank

Venus mill language:
  Finite max|omega|, max|J| on one run = this solution stayed smooth,
  NOT an A1 / Clay theorem claim.
  Peel = |J| climbs (or stays high) while |omega| does not follow.
  I_BKM finite on the table is yes/no only.
  If E(k_max)/E_tot >= 1e-2, flag aliasing; do not retune hyper_kcut.
  Next after aliasing on /8 is N up, not hyper_kcut.

Seed (A2c HAVE, do not replace with u=B):
  u = U0 (-sin y, sin x, 0.2 cos z)
  B = B0 (-sin y, sin 2x, 0.2 cos z)
  Qin-project B. N must be >= 16 (N=8 drops the 2x harmonic).
"""
import argparse
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import (
    run_framework, generate_u_ot, generate_b0, make_grid,
    DEFAULT_MHD, cfl_dt_mhd,
)

T_END = 1.5
DT_SAMPLE = 0.1
CFL = 0.4
U0 = 1.0
B0 = 1.0
# Hive MHD OT: eta_mag from DEFAULT_MHD; nu matches A2c OT / Pr_m=1.
# driver dim=3 hydro default nu=5e-4 is not used here.
NU_DEF = 1.0e-3
ETA_DEF = float(DEFAULT_MHD["eta_mag"])
ALIAS_FLAG = 1.0e-2
DIVB_LIMIT = 1.0e-12
PREFERRED_N = 32
FALLBACK_N = 16
# Wall-time policy (CPU, TrinityOrb calibration from HAVE Section A N=32).
SEC_PER_STEP_N32 = 0.44
OVERNIGHT_S = 8.0 * 3600.0
RUN_TIMEOUT_S = 3.0 * 3600.0
# Previous N=32 t=1.5 |J| peaks (HAVE Section A) for crank verdict (2).
PREV_N32_T15 = {
    "mhd_default": (95.21, 0.3),
    "mhd_div4": (104.02, 0.3),  # not /8; last study had no /8
    "hall_di02": (53.16, 0.3),
}


def _arr(x):
    return np.asarray(x, dtype=float)


def log(msg, fh=None):
    line = str(msg)
    print(line, flush=True)
    if fh is not None:
        fh.write(line + "\n")
        fh.flush()


def running_trapz(y, t):
    """Running trapezoidal integral; out[0]=0, out[i]=int_0^{t_i} y dt."""
    y = _arr(y)
    t = _arr(t)
    out = np.zeros_like(y)
    if y.size > 1:
        pieces = 0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])
        out[1:] = np.cumsum(pieces)
    return out


def peel_decision(t, w, j):
    """Say peel from the table only. Same rule as A2c. Do not invent."""
    t, w, j = _arr(t), _arr(w), _arr(j)
    rel = np.max(np.abs(j - w) / (np.maximum(w, j) + 1e-30))
    wmax, jmax = float(np.max(w)), float(np.max(j))
    tw, tj = float(t[int(np.argmax(w))]), float(t[int(np.argmax(j))])
    j_over_w = jmax / (wmax + 1e-30)
    w_bounded = w[-1] <= 1.2 * wmax
    j_run = jmax > 1.15 * wmax and jmax > 1.15 * j[0]
    cols_same = rel < 0.02
    if cols_same:
        peel = False
        why = (
            f"columns nearly identical (max rel |J-omega|={rel:.3f}); "
            "no peel on this window"
        )
    elif j_run and w_bounded:
        peel = True
        why = (
            f"columns not identical (max rel |J-omega|={rel:.3f}); "
            f"|J| runs (peak {jmax:.4e} at t={tj:.4f}) at bounded |omega| "
            f"(peak {wmax:.4e} at t={tw:.4f}, end/peak={w[-1]/(wmax+1e-30):.3f})"
        )
    else:
        peel = False
        why = (
            f"columns differ (max rel |J-omega|={rel:.3f}, "
            f"|J|_peak/|omega|_peak={j_over_w:.3f}) "
            "but |J| does not run away at bounded |omega| on this window"
        )
    return peel, why


def choose_dt(u, B, dx, nu, eta, d_i, cfl=CFL):
    """Hive cfl_dt_mhd, snapped so diag rows land on dt_sample=0.1.

    Existing Hall CFL (mhd.cfl_dt_mhd):
      hall = pi^2 |d_i| max|B| / dx
            = pi * (d_i * k_Nyquist * max|B|)
      k_Nyquist = pi/dx
      dt = cfl * dx / (max|u| + max|B| + 4(nu+eta)/dx + hall)
    Job v_hall = d_i * k_max * max|B| with k_max = k_Nyquist.
    Hive is stricter by a factor of pi (does not explode on d_i=0.2).
    We use the hive formula (adaptive in d_i, max|B| at t=0) and only
    snap dt down so 0.1 / dt is an integer.
    """
    dt_cfl = float(cfl_dt_mhd(u, B, dx, nu, eta, cfl=cfl, d_i=d_i))
    n = max(1, int(np.ceil(DT_SAMPLE / dt_cfl)))
    dt = DT_SAMPLE / n
    umax = float(np.max(np.sqrt(np.sum(np.asarray(u) ** 2, axis=0))))
    bmax = float(np.max(np.sqrt(np.sum(np.asarray(B) ** 2, axis=0))))
    k_nyq = float(np.pi / (dx + 1e-30))
    v_hall = abs(float(d_i)) * k_nyq * bmax
    v_job = umax + bmax + v_hall
    dt_job = cfl * dx / (v_job + 4.0 * (nu + eta) / dx + 1e-12)
    return dt, n, dt_cfl, dt_job, umax, bmax, k_nyq, v_hall


def estimate_dt_steps(N, t_end, nu, eta, d_i, cfl=CFL,
                      umax=1.414213562, bmax=1.414213562):
    """Cheap CFL estimate without allocating fields (hive formula)."""
    dx = 1.0 / float(N)
    hall = (np.pi ** 2) * abs(float(d_i)) * bmax / dx
    dt_cfl = cfl * dx / (umax + bmax + 4.0 * (nu + eta) / dx + hall + 1e-12)
    n = max(1, int(np.ceil(DT_SAMPLE / dt_cfl)))
    dt = DT_SAMPLE / n
    steps = int(round(float(t_end) / dt))
    return dt, steps, dt_cfl


def estimate_wall_s(N, t_end, nu, eta, d_i):
    dt, steps, dt_cfl = estimate_dt_steps(N, t_end, nu, eta, d_i)
    scale = (float(N) / 32.0) ** 3 * (np.log(max(float(N), 2.0)) / np.log(32.0))
    return steps * SEC_PER_STEP_N32 * scale, dt, steps, dt_cfl


def seed_and_divb(N, fh=None):
    g = make_grid(N, L=1.0, dim=3)
    L = float(g["L"])
    u = np.asarray(generate_u_ot(g, U0=U0))
    Bhat = generate_b0(g, B0=B0, kind="ot")
    B = np.asarray(jax.numpy.fft.ifftn(Bhat, axes=(1, 2, 3)).real)
    x = np.linspace(0.0, L, N, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    xx = 2.0 * np.pi * X / L
    yy = 2.0 * np.pi * Y / L
    zz = 2.0 * np.pi * Z / L
    u_raw = np.stack([-np.sin(yy), np.sin(xx), 0.2 * np.cos(zz)])
    B_raw = np.stack([-np.sin(yy), np.sin(2.0 * xx), 0.2 * np.cos(zz)])
    B_match = np.stack([-np.sin(yy), np.sin(xx), 0.2 * np.cos(zz)])
    corr_by_2x = float(np.corrcoef(B[1].ravel(), B_raw[1].ravel())[0, 1])
    corr_by_x = float(np.corrcoef(B[1].ravel(), B_match[1].ravel())[0, 1])
    corr_uy_x = float(np.corrcoef(u[1].ravel(), u_raw[1].ravel())[0, 1])
    corr_uy_by = float(np.corrcoef(u[1].ravel(), B[1].ravel())[0, 1])
    k_stack = np.asarray(g["k_stack"])
    divB = float(np.max(np.abs(
        np.fft.ifftn(1j * np.sum(k_stack * np.asarray(Bhat), axis=0)).real
    )))
    log(
        f"SEED N={N}  corr(By, sin 2x)={corr_by_2x:.4f}  "
        f"corr(By, sin x)={corr_by_x:.4f}  corr(uy, sin x)={corr_uy_x:.4f}  "
        f"corr(uy, By)={corr_uy_by:.4f}  max|div B|={divB:.3e}  "
        f"(immediately after Qin)",
        fh,
    )
    ok_seed = (
        corr_by_2x > 0.95
        and corr_by_x < 0.5
        and corr_uy_x > 0.95
        and abs(corr_uy_by) < 0.5
    )
    if not ok_seed:
        log("FAILED 3D textbook-B seed (By=sin 2x, u not a copy of B)", fh)
        return None
    if divB >= DIVB_LIMIT:
        log(
            f"STOP: max|div B|={divB:.3e} >= {DIVB_LIMIT:.0e} after Qin. "
            "Fix projection before marching.",
            fh,
        )
        return None
    log(
        f"PASS Qin max|div B|={divB:.3e} < {DIVB_LIMIT:.0e}; "
        "textbook-B seed OK (not u=B)",
        fh,
    )
    return dict(grid=g, u=u, B=B, divB0=divB)


def print_table(t, w, j, ibkm, ek, divb, fh=None):
    hdr = (
        f"{'t':>8} {'max|w|':>14} {'max|J|':>14} {'|J|/|w|':>12} "
        f"{'I_BKM':>14} {'E(kmax)/Etot':>14} {'max|divB|':>12}"
    )
    log(hdr, fh)
    for i in range(t.size):
        r = j[i] / (w[i] + 1e-30)
        log(
            f"{t[i]:8.4f} {w[i]:14.6e} {j[i]:14.6e} {r:12.6f} "
            f"{ibkm[i]:14.6e} {ek[i]:14.6e} {divb[i]:12.3e}",
            fh,
        )


def one_run(N, mode, nu, eta, d_i, ic_fields, fh=None, t_end=None, dt_scale=1.0):
    if t_end is None:
        t_end = T_END
    u, B = ic_fields["u"], ic_fields["B"]
    dx = float(ic_fields["grid"]["dx"])
    dt, n_per, dt_cfl, dt_job, umax, bmax, k_nyq, v_hall = choose_dt(
        u, B, dx, nu, eta, d_i
    )
    dt_scale = float(dt_scale) if float(dt_scale) > 0 else 1.0
    dt_base = dt
    dt = dt_base / dt_scale
    n_per = max(1, int(round(DT_SAMPLE / dt)))
    steps = int(round(t_end / dt))
    diag_every = n_per
    log(
        f"RUN mode={mode} N={N} t_end={t_end} nu={nu:.3e} eta={eta:.3e} "
        f"d_i={d_i} force_off scheme=rk2 ic=ot dt_scale={dt_scale:g}",
        fh,
    )
    log(
        f"  Hall CFL: hive dt_cfl={dt_cfl:.6e}  job-style "
        f"dt(v_hall=d_i*k_nyq*max|B|)={dt_job:.6e}  snapped dt={dt_base:.6e} "
        f"used dt={dt:.6e} (= snapped/dt_scale; sample 0.1). "
        f"k_nyq={k_nyq:.4f} max|u|={umax:.4f} max|B|={bmax:.4f} "
        f"v_hall={v_hall:.4f} steps={steps} diag_every={diag_every}",
        fh,
    )
    t0 = time.perf_counter()
    try:
        out = run_framework(
            N=N, dim=3, steps=steps, dt=dt, diag_every=diag_every,
            scheme="rk2", mode=mode, ic="ot", force_on=False,
            viscoelastic=False, nu=nu,
            mhd_params=dict(
                B0=B0, ot_u0=U0, eta_mag=eta, eta_hyper=0.0,
                glm_ch=0.0, d_i=float(d_i), n_hall=1.0,
            ),
        )
    except MemoryError as e:
        log(f"OOM during run_framework: {e}", fh)
        return dict(oom=True, nan=True)
    elapsed = time.perf_counter() - t0
    if elapsed > RUN_TIMEOUT_S:
        log(
            f"  WALL CLOCK {elapsed:.1f}s exceeded ~3h budget "
            f"(finished anyway; report last good t).",
            fh,
        )
    t = _arr(out["time"])
    w = _arr(out["max_vort"])
    j = _arr(out["max_j"])
    divb = _arr(out["max_div_b"])
    ek = _arr(out.get("ekmax_frac", np.zeros_like(t)))
    finite = np.isfinite(w) & np.isfinite(j)
    nan = not bool(np.all(finite))
    if nan:
        good = np.where(finite)[0]
        last_good_t = float(t[good[-1]]) if good.size else float("nan")
        log(
            f"  NaN detected. last good t={last_good_t:.4f}  "
            f"n_finite={int(good.size)}/{t.size}  elapsed={elapsed:.1f}s",
            fh,
        )
        if good.size:
            sl = good
            t, w, j, divb, ek = t[sl], w[sl], j[sl], divb[sl], ek[sl]
        else:
            return dict(
                nan=True, oom=False, t=t, w=w, j=j, elapsed=elapsed,
                dt=dt, last_good_t=last_good_t,
            )
    else:
        last_good_t = float(t[-1])
        log(
            f"  finished t={last_good_t:.4f} elapsed={elapsed:.1f}s  "
            f"NaN=no  rows={t.size}",
            fh,
        )
    ibkm = running_trapz(w + j, t)
    print_table(t, w, j, ibkm, ek, divb, fh)
    peel, why = peel_decision(t, w, j)
    alias = bool(np.any(ek >= ALIAS_FLAG))
    ek_max = float(np.max(ek)) if ek.size else float("nan")
    r = j / (w + 1e-30)
    log(f"  PEEL={'yes' if peel else 'no'}: {why}", fh)
    log(
        f"  r=|J|/|omega|  start={float(r[0]):.4f}  end={float(r[-1]):.4f}  "
        f"peak={float(np.max(r)):.4f} at t={float(t[int(np.argmax(r))]):.4f}",
        fh,
    )
    log(
        f"  I_BKM method=trapezoid on dt_sample={DT_SAMPLE} rows; "
        f"I_BKM(t_end)={float(ibkm[-1]):.6e}  finite={bool(np.isfinite(ibkm[-1]))}",
        fh,
    )
    log(
        f"  E(k_max)/E_tot def: outermost dealiased shell "
        f"(k >= k_max_dealias - 2pi/L) of 0.5 N^{{-6}} sum(|u_hat|^2+|B_hat|^2) "
        f"over total spectral kin+mag. max={ek_max:.3e}  "
        f"ALIASING={'FLAG E(k_max)/E_tot >= 1e-2 (N may be too small; not retuning hyper_kcut)' if alias else 'no flag'}",
        fh,
    )
    log(
        f"  max|div B| t=0 (history)={float(divb[0]):.3e}  "
        f"t_end={float(divb[-1]):.3e}  pre-march Qin={ic_fields['divB0']:.3e}",
        fh,
    )
    w_all_fin = bool(np.all(np.isfinite(w)))
    j_all_fin = bool(np.all(np.isfinite(j)))
    smooth = w_all_fin and j_all_fin and (not nan)
    if smooth:
        log(
            "  this solution stayed smooth on this run "
            "(finite max|omega|, max|J|; NOT an A1 theorem claim).",
            fh,
        )
    else:
        log("  max|omega| or max|J| not finite on the whole window.", fh)
    return dict(
        nan=nan, oom=False, t=t, w=w, j=j, ibkm=ibkm, ek=ek, divb=divb,
        peel=peel, why=why, alias=alias, ek_max=ek_max,
        last_good_t=last_good_t, dt=dt, dt_cfl=dt_cfl, elapsed=elapsed,
        nu=nu, eta=eta, d_i=d_i, mode=mode, N=N, t_end=t_end,
        ibkm_end=float(ibkm[-1]) if ibkm.size else float("nan"),
        r_start=float(r[0]), r_end=float(r[-1]), r_peak=float(np.max(r)),
        w_end=float(w[-1]), j_end=float(j[-1]),
        w_max=float(np.max(w)), j_max=float(np.max(j)),
        tw_max=float(t[int(np.argmax(w))]), tj_max=float(t[int(np.argmax(j))]),
        divb0=float(divb[0]),
        finite_ibkm=bool(np.isfinite(ibkm[-1])) if ibkm.size else False,
        smooth=smooth,
    )


def peak_window(t, y, tmax=1.5):
    t, y = _arr(t), _arr(y)
    m = t <= tmax + 1e-12
    if not np.any(m):
        return float("nan"), float("nan")
    i = int(np.argmax(y[m]))
    return float(y[m][i]), float(t[m][i])


def compare_peel(a, b):
    """stronger / weaker / same from peel flag + peak r and |J| run."""
    if a is None or b is None:
        return "n/a"
    if a.get("nan") and not b.get("nan"):
        return "n/a (run a NaN)"
    if b.get("nan") and not a.get("nan"):
        return "n/a (run b NaN)"
    if a.get("nan") and b.get("nan"):
        return "n/a (both NaN)"
    pa, pb = bool(a["peel"]), bool(b["peel"])
    if pa and not pb:
        return "weaker (peel on default, not on this run)"
    if pb and not pa:
        return "stronger (peel appears when damping dropped / Hall on)"
    ra, rb = float(a["r_peak"]), float(b["r_peak"])
    ja, jb = float(a["j_max"]), float(b["j_max"])
    if (not pa) and (not pb):
        return "same (no peel on either window)"
    # both peel: compare peak r
    if rb > 1.1 * ra or jb > 1.1 * ja:
        return "stronger"
    if rb < ra / 1.1 and jb < ja / 1.1:
        return "weaker"
    return "same"


def parse_args():
    p = argparse.ArgumentParser(
        description="Section A 3D textbook-B OT study (HAVE + crank)."
    )
    p.add_argument(
        "--crank", action="store_true",
        help="CRANK matrix: t_end=2, nu_fac=8, hall d_i=0.2 at both dampings; "
             "try N=64 then drop to 32 if OOM/overnight.",
    )
    p.add_argument("--N", dest="N", type=int, default=None,
                   help="Grid N (crank default 64-try; HAVE default 32).")
    p.add_argument("--t-end", dest="t_end", type=float, default=None,
                   help="Integration time (crank default 2.0; HAVE default 1.5).")
    p.add_argument("--nu-fac", dest="nu_fac", type=float, default=None,
                   help="Divide default nu,eta by this for the small-damping run "
                        "(crank default 8; HAVE default 4).")
    p.add_argument(
        "--d-i", dest="d_i", type=float, nargs="+", default=None,
        help="Hall d_i values. HAVE default: 0.05 0.2 (both at default nu). "
             "Crank default: 0.2 (used at default AND /nu_fac).",
    )
    p.add_argument("--out", dest="out", type=str, default=None,
                   help="Output txt path. Default: section_A_out.txt or "
                        "section_A_crank_out.txt with --crank.")
    p.add_argument(
        "--dt-scale", dest="dt_scale", type=float, default=1.0,
        help="Divide the snapped CFL dt by this (default 1). "
             "dt_used = dt / dt_scale. Larger = smaller steps.",
    )
    return p.parse_args()


def build_runs(crank, nu_fac, d_i_list, nu_def, eta_def):
    """Return ordered run dicts. Crank: hall at same d_i, two dampings."""
    if crank:
        di = float(d_i_list[0]) if d_i_list else 0.2
        return [
            dict(key="1", mode="mhd", nu=nu_def, eta=eta_def, d_i=0.0,
                 label="mhd default"),
            dict(key="2", mode="mhd", nu=nu_def / nu_fac, eta=eta_def / nu_fac,
                 d_i=0.0, label=f"mhd default/{nu_fac:g}"),
            dict(key="3", mode="hall", nu=nu_def, eta=eta_def, d_i=di,
                 label=f"hall d_i={di:g} default"),
            dict(key="4", mode="hall", nu=nu_def / nu_fac, eta=eta_def / nu_fac,
                 d_i=di, label=f"hall d_i={di:g} default/{nu_fac:g}"),
        ]
    di_list = d_i_list if d_i_list else [0.05, 0.2]
    runs = [
        dict(key="1", mode="mhd", nu=nu_def, eta=eta_def, d_i=0.0,
             label="mhd default"),
        dict(key="2", mode="mhd", nu=nu_def / nu_fac, eta=eta_def / nu_fac,
             d_i=0.0, label=f"mhd default/{nu_fac:g}"),
    ]
    for i, di in enumerate(di_list):
        runs.append(dict(
            key=str(3 + i), mode="hall", nu=nu_def, eta=eta_def, d_i=float(di),
            label=f"hall d_i={di:g} default",
        ))
    return runs


def choose_crank_N(prefer_N, t_end, nu_fac, d_i_hall, fh):
    """Try N=64; drop ALL to 32 if OOM-risk or hall won't finish overnight."""
    reason = "preferred"
    N = int(prefer_N)
    est_rows = []
    specs = [
        ("mhd default", NU_DEF, ETA_DEF, 0.0),
        (f"mhd /{nu_fac:g}", NU_DEF / nu_fac, ETA_DEF / nu_fac, 0.0),
        (f"hall d_i={d_i_hall:g} default", NU_DEF, ETA_DEF, d_i_hall),
        (f"hall d_i={d_i_hall:g} /{nu_fac:g}", NU_DEF / nu_fac, ETA_DEF / nu_fac,
         d_i_hall),
    ]
    for label, nu, eta, di in specs:
        wall, dt, steps, dt_cfl = estimate_wall_s(N, t_end, nu, eta, di)
        est_rows.append((label, wall, dt, steps, dt_cfl))
        log(
            f"EST N={N} {label}: dt~{dt:.3e} steps={steps} "
            f"wall~{wall/3600.0:.2f}h (N=32 calib {SEC_PER_STEP_N32}s/step "
            f"* N^3 logN)",
            fh,
        )
    hall_walls = [r[1] for r in est_rows if r[0].startswith("hall")]
    total = sum(r[1] for r in est_rows)
    log(
        f"EST N={N} total matrix ~{total/3600.0:.2f}h  "
        f"max hall ~{(max(hall_walls) if hall_walls else 0)/3600.0:.2f}h",
        fh,
    )
    drop = False
    if hall_walls and max(hall_walls) > OVERNIGHT_S:
        drop = True
        reason = (
            f"hall d_i={d_i_hall:g} N={N} t_end={t_end} estimated "
            f"{max(hall_walls)/3600.0:.1f}h; will not finish overnight"
        )
    elif total > 1.5 * OVERNIGHT_S:
        drop = True
        reason = (
            f"full matrix N={N} estimated {total/3600.0:.1f}h; "
            "will not finish overnight"
        )
    if drop and N > 32:
        log(
            f"N={N} dropped for ALL runs -> N=32. Reason: {reason}. "
            "Prefer completing the matrix at N=32 t=2 over a partial N=64.",
            fh,
        )
        N = 32
        reason = "dropped to 32: " + reason
        for label, nu, eta, di in specs:
            wall, dt, steps, dt_cfl = estimate_wall_s(N, t_end, nu, eta, di)
            log(
                f"EST N={N} {label}: dt~{dt:.3e} steps={steps} "
                f"wall~{wall/3600.0:.2f}h",
                fh,
            )
    return N, reason


def crank_three_verdicts(results, N, n_reason, nu_fac, skipped4, fh):
    """Venus mill THREE verdicts only. Do not invent peel."""
    r1, r2 = results.get("1"), results.get("2")
    r3, r4 = results.get("3"), results.get("4")
    log("", fh)
    log("==== THREE VERDICTS (Venus mill) ====", fh)

    # (1) /8 — peel back, or omega still follows?
    if r2 is None or r2.get("oom"):
        v1 = "no /8 table (run 2 missing/OOM); no peel claim"
    elif r2.get("nan"):
        v1 = (
            f"run 2 NaN last good t={r2.get('last_good_t')}; "
            "no clean /8 peel claim"
        )
    else:
        peel8 = bool(r2.get("peel"))
        peel1 = bool(r1.get("peel")) if r1 and not r1.get("nan") else None
        if peel8:
            v1 = (
                f"peel on /{nu_fac:g} — |J| runs while |omega| does not follow. "
                f"{r2.get('why')}"
            )
        else:
            follow = (
                "omega still follows |J| on this window "
                f"(PEEL=no). {r2.get('why')}"
            )
            if peel1 is True:
                v1 = (
                    f"peel back at /{nu_fac:g} vs default: default peeled, "
                    f"/{nu_fac:g} did not — {follow}"
                )
            elif peel1 is False:
                v1 = (
                    f"no peel on default or /{nu_fac:g} — {follow}"
                )
            else:
                v1 = follow
        v1 += (
            f"  |J|_peak={r2.get('j_max'):.4f} @{r2.get('tj_max')}  "
            f"|omega|_peak={r2.get('w_max'):.4f} @{r2.get('tw_max')}  "
            f"r_peak={r2.get('r_peak'):.4f}"
        )
    log(f"(1) /{nu_fac:g} — peel back, or omega still follows? {v1}", fh)

    # (2) peak |J| at 64 vs 32
    def jline(rr, tag):
        if rr is None or rr.get("oom"):
            return f"{tag}: missing"
        j15, t15 = peak_window(rr["t"], rr["j"], 1.5)
        jall, tall = rr.get("j_max"), rr.get("tj_max")
        return (
            f"{tag} N={rr.get('N')} |J|_peak={jall:.2f} @{tall}  "
            f"t<=1.5 |J|_peak={j15:.2f} @{t15}  NaN={rr.get('nan')}"
        )

    prev = (
        f"previous N=32 t=1.5: mhd default |J| peak {PREV_N32_T15['mhd_default'][0]} "
        f"@{PREV_N32_T15['mhd_default'][1]}; /4 was {PREV_N32_T15['mhd_div4'][0]} "
        f"(not /8); hall d_i=0.2 |J| peak {PREV_N32_T15['hall_di02'][0]} "
        f"@{PREV_N32_T15['hall_di02'][1]}"
    )
    if N == 64 and r1 and not r1.get("oom"):
        jump_notes = []
        for rr, prev_j, name in [
            (r1, PREV_N32_T15["mhd_default"][0], "mhd default"),
            (r3, PREV_N32_T15["hall_di02"][0], "hall d_i=0.2 default"),
        ]:
            if rr is None or rr.get("oom") or rr.get("nan"):
                continue
            j15, t15 = peak_window(rr["t"], rr["j"], 1.5)
            if j15 > 1.3 * prev_j:
                jump_notes.append(
                    f"{name} t<=1.5 |J| {j15:.2f} vs prev N=32 {prev_j:.2f} "
                    "JUMPS — sheet was not resolved at 32"
                )
            else:
                jump_notes.append(
                    f"{name} t<=1.5 |J| {j15:.2f} vs prev N=32 {prev_j:.2f} "
                    "(no jump; not a newly unresolved sheet)"
                )
        v2 = (
            f"this crank ran N=64. {'; '.join(jump_notes) if jump_notes else 'no comparable peaks'}. "
            f"{jline(r1, 'run1')} | {jline(r2, 'run2')} | {jline(r3, 'run3')}"
            + (f" | {jline(r4, 'run4')}" if r4 else "")
            + f"  {prev}"
        )
    else:
        v2 = (
            f"N=64 not used for the matrix ({n_reason}). "
            "Cannot compare 64 vs 32 from this crank. "
            "This N=32 t<=1.5 |J| vs previous N=32 t=1.5: "
            f"{jline(r1, 'run1')} | {jline(r2, 'run2')} | {jline(r3, 'run3')}"
            + (f" | {jline(r4, 'run4')}" if r4 else "")
            + f"  {prev}"
        )
    log(f"(2) peak |J| at 64 vs 32 — if it jumps, the sheet wasn't resolved. {v2}", fh)

    # (3) hall d_i vs mhd at the SAME damping
    bits = []
    if r1 is None or r3 is None or r1.get("oom") or r3.get("oom"):
        bits.append("1 vs 3: n/a (missing/OOM)")
    elif r1.get("nan") or r3.get("nan"):
        bits.append(
            f"1 vs 3: no clean claim (NaN last_t mhd={r1.get('last_good_t')} "
            f"hall={r3.get('last_good_t')})"
        )
    else:
        chg = compare_peel(r1, r3)
        bits.append(
            f"1 vs 3 (default nu,eta): peel {chg}; "
            f"mhd |J|_peak={r1.get('j_max'):.2f} @{r1.get('tj_max')} "
            f"|omega|_peak={r1.get('w_max'):.2f} r_peak={r1.get('r_peak'):.4f}; "
            f"hall |J|_peak={r3.get('j_max'):.2f} @{r3.get('tj_max')} "
            f"|omega|_peak={r3.get('w_max'):.2f} r_peak={r3.get('r_peak'):.4f}"
        )
    if skipped4:
        bits.append("2 vs 4: skipped (run 2 or 3 NaN)")
    elif r4 is None:
        bits.append("2 vs 4: did not run")
    elif r2 is None or r2.get("oom") or r4.get("oom"):
        bits.append("2 vs 4: n/a (missing/OOM)")
    elif r2.get("nan") or r4.get("nan"):
        bits.append(
            f"2 vs 4: no clean claim (NaN last_t mhd={r2.get('last_good_t')} "
            f"hall={r4.get('last_good_t')})"
        )
    else:
        chg = compare_peel(r2, r4)
        bits.append(
            f"2 vs 4 (default/{nu_fac:g}): peel {chg}; "
            f"mhd |J|_peak={r2.get('j_max'):.2f} @{r2.get('tj_max')} "
            f"|omega|_peak={r2.get('w_max'):.2f} r_peak={r2.get('r_peak'):.4f}; "
            f"hall |J|_peak={r4.get('j_max'):.2f} @{r4.get('tj_max')} "
            f"|omega|_peak={r4.get('w_max'):.2f} r_peak={r4.get('r_peak'):.4f}"
        )
    v3 = "  ".join(bits)
    log(
        f"(3) hall d_i vs mhd at the SAME damping (1 vs 3, and 2 vs 4 if 4 ran). {v3}",
        fh,
    )
    log(
        "Finite max|omega|, max|J| on these runs is NOT an A1 / Clay theorem claim.",
        fh,
    )
    return v1, v2, v3


def main():
    global T_END
    args = parse_args()
    crank = bool(args.crank)
    t_end = float(args.t_end) if args.t_end is not None else (2.0 if crank else 1.5)
    T_END = t_end
    nu_fac = float(args.nu_fac) if args.nu_fac is not None else (8.0 if crank else 4.0)
    dt_scale = float(args.dt_scale) if args.dt_scale is not None else 1.0
    if dt_scale <= 0:
        raise SystemExit("--dt-scale must be > 0")
    d_i_list = list(args.d_i) if args.d_i is not None else (
        [0.2] if crank else [0.05, 0.2]
    )
    here = Path(__file__).resolve().parent
    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = here / out_path
    else:
        out_path = here / ("section_A_crank_out.txt" if crank else "section_A_out.txt")

    fh = open(out_path, "w", encoding="utf-8")
    try:
        log("Section A study — 3D textbook-B OT (A1-A4). Not a smoke.", fh)
        log("Watch only. No Clay-proof. No singularity claim. No Crow, no merge.", fh)
        log("u = U0 (-sin y, sin x, 0.2 cos z)", fh)
        log("B = B0 (-sin y, sin 2x, 0.2 cos z)  Qin-project B.", fh)
        log(
            f"matrix={'CRANK' if crank else 'HAVE-default'}  N_cli={args.N} "
            f"t_end={t_end} nu_fac={nu_fac:g} d_i={d_i_list} out={out_path}",
            fh,
        )
        log(
            f"hive defaults: nu={NU_DEF:.3e} (A2c OT, Pr_m=1)  "
            f"eta=DEFAULT_MHD eta_mag={ETA_DEF:.3e}  "
            f"/{nu_fac:g} -> nu={NU_DEF/nu_fac:.3e} eta={ETA_DEF/nu_fac:.3e}",
            fh,
        )
        log(
            "E(k_max)/E_tot: outermost dealiased Fourier shell vs total "
            "spectral kinetic+magnetic energy (Parseval 0.5 N^{-6} sum |hat|^2).",
            fh,
        )
        log("I_BKM = trapezoid of (max|omega|+max|J|) on the 0.1 samples.", fh)

        n_reason = "HAVE default N=32"
        if crank:
            prefer = int(args.N) if args.N is not None else 64
            N, n_reason = choose_crank_N(
                prefer, t_end, nu_fac, float(d_i_list[0]), fh
            )
        else:
            N = int(args.N) if args.N is not None else PREFERRED_N

        ic = seed_and_divb(N, fh)
        if ic is None:
            if crank:
                log(
                    f"FAILED seed/projection at N={N}. STOP (do not march). "
                    "div B / textbook-B seed must pass before crank.",
                    fh,
                )
                sys.exit(1)
            log(f"N={N} seed/divB failed; trying N={FALLBACK_N}", fh)
            N = FALLBACK_N
            ic = seed_and_divb(N, fh)
            if ic is None:
                log("FAILED seed/projection. Stop.", fh)
                sys.exit(1)
            log(f"N={N} (fallback because preferred N seed/divB failed)", fh)
            n_reason = f"fallback N={N}"
        else:
            log(f"N={N} ({n_reason}; 2x harmonic resolved; N=8 would drop it)", fh)

        runs = build_runs(crank, nu_fac, d_i_list, NU_DEF, ETA_DEF)
        results = {}
        skipped4 = False

        for spec in runs:
            k = spec["key"]
            if crank and k == "4":
                r2 = results.get("2") or {}
                r3 = results.get("3") or {}
                if r2.get("nan") or r2.get("oom") or r3.get("nan") or r3.get("oom"):
                    skipped4 = True
                    log(
                        "skip run 4 (run 2 or 3 NaN/OOM) as specified for crank.",
                        fh,
                    )
                    results["4"] = None
                    continue
            log(f"--- {spec['label']} ---", fh)
            rr = one_run(
                N, spec["mode"], spec["nu"], spec["eta"], spec["d_i"],
                ic, fh, t_end=t_end,
                dt_scale=dt_scale,
            )
            if k == "1" and rr.get("oom") and N > 32:
                log(
                    f"N={N} OOM on run 1; dropping ALL runs to N=32 and restarting.",
                    fh,
                )
                N = 32
                n_reason = "OOM at larger N; dropped ALL to 32"
                ic = seed_and_divb(N, fh)
                if ic is None:
                    log("FAILED seed on N=32 after OOM. Stop.", fh)
                    sys.exit(1)
                rr = one_run(
                    N, spec["mode"], spec["nu"], spec["eta"], spec["d_i"],
                    ic, fh, t_end=t_end,
                dt_scale=dt_scale,
            )
            if rr.get("oom") and k == "1" and N <= 32:
                log("FAILED: OOM even at N=32. Stop.", fh)
                sys.exit(1)
            results[k] = rr

        if crank:
            crank_three_verdicts(
                results, N, n_reason, nu_fac, skipped4, fh
            )
        else:
            log("", fh)
            log("==== 4-line verdict ====", fh)
            p1 = results["1"]
            peel1 = "peel" if p1.get("peel") else "no peel"
            if p1.get("nan"):
                peel1 = (
                    f"no clean peel claim (NaN; last good t={p1.get('last_good_t')})"
                )
            log(f"- peel or no peel on run 1: {peel1}. {p1.get('why','')}", fh)
            failed_small = bool(
                results["2"] and (results["2"].get("nan") or results["2"].get("oom"))
            )
            if failed_small:
                v2 = "FAILED smaller-damping (NaN/blowup); keep default"
            else:
                v2 = compare_peel(p1, results["2"])
            log(
                f"- peel stronger / weaker / same when nu,eta dropped (run 2): {v2}",
                fh,
            )
            if results["3"].get("nan"):
                v3 = (
                    f"hall run NaN at t>{results['3'].get('last_good_t')}; "
                    "no clean hall-vs-mhd peel claim"
                )
            else:
                chg = compare_peel(p1, results["3"])
                r_m = p1.get("r_peak")
                r_h = results["3"].get("r_peak")
                di3 = results["3"].get("d_i")
                v3 = (
                    f"peel {chg}; peak r mhd={r_m:.4f} hall(d_i={di3})={r_h:.4f}"
                )
            log(f"- hall vs mhd: peel changed? ratio changed? {v3}", fh)
            ibkm_all = []
            for k, rr in results.items():
                if rr and not rr.get("oom"):
                    ibkm_all.append(bool(rr.get("finite_ibkm")))
            yesno = "yes" if ibkm_all and all(ibkm_all) else "no"
            extra = []
            for k, rr in results.items():
                if not rr:
                    continue
                extra.append(
                    f"run{k}: I_BKM={rr.get('ibkm_end')} finite={rr.get('finite_ibkm')} "
                    f"NaN={rr.get('nan')}"
                )
            log(
                f"- I_BKM still finite on all runs? {yesno}  ({'; '.join(extra)})",
                fh,
            )

        log("", fh)
        log("==== run summary ====", fh)
        for k, rr in results.items():
            if not rr:
                log(f"run {k}: skipped", fh)
                continue
            log(
                f"run {k}: mode={rr.get('mode')} N={rr.get('N')} t_end_req={t_end} "
                f"last_t={rr.get('last_good_t')} nu={rr.get('nu')} eta={rr.get('eta')} "
                f"d_i={rr.get('d_i')} NaN={rr.get('nan')} dt={rr.get('dt')} "
                f"divB0={rr.get('divb0')} alias={rr.get('alias')} "
                f"ek_max={rr.get('ek_max')} elapsed={rr.get('elapsed')} "
                f"smooth={rr.get('smooth')}",
                fh,
            )
        log(f"tables written to {out_path}", fh)
        if crank:
            log(
                f"HAVE Section A crank (N={N} t={t_end:g}; "
                f"/{nu_fac:g} + hall {d_i_list[0]:g}; three verdicts).",
                fh,
            )
        else:
            log(
                "HAVE Section A (3D textbook-B; mhd/hall matrix; BKM + peel verdict).",
                fh,
            )
    finally:
        fh.close()


if __name__ == "__main__":
    main()

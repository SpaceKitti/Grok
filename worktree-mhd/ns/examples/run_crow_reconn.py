"""Crow reconnection: hydro / MHD (Shen flux) / Hall. HAVE script only.

3D anti-parallel Crow tubes. Same IC for three runs:
  1) hydro  mode="vorticity"  B=0  (magnetic off)
  2) mhd    mode="mhd"        Shen co-located flux  b_guide="flux"
  3) hall   mode="hall"       same B IC, d_i = 0.25 * R_tube

Akitti runs locally. Default N=32, t_end=0.5. No campaign, no merge,
no OT, no 0% I_leak hunt, no RHS smash.

Re-run:
  cd C:\\Users\\Akitt\\Grok\\worktree-mhd\\ns
  $env:PYTHONPATH="C:\\Users\\Akitt\\Grok\\worktree-mhd\\ns"
  $env:JAX_PLATFORMS="cpu"
  C:\\Users\\Akitt\\Grok\\.venv\\Scripts\\python.exe .\\examples\\run_crow_reconn.py --dry-run
  C:\\Users\\Akitt\\Grok\\.venv\\Scripts\\python.exe .\\examples\\run_crow_reconn.py

CLI: --N --t-end --steps --dry-run

================================================================
Notes vs filled (Crow/Hall notes + mill defaults)
================================================================
FROM NOTES / hive mill (not invented):
  Gamma = tube_circulation = 0.7     DEFAULT_MHD / generate_antiparallel_tubes
  R     = tube_radius      = 0.08    same
  sep   = tube_separation  = 0.24    same
  pert  = 0.04, axial_wave = 1       same
  eta_mag = 1e-3                     DEFAULT_MHD
  gamma_m DEFAULT is 0.0             empty B if left alone (mill comment)
  b_guide DEFAULT is "z"             uniform guide; NOT used here
  Shen path LIVE                     split_guide_fields: b_guide in
                                     ("flux","flux_tubes","shen") ->
                                     generate_b_flux_tubes (co-located)
  Hall Ohm LIVE                      mode="hall", d_i=0 matches mhd
  Crow notes (Merge/02, Lorentz/02)  viscoresistive floor / energy story;
                                     no Gamma/R/B table of their own
  open/01, open/03                   Crow campaigns closed; Phi meter is
                                     Harris E2 (flux_x_half live on MHD)

FILLED (not in those note files as a number / choice):
  gamma_m = Gamma = 0.7              DEFAULT 0 would give empty B; set
                                     equal to circulation for co-located
  b_guide = "flux"                   Shen live path. NOT hive Crow B
                                     (x / z / tube uniform). B0 ignored.
  d_i = 0.25 * R = 0.02              Aethon/Venus rule (not in the notes)
  N=32, dim=3, t_end=0.5             short local default
  nu = 5e-4                          driver dim=3 default
  force_on=False, viscoelastic=False
  core_sep definition                hive has no Crow core-distance diag
  reconnects-first rule              see below (not a who-wins from a fake run)

Shen flux used? YES if generate_b_flux_tubes / split_guide_fields
returns nonzero B at gamma_m=0.7 (printed at startup). If that path
were dead the script would refuse rather than silently use uniform B0.

================================================================
Core separation (helper; hive has no Crow core-distance diagnostic)
================================================================
Tubes run along x, split in y, Crow-kinked in z. Closest approach of
the symmetric Crow mode is at x = L/4 (axial_wave=1, sin(kx)=1).
This script takes |omega| on that y-z cut and returns the min-image
distance between the |omega| peak in y < L/2 and the peak in y >= L/2.
That is "distance of the two |omega| peaks in a y-z cut."

================================================================
Reconnects first (printed rule; fill after a real local run)
================================================================
Earliest t where core_sep first drops below R. If a run never crosses,
use the time of its first clear min of core_sep. max|J| peak time is
secondary (printed, not the crown). Phi=flux_x_half is optional/live
on MHD/Hall; Crow is not Harris — do not crown a Phi winner alone.
Hydro Phi is N/A (B=0).
"""
import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax
jax.config.update("jax_enable_x64", True)

import numpy as np
from chive_ns import (
    DEFAULT_MHD,
    cfl_dt,
    cfl_dt_mhd,
    generate_antiparallel_tubes,
    generate_b_flux_tubes,
    make_grid,
    run_framework,
    split_guide_fields,
    vorticity_from_velocity,
)


# Hive mill Crow / Shen defaults (see header).
GAMMA = float(DEFAULT_MHD["tube_circulation"])   # 0.7
R_TUBE = float(DEFAULT_MHD["tube_radius"])       # 0.08
SEP0 = float(DEFAULT_MHD["tube_separation"])     # 0.24
PERT = float(DEFAULT_MHD["tube_perturbation"])   # 0.04
AXIAL = int(DEFAULT_MHD["tube_axial_wave"])      # 1
ETA = float(DEFAULT_MHD["eta_mag"])              # 1e-3
NU = 5.0e-4   # driver dim=3 default
GAMMA_M = GAMMA   # FILLED: DEFAULT_MHD gamma_m is 0 -> empty B
D_I = 0.25 * R_TUBE   # FILLED: 0.25 * R = 0.02
B_GUIDE = "flux"      # Shen co-located; NOT uniform x/z/tube
T_END_DEF = 0.5
N_DEF = 32
CFL = 0.4
L_BOX = 1.0


def _arr(x):
    return np.asarray(x, dtype=float)


def log(msg):
    print(str(msg), flush=True)


def ic_params():
    return dict(
        circulation=GAMMA,
        radius=R_TUBE,
        separation=SEP0,
        perturbation=PERT,
        axial_wave=AXIAL,
    )


def mhd_params_shen(d_i=0.0):
    """Shen co-located flux. Do not pass uniform B0 guide."""
    return dict(
        DEFAULT_MHD,
        b_guide=B_GUIDE,
        gamma_m=GAMMA_M,
        B0=0.0,
        freeze_ext=0.0,
        eta_mag=ETA,
        eta_odd=0.0,
        eta_hyper=0.0,
        hyper_kcut=0.0,
        posdiv=0.0,
        glm_ch=0.0,
        d_i=float(d_i),
        T_e=0.0,
        harris=False,
        tube_radius=R_TUBE,
        tube_circulation=GAMMA,
        tube_separation=SEP0,
        tube_perturbation=PERT,
        tube_axial_wave=AXIAL,
    )


def closest_cut_index(N, L, axial_wave=1):
    """x-index of Crow closest approach: kx = pi/2 => x = L/(4*axial_wave)."""
    x_cut = L / (4.0 * max(int(axial_wave), 1))
    return int(np.round(x_cut / L * N)) % N


def core_separation(omega, grid, axial_wave=1):
    """Distance of the two |omega| peaks in a y-z cut.

    Hive mill has no Crow core-distance diagnostic. Definition:
    |omega| on the y-z plane at the Crow closest-approach cut
    (x = L/4 for axial_wave=1). Left peak = argmax in y < L/2;
    right peak = argmax in y >= L/2. Return min-image hypot(dy, dz).
    """
    w = np.asarray(omega)
    if np.iscomplexobj(w):
        axes = tuple(range(1, w.ndim))
        w = np.fft.ifftn(w, axes=axes).real
    wabs = np.sqrt(np.sum(np.square(w), axis=0))
    N = int(wabs.shape[0])
    L = float(grid["L"])
    dx = L / N
    ix = closest_cut_index(N, L, axial_wave)
    sl = wabs[ix, :, :]
    half = N // 2
    left = sl[:half, :]
    right = sl[half:, :]
    i1 = np.unravel_index(int(np.argmax(left)), left.shape)
    i2 = np.unravel_index(int(np.argmax(right)), right.shape)
    y1, z1 = float(i1[0]), float(i1[1])
    y2, z2 = float(i2[0] + half), float(i2[1])
    dy = (y2 - y1) * dx
    dz = (z2 - z1) * dx
    if dy > 0.5 * L:
        dy -= L
    if dy < -0.5 * L:
        dy += L
    if dz > 0.5 * L:
        dz -= L
    if dz < -0.5 * L:
        dz += L
    return float(np.hypot(dy, dz))


def omega_real_from_u(u, grid):
    u_hat = np.fft.fftn(np.asarray(u), axes=range(1, 4))
    om_hat = vorticity_from_velocity(u_hat, grid)
    return np.fft.ifftn(np.asarray(om_hat), axes=(1, 2, 3)).real


def omega_real_from_hat(omega_hat):
    return np.fft.ifftn(np.asarray(omega_hat), axes=(1, 2, 3)).real


def first_cross_or_min(t, sep, R):
    """Earliest t with sep < R; else time of first clear min of sep.

    'First clear min' = first index of the global minimum (leftmost if
    a plateau). Returns (t_hit, kind) with kind in ('cross_R', 'min_sep').
    """
    t = _arr(t)
    sep = _arr(sep)
    if t.size == 0:
        return float("nan"), "empty"
    below = np.where(sep < float(R))[0]
    if below.size:
        return float(t[int(below[0])]), "cross_R"
    imin = int(np.argmin(sep))
    return float(t[imin]), "min_sep"


def print_notes():
    log("=== Crow reconnection (HAVE script) ===")
    log("FROM NOTES / hive mill: Gamma=0.7 R=0.08 sep=0.24 pert=0.04 axial_wave=1 eta=1e-3")
    log("FROM NOTES / hive mill: gamma_m DEFAULT=0 (empty B); b_guide DEFAULT=z (unused)")
    log("FROM NOTES / hive mill: Shen flux LIVE at b_guide in (flux, flux_tubes, shen)")
    log("FILLED: gamma_m=Gamma=0.7 (co-located); b_guide=flux (NOT uniform x/z/tube)")
    log("FILLED: d_i = 0.25 * R_tube = %.4f  (R=%.4f)" % (D_I, R_TUBE))
    log("FILLED: N=32 dim=3 t_end=%.2f nu=5e-4 force_on=False viscoelastic=False" % T_END_DEF)
    log("core_sep: two |omega| peaks in the y-z cut at x=L/4 (Crow closest approach)")
    log("reconnects-first: earliest t with core_sep < R; else first clear min of sep")
    log("max|J| peak time is secondary. Phi=flux_x_half optional/live; not the crown.")
    log("hydro Phi is N/A (B=0). Crow is not Harris.")


def check_shen_flux(grid):
    """Confirm Shen co-located path is live (nonzero B at gamma_m=Gamma)."""
    mp = mhd_params_shen(d_i=0.0)
    B_hat = generate_b_flux_tubes(grid, mp, ic_params())
    B = np.fft.ifftn(np.asarray(B_hat), axes=(1, 2, 3)).real
    bmax = float(np.max(np.sqrt(np.sum(B ** 2, axis=0))))
    B_hat2, _, _ = split_guide_fields(grid, mp, ic_params())
    B2 = np.fft.ifftn(np.asarray(B_hat2), axes=(1, 2, 3)).real
    bmax2 = float(np.max(np.sqrt(np.sum(B2 ** 2, axis=0))))
    live = (bmax > 0.0) and (bmax2 > 0.0)
    log(
        "Shen flux path: generate_b_flux_tubes max|B|=%.6e  "
        "split_guide_fields max|B|=%.6e  live=%s  (b_guide=%s gamma_m=%.3f)"
        % (bmax, bmax2, live, B_GUIDE, GAMMA_M)
    )
    if not live:
        raise SystemExit(
            "Shen flux path returned empty B. Refusing hive Crow uniform "
            "b_guide x/z/tube. Set gamma_m>0 and keep b_guide=flux."
        )
    return bmax


def _run_one(mode, N, steps, dt, diag_every, d_i=0.0):
    """One Crow run via run_framework. Same tubes IC for all modes."""
    magnetic = mode in ("mhd", "hall")
    mp = mhd_params_shen(d_i=d_i) if magnetic else None
    out = run_framework(
        N=N, dim=3, steps=steps, dt=dt, diag_every=diag_every, scheme="rk2",
        mode=mode, ic="tubes", force_on=False, viscoelastic=False, nu=NU,
        ic_params=ic_params(),
        mhd_params=mp,
        magnetic=magnetic,
        n_scars=1, force_amp=0.0,
    )
    return out


def _sep_series_from_out(out, grid, u0):
    """core_sep at t=0 (IC) and t=t_end (final omega). Mill has no omega hist.

    Intermediate mill times have max|omega|, max|J|, Phi from run_framework.
    Mill hist has no omega snapshots, so core_sep is filled at t=0 (IC)
    and t=t_end (final omega_hat) only; other rows print n/a.
    Reconnects-first uses those two sampled sep points.
    """
    t = _arr(out["time"])
    sep = np.full(t.shape, np.nan, dtype=float)
    om0 = omega_real_from_u(u0, grid)
    sep0 = core_separation(om0, grid, AXIAL)
    om1 = omega_real_from_hat(out["omega_hat"])
    sepend = core_separation(om1, grid, AXIAL)
    if t.size:
        sep[0] = sep0
        sep[-1] = sepend
    return sep, sep0, sepend


def print_table(label, t, sep, maxw, maxj, phi, magnetic):
    log("--- %s ---" % label)
    if magnetic:
        log("%10s %12s %14s %14s %14s" % ("t", "core_sep", "max|w|", "max|J|", "Phi"))
    else:
        log("%10s %12s %14s %14s %14s" % ("t", "core_sep", "max|w|", "max|J|", "Phi"))
    for i in range(t.size):
        s = sep[i]
        s_s = ("%12.6f" % s) if np.isfinite(s) else ("%12s" % "n/a")
        j = maxj[i]
        p = phi[i]
        if magnetic:
            log("%10.4f %s %14.6e %14.6e %14.6e" % (t[i], s_s, maxw[i], j, p))
        else:
            log("%10.4f %s %14.6e %14s %14s" % (t[i], s_s, maxw[i], "N/A", "N/A"))


def parse_args():
    ap = argparse.ArgumentParser(description="Crow reconnection hydro/mhd/hall")
    ap.add_argument("--N", type=int, default=N_DEF)
    ap.add_argument("--t-end", type=float, default=T_END_DEF, dest="t_end")
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true", dest="dry_run")
    return ap.parse_args()


def plan_one(dt, t_end, steps_cli):
    """Per-mode steps from that mode's own CFL. Do not force hydro onto Hall dt."""
    if steps_cli is None:
        steps = max(1, int(np.ceil(float(t_end) / dt)))
    else:
        steps = int(steps_cli)
    diag_every = max(1, steps // 8)
    return steps, diag_every, steps * dt


def plan_dts(grid, u0, B_mhd):
    dt_h = float(cfl_dt(u0, float(grid["dx"]), NU, cfl=CFL))
    dt_m = float(cfl_dt_mhd(u0, B_mhd, float(grid["dx"]), NU, ETA, cfl=CFL, d_i=0.0))
    dt_ha = float(cfl_dt_mhd(u0, B_mhd, float(grid["dx"]), NU, ETA, cfl=CFL, d_i=D_I))
    return dt_h, dt_m, dt_ha


def print_reconnects_rule(results=None):
    log(
        "RECONNECTS-FIRST RULE: earliest t where core_sep drops below R=%.4f; "
        "if a run never crosses, use the time of its first clear min of core_sep. "
        "max|J| peak time is secondary. Phi is not the crown."
        % R_TUBE
    )
    if not results:
        log(
            "RECONNECTS-FIRST (placeholder): no march in this invocation; "
            "Akitti local run fills who hits the threshold first."
        )
        return
    hits = []
    for name, rec in results:
        t_hit, kind = first_cross_or_min(rec["t_sep"], rec["sep_e"], R_TUBE)
        jpeak_t = rec.get("t_jpeak", float("nan"))
        log(
            "  %s: t_hit=%.4f (%s)  sep0=%.4f  sepend=%.4f  t_max|J|=%s"
            % (
                name, t_hit, kind, rec["sep0"], rec["sepend"],
                ("%.4f" % jpeak_t) if np.isfinite(jpeak_t) else "N/A",
            )
        )
        hits.append((t_hit, name, kind))
    valid = [(th, n, k) for th, n, k in hits if np.isfinite(th)]
    if not valid:
        log("RECONNECTS-FIRST: no finite t_hit (no data).")
        return
    # Prefer any actual R-crossing over a min-only; among those, earliest t.
    crosses = [(th, n, k) for th, n, k in valid if k == "cross_R"]
    pool = crosses if crosses else valid
    pool.sort(key=lambda x: x[0])
    th, winner, kind = pool[0]
    log(
        "WHO HITS THE SEPARATION THRESHOLD FIRST: %s at t=%.4f (%s)."
        % (winner, th, kind)
    )


def main():
    args = parse_args()
    N = int(args.N)
    print_notes()
    log("d_i formula: d_i = 0.25 * R_tube = 0.25 * %.4f = %.4f" % (R_TUBE, D_I))

    grid = make_grid(N, L=L_BOX, dim=3)
    u0 = np.asarray(generate_antiparallel_tubes(grid, **ic_params()))
    om0 = omega_real_from_u(u0, grid)
    sep0 = core_separation(om0, grid, AXIAL)
    bmax = check_shen_flux(grid)
    mp = mhd_params_shen(d_i=0.0)
    B_hat, _, _ = split_guide_fields(grid, mp, ic_params())
    B0 = np.fft.ifftn(np.asarray(B_hat), axes=(1, 2, 3)).real

    log(
        "IC: dim=3 ic=tubes N=%d L=%.3f dx=%.6e  Gamma=%.3f R=%.4f sep=%.4f "
        "pert=%.4f axial=%d  core_sep(t=0)=%.6f (IC sep=%.4f)"
        % (N, float(grid["L"]), float(grid["dx"]), GAMMA, R_TUBE, SEP0, PERT,
           AXIAL, sep0, SEP0)
    )
    log(
        "B IC: Shen flux b_guide=%s gamma_m=%.3f max|B|=%.6e  "
        "(NOT uniform hive Crow B x/z/tube)"
        % (B_GUIDE, GAMMA_M, bmax)
    )
    log("Hall: d_i=0.25*R=%.4f   hydro B=0   force_on=False viscoelastic=False" % D_I)

    dt_h, dt_m, dt_ha = plan_dts(grid, u0, B0)
    # Per-mode CFL. Hall is tight: d_i * max|B| / dx (Shen |B| ~ Gamma_m / (pi R^2)).
    plans = {
        "hydro": (dt_h,) + plan_one(dt_h, args.t_end, args.steps),
        "mhd": (dt_m,) + plan_one(dt_m, args.t_end, args.steps),
        "hall": (dt_ha,) + plan_one(dt_ha, args.t_end, args.steps),
    }
    for name in ("hydro", "mhd", "hall"):
        dt, steps, diag_every, t_act = plans[name]
        log(
            "plan %s: t_end_req=%.4f dt=%.6e steps=%d diag_every=%d t_act=%.4f"
            % (name, args.t_end, dt, steps, diag_every, t_act)
        )
    log(
        "Hall CFL is tight (d_i=%.4f, Shen max|B|~%.2f): local hall march "
        "is the slow one. Hydro/mhd use their own larger dt. "
        "Cap with --steps if you only want a short smoke."
        % (D_I, float(np.max(np.sqrt(np.sum(B0 ** 2, axis=0)))))
    )

    if args.dry_run:
        log("dry-run: IC params + Shen live check printed; no march.")
        print_reconnects_rule(results=None)
        return

    results = []
    jobs = (
        ("hydro", "vorticity", 0.0, False),
        ("mhd", "mhd", 0.0, True),
        ("hall", "hall", D_I, True),
    )
    for name, mode, d_i, magnetic in jobs:
        dt, steps, diag_every, t_act = plans[name]
        log("RUN %s mode=%s d_i=%.4f magnetic=%s Shen=%s dt=%.6e steps=%d t_act=%.4f" % (
            name, mode, d_i, magnetic, magnetic, dt, steps, t_act))
        out = _run_one(mode, N, steps, dt, diag_every, d_i=d_i)
        t = _arr(out["time"])
        maxw = _arr(out["max_vort"])
        maxj = _arr(out.get("max_j", np.zeros_like(t)))
        phi = _arr(out.get("flux_x_half", np.zeros_like(t)))
        sep, s0, s1 = _sep_series_from_out(out, grid, u0)
        print_table(name, t, sep, maxw, maxj, phi, magnetic)
        t_jpeak = float("nan")
        if magnetic and maxj.size:
            t_jpeak = float(t[int(np.argmax(maxj))])
        # reconnects-first uses the two sampled sep points (t=0, t_end)
        t_sep = np.array([float(t[0]), float(t[-1])]) if t.size else np.array([])
        sep_e = np.array([s0, s1]) if t.size else np.array([])
        results.append((name, dict(
            t=t, sep=sep, t_sep=t_sep, sep_e=sep_e, sep0=s0, sepend=s1,
            t_jpeak=t_jpeak,
        )))
        log("%s sep(t=0)=%.6f sep(t_end)=%.6f max|w|_peak=%.6e" % (
            name, s0, s1, float(np.max(maxw)) if maxw.size else float("nan")))

    print_reconnects_rule(results)
    log("done. no merge, no Crow campaign, no OT, no 0% I_leak, mill RHS untouched.")


if __name__ == "__main__":
    main()


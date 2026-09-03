"""Section A study: 3D textbook-B OT regularity / current sheets (A1-A4).

Orion short-list #1. Not a smoke. Re-run from:
  cd C:\\Users\\Akitt\\Grok\\worktree-mhd\\ns
  python .\\examples\\run_section_A.py

Venus mill language:
  Finite max|omega|, max|J| on one run = this solution stayed smooth,
  NOT an A1 / Clay theorem claim.
  Peel = |J| climbs (or stays high) while |omega| does not follow.
  I_BKM finite on the table is yes/no only.
  If E(k_max)/E_tot >= 1e-2, flag aliasing; do not retune hyper_kcut.

Seed (A2c HAVE, do not replace with u=B):
  u = U0 (-sin y, sin x, 0.2 cos z)
  B = B0 (-sin y, sin 2x, 0.2 cos z)
  Qin-project B. N must be >= 16 (N=8 drops the 2x harmonic).
"""
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


def one_run(N, mode, nu, eta, d_i, ic_fields, fh=None):
    u, B = ic_fields["u"], ic_fields["B"]
    dx = float(ic_fields["grid"]["dx"])
    dt, n_per, dt_cfl, dt_job, umax, bmax, k_nyq, v_hall = choose_dt(
        u, B, dx, nu, eta, d_i
    )
    steps = int(round(T_END / dt))
    diag_every = n_per
    log(
        f"RUN mode={mode} N={N} t_end={T_END} nu={nu:.3e} eta={eta:.3e} "
        f"d_i={d_i} force_off scheme=rk2 ic=ot",
        fh,
    )
    log(
        f"  Hall CFL: hive dt_cfl={dt_cfl:.6e}  job-style "
        f"dt(v_hall=d_i*k_nyq*max|B|)={dt_job:.6e}  used dt={dt:.6e} "
        f"(snapped to sample 0.1; hive is stricter by ~pi). "
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
        nu=nu, eta=eta, d_i=d_i, mode=mode, N=N,
        ibkm_end=float(ibkm[-1]) if ibkm.size else float("nan"),
        r_start=float(r[0]), r_end=float(r[-1]), r_peak=float(np.max(r)),
        w_end=float(w[-1]), j_end=float(j[-1]),
        w_max=float(np.max(w)), j_max=float(np.max(j)),
        divb0=float(divb[0]),
        finite_ibkm=bool(np.isfinite(ibkm[-1])) if ibkm.size else False,
        smooth=smooth,
    )


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


def main():
    out_path = Path(__file__).resolve().parent / "section_A_out.txt"
    fh = open(out_path, "w", encoding="utf-8")
    try:
        log("Section A study — 3D textbook-B OT (A1-A4). Not a smoke.", fh)
        log("Watch only. No Clay-proof. No singularity claim. No Crow, no merge.", fh)
        log("u = U0 (-sin y, sin x, 0.2 cos z)", fh)
        log("B = B0 (-sin y, sin 2x, 0.2 cos z)  Qin-project B.", fh)
        log(
            f"hive defaults: nu={NU_DEF:.3e} (A2c OT, Pr_m=1)  "
            f"eta=DEFAULT_MHD eta_mag={ETA_DEF:.3e}  "
            f"/4 -> nu={NU_DEF/4:.3e} eta={ETA_DEF/4:.3e}",
            fh,
        )
        log(
            "E(k_max)/E_tot: outermost dealiased Fourier shell vs total "
            "spectral kinetic+magnetic energy (Parseval 0.5 N^{-6} sum |hat|^2).",
            fh,
        )
        log("I_BKM = trapezoid of (max|omega|+max|J|) on the 0.1 samples.", fh)

        N = PREFERRED_N
        ic = seed_and_divb(N, fh)
        if ic is None:
            log(f"N={N} seed/divB failed; trying N={FALLBACK_N}", fh)
            N = FALLBACK_N
            ic = seed_and_divb(N, fh)
            if ic is None:
                log("FAILED seed/projection. Stop.", fh)
                sys.exit(1)
            log(f"N={N} (fallback because preferred N seed/divB failed)", fh)
        else:
            log(f"N={N} preferred (2x harmonic resolved; N=8 would drop it)", fh)

        results = {}
        # 1) mhd default
        r1 = one_run(N, "mhd", NU_DEF, ETA_DEF, 0.0, ic, fh)
        if r1.get("oom"):
            log("N=32 OOM; dropping to N=16 as allowed.", fh)
            N = FALLBACK_N
            ic = seed_and_divb(N, fh)
            if ic is None:
                log("FAILED seed on fallback N. Stop.", fh)
                sys.exit(1)
            r1 = one_run(N, "mhd", NU_DEF, ETA_DEF, 0.0, ic, fh)
        results["1"] = r1
        if r1.get("oom"):
            log("FAILED: OOM even at N=16. Stop.", fh)
            sys.exit(1)

        # 2) smaller damping
        r2 = one_run(N, "mhd", NU_DEF / 4.0, ETA_DEF / 4.0, 0.0, ic, fh)
        failed_small = bool(r2.get("nan") or r2.get("oom"))
        if failed_small:
            log(
                "FAILED smaller-damping: nu,eta = default/4 blew up or NaN. "
                "Keeping default (run 1) for the /4 comparison.",
                fh,
            )
        results["2"] = r2

        # 3) hall d_i=0.05
        r3 = one_run(N, "hall", NU_DEF, ETA_DEF, 0.05, ic, fh)
        results["3"] = r3

        # 4) hall d_i=0.2 if 1-3 did not OOM
        r4 = None
        if not r3.get("oom"):
            r4 = one_run(N, "hall", NU_DEF, ETA_DEF, 0.2, ic, fh)
            results["4"] = r4
        else:
            log("skip run 4 (run 3 OOM)", fh)

        log("", fh)
        log("==== 4-line verdict ====", fh)
        p1 = results["1"]
        peel1 = "peel" if p1.get("peel") else "no peel"
        if p1.get("nan"):
            peel1 = f"no clean peel claim (NaN; last good t={p1.get('last_good_t')})"
        log(f"- peel or no peel on run 1: {peel1}. {p1.get('why','')}", fh)

        if failed_small:
            v2 = "FAILED smaller-damping (NaN/blowup); keep default"
        else:
            v2 = compare_peel(p1, results["2"])
        log(f"- peel stronger / weaker / same when nu,eta dropped (run 2): {v2}", fh)

        if results["3"].get("nan"):
            v3 = (
                f"hall run NaN at t>{results['3'].get('last_good_t')}; "
                "no clean hall-vs-mhd peel claim"
            )
        else:
            chg = compare_peel(p1, results["3"])
            r_m = p1.get("r_peak")
            r_h = results["3"].get("r_peak")
            v3 = (
                f"peel {chg}; peak r mhd={r_m:.4f} hall(d_i=0.05)={r_h:.4f}"
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
        log(f"- I_BKM still finite on all runs? {yesno}  ({'; '.join(extra)})", fh)

        log("", fh)
        log("==== run summary ====", fh)
        for k, rr in results.items():
            if not rr:
                continue
            log(
                f"run {k}: mode={rr.get('mode')} N={rr.get('N')} t_end_req={T_END} "
                f"last_t={rr.get('last_good_t')} nu={rr.get('nu')} eta={rr.get('eta')} "
                f"d_i={rr.get('d_i')} NaN={rr.get('nan')} dt={rr.get('dt')} "
                f"divB0={rr.get('divb0')} alias={rr.get('alias')} "
                f"smooth={rr.get('smooth')}",
                fh,
            )
        log(f"tables written to {out_path}", fh)
        log("HAVE Section A (3D textbook-B; mhd/hall matrix; BKM + peel verdict).", fh)
    finally:
        fh.close()


if __name__ == "__main__":
    main()

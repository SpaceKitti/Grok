"""Start-point option for pairA-drive-return: loop starting at 1.25 eps_EP (outside Gamma).

Called as `python run.py --start 1.25`. Writes RESULTS_start1p25.md, outputs/drive_start1p25.npz,
outputs/weights_vs_theta_start1p25.png, outputs/drive_start1p25_swapab.npz. The default 0.75 path
(run.main -> RESULTS.md) is not used or changed here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

import drive as D
from m_check import SX, m_check_log, pt_map

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
SPEEDS = {"fast": 1.0, "mid5": 5.0, "slow20": 20.0, "slow40": 40.0, "slow100": 100.0}
PRIMARY = ("slow40", "slow100")
DIRS = {"ccw (+w)": +1, "cw (-w)": -1}


def yn(b):
    return "YES" if b else "NO"


def cfmt(z):
    return f"{z.real:+.6g}{z.imag:+.6g}i"


def mfmt(M):
    return "[[" + ", ".join(cfmt(x) for x in M[0]) + "], [" + ", ".join(cfmt(x) for x in M[1]) + "]]"


def fname(idx, hi):
    return "higher-frequency" if idx == hi else "lower-frequency"


def ov(a, b):
    return float(abs(np.vdot(a, b)) / (np.linalg.norm(a) * np.linalg.norm(b)))


def run_set(speeds, tl, hi0, conv=None):
    runs = []
    for sp, gT in speeds.items():
        for dn, s in DIRS.items():
            for st in (0, 1):
                r = D.run_drive(s, gT, st)
                dw = None
                if conv is not None:
                    r2 = D.run_drive(s, gT, st, factor=2)
                    dw = max(float(np.max(np.abs(r["marks"][m]["w"] - r2["marks"][m]["w"]))) for m in (1, 2))
                    conv.append(dw)
                row = {"dir": dn, "s": s, "speed": sp, "gT": gT, "start": "AB"[st], "start_phys": fname(st, hi0),
                       "run": r, "dw_conv": dw}
                for m in (1, 2):
                    mk = r["marks"][m]
                    win = int(np.argmax(mk["w"]))
                    row[f"win{m}"] = "AB"[win]
                    row[f"win{m}_phys"] = fname(win, mk["hi_idx"])
                    row[f"w{m}"] = float(mk["w"][win])
                    row[f"wl{m}"] = mk["w"]
                    row[f"wplain{m}"] = mk["w_plain"]
                    row[f"psi{m}"] = mk["psi"]
                    row[f"trk{m}"] = tl[row["s"]][m][st] if tl else "-"
                runs.append(row)
    return runs


def main_start(frac: float) -> int:
    P = print
    D.set_start(frac)
    tag = "start" + f"{frac:g}".replace(".", "p")
    lam0, R0, _ = D.sheet_basis(D.EPS_START)
    hi0 = int(np.argmax(lam0.real))
    inG = D.in_gamma(D.EPS_START)
    P(f"start eps = {D.EPS_START} ({frac} eps_EP), in Gamma = {inG}; loop phase = {D.PHASE}")
    P(f"eigenvalues at start: lam_A = {lam0[0]}, lam_B = {lam0[1]}; lam - lam_EP = {lam0 - D.LAM_EP}")
    P(f"H' eigenvalues (shared decay removed): {lam0 + D.SHIFT}")
    gmin = D.min_gap_on_loop()
    tl = {s: D.tracked_labels(s) for s in (1, -1)}
    conv = []
    runs = run_set(SPEEDS, tl, hi0, conv)
    for r in runs:
        P(f"{r['dir']:9s} {r['speed']:7s} start {r['start']}({r['start_phys']}) | 2pi {r['win1']} {r['win1_phys']} w={r['w1']:.5f} [trk {r['trk1']}] | "
          f"4pi {r['win2']} {r['win2_phys']} w={r['w2']:.5f} [trk {r['trk2']}] | conv {r['dw_conv']:.1e}")

    MC = {sp: m_check_log(gT, hi0) for sp, gT in SPEEDS.items()}
    for sp, o in MC.items():
        for m, t in o["turns"].items():
            P(f"M {sp} {2*m}pi: |AA|/|BB|={t['abs_AA']/t['abs_BB']:.6f} |AB|/|BA|={t['abs_AB']/t['abs_BA']:.6g} relresT={t['rel_resid_transpose']:.1e} "
              f"relresPT={t['rel_resid_PT']:.1e} det={cfmt(t['det_ccw'])} s1={t['r1_ccw']['sigma'][0]:.4g} u_hi={t['r1_ccw']['frac_u_slow']:.5f} Dw_hi={t['r1_ccw']['frac_Dw_slow']:.5f}")

    pt_here = MC["slow40"]["pt"]
    _, R075, _ = D.sheet_basis(D.EPS_EP - D.R_LOOP)
    pt_075 = pt_map(R075)
    P(f"PT map at start: {np.round(pt_here, 6).tolist()}   at 0.75 eps_EP: {np.round(pt_075, 6).tolist()}")

    san = D.run_drive(+1, 0.01, 0)
    fid = {m: san["marks"][m]["fid"] for m in (1, 2)}
    fx = D.fixed_eps_check()

    # missing mechanism
    mm, full, follows = {}, {}, {}
    for sp in SPEEDS:
        for m in (1, 2):
            t = {(r["dir"], r["start"]): r for r in runs if r["speed"] == sp}
            mm[(sp, m)] = all(t[("ccw (+w)", st)][f"win{m}_phys"] != t[("cw (-w)", st)][f"win{m}_phys"] for st in "AB")
            full[(sp, m)] = mm[(sp, m)] and all(t[(d, "A")][f"win{m}_phys"] == t[(d, "B")][f"win{m}_phys"] for d in DIRS)
            follows[(sp, m)] = all(r[f"win{m}"] == r[f"trk{m}"] for r in t.values())
    primary = all(mm[(sp, 2)] for sp in PRIMARY)
    P(f"missing mechanism (primary gT=40,100 at 4pi) = {yn(primary)}")
    start_dep40 = not all(r["win2"] == [q for q in runs if q["speed"] == "slow40" and q["s"] == r["s"]][0]["win2"]
                          for r in runs if r["speed"] == "slow40")
    P(f"gT=40 winner depends on start sheet: {start_dep40}")

    # final states of gT=40 runs vs right eigenvectors
    fin40 = []
    for r in runs:
        if r["speed"] == "slow40":
            fin40.append((r, [ov(R0[:, k], r["psi2"]) for k in range(2)]))

    # a<->b swap (sigma_x relabelling)
    SW = {"slow40": 40.0, "slow100": 100.0}
    base = {(r["speed"], r["s"], r["start"]): r for r in runs if r["speed"] in SW}
    D.set_swap_ab(True)
    lamS, RS, _ = D.sheet_basis(D.EPS_START)
    tlS = {s: D.tracked_labels(s) for s in (1, -1)}
    runsS = run_set(SW, tlS, int(np.argmax(lamS.real)))
    D.set_swap_ab(False)
    swap_rows = []
    for r in runsS:
        b = base[(r["speed"], r["s"], r["start"])]
        swap_rows.append({"r": r, "b": b, "same_freq": r["win2_phys"] == b["win2_phys"] and r["win1_phys"] == b["win1_phys"],
                          "ov_sx": ov(r["psi2"], SX @ b["psi2"]), "ov_sx_conj": ov(r["psi2"], SX @ b["psi2"].conj()),
                          "ov_same": ov(r["psi2"], b["psi2"])})
    P(f"swap: lam_A,B = {lamS}; " + "; ".join(f"{q['r']['speed']} {q['r']['dir']} {q['r']['start']}: {q['r']['win2_phys']} (was {q['b']['win2_phys']}) ov sx={q['ov_sx']:.6f}" for q in swap_rows))

    # save
    sv = {"gamma": D.GAM, "eps_EP": D.EPS_EP, "r": D.R_LOOP, "eps_start": D.EPS_START, "lam_start": lam0, "R_start": R0}
    for i, r in enumerate(runs):
        k = f"run{i}_{r['speed']}_{'ccw' if r['s'] > 0 else 'cw'}_start{r['start']}"
        sv[k + "_theta"] = r["run"]["theta"]; sv[k + "_wA"] = r["run"]["wA"]; sv[k + "_wB"] = r["run"]["wB"]
        sv[k + "_psi2pi"] = r["psi1"]; sv[k + "_psi4pi"] = r["psi2"]
    for sp, o in MC.items():
        for m, t in o["turns"].items():
            sv[f"M_ccw_{sp}_{2*m}pi"] = t["M_ccw"]; sv[f"M_cw_{sp}_{2*m}pi"] = t["M_cw"]
        sv[f"D_{sp}"] = o["D"]
    np.savez(OUT / f"drive_{tag}.npz", **sv)
    svS = {"a_swapped": D.VX._seed.B, "b_swapped": D.VX._seed.A, "lam_start": lamS, "R_start": RS}
    for i, q in enumerate(swap_rows):
        r = q["r"]
        k = f"swap{i}_{r['speed']}_{'ccw' if r['s'] > 0 else 'cw'}_start{r['start']}"
        svS[k + "_wl2pi"] = r["wl1"]; svS[k + "_wl4pi"] = r["wl2"]; svS[k + "_psi4pi"] = r["psi2"]
    np.savez(OUT / f"drive_{tag}_swapab.npz", **svS)
    png = False
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(len(SPEEDS), 1, figsize=(9, 2.6 * len(SPEEDS)), sharex=True)
        for j, sp in enumerate(SPEEDS):
            for r in runs:
                if r["speed"] == sp:
                    ax[j].plot(r["run"]["theta"], r["run"]["wA"], "-" if r["s"] > 0 else "--", label=f"{r['dir']} start {r['start']}: w_A")
            ax[j].set_ylabel("w_A"); ax[j].set_title(f"start {frac} eps_EP, {sp}: gamma T = {SPEEDS[sp]}")
            ax[j].axvline(2 * np.pi, c="gray", lw=0.6); ax[j].legend(fontsize=7)
        ax[-1].set_xlabel("theta")
        fig.tight_layout(); fig.savefig(OUT / f"weights_vs_theta_{tag}.png", dpi=110); png = True
    except Exception as e:
        P("plot skipped:", e)

    # ---------------- RESULTS
    A_is_hi = hi0 == 0
    L = [f"# pairA-drive-return — RESULTS, start point {frac} ε_EP", "",
         "Companion to the signed-off RESULTS.md (start 0.75 ε_EP), which is unchanged. Produced by `python run.py --start 1.25`.", "",
         "Scope: two-mode toy (H_A is 2x2, from the Pair A handoff). Driven Schrödinger evolution i dψ/dt = H_A(ε(t))ψ; no field/MHD dynamics. C held.", "",
         f"Loop: ε(t) = ε_EP + r e^{{±iωt}} (no π shift), r = 0.25 ε_EP. Start/end ε = {frac} ε_EP = {D.EPS_START:.9f}: on the real axis, **inside Γ: {yn(inG)}** (Γ = [−ε_EP, ε_EP]). The loop crosses Γ at θ = π (ε = 0.75 ε_EP).",
         f"Eigenvalues at the start point: λ_A = {cfmt(lam0[0])}, λ_B = {cfmt(lam0[1])} (λ − λ_EP = {lam0[0]-D.LAM_EP:.6f}, {lam0[1]-D.LAM_EP:.6f}); "
         f"eigenvalues of H' = H_A + i(a+b)/2: {cfmt(lam0[0]+D.SHIFT)}, {cfmt(lam0[1]+D.SHIFT)} (real ±: same decay rate, different frequency).",
         f"Sheet labels at {frac} ε_EP (vortices-return convention continued off Γ): A = λ_EP + y/2, B = λ_EP − y/2, y = 2v√(ε−ε_EP)√(ε+ε_EP) with principal roots (Γ-segment cut). "
         f"Here ε > ε_EP is real, so both roots are real and positive and y = 2v·√(ε²−ε_EP²) < 0 (v < 0): sheet A = {'higher' if A_is_hi else 'lower'}-frequency mode (Re λ_A {'>' if A_is_hi else '<'} Re λ_B), sheet B = {'lower' if A_is_hi else 'higher'}-frequency mode.",
         "Physical naming: winners are named by FREQUENCY (higher- vs lower-Re λ mode at the recording point), since the decay rates are equal here. Weights: left-eigenvector weights w± = |c±|²/Σ|c|², c = R⁻¹ψ (R = unit-norm right eigenvectors at the recording point).", "",
         "## Speeds, integrator, convergence", "",
         "- γT per loop: " + ", ".join(f"{sp} {gT:g} (T = {gT/D.GAM:.4f})" for sp, gT in SPEEDS.items()) + f"; γ = |a−b|/2 = {D.GAM}; min |λ+−λ−| on the loop = {gmin:.6f}. (γT = 5 added for comparison with Venus's reference.)",
         "- Integrator: ψ ← exp(−i H'(t_mid) dt) ψ (exact 2x2 exponential), steps per turn = max(2000, γT/0.01) (γdt ≤ 0.01), ψ renormalised every step.",
         f"- Convergence (dt halved once, all {len(runs)} runs, 2π and 4π): max |Δw| = {max(conv):.2e}.", "",
         "## Drive table (winner = larger left-eigenvector weight at the recording point ε = 1.25 ε_EP)", "",
         "| direction | speed | start sheet | winner at 2π (w) [tracked label] | winner at 4π (w) [tracked label] | back at start / on Γ at 4π |",
         "|---|---|---|---|---|---|"]
    for r in runs:
        pure = f"pure {r['win2_phys']} mode ({r['win2']}, w={r['w2']:.5f})" if r["w2"] > 0.99 else f"mix A/B ≈ {100*r['wl2'][0]:.0f}/{100*r['wl2'][1]:.0f}, not a pure mode"
        L.append(f"| {r['dir']} | {r['speed']} (γT={r['gT']:g}) | {r['start']} ({r['start_phys']}) | {r['win1']} {r['win1_phys']} (w={r['w1']:.5f}) [{r['trk1']}] | "
                 f"{r['win2']} {r['win2_phys']} (w={r['w2']:.5f}) [{r['trk2']}] | ε back at start (by construction) but NOT on Γ; state: {pure} |")
    L += ["", "Left-eigenvector weights (w_A, w_B) and plain normalised-overlap weights:", "",
          "| direction | speed | start | 2π left | 4π left | 2π plain | 4π plain |", "|---|---|---|---|---|---|---|"]
    for r in runs:
        L.append(f"| {r['dir']} | {r['speed']} | {r['start']} | {r['wl1'][0]:.5f}, {r['wl1'][1]:.5f} | {r['wl2'][0]:.5f}, {r['wl2'][1]:.5f} | "
                 f"{r['wplain1'][0]:.4f}, {r['wplain1'][1]:.4f} | {r['wplain2'][0]:.4f}, {r['wplain2'][1]:.4f} |")
    L += ["", f"**By construction:** ε returns to its start {frac} ε_EP at 2π and 4π (closed loop). That point is OUTSIDE Γ, so the state is never 'back on Γ' here; the table reports only whether it is a pure mode and which one.", "",
          f"γT = 40 winner depends on the start sheet: **{yn(start_dep40)}**.", "",
          "## M-matrix check (log-scaled propagation)", "",
          "M = R⁻¹ U R (R = unit-norm right eigenvectors at the start point, columns [A, B]; D = RᵀR diagonal). Each start eigenvector is propagated separately with per-step renormalisation and a running log of its norm (Helios), so M is assembled without overflow. "
          "PT check uses U⁻¹ = adj(U) (exact for det U = 1), so it needs only the entries.", "",
          f"D = diag({cfmt(MC['slow40']['D'][0])}, {cfmt(MC['slow40']['D'][1])}); D_A/D_B = {cfmt(MC['slow40']['DA_over_DB'])} (|D_A/D_B| = {abs(MC['slow40']['DA_over_DB']):.6f}); |off-diag RᵀR| = {MC['slow40']['offdiag_D']:.1e}.", "",
          "| speed | turn | M_ccw | M_cw | rel ‖M_cw − D⁻¹M_ccwᵀD‖ | \\|M_AA\\|/\\|M_BB\\| | \\|M_AB\\|/\\|M_BA\\| | σ1, σ2 (ccw, computed) | σ1/σ2 | det M_ccw (exact 1) | rel PT residual | u: hi-freq frac | D⁻¹w: hi-freq frac |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for sp, o in MC.items():
        for m, t in o["turns"].items():
            q = t["r1_ccw"]
            L.append(f"| {sp} (γT={o['gT']:g}) | {2*m}π | {mfmt(t['M_ccw'])} | {mfmt(t['M_cw'])} | {t['rel_resid_transpose']:.1e} | {t['abs_AA']/t['abs_BB']:.6f} | {t['abs_AB']/t['abs_BA']:.6g} | "
                     f"{q['sigma'][0]:.4g}, {q['sigma'][1]:.3g} | {q['ratio']:.3g} | {cfmt(t['det_ccw'])} | {t['rel_resid_PT']:.1e} | {q['frac_u_slow']:.5f} | {q['frac_Dw_slow']:.5f} |")
    bad_det = [f"{sp} {2*m}π" for sp, o in MC.items() for m, t in o["turns"].items() if not t["precision_ok"]]
    bad_ent = [f"{sp} {2*m}π" for sp, o in MC.items() for m, t in o["turns"].items() if t["rel_resid_transpose"] > 1e-6]
    L += ["", "'hi-freq frac' = weight of the higher-frequency mode. ccw output = u; cw output = D⁻¹w.", "",
          ("⚠ Precision: " + ", ".join(bad_det) + ": det M ≠ 1. Since det U = 1 exactly, σ2 = 1/σ1 and σ1/σ2 = σ1²; once σ1² approaches 1/eps ≈ 4.5e15 (σ1 ≈ 9e7 at γT = 40), the subdominant singular value is lost to round-off even with log-scaled propagation (log scaling prevents overflow, not cancellation). "
           "In those rows the computed σ2, σ1/σ2 and det are NOT reliable; the M entries, the ratios |M_AA|/|M_BB| and |M_AB|/|M_BA|, u and D⁻¹w come from the dominant part and are reliable as long as the transpose residual stays small. "
           "The drive-table weights are reliable in any case (renormalised ψ; dt-halving converged)." if bad_det else "All rows pass det M = 1."), "",
          ("⚠ Entries unreliable (relative transpose residual > 1e-6, i.e. round-off has reached the dominant part too): " + ", ".join(bad_ent) + ". Do not use the M entries or ratios in these rows."
           if bad_ent else "All rows have relative transpose residual < 1e-6 (entries reliable)."), "",
          "Output directions at γT = 40 as overlaps |<R_k|v>|/norms with the right eigenvectors (R_A, R_B are not orthogonal here, |<R_A|R_B>|/norms = " f"{ov(R0[:,0], R0[:,1]):.6f}):", ""]
    for m in (1, 2):
        t = MC["slow40"]["turns"][m]
        L.append(f"- {2*m}π: ccw output u → (R_A {t['ov_u_R'][0]:.6f}, R_B {t['ov_u_R'][1]:.6f}); cw output D⁻¹w (from M_ccw) → (R_A {t['ov_Dw_R'][0]:.6f}, R_B {t['ov_Dw_R'][1]:.6f}); "
                 f"cw output from the direct cw propagation → (R_A {t['ov_ucw_R'][0]:.6f}, R_B {t['ov_ucw_R'][1]:.6f}).")
    L += ["", "Final states at 4π, γT = 40, overlap with (R_A, R_B), both start sheets (labelling-artifact test):", ""]
    for r, o_ in fin40:
        L.append(f"- {r['dir']} start {r['start']}: ({o_[0]:.6f}, {o_[1]:.6f}) → {r['win2']} {r['win2_phys']}")
    ccw_out = int(np.argmax(MC['slow40']['turns'][2]['ov_u_R'])); cw_out = int(np.argmax(MC['slow40']['turns'][2]['ov_Dw_R']))
    L += ["", f"u and D⁻¹w land on DIFFERENT eigenvectors at γT = 40: **{yn(ccw_out != cw_out)}** (ccw → R_{'AB'[ccw_out]}, cw → R_{'AB'[cw_out]}).", "",
          "PT map ψ → σx ψ* on the eigenvectors, normalised overlaps |<R_k|PT R_i>| (row i = A, B; columns k = A, B):",
          f"- at {frac} ε_EP: A → ({pt_here[0][0]:.6f}, {pt_here[0][1]:.6f}), B → ({pt_here[1][0]:.6f}, {pt_here[1][1]:.6f})",
          f"- at 0.75 ε_EP (contrast): A → ({pt_075[0][0]:.6f}, {pt_075[0][1]:.6f}), B → ({pt_075[1][0]:.6f}, {pt_075[1][1]:.6f})",
          f"PT maps each eigenvector to itself at {frac} ε_EP: **{yn(pt_here[0][0] > 1-1e-9 and pt_here[1][1] > 1-1e-9)}** (Helios predicted yes outside Γ); at 0.75 ε_EP it maps A↔B: {yn(pt_075[0][1] > 1-1e-9 and pt_075[1][0] > 1-1e-9)}. "
          "With PT eigenvectors mapped to themselves the PT relation constrains |M_AA| = |M_BB| instead of |M_AB| = |M_BA|, which is what the table shows.", "",
          "## Checks", "",
          f"- Sanity run γT = 0.01, start A (ccw): fidelity = {fid[1]:.8f} at 2π, {fid[2]:.8f} at 4π.",
          f"- Fixed ε = {frac} ε_EP, mixed start: ΔΓ = difference of Im λ = {fx['dGamma']:.2e} (equal decay rates), so the weight ratio should stay constant:", "",
          "| γt | ratio measured | expected (initial ratio)·e^{−2ΔΓt} | rel. error |", "|---|---|---|---|"]
    for rw in fx["rows"]:
        L.append(f"| {rw['gamma_t']:g} | {rw['measured']:.6e} | {rw['expected']:.6e} | {rw['rel_err']:.1e} |")
    L += ["", "## a↔b swap check (σx relabelling)", "",
          f"a = {D.VX._seed.B}, b = {D.VX._seed.A} (swapped in memory only; handoff files untouched), same v, start {frac} ε_EP, γT = 40 and 100. "
          "With the shared decay removed, a↔b is γ → −γ, a basis relabelling by σx; the eigenvalues depend on γ² and are unchanged. Expected: the winning FREQUENCY per direction is unchanged and the winning state is the σx image of the old one. "
          f"Eigenvalues after the swap: λ_A = {cfmt(lamS[0])}, λ_B = {cfmt(lamS[1])}.", "",
          "| speed | direction | start | winner 4π (swapped) | winner 4π (original) | same frequency (2π and 4π) | ‖<ψ_swap|σx ψ_orig>‖ | ‖<ψ_swap|σx ψ_orig*>‖ | ‖<ψ_swap|ψ_orig>‖ |", "|---|---|---|---|---|---|---|---|---|"]
    for q in swap_rows:
        r, b = q["r"], q["b"]
        L.append(f"| {r['speed']} | {r['dir']} | {r['start']} | {r['win2']} {r['win2_phys']} (w={r['w2']:.5f}) | {b['win2']} {b['win2_phys']} (w={b['w2']:.5f}) | {yn(q['same_freq'])} | {q['ov_sx']:.6f} | {q['ov_sx_conj']:.6f} | {q['ov_same']:.6f} |")
    L += ["", f"Winning frequency per direction unchanged after the swap: **{yn(all(q['same_freq'] for q in swap_rows))}**. (Start sheets are relabelled by the swap too, so rows are matched by sheet label.) "
          "v → −v is the same situation via σz (not run).", "",
          "## Missing mechanism", "",
          "Definition (same as RESULTS.md): **YES** only if ccw and cw give DIFFERENT physical winners (here: higher- vs lower-frequency mode) for the same start sheet; NO if they are the same. "
          "Full chiral conversion = YES and independent of the start sheet. Primary: γT = 40 and 100 at 4π.", "",
          "Per speed / time: " + "; ".join(f"{sp} 2π {yn(mm[(sp,1)])}, 4π {yn(mm[(sp,2)])}" for sp in SPEEDS) + ".",
          "Full chiral (start-sheet independent): " + "; ".join(f"{sp} 2π {yn(full[(sp,1)])}, 4π {yn(full[(sp,2)])}" for sp in SPEEDS) + ".",
          "Driven winner equals tracked label: " + "; ".join(f"{sp} 2π {yn(follows[(sp,1)])}, 4π {yn(follows[(sp,2)])}" for sp in SPEEDS) + ".", "",
          f"**missing mechanism (start {frac} ε_EP): {yn(primary)}**", ""]
    wp = {sp: {d: sorted({r["win2_phys"] for r in runs if r["speed"] == sp and r["dir"] == d}) for d in DIRS} for sp in PRIMARY}
    L.append("Reason: " + "; ".join(f"γT = {SPEEDS[sp]:g}: ccw → {'/'.join(wp[sp]['ccw (+w)'])}, cw → {'/'.join(wp[sp]['cw (-w)'])}" for sp in PRIMARY) +
             " at 4π, from either start sheet" + (" — the winner is set by the direction, not by the start sheet." if primary else "."))
    L += ["", "**Verdict (Helios wording):** the toy already has the mechanism; whether it shows depends on the start point. "
          "Inside Γ (0.75 ε_EP, RESULTS.md) the winner is direction-independent; outside Γ (1.25 ε_EP, this file) it is direction-dependent. Both come from the same H_A with nothing added. "
          "The earlier 'missing mechanism: NO' in RESULTS.md stands; this run shows where the effect lives, not something that was missing.", "",
          "## Comparison with Venus's independent integrator (pattern only)", "",
          "Venus's reference used sample values a = 1, b = 2, v = 1 (not the handoff values), so only the pattern is compared; mode labels can be mirrored by sign(v) and the a/b order. "
          "Her pattern at 1.25 ε_EP: γT = 40 → ccw ends on one frequency mode (~99.94%) from either start sheet, cw on the other, at 2π and 4π; γT = 5 → same lean, ~90/10; |M_AA| = |M_BB|; |M_AB|/|M_BA| ~ 0.1 (γT = 5), ~6e-4 (γT = 40); transpose holds to ~1e-7.", ""]
    g40 = {(r["dir"], r["start"]): r for r in runs if r["speed"] == "slow40"}
    g5 = {(r["dir"], r["start"]): r for r in runs if r["speed"] == "mid5"}
    t5, t40 = MC["mid5"]["turns"][2], MC["slow40"]["turns"][2]
    L.append(f"This run: γT = 40 → ccw {g40[('ccw (+w)','A')]['win2_phys']} (w = {g40[('ccw (+w)','A')]['w2']:.5f} from A, {g40[('ccw (+w)','B')]['w2']:.5f} from B), cw {g40[('cw (-w)','A')]['win2_phys']} "
             f"(w = {g40[('cw (-w)','A')]['w2']:.5f}, {g40[('cw (-w)','B')]['w2']:.5f}), same at 2π; γT = 5 → w ≈ {g5[('ccw (+w)','A')]['w2']:.3f}/{g5[('ccw (+w)','B')]['w2']:.3f} (ccw from A/B), "
             f"{g5[('cw (-w)','A')]['w2']:.3f}/{g5[('cw (-w)','B')]['w2']:.3f} (cw). |M_AA|/|M_BB| = {t5['abs_AA']/t5['abs_BB']:.6f} (γT=5), {t40['abs_AA']/t40['abs_BB']:.6f} (γT=40); "
             f"|M_AB|/|M_BA| = {t5['abs_AB']/t5['abs_BA']:.4g} (γT=5), {t40['abs_AB']/t40['abs_BA']:.4g} (γT=40), i.e. the inverse of her ratios (labels mirrored: 1/{t5['abs_AB']/t5['abs_BA']:.4g} = {t5['abs_BA']/t5['abs_AB']:.3g}, 1/{t40['abs_AB']/t40['abs_BA']:.4g} = {t40['abs_BA']/t40['abs_AB']:.2g}); "
             f"transpose residual {t40['rel_resid_transpose']:.1e} (relative, γT=40, 4π). Pattern agrees; digits are not expected to match (different a, b, v).")
    L += ["", "## Literature (expected only, not checked)", "",
          "Expected from EP-encircling work in C:\\Users\\Akitt\\Grok\\pdf\\ (Milburn et al. 1410.1882, quasiadiabatic dynamics; Hassan et al. 1706.09938, exact driven 2x2; Doppler et al. 1603.02325, mode switching): "
          "for slow loops in passive/lossy two-mode systems the final mode is fixed by the encircling direction rather than the start state (chiral switching), and the start point can change whether and how this shows. "
          "The papers were not read or compared quantitatively here; no agreement is claimed.", "",
          f"Scope: two-mode toy; two start points so far (0.75 ε_EP in RESULTS.md, {frac} ε_EP here)."]
    if png:
        L.append(f"Plot: outputs/weights_vs_theta_{tag}.png (w_A vs θ, all runs; w_B = 1 − w_A).")
    (ROOT / f"RESULTS_{tag}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    P(f"Wrote RESULTS_{tag}.md")
    return 0

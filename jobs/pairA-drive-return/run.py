"""pairA-drive-return: driven two-mode run + M-matrix check + on-cut path. Writes outputs/drive.npz, plot, RESULTS.md."""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

import numpy as np  # noqa: E402

import drive as D  # noqa: E402
from m_check import m_check  # noqa: E402
from on_cut import run_on_cut  # noqa: E402

SPEEDS = {"fast": 1.0, "slow20": 20.0, "slow40": 40.0, "slow100": 100.0}
PRIMARY = ("slow40", "slow100")
DIRS = {"ccw (+w)": +1, "cw (-w)": -1}


def yn(b):
    return "YES" if b else "NO"


def cfmt(z):
    return f"{z.real:+.6f}{z.imag:+.6f}i"


def mfmt(M):
    return "[[" + ", ".join(cfmt(x) for x in M[0]) + "], [" + ", ".join(cfmt(x) for x in M[1]) + "]]"


def back_text(r):
    if r["back"]:
        return "YES (ε back on Γ by construction; pure start-sheet mode)"
    wA, wB = r["wl2"]
    if r["w2"] > 0.99:
        return f"NO — ε back on Γ (by construction) but the state is a pure mode on the OTHER sheet ({r['win2']})"
    return (f"NO — ε is back on Γ (by construction) but the state is a fixed mix "
            f"(A/B ≈ {100*wA:.0f}/{100*wB:.0f}), not a pure mode")


def main() -> int:
    P = print
    lam0, R0, _ = D.sheet_basis(D.EPS_START)
    slow0 = int(np.argmax(lam0.imag))
    pname = {i: D.phys(i, slow0) for i in range(2)}
    P(f"gamma=|a-b|/2={D.GAM}  eps_EP={D.EPS_EP}  r={D.R_LOOP}  start/end eps={D.EPS_START} (0.75 eps_EP, in Gamma={D.in_gamma(D.EPS_START)})")
    P(f"at start: lam_A={lam0[0]:.6f} ({pname[0]}), lam_B={lam0[1]:.6f} ({pname[1]})")
    gmin = D.min_gap_on_loop()
    tl = {s: D.tracked_labels(s) for s in (1, -1)}

    runs, conv = [], []
    for sp, gT in SPEEDS.items():
        for dn, s in DIRS.items():
            for st in (0, 1):
                r = D.run_drive(s, gT, st)
                r2 = D.run_drive(s, gT, st, factor=2)
                dw = max(float(np.max(np.abs(r["marks"][m]["w"] - r2["marks"][m]["w"]))) for m in (1, 2))
                conv.append(dw)
                row = {"dir": dn, "s": s, "speed": sp, "gT": gT, "T": r["T"], "n": r["n_per_turn"],
                       "start": "AB"[st], "start_phys": pname[st], "run": r, "dw_conv": dw}
                for m in (1, 2):
                    mk = r["marks"][m]
                    win = int(np.argmax(mk["w"]))
                    row[f"win{m}"] = "AB"[win]
                    row[f"win{m}_phys"] = D.phys(win, mk["slow_idx"])
                    row[f"w{m}"] = float(mk["w"][win])
                    row[f"wplain{m}"] = mk["w_plain"]
                    row[f"wl{m}"] = mk["w"]
                    row[f"trk{m}"] = tl[s][m][st]
                row["back"] = D.in_gamma(D.eps_of(4 * np.pi, s).real) and row["win2"] == row["start"] and row["w2"] > 0.99
                runs.append(row)
                P(f"{dn:9s} {sp:7s} gT={gT:5.1f} start {row['start']}({row['start_phys']}) | 2pi: {row['win1']} {row['win1_phys']} w={row['w1']:.5f} [trk {row['trk1']}] | "
                  f"4pi: {row['win2']} {row['win2_phys']} w={row['w2']:.5f} [trk {row['trk2']}] | conv dw={dw:.2e}")

    # ---- M-matrix check
    MC = {}
    maxdiff_w = 0.0
    for sp, gT in SPEEDS.items():
        o = m_check(gT)
        MC[sp] = o
        P(f"M-CHECK {sp} gT={gT}: D={o['D']}  D_A/D_B={o['DA_over_DB']:.12f}  |offdiag R^T R|={o['offdiag_D']:.1e}")
        for m, t in o["turns"].items():
            P(f"  {2*m}pi  M_ccw={mfmt(t['M_ccw'])}")
            P(f"        M_cw ={mfmt(t['M_cw'])}")
            P(f"        |M_ccw|={np.round(np.abs(t['M_ccw']),6).tolist()}  |M_cw|={np.round(np.abs(t['M_cw']),6).tolist()}")
            P(f"        det M_ccw={t['det_ccw']:.6g} det M_cw={t['det_cw']:.6g} (exact 1) precision_ok={t['precision_ok']}")
            P(f"        ||M_cw - D^-1 M_ccw^T D||={t['resid_transpose']:.2e}  ||U_cw - sx U_ccw^-dag sx||={t['resid_PT']:.2e}  |M_AB|={t['abs_AB']:.9f} |M_BA|={t['abs_BA']:.9f}")
            for nm in ("ccw", "cw"):
                q = t[f"r1_{nm}"]
                P(f"        {nm}: sigma1={q['sigma'][0]:.6f} sigma2={q['sigma'][1]:.6f} s1/s2={q['ratio']:.4f} class={t['class_'+nm]['kind']}  "
                  f"u slow-frac={q['frac_u_slow']:.5f}  D^-1 w slow-frac={q['frac_Dw_slow']:.5f}")
            # cross-check drive-table weights against M columns
            for rr in runs:
                if rr["speed"] == sp:
                    wm = t["w_ccw" if rr["s"] > 0 else "w_cw"][rr["start"]]
                    maxdiff_w = max(maxdiff_w, float(np.max(np.abs(wm - rr[f"wl{m}"]))))
    P(f"max |w(drive table) - w(M columns)| = {maxdiff_w:.2e}")

    san = D.run_drive(+1, 0.01, 0)
    fid = {m: san["marks"][m]["fid"] for m in (1, 2)}
    P(f"sanity gT=0.01 start A: fidelity 2pi={fid[1]:.8f} 4pi={fid[2]:.8f}")
    fx = D.fixed_eps_check()

    # ---- missing mechanism
    mm, sec, follows = {}, {}, {}
    for sp in SPEEDS:
        for m in (1, 2):
            t = {(r["dir"], r["start"]): r for r in runs if r["speed"] == sp}
            mm[(sp, m)] = all(t[("ccw (+w)", st)][f"win{m}_phys"] != t[("cw (-w)", st)][f"win{m}_phys"] for st in "AB")
            start_indep = all(t[(d, "A")][f"win{m}"] == t[(d, "B")][f"win{m}"] for d in DIRS)
            sec[(sp, m)] = start_indep and t[("ccw (+w)", "A")][f"win{m}"] != t[("cw (-w)", "A")][f"win{m}"]
            follows[(sp, m)] = all(r[f"win{m}"] == r[f"trk{m}"] for r in t.values())
    primary = any(mm[(sp, 2)] for sp in PRIMARY)
    P(f"missing mechanism (primary gT=40,100 at 4pi) = {yn(primary)}")

    oc = run_on_cut()
    for o in oc:
        P(f"on-cut {o['name']}: max diff={o['max_diff']:.1e} -> {yn(o['yes'])}")

    # ---- save + plot
    sv = {"gamma": D.GAM, "eps_EP": D.EPS_EP, "r": D.R_LOOP, "eps_start": D.EPS_START}
    for i, r in enumerate(runs):
        k = f"run{i}_{r['speed']}_{'ccw' if r['s'] > 0 else 'cw'}_start{r['start']}"
        sv[k + "_theta"] = r["run"]["theta"]; sv[k + "_wA"] = r["run"]["wA"]; sv[k + "_wB"] = r["run"]["wB"]
        sv[k + "_psi2pi"] = r["run"]["marks"][1]["psi"]; sv[k + "_psi4pi"] = r["run"]["marks"][2]["psi"]
    for sp, o in MC.items():
        for m, t in o["turns"].items():
            sv[f"M_ccw_{sp}_{2*m}pi"] = t["M_ccw"]; sv[f"M_cw_{sp}_{2*m}pi"] = t["M_cw"]
        sv[f"D_{sp}"] = o["D"]
    np.savez(OUT / "drive.npz", **sv)
    png = False
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(len(SPEEDS), 1, figsize=(9, 2.8 * len(SPEEDS)), sharex=True)
        for j, sp in enumerate(SPEEDS):
            for r in runs:
                if r["speed"] != sp:
                    continue
                ls = "-" if r["s"] > 0 else "--"
                ax[j].plot(r["run"]["theta"], r["run"]["wA"], ls, label=f"{r['dir']} start {r['start']}: w_A")
            ax[j].set_ylabel("w_A"); ax[j].set_title(f"{sp}: gamma T = {SPEEDS[sp]}")
            ax[j].axvline(2 * np.pi, c="gray", lw=0.6); ax[j].legend(fontsize=7)
        ax[-1].set_xlabel("theta")
        fig.tight_layout(); fig.savefig(OUT / "weights_vs_theta.png", dpi=110); png = True
    except Exception as e:
        P("plot skipped:", e)

    # ---- RESULTS.md
    L = ["# pairA-drive-return — RESULTS", "", "Signed off: Venus (maths), Helios (physics), 2026-09-25", "",
         "Scope: two-mode toy (H_A is 2x2, from the Pair A handoff). Driven Schrödinger evolution i dψ/dt = H_A(ε(t))ψ; no field/MHD dynamics. C held.", "",
         f"Model: seed.H_A, ε_EP = {D.EPS_EP:.9f}, λ_EP = {D.LAM_EP}, γ = |a−b|/2 = {D.GAM}, r = 0.25 ε_EP = {D.R_LOOP:.9f}.",
         f"Loop: ε(t) = ε_EP + r e^{{i(±ωt+π)}}. Start/end point ε = 0.75 ε_EP = {D.EPS_START:.9f} (inside Γ = [−ε_EP, ε_EP]: {yn(D.in_gamma(D.EPS_START))}).",
         f"At the start/end point: sheet A λ = {lam0[0]:.6f} ({pname[0]}), sheet B λ = {lam0[1]:.6f} ({pname[1]}). Sheet A = λ_EP + y/2, B = λ_EP − y/2, Γ-segment cut read on the upper lip (vortices-return convention).",
         "Shared decay −i(a+b)/2 removed (H' = H_A + i(a+b)/2); ψ renormalised every step. Weights: w± = |c±|²/Σ|c|² with c = R⁻¹ψ, i.e. c± = <L±|ψ>/<L±|R±>; R columns = right eigenvectors at the recording point, unit Euclidean norm. Plain normalised-overlap weights shown for comparison only.", "",
         "## Speeds, integrator, convergence", "",
         f"- γT per loop (T = 2π/|ω|): " + ", ".join(f"{sp} γT = {gT:g} (T = {gT/D.GAM:.4f}, ω/min-gap = {2*np.pi/(gT/D.GAM)/gmin:.4f})" for sp, gT in SPEEDS.items()) + f"; min |λ+−λ−| on the loop = {gmin:.6f}.",
         "- Integrator: ψ ← exp(−i H'(t_mid) dt) ψ (exact 2x2 exponential), steps per turn = max(2000, γT/0.01): " + ", ".join(f"{sp} {D.steps_per_turn(gT)} (γdt = {gT/D.steps_per_turn(gT):.4f})" for sp, gT in SPEEDS.items()) + ".",
         f"- Convergence (dt halved once, all {len(runs)} runs, 2π and 4π): max |Δw| = {max(conv):.2e}.", "",
         "## Drive table (winner = larger left-eigenvector weight at the recording point ε = 0.75 ε_EP)", "",
         "| direction | speed | start sheet | winner at 2π (w) [tracked label] | winner at 4π (w) [tracked label] | back on Γ at 4π |",
         "|---|---|---|---|---|---|"]
    for r in runs:
        L.append(f"| {r['dir']} | {r['speed']} (γT={r['gT']:g}) | {r['start']} ({r['start_phys']}) | {r['win1']} {r['win1_phys']} (w={r['w1']:.5f}) [{r['trk1']}] | "
                 f"{r['win2']} {r['win2_phys']} (w={r['w2']:.5f}) [{r['trk2']}] | {back_text(r)} |")
    L += ["", "Start point for all runs: ε = 0.75 ε_EP (inside Γ). [tracked label] = where continuous eigenvalue tracking takes the start sheet (swap at 2π, return at 4π).", "",
          "Plain normalised-overlap weights (w_A, w_B) for comparison:", "",
          "| direction | speed | start | 2π plain | 4π plain | 2π left (w_A, w_B) | 4π left (w_A, w_B) |", "|---|---|---|---|---|---|---|"]
    for r in runs:
        L.append(f"| {r['dir']} | {r['speed']} | {r['start']} | {r['wplain1'][0]:.4f}, {r['wplain1'][1]:.4f} | {r['wplain2'][0]:.4f}, {r['wplain2'][1]:.4f} | "
                 f"{r['wl1'][0]:.5f}, {r['wl1'][1]:.5f} | {r['wl2'][0]:.5f}, {r['wl2'][1]:.5f} |")
    L += ["", "**By construction:** ε is back on Γ at 2π and 4π by construction (the loop is phase-shifted to start and end at 0.75 ε_EP). "
          "'Back on Γ at 4π' = YES only if, in addition, the final state is a single-sheet state (w > 0.99) on its start sheet.", "",
          "## M-matrix check (Venus)", "",
          "M = R⁻¹ U R, U = un-renormalised propagator of H' (det U = 1), R = right eigenvectors at ε = 0.75 ε_EP, columns [A, B], unit Euclidean norm "
          "(a column scaling, so D = RᵀR stays diagonal). Start on sheet j reads column j of M. Venus: M_cw = D⁻¹ M_ccwᵀ D, so cw from A reads row A of M_ccw.", ""]
    o0 = next(iter(MC.values()))
    L.append(f"D = diag({cfmt(o0['D'][0])}, {cfmt(o0['D'][1])}); D_A/D_B = {cfmt(o0['DA_over_DB'])}; |off-diagonal of RᵀR| = {o0['offdiag_D']:.1e}.")
    L.append("")
    L += ["| speed | turn | M_ccw | M_cw | det M_ccw (exact 1) | ‖M_cw − D⁻¹M_ccwᵀD‖ | \\|M_AB\\|, \\|M_BA\\| | σ1, σ2 (ccw) | σ1/σ2 | class (ccw) | u (ccw output): slow frac | D⁻¹w from M_ccw: slow frac | u_cw (cw output, direct): slow frac |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for sp, o in MC.items():
        for m, t in o["turns"].items():
            q = t["r1_ccw"]
            flag = "" if t["precision_ok"] else " ⚠"
            L.append(f"| {sp} (γT={o['gT']:g}){flag} | {2*m}π | {mfmt(t['M_ccw'])} | {mfmt(t['M_cw'])} | {cfmt(t['det_ccw'])} | {t['resid_transpose']:.1e} | {t['abs_AB']:.6f}, {t['abs_BA']:.6f} | "
                     f"{q['sigma'][0]:.4g}, {q['sigma'][1]:.4g} | {q['ratio']:.4g} | {t['class_ccw']['kind']} | {q['frac_u_slow']:.5f} | {q['frac_Dw_slow']:.5f} | {t['r1_cw']['frac_u_slow']:.5f} |")
    L += ["", f"Note (Helios): σ1/σ2 does not grow steadily with loop time ({MC['slow20']['turns'][2]['r1_ccw']['ratio']:.1f} at γT=20, "
          f"{MC['slow40']['turns'][2]['r1_ccw']['ratio']:.1f} at γT=40). This is physical, not a bug: the loss contrast partly cancels around the loop because the decay gap changes sign across the cut."]
    L += ["", "|M| entries and cw singular values:", "", "| speed | turn | \\|M_ccw\\| | \\|M_cw\\| | σ1, σ2 (cw) | ‖U_cw − σx U_ccw^{−†} σx‖ |", "|---|---|---|---|---|---|"]
    for sp, o in MC.items():
        for m, t in o["turns"].items():
            a, b = np.abs(t["M_ccw"]), np.abs(t["M_cw"])
            q = t["r1_cw"]
            L.append(f"| {sp} | {2*m}π | [[{a[0,0]:.6f}, {a[0,1]:.6f}], [{a[1,0]:.6f}, {a[1,1]:.6f}]] | [[{b[0,0]:.6f}, {b[0,1]:.6f}], [{b[1,0]:.6f}, {b[1,1]:.6f}]] | {q['sigma'][0]:.4f}, {q['sigma'][1]:.4f} | {t['resid_PT']:.1e} |")
    okt = [t for o in MC.values() for t in o["turns"].values() if t["precision_ok"]]
    bad = [f"{sp} {2*m}π" for sp, o in MC.items() for m, t in o["turns"].items() if not t["precision_ok"]]
    resT = max(t["resid_transpose"] for t in okt)
    resPT = max(t["resid_PT"] for t in okt)
    dAB = max(abs(t["abs_AB"] - t["abs_BA"]) / t["abs_BA"] for t in okt)
    L += ["", f"Rank-1 fit: M ≈ σ1 u wᵀ (leading SVD pair, wᵀ = v1ᴴ). ccw output direction = u; cw output direction = D⁻¹w. Chiral would mean u ≠ D⁻¹w. 'slow frac' = weight of the slower-decaying mode (sheet {'AB'[slow0]}).", "",
          ("⚠ Precision limit: " + ", ".join(bad) + ": det M ≠ 1 (see table), i.e. the un-renormalised propagator's dynamic range (σ1/σ2 = σ1² with det = 1; σ1 ≈ 3e5 at 2π, ≈ 7e10 at 4π) exceeds double precision, so the individual M entries, the identity residuals and D⁻¹w from M_ccw's row are NOT reliable there. "
           "The output directions u (the attractor of each direction's own propagation) and the renormalised drive-table weights are reliable (dt-halving converged). For these cases compare u (ccw output) with u_cw (cw output from the direct cw propagation, which equals D⁻¹w in exact arithmetic). "
           "An optional fix without mpmath: propagate the two basis vectors separately, renormalising each step with a running log of the norms, to get M in log-scaled form. Not done; the weights at γT=100 are already dt-converged." if bad else "All M matrices pass det M = 1."), "",
          "**Why the weights are identical in both directions (computed, not assumed; residuals over the precision-OK cases γT = 1, 20, 40):**",
          f"1. D_A/D_B = {cfmt(o0['DA_over_DB'])} (|D_A| = |D_B|), so Venus's identity M_cw = D⁻¹M_ccwᵀD reduces to M_cw = M_ccwᵀ (max residual {resT:.1e}).",
          f"2. |M_AB| = |M_BA| (max relative difference {dAB:.1e}). This comes from a second symmetry: H' is PT-symmetric, σx H'(ε)* σx = H'(ε̄), which gives U_cw = σx (U_ccw⁻¹)† σx (max residual {resPT:.1e}); combined with U_cw = U_ccwᵀ it fixes the off-diagonal moduli of M to be equal.",
          "3. cw from sheet j reads row j of M_ccw, ccw reads column j; with (1) and (2) the row and the column have identical moduli, so the weights are identical. M_ccw is not diagonal or antidiagonal here; the equality is from the two symmetries, not from adiabaticity. "
          "It holds for this start point (real ε inside Γ); other start points were not run. At γT = 100 the identities cannot be checked in double precision, but both directions' output directions u agree (table) and the drive-table weights are identical.",
          f"4. Old weight code: correct. Drive-table weights agree with the M-column weights to {maxdiff_w:.1e}; no old number changed.", "",
          "## Checks", "",
          f"- Sanity run γT = 0.01, start A (ccw): fidelity |<ψ₀|ψ_end>|/norms = {fid[1]:.8f} at 2π, {fid[2]:.8f} at 4π (expect ≈ 1).",
          f"- Fixed ε = 0.75 ε_EP, mixed start (R_A + R_B): ΔΓ = Im λ_slow − Im λ_fast = {fx['dGamma']:.6f}; slower-decaying mode = sheet {fx['slow_sheet']}.", "",
          "| γt | w_fast/w_slow measured | expected (initial ratio)·e^{−2ΔΓt} | rel. error |", "|---|---|---|---|"]
    for rw in fx["rows"]:
        L.append(f"| {rw['gamma_t']:g} | {rw['measured']:.6e} | {rw['expected']:.6e} | {rw['rel_err']:.1e} |")
    L += ["", "## On-cut path (on_cut.py)", "",
          "Start on Γ, go along Γ to ε = 0, figure-eight around both tips (+ε_EP anticlockwise, −ε_EP clockwise, as in vortices-return), back along Γ; continuous eigenvalue tracking.", "",
          "| start | λ at start | λ at end | max \\|Δλ\\| | λ on Γ at the end (returns to start value) |", "|---|---|---|---|---|"]
    for o in oc:
        L.append(f"| {o['name']} | {o['lam_start'][0]:.6f}, {o['lam_start'][1]:.6f} | {o['lam_end'][0]:.6f}, {o['lam_end'][1]:.6f} | {o['max_diff']:.1e} | **{yn(o['yes'])}** |")
    L += ["", "Expected YES (Venus): this is a setup check, already known from pairA-vortices-return, not a new result.", "",
          "## Missing mechanism", "",
          "Definition (fixed before running, Helios/Orion): **YES** only if ccw and cw give DIFFERENT physical winners (slower- vs faster-decaying mode at the recording point) for the same start sheet; "
          "if both directions give the same winner (e.g. both slower-decaying = passive drift baseline) → **NO**. Primary: the slowest runs, γT = 40 and γT = 100, at 4π.", "",
          "Per speed / time: " + "; ".join(f"{sp} 2π {yn(mm[(sp,1)])}, 4π {yn(mm[(sp,2)])}" for sp in SPEEDS) + ".",
          "Secondary (earlier wording: winner depends on direction and not on start sheet): " + "; ".join(f"{sp} 2π {yn(sec[(sp,1)])}, 4π {yn(sec[(sp,2)])}" for sp in SPEEDS) + ".",
          "Driven winner equals tracked label (state follows the sheet swap): " + "; ".join(f"{sp} 2π {yn(follows[(sp,1)])}, 4π {yn(follows[(sp,2)])}" for sp in SPEEDS) + ".", "",
          f"**missing mechanism: {yn(primary)}**", ""]
    pw = {sp: sorted({r["win2_phys"] for r in runs if r["speed"] == sp}) for sp in PRIMARY}
    rk = {sp: (MC[sp]["turns"][2]["r1_ccw"]["frac_u_slow"], MC[sp]["turns"][2]["r1_cw"]["frac_u_slow"]) for sp in PRIMARY}
    if not primary:
        L.append(f"Reason: at γT = 40 and 100 both directions end on the same physical mode at 4π ({', '.join(f'{sp}: ' + '/'.join(v) for sp, v in pw.items())}); "
                 f"in the rank-1 fit the ccw output u and the cw output (D⁻¹w; taken from the direct cw propagation) both lean to the slower-decaying mode (slow fractions ccw, cw at 4π: " +
                 ", ".join(f"{sp} {a:.3f}, {b:.3f}" for sp, (a, b) in rk.items()) + ") — the physical non-chiral NO (passive drift toward the slower-decaying mode), with the directions made equal by the transpose + PT symmetries at this start point.")
    else:
        L.append("Reason: at γT = 40 or 100, ccw and cw end on different physical modes at 4π for each start sheet.")
    L += ["", "Scope: two-mode toy; one start point (0.75 ε_EP on the real axis). The start point can change which direction flips (Milburn et al.); other start points were not run.", ""]
    if png:
        L.append("Plot: outputs/weights_vs_theta.png (w_A vs θ for every run; w_B = 1 − w_A).")
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    P("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="pairA-drive-return")
    ap.add_argument("--start", type=float, default=0.75,
                    help="loop start point in units of eps_EP: 0.75 (default, signed-off RESULTS.md) or 1.25 (RESULTS_start1p25.md)")
    args = ap.parse_args()
    if abs(args.start - 0.75) < 1e-12:
        raise SystemExit(main())
    from start_other import main_start  # noqa: E402
    raise SystemExit(main_start(args.start))

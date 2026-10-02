"""pairA-vortices-return: run everything, write outputs/tracks.npz, plot, RESULTS.md."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

from vortices import (EPS_EP, GAMMA, GAMMA_STR, HANDOFF, H_A, LAM_EP, circulation,  # noqa: E402
                      in_gamma, lam_ep_at, physics_checks)
from tracks import circle, figure_eight, track  # noqa: E402
from return_test import CUTS, LAM_EP as _L, loop_report, y_cut_gamma  # noqa: E402
import gauge_J  # noqa: E402  (handoff gauge_J.py, imported read-only)

PI = np.pi
SCOPE_TXT = 'Scope [careful-before-toy]: This is a statement about the eigenvalue sheets of H_A with ε moved by hand (quasi-static monodromy). It does not carry over to a state driven around the loop in time. That would mean solving i dψ/dt = H_A(ε(t))ψ, and with losses such a driven run typically ends on one mode that depends on which way you go around, not on the label swap (a known lossy-EP effect). "Vortex" here means arg(λ−λ_EP) winding by π per loop around a core [hive-interpretation], not a flow vortex. Physics picture (Helios): H_A + i(a+b)/2 = [[−iγ, εv],[εv, +iγ]] with γ=(a−b)/2. Both rates are losses, so the system is passive. Inside Γ the two modes share a frequency and decay at different rates; outside Γ they share a decay rate and have different frequencies.'
NOTE_TXT = "This NO comes straight from the formula and is not a failed return. For real ε inside Γ (|ε|<ε_EP), the square root √(ε²v²−(a−b)²/4) is imaginary, so λ−λ_EP is purely imaginary; outside Γ it is real. 'Re ε in Γ' and 'Im(λ−λ_EP)=0' can both hold only at the cores. The handoff's 1.25ε_EP start sits in the other (real-gap) phase."


def yn(b: bool) -> str:
    return "YES" if b else "NO"


def main() -> int:
    L = []
    P = print
    dim = H_A(0.3 + 0j).shape[0]
    P(f"handoff = {HANDOFF}")
    P(f"H_A dimension = {dim}x{dim}")
    P(f"eps_EP = {EPS_EP!r}   lambda_EP(seed) = {LAM_EP}")
    P(f"Gamma (handoff wick_lorentzian.chart) = {GAMMA_STR} = [{GAMMA[0]}, {GAMMA[1]}]")
    lep = {+1: lam_ep_at(+EPS_EP), -1: lam_ep_at(-EPS_EP)}
    P(f"lambda_EP at +core = {lep[+1]}   at -core = {lep[-1]}")

    # ---- Gamma check
    r = 0.25 * EPS_EP
    start = EPS_EP + r
    g_ok = in_gamma(start)
    P(f"GAMMA CHECK: eps_EP + r = 1.25 eps_EP = {start:.12f} in Gamma=[{GAMMA[0]:.6f},{GAMMA[1]:.6f}]? {yn(g_ok)}")

    # ---- Handoff Jhat2 / Jhat4
    jz = np.load(HANDOFF / "outputs" / "Jhat.npz")
    Jhat2_saved, Jhat4_saved = jz["Jhat2"], jz["Jhat4"]
    strip = gauge_J.run_strip()
    I2 = np.eye(2)
    fro4_saved = float(np.linalg.norm(Jhat4_saved - I2))
    fro4_re = strip["fro_Jhat4_I"]
    fro2sq = float(np.linalg.norm(Jhat2_saved @ Jhat2_saved - I2))
    fro2_I = float(np.linalg.norm(Jhat2_saved - I2))
    P(f"Jhat (handoff outputs/Jhat.npz): ||Jhat4-I||={fro4_saved:.3e} ||Jhat2^2-I||={fro2sq:.3e} ||Jhat2-I||={fro2_I:.3f}")
    P(f"Jhat4 recomputed via handoff gauge_J.run_strip(): ||Jhat4-I||={fro4_re:.3e}")

    # ---- main track around +core, 0 -> 4pi, sheet A first (Gamma-cut labels at start)
    th, z = circle(+EPS_EP, r, turns=2.0, n_per_turn=4000)
    y0 = y_cut_gamma(z[0])
    first = np.array([LAM_EP + 0.5 * y0, LAM_EP - 0.5 * y0])
    T = track(z, first=first)
    ev = T["evals"]
    i2 = int(np.argmin(np.abs(th - 2 * PI)))
    circ_p = circulation(ev, lep[+1])
    # -core loop, same radius, 0 -> 4pi (starts at -0.75 eps_EP, which IS in Gamma)
    thm, zm = circle(-EPS_EP, r, turns=2.0, n_per_turn=4000)
    Tm = track(zm)
    circ_m = circulation(Tm["evals"], lep[-1])
    im2 = int(np.argmin(np.abs(thm - 2 * PI)))
    P("CIRCULATION  d arg(lambda - lambda_EP(core)), sheet0 / sheet1 [units of pi]")
    cp1 = circ_p[i2] / PI; cp2 = circ_p[-1] / PI
    cm1 = circ_m[im2] / PI; cm2 = circ_m[-1] / PI
    P(f"  +core 1 turn: {cp1[0]:+.6f} / {cp1[1]:+.6f}   2 turns: {cp2[0]:+.6f} / {cp2[1]:+.6f}")
    P(f"  -core 1 turn: {cm1[0]:+.6f} / {cm1[1]:+.6f}   2 turns: {cm2[0]:+.6f} / {cm2[1]:+.6f}")
    P(f"  tracking jump ratio (max step / local gap): +core {T['jump_ratio']:.3e}  -core {Tm['jump_ratio']:.3e}")
    half_ok = all(abs(abs(x) - 1.0) < 1e-3 for x in list(cp1) + list(cm1)) and \
        all(abs(abs(x) - 2.0) < 1e-3 for x in list(cp2) + list(cm2))

    # ---- T1..T3
    swap2 = bool(abs(ev[i2, 0] - ev[0, 1]) < abs(ev[i2, 0] - ev[0, 0]))
    back4 = bool(np.max(np.abs(ev[-1] - ev[0])) < 1e-8)
    T1 = swap2 and back4 and fro4_saved < 1e-8 and fro2_I > 0.5
    eps4 = z[-1]
    T2 = abs(eps4.imag) < 1e-9 and abs(eps4 - z[0]) < 1e-9
    T3_same = back4
    dl = ev[-1] - LAM_EP
    T3_crit = bool(in_gamma(eps4.real) and np.all(np.abs(dl.imag) < 1e-9))
    P(f"T1 labels: swapped at 2pi={swap2}, back at 4pi={back4}, Jhat4=I, Jhat2!=I -> {yn(T1)}")
    P(f"T2 eps(4pi)={eps4:.12f}  on real axis -> {yn(T2)}  (in Gamma: {yn(in_gamma(eps4.real))})")
    P(f"T3a lambda(4pi)==lambda(0) -> {yn(T3_same)}   max|diff|={np.max(np.abs(ev[-1]-ev[0])):.2e}")
    P(f"T3b brief criterion (Re eps in Gamma and Im(lambda-lambda_EP)=0) -> {yn(T3_crit)}; lambda(0)-lambda_EP={ev[0]-LAM_EP}")
    # what lambda - lambda_EP looks like on Gamma interior
    wG = np.linalg.eigvals(H_A(0.5 * EPS_EP + 0j)) - LAM_EP
    P(f"   on Gamma (eps=0.5 eps_EP): lambda-lambda_EP = {wG}  (purely imaginary)")

    # ---- T4
    loops = {}
    th1, z1 = circle(+EPS_EP, r, turns=1.0)
    loops["+core only (1 turn, start 1.25 eps_EP)"] = track(z1)
    th1b, z1b = circle(+EPS_EP, r, turns=1.0, theta0=PI)
    loops["+core only (1 turn, start 0.75 eps_EP in Gamma)"] = track(z1b)
    th2, z2 = circle(-EPS_EP, r, turns=1.0)
    loops["-core only (1 turn, start -0.75 eps_EP in Gamma)"] = track(z2)
    s8, z8 = figure_eight()
    T8 = track(z8)
    loops["figure-eight (+core ccw, -core cw, start 0)"] = T8
    thb, zb = circle(0.0, 2.0 * EPS_EP, turns=1.0)
    loops["big loop around both (radius 2 eps_EP, start 2 eps_EP)"] = track(zb)
    reps = [loop_report(k, v) for k, v in loops.items()]
    P("T4 (cuts: " + " ; ".join(CUTS.keys()) + ")")
    for rp in reps:
        cs = "  ".join(f"[{k.split(' ')[0]}: swap={c['swap']} flips={c['flips']}]" for k, c in rp["cuts"].items())
        P(f"  {rp['name']}: tracked swap={rp['tracked_swap']}  {cs}  cut-indep={rp['cut_independent']}  "
          f"end eps={rp['chart']['eps_end']:.6f} on-axis={rp['chart']['on_real_axis']} in-Gamma={rp['chart']['in_Gamma']}  jump={rp['jump_ratio']:.2e}")
    # figure-eight per-lobe circulation, each with its own core's lambda_EP
    nl = 4000
    ev8 = T8["evals"]
    lobe1 = circulation(ev8[: nl + 1], lep[+1])[-1] / PI
    lobe2 = circulation(ev8[nl:], lep[-1])[-1] / PI
    P(f"  figure-eight lobe circulation [pi]: lobe1 (+core, ccw) {lobe1[0]:+.6f}/{lobe1[1]:+.6f}   lobe2 (-core, cw) {lobe2[0]:+.6f}/{lobe2[1]:+.6f}")
    r_by = {rp["name"]: rp for rp in reps}
    all_indep = all(rp["cut_independent"] for rp in reps)
    single_swap = all(rp["tracked_swap"] for k, rp in r_by.items() if "only" in k)
    pair_return = all(not rp["tracked_swap"] and rp["lam_back"] for k, rp in r_by.items() if "figure" in k or "big" in k)
    f8 = r_by["figure-eight (+core ccw, -core cw, start 0)"]
    T4 = single_swap and pair_return and all_indep and f8["chart"]["in_Gamma"]
    P(f"T4: single-core loops swap={single_swap}; figure-eight & big loop return labels+lambda={pair_return}; "
      f"figure-eight ends in Gamma={f8['chart']['in_Gamma']}; cut-independent={all_indep} -> {yn(T4)}")

    # ---- physics checks
    pc = physics_checks()
    P("PHYSICS CHECKS")
    for core, d in pc["cores"].items():
        P(f"  core {core:+.6f}: gap exponent={d['exponent']:.4f}  gap at core={d['gap_at_core']:.2e}  overlap at core={d['overlap_at_core']:.6f}")
        for f, row in zip(pc["fracs"], d["rows"]):
            P(f"     r={f:5.2f} eps_EP  mean|l+-l-|={row['gap_mean']:.6e}  mean overlap={row['overlap_mean']:.6f}")
    P(f"  ||H-H^dag|| on Gamma samples: min={min(pc['herm_norms']):.6f} max={max(pc['herm_norms']):.6f}")
    P(f"  off-diag part of H-H^dag = {pc['offdiag_herm']:.2e};  diag of H-H^dag = {pc['diag_antiherm']}")

    # ---- save tracks
    np.savez(OUT / "tracks.npz", theta=th, eps=z, re_eps=z.real, im_eps=z.imag, lam=ev,
             re_lam=ev.real, im_lam=ev.imag, circ_plus=circ_p, theta_minus=thm, eps_minus=zm,
             lam_minus=Tm["evals"], circ_minus=circ_m, s_fig8=s8, eps_fig8=z8, lam_fig8=ev8,
             eps_EP=EPS_EP, lam_EP=LAM_EP, r=r)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(3, 1, figsize=(8, 9), sharex=True)
        ax[0].plot(th, z.real, label="Re eps"); ax[0].plot(th, z.imag, label="Im eps")
        ax[0].axhline(EPS_EP, ls=":", c="k", lw=0.8, label="eps_EP (edge of Gamma)"); ax[0].legend()
        for k in range(2):
            ax[1].plot(th, ev[:, k].real, label=f"Re lambda sheet{k}")
            ax[2].plot(th, ev[:, k].imag, label=f"Im lambda sheet{k}")
        ax[1].legend(); ax[2].legend(); ax[2].set_xlabel("theta")
        for a in ax:
            for x in (2 * PI, 4 * PI):
                a.axvline(x, c="gray", lw=0.6)
        fig.suptitle("Loop eps = eps_EP + 0.25 eps_EP e^{i theta}, theta 0..4pi")
        fig.tight_layout(); fig.savefig(OUT / "tracks_vs_theta.png", dpi=110)
        png = True
    except Exception as e:  # pragma: no cover
        P("plot skipped:", e); png = False

    # ---- RESULTS.md
    verdict = T4 and half_ok
    L += ["# pairA-vortices-return — RESULTS", "",
          f"Model: handoff `{HANDOFF}` (seed.H_A, 2x2). eps_EP = {EPS_EP:.12f}, lambda_EP = {LAM_EP}.",
          f"lambda_EP evaluated at each core: +core {lep[+1]}, -core {lep[-1]} (identical: tr H_A/2 = -i(a+b)/2 does not depend on eps).",
          f"Gamma (real chart, handoff wick_lorentzian.chart): {GAMMA_STR} = [{GAMMA[0]:.6f}, {GAMMA[1]:.6f}]. C held (not used).", "",
          "## Gamma check for the start point 1.25 eps_EP", "",
          f"eps_EP + r = 1.25 eps_EP = {start:.9f}. Inside Gamma? **{yn(g_ok)}**", ""]
    if not g_ok:
        L += ["**WARNING — THE REQUESTED LOOP DOES NOT START ON THE REAL CHART.** In this handoff Gamma is the segment "
              "[-eps_EP, +eps_EP] between the two tips, so 1.25 eps_EP is on the real axis but OUTSIDE Gamma "
              "(it lies on the real sheets |eps|>eps_EP, where lambda-lambda_EP is real). The handoff's own Jhat loop "
              "(gauge_J.run_strip) uses this same start. To still test a real-chart start, T4 also runs loops starting "
              "at 0.75 eps_EP, -0.75 eps_EP and 0 (all inside Gamma).", "", "Note: " + NOTE_TXT, ""]
    L += ["## Circulation  Δarg(λ − λ_EP(core)), continuous tracking, r = 0.25 eps_EP", "",
          "| core | 1 turn (0→2π) sheet0 / sheet1 | 2 turns (0→4π) sheet0 / sheet1 |", "|---|---|---|",
          f"| +eps_EP | {cp1[0]:+.6f}π / {cp1[1]:+.6f}π | {cp2[0]:+.6f}π / {cp2[1]:+.6f}π |",
          f"| −eps_EP | {cm1[0]:+.6f}π / {cm1[1]:+.6f}π | {cm2[0]:+.6f}π / {cm2[1]:+.6f}π |", "",
          f"Half-turn circulation (π per turn, 2π per two turns) at both cores: **{yn(half_ok)}**. "
          f"Tracking jump ratio (max step / local gap) {T['jump_ratio']:.2e} (+core), {Tm['jump_ratio']:.2e} (−core): no sheet jumps.", "",
          "## Return tests (main loop eps = eps_EP + r e^{iθ}, θ 0→4π, 8001 points)", "",
          f"- **T1** labels back at 4π: **{yn(T1)}** (swap at 2π = {swap2}; back at 4π = {back4}; handoff Jhat.npz ||Jhat4−I|| = {fro4_saved:.2e}, ||Jhat2−I|| = {fro2_I:.3f}, ||Jhat2²−I|| = {fro2sq:.2e}; recomputed ||Jhat4−I|| = {fro4_re:.2e}). Expected; already known.",
          f"- **T2** ε back on real axis at 4π: **{yn(T2)}** (ε(4π) = {eps4.real:.9f}{eps4.imag:+.1e}i). **Passes by construction** — ε is moved by hand and returns to eps_EP + r at 2π and 4π. Says nothing about the vortices. Note: that point is on the real axis but NOT in Gamma.",
          f"- **T3** λ back to its start value at 4π: **{yn(T3_same)}** (max |λ(4π)−λ(0)| = {np.max(np.abs(ev[-1]-ev[0])):.1e}). **Passes by construction**: λ± − λ_EP ≈ ±c√(ε−ε_EP), so two turns return λ — same fact as the known 4π label return. "
          f"Brief's stricter real-chart form (Re ε in Gamma and Im(λ−λ_EP)=0): **{yn(T3_crit)}** — the start ε is outside Gamma. Also note: on Gamma's interior λ−λ_EP is purely IMAGINARY in this model (e.g. ε=0.5 eps_EP: {wG[0]:.6f}, {wG[1]:.6f}); Im(λ−λ_EP)=0 holds on the outer real sheets |ε|>eps_EP, not on Gamma.",
          "  - T3 strict note: " + NOTE_TXT,
          f"- **T4** (the real test): **{yn(T4)}**", "",
          "Branch cuts used for sheet labels (A := λ_EP + y/2, B := λ_EP − y/2, y² = 4v²(ε²−eps_EP²)):",
          "1. Gamma-segment [−eps_EP, +eps_EP] (the handoff cut): y = 2v√(ε−eps_EP)√(ε+eps_EP); points on the cut read on the upper lip ε+i0.",
          "2. Outward rays (−∞,−eps_EP] ∪ [+eps_EP,+∞): y = 2iv√(eps_EP−ε)√(eps_EP+ε).", "",
          "T4 is branch-cut independent: whether labels swap is the monodromy of the continuously tracked path; the cut only sets where the label jump is drawn. The two-cut run is a bug check (both cuts must agree with the tracked swap).", "",
          "| loop | tracked swap | cut 1 swap (flips) | cut 2 swap (flips) | λ back | ends at ε | on real axis | in Gamma |", "|---|---|---|---|---|---|---|---|"]
    for rp in reps:
        c = list(rp["cuts"].values())
        e = rp["chart"]["eps_end"]
        L.append(f"| {rp['name']} | {rp['tracked_swap']} | {c[0]['swap']} ({c[0]['flips']}) | {c[1]['swap']} ({c[1]['flips']}) | {rp['lam_back']} | {e.real:.6f}{e.imag:+.1e}i | {rp['chart']['on_real_axis']} | {rp['chart']['in_Gamma']} |")
    L += ["", f"Figure-eight per-lobe circulation (each lobe with its own core's λ_EP): lobe 1 (+core, anticlockwise) {lobe1[0]:+.6f}π / {lobe1[1]:+.6f}π; lobe 2 (−core, clockwise) {lobe2[0]:+.6f}π / {lobe2[1]:+.6f}π.",
          f"Cut-independence bug check passed for all loops: **{yn(all_indep)}**.", "",
          "## Physics checks", "",
          f"- H_A is {dim}x{dim}: only one eigenvalue pair exists, so the same two sheets (A, B) meet at both cores.",
          "- Gap scaling |λ+ − λ−| (mean over circle) and eigenvector overlap |<v+|v−>|/(|v+||v−|):", "",
          "| core | r/eps_EP | mean gap | mean overlap |", "|---|---|---|---|"]
    for core, d in pc["cores"].items():
        for f, row in zip(pc["fracs"], d["rows"]):
            L.append(f"| {core:+.6f} | {f} | {row['gap_mean']:.6e} | {row['overlap_mean']:.6f} |")
    for core, d in pc["cores"].items():
        L.append(f"\nCore {core:+.6f}: fitted gap exponent **{d['exponent']:.4f}** (EP ⇒ 1/2, ordinary crossing ⇒ 1); at the core gap = {d['gap_at_core']:.1e}, overlap = {d['overlap_at_core']:.6f} (→1: eigenvectors coalesce).")
    L += ["", f"- Hermiticity on the real chart: ||H − H†|| = {min(pc['herm_norms']):.6f} for every sampled real ε in Gamma (constant). "
          f"Off-diagonal part of H − H† = {pc['offdiag_herm']:.1e} (coupling εv is real-symmetric). Diagonal of H − H† = {pc['diag_antiherm'][0]:.5f}, {pc['diag_antiherm'][1]:.5f}: "
          "the non-Hermitian terms are the diagonal −i a, −i b (both loss/damping, unequal rates; no gain). H_A is NOT Hermitian for real ε.", "",
          "## Verdict", "",
          f"**vortices return to real axis: {yn(verdict)}**", ""]
    if verdict:
        L.append("Labels and λ return to their start values after ONE figure-eight pass (one 2π trip), whereas a one-core loop needs 4π. "
                 "ε returning is by construction, since any closed loop ends where it started. "
                 "Mechanism: once around one core swaps the two eigenvalues; the figure-eight's opposite-sense lobes (+π, −π) undo the swap.")
    else:
        L.append("See T4 table and circulation: the conditions (half-turn circulation at each core and a cut-independent return of the two-core loop to Gamma) were not all met.")
    L += ["", SCOPE_TXT]
    if png:
        L += ["", "Plot: outputs/tracks_vs_theta.png (Re/Im ε and Re/Im λ vs θ for the main loop)."]
    (ROOT / "RESULTS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    P("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Probe dictionary D1-D7 (each PASS/FAIL, tagged [by definition] / [by construction] / [computed])."""
from __future__ import annotations

import numpy as np

from pathlib import Path

from load_surface import DRIVE, HANDOFF, LOADED, VORT, grep, y_cut_gamma

EXTERNAL_STALL = [Path(r"C:\Users\Akitt\Grok\MHD\11_hamiltonian_pancake_symplectic.txt"),
                  Path(r"C:\Users\Akitt\Grok\converged\04_MHD_notes.txt")]


def sheets_at(S, eps):
    lam = np.linalg.eigvals(S["H_A"](complex(eps)))
    y = y_cut_gamma(eps, S["EPS_EP"], S["V"])
    lamA = S["LAM_EP"] + 0.5 * y
    if abs(lam[1] - lamA) < abs(lam[0] - lamA):
        lam = lam[::-1]
    return lam  # [A, B]


def winners(npz_path):
    d = np.load(npz_path)
    out = {}
    for k in d.files:
        if k.endswith("_wA"):
            base = k[:-3]
            _, speed, direction, start = base.split("_")
            th, wA, wB = d[base + "_theta"], d[base + "_wA"], d[base + "_wB"]
            i2 = int(np.argmin(np.abs(th - 2 * np.pi)))
            rec = {}
            for m, i in ((1, i2), (2, len(th) - 1)):
                rec[m] = ("A" if wA[i] >= wB[i] else "B", float(max(wA[i], wB[i])))
            out[(speed, direction, start[-1])] = rec
    return out


def chirality(W, speed):
    """per turn m: (ccw winner != cw winner for both start sheets, winners start-independent per direction)."""
    res = {}
    for m in (1, 2):
        diff = all(W[(speed, "ccw", s)][m][0] != W[(speed, "cw", s)][m][0] for s in "AB")
        indep = all(W[(speed, d, "A")][m][0] == W[(speed, d, "B")][m][0] for d in ("ccw", "cw"))
        res[m] = (diff, indep)
    return res


def gap_fit(S, core, fracs=(0.25, 0.1, 0.03, 0.01), n=721):
    E = S["EPS_EP"]
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    g, ovl = [], []
    for f in fracs:
        gg, oo = [], []
        for t in th:
            w, Vm = np.linalg.eig(S["H_A"](core + f * E * np.exp(1j * t)))
            gg.append(abs(w[0] - w[1]))
            oo.append(abs(np.vdot(Vm[:, 0], Vm[:, 1])) / (np.linalg.norm(Vm[:, 0]) * np.linalg.norm(Vm[:, 1])))
        g.append(np.mean(gg)); ovl.append(np.mean(oo))
    expo = float(np.polyfit(np.log(np.array(fracs) * E), np.log(g), 1)[0])
    w, Vm = np.linalg.eig(S["H_A"](complex(core)))
    ov_core = abs(np.vdot(Vm[:, 0], Vm[:, 1])) / (np.linalg.norm(Vm[:, 0]) * np.linalg.norm(Vm[:, 1]))
    return {"exponent": expo, "overlaps": ovl, "fracs": list(fracs), "overlap_core": float(ov_core), "gap_core": float(abs(w[0] - w[1]))}


def build(S, cover_rows, h_before, h_after):
    E = S["EPS_EP"]
    rows = []

    # D1
    cit = grep([HANDOFF], r"real chart only|real_section_support|real_chart_support")
    inside = [sheets_at(S, x) - S["LAM_EP"] for x in np.linspace(-0.95 * E, 0.95 * E, 21)]
    outside = [sheets_at(S, x) - S["LAM_EP"] for x in np.concatenate([np.linspace(1.05 * E, 2 * E, 10), -np.linspace(1.05 * E, 2 * E, 10)])]
    re_in = max(float(np.max(np.abs(v.real))) for v in inside)
    im_out = max(float(np.max(np.abs(v.imag))) for v in outside)
    cits = "; ".join(f"{p.split(chr(92))[-1]}:{i} `{l[:70]}`" for p, i, l in cit)
    rows.append({"id": "D1", "claim": "real chart only on Γ", "result": True, "tag": "[by definition]",
                 "conditions": "'real chart' = the handoff's chart, which the handoff places on Γ = [−ε_EP, ε_EP]",
                 "evidence": f"handoff: {cits}. Computed fact (not hidden): for real ε inside Γ, λ−λ_EP is purely imaginary (max |Re| = {re_in:.1e} over 21 points); "
                             f"outside Γ it is real (max |Im| = {im_out:.1e} over 20 points). Real eigenvalue differences live OUTSIDE Γ; inside Γ the two modes share a frequency and differ in decay."})

    # D2
    gp, gm = gap_fit(S, +E), gap_fit(S, -E)
    ok2 = all(abs(g["exponent"] - 0.5) < 0.02 and g["overlap_core"] > 0.999 and np.all(np.diff(g["overlaps"]) > 0) for g in (gp, gm))
    rows.append({"id": "D2", "claim": "dies at both EPs", "result": ok2, "tag": "[computed]",
                 "conditions": "circles r = 0.25, 0.1, 0.03, 0.01 ε_EP around each EP; gap = mean |λ+−λ−| on the circle; overlap = normalised |<v+|v−>|",
                 "evidence": f"+ε_EP: gap exponent {gp['exponent']:.4f}, overlap {', '.join(f'{o:.4f}' for o in gp['overlaps'])} → {gp['overlap_core']:.6f} at the EP (gap {gp['gap_core']:.1e}); "
                             f"−ε_EP: exponent {gm['exponent']:.4f}, overlap {', '.join(f'{o:.4f}' for o in gm['overlaps'])} → {gm['overlap_core']:.6f} (gap {gm['gap_core']:.1e}). r^(1/2) and merging eigenvectors at both EPs."})

    # D3
    cr = {r["name"].split(" (")[0]: r for r in cover_rows}
    once = [cr["+EP once"], cr["-EP once"]]
    twice = [cr["+EP twice"], cr["-EP twice"]]
    j4 = float(np.linalg.norm(S["Jhat4"] - np.eye(2)))
    j2 = float(np.linalg.norm(S["Jhat2"] - np.eye(2)))
    ok3 = all(r["n_A"] == 1 and r["n_B"] == 1 for r in once) and all(r["n_A"] == 0 and r["n_B"] == 0 for r in twice) and j4 < 1e-10 and j2 > 0.5
    rows.append({"id": "D3", "claim": "4π return of labels", "result": ok3, "tag": "[computed, known]",
                 "conditions": "continuous eigenvalue tracking on circles r = 0.25 ε_EP around each EP (this run); handoff Jhat from outputs/Jhat.npz",
                 "evidence": f"one turn: swap (n=1) at +ε_EP and −ε_EP for A and B; two turns: return (n=0); handoff ‖Jhat4−I‖ = {j4:.1e}, ‖Jhat2−I‖ = {j2:.3f}. Known result (2π swap, 4π return), re-confirmed."})

    # D4 (definition supplied by Akitti, 2026-09-25: stall = both EPs +-eps_EP)
    import stall as ST
    cfiles4 = sorted({p for p, i, l in grep([HANDOFF], r"\bC imaginary|\"C\"|held|NOT-SELECTED")})
    c_ok = all(h_before.get(p) == h_after.get(p) for p in cfiles4) and bool(cfiles4)
    awick = [h for h in grep([HANDOFF], r"allowed_past_Wick") if h[0].endswith("probe.py")]
    d_ok = any(h[1] == 44 and '["A", "B"]' in h[2] for h in awick)
    cr4 = {r["name"].split(" (")[0]: r for r in cover_rows}
    j4 = float(np.linalg.norm(S["Jhat4"] - np.eye(2)))
    j2 = float(np.linalg.norm(S["Jhat2"] - np.eye(2)))
    parts, ev_tips, fails = {}, [], []
    for sg, nm in ((+1, "+ε_EP"), (-1, "−ε_EP")):
        d = ST.detours(S, sg)
        k = "+EP" if sg > 0 else "-EP"
        a_ok = d["swapped"] and abs(d["loop_winding"]) == 1
        b_ok = (cr4[k + " once"]["n_A"] == 1 and cr4[k + " once"]["n_B"] == 1 and cr4[k + " twice"]["n_A"] == 0
                and cr4[k + " twice"]["n_B"] == 0 and j4 < 1e-10 and j2 > 0.5)
        c_tip = c_ok and all(set(d[rt]["land"].values()) == {"higher", "lower"} for rt in ("above", "below"))
        parts[nm] = {"a": a_ok, "b": b_ok, "c": c_tip, "d": d_ok, "detour": d}
        for lab, ok in (("a", a_ok), ("b", b_ok), ("c", c_tip), ("d", d_ok)):
            if not ok:
                fails.append(f"({lab}) at {nm}")
        ab, be = d["above"], d["below"]
        ev_tips.append(
            f"<b>{nm}</b>: (a) start {d['start'].real/E:+.2f} ε_EP (inside Γ) → end {d['end'].real/E:+.2f} ε_EP (outside Γ), semicircle r = 0.25 ε_EP; "
            f"above (Im ε>0): A → {ab['land']['A']}-frequency mode, B → {ab['land']['B']} (labels at the end point: A stays {ab['label_at_end']['A']}, B stays {ab['label_at_end']['B']}); "
            f"below (Im ε<0): A → {be['land']['A']}, B → {be['land']['B']} (A arrives on sheet {be['label_at_end']['A']}, B on sheet {be['label_at_end']['B']}); "
            f"pairings swapped: {'YES' if d['swapped'] else 'NO'}; above ∘ reversed below = one closed loop around the tip (winding {d['loop_winding']:+d}); "
            f"end modes Re λ = {d['hi'].real:+.6f} (higher), {d['lo'].real:+.6f} (lower), |Im(λA−λB)| at end {max(ab['im_gap_end'], be['im_gap_end']):.1e}; "
            f"tracking jump ratio {max(ab['jump_ratio'], be['jump_ratio']):.1e}. "
            f"(b) 2π loop: n_A = {cr4[k+' once']['n_A']}, n_B = {cr4[k+' once']['n_B']} (swap); 4π: n_A = {cr4[k+' twice']['n_A']}, n_B = {cr4[k+' twice']['n_B']} (return). "
            f"(c) only the two sheets A, B of the 2x2 H_A are continued; C files unchanged: {'YES' if c_ok else 'NO'}. (d) probe.py:44 allowed_past_Wick [A, B] cited above: {'YES' if d_ok else 'NO'}.")
    ok4 = not fails
    _sz = np.diag([1.0, -1.0])
    sym_res = max(float(np.linalg.norm(_sz @ S['H_A'](z) @ _sz - S['H_A'](-z))) for z in (0.3 + 0.2j, 1.1 - 0.4j, -0.7 + 0.05j, 0.9 + 0j))
    mg_tip = {nm: min(pt['detour'][rt]['min_gap'] for rt in ('above', 'below')) for nm, pt in parts.items()}
    min_gap4 = min(mg_tip.values())
    if not min_gap4 > 0:
        fails.append('gap closes on a detour'); ok4 = False
    ev4 = (f"Definition (Akitti, {ST.AKITTI_DATE}, verbatim): \"{ST.AKITTI_DEF}\" "
           "Handoff definition source, same fact per Akitti: " + "; ".join(f"{p.split(chr(92))[-1]}:{i} `{l.strip()[:60]}`" for p, i, l in awick) + ". "
           + " ".join(ev_tips).replace("<b>", "").replace("</b>", "") +
           f" Route dependence: the route that stays on the upper lip (above) keeps the start labels (A ends as sheet A, B as sheet B); the route below crosses to the other lip and the labels arrive swapped, "
           f"so which outside-Γ mode A lands on is set by the side of the tip it passes, and the two answers differ by exactly one 2π loop around the tip. "
           f"Handoff ‖Jhat4−I‖ = {j4:.1e}, ‖Jhat2−I‖ = {j2:.3f}. C-related files ({len(cfiles4)}) unchanged: {'YES' if c_ok else 'NO'}."
           + (f" Note (Venus): which pairing counts as 'A continues to A' is a choice set by the cut; the only choice-independent fact is that the two detours disagree by exactly one swap. "
              f"The gap stays open along both detours (they never touch the tip): min |λA−λB| over all four detours = {min_gap4:.6f} (at +ε_EP: {mg_tip['+ε_EP']:.6f}, at −ε_EP: {mg_tip['−ε_EP']:.6f}; > 0), and that is what makes 'allowed past' true.")
           + (f" The results at the two tips mirror each other (going above −ε_EP behaves like going below +ε_EP) because of the ε → −ε symmetry of H_A (σz); expected, not an error "
              f"(computed: max ‖σz H_A(ε) σz − H_A(−ε)‖ = {sym_res:.1e} at 4 complex ε). "
              "Scope [careful-before-toy]: D4 is about the eigenvalue sheets with ε moved by hand. A driven state taken past a tip is covered by D6 and D7, where the direction of travel and the loss decide the outcome, not the sheet label.")
           + (f" FAILED parts: {', '.join(fails)}." if fails else " All parts (a)–(d) pass at both tips."))
    rows.append({"id": "D4", "claim": "A and B allowed past the stall (stall = both EPs ±ε_EP, Akitti 2026-09-25)", "result": ok4,
                 "tag": "[computed, equivalent to 2π swap] (definition supplied by Akitti)",
                 "info": "no (same fact as the one-tip 2π swap, read along an open path)",
                 "conditions": "at each tip: (a) Helios two-detour test, semicircles r = 0.25 ε_EP just above / just below the tip from ±0.75 to ±1.25 ε_EP, continuous tracking (handoff align_evals, 8000 steps), PASS only if the pairings are swapped; "
                               "(b) 2π swap / 4π return from the cover loops and handoff Jhat; (c) only A and B continue, C files unchanged (SHA-256); (d) probe.py:44 allowed_past_Wick [A, B] cited as the same fact",
                 "evidence": ev4, "parts": parts})

    # D5
    cfiles = sorted({p for p, i, l in grep([HANDOFF], r"\bC imaginary|\"C\"|held|NOT-SELECTED")})
    unchanged = all(h_before.get(p) == h_after.get(p) for p in cfiles) and bool(cfiles)
    rows.append({"id": "D5", "claim": "C held", "result": unchanged, "tag": "[by construction]",
                 "conditions": "this probe never writes C or any handoff file; checked by SHA-256 before/after",
                 "evidence": f"C-related handoff files ({len(cfiles)}): " + ", ".join(p.split(chr(92))[-1] for p in cfiles) +
                             f" — unchanged: {'YES' if unchanged else 'NO'}. Handoff status: C imaginary cap NOT-SELECTED, 'held: C' (RESULTS_probe.md)."})

    # D6
    W0 = winners(DRIVE / "outputs" / "drive.npz")
    lam075 = sheets_at(S, 0.75 * E)
    slow_sheet = "AB"[int(np.argmax(lam075.imag))]
    sp0 = sorted({k[0] for k in W0}, key=lambda s: {"fast": 1, "slow20": 20, "slow40": 40, "slow100": 100}.get(s, 0))
    ch0 = {sp: chirality(W0, sp) for sp in sp0}
    ok6 = all(not ch0[sp][m][0] and all(W0[(sp, "ccw", s)][m][0] == W0[(sp, "cw", s)][m][0] for s in "AB") for sp in sp0 for m in (1, 2))
    q6 = grep([DRIVE], r"^\*\*missing mechanism: ")
    sig6 = grep([DRIVE], r"^\W*Signed off")
    ev6 = "; ".join(f"{sp}: " + ", ".join(f"{2*m}π ccw/cw from A → {W0[(sp,'ccw','A')][m][0]}/{W0[(sp,'cw','A')][m][0]}, from B → {W0[(sp,'ccw','B')][m][0]}/{W0[(sp,'cw','B')][m][0]}" for m in (1, 2)) for sp in sp0)
    rows.append({"id": "D6", "claim": "loop starting inside Γ at 0.75ε_EP: the direction of travel is ignored (loss picks the mode)", "result": ok6, "tag": "[computed]",
                 "conditions": "loop r = 0.25 ε_EP around +ε_EP, start/end 0.75 ε_EP (inside Γ), γT = 1, 20, 40, 100; left-eigenvector weights. The loop straddles the tip (it also passes 1.25 ε_EP outside Γ); no driven loop lies entirely inside or outside Γ",
                 "evidence": f"drive-return outputs/drive.npz: {ev6}. Slower-decaying mode at 0.75 ε_EP = sheet {slow_sheet}. "
                             f"RESULTS.md: {q6[0][2] if q6 else '(line not found)'} {('— ' + sig6[0][2]) if sig6 else ''}"})

    # D7
    W1 = winners(DRIVE / "outputs" / "drive_start1p25.npz")
    lam125 = sheets_at(S, 1.25 * E)
    hi = "AB"[int(np.argmax(lam125.real))]
    ch1 = {sp: chirality(W1, sp) for sp in ("fast", "mid5", "slow20", "slow40", "slow100")}
    ok7 = all(ch1[sp][m][0] and ch1[sp][m][1] for sp in ("slow20", "slow40", "slow100") for m in (1, 2))
    q7 = grep([DRIVE], r"^\*\*missing mechanism \(start 1\.25")
    sig7 = [h for h in grep([DRIVE], r"^\W*Signed off") if "start1p25" in h[0]]

    def desc(sp):
        return ", ".join(f"{2*m}π ccw → {W1[(sp,'ccw','A')][m][0]}/{W1[(sp,'ccw','B')][m][0]} (w {W1[(sp,'ccw','A')][m][1]:.5f}), cw → {W1[(sp,'cw','A')][m][0]}/{W1[(sp,'cw','B')][m][0]}" for m in (1, 2))
    ev7 = "; ".join(f"{sp}: {desc(sp)} [direction-dependent: {'YES' if ch1[sp][2][0] else 'NO'}]" for sp in ch1)
    rows.append({"id": "D7", "claim": "loop starting outside Γ at 1.25ε_EP, slow drive (γT≳20): the direction picks the mode (cw and ccw pick opposite modes)", "result": ok7, "tag": "[computed]",
                 "conditions": "r = 0.25 ε_EP, start/end 1.25 ε_EP (outside Γ), slow drive: the direction picks the mode cleanly from about γT ≈ 20 (w = 0.99699 at γT = 20, 0.99937 at 40, 0.99991 at 100), only partially at γT = 5 (a lean of about 91/9), and not at γT = 1. The loop straddles the tip (it crosses Γ at 0.75 ε_EP); no driven loop lies entirely inside or outside Γ",
                 "evidence": f"drive-return outputs/drive_start1p25.npz (winners from start A/B): {ev7}. Higher-frequency mode at 1.25 ε_EP = sheet {hi}. "
                             f"RESULTS_start1p25.md: {q7[0][2] if q7 else '(line not found)'} {('— ' + sig7[0][2]) if sig7 else ''}"})
    return rows

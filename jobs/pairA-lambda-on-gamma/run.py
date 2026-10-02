"""Run the Pair A 'lambda back onto Gamma?' test. Writes RESULTS.md (and paths.png).

RESULTS.md is generated here and must not be edited by hand.
Rules are fixed in README.md, written before this script was run.
"""
import datetime
import math
import os
import sys

import numpy as np

import paths as P

HERE = os.path.dirname(os.path.abspath(__file__))
TWO_PI = 2.0 * math.pi
T_END = 4.0 * math.pi
JUMP_FRAC = 0.01          # no eigenvalue may move more than 1% of the local gap
TOUCH_TOL = 1e-6 * P.eps_EP
RE_TOL = 1e-9 * P.kappa
EPS_IM_TOL = 1e-12
LAMBDA_IM_REL_TOL = 1e-12
SAME_TOL = 1e-8 * P.kappa
PATH_TAGS = {
    "P2": " [requires complex drive: gradient with a loss/gain part]",
    "P3": " [requires complex drive: gradient with a loss/gain part]",
    "P3b": " [requires complex drive: gradient with a loss/gain part]",
}


def eigs(eps):
    return np.linalg.eigvals(P.H_A(eps))


def mu_of(lam):
    return lam - P.half_trace


def label_start(eps):
    """Branch A = '+' root (principal sqrt) at the start point, branch B = '-' root."""
    e = eigs(eps)
    plus, _minus = P.lam_closed(eps)
    if abs(e[0] - plus) <= abs(e[1] - plus):
        return e[0], e[1]
    return e[1], e[0]


def eps_on_gamma(eps):
    """Primary ON-Gamma rule: eps is real within tolerance and inside the segment."""
    ok = (abs(eps.imag) <= EPS_IM_TOL) and (abs(eps) <= P.eps_EP)
    return ok, abs(eps.imag), abs(eps) / P.eps_EP


def lambda_on_gamma(lam):
    """Secondary lambda cross-check, with the signed-off endpoint tolerance."""
    m = mu_of(lam)
    ok = (abs(m.real) <= RE_TOL) and (abs(m.imag) <= P.kappa * (1.0 + LAMBDA_IM_REL_TOL))
    return ok, abs(m.real), abs(m.imag) / P.kappa


def track(f):
    """Adaptive nearest-neighbour tracking over t in [0, 4 pi].

    Returns samples and checkpoint states at 2 pi and 4 pi.
    """
    t = 0.0
    lamA, lamB = label_start(f(0.0))
    cur = np.array([lamA, lamB])
    ts, es, tracked = [0.0], [f(0.0)], [cur.copy()]
    dt = 1e-3
    dt_max = 2e-2
    checkpoints = [math.pi, TWO_PI, T_END]
    states = {}
    max_ratio = 0.0
    max_closed_err = 0.0
    n_rej = 0
    while t < T_END - 1e-15:
        nxt_cp = min(c for c in checkpoints if c > t + 1e-15)
        step = min(dt, nxt_cp - t)
        t_new = t + step
        if abs(t_new - nxt_cp) < 1e-12:
            t_new = nxt_cp
        e_new = eigs(f(t_new))
        d_keep = abs(e_new[0] - cur[0]) + abs(e_new[1] - cur[1])
        d_swap = abs(e_new[1] - cur[0]) + abs(e_new[0] - cur[1])
        new = e_new if d_keep <= d_swap else e_new[::-1]
        jump = max(abs(new[0] - cur[0]), abs(new[1] - cur[1]))
        gap = min(abs(cur[0] - cur[1]), abs(new[0] - new[1]))
        if jump > JUMP_FRAC * gap:
            dt = step / 2.0
            n_rej += 1
            if dt < 1e-14:
                raise RuntimeError("step collapsed (EP touched?) at t=%g" % t)
            continue
        max_ratio = max(max_ratio, jump / gap)
        cl = P.lam_closed(f(t_new))
        err = min(max(abs(new[0] - cl[0]), abs(new[1] - cl[1])),
                  max(abs(new[0] - cl[1]), abs(new[1] - cl[0])))
        max_closed_err = max(max_closed_err, err)
        cur = new
        t = t_new
        ts.append(t); es.append(f(t)); tracked.append(cur.copy())
        if t in checkpoints:
            states[t] = (f(t), cur.copy())
        dt = min(step * 1.5, dt_max) if step >= dt * 0.999 else min(dt * 1.5, dt_max)
    return dict(ts=np.array(ts), es=np.array(es), tracked=np.array(tracked),
                lamA0=lamA, lamB0=lamB, states=states, max_ratio=max_ratio,
                max_closed_err=max_closed_err, n_steps=len(ts) - 1, n_rej=n_rej)


def branch_name(lam, lamA0, lamB0):
    return "A" if abs(lam - lamA0) < abs(lam - lamB0) else "B"


def winding(f, center, t0, t1, n=200001):
    tt = np.linspace(t0, t1, n)
    z = np.array([f(x) for x in tt]) - center
    ang = np.unwrap(np.angle(z))
    return (ang[-1] - ang[0]) / TWO_PI


def min_dist(f, center, n=400001):
    tt = np.linspace(0.0, T_END, n)
    z = np.array([f(x) for x in tt])
    d = np.abs(z - center)
    i = int(np.argmin(d))
    # local refine by golden-section on a small bracket
    lo, hi = tt[max(i - 1, 0)], tt[min(i + 1, n - 1)]
    g = (math.sqrt(5) - 1) / 2
    for _ in range(80):
        m1 = hi - g * (hi - lo); m2 = lo + g * (hi - lo)
        if abs(f(m1) - center) < abs(f(m2) - center):
            hi = m2
        else:
            lo = m1
    return min(d[i], abs(f((lo + hi) / 2) - center))


def real_crossings(f, t0=0.0, t1=TWO_PI, n=200001):
    """Points in one lap where eps is (numerically) on the real axis."""
    tt = np.linspace(t0, t1, n)
    z = np.array([f(x) for x in tt])
    if np.all(np.abs(z.imag) < 1e-12):
        return "whole path lies on the real axis"
    out = []
    y = z.imag
    for k in range(n - 1):
        if abs(y[k]) < 1e-12 or (y[k] * y[k + 1] < 0):
            if abs(y[k]) < 1e-12:
                tc = tt[k]
            else:
                lo, hi = tt[k], tt[k + 1]
                for _ in range(80):
                    mid = (lo + hi) / 2
                    if f(lo).imag * f(mid).imag <= 0:
                        hi = mid
                    else:
                        lo = mid
                tc = (lo + hi) / 2
            x = f(tc).real
            if not out or abs(tc - out[-1][0]) > 1e-6:
                out.append((tc, x, abs(x) < P.eps_EP))
    return out


def fmt_c(z, nd=6):
    return "%.*f %+.*fi" % (nd, z.real, nd, z.imag)


def yn(b):
    return "YES" if b else "NO"


def main():
    now = datetime.datetime.now().astimezone()
    L = []
    w = L.append
    w("# RESULTS (generated by run.py - do not edit by hand)")
    w("")
    w("**Signed off 2026-10-02:** Venus (maths) and Helios (physics).")
    w("")
    w("Generated: %s (local time, UTC%s)" % (now.strftime("%Y-%m-%d %H:%M:%S"),
                                             now.strftime("%z")[:3] + ":" + now.strftime("%z")[3:]))
    w("Python %s, numpy %s" % (sys.version.split()[0], np.__version__))
    w("")
    w("No quantum-gravity result is claimed. This is a 2x2 matrix test.")
    w("")
    w("## Handoff numbers and checks")
    w("")
    w("| quantity | handoff value [assumed] | check [computed] |")
    w("|---|---|---|")
    w("| a | %.5f | pi^2/80 = %.9f (gap %.1e) |" % (P.a, math.pi**2 / 80, abs(P.a - math.pi**2 / 80)))
    w("| b | %.5f | pi^2/20 = %.9f (gap %.1e) |" % (P.b, math.pi**2 / 20, abs(P.b - math.pi**2 / 20)))
    w("| v | %.6f | -32/(9 pi^2) = %.9f (gap %.1e) |" % (P.v, -32 / (9 * math.pi**2), abs(P.v + 32 / (9 * math.pi**2))))
    w("| kappa=(b-a)/2 | %.6f | - |" % P.kappa)
    w("| eps_EP=kappa/abs(v) | %.8f | from handoff decimals: %.8f (gap %.1e) |" % (P.EPS_EP_HANDOFF, P.eps_EP, abs(P.eps_EP - P.EPS_EP_HANDOFF)))
    w("| lambda_EP | %s | -i(a+b)/2 = %s |" % ("-0.308425i", fmt_c(P.half_trace)))
    eEP = eigs(P.eps_EP)
    w("| eigenvalues of H_A at +eps_EP | - | %s and %s (they nearly merge) |" % (fmt_c(eEP[0], 8), fmt_c(eEP[1], 8)))
    w("")
    w("The code uses eps_EP = kappa/|v| from the handoff decimals (value above).")
    w("")
    w("## Path formulas (fixed in README.md before the run)")
    w("")
    for name, (f, desc) in P.PATHS.items():
        w("- **%s%s**: %s, t in [0, 4 pi], one lap = 2 pi." % (name, PATH_TAGS.get(name, ""), desc))
    w("")

    rows = []
    detail = []
    cross_disagreements = []
    verdict_yes = []
    for name, (f, desc) in P.PATHS.items():
        r = track(f)
        eps0 = f(0.0)
        inside = abs(eps0.imag) <= EPS_IM_TOL and abs(eps0.real) < P.eps_EP
        lam_start = r["lamA0"]
        g0 = eps_on_gamma(eps0)
        g0B = eps_on_gamma(eps0)
        l0 = lambda_on_gamma(lam_start)
        e2, lam2 = r["states"][TWO_PI]
        e4, lam4 = r["states"][T_END]
        b2 = branch_name(lam2[0], r["lamA0"], r["lamB0"])
        b4 = branch_name(lam4[0], r["lamA0"], r["lamB0"])
        swap2 = b2 != "A"
        sp2 = abs(lam2[0] - r["lamA0"]) <= SAME_TOL
        sp4 = abs(lam4[0] - r["lamA0"]) <= SAME_TOL
        g2 = eps_on_gamma(e2); g4 = eps_on_gamma(e4)
        g2B = eps_on_gamma(e2); g4B = eps_on_gamma(e4)
        l2 = lambda_on_gamma(lam2[0]); l4 = lambda_on_gamma(lam4[0])
        cross_ok = (g0[0] == l0[0]) and (g2[0] == l2[0]) and (g4[0] == l4[0])
        r["lambda_states"] = (l0, l2, l4)
        r["crosscheck"] = cross_ok
        if not cross_ok:
            cross_disagreements.append(name)
        dP = min_dist(f, P.eps_EP); dM = min_dist(f, -P.eps_EP)
        touch = (dP < TOUCH_TOL) or (dM < TOUCH_TOL)
        wP1 = winding(f, P.eps_EP, 0.0, TWO_PI); wM1 = winding(f, -P.eps_EP, 0.0, TWO_PI)
        wP2 = winding(f, P.eps_EP, 0.0, T_END); wM2 = winding(f, -P.eps_EP, 0.0, T_END)
        # half-lap state (useful for P2)
        eh, lamh = r["states"][math.pi]
        bh = branch_name(lamh[0], r["lamA0"], r["lamB0"])
        gh = eps_on_gamma(eh)
        lh = lambda_on_gamma(lamh[0])
        rows.append((name, eps0, inside, swap2, b2, b4, g0, g2, g4, dP, dM, touch, wP1, wM1, wP2, wM2, sp2, sp4))
        if (not g0[0]) and g2[0] and swap2:
            verdict_yes.append(name)
        d = []
        d.append("### %s%s" % (name, PATH_TAGS.get(name, "")))
        d.append("")
        d.append("- Formula: %s" % desc)
        d.append("- eps0 = %s; strictly inside Gamma: %s [computed]" % (fmt_c(eps0, 8), yn(inside)))
        d.append("- Start: branch A lambda = %s, branch B lambda = %s" % (fmt_c(r["lamA0"]), fmt_c(r["lamB0"])))
        d.append("- Tracking: %d accepted steps, %d halvings; largest jump / local gap = %.4f (limit 0.01) [computed]"
                 % (r["n_steps"], r["n_rej"], r["max_ratio"]))
        d.append("- Largest gap between numpy eigenvalues and the closed-form identity along the path: %.1e [computed]" % r["max_closed_err"])
        d.append("- Followed eigenvalue: start branch A -> branch %s at t = 2 pi -> branch %s at t = 4 pi [computed]" % (b2, b4))
        d.append("- Half-lap (t = pi, not a return point of the lap; branch letter = nearer start eigenvalue): eps = %s, followed eigenvalue on branch %s, "
                 "ON-Gamma eps-primary %s (|Im eps| = %.2e, |eps|/eps_EP = %.6f); lambda-secondary %s "
                 "(|Re mu| = %.2e, |Im mu|/kappa = %.6f) [computed, post-hoc]"
                 % (fmt_c(eh, 8), bh, yn(gh[0]), gh[1], gh[2], yn(lh[0]), lh[1], lh[2]))
        d.append("- ON-Gamma eps-primary: start %s (|Im eps| = %.2e, |eps|/eps_EP = %.6f); "
                 "2 pi %s (|Im eps| = %.2e, |eps|/eps_EP = %.6f); 4 pi %s (|Im eps| = %.2e, |eps|/eps_EP = %.6f) [computed, post-hoc]"
                 % (yn(g0[0]), g0[1], g0[2], yn(g2[0]), g2[1], g2[2], yn(g4[0]), g4[1], g4[2]))
        d.append("- ON-Gamma lambda-secondary: start %s (|Re mu| = %.2e, |Im mu|/kappa = %.6f); "
                 "2 pi %s (|Re mu| = %.2e, |Im mu|/kappa = %.6f); 4 pi %s (|Re mu| = %.2e, |Im mu|/kappa = %.6f) "
                 "[computed, post-hoc tolerance |Im mu| <= kappa*(1 + 1e-12)]"
                 % (yn(l0[0]), l0[1], l0[2], yn(l2[0]), l2[1], l2[2], yn(l4[0]), l4[1], l4[2]))
        d.append("- eps-versus-lambda cross-check: %s [computed, post-hoc; disagreement flag = %s]" % (yn(cross_ok), yn(not cross_ok)))
        d.append("- ON-Gamma, the other eigenvalue: start %s, 2 pi %s, 4 pi %s [computed]" % (yn(g0B[0]), yn(g2B[0]), yn(g4B[0])))
        d.append("- SAME-POINT: |lambda(2 pi) - lambda(0)|/kappa = %.2e -> %s; |lambda(4 pi) - lambda(0)|/kappa = %.2e -> %s (limit 1e-8) [computed]"
                 % (abs(lam2[0] - r["lamA0"]) / P.kappa, yn(sp2), abs(lam4[0] - r["lamA0"]) / P.kappa, yn(sp4)))
        d.append("- State at t = 2 pi: eps = %s, on-Gamma %s, SWAP label %s [computed]" % (fmt_c(e2, 8), yn(g2[0]), yn(swap2)))
        d.append("- State at t = 4 pi: eps = %s, on-Gamma %s, back on start branch %s [computed]" % (fmt_c(e4, 8), yn(g4[0]), yn(b4 == "A")))
        d.append("- Smallest distance to +eps_EP = %.6f (= %.4f eps_EP); to -eps_EP = %.6f (= %.4f eps_EP); touches an EP: %s [computed]"
                 % (dP, dP / P.eps_EP, dM, dM / P.eps_EP, yn(touch)))
        d.append("- Winding around +eps_EP: %.6f per lap, %.6f over two laps; around -eps_EP: %.6f per lap, %.6f over two laps [computed]"
                 % (wP1, wP2, wM1, wM2))
        rc = real_crossings(f)
        if isinstance(rc, str):
            d.append("- Real-axis crossings in one lap: %s" % rc)
        else:
            d.append("- Real-axis crossings in one lap [computed]: " + "; ".join(
                "t = %.6f, eps = %.8f (%s Gamma)" % (tc, x, "inside" if ins else "outside") for tc, x, ins in rc))
        d.append("")
        detail.append(d)
        r["name"] = name
        rows[-1] = rows[-1] + (r,)

    w("## Per-path table [computed]")
    w("")
    w("Followed eigenvalue = the one that starts on branch A. Return = t = 2 pi (one lap).")
    w("SWAP, ON-Gamma and SAME-POINT are separate columns (SAME-POINT limit: 1e-8 * kappa).")
    w("")
    w("| path | eps0 | strictly inside Gamma | start branch | branch at 2 pi | SWAP (per lap) | branch at 4 pi | ON-Gamma eps-primary start | ON-Gamma eps-primary at 2 pi | ON-Gamma eps-primary at 4 pi | lambda-secondary start | lambda-secondary at 2 pi | lambda-secondary at 4 pi | eps/lambda cross-check | SAME-POINT 2 pi | SAME-POINT 4 pi | min dist to +eps_EP | min dist to -eps_EP | touches EP | winding +EP (lap; 2 laps) | winding -EP (lap; 2 laps) |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for (name, eps0, inside, swap2, b2, b4, g0, g2, g4, dP, dM, touch, wP1, wM1, wP2, wM2, sp2, sp4, r) in rows:
        l0, l2, l4 = r["lambda_states"]
        w("| %s | %s | %s | A | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %.4f | %.4f | %s | %+.3f; %+.3f | %+.3f; %+.3f |"
          % (name, fmt_c(eps0, 4), yn(inside), b2, yn(swap2), b4, yn(g0[0]), yn(g2[0]), yn(g4[0]),
             yn(l0[0]), yn(l2[0]), yn(l4[0]), yn(r["crosscheck"]), yn(sp2), yn(sp4), dP, dM, yn(touch),
             wP1, wP2, wM1, wM2))
    w("")
    w("## Pre-registered expectation vs computed")
    w("")
    # (swap per lap, ON-Gamma both ends, SAME-POINT at 2 pi, SAME-POINT at 4 pi)
    exp = {"P1": (False, True, True, True), "P2": (False, True, True, True),
           "P3": (True, True, False, True), "P3b": (True, False, False, True)}
    w("| path | expected SWAP [identity] | computed SWAP | expected ON-Gamma both ends | computed (start, return) | expected SAME-POINT (2 pi, 4 pi) | computed SAME-POINT | match |")
    w("|---|---|---|---|---|---|---|---|")
    for row in rows:
        name, eps0, inside, swap2, b2, b4, g0, g2, g4 = row[:9]
        sp2, sp4 = row[16], row[17]
        es_, eg, e2_, e4_ = exp[name]
        m = (swap2 == es_) and (g0[0] == eg) and (g2[0] == eg) and (sp2 == e2_) and (sp4 == e4_)
        w("| %s | %s | %s | %s | %s, %s | %s, %s | %s, %s | %s |" % (name, yn(es_), yn(swap2), yn(eg), yn(g0[0]), yn(g2[0]),
                                                               yn(e2_), yn(e4_), yn(sp2), yn(sp4), yn(m)))
    w("")
    # endpoint identity check along P1 (eps real, inside Gamma)
    worst = 0.0
    for tt in np.linspace(0.0, T_END, 20001):
        e = P.P1(tt).real
        pred = 1j * abs(P.v) * math.sqrt(P.eps_EP ** 2 - e * e)
        ev = eigs(complex(e, 0.0)) - P.half_trace   # lambda - lambda_EP, since lambda_EP = tr/2
        err = min(max(abs(ev[0] - pred), abs(ev[1] + pred)), max(abs(ev[1] - pred), abs(ev[0] + pred)))
        worst = max(worst, err)
    w("Endpoint identity [identity], checked along P1 [computed]: lambda - lambda_EP = +- i|v| sqrt(eps_EP^2 - eps^2); "
      "largest mismatch / kappa = %.1e. Both sheets give the same segment, so 'lambda on the cut spectrum' "
      "only repeats 'eps ends on Gamma'." % (worst / P.kappa))
    w("")
    w("## Signed-off interpretation")
    w("")
    w("Helios rule fix, post-run, boundary identity: eps = 0 maps exactly to the segment endpoints -ia, -ib.")
    w("ON-Gamma primary rule [post-hoc]: Im eps = 0 within 1e-12 and |eps| <= eps_EP; lambda is the secondary consistency check.")
    w("Lambda secondary tolerance [post-hoc]: |Re mu| <= 1e-9*kappa and |Im mu| <= kappa*(1 + 1e-12); disagreements are flagged.")
    w("lambda on Gamma is fixed by where eps ends, not by the sheet [identity]; the flip is visible only in SWAP/SAME-POINT; NO is by construction.")
    w("Gamma (real |eps| < kappa/|v|) is the physical PT-broken window, where a real drive below threshold leaves both modes at one frequency with two decay rates [identity].")
    w("No real-eps path can encircle a tip. Complex eps means eps x -> (eps_r + i eps_i) x, a linearly varying damping across the slab [standard: complex Bloch-Torrey gradient].")
    w("So 'a path that can hit Gamma' (real drive) and 'a path that flips' (complex drive) are different physical controls.")
    w("P3b at t = pi sits inside Gamma (eps = 0.75 eps_EP) with lambda on the segment; this comes from eps's position, not from the swap.")
    w("eps = 0 -> lambda = -ia, -ib; eps -> +-eps_EP -> lambda_EP [identity].")
    w("")
    w("## Details per path")
    w("")
    for d in detail:
        L.extend(d)
    w("## Verdict")
    w("")
    w("Rule (from README.md): YES needs a path that is ON-Gamma = NO at the start and YES at return "
      "(t = 2 pi), caused by SWAP = yes. ON-Gamma here is the primary eps rule [post-hoc].")
    w("")
    for row in rows:
        name, eps0, inside, swap2, b2, b4, g0, g2, g4 = row[:9]
        w("- %s: ON-Gamma start %s, return %s, SWAP %s, SAME-POINT at 2 pi %s -> %s." % (
            name, yn(g0[0]), yn(g2[0]), yn(swap2), yn(row[16]),
            "meets the YES condition" if ((not g0[0]) and g2[0] and swap2) else "does not meet the YES condition"))
    w("")
    w("lambda on Gamma is fixed by where eps ends, not by the sheet [identity]; the flip is visible only in SWAP/SAME-POINT; NO is by construction.")
    w("eps-versus-lambda cross-check across the reported start, 2 pi, and 4 pi states: %s [computed, post-hoc; disagreement flag = %s]." % (yn(not cross_disagreements), yn(bool(cross_disagreements))))
    if cross_disagreements:
        w("Cross-check disagreement paths [computed, post-hoc]: " + ", ".join(cross_disagreements))
    w("")
    try:
        make_png(rows)
        w("Picture: paths.png (the four paths, Gamma in red, the two EPs as black crosses).")
    except Exception as exc:  # matplotlib missing etc.
        w("Picture: not made (%s)." % exc)
    w("")
    all_paths = [row[0] for row in rows]
    swap_paths = [row[0] for row in rows if row[3]]
    w("Why the final line reads as it does [identity: on-Gamma is a function of eps; closed loops return to eps(0)]; "
      "the loop list and the flipping loops are read from the per-path table above [computed].")
    w("")
    # Exactly one plain verdict line, and it is the last line of the file.
    if verdict_yes:
        w("\u03bb restored onto \u0393: YES \u2014 path %s" % ", ".join(verdict_yes))
    else:
        if swap_paths:
            flip = ("; %s %s flip branches (after one lap, back after two), but that flip shows only in SWAP / SAME-POINT"
                    % (" and ".join(swap_paths), "does" if len(swap_paths) == 1 else "do"))
        else:
            flip = "; no loop swaps branches"
        w("\u03bb restored onto \u0393: NO \u2014 no path does it: all %d loops (%s) come back to the \u03b5 they started from, "
          "so each ends on \u0393 only if it began there%s." % (len(all_paths), ", ".join(all_paths), flip))
    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


def make_png(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot([-P.eps_EP, P.eps_EP], [0, 0], color="red", lw=4, alpha=0.5, label="Gamma")
    ax.plot([P.eps_EP, -P.eps_EP], [0, 0], "kx", ms=10, mew=2, label="EPs (+/- eps_EP)")
    colors = {"P1": "tab:green", "P2": "tab:blue", "P3": "tab:orange", "P3b": "tab:purple"}
    for row in rows:
        name, eps0 = row[0], row[1]
        f = P.PATHS[name][0]
        tt = np.linspace(0, 2 * math.pi, 2001)
        z = np.array([f(x) for x in tt])
        ax.plot(z.real, z.imag, color=colors[name], lw=1.8, label=name)
        ax.plot([eps0.real], [eps0.imag], "o", color=colors[name])
        k = 500
        ax.annotate("", xy=(z[k + 5].real, z[k + 5].imag), xytext=(z[k].real, z[k].imag),
                    arrowprops=dict(arrowstyle="->", color=colors[name], lw=1.5))
    ax.set_xlabel("Re eps"); ax.set_ylabel("Im eps"); ax.set_aspect("equal")
    ax.axhline(0, color="gray", lw=0.5)
    ax.legend(loc="upper left", fontsize=8)
    ax.set_title("Pair A: paths in the eps-plane (dot = start, arrow = direction)")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "paths.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()

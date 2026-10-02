"""D4 test (Akitti's definition 2026-09-25: stall = both EPs +-eps_EP).
Helios's two-detour test at each tip: start on real eps inside Gamma near the tip with sheets A/B labelled
(A = lam_EP + y/2, B = lam_EP - y/2, upper-lip convention), continue along a semicircle of radius r around the tip
just above (Im eps > 0) and just below (Im eps < 0) to real eps outside Gamma, tracking eigenvalues continuously."""
from __future__ import annotations

import numpy as np

from load_surface import y_cut_gamma

N = 8000
AKITTI_DEF = ("stall = both EPs (±ε_EP). Real / Wick / Lorentzian chart dies there. D4 test: A and B are the two sheets that "
              "continue past those tips (labels swap on a 2π loop around a tip, return at 4π). C stays held. "
              "Use allowed_past_Wick: [A,B] as the same fact.")
AKITTI_DATE = "2026-09-25"


def labelled(S, eps):
    y = y_cut_gamma(eps, S["EPS_EP"], S["V"])
    return np.array([S["LAM_EP"] + 0.5 * y, S["LAM_EP"] - 0.5 * y])  # [A, B]


def track(S, z):
    H, align = S["H_A"], S["align_evals"]
    ev = align(labelled(S, z[0]), np.linalg.eigvals(H(complex(z[0]))))
    start = ev.copy()
    maxstep, mingap = 0.0, np.inf
    for zi in z[1:]:
        new = align(ev, np.linalg.eigvals(H(complex(zi))))
        maxstep = max(maxstep, float(np.max(np.abs(new - ev))))
        mingap = min(mingap, float(abs(new[0] - new[1])))
        ev = new
    return start, ev, maxstep / mingap, mingap


def detours(S, tip_sign: int, frac_in: float = 0.75, frac_out: float = 1.25):
    E = S["EPS_EP"]
    p = tip_sign * E
    r = (frac_out - 1.0) * E
    assert abs((1.0 - frac_in) * E - r) < 1e-12
    # angle of the start point (inside Gamma) and end point (outside) about the tip
    th0 = np.pi if tip_sign > 0 else 0.0
    th1 = 0.0 if tip_sign > 0 else np.pi
    s = np.linspace(0.0, 1.0, N + 1)
    # above: Im > 0 along the way; below: Im < 0
    if tip_sign > 0:
        th_above = th0 + (th1 - th0) * s            # pi -> 0 through pi/2
        th_below = th0 + (2 * np.pi - th0) * s      # pi -> 2pi through 3pi/2
    else:
        th_above = th0 + (np.pi - th0) * s          # 0 -> pi through pi/2
        th_below = th0 - np.pi * s                  # 0 -> -pi through -pi/2
    out = {"tip": p, "start": p + r * np.exp(1j * th0), "end": p + r * np.exp(1j * th1)}
    lam_end = np.linalg.eigvals(S["H_A"](complex(out["end"])))
    hi, lo = lam_end[np.argmax(lam_end.real)], lam_end[np.argmin(lam_end.real)]
    lab_end = labelled(S, out["end"])  # sheet labels at the end point (y_cut_gamma, analytic off Gamma)
    for name, th in (("above", th_above), ("below", th_below)):
        z = p + r * np.exp(1j * th)
        assert (np.all(z[1:-1].imag > 0) if name == "above" else np.all(z[1:-1].imag < 0))
        st, en, jr, mg = track(S, z)
        land = {}
        for j, lab in enumerate("AB"):
            land[lab] = "higher" if abs(en[j] - hi) < abs(en[j] - lo) else "lower"
        keep = {lab: ("A" if abs(en[j] - lab_end[0]) < abs(en[j] - lab_end[1]) else "B") for j, lab in enumerate("AB")}
        out[name] = {"land": land, "label_at_end": keep, "jump_ratio": jr, "min_gap": mg,
                     "end_vals": en, "im_gap_end": float(abs((en[0] - en[1]).imag))}
    out["hi"], out["lo"] = hi, lo
    distinct = out["above"]["land"]["A"] != out["above"]["land"]["B"] and out["below"]["land"]["A"] != out["below"]["land"]["B"]
    out["swapped"] = distinct and all(out["above"]["land"][k] != out["below"]["land"][k] for k in "AB")
    # above followed by reversed below = one closed loop around the tip
    z_loop = np.concatenate([p + r * np.exp(1j * th_above), (p + r * np.exp(1j * th_below))[::-1][1:]])
    ang = np.unwrap(np.angle(z_loop - p))
    out["loop_winding"] = int(round((ang[-1] - ang[0]) / (2 * np.pi)))
    return out

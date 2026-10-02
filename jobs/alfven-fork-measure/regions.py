"""
Split the tracked fork into EP window / mid-arm 1-D locus / junction leftover.
No third prong: leftover is recorded empty of a prong, not histogrammed as one.

N>2: EP window is data-driven (min gap of tracked pair). Not gated on Pair A λ_EP.
"""

from __future__ import annotations

import numpy as np


def track_two_lowest_damped(evals: np.ndarray, spurious: np.ndarray) -> np.ndarray:
    """
    evals: (n_eps, N) complex.
    At each ε, among non-spurious modes, take the two with largest Im
    (least damped; Im < 0). Match across ε by nearest neighbour.
    Returns branches: (n_eps, 2).
    """
    n_eps, N = evals.shape
    branches = np.full((n_eps, 2), np.nan + 1j * np.nan)
    for i in range(n_eps):
        w = evals[i]
        ok = np.isfinite(w) & (~spurious[i])
        cand = w[ok]
        if cand.size < 2:
            continue
        order = np.argsort(-cand.imag)
        pair = cand[order[:2]]
        if i == 0:
            pair = pair[np.argsort(pair.real)]
        else:
            prev = branches[i - 1]
            # assign to minimise |z - prev|
            d00 = abs(pair[0] - prev[0]) + abs(pair[1] - prev[1])
            d01 = abs(pair[0] - prev[1]) + abs(pair[1] - prev[0])
            if d01 < d00:
                pair = pair[::-1]
        branches[i] = pair
    return branches


def opening_metric(branches: np.ndarray) -> dict:
    """ε-opening: Re split of the two branches. Vertical Im stack only → no fork."""
    re_split = np.abs(branches[:, 0].real - branches[:, 1].real)
    im_split = np.abs(branches[:, 0].imag - branches[:, 1].imag)
    gap = np.abs(branches[:, 0] - branches[:, 1])
    return {
        "re_split": re_split,
        "im_split": im_split,
        "gap": gap,
        "max_re_split": float(np.nanmax(re_split)),
        "has_fork": bool(np.nanmax(re_split) > 0.05),
    }


def split_regions(eps: np.ndarray, branches: np.ndarray) -> dict:
    """
    EP window: neighbourhood of data-driven min-gap ε*.
    mid-arm: opened branches outside that window, 1-D in ε.
    junction: leftover (no third prong; sample empty by construction
    if every selected point is on the two tracked branches).
    """
    gap = np.abs(branches[:, 0] - branches[:, 1])
    i_star = int(np.nanargmin(gap))
    eps_star = float(eps[i_star])
    z_ep = 0.5 * (branches[i_star, 0] + branches[i_star, 1])
    # window width: until Re split exceeds 3× min gap, min 2 samples each side
    min_gap = float(gap[i_star])
    opened = np.abs(branches[:, 0].real - branches[:, 1].real) > max(3.0 * min_gap, 0.02)
    # EP window: contiguous block around i_star where not yet opened
    ep_mask = np.zeros(eps.size, dtype=bool)
    ep_mask[i_star] = True
    for k in range(i_star - 1, -1, -1):
        if opened[k]:
            break
        ep_mask[k] = True
    for k in range(i_star + 1, eps.size):
        if opened[k]:
            break
        ep_mask[k] = True
    # if everything is "EP", shrink to ±2 samples
    if ep_mask.sum() > max(5, eps.size // 3):
        ep_mask[:] = False
        lo = max(0, i_star - 2)
        hi = min(eps.size, i_star + 3)
        ep_mask[lo:hi] = True
    arm_mask = opened & (~ep_mask) & np.isfinite(branches[:, 0])
    # Un-opened points away from ε★ are the same two branches still
    # stacked on Im (closed fork), not a third prong and not junction.
    leftover = np.zeros(eps.size, dtype=bool)

    pts_ep = []
    pts_arm_l = []
    pts_arm_r = []
    pts_junc = []
    for i, e in enumerate(eps):
        z0, z1 = branches[i, 0], branches[i, 1]
        if not np.isfinite(z0):
            continue
        rec = {"eps": float(e), "lam0": z0, "lam1": z1}
        if ep_mask[i]:
            pts_ep.append(rec)
        elif arm_mask[i]:
            # left = smaller Re, right = larger Re
            if z0.real <= z1.real:
                pts_arm_l.append({"eps": float(e), "lam": z0, "arm": "L"})
                pts_arm_r.append({"eps": float(e), "lam": z1, "arm": "R"})
            else:
                pts_arm_l.append({"eps": float(e), "lam": z1, "arm": "L"})
                pts_arm_r.append({"eps": float(e), "lam": z0, "arm": "R"})
        elif leftover[i]:
            pts_junc.append(rec)

    return {
        "eps_star": eps_star,
        "z_ep": z_ep,
        "i_star": i_star,
        "min_gap": min_gap,
        "ep_mask": ep_mask,
        "arm_mask": arm_mask,
        "leftover_mask": leftover,
        "pts_ep": pts_ep,
        "pts_arm_L": pts_arm_l,
        "pts_arm_R": pts_arm_r,
        "pts_junc": pts_junc,
        "n_ep": len(pts_ep) * 2,
        "n_arm": len(pts_arm_l) + len(pts_arm_r),
        "n_junc": len(pts_junc) * 2,
        "third_prong": False,
        "third_prong_note": "No third prong allowed. Junction is leftover of the two tracked branches only; empty of an extra prong.",
    }

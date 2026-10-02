"""Face-site percolation on GP(m,0): Betti numbers, largest cluster, Berry sum."""
import math

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components


def _components(N, edges, mask):
    """Connected components of the sub-graph induced on mask. Returns (count, labels on masked nodes)."""
    idx = np.flatnonzero(mask)
    n = len(idx)
    if n == 0:
        return 0, idx, np.array([], dtype=int)
    inv = -np.ones(N, dtype=np.int64)
    inv[idx] = np.arange(n)
    keep = mask[edges[:, 0]] & mask[edges[:, 1]]
    e = edges[keep]
    A = coo_matrix((np.ones(len(e)), (inv[e[:, 0]], inv[e[:, 1]])), shape=(n, n))
    c, lab = connected_components(A, directed=False)
    return c, idx, lab


def analyse(G, occ, q_B=0.5, c_B=1.0):
    """All observables for one occupation pattern occ (bool array over faces)."""
    N, edges, tris = G["N"], G["edges"], G["tris"]
    out = {}
    nocc = int(occ.sum())
    # whole occupied set
    b0, idx, lab = _components(N, edges, occ)
    cu, _, _ = _components(N, edges, ~occ)
    if nocc == 0:
        b1_alex, b2 = 0, 0
    elif nocc == N:
        b1_alex, b2 = 0, 1
    else:
        b1_alex, b2 = cu - 1, 0
    Ein = int(np.sum(occ[edges[:, 0]] & occ[edges[:, 1]]))
    Tin = int(np.sum(occ[tris[:, 0]] & occ[tris[:, 1]] & occ[tris[:, 2]]))
    chi = nocc - Ein + Tin
    b1_euler = b0 + b2 - chi
    out.update(b0=b0, b1=b1_alex, b1_euler=b1_euler, chi=chi, graph_cycles=Ein - nocc + b0)
    # largest cluster C
    if nocc == 0:
        out.update(frac_max=0.0, b1_C=0, berry=0.0)
        return out
    sizes = np.bincount(lab)
    big = int(np.argmax(sizes))
    C = np.zeros(N, dtype=bool)
    C[idx[lab == big]] = True
    out["frac_max"] = sizes[big] / N
    if C.all():
        out.update(b1_C=0, berry=0.0)
        return out
    ch, hidx, hlab = _components(N, edges, ~C)
    hs = np.bincount(hlab)
    out["b1_C"] = ch - 1
    holes = np.sort(hs)[:-1]           # drop the largest complement piece ("outside")
    gam = q_B * 4 * math.pi * holes / N
    out["berry"] = float(c_B * np.sum(1 - np.cos(gam)))   # times eps_V / L^d later
    return out


def sweep(G, ps, seeds, rng):
    """Coupled sweep: one uniform number per face per seed; occ = u < p."""
    keys = ["b0", "b1", "b1_euler", "chi", "graph_cycles", "frac_max", "b1_C", "berry"]
    res = {k: np.zeros((len(ps), seeds)) for k in keys}
    mismatch = 0
    for s in range(seeds):
        u = rng.random(G["N"])
        for i, p in enumerate(ps):
            o = analyse(G, u < p)
            for k in keys:
                res[k][i, s] = o[k]
            mismatch += int(o["b1"] != o["b1_euler"])
    return res, mismatch

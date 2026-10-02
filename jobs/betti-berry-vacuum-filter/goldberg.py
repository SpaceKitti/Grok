"""Goldberg polyhedron GP(m,0), built here (no existing GoldbergHexa code was found).

GP(m,0) is the dual of the class-I geodesic icosahedron of frequency m:
  geodesic vertices  <->  Goldberg faces (12 pentagons + 10(m^2-1) hexagons)
  geodesic edges     <->  pairs of Goldberg faces sharing an edge
  geodesic triangles <->  Goldberg vertices (three faces meet at each)
So face-site percolation on GP(m,0) is site percolation on this triangulation.
"""
import itertools
import math

import numpy as np


def icosahedron():
    t = (1 + math.sqrt(5)) / 2
    v = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
         (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
         (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    f = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
         (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
         (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
         (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    v = np.array(v, dtype=float)
    v /= np.linalg.norm(v, axis=1)[:, None]
    return v, f


def goldberg(m):
    """Return dict with face centres (unit vectors), face adjacency edges, triangles, degrees."""
    V0, F0 = icosahedron()
    key_to_idx = {}
    pts = []

    def vid(p):
        p = p / np.linalg.norm(p)
        k = tuple(np.round(p, 9))
        if k not in key_to_idx:
            key_to_idx[k] = len(pts)
            pts.append(p)
        return key_to_idx[k]

    tris = set()
    for (a, b, c) in F0:
        A, B, C = V0[a], V0[b], V0[c]
        grid = {}
        for i in range(m + 1):
            for j in range(m + 1 - i):
                # barycentric (exact on shared icosahedron edges up to rounding)
                P = (A * (m - i - j) + B * i + C * j) / m
                grid[(i, j)] = vid(P)
        for i in range(m):
            for j in range(m - i):
                tris.add(tuple(sorted((grid[(i, j)], grid[(i + 1, j)], grid[(i, j + 1)]))))
                if i + j < m - 1:
                    tris.add(tuple(sorted((grid[(i + 1, j)], grid[(i + 1, j + 1)], grid[(i, j + 1)]))))
    tris = sorted(tris)
    edges = set()
    for t in tris:
        for e in itertools.combinations(t, 2):
            edges.add(e)
    edges = np.array(sorted(edges), dtype=np.int64)
    tris = np.array(tris, dtype=np.int64)
    N = len(pts)
    deg = np.bincount(edges.ravel(), minlength=N)
    return {"m": m, "N": N, "centres": np.array(pts), "edges": edges, "tris": tris, "deg": deg}


def check(G):
    m, N = G["m"], G["N"]
    E, T = len(G["edges"]), len(G["tris"])
    deg = G["deg"]
    return {
        "faces N": N, "expected 10m^2+2": 10 * m * m + 2,
        "pentagons (degree 5)": int(np.sum(deg == 5)), "hexagons (degree 6)": int(np.sum(deg == 6)),
        "other degrees": int(np.sum((deg != 5) & (deg != 6))),
        "face-adjacency edges": E, "expected 30m^2": 30 * m * m,
        "Goldberg vertices (= triangles)": T, "expected 20m^2": 20 * m * m,
        "Euler V-E+F of Goldberg polyhedron": T - E + N,
    }

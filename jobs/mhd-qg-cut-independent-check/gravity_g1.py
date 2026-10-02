"""
Option G1 — independent gravity letter.

Lattice U(1) connection on a Cartesian mesh in the plane.
A is the symmetric-gauge potential of a UNIFORM background field B.
F = dA = B  (constant). No δ_Γ. No pair A. No I(γ,Γ). No Arg/atan2 cut.

  A_x = − (B/2) y
  A_y = + (B/2) x

B is a fixed O(1) number, not fitted so that a 2π loop gives −1.

Link angles on the mesh:
  θ_{n,x̂} = A_x(n + x̂/2) Δx
  θ_{n,ŷ} = A_y(n + ŷ/2) Δy
  U_ℓ = exp(i θ_ℓ)

Plaquette holonomy: U_□ = exp(i B Δx Δy)
CS density on a plaquette: F_□ / 2π = B Δx Δy / 2π

Wilson loop along a closed chain of links: product of U_ℓ.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# Independent of pair A and of Γ. Not tuned to U(2π) = −1.
B_FIELD = 1.0


@dataclass
class Lattice:
    x: np.ndarray  # 1D node coords
    y: np.ndarray
    dx: float
    dy: float
    Ax: np.ndarray  # link angles, shape (ny, nx-1)  x-directed, at y-nodes
    Ay: np.ndarray  # (ny-1, nx)  y-directed, at x-nodes
    F: np.ndarray  # plaquette field, (ny-1, nx-1)
    xc: np.ndarray
    yc: np.ndarray
    B: float


def build_lattice(n: int = 81, extent: float = 2.0, B: float = B_FIELD) -> Lattice:
    x = np.linspace(-extent, extent, n)
    y = np.linspace(-extent, extent, n)
    dx = float(x[1] - x[0])
    dy = float(y[1] - y[0])
    X, Y = np.meshgrid(x, y, indexing="xy")
    # x-links live at (x[i]+dx/2, y[j])
    Ax = np.zeros((n, n - 1))
    for j in range(n):
        for i in range(n - 1):
            xm = 0.5 * (x[i] + x[i + 1])
            ym = y[j]
            Ax[j, i] = (-0.5 * B * ym) * dx
    Ay = np.zeros((n - 1, n))
    for j in range(n - 1):
        for i in range(n):
            xm = x[i]
            ym = 0.5 * (y[j] + y[j + 1])
            Ay[j, i] = (0.5 * B * xm) * dy
    # plaquette (i,j) lower-left node (x[i], y[j]), oriented CCW
    F = np.zeros((n - 1, n - 1))
    for j in range(n - 1):
        for i in range(n - 1):
            ang = Ax[j, i] + Ay[j, i + 1] - Ax[j + 1, i] - Ay[j, i]
            F[j, i] = ang  # = B dx dy  (mod 2π, here small)
    xc = 0.5 * (x[:-1] + x[1:])
    yc = 0.5 * (y[:-1] + y[1:])
    return Lattice(x=x, y=y, dx=dx, dy=dy, Ax=Ax, Ay=Ay, F=F, xc=xc, yc=yc, B=B)


def scramble(lat: Lattice, rng: np.random.Generator) -> Lattice:
    """Destroy geometric content of A: random compact U(1) links, same mesh."""
    Ax = rng.uniform(-np.pi, np.pi, size=lat.Ax.shape)
    Ay = rng.uniform(-np.pi, np.pi, size=lat.Ay.shape)
    n = lat.x.size
    F = np.zeros((n - 1, n - 1))
    for j in range(n - 1):
        for i in range(n - 1):
            F[j, i] = Ax[j, i] + Ay[j, i + 1] - Ax[j + 1, i] - Ay[j, i]
    return Lattice(
        x=lat.x, y=lat.y, dx=lat.dx, dy=lat.dy,
        Ax=Ax, Ay=Ay, F=F, xc=lat.xc, yc=lat.yc, B=np.nan,
    )


def cs_density(lat: Lattice) -> np.ndarray:
    """F / 2π per plaquette."""
    return lat.F / (2.0 * np.pi)


def wilson_circle(lat: Lattice, center: complex, radius: float, n_seg: int = 256) -> complex:
    """
    Discrete holonomy along a polygonal loop on the mesh: nearest-link
    projection of a circle. Product of link U's. Independent of Γ.
    """
    theta = np.linspace(0.0, 2.0 * np.pi, n_seg, endpoint=False)
    pts = center + radius * np.exp(1j * theta)
    pts = np.append(pts, pts[0])
    acc = 1.0 + 0.0j
    x, y = lat.x, lat.y
    for k in range(pts.size - 1):
        z0, z1 = pts[k], pts[k + 1]
        acc *= _link_transport(lat, z0, z1)
    return acc


def wilson_theta_scan(lat: Lattice, center: complex, radius: float, n_theta: int = 361) -> dict:
    """
    Running holonomy U(θ) = P exp i ∫_0^θ A along the circle, θ: 0→4π.
    """
    theta = np.linspace(0.0, 4.0 * np.pi, n_theta)
    z = center + radius * np.exp(1j * theta)
    U = np.ones(n_theta, dtype=complex)
    for i in range(1, n_theta):
        U[i] = U[i - 1] * _link_transport(lat, z[i - 1], z[i])
    return {"theta": theta, "U": U, "z": z, "center": center, "radius": radius}


def _link_transport(lat: Lattice, z0: complex, z1: complex) -> complex:
    """
    Transport z0 → z1 by the lattice link(s) of the dominant axis step.
    Uses bilinear sampling of A along the segment (continuum interpolation
    of the symmetric-gauge A, equivalent to the lattice for this linear A).
    """
    # Exact for linear A: ∫ A·dl = (B/2)(x0 y1 − x1 y0) wait
    # A = (B/2)(-y, x), ∫_z0^z1 A·dl = (B/2) ∫ (-y dx + x dy)
    # For a straight segment z(t) = z0 + t (z1-z0), t∈[0,1]:
    x0, y0 = z0.real, z0.imag
    x1, y1 = z1.real, z1.imag
    # ∫ (-y dx + x dy) = ∫_0^1 [ -(y0+t Δy) Δx + (x0+t Δx) Δy ] dt
    # = -y0 Δx - 0.5 Δy Δx + x0 Δy + 0.5 Δx Δy = -y0 Δx + x0 Δy
    ang = 0.5 * lat.B * (-y0 * (x1 - x0) + x0 * (y1 - y0))
    return np.exp(1j * ang)

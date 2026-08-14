# ============================================================
# @Akitti C*Hive – Spectral Grid & Projection Utilities
# ============================================================

import jax.numpy as jnp
from jax import jit, random


def make_grid(N, L=1.0, dim=2):
    """Periodic torus (Clay Case 1). L=1 is the official Clay period.

    N and dim stay Python ints so later jitted kernels can branch on them.
    """
    N, dim = int(N), int(dim)
    L = float(L)
    k1d = jnp.fft.fftfreq(N, d=L / N) * 2 * jnp.pi
    if dim == 2:
        kx, ky = jnp.meshgrid(k1d, k1d, indexing="ij")
        k = (kx, ky)
        k2 = kx**2 + ky**2 + 1e-12
        dealias = (jnp.abs(kx) < (2 / 3) * k1d.max()) & (jnp.abs(ky) < (2 / 3) * k1d.max())
    else:
        kx, ky, kz = jnp.meshgrid(k1d, k1d, k1d, indexing="ij")
        k = (kx, ky, kz)
        k2 = kx**2 + ky**2 + kz**2 + 1e-12
        dealias = jnp.all(jnp.abs(jnp.stack(k)) < (2 / 3) * k1d.max(), axis=0)
    return {
        "k": k,
        "k_stack": jnp.stack(k),
        "k2": k2,
        "dealias": dealias,
        "N": N,
        "L": L,
        "dim": dim,
        "dx": L / N,
    }


@jit
def ik_cross(v_hat, grid):
    """Fourier curl: (ik × v̂). v_hat is (3, N, N, N)."""
    kx, ky, kz = grid["k"]
    return jnp.stack([
        1j * (ky * v_hat[2] - kz * v_hat[1]),
        1j * (kz * v_hat[0] - kx * v_hat[2]),
        1j * (kx * v_hat[1] - ky * v_hat[0]),
    ])


@jit
def project_div_free(u_hat, grid):
    """Exact divergence-free projection on the torus (Clay-compatible)."""
    k_stack, k2, dealias = grid["k_stack"], grid["k2"], grid["dealias"]
    div = jnp.sum(k_stack * u_hat, axis=0)
    return (u_hat - k_stack * div[None] / k2) * dealias[None]


@jit
def _vort_from_u_2d(u_hat, grid):
    return 1j * (grid["k"][0] * u_hat[1] - grid["k"][1] * u_hat[0])


@jit
def _vort_from_u_3d(u_hat, grid):
    return ik_cross(u_hat, grid) * grid["dealias"]


def vorticity_from_velocity(u_hat, grid):
    """ω̂ = ik × û  (2D returns the scalar ω_z hat)."""
    if u_hat.ndim == 3:
        return _vort_from_u_2d(u_hat, grid)
    return _vort_from_u_3d(u_hat, grid)


@jit
def _u_from_vort_2d(vort_hat, grid):
    psi_hat = -vort_hat / grid["k2"]
    return jnp.stack([
        1j * grid["k"][1] * psi_hat,
        -1j * grid["k"][0] * psi_hat,
    ]) * grid["dealias"]


@jit
def _u_from_vort_3d(vort_hat, grid):
    return (ik_cross(vort_hat, grid) / grid["k2"]) * grid["dealias"]


def velocity_from_vorticity(vort_hat, grid):
    """Biot–Savart: û = (ik × ω̂) / k². 2D uses the streamfunction."""
    if vort_hat.ndim == 2:
        return _u_from_vort_2d(vort_hat, grid)
    return _u_from_vort_3d(vort_hat, grid)


def generate_smooth_div_free_u0(key, grid, scale=0.008, modes=8):
    """C∞ smooth, exactly divergence-free IC (Clay requirement)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    coeffs = random.normal(key, (dim,) + (N,) * dim, dtype=jnp.complex128)
    coeffs *= jnp.exp(-grid["k2"] / (2 * modes**2))
    u_hat = jnp.fft.fftn(coeffs, axes=range(1, dim + 1))
    u_hat = project_div_free(u_hat, grid)
    return jnp.fft.ifftn(u_hat, axes=range(1, dim + 1)).real * scale


def generate_taylor_green(grid, scale=1.0):
    """Taylor–Green vortex — canonical 3D stretching IC on the Clay torus."""
    N, L = int(grid["N"]), float(grid["L"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
    k0 = 2 * jnp.pi / L
    u = scale * jnp.sin(k0 * X) * jnp.cos(k0 * Y) * jnp.cos(k0 * Z)
    v = -scale * jnp.cos(k0 * X) * jnp.sin(k0 * Y) * jnp.cos(k0 * Z)
    w = jnp.zeros_like(u)
    return jnp.stack([u, v, w])


def generate_antiparallel_tubes(grid, circulation=0.7, radius=0.08,
                               separation=0.24, perturbation=0.04,
                               axial_wave=1):
    """Crow-perturbed anti-parallel Gaussian tubes (reconnection IC).

    Two opposite-circulation cores along x on the Clay torus, displaced
    in the separating (y) direction out of phase and given a common
    z-kink — the symmetric Crow mode that drives the tubes together.
    Vorticity is aligned with the local centerline tangent, then
    projected solenoidal and converted to u by Biot–Savart.
    """
    N, L = int(grid["N"]), float(grid["L"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
    k = 2.0 * jnp.pi * axial_wave / L
    y1 = 0.5 * L - 0.5 * separation
    y2 = 0.5 * L + 0.5 * separation
    z0 = 0.5 * L
    s, c = jnp.sin(k * X), jnp.cos(k * X)
    y1c = y1 + perturbation * s
    y2c = y2 - perturbation * s
    z1c = z0 + perturbation * c
    z2c = z0 + perturbation * c
    ty, tz = perturbation * k * c, -perturbation * k * s
    inv = 1.0 / jnp.sqrt(1.0 + ty**2 + tz**2)
    t1 = jnp.stack([inv, ty * inv, tz * inv])
    t2 = jnp.stack([inv, -ty * inv, tz * inv])
    amp = circulation / (jnp.pi * radius**2)
    a1 = amp * jnp.exp(-((Y - y1c)**2 + (Z - z1c)**2) / radius**2)
    a2 = amp * jnp.exp(-((Y - y2c)**2 + (Z - z2c)**2) / radius**2)
    omega = t1 * a1 - t2 * a2
    omega_hat = project_div_free(
        jnp.fft.fftn(omega, axes=(1, 2, 3)) * grid["dealias"], grid)
    u_hat = velocity_from_vorticity(omega_hat, grid)
    return jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real


def cfl_dt(u, dx, nu, cfl=0.4):
    """Advective + viscous CFL bound from a physical-space velocity field."""
    umax = jnp.max(jnp.sqrt(jnp.sum(u**2, axis=0)))
    return cfl * dx / (umax + 4.0 * nu / dx + 1e-12)

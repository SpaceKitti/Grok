# ============================================================
# @Akitti C*Hive – Compressible MHD (patches 5+6, 7 Venus I_leak, 8 Brio-Wu)
# Continuity:  dt rho + div(rho u) = 0. Dealias the product rho u.
# Energy: Russell Dp/Dt = -gamma p div(u) + (gamma-1) Q
#         ideal EOS p = (gamma-1) rho e ; gamma=5/3 default.
# Primitive u on mode="cmhd" only:
#   dt u = -(u·∇)u - ∇p/ρ + (J×B)/ρ + ν ∇²u
# Qin / Helmholtz / project_div_free is OFF on u (sound lives here).
# mode="mhd" stays the projected vorticity toy in vorticity.py.
# I_leak (cmhd only) = Delta(E_kin + E_int + E_mag + e_glm),
# E_kin = <1/2 rho |u|^2>. Heat already in E_int; do not add int(eps_nu+eps_eta).
# Lorentz and p div u are transfers, not leaks. Bulk visc zeta default 0
# (cmhd only): dt u += grad(zeta div u), Q += zeta (div u)^2. zeta=0 is current cmhd.
# No nabla p on the vorticity RHS. No mean-pin and no floor.
# ============================================================

from functools import partial

import jax.numpy as jnp
from jax import jit

from .grid import project_div_free
from .mhd import current_from_b, induction_rhs, glm_psi_rhs, glm_grad_psi
from .diagnostics import strain_tensor, velocity_gradient


GAMMA_DEFAULT = 5.0 / 3.0


def uniform_rho_hat(grid, rho0=1.0, dtype=jnp.complex128):
    """Fourier transform of uniform density rho === rho0 (default 1)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    rho = jnp.full((N,) * dim, float(rho0), dtype=jnp.float64)
    return jnp.fft.fftn(rho).astype(dtype)


def bump_rho_hat(grid, eps=0.01, dtype=jnp.complex128):
    """rho = 1 + eps sin(2 pi x / L) on the periodic box. Mean is 1.

    Small eps (default 0.01) so min rho stays positive with no floor.
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, _Y = jnp.meshgrid(x, x, indexing="ij")
    else:
        X, _Y, _Z = jnp.meshgrid(x, x, x, indexing="ij")
    rho = 1.0 + float(eps) * jnp.sin(2.0 * jnp.pi * X / L)
    return jnp.fft.fftn(rho).astype(dtype)


def uniform_p_hat(grid, p0=1.0, dtype=jnp.complex128):
    """Fourier pressure field with uniform physical value p0 (default 1)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    p = jnp.full((N,) * dim, float(p0), dtype=jnp.float64)
    return jnp.fft.fftn(p).astype(dtype)


def bump_p_hat(grid, eps=0.01, p0=1.0, dtype=jnp.complex128):
    """p = p0 + eps sin(2 pi x / L) on the periodic box."""
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, _Y = jnp.meshgrid(x, x, indexing="ij")
    else:
        X, _Y, _Z = jnp.meshgrid(x, x, x, indexing="ij")
    p = float(p0) + float(eps) * jnp.sin(2.0 * jnp.pi * X / L)
    return jnp.fft.fftn(p).astype(dtype)


def max_abs_div_u(u_hat, grid):
    """max |div u| from a primitive (possibly compressive) u_hat."""
    div = jnp.fft.ifftn(1j * jnp.sum(grid["k_stack"] * u_hat, axis=0)).real
    return jnp.max(jnp.abs(div))


def uniform_eint_hat(grid, e0=1.5, dtype=jnp.complex128):
    """Fourier specific internal energy, uniform e0 (p0=1, gamma=5/3, rho=1)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    e = jnp.full((N,) * dim, float(e0), dtype=jnp.float64)
    return jnp.fft.fftn(e).astype(dtype)


def zero_eint_hat(grid, dtype=jnp.complex128):
    """Zeros in Fourier internal energy (parked helper; live field is p_hat)."""
    N, dim = int(grid["N"]), int(grid["dim"])
    return jnp.zeros((N,) * dim, dtype=dtype)


def eos_pressure(rho, e_int, gamma=GAMMA_DEFAULT):
    """Ideal EOS: p = (gamma - 1) rho e  (e = specific internal energy)."""
    return (gamma - 1.0) * rho * e_int


def eos_eint(rho, p, gamma=GAMMA_DEFAULT):
    """Ideal EOS inverse: e = p / ((gamma - 1) rho). No floor."""
    return p / ((gamma - 1.0) * rho)


def sound_wave_fields(grid, eps=1e-3, rho0=1.0, p0=1.0, gamma=GAMMA_DEFAULT):
    """Traveling 1D acoustic wave on a 1D-like 2D/3D grid (varies in x only).

    rho = rho0 + eps sin(2 pi x / L)
    p   = p0 + c_s^2 (rho - rho0)
    u_x = (c_s / rho0) (rho - rho0)
    c_s = sqrt(gamma p0 / rho0)
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    eps, rho0, p0, gamma = float(eps), float(rho0), float(p0), float(gamma)
    cs = jnp.sqrt(gamma * p0 / rho0)
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, _Y = jnp.meshgrid(x, x, indexing="ij")
        wave = jnp.sin(2.0 * jnp.pi * X / L)
        ux = (cs / rho0) * eps * wave
        u = jnp.stack([ux, jnp.zeros_like(ux)])
    else:
        X, _Y, _Z = jnp.meshgrid(x, x, x, indexing="ij")
        wave = jnp.sin(2.0 * jnp.pi * X / L)
        ux = (cs / rho0) * eps * wave
        z = jnp.zeros_like(ux)
        u = jnp.stack([ux, z, z])
    rho = rho0 + eps * wave
    p = p0 + (cs * cs) * eps * wave
    return u, rho, p, cs


def brio_wu_fields(grid, gamma=2.0):
    """Brio & Wu 1988 1D MHD Riemann on a 1D-like periodic torus.

    Paper gamma is 2. Primitive left/right states do not depend on gamma;
    the arg is for the caller EOS/CFL. Hive GAMMA_DEFAULT stays 5/3;
    evolution gamma is test-local via mhd_params/ic_params.

    Left  (x < L/2):  rho=1,     p=1,   u=0, Bx=0.75, By=+1
    Right (x >= L/2): rho=0.125, p=0.1, u=0, Bx=0.75, By=-1

    Periodic wrap puts a second jump at x=0. Stop before waves meet
    (t < (L/4) / max(|u|+c_s+|v_A|)). Spectral Gibbs ringing is the
    scheme (rho may go negative); no floor, no WENO/TVD.
    """
    gamma = float(gamma)
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, _Y = jnp.meshgrid(x, x, indexing="ij")
        z = jnp.zeros_like(X)
        left = X < (0.5 * L)
        rho = jnp.where(left, 1.0, 0.125)
        p = jnp.where(left, 1.0, 0.1)
        u = jnp.stack([z, z])
        Bx = jnp.full_like(X, 0.75)
        By = jnp.where(left, 1.0, -1.0)
        B = jnp.stack([Bx, By])
    else:
        X, _Y, _Z = jnp.meshgrid(x, x, x, indexing="ij")
        z = jnp.zeros_like(X)
        left = X < (0.5 * L)
        rho = jnp.where(left, 1.0, 0.125)
        p = jnp.where(left, 1.0, 0.1)
        u = jnp.stack([z, z, z])
        Bx = jnp.full_like(X, 0.75)
        By = jnp.where(left, 1.0, -1.0)
        B = jnp.stack([Bx, By, z])
    return u, rho, p, B


def brio_wu_wrap_time(grid, gamma=2.0):
    """Earliest t at which the two periodic Riemann fans can meet.

    Jumps at x=0 and x=L/2; each fan travels at most L/4. Bound by
    max(|u| + c_s + |v_A|) on the IC. No floor.
    """
    gamma = float(gamma)
    u, rho, p, B = brio_wu_fields(grid, gamma=gamma)
    speed = jnp.sqrt(jnp.sum(u ** 2, axis=0))
    cs = jnp.sqrt(gamma * p / rho)
    vA = jnp.sqrt(jnp.sum(B ** 2, axis=0) / rho)
    vfast = jnp.max(speed + cs + vA)
    return 0.25 * float(grid["L"]) / (float(vfast) + 1e-30)


def cfl_dt_cmhd(u, rho, p, B, dx, nu, eta_mag, gamma=GAMMA_DEFAULT, cfl=0.4, zeta=0.0):
    """dt from max(|u| + c_s + |v_A|) with c_s = sqrt(gamma p / rho).

    v_A = |B| / sqrt(rho). Viscous/resistive piece matches cfl_dt_mhd.
    No rho pin/floor.
    """
    speed = jnp.sqrt(jnp.sum(u ** 2, axis=0))
    cs = jnp.sqrt(gamma * p / rho)
    vA = jnp.sqrt(jnp.sum(B ** 2, axis=0) / rho)
    fast = jnp.max(speed + cs + vA)
    return cfl * dx / (fast + 4.0 * (nu + eta_mag + zeta) / dx + 1e-12)


@jit
def continuity_rhs(rho_hat, u_hat, grid):
    """Spectral 2/3-dealiased continuity: d_t rho = -div(rho u)."""
    dealias = grid["dealias"]
    k_stack = grid["k_stack"]
    rho = jnp.fft.ifftn(rho_hat).real
    u = jnp.fft.ifftn(u_hat, axes=range(1, u_hat.ndim)).real
    mom = rho[None] * u
    mom_hat = jnp.fft.fftn(mom, axes=range(1, mom.ndim)) * dealias[None]
    div_hat = jnp.sum(1j * k_stack * mom_hat, axis=0)
    return -div_hat * dealias


@partial(jit, static_argnums=(4,))
def continuity_step(rho_hat, u_hat, grid, dt, scheme="rk2"):
    """Advance rho with frozen u. No pin, no floor."""
    if scheme == "euler":
        out = rho_hat + dt * continuity_rhs(rho_hat, u_hat, grid)
    else:
        k1 = continuity_rhs(rho_hat, u_hat, grid)
        k2 = continuity_rhs(rho_hat + dt * k1, u_hat, grid)
        out = rho_hat + 0.5 * dt * (k1 + k2)
    return out * grid["dealias"]


density_step = continuity_step


def density_diagnostics(rho_hat, u_hat, grid):
    """mean/min/max rho and max|d_t rho|. Leftover <rho>-1 is not pinned."""
    rho = jnp.fft.ifftn(rho_hat).real
    drho = jnp.fft.ifftn(continuity_rhs(rho_hat, u_hat, grid)).real
    return {
        "mean_rho": jnp.mean(rho),
        "max_rho": jnp.max(rho),
        "min_rho": jnp.min(rho),
        "max_abs_rho_m1": jnp.max(jnp.abs(rho - 1.0)),
        "max_drho_dt": jnp.max(jnp.abs(drho)),
    }


@jit
def heating_Q(u_hat, B_hat, grid, eta_mag, nu, B_ext_hat=None, zeta=0.0):
    """Volumetric Q = Ohmic eta|J|^2 + viscous 2 nu S:S + zeta (div u)^2.

    For incompressible u, 2<S:S> = <omega^2> so mean Q_visc matches eps_nu.
    zeta=0 is the current cmhd (no bulk). Do not retune 2 nu S:S vs nu lap u.
    """
    Btot = B_hat if B_ext_hat is None else (B_hat + B_ext_hat)
    J_hat = current_from_b(Btot, grid)
    spatial = tuple(range(1, u_hat.ndim))
    if B_hat.shape[0] == 2:
        J = jnp.fft.ifftn(J_hat).real
        Q_ohm = eta_mag * (J * J)
    else:
        J = jnp.fft.ifftn(J_hat, axes=spatial).real
        Q_ohm = eta_mag * jnp.sum(J * J, axis=0)
    S = strain_tensor(u_hat, grid)
    Q_visc = 2.0 * nu * jnp.sum(S * S, axis=(0, 1))
    div_u = jnp.fft.ifftn(1j * jnp.sum(grid["k_stack"] * u_hat, axis=0)).real
    Q_bulk = zeta * (div_u * div_u)
    return Q_ohm + Q_visc + Q_bulk


@jit
def pressure_rhs(p_hat, u_hat, grid, gamma, Q):
    """Eulerian Russell: dt p = -u.grad p - gamma p div(u) + (gamma-1) Q.

    Russell: Dp/Dt = -gamma p div(u) + (gamma-1) Q.
    Products are 2/3-dealiased. No floor.
    """
    spatial = tuple(range(1, u_hat.ndim))
    dealias = grid["dealias"]
    u = jnp.fft.ifftn(u_hat, axes=spatial).real
    p = jnp.fft.ifftn(p_hat).real
    grad_p_hat = 1j * grid["k_stack"] * p_hat
    grad_p = jnp.fft.ifftn(grad_p_hat, axes=spatial).real
    u_dot_grad_p = jnp.sum(u * grad_p, axis=0)
    div_u_hat = 1j * jnp.sum(grid["k_stack"] * u_hat, axis=0)
    div_u = jnp.fft.ifftn(div_u_hat).real
    adv_hat = jnp.fft.fftn(u_dot_grad_p) * dealias
    pdiv_hat = jnp.fft.fftn(p * div_u) * dealias
    Q_hat = jnp.fft.fftn(Q) * dealias
    return (-adv_hat - gamma * pdiv_hat + (gamma - 1.0) * Q_hat) * dealias


@partial(jit, static_argnums=(4,))
def pressure_step(p_hat, u_hat, grid, dt, scheme, gamma, Q):
    """Advance p one step with frozen u and Q. Euler or Heun (rk2). No floor."""
    def rhs(p_hat):
        return pressure_rhs(p_hat, u_hat, grid, gamma, Q)

    if scheme == "euler":
        out = p_hat + dt * rhs(p_hat)
    else:
        k1 = rhs(p_hat)
        k2 = rhs(p_hat + dt * k1)
        out = p_hat + 0.5 * dt * (k1 + k2)
    return out * grid["dealias"]


def kinetic_energy_rho(rho_hat, u_hat):
    """E_kin = <1/2 rho |u|^2>. Not 1/2 <|u|^2>."""
    spatial = tuple(range(1, u_hat.ndim))
    rho = jnp.fft.ifftn(rho_hat).real
    u = jnp.fft.ifftn(u_hat, axes=spatial).real
    return 0.5 * jnp.mean(rho * jnp.sum(u * u, axis=0))


def viscous_work_lap(u_hat, grid, nu):
    """Mean work of the primitive viscous term: <u · ν ∇²u>. Bulk is separate."""
    spatial = tuple(range(1, u_hat.ndim))
    u = jnp.fft.ifftn(u_hat, axes=spatial).real
    lap = jnp.fft.ifftn(-grid["k2"][None] * u_hat, axes=spatial).real
    return jnp.mean(jnp.sum(u * (nu * lap), axis=0))


def viscous_heat_SS(u_hat, grid, nu):
    """Mean viscous heat Q = <2 ν S:S>. Bulk is separate."""
    S = strain_tensor(u_hat, grid)
    return jnp.mean(2.0 * nu * jnp.sum(S * S, axis=(0, 1)))


def bulk_heat_div(u_hat, grid, zeta):
    """Mean bulk heat Q_bulk = <ζ (∇·u)²>. Zero when zeta=0."""
    div_u = jnp.fft.ifftn(1j * jnp.sum(grid["k_stack"] * u_hat, axis=0)).real
    return jnp.mean(zeta * div_u * div_u)


def viscous_disagreement(u_hat, grid, nu):
    """When ∇·u ≠ 0, <u · ν ∇²u> and <2 ν S:S> disagree. Measure, do not retune."""
    return viscous_work_lap(u_hat, grid, nu), viscous_heat_SS(u_hat, grid, nu)


def energy_diagnostics(rho_hat, p_hat, gamma=GAMMA_DEFAULT, u_hat=None):
    """e_int is volumetric <p/(gamma-1)>. Optional e_kin = <1/2 rho |u|^2>."""
    p = jnp.fft.ifftn(p_hat).real
    e_dens = p / (gamma - 1.0)
    out = {
        "e_int": jnp.mean(e_dens),
        "mean_e_int": jnp.mean(e_dens),
        "p": jnp.mean(p),
        "mean_p": jnp.mean(p),
        "min_p": jnp.min(p),
        "gamma": jnp.asarray(gamma, dtype=jnp.float64),
    }
    if u_hat is not None:
        out["e_kin"] = kinetic_energy_rho(rho_hat, u_hat)
    return out


@jit
def primitive_u_rhs(u_hat, rho_hat, p_hat, B_hat, grid, nu, force_hat,
                    B_ext_hat, zeta=0.0):
    """dt u = -(u·∇)u - ∇p/ρ + (J×B)/ρ + ν ∇²u + ζ ∇(∇·u) + f. No Qin on u."""
    spatial = tuple(range(1, u_hat.ndim))
    dealias = grid["dealias"]
    k_stack = grid["k_stack"]
    u = jnp.fft.ifftn(u_hat, axes=spatial).real
    rho = jnp.fft.ifftn(rho_hat).real
    grad_u = velocity_gradient(u_hat, grid)
    adv = jnp.einsum("j...,ij...->i...", u, grad_u)
    adv_hat = jnp.fft.fftn(adv, axes=spatial) * dealias[None]
    grad_p = jnp.fft.ifftn(1j * k_stack * p_hat, axes=spatial).real
    gp_hat = jnp.fft.fftn(grad_p / rho, axes=spatial) * dealias[None]
    Btot = B_hat + B_ext_hat
    J_hat = current_from_b(Btot, grid)
    B = jnp.fft.ifftn(Btot, axes=spatial).real
    if B_hat.shape[0] == 2:
        Jz = jnp.fft.ifftn(J_hat).real
        JxB = jnp.stack([-Jz * B[1], Jz * B[0]])
    else:
        J = jnp.fft.ifftn(J_hat, axes=spatial).real
        JxB = jnp.stack([
            J[1] * B[2] - J[2] * B[1],
            J[2] * B[0] - J[0] * B[2],
            J[0] * B[1] - J[1] * B[0],
        ])
    lor_hat = jnp.fft.fftn(JxB / rho, axes=spatial) * dealias[None]
    visc = -nu * grid["k2"][None] * u_hat
    # Constant-zeta bulk, same kinematic placement as nu lap u (not /rho).
    div_u_hat = 1j * jnp.sum(k_stack * u_hat, axis=0)
    bulk = zeta * (1j * k_stack * div_u_hat[None])
    return (-adv_hat - gp_hat + lor_hat + visc + bulk + force_hat) * dealias[None]


@jit
def primitive_cmhd_rhs(u_hat, B_hat, rho_hat, p_hat, psi_hat, grid,
                       nu, force_hat, eta_mag, B_ext_hat, induct_ext,
                       eta_hyper, hyper_kcut, glm_ch, glm_cr, gamma, zeta):
    """Coupled (u, B, rho, p, psi) tendencies. Helmholtz off on u."""
    du = primitive_u_rhs(
        u_hat, rho_hat, p_hat, B_hat, grid, nu, force_hat, B_ext_hat, zeta)
    B_cross = B_hat + induct_ext * B_ext_hat
    dB = induction_rhs(
        B_hat, u_hat, grid, eta_mag, B_cross, eta_hyper, hyper_kcut,
        None, 0.0)
    glm_on = (glm_ch != 0.0).astype(B_hat.real.dtype)
    dB = dB + glm_grad_psi(psi_hat, grid) * glm_on
    drho = continuity_rhs(rho_hat, u_hat, grid)
    Q = heating_Q(u_hat, B_hat, grid, eta_mag, nu, B_ext_hat, zeta)
    dp = pressure_rhs(p_hat, u_hat, grid, gamma, Q)
    dpsi = glm_psi_rhs(psi_hat, B_hat, grid, glm_ch, glm_cr) * glm_on
    return du, dB, drho, dp, dpsi


@partial(jit, static_argnums=(7,))
def primitive_cmhd_step(u_hat, B_hat, rho_hat, p_hat, psi_hat, grid, dt, scheme,
                        nu, force_hat, eta_mag, B_ext_hat, induct_ext,
                        eta_hyper, hyper_kcut, glm_ch, glm_cr, gamma, zeta):
    """One coupled primitive-u cmhd step. No project_div_free on u."""
    def rhs(u, B, rho, p, psi):
        return primitive_cmhd_rhs(
            u, B, rho, p, psi, grid, nu, force_hat, eta_mag, B_ext_hat,
            induct_ext, eta_hyper, hyper_kcut, glm_ch, glm_cr, gamma, zeta)

    if scheme == "euler":
        du, dB, drho, dp, dpsi = rhs(u_hat, B_hat, rho_hat, p_hat, psi_hat)
        u_hat = u_hat + dt * du
        B_hat = B_hat + dt * dB
        rho_hat = rho_hat + dt * drho
        p_hat = p_hat + dt * dp
        psi_hat = psi_hat + dt * dpsi
    else:
        k1u, k1b, k1r, k1p, k1s = rhs(u_hat, B_hat, rho_hat, p_hat, psi_hat)
        k2u, k2b, k2r, k2p, k2s = rhs(
            u_hat + dt * k1u, B_hat + dt * k1b, rho_hat + dt * k1r,
            p_hat + dt * k1p, psi_hat + dt * k1s)
        u_hat = u_hat + 0.5 * dt * (k1u + k2u)
        B_hat = B_hat + 0.5 * dt * (k1b + k2b)
        rho_hat = rho_hat + 0.5 * dt * (k1r + k2r)
        p_hat = p_hat + 0.5 * dt * (k1p + k2p)
        psi_hat = psi_hat + 0.5 * dt * (k1s + k2s)
    dealias = grid["dealias"]
    u_hat = u_hat * dealias[None]
    rho_hat = rho_hat * dealias
    p_hat = p_hat * dealias
    psi_hat = psi_hat * dealias
    B_proj = project_div_free(B_hat, grid)
    B_hat = jnp.where(glm_ch != 0.0, B_hat * dealias[None], B_proj)
    return u_hat, B_hat, rho_hat, p_hat, psi_hat


def coupled_cmhd_step(u_hat, tau_hat, B_hat, rho_hat, p_hat, grid, nu, dt,
                      force_hat=0, scheme="rk2", t=0.0,
                      eta_p=0.003, lambda_relax=0.6, alpha=0.085,
                      beta_scar=0.13, stress_diff=1e-4, clay_gain=0.0,
                      gum_scale=1.0, stress_couple=1.0, regs=None,
                      eta_mag=1.0e-3, eta_odd=0.0, B_ext_hat=None,
                      induct_ext=1.0, mu_eff=0.0, berry_gain=0.0,
                      eta_hyper=0.0, posdiv=0.0, hyper_kcut=0.0,
                      psi_hat=None, glm_ch=0.0, glm_cr=0.18,
                      gamma=GAMMA_DEFAULT, zeta=0.0):
    """Primitive-u compressible MHD step + continuity + Russell p.

    force_hat is in velocity space. Qin/Helmholtz is OFF on u (no
    project_div_free). B stays projected unless GLM is on. Clay/odd
    args are accepted for driver compatibility and ignored. nu_tot
    includes mu_eff. t/eta_p/posdiv unused. mode="mhd" is not this.
    """
    del (eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
         gum_scale, stress_couple, regs, eta_odd, berry_gain, posdiv, t)
    if B_ext_hat is None:
        B_ext_hat = jnp.zeros_like(B_hat)
    if psi_hat is None:
        psi_hat = jnp.zeros_like(B_hat[0])
    if isinstance(force_hat, (int, float)) and float(force_hat) == 0.0:
        force_hat = jnp.zeros_like(u_hat)
    nu_tot = nu + mu_eff
    u_hat, B_hat, rho_hat, p_hat, psi_hat = primitive_cmhd_step(
        u_hat, B_hat, rho_hat, p_hat, psi_hat, grid, dt, scheme,
        nu_tot, force_hat, eta_mag, B_ext_hat, induct_ext,
        eta_hyper, hyper_kcut, glm_ch, glm_cr, gamma, zeta)
    return u_hat, tau_hat, B_hat, psi_hat, rho_hat, p_hat

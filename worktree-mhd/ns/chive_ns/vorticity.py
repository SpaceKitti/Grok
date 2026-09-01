# ============================================================
# @Akitti C*Hive – Vorticity + Z₇ Scar Forcing + 3D Stretching
# ============================================================

from functools import partial

import jax.numpy as jnp
from jax import jit

from .grid import (
    ik_cross, project_div_free, _u_from_vort_2d, _u_from_vort_3d,
    _vort_from_u_2d,
)
from .clay import (
    _oldroyd_rhs_2d, _oldroyd_rhs_3d, gum_damping,
    _stress_vort_force_2d, _stress_vort_force_3d, _div_tau,
)
from .regularisers import (
    mollify_hat, kinematic_lambda, high_de_blend, lb_filtered_div,
    _voigt_rhs_3d_sheet, _voigt_rhs_2d, frechet_stress_rhs,
)
from .diagnostics import strain_tensor
from .constants import DELTA_MIN
from .mhd import (
    _lorentz_vort_2d, _lorentz_vort_3d,
    _induction_2d, _induction_3d,
    _odd_vort_2d, _odd_vort_3d,
    glm_grad_psi, glm_psi_rhs,
)

# regs = (soft_J, α∥, α⊥, γ_s, ε_Fréchet, high_De, α_LB, soft_LB, λ_kin)
_ZERO_REGS = jnp.zeros((9,), dtype=jnp.float64)


@jit
def modest_liar(t_norm):
    return jnp.sqrt(1.0 - jnp.clip(t_norm, 0.0, 1.0))


def _wrap(d, L):
    """Minimum-image displacement on the period-L torus."""
    return d - L * jnp.round(d / L)


def default_scar_centres(L, n_scars=1, dim=3):
    """Lattice of 1–8 (or more) scar centres on the Clay torus."""
    n = max(int(n_scars), 1)
    c = 0.5 * L
    a = 0.25 * L
    if n == 1:
        return ((c,) * dim,)
    if dim == 2:
        if n == 2:
            return ((c - a, c), (c + a, c))
        pts = []
        for k in range(n):
            ang = 2.0 * jnp.pi * k / n
            pts.append((c + a * float(jnp.cos(ang)), c + a * float(jnp.sin(ang))))
        return tuple(pts)
    if n == 2:
        return ((c - a, c, c), (c + a, c, c))
    if n == 3:
        return ((c + a, c, c), (c - 0.5 * a, c + 0.866 * a, c),
                (c - 0.5 * a, c - 0.866 * a, c))
    if n == 4:
        return ((c + a, c + a, c + a), (c + a, c - a, c - a),
                (c - a, c + a, c - a), (c - a, c - a, c + a))
    if n == 5:
        return default_scar_centres(L, 4, 3) + ((c, c, c),)
    if n == 6:
        return ((c + a, c, c), (c - a, c, c), (c, c + a, c),
                (c, c - a, c), (c, c, c + a), (c, c, c - a))
    if n == 7:
        return default_scar_centres(L, 6, 3) + ((c, c, c),)
    # n >= 8: 2×2×2 cube, then extra points on a 3³ grid
    cube = []
    for sx in (-a, a):
        for sy in (-a, a):
            for sz in (-a, a):
                cube.append((c + sx, c + sy, c + sz))
    if n <= 8:
        return tuple(cube[:n])
    extra = []
    b = L / 3.0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                p = ((i + 0.5) * b, (j + 0.5) * b, (k + 0.5) * b)
                extra.append(p)
    return tuple(cube + extra)[:n]


def resolve_scar_centres(grid, n_scars=1, scar_centres=None, center=None):
    """scar_centres wins; else n_scars on the default lattice; else `center`."""
    L, dim = float(grid["L"]), int(grid["dim"])
    if scar_centres is not None:
        return tuple(tuple(map(float, c)) for c in scar_centres)
    if center is not None and int(n_scars) <= 1:
        c = tuple(center)
        if len(c) < dim:
            c = c + (L / 2,) * (dim - len(c))
        return (c[:dim],)
    return default_scar_centres(L, n_scars, dim)


def _one_scar_2d(X, Y, center, L, amplitude, phase0, sigma):
    dx, dy = _wrap(X - center[0], L), _wrap(Y - center[1], L)
    theta = jnp.arctan2(dy, dx)
    phase = jnp.cos(7 * theta + phase0) + 0.5 * jnp.sin(7 * theta - phase0)
    return amplitude * phase * jnp.exp(-(dx**2 + dy**2) / (2 * sigma**2))


def _one_scar_3d_body(X, Y, Z, center, L, amplitude, phase0, helix_sign, sigma):
    """Local helical Z₇ body force about `center` (periodic)."""
    dx = _wrap(X - center[0], L)
    dy = _wrap(Y - center[1], L)
    dz = _wrap(Z - center[2], L)
    theta = jnp.arctan2(dy, dx)
    z_ang = helix_sign * 4.0 * jnp.pi * dz / L
    phase = jnp.cos(7 * theta + z_ang + phase0) + 0.5 * jnp.sin(7 * theta - z_ang)
    env = jnp.exp(-(dx**2 + dy**2 + dz**2) / (2 * sigma**2))
    return amplitude * phase * env * jnp.stack([
        -dy,
        dx,
        0.45 * jnp.sin(z_ang) * jnp.ones_like(dx),
    ])


def z7_braid_forcing(grid, amplitude, center=None, n_scars=1,
                     scar_centres=None, sigma=None):
    """Z₇ anyonic phase + Gaussian mollifier → fractal butterfly scars.

    2D: scalar vorticity force.  3D: curl of a helical body force.
    Multi-scar: sum local braids at `scar_centres`, or at the default
    n_scars-point lattice. n_scars=1 recovers the single central scar.
    Each centre gets a 2π k / 7 phase shift and alternating helix sign.
    """
    N, L, dim = int(grid["N"]), float(grid["L"]), int(grid["dim"])
    centres = resolve_scar_centres(grid, n_scars, scar_centres, center)
    x = jnp.linspace(0.0, L, N, endpoint=False)
    if dim == 2:
        X, Y = jnp.meshgrid(x, x, indexing="ij")
        sig = 0.35 if sigma is None else sigma
        force = 0.0
        for k, c in enumerate(centres):
            force = force + _one_scar_2d(
                X, Y, c, L, amplitude, 2.0 * jnp.pi * k / 7.0, sig)
        force_hat = jnp.fft.fftn(force) * grid["dealias"]
        return force_hat

    X, Y, Z = jnp.meshgrid(x, x, x, indexing="ij")
    sig = 0.28 if sigma is None else sigma
    body = 0.0
    for k, c in enumerate(centres):
        helix = 1.0 if (k % 2 == 0) else -1.0
        body = body + _one_scar_3d_body(
            X, Y, Z, c, L, amplitude, 2.0 * jnp.pi * k / 7.0, helix, sig)
    body_hat = jnp.fft.fftn(body, axes=(1, 2, 3)) * grid["dealias"]
    return ik_cross(body_hat, grid)


@jit
def _rhs_2d(vort_hat, grid, nu, force_hat):
    dealias, k2 = grid["dealias"], grid["k2"]
    u_hat = _u_from_vort_2d(vort_hat, grid)
    u = jnp.fft.ifftn(u_hat[0]).real
    v = jnp.fft.ifftn(u_hat[1]).real
    adv = (u * jnp.fft.ifftn(1j * grid["k"][0] * vort_hat).real +
           v * jnp.fft.ifftn(1j * grid["k"][1] * vort_hat).real)
    rhs = -jnp.fft.fftn(adv) * dealias - nu * k2 * vort_hat
    return (rhs + force_hat) * dealias


@jit
def _rhs_3d(vort_hat, grid, nu, force_hat):
    """Rotational form ∇×(u×ω) = (ω·∇)u − (u·∇)ω when both fields are solenoidal."""
    dealias, k2 = grid["dealias"], grid["k2"]
    u_hat = _u_from_vort_3d(vort_hat, grid)
    u = jnp.fft.ifftn(u_hat, axes=(1, 2, 3)).real
    omega = jnp.fft.ifftn(vort_hat, axes=(1, 2, 3)).real
    cross = jnp.stack([
        u[1] * omega[2] - u[2] * omega[1],
        u[2] * omega[0] - u[0] * omega[2],
        u[0] * omega[1] - u[1] * omega[0],
    ])
    cross_hat = jnp.fft.fftn(cross, axes=(1, 2, 3)) * dealias
    rhs = ik_cross(cross_hat, grid) - nu * k2 * vort_hat
    return (rhs + force_hat) * dealias


def ns_vorticity_rhs(vort_hat, grid, nu, force_hat=0):
    """Vorticity RHS. 3D uses the rotational form that includes full stretching."""
    if vort_hat.ndim == 2:
        return _rhs_2d(vort_hat, grid, nu, force_hat)
    return _rhs_3d(vort_hat, grid, nu, force_hat)


@partial(jit, static_argnums=(5,))
def _step_2d(vort_hat, grid, nu, dt, force_hat, scheme):
    rhs = _rhs_2d
    if scheme == "euler":
        return (vort_hat + dt * rhs(vort_hat, grid, nu, force_hat)) * grid["dealias"]
    k1 = rhs(vort_hat, grid, nu, force_hat)
    k2 = rhs(vort_hat + dt * k1, grid, nu, force_hat)
    return (vort_hat + 0.5 * dt * (k1 + k2)) * grid["dealias"]


@partial(jit, static_argnums=(5,))
def _step_3d(vort_hat, grid, nu, dt, force_hat, scheme):
    rhs = _rhs_3d
    if scheme == "euler":
        out = vort_hat + dt * rhs(vort_hat, grid, nu, force_hat)
    else:
        k1 = rhs(vort_hat, grid, nu, force_hat)
        k2 = rhs(vort_hat + dt * k1, grid, nu, force_hat)
        out = vort_hat + 0.5 * dt * (k1 + k2)
    return project_div_free(out, grid)


def ns_vorticity_step(vort_hat, grid, nu, dt, force_hat=0, scheme="rk2"):
    """Classic vorticity formulation. RK2 (Heun) is the 3D default;
    forward Euler is kept for the original 2D scar runs."""
    if vort_hat.ndim == 2:
        return _step_2d(vort_hat, grid, nu, dt, force_hat, scheme)
    return _step_3d(vort_hat, grid, nu, dt, force_hat, scheme)


def _strain_source_eta(eta_p, tau, S, nu, lam_g):
    """Reduce 2(η_p/λ)S when polymer work is already large (self-consistent λ)."""
    work = jnp.mean(jnp.einsum("ij...,ij...->...", tau, S))
    Z = jnp.mean(jnp.sum(S**2, axis=(0, 1))) * 2.0 + 1e-30
    lam = kinematic_lambda(work, nu, Z)
    return eta_p * (1.0 - lam_g * lam)


@partial(jit, static_argnums=(6,))
def _coupled_step_2d(omega, tau, grid, nu, dt, force, scheme, t,
                     eta_p, lambda_relax, alpha, beta_scar, stress_diff,
                     clay_gain, gum_scale, stress_couple, regs):
    soft_J, a_par, a_perp, g_s, eps_fr, high_de, a_LB, s_LB, lam_g = regs

    def rhs(omega, tau):
        u_hat = mollify_hat(_u_from_vort_2d(omega, grid), grid, soft_J)
        tau_phys = jnp.fft.ifftn(tau, axes=(2, 3)).real
        S = strain_tensor(u_hat, grid)
        eta_eff = _strain_source_eta(eta_p, tau_phys, S, nu, lam_g)
        dtau = (_oldroyd_rhs_2d(tau, u_hat, grid, eta_eff, lambda_relax,
                                alpha, beta_scar, stress_diff, clay_gain)
                + _voigt_rhs_2d(tau, None, grid, a_par, a_perp, g_s)
                + frechet_stress_rhs(tau, tau_phys, grid, eps_fr))
        vort = jnp.fft.ifftn(omega).real
        blended, _ = high_de_blend(tau_phys, vort[None], S, eta_p,
                                   lambda_relax, high_de)
        tau_use = jnp.fft.fftn(blended, axes=(2, 3)) * grid["dealias"]
        tau_f = stress_couple * _stress_vort_force_2d(tau_use, grid)
        f_lb = _vort_from_u_2d(lb_filtered_div(tau_use, grid, s_LB), grid)
        tau_f = (1.0 - a_LB) * tau_f + a_LB * f_lb * grid["dealias"]
        dw = _rhs_2d(omega, grid, nu, force + tau_f)
        return dw, dtau

    if scheme == "euler":
        dw, dtau = rhs(omega, tau)
        omega, tau = omega + dt * dw, tau + dt * dtau
    else:
        k1w, k1t = rhs(omega, tau)
        k2w, k2t = rhs(omega + dt * k1w, tau + dt * k1t)
        omega = omega + 0.5 * dt * (k1w + k2w)
        tau = tau + 0.5 * dt * (k1t + k2t)
    tau = 0.5 * (tau + jnp.swapaxes(tau, 0, 1))
    return omega * grid["dealias"], gum_damping(tau, t, gum_scale)


@partial(jit, static_argnums=(6,))
def _coupled_step_3d(omega, tau, grid, nu, dt, force, scheme, t,
                     eta_p, lambda_relax, alpha, beta_scar, stress_diff,
                     clay_gain, gum_scale, stress_couple, regs):
    """NS stretching + ∇×(∇·τ_reg) with hybrid regularisers."""
    soft_J, a_par, a_perp, g_s, eps_fr, high_de, a_LB, s_LB, lam_g = regs

    def rhs(omega, tau):
        u_hat = mollify_hat(_u_from_vort_3d(omega, grid), grid, soft_J)
        omg = jnp.fft.ifftn(omega, axes=(1, 2, 3)).real
        tau_phys = jnp.fft.ifftn(tau, axes=(2, 3, 4)).real
        S = strain_tensor(u_hat, grid)
        eta_eff = _strain_source_eta(eta_p, tau_phys, S, nu, lam_g)
        dtau = (_oldroyd_rhs_3d(tau, u_hat, grid, eta_eff, lambda_relax,
                                alpha, beta_scar, stress_diff, clay_gain)
                + _voigt_rhs_3d_sheet(tau, omg, S, grid, a_par, a_perp, g_s)
                + frechet_stress_rhs(tau, tau_phys, grid, eps_fr))
        blended, _ = high_de_blend(tau_phys, omg, S, eta_p, lambda_relax, high_de)
        tau_use = jnp.fft.fftn(blended, axes=(2, 3, 4)) * grid["dealias"]
        tau_f = stress_couple * _stress_vort_force_3d(tau_use, grid)
        f_lb = ik_cross(lb_filtered_div(tau_use, grid, s_LB), grid)
        tau_f = (1.0 - a_LB) * tau_f + a_LB * f_lb * grid["dealias"]
        dw = _rhs_3d(omega, grid, nu, force + tau_f)
        return dw, dtau

    if scheme == "euler":
        dw, dtau = rhs(omega, tau)
        omega, tau = omega + dt * dw, tau + dt * dtau
    else:
        k1w, k1t = rhs(omega, tau)
        k2w, k2t = rhs(omega + dt * k1w, tau + dt * k1t)
        omega = omega + 0.5 * dt * (k1w + k2w)
        tau = tau + 0.5 * dt * (k1t + k2t)
    omega = project_div_free(omega, grid)
    tau = 0.5 * (tau + jnp.swapaxes(tau, 0, 1))
    return omega, gum_damping(tau, t, gum_scale)


def coupled_vorticity_stress_step(omega_hat, tau_hat, grid, nu, dt, force_hat=0,
                                  scheme="rk2", t=0.0, eta_p=0.003,
                                  lambda_relax=0.6, alpha=0.085,
                                  beta_scar=0.13, stress_diff=1e-4,
                                  clay_gain=float(DELTA_MIN),
                                  gum_scale=1.0, stress_couple=1.0,
                                  regs=None):
    """One coupled (ω, τ) step with optional hybrid regularisers."""
    if regs is None:
        regs = _ZERO_REGS
    args = (omega_hat, tau_hat, grid, nu, dt, force_hat, scheme, t,
            eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
            gum_scale, stress_couple, regs)
    if omega_hat.ndim == 2:
        return _coupled_step_2d(*args)
    return _coupled_step_3d(*args)


@partial(jit, static_argnums=(7,))
def _coupled_mhd_step_2d(omega, tau, B, grid, nu, dt, force, scheme, t,
                         eta_p, lambda_relax, alpha, beta_scar, stress_diff,
                         clay_gain, gum_scale, stress_couple, regs,
                         eta_mag, eta_odd, B_ext, induct_ext, mu_eff,
                         berry_gain, eta_hyper, posdiv, hyper_kcut,
                         psi, glm_ch, glm_cr):
    """(omega, tau, B, psi) step in 2D: NS + Oldroyd-B + Lorentz + induction + odd visc."""
    soft_J, a_par, a_perp, g_s, eps_fr, high_de, a_LB, s_LB, lam_g = regs
    nu_tot = nu + mu_eff

    def rhs(omega, tau, B, psi):
        u_raw = _u_from_vort_2d(omega, grid)
        u_hat = mollify_hat(u_raw, grid, soft_J)
        tau_phys = jnp.fft.ifftn(tau, axes=(2, 3)).real
        S = strain_tensor(u_hat, grid)
        eta_eff = _strain_source_eta(eta_p, tau_phys, S, nu, lam_g)
        dtau = (_oldroyd_rhs_2d(tau, u_hat, grid, eta_eff, lambda_relax,
                                alpha, beta_scar, stress_diff, clay_gain)
                + _voigt_rhs_2d(tau, None, grid, a_par, a_perp, g_s)
                + frechet_stress_rhs(tau, tau_phys, grid, eps_fr))
        vort = jnp.fft.ifftn(omega).real
        blended, _ = high_de_blend(tau_phys, vort[None], S, eta_p,
                                   lambda_relax, high_de)
        tau_use = jnp.fft.fftn(blended, axes=(2, 3)) * grid["dealias"]
        tau_f = stress_couple * _stress_vort_force_2d(tau_use, grid)
        f_lb = _vort_from_u_2d(lb_filtered_div(tau_use, grid, s_LB), grid)
        tau_f = (1.0 - a_LB) * tau_f + a_LB * f_lb * grid["dealias"]
        B_tot = B + B_ext
        B_cross = B + induct_ext * B_ext
        mag_f = _lorentz_vort_2d(B_tot, grid) + _odd_vort_2d(u_raw, grid, eta_odd)
        dw = _rhs_2d(omega, grid, nu_tot, force + tau_f + mag_f)
        dB = _induction_2d(B, u_raw, grid, eta_mag, B_cross, eta_hyper, hyper_kcut)
        glm_on = (glm_ch != 0.0).astype(B.real.dtype)
        dB = dB + glm_grad_psi(psi, grid) * glm_on
        dpsi = glm_psi_rhs(psi, B, grid, glm_ch, glm_cr) * glm_on
        return dw, dtau, dB, dpsi

    if scheme == "euler":
        dw, dtau, dB, dpsi = rhs(omega, tau, B, psi)
        omega, tau, B = omega + dt * dw, tau + dt * dtau, B + dt * dB
        psi = psi + dt * dpsi
    else:
        k1w, k1t, k1b, k1p = rhs(omega, tau, B, psi)
        om_m = omega + dt * k1w
        B_m = B + dt * k1b
        om_p = om_m * grid["dealias"]
        B_p = project_div_free(B_m, grid)
        om_m = posdiv * om_p + (1.0 - posdiv) * om_m
        B_m = posdiv * B_p + (1.0 - posdiv) * B_m
        k2w, k2t, k2b, k2p = rhs(om_m, tau + dt * k1t, B_m, psi + dt * k1p)
        omega = omega + 0.5 * dt * (k1w + k2w)
        tau = tau + 0.5 * dt * (k1t + k2t)
        B = B + 0.5 * dt * (k1b + k2b)
        psi = psi + 0.5 * dt * (k1p + k2p)
    tau = 0.5 * (tau + jnp.swapaxes(tau, 0, 1))
    B_proj = project_div_free(B, grid)
    B = jnp.where(glm_ch != 0.0, B * grid["dealias"], B_proj)
    psi = psi * grid["dealias"]
    return omega * grid["dealias"], gum_damping(tau, t, gum_scale), B, psi


@partial(jit, static_argnums=(7,))
def _coupled_mhd_step_3d(omega, tau, B, grid, nu, dt, force, scheme, t,
                         eta_p, lambda_relax, alpha, beta_scar, stress_diff,
                         clay_gain, gum_scale, stress_couple, regs,
                         eta_mag, eta_odd, B_ext, induct_ext, mu_eff,
                         berry_gain, eta_hyper, posdiv, hyper_kcut,
                         psi, glm_ch, glm_cr):
    """(omega, tau, B, psi) step in 3D: stretching + curl(div tau) + curl(JxB) + induction.

    B_ext is a static freeze-out field: Lorentz uses B+B_ext, induction
    stretches only B + induct_ext B_ext (induct_ext=0 → pure back-pressure).
    Qin Helmholtz on ω and B after Heun. Polymer law unchanged.
    Unmollified u for induction / Lorentz / odd (energy identity).
    """
    soft_J, a_par, a_perp, g_s, eps_fr, high_de, a_LB, s_LB, lam_g = regs
    nu_tot = nu + mu_eff

    def rhs(omega, tau, B, psi):
        u_raw = _u_from_vort_3d(omega, grid)
        u_hat = mollify_hat(u_raw, grid, soft_J)
        omg = jnp.fft.ifftn(omega, axes=(1, 2, 3)).real
        tau_phys = jnp.fft.ifftn(tau, axes=(2, 3, 4)).real
        S = strain_tensor(u_hat, grid)
        eta_eff = _strain_source_eta(eta_p, tau_phys, S, nu, lam_g)
        dtau = (_oldroyd_rhs_3d(tau, u_hat, grid, eta_eff, lambda_relax,
                                alpha, beta_scar, stress_diff, clay_gain)
                + _voigt_rhs_3d_sheet(tau, omg, S, grid, a_par, a_perp, g_s)
                + frechet_stress_rhs(tau, tau_phys, grid, eps_fr))
        blended, _ = high_de_blend(tau_phys, omg, S, eta_p, lambda_relax, high_de)
        tau_use = jnp.fft.fftn(blended, axes=(2, 3, 4)) * grid["dealias"]
        tau_f = stress_couple * _stress_vort_force_3d(tau_use, grid)
        f_lb = ik_cross(lb_filtered_div(tau_use, grid, s_LB), grid)
        tau_f = (1.0 - a_LB) * tau_f + a_LB * f_lb * grid["dealias"]
        B_tot = B + B_ext
        B_cross = B + induct_ext * B_ext
        mag_f = (_lorentz_vort_3d(B_tot, grid)
                 + _odd_vort_3d(u_raw, B_tot, grid, eta_odd, berry_gain))
        dw = _rhs_3d(omega, grid, nu_tot, force + tau_f + mag_f)
        dB = _induction_3d(B, u_raw, grid, eta_mag, B_cross, eta_hyper, hyper_kcut)
        glm_on = (glm_ch != 0.0).astype(B.real.dtype)
        dB = dB + glm_grad_psi(psi, grid) * glm_on
        dpsi = glm_psi_rhs(psi, B, grid, glm_ch, glm_cr) * glm_on
        return dw, dtau, dB, dpsi

    if scheme == "euler":
        dw, dtau, dB, dpsi = rhs(omega, tau, B, psi)
        omega, tau, B = omega + dt * dw, tau + dt * dtau, B + dt * dB
        psi = psi + dt * dpsi
    else:
        k1w, k1t, k1b, k1p = rhs(omega, tau, B, psi)
        om_m = omega + dt * k1w
        B_m = B + dt * k1b
        om_p = project_div_free(om_m, grid)
        B_p = project_div_free(B_m, grid)
        om_m = posdiv * om_p + (1.0 - posdiv) * om_m
        B_m = posdiv * B_p + (1.0 - posdiv) * B_m
        k2w, k2t, k2b, k2p = rhs(om_m, tau + dt * k1t, B_m, psi + dt * k1p)
        omega = omega + 0.5 * dt * (k1w + k2w)
        tau = tau + 0.5 * dt * (k1t + k2t)
        B = B + 0.5 * dt * (k1b + k2b)
        psi = psi + 0.5 * dt * (k1p + k2p)
    omega = project_div_free(omega, grid)
    B_proj = project_div_free(B, grid)
    B = jnp.where(glm_ch != 0.0, B * grid["dealias"], B_proj)
    psi = psi * grid["dealias"]
    tau = 0.5 * (tau + jnp.swapaxes(tau, 0, 1))
    return omega, gum_damping(tau, t, gum_scale), B, psi


def coupled_mhd_step(omega_hat, tau_hat, B_hat, grid, nu, dt, force_hat=0,
                     scheme="rk2", t=0.0, eta_p=0.003,
                     lambda_relax=0.6, alpha=0.085,
                     beta_scar=0.13, stress_diff=1e-4,
                     clay_gain=float(DELTA_MIN),
                     gum_scale=1.0, stress_couple=1.0,
                     regs=None, eta_mag=1.0e-3, eta_odd=0.0,
                     B_ext_hat=None, induct_ext=1.0, mu_eff=0.0,
                     berry_gain=0.0, eta_hyper=0.0, posdiv=0.0, hyper_kcut=0.0,
                     psi_hat=None, glm_ch=0.0, glm_cr=0.18):
    """One coupled (omega, tau, B, psi) step. Polymer law unchanged.

    Dedner GLM: psi carries div B as a damped wave (not Lorentz, not projector).

    B_ext_hat is a static freeze-out guide (not time-stepped). Lorentz
    uses B+B_ext; induction stretches B + induct_ext B_ext. mu_eff is an
    additive even viscosity; berry_gain scales odd viscosity with |B|.
    Unmollified u for induction / Lorentz / odd.
    """
    if regs is None:
        regs = _ZERO_REGS
    if B_ext_hat is None:
        B_ext_hat = jnp.zeros_like(B_hat)
    if psi_hat is None:
        psi_hat = jnp.zeros_like(B_hat[0])
    args = (omega_hat, tau_hat, B_hat, grid, nu, dt, force_hat, scheme, t,
            eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
            gum_scale, stress_couple, regs, eta_mag, eta_odd,
            B_ext_hat, induct_ext, mu_eff, berry_gain, eta_hyper, posdiv,
            hyper_kcut, psi_hat, glm_ch, glm_cr)
    if omega_hat.ndim == 2:
        return _coupled_mhd_step_2d(*args)
    return _coupled_mhd_step_3d(*args)

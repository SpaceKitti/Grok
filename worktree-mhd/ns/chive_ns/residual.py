# ============================================================
# @Akitti C*Hive – Hybrid ASGS residual (Sets 1–5, JAX spectral)
# ============================================================

import jax.numpy as jnp
from jax import jit

from .grid import project_div_free, ik_cross, _vort_from_u_2d
from .clay import _div_tau, oldroyd_b_rhs
from .regularisers import (
    mollify_hat, kinematic_lambda, high_de_blend, lb_filtered_div,
    _sheet_order_from_S,
)
from .diagnostics import velocity_gradient, strain_tensor


@jit
def _curl_div_2d(tau_hat, grid):
    return _vort_from_u_2d(_div_tau(tau_hat, grid), grid) * grid["dealias"]


@jit
def _curl_div_3d(tau_hat, grid):
    return ik_cross(_div_tau(tau_hat, grid), grid) * grid["dealias"]


def hybrid_asgs_residual(u_hat, tau_hat, grid, nu, eta_p, lambda_relax,
                         regs=None, force_hat=0, alpha=0.085, beta_scar=0.13,
                         stress_diff=1e-4, clay_gain=0.0, B_hat=None):
    """Three-field residual on the spectral torus.

    R_mom  — vorticity residual of NS + ∇×(∇·τ_reg) + force
    R_con  — ∇·u  (should be ~0 after projection)
    R_const — Oldroyd-B constitutive residual at the current (u,τ)

    Regularisations (regs) hybridise τ → τ_reg before the momentum force:
    J-mollify, high-De core blend, LB second-moment filter.
    """
    p = regs or {}
    axes_u = range(1, u_hat.ndim)
    u = jnp.fft.ifftn(u_hat, axes=axes_u).real
    tau = jnp.fft.ifftn(tau_hat, axes=range(2, tau_hat.ndim)).real
    S = strain_tensor(u_hat, grid)
    if u_hat.ndim == 4:
        from .grid import _vort_from_u_3d
        omega = jnp.fft.ifftn(_vort_from_u_3d(u_hat, grid), axes=(1, 2, 3)).real
        curl_div = _curl_div_3d
    else:
        from .grid import _vort_from_u_2d as v2
        omega = jnp.fft.ifftn(v2(u_hat, grid)).real
        omega = omega[None]
        curl_div = _curl_div_2d

    high_de = float(p.get("high_de", 0.0))
    if high_de > 0.0:
        tau_reg, phi = high_de_blend(
            tau, omega if omega.ndim == tau.ndim - 1 else omega[:1],
            S, eta_p, lambda_relax, high_de)
        tau_reg_hat = jnp.fft.fftn(tau_reg, axes=range(2, tau.ndim)) * grid["dealias"]
    else:
        tau_reg_hat = tau_hat
        phi = jnp.zeros(grid["k2"].shape)

    alpha_LB = float(p.get("alpha_LB", 0.0))
    soft_lb = float(p.get("soft_LB", 0.08))
    f_cont = _div_tau(tau_reg_hat, grid)
    if alpha_LB > 0.0:
        f_lb = lb_filtered_div(tau_reg_hat, grid, soft_lb)
        f_hat = (1.0 - alpha_LB) * f_cont + alpha_LB * f_lb
    else:
        f_hat = f_cont

    div_u = jnp.fft.ifftn(jnp.sum(grid["k_stack"] * u_hat, axis=0)).real
    R_con = div_u
    # momentum residual in vorticity form (force imbalance)
    R_mom = curl_div(tau_reg_hat, grid) + force_hat
    if B_hat is not None:
        from .mhd import lorentz_vorticity_force
        R_mom = R_mom + lorentz_vorticity_force(B_hat, grid)

    R_const = oldroyd_b_rhs(
        tau_hat, u_hat, grid, eta_p, lambda_relax, alpha, beta_scar,
        stress_diff, clay_gain)

    work = jnp.mean(jnp.einsum("ij...,ij...->...", tau, S))
    Z = jnp.mean(jnp.sum(omega**2, axis=0)) if omega.ndim > 2 else jnp.mean(omega**2)
    lam = kinematic_lambda(work, nu, Z)
    asgs_m = float(p.get("asgs_mom", 0.0))
    asgs_c = float(p.get("asgs_const", 0.0))
    R_mom = R_mom - asgs_m * R_mom
    R_const = R_const - asgs_c * R_const
    return {
        "R_mom": R_mom,
        "R_con": R_con,
        "R_const": R_const,
        "tau_reg_hat": tau_reg_hat,
        "force_tau": f_hat,
        "work": work,
        "lambda_kin": lam,
        "phi_core": jnp.mean(phi),
        "max_div": jnp.max(jnp.abs(div_u)),
    }

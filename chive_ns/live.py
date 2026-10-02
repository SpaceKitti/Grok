# ============================================================
# @Akitti C*Hive – Live diagnostics + holographic feedback
# ============================================================

import jax.numpy as jnp
from jax import jit

from .regularisers import kinematic_lambda, _sheet_order_from_S
from .diagnostics import velocity_gradient, strain_tensor
from .clay import _div_tau
from .grid import ik_cross, _vort_from_u_2d, _vort_from_u_3d


@jit
def weighted_bkm_increment(omega_inf, work, sheet_mean, alpha=0.15, beta=0.08, dt=1.0):
    """I += ||ω||_∞ / (1 + α|W| + β(1-s)) dt  (Sets 2–4)."""
    weight = 1.0 + alpha * jnp.abs(work) + beta * (1.0 - sheet_mean)
    return (omega_inf / weight) * dt


@jit
def _live_3d(u_hat, tau_hat, grid, nu, eta_p, lambda_relax, dt,
             I_bkm_w, I_sigma, DeltaF, rho_neg, alpha=0.15, beta=0.08):
    axes = (1, 2, 3)
    u = jnp.fft.ifftn(u_hat, axes=axes).real
    tau = jnp.fft.ifftn(tau_hat, axes=(2, 3, 4)).real
    S = strain_tensor(u_hat, grid)
    omega = jnp.fft.ifftn(_vort_from_u_3d(u_hat, grid), axes=axes).real
    w2 = jnp.sum(omega**2, axis=0)
    omega_inf = jnp.max(jnp.sqrt(w2))
    work = jnp.mean(jnp.einsum("ij...,ij...->...", tau, S))
    Z = jnp.mean(w2)
    lam = kinematic_lambda(work, nu, Z)
    s = jnp.mean(_sheet_order_from_S(S))
    # σ = τ − 2 η_p S  (Liu–Wang stress deviation)
    sigma = tau - 2.0 * eta_p * S
    sigma_inf = jnp.max(jnp.abs(sigma))
    I_sigma = I_sigma + sigma_inf * dt
    I_bkm_w = I_bkm_w + weighted_bkm_increment(omega_inf, work, s, alpha, beta, dt)
    # Γ = ω − Rτ, R = curl∘div / (k²-scaled)
    src = ik_cross(_div_tau(tau_hat, grid), grid)
    src_phys = jnp.fft.ifftn(src, axes=axes).real
    scale = lambda_relax / (eta_p + 1e-12)
    Gamma = jnp.mean(jnp.sqrt(jnp.sum((omega - scale * src_phys)**2, axis=0)))
    n_tau = jnp.sqrt(jnp.mean(jnp.sum(tau**2, axis=(0, 1))))
    n_S = jnp.sqrt(jnp.mean(jnp.sum(S**2, axis=(0, 1))))
    n_eps = jnp.sqrt(jnp.mean(jnp.sum(sigma**2, axis=(0, 1))))
    ratio = n_eps / (n_tau + 1e-30)
    # holographic injection
    DeltaF = DeltaF + 0.08 * work * (ratio ** 0.5) + 0.1 * I_bkm_w
    rho_neg = rho_neg * (1.0 + 0.15 * work)
    Tstar = jnp.maximum(0.0, 1.0 / (jnp.abs(ratio - 0.5) + 1e-3) - 1.0)
    newtonian = (ratio < 0.01)
    return {
        "work": work,
        "lambda_kin": lam,
        "sheet_order": s,
        "I_bkm_w": I_bkm_w,
        "I_sigma": I_sigma,
        "sigma_inf": sigma_inf,
        "Gamma": Gamma,
        "eps_ratio": ratio,
        "Tstar": Tstar,
        "DeltaF": DeltaF,
        "rho_neg": rho_neg,
        "newtonian": newtonian,
        "n_tau": n_tau,
        "n_S": n_S,
    }


@jit
def _live_2d(u_hat, tau_hat, grid, nu, eta_p, lambda_relax, dt,
             I_bkm_w, I_sigma, DeltaF, rho_neg, alpha=0.15, beta=0.08):
    u = jnp.fft.ifftn(u_hat, axes=(1, 2)).real
    tau = jnp.fft.ifftn(tau_hat, axes=(2, 3)).real
    S = strain_tensor(u_hat, grid)
    vort = jnp.fft.ifftn(_vort_from_u_2d(u_hat, grid)).real
    omega_inf = jnp.max(jnp.abs(vort))
    work = jnp.mean(jnp.einsum("ij...,ij...->...", tau, S))
    Z = jnp.mean(vort**2)
    lam = kinematic_lambda(work, nu, Z)
    s = jnp.mean(_sheet_order_from_S(S))
    sigma = tau - 2.0 * eta_p * S
    sigma_inf = jnp.max(jnp.abs(sigma))
    I_sigma = I_sigma + sigma_inf * dt
    I_bkm_w = I_bkm_w + weighted_bkm_increment(omega_inf, work, s, alpha, beta, dt)
    n_tau = jnp.sqrt(jnp.mean(jnp.sum(tau**2, axis=(0, 1))))
    n_eps = jnp.sqrt(jnp.mean(jnp.sum(sigma**2, axis=(0, 1))))
    ratio = n_eps / (n_tau + 1e-30)
    DeltaF = DeltaF + 0.08 * work + 0.1 * I_bkm_w
    rho_neg = rho_neg * (1.0 + 0.15 * work)
    return {
        "work": work,
        "lambda_kin": lam,
        "sheet_order": s,
        "I_bkm_w": I_bkm_w,
        "I_sigma": I_sigma,
        "sigma_inf": sigma_inf,
        "Gamma": jnp.array(0.0),
        "eps_ratio": ratio,
        "Tstar": jnp.maximum(0.0, 1.0 / (jnp.abs(ratio - 0.5) + 1e-3) - 1.0),
        "DeltaF": DeltaF,
        "rho_neg": rho_neg,
        "newtonian": ratio < 0.01,
        "n_tau": n_tau,
        "n_S": jnp.sqrt(jnp.mean(jnp.sum(S**2, axis=(0, 1)))),
    }


def live_diagnostics_and_feedback(u_hat, tau_hat, grid, nu, eta_p, lambda_relax,
                                  dt, carry=None, alpha=0.15, beta=0.08):
    """Live monitors + holographic (ΔF, ρ_neg) update. 2D/3D."""
    if carry is None:
        carry = dict(I_bkm_w=0.0, I_sigma=0.0, DeltaF=0.0, rho_neg=1.0)
    args = (u_hat, tau_hat, grid, nu, eta_p, lambda_relax, dt,
            carry["I_bkm_w"], carry["I_sigma"], carry["DeltaF"],
            carry["rho_neg"], alpha, beta)
    if int(grid["dim"]) == 2:
        return _live_2d(*args)
    return _live_3d(*args)


def _zero_live():
    z = jnp.array(0.0)
    return {
        "work": z, "lambda_kin": z,
        "I_bkm_w": z, "I_sigma": z, "sigma_inf": z, "Gamma": z,
        "eps_ratio": z, "Tstar": z, "DeltaF": z, "rho_neg": jnp.array(1.0),
        "newtonian": z, "n_tau": z, "n_S": z,
    }

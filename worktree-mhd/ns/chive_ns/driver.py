# ============================================================
# @Akitti C*Hive – Unified Driver
# ============================================================

import jax
import jax.numpy as jnp
from jax import random

from .grid import (
    make_grid, project_div_free, generate_smooth_div_free_u0,
    generate_taylor_green, generate_antiparallel_tubes,
    velocity_from_vorticity, vorticity_from_velocity, cfl_dt,
    paper_ni_ic, paper_sigma_c,
)
from .vorticity import (
    modest_liar, z7_braid_forcing, ns_vorticity_step,
    coupled_vorticity_stress_step, coupled_mhd_step, coupled_twofluid_step,
    resolve_scar_centres,
)
from .clay import DEFAULT_CLAY, zero_tau_hat
from .bubble import coupled_rp_attractor_rhs
from .diagnostics import field_diagnostics, millennium_series, sample_times
from .live import live_diagnostics_and_feedback, _zero_live
from .constants import DELTA_MIN
from .mhd import (
    DEFAULT_MHD, generate_b0, generate_u_ot, generate_u_alfven,
    zero_b_hat, zero_psi_hat,
    mhd_field_diagnostics, _zero_mhd, cfl_dt_mhd, split_guide_fields,
)
from .es_lhdi import es_placeholder_diagnostics
from .compressible import (
    uniform_rho_hat, bump_rho_hat, uniform_p_hat, bump_p_hat, coupled_cmhd_step,
    density_diagnostics, energy_diagnostics, heating_Q, GAMMA_DEFAULT,
    sound_wave_fields, brio_wu_fields, cfl_dt_cmhd,
)


_TUBE_KEYS = ("circulation", "radius", "separation", "perturbation", "axial_wave")
_REG_KEYS = (
    "soft_J", "alpha_par", "alpha_perp", "gamma_s", "epsilon_frechet",
    "high_de", "alpha_LB", "soft_LB", "lam_kin_gain",
)
_REG_DEFAULTS = (0.004, 0.0, 3e-4, 1.5, 0.0, 0.08, 0.08, 0.05, 0.10)


def _regs_from_params(p):
    return jnp.array([p.get(k, d) for k, d in zip(_REG_KEYS, _REG_DEFAULTS)],
                     dtype=jnp.float64)


def _snapshot_ns(omega_hat, grid):
    u_hat = velocity_from_vorticity(omega_hat, grid)
    d = field_diagnostics(u_hat, grid, tau_hat=None)
    d.update(_zero_live())
    d.update(_zero_mhd())
    d.update(es_placeholder_diagnostics())
    return d


def _snapshot_clay(state, grid, nu, clay_params):
    omega_hat, tau_hat = state
    u_hat = velocity_from_vorticity(omega_hat, grid)
    d = field_diagnostics(u_hat, grid, tau_hat=tau_hat)
    live = live_diagnostics_and_feedback(
        u_hat, tau_hat, grid, nu, clay_params["eta_p"],
        clay_params["lambda_relax"], 0.0)
    d.update(live)
    d.update(_zero_mhd())
    d.update(es_placeholder_diagnostics())
    return d


def _snapshot_mhd(state, grid, nu, clay_params, mhd_params, B_ext_hat, u_hat=None):
    omega_hat, tau_hat, B_hat = state[0], state[1], state[2]
    psi_hat = state[3] if len(state) > 3 else None
    if u_hat is None:
        u_hat = velocity_from_vorticity(omega_hat, grid)
    d = field_diagnostics(u_hat, grid, tau_hat=tau_hat)
    live = live_diagnostics_and_feedback(
        u_hat, tau_hat, grid, nu, clay_params["eta_p"],
        clay_params["lambda_relax"], 0.0)
    d.update(live)
    d.update(mhd_field_diagnostics(
        B_hat, u_hat, grid, mhd_params["eta_mag"], tau_hat, B_ext_hat,
        eta_hyper=float(mhd_params.get("eta_hyper", 0.0))))
    R = float(mhd_params.get("tube_radius", 0.08))
    G0 = float(mhd_params.get("tube_circulation", 0.7))
    Gm0 = float(mhd_params.get("gamma_m", 0.0))
    eta = float(mhd_params["eta_mag"])
    d["ni_paper0"] = jnp.array(paper_ni_ic(G0, Gm0, eta, R))
    area = jnp.pi * R * R
    sig = paper_sigma_c(R)
    Gt = d["max_vort"] * area
    Gmt = d["max_b"] * area
    d["ni_paper"] = Gmt**2 / (Gt * eta * sig * sig + 1e-30)
    # Dimensionless Lorentz/inertia: <|J×B|> / (ρ u²/ℓ), ℓ=σ_c, ρ=1.
    d["ni_li"] = d["N_i_force"] * sig
    L = float(grid["L"])
    u_rms = jnp.sqrt(2.0 * d["energy"])
    v_A = jnp.sqrt(2.0 * d["e_mag_tot"])
    d["Re"] = u_rms * L / (nu + 1e-30)
    d["Rm"] = u_rms * L / (eta + 1e-30)
    d["Pr_m"] = jnp.array(nu / (eta + 1e-30))
    d["v_A"] = v_A
    d["lundquist"] = L * v_A / (eta + 1e-30)
    d["plasma_beta"] = 2.0 * d["energy"] / (d["e_mag_tot"] + 1e-30)
    d.update(es_placeholder_diagnostics())
    glm_ch = float(mhd_params.get("glm_ch", 0.0))
    if psi_hat is not None and glm_ch != 0.0:
        psi = jnp.fft.ifftn(psi_hat).real
        d["max_psi"] = jnp.max(jnp.abs(psi))
        d["e_glm"] = 0.5 * jnp.mean(psi ** 2) / (glm_ch ** 2 + 1e-30)
    else:
        d["max_psi"] = jnp.array(0.0)
        d["e_glm"] = jnp.array(0.0)
    return d


def _initial_velocity(key, grid, ic, dim, ic_params=None, mhd_params=None):
    p = ic_params or {}
    if ic == "ot":
        U0 = float((mhd_params or {}).get("ot_u0", p.get("ot_u0", 1.0)))
        return generate_u_ot(grid, U0=U0)
    if ic == "alfven":
        amp = float((mhd_params or {}).get("alfven_amp", p.get("alfven_amp", 0.01)))
        return generate_u_alfven(grid, amp=amp)
    if dim == 3 and ic == "taylor_green":
        return generate_taylor_green(grid, scale=p.get("scale", 1.0))
    if dim == 3 and ic == "tubes":
        return generate_antiparallel_tubes(
            grid, **{k: p[k] for k in _TUBE_KEYS if k in p})
    if ic == "sound":
        eps = float(p.get("sound_eps", 1e-3))
        rho0 = float(p.get("rho0", 1.0))
        p0 = float((mhd_params or {}).get("p0", p.get("p0", 1.0)))
        gamma = float((mhd_params or {}).get("gamma", GAMMA_DEFAULT))
        u, _rho, _p, _cs = sound_wave_fields(
            grid, eps=eps, rho0=rho0, p0=p0, gamma=gamma)
        return u
    if ic == "brio_wu":
        gamma = float((mhd_params or {}).get(
            "gamma", p.get("gamma", 2.0)))
        u, _rho, _p, _B = brio_wu_fields(grid, gamma=gamma)
        return u
    return generate_smooth_div_free_u0(key, grid, scale=p.get("u_scale", 0.008))


def _scan_loop(advance, snapshot, state0, steps, diag_every):
    """Chunked lax.scan with a t=0 snapshot. `advance(state, idx) -> state`."""
    n_chunks = int(steps // diag_every)
    remainder = int(steps % diag_every)
    d0 = snapshot(state0)

    def chunk(state, cidx):
        start = cidx * diag_every

        def one(state, j):
            return advance(state, start + j), None

        state, _ = jax.lax.scan(one, state, jnp.arange(diag_every))
        return state, snapshot(state)

    if n_chunks:
        state, hist = jax.lax.scan(chunk, state0, jnp.arange(n_chunks))
        hist = jax.tree.map(lambda a, b: jnp.concatenate([a[None], b]), d0, hist)
    else:
        state, hist = state0, jax.tree.map(lambda v: v[None], d0)
    if remainder:
        start = n_chunks * diag_every

        def tail(state, j):
            return advance(state, start + j), None

        state, _ = jax.lax.scan(tail, state, jnp.arange(remainder))
        last = snapshot(state)
        hist = jax.tree.map(lambda a, b: jnp.concatenate([a, b[None]]), hist, last)
    return state, hist


def _run_vorticity_scanned(omega_hat, grid, nu, dt, steps, force_on,
                           scheme, diag_every, n_scars=1, scar_centres=None,
                           force_amp=1.0):
    """Pure NS stretching loop."""
    force_pat = z7_braid_forcing(grid, 1.0, n_scars=n_scars,
                                 scar_centres=scar_centres)
    force_scale = (1.0 if force_on else 0.0) * float(force_amp)

    def advance(omega_hat, idx):
        t_norm = idx / jnp.maximum(steps - 1, 1)
        force = force_pat * (modest_liar(t_norm) * force_scale)
        return ns_vorticity_step(omega_hat, grid, nu, dt, force, scheme)

    def snapshot(omega_hat):
        return _snapshot_ns(omega_hat, grid)

    return _scan_loop(advance, snapshot, omega_hat, steps, diag_every)


def _run_clay_scanned(omega_hat, tau_hat, grid, nu, dt, steps, force_on,
                      scheme, diag_every, clay_params, n_scars=1,
                      scar_centres=None, force_amp=1.0):
    """Coupled NS stretching + Oldroyd-B extra-stress loop."""
    force_pat = z7_braid_forcing(grid, 1.0, n_scars=n_scars,
                                 scar_centres=scar_centres)
    force_scale = (1.0 if force_on else 0.0) * float(force_amp)
    eta_p = clay_params["eta_p"]
    lambda_relax = clay_params["lambda_relax"]
    alpha = clay_params["alpha"]
    beta_scar = clay_params["beta_scar"]
    stress_diff = clay_params["stress_diff"]
    clay_gain = clay_params["clay_gain"]
    gum_scale = clay_params.get("gum_scale", 1.0)
    stress_couple = clay_params.get("stress_couple", 1.0)
    regs = _regs_from_params(clay_params)

    def advance(state, idx):
        omega_hat, tau_hat = state
        t = idx * dt
        t_norm = idx / jnp.maximum(steps - 1, 1)
        force = force_pat * (modest_liar(t_norm) * force_scale)
        return coupled_vorticity_stress_step(
            omega_hat, tau_hat, grid, nu, dt, force, scheme, t,
            eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
            gum_scale, stress_couple, regs)

    def snapshot(state):
        return _snapshot_clay(state, grid, nu, clay_params)

    return _scan_loop(advance, snapshot, (omega_hat, tau_hat), steps, diag_every)


def _run_mhd_scanned(omega_hat, tau_hat, B_hat, grid, nu, dt, steps, force_on,
                     scheme, diag_every, clay_params, mhd_params, n_scars=1,
                     scar_centres=None, force_amp=1.0, B_ext_hat=None,
                     induct_ext=1.0):
    """Coupled NS + Oldroyd-B + induction / Lorentz loop."""
    force_pat = z7_braid_forcing(grid, 1.0, n_scars=n_scars,
                                 scar_centres=scar_centres)
    force_scale = (1.0 if force_on else 0.0) * float(force_amp)
    eta_p = clay_params["eta_p"]
    lambda_relax = clay_params["lambda_relax"]
    alpha = clay_params["alpha"]
    beta_scar = clay_params["beta_scar"]
    stress_diff = clay_params["stress_diff"]
    clay_gain = clay_params["clay_gain"]
    gum_scale = clay_params.get("gum_scale", 1.0)
    stress_couple = clay_params.get("stress_couple", 1.0)
    regs = _regs_from_params(clay_params)
    eta_mag = mhd_params["eta_mag"]
    eta_odd = mhd_params["eta_odd"]
    mu_eff = float(mhd_params.get("mu_eff", 0.0))
    berry_gain = float(mhd_params.get("berry_gain", 0.0))
    eta_hyper = float(mhd_params.get("eta_hyper", 0.0))
    posdiv = float(mhd_params.get("posdiv", 0.0))
    hyper_kcut = float(mhd_params.get("hyper_kcut", 0.0))
    glm_ch = float(mhd_params.get("glm_ch", 0.0))
    glm_cr = float(mhd_params.get("glm_cr", 0.18))
    d_i = float(mhd_params.get("d_i", 0.0))
    n_hall = float(mhd_params.get("n_hall", mhd_params.get("n", 1.0)))
    if B_ext_hat is None:
        B_ext_hat = zero_b_hat(grid, dtype=omega_hat.dtype)
    psi0 = zero_psi_hat(grid, dtype=omega_hat.dtype)

    def advance(state, idx):
        omega_hat, tau_hat, B_hat, psi_hat = state
        t = idx * dt
        t_norm = idx / jnp.maximum(steps - 1, 1)
        force = force_pat * (modest_liar(t_norm) * force_scale)
        return coupled_mhd_step(
            omega_hat, tau_hat, B_hat, grid, nu, dt, force, scheme, t,
            eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
            gum_scale, stress_couple, regs, eta_mag, eta_odd,
            B_ext_hat, induct_ext, mu_eff, berry_gain, eta_hyper, posdiv,
            hyper_kcut, psi_hat, glm_ch, glm_cr, d_i, n_hall)

    def snapshot(state):
        return _snapshot_mhd(state, grid, nu, clay_params, mhd_params, B_ext_hat)

    return _scan_loop(advance, snapshot, (omega_hat, tau_hat, B_hat, psi0),
                      steps, diag_every)


def _snapshot_twofluid(state, grid, nu, clay_params, mhd_params, B_ext_hat):
    """MHD snapshot plus quasi-neutral n_i = n_e meters. No pin/floor."""
    omega_hat, tau_hat, B_hat, psi_hat, n_i_hat = state
    d = _snapshot_mhd(
        (omega_hat, tau_hat, B_hat, psi_hat), grid, nu, clay_params,
        mhd_params, B_ext_hat)
    u_hat = velocity_from_vorticity(omega_hat, grid)
    d.update(density_diagnostics(n_i_hat, u_hat, grid))
    n = jnp.fft.ifftn(n_i_hat).real
    d["min_n_i"] = jnp.min(n)
    d["min_n_e"] = jnp.min(n)
    d["mean_n_i"] = jnp.mean(n)
    d["mean_n_e"] = jnp.mean(n)
    d["max_n_i"] = jnp.max(n)
    d["max_n_e"] = jnp.max(n)
    return d


def _run_twofluid_scanned(omega_hat, tau_hat, B_hat, n_i_hat, grid, nu, dt,
                          steps, force_on, scheme, diag_every, clay_params,
                          mhd_params, n_scars=1, scar_centres=None,
                          force_amp=1.0, B_ext_hat=None, induct_ext=1.0):
    """Hall vorticity MHD + twofluid Ohm + continuity on n_i."""
    force_pat = z7_braid_forcing(grid, 1.0, n_scars=n_scars,
                                 scar_centres=scar_centres)
    force_scale = (1.0 if force_on else 0.0) * float(force_amp)
    eta_p = clay_params["eta_p"]
    lambda_relax = clay_params["lambda_relax"]
    alpha = clay_params["alpha"]
    beta_scar = clay_params["beta_scar"]
    stress_diff = clay_params["stress_diff"]
    clay_gain = clay_params["clay_gain"]
    gum_scale = clay_params.get("gum_scale", 1.0)
    stress_couple = clay_params.get("stress_couple", 1.0)
    regs = _regs_from_params(clay_params)
    eta_mag = mhd_params["eta_mag"]
    eta_odd = mhd_params["eta_odd"]
    mu_eff = float(mhd_params.get("mu_eff", 0.0))
    berry_gain = float(mhd_params.get("berry_gain", 0.0))
    eta_hyper = float(mhd_params.get("eta_hyper", 0.0))
    posdiv = float(mhd_params.get("posdiv", 0.0))
    hyper_kcut = float(mhd_params.get("hyper_kcut", 0.0))
    glm_ch = float(mhd_params.get("glm_ch", 0.0))
    glm_cr = float(mhd_params.get("glm_cr", 0.18))
    d_i = float(mhd_params.get("d_i", 0.0))
    T_e = float(mhd_params.get("T_e", 0.0))
    if B_ext_hat is None:
        B_ext_hat = zero_b_hat(grid, dtype=omega_hat.dtype)
    psi0 = zero_psi_hat(grid, dtype=omega_hat.dtype)

    def advance(state, idx):
        omega_hat, tau_hat, B_hat, psi_hat, n_i_hat = state
        t = idx * dt
        t_norm = idx / jnp.maximum(steps - 1, 1)
        force = force_pat * (modest_liar(t_norm) * force_scale)
        return coupled_twofluid_step(
            omega_hat, tau_hat, B_hat, n_i_hat, grid, nu, dt, force, scheme, t,
            eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
            gum_scale, stress_couple, regs, eta_mag, eta_odd,
            B_ext_hat, induct_ext, mu_eff, berry_gain, eta_hyper, posdiv,
            hyper_kcut, psi_hat, glm_ch, glm_cr, d_i, T_e)

    def snapshot(state):
        return _snapshot_twofluid(state, grid, nu, clay_params, mhd_params,
                                  B_ext_hat)

    return _scan_loop(
        advance, snapshot,
        (omega_hat, tau_hat, B_hat, psi0, n_i_hat),
        steps, diag_every)


def _snapshot_cmhd(state, grid, nu, clay_params, mhd_params, B_ext_hat, gamma):
    u_hat, tau_hat, B_hat, psi_hat, rho_hat, p_hat = state
    omega_hat = vorticity_from_velocity(u_hat, grid)
    d = _snapshot_mhd(
        (omega_hat, tau_hat, B_hat, psi_hat), grid, nu, clay_params,
        mhd_params, B_ext_hat, u_hat=u_hat)
    d.update(density_diagnostics(rho_hat, u_hat, grid))
    d.update(energy_diagnostics(rho_hat, p_hat, gamma, u_hat=u_hat))
    Q = heating_Q(u_hat, B_hat, grid, mhd_params["eta_mag"], nu, B_ext_hat)
    d["mean_Q"] = jnp.mean(Q)
    return d


def _run_cmhd_scanned(u_hat, tau_hat, B_hat, rho_hat, p_hat, grid, nu, dt, steps,
                      force_on, scheme, diag_every, clay_params, mhd_params,
                      n_scars=1, scar_centres=None, force_amp=1.0,
                      B_ext_hat=None, induct_ext=1.0, gamma=GAMMA_DEFAULT):
    """Primitive-u compressible MHD: Qin/Helmholtz off on u.

    dt u = -(u·∇)u - ∇p/ρ + (J×B)/ρ + ν ∇²u. Continuity + Russell p stay.
    force_pat is converted from vorticity space to velocity space.
    mode="mhd" is not this loop.
    """
    force_pat = z7_braid_forcing(grid, 1.0, n_scars=n_scars,
                                 scar_centres=scar_centres)
    force_u_pat = velocity_from_vorticity(force_pat, grid)
    force_scale = (1.0 if force_on else 0.0) * float(force_amp)
    eta_p = clay_params["eta_p"]
    lambda_relax = clay_params["lambda_relax"]
    alpha = clay_params["alpha"]
    beta_scar = clay_params["beta_scar"]
    stress_diff = clay_params["stress_diff"]
    clay_gain = clay_params["clay_gain"]
    gum_scale = clay_params.get("gum_scale", 1.0)
    stress_couple = clay_params.get("stress_couple", 1.0)
    regs = _regs_from_params(clay_params)
    eta_mag = mhd_params["eta_mag"]
    eta_odd = mhd_params["eta_odd"]
    mu_eff = float(mhd_params.get("mu_eff", 0.0))
    berry_gain = float(mhd_params.get("berry_gain", 0.0))
    eta_hyper = float(mhd_params.get("eta_hyper", 0.0))
    posdiv = float(mhd_params.get("posdiv", 0.0))
    hyper_kcut = float(mhd_params.get("hyper_kcut", 0.0))
    glm_ch = float(mhd_params.get("glm_ch", 0.0))
    glm_cr = float(mhd_params.get("glm_cr", 0.18))
    if B_ext_hat is None:
        B_ext_hat = zero_b_hat(grid, dtype=u_hat.dtype)
    psi0 = zero_psi_hat(grid, dtype=u_hat.dtype)

    def advance(state, idx):
        u_hat, tau_hat, B_hat, psi_hat, rho_hat, p_hat = state
        t = idx * dt
        t_norm = idx / jnp.maximum(steps - 1, 1)
        force = force_u_pat * (modest_liar(t_norm) * force_scale)
        return coupled_cmhd_step(
            u_hat, tau_hat, B_hat, rho_hat, p_hat, grid, nu, dt, force, scheme, t,
            eta_p, lambda_relax, alpha, beta_scar, stress_diff, clay_gain,
            gum_scale, stress_couple, regs, eta_mag, eta_odd,
            B_ext_hat, induct_ext, mu_eff, berry_gain, eta_hyper, posdiv,
            hyper_kcut, psi_hat, glm_ch, glm_cr, gamma)

    def snapshot(state):
        return _snapshot_cmhd(state, grid, nu, clay_params, mhd_params, B_ext_hat, gamma)

    return _scan_loop(
        advance, snapshot, (u_hat, tau_hat, B_hat, psi0, rho_hat, p_hat),
        steps, diag_every)


_MHD_HIST = (
    "e_mag", "e_mag_ext", "e_mag_tot", "ohmic", "hyper_ohmic", "max_j", "max_b",
    "H_mag", "H_cross", "H_current", "max_div_b", "lorentz_work",
    "maxwell", "op_ratio", "N_i", "N_i_force", "ni_paper", "ni_paper0",
    "ni_li", "Re", "Rm", "Pr_m", "v_A", "lundquist", "plasma_beta",
    "lam_min", "lam_min_dx",
    "P_back", "b_stretch", "b_comp", "b_stretch_j", "b_comp_j",
    "wl_j", "K_sheet", "j_w", "j_over_b_w", "sheet_ind",
    "max_e", "max_charge", "es_energy", "edge_j",
    "flux_x_half", "flux_y_half", "flux_z_half",
    "circ_x_half", "circ_y_half",
    "E_rec", "E_par", "E_rec_sheet",
    "e_glm", "max_psi",
)

_CMHD_HIST = (
    "mean_rho", "max_rho", "min_rho", "max_abs_rho_m1", "max_drho_dt",
    "e_int", "e_kin", "p", "gamma", "mean_p", "min_p", "mean_e_int", "mean_Q",
)

_TWOFLUID_HIST = (
    "min_n_i", "min_n_e", "mean_n_i", "mean_n_e", "max_n_i", "max_n_e",
)


def _pack_out(hist, u_hat, omega_hat, tau_hat, grid, dt, N, nu, ic, scheme,
              viscoelastic, clay_params, steps, diag_every, n_scars,
              scar_centres, force_on, B_hat=None, mhd_params=None,
              magnetic=False, rho_hat=None, p_hat=None, n_i_hat=None):
    time = sample_times(hist["energy"].shape[0], steps, dt, diag_every)
    mill = millennium_series(hist, time, nu)
    out = {
        "energy": hist["energy"],
        "enstrophy": hist["enstrophy"],
        "ipr": hist["ipr"],
        "helicity": hist["helicity"],
        "max_vort": hist["max_vort"],
        "stretch": hist["stretch"],
        "max_div": hist["max_div"],
        "lambda2_neg_frac": hist["lambda2_neg_frac"],
        "mean_tau": hist["mean_tau"],
        "max_tau": hist["max_tau"],
        "tau_s": hist["tau_s"],
        "max_strain": mill["max_strain"],
        "palinstrophy": mill["palinstrophy"],
        "bkm_integral": mill["bkm_integral"],
        "dZ_dt": mill["dZ_dt"],
        "dE_dt": mill["dE_dt"],
        "dE_tot_dt": mill["dE_tot_dt"],
        "e_tot": mill["e_tot"],
        "eps_nu": mill["eps_nu"],
        "I_nu": mill["I_nu"],
        "I_eta": mill["I_eta"],
        "I_tau": mill["I_tau"],
        "energy_leak": mill["energy_leak"],
        "I_leak": mill["I_leak"],
        "rec_rate_flux": mill.get("rec_rate_flux", mill["time"] * 0.0),
        "dissipation": mill["dissipation"],
        "dZ_dt_budget": mill["dZ_dt_budget"],
        "I_bkm_w": mill["I_bkm_w"],
        "I_sigma": mill["I_sigma"],
        "sheet_order": mill["sheet_order"],
        "work": mill["work"],
        "lambda_kin": mill["lambda_kin"],
        "eps_ratio": mill["eps_ratio"],
        "Gamma": mill["Gamma"],
        "Tstar": hist.get("Tstar", mill["time"] * 0.0),
        "time": mill["time"],
        "u_hat": u_hat,
        "omega_hat": omega_hat,
        "tau_hat": tau_hat,
        "B_hat": B_hat,
        "grid": grid,
        "dt": dt,
        "N": N,
        "nu": nu,
        "ic": ic,
        "scheme": scheme,
        "viscoelastic": viscoelastic,
        "magnetic": magnetic,
        "clay_params": clay_params,
        "mhd_params": mhd_params,
        "n_scars": n_scars,
        "scar_centres": scar_centres,
        "force_on": force_on,
    }
    z = mill["time"] * 0.0
    for k in _MHD_HIST:
        out[k] = hist.get(k, z)
    for k in _CMHD_HIST:
        out[k] = hist.get(k, z)
    for k in _TWOFLUID_HIST:
        out[k] = hist.get(k, z)
    out["rho_hat"] = rho_hat
    out["p_hat"] = p_hat
    out["n_i_hat"] = n_i_hat
    out["n_e_hat"] = n_i_hat
    # PATCH 7 Venus (cmhd only). mill I_leak above stays the two-bucket
    # MHD identity: (e_tot+e_glm - that[0]) + I_nu + I_eta + I_tau.
    # Heat already sits in E_int, so do NOT add int(eps_nu+eps_eta).
    if "e_kin" in hist:
        e_kin = hist["e_kin"]
        e_int = hist["e_int"]
        e_mag = hist.get("e_mag_tot", hist.get("e_mag", z))
        e_glm = hist.get("e_glm", z)
        e_cons_c = e_kin + e_int + e_mag + e_glm
        out["I_leak"] = e_cons_c - e_cons_c[0]
        out["e_cons_cmhd"] = e_cons_c
    return out


def run_framework(N=None, dim=2, steps=800, mode="vorticity",
                  nu=None, dt=None, seed=42, force_on=True,
                  bubble_params=None, ic=None, scheme=None,
                  cfl=0.4, diag_every=20, viscoelastic=None,
                  clay_params=None, ic_params=None,
                  n_scars=1, scar_centres=None, force_amp=1.0,
                  magnetic=None, mhd_params=None):
    """
    mode = "vorticity"   → rotational-form NS (full 3D stretching)
         = "clay"        → same NS + Oldroyd-B E-brane extra-stress
         = "hybrid"      → alias for clay (λ₂ is always recorded in 3D)
         = "mhd"         → NS + (optional clay) + induction / Lorentz
         = "hall"        -> same vorticity MHD path as mode="mhd" with Hall Ohm
                            E = -u x B + eta J + (d_i/n) J x B; d_i=0 matches mhd
         = "twofluid"    -> hall path + electron pressure in Ohm (no inertia)
                            E = -u_e x B - grad(p_e)/n + eta J, u_e = u_i - (d_i/n) J
                            p_e = n T_e, T_e=0 matches hall; continuity on n_i=n_e
         = "cmhd" / "compressible" → primitive-u MHD + continuity + Russell p (Qin off)
         = "bubble"      → pure RP + Liu–Sun tower

    viscoelastic=True forces the clay coupling even if mode="vorticity".
    magnetic=True forces the MHD layer (induction + Lorentz + helicity).
    mode="mhd" or mode="hall" or mode="twofluid" implies magnetic=True; clay stays on unless viscoelastic=False.
    ic = "taylor_green" | "tubes" | "smooth" | "ot" | "alfven" | "sound" | "brio_wu".  tubes = Crow-perturbed
    anti-parallel pair. ot = Orszag-Tang u matching generate_b0(kind='ot').
    alfven = small transverse δv=-δb on the uniform guide (v_A = |B0|).
    brio_wu = Brio-Wu 1988 1D MHD Riemann on the torus (cmhd; paper gamma=2 test-local; stop before wrap; spectral ringing expected).
    n_scars / scar_centres select the helical Z₇ lattice (n_scars=1 default).
    dim=3 defaults: N=64, Taylor–Green IC, RK2, CFL dt, helical Z₇ force.
    """
    if magnetic is None:
        magnetic = mode in ("mhd", "hall", "twofluid")
    if viscoelastic is None:
        viscoelastic = mode in ("clay", "hybrid", "mhd", "hall", "twofluid")
    is_cmhd = mode in ("cmhd", "compressible")
    is_twofluid = mode == "twofluid"
    if is_cmhd:
        # Primitive u + continuity + Russell p. Qin off. mode="mhd" unchanged.
        magnetic = True
    if mode == "hybrid":
        mode = "clay" if viscoelastic else "vorticity"
    if clay_params is None:
        clay_params = dict(DEFAULT_CLAY)
    else:
        merged = dict(DEFAULT_CLAY)
        merged.update(clay_params)
        clay_params = merged
    if mhd_params is None:
        mhd_params = dict(DEFAULT_MHD)
    else:
        merged_m = dict(DEFAULT_MHD)
        merged_m.update(mhd_params)
        mhd_params = merged_m
    if ic_params:
        _map = (("radius", "tube_radius"), ("circulation", "tube_circulation"),
                ("separation", "tube_separation"),
                ("perturbation", "tube_perturbation"),
                ("axial_wave", "tube_axial_wave"))
        for src, dst in _map:
            if src in ic_params:
                mhd_params[dst] = ic_params[src]

    if N is None:
        N = 64 if dim == 3 else 32
    if nu is None:
        nu = 5e-4 if dim == 3 else 0.001
    if ic is None:
        ic = "taylor_green" if dim == 3 else "smooth"
    if ic == "ot":
        mhd_params["b_guide"] = "ot"
    if ic == "alfven":
        mhd_params["b_guide"] = "alfven"
    if scheme is None:
        scheme = "rk2" if (dim == 3 or viscoelastic or is_cmhd) else "euler"

    grid = make_grid(N, L=1.0 if mode != "bubble" else 2 * jnp.pi, dim=dim)
    key = random.PRNGKey(seed)

    if mode == "bubble":
        p = bubble_params or {
            "rho": 1000., "sigma": 0.072, "mu": 0.001,
            "Pg0": 1.01325e5, "R0": 1e-5, "kappa": 1.4,
            "P0": 1.01325e5, "Pa": 1.2e5, "omega": 2 * jnp.pi * 20e3,
            "omega1_r": 2 * jnp.pi * 20e3, "omega1_i": 5e3,
            "alpha": 0.125, "n_max": 8, "beta": 0.05,
            "scar_floor": DELTA_MIN, "mu_visc": 0.01, "drive": 0.1
        }
        y = jnp.array([p["R0"], 0.0, 1.0])
        hist = []
        bubble_dt = dt if dt is not None else 0.005
        for step in range(steps):
            t = step * bubble_dt
            y = y + bubble_dt * coupled_rp_attractor_rhs(y, t, p)
            if step % 20 == 0:
                hist.append(y)
        return {"traj": jnp.stack(hist), "params": p}

    u0 = _initial_velocity(key, grid, ic, dim, ic_params, mhd_params)
    B_hat = None
    B_ext_hat = None
    induct_ext = 1.0
    psi_hat = None
    rho_hat = None
    p_hat = None
    n_i_hat = None
    if magnetic:
        B_hat, B_ext_hat, induct_ext = split_guide_fields(
            grid, mhd_params, ic_params)
        d_i_run = float(mhd_params.get("d_i", 0.0))
        # 2.5D pad: in-plane Hall Faraday is identically 0, so Bz is
        # required for whistlers. mode=mhd / d_i=0 stay 2-comp.
        if (not is_cmhd) and dim == 2 and d_i_run != 0.0 and B_hat.shape[0] == 2:
            z = jnp.zeros_like(B_hat[0])
            B_hat = jnp.concatenate([B_hat, z[None]], axis=0)
            B_ext_hat = jnp.concatenate([B_ext_hat, z[None]], axis=0)
        if is_cmhd and ic == "brio_wu":
            _u_bw, _rho_bw, _p_bw, B_bw = brio_wu_fields(
                grid, gamma=float(mhd_params.get("gamma", GAMMA_DEFAULT)))
            del _u_bw, _rho_bw, _p_bw
            B_hat = project_div_free(
                jnp.fft.fftn(B_bw, axes=range(1, dim + 1)), grid)
            B_ext_hat = zero_b_hat(grid, dtype=B_hat.dtype)
            induct_ext = 1.0
            B0_phys = B_bw
        else:
            B0_phys = jnp.fft.ifftn(
                B_hat + B_ext_hat, axes=range(1, dim + 1)).real
    if dt is None:
        nu_cfl = nu + (clay_params["eta_p"] if (viscoelastic or mode == "clay") else 0.0)
        if is_cmhd:
            nu_cfl = nu_cfl + float(mhd_params.get("mu_eff", 0.0))
            gamma_cfl = float(mhd_params.get(
                "gamma", (ic_params or {}).get("gamma", GAMMA_DEFAULT)))
            p0_cfl = float(mhd_params.get("p0", 1.0))
            icp_cfl = ic_params or {}
            if ic == "sound":
                _u_s, rho_cfl, p_cfl, _cs = sound_wave_fields(
                    grid, eps=float(icp_cfl.get("sound_eps", 1e-3)),
                    rho0=float(icp_cfl.get("rho0", 1.0)), p0=p0_cfl,
                    gamma=gamma_cfl)
                del _u_s, _cs
            elif ic == "brio_wu":
                _u_bw, rho_cfl, p_cfl, _B_bw = brio_wu_fields(
                    grid, gamma=gamma_cfl)
                del _u_bw, _B_bw
            else:
                rho_eps = float(icp_cfl.get("rho_eps", 0.0))
                if rho_eps != 0.0:
                    rho_cfl = jnp.fft.ifftn(bump_rho_hat(grid, eps=rho_eps)).real
                else:
                    rho_cfl = jnp.full((N,) * dim, float(icp_cfl.get("rho0", 1.0)))
                p_cfl = jnp.full((N,) * dim, p0_cfl)
            dt = float(cfl_dt_cmhd(
                u0, rho_cfl, p_cfl, B0_phys, grid["dx"], nu_cfl,
                mhd_params["eta_mag"], gamma_cfl, cfl=cfl))
        elif magnetic:
            nu_cfl = nu_cfl + float(mhd_params.get("mu_eff", 0.0))
            dt = float(cfl_dt_mhd(
                u0, B0_phys, grid["dx"], nu_cfl, mhd_params["eta_mag"], cfl=cfl,
                d_i=float(mhd_params.get("d_i", 0.0))))
        else:
            dt = float(cfl_dt(u0, grid["dx"], nu_cfl, cfl=cfl))
        # 2D scar default. Do not clobber MHD Alfvén CFL (hidden dt sink).
        if dim == 2 and not magnetic:
            dt = 0.005

    u_hat_raw = jnp.fft.fftn(u0, axes=range(1, dim + 1))
    if is_cmhd:
        # Qin / Helmholtz off: keep the compressive part of u (sound).
        u_hat = u_hat_raw * grid["dealias"]
        omega_hat = vorticity_from_velocity(u_hat, grid)
    else:
        u_hat = project_div_free(u_hat_raw, grid)
        omega_hat = vorticity_from_velocity(u_hat, grid)
        if dim == 3:
            omega_hat = project_div_free(omega_hat, grid)

    centres = resolve_scar_centres(grid, n_scars, scar_centres)
    n_scars = len(centres)

    if is_cmhd:
        tau_hat = zero_tau_hat(grid, dtype=omega_hat.dtype)
        clay_use = clay_params
        if not viscoelastic:
            clay_use = dict(clay_params, eta_p=0.0, stress_couple=0.0,
                            clay_gain=0.0, gum_scale=0.0,
                            soft_J=0.0, high_de=0.0, alpha_LB=0.0,
                            lam_kin_gain=0.0, alpha_perp=0.0)
        gamma = float(mhd_params.get(
            "gamma", (ic_params or {}).get("gamma", GAMMA_DEFAULT)))
        p0 = float(mhd_params.get("p0", 1.0))
        icp = ic_params or {}
        if ic == "sound":
            _u_s, rho_phys, p_phys, _cs = sound_wave_fields(
                grid, eps=float(icp.get("sound_eps", 1e-3)),
                rho0=float(icp.get("rho0", 1.0)), p0=p0, gamma=gamma)
            del _u_s, _cs
            rho_hat = jnp.fft.fftn(rho_phys).astype(omega_hat.dtype) * grid["dealias"]
            p_hat = jnp.fft.fftn(p_phys).astype(omega_hat.dtype) * grid["dealias"]
        elif ic == "brio_wu":
            _u_bw, rho_phys, p_phys, _B_bw = brio_wu_fields(grid, gamma=gamma)
            del _u_bw, _B_bw
            rho_hat = jnp.fft.fftn(rho_phys).astype(omega_hat.dtype) * grid["dealias"]
            p_hat = jnp.fft.fftn(p_phys).astype(omega_hat.dtype) * grid["dealias"]
        else:
            rho_eps = float(icp.get("rho_eps", 0.0))
            if rho_eps != 0.0:
                rho_hat = bump_rho_hat(grid, eps=rho_eps, dtype=omega_hat.dtype)
            else:
                rho_hat = uniform_rho_hat(
                    grid, rho0=float(icp.get("rho0", 1.0)), dtype=omega_hat.dtype)
            p_eps = float(icp.get("p_eps", 0.0))
            if p_eps != 0.0:
                p_hat = bump_p_hat(grid, eps=p_eps, p0=p0, dtype=omega_hat.dtype)
            else:
                p_hat = uniform_p_hat(grid, p0=p0, dtype=omega_hat.dtype)
        (u_hat, tau_hat, B_hat, psi_hat, rho_hat, p_hat), hist = _run_cmhd_scanned(
            u_hat, tau_hat, B_hat, rho_hat, p_hat, grid, nu, dt, steps, force_on,
            scheme, diag_every, clay_use, mhd_params, n_scars, centres,
            force_amp, B_ext_hat=B_ext_hat, induct_ext=induct_ext, gamma=gamma)
    elif is_twofluid:
        tau_hat = zero_tau_hat(grid, dtype=omega_hat.dtype)
        clay_use = clay_params
        if not viscoelastic:
            clay_use = dict(clay_params, eta_p=0.0, stress_couple=0.0,
                            clay_gain=0.0, gum_scale=0.0,
                            soft_J=0.0, high_de=0.0, alpha_LB=0.0,
                            lam_kin_gain=0.0, alpha_perp=0.0)
        n0 = float(mhd_params.get("n", mhd_params.get("n_hall", 1.0)))
        n_eps = float(mhd_params.get("n_eps", 0.0))
        if n_eps != 0.0:
            n_i_hat = bump_rho_hat(grid, eps=n_eps, dtype=omega_hat.dtype)
        else:
            n_i_hat = uniform_rho_hat(grid, rho0=n0, dtype=omega_hat.dtype)
        (omega_hat, tau_hat, B_hat, psi_hat, n_i_hat), hist = _run_twofluid_scanned(
            omega_hat, tau_hat, B_hat, n_i_hat, grid, nu, dt, steps, force_on,
            scheme, diag_every, clay_use, mhd_params, n_scars, centres,
            force_amp, B_ext_hat=B_ext_hat, induct_ext=induct_ext)
    elif magnetic:
        tau_hat = zero_tau_hat(grid, dtype=omega_hat.dtype)
        clay_use = clay_params
        if not viscoelastic:
            clay_use = dict(clay_params, eta_p=0.0, stress_couple=0.0,
                            clay_gain=0.0, gum_scale=0.0,
                            soft_J=0.0, high_de=0.0, alpha_LB=0.0,
                            lam_kin_gain=0.0, alpha_perp=0.0)
        (omega_hat, tau_hat, B_hat, psi_hat), hist = _run_mhd_scanned(
            omega_hat, tau_hat, B_hat, grid, nu, dt, steps, force_on,
            scheme, diag_every, clay_use, mhd_params, n_scars, centres,
            force_amp, B_ext_hat=B_ext_hat, induct_ext=induct_ext)
    elif viscoelastic or mode == "clay":
        tau_hat = zero_tau_hat(grid, dtype=omega_hat.dtype)
        (omega_hat, tau_hat), hist = _run_clay_scanned(
            omega_hat, tau_hat, grid, nu, dt, steps, force_on,
            scheme, diag_every, clay_params, n_scars, centres, force_amp)
    else:
        omega_hat, hist = _run_vorticity_scanned(
            omega_hat, grid, nu, dt, steps, force_on, scheme, diag_every,
            n_scars, centres, force_amp)
        tau_hat = zero_tau_hat(grid, dtype=omega_hat.dtype)

    if is_cmhd:
        omega_hat = vorticity_from_velocity(u_hat, grid)
    else:
        u_hat = velocity_from_vorticity(omega_hat, grid)
    nu_out = nu + (float(mhd_params.get("mu_eff", 0.0)) if magnetic else 0.0)
    out = _pack_out(hist, u_hat, omega_hat, tau_hat, grid, dt, N, nu_out, ic,
                    scheme, bool(viscoelastic or mode == "clay"), clay_params,
                    steps, diag_every, n_scars, centres, force_on,
                    B_hat=B_hat, mhd_params=mhd_params, magnetic=bool(magnetic),
                    rho_hat=rho_hat, p_hat=p_hat, n_i_hat=n_i_hat)
    out["nu_solvent"] = nu
    out["B_ext_hat"] = B_ext_hat
    if magnetic:
        out["psi_hat"] = psi_hat
    return out

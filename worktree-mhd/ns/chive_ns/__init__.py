# ============================================================
# @Akitti C*Hive – Package Init
# ============================================================

import jax
jax.config.update("jax_enable_x64", True)

from .constants import PHI, DELTA_MIN, NU_GUM
from .grid import (
    make_grid, project_div_free, generate_smooth_div_free_u0,
    generate_taylor_green, generate_antiparallel_tubes,
    antiparallel_tube_vector, paper_ni_ic, paper_sigma_c,
    velocity_from_vorticity, vorticity_from_velocity, ik_cross, cfl_dt,
)
from .vorticity import (
    modest_liar, z7_braid_forcing, ns_vorticity_step, ns_vorticity_rhs,
    coupled_vorticity_stress_step, coupled_mhd_step,
    default_scar_centres, resolve_scar_centres,
)
from .clay import (
    nonlinear_trilinear, gum_damping, oldroyd_b_step, oldroyd_b_rhs,
    stress_vorticity_force, zero_tau_hat, DEFAULT_CLAY,
)
from .bubble import rayleigh_plesset, attractor_tower, coupled_rp_attractor_rhs
from .diagnostics import (
    lambda2_criterion, lambda2_criterion_3d, field_diagnostics, stress_diagnostics,
    millennium_series, max_strain_rate, strain_tensor,
)
from .regularisers import mollify_hat, kinematic_lambda, high_de_blend
from .residual import hybrid_asgs_residual
from .live import live_diagnostics_and_feedback
from .mhd import (
    DEFAULT_MHD, generate_b0, generate_b_ext, generate_b_flux_tubes,
    generate_u_ot, zero_b_hat, zero_psi_hat, current_from_b,
    lorentz_vorticity_force, induction_rhs, odd_vorticity_force,
    glm_grad_psi, glm_psi_rhs,
    mhd_field_diagnostics, cfl_dt_mhd, split_guide_fields, beta_from_lambda_in,
)
from .es_lhdi import (
    zero_e_hat, zero_charge_hat, generate_harris_sheet,
    generate_harris_edge_seed, es_placeholder_diagnostics, es_equation_notes,
)
from .scaffold_heavy import heavy_placeholder_diagnostics, heavy_equation_notes
from .driver import run_framework

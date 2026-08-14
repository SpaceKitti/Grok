# ============================================================
# @Akitti C*Hive – Package Init
# ============================================================

import jax
jax.config.update("jax_enable_x64", True)

from .constants import PHI, DELTA_MIN, NU_GUM
from .grid import (
    make_grid, project_div_free, generate_smooth_div_free_u0,
    generate_taylor_green, generate_antiparallel_tubes,
    velocity_from_vorticity, vorticity_from_velocity, ik_cross, cfl_dt,
)
from .vorticity import (
    modest_liar, z7_braid_forcing, ns_vorticity_step, ns_vorticity_rhs,
    coupled_vorticity_stress_step, default_scar_centres, resolve_scar_centres,
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
from .driver import run_framework

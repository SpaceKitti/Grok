"""Tiny compile/identity smoke for freeze-out + odd + mu_eff."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax.numpy as jnp
from chive_ns import run_framework, DEFAULT_MHD, split_guide_fields, make_grid


def main():
    print("split_guide freeze=0 vs 1", flush=True)
    g = make_grid(16, L=1.0, dim=3)
    B, Bext, ind = split_guide_fields(g, dict(DEFAULT_MHD, freeze_ext=0.0))
    print(" freeze0  |B|", float(jnp.mean(jnp.abs(B))),
          "|Bext|", float(jnp.mean(jnp.abs(Bext))), "induct", ind)
    B, Bext, ind = split_guide_fields(g, dict(DEFAULT_MHD, freeze_ext=1.0))
    print(" freeze1  |B|", float(jnp.mean(jnp.abs(B))),
          "|Bext|", float(jnp.mean(jnp.abs(Bext))), "induct", ind)

    common = dict(dim=3, N=16, steps=6, dt=0.002, ic="tubes", scheme="rk2",
                  force_on=False, nu=5e-4, diag_every=3)
    for name, ve, kw in (
        ("ctrl", False, dict(freeze_ext=0.0)),
        ("freeze", False, dict(freeze_ext=1.0)),
        ("odd", False, dict(eta_odd=1e-3, berry_gain=0.5)),
        ("mu", False, dict(mu_eff=2e-4)),
        ("hyfr", True, dict(freeze_ext=1.0)),
    ):
        out = run_framework(mode="mhd", viscoelastic=ve, magnetic=True,
                            mhd_params=dict(DEFAULT_MHD, **kw), **common)
        print(name, "E", float(out["energy"][-1]),
              "Em", float(out["e_mag"][-1]),
              "Emt", float(out["e_mag_tot"][-1]),
              "J", float(out["max_j"].max()),
              "divB", float(out["max_div_b"].max()),
              "Ni", float(out["N_i"][-1]),
              "lam/dx", float(out["lam_min_dx"][-1]),
              flush=True)
        assert jnp.isfinite(out["energy"][-1])
        assert float(out["max_div_b"].max()) < 1e-8
    print("SMOKE MHD2 OK")


if __name__ == "__main__":
    main()

"""Post-fix magnetic energy identity check (hy+MHD, N=24) + 2D smoke."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jax.numpy as jnp
from chive_ns import run_framework, default_scar_centres


def trapz(y, t):
    y, t = jnp.asarray(y), jnp.asarray(t)
    return float(jnp.sum(0.5 * (y[1:] + y[:-1]) * (t[1:] - t[:-1])))


def report(name, out, nu):
    e0, e1 = float(out["energy"][0]), float(out["energy"][-1])
    em0, em1 = float(out["e_mag"][0]), float(out["e_mag"][-1])
    t = out["time"]
    I_nu = trapz(nu * out["enstrophy"], t)
    I_W = trapz(out["work"], t)
    I_ohm = trapz(out["ohmic"], t)
    I_L = trapz(out["lorentz_work"], t)
    dEk, dEm = e0 - e1, em1 - em0
    print(f"--- {name} ---")
    print(f"dE_kin={dEk:.4e}  pred={I_nu + I_W - I_L:.4e}  "
          f"(nuZ={I_nu:.4e} W={I_W:.4e} L={I_L:.4e})")
    print(f"dE_mag={dEm:.4e}  pred={-I_L - I_ohm:.4e}  (Ohm={I_ohm:.4e})")
    print(f"dE_tot={dEk - dEm:.4e} pred={I_nu + I_W + I_ohm:.4e}")
    print(f"maxJ={float(out['max_j'].max()):.3e} maxB={float(out['max_b'].max()):.4f} "
          f"divB={float(out['max_div_b'].max()):.2e}")
    print(f"|w|_end={float(out['max_vort'][-1]):.3f} W={float(out['work'][-1]):.3e} "
          f"tau={float(out['max_tau'].max()):.4f}")


def main():
    print("2D MHD smoke...", flush=True)
    o2 = run_framework(
        dim=2, N=16, steps=8, dt=0.005, ic="smooth", scheme="rk2",
        force_on=False, nu=1e-3, diag_every=4, mode="mhd",
        viscoelastic=True, magnetic=True)
    print("2D ok E", float(o2["energy"][-1]), "Em", float(o2["e_mag"][-1]),
          "divB", float(o2["max_div_b"].max()), flush=True)

    centres = default_scar_centres(1.0, 4, 3)
    common = dict(
        dim=3, N=24, steps=80, dt=0.0015, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=20)
    print("N=24 hy+MHD budget check...", flush=True)
    out = run_framework(mode="mhd", viscoelastic=True, magnetic=True, **common)
    report("hy+MHD N=24 t=0.12", out, 5e-4)


if __name__ == "__main__":
    main()

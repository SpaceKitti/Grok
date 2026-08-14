"""N=96 t≈0.5 confirmation of milder clay (eta_p=0.003) vs stored NS / old clay."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import run_framework, default_scar_centres, DEFAULT_CLAY


def main():
    centres = default_scar_centres(1.0, 4, 3)
    print("DEFAULT_CLAY", DEFAULT_CLAY, flush=True)
    print("--- milder clay  N=96  tubes+4scar  t≈0.5 ---", flush=True)
    out = run_framework(
        dim=3, N=96, steps=660, dt=7.5542e-04, ic="tubes", scheme="rk2",
        force_on=True, n_scars=4, scar_centres=centres, force_amp=0.35,
        nu=5e-4, diag_every=30, mode="clay", viscoelastic=True,
        clay_params=dict(DEFAULT_CLAY),
    )
    e0, e1 = float(out["energy"][0]), float(out["energy"][-1])
    print(f"t={float(out['time'][-1]):.3f}  dE={100*(e0-e1)/e0:.2f}%  "
          f"max|w| {float(out['max_vort'][0]):.3f}->{float(out['max_vort'][-1]):.3f} "
          f"(peak {float(out['max_vort'].max()):.3f})  "
          f"BKM={float(out['bkm_integral'][-1]):.3f}  "
          f"stretch={float(out['stretch'].max()):.3f}  "
          f"max|tau|={float(out['max_tau'].max()):.4f}", flush=True)
    print()
    print(f"{'t':>6}  {'E':>9} {'Z':>9} {'|ω|':>9} {'|S|':>9} "
          f"{'BKM':>9} {'ω·S·ω':>9} {'⟨|τ|⟩':>9} {'max|τ|':>9}")
    for i in range(len(out["time"])):
        print(f"{float(out['time'][i]):6.3f}  "
              f"{float(out['energy'][i]):9.4e} {float(out['enstrophy'][i]):9.4e} "
              f"{float(out['max_vort'][i]):9.4e} {float(out['max_strain'][i]):9.4e} "
              f"{float(out['bkm_integral'][i]):9.4e} {float(out['stretch'][i]):9.4e} "
              f"{float(out['mean_tau'][i]):9.4e} {float(out['max_tau'][i]):9.4e}")
    return out


if __name__ == "__main__":
    main()

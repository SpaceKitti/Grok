"""Higher-resolution 3D C*Hive NS with full vortex stretching.

Run from the repo root:

    python examples/run_3d_highres.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chive_ns import run_framework


def main():
    out = run_framework(
        dim=3,
        N=64,
        steps=200,
        mode="vorticity",
        ic="taylor_green",
        scheme="rk2",
        force_on=True,
        diag_every=20,
    )
    e, z, s, w = out["energy"], out["enstrophy"], out["stretch"], out["max_vort"]
    print(f"N={out['N']}  nu={out['nu']:.2e}  dt={out['dt']:.4e}  ic={out['ic']}")
    print("step   energy        enstrophy     stretch       max|ω|")
    for i, (ei, zi, si, wi) in enumerate(zip(e, z, s, w)):
        print(f"{i*20:4d}  {float(ei):.6e}  {float(zi):.6e}  {float(si):.6e}  {float(wi):.6e}")
    print(f"energy     {float(e[0]):.6e} → {float(e[-1]):.6e}")
    print(f"enstrophy  {float(z[0]):.6e} → {float(z[-1]):.6e}  (peak {float(z.max()):.6e})")
    print(f"stretch    {float(s[0]):.6e} → {float(s[-1]):.6e}  (peak {float(s.max()):.6e})")
    print(f"max |ω|    {float(w[0]):.6e} → {float(w[-1]):.6e}  (peak {float(w.max()):.6e})")
    print(f"max |div u| {float(out['max_div'].max()):.3e}")
    print(f"helicity    {float(out['helicity'][-1]):.3e}")
    return out


if __name__ == "__main__":
    main()

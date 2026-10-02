"""L5: predictions. Each item tagged PREDICTED / FITTED / [by construction/identity]; 'genuine' per README criteria."""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

import H_QG as HQ  # noqa: E402
import action_R1 as AR  # noqa: E402
import loss_qg as LQ  # noqa: E402

E, V = HQ.E, HQ.V
DRIVE = Path(r"C:\Users\Akitt\pairA-drive-return")
SWEEP = Path(r"C:\Users\Akitt\pairA-drive-sweep")


def drive_return_w(fname, sp, dn, st, m):
    d = np.load(DRIVE / "outputs" / fname)
    keys = [k for k in d.files if k.startswith("run") and f"_{sp}_{dn}_start{st}_" in k and k.endswith("_theta")]
    assert len(keys) == 1, (sp, dn, st, keys)
    base = keys[0][:-len("theta")]
    th = d[base + "theta"]
    i = int(np.argmin(np.abs(th - 2 * np.pi * m)))
    assert abs(th[i] - 2 * np.pi * m) < 1e-9
    return np.array([d[base + "wA"][i], d[base + "wB"][i]])


def p_rate(l3):
    rows = []
    sw = np.load(SWEEP / "outputs" / "sweep.npz") if (SWEEP / "outputs" / "sweep.npz").exists() else None
    for gT, sp in ((20.0, "slow20"), (40.0, "slow40"), (100.0, "slow100")):
        for st in "AB":
            for m in (1, 2):
                rec = l3[0.75]["runs"][(gT, "ccw", st)][m]
                wd = drive_return_w("drive.npz", sp, "ccw", st, m)
                wsw = float(np.max(sw[f"row2_0.75_p_{sp}_ccw_{st}_{2*m}pi_w"])) if sw is not None else None
                rows.append({"gT": gT, "st": st, "turn": 2 * m, "w": rec["w"], "win": rec["phys"], "w_dr": float(np.max(wd)), "w_sw": wsw})
    return rows


def p_period():
    h = 1e-6
    Fp = ((E + h) ** 2 - (E - h) ** 2) / (2 * h)       # F'(eps_EP) numerically
    kappa = Fp / 2
    return {"kappa": kappa, "beta_smooth": 2 * np.pi / kappa, "beta_formula": 2 * np.pi / E, "tau_swap": 4 * np.pi / E, "T_H": kappa / (2 * np.pi)}


def p_gap():
    ds = np.array([1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6])
    out = {}
    for name, direc in (("real, outside", 1.0), ("real, inside", -1.0), ("complex ray 45°", np.exp(1j * np.pi / 4))):
        g = [abs(np.diff(np.linalg.eigvals(HQ.H_qg_a(E + d * E * direc)))[0]) for d in ds]
        out[name] = float(np.polyfit(np.log(ds), np.log(g), 1)[0])
    return out


def p_S():
    rows = []
    for f in (1.1, 1.25, 1.5, 2.0):
        b = f * E
        rows.append({"b": f, "num": AR.S1_numeric(b), "ana": AR.S1_analytic(b)})
    return rows


def p_adiab(speeds=(20.0, 40.0, 100.0, 200.0)):
    rows = []
    for gT in speeds:
        mk = LQ.run_drive(HQ.H_qg_a, 1.25, +1, gT, 0)
        w = mk[2]["w"]
        rows.append({"gT": gT, "one_minus_w": float(1 - np.max(w))})
    x = np.log([r["gT"] for r in rows]); yv = np.log([r["one_minus_w"] for r in rows])
    p_last = float((yv[-1] - yv[-2]) / (x[-1] - x[-2]))
    p_all = float(np.polyfit(x, yv, 1)[0])
    return {"rows": rows, "p_last": p_last, "p_all": p_all, "pass": abs(p_last + 2) <= 0.3}

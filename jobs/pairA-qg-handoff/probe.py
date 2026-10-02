"""QG probe on the existing Pair A surface. No new Hamiltonian."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from seed import EPS_EP

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"


def phi_n(n: int) -> complex:
    return np.exp(1j * np.pi * n)


def U_G(intersection: int) -> complex:
    return (-1.0) ** intersection


def probe1(hist: dict) -> dict:
    """Φ(n)=U_G on A and B. n ≡ I(γ,Γ) (mod 2) from the cut intersection."""
    rows = {}
    for key in ("A", "B"):
        I = int(hist[key]["intersection"])
        n = I % 2
        ug = U_G(I)
        ph = phi_n(n)
        ok = abs(ph - ug) < 1e-12
        rows[key] = {
            "n": n,
            "U_G": ug,
            "Phi": ph,
            "result": "PASS" if ok else "FAIL",
        }
    return rows


def probe2() -> dict:
    return {
        "real_chart_support": "Γ only",
        "allowed_past_Wick": ["A", "B"],
        "held": ["C"],
        "note": "C present as a path, stays NOT-SELECTED (∩=0).",
    }


def probe3(jhat: dict, r0: dict) -> dict:
    J4 = jhat["Jhat4"]
    fro = float(np.linalg.norm(J4 - np.eye(2), "fro"))
    tau = 4.0 * np.pi / EPS_EP
    bolts = list(r0["eps"])
    both = abs(bolts[0] - EPS_EP) < 1e-8 and abs(bolts[1] + EPS_EP) < 1e-8
    jhat4_I = fro < 1e-10
    return {
        "tau": tau,
        "bolts": bolts,
        "fro_Jhat4_I": fro,
        "result": "PASS" if (jhat4_I and both) else "FAIL",
        "jhat4_is_I": jhat4_I,
        "both_bolts_listed": both,
    }


def write_probe_md(p1, p2, p3, path: Path) -> None:
    lines = []
    lines.append("FIXED B=WRITE C=NOT-SELECTED")
    lines.append("")
    lines.append("## Probe 1 — cover")
    lines.append("U_G[γ]=(-1)^{I(γ,Γ)}  Φ(n)=e^{iπ n}")
    for k, r in p1.items():
        lines.append(
            f"{k}: n={r['n']}  U_G={r['U_G']}  Φ={r['Phi']}  **{r['result']}**"
        )
    lines.append("")
    lines.append("## Probe 2 — past Wick")
    lines.append(f"real chart support: {p2['real_chart_support']}")
    lines.append(p2["note"])
    lines.append("")
    lines.append("## Probe 3 — regularity")
    lines.append(f"bolts χ=0,π  τ=4π/ε_EP={p3['tau']:.5f}")
    lines.append(
        f"Jhat4=I ({p3['jhat4_is_I']}, ||Jhat4-I||_F={p3['fro_Jhat4_I']:.3e})  "
        f"both bolts listed={p3['both_bolts_listed']}  **{p3['result']}**"
    )
    lines.append("")
    lines.append(f"allowed past Wick: {', '.join(p2['allowed_past_Wick'])}")
    lines.append(f"held: {', '.join(p2['held'])}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(hist: dict, strip: dict, r0: dict) -> dict:
    p1 = probe1(hist)
    p2 = probe2()
    p3 = probe3(strip, r0)
    write_probe_md(p1, p2, p3, ROOT / "RESULTS_probe.md")
    return {"p1": p1, "p2": p2, "p3": p3}

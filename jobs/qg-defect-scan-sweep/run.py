"""T1 then T2 then T3 then T4 then T5 (T1×T3) then T6. Separate tracks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))

import t1_cs_puncture
import t2_foam_scan
import t3_holo_scan
import t4_worldsheet
import t5_hybrid
import t6_control
from protocol import EPS_EP, GAMMA, n_mhd


def yn(b) -> str:
    return "yes" if b else "no"


def tf(b) -> str:
    return "PASS" if b else "FAIL"


def pfmt(p) -> str:
    if isinstance(p, str):
        return p
    return f"{complex(p):.4f}"


def write_results(mhd: dict, tracks: list[dict], path: Path) -> str:
    prefer = [t["family"] for t in tracks if t["verdict"] == "prefers Γ"]
    if prefer:
        sent = "scans that prefer Γ without insertion: " + ", ".join(prefer)
    else:
        sent = "no scan prefers Γ without insertion"

    lines = []
    lines.append("# QG defect-scan sweep")
    lines.append("")
    lines.append("New folder. Hive not opened. Tearing not rerun. Pair A not rebuilt.")
    lines.append("No letter is $\\exp(i\\pi n_{\\mathrm{MHD}})$ or $da=\\pi\\delta_\\Gamma$.")
    lines.append(
        f"Locked MHD: $\\varepsilon_{{\\mathrm{{EP}}}}={EPS_EP:.6f}$, "
        f"$\\Delta n(2\\pi)={mhd['dn_2pi']}$, $\\Delta n(4\\pi)={mhd['dn_4pi']}$."
    )
    lines.append("Defect/source/pinch is scanned. Γ is a score mask only.")
    lines.append("")
    for t in tracks:
        lines.append(f"## {t['family']}")
        lines.append("")
        lines.append("```")
        lines.append(t["operator"])
        lines.append("```")
        lines.append("")
        lines.append(
            f"P_site(on-loop)={pfmt(t['P_site'])}; "
            f"P_site(off-loop)={pfmt(t['P_site_off'])}. "
            f"defined without MHD jump: **{yn(t['defined_without_mhd'] and not t['inserted'])}**. "
            f"S1 {tf(t['S1'])} ({t['s1']}). "
            f"S2 {tf(t['S2'])} ({t['s2']}). "
            f"S3 {tf(t['S3'])} ({t['s3']}). "
            f"S4 {tf(t['S4'])} ({t['s4']}). "
            f"verdict: **{t['verdict']}**."
        )
        lines.append("")

    lines.append("## Table")
    lines.append("")
    lines.append(
        "| family | P_site | defined without MHD jump? | S1 | S2 | S3 | S4 | verdict |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for t in tracks:
        lines.append(
            f"| {t['family']} | {pfmt(t['P_site'])} | "
            f"{yn(t['defined_without_mhd'] and not t['inserted'])} | "
            f"{tf(t['S1'])} | {tf(t['S2'])} | {tf(t['S3'])} | {tf(t['S4'])} | "
            f"**{t['verdict']}** |"
        )
    lines.append("")
    lines.append("## One sentence")
    lines.append("")
    lines.append(f"**{sent}**")
    lines.append("")
    lines.append("Not a QG theorem. No Qin, leapfrog, Hall 3×3, dynamo phenomenology.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return sent


def plot_scan(t: dict, outdir: Path) -> None:
    sites = t.get("sites")
    sig = t.get("sig_on")
    if sites is None or sig is None or isinstance(t["P_site"], str):
        return
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    sc = ax.scatter(sites.real, sites.imag, c=sig, s=18, cmap="magma")
    fig.colorbar(sc, ax=ax, label="|letter−trivial|")
    lo, hi = GAMMA
    ax.plot([lo, hi], [0, 0], color="cyan", lw=2.2, label=r"$\Gamma$")
    p = complex(t["P_site"])
    ax.scatter([p.real], [p.imag], marker="*", s=120, c="lime", label="P_site", zorder=5)
    ax.set_aspect("equal")
    ax.set_title(t["family"] + " scan")
    ax.legend(fontsize=8)
    fig.tight_layout()
    safe = t["family"].split()[0]
    fig.savefig(outdir / f"scan_{safe}.png")
    plt.close(fig)


def main() -> int:
    print("MHD n_sheet")
    mhd = n_mhd()
    print(f"  Δn 2π={mhd['dn_2pi']} 4π={mhd['dn_4pi']}")

    print("T1 CS puncture scan")
    t1 = t1_cs_puncture.run(mhd)
    print(" ", t1["verdict"], t1["s1"])

    print("T2 foam defect scan")
    t2 = t2_foam_scan.run(mhd)
    print(" ", t2["verdict"], t2["s1"])

    print("T3 holo attachment scan")
    t3 = t3_holo_scan.run(mhd)
    print(" ", t3["verdict"], t3["s1"])

    print("T4 worldsheet pinch scan")
    t4 = t4_worldsheet.run(mhd)
    print(" ", t4["verdict"], t4["s1"])

    print("T5 hybrid (after T1 and T3)")
    t5 = t5_hybrid.run(mhd, t1, t3)
    print(" ", t5["verdict"], t5["s1"])

    print("T6 uniform U(1) control")
    t6 = t6_control.run(mhd)
    print(" ", t6["verdict"], t6["s1"])

    if t6["verdict"] == "prefers Γ":
        raise SystemExit("T6 passed: sweep is broken")

    tracks = [t1, t2, t3, t4, t5, t6]
    for t in tracks:
        plot_scan(t, OUT)
    sent = write_results(mhd, tracks, ROOT / "RESULTS.md")

    table = []
    for t in tracks:
        table.append({
            "family": t["family"],
            "P_site": pfmt(t["P_site"]),
            "P_site_off": pfmt(t["P_site_off"]),
            "defined_without_mhd": t["defined_without_mhd"] and not t["inserted"],
            "S1": t["S1"], "S2": t["S2"], "S3": t["S3"], "S4": t["S4"],
            "verdict": t["verdict"],
            "s1": t["s1"],
        })
    (OUT / "summary.json").write_text(json.dumps({"sentence": sent, "table": table}, indent=2), encoding="utf-8")
    with (OUT / "scan_table.csv").open("w", encoding="utf-8") as f:
        f.write("family,P_site,defined_without_mhd,S1,S2,S3,S4,verdict\n")
        for t in tracks:
            f.write(
                f"{t['family']},{pfmt(t['P_site'])},"
                f"{int(t['defined_without_mhd'] and not t['inserted'])},"
                f"{int(t['S1'])},{int(t['S2'])},{int(t['S3'])},{int(t['S4'])},"
                f"{t['verdict']}\n"
            )
    print("SENTENCE:", sent)
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

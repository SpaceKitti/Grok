"""
Five separate tracks: F1, then F2, then F3, then F4 (F1×F3), then F5.
Do not fuse into one QG object.
"""

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

import f1_cs
import f2_foam
import f3_holo
import f4_hybrid
import f5_uniform
from protocol import n_mhd


def yn(b: bool) -> str:
    return "yes" if b else "no"


def tf(b: bool) -> str:
    return "PASS" if b else "FAIL"


def write_results(mhd: dict, tracks: list[dict], path: Path) -> str:
    jumpers = [t["family"] for t in tracks if t["score"]["verdict"] == "jumps with MHD"]
    if jumpers:
        sent = "families that jump with the MHD sheet: " + ", ".join(jumpers)
    else:
        sent = "no family jumps with the MHD sheet"

    lines = []
    lines.append("# QG family sheet-jump sweep")
    lines.append("")
    lines.append("New folder. Hive not opened. Tearing not rerun. Pair A not rebuilt.")
    lines.append("No letter is $U=\\exp(i\\pi n_{\\mathrm{MHD}})$ or $da=\\pi\\delta_\\Gamma$.")
    lines.append("")
    lines.append("Locked MHD: pair A, $\\varepsilon_{\\mathrm{EP}}=0.513681$, "
                 f"$\\Delta n(2\\pi)={mhd['dn_2pi']}$, $\\Delta n(4\\pi)={mhd['dn_4pi']}$.")
    lines.append("Same loop family around $+\\varepsilon_{\\mathrm{EP}}$; control centre $+1.2i$.")
    lines.append("")
    for t in tracks:
        lines.append(f"## {t['family']}")
        lines.append("")
        lines.append("```")
        lines.append(t["operator"])
        lines.append("```")
        lines.append("")
        sc = t["score"]
        lines.append(
            f"defined without MHD jump: **{yn(t['defined_without_mhd'] and not t['inserted'])}**. "
            f"S1 {tf(sc['S1'])} ({sc['s1']}). "
            f"S2 {tf(sc['S2'])} ({sc['s2']}). "
            f"S3 {tf(sc['S3'])} ({sc['s3']}). "
            f"S4 {tf(sc['S4'])} ({sc['s4']}). "
            f"verdict: **{sc['verdict']}**."
        )
        lines.append("")

    lines.append("## Table")
    lines.append("")
    lines.append("| family | defined without MHD jump? | S1 | S2 | S3 | S4 | verdict |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for t in tracks:
        sc = t["score"]
        lines.append(
            f"| {t['family']} | {yn(t['defined_without_mhd'] and not t['inserted'])} | "
            f"{tf(sc['S1'])} | {tf(sc['S2'])} | {tf(sc['S3'])} | {tf(sc['S4'])} | "
            f"**{sc['verdict']}** |"
        )
    lines.append("")
    lines.append("## One sentence")
    lines.append("")
    lines.append(f"**{sent}**")
    lines.append("")
    lines.append("Not quantum gravity solved. No Qin, leapfrog, Hall 3×3, dynamo phenomenology.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return sent


def plot_tracks(mhd: dict, tracks: list[dict], outdir: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.0))
    th = mhd["theta"] / np.pi
    ax.step(th, mhd["n_sheet"], where="post", color="k", lw=1.6, label=r"$n_{\mathrm{MHD}}$")
    for t, c in zip(tracks, ["C0", "C1", "C2", "C3", "C4"]):
        ax.plot(th, np.real(t["U_on"]), color=c, lw=1.2, label=t["family"])
    ax.axvline(2, color="0.5", ls=":", lw=0.8)
    ax.axvline(4, color="0.5", ls=":", lw=0.8)
    ax.set_xlabel(r"$\theta/\pi$ around endpoint")
    ax.set_ylabel(r"$n_{\mathrm{MHD}}$ / $\mathrm{Re}\,U$")
    ax.set_title("Five letters on the same loop (not one QG object)")
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(outdir / "five_tracks_U.png")
    plt.close(fig)


def main() -> int:
    print("protocol: MHD n_sheet")
    mhd = n_mhd()
    print(f"  Δn 2π={mhd['dn_2pi']} 4π={mhd['dn_4pi']}")

    print("F1 CS")
    t1 = f1_cs.run(mhd)
    print(" ", t1["score"]["verdict"], t1["score"]["s2"])

    print("F2 foam")
    t2 = f2_foam.run(mhd)
    print(" ", t2["score"]["verdict"], "defect", t2["defect_center"])

    print("F3 holo")
    t3 = f3_holo.run(mhd)
    print(" ", t3["score"]["verdict"])

    print("F4 hybrid (F1 × F3)")
    t4 = f4_hybrid.run(mhd, t1, t3)
    print(" ", t4["score"]["verdict"])

    print("F5 uniform U(1) control")
    t5 = f5_uniform.run(mhd)
    print(" ", t5["score"]["verdict"])

    tracks = [t1, t2, t3, t4, t5]
    if t5["score"]["verdict"] == "jumps with MHD":
        raise SystemExit("F5 passed: sweep is broken")

    plot_tracks(mhd, tracks, OUT)
    sent = write_results(mhd, tracks, ROOT / "RESULTS.md")

    table = []
    for t in tracks:
        sc = t["score"]
        table.append({
            "family": t["family"],
            "defined_without_mhd": t["defined_without_mhd"] and not t["inserted"],
            "S1": sc["S1"], "S2": sc["S2"], "S3": sc["S3"], "S4": sc["S4"],
            "verdict": sc["verdict"],
            "s1": sc["s1"], "s2": sc["s2"], "s3": sc["s3"], "s4": sc["s4"],
        })
    (OUT / "summary.json").write_text(json.dumps({"sentence": sent, "table": table}, indent=2), encoding="utf-8")
    with (OUT / "family_table.csv").open("w", encoding="utf-8") as f:
        f.write("family,defined_without_mhd_jump,S1,S2,S3,S4,verdict\n")
        for t in tracks:
            sc = t["score"]
            f.write(
                f"{t['family']},{int(t['defined_without_mhd'] and not t['inserted'])},"
                f"{int(sc['S1'])},{int(sc['S2'])},{int(sc['S3'])},{int(sc['S4'])},"
                f"{sc['verdict']}\n"
            )
    print("SENTENCE:", sent)
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Crossing probe. P0 must pass. Then P1–P6 separate tracks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))

import p0_pairA
import p1_cs
import p2_foam
import p3_holo
import p4_worldsheet
import p5_hybrid
import p6_uniform
from protocol import DELTA, EPS_EP, X_OFF, X_ON


def yn(b) -> str:
    return "yes" if b else "no"


def write_results(tracks: list[dict], path: Path, p0_ok: bool) -> str:
    seers = [t["family"] for t in tracks[1:] if t["verdict"] == "sees the wall"]
    if not p0_ok:
        sent = "probe-broken (P0 failed)"
    elif seers:
        sent = "wall-probe works; letters that see the wall: " + ", ".join(seers)
    else:
        sent = "wall-probe works; no named letter sees the wall"

    lines = []
    lines.append("# Cut-crossing probe")
    lines.append("")
    lines.append("New folder. Hive not opened. Pair A not rebuilt.")
    lines.append("No letter is copied from $n_{\\mathrm{MHD}}$ or $da=\\pi\\delta_\\Gamma$.")
    lines.append(
        f"$\\Gamma=[-{EPS_EP:.6f},{EPS_EP:.6f}]$. "
        f"$\\gamma_{{\\mathrm{{cross}}}}$: $x={X_ON}$, $y=+{DELTA}\\to-{DELTA}$. "
        f"$\\gamma_{{\\mathrm{{miss}}}}$: $x={X_OFF}$, same length."
    )
    lines.append("Main number: jump across the segment, not flux of a closed loop.")
    lines.append("")
    for t in tracks:
        lines.append(f"## {t['family']}")
        lines.append("")
        lines.append("```")
        lines.append(t["operator"])
        lines.append("```")
        extra = ""
        if "P_site" in t:
            extra = f" P_site={t['P_site']}."
        if "n_on" in t:
            extra += f" n(before,after) on={t['n_on']} off={t['n_off']}."
        lines.append(
            f"J_on={t['J_on']:.6g}, J_off={t['J_off']:.6g}, "
            f"ratio={t['ratio']:.4f}.{extra} "
            f"defined without MHD jump: **{yn(t.get('defined_without_mhd', True))}**. "
            f"verdict: **{t['verdict']}**."
        )
        lines.append("")

    lines.append("## Table")
    lines.append("")
    lines.append("| family | J_on | J_off | ratio | defined without MHD jump? | verdict |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for t in tracks:
        lines.append(
            f"| {t['family']} | {t['J_on']:.6g} | {t['J_off']:.6g} | "
            f"{t['ratio']:.4f} | {yn(t.get('defined_without_mhd', True))} | "
            f"**{t['verdict']}** |"
        )
    lines.append("")
    lines.append("## One sentence")
    lines.append("")
    lines.append(f"**{sent}**")
    lines.append("")
    lines.append("Not a theorem. No Qin, leapfrog, Hall 3×3, dynamo phenomenology.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return sent


def main() -> int:
    print("P0 pair A crossing")
    t0 = p0_pairA.run()
    print(f"  J_on={t0['J_on']:.6g} J_off={t0['J_off']:.6g} ratio={t0['ratio']:.4f} {t0['verdict']}")
    if t0["verdict"] == "probe-broken" or not t0["passed"]:
        write_results([t0], ROOT / "RESULTS.md", False)
        print("P0 failed. STOP.")
        return 1

    print("P1 CS")
    t1 = p1_cs.run()
    print(" ", t1["verdict"], t1["ratio"])

    print("P2 foam scan")
    t2 = p2_foam.run()
    print(" ", t2["verdict"], "P_site", t2.get("P_site"))

    print("P3 holo")
    t3 = p3_holo.run()
    print(" ", t3["verdict"], t3["ratio"])

    print("P4 worldsheet")
    t4 = p4_worldsheet.run()
    print(" ", t4["verdict"], t4["ratio"])

    print("P5 hybrid after P1 and P3")
    t5 = p5_hybrid.run(t1, t3)
    print(" ", t5["verdict"])

    print("P6 uniform U(1) control")
    t6 = p6_uniform.run()
    print(" ", t6["verdict"], t6["ratio"])
    if t6["verdict"] == "sees the wall":
        print("P6 passed: sweep is broken")
        return 2

    tracks = [t0, t1, t2, t3, t4, t5, t6]
    sent = write_results(tracks, ROOT / "RESULTS.md", True)
    table = [
        {
            "family": t["family"],
            "J_on": t["J_on"],
            "J_off": t["J_off"],
            "ratio": t["ratio"],
            "verdict": t["verdict"],
        }
        for t in tracks
    ]
    (OUT / "summary.json").write_text(json.dumps({"sentence": sent, "table": table}, indent=2), encoding="utf-8")
    print("SENTENCE:", sent)
    print("Wrote RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

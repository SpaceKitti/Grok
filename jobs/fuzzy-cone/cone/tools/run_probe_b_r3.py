#!/usr/bin/env python3
"""Probe B round 3 (wrad=1e4): step clamp C1, same 36 solves. Launch via launch_gated."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import probe_b as pb
from ring_projector import uk_now

CFG = "/workspace/lift/fuzz/cone/SWEEP_PROBE_B_R3_CONFIG.json"

def main():
    cfg = json.load(open(CFG))
    cfg["step_clamp"] = True
    print("START Probe B R3", uk_now(), "jobs", len(pb.jobs_B(cfg)), "clamp", cfg["step_clamp"], flush=True)
    t0 = time.time()
    table = pb.run_probe_B(cfg, force=True)
    print("DONE B R3 elapsed", round(time.time() - t0, 1), "ok", table.get("n_rows_ok"), flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

"""
F4 — Hybrid (Akitti blend). ONLY combination of F1 and F3.
Run AFTER F1 and F3 already have their own rows.
Still no U = exp(i π n_MHD).

  U_F4[γ] = U_CS[γ]  ·  U_3[γ]
  same meridian, same loop family.

This is a product of two named letters, not a fifth nickname and not a
new matrix that swallows F1–F5.
"""

from __future__ import annotations

import numpy as np

from protocol import score_S

FAMILY = "F4 hybrid"
INSERTED = False


def operator_block() -> str:
    return (
        "F4  hybrid on one meridian\n"
        "    U_F4[γ] = U_F1_CS[γ] × U_F3_holo[γ]\n"
        "    F1 vacuum A=0  and  F3 IR geodesic χ=βx\n"
        "    not exp(i π n_MHD)"
    )


def run(mhd: dict, f1: dict, f3: dict) -> dict:
    U_on = f1["U_on"] * f3["U_on"]
    U_off = f1["U_off"] * f3["U_off"]
    # spatial: both parents 0 on/off
    son, soff = 0.0, 0.0
    sc = score_S(U_on, U_off, son, soff, mhd["n_sheet"], mhd["i2"], mhd["i4"], True, INSERTED)
    return {
        "family": FAMILY,
        "operator": operator_block(),
        "inserted": INSERTED,
        "defined_without_mhd": True,
        "U_on": U_on,
        "U_off": U_off,
        "score": sc,
    }

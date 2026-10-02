"""Verdict: exactly one line."""
from __future__ import annotations


def verdict(rows) -> str:
    failed = [r["id"] for r in rows if not r["result"]]
    if not failed:
        return "SURFACE READY — QG probe may use D1–D7"
    return "SURFACE GAP — " + ", ".join(failed)

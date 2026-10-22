# Condensed raw outputs

Each file concatenates many per-run output files into one table. Every original row is kept.
Each row carries its source filename and a short hash of that source file, so it can be traced back.
_manifest.json lists every source file, its hash and row count, and which condensed file it went into.

Columns that came from ows_*.json sources are labelled c0..c8:
c0 = n, c1 = κ, c2 = α, c3 = mode index, c4 = ω², ..., last column = status.

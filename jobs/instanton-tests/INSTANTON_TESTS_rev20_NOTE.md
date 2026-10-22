# Note on INSTANTON_TESTS rev 20 (22C77378), 2026-10-16 03:50. Record-only; the spec is unchanged and Aethon stays pinned.
- IT1 guard split: 6+6 kept [Venus]; the earlier 3+3 cut preference is withdrawn (it saves only about 0.5 h).
- Relaxation check (report-only): fit the drift on two disjoint halves, 1.0→1.5·t_f and 1.5→2.0·t_f. Flag if they differ by more than 20% [assumed]. Aethon's overlapping windows (1.0→2 and 1.5→2) are rejected, because shared data makes the two fits agree by construction [Venus]. Fixed before any run.
- Cost [Aethon]: IT1 6+6 about 12.1 h, plus the δ pick (about 1.6 h for B10, about 4.0 h for B12). B12 is [scaled, not re-timed] until measured.
- TrinityOrb has been offline since about 03:22 and still runs rev 19. The rev 20 deploy package is rev20.tgz 7423F622; tests and smoke there are NOT COMPUTED (YET).

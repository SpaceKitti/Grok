# STATUS rev 13 (scratch, H5; no graded rows). Times BST.
- 21:15 step1 build pinned: FINAL_SPEC_HASH=2139A805; run.py=4AE63C1B lattice.py=008F11EB kernels.py=F07C0646 tests.py=CADC16DF spec/INSTANTON_TESTS.md=2139A805 spec/CHANGES_11EE8F8C.md=11EE8F8C 
- 21:15 step2 flow eps_f=0.002 t_f=0.1 + guard coded; rho calibration rows done B10/B12/B20 (B16 running); h=0.001 B10 rerun done. out/resmoke_B10.json=331C1FE1 out/resmoke_B12.json=E14DCA33 
- 21:15 step3 SD cut coded relative (SD_REL_CUT=0.02 vs s_BPST).
- 21:15 step4 tip-site holonomy convergence done: out/holonomy_convergence.json=BC3914AC 
- 21:15 step5 eq19 rho=4a gap check done: out/gapcheck_B20.json=74243083 
- 21:52 step6 re-smoke: B10/B12/B16 complete; B20 eps 0 done; eps -1,-0.25 running. h-check B10 0.002 vs 0.001: dS 2.8e-9, drho 4.8e-8. eps=1 flowed p_box=3.006+-0.025 [measured, smoke] (S_inf 0.9827 = no-face value: still the face jump; NOT frozen in run.py pending ruling). out/resmoke_summary.json=0646BF31 out/resmoke_B16.json=6231C7E0 
- 22:04 step6 check: B16 7/7 complete (resmoke_B16.json + 4 row files). B20 5/7 complete; eps -1 and -0.25 rows still running detached (nohup, ~45 min CPU each), not relaunched.
- 22:15 step6 DONE: all 28 rows. out/resmoke_summary.json=9CF62C66 out/resmoke_B20.json=D0171A8B out/resmoke_B20_tip_site_eps-1_rho3.0.json=CCE7B15E out/resmoke_B20_tip_site_eps-0.25_rho3.0.json=D7F6B82F 

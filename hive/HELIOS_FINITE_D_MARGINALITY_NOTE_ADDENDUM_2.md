# ADDENDUM 2 to HELIOS_FINITE_D_MARGINALITY_NOTE.md: corrections from Venus audit 68ecb793 (2026-11-10, UK)
STATUS: corrections only. Applies VENUS_FINITE_D_MARGINALITY_AUDIT.md (sha8 68ecb793). The original note and Addendum 1 are not overwritten. Banners point here.

## Withdrawn
- s6b (decaying-response bound gamma >= [1-(a/d)(1+theta)]/[2+theta-(a/d)(1+theta)]) is WITHDRAWN as an established bound. It drew f independently of the response, but virtual work forces f/f_typ = b W (LDW 1302.3990 Eq. 7, 10, p3-4). With f = bW, the a-dependence cancels exactly in kappa (LDW Eq. 20). The sentence "saturation REQUIRES a = 0" is also withdrawn, since it misreads an inequality (a > 0 would mean strictly stable, not forbidden). DEAD_ENDS line already added by Venus.

## Relabelled
- 6a: "gamma_x = gamma iff independence" becomes: independence is SUFFICIENT. The necessary and sufficient condition is P(h <= X|c|, c approaching) ~ X^{1-gamma} with an N-independent, non-zero conditional moment.
- s5: "in d=inf these closures hold" becomes "the d=inf exponents satisfy the saturated relation". The d=inf theory has no real-space floppy modes in which closures (ii)-(iii) can be stated.
- s3: Parisi-Zamponi 2606.03300 becomes [PROOF CLAIMED, preprint v1, d=inf only, conditional on its taken-as-given scaling equations, marginality identities and existence of the fullRSB profile (p4, s1.3)]. Their alpha = our gamma.
- s4 mixture: theta_eff is a pdf local exponent; 1411.3975 Fig. 1 plots the cdf. "Equal amplitudes" is an assumption. The theta_f-grows-with-d explanation is 1411.3975's own (p4).
- Citations: the "unanswered" quote is on 1411.3975 v2 p4 (not p5). 1410.4523: "except for a tiny region of the 1RSB breaking parameter". theta_e = 0.42311 (the paper's value; 0.42313 was rounding). PRE 111 045508 is a CPA for diluted networks/rigidity, read from the abstract only, and does not address gamma or theta.

## Addendum 1 corrections
- B: "MK certified jammed, hence one of L1-L3 false or pre-asymptotic" is INCOMPLETE. A third option: MK packings are LP-jammed (an exact local statement, see HELIOS_JAMMING_STABILITY_NOTIONS_NOTE.md s1) yet unstable in LDW's finite-opening sense. N^{+0.149} is asymptotic with unknown prefactors and is no finite-N contradiction. CHB21 p13 does compare sizes for f_l ("no clear finite N signature").
- C: rms argument wrong (already conceded in the closing-count note s4). "Which assumption differs: L3" does not follow. gamma_MK: "supported by FSS collapse; pure power law not reached" (CHB21 p11-12).
- A: kappa > 1 is a quadratic, local, one-mode diagnostic. LDW claim only kappa < 1 => unstable. For MK, all geometry uses the shifted distance |r_i - r_j + A_ij| (CHB21 p5).
- Symbol: Addendum 1's lambda = eta (a response exponent, not the hive coupling).

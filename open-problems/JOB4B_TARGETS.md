# Job 4B: toy-fit targets (3 CKM magnitudes + 4 quark mass ratios)

Checked 2026-10-02. Every input number below was read straight from the source PDFs with `pdftotext`, not from memory. The mass ratios are computed from those inputs and marked "computed". Nothing in this file is UNVERIFIED.

## Sources
- **[PDG26]** Particle Data Group, *Review of Particle Physics* (2026 edition): F. Takahashi et al. (PDG), Int. J. Mod. Phys. A 41, 2630011 (2026). Review used: "12. CKM Quark-Mixing Matrix", revised March 2026 by A. Ceccucci, Z. Ligeti, Y. Sakai. https://pdg.lbl.gov/2026/reviews/rpp2026-rev-ckm-matrix.pdf
- **[HZ21]** G.-y. Huang, S. Zhou, *Precise Values of Running Quark and Lepton Masses in the Standard Model*, Phys. Rev. D 103, 016010 (2021). https://arxiv.org/abs/2009.04851 , https://doi.org/10.1103/PhysRevD.103.016010 . This is the newest update in the Xing-Zhang-Zhou line (Zhou is a co-author of XZZ; Xing is not an author). It uses $\overline{\rm MS}$ masses with errors given as $\pm\sqrt{\delta_{\rm exp}^2+\delta_{\rm trunc}^2}$.
- **[XZZ12]** Z.-z. Xing, H. Zhang, S. Zhou, *Impacts of the Higgs mass on vacuum stability, running fermion masses and two-body Higgs decays*, Phys. Rev. D 86, 013013 (2012). https://arxiv.org/abs/1112.3112 , https://doi.org/10.1103/PhysRevD.86.013013 . Uses $M_H \simeq 125$ GeV.
- **[XZZ08]** Z.-z. Xing, H. Zhang, S. Zhou, *Updated Values of Running Quark and Lepton Masses*, Phys. Rev. D 77, 113016 (2008). https://arxiv.org/abs/0712.1419 , https://doi.org/10.1103/PhysRevD.77.113016 . The SM table above $M_Z$ uses $m_H = 140$ GeV and $\Lambda_{\rm GUT} = 2\times10^{16}$ GeV.

## Targets: primary set
CKM from the PDG 2026 global fit; masses from HZ21 at $\mu = M_Z$ (full SM).

| # | Target | Value | Uncertainty | Source, location | Scale | Link |
|---|---|---|---|---|---|---|
| 1 | $\lvert V_{us}\rvert$ | 0.22517 | ±0.00068 | PDG26 Eq. (12.27), global fit (CKMfitter method) | n/a | PDG26 URL above |
| 2 | $\lvert V_{cb}\rvert$ | 0.04189 | +0.00081 / −0.00069 | PDG26 Eq. (12.27), global fit | n/a | PDG26 |
| 3 | $\lvert V_{ub}\rvert$ | 0.003763 | +0.000088 / −0.000083 | PDG26 Eq. (12.27), global fit | n/a | PDG26 |
| 4 | $m_u/m_c$ | 1.98e-3 | ±0.34e-3 | computed from HZ21 Table 2 ($m_u = 1.23\pm0.21$ MeV, $m_c = 0.620\pm0.017$ GeV) | $M_Z$, full SM | arXiv:2009.04851 |
| 5 | $m_c/m_t$ | 3.685e-3 | ±0.10e-3 | computed from HZ21 Table 2 ($m_c = 0.620\pm0.017$ GeV, $m_t = 168.26\pm0.75$ GeV) | $M_Z$, full SM | arXiv:2009.04851 |
| 6 | $m_d/m_s$ | 5.02e-2 | ±0.56e-2 | computed from HZ21 Table 2 ($m_d = 2.67\pm0.19$ MeV, $m_s = 53.16\pm4.61$ MeV) | $M_Z$, full SM | arXiv:2009.04851 |
| 7 | $m_s/m_b$ | 1.87e-2 | ±0.16e-2 | computed from HZ21 Table 2 ($m_s = 53.16\pm4.61$ MeV, $m_b = 2.839\pm0.026$ GeV) | $M_Z$, full SM | arXiv:2009.04851 |

### Alternative CKM targets: PDG26 direct-measurement averages (no unitarity imposed)
| Target | Value | Source |
|---|---|---|
| $\lvert V_{us}\rvert$ | 0.22431 ± 0.00085 | PDG26 Eq. (12.8). Average of $K_{\ell3}$ and $K_{\mu2}$; error scaled by $\sqrt{\chi^2}=2.5$. |
| $\lvert V_{cb}\rvert$ | (40.7 ± 1.3)e-3 | PDG26 Eq. (12.11). Inclusive and exclusive combined; error scaled by $\sqrt{\chi^2}=3.7$. Exclusive alone is (39.5 ± 0.5)e-3. |
| $\lvert V_{ub}\rvert$ | (3.89 ± 0.16)e-3 | PDG26 Eq. (12.12). Inclusive (4.06 ± 0.11 ± 0.13 ± 0.18)e-3 and exclusive (3.75 ± 0.06 ± 0.19)e-3 combined; error scaled by $\sqrt{\chi^2}=1.1$. |

### Mass ratios at other scales and from other papers (all computed)
The $+/-$ errors combine the two masses' relative errors in quadrature, ignoring correlations.

| Source, location | Scale | $m_u/m_c$ | $m_c/m_t$ | $m_d/m_s$ | $m_s/m_b$ |
|---|---|---|---|---|---|
| HZ21 Table 2, full SM | $M_Z$ | 1.98e-3 ± 0.34e-3 | 3.685e-3 ± 0.10e-3 | 5.02e-2 ± 0.56e-2 | 1.87e-2 ± 0.16e-2 |
| HZ21 Table 2, full SM | $10^{12}$ GeV | 1.98e-3 ± 0.36e-3 | 3.33e-3 ± 0.11e-3 | 5.01e-2 ± 0.57e-2 | 2.07e-2 ± 0.18e-2 |
| XZZ12 Table I | $M_Z$ | 2.16e-3 +0.72/−0.66e-3 | 3.71e-3 +0.25/−0.49e-3 | 4.9e-2 +1.3/−1.8e-2 | 1.99e-2 +0.63/−0.43e-2 |
| XZZ12 Table I | $\Lambda_{\rm VS}\simeq4\times10^{12}$ GeV | 2.17e-3 +0.74/−0.66e-3 | 3.40e-3 +0.25/−0.49e-3 | 4.9e-2 +1.3/−1.7e-2 | 2.24e-2 +0.69/−0.45e-2 |
| XZZ08 Table IV (SM, $m_H=140$) | $M_Z$ | 2.05e-3 +0.85/−0.73e-3 | 3.61e-3 ± 0.49e-3 | 5.3e-2 ± 2.7e-2 | 1.90e-2 +0.56/−0.52e-2 |
| XZZ08 Table IV (SM, $m_H=140$) | $\Lambda_{\rm GUT}=2\times10^{16}$ GeV | 2.04e-3 +0.90/−0.78e-3 | 3.18e-3 +0.50/−0.49e-3 | 5.2e-2 ± 2.7e-2 | 2.20e-2 +0.71/−0.61e-2 |

Input masses at the high scales, read from the tables:
- HZ21, $10^{12}$ GeV: $m_u = 0.56\pm0.10$ MeV, $m_d = 1.24\pm0.09$ MeV, $m_s = 24.76\pm2.17$ MeV, $m_c = 0.283\pm0.009$ GeV, $m_b = 1.194\pm0.015$ GeV, $m_t = 85.07\pm0.89$ GeV.
- XZZ08, $\Lambda_{\rm GUT}$: $m_u = 0.48^{+0.20}_{-0.17}$ MeV, $m_d = 1.14^{+0.51}_{-0.48}$ MeV, $m_s = 22^{+7}_{-6}$ MeV, $m_c = 0.235^{+0.035}_{-0.034}$ GeV, $m_b = 1.00\pm0.04$ GeV, $m_t = 74.0^{+4.0}_{-3.7}$ GeV.

HZ21 Table 2 tabulates up to $10^{12}$ GeV and has no GUT-scale column. In the extracted text the HZ21 scale labels "105, 108, 1012" are $10^5$, $10^8$, $10^{12}$ GeV with the superscripts lost.

## Notes
- **Which scale to fit at.** Fit at $\mu = M_Z$ with HZ21 (full SM). It is the most precise and most recent set, and its errors are symmetric. Use a high scale only if the toy model is defined there: HZ21 at $10^{12}$ GeV, or XZZ08 at $\Lambda_{\rm GUT} = 2\times10^{16}$ GeV (older inputs, $m_H = 140$ GeV, errors several times larger). Never mix scales between ratios. The CKM magnitudes run only very weakly in the SM, so the PDG low-energy values can be used at $M_Z$.
- **Scheme independence.** In QCD the mass anomalous dimension is flavour-blind. So a ratio of two quark masses taken at the same scale in a mass-independent scheme ($\overline{\rm MS}$) is, to good approximation, independent of the scheme and of $\mu$, as long as no threshold or Yukawa effect separates the two quarks. This is why $m_u/m_c$ and $m_d/m_s$ barely change from $M_Z$ to $10^{12}$ GeV. Ratios involving third-generation quarks ($m_c/m_t$, $m_s/m_b$) do change with scale through Yukawa running (about 10% from $M_Z$ to $10^{12}$ GeV in HZ21). So: always quote the scale, and take both masses of a ratio from the same table row.
- **Correlations.** HZ21 gives the error correlation matrix at $M_Z$ (Tables 7–8), which the simple quadrature errors above ignore. Use it if the fit needs proper ratio errors.
- **Edition change.** The previous PDG CKM review (revised April 2024, at pdg.lbl.gov/2025) had global-fit $|V_{us}| = 0.22501$, $|V_{cb}| = 0.04183$, $|V_{ub}| = 0.003732$, and direct $|V_{cb}| = (41.1\pm1.2)\times10^{-3}$, $|V_{ub}| = (3.82\pm0.20)\times10^{-3}$. The 2026 values are slightly higher, except direct $|V_{cb}|$, which is lower.

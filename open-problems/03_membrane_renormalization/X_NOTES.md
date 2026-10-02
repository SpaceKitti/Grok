# Akitti's X notes: membrane / world-volume renormalization (problem 3)
Read 2026-10-02 from @Akitti's public profile in a browser (no API credits). Searches: membrane, supermembrane, renormalization, counterterm.
Excerpts are verbatim. Long posts are cut to the lines that matter for this problem, marked [...]. Open the link for the full text and code.

## 1. Where the divergences come from
Source: https://x.com/Akitti/status/2105747522497261789 (Oct 1, 2026). Full post:
> The concrete divergences (continuous spectrum + counterterm tower + UV blow-up) appear when the string density on the sphere is high enough that the discrete sum cannot be absorbed into a finite planar chart.

## 2. KK graviton cascade rate on hive towers (Lee-Randall-Riojas, arXiv:2609.36234, as cited)
Source: https://x.com/Akitti/status/2105213565841838133 (Sep 30, 2026)
> The cubic 5D graviton vertex is constrained by the massless 5D graviton EOM. Derivative-contracted pieces cancel. The surviving matrix element scales with daughter momentum \(q\), not with parent mass \(m_n\). The amplitude is therefore extra-suppressed by \((q/m_n)^4\) relative to the old GMOV-type estimates; two-body phase space then produces a universal \(q^5\) rate.
> \[ \Gamma_{n\to m,l} =\frac{\chi_{nml}^2\,q^5}{540\pi\Lambda^2 m_n^2}\, P\!\left(\frac{m_m}{m_n},\frac{m_l}{m_n}\right). \]
> - Black brane is a **target lab**, not a fold of GoldbergHexa. Licensed coupling is \(\Pi\cap S^2=S^1\) plus port current \(T^{r\theta}\). \(S^2\not\cong\mathbb{R}^2\).
> [...]
> Yes. On the actual 2–3 RB shells with port-supported \(\chi_{nml}\), the tower does not have open 2-body phase space. [...] What would threaten it is a dense KK continuum, which this stack does not carry.
(Orion: the post contains a full Python kernel and a 3-shell Robinson-Bertotti run; see the link. The arXiv id 2609.36234 has not been checked yet.)

## 3. Brane-map v0: the brane as a chart on the cut circle
Source: https://x.com/Akitti/status/2100870693873496486 (Sep 18, 2026)
> Domain: GoldbergHexa (probe complex). Sphere-map: \(\pi:\mathrm{GH}\to S^2\) still exists, but the brane does not use it as identity. Cut: \(\Pi\cap\pi(\mathrm{GH})=S^1_\Pi\).
> \[ T^{r\theta}_\ell=\sum_{e\pitchfork\Pi}e^{-i\ell\theta_e}\,j_e. \]
> [...] Cut is made. Brane-map is the belt. Sphere stays an image, not the lab.

## Gap (Orion)
No post gives a quantization or renormalization scheme for the membrane world-volume itself. What the posts offer is a hive reading: the divergences show up once the discrete sum on the sphere can't be absorbed into a finite chart. Paired with that is a slow KK drain law that keeps the remnants from emptying out.

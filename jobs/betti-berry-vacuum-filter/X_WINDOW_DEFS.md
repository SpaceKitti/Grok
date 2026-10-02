# Job Three: Akitti's own definitions on X (window, p(phi), filter details)
Read 2026-10-02 ~17:20 from @Akitti's public profile in a browser (read-only, no API credits). Nine searches run: window, "structure formation", percolation, occupancy, relaxon, Betti, "cosmological constant", monopole, freeze. The Articles tab was empty.
Quotes below are verbatim excerpts. Long posts are cut to the relevant lines, marked [...]. Full text of the two main posts is in X_POSTS_verbatim.md.

## Bottom line (Orion)
1. Structure-formation window: NOT DEFINED. Only the words "narrow window compatible with structure formation" appear. There are no numbers, bounds or Weinberg-type inequality. Keep 0.010-0.030 tagged [assumed input].
2. p(phi) and phi_0: NOT DEFINED. Scars survive above p_c and the system goes MBL below it. The only p_c values are for borrowed directed-percolation models (0.7055 DK, 0.38 3D bond-DP) and are not tied to V(phi). There is no phi_0. Keep p = clip(-phi/20) tagged [assumed input].
3. Betti-Berry filter: PARTIAL. The index k is never fixed (generic b_k(C)). There's no Berry-monopole formula. "Freeze" is qualitative: the scar projector engages after the spike and the Berry-Betti gap suppresses further rolling. The scar-floor projector ~0.041 appears in a separate post. A later variant adds a CSK theta-lock term to V(phi).

## A. Betti spike post (structure-formation window, freeze, b_k)
Source: https://x.com/Akitti/status/2105755883904831888 (Oct 1, 2026)
> At critical occupancy the homology changes: new independent cycles appear and the Betti numbers jump. Those jumps are the spikes.
> where \(b_{k}\) is the relevant Betti number of the percolating complex \(\mathcal{C}\) and \(L\) is the scale at which the spike locks. Once the homology saturates, further rolling is suppressed by the gap that the same Berry-Betti locking produces; the field freezes and the leftover density is the observed cosmological constant.
> Only those vacua whose fractal vacuum network produces a spike whose protected residue lies inside the narrow window compatible with structure formation remain populated; all others either cancel completely or overshoot into de Sitter or AdS regions that are dynamically inaccessible once the Betti lock engages.
> (with irrational \(\alpha\), golden-ratio or similar, so the minima form a Hofstadter-style self-similar set).
> Once the scar projector engages, further rolling is suppressed by the gap the same Berry-Betti locking produces. The field freezes and the protected residue is the leftover cosmological constant.

## B. Scar-floor projector value
Source: https://x.com/Akitti/status/2104923708053700844 (Sep 29, 2026)
> Those leftovers are stored by the scar-floor projector (\(\sim0.041\)) after quench.

## C. Occupancy p and p_c (percolation layer)
Source: https://x.com/Akitti/status/2095609094249824572 (Sep 3, 2026)
> Classical bond percolation is no longer a hard cut. It becomes a spider-fusion rewrite: same-type spiders fuse when a bond drops, so the effective dimension of the tensor network fluctuates with occupancy \(p\). Above \(p_c\) scars survive as deformable, scale-invariant manifolds; below \(p_c\) the system crosses into percolation-driven MBL. Parent Hamiltonian becomes weighted:
> \[ H(p)=\sum_{\langle i,j\rangle}w_{ij}(p)\,h_{ij} \]
> [...]
> - Truncated window: \(\ell_{\mathrm{inner}} < r < L_{\mathrm{outer}}\) (inner cutoff = Larmor / mean-free-path / grid scale; outer = MHD continuum).
(Orion: this "window" is a length-scale cutoff, not the rho_res window.)

Source: https://x.com/Akitti/status/2060759935604985918 (May 30, 2026; Boesl, Pollmann & Knap, arXiv:2605.26219)
> **Critical line** (p_c ≈ 0.7055 for p₂ = p₃ = p, p₁ = 0)
> [...]
> # Critical: p_c ≈ 0.38; algebraic corr ALL directions (Fig. S2)
(Orion: these are directed-percolation thresholds for the DK automaton and 3D bond-DP, not a relaxon map.)

Source: https://x.com/Akitti/status/2094755668011909144 (Sep 1, 2026)
> yesterday i was reading about how in percolation theory the lattice shape determines how fast the fluid flooding suddenly happens by dictating the network's connectivity and its specific percolation threshold. it undergoes an abrupt phase transition.
> maybe we could apply this to a pregeometric lattice and reimagine the propagation of information, causal relationships, or energy density towards emergent spacetime or quantum gravity topics

## D. Relaxon potential variant with CSK theta-lock
Source: https://x.com/Akitti/status/2063629659644846163 (Apr 21, 2026, as dated on X)
> **relaxon potentials** (Hofstadter-style V(φ) with golden-ratio α ≈ 1.618 modulation + ε[cos φ + β cos(αφ)] terms), **Betti/Berry flux spikes** (quantum scars that self-cancel bare vacuum energy down to topologically protected residuals)
> \[ \theta = \frac{12\pi^2}{\Lambda \ell_{\rm p}^2} \pmod{2\pi} \quad \Leftrightarrow \quad \Lambda = \frac{12\pi^2}{\theta \ell_{\rm p}^2} \]
> \[ \sigma_{\rm H} = \frac{3}{2\Lambda \ell_{\rm p}^2} \]
> The relaxon potential (already fractal-modulated) gains the CS term:
> \[ V(\phi) = \Lambda_0 + g\phi + \varepsilon[\cos\phi + \beta\cos(\alpha\phi)] + \sigma_{\rm H} \cdot |\text{CS}_{\rm disc}[U]| \]
> V_relaxon = Lambda + 0.1*phi + 0.01*(torch.cos(phi) + 0.618*torch.cos(1.618*phi))
(Orion: the code example uses g=0.1, eps=0.01, beta=0.618, alpha=1.618, with f=2*pi implied. These are example values from the post, not fitted ones. The CSK term is optional and was not in the Job Three brief.)

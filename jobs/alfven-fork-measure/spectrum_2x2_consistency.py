"""
CONSISTENCY ONLY — Layer A.3.
Rebuild the N=2 pair-A matrix. This is not MHD.
"""

from __future__ import annotations

import numpy as np

from spectrum_slab import A_REF, B_REF, ETA, V_REF, assemble_H


def pair_a_evals(eps: float, eta: float = ETA) -> np.ndarray:
    H = assemble_H(2, eps, eta)
    return np.linalg.eigvals(H)


def ref_matrix(eps: float) -> np.ndarray:
    return np.array(
        [[-1j * A_REF, eps * V_REF], [eps * V_REF, -1j * B_REF]],
        dtype=complex,
    )

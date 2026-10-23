"""Rev 6: over-improved action S(eps) of Garcia Perez et al. NPB413 (1994): (4-eps)/3 * 1x1 + (eps-1)/48 * 2x2 (eps=1 Wilson, eps=0 tree-level LW)."""
import numpy as np, run as R, hashlib, os
from kernels import Loops
from lattice import Lattice
def _lat(): return Lattice(4, 4, 6, 6, alpha=1.0)
def test_eps1_has_no_2x2_and_eps_m1_does():
    lat = _lat(); assert all(c["size"] == 1 for c in Loops(lat, 1).cls) and any(c["size"] == 2 for c in Loops(lat, -1).cls)
def test_eps_coefficients():
    c = lambda e: ((4-e)/3, (e-1)/48)
    assert c(1) == (1.0, 0.0) and c(0) == (4/3, -1/48) and c(-1) == (5/3, -1/24)
    src = open(os.path.join(R.HERE, "kernels.py"), encoding="utf-8").read(); assert "c11, c22 = (4-eps)/3, (eps-1)/48" in src
    assert "c11 = (4-eps)/3; c22 = (eps-1)/48" in open(os.path.join(R.HERE, "lattice.py"), encoding="utf-8").read()
def test_eq19_small_a_sign():
    # NPB413 eq. (19): S(eps)/8pi^2 = 1 - (eps/5)(a/rho)^2 + ...: eps=-1 lies ABOVE 1 at O(a^2), eps=1 below
    assert R.eq19(-1, 3.0) > 0 > R.eq19(1, 3.0) and abs(R.eq19(-1, 3.0) - (1/45 + 27/210/81)) < 1e-12
def test_eps_flows_monotone_small():
    from kernels import generic_seed
    lat = _lat(); c = (0., 0., lat.x3[3], lat.x4[3])
    for e in (1, -1):
        lp = Loops(lat, e); U = generic_seed(lat, 1.5, seed=0, centre=c); S0 = lp.action(U); U1, _ = lp.flow(U, h=0.002, max_steps=5, record=5)
        assert lp.action(U1) <= S0
def test_eps1_flow_deterministic_bitwise():
    from kernels import generic_seed
    lat = _lat(); c = (0., 0., lat.x3[3], lat.x4[3]); U = generic_seed(lat, 1.5, seed=0, centre=c)
    a, _ = Loops(lat, 1).flow(U.copy(), h=0.002, max_steps=3, record=3); b, _ = Loops(lat, 1.0).flow(U.copy(), h=0.002, max_steps=3, record=3)
    assert np.array_equal(a, b)

def test_normalisation_c11_plus_16c22():
    for e in (1, 0, -1): assert abs((4-e)/3 + 16*(e-1)/48 - 1) < 1e-15
    assert (4-(-1))/3 == 5/3 and ((-1)-1)/48 == -1/24
def test_eps_enters_force():
    from kernels import generic_seed
    lat = _lat(); c = (0., 0., lat.x3[3], lat.x4[3]); U = generic_seed(lat, 1.5, seed=0, centre=c)
    g1, gm = Loops(lat, 1).grad(U), Loops(lat, -1).grad(U); assert not np.allclose(g1, gm)
    lp = Loops(lat, -1); X = np.random.default_rng(1).standard_normal((lp.NL, 3))*1e-6; X[lp.frozen] = 0
    dS = lp.action(lp.step(U, X)) - lp.action(U); assert abs(dS - np.sum(lp.grad(U)*X)) < 0.1*abs(dS)   # first-order check at |X|~1e-6 (O(X^2) + round-off)
def test_2x2_are_squares():
    for cc in Loops(_lat(), -1).cls:
        if cc["size"] == 2: assert cc["ids"].shape[1] == 8
def test_spec_hash_guard(): assert R.IT1B_SPEC == "E360229B" and R.it1b_spec_ok()

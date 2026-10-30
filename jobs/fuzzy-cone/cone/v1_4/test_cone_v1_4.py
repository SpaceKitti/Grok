import inspect, re, numpy as np
from cone_v1_4 import *
def test_C8_no_exponent_in_seed():
    src = inspect.getsource(fuzzy_seed).split('"""')[-1]
    assert "alpha" not in src and not re.search(r"n\s*/", src)
def test_seed_neutral_tip():
    f, a = fuzzy_seed(np.array([0.0, 5.0]), 1); assert f[0] == 0 and a[0] == 0 and f[1] > 0.99
def test_gauss_bonnet():
    for al in (0.9, 0.75, 0.5, 1/3, 2.0): assert curvature_check(al)[2] < 0.01
def test_metric_tip_is_cone():
    assert abs(metric_h(1e-4, 0.5) / 1e-4 - 0.5) < 1e-6

import numpy as np
from simulate_Hull_White_One_Factor import simulate_Hull_White_One_Factor


# The DataFrame used to be built inside the loop, so a single time point raised UnboundLocalError
def test_single_time_point():
    out = simulate_Hull_White_One_Factor(0.02, 0.04, 0.01, np.array([0.0]), np.array([0.02]))
    assert out.shape == (1, 1)
    assert out["Interest Rate"].iloc[0] == 0.02

# Without noise, starting from the first forward rate, the short rate follows the forward curve
def test_deterministic_path_follows_forward_curve():
    t = np.arange(0, 11, dtype=float)
    f = 0.02 + 0.001 * t
    out = simulate_Hull_White_One_Factor(f[0], 0.1, 0.0, t, f)
    assert np.allclose(out["Interest Rate"].values, f)

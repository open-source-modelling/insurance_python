import numpy as np
import pytest
from Vasicek_one_factor import simulate_Vasicek_One_Factor


# 0.3 / 0.1 = 2.9999999999999996 in floating point, which int() used to truncate, giving a grid with step 0.15
def test_time_grid_when_T_over_dt_is_not_exact_in_floating_point():
    out = simulate_Vasicek_One_Factor(0.1, 1.0, 0.1, 0.2, 0.3, 0.1)
    assert np.allclose(out.index.values, [0, 0.1, 0.2, 0.3])

def test_T_not_multiple_of_dt_raises():
    with pytest.raises(ValueError, match="multiple of dt"):
        simulate_Vasicek_One_Factor(0.1, 1.0, 0.1, 0.2, 10, 0.3)

# Without noise the rate follows lam + (r0 - lam) * exp(-a * t) exactly at the grid times
def test_deterministic_path_matches_exact_solution():
    r0, a, lam = 0.05, 2.0, 0.03
    out = simulate_Vasicek_One_Factor(r0, a, lam, 0.0, 0.3, 0.1)
    t = out.index.values
    assert np.allclose(out["Interest Rate"].values, lam + (r0 - lam) * np.exp(-a * t))

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

# a = 0 used to return NaN rates with a RuntimeWarning (the noise variance was 0 / 0), and a negative a
# gave a process that drifts away from lam instead of reverting to it
@pytest.mark.parametrize("a", [0, -1.0, np.nan, np.inf])
def test_non_positive_speed_of_reversion_raises(a):
    with pytest.raises(ValueError, match="a must be positive"):
        simulate_Vasicek_One_Factor(0.1, a, 0.1, 0.02, 1, 0.5)

# A negative sigma used to be accepted silently
@pytest.mark.parametrize("sigma", [-0.02, np.nan, np.inf])
def test_negative_or_non_finite_sigma_raises(sigma):
    with pytest.raises(ValueError, match="sigma must be non-negative"):
        simulate_Vasicek_One_Factor(0.1, 1.0, 0.1, sigma, 1, 0.5)

# A negative T with a negative dt used to pass the multiple-of-dt check and return NaN rates on a negative time grid.
# dt = 0 raised ZeroDivisionError, a NaN T an unrelated message from int(), and an infinite T an OverflowError
@pytest.mark.parametrize("T, dt", [(-1, -0.5), (1, 0), (1, -0.5), (-1, 0.5), (0, 0.5), (np.nan, 0.5), (1, np.nan), (np.inf, 0.5)])
def test_non_positive_or_non_finite_T_or_dt_raises(T, dt):
    with pytest.raises(ValueError, match="T and dt must be positive"):
        simulate_Vasicek_One_Factor(0.1, 1.0, 0.1, 0.02, T, dt)

# NaN or infinite starting or long-term rates used to give a path of NaN or infinite rates
@pytest.mark.parametrize("r0, lam", [(np.nan, 0.1), (0.1, np.nan), (np.inf, 0.1), (0.1, -np.inf)])
def test_non_finite_r0_or_lam_raises(r0, lam):
    with pytest.raises(ValueError, match="r0 and lam must be finite"):
        simulate_Vasicek_One_Factor(r0, 1.0, lam, 0.02, 1, 0.5)

# The checks must not reject valid inputs: the Vasicek model allows negative rates, and sigma = 0 is the deterministic path
@pytest.mark.filterwarnings("error")
@pytest.mark.parametrize("r0, lam, sigma", [(-0.01, -0.005, 0.02), (0.02, -0.01, 0.0), (0.0, 0.0, 0.01)])
def test_negative_rates_and_zero_volatility_are_accepted(r0, lam, sigma):
    out = simulate_Vasicek_One_Factor(r0, 1.0, lam, sigma, 1, 0.5)
    assert out["Interest Rate"].iloc[0] == r0
    assert np.all(np.isfinite(out["Interest Rate"].values))

import numpy as np
import pytest
from Dothan_one_factor import simulate_Dothan_One_Factor


def test_time_grid_when_T_over_dt_is_not_exact_in_floating_point():
    out = simulate_Dothan_One_Factor(0.1, 1.0, 0.2, 0.3, 0.1)
    assert np.allclose(out.index.values, [0, 0.1, 0.2, 0.3])

def test_T_not_multiple_of_dt_raises():
    with pytest.raises(ValueError, match="multiple of dt"):
        simulate_Dothan_One_Factor(0.1, 1.0, 0.2, 10, 0.3)

# The old normal approximation gave negative rates on most paths with a large volatility
def test_rates_stay_positive_with_large_volatility():
    np.random.seed(0)
    for _ in range(50):
        out = simulate_Dothan_One_Factor(0.05, 0.1, 1.0, 10, 1.0)
        assert (out["Interest Rate"].values > 0).all()

# dr = -a r dt + sigma r dW: log(r(t+dt) / r(t)) is normal with mean (-a - sigma^2/2) dt and variance sigma^2 dt
def test_log_increments_have_gbm_moments():
    np.random.seed(0)
    a, sigma, dt = 0.1, 0.2, 0.1
    out = simulate_Dothan_One_Factor(0.05, a, sigma, 2000, dt)
    log_increments = np.diff(np.log(out["Interest Rate"].values))
    assert np.mean(log_increments) == pytest.approx((-a - 0.5 * sigma**2) * dt, abs=0.002)
    assert np.var(log_increments) == pytest.approx(sigma**2 * dt, rel=0.05)

# Without noise the rate is r0 * exp(-a * t)
def test_deterministic_path():
    out = simulate_Dothan_One_Factor(0.05, 0.5, 0.0, 2, 0.5)
    t = out.index.values
    assert np.allclose(out["Interest Rate"].values, 0.05 * np.exp(-0.5 * t))

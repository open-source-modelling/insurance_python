import numpy as np
import pytest
from simulate_black_scholes import simulate_black_scholes


# 0.3 / 0.1 = 2.9999999999999996 in floating point, which int() used to truncate to 2 steps
def test_time_grid_when_T_over_dt_is_not_exact_in_floating_point():
    out = simulate_black_scholes(100, 0.05, 0.3, 0.3, 0.1)
    assert np.allclose(out.index.values, [0, 0.1, 0.2, 0.3])

def test_T_not_multiple_of_dt_raises():
    with pytest.raises(ValueError, match="multiple of dt"):
        simulate_black_scholes(100, 0.05, 0.3, 10, 0.3)

# Log returns over a step dt have variance sigma^2 * dt
def test_log_return_variance():
    np.random.seed(0)
    sigma, dt = 0.3, 0.01
    out = simulate_black_scholes(100, 0.05, sigma, 200, dt)
    log_returns = np.diff(np.log(out["Simulation"].values))
    assert np.var(log_returns) == pytest.approx(sigma**2 * dt, rel=0.05)

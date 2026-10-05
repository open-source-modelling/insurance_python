import numpy as np
import pytest
from simulate_Hull_White_One_Factor import simulate_Hull_White_One_Factor


# A single time point today gives today's short rate, which is the first forward rate
def test_single_time_point():
    out = simulate_Hull_White_One_Factor(0.04, 0.01, np.array([0.0]), np.array([0.02]))
    assert out.shape == (1, 1)
    assert out["Interest Rate"].iloc[0] == 0.02

# Without noise the short rate follows the forward curve
def test_deterministic_path_follows_forward_curve():
    t = np.arange(0, 11, dtype=float)
    f = 0.02 + 0.001 * t
    out = simulate_Hull_White_One_Factor(0.1, 0.0, t, f)
    assert np.allclose(out["Interest Rate"].values, f)

# Today's short rate is f(0,0), also when the rate is random afterwards
def test_first_value_is_todays_forward_rate():
    np.random.seed(0)
    out = simulate_Hull_White_One_Factor(0.1, 0.01, np.array([0.0, 1.0, 2.0]), np.array([0.025, 0.03, 0.035]))
    assert out["Interest Rate"].iloc[0] == 0.025

# r(t) is normal with mean alpha(t) = f(0,t) + sigma^2 / (2 a^2) * (1 - exp(-a t))^2 and variance
# sigma^2 / (2 a) * (1 - exp(-2 a t)), with t measured from today, also when the grid does not start today
@pytest.mark.parametrize("t", [np.array([0.0, 1.0, 5.0, 10.0]), np.array([1.0, 5.0, 10.0])])
def test_mean_and_variance_of_the_short_rate(t):
    np.random.seed(0)
    a, sigma, n = 0.04, 0.01, 4000
    f = 0.02 + 0.002 * t
    rates = np.array([simulate_Hull_White_One_Factor(a, sigma, t, f)["Interest Rate"].values for _ in range(n)])
    mean = f + sigma**2 / (2 * a**2) * (1 - np.exp(-a * t))**2
    var = sigma**2 / (2 * a) * (1 - np.exp(-2 * a * t))
    assert np.allclose(rates.mean(axis=0), mean, rtol=0, atol=4 * np.sqrt(var.max() / n))
    assert np.allclose(rates.var(axis=0), var, rtol=0.1, atol=1e-12)

# The model reproduces today's term structure: the simulated price of a zero coupon bond, E[exp(-integral of r)],
# equals the market price exp(-integral of f(0,s)). When the code started at r0 = f(0,0) - 1%, the 5-year price was 4.6% too high
def test_bond_price_matches_market_curve():
    np.random.seed(0)
    a, sigma, n = 0.04, 0.01, 3000
    t = np.linspace(0, 5, 21)
    f = 0.02 + 0.002 * t
    def integral(y):  # trapezoidal rule on the grid t
        return np.sum((y[1:] + y[:-1]) / 2 * np.diff(t))
    discount = [np.exp(-integral(simulate_Hull_White_One_Factor(a, sigma, t, f)["Interest Rate"].values)) for _ in range(n)]
    assert np.mean(discount) == pytest.approx(np.exp(-integral(f)), rel=0.005)

@pytest.mark.parametrize("t, f", [(np.array([0.0, 2.0, 1.0]), np.full(3, 0.03)),
                                  (np.array([-1.0, 0.0]), np.full(2, 0.03)),
                                  (np.array([0.0, 1.0]), np.full(3, 0.03))])
def test_invalid_time_grid_raises(t, f):
    with pytest.raises(ValueError):
        simulate_Hull_White_One_Factor(0.04, 0.01, t, f)

# The speed of mean reversion must be positive. a = 0 used to raise ZeroDivisionError or give NaNs,
# and a negative a raised an unclear "scale < 0" error
@pytest.mark.parametrize("a", [0, np.float64(0.0), -0.04, np.nan])
def test_non_positive_mean_reversion_raises(a):
    with pytest.raises(ValueError, match="a must be positive"):
        simulate_Hull_White_One_Factor(a, 0.01, np.arange(0, 4.0), np.full(4, 0.03))

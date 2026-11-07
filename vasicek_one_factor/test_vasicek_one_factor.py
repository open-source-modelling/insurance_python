import numpy as np
import pytest
from scipy import stats
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

# Over a step dt, the exact solution of dr = a (lam - r) dt + sigma dW is
#   r(t + dt) = r(t) e^(-a dt) + lam (1 - e^(-a dt)) + sigma sqrt((1 - e^(-2 a dt)) / (2 a)) Z,   Z ~ N(0, 1),
# with Z independent of everything before t. Standardising every step therefore gives independent N(0, 1) residuals.
# a * dt = 1 is large on purpose: an Euler step r(t) + a (lam - r(t)) dt + sigma sqrt(dt) Z would give residuals with a
# standard deviation of about 1.6 and a lag-1 autocorrelation of about -0.3, so the test also checks that the step is exact
def test_each_step_has_the_exact_transition_distribution():
    r0, a, lam, sigma, dt, n = 0.05, 2.0, 0.03, 0.01, 0.5, 20000
    np.random.seed(0)
    r = simulate_Vasicek_One_Factor(r0, a, lam, sigma, n * dt, dt)["Interest Rate"].values
    decay = np.exp(-a * dt)
    z = (r[1:] - r[:-1] * decay - lam * (1 - decay)) / (sigma * np.sqrt((1 - decay**2) / (2 * a)))
    # The tolerances are 4 standard errors, so the test does not depend on the seed: 1 / sqrt(n) for the mean and
    # the autocorrelation, 1 / sqrt(2 n) for the standard deviation
    assert z.size == n
    assert abs(z.mean()) < 4 / np.sqrt(n)
    assert abs(z.std() - 1) < 4 / np.sqrt(2 * n)
    assert abs(np.corrcoef(z[:-1], z[1:])[0, 1]) < 4 / np.sqrt(n)
    assert stats.kstest(z, "norm").pvalue > 0.01

# In the long run the Vasicek rate forgets r0 and settles into its stationary distribution: normal with mean lam and
# variance sigma^2 / (2 a), where values a time h apart have correlation e^(-a h). The simulated grid is the AR(1) process
#   r(k) = rho r(k-1) + (1 - rho) lam + noise,   rho = e^(-a dt),
# whose stationary variance is sigma^2 / (2 a) exactly for any dt (an Euler step would give sigma^2 / (a (2 - a dt)))
def test_path_settles_into_the_stationary_distribution():
    r0, a, lam, sigma, dt, T = 0.08, 2.0, 0.03, 0.02, 0.25, 10000
    np.random.seed(0)
    r = simulate_Vasicek_One_Factor(r0, a, lam, sigma, T, dt)["Interest Rate"].values
    x = r[int(round(10 / a / dt)):] # drop the first 10 / a years: only e^(-10) of the starting gap r0 - lam is left after them
    n, rho, v = x.size, np.exp(-a * dt), sigma**2 / (2 * a)
    # Tolerances are 4 standard errors. Consecutive values are correlated, which widens the standard errors of the mean
    # and the variance by the factors (1 + rho) / (1 - rho) and (1 + rho^2) / (1 - rho^2) compared with independent values
    assert abs(x.mean() - lam) < 4 * np.sqrt(v / n * (1 + rho) / (1 - rho))
    assert abs(x.var() / v - 1) < 4 * np.sqrt(2 / n * (1 + rho**2) / (1 - rho**2))
    assert abs(np.corrcoef(x[:-1], x[1:])[0, 1] - rho) < 4 * np.sqrt((1 - rho**2) / n)

# Starting from a fixed r0, the rate at time t is normal with
#   mean      m(t) = lam + (r0 - lam) e^(-a t)
#   variance  v(t) = sigma^2 (1 - e^(-2 a t)) / (2 a)
# Simulating many paths with repeated calls checks these at every grid time, including the early times where the rate
# has not settled yet. Each call must also give a new path, independent of the previous one
def test_many_paths_have_the_exact_mean_and_variance_at_every_time():
    r0, a, lam, sigma, T, dt, n_paths = 0.08, 0.5, 0.03, 0.02, 2, 0.5, 2000
    np.random.seed(0)
    paths = np.array([simulate_Vasicek_One_Factor(r0, a, lam, sigma, T, dt)["Interest Rate"].values for _ in range(n_paths)])
    t = np.arange(0, T + dt / 2, dt)
    m = lam + (r0 - lam) * np.exp(-a * t)
    v = sigma**2 * (1 - np.exp(-2 * a * t)) / (2 * a)
    assert np.all(paths[:, 0] == r0)
    # Tolerances are 4 standard errors: sqrt(v / n) for a mean, sqrt(2 / (n - 1)) for a variance ratio, 1 / sqrt(n) for a correlation
    assert np.all(np.abs(paths[:, 1:].mean(axis=0) - m[1:]) < 4 * np.sqrt(v[1:] / n_paths))
    assert np.all(np.abs(paths[:, 1:].var(axis=0, ddof=1) / v[1:] - 1) < 4 * np.sqrt(2 / (n_paths - 1)))
    assert abs(np.corrcoef(paths[:-1, -1], paths[1:, -1])[0, 1]) < 4 / np.sqrt(n_paths - 1)

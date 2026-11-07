import numpy as np
import pytest
from scipy import stats
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

# dr = -a r dt + sigma r dW. By Ito's lemma d(log r) = (-a - sigma^2 / 2) dt + sigma dW, so over a step dt
#   log(r(t + dt) / r(t)) ~ N((-a - sigma^2 / 2) dt, sigma^2 dt),   independent of everything before t,
# and the standardised log increments are independent N(0, 1). The Ito correction -sigma^2 / 2 is what keeps
# E[r(t)] = r0 e^(-a t); without it the mean rate would be too high by a factor e^(sigma^2 t / 2).
# The 20,000 steps come from 200 paths of 25 years: one 5,000-year path would shrink to about 1e-320, where a float
# keeps only two or three significant digits and the log increments would be wrong
def test_each_step_has_the_exact_lognormal_distribution():
    r0, a, sigma, T, dt, n_paths = 0.05, 0.1, 0.3, 25, 0.25, 200
    np.random.seed(0)
    paths = np.array([simulate_Dothan_One_Factor(r0, a, sigma, T, dt)["Interest Rate"].values for _ in range(n_paths)])
    z = (np.diff(np.log(paths), axis=1) - (-a - sigma**2 / 2) * dt) / (sigma * np.sqrt(dt))
    n = z.size
    # Tolerances are 4 standard errors: 1 / sqrt(n) for the mean and the autocorrelation, 1 / sqrt(2 n) for the standard deviation
    assert n == n_paths * round(T / dt)
    assert abs(z.mean()) < 4 / np.sqrt(n)
    assert abs(z.std() - 1) < 4 / np.sqrt(2 * n)
    assert abs(np.corrcoef(z[:, :-1].ravel(), z[:, 1:].ravel())[0, 1]) < 4 / np.sqrt(n)
    assert stats.kstest(z.ravel(), "norm").pvalue > 0.01

# Starting from r0, log r(t) = log r0 + (-a - sigma^2 / 2) t + sigma W(t), so at each time t
#   log r(t) ~ N(log r0 - (a + sigma^2 / 2) t, sigma^2 t)
#   E[r(t)] = r0 e^(-a t),   Var[r(t)] = r0^2 e^(-2 a t) (e^(sigma^2 t) - 1)
# Simulating many paths with repeated calls checks these at every grid time. Each call must also give a new path,
# independent of the previous one
def test_many_paths_have_the_exact_lognormal_distribution_at_every_time():
    r0, a, sigma, T, dt, n_paths = 0.05, 0.5, 0.3, 2, 0.5, 2000
    np.random.seed(0)
    paths = np.array([simulate_Dothan_One_Factor(r0, a, sigma, T, dt)["Interest Rate"].values for _ in range(n_paths)])
    t = np.arange(0, T + dt / 2, dt)[1:]
    r, log_r = paths[:, 1:], np.log(paths[:, 1:])
    assert np.all(paths[:, 0] == r0)
    # Tolerances are 4 standard errors: sqrt(variance / n) for a mean, sqrt(2 / (n - 1)) for a variance ratio of normal
    # values, 1 / sqrt(n) for a correlation
    var_r = r0**2 * np.exp(-2 * a * t) * (np.exp(sigma**2 * t) - 1)
    assert np.all(np.abs(r.mean(axis=0) - r0 * np.exp(-a * t)) < 4 * np.sqrt(var_r / n_paths))
    assert np.all(np.abs(log_r.mean(axis=0) - (np.log(r0) - (a + sigma**2 / 2) * t)) < 4 * np.sqrt(sigma**2 * t / n_paths))
    assert np.all(np.abs(log_r.var(axis=0, ddof=1) / (sigma**2 * t) - 1) < 4 * np.sqrt(2 / (n_paths - 1)))
    assert abs(np.corrcoef(log_r[:-1, -1], log_r[1:, -1])[0, 1]) < 4 / np.sqrt(n_paths - 1)

# Without noise the rate is r0 * exp(-a * t)
def test_deterministic_path():
    out = simulate_Dothan_One_Factor(0.05, 0.5, 0.0, 2, 0.5)
    t = out.index.values
    assert np.allclose(out["Interest Rate"].values, 0.05 * np.exp(-0.5 * t))

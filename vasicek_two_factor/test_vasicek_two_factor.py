import numpy as np
import pytest
from Vasicek import BrownianMotion
from Pricing import ZeroCouponBond


# Increments of a Brownian motion over a step dt have variance dt
@pytest.mark.parametrize("dt", [0.1, 0.01])
def test_wiener_increment_variance_is_dt(dt):
    np.random.seed(0)
    W = BrownianMotion().generate_weiner_process(T=2000*dt, dt=dt)
    assert np.var(np.diff(W)) == pytest.approx(dt, rel=0.1)

# Same for both paths of the two-dimensional process, which should also have correlation rho
def test_correlated_wiener_increments():
    np.random.seed(0)
    dt = 0.01
    rho = 0.4
    W_1, W_2 = BrownianMotion().generate_weiner_process(T=20000*dt, dt=dt, rho=rho)
    dW_1, dW_2 = np.diff(W_1), np.diff(W_2)
    assert np.var(dW_1) == pytest.approx(dt, rel=0.05)
    assert np.var(dW_2) == pytest.approx(dt, rel=0.05)
    assert np.corrcoef(dW_1, dW_2)[0, 1] == pytest.approx(rho, abs=0.03)

# rho = 0 means two uncorrelated Brownian motions, not a one-dimensional one
def test_zero_correlation_gives_two_paths():
    np.random.seed(0)
    W = BrownianMotion().generate_weiner_process(T=1, dt=0.01, rho=0.0)
    assert len(W) == 2
    out = BrownianMotion().simulate_Vasicek_Two_Factor(rho=0.0)
    assert out.shape[1] == 2

# The time index used to have T/dt points with a step slightly larger than dt (0.10019 for T = 52, dt = 0.1)
def test_time_grid_has_step_dt():
    np.random.seed(0)
    out = BrownianMotion().simulate_Vasicek_Two_Factor(T=52, dt=0.1)
    assert out.shape == (521, 2)
    assert np.allclose(np.diff(out.index.values), 0.1)
    assert out.index[-1] == pytest.approx(52)

def test_T_not_multiple_of_dt_raises():
    with pytest.raises(ValueError, match="multiple of dt"):
        BrownianMotion().simulate_Vasicek_Two_Factor(T=10, dt=0.3)

# A correlation outside [-1, 1] used to give NaN nominal rates (with only a NumPy warning, or none for NaN),
# and rho = None an unrelated TypeError
@pytest.mark.parametrize("rho", [1.5, -2, np.nan, None])
def test_invalid_rho_raises(rho):
    with pytest.raises(ValueError, match="between -1 and 1"):
        BrownianMotion().simulate_Vasicek_Two_Factor(rho=rho, T=1, dt=0.1)
    if rho is not None: # None is valid here: it asks for one Brownian motion
        with pytest.raises(ValueError, match="between -1 and 1"):
            BrownianMotion().generate_weiner_process(1, 0.1, rho)

# rho = -1 and 1 are valid: the two Brownian motions are perfectly correlated
@pytest.mark.parametrize("rho", [-1, 1])
def test_perfect_correlation_is_valid(rho):
    out = BrownianMotion().simulate_Vasicek_Two_Factor(rho=rho, T=1, dt=0.1)
    assert np.isfinite(out.values).all()

# Each parameter list needs one value for the real rate and one for inflation. A third value used to be ignored
# without an error, and a single value raised an IndexError
@pytest.mark.parametrize("argument", ["r0", "a", "b", "sigma"])
@pytest.mark.parametrize("value", [[0.1], [0.1, 0.1, 0.1]])
def test_parameter_lists_need_two_elements(argument, value):
    with pytest.raises(ValueError, match=f"{argument} must have 2 elements"):
        BrownianMotion().simulate_Vasicek_Two_Factor(**{argument: value}, T=1, dt=0.1)

# Without noise and starting at the long-term means, the nominal rate is constant at b[0] + b[1],
# so the bond price is exp(-(b[0] + b[1]) * maturity). The old code integrated with a step of 1 instead of dt,
# over the whole simulation horizon instead of up to maturity, and used the real rate
def test_zero_coupon_bond_price_with_constant_rates():
    b = [0.01, 0.02]
    bond = ZeroCouponBond(2)
    price = bond.price(b, [1.0, 1.0], b, [0.0, 0.0], 0.5, 5, 0.1, 3)
    assert price == pytest.approx(np.exp(-(b[0] + b[1]) * 2))
    assert bond._price == price
    assert bond.price_Vasicek_Two_Factor(b, [1.0, 1.0], b, [0.0, 0.0], 0.5, 5, 0.1, 3) == pytest.approx(price)

def test_zero_coupon_bond_maturity_checks():
    with pytest.raises(ValueError, match="at least the maturity"):
        ZeroCouponBond(2).price([0.01, 0.02], [1.0, 1.0], [0.01, 0.02], [0.0, 0.0], 0.5, 1, 0.1, 1)
    with pytest.raises(ValueError, match="multiple of dt"):
        ZeroCouponBond(1.25).price([0.01, 0.02], [1.0, 1.0], [0.01, 0.02], [0.0, 0.0], 0.5, 2, 0.5, 1)

# The rates are simulated with the exact transition, so large time steps do not distort the distribution.
# The Euler scheme used before overstated the long-run variances by 24% and 32% for these parameters.
def test_long_run_moments_with_large_time_step():
    np.random.seed(0)
    a, b, sigma, rho, dt = [0.8, 1.0], [0.01, 0.015], [0.05, 0.04], 0.6, 0.5
    out = BrownianMotion().simulate_Vasicek_Two_Factor(b, a, b, sigma, rho, 50000, dt)
    real = out["Real Interest Rate"].values
    inflation = out["Nominal Interest Rate"].values - real
    assert np.var(real) == pytest.approx(sigma[0]**2 / (2 * a[0]), rel=0.05)
    assert np.var(inflation) == pytest.approx(sigma[1]**2 / (2 * a[1]), rel=0.05)
    assert np.corrcoef(real, inflation)[0, 1] == pytest.approx(2 * rho * np.sqrt(a[0] * a[1]) / (a[0] + a[1]), abs=0.02)

# Without noise each rate follows b + (r0 - b) * exp(-a * t) exactly at the grid times
def test_deterministic_path_matches_exact_solution():
    r0, a, b = [0.05, 0.03], [0.8, 1.0], [0.01, 0.015]
    out = BrownianMotion().simulate_Vasicek_Two_Factor(r0, a, b, [0.0, 0.0], 0.6, 5, 0.5)
    t = out.index.values
    real = b[0] + (r0[0] - b[0]) * np.exp(-a[0] * t)
    inflation = b[1] + (r0[1] - b[1]) * np.exp(-a[1] * t)
    assert np.allclose(out["Real Interest Rate"].values, real)
    assert np.allclose(out["Nominal Interest Rate"].values, real + inflation)

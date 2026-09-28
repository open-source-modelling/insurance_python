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

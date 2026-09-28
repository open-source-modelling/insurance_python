import numpy as np
import pytest
from Vasicek import BrownianMotion


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

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest
import warnings
from ssaBasic import ssaBasic

warnings.filterwarnings("ignore", category=UserWarning) # plt.show() on the Agg backend

@pytest.fixture
def series():
    np.random.seed(0)
    t = np.arange(120)
    return 5 + 0.05*t + np.sin(2*np.pi*t/12) + 0.2*np.random.randn(120)

@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")

# A 1-dimensional array is accepted and treated the same as a row vector
def test_one_dimensional_input(series):
    a = ssaBasic(series, 24)
    b = ssaBasic(series[np.newaxis, :], 24)
    assert np.allclose(a.reconstruction(3), b.reconstruction(3))

# Invalid inputs raise a ValueError with a readable message
def test_invalid_r0_raises_value_error(series):
    s = ssaBasic(series, 24)
    with pytest.raises(ValueError, match="r0 must be less than L"):
        s.reconstruction(99)
    with pytest.raises(ValueError, match="must be less than or equal to the embedding dimension"):
        s.validateNumVal(99)

# A scalar r0 is the number of eigen-triples, an array r0 contains 0-based indices (also when it has one element)
def test_r0_scalar_is_count_array_is_indices(series):
    s = ssaBasic(series, 24)
    assert np.allclose(s.reconstruction(np.array([0])), s.reconstruction(1))
    assert np.allclose(s.reconstruction([0, 1, 2]), s.reconstruction(3))
    assert not np.allclose(s.reconstruction(np.array([3])), s.reconstruction(3))
    with pytest.raises(ValueError):
        s.reconstruction(0)

# The w-correlation uses the weights w_i = min(i, L, K, N - i + 1)
def test_wcorrelation_matches_definition(series):
    s = ssaBasic(series, 24)
    G = np.zeros(s.L + 1, dtype=int)
    G[0], G[1:3], G[3] = 1, 2, 3
    C = s.wcorrelation(G, "off")

    Y = s.grouping(G, "off")
    N, Lw = s.N, s.L + 1
    K = N - Lw + 1
    w = np.array([min(i, Lw, K, N - i + 1) for i in range(1, N + 1)])
    def wcor(a, b):
        a = a - np.sum(w*a)/np.sum(w)
        b = b - np.sum(w*b)/np.sum(w)
        return np.sum(w*a*b) / np.sqrt(np.sum(w*a*a) * np.sum(w*b*b))
    expected = np.array([[wcor(Y[i], Y[j]) for j in range(3)] for i in range(3)])
    assert np.allclose(C, expected)

# For a noiseless sinusoid around a non-zero mean both in-sample and out-of-sample errors are ~0.
# Adding the mean twice in crossval_L0 used to make the in-sample error equal to the mean.
def test_crossval_L0_does_not_add_mean_twice():
    t = np.arange(120)
    x = 10 + np.sin(2*np.pi*t/12)
    s = ssaBasic(x, 24)
    best_L0, best_rmse = s.crossval_L0(2, 0.9, 5, "off")
    assert best_rmse == pytest.approx(0, abs=1e-6)

# The plotted forecast mean is the mean of the bootstrap samples
def test_fan_chart_mean(series):
    s = ssaBasic(series, 24)
    np.random.seed(1)
    xM, xCi, xSamp = s.forecast(3, 12, num_samp=50, display="on")
    line = [l for l in plt.gca().get_lines() if l.get_label() == "Forecast Mean"][0]
    assert np.allclose(line.get_ydata(), xSamp.mean(axis=0))

# The relative contribution to the variance uses the squared singular values
def test_singular_value_contribution_uses_squares(series):
    s = ssaBasic(series, 24)
    s.plotSingularValues(10, "cm")
    heights = np.array([p.get_height() for p in plt.gca().patches])
    d = np.diag(s.S)
    assert np.allclose(heights, (np.cumsum(d**2) / np.sum(d**2))[:10])

# Backtest works for any ordering of the in-sample proportions and returns the forecast of the longest out-of-sample period
@pytest.mark.parametrize("q", [[0.8, 0.9], [0.9, 0.8]])
def test_backtest(series, q):
    s = ssaBasic(series, 24)
    testRMSE, xF = s.backtest(3, np.array(q))
    assert testRMSE.shape == (2, 2)
    assert xF.shape == (24, 2)
    inX = series[:96]
    xM, _, _ = ssaBasic(inX, 24).forecast(3, 24, num_samp=None)
    assert np.allclose(xF[:, 0], xM[0, 96:])

# Plot labels describe what is plotted: the in-sample L actually used, and which eigen-triples were used
def test_crossval_plot_titles(series):
    s = ssaBasic(series, 60) # the 90% in-sample part has 108 observations, so its L is reduced to 54
    s.crossval_r0(0.9, 5, "on")
    assert plt.gca().get_title() == "Cross-validation of r with L = 54"
    assert plt.gca().get_xlabel() == "r (number of eigen-triples)"
    s.crossval_L0(3, 0.9, 5, "on")
    assert plt.gca().get_title() == "Cross-validation of L with r0 = 3"
    s.crossval_L0(np.array([0, 2]), 0.9, 5, "on")
    assert plt.gca().get_title() == "Cross-validation of L with eigen-triples [0, 2]"

import numpy as np
import pytest
from CorBM import CorBrownian


# An integer Variance-Covariance matrix must give the same distribution as the equivalent float matrix
@pytest.mark.parametrize("E", [np.array([[4, 1], [1, 3]]), np.array([[4., 1.], [1., 3.]]), np.matrix('4, 1; 1, 3')])
def test_sample_covariance_matches_input(E):
    np.random.seed(0)
    # the tolerances are more than 4 standard errors
    mu = np.array([1, 2])
    Y = CorBrownian(mu, E, 200000)
    assert Y.shape == (200000, 2)
    assert np.cov(Y.T) == pytest.approx(np.asarray(E, dtype=float), abs=0.06)
    assert Y.mean(axis=0) == pytest.approx(mu, abs=0.02)

# CorBrownian uses numpy's global random generator, so np.random.seed makes it reproducible
def test_seed_makes_samples_reproducible():
    E = np.array([[1.5, 0.8], [0.8, 2.0]])
    np.random.seed(1)
    a = CorBrownian([1, 0], E, 10)
    np.random.seed(1)
    b = CorBrownian([1, 0], E, 10)
    assert np.array_equal(a, b)

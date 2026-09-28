import numpy as np
import pytest
from bisection_alpha import Galfa, BisectionAlpha

M_Obs = np.array([1, 2, 4, 5, 6, 7])
r_Obs = np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04])
Tau = 0.0001
Precision = 1e-10

# Example from the README and the docstring
def test_readme_example_finds_the_root():
    alpha = BisectionAlpha(0.05, 0.5, M_Obs, r_Obs, 0.04, Tau, Precision, 1000)
    assert alpha == pytest.approx(0.11549789285636511, abs=1e-9)
    assert Galfa(M_Obs, r_Obs, 0.04, alpha - 1e-6, Tau) > 0 > Galfa(M_Obs, r_Obs, 0.04, alpha + 1e-6, Tau)

def test_column_vectors_give_same_result():
    alpha = BisectionAlpha(0.05, 0.5, M_Obs[:, np.newaxis], r_Obs[:, np.newaxis], 0.04, Tau, Precision, 1000)
    assert alpha == pytest.approx(0.11549789285636511, abs=1e-9)

# If the curve is already within Tau of the ufr at the lowest alpha, the lowest alpha is optimal.
# The old code converged to xEnd instead.
def test_returns_lower_bound_when_already_within_tolerance():
    assert Galfa(M_Obs, r_Obs, 0.042, 0.3, Tau) < 0
    assert BisectionAlpha(0.3, 0.5, M_Obs, r_Obs, 0.042, Tau, Precision, 1000) == 0.3

def test_raises_when_no_alpha_in_interval_meets_the_tolerance():
    with pytest.raises(ValueError, match="larger than Tau"):
        BisectionAlpha(0.05, 0.08, M_Obs, r_Obs, 0.042, Tau, Precision, 1000)

# The old code printed a message and returned None
def test_raises_when_not_converged():
    with pytest.raises(RuntimeError, match="failed to converge"):
        BisectionAlpha(0.05, 0.5, M_Obs, r_Obs, 0.042, Tau, 1e-15, 3)

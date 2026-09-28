import numpy as np
import pytest
import nelsonsiegelsvensson
from nelsonsiegelsvensson import NelsonSiegelSvensson, NelsonSiegelSvansson, NSSMinimize

TimeVec = np.array([1, 2, 5, 10, 25])
YieldVec = np.array([0.0039, 0.0061, 0.0166, 0.0258, 0.0332])

# Example from the README and main.py
def test_readme_example_fits_the_data():
    params = NSSMinimize(0.1, 0.1, 0.1, 0.1, 1, 1, TimeVec, YieldVec)
    assert params[4] > 0 and params[5] > 0
    assert np.allclose(NelsonSiegelSvensson(TimeVec, *params), YieldVec, atol=1e-6)

# At T = 0 the curve is the limit beta0 + beta1 instead of nan
def test_zero_maturity():
    params = (0.04, -0.03, -0.05, -0.01, 1.3, 5.6)
    out = NelsonSiegelSvensson(np.array([0.0, 1e-9]), *params)
    assert np.all(np.isfinite(out))
    assert out[0] == pytest.approx(params[0] + params[1])
    assert out[0] == pytest.approx(out[1])

# NSSMinimize used to return an empty list, so the caller failed later with an IndexError
def test_raises_when_optimization_fails(monkeypatch):
    class Failed:
        success = False
        message = "Maximum number of function evaluations has been exceeded."
    monkeypatch.setattr(nelsonsiegelsvensson, "minimize", lambda *args, **kwargs: Failed())
    with pytest.raises(RuntimeError, match="did not converge"):
        NSSMinimize(0.1, 0.1, 0.1, 0.1, 1, 1, TimeVec, YieldVec)

# The function was renamed to the correct spelling; the old name still works
def test_old_function_name_is_an_alias():
    assert NelsonSiegelSvansson is NelsonSiegelSvensson

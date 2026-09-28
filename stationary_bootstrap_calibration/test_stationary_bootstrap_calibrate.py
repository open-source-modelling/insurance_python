## Test calibration
import numpy as np
import pytest
from stationary_bootstrap_calibrate import OptimalLength, lam, mlag


#Test lam output type
def test_output_numpy_array():
    x = np.array([-0.2, 0.1, 0.6, 0.8, 1.1])
    out = lam(x)
    assert isinstance (out, np.ndarray), "Output is not a numpy ndarray."

# Test on interval -1 
def test_result_bellow_minue_one():
    x = np.array([-1.2])
    out = lam(x)
    assert out[0] == pytest.approx(0., 0.00001), "Output in the inteval bellow -1 is outside expectations."

# Test on interval -0.5 - -1; should be 2(1-|-0.7|)
def test_lambda_on_interval_mid_negative(): 
    x = np.array([-0.7])
    out = lam(x)
    assert out == pytest.approx(0.6, 0.00001) , "Output in the inteval bellow -0.50 and -1 is outside expectations." 

# Test on interval -0.5 - 0 
def test_lambda_on_interval_low_negative():
    x = np.array([-0.4])
    out = lam(x)
    assert out[0] == pytest.approx(1., 0.00001), "Output in the inteval between -0.5 and 0 is outside expectations."

# Test lambda on interval 0-0.5; should be 1 
def test_lambda_on_interval_low_positive():
    x = np.array([0.3])
    out = lam(x)
    assert out == np.array([1.]), "Output in the inteval bellow 0 and 0.5 is outside expectations." 

# Test on interval 0.5 - 1; should be 2(1-|0.7|) = 2*0.3 = 0.6
def test_lambda_on_interval_mid_positive():
    x = np.array([0.7])
    out = lam(x)
    assert out[0] == pytest.approx(0.6,0.00001), "Output in the inteval bellow 0.5 and 1 is outside expectations." 

# Test on interval  bigger than 1; should be 0
def test_lambda_on_interval_high_positive():
    x = np.array([2.3])
    out = lam(x)
    assert out[0] == pytest.approx(0.,0.00001), "Output in the inteval bigger than 1 is outside expectations." 

# Test on multiple outputs
def test_lambda_multiple_outputs():
    x = np.array([-0.2, 0.1, 0.6, 0.8, 1.1])
    out = lam(x)
    assert out.size == 5, "Output is of different size than input."

#Test lam output type
def test_mlag_numpy_array():
    x = np.array([1,2,3,4])
    n = 2
    assert isinstance(mlag(x,n), np.ndarray), "Output is not a numpy ndarray."

# Test mlag  size
def test_mlag_typical_input_size():
    x = np.array([1,2,3,4])
    n = 2
    assert mlag(x,n).shape == (4,2)

# Test mlag normal
def test_mlag_typical_input():
    x = np.array([1,2,3,4])
    n = 2
    out_hardcoded = np.array([[0,0], [1,0], [2,1], [3,2]])
    out = mlag(x,n)
    assert np.array_equal(out, out_hardcoded), "Typical output 1,2,3,4 is not as originaly expected."
     
# Test mlag single input
def test_mlag_single_input():
    x = np.array([1])
    n = 2
    out = mlag(x,n)
    out_hardcoded = np.array([[0,0]])
    assert np.array_equal(out, out_hardcoded)

# Test mlag single lag
def test_mlag_single_lag():
    x = np.array([1,2,3])
    n = 1
    out = mlag(x,n)
    out_hardcoded = np.array([[0.],[1.],[2.]])
    assert np.array_equal(out, out_hardcoded)

# Test OptimalLength on the example from the docstring
def test_optimal_length_docstring_example():
    data = np.array([0.4, 0.2, 0.1, 0.4, 0.3, 0.1, 0.3, 0.4, 0.2, 0.5, 0.1, 0.2])
    assert OptimalLength(data) == pytest.approx(4.0)

# The optimal block length is capped at ceil(min(3*sqrt(n), n/3))
def test_optimal_length_bounded():
    data = np.array([1, 0.2, 17, 0.4, 0.3, 2, 0.3, 12, 0.2, 11, 0.1])
    n = data.shape[0]
    out = OptimalLength(data)
    assert 0 < out <= np.ceil(min(3*np.sqrt(n), n/3))

def ar1(phi, n, seed):
    rng = np.random.default_rng(seed)
    e = rng.normal(size=n)
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = phi*x[i-1] + e[i]
    return x

# For an AR(1) process the theoretical optimal block length of Politis & White (2004) is
# (G/g(0))^(2/3) * n^(1/3) with G/g(0) = 2*phi/(1-phi^2). The average estimate should be close to it.
# The seeds are fixed so the test is deterministic. With a mhat that is off by one lag (a bug fixed in
# January 2025) the average estimate is 20-27% too low for these cases, so the tolerance catches it.
@pytest.mark.parametrize("n", [500, 1000])
def test_optimal_length_ar1_matches_theory(n):
    phi = 0.3
    theory = (2*phi/(1-phi**2))**(2/3) * n**(1/3)
    estimates = [OptimalLength(ar1(phi, n, seed)) for seed in range(40)]
    assert np.mean(estimates) == pytest.approx(theory, rel=0.12)

# Patton's rule for the lag cut-off M, written out directly: autocorrelations on the common sample, mhat is the first
# lag of the first run of kn insignificant autocorrelations (lags 1 to mmax), otherwise the largest significant lag;
# M = min(2*mhat, mmax). Only short series (n <= 25) can tell apart whether the last window (lags mmax-kn+1 to mmax)
# is checked, which the Python port used to skip.
def reference_M(x):
    n = len(x)
    kn = int(max(5, np.sqrt(np.log10(n))))
    mmax = int(np.ceil(np.sqrt(n)) + kn)
    cv = 2 * np.sqrt(np.log10(n) / n)
    rho = np.array([np.corrcoef(x[mmax:], x[mmax - k:n - k])[0, 1] for k in range(1, mmax + 1)]) # rho[k-1] is lag k
    insig = np.abs(rho) < cv
    mhat = next((m for m in range(1, mmax - kn + 2) if insig[m - 1:m - 1 + kn].all()), None)
    if mhat is None:
        sig = np.where(~insig)[0]
        mhat = sig[-1] + 1 if sig.size else None
    return 0 if mhat is None else min(2 * mhat, mmax)

def test_lag_cutoff_matches_reference_rule(monkeypatch):
    import stationary_bootstrap_calibrate as sbc
    seen = []
    def spy_lam(x): # OptimalLength calls lam(kk/M) with kk = -M..M, which reveals M
        seen.append((len(x) - 1) // 2)
        return lam(x)
    monkeypatch.setattr(sbc, "lam", spy_lam)
    rng = np.random.default_rng(0)
    for n in range(12, 26):
        for _ in range(150):
            x = rng.normal(size=n) if rng.random() < 0.5 else np.cumsum(rng.normal(size=n))
            seen.clear()
            OptimalLength(x)
            M = seen[0] if seen else 0
            assert M == reference_M(x), f"n={n}: M={M}, expected {reference_M(x)}"

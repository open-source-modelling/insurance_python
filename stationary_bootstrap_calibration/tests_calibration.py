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
def test_mlag_typical_input():
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

# Test OptimalLength
data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2])
print(OptimalLength(data).shape)

# Test OptimalLength
data = np.array([1,0.2,17,0.4,0.3,2,0.3,12,0.2,11,0.1])
print(OptimalLength(data))

data = np.array([0.4, 0.2, 0.1, 0.4, 0.3, 0.1, 0.3, 0.4, 0.2, 0.5, 0.1, 0.2])
m = OptimalLength(data)
print(m)






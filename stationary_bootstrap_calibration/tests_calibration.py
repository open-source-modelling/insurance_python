## Test calibration
import numpy as np
import pytest
from stationary_bootstrap_calibrate import OptimalLength, lam, mlag


#Test lam output type
def test_output_numpy_array():
    x = np.array([-0.2, 0.1, 0.6, 0.8, 1.1])
    out = lam(x)
    assert isinstance (out, np.ndarray), "Output is not a numpy ndarray."

# Test on interval <0
def test_result_bellow_zero():
    x = np.array([-1.2])
    out = lam(x)
    assert out == np.array([0.])


# Test lambda on interval 0-0.5; should be 1 
def test_result_low():
    x = np.array([0.5])
    out = lam(x)
    assert out == np.array([1.])

# Test on interval 0.5 - 1; should be 2(1-|0.7|) = 2*0.3 = 0.6
def test_lambda_on_interval_mid(): 
    x = np.array([0.7])
    out = lam(x)
    assert out[0] == pytest.approx(0.6,0.00001)

# Test on interval -0.5 - -1; should be 2(1-|-0.7|)
def test_lambda_on_interval_mid_negative(): 
    x = np.array([-0.7])
    out = lam(x)
    assert out == pytest.approx(0.6,0.00001)

# Test on interval >1
x = np.array([1.2])
out = lam(x)
print(out)


# Test on multiple outputs
x = np.array([-0.2, 0.1, 0.6, 0.8, 1.1])
out = lam(x)
print(out)

# Test mlag normal
x = np.array([1,2,3,4])
n = 2
print(mlag(x,n))
     
# Test mlag normal size
x = np.array([1,2,3,4])
n = 2
print(mlag(x,n).shape)

# Test mlag single input
x = np.array([1])
n = 2
print(mlag(x,n))

# Test mlag single input
x = np.array([1,2,3])
n = 1
print(mlag(x,n))

# Test mlag single input
x = np.array([1,2,3])
n = 1
print(mlag(x,n))

# Test OptimalLength
data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2])
print(OptimalLength(data).shape)

# Test OptimalLength
data = np.array([1,0.2,17,0.4,0.3,2,0.3,12,0.2,11,0.1])
print(OptimalLength(data))

data = np.array([0.4, 0.2, 0.1, 0.4, 0.3, 0.1, 0.3, 0.4, 0.2, 0.5, 0.1, 0.2])
m = OptimalLength(data)
print(m)






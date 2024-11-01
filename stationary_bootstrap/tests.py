# Collection of tests that show how Stationary boostrap works. This will be written again in pytest
import numpy as np
import pytest
from StationaryBootstrap import StationaryBootstrap


# Normal behaviour
def test_normal():
    data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
    m = 4 # Average length of the block
    sampleLength = 12 # Length of output sample
    ans = StationaryBootstrap(data, m, sampleLength)
    assert(isinstance(ans, np.ndarray))


# Is output same length as sampleLength
def test_correct_length():
    data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
    m = 4 # Average length of the block
    sampleLength = 12 # Length of output sample
    ans = StationaryBootstrap(data, m, sampleLength)
    assert(len(ans)== sampleLength)


# One element sampled always
def test_one_element_always_sampled():
    data = np.array([0.4])
    sampleLength = 4
    m = 4
    ans = StationaryBootstrap(data, m, sampleLength)
    assert(ans == np.array([[0.4], [0.4], [0.4], [0.4]]))


# Sample of length 1
def test_sample_of_length_one():
    data = np.array([0.5])
    m = 4
    sampleLength = 1
    ans = StationaryBootstrap(data, m, sampleLength)
    assert(ans == np.array([0.5]))

# Sampling empty data
#data = np.array([])
#sampleLength = 1
#ans = StationaryBootstrap(data, m, sampleLength)
#print(ans == np.array([0.5]))

# Negative sample length parameter
#data = np.array([0.5])
#sampleLength = -1
#ans = StationaryBootstrap(data, m, sampleLength)
#print(ans == np.array([0.5]))


# negative average length 
#def test_negative_average_length():
#    data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
#    m = -4 # Average length of the block
#    sampleLength = 12 # Length of output sample
#    ans = StationaryBootstrap(data, m, sampleLength)
#    print(ans)
#print("Fix this")


# Average length longer than sample 
def test_average_length_longer_than_sample():
    data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
    m = 20 # Average length of the block
    sampleLength = 12 # Length of output sample
    ans = StationaryBootstrap(data, m, sampleLength)
    assert(len(ans)== sampleLength)


# Data in columns
def test_data_passed_in_column():
    data = np.array([[0.4],[0.2],[0.1],[0.4],[0.3],[0.1],[0.3],[0.4],[0.2],[0.5],[0.1],[0.2]]) # Original time-series
    m = 4 # Average length of the block
    sampleLength = 12 # Length of output sample
    ans = StationaryBootstrap(data, m, sampleLength)
    data2 = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) 
    ans2 = StationaryBootstrap(data2, m, sampleLength)
    assert(ans.size == ans2.size)


# Negative data
def test_negative_input_data():
    data = np.array([-0.4,0.2,-0.1,0.4,-0.3,0.1,-0.3,0.4,-0.2,-0.5,0.1,-0.2]) # Original time-series
    m = 4 # Average length of the block
    sampleLength = 12 # Length of output sample
    ans = StationaryBootstrap(data, m, sampleLength)
    assert(len(ans)== sampleLength)


# Data not in numpy array
#data = [0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2] # Original time-series
#m = 4 # Average length of the block
#sampleLength = 12 # Length of output sample
#ans = StationaryBootstrap(data, m, sampleLength)
#print(ans)

# Data contains strings
def test_string_number_input_data():
    data = np.array(["-0.4","0.2","-0.1","0.4","-0.3","0.1","0.3","0.4","0.2","0.5","0.1","0.2"]) # Original time-series
    m = 4 # Average length of the block
    sampleLength = 12 # Length of output sample
    ans = StationaryBootstrap(data, m, sampleLength)
    assert(len(ans)== sampleLength)


## Test calibration

from stationary_bootstrap_calibrate import OptimalLength, lam, mlag

data = np.array([0.4, 0.2, 0.1, 0.4, 0.3, 0.1, 0.3, 0.4, 0.2, 0.5, 0.1, 0.2])

m = OptimalLength(data)
print(m)


# Test lambda on interval 0-0.5
x = np.array([0.5])
out = lam(x)
print(out)

# Test on interval 0.5-1 and >1
x = np.array([0.7])
out = lam(x)
print(out)

# Test on interval >1
x = np.array([1.2])
out = lam(x)
print(out)

# Test on interval <0
x = np.array([-1.2])
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







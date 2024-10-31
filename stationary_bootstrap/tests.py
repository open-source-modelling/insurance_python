# Collection of tests that show how Stationary boostrap works. This will be written again in pytest
import numpy as np
from StationaryBootstrap import StationaryBootstrap


# Normal behaviour
data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
m = 4 # Average length of the block
sampleLength = 12 # Length of output sample
ans = StationaryBootstrap(data, m, sampleLength)
print(ans)


# Is output same length as sampleLength
data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
m = 4 # Average length of the block
sampleLength = 12 # Length of output sample
ans = StationaryBootstrap(data, m, sampleLength)
print(len(ans)== sampleLength)


# One element sampled always
data = np.array([0.4])
sampleLength = 4
ans = StationaryBootstrap(data, m, sampleLength)
print(ans == np.array([[0.4], [0.4], [0.4], [0.4]]))


# Sample of length 1
data = np.array([0.5])
sampleLength = 1
ans = StationaryBootstrap(data, m, sampleLength)
print(ans == np.array([0.5]))

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
data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
m = -4 # Average length of the block
sampleLength = 12 # Length of output sample
ans = StationaryBootstrap(data, m, sampleLength)
print(ans)
print("Fix this")


# Average length longer than sample 
data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2]) # Original time-series
m = 20 # Average length of the block
sampleLength = 12 # Length of output sample
ans = StationaryBootstrap(data, m, sampleLength)
print(ans)


# Data in columns
data = np.array([[0.4],[0.2],[0.1],[0.4],[0.3],[0.1],[0.3],[0.4],[0.2],[0.5],[0.1],[0.2]]) # Original time-series
m = 4 # Average length of the block
sampleLength = 12 # Length of output sample
ans = StationaryBootstrap(data, m, sampleLength)
print(ans)


# Negative data
data = np.array([-0.4,0.2,-0.1,0.4,-0.3,0.1,-0.3,0.4,-0.2,-0.5,0.1,-0.2]) # Original time-series
m = 4 # Average length of the block
sampleLength = 12 # Length of output sample
ans = StationaryBootstrap(data, m, sampleLength)
print(ans)


# Data not in numpy array
#data = [0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2] # Original time-series
#m = 4 # Average length of the block
#sampleLength = 12 # Length of output sample
#ans = StationaryBootstrap(data, m, sampleLength)
#print(ans)

# Data contains strings
data = np.array(["-0.4","0.2","-0.1","0.4","-0.3","0.1","0.3","0.4","0.2","0.5","0.1","0.2"]) # Original time-series
m = 4 # Average length of the block
sampleLength = 12 # Length of output sample
ans = StationaryBootstrap(data, m, sampleLength)
print(ans)


## Test calibration

from stationary_bootstrap_calibrate import OptimalLength, lam, mlag

data = np.array([0.4, 0.2, 0.1, 0.4, 0.3, 0.1, 0.3, 0.4, 0.2, 0.5, 0.1, 0.2])

m = OptimalLength(data)
print(m)

data = np.array([1.1,3,5.2,3,1,3.1,5,3,1.2,3,5,3.1,1,3,5,3,5,3,1,3,5,3,1,3,5,3,1,3,5,3,1])

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







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



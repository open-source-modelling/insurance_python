# Nelson-Siegel-Svannson algorithm
</br>

## Problem

## Solution

### Parameters

### Desired output

## Getting started

```bash
from nelsonsiegelsvensson import *
import numpy as np

TimeVec = np.array([1,2,5,10,25])
YieldVec = np.array([0.0039, 0.0061, 0.0166, 0.0258, 0.0332])
beta0   = 0.1 # initial guess
beta1   = 0.1 # initial guess
beta2   = 0.1 # initial guess
beta3   = 0.1 # initial guess
lambda0 = 1 # initial guess
lambda1 = 1 # initial guess

TimeResultVec = np.array([1,2,5,10,25,30,31]) # Maturities for yields that we are interested in

## Implementation
OptiParam = NSSMinimize(beta0, beta1, beta2, beta3, lambda0, lambda1, TimeVec, YieldVec) # The Nelder-Mead simplex algorithem is used to find the parameters that result in a curve with the minimum residuals compared to the market data.

# Print the yield curve with optimal parameter to compare with the data provided
print(NelsonSiegelSvansson(TimeResultVec, OptiParam[0], OptiParam[1], OptiParam[2], OptiParam[3], OptiParam[4], OptiParam[5]))
```


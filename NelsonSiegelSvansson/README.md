# Nelson-Siegel-Svannson algorithm
</br>

Popular algorithm for fitting a yield curve to obseved data. 

## Problem
Data on bond yields is usualy avalible only for a small set of maturities, while the user is normaly interested in a wider range of yields. 
  
## Solution
A popular solution is to try to describe the yields as curve with the maturity on the x-axis and the yield on the y-axis. This curve is selected in such a way as to fit the yields, that can be observed on the market. The Nelson-Siegel-Svannson model is a curve form that is flexible enough to approximate most real world scenairos.

<FORMULA FOR NSS HER>
  

### Parameters

   - Observed yield rates (YieldVec)
   - Maturity of each observed yield (TimeVec)
   - Initial guess for parameters (beta0, beta1, beta2,beta3, labda0 , and lambda1) 
   - Target maturities (TimeResultVec)

### Desired output
   - Calculated yield rates for maturities of interest (TimeResultVec)

## Getting started
The user is interested in the projected yield for government bonds with a maturity in 1,2,5,10,25,30, and 31 years. They have data on government bonds maturing in 
1,2,5,10, and 25 years. The calculated yield for those bonds are 0.39%, 0.61%, 1.66%, 2.58%, and 3.32%. 

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

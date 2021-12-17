This repository has an implementation for a simple bisection method that finds the optimal parameter alpha for the Smith & Wilson algorithm offten used in insurance to interpolate/extrapolate rates or yields.  

## Problem
Before using the Smith & Wilson algorithm, the user needs to provide the convergence speed parameter alpha. This parameter needs to be calibrated primarily so that that the extrapolated result matches the desired long term behaviour.

## Solution
By transforming the minimization problem at the point of convergence into a problem of finding a root of the shifted function g(alpha) - Tau, this repository implements a simple bisection algorithm to find the optimal alpha.

### Input
 - The minimum allowed value of the convergence speed parameter alpha.
 - The maximum allowed value of the convergence speed parameter alpha.
 - Maturities of bonds, observed on the market and provided as output
 - Zero-coupon rates, for which the user wishes to calibrate the algorithm. Each rate belongs to an observable zero coupon bond with a known maturity. 
 - The ultimate forward rate towards which the user wishes the resulting curve to converge.
 - Allowed difference between the given ultimate forward rate and the resulting curve. 
 - The numeric precision of the calculation. Higher the precision, more aqurate the estimation of the root
 - The maximum number of iterations allowed. This is to prevent an infinite loop in case the method does not converge to a solution         
 
### Output
  - Optimal value of the parameter alpha if the roposedd method converged
 
 Note that to be consistent with EIOPA's recomandations, the lower bound of the interval should be set to 0.05. 
 
## Getting started
```python
import numpy as np
from SWCalibrate import SWCalibrate as SWCalibrate
from SWExtrapolate import SWExtrapolate as SWExtrapolate
from bisection_alpha import Galfa as Galfa
from bisection_alpha import BisectionAlpha as BisectionAlpha

M_Obs = np.transpose(np.array([1, 2, 4, 5, 6, 7]))
r_Obs =  np.transpose(np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04]))
ufr = 0.04
Precision = 0.0000000001
Tau = 0.0001 # 1 basis point

print("Example in the documentation for Galfa: "+ str(Galfa(M_Obs, r_Obs, ufr, 0.15, Tau)))
print("Example in the documentation for BisectionAlpha: "+ str(BisectionAlpha(0.05, 0.5, M_Obs, r_Obs, ufr, Tau, Precision, 1000)))
```

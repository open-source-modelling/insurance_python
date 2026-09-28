<h1 align="center" style="border-botom: none">
  <b>
    🐍 Nelson-Siegel-Svensson algorithm 🐍     
  </b>
</h1>

</br>

Popular algorithm for fitting a yield curve to observed data. 

## Problem
Data on bond yields is usually available only for a small set of maturities, while the user is normally interested in a wider range of yields. 
  
## Solution
A popular solution is to use an algorithm to find a function that fits the existing datapoints. This way, the function can be used to interpolate/extrapolate any other point. The Nelson-Siegel-Svensson model is a curve-fitting-algorithm that is flexible enough to approximate most real-world applications.

The Nelson-Siegel-Svensson is an extension of the 4-parameter Nelson-Siegel method to 6 parameters. Svensson introduced two extra parameters to better fit the variety of shapes of either the instantaneous forward rate or yield curves that are observed in practice. 

Advantages:
-  It produces a smooth and well-behaved forward rate curve.
-  The intuitive explanation of the parameters. `beta0` is the long-term interest rate and `beta0+beta1` is the instantaneous short-term rate. 

To find the optimal value of the parameters, the Nelder-Mead simplex algorithm is used (Already implemented in the scipy package). The link to the optimization algorithm is Gao, F. and Han, L. Implementing the Nelder-Mead simplex algorithm with adaptive parameters. 2012. Computational Optimization and Applications. 51:1, pp. 259-277.

The formula for the yield curve (Value of the yield for a maturity at time 't') is given by the formula:

$$
r(t) = \beta_0 + \beta_1 \frac{1-e^{-t/\lambda_0}}{t/\lambda_0} + \beta_2 \left(\frac{1-e^{-t/\lambda_0}}{t/\lambda_0} - e^{-t/\lambda_0}\right) + \beta_3 \left(\frac{1-e^{-t/\lambda_1}}{t/\lambda_1} - e^{-t/\lambda_1}\right)
$$

The parameters are named as in the code: `beta0` to `beta3` and the shape parameters `lambda0` and `lambda1`, which must be positive. At $t = 0$ the formula is taken as its limit, $r(0) = eta_0 + eta_1$.

### Parameters

   - Observed yield rates `YieldVec`.
   - Maturity of each observed yield `TimeVec`.
   - Initial guess for parameters `beta0`, `beta1`, `beta2`, `beta3`, `lambda0`, and `lambda1`.
   - Target maturities `TimeResultVec`.

### Desired output

   - Calculated yield rates for maturities of interest `TimeResultVec`.

## Getting started

The user is interested in the projected yield for government bonds with a maturity in 1, 2, 5, 10, 25, 30, and 31 years. They have data on government bonds maturing in 
1, 2, 5, 10, and 25 years. The calculated yield for those bonds is 0.39%, 0.61%, 1.66%, 2.58%, and 3.32%. 

  ```python
from nelsonsiegelsvensson import *
import numpy as np

TimeVec = np.array([1, 2, 5, 10, 25])
YieldVec = np.array([0.0039, 0.0061, 0.0166, 0.0258, 0.0332])
beta0   = 0.1 # initial guess
beta1   = 0.1 # initial guess
beta2   = 0.1 # initial guess
beta3   = 0.1 # initial guess
lambda0 = 1 # initial guess
lambda1 = 1 # initial guess

TimeResultVec = np.array([1, 2, 5, 10, 25, 30, 31]) # Maturities for yields that we are interested in

## Implementation
OptiParam = NSSMinimize(beta0, beta1, beta2, beta3, lambda0, lambda1, TimeVec, YieldVec) # The Nelder-Mead simplex algorithm is used to find the parameters that result in a curve with the minimum residuals compared to the market data.

# Print the yield curve with optimal parameter to compare with the data provided
print(NelsonSiegelSvensson(TimeResultVec, OptiParam[0], OptiParam[1], OptiParam[2], OptiParam[3], OptiParam[4], OptiParam[5]))
```

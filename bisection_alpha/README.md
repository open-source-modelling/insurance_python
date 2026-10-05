<h1 align="center" style="border-botom: none">
  <b>
    🐍 Bisection method that finds the optimal parameter α for the Smith & Wilson algorithm 🐍     
  </b>
</h1>

This repository has an implementation for a simple bisection method that finds the optimal parameter α for the Smith & Wilson algorithm often used in insurance to interpolate/extrapolate rates or yields.

The implementation is based on [Technical documentation of the Methodology to derive EIOPA's risk-free interest rate term structure](https://www.eiopa.europa.eu/document/download/df541a50-a9e7-458b-86ae-6ad16c2d6a29_en?filename=16-09-2022%20Technical%20documentation) and [Wiki on Bisection method](https://en.wikipedia.org/wiki/Bisection_method)

## Problem
Before using the Smith & Wilson algorithm, the user needs to provide the convergence speed parameter α. This parameter needs to be calibrated primarily so that the extrapolated result matches the desired long-term behaviour.

## Solution
By transforming the minimization problem at the point of convergence into a problem of finding a root of the shifted function g(α) - τ, this repository implements a simple bisection algorithm to find the optimal α.

### Input
 - The minimum allowed value of the convergence speed parameter α.
 - The maximum allowed value of the convergence speed parameter α.
 - Maturities of bonds, observed on the market and provided as input.
 - Zero-coupon rates, for which the user wishes to calibrate the algorithm. Each rate belongs to an observable zero-coupon bond with a known maturity. 
 - The ultimate forward rate towards which the user wishes the resulting curve to converge.
 - Allowed difference τ between the forward rate of the resulting curve at the convergence point and the ultimate forward rate. EIOPA uses 1 basis point (0.0001).
 - The numeric precision of the calculation. The higher the precision, the more accurate the estimate of the root.
 - The maximum number of iterations allowed. This is to prevent an infinite loop in case the method does not converge to a solution.        
 
### Output
  - Optimal value of the parameter α: the lowest α in the interval for which the forward rate at the convergence point is within τ of the ultimate forward rate. This is how EIOPA chooses α (paragraphs 123 and 161 of the technical documentation). If the lower bound of the interval already meets the tolerance, the lower bound is returned.
  - If no α in the interval meets the tolerance, a `ValueError` is raised. If the bisection does not converge within the maximum number of iterations, a `RuntimeError` is raised.
 
 Note that to be consistent with EIOPA's recommendations, the lower bound of the interval should be set to 0.05. 
 
## Getting started
```python
import numpy as np
from SWCalibrate import SWCalibrate as SWCalibrate
from SWExtrapolate import SWExtrapolate as SWExtrapolate
from bisection_alpha import Galfa as Galfa
from bisection_alpha import BisectionAlpha as BisectionAlpha

# Maturities of bonds observed on the market
M_Obs = np.transpose(np.array([1, 2, 4, 5, 6, 7]))

# Yields observed on the market
r_Obs = np.transpose(np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04]))

# Ultimate forward rate
ufr = 0.04

# Numeric precision of the optimisation
Precision = 0.0000000001

# Tolerance: the largest allowed gap between the forward rate and the ufr at the convergence point
Tau = 0.0001 # 1 basis point

# Gap at the convergence point minus Tau, for alpha = 0.15. A negative value means that alpha = 0.15 meets the tolerance
print("Galfa for alpha = 0.15: " + str(Galfa(M_Obs, r_Obs, ufr, 0.15, Tau)))

# The lowest alpha in the interval [0.05, 0.5] that meets the tolerance
print("Optimal alpha: " + str(BisectionAlpha(0.05, 0.5, M_Obs, r_Obs, ufr, Tau, Precision, 1000)))
```

The output is (the last digits can differ slightly between computers):

```
Galfa for alpha = 0.15: -8.544212205612415e-05
Optimal alpha: 0.11549789285636511
```

### What the results mean

`Galfa` is the shifted function g(α) - τ from the Solution section. g(α) is the convergence gap from paragraph 160 of the technical documentation: the distance at the convergence point between the forward rate of the extrapolated curve and the ultimate forward rate, both continuously compounded. The convergence point is max(LLP + 40, 60) years, where LLP is the last liquid point (the longest observed maturity). In this example it is max(7 + 40, 60) = 60 years.
 - A negative value means that α meets the tolerance; a positive value means that it does not.
 - For α = 0.15 the result is -0.0000854, so the gap is 0.0001 - 0.0000854 = 0.0000146. The forward rate at 60 years is 0.15 basis points from the ultimate forward rate, well within the tolerance of 1 basis point.

`BisectionAlpha` returns the optimal α, the lowest α in the interval [0.05, 0.5] that meets the tolerance: 0.1155. At this α the gap is exactly τ = 1 basis point, so `Galfa` is 0 there. The gap gets smaller as α increases, so every α from 0.1155 upwards meets the tolerance and every smaller α does not. This is why `Galfa` is negative for α = 0.15.

| α | Gap at 60 years | `Galfa` (gap - τ) | Meets the 1 bp tolerance? |
|---|---|---|---|
| 0.05 | 61.7 bp | +0.0061 | No |
| 0.10 | 2.4 bp | +0.00014 | No |
| 0.1155 | 1.0 bp | 0 | Yes: the optimal α |
| 0.15 | 0.15 bp | -0.0000854 | Yes |

Note that this implementation uses functions `SWCalibrate` and `SWExtrapolate` from the [Smith & Wilson implementation](https://github.com/open-source-modelling/insurance_python/tree/main/smith_wilson). They are duplicated to this repository for completeness. If there are any inconsistencies or suggestions, raise an issue or contact us directly.


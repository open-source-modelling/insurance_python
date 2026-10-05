<h1 align="center" style="border-botom: none">
  <b>
    🐍 Automatic calibration of the stationary bootstrap algorithm 🐍     
  </b>
</h1>

</br>

## Problem

Implementation of a stationary bootstrap method for weakly dependent stationary data requires the selection of the average block length as input. This can be time-consuming and introduce a degree of subjectivity into the implementation.

## Solution

The proposed methodology automatically estimates the optimal block size. As mentioned in the original paper, the methodology is based on the notion of spectral estimation via the flat-top lag-windows of Politis and Romano (1995). The proposed solution is described in the paper [Politis and White (2004)](http://public.econ.duke.edu/~ap172/Politis_White_2004.pdf) 

### Input
- The time-series for which the calibration is necessary `data`. It needs at least 12 elements; shorter series raise a `ValueError`.

### Output
- The optimal average block length. It is a positive real number of at most ⌈min(3√n, n/3)⌉, where n is the length of the series, and does not need to be an integer. For weakly dependent data it can be below 1; the stationary bootstrap treats such values like 1, which means a new block at every step (the ordinary bootstrap).

## Getting started
Given a time series with values 0.4, 0.2, 0.1, 0.4, 0.3, 0.1, 0.3, 0.4, 0.2, 0.5, 0.1, and 0.2 the user desires to use the stationary bootstrap algorithm for resampling. The objective is to automatically retrieve the "optimal" value of the parameter needed for stationary bootstrap algorithm. 

```python

import numpy as np

from stationary_bootstrap_calibrate import OptimalLength

data = np.array([0.4, 0.2, 0.1, 0.4, 0.3, 0.1, 0.3, 0.4, 0.2, 0.5, 0.1, 0.2])

m = OptimalLength(data)
# Out[0]:  4.0
```

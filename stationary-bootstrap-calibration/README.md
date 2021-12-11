# Automatic calibration of the stationary bootstrap algorithm
</br>

## Problem




## Solution

Proposed solution in the paper by [Polis and White](http://public.econ.duke.edu/~ap172/Politis_White_2004.pdf) 




### Input
- 

### Output
- 

## Getting started


```bash

import numpy as np

from stationary_bootstrap_calibrate import OptimalLength

data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2])

m = OptimalLength(data)

```

Calculate the optimal parameter for stationary bootstrap algorithm based on based on the 2004 paper by Politis &amp; White.

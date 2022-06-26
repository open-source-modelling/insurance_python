# Vasicek One-Factor


## Problem

## Solution

### Input

### Output


## Getting started
```python
import numpy as np
import pandas as pd
from typing import Any
from Vasicek_one_factor import generate_weiner_process, simulate_Vasicek_One_Factor

x0 = 1 # Starting point of the Brownian motion.
r0 = 0.1 # The starting interest rate
a = 1.0 # speed of reversion parameter
b = 0.1 # long term mean interest rate level 
sigma = 0.2 # instantaneous volatility
T = 52 # end modelling time
dt = 0.1 # increments of time

print(simulate_Vasicek_One_Factor(x0,r0, a, b, sigma, T, dt))
```

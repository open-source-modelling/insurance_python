# Vasicek One-Factor
Vasicek one factor model for simulating the evolution of a credit instrument such as a government bond.

## Problem
When trying to simulate the credit market, there is a rich body of developed models. The choice of the model and its limitations are a key decision. 

## Solution
One of the simplest short rate models, the [Vasicek one factor model](https://en.wikipedia.org/wiki/Vasicek_model) assumes that the credit market can be described by a simple mean reverting stochastic process with one source of uncertainty comming from a [Brownian motion](https://en.wikipedia.org/wiki/Brownian_motion). 
### Input

### Output

## Getting started
```python
import numpy as np
import pandas as pd
from typing import Any
from Vasicek_one_factor import generate_weiner_process, simulate_Vasicek_One_Factor

r0 = 0.1 # The starting interest rate
a = 1.0 # speed of reversion parameter
b = 0.1 # long term mean interest rate level 
sigma = 0.2 # instantaneous volatility
T = 52 # end modelling time
dt = 0.1 # increments of time

print(simulate_Vasicek_One_Factor(r0, a, b, sigma, T, dt))
```

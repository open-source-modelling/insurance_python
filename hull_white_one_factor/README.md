<h1 align="center" style="border-botom: none">
  <b>
    🐍 Hull White One-Factor model 🐍     
  </b>
</h1>


## Problem
Modelling nterest rate evolution is common task in financial modelling. Some common use cases are derivative valuation and risk management. This is usualy done using different time structure models that describe the evolution of the future interest rates (The modelling can describe the evolution of different quantities. mainly the choice is between future rates and short rates. ).

## Solution
A popular choice of model in practice is the Hull-White model. This is an extension of the Vasicek model, that is able to completely replicate the initial term structure. This allow to construct no-arbitrage curves using current market structure of interest rates. This is acchived by allowing the reversion-level parameter theta which is constant in the classical Vasicek model to vary in time with the observable future rates. The one factor version presented in this repository models the short rate using the dynamics described in the [Wiki](https://en.wikipedia.org/wiki/Hull%E2%80%93White_model)

### Input
The inputs to the Hull-White model are the following:
 - `r0`    = float, starting interest rate of the Hull White process 
 - `a` = float, speed of reversion parameter that is related to the velocity at which such trajectories will regroup around the forward rate theta
 - `sigma` = float, instantaneous volatility measures instant by instant the amplitude of randomness entering the system
 - `t`   = array of floats representing times at which the output is generated. 
 - `f`     = array of floats, representing the instantaneous forward rates at times from input t.

### Output
 - interest_rate_simulation = N x 2 pandas DataFrame where index is modeling time and values are a realisation of the spot rate increments

## Getting started

```python
import numpy as np
import pandas as pd
from Hull_White_one_factor import simulate_Hull_White_One_Factor

time = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
forwards = np.array([0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03])
sigma = 0.2
alpha = 0.04
r0 = 0.02

out = simulate_Hull_White_One_Factor(r0, alpha, sigma, time, forwards)

index_evolution = np.insert(np.exp(np.cumsum(out["Interest Rate"].values)),0,1)
print(index_evolution)
```

<h1 align="center" style="border-botom: none">
  <b>
    🐍 Hull White One-Factor model 🐍     
  </b>
</h1>


## Problem
Modelling interest rate evolution simulation is common task in financial modelling. Some common use cases are derivative valuation and risk management. This is usually done using different time structure models that describe the evolution of the future interest rates (The modelling can describe the evolution of different quantities. mainly the choice is between future rates and short rates.).

## Solution
A popular choice of model in practice is the Hull-White model. This is an extension of the Vasicek model, that can completely replicate the initial term structure. This allows to construct no-arbitrage curves using current market structure of interest rates. This is achieved by allowing the reversion-level parameter theta which is constant in the classical Vasicek model to vary in time with the observable future rates. The one factor version presented in this repository models the short rate using the dynamics described in the [Wiki](https://en.wikipedia.org/wiki/Hull%E2%80%93White_model)

### Input
The inputs to the Hull-White model are the following:
 - `a` (float): speed of reversion parameter that is related to the velocity at which such trajectories will regroup around the forward rate theta.
 - `sigma` (float): instantaneous volatility of the short rate. It is an absolute volatility in units of the rate: sigma = 0.01 means changes of about 1 percentage point per year.
 - `t` (array of floats): times at which the output is generated, in years from today. They must be non-negative and increasing; with t[0] = 0 the first value is today's short rate.
 - `f` (array of floats): today's instantaneous forward rates f(0,t) for the times in t.

Today's short rate is not an input. In the Hull-White model it equals the first instantaneous forward rate f(0,0); any other starting value would make the model miss the initial term structure.

### Output
 -  N x 1 Pandas DataFrame where index is modelling time and values are a realisation of the short rate.

## Getting started

```python
import numpy as np
import pandas as pd
from simulate_Hull_White_One_Factor import simulate_Hull_White_One_Factor

time = np.arange(0, 11)       # today and the next 10 years
forwards = np.full(11, 0.03)  # flat forward curve of 3%, so today's short rate is 3%
sigma = 0.01 # absolute volatility of the short rate, about 1 percentage point per year
a = 0.04     # speed of mean reversion

out = simulate_Hull_White_One_Factor(a, sigma, time, forwards)

# Value of a bank account that starts at 1 and earns the simulated short rate (the rate at the start of each year)
index_evolution = np.insert(np.exp(np.cumsum(out["Interest Rate"].values[:-1] * np.diff(time))), 0, 1)
print(index_evolution)
```

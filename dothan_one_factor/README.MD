
<h1 align="center" style="border-botom: none">
  <b>
    🐍 Dothan One-Factor model 🐍     
  </b>
</h1>

The Dothan one factor model is a simple model for simulating the evolution of short rates. The model assumes that the short rate process evolves as adriftless geometric Brownian motion. 

## Problem

When trying to simulate interest rates, there is a variety of models. The choice of the model and its limitations are a key factor in deciding which model to implement. A good practice is to start with simpler models. The Dothan model is one such model.

## Solution

One of the simplest models, the [Dothan one factor model](https://quant.stackexchange.com/questions/16017/for-the-dothan-model-eqbt-infty) assumes that the short rate can be described by a simple stochastic process with one source of uncertainty coming from a [Brownian motion](https://en.wikipedia.org/wiki/Brownian_motion). 

The stochastic differential equation (SDE) of the Dothan model is shown on the Wiki page https://en.wikipedia.org/wiki/Geometric_Brownian_motion but without drift#.

### Input

  - `r0` (float): starting interest rate of the Vasicek process.
  - `a` (float): market price of risk.
  - `sigma` (float): instantaneous volatility measures instant by instant the amplitude of randomness entering the system.
  - `T` (integer): end modelling time. From 0 to T the time series runs.
  - `dt` (float): increment of time that the process runs on. Ex. dt = 0.1 then the time series is 0, 0.1, 0.2,...

### Output

 - N x 2 Pandas DataFrame with a sample path as values and modelling time as index.

## Getting started

```python
import numpy as np
import pandas as pd
from Dothan_one_factor import simulate_Dothan_One_Factor

r0 = 0.1 # The starting interest rate
a = 1.0 # market price of risk
sigma = 0.2 # instantaneous volatility
T = 52 # end modelling time
dt = 0.1 # increments of time

print(simulate_Dothan_One_Factor(r0, a, sigma, T, dt))
```


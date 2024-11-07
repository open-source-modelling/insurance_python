<h1 align="center" style="border-botom: none">
  <b>
    🐍 Black-Sholes model for simulating the price of a stock🐍     
  </b>
</h1>

Black Sholes model is one of oldest models for simulating the stock market.

## Problem

Modelling the stock market is a well-researched field. There are numerous models each with their advantages and drawbacks.

## Solution

One of the oldest and simplest models developed is the [Black-Sholes-Merton](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model) model which assumes that the asset prices can be described by the [Black-Sholes equation](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_equation). This implementation simulates the price of a stock in time.

### Input

Black Sholes simulation:
 - `S0`    ... integer, specifying the initial value of the underlying asset.
 - `mu`    ... float, specifying the drift rate of the underlying asset.
 - `sigma` ... float, standard deviation of the underlying asset's return.
 - `T`     ... integer, specifying the maximum modelling time. ex. if T = 2 then modelling time will run from 0 to 2.
 - `dt`    ... float, specifying the length of each subinterval. ex. dt=10, then there will be 10 intervals of length 0.1 between two integers of modelling time.

### Output

Return:
 - `stock_price_simulation` ... N x 2 pandas DataFrame where index is modelling time and values are a realisation of the underlying’s price.

## Getting started

Model the price of a stock which is worth today 100. The market has a future annualized risk-free rate of 5% and an annualized volatility of 30%. The user is interested in a price projection for the next 10 years in increments of 6 months (0.5 years)

``` python
import numpy as np
import pandas as pd
from simulate_black_scholes import simulate_black_scholes

# Example usage
S0 = 100       # Initial stock price
mu = 0.05      # Expected return
sigma = 0.3    # Volatility
T = 10         # 10 years
dt = 0.5       # 6-month intervals

print(simulate_black_scholes(S0=S0, mu=mu, sigma=sigma, T=T, dt=dt))
        Simulation
  0.0   100.000000
  0.5   102.844245
  1.0   110.906953
  1.5   144.208580
  2.0   200.774653
  2.5   209.315112
  3.0   151.210005
  3.5    96.068103
  4.0    82.690847
  4.5    86.983517
  5.0   102.113069
  5.5   119.007173
  6.0   171.645169
  6.5   202.591723
  7.0   321.676284
  7.5   401.060230
  8.0   364.666643
  8.5   514.189187
  9.0   364.648269
  9.5   499.020044
  10.0  496.552723
```
## Risk neutral pricing
When an ESG simulation output is presented, a standard test is applied to confirm that the scenarios are risk neutral. Black Sholes can be one such model. This test relies on the fact that in a risk-neutral framework, there is an explicit relationship between the price of a fixed income financial instrument and the expected discounted cash flows. 

Below is the Martingale test for the hypothetical example from above. To pass the test, the expected discounted cash flows should equal the initial stock price of 100.

``` python
import numpy as np
import pandas as pd
from simulate_black_scholes import simulate_black_scholes

# Risk neutral pricing test
S0 = 100       # Initial stock price
mu = 0.05      # Expected return
sigma = 0.3    # Volatility
T = 10         # 10 years
dt = 0.5       # 6-month intervals
bank_end = np.exp(T*mu) # return of the risk-free asset

nIter = 50000
result = np.zeros(nIter)

for iter in range(1,nIter):
    out = simulate_black_scholes(S0, mu, sigma, T, dt)
    martingale = out.iloc[-1,:].values[0] / bank_end
    result[iter] = martingale

print(np.mean(result))
#   [out] = 99.8743118539787
```

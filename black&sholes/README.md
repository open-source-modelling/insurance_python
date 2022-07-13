# Black Sholes model
Simple Black-Sholes model for simulating the price of a stock.

## Problem
Modelling the stock market is a well researced field. Selecting the right model with its restrictions is a key decision.

## Solution
One of the oldest and simplest models developed is the [Black-Sholes-Merton](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model) model which assumes that the stock market can be described by the [Black-Sholes equation](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_equation). This implementation simulates the price of a stock in time.

### Input
Black Sholes simulation:
 - x0    ... float, the starting value of the Brownian motion
 - S0    ... integer, specifying the initial value of the underlying asset
 - mu    ... float, specifying the drift rate of the underlying asset 
 - sigma ... float, standard deviation of the underlying asset's return
 - T     ... integer, specifying the maximum modeling time. ex. if T = 2 then modelling time will run from 0 to 2
 - dt    ... float, specifying the length of each subinterval. ex. dt=10, then there will be 10 intervals of length 0.1 between two integers of modeling time 
  - rho  ... float, specifying the correlation coefficient of the Brownian motion. ex. rho = 0.4 means that two Brownian motions have a correlation coefficient of 0.4 

### Output
Return:
 - stock_price_simulation ... N x 2 pandas DataFrame where index is modeling time and values are a realisation of the uderlying's price


## Getting started
Model the price of a stock whitch is worth today 100. The market has a future annualized risk free rate of 5% and an annualized volatility of 30%. The user is interested in a price projection for the next 10 years in increments of 6 months (0.5 years)

``` python
import pandas as pd
import numpy as np
from typing import Any
from Black_Sholes import generate_weiner_process, simulate_Black_Scholes
print(simulate_Black_Scholes(0, 100, 0.05, 0.3, 10,0.5, None))
    #   [out] = Time    Stock Price                
    #       0.000000    100.000000
    #       0.526316    118.331770
    #       1.052632    124.917098
    #       1.578947    111.144199
    #       2.105263     96.456035
    #       2.631579    114.070441
    #       3.157895    104.079196
    #       3.684211    103.188868
    #       4.210526     94.063995
    #       4.736842     89.687491
    #       5.263158     85.532788
    #       5.789474     85.782690
    #       6.315789     87.584947
    #       6.842105     93.350451
    #       7.368421     95.605490
    #       7.894737     83.973386
    #       8.421053     67.723336
    #       8.947368     53.338441
    #       9.473684     61.878926
    #       10.000000    74.848335
```

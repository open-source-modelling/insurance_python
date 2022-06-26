# Black Sholes model

## Problem


## Solution


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
print(simulate_Black_Scholes(1, 100, 0.05, 0.3, 10,0.5, None))
#   [out] = Time    Stock Price                
#           0.000000    134.985881
#           0.526316    130.306622
#           1.052632    122.687338
#           1.578947    103.717078
#           2.105263    109.418052
#           2.631579     88.875926
#           3.157895    112.805021
#           3.684211    119.405081
#           4.210526    159.967595
#           4.736842    160.401897
#           5.263158    169.804621
#           5.789474    167.541434
#           6.315789    192.277426
#           6.842105    193.039165
#           7.368421    177.318946
#           7.894737    182.171283
#           8.421053    139.995595
#           8.947368    189.266738
#           9.473684    200.767017
#           10.000000   182.350764
```
















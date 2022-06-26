import numpy as np
import pandas as pd
from typing import Any

def generate_weiner_process(x0: float= 1, T: int = 1, dt: float = 0.001, rho: float = None) -> Any:
    # GENERATE_WEINER_PROCESS calculates the sample paths of a one-dimensional Brownian motion or a two-dimensional Brownian motion with a correlation coefficient of rho.
    # The function's output are two sample paths (realisations) of such a process, recorded on increments specified by dt. 
    # W = generate_weiner_process(x0, T, dt, rho)
    #
    # Arguments:   
    #   x0   =  float, the starting value of the Brownian motion
    #   T    = integer, specifying the maximum modeling time. ex. if T = 2 then modelling time will run from 0 to 2
    #   dt   = float, specifying the length of each subinterval. ex. dt=10, then there will be 10 intervals of length 0.1 between two integers of modeling time 
    #   rho  = float, specifying the correlation coefficient of the Brownian motion. ex. rho = 0.4 means that two 
    #          Brownian procesess on the same modeling time interval have a correlation coefficient of 0.4. SOURCE
    #
    # Returns:
    #   W =  N x 1 or N x 2 ndarray, where N is the number of subintervals, and the second dimension is eiter 1 or 2 depending if the function is called 
    #        to generate a one or two dimensional Brownian motion. Each column represents a sample path of a Brownian motion starting at x0 
    #
    # Example:
    # The user wants to generate discreete sample paths of two Brownian motions with a correlation coefficient of 0.4. 
    #    The Brownian motions needs to start at 0 at time 0 and on for 3 units of time with an increment of 0.5.
    #
    #   import numpy as np
    #   from typing import Any
    #   generate_weiner_process(0, 3, 0.5, 0.4)
    #   [out] = [array([ 0.        , -0.07839855,  0.26515158,  1.15447737,  1.04653442,
    #           0.81159737]),
    #           array([ 0.        , -0.78942881, -0.84976461, -1.06830757, -1.21829101,
    #           -0.61179385])]
    #       
    # Ideas for improvement:
    # Remove x0 as a necessary argument
    # Generate increments directly
    # 
    # For more information see https://en.wikipedia.org/wiki/Brownian_motion

    N = int(T / dt) # number of subintervals of length 1/dt between 0 and max modeling time T

    if not rho: # if rho is empty, assume uncorrelated Brownian motion

        W = np.ones(N) * x0 # preallocate the output array holding the sample paths with the inital point

        for iter in range(1, N): # add a random normal increment at every step

            W[iter] = W[iter-1] + np.random.normal(scale = dt)

        return W

    if rho: # if rho is defined, that means that the output will be a 2-dimensional Brownian motion

        W_1 = np.ones(N) * x0 # preallocate the output array holding the sample paths with the inital point
        W_2 = np.ones(N) * x0 # preallocate the output array holding the sample paths with the inital point

        for iter in range(1, N): # generate two independent BMs and entangle them with the formula from SOURCE

            Z1 = np.random.normal(scale = dt)
            Z2 = np.random.normal(scale = dt)
            Z3 = rho * Z1 + np.sqrt(1 - rho**2) * Z2

            W_1[iter] = W_1[iter-1] + Z1 # Generate first BM
            W_2[iter] = W_2[iter-1] + Z3 # Generate second BM

        return [W_1, W_2]

def simulate_Black_Scholes(x0: float= 1, S0: int = 100, mu: float = 0.05, sigma: float = 0.3, T: int = 52, dt: float = 0.1, rho: float = None) -> pd.DataFrame:
    # SIMULATE_BLACK_SHOLES calculates a temporal series of stock prices using the Black Scholes log normal model and the generated Brownian motion
    # stock_price_simulation = simulate_Black_Scholes(x0, S0, mu, sigma, T, dt, rho)
    #
    # Arguments:
    #   x0   =  float, the starting value of the Brownian motion
    #   S0    = integer, specifying the initial value of the underlying asset
    #   mu    = float, specifying the drift rate of the underlying asset 
    #   sigma = float, standard deviation of the underlying asset's return
    #   T     = integer, specifying the maximum modeling time. ex. if T = 2 then modelling time will run from 0 to 2
    #   dt    = float, specifying the length of each subinterval. ex. dt=10, then there will be 10 intervals of length 0.1 between two integers of modeling time 
    #   rho   = float, specifying the correlation coefficient of the Brownian motion. ex. rho = 0.4 means that two 
    #
    # Returns:
    #   stock_price_simulation = N x 2 pandas DataFrame where index is modeling time and values are a realisation of the uderlying's price
    #
    # Example:
    #   Model the price of a stock whitch is worth today 100. The market has a future annualized risk free rate of 5% and an annualized volatility of 30%. The user is interested in a price projection for the next 10 years in increments of 6 months (0.5 years)
    #   import pandas as pd
    #   import numpy as np
    #   from typing import Any
    #   simulate_Black_Scholes(1, 100, 0.05, 0.3, 10,0.5, None)   
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
    #
    # For more information see SOURCE
    
    N = int(T / dt) # number of subintervals of length 1/dt between 0 and max modeling time T

    time, delta_t = np.linspace(0, T, num = N, retstep = True)

    stock_variation = (mu - (sigma**2/2)) * time

    weiner_process = sigma * generate_weiner_process(x0, T, dt)

    S = S0*(np.exp(stock_variation + weiner_process)) # Change in price of the stock in time

    dict = {'Time' : time, 'Stock Price' : S}

    stock_price_simulation = pd.DataFrame.from_dict(data = dict)
    stock_price_simulation.set_index('Time', inplace = True)

    return stock_price_simulation

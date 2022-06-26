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

def simulate_Vasicek_One_Factor(x0: float = 1, r0: float = 0.1, a: float = 1.0, b: float = 0.1, sigma: float = 0.2, T: int = 52, dt = 0.1) -> pd.DataFrame:
    # SIMULATE_VASICEK_ONE_FACTOR simulates a temporal series of interest rates using the One Factor Vasicek model
    # interest_rate_simulation = simulate_Vasicek_One_Factor(x0, r0, a, b, sigma, T, dt)
    #
    # Arguments:
    #   x0    = float, specifies the starting value of the Brownian motion
    #   r0    = float, starting interest rate of the vasicek process 
    #   a     = float, speed of reversion" parameter that characterizes the velocity at which such trajectories will regroup around b in time
    #   b     = float, long term mean level. All future trajectories of  r will evolve around a mean level b in the long run  
    #   sigma = float, instantaneous volatility measures instant by instant the amplitude of randomness entering the system
    #   T     = integer, end modelling time. From 0 to T the time series runs. 
    #   dt    = float, increment of time that the proces runs on. Ex. dt = 0.1 then the time series is 0, 0.1, 0.2,...
    #
    # Returns:
    #   interest_rate_simulation = N x 2 pandas DataFrame where index is modeling time and values are a realisation of the uderlying's price
    #
    # Example:
    #   Model the interest rate which is 10% today. The annualized instant volatility is 20%. The external analysis points out that the mean reversion parameter is 1 and the long term interest rate level is 10% The user is interested in an interest rate projection of the next 10 years in increments of 6 months (0.5 years)
    #
    #   import pandas as pd
    #   import numpy as np
    #
    #   simulate_Vasicek_One_Factor(1,0.1, 1.0,0.1,0.2,10,0.5)   
    #   [out] = Time    Stock Price                
    #           0.000000        0.100000
    #           0.526316        0.147296
    #           1.052632        0.156119
    #           1.578947        0.292903
    #           2.105263        0.291621
    #           2.631579        0.199320
    #           3.157895        0.149609
    #           3.684211        0.158028
    #           4.210526        0.262529
    #           4.736842        0.256974
    #           5.263158        0.161881
    #           5.789474        0.017671
    #           6.315789       -0.152944
    #           6.842105       -0.224443
    #           7.368421       -0.057381
    #           7.894737       -0.113432
    #           8.421053        0.130159
    #           8.947368        0.093998
    #           9.473684        0.245016
    #           10.000000       0.142039
    # For more information see SOURCE
    
    N = int(T / dt) # number of subintervals of length 1/dt between 0 and max modeling time T

    time, delta_t = np.linspace(0, T, num = N, retstep = True)

    weiner_process = generate_weiner_process(x0, T, dt)

    r = np.ones(N) * r0

    for t in range(1,N):
        r[t] = r[t-1] + a * (b - r[t-1]) * dt + sigma * (weiner_process[t] - weiner_process[t-1])

    dict = {'Time' : time, 'Interest Rate' : r}

    interest_rate_simulation = pd.DataFrame.from_dict(data = dict)
    interest_rate_simulation.set_index('Time', inplace = True)

    return interest_rate_simulation

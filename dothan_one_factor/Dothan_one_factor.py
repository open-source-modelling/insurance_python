import numpy as np
import pandas as pd

def simulate_Dothan_One_Factor(r0: float = 0.1, a: float = 1.0, sigma: float = 0.2, T: int = 52, dt = 0.1) -> pd.DataFrame:
    """ Simulates a temporal series of interest rates using the One Factor Dothan model
     interest_rate_simulation = simulate_Dothan_One_Factor(r0, a, lam, sigma, T, dt)
    
     Args:
       r0 (float): starting interest rate of the driftless geometric Brownian process 
       a  (float): market price of risk
       sigma (float): instantaneous volatility measures instant by instant the amplitude of randomness entering the system
       T (integer): end modelling time. From 0 to T the time series runs. 
       dt (float): increment of time that the process runs on. Ex. dt = 0.1 then the time series is 0, 0.1, 0.2,...
    
     Returns:
       N x 2 DataFrame where index is modelling time and values are a realisation of the underlying's price
    
     Example:
       Model the interest rate which is 10% today. The annualized instant volatility is 20%. The market price of risk is 1. The user is interested in an interest rate projection of the next 10 years in increments of 6 months (0.5 years)
    
       import pandas as pd
       import numpy as np
    
       simulate_Dothan_One_Factor(0.1, 1.0, 0.2, 10, 0.5)   
       [out] = Time    Stock Price                
               0.0        0.100000
               0.5        0.049780
               1.0        0.019302
               1.5        0.013762
               2.0        0.006840
               2.5        0.004245
               3.0        0.002246
               3.5        0.001363
               4.0        0.000936
               4.5        0.000650
               5.0        0.000385
               5.5        0.000249
               6.0        0.000172
               6.5        0.000122
               7.0        0.000050
               7.5        0.000034
               8.0        0.000020
               8.5        0.000013
               9.0        0.000009
               9.5        0.000005
               10.0       0.000003
    """
    N = int(T / dt) + 1 # number of end-points of subintervals of length 1/dt between 0 and max modelling time T

    time, delta_t = np.linspace(0, T, num = N, retstep = True)

    r = np.ones(N) * r0

    for t in range(1,N):
        E = r[t-1] * np.exp(-a*dt)
        SD = r[t-1]* np.exp(-a*dt)* np.sqrt(np.exp(sigma**2*dt)-1)
        r[t] = E + SD * np.random.normal(loc = 0,scale = 1)

    dict = {'Time' : time, 'Interest Rate' : r}

    interest_rate_simulation = pd.DataFrame.from_dict(data = dict)
    interest_rate_simulation.set_index('Time', inplace = True)

    return interest_rate_simulation

import numpy as np
import pandas as pd

def simulate_Vasicek_One_Factor(r0: float = 0.1, a: float = 1.0, lam: float = 0.1, sigma: float = 0.2, T: int = 52, dt = 0.1) -> pd.DataFrame:
    """ Simulates a temporal series of interest rates using the One Factor Vasicek model
     interest_rate_simulation = simulate_Vasicek_One_Factor(r0, a, lam, sigma, T, dt)
    
     Arguments:
       r0    = float, starting interest rate of the vasicek process 
       a     = float, speed of reversion parameter that characterizes the velocity at which such trajectories will regroup around lam in time
       lam   = float, long term mean level that all future trajectories will evolve around
       sigma = float, instantaneous volatility of the rate. It is an absolute volatility in units of the rate: sigma = 0.01 means changes of about 1 percentage point per year.
       T     = integer, end modelling time. From 0 to T the time series runs.
       dt    = float, increment of time that the process runs on. Ex. dt = 0.1 then the time series is 0, 0.1, 0.2,... T must be a multiple of dt.

     Returns:
       interest_rate_simulation = N x 1 Pandas DataFrame where index is modelling time and values are a realisation of the interest rate

     Example:
       Model the interest rate which is 10% today. The absolute volatility of the rate is 2 percentage points per year (sigma = 0.02). The external analysis points out that the mean reversion parameter is 1 and the long-term interest rate level is 10%. The user is interested in an interest rate projection of the next 10 years in increments of 6 months (0.5 years)

       import pandas as pd
       import numpy as np

       np.random.seed(1)
       simulate_Vasicek_One_Factor(0.1, 1.0, 0.1, 0.02, 10, 0.5)
       [out] =       Interest Rate
               Time               
               0.0        0.100000
               0.5        0.118264
               1.0        0.104199
               1.5        0.096608
               2.0        0.085878
               2.5        0.101165
               3.0        0.074829
               3.5        0.104351
               4.0        0.094080
               4.5        0.099997
               5.0        0.097194
               5.5        0.114738
               6.0        0.085775
               6.5        0.087747
               7.0        0.088250
               7.5        0.105621
               8.0        0.091042
               8.5        0.092628
               9.0        0.085658
               9.5        0.091776
               10.0       0.101565
     For more information see https://en.wikipedia.org/wiki/Vasicek_model
    """
    
    steps = int(round(T / dt)) # number of subintervals of length dt. round() because e.g. 0.3 / 0.1 = 2.9999999999999996
    if steps < 1 or not np.isclose(steps * dt, T):
        raise ValueError("T must be a positive multiple of dt")
    N = steps + 1 # number of end-points of subintervals of length dt between 0 and max modelling time T

    time, delta_t = np.linspace(0, T, num = N, retstep = True)

    r = np.ones(N) * r0

    for t in range(1,N):
        r[t] = r[t-1] * np.exp(-a*delta_t)+lam*(1-np.exp(-a*delta_t))+sigma*np.sqrt((1-np.exp(-2*a*delta_t))/(2*a))* np.random.normal(loc = 0,scale = 1)

    data = {'Time' : time, 'Interest Rate' : r}

    interest_rate_simulation = pd.DataFrame.from_dict(data = data)
    interest_rate_simulation.set_index('Time', inplace = True)

    return interest_rate_simulation

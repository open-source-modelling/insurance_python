import numpy as np
import pandas as pd

def simulate_Dothan_One_Factor(r0: float = 0.1, a: float = 1.0, sigma: float = 0.2, T: int = 52, dt = 0.1) -> pd.DataFrame:
    """ Simulates a temporal series of interest rates using the One Factor Dothan model
     interest_rate_simulation = simulate_Dothan_One_Factor(r0, a, sigma, T, dt)

     The short rate follows dr = -a * r * dt + sigma * r * dW, a geometric Brownian motion. It is simulated exactly:
     r(t + dt) = r(t) * exp((-a - sigma^2 / 2) * dt + sigma * sqrt(dt) * Z) with Z standard normal, so the rate stays positive.

     Args:
       r0 (float): starting interest rate of the geometric Brownian process
       a  (float): market price of risk. It enters the dynamics as the drift coefficient -a above.
       sigma (float): instantaneous volatility measures instant by instant the amplitude of randomness entering the system
       T (integer): end modelling time. From 0 to T the time series runs.
       dt (float): increment of time that the process runs on. Ex. dt = 0.1 then the time series is 0, 0.1, 0.2,... T must be a multiple of dt.

     Returns:
       N x 1 DataFrame where index is modelling time and values are a realisation of the interest rate
    
     Example:
       Model the interest rate which is 10% today. The annualized instant volatility is 20%. The market price of risk is 1. The user is interested in an interest rate projection of the next 10 years in increments of 6 months (0.5 years)
    
       import pandas as pd
       import numpy as np
    
       np.random.seed(1)
       simulate_Dothan_One_Factor(0.1, 1.0, 0.2, 10, 0.5)
       [out] =       Interest Rate
               Time               
               0.0        0.100000
               0.5        0.075557
               1.0        0.041611
               1.5        0.023189
               2.0        0.011964
               2.5        0.008120
               3.0        0.003521
               3.5        0.002706
               4.0        0.001459
               4.5        0.000917
               5.0        0.000531
               5.5        0.000392
               6.0        0.000176
               6.5        0.000101
               7.0        0.000057
               7.5        0.000041
               8.0        0.000021
               8.5        0.000012
               9.0        0.000006
               9.5        0.000004
               10.0       0.000003
    """
    steps = int(round(T / dt)) # number of subintervals of length dt. round() because e.g. 0.3 / 0.1 = 2.9999999999999996
    if steps < 1 or not np.isclose(steps * dt, T):
        raise ValueError("T must be a positive multiple of dt")
    N = steps + 1 # number of end-points of subintervals of length dt between 0 and max modelling time T

    time, delta_t = np.linspace(0, T, num = N, retstep = True)

    r = np.ones(N) * r0

    for t in range(1,N):
        # Exact step of the geometric Brownian motion: lognormal with mean r[t-1] * exp(-a*delta_t) and
        # variance mean^2 * (exp(sigma^2*delta_t) - 1), the same moments as before but never negative
        r[t] = r[t-1] * np.exp((-a - 0.5*sigma**2)*delta_t + sigma*np.sqrt(delta_t)*np.random.normal(loc = 0,scale = 1))

    data = {'Time' : time, 'Interest Rate' : r}

    interest_rate_simulation = pd.DataFrame.from_dict(data = data)
    interest_rate_simulation.set_index('Time', inplace = True)

    return interest_rate_simulation

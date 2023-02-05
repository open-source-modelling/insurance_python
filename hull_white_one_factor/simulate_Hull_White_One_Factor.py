import numpy as np
import pandas as pd

def simulate_Hull_White_One_Factor(r0 , a, sigma, t, f):
    # SIMULATE_HULL_WHITE_ONE_FACTOR simulates a temporal series of interest rates using the One Factor Hull-White model
    # Form of the model is dr_{t} = [theta[t] - alpha * r_{t-1}] dt + sigma * dW_{t} 
    # interest_rate_simulation = simulate_Hull_White_One_Factor(r0, alpha, sigma, t, f)
    #
    # Arguments:
    #   r0    = float, starting interest rate of the Hull White process 
    #   a = float, speed of reversion parameter that is related to the velocity at which such trajectories will regroup around the forward rate theta
    #   sigma = float, instantaneous volatility measures instant by instant the amplitude of randomness entering the system
    #   t     = array of floats representing times at which the output is generated. 
    #   f     = array of floats, representing the instantaneous forward rates at times from input t.
    #
    # Returns:
    #   interest_rate_simulation = N x 2 pandas DataFrame where index is modeling time and values are a realisation of the spot rate increments
    #
    # Example:
    #   Model the interest rate which is 2% today. The annualized instant volatility is 20%. The external analysis points out that the parameter alpha is 0.04 and the forward rates are equal to 3% in all maturities. 
    #   The user is interested in an interest rate projection of the next 10 years in annual time steps
    #
    #   import pandas as pd
    #   import numpy as np
    #
    #   simulate_Hull_White_One_Factor(0.02, 0.04, 0.2, np.array([1,2,3,4,5,6,7,8,9,10]), np.array([0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03]))   
    #   [out] = Time    Interest Rate                
    #           1 	0.020000
    #           2 	0.168049
    #           3 	0.265637
    #           4 	0.400717
    #           5 	0.053308
    #           6 	0.088566
    #           7 	0.434668
    #           8 	0.414285
    #           9 	0.186548
    #           10 	0.354167
    # For more information see https://en.wikipedia.org/wiki/Hull-White_model
        
    N = t.shape[0]
    e = np.zeros(N)
    v = np.zeros(N)
    r = np.ones(N) * r0
    alpha = f + sigma**2/(2*a**2)*(1-np.exp(-a*t))**2
    for el in range(1, N):
        deltat = t[el] - t[el-1]
        e[el] = r[el-1] * np.exp(-a*deltat) + alpha[el] - alpha[el-1] * np.exp(-a*deltat)
        v[el] = sigma**2/(2*a) * (1 - np.exp(-2*a*deltat))
        r[el] = np.random.normal(e[el], np.sqrt(v[el]))
        dict = {'Time' : t, 'Interest Rate' : r}

    interest_rate_simulation = pd.DataFrame.from_dict(data = dict)
    interest_rate_simulation.set_index('Time', inplace = True)
    return interest_rate_simulation

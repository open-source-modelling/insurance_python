import numpy as np
import pandas as pd
from typing import Any
from typing import List

class BrownianMotion():

    def __init__(self, x0: float = 0) -> None:

        self.x0 = float(x0)

    # This method generates a Weiner process (more commonly known as a Brownian Motion)
    def generate_weiner_process(self, T: int = 1, dt: float = 0.001, rho: float = None) -> Any:
        # GENERATE_WEINER_PROCESS calculates the sample paths of a one-dimensional Brownian motion or a two-dimensional Brownian motion with a correlation coefficient of rho.
        # The function's output are two sample paths (realisations) of such a process, recorded on increments specified by dt. 
        # W = generate_weiner_process(self, T, dt, rho)
        #
        # Arguments:   
        #   self = reference to the current instance of the class. This class includes the x0 parameter that specifies the starting value of the Brownian motion
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

            W = np.ones(N) * self.x0 # preallocate the output array holding the sample paths with the inital point

            for iter in range(1, N): # add a random normal increment at every step

                W[iter] = W[iter-1] + np.random.normal(scale = dt)

            return W

        if rho: # if rho is defined, that means that the output will be a 2-dimensional Brownian motion

            W_1 = np.ones(N) * self.x0 # preallocate the output array holding the sample paths with the inital point
            W_2 = np.ones(N) * self.x0 # preallocate the output array holding the sample paths with the inital point

            for iter in range(1, N): # generate two independent BMs and entangle them with the formula from SOURCE

                Z1 = np.random.normal(scale = dt)
                Z2 = np.random.normal(scale = dt)
                Z3 = rho * Z1 + np.sqrt(1 - rho**2) * Z2

                W_1[iter] = W_1[iter-1] + Z1 # Generate first BM
                W_2[iter] = W_2[iter-1] + Z3 # Generate second BM

            return [W_1, W_2]

    # This simulates a temporal series of stock prices using the Black Scholes log normal model and the generated Weiner process
    def simulate_Black_Scholes(self, S0: int = 100, mu: float = 0.05, sigma: float = 0.3, T: int = 52, dt: float = 0.1, rho: float = None) -> pd.DataFrame:
        # SIMULATE_BLACK_SHOLES calculates a temporal series of stock prices using the Black Scholes log normal model and the generated Brownian motion
        # stock_price_simulation = simulate_Black_Scholes(self, S0, mu, sigma, T, dt, rho)
        #
        # Arguments:
        #   self  = reference to the current instance of the class. This class includes the x0 parameter that specifies the starting value of the Brownian motion
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
        #   import pandas as pd
        #   import numpy as np
        #   ToFinish: simulate_Black_Scholes(100,0.05,0.3, 4,0.5,None)   
        #   [out] =  pd array    
        #
        # For more information see SOURCE
        
        N = int(T / dt)

        time, delta_t = np.linspace(0, T, num = N, retstep = True)

        stock_variation = (mu - (sigma**2/2)) * time

        weiner_process = sigma * self.generate_weiner_process(T, dt)

        S = S0*(np.exp(stock_variation + weiner_process))

        dict = {'Time' : time, 'Stock Price' : S}

        stock_price_simulation = pd.DataFrame.from_dict(data = dict)
        stock_price_simulation.set_index('Time', inplace = True)

        return stock_price_simulation

    # This simulates a temporal series of interest rates using the One Factor Vasicek mean reverting model and the generated Weiner process
    def simulate_Vasicek_One_Factor(self, r0: float = 0.1, a: float = 1.0, b: float = 0.1, sigma: float = 0.2, T: int = 52, dt = 0.1) -> pd.DataFrame:
        # SIMULATE_VASICEK_ONE_FACTOR simulates a temporal series of interest rates using the One Factor Vasicek mean reverting model and the generated Weiner process
        #
        # interest_rate_simulation = simulate_Vasicek_One_Factor(self, r0, a, b, sigma, T, dt)
        #
        # Arguments:
        #   self  = reference to the current instance of the class. This class includes the x0 parameter that specifies the starting value of the Brownian motion
        #   r0    = float, starting interest rate of the vasicek process 
        #   a     = float, speed of reversion" parameter thatcharacterizes the velocity at which such trajectories will regroup around b in time
        #   b     = float, long term mean level. All future trajectories of  r will evolve around a mean level b in the long run  
        #   sigma = float, instantaneous volatility measures instant by instant the amplitude of randomness entering the system
        #   T     = integer, end modelling time. From 0 to T the time series runs. 
        #   dt    = float, increment of time that the proces runs on. Ex. dt = 0.1 then the time series is 0, 0.1, 0.2,...
        #
        # Returns:
        #   interest_rate_simulation = pandas dataframe contains the simulated interest rate process
        #
        # Example:
        #   import pandas as pd
        #   import numpy as np
        #   <ToFinish>simulate_Vasicek_One_Factor(0.1, 1.0, 0.1,0.2,52,0.1)   
        #   [out] =  pd array    
        # For more information see SOURCE
        
        N = int(T / dt)

        time, delta_t = np.linspace(0, T, num = N, retstep = True)

        weiner_process = self.generate_weiner_process(T, dt)

        r = np.ones(N) * r0

        for t in range(1,N):
            r[t] = r[t-1] + a * (b - r[t-1]) * dt + sigma * (weiner_process[t] - weiner_process[t-1])

        dict = {'Time' : time, 'Interest Rate' : r}

        interest_rate_simulation = pd.DataFrame.from_dict(data = dict)
        interest_rate_simulation.set_index('Time', inplace = True)

        return interest_rate_simulation

    def simulate_Vasicek_Two_Factor(self, r0: List[float] = [0.1, 0.1], a: List[float] = [1.0, 1.0], b: List[float] = [0.1, 0.1], sigma: List[float] = [0.2, 0.2], rho: float = 0.5, T: int = 52, dt: float = 0.1) -> pd.DataFrame:
        # SIMULATE_VASICEK_TWO_FACTOR calculates a posible sample path of the nominal interest rate by simulating the real rate and inflation. Both are assumed to follow a mean-reverting vasicek process
        # interest_rate_simulation = simulate_Vasicek_Two_Factor(self, r0, a, b, sigma, rho, T, dt)
        #
        # Arguments:
        #   self  = reference to the current instance of the class. This class includes the x0 parameter that specifies the starting value of the Brownian motion
        #   r0    = list with 2 floats, starting interest rate of each vasicek process  
        #   a     = list with 2 floats, speed of reversion of each process that characterizes the velocity at which such trajectories will regroup around each b
        #   b     = list with 2 floats, long term mean level of each process. All future trajectories of r will evolve around a mean level b in the long run 
        #   sigma = list with 2 floats, instantaneous volatility, amplitude of randomness of each process
        #   rho  = float, specifying the correlation coefficient of the Brownian motion. ex. rho = 0.4 means that two 
        #             Brownian procesess on the same modeling time interval have a correlation coefficient of 0.4. SOURCE
        #   T    = integer specifying the maximum modeling time. ex. if T = 2 then modelling time will run from 0 to 2
        #   dt   = float specifying the length of each subinterval. ex. dt=10, then there will be 10 intervals of length 0.1 between two integers of modeling time 
        #
        # Returns:
        #   interest_rate_simulation = pandas dataframe with 3 columns. First is modelling time, second is the Nominal interest rate and the third is the Real interest rate
        #
        # Example:
        #
        #   import numpy as np       
        #   import pandas as pd
        #   from typing import any
        #   simulate_Vasicek_Two_Factor([0.1, 0.2], [1.0, 0.5],[0.1, 0.2], [0.2, 0.2], 0.5, 52,0.1)
        #   [out]  pandas dataframes with 3 columns and 520 rows
        #
        # For more information see SOURCE
        
        N = int(T / dt)  # number of subintervals of length 1/dt between 0 and max modeling time T

        time, delta_t = np.linspace(0, T, num = N, retstep = True) # time is a series from 0 to T

        weiner_process = self.generate_weiner_process(T, dt, rho) # This method generates increments from a Weiner process (more commonly known as a Brownian Motion)

        weiner_process_e = weiner_process[0]
        weiner_process_s = weiner_process[1]

        r_e, s = np.ones(N) * r0[0], np.ones(N) * r0[1]

        a_e, a_s = a[0], a[1]

        b_e, b_s = b[0], b[1]

        sigma_e, sigma_s = sigma[0], sigma[1]

        for t in range(1,N):
            r_e[t] = r_e[t-1] + a_e * (b_e - r_e[t-1]) * dt + sigma_e * (weiner_process_e[t] - weiner_process_e[t-1]) # Real interest rate
            s[t] = s[t-1] + a_s * (b_s - s[t-1]) * dt + sigma_s * (weiner_process_s[t] - weiner_process_s[t-1]) # Inflation rate

        r_s = r_e + s # Nominal interest rate as real interest rate plus inflation

        dict = {'Time' : time, 'Real Interest Rate' : r_e, 'Nominal Interest Rate' : r_s}

        interest_rate_simulation = pd.DataFrame.from_dict(data = dict)
        interest_rate_simulation.set_index('Time', inplace = True)

        return interest_rate_simulation

import numpy as np
import pandas as pd
from typing import Any
from typing import List

class BrownianMotion():

    def __init__(self, x0: float = 0) -> None:

        self.x0 = float(x0)

    def generate_weiner_process(self, T: int = 1, dt: float = 0.001, rho: float = None) -> Any:
        # GENERATE_WEINER_PROCESS calculates the sample paths of a one-dimensional Brownian motion or a two-dimensional Brownian motion with a correlation coefficient of rho.
        # The function's output are two sample paths (realisations) of such a process, recorded on increments specified by dt. 
        # W = generate_weiner_process(self, T, dt, rho)
        #
        # Arguments:   
        #   self = reference to the current instance of the class. This class includes the x0 parameter that specifies the starting value of the Brownian motion
        #   T    = integer, specifying the maximum modeling time. ex. if T = 2 then modelling time will run from 0 to 2
        #   dt   = float, specifying the length of each subinterval. ex. dt=0.1, then the time grid is 0, 0.1, 0.2, ..., T. T must be a multiple of dt 
        #   rho  = float between -1 and 1, specifying the correlation coefficient of the Brownian motion. ex. rho = 0.4 means that two
        #          Brownian procesess on the same modeling time interval have a correlation coefficient of 0.4. Without rho (None) the output is one Brownian motion
        #
        # Returns:
        #   W =  N x 1 or N x 2 ndarray, where N = T/dt + 1 is the number of points on the time grid 0, dt, ..., T, and the second dimension is eiter 1 or 2 depending if the function is called 
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

        steps = int(round(T / dt)) # number of subintervals of length dt. round() because e.g. 0.3 / 0.1 = 2.9999999999999996
        if steps < 1 or not np.isclose(steps * dt, T):
            raise ValueError("T must be a positive multiple of dt")
        if rho is not None and not -1 <= rho <= 1: # a correlation lies between -1 and 1; this also rejects NaN
            raise ValueError("rho must be a number between -1 and 1")
        N = steps + 1 # number of points on the time grid 0, dt, 2*dt, ..., T

        if rho is None: # if rho is empty, generate a one-dimensional Brownian motion

            W = np.ones(N) * self.x0 # preallocate the output array holding the sample paths with the inital point

            for iter in range(1, N): # add a random normal increment at every step. Increments of a BM have variance dt

                W[iter] = W[iter-1] + np.random.normal(scale = np.sqrt(dt))

            return W

        else: # if rho is defined (including rho = 0), the output will be a 2-dimensional Brownian motion

            W_1 = np.ones(N) * self.x0 # preallocate the output array holding the sample paths with the inital point
            W_2 = np.ones(N) * self.x0 # preallocate the output array holding the sample paths with the inital point

            for iter in range(1, N): # generate two independent BMs and entangle them with the formula

                Z1 = np.random.normal(scale = np.sqrt(dt)) # Increments of a BM have variance dt
                Z2 = np.random.normal(scale = np.sqrt(dt))
                Z3 = rho * Z1 + np.sqrt(1 - rho**2) * Z2

                W_1[iter] = W_1[iter-1] + Z1 # Generate first BM
                W_2[iter] = W_2[iter-1] + Z3 # Generate second BM

            return [W_1, W_2]

    def simulate_Vasicek_Two_Factor(self, r0: List[float] = [0.1, 0.1], a: List[float] = [1.0, 1.0], b: List[float] = [0.1, 0.1], sigma: List[float] = [0.2, 0.2], rho: float = 0.5, T: int = 52, dt: float = 0.1) -> pd.DataFrame:
        # SIMULATE_VASICEK_TWO_FACTOR calculates a posible sample path of the nominal interest rate by simulating the real rate and inflation. Both are assumed to follow a mean-reverting vasicek process,
        # simulated with its exact transition distribution
        # interest_rate_simulation = simulate_Vasicek_Two_Factor(self, r0, a, b, sigma, rho, T, dt)
        #
        # Arguments:
        #   self  = reference to the current instance of the class. This class includes the x0 parameter that specifies the starting value of the Brownian motion
        #   r0    = list with 2 floats, starting interest rate of each vasicek process  
        #   a     = list with 2 floats, speed of reversion of each process that characterizes the velocity at which such trajectories will regroup around each b
        #   b     = list with 2 floats, long term mean level of each process. All future trajectories of r will evolve around a mean level b in the long run 
        #   sigma = list with 2 floats, instantaneous volatility, amplitude of randomness of each process
        #   rho  = float between -1 and 1, specifying the correlation coefficient of the Brownian motion. ex. rho = 0.4 means that two
        #             Brownian procesess on the same modeling time interval have a correlation coefficient of 0.4.
        #   T    = integer specifying the maximum modeling time. ex. if T = 2 then modelling time will run from 0 to 2
        #   dt   = float specifying the length of each subinterval. ex. dt=0.1, then the time grid is 0, 0.1, 0.2, ..., T. T must be a multiple of dt 
        #
        # Returns:
        #   interest_rate_simulation = pandas dataframe indexed by modelling time with 2 columns: the real interest rate and the nominal interest rate (real rate + inflation)
        #
        # Example:
        #
        #   import numpy as np       
        #   import pandas as pd
        #   BrownianMotion().simulate_Vasicek_Two_Factor([0.1, 0.2], [1.0, 0.5],[0.1, 0.2], [0.2, 0.2], 0.5, 52,0.1)
        #   [out]  pandas dataframe indexed by time with 2 columns and 521 rows (times 0, 0.1, ..., 52)
        #

        for name, value in [("r0", r0), ("a", a), ("b", b), ("sigma", sigma)]: # a third element would be ignored without an error
            if np.size(value) != 2:
                raise ValueError(f"{name} must have 2 elements, one for the real rate and one for inflation")
        if rho is None or not -1 <= rho <= 1: # the two processes need a correlation between -1 and 1; this also rejects NaN
            raise ValueError("rho must be a number between -1 and 1")

        N = int(round(T / dt)) + 1  # number of points on the time grid 0, dt, 2*dt, ..., T (generate_weiner_process checks that T is a multiple of dt)

        time, delta_t = np.linspace(0, T, num = N, retstep = True) # time is a series from 0 to T with step dt

        a_e, a_s = a[0], a[1]

        b_e, b_s = b[0], b[1]

        sigma_e, sigma_s = sigma[0], sigma[1]

        # Exact discretisation of the two Vasicek processes, as in the one factor model. Over a step delta_t each process
        # decays towards its mean by exp(-a*delta_t) and receives normal noise with variance sigma^2 * (1 - exp(-2*a*delta_t)) / (2*a).
        # The noise of the two processes has covariance rho * sigma_e * sigma_s * (1 - exp(-(a_e+a_s)*delta_t)) / (a_e+a_s).
        def integral_of_exp(k): # integral of exp(-k*u) du from 0 to delta_t
            return delta_t if k == 0 else (1 - np.exp(-k * delta_t)) / k

        var_e, var_s = integral_of_exp(2 * a_e), integral_of_exp(2 * a_s) # variance of the noise of each process divided by sigma^2
        rho_noise = rho * integral_of_exp(a_e + a_s) / np.sqrt(var_e * var_s) # correlation of the noise of the two processes, equal to rho if a_e = a_s

        weiner_process = self.generate_weiner_process(T, dt, rho_noise) # This method generates increments from a Weiner process (more commonly known as a Brownian Motion)

        # The increments of the Brownian motions have variance delta_t; rescaling them gives the exact noise of each process
        noise_e = sigma_e * np.sqrt(var_e / delta_t) * np.diff(weiner_process[0])
        noise_s = sigma_s * np.sqrt(var_s / delta_t) * np.diff(weiner_process[1])

        r_e, s = np.ones(N) * r0[0], np.ones(N) * r0[1]

        decay_e, decay_s = np.exp(-a_e * delta_t), np.exp(-a_s * delta_t)

        for t in range(1,N):
            r_e[t] = r_e[t-1] * decay_e + b_e * (1 - decay_e) + noise_e[t-1] # Real interest rate
            s[t] = s[t-1] * decay_s + b_s * (1 - decay_s) + noise_s[t-1] # Inflation rate

        r_s = r_e + s # Nominal interest rate as real interest rate plus inflation

        data = {'Time' : time, 'Real Interest Rate' : r_e, 'Nominal Interest Rate' : r_s}

        interest_rate_simulation = pd.DataFrame.from_dict(data = data)
        interest_rate_simulation.set_index('Time', inplace = True)

        return interest_rate_simulation

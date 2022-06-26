import pandas as pd
import numpy as np
from scipy import integrate

from Vasicek import BrownianMotion

class Swaption(object):

    def __init__(self,
                 type: str,
                 maturity: float = 1,
                 exercise_date: float = 0.5,
                 notional: float = 10**6,
                 fixed_rate: float = 0.1,
                 floating_leg_frequency: float = 0.5,
                 payer: bool = True):

        receiver = not payer
        self._maturity = maturity
        self._exercise_date = exercise_date
        self._notional = notional
        self._fixed_rate = fixed_rate
        self._floating_leg_frequency = floating_leg_frequency
        self._is_payer = payer
        self._is_receiver = receiver
        self._type = type


class ZeroCouponBond():

    def __init__(self,
                 maturity):

        self._T = maturity

    def price_Vasicek_Two_Factor(self, r0, a, b, sigma, rho, T, dt, nScen):
        # PRICE_VASICEK_TWO_FACTOR calculates the price of a zero cupon bond of maturity T using numeric integration
        # price_Vasicek_Two_Factor(self, r0, a, b, sigma, rho, T, dt, nScen) 
        #  
        # Arguments:
        #   self  = reference to the current instance of the class.
        #   r0    = list with 2 floats, starting interest rate of each vasicek process  
        #   a     = list with 2 floats, speed of reversion of each process that characterizes the velocity at which such trajectories will regroup around each b
        #   b     = list with 2 floats, long term mean level of each process. All future trajectories of r will evolve around a mean level b in the long run 
        #   sigma = list with 2 floats, instantaneous volatility, amplitude of randomness of each process
        #   rho   = float, specifying the correlation coefficient of the Brownian motion. ex. rho = 0.4 means that two 
        #             Brownian procesess on the same modeling time interval have a correlation coefficient of 0.4. SOURCE
        #   T     = integer specifying the maximum modeling time. ex. if T = 2 then modelling time will run from 0 to 2
        #   dt    = float specifying the length of each subinterval. ex. dt=10, then there will be 10 intervals of length 0.1 between two integers of modeling time 
        #   nScen = number of numeric integrations of which the mean is the price estimation 
        #
        # Returns:
        #   ZeroCouponBond object with the added property _price containing the price of a zero cupon bond
        #
        # Example:
        # TBD

        interest_rate_simulation = pd.DataFrame()
        brownian_motion = BrownianMotion()
        for i in range(nScen):
            interest_rate_simulation = pd.concat([interest_rate_simulation,
            brownian_motion.simulate_Vasicek_Two_Factor(r0, a, b, sigma, rho, T, dt)['Real Interest Rate']],axis = 1)
        integral = interest_rate_simulation.apply(integrate.trapz)
        self._price = np.mean(np.exp(-integral))
        return self._price

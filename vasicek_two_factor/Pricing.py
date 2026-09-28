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

    def price(self, r0, a, b, sigma, rho, T, dt, nScen):
        # PRICE calculates the price of a zero cupon bond paying 1 at its maturity (self._T) using Monte Carlo simulation
        # of the nominal short rate and numeric integration: price = mean over scenarios of exp(-integral of r from 0 to maturity)
        # price(self, r0, a, b, sigma, rho, T, dt, nScen)
        #
        # Arguments:
        #   self  = reference to the current instance of the class.
        #   r0    = list with 2 floats, starting interest rate of each vasicek process
        #   a     = list with 2 floats, speed of reversion of each process that characterizes the velocity at which such trajectories will regroup around each b
        #   b     = list with 2 floats, long term mean level of each process. All future trajectories of r will evolve around a mean level b in the long run
        #   sigma = list with 2 floats, instantaneous volatility, amplitude of randomness of each process
        #   rho   = float, specifying the correlation coefficient of the Brownian motion. ex. rho = 0.4 means that two
        #             Brownian procesess on the same modeling time interval have a correlation coefficient of 0.4. SOURCE
        #   T     = float specifying the maximum modeling time of the simulation. Must be at least the maturity of the bond.
        #   dt    = float specifying the length of each subinterval. ex. dt=0.1, then the time grid is 0, 0.1, 0.2, ..., T.
        #             T and the maturity of the bond must be multiples of dt.
        #   nScen = number of simulated scenarios of which the mean is the price estimation
        #
        # Returns:
        #   The price of the zero cupon bond, which is also stored in the property _price
        #
        # Example:
        #   zero_coupon_bond = ZeroCouponBond(1)
        #   zero_coupon_bond.price([0.014, 0.06], [0.8, 1], [0.01, 0.015], [0.05, 0.04], 0.6, 1, 0.1, 1000)

        if T < self._T and not np.isclose(T, self._T):
            raise ValueError("The simulation horizon T must be at least the maturity of the bond")
        steps_to_maturity = int(round(self._T / dt))
        if not np.isclose(steps_to_maturity * dt, self._T):
            raise ValueError("The maturity of the bond must be a multiple of dt")

        brownian_motion = BrownianMotion()
        discount_factors = np.zeros(nScen)
        for i in range(nScen):
            simulation = brownian_motion.simulate_Vasicek_Two_Factor(r0, a, b, sigma, rho, T, dt)
            # The bond pays a nominal amount, so it is discounted with the nominal rate up to its maturity
            nominal_rate = simulation['Nominal Interest Rate'].values[:steps_to_maturity + 1]
            time = simulation.index.values[:steps_to_maturity + 1]
            discount_factors[i] = np.exp(-integrate.trapezoid(nominal_rate, time))
        self._price = np.mean(discount_factors)
        return self._price

    # Previous name of the method, kept so that existing code keeps working
    price_Vasicek_Two_Factor = price

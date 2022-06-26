import numpy as np
import pandas as pd

from scipy.optimize import minimize

class Calibrator():

    def __init__(self, method):
        self.method = method


    def swapRates(t, p, matrix):
        # SWAPRATES calculates the XXX 
        # S = swapRates(t, p, matrix)
        #
        # Arguments:
        #   t = 
        #   p = 
        #   matrix = 
        #
        # Returns:
        #   S = 
        #
        # Example:
        #
        # For more information see SOURCE
        
        tmax = matrix[-1]

        ttemp = np.arange(0.5, tmax + 0.5, 0.5)
        ptemp = np.interp(ttemp, t, p)

        dis = np.cumsum(ptemp)
        pmatrix = np.interp(matrix, t, p)

        index = (2 * matrix).astype(int) - 1
        S = 100 * 2 * (1 - pmatrix) / dis[index]

        return S

    def rates(t, p, matrix):
        # RATES calculates the XXX
        # R = rates(t, p, matrix)
        #
        # Arguments:
        #   t =
        #   p = 
        #   matrix = 
        #
        # Returns:
        #   R = 
        #
        # Example:
        #       
        # For more information see SOURCE
        
        pmatrix = np.interp(matrix, t, p)
        R = 100 * (1. / pmatrix - 1) / matrix

        return R

    def objectiveFunction(params, t, RATES, SWAP):
        # OBJECTIVEFUNCTION calculates the XXX
        # mse = objectiveFunction(params, t, RATES, SWAP)
        #
        # Arguments:
        #   params =
        #   t = 
        #   RATES = 
        #   SWAP
        #
        # Returns:
        #   mse = 
        #
        # Example:
        #
        # For more information see SOURCE
        
        r0 = params[0]
        a = params[1]
        b = params[2]
        sigma = params[3]

        p = self.zeroCoupon(t, r0, a, b, sigma)
        S = self.swapRates(t, p, SWAP[:,0])
        L = self.rates(t, p, RATES[:,0])

        rel1 = (S - SWAP[:,1]) / SWAP[:,1]
        rel2 = (L - RATES[:,1]) / RATES[:,1]

        mse = np.sum(rel1**2) + np.sum(rel2**2)

        return mse

    def calibration(fun, param_0, t, RATES, SWAP):
        # CALIBRATION calculates the XXX
        # p, L, S = calibration(fun, param_0, t, RATES, SWAP)
        #
        # Arguments:
        #   fun =
        #   param_0 = 
        #   t = 
        #   RATES = 
        #   SWAP = 
        #
        # Returns:
        #   p =
        #   L = 
        #   S =
        #
        # Example:
        #
        # For more information see SOURCE
        
        opt = {'maxiter':1000, 'maxfev':5e3}
        solution = minimize(fun, param_0, args = (t, RATES, SWAP, model), method='Nelder-Mead', options=opt)
        parameters = np.array(solution.x)

        r_star = parameters[0]
        a_star = parameters[1]
        b_star = parameters[2]
        sigma_star = parameters[3]

        p = self.zeroCoupon(t, r_star, a_star, b_star, sigma_star, model)
        R = rates(t, p, RATES[:, 0])
        S = swapRates(t, p, SWAP[:, 0])

        return p, L, S

    def calibrate(self, rates):
        # CALIBRATIE calculates the XXX
        # p, E = calibrate(self, rates)
        #
        # Arguments:
        #   self =
        #   rates = 
        #
        # Returns:
        #   p =
        #   E = 
        #
        # Example:
        #
        # For more information see SOURCE
        
        if self.method == 'Optimize Error':

            p, E = calibrate_Optimize_Error(objectiveFunction, [0.1, 1.0, 1.0, 0.2], 0.1, rates)

        return p, E

    def zeroCoupon(t: float = 1.0, r0: float = 0.01, a: float = 1.0, b: float = 1.0, sigma: float = 0.2):
        # ZEROCOUPON calculates the XXX
        # zc = zeroCoupon(t, r0, a, b, sigma)
        #
        # Arguments:
        #   t =
        #   r0 = 
        #   a =
        #   b = 
        #   sigma = 
        #
        # Returns:
        #   zc = 
        #
        # Example:
        #       
        # For more information see SOURCE
        
        B = (1 - np.exp(-a * t)) / a
        A = (b - sigma**2 / (2 * a**2)) * (B - t) - (sigma**2 / (4 * a)) * B**2
        n = len(A)
        r = np.repeat(r0, n)
        zc = np.exp(A - B * r)

        return zc

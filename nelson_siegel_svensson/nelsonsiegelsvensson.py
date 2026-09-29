import numpy as np
from scipy.optimize import minimize

def NelsonSiegelSvensson(T, beta0: float, beta1: float, beta2: float, beta3: float, lambda0: float, lambda1: float):
    """
    NelsonSiegelSvensson calculates the interpolated/extrapolated curve at points in the array "T" using the Nelson-Siegel-Svensson algorithm,
    parameterized with parameters beta0, beta1, beta2, beta3, lambda0, lambda1. It returns a numpy ndarray of points.
    
    Arguments:
        T: n x 1 ndarray of maturities for which the user wants to calculate the corresponding rate.
        beta0: 1 x 1 floating number, representing the first factor of the NSS parametrization.
        beta1: 1 x 1 floating number, representing the second factor of the NSS parametrization.
        beta2: 1 x 1 floating number, representing the third factor of the NSS parametrization.
        beta3: 1 x 1 floating number, representing the fourth factor of the NSS parametrization.
        lambda0: 1 x 1 floating number, representing the first shape parameter lambda of the NSS parametrization.
        lambda1: 1 x 1 floating number, representing the second shape parameter lambda of the NSS parametrization.
        
    Returns:
        n x 1 ndarray of interpolated/extrapolated points corresponding to maturities inside T. Where n is the length of the vector T.
        At T = 0 the rate is the limit beta0 + beta1.
        
    Implemented by Gregor Fabjan from Qnity Consultants on  11/07/2023
    """
    T = np.asarray(T, dtype=float)

    def slope_loading(lam):
        # (1 - exp(-T/lam)) / (T/lam), which tends to 1 as T tends to 0
        x = T / lam
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(x == 0, 1.0, (1 - np.exp(-x)) / x)

    alpha1 = slope_loading(lambda0)
    alpha2 = alpha1 - np.exp(-T/lambda0)
    alpha3 = slope_loading(lambda1) - np.exp(-T/lambda1)

    return beta0 + beta1*alpha1 + beta2*alpha2 + beta3*alpha3

def NSSGoodFit(params: list, TimeVec, YieldVec):
    """
    NSSGoodFit calculates the residuals between the yield predicted by the NSS algorithm with the specified parameterization and the market observed ones.
    
    Arguments:
        params: 6 x 1 tuple containing the 6 parameters of the NSS algorithm. The sequence of parameters needs to be (beta0, ..., beta3, lambda0, lambda1).
        TimeVec: n x 1 ndarray of maturities for which the yields in YieldVec were observed.
        YieldVec: n x 1 ndarray of observed yields.
        
    Returns:
        1 x 1 float number, the sum of squared differences between the calculated points and observed data.
        
    Implemented by Gregor Fabjan from Qnity Consultants on  11/07/2023
    """

    return np.sum((NelsonSiegelSvensson(TimeVec, params[0], params[1], params[2], params[3], params[4], params[5])-YieldVec)**2)

def NSSMinimize(beta0: float, beta1: float, beta2: float, beta3: float, lambda0: float, lambda1: float, TimeVec, YieldVec) -> list:
    """
    NSSMinimize uses the built-in minimize function from the Python's scipy package. The function sets up the parameters and the function NSSGoodFit as to make it
    compatible with the way minimize requires its arguments. The shape parameters lambda0 and lambda1 are kept positive. If the optimization does not converge, a RuntimeError is raised.
    
    Arguments:
        beta0: 1 x 1 floating number, representing the first factor of the NSS parametrization.
        beta1: 1 x 1 floating number, representing the second factor of the NSS parametrization.
        beta2: 1 x 1 floating number, representing the third factor of the NSS parametrization.
        beta3: 1 x 1 floating number, representing the fourth factor of the NSS parametrization.
        lambda0: 1 x 1 floating number, representing the first shape parameter lambda of the NSS parametrization.
        lambda1: 1 x 1 floating number, representing the second shape parameter lambda of the NSS parametrization.
        TimeVec: n x 1 ndarray of maturities for which the yields in YieldVec were observed.
        YieldVec: n x 1 ndarray of observed yields.
        
    Returns:
        6 x 1 array of parameters and factors that best fit the observed yields.
        
    Source:
    - https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html
    - https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method
    
    Implemented by Gregor Fabjan from Qnity Consultants on  11/07/2023
    """

    bounds = [(None, None)] * 4 + [(1e-6, None)] * 2 # the shape parameters lambda0 and lambda1 must be positive
    opt_sol = minimize(NSSGoodFit, x0=np.array([beta0, beta1, beta2, beta3, lambda0, lambda1]), args = (TimeVec, YieldVec), method="Nelder-Mead", bounds = bounds)
    if (opt_sol.success):
        return opt_sol.x
    else:
        raise RuntimeError("The Nelder-Mead optimization did not converge: " + str(opt_sol.message))

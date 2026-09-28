import numpy as np
from SWCalibrate import SWCalibrate as SWCalibrate
from SWExtrapolate import SWExtrapolate as SWExtrapolate

def Galfa(M_Obs: np.ndarray, r_Obs: np.ndarray, ufr: float, alpha: float, Tau: float)->float:
    """
    Calculates the gap at the convergence point between the allowable tolerance Tau and the curve extrapolated using the Smith-Wilson algorithm.
    interpolation and extrapolation of rates.
    
    Args:
        M_Obs = 1-dimensional ndarray of n maturities of bonds, that have rates provided in input (r). Ex. M_Obs = np.array([1, 3])
        r_Obs = 1-dimensional ndarray of n rates, for which you wish to calibrate the algorithm. Each rate belongs to an observable Zero-Coupon Bond with a known maturity. Ex. r_Obs = np.array([0.0024, 0.0034])
        ufr =   1 x 1 floating number, representing the ultimate forward rate. Ex. ufr = 0.042
        alpha = 1 x 1 floating number representing the convergence speed parameter alpha. Ex. alpha = 0.05
        Tau =   1 x 1 floating number representing the allowed difference between ufr and actual curve. Ex. Tau = 0.00001
    
    Returns:
        1 x 1 floating number representing the distance between ufr input and the maximum allowed discrepancy Tau 

    Example of use:
        >>> import numpy as np
        >>> from SWCalibrate import SWCalibrate as SWCalibrate
        >>> from SWExtrapolate import SWExtrapolate as SWExtrapolate
        >>> M_Obs = np.transpose(np.array([1, 2, 4, 5, 6, 7]))
        >>> r_Obs =  np.transpose(np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04]))
        >>> alfa = 0.15
        >>> ufr = 0.04
        >>> Precision = 0.0000000001
        >>> Tau = 0.0001
        >>> Galfa(M_Obs, r_Obs, ufr, alfa, Tau)
        [Out] -8.544212205612438e-05

    For more information see https://www.eiopa.europa.eu/document/download/df541a50-a9e7-458b-86ae-6ad16c2d6a29_en?filename=16-09-2022%20Technical%20documentation
    
    Implemented by Gregor Fabjan from Qnity Consultants on 17/12/2021.
    """
    
    M_Obs = np.ravel(M_Obs)                       # Accept column vectors as well as 1-dimensional arrays
    r_Obs = np.ravel(r_Obs)
    U = max(M_Obs)                                # Find maximum liquid maturity from input
    T = max(U + 40, 60)                             # Define the convergence point as defined in paragraph 122 and again in 159
    C = np.identity(M_Obs.size)                   # Construct cash flow matrix described in paragraph 139 assuming the input is ZCB bonds with notional value of 1
    d = np.exp(-np.log(1 + ufr) * M_Obs)            # Calculate vector d described in paragraph 140
    Q = np.diag(d) @ C                            # Matrix Q described in paragraph 141
    b = SWCalibrate(r_Obs, M_Obs, ufr, alpha)     # Calculate the calibration vector b using the equation from paragraph 151
    K = (1+alpha * M_Obs @ Q@ b) / (np.sinh(alpha * M_Obs.transpose())@ Q@ b) # Calculate kappa as defined in the paragraph 157
    return( alpha/np.abs(1 - K*np.exp(alpha*T))-Tau) # Size of the gap at the convergence point between the allowable tolerance Tau and the actual curve. Defined in paragraph 160

def BisectionAlpha(xStart: float, xEnd: float, M_Obs: np.ndarray, r_Obs: np.ndarray, ufr: float, Tau: float, Precision: float, maxIter: int)->float:
    """
    Bisection root finding algorithm for finding the root of a function. The function here is the allowed difference between the ultimate forward rate and the extrapolated curve using Smith & Wilson.

    Args:
        xStart =    1 x 1 floating number representing the minimum allowed value of the convergence speed parameter alpha. Ex. alpha = 0.05
        xEnd =      1 x 1 floating number representing the maximum allowed value of the convergence speed parameter alpha. Ex. alpha = 0.8
        M_Obs =     1-dimensional ndarray of n maturities of bonds, that have rates provided in input (r). Ex. M_Obs = np.array([1, 3])
        r_Obs =     1-dimensional ndarray of n rates, for which you wish to calibrate the algorithm. Each rate belongs to an observable Zero-Coupon Bond with a known maturity. Ex. r_Obs = np.array([0.0024, 0.0034])
        ufr  =      1 x 1 floating number, representing the ultimate forward rate. Ex. ufr = 0.042
        Tau =       1 x 1 floating number representing the allowed difference between ufr and actual curve. Ex. Tau = 0.00001
        Precision = 1 x 1 floating number representing the precision of the calculation. Higher the precision, more accurate the estimation of the root
        maxIter =   1 x 1 positive integer representing the maximum number of iterations allowed. This is to prevent an infinite loop in case the method does not converge to a solution         
    
    Returns:
        1 x 1 floating number representing the optimal value of the parameter alpha. If the curve is already within Tau
        of the ufr at xStart, xStart is returned.

    Raises:
        ValueError if the gap is larger than Tau for every alpha in [xStart, xEnd].
        RuntimeError if the method does not converge within maxIter iterations.

    Example of use:
        >>> import numpy as np
        >>> from SWCalibrate import SWCalibrate as SWCalibrate
        >>> M_Obs = np.transpose(np.array([1, 2, 4, 5, 6, 7]))
        >>> r_Obs =  np.transpose(np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04]))
        >>> xStart = 0.05
        >>> xEnd = 0.5
        >>> maxIter = 1000
        >>> alfa = 0.15
        >>> ufr = 0.04
        >>> Precision = 0.0000000001
        >>> Tau = 0.0001
        >>> BisectionAlpha(xStart, xEnd, M_Obs, r_Obs, ufr, Tau, Precision, maxIter)
        [Out] 0.11549789285636511

    For more information see https://www.eiopa.europa.eu/document/download/df541a50-a9e7-458b-86ae-6ad16c2d6a29_en?filename=16-09-2022%20Technical%20documentation and https://en.wikipedia.org/wiki/Bisection_method
     
    Implemented by Gregor Fabjan from Qnity Consultants on 17/12/2021.
    """   

    yStart = Galfa(M_Obs, r_Obs, ufr, xStart, Tau) # Check if the initial point is a solution
    yEnd = Galfa(M_Obs, r_Obs, ufr, xEnd, Tau) # Check if the final point is a solution
    if np.abs(yStart) < Precision:
        return xStart # If initial point already satisfies the conditions return start point
    if np.abs(yEnd) < Precision:
        return xEnd # If final point already satisfies the conditions return end point
    if np.sign(yStart) == np.sign(yEnd): # The interval does not bracket a root
        if yStart < 0:
            return xStart # The curve is already within Tau of the ufr at the lowest allowed alpha. EIOPA uses the lowest alpha (at least 0.05) that meets the tolerance (paragraphs 123 and 161)
        raise ValueError("The gap to the ufr is larger than Tau for every alpha in [xStart, xEnd]; increase xEnd")
    iIter = 0
    while iIter <= maxIter:
        xMid = (xEnd+xStart)/2 # calculate mid-point 
        yMid = Galfa(M_Obs, r_Obs, ufr, xMid, Tau) # What is the solution at midpoint

        if (yMid == 0 or (xEnd-xStart)/2 < Precision): # Solution found
            return xMid
        else: # Solution not found
            iIter += 1
            if np.sign(yMid) == np.sign(yStart): # If the start point and the middle point have the same sign, then the root must be in the second half of the interval   
                xStart = xMid
            else: # If the start point and the middle point have a different sign than by mean value theorem the interval must contain at least one root
                xEnd = xMid
    raise RuntimeError("Method failed to converge within maxIter iterations")

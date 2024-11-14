import numpy as np

def SWCalibrate(r, M, ufr: float, alpha: float):
    """
    Calculate the calibration vector using the Smith-Wilson algorithm.

    Calculates the calibration vector `b` used for interpolation and extrapolation of rates.

    Arguments:
        r: n x 1 ndarray of rates for which you wish to calibrate the algorithm. Each rate belongs to an observable zero-coupon bond with a known maturity. Example: r = np.array([[0.0024], [0.0034]])
        M: n x 1 ndarray of maturities of bonds that have rates provided in the input `r`. Example: M = np.array([[1], [3]])
        ufr: Floating number representing the ultimate forward rate. Example: ufr = 0.042
        alpha: Floating number representing the convergence speed parameter alpha. Example: alpha = 0.05

    Returns:
        n x 1 ndarray representing the calibration vector needed for interpolation and extrapolation. Example: b = np.array([[14], [-21]])

    For more information, refer to the documentation at:
    https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
    """

    from SWHeart import SWHeart as SWHeart

    C = np.identity(M.size)
    p = (1+r) **(-M)  # Transform rates to implied market prices of a ZCB bond
    d = np.exp(-np.log(1+ufr) * M)    # Calculate vector d described in paragraph 138
    Q = np.diag(d) @ C                  # Matrix Q described in paragraph 139
    q = C.transpose() @ d                         # Vector q described in paragraph 139
    H = SWHeart(M, M, alpha) # Heart of the Wilson function from paragraph 132

    return np.linalg.inv(Q.transpose() @ H @ Q) @ (p-q)          # Calibration vector b from paragraph 149

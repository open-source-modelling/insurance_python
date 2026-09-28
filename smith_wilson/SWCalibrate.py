import numpy as np

def SWCalibrate(r: np.ndarray, M: np.ndarray, ufr: float, alpha: float) -> np.ndarray:
    """
    Calculate the calibration vector using the Smith-Wilson algorithm.

    Calculates the calibration vector `b` used for interpolation and extrapolation of rates.

    Arguments:
        r: 1-dimensional ndarray of n rates for which you wish to calibrate the algorithm. Each rate belongs to an observable zero-coupon bond with a known maturity. Example: r = np.array([0.0024, 0.0034])
        M: 1-dimensional ndarray of the n maturities of bonds that have rates provided in the input `r`. Example: M = np.array([1, 3])
        ufr: Floating number representing the ultimate forward rate. Example: ufr = 0.042
        alpha: Floating number representing the convergence speed parameter alpha. Example: alpha = 0.05

    Returns:
        1-dimensional ndarray of n elements representing the calibration vector needed for interpolation and extrapolation. Example: b = np.array([14, -21])

    Column vectors (n x 1 ndarrays) are also accepted; they are flattened.

    For more information, refer to the documentation at:
    https://www.eiopa.europa.eu/document/download/df541a50-a9e7-458b-86ae-6ad16c2d6a29_en?filename=16-09-2022%20Technical%20documentation
    """

    from SWHeart import SWHeart as SWHeart

    r = np.ravel(r)
    M = np.ravel(M)
    C = np.identity(M.size)
    p = (1+r) **(-M)                  # Transform rates to implied market prices of a ZCB bond
    d = np.exp(-np.log(1+ufr) * M)    # Calculate vector d described in paragraph 140
    Q = np.diag(d) @ C                # Matrix Q described in paragraph 141
    q = C.transpose() @ d             # Vector q described in paragraph 141
    H = SWHeart(M, M, alpha)          # Heart of the Wilson function from paragraph 134

    return np.linalg.solve(Q.transpose() @ H @ Q, p-q) # Calibration vector b from paragraph 151, solving the linear system rather than inverting the matrix

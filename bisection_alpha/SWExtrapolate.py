import numpy as np

def SWExtrapolate(M_Target: np.ndarray, M_Obs: np.ndarray, b: np.ndarray, ufr: float, alpha: float) -> np.ndarray:
    """
    Interpolate or extrapolate rates for targeted maturities using the Smith-Wilson algorithm.

    Calculates the rates for maturities specified in `M_Target` using the calibration vector `b` obtained
    from observed bond maturities in `M_Obs`.

    Arguments:
        M_Target: 1-dimensional ndarray of the k targeted bond maturities of interest. They must be non-negative. Example: M_Target = np.array([1, 2, 3, 5])
        M_Obs: 1-dimensional ndarray of the n observed bond maturities used for calibrating the calibration vector `b`. Example: M_Obs = np.array([1, 3])
        b: 1-dimensional ndarray of n elements representing the calibration vector calculated on observed bonds.
        ufr: Floating number representing the ultimate forward rate. Example: ufr = 0.042
        alpha: Floating number representing the convergence speed parameter alpha. Example: alpha = 0.05

    Returns:
        1-dimensional ndarray of k elements representing the targeted rates for zero-coupon bonds. Each rate belongs to a targeted
        zero-coupon bond with a maturity from `M_Target`. Example: r = np.array([0.0024, 0.0029, 0.0034, 0.0039])
        For maturity 0 the rate is the limit of the rates as the maturity goes to 0, exp(y(0)) - 1, where y(0) is the
        zero spot intensity from paragraph 155.

    Raises:
        ValueError if a targeted maturity is negative or NaN.

    Column vectors (n x 1 ndarrays) are also accepted; they are flattened.

    For more information, refer to the documentation at:
    https://www.eiopa.europa.eu/document/download/df541a50-a9e7-458b-86ae-6ad16c2d6a29_en?filename=16-09-2022%20Technical%20documentation
    """

    from SWHeart import SWHeart as SWHeart

    M_Target = np.ravel(M_Target).astype(float)
    M_Obs = np.ravel(M_Obs)
    b = np.ravel(b)
    if not np.all(M_Target >= 0): # also rejects NaN
        raise ValueError("The targeted maturities must be non-negative")
    C = np.identity(M_Obs.size)
    d = np.exp(-np.log(1+ufr) * M_Obs)   # Calculate vector d described in paragraph 140
    Q = np.diag(d) @ C                   # Matrix Q described in paragraph 141
    H = SWHeart(M_Target, M_Obs, alpha)  # Heart of the Wilson function from paragraph 134
    p = np.exp(-np.log(1+ufr)* M_Target) + np.diag(np.exp(-np.log(1+ufr) * M_Target)) @ H @ Q @ b # Discount pricing function for targeted maturities from paragraph 149

    rates = np.empty(M_Target.size)
    positive = M_Target > 0
    rates[positive] = p[positive] ** (-1/ M_Target[positive]) -1 # Convert obtained prices to rates
    # At maturity 0 the rate p(t)^(-1/t) - 1 is undefined: p(0) = 1 and -1/t is infinite. Its limit is exp(y(0)) - 1, where
    # y(0) = ln(1+ufr) - alpha * (1 - exp(-alpha*M_Obs))' Q b is the zero spot intensity from paragraph 155
    y0 = np.log(1+ufr) - alpha * (1 - np.exp(-alpha * M_Obs)) @ Q @ b
    rates[~positive] = np.exp(y0) - 1
    return rates

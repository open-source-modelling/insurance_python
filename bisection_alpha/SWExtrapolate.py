import numpy as np 

def SWExtrapolate(M_Target: np.ndarray, M_Obs: np.ndarray, b: np.ndarray, ufr: float, alpha:float)->np.ndarray:
   """
   Interpolate or extrapolate rates for targeted maturities using the Smith-Wilson algorithm.

   Calculates the rates for maturities specified in `M_Target` using the calibration vector `b` obtained
   from observed bond maturities in `M_Obs`.

   Arguments:
       M_Target: k x 1 ndarray representing each targeted bond maturity of interest. Example: M_Target = np.array([[1], [2], [3], [5]])
       M_Obs: n x 1 ndarray representing the observed bond maturities used for calibrating the calibration vector `b`. Example: M_Obs = np.array([[1], [3]])
       b: n x 1 ndarray representing the calibration vector calculated on observed bonds.
       ufr: Floating number representing the ultimate forward rate. Example: ufr = 0.042
       alpha: Floating number representing the convergence speed parameter alpha. Example: alpha = 0.05

   Returns:
       k x 1 ndarray representing the targeted rates for zero-coupon bonds. Each rate belongs to a targeted
       zero-coupon bond with a maturity from `M_Target`. Example: r = np.array([0.0024, 0.0029, 0.0034, 0.0039])

   For more information, refer to the documentation at:
   https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
   """

   from SWHeart import SWHeart as SWHeart

   C = np.identity(M_Obs.size)
   d = np.exp(-np.log(1+ufr) * M_Obs)                                                # Calculate vector d described in paragraph 138
   Q = np.diag(d) @ C                                                             # Matrix Q described in paragraph 139
   H = SWHeart(M_Target, M_Obs, alpha)                                          # Heart of the Wilson function from paragraph 132
   p = np.exp(-np.log(1+ufr)* M_Target) + np.diag(np.exp(-np.log(1+ufr) * M_Target)) @ H @ Q @ b # Discount pricing function for targeted maturities from paragraph 147
   return p ** (-1/ M_Target) -1 # Convert obtained prices to rates and return prices

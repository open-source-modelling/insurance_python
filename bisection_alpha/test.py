import numpy as np
from SWCalibrate import SWCalibrate as SWCalibrate
from SWExtrapolate import SWExtrapolate as SWExtrapolate
from bisection_alpha import Galfa as Galfa
from bisection_alpha import BisectionAlpha as BisectionAlpha

# Maturities of bonds observed on the market
M_Obs = np.transpose(np.array([1, 2, 4, 5, 6, 7]))

# Yields observed on the market
r_Obs = np.transpose(np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04]))

# Ultimate forward rate
ufr = 0.04

# Numeric precision of the optimisation
Precision = 0.0000000001

# Targeted distance between the extrapolated curve and the ultimate forward rate at the convergence point
Tau = 0.0001 # 1 basis point

# Examples of a call to Galfa and BisectionAlpha
print("Example in the documentation for Galfa: "+ str(Galfa(M_Obs, r_Obs, ufr, 0.15, Tau)))
print("Example in the documentation for BisectionAlpha: "+ str(BisectionAlpha(0.05, 0.5, M_Obs, r_Obs, ufr, Tau, Precision, 1000)))
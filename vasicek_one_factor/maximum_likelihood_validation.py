import numpy as np
from Vasicek_one_factor import simulate_Vasicek_One_Factor

# Simulate a long path of the Vasicek process dr = a * (lam - r) dt + sigma dW with known parameters,
# then estimate the parameters back from the path. The estimates should be close to the true values.
# The estimators follow T. van den Berg, "Calibrating the Ornstein-Uhlenbeck (Vasicek) model" (2011),
# where lambda is the speed of reversion (a here) and mu is the long-term mean (lam here).

r0 = 3 # The starting interest rate
a = 3 # speed of reversion parameter
lam = 1 # long term mean interest rate level. The process reverts towards lam
sigma = 0.5 # instantaneous volatility
T = 500 # end modelling time
dt = 0.01 # increments of time

out = simulate_Vasicek_One_Factor(r0, a, lam, sigma, T, dt)

Yield = out.values.flatten()
SampleSize = Yield.size

Yieldx = Yield[0:(SampleSize-1)]
Yieldy = Yield[1:SampleSize]

Sx = np.sum(Yieldx)
Sy = np.sum(Yieldy)
Sxx = np.sum(Yieldx * Yieldx)
Sxy = np.sum(Yieldx * Yieldy)
Syy = np.sum(Yieldy * Yieldy)

n = SampleSize-1

# Least squares: regress Yieldy on Yieldx, Yieldy = slope * Yieldx + intercept + noise
slope = (n * Sxy - Sx * Sy)/(n * Sxx - Sx**2)
intercept = (Sy - slope*Sx)/n
sd = np.sqrt((n*Syy-Sy**2 - slope*(n*Sxy-Sx*Sy))/(n*(n-2)))

LSlam = -np.log(slope)/dt
LSmu = intercept/(1-slope)
LSsigma = sd * np.sqrt((-2*np.log(slope))/(dt*(1-slope**2)))

# Maximum likelihood
MLmu = (Sy*Sxx - Sx*Sxy) / (n*(Sxx-Sxy)-(Sx**2 - Sx*Sy))
MLlam = -1/dt* np.log((Sxy-MLmu*Sx-MLmu*Sy+n*MLmu**2)/(Sxx-2*MLmu*Sx+n*MLmu**2))

alpha = np.exp(-MLlam*dt)
sigmaHat = 1/n * (Syy - 2* alpha* Sxy + alpha **2 * Sxx-2*MLmu*(1-alpha)*(Sy-alpha*Sx)+n*MLmu**2 *(1-alpha)**2)
MLsigma = np.sqrt(sigmaHat * (2*MLlam)/(1-alpha**2))

print("                          true   least squares   maximum likelihood")
print(f"long-term mean (lam)  {lam:8.4f}   {LSmu:13.4f}   {MLmu:18.4f}")
print(f"speed of reversion (a){a:8.4f}   {LSlam:13.4f}   {MLlam:18.4f}")
print(f"volatility (sigma)    {sigma:8.4f}   {LSsigma:13.4f}   {MLsigma:18.4f}")

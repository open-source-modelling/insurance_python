import numpy as np
from Vasicek_one_factor import simulate_Vasicek_One_Factor

r0 = 3 # The starting interest rate
a = 3 # speed of reversion parameter
b = 1 # long term mean interest rate level correction. (Long-term mean is a * b) 
sigma = 0.5 # instantaneous volatility
T = 500 # end modelling time
dt = 0.01 # increments of time

out = simulate_Vasicek_One_Factor(r0, a, b, sigma, T, dt)

Yield = np.array(out.values)
SampleSize = Yield.size

Yieldx = Yield[0:(SampleSize-1)]
Yieldy = Yield[1:SampleSize]

Sx = sum(Yieldx)
Sy = sum(Yieldy)
Sxx = sum(Yieldx * Yieldx)
Sxy = sum(Yieldx * Yieldy)
Syy = sum(Yieldy * Yieldy)

n = SampleSize-1

a = (n * Sxy - Sx * Sy)/(n * Sxx - Sx**2)
b = (Sy - a*Sx)/n
sd = np.sqrt((n*Syy-Sy**2 - a*(n*Sxy-Sx*Sy))/(n*(n-2)))

lam = -np.log(a)/dt
mu = b/(1-a)
sigma = sd * np.sqrt((-2*np.log(a))/(dt*(1-a**2)))

MLmu = (Sy*Sxx - Sx*Sxy) / (n*(Sxx-Sxy)-(Sx**2 - Sx*Sy))
MLlam = -1/dt* np.log((Sxy-mu*Sx-mu*Sy+n*mu**2)/(Sxx-2*mu*Sx+n*mu**2))

alpha = np.exp(-lam*dt)
sigmaHat = 1/n * (Syy - 2* alpha* Sxy + alpha **2 * Sxx-2*mu*(1-alpha)*(Sy-alpha*Sx)+n*mu**2 *(1-alpha)**2)
MLsigmaSqrt = np.sqrt(sigmaHat * (2*lam)/(1-alpha**2)) 

print("ML mu for Vasicek is:")
print(MLmu)
print("ML lambda for Vasicek is:")
print(MLlam)
print("ML sigma for Vasicek is:")
print(MLsigmaSqrt)

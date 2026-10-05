import numpy as np
import pandas as pd

def simulate_Hull_White_One_Factor(a: float, sigma: float, t, f) ->pd.DataFrame:
    """ Simulates a temporal series of interest rates using the One Factor Hull-White model
     Form of the model is dr_{t} = [theta(t) - a * r_{t}] dt + sigma * dW_{t}, where theta(t) is chosen so that
     the model reproduces today's term structure of interest rates
     interest_rate_simulation = simulate_Hull_White_One_Factor(a, sigma, t, f)

     The short rate is simulated as r(t) = x(t) + alpha(t), where x(t) follows dx = -a * x * dt + sigma * dW
     and starts at x(0) = 0 today, and alpha(t) = f(0,t) + sigma^2 / (2 * a^2) * (1 - exp(-a * t))^2.
     Today's short rate is therefore r(0) = f(0,0), given by the forward curve.
     x(t) is simulated exactly from today (t = 0) to each time in t.

     Args:
       a (float): speed of mean reversion; it must be positive. The short rate reverts towards its mean path alpha(t),
                  and deviations from it die out like exp(-a * t).
       sigma (float): instantaneous volatility of the short rate. It is an absolute volatility in units of the rate: sigma = 0.01 means changes of about 1 percentage point per year.
       t (array of floats): times at which the output is generated, in years from today. They must be non-negative and strictly increasing.
                            With t[0] = 0 the first value is today's short rate f(0,0); if the grid starts later, the first value is already random.
       f (array of floats): today's instantaneous forward rates f(0,t) for the times in t.

     Returns:
       N x 1 Pandas DataFrame where index is modeling time and values are a realisation of the short rate.

     Example:
       The forward rates are equal to 3% for all maturities, so today's short rate is 3%. The absolute volatility of the short rate is 1 percentage point per year (sigma = 0.01) and the external analysis points out that the parameter a is 0.04.
       The user is interested in an interest rate projection of the next 10 years in annual time steps

       import pandas as pd
       import numpy as np

       np.random.seed(1)
       simulate_Hull_White_One_Factor(0.04, 0.01, np.arange(0, 11), np.full(11, 0.03))
       [out] =       Interest Rate
               Time               
               0.0        0.030000
               1.0        0.024051
               2.0        0.019245
               3.0        0.009370
               4.0        0.018962
               5.0       -0.002797
               6.0        0.016030
               7.0        0.009612
               8.0        0.014092
               9.0        0.012876
               10.0       0.028533
     For more information see https://en.wikipedia.org/wiki/Hull-White_model
    """

    if not a > 0:
        raise ValueError("a must be positive") # a = 0 is a different model (Ho-Lee) that needs other formulas
    t = np.asarray(t, dtype=float)
    f = np.asarray(f, dtype=float)
    if t.ndim != 1 or t.size == 0 or t.shape != f.shape:
        raise ValueError("t and f must be non-empty one-dimensional arrays of the same length")
    if t[0] < 0 or np.any(np.diff(t) <= 0):
        raise ValueError("t must be non-negative and strictly increasing")

    alpha = f + sigma**2/(2*a**2)*(1-np.exp(-a*t))**2 # deterministic shift that makes the model fit today's curve
    x = np.zeros(t.shape[0])
    x_prev, t_prev = 0.0, 0.0 # x starts at 0 today (t = 0)
    for el in range(t.shape[0]):
        deltat = t[el] - t_prev
        mean = x_prev * np.exp(-a*deltat)
        var = sigma**2/(2*a) * (1 - np.exp(-2*a*deltat))
        x[el] = np.random.normal(mean, np.sqrt(var))
        x_prev, t_prev = x[el], t[el]
    r = x + alpha

    data = {'Time' : t, 'Interest Rate' : r}

    interest_rate_simulation = pd.DataFrame.from_dict(data = data)
    interest_rate_simulation.set_index('Time', inplace = True)
    return interest_rate_simulation

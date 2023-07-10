import numpy as np
import pandas as pd

def simulate_Black_Scholes(S0, mu, sigma, T, dt) -> pd.DataFrame:
    """Simulate a temporal series of stock prices using the Black-Scholes log-normal model and generated Brownian motion.

    Args:
        S0 (int): Initial value of the underlying asset.
        mu (float): Drift rate of the underlying asset.
        sigma (float): Standard deviation of the underlying asset's return.
        T (int): Maximum modeling time.
        dt (float): Length of each subinterval.

    Returns:
        pd.DataFrame: N x 2 DataFrame with index as modeling time and values as realizations of the underlying's price.

    Example:
        Model the price of a stock which is worth today 100. The market has a future annualized risk-free rate of 5% and an annualized volatility of 30%. The user is interested in a price projection for the next 10 years in increments of 6 months (0.5 years).
        import pandas as pd
        import numpy as np
        simulate_Black_Scholes(100, 0.05, 0.3, 10, 0.5)
        Output:
               Stock Price
        Time
        0.0     100.000000
        0.5     131.721286
        1.0     124.924654
        1.5     209.302935
        2.0     222.085955
        ...     ...
        9.5    202.368581
        10.0   262.282989

    Reference:
    For more information, see: https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
    """
    
    N = int(T / dt) # number of subintervals of length 1/dt between 0 and max modeling time T

    time, delta_t = np.linspace(0, T, num = N+1, retstep = True)
    
    S = np.exp((mu - sigma ** 2 / 2) * dt + sigma * np.random.normal(0, np.sqrt(dt), size= N))
    S = np.hstack([1, S])
    S = S0* S.cumprod(axis=0)

    dict = {'Time' : time, 'Stock Price' : S}

    stock_price_simulation = pd.DataFrame.from_dict(data = dict)
    stock_price_simulation.set_index('Time', inplace = True)

    return stock_price_simulation

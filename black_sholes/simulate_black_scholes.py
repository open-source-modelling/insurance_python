import numpy as np
import pandas as pd

def simulate_black_scholes(S0: float, mu: float, sigma: float, T: float, dt: float) -> pd.DataFrame:
    """
    Simulate a single path for stock prices using the Black-Scholes model with vectorized operations.
    
    Args:
        S0 (float): Initial value of the underlying asset.
        mu (float): Drift rate of the underlying asset.
        sigma (float): Standard deviation of the underlying asset's return.
        T (float): Maximum modeling time.
        dt (float): Length of each subinterval.
        
    Returns:
        pd.DataFrame: DataFrame with time as the index and a single column for the simulated stock price.

    Example:
        Model the price of a stock which is worth today 100. The market has a future annualized risk-free rate of 5% and an annualized volatility of 30%. The user is interested in a price projection for the next 10 years in increments of 6 months (0.5 years).
        import pandas as pd
        import numpy as np
        simulate_Black_Scholes(100, 0.05, 0.3, 10, 0.5)
        Output:
                Cumulative_Price
            0.0         100.000000
            0.5         129.988711
            1.0         164.336273
            1.5         123.987617
            2.0         170.535179
            2.5         165.820812
            3.0         168.108448
            3.5         155.481838
            4.0         125.441538
            4.5          96.216396
            5.0          99.090337
            5.5         149.457225
            6.0         183.199463
            6.5         183.598311
            7.0         130.795698
            7.5         126.942983
            8.0         152.856431
            8.5         184.111451
            9.0         140.536182
            9.5         120.704683
            10.0        157.433053     

    Reference:
    For more information, see: https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model 
    """
    
    N = int(T / dt)  # number of steps
    time = np.linspace(0, T, N + 1)
    
    # Generate random shocks with standard deviation adjusted by sqrt(dt)
    random_shocks = np.random.normal(0, 1, N)
    
    # Calculate the increments in a vectorized manner
    increments = (mu - 0.5 * sigma ** 2) * dt + sigma* np.sqrt(dt)* random_shocks
    
    # Compute the cumulative product for the price path
    price_path = S0 * np.exp(np.insert(np.cumsum(increments), 0, 0))
    
    # Convert to DataFrame with a single column for the simulated path
    return pd.DataFrame(price_path, index=time, columns=['Simulation'])


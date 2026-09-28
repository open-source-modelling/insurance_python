import numpy as np

def SWHeart(u: np.ndarray, v: np.ndarray, alpha: float) -> np.ndarray:
    """
    Calculate the heart of the Wilson function.

    Calculates the matrix H (Heart of the Wilson function) for maturities specified by vectors u and v.
    The formula is taken from the EIOPA technical specifications paragraph 132.

    Arguments:
        u: 1-dimensional ndarray of n_1 maturities. Example: u = np.array([1, 3])
        v: 1-dimensional ndarray of n_2 maturities. Example: v = np.array([1, 2, 3, 5])
        alpha: Floating number representing the convergence speed parameter alpha. Example: alpha = 0.05

    Returns:
        n_1 x n_2 ndarray representing the Heart of the Wilson function for selected maturities and parameter alpha.
        H is calculated as described in paragraph 132 of the EIOPA documentation.

    Column vectors (n x 1 ndarrays) are also accepted; they are flattened.

    For more information, see:
    https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
    """

    u = np.ravel(u)
    v = np.ravel(v)
    u_Mat = np.tile(u, [v.size, 1]).transpose()
    v_Mat = np.tile(v, [u.size, 1])

    # Return the heart of the Wilson function from paragraph 132
    return 0.5 * (alpha * (u_Mat + v_Mat) + np.exp(-alpha * (u_Mat + v_Mat)) - alpha * np.absolute(u_Mat-v_Mat) - np.exp(-alpha * np.absolute(u_Mat-v_Mat)))

import numpy as np
from scipy.stats import norm


def black_scholes_price(S0, K, T, r, sigma, option_type='call'):
    """
    Compute the Black-Scholes price for European call or put option.

    Parameters:
    - S0: initial stock price
    - K: strike price
    - T: time to maturity (in years)
    - r: risk-free interest rate
    - sigma: volatility
    - option_type: 'call' or 'put'

    Returns:
    - price: the option price
    """
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Choose 'call' or 'put'.")

    return price

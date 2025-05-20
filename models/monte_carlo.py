import numpy as np
from .simulate_paths import simulate_gbm_paths


def monte_carlo_price(S0, K, T, r, sigma, option_type='call', n_paths=10000, steps=252, seed=42):
    """
    Price a European call or put option using Monte Carlo simulation.

    Returns:
    - estimated price (float)
    - simulated stock paths (array)
    """
    paths = simulate_gbm_paths(
        S0, mu=r, sigma=sigma, T=T, steps=steps, n_paths=n_paths, seed=seed)
    S_T = paths[:, -1]

    if option_type == 'call':
        payoffs = np.maximum(S_T - K, 0)
    elif option_type == 'put':
        payoffs = np.maximum(K - S_T, 0)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    price = np.exp(-r * T) * np.mean(payoffs)
    return price, paths

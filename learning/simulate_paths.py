import numpy as np


def simulate_gbm_paths(S0, mu, sigma, T, steps, n_paths, seed=None):
    """
    Simulate stock price paths using Geometric Brownian Motion.

    Parameters:
    - S0: initial stock price
    - mu: expected return
    - sigma: volatility
    - T: total time (in years)
    - steps: number of time steps
    - n_paths: number of simulated paths
    - seed: random seed for reproducibility

    Returns:
    - paths: ndarray of shape (n_paths, steps+1)
    """
    if seed is not None:
        np.random.seed(seed)

    dt = T / steps
    paths = np.zeros((n_paths, steps + 1))
    paths[:, 0] = S0

    for t in range(1, steps + 1):
        z = np.random.standard_normal(n_paths)  # Z ~ N(0, 1)
        paths[:, t] = paths[:, t-1] * \
            np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)

    return paths

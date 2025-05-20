from options import call_payoff, put_payoff
from simulate_paths import simulate_gbm_paths
import numpy as np

# Step 1: Simulate stock paths
S0 = 150
mu = 0.1
sigma = 0.2
T = 1
steps = 252
n_paths = 10000
K = 160  # Strike price
r = 0.05  # Risk-free rate

paths = simulate_gbm_paths(S0, mu, sigma, T, steps, n_paths, seed=42)

# Step 2: Extract terminal prices
S_T = paths[:, -1]

# Step 3: Calculate payoffs
payoffs = call_payoff(S_T, K)

# Step 4: Discount to present value
discounted_price = np.exp(-r * T) * np.mean(payoffs)

print(f"Estimated Call Option Price: ${discounted_price:.2f}")


def price_option_monte_carlo(
    S0, K, T, r, sigma, option_type='call',
    n_paths=10000, steps=252, seed=None
):
    """
    Monte Carlo pricer for European call or put options.

    Parameters:
    - S0: initial stock price
    - K: strike price
    - T: time to maturity (in years)
    - r: risk-free interest rate
    - sigma: volatility
    - option_type: 'call' or 'put'
    - n_paths: number of simulations
    - steps: time steps
    - seed: random seed for reproducibility

    Returns:
    - Estimated option price (float)
    """
    paths = simulate_gbm_paths(
        S0, mu=r, sigma=sigma, T=T, steps=steps, n_paths=n_paths, seed=seed)
    S_T = paths[:, -1]

    if option_type == 'call':
        payoffs = call_payoff(S_T, K)
    elif option_type == 'put':
        payoffs = put_payoff(S_T, K)
    else:
        raise ValueError("Invalid option_type. Use 'call' or 'put'.")

    discounted_price = np.exp(-r * T) * np.mean(payoffs)
    return discounted_price

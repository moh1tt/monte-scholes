import matplotlib.pyplot as plt
from simulate_paths import simulate_gbm_paths

S0 = 150        # Starting price (like AAPL)
mu = 0.1        # 10% expected return
sigma = 0.2     # 20% annual volatility
T = 1           # 1 year
steps = 252     # daily steps
n_paths = 20    # simulate 20 paths

paths = simulate_gbm_paths(S0, mu, sigma, T, steps, n_paths, seed=42)

plt.figure(figsize=(10, 6))
plt.plot(paths.T)
plt.title("Simulated Stock Price Paths (GBM)")
plt.xlabel("Time Step (Days)")
plt.ylabel("Price")
plt.grid(True)
plt.show()

from pricer import price_option_monte_carlo

# Call the Monte Carlo option pricer with parameters
price = price_option_monte_carlo(
    S0=150,           # Initial stock price (e.g., Apple at $150 today)
    K=160,            # Strike price of the option
    T=1,              # Time to maturity in years (1 year)
    r=0.05,           # Risk-free interest rate (5%)
    sigma=0.2,        # Volatility of the stock (20%)
    option_type='call',  # Type of option: 'call' or 'put'
    seed=42           # Random seed for reproducibility
)

# Display the estimated price of the option
print(f"Estimated Call Option Price: ${price:.2f}")

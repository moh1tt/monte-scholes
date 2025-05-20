import pandas as pd
import streamlit as st
import numpy as np
from models.black_scholes import black_scholes_price
from models.monte_carlo import monte_carlo_price
from models.simulate_paths import simulate_gbm_paths
import matplotlib.pyplot as plt

st.set_page_config(page_title="MonteScholes", layout="wide")
st.title("📈 MonteScholes: Monte Carlo vs. Black-Scholes Options Pricer")

st.markdown("""
This app lets you compare two foundational option pricing models:
- **Black-Scholes**: A closed-form mathematical solution
- **Monte Carlo Simulation**: A data-driven simulation approach

Adjust parameters below and visualize how options are priced differently.
""")

with st.expander("📘 What Are We Doing Here?"):
    st.markdown("""
**OptionInsight** lets you price European-style options using two foundational models:

### 🔹 Black-Scholes Model (1973)

A closed-form analytical formula for pricing options, assuming:
- Constant volatility
- Risk-neutral market
- No dividends
- No arbitrage

#### 📈 Call Option Formula:
""")
    st.latex(r"C = S_0 \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)")
    st.markdown("Where:")
    st.latex(
        r"d_1 = \frac{\ln(S_0 / K) + (r + 0.5 \sigma^2) T}{\sigma \sqrt{T}}")
    st.latex(r"d_2 = d_1 - \sigma \sqrt{T}")

    st.markdown("#### 📉 Put Option Formula:")
    st.latex(r"P = K \cdot e^{-rT} \cdot N(-d_2) - S_0 \cdot N(-d_1)")

    st.markdown("""
---

### 🔹 Monte Carlo Simulation

A numerical method that:
1. Simulates thousands of possible stock price paths using **Geometric Brownian Motion**
2. Calculates the option **payoff** at each path's expiry
3. Averages those payoffs and **discounts** to the present

**Why Monte Carlo?**
- ✅ Works for exotic or path-dependent options
- ✅ Intuitive and flexible
- ⚠️ Slower and more random than Black-Scholes

---

Both models assume a **risk-neutral world** (returns adjusted for risk), and no arbitrage.
    """)


# --- Sidebar Inputs ---
st.sidebar.header("🔧 Option Parameters")

S0 = st.sidebar.number_input("Initial Stock Price (S₀)", 50, 500, 150)
K = st.sidebar.number_input("Strike Price (K)", 50, 500, 160)
T = st.sidebar.slider("Time to Maturity (T, in years)", 0.01, 2.0, 1.0)
r = st.sidebar.slider("Risk-Free Rate (r)", 0.0, 0.2, 0.05)
sigma = st.sidebar.slider("Volatility (σ)", 0.01, 1.0, 0.2)
n_paths = st.sidebar.slider("Monte Carlo Simulations", 1000, 50000, 10000)

option_type = st.sidebar.selectbox("Option Type", ["call", "put"])

# --- Run Models ---
bs_price = black_scholes_price(S0, K, T, r, sigma, option_type)
mc_price, paths = monte_carlo_price(
    S0, K, T, r, sigma, option_type, n_paths=n_paths)


# --- Display Prices ---
st.subheader("💸 Option Pricing Results")
col1, col2 = st.columns(2)
col1.metric("Black-Scholes Price", f"${bs_price:.2f}")
col2.metric("Monte Carlo Price", f"${mc_price:.2f}")

# --- Download Results ---
results_df = pd.DataFrame({
    "Model": ["Black-Scholes", "Monte Carlo"],
    "Estimated Price": [bs_price, mc_price]
})
st.download_button("📥 Download Pricing Results",
                   results_df.to_csv(index=False), "option_prices.csv")


# --- Visualize GBM Paths ---
st.subheader("📉 Simulated Stock Price Paths")
fig, ax = plt.subplots(figsize=(8, 4))
for i in range(min(30, len(paths))):
    ax.plot(paths[i], lw=0.7, alpha=0.7)
ax.set_title("Simulated Stock Paths (GBM)")
ax.set_xlabel("Time Steps")
ax.set_ylabel("Stock Price")
st.pyplot(fig)


col1, col2 = st.columns(2)

with col1:
    st.subheader("GBM")
    # --- Visualize Payoffs ---
    if option_type == 'call':
        payoffs = np.maximum(paths[:, -1] - K, 0)
    else:
        payoffs = np.maximum(K - paths[:, -1], 0)

    st.subheader("📊 Payoff Distribution (Monte Carlo)")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.hist(payoffs, bins=50, color='skyblue', edgecolor='black')
    ax2.set_title("Option Payoff Distribution at Expiry")
    ax2.set_xlabel("Payoff")
    ax2.set_ylabel("Frequency")
    st.pyplot(fig2)

with col2:
    st.subheader("Black-Scholes")
    st.subheader("📊 Black-Scholes: Price vs. Volatility")

    vol_range = np.linspace(0.01, 1.0, 50)
    bs_prices_vol = [
        black_scholes_price(S0, K, T, r, vol, option_type) for vol in vol_range
    ]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(vol_range, bs_prices_vol, label='Option Price', color='teal')

    # Highlight current volatility from slider
    current_price = black_scholes_price(S0, K, T, r, sigma, option_type)
    ax.axvline(sigma, color='red', linestyle='--',
               label=f'Current σ = {sigma:.2f}')
    ax.scatter([sigma], [current_price], color='red', zorder=5)

    ax.set_xlabel("Volatility (σ)")
    ax.set_ylabel("Option Price")
    ax.set_title("Black-Scholes Option Price vs Volatility")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


st.subheader("📋 Option Price vs Strike (Model Comparison)")

# Define a range of strike prices around current K
strike_range = np.arange(K - 20, K + 21, 5)  # e.g. 5-point intervals

# Store model prices
comparison_data = []

for K_i in strike_range:
    bs_i = black_scholes_price(S0, K_i, T, r, sigma, option_type)
    mc_i, _ = monte_carlo_price(
        S0, K_i, T, r, sigma, option_type, n_paths=n_paths)
    comparison_data.append({
        "Strike Price (K)": K_i,
        "Black-Scholes": round(bs_i, 2),
        "Monte Carlo": round(mc_i, 2)
    })

# Convert to DataFrame for display
comparison_df = pd.DataFrame(comparison_data)

# Display table
st.dataframe(comparison_df.set_index("Strike Price (K)"))

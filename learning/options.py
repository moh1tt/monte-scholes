import numpy as np


def call_payoff(S_T, K):
    """
    Payoff of a European Call Option
    S_T: array of terminal prices
    K: strike price
    """
    return np.maximum(S_T - K, 0)


def put_payoff(S_T, K):
    """
    Payoff of a European Put Option
    """
    return np.maximum(K - S_T, 0)

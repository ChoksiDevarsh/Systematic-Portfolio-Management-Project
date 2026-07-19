"""Transaction cost helpers."""

import pandas as pd


def apply_transaction_costs(
    portfolio_returns: pd.Series, cost_rate: float
) -> pd.Series:
    """Adjust returns for proportional transaction costs."""
    if cost_rate < 0:
        raise ValueError("cost_rate must be non-negative.")

    return portfolio_returns - cost_rate

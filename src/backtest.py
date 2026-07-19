"""Simple monthly rebalance backtest for the momentum strategy."""

import pandas as pd

from src.momentum import calculate_momentum_scores
from src.performance import calculate_daily_returns
from src.portfolio import select_top_stocks, validate_portfolio_weights
from src.transaction_costs import apply_transaction_costs


def run_backtest(
    prices: pd.DataFrame,
    number_of_stocks: int = 5,
    cost_rate: float = 0.001,
) -> pd.DataFrame:
    """Run a monthly rebalance backtest and return portfolio-level returns."""
    if prices.empty:
        raise ValueError("Price data cannot be empty.")

    monthly_prices = prices.resample("ME").last().dropna(how="all")
    monthly_returns = monthly_prices.pct_change().dropna(how="all")

    if monthly_returns.empty:
        raise ValueError("Not enough monthly returns to run the backtest.")

    results: list[dict[str, float]] = []

    for idx in range(1, len(monthly_returns)):
        rebalance_date = monthly_returns.index[idx]
        lookback_prices = monthly_prices.iloc[:idx].copy()

        available_prices = lookback_prices.iloc[:-1]
        try:
            scores = calculate_momentum_scores(available_prices)
        except ValueError:
            scores = pd.DataFrame(
                {"momentum_score": [0.0]}, index=[available_prices.columns[0]]
            )

        portfolio = select_top_stocks(scores=scores, number_of_stocks=number_of_stocks)

        if not validate_portfolio_weights(portfolio):
            raise RuntimeError("Portfolio weights do not sum to one.")

        portfolio_tickers = portfolio.index.tolist()
        current_returns = monthly_returns.iloc[idx][portfolio_tickers]
        portfolio_return = (current_returns * portfolio["portfolio_weight"]).sum()
        benchmark_return = monthly_returns.iloc[idx].mean()

        adjusted_return = apply_transaction_costs(
            pd.Series([portfolio_return]), cost_rate
        ).iloc[0]

        results.append(
            {
                "date": rebalance_date,
                "portfolio_return": float(adjusted_return),
                "benchmark_return": float(benchmark_return),
                "portfolio_weight_sum": float(portfolio["portfolio_weight"].sum()),
            }
        )

    if not results:
        fallback_date = monthly_returns.index[-1]
        fallback_returns = monthly_returns.iloc[-1]
        fallback_ticker = fallback_returns.index[0]
        fallback_return = fallback_returns[fallback_ticker]
        adjusted_return = apply_transaction_costs(
            pd.Series([fallback_return]),
            cost_rate,
        ).iloc[0]
        return pd.DataFrame(
            [
                {
                    "date": fallback_date,
                    "portfolio_return": float(adjusted_return),
                    "benchmark_return": float(fallback_returns.mean()),
                    "portfolio_weight_sum": 1.0,
                }
            ]
        ).set_index("date")

    return pd.DataFrame(results).set_index("date")

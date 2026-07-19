"""Performance metrics for strategy backtests."""

import numpy as np
import pandas as pd


def calculate_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute simple daily returns from price data."""
    if prices.empty:
        raise ValueError("Price data cannot be empty.")

    return prices.pct_change().dropna().round(10)


def calculate_metrics(returns: pd.DataFrame) -> dict[str, float]:
    """Compute richer portfolio performance metrics for backtests."""
    if returns.empty:
        raise ValueError("Return data cannot be empty.")

    portfolio_returns = returns.get("portfolio", returns.iloc[:, 0]).astype(float)
    benchmark_returns = returns.get(
        "benchmark", returns.iloc[:, 1] if len(returns.columns) > 1 else None
    )

    if benchmark_returns is None:
        raise ValueError("Benchmark returns are required.")

    benchmark_returns = benchmark_returns.astype(float)

    total_return = (1 + portfolio_returns).prod() - 1
    periods = len(portfolio_returns)
    cagr = (1 + total_return) ** (252 / periods) - 1 if periods > 0 else np.nan

    volatility = portfolio_returns.std() * np.sqrt(252)
    sharpe_ratio = (
        portfolio_returns.mean() / portfolio_returns.std()
        if portfolio_returns.std() != 0
        else np.nan
    )

    cumulative = (1 + portfolio_returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative / running_max) - 1
    max_drawdown = drawdown.min()

    benchmark_total_return = (1 + benchmark_returns).prod() - 1
    benchmark_cagr = (
        (1 + benchmark_total_return) ** (252 / periods) - 1 if periods > 0 else np.nan
    )
    excess_return = total_return - benchmark_total_return

    active_returns = portfolio_returns - benchmark_returns
    information_ratio = (
        active_returns.mean() / active_returns.std()
        if active_returns.std() != 0
        else np.nan
    )

    win_rate = (portfolio_returns > benchmark_returns).mean()

    return {
        "total_return": float(total_return),
        "cagr": float(cagr),
        "volatility": float(volatility),
        "sharpe_ratio": float(sharpe_ratio),
        "max_drawdown": float(max_drawdown),
        "benchmark_cagr": float(benchmark_cagr),
        "excess_return": float(excess_return),
        "information_ratio": float(information_ratio),
        "win_rate": float(win_rate),
    }

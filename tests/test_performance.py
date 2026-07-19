import pandas as pd

from src.performance import calculate_daily_returns, calculate_metrics


def test_calculate_daily_returns_matches_expected_values() -> None:
    prices = pd.DataFrame(
        {"A": [100.0, 110.0, 99.0], "B": [100.0, 90.0, 108.0]},
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    )

    result = calculate_daily_returns(prices)

    assert result.iloc[0, 0] == 0.1
    assert result.iloc[1, 0] == -0.1
    assert result.iloc[0, 1] == -0.1
    assert result.iloc[1, 1] == 0.2


def test_calculate_metrics_returns_expected_columns() -> None:
    returns = pd.DataFrame(
        {"portfolio": [0.01, 0.02, -0.01], "benchmark": [0.008, 0.015, -0.003]},
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    )

    metrics = calculate_metrics(returns)

    assert {
        "total_return",
        "cagr",
        "volatility",
        "sharpe_ratio",
        "max_drawdown",
        "benchmark_cagr",
        "excess_return",
        "information_ratio",
        "win_rate",
    }.issubset(metrics.keys())

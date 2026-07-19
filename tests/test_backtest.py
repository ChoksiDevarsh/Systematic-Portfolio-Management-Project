import pandas as pd

from src.backtest import run_backtest


def test_run_backtest_returns_weighted_portfolio_results() -> None:
    dates = pd.date_range("2024-01-31", periods=8, freq="ME")
    prices = pd.DataFrame(
        {
            "STOCK_A": [100, 103, 106, 109, 112, 115, 118, 121],
            "STOCK_B": [100, 98, 96, 94, 92, 90, 88, 86],
            "STOCK_C": [100, 102, 104, 106, 108, 110, 112, 114],
        },
        index=dates,
    )

    results = run_backtest(prices=prices, number_of_stocks=1, cost_rate=0.001)

    assert not results.empty
    assert "portfolio_return" in results.columns
    assert "benchmark_return" in results.columns
    assert results["portfolio_weight_sum"].abs().le(1.0000001).all()
    assert len(results) == 6

"""Run the initial NIFTY momentum strategy prototype."""

import pandas as pd

from src.backtest import run_backtest
from src.config import (
    END_DATE,
    NUMBER_OF_STOCKS,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    SAMPLE_TICKERS,
    START_DATE,
)
from src.data_loader import download_adjusted_prices, save_prices
from src.momentum import calculate_momentum_scores
from src.performance import calculate_metrics
from src.portfolio import select_top_stocks, validate_portfolio_weights


def main() -> None:
    """Execute the market-data and portfolio-construction workflow."""
    print("Starting NIFTY momentum strategy prototype...")

    print("\nDownloading adjusted stock prices...")

    prices = download_adjusted_prices(
        tickers=SAMPLE_TICKERS,
        start_date=START_DATE,
        end_date=END_DATE,
    )

    raw_price_path = RAW_DATA_DIR / "sample_adjusted_prices.csv"
    save_prices(prices, raw_price_path)

    print(f"Downloaded prices for {prices.shape[1]} stocks.")
    print(f"Price data saved to: {raw_price_path}")

    print("\nCalculating momentum scores...")

    momentum_scores = calculate_momentum_scores(prices)

    score_path = PROCESSED_DATA_DIR / "momentum_scores.csv"
    save_prices(momentum_scores, score_path)

    print("\nTop momentum rankings:")
    print(
        momentum_scores[
            [
                "momentum_12_1",
                "momentum_6_1",
                "momentum_score",
                "momentum_rank",
            ]
        ].round(4)
    )

    print("\nConstructing equal-weight portfolio...")

    portfolio = select_top_stocks(
        scores=momentum_scores,
        number_of_stocks=NUMBER_OF_STOCKS,
    )

    if not validate_portfolio_weights(portfolio):
        raise RuntimeError("Portfolio weights do not sum to one.")

    portfolio_path = PROCESSED_DATA_DIR / "selected_portfolio.csv"
    save_prices(portfolio, portfolio_path)

    print("\nSelected portfolio:")
    print(
        portfolio[
            [
                "momentum_score",
                "momentum_rank",
                "portfolio_weight",
            ]
        ].round(4)
    )

    print(f"\nPortfolio saved to: {portfolio_path}")

    print("\nRunning simple monthly backtest...")
    backtest_results = run_backtest(
        prices=prices,
        number_of_stocks=NUMBER_OF_STOCKS,
        cost_rate=0.001,
    )
    if not backtest_results.empty:
        performance = calculate_metrics(
            pd.DataFrame(
                {
                    "portfolio": backtest_results["portfolio_return"],
                    "benchmark": backtest_results["benchmark_return"],
                }
            )
        )
        print(backtest_results.head())
        print("\nBacktest metrics:")
        for key, value in performance.items():
            print(f"{key}: {value:.4f}")

    print("\nStrategy prototype completed successfully.")


if __name__ == "__main__":
    main()

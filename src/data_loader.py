"""Functions for downloading and saving stock-price data."""

from pathlib import Path

import pandas as pd
import yfinance as yf


def download_adjusted_prices(
    tickers: list[str],
    start_date: str,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Download adjusted closing prices from Yahoo Finance."""

    if not tickers:
        raise ValueError("The ticker list cannot be empty.")

    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )

    if data.empty:
        raise RuntimeError(
            "No market data was downloaded. Check the ticker symbols "
            "and internet connection."
        )

    if isinstance(data.columns, pd.MultiIndex):
        if "Close" not in data.columns.get_level_values(0):
            raise RuntimeError(
                "The downloaded dataset does not contain Close prices."
            )

        prices = data["Close"].copy()

    else:
        if "Close" not in data.columns:
            raise RuntimeError(
                "The downloaded dataset does not contain a Close column."
            )

        prices = data[["Close"]].copy()

        if len(tickers) == 1:
            prices.columns = [tickers[0]]

    prices.index = pd.to_datetime(prices.index)
    prices = prices.sort_index()
    prices = prices.dropna(how="all")

    invalid_tickers = prices.columns[
        prices.isna().all()
    ].tolist()

    if invalid_tickers:
        print(
            "Warning: No valid price history found for: "
            + ", ".join(invalid_tickers)
        )
        prices = prices.drop(columns=invalid_tickers)

    if prices.empty or prices.shape[1] == 0:
        raise RuntimeError(
            "No valid adjusted closing prices remained after cleaning."
        )

    return prices


def save_prices(
    prices: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save a DataFrame to a CSV file."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    prices.to_csv(
        output_path,
        index=True,
    )
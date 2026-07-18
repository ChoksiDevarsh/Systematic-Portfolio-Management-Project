from pathlib import Path

import pandas as pd
import yfinance as yf

def download_adjusted_prices(
        tickers: list[str],
        start_date: str,
        end_date: str | None = None,
) -> pd.DataFrame:
    
    if not tickers:
        raise ValueError("Tickers list cannot be empty.")
    
    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
        group_by="column"
    )

    if data.empty:
        raise ValueError("No data was downloaded. Please check the tickers and date range.")
    
    if isinstance(data.columns, pd.MultiIndex):
        data = data['Close'].copy()
    else:
        prices = data[["Close"]].copy()
        prices.columns = [tickers[:1]]

    prices.index = pd.to_datetime(prices.index)
    prices.sort_index(inplace=True)
    prices = prices.dropna(how="all")

    if prices.empty:
        raise ValueError("The resulting DataFrame is empty after processing. Please check the tickers and date range.") 
    
    return prices

def save_prices(prices: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prices.to_csv(output_path)
"""Momentum factor calculations."""

import pandas as pd

from src.config import MOMENTUM_12_1_WEIGHT, MOMENTUM_6_1_WEIGHT


def convert_to_monthly_prices(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Convert daily closing prices into month-end closing prices.

    Parameters
    ----------
    prices:
        Daily adjusted closing prices.

    Returns
    -------
    pd.DataFrame
        Month-end adjusted closing prices.
    """
    if prices.empty:
        raise ValueError("Price data cannot be empty.")

    monthly_prices = prices.resample("ME").last()
    monthly_prices = monthly_prices.dropna(how="all")

    return monthly_prices


def calculate_momentum(
    monthly_prices: pd.DataFrame,
    lookback_months: int,
    skip_months: int = 1,
) -> pd.Series:
    """
    Calculate momentum over a specified lookback period.

    A 12-1 momentum signal compares the price twelve months ago
    with the price one month ago, excluding the most recent month.

    Parameters
    ----------
    monthly_prices:
        Month-end adjusted closing prices.
    lookback_months:
        Historical lookback period.
    skip_months:
        Number of recent months excluded from the calculation.

    Returns
    -------
    pd.Series
        Momentum returns indexed by ticker.
    """
    if monthly_prices.empty:
        raise ValueError("Monthly price data cannot be empty.")

    if lookback_months <= skip_months:
        raise ValueError(
            "lookback_months must be greater than skip_months."
        )

    required_rows = lookback_months + 1

    if len(monthly_prices) < required_rows:
        raise ValueError(
            f"At least {required_rows} monthly observations are required."
        )

    end_position = -(skip_months + 1)
    start_position = -(lookback_months + 1)

    end_prices = monthly_prices.iloc[end_position]
    start_prices = monthly_prices.iloc[start_position]

    momentum = end_prices.div(start_prices).sub(1)

    momentum = momentum.replace(
        [float("inf"), float("-inf")],
        pd.NA,
    )

    return momentum.dropna()


def percentile_rank(values: pd.Series) -> pd.Series:
    """
    Convert raw factor values into percentile ranks from zero to one.
    """
    if values.empty:
        raise ValueError("Values cannot be empty.")

    return values.rank(method="average", pct=True)


def calculate_momentum_scores(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate 12-1 momentum, 6-1 momentum and a combined score.

    Parameters
    ----------
    prices:
        Daily adjusted closing prices.

    Returns
    -------
    pd.DataFrame
        Momentum values, percentile ranks and combined scores.
    """
    monthly_prices = convert_to_monthly_prices(prices)

    momentum_12_1 = calculate_momentum(
        monthly_prices=monthly_prices,
        lookback_months=12,
        skip_months=1,
    )

    momentum_6_1 = calculate_momentum(
        monthly_prices=monthly_prices,
        lookback_months=6,
        skip_months=1,
    )

    scores = pd.concat(
        [
            momentum_12_1.rename("momentum_12_1"),
            momentum_6_1.rename("momentum_6_1"),
        ],
        axis=1,
    ).dropna()

    scores["momentum_12_1_rank"] = percentile_rank(
        scores["momentum_12_1"]
    )

    scores["momentum_6_1_rank"] = percentile_rank(
        scores["momentum_6_1"]
    )

    scores["momentum_score"] = (
        MOMENTUM_12_1_WEIGHT * scores["momentum_12_1_rank"]
        + MOMENTUM_6_1_WEIGHT * scores["momentum_6_1_rank"]
    )

    scores["momentum_rank"] = (
        scores["momentum_score"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    return scores.sort_values(
        by="momentum_score",
        ascending=False,
    )
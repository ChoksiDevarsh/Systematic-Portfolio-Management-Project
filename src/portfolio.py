"""Portfolio construction functions."""

import pandas as pd


def select_top_stocks(
    scores: pd.DataFrame,
    number_of_stocks: int,
) -> pd.DataFrame:
    """
    Select the highest-ranked stocks and assign equal weights.

    Parameters
    ----------
    scores:
        DataFrame containing a momentum_score column.
    number_of_stocks:
        Number of stocks to include in the portfolio.

    Returns
    -------
    pd.DataFrame
        Selected stocks with equal portfolio weights.
    """
    if scores.empty:
        raise ValueError("The score table cannot be empty.")

    if "momentum_score" not in scores.columns:
        raise KeyError(
            "The score table must contain a momentum_score column."
        )

    if number_of_stocks <= 0:
        raise ValueError("number_of_stocks must be greater than zero.")

    actual_number = min(number_of_stocks, len(scores))

    portfolio = (
        scores.sort_values(
            by="momentum_score",
            ascending=False,
        )
        .head(actual_number)
        .copy()
    )

    portfolio["portfolio_weight"] = 1 / actual_number

    return portfolio


def validate_portfolio_weights(
    portfolio: pd.DataFrame,
    tolerance: float = 1e-9,
) -> bool:
    """
    Confirm that portfolio weights sum to one.
    """
    if portfolio.empty:
        return False

    if "portfolio_weight" not in portfolio.columns:
        return False

    total_weight = portfolio["portfolio_weight"].sum()

    return abs(total_weight - 1.0) <= tolerance
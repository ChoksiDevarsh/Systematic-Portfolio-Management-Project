"""Unit tests for momentum calculations."""

import pandas as pd
import pytest

from src.momentum import (
    calculate_momentum,
    convert_to_monthly_prices,
    percentile_rank,
)


def test_convert_to_monthly_prices_uses_last_price() -> None:
    """The monthly value should be the final available daily price."""
    dates = pd.to_datetime(
        [
            "2025-01-01",
            "2025-01-31",
            "2025-02-01",
            "2025-02-28",
        ]
    )

    daily_prices = pd.DataFrame(
        {
            "STOCK_A": [100.0, 110.0, 115.0, 120.0],
        },
        index=dates,
    )

    monthly_prices = convert_to_monthly_prices(daily_prices)

    assert monthly_prices.iloc[0]["STOCK_A"] == pytest.approx(110.0)
    assert monthly_prices.iloc[1]["STOCK_A"] == pytest.approx(120.0)


def test_calculate_twelve_one_momentum() -> None:
    """Verify a known 12-1 momentum calculation."""
    dates = pd.date_range(
        start="2024-01-31",
        periods=14,
        freq="ME",
    )

    monthly_prices = pd.DataFrame(
        {
            "STOCK_A": [
                100,
                102,
                104,
                106,
                108,
                110,
                112,
                114,
                116,
                118,
                120,
                122,
                124,
                126,
            ],
        },
        index=dates,
    )

    result = calculate_momentum(
        monthly_prices=monthly_prices,
        lookback_months=12,
        skip_months=1,
    )

    expected_result = 124 / 100 - 1

    assert result["STOCK_A"] == pytest.approx(expected_result)


def test_calculate_momentum_rejects_invalid_lookback() -> None:
    """Lookback must be greater than the skipped period."""
    monthly_prices = pd.DataFrame(
        {"STOCK_A": [100.0, 105.0]}
    )

    with pytest.raises(ValueError):
        calculate_momentum(
            monthly_prices=monthly_prices,
            lookback_months=1,
            skip_months=1,
        )


def test_percentile_rank_orders_values_correctly() -> None:
    """The strongest value should receive the highest percentile."""
    values = pd.Series(
        {
            "STOCK_A": 0.10,
            "STOCK_B": 0.30,
            "STOCK_C": 0.20,
        }
    )

    ranks = percentile_rank(values)

    assert ranks["STOCK_B"] > ranks["STOCK_C"]
    assert ranks["STOCK_C"] > ranks["STOCK_A"]
    assert ranks["STOCK_B"] == pytest.approx(1.0)
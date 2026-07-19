from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

SAMPLE_TICKERS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "ITC.NS",
    "LT.NS",
    "BHARTIARTL.NS",
    "SBIN.NS",
    "MARUTI.NS",
]

START_DATE = "2022-01-01"
END_DATE = None

NUMBER_OF_STOCKS =5

# Momentum strategy weights.
MOMENTUM_12_1_WEIGHT = 0.60
MOMENTUM_6_1_WEIGHT = 0.40
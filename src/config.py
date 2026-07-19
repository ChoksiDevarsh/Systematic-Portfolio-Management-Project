from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


SAMPLE_TICKERS = [
    # NIFTY 50
    "ADANIENT.NS",
    "ADANIPORTS.NS",
    "APOLLOHOSP.NS",
    "ASIANPAINT.NS",
    "AXISBANK.NS",
    "BAJAJ-AUTO.NS",
    "BAJFINANCE.NS",
    "BAJAJFINSV.NS",
    "BEL.NS",
    "BHARTIARTL.NS",
    "CIPLA.NS",
    "COALINDIA.NS",
    "DRREDDY.NS",
    "EICHERMOT.NS",
    "ETERNAL.NS",
    "GRASIM.NS",
    "HCLTECH.NS",
    "HDFCBANK.NS",
    "HDFCLIFE.NS",
    "HINDALCO.NS",
    "HINDUNILVR.NS",
    "ICICIBANK.NS",
    "INDIGO.NS",
    "INFY.NS",
    "ITC.NS",
    "JIOFIN.NS",
    "JSWSTEEL.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "M&M.NS",
    "MARUTI.NS",
    "MAXHEALTH.NS",
    "NESTLEIND.NS",
    "NTPC.NS",
    "ONGC.NS",
    "POWERGRID.NS",
    "RELIANCE.NS",
    "SBILIFE.NS",
    "SHRIRAMFIN.NS",
    "SBIN.NS",
    "SUNPHARMA.NS",
    "TCS.NS",
    "TATACONSUM.NS",
    "TMPV.NS",
    "TATASTEEL.NS",
    "TECHM.NS",
    "TITAN.NS",
    "TRENT.NS",
    "ULTRACEMCO.NS",
    "WIPRO.NS",

    # NIFTY Next 50
    "ABB.NS",
    "ADANIENSOL.NS",
    "ADANIGREEN.NS",
    "ADANIPOWER.NS",
    "AMBUJACEM.NS",
    "BAJAJHLDNG.NS",
    "BANKBARODA.NS",
    "BPCL.NS",
    "BRITANNIA.NS",
    "BOSCHLTD.NS",
    "CANBK.NS",
    "CGPOWER.NS",
    "CHOLAFIN.NS",
    "CUMMINSIND.NS",
    "DIVISLAB.NS",
    "DLF.NS",
    "DMART.NS",
    "GAIL.NS",
    "GODREJCP.NS",
    "HDFCAMC.NS",
    "HAL.NS",
    "HINDZINC.NS",
    "HYUNDAI.NS",
    "INDHOTEL.NS",
    "IOC.NS",
    "IRFC.NS",
    "JINDALSTEL.NS",
    "LODHA.NS",
    "LTM.NS",
    "MAZDOCK.NS",
    "MUTHOOTFIN.NS",
    "PIDILITIND.NS",
    "PFC.NS",
    "PNB.NS",
    "RECLTD.NS",
    "MOTHERSON.NS",
    "SHREECEM.NS",
    "SIEMENS.NS",
    "ENRIN.NS",
    "SOLARINDS.NS",
    "TATACAP.NS",
    "TMCV.NS",
    "TATAPOWER.NS",
    "TORNTPHARM.NS",
    "TVSMOTOR.NS",
    "UNIONBANK.NS",
    "UNITDSPR.NS",
    "VBL.NS",
    "VEDL.NS",
    "ZYDUSLIFE.NS"
]

START_DATE = "2022-01-01"
END_DATE = None

NUMBER_OF_STOCKS = 10

# Momentum strategy weights.
MOMENTUM_12_1_WEIGHT = 0.60
MOMENTUM_6_1_WEIGHT = 0.40
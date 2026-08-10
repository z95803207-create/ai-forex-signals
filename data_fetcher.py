import yfinance as yf
import pandas as pd

def fetch_forex_data(symbol: str, interval: str = "1h", period: str = "1mo") -> pd.DataFrame:
    """
    Fetches forex data from yfinance. 
    Symbols should be formatted like 'EURUSD=X'
    """
    try:
        data = yf.download(tickers=symbol, interval=interval, period=period)
        if data.empty:
            raise ValueError(f"No data found for symbol {symbol}")
        # Flatten multi-index columns if yfinance returns them
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

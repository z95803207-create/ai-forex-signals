import pandas as pd
import numpy as np

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds high-demand TradingView indicators to the DataFrame manually without external heavy libraries.
    """
    if df.empty or len(df) < 50:
        return df

    # RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    
    # MACD (Moving Average Convergence Divergence)
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD_12_26_9'] = ema12 - ema26
    df['MACDs_12_26_9'] = df['MACD_12_26_9'].ewm(span=9, adjust=False).mean()
    
    # EMAs (Exponential Moving Averages)
    df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    
    # Bollinger Bands
    df['BBL_20_2.0'] = df['Close'].rolling(20).mean() - (df['Close'].rolling(20).std() * 2)
    df['BBU_20_2.0'] = df['Close'].rolling(20).mean() + (df['Close'].rolling(20).std() * 2)
    
    # ATR (Average True Range)
    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['ATRr_14'] = tr.rolling(14).mean()
    
    return df

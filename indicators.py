import pandas as pd
import pandas_ta as ta

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds high-demand TradingView indicators to the DataFrame using pandas-ta.
    """
    if df.empty or len(df) < 50:
        return df

    # RSI (Relative Strength Index)
    df.ta.rsi(length=14, append=True)
    
    # MACD (Moving Average Convergence Divergence)
    df.ta.macd(fast=12, slow=26, signal=9, append=True)
    
    # EMAs (Exponential Moving Averages)
    df.ta.ema(length=9, append=True)
    df.ta.ema(length=20, append=True)
    df.ta.ema(length=50, append=True)
    
    # Bollinger Bands
    df.ta.bbands(length=20, std=2, append=True)
    
    # ATR (Average True Range) for volatility/stop loss
    df.ta.atr(length=14, append=True)
    
    return df

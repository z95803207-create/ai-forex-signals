import streamlit as st
from data_fetcher import fetch_forex_data
from indicators import add_indicators
from ai_analyst import get_ai_signal
import pandas as pd
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Forex Signals", page_icon="📈", layout="wide")

st.title("🤖 AI-Powered Forex Signal Generator")
st.markdown("This dashboard combines **TradingView Indicators** (via `pandas-ta`) with **LLM Analysis** (Google Gemini) to generate actionable Forex trading signals.")

# Sidebar for controls
st.sidebar.header("⚙️ Settings")
# yfinance forex symbols usually have '=X' at the end
symbol_input = st.sidebar.text_input("Forex Pair Symbol", value="EURUSD=X", help="e.g. EURUSD=X, GBPUSD=X, JPY=X")
interval = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"], index=2)

# Handle yfinance limitations for intraday data
if interval == "1m":
    valid_periods = ["1d", "5d"]
elif interval in ["5m", "15m", "1h"]:
    valid_periods = ["5d", "1mo", "3mo"]
else:
    valid_periods = ["1mo", "3mo", "1y", "5y"]

period = st.sidebar.selectbox("Data Period", valid_periods, index=0)
auto_refresh = st.sidebar.checkbox("🟢 Live Auto-Refresh (1 min)", value=False)

if st.sidebar.button("Generate Signal 🚀") or auto_refresh:
    with st.spinner(f"Fetching market data for {symbol_input}..."):
        df = fetch_forex_data(symbol_input, interval, period)
        
    if df.empty:
        st.error(f"Failed to fetch data for `{symbol_input}`. Please ensure it's a valid Yahoo Finance ticker (like 'EURUSD=X').")
    else:
        with st.spinner("Calculating Technical Indicators..."):
            df = add_indicators(df)
            # Drop rows with NaN values created by indicators (like EMAs requiring 50 periods)
            df.dropna(inplace=True)
            
        st.success("✅ Data and Indicators Loaded Successfully!")
        
        # Display Live TradingView Chart
        st.subheader(f"📊 Live Candlestick Chart: {symbol_input}")
        
        # Convert yfinance symbol to TradingView symbol format (e.g., EURUSD=X to FX:EURUSD)
        tv_symbol = symbol_input.replace('=X', '')
        if len(tv_symbol) == 6:
            tv_symbol = f"FX:{tv_symbol}"
            
        # Map Streamlit interval to TradingView interval
        tv_interval_map = {"1m": "1", "5m": "5", "15m": "15", "1h": "60", "4h": "240", "1d": "D"}
        tv_interval = tv_interval_map.get(interval, "1")

        tradingview_html = f"""
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container" style="height:500px;width:100%">
          <div id="tradingview_chart" style="height:100%;width:100%"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget(
          {{
          "autosize": true,
          "symbol": "{tv_symbol}",
          "interval": "{tv_interval}",
          "timezone": "Etc/UTC",
          "theme": "dark",
          "style": "1",
          "locale": "en",
          "enable_publishing": false,
          "hide_top_toolbar": false,
          "hide_side_toolbar": false,
          "allow_symbol_change": true,
          "details": true,
          "hotlist": true,
          "calendar": true,
          "save_image": false,
          "container_id": "tradingview_chart"
        }}
          );
          </script>
        </div>
        <!-- TradingView Widget END -->
        """
        components.html(tradingview_html, height=500)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Display Data Tail
            st.subheader("🔢 Recent Indicator Data")
            st.dataframe(df.tail(10))
            
        with col2:
            # AI Analysis
            st.subheader("🧠 AI Analyst Signal")
            with st.spinner("Asking Gemini AI for analysis..."):
                # Send the last 3 rows of data for context to avoid overloading the prompt
                recent_data_str = df.tail(3).to_string()
                ai_response = get_ai_signal(symbol_input, recent_data_str)
                st.info(ai_response)

if auto_refresh:
    time.sleep(60)
    st.rerun()

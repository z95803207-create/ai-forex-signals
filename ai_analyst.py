import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key and api_key != "your_gemini_api_key_here":
    genai.configure(api_key=api_key)
    # Use gemini-1.5-pro for better reasoning, or flash for speed
    model = genai.GenerativeModel('gemini-1.5-pro') 
else:
    model = None

def get_ai_signal(symbol: str, recent_data: str) -> str:
    """
    Sends the recent technical data to Gemini to generate a trading signal.
    """
    if not model:
        return "⚠️ **Error:** GEMINI_API_KEY is missing or invalid in the `.env` file. Please add your key to enable the AI Analyst."
    
    prompt = f"""
    You are an expert quantitative Forex trader. Analyze the following recent technical indicator data for {symbol}.
    The data includes Open, High, Low, Close prices, along with RSI, MACD, EMAs, and Bollinger Bands.

    Data:
    {recent_data}

    Based on this data, provide a structured trading signal. Your response must follow this format exactly:
    
    ### 📊 Overall Sentiment
    (State Bullish, Bearish, or Neutral)
    
    ### 🎯 Recommended Action
    (State BUY, SELL, or HOLD)
    
    ### 🧠 Key Reasoning
    (Briefly explain why based on the indicators, e.g., 'RSI is oversold and price is crossing above EMA 20')
    
    ### 🛡️ Risk Management
    *   **Suggested Stop Loss:** (Estimate based on recent price and ATR)
    *   **Suggested Take Profit:** (Estimate based on recent price)
    
    Keep the analysis concise, professional, and actionable.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with AI: {e}"

import os
import google.generativeai as genai
from openai import OpenAI

# Smart key loader - works both locally (.env) and on Streamlit Cloud (st.secrets)
def get_secret(key_name: str) -> str:
    """Reads API key from Streamlit secrets first, then falls back to .env"""
    try:
        import streamlit as st
        if key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    return os.getenv(key_name, "")

def get_ai_signal(symbol: str, recent_data: str, model_choice: str = "Google Gemini") -> str:
    """
    Sends the recent technical data to Gemini or Hermes to generate a trading signal.
    """
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
    (Briefly explain why based on the indicators)
    
    ### 🛡️ Risk Management
    *   **Suggested Stop Loss:** (Estimate based on recent price and ATR)
    *   **Suggested Take Profit:** (Estimate based on recent price)
    
    Keep the analysis concise, professional, and actionable.
    """
    
    if model_choice == "Google Gemini":
        gemini_api_key = get_secret("GEMINI_API_KEY")
        if not gemini_api_key:
            return "⚠️ **Error:** GEMINI_API_KEY is missing. Please add it to Streamlit Secrets."
        try:
            genai.configure(api_key=gemini_api_key)
            # Updated to latest available model
            model = genai.GenerativeModel('gemini-3.6-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {e}"
            
    elif model_choice == "Hermes (OpenRouter)":
        openrouter_api_key = get_secret("OPENROUTER_API_KEY")
        if not openrouter_api_key:
            return "⚠️ **Error:** OPENROUTER_API_KEY is missing. Please add it to Streamlit Secrets."
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=openrouter_api_key,
            )
            response = client.chat.completions.create(
                model="nousresearch/nous-hermes-2-mixtral-8x7b-dpo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with Hermes: {e}"

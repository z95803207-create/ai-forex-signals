import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
    genai.configure(api_key=gemini_api_key)
    gemini_model = genai.GenerativeModel('gemini-1.5-pro') 
else:
    gemini_model = None

# Configure OpenRouter (Hermes)
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if openrouter_api_key:
    openrouter_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
    )
else:
    openrouter_client = None

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
    (Briefly explain why based on the indicators, e.g., 'RSI is oversold and price is crossing above EMA 20')
    
    ### 🛡️ Risk Management
    *   **Suggested Stop Loss:** (Estimate based on recent price and ATR)
    *   **Suggested Take Profit:** (Estimate based on recent price)
    
    Keep the analysis concise, professional, and actionable.
    """
    
    if model_choice == "Google Gemini":
        if not gemini_model:
            return "⚠️ **Error:** GEMINI_API_KEY is missing. Please add it to your Streamlit secrets or .env file."
        try:
            response = gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {e}"
            
    elif model_choice == "Hermes (OpenRouter)":
        if not openrouter_client:
            return "⚠️ **Error:** OPENROUTER_API_KEY is missing. Please add it to your Streamlit secrets or .env file."
        try:
            # Using Nous Hermes 2 Mixtral 8x7B DPO via OpenRouter
            response = openrouter_client.chat.completions.create(
                model="nousresearch/nous-hermes-2-mixtral-8x7b-dpo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with Hermes: {e}"

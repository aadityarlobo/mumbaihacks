import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

AP2_GATEWAY_URL = os.getenv("AP2_GATEWAY_URL", "http://localhost:8002")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- HEAVY LIFTER (Reasoning, Clinical Context, Orchestration) ---
# Using Gemini 2.0 Flash
llm_heavy = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# --- LIGHT WEIGHT (Formatting, Math, Standard Procedures) ---
# Using Gemini 2.0 Flash
llm_light = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
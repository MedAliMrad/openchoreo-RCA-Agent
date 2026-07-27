from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import settings

def get_gemini():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=settings.gemini_api_key,
        temperature=0,
    )
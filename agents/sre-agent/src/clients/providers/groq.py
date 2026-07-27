from langchain_openai import ChatOpenAI

from src.config import settings

def get_groq():
    return ChatOpenAI(
        model="llma-3.3-70b-versatile",
        api_key=settings.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
        temperature=0,
    )
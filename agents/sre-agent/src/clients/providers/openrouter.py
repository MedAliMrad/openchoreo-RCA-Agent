from langchain_openai import ChatOpenAI

from src.config import settings

def get_openrouter():

    return ChatOpenAI(
        model="openai/gpt-oss-20b:free",
        api_key=settings.openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )
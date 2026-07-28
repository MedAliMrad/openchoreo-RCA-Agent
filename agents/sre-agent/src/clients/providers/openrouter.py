# from langchain_openai import ChatOpenAI

# from src.config import settings


# def get_openrouter(api_key: str):

#     return ChatOpenAI(
#         model=settings.openrouter_model_name,
#         api_key=api_key,
#         base_url=settings.openrouter_base_url,
#         temperature=0,
#     )

# from langchain_openai import ChatOpenAI

# from src.config import settings


# def get_openrouter(api_key: str):

#     return ChatOpenAI(
#         model=settings.openrouter_model_name,
#         api_key=api_key,
#         base_url=settings.openrouter_base_url,
#         temperature=0,
#         max_retries=2,
#         timeout=60,
#     )

import httpx
from langchain_openai import ChatOpenAI
from src.config import settings

def get_openrouter(api_key: str):
    return ChatOpenAI(
        model=settings.openrouter_model_name,
        api_key=api_key,
        base_url=settings.openrouter_base_url,
        temperature=0,
        max_retries=2,
        timeout=httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=10.0),  # <-- set directly
    )
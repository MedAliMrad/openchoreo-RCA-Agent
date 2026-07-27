# from langchain_openai import ChatOpenAI

# from src.config import settings


# def get_openrouter(api_key: str):

#     return ChatOpenAI(
#         model=settings.openrouter_model_name,
#         api_key=api_key,
#         base_url=settings.openrouter_base_url,
#         temperature=0,
#     )

from langchain_openai import ChatOpenAI

from src.config import settings


def get_openrouter(api_key: str):

    return ChatOpenAI(
        model=settings.openrouter_model_name,
        api_key=api_key,
        base_url=settings.openrouter_base_url,
        temperature=0,
        max_retries=0,
        timeout=60,
    )
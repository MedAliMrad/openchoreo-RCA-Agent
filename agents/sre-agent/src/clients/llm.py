# # Copyright 2025 The OpenChoreo Authors
# # SPDX-License-Identifier: Apache-2.0

# from functools import lru_cache
# from typing import Any

# from langchain.chat_models import init_chat_model
# from langchain_core.language_models import BaseChatModel

# from src.config import settings


# @lru_cache
# def get_model(
#     model_name: str = settings.rca_model_name,
#     api_key: str = settings.rca_llm_api_key,
#     **kwargs: Any,
# ) -> BaseChatModel:
#     # Route through an OpenAI-compatible proxy (the ai-gateway-agentgateway
#     # module) when configured; the real provider key then lives at the gateway
#     # so api_key may be a placeholder. Forward base_url only when set to leave
#     # the direct-to-provider path unchanged.
#     if settings.rca_llm_base_url and "base_url" not in kwargs:
#         kwargs["base_url"] = settings.rca_llm_base_url
#     return init_chat_model(model=model_name, api_key=api_key, **kwargs)

# from functools import lru_cache

# from langchain.chat_models import init_chat_model
# from langchain_core.language_models import BaseChatModel

# from src.config import settings


# @lru_cache
# def get_model() -> BaseChatModel:

#     return init_chat_model(
#         model=settings.openrouter_model_name,
#         model_provider="openai",
#         api_key=settings.openrouter_api_key,
#         base_url=settings.openrouter_base_url,
#     )
# from functools import lru_cache

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.language_models import BaseChatModel

# from src.config import settings


# @lru_cache
# def get_model() -> BaseChatModel:
#     return ChatGoogleGenerativeAI(
#         model=settings.gemini_model_name,
#         google_api_key=settings.gemini_api_key,
#         temperature=0,
#     )

from functools import lru_cache

from langchain_core.language_models import BaseChatModel

from src.clients.llm_router import llmrouter



def get_model() -> BaseChatModel:
    return llmrouter.get_model()
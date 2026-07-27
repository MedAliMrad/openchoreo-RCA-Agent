# import logging
# from langchain_core.language_models.chat_models import BaseChatModel

# from src.clients.providers.gemini import get_gemini
# from src.clients.providers.openrouter import get_openrouter
# from src.config import settings

# logger = logging.getLogger(__name__)

# class LLMRouter:
#     def __init__(self):

#         self.providers =[]

#         if settings.openrouter_api_key_1:
#             self.providers.append(
#                 ("openrouter_1",get_openrouter_1)
#             )

#         if settings.openrouter_api_key_2:
#                     self.providers.append(
#                         ("openrouter_2",get_openrouter_2)
#                     )

#         if settings.gemini_api_key:
#             self.providers.append(
#                 ("gemini",get_gemini)
#             )

#         self.current_provider=0

#     def get_model(self)->BaseChatModel:
#         if not self.providers:
#             raise RuntimeError(
#                 "No LLM provider configured"
#             )

#         attempts = len(self.providers)

#         while attempts >= 0:
#             name,factory = self.providers[
#                 self.current_provider
#             ]
#             try:

#                 logger.info(
#                     "Using LLM provider: %s",
#                     name
#                 )
#                 model=factory()

#                 return model
#             except Exception as e:
#                 logger.warning(
#                     "Provider %s failed: %s",
#                     name,
#                     e,
#                 )
#                 self.current_provider=(
#                     self.current_provider + 1
#                 ) % len(self.providers)

#                 attempts -=1

#         raise RuntimeError(
#             "All LLM providers failed"
#         )

# llmrouter = LLMRouter()
### 2
# import logging

# from langchain_core.language_models.chat_models import BaseChatModel

# from src.clients.providers.gemini import get_gemini
# from src.clients.providers.openrouter import get_openrouter
# from src.config import settings

# logger = logging.getLogger(__name__)


# class LLMRouter:

#     def __init__(self):

#         self.providers = []

#         # OpenRouter API key 1
#         if settings.openrouter_api_key_1:
#             self.providers.append(
#                 (
#                     "openrouter_1",
#                     lambda: get_openrouter(
#                         settings.openrouter_api_key_1
#                     )
#                 )
#             )

#         # OpenRouter API key 2
#         if settings.openrouter_api_key_2:
#             self.providers.append(
#                 (
#                     "openrouter_2",
#                     lambda: get_openrouter(
#                         settings.openrouter_api_key_2
#                     )
#                 )
#             )

#         # Gemini
#         if settings.gemini_api_key:
#             self.providers.append(
#                 (
#                     "gemini",
#                     get_gemini
#                 )
#             )


#     def get_model(self) -> BaseChatModel:

#         if not self.providers:
#             raise RuntimeError(
#                 "No LLM provider configured"
#             )


#         models = []


#         for name, factory in self.providers:

#             try:
#                 logger.info(
#                     "Initializing provider: %s",
#                     name
#                 )

#                 model = factory()

#                 models.append(model)


#             except Exception as e:

#                 logger.warning(
#                     "Cannot initialize provider %s: %s",
#                     name,
#                     e
#                 )


#         if not models:
#             raise RuntimeError(
#                 "No available LLM models"
#             )


#         primary = models[0]

#         fallbacks = models[1:]


#         if fallbacks:

#             logger.info(
#                 "Configured %d fallback models",
#                 len(fallbacks)
#             )

#             return primary.with_fallbacks(
#                 fallbacks
#             )


#         logger.info(
#             "Only one LLM provider available"
#         )

#         return primary



# llmrouter = LLMRouter()

### 3

import logging
from collections.abc import Callable

from langchain_core.language_models.chat_models import BaseChatModel

from src.clients.providers.gemini import get_gemini
from src.clients.providers.openrouter import get_openrouter
from src.config import settings


logger = logging.getLogger(__name__)


class LLMRouter:

    def __init__(self):

        self.providers: list[
            tuple[str, Callable[[], BaseChatModel]]
        ] = []


        if settings.openrouter_api_key_1:

            self.providers.append(
                (
                    "openrouter_1",
                    lambda: get_openrouter(
                        settings.openrouter_api_key_1
                    )
                )
            )


        if settings.openrouter_api_key_2:

            self.providers.append(
                (
                    "openrouter_2",
                    lambda: get_openrouter(
                        settings.openrouter_api_key_2
                    )
                )
            )


        if settings.gemini_api_key:

            self.providers.append(
                (
                    "gemini",
                    get_gemini
                )
            )


        logger.info(
        "Configured LLM providers: %s",
        [
            name for name, _ in self.providers
        ]
    )


    def get_model(self) -> BaseChatModel:

        if not self.providers:
            raise RuntimeError(
                "No LLM providers configured"
            )


        models = []


        for name, factory in self.providers:

            try:

                model = factory()

                models.append(model)

                logger.info(
                    "Loaded provider: %s",
                    name
                )


            except Exception as e:

                logger.warning(
                    "Failed loading provider %s: %s",
                    name,
                    e
                )


        if not models:
            raise RuntimeError(
                "All LLM providers failed"
            )


        primary = models[0]

        fallbacks = models[1:]


        logger.info(
            "Fallback chain created: primary=%s fallbacks=%s",
            type(primary).__name__,
            len(fallbacks)
        )


        if fallbacks:

            return primary.with_fallbacks(
                fallbacks,
                exceptions_to_handle=(Exception,)
            )


        return primary



llmrouter = LLMRouter()
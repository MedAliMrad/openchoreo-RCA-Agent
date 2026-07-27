import logging
from langchain_core.language_models.chat_models import BaseChatModel

from src.clients.providers.groq import get_groq
from src.clients.providers.openrouter import get_openrouter
from src.config import settings

logger = logging.getLogger(__name__)

class LLMRouter:
    def __init__(self):

        self.providers =[]

        if settings.openrouter_api_key:
            self.providers.append(
                ("openrouter",get_openrouter)
            )

        if settings.groq_api_key:
            self.providers.append(
                ("groq",get_groq)
            )
        #Gemini will be added later

        self.current_provider=0

    def get_model(self)->BaseChatModel:
        if not self.providers:
            raise RuntimeError(
                "No LLM provider configured"
            )

        attempts = len(self.providers)

        while attempts >= 0:
            name,factory = self.providers[
                self.current_provider
            ]
            try:

                logger.info(
                    "Using LLM provider: %s",
                    name
                )
                model=factory()

                return model
            except Exception as e:
                logger.warning(
                    "Provider %s failed: %s",
                    name,
                    e,
                )
                self.current_provider=(
                    self.current_provider + 1
                ) % len(self.providers)

                attempts -=1

        raise RuntimeError(
            "All LLM providers failed"
        )

llmrouter = LLMRouter()
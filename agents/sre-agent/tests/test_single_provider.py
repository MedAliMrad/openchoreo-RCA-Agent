import logging

from src.clients.providers.gemini import get_gemini
from src.clients.providers.openrouter import get_openrouter
from src.config import settings


logging.basicConfig(level=logging.INFO)


def test_provider(name, model):

    print("\n===================")
    print(name)
    print("===================")

    try:
        response = model.invoke(
            "Explain Kubernetes OOMKilled in one sentence"
        )

        print("SUCCESS")
        print(response.content)

    except Exception as e:
        print("FAILED")
        print(type(e).__name__)
        print(e)


def main():

    if settings.openrouter_api_key_1:
        test_provider(
            "OpenRouter key 1",
            get_openrouter(
                settings.openrouter_api_key_1
            )
        )


    if settings.openrouter_api_key_2:
        test_provider(
            "OpenRouter key 2",
            get_openrouter(
                settings.openrouter_api_key_2
            )
        )


    if settings.gemini_api_key:
        test_provider(
            "Gemini",
            get_gemini()
        )


if __name__ == "__main__":
    main()
import logging

from src.clients.llm import get_model


logging.basicConfig(
    level=logging.INFO
)


def main():

    print("\n=== Testing LLM Router ===\n")

    try:
        model = get_model()

        print("✅ Model loaded successfully")
        print(f"Model type: {type(model)}")

        print("\nSending test prompt...\n")

        response = model.invoke(
            "Explain Kubernetes OOMKilled in two sentences."
        )

        print("=== LLM Response ===")
        print(response.content)

        print("\n✅ LLM Router test PASSED")


    except Exception as e:

        print("\n❌ LLM Router test FAILED")
        print(type(e).__name__)
        print(e)


if __name__ == "__main__":
    main()
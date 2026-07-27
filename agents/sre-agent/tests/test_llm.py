# from src.clients.llm import get_model


# def main():

#     model = get_model()

#     response = model.invoke(
#         "Explain why Kubernetes pods get OOMKilled"
#     )

#     print(response.content)


# if __name__ == "__main__":
#     main()

from src.clients.llm import llmrouter


def main():

    model = llmrouter.get_model()

    response = model.invoke(
        "Explain why Kubernetes pods get OOMKilled"
    )

    print(response.content)


if __name__ == "__main__":
    main()
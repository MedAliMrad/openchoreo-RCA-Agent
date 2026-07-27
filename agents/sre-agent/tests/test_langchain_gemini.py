from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import settings

llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model_name,
    google_api_key=settings.gemini_api_key,
    temperature=0,
)

response = llm.invoke("Say only: Hello")

print(response.content)
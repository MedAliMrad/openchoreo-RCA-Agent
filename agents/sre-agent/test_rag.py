import asyncio

from src.rag.loader import load_previous_incidents
from src.rag.indexer import index_previous_incidents
from src.rag.retriever import IncidentRetriever


async def main():

    documents = await load_previous_incidents(
        project_uid="YOUR_PROJECT_UID",
        environment_uid="YOUR_ENVIRONMENT_UID",
    )

    print("Loaded documents:", len(documents))

    count = await index_previous_incidents(
        project_uid="YOUR_PROJECT_UID",
        environment_uid="YOUR_ENVIRONMENT_UID",
    )

    print("Indexed:", count)

    retriever = IncidentRetriever()

    results = retriever.find_similar_incidents(
        "container memory exceeded OOMKilled",
        limit=3,
    )

    print(results)


asyncio.run(main())
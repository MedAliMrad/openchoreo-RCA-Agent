import asyncio

from src.rag.rag_service import retrieve_similar_incidents


async def test_rag():

    print("Searching similar incidents...")

    results = await retrieve_similar_incidents(
        query="""
        Application crashed because container
        exceeded memory limit and was OOMKilled.
        Backend API pods restarted.
        """,
        project_id="fallback-test-project",
        environment_id="test-env",
        top_k=3,
    )


    print("\nRESULTS")
    print("=" * 50)


    for incident in results:
        print("----------------------")

        print("Similarity:")
        print(incident.get("similarity"))

        print("Document:")
        print(incident.get("document"))

        print("\nMetadata:")
        print(incident.get("metadata"))


    assert isinstance(results, list)

    print("\nRAG TEST PASSED")


if __name__ == "__main__":
    asyncio.run(test_rag())
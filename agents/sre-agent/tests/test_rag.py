from src.rag.vector_store import VectorStore
from src.rag.retriever import IncidentRetriever


def test_rag_roundtrip():

    print("Adding test incident...")

    store = VectorStore()

    store.add_document(
        document_id="incident-test-001",
        text="""
        Incident:
        Payment service crashed.

        Root Cause:
        Container exceeded memory limit and was OOMKilled.

        Date:
        2026-07-20

        Recommendation:
        Increase memory limit and fix memory leak.
        """,
        metadata={
            "date": "2026-07-20",
            "type": "OOMKilled",
        },
    )


    print("Searching similar incident...")

    retriever = IncidentRetriever()

    results = retriever.find_similar_incidents(
        incident_description="""
        Application crashed because container
        exceeded memory limit and was killed.
        """,
        limit=3,
    )


    for incident in results:

        print("----------------------")

        print(
            "Similarity:",
            incident["similarity"]
        )

        print("Document:")
        print(
            incident["document"]
        )

        print(
            "Metadata:",
            incident.get("metadata")
        )


    assert len(results) > 0



if __name__ == "__main__":
    test_rag_roundtrip()
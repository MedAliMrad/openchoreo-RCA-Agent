from src.rag.indexer import index_mock_reports
from src.rag.retriever import IncidentRetriever


def test_retrieve_similar_incident():

    # Build memory
    index_mock_reports()

    retriever = IncidentRetriever()

    results = retriever.find_similar_incidents(
        "The payment container keeps restarting after deployment"
    )

    print("\nSimilar incidents:\n")

    for r in results:
        print(r["document"])
        print(
            "distance:",
            r["similarity"]
        )

    assert len(results) > 0
from src.rag.vector_store import VectorStore


def test_vector_store():

    store = VectorStore()

    store.add_document(
        "test-001",
        """
        High CPU usage after deployment.
        Root cause was an infinite loop.
        """
    )


    results = store.search(
        "CPU increased after a new release"
    )


    print(results)

    assert len(
        results["documents"][0]
    ) > 0
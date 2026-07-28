# from src.rag.vector_store import VectorStore


# def test_vector_store():

#     store = VectorStore()

#     store.add_document(
#         "test-001",
#         """
#         High CPU usage after deployment.
#         Root cause was an infinite loop.
#         """
#     )


#     results = store.search(
#         "CPU increased after a new release"
#     )


#     print(results)

#     assert len(
#         results["documents"][0]
#     ) > 0

from src.rag.vector_store import VectorStore


def check_count():

    store = VectorStore()

    count = store.collection.count()

    print(
        f"Indexed incidents: {count}"
    )


    # Optional: print IDs of indexed documents
    documents = store.collection.get()

    print("\nDocument IDs:")
    for doc_id in documents["ids"]:
        print("-", doc_id)


if __name__ == "__main__":
    check_count()
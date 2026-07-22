from src.rag.indexer import index_mock_reports


def test_index_mock_reports():

    count = index_mock_reports()

    print(
        f"\nIndexed {count} incidents"
    )

    assert count >= 1
import json
from pathlib import Path

from src.rag.ingestion import report_to_document


def test_mock_reports_ingestion():

    reports_path = (
        Path(__file__).parent.parent
        / "src"
        / "mock_data"
        / "reports"
    )

    documents = []

    for report_file in reports_path.glob("*.json"):

        with open(report_file, "r", encoding="utf-8") as f:
            report = json.load(f)

        document = report_to_document(report)

        print(f"\n===== {report_file.name} =====")
        print(document)

        documents.append(document)

    # We should have loaded all incidents
    assert len(documents) >= 1

    # Check that the first incident is correctly processed
    assert any(
        "High CPU Usage" in doc
        for doc in documents
    )

    assert any(
        "Infinite loop introduced" in doc
        for doc in documents
    )
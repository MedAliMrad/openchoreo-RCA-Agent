from src.rag.ingestion import report_to_document


def test_report_to_document():

    report = {
        "report": {
            "alert_context": {
                "alert_name": "High CPU",
                "component": "api-service",
                "environment": "production",
            },
            "summary": "CPU increased after deployment",
            "result": {
                "type": "root_cause_identified",
                "root_causes": [
                    {
                        "summary": "Infinite loop introduced",
                        "analysis": "New code caused excessive CPU usage",
                        "supporting_findings": [
                            {
                                "observation": "CPU reached 99%"
                            }
                        ],
                    }
                ],
                "recommendations": {
                    "recommended_actions": [
                        {
                            "description": "Rollback deployment"
                        }
                    ]
                },
            },
        }
    }

    document = report_to_document(report)

    assert "High CPU" in document
    assert "Infinite loop introduced" in document
    assert "Rollback deployment" in document
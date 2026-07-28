from datetime import datetime, timedelta, timezone

from src.clients.backend import get_report_backend


def format_rca_document(
    report_id: str,
    report: dict,
) -> str:

    alert_context = report.get(
        "alert_context",
        {}
    )

    result = report.get(
        "result",
        {}
    )


    root_causes = result.get(
        "root_causes",
        []
    )


    recommendations = result.get(
        "recommendations",
        []
    )


    return f"""
Incident ID:
{report_id}


Alert:
{alert_context.get("alert_name", "")}


Component:
{alert_context.get("component", "")}


Environment:
{alert_context.get("environment", "")}


Root Cause:
{root_causes}


Summary:
{report.get("summary", "")}


Recommendations:
{recommendations}
"""

async def load_previous_incidents(
    project_uid: str,
    environment_uid: str,
    days: int = 30,
):
    """
    Load previous RCA reports from the backend
    and convert them into RAG documents.
    """

    backend = get_report_backend()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days)

    result = await backend.list_rca_reports(
        project_uid=project_uid,
        environment_uid=environment_uid,
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat(),
        limit=100,
    )
    print("BACKEND RESULT:")
    print(result)

    documents = []

    for report_summary in result["reports"]:
        if report_summary.get("status") != "completed":
            continue
        report_id = report_summary["reportId"]

        full_report = await backend.get_rca_report(report_id)

        print("FULL REPORT:")
        print(full_report)

        if not full_report:
            continue
        if full_report.get("status") != "completed":
            continue

        rca_content = full_report.get("report", {})

        documents.append(
            {
                "id": report_id,

                "content": format_rca_document(report_id, rca_content),

                "metadata": {
                    "alert_id": full_report.get("alertId"),
                    "timestamp": full_report.get("@timestamp"),
                    "status": full_report.get("status"),
                    "project_uid": project_uid,
                    "environment_uid": environment_uid,
                },
            }
        )

    return documents
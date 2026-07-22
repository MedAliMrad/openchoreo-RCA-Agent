from datetime import datetime, timedelta, timezone

from src.clients.backend import get_report_backend


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

    documents = []

    for report_summary in result["reports"]:

        report_id = report_summary["reportId"]

        full_report = await backend.get_rca_report(
            report_id
        )

        if not full_report:
            continue

        rca_content = full_report.get("report", {})

        documents.append(
            {
                "id": report_id,

                "content": str(rca_content),

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
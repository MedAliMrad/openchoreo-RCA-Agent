import logging
from typing import Any

logger = logging.getLogger(__name__)


def report_to_document(report: dict[str, Any]) -> str:
    """
    Convert an RCA report into a text document for RAG indexing.
    """

    rca = report.get("report", {})

    if not rca:
        logger.warning("Empty RCA report received")
        return ""

    alert_context = rca.get("alert_context", {})

    component = alert_context.get("component", "unknown")
    alert_name = alert_context.get("alert_name", "unknown")
    environment = alert_context.get("environment", "unknown")

    summary = rca.get("summary", "")

    document_parts = [
        f"Incident Alert: {alert_name}",
        f"Component: {component}",
        f"Environment: {environment}",
        "",
        f"Summary: {summary}",
    ]

    result = rca.get("result", {}) or {}

    # root cause identified case
    if result.get("type") == "root_cause_identified":
        root_causes = result.get("root_causes", [])

        document_parts.append("")
        document_parts.append("Root Causes:")

        for cause in root_causes:
            document_parts.append(f"- {cause.get('summary', '')}")
            document_parts.append(f"  Analysis: {cause.get('analysis', '')}")
            findings = cause.get("supporting_findings", [])

            for finding in findings:
                document_parts.append(f"  Evidence: {finding.get('observation', '')}")

        recommendations = (result.get("recommendations", {}) or {}).get("recommended_actions", [])
        if recommendations:
            document_parts.append("")
            document_parts.append("Recommended Actions:")

            for action in recommendations:
                document_parts.append(f"- {action.get('description', '')}")

    # no root cause case
    elif result.get("type") == "no_root_cause_identified":
        document_parts.append("")
        document_parts.append(f"No root cause identified: {result.get('explanation', '')}")

    return "\n".join(document_parts)
        
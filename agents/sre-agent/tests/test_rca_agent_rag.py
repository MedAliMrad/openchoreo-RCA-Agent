import asyncio

from src.agent.agent import run_analysis
from src.helpers import AlertScope


async def main():

    scope = AlertScope(
        project_uid="test-project",
        environment_uid="test-env",
    )

    alert = {
        "alertname": "OOMKilled",
        "component": "payment-service",
        "description": """
        Kubernetes container exceeded memory limit.
        Container was killed.
        """
    }


    await run_analysis(
        report_id="rag-test-001",
        alert_id="alert-test-001",
        alert=alert,
        scope=scope,
        meta={
            "source": "manual-test"
        },
    )


if __name__ == "__main__":
    asyncio.run(main())
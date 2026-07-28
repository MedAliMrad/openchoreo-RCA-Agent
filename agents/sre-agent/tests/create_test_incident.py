import asyncio

from src.clients.backend import get_report_backend


async def main():

    backend = get_report_backend()

    await backend.initialize()

    report = {
        "alert_context": {
            "alert_name": "HighMemoryUsage",
            "component": "backend-api",
            "environment": "test-env"
        },

        "result": {
            "root_causes": [
                "Memory leak in backend-api pod",
                "Pod restart due to OOMKilled"
            ],

            "recommendations": [
                "Increase memory limits",
                "Analyze heap usage"
            ]
        },

        "summary": (
            "Backend API pods restarted because "
            "memory usage exceeded limits."
        )
    }


    result = await backend.upsert_rca_report(
        report_id="rca-memory-001",
        alert_id="alert-memory-high-001",
        status="completed",
        report=report,
        summary=report["summary"],
        project_uid="fallback-test-project",
        environment_uid="test-env",
    )


    print(result)


asyncio.run(main())

# #verification
# import asyncio
# from src.clients.backend import get_report_backend


# async def main():

#     backend = get_report_backend()

#     await backend.initialize()

#     result = await backend.list_rca_reports(
#         project_uid="fallback-test-project",
#         environment_uid="test-env",
#         start_time="2026-01-01T00:00:00+00:00",
#         end_time="2027-01-01T00:00:00+00:00",
#     )

#     print(result)


# asyncio.run(main())
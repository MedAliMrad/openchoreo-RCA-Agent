# import asyncio

# from src.agent.agent import run_analysis
# from src.helpers import AlertScope
# from src.clients import get_report_backend
# import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(levelname)s:%(name)s:%(message)s"
# )

# async def main():

#     # Initialize database (creates rca_reports table)
#     backend = get_report_backend()
#     await backend.initialize()

#     scope = AlertScope(
#         namespace="default",
#         project="test-project",
#         project_uid="test-project",
#         environment="test-env",
#         environment_uid="test-env",
#         component="payment-service",
#     )

#     alert = {
#         "rule": {
#             "name": "oom-critical-alert"
#         },
#         "severity": "critical",
#         "description": "Memory usage exceeded 90% for payment-service",
#         "labels": {
#             "component": "payment-service",
#             "namespace": "default",
#             "alertname": "oom-critical-alert",
#         },
#         "annotations": {
#             "summary": "High memory usage detected",
#             "description": "The payment-service component exceeded the memory threshold."
#         },
#         "status": "firing",
#     }

#     await run_analysis(
#         report_id="test-rag-llm-001",
#         alert_id="alert-001",
#         alert=alert,
#         scope=scope,
#         meta={
#             "source": "manual-test",
#         },
#     )


# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio

from src.agent.agent import run_analysis
from src.helpers import AlertScope
from src.clients import get_report_backend
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s"
)


async def main():

    # Initialize database
    backend = get_report_backend()
    await backend.initialize()


    scope = AlertScope(
        namespace="default",
        project="ecommerce",
        project_uid="ecommerce",
        environment="production",
        environment_uid="production",
        component="cache-service",
    )


    # Similar incident to incident-005
    # RAG should retrieve the previous Redis RCA
    alert = {

        "rule": {
            "name": "redis-connection-failure"
        },

        "severity": "critical",

        "description":
            "Redis became unavailable and cache requests are failing for cache-service.",

        "labels": {

            "component": "cache-service",

            "namespace": "default",

            "alertname": "redis-connection-failure",
        },


        "annotations": {

            "summary":
                "Redis unavailable",

            "description":
                "Applications cannot connect to Redis because the cache service is unreachable."
        },


        "status": "firing",
    }


    await run_analysis(

        report_id="test-rag-redis-001",

        alert_id="redis-alert-001",

        alert=alert,

        scope=scope,

        meta={
            "source": "rag-redis-test",
        },
    )


if __name__ == "__main__":
    asyncio.run(main())
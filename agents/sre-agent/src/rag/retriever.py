# import logging
# from datetime import datetime,timedelta,UTC

# from src.clients import get_report_backend
# from src.rag.ingestion import report_to_document

# logger = logging.getLogger(__name__)

# async def load_previous_incidents(
#         project_uid:str,
#         environment_uid:str,
#         days: int =30,
# ):
#     """
#     Load previous RCA reports and convert them into documents.
#     """
#     backend = get_report_backend()
#     end_time = datetime.now(UTC)
#     start_time = end_time - timedelta(days=days)
    
#     result = await backend.list_rca_reports(
#         project_uid=project_uid,
#         environment_uid=environment_uid,
#         start_time=start_time.isoformat(),
#         end_time=end_time.isoformat(),
#         status="completed",
#         limit=100,
#     )

#     documents = []

#     for report_summary in result["reports"]:
#         report_id = report_summary["reportId"]
#         full_report = await backend.get_rca_report(
#             report_id
#         )
#         if not full_report:
#             continue
#         document = report_to_document(full_report)

#         if document:
#             documents.append(
#                 {
#                     "id":report_id,
#                     "content":document,
#                     "timestamp":full_report["@timestamp"],
#             }
#             )
    
#     logger.info(
#         "Loaded %d previous incidents",
#         len(documents)
#     )

#     return documents


from src.rag.vector_store import VectorStore

class IncidentRetriever:

    def __init__(self):
        self.store = VectorStore()



    def find_similar_incidents(
        self,
        incident_description: str,
        limit: int = 3,
    ):
        results= self.store.search(
            incident_description,
            limit=limit,
        )

        incidents = []

        documents = results.get(
            "documents",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        for doc,distance in zip(
            documents,
            distances
        ):
            incidents.append(
                {
                    "document":doc,
                    "similarity":distance,
                }
            )
    
        return incidents
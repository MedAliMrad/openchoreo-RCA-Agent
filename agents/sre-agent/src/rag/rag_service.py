from src.rag.indexer import index_previous_incidents
from src.rag.retriever import IncidentRetriever

async def retrieve_similar_incidents(
        query: str,
        project_id: str,
        environment_id: str,
        top_k: int = 3,
):
    """
    Retrieve similar historical incidents.
    """

    #Make sure historical reports are indexed 
    await index_previous_incidents(
        project_uid=project_id,
        environment_id=environment_id,
    )

    retriever = IncidentRetriever()

    similar_incidents = retriever.find_similar_incidents(
        incident_description=query,
        limit=top_k,
    )

    return similar_incidents
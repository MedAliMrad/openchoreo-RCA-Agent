import logging

from src.rag.indexer import index_previous_incidents
from src.rag.retriever import IncidentRetriever


logger = logging.getLogger(__name__)


# Keep track of indexed environments
_indexed_contexts: set[tuple[str, str]] = set()


async def retrieve_similar_incidents(
    query: str,
    project_id: str,
    environment_id: str,
    top_k: int = 3,
):
    """
    Retrieve similar historical incidents.

    Index historical reports only once per
    project/environment combination.
    """

    context_key = (project_id, environment_id)

    if context_key not in _indexed_contexts:

        logger.info(
            "Indexing previous incidents for project=%s environment=%s",
            project_id,
            environment_id,
        )

        count = await index_previous_incidents(
            project_uid=project_id,
            environment_id=environment_id,
        )

        logger.info(
            "Indexed %d previous incidents",
            count,
        )

        _indexed_contexts.add(context_key)

    else:
        logger.debug(
            "RAG index already exists for project=%s environment=%s",
            project_id,
            environment_id,
        )


    retriever = IncidentRetriever()

    similar_incidents = retriever.find_similar_incidents(
        incident_description=query,
        limit=top_k,
    )

    logger.info(
        "Retrieved %d similar incidents",
        len(similar_incidents),
    )

    return similar_incidents
from src.rag.loader import load_previous_incidents
from src.rag.vector_store import VectorStore

async def index_previous_incidents(
        project_uid: str,
        environment_id: str,
):
    """
    Load previous RCA reports and index them into ChromaDB.
    """

    documents = await load_previous_incidents(
        project_uid=project_uid,
        environment_uid=environment_id,
    )

    store = VectorStore()

    store.add_documents(
        documents
    )

    return len(documents)
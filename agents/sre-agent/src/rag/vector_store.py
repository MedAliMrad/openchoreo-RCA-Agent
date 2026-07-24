import logging

import chromadb
from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="rca_incidents"
        )

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )


    def add_document(
        self,
        document_id: str,
        text: str,
        metadata: dict | None = None,
    ):

        embedding = self.model.encode(text).tolist()

        self.collection.upsert(
            ids=[document_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata or {}],
        )


    def add_documents(
        self,
        documents: list[dict],
    ):
        """
        Add or update RCA documents.
        """

        for document in documents:

            self.add_document(
                document_id=document["id"],
                text=document["content"],
                metadata=document.get("metadata"),
            )


    def search(
        self,
        query: str,
        limit: int = 3,
    ):

        embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=limit,
            include=[
                "documents",
                "distances",
                "metadatas",
            ],
        )

        return results
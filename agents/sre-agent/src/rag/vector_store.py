import logging
from functools import lru_cache

import chromadb
import os
os.environ.setdefault("SENTENCE_TRANSFORMERS_HOME", r"C:\Users\user\.cache\sre-agent-models")
from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)


@lru_cache()
def get_embedding_model():
    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="rca_incidents",
            metadata={"hnsw:space": "cosine"},
        )

        self.model = get_embedding_model()


    def add_document(
        self,
        document_id: str,
        text: str,
        metadata: dict | None = None,
    ):

        embedding = self.model.encode(
            text, normalize_embeddings=True
        ).tolist()

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

        embedding = self.model.encode(
            query, normalize_embeddings=True
        ).tolist()


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
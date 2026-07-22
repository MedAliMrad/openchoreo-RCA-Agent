import chromadb
from sentence_transformers import SentenceTransformer


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
    ):
        embedding = self.model.encode(text).tolist()

        self.collection.add(
            ids=[document_id],
            documents=[text],
            embeddings=[embedding],
        )

    def add_documents(
        self,
        documents: list[dict],
    ):
        """
        Add multiple RCA documents to the vector database
        """

        for document in documents:
            self.add_document(
                document_id=document["id"],
                text=document["content"],
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
        )

        return results
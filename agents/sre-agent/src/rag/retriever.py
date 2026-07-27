# from src.rag.vector_store import VectorStore


# class IncidentRetriever:

#     def __init__(self):
#         self.store = VectorStore()


#     def find_similar_incidents(
#         self,
#         incident_description: str,
#         limit: int = 3,
#     ):

#         results = self.store.search(
#             incident_description,
#             limit=limit,
#         )

#         incidents = []

#         documents = results.get(
#             "documents",
#             [[]]
#         )[0]

#         distances = results.get(
#             "distances",
#             [[]]
#         )[0]

#         metadatas = results.get(
#             "metadatas",
#             [[]]
#         )[0]


#         for doc, distance, metadata in zip(
#             documents,
#             distances,
#             metadatas,
#         ):

#             # Chroma returns distance:
#             # lower = more similar
#             #
#             # Convert to similarity score
#             similarity = round(
#                 1 - distance,
#                 3
#             )

#             incidents.append(
#                 {
#                     "document": doc,
#                     "similarity": similarity,
#                     "metadata": metadata,
#                 }
#             )

#         return incidents

from src.rag.vector_store import VectorStore


class IncidentRetriever:

    def __init__(self):
        self.store = VectorStore()


    async def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ):

        results = self.store.search(
            query,
            limit=top_k,
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

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]


        for doc, distance, metadata in zip(
            documents,
            distances,
            metadatas,
        ):

            incidents.append(
                {
                    "document": doc,
                    "similarity": round(
                        1 - distance,
                        3
                    ),
                    "metadata": metadata,
                }
            )

        return incidents
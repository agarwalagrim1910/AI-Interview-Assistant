from utils.rag.embedder import get_embedding
from utils.rag.vector_store import VectorStore


class Retriever:
    """
    Retrieves the most relevant resume chunks
    using semantic similarity search.
    """

    def __init__(self, vector_store: VectorStore):

        self.vector_store = vector_store

    # ------------------------------------------
    # Retrieve Top K Chunks
    # ------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ):
        """
        Retrieves the most relevant chunks
        for a given query.

        Args:
            query: User query
            top_k: Number of chunks to retrieve

        Returns:
            List of relevant chunks
        """

        query_embedding = get_embedding(query)

        results = self.vector_store.search(

            query_embedding,

            top_k

        )

        return results
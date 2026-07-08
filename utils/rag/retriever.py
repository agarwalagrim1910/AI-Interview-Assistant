from utils.rag.embedder import get_embedding
from utils.rag.vector_store import VectorStore


class Retriever:
    """
    Retrieves the most relevant resume chunks
    using semantic similarity search.
    """

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):
        """
        Retrieve the Top-K most relevant resume chunks.

        Args:
            query (str): Search query.
            top_k (int): Number of chunks to retrieve.

        Returns:
            List of retrieved chunks ranked by similarity.
        """

        query_embedding = get_embedding(query)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return results
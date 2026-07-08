class Reranker:
    """
    Selects the most relevant chunks from the retrieved
    results before sending them to the LLM.
    """

    def __init__(self, top_n: int = 2):
        self.top_n = top_n

    def rerank(self, retrieved_chunks):
        """
        Rerank retrieved chunks using similarity scores.

        Args:
            retrieved_chunks (list): List of dictionaries with
                'text' and 'score'.

        Returns:
            List of the best chunks.
        """

        if not retrieved_chunks:
            return []

        ranked_chunks = sorted(
            retrieved_chunks,
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked_chunks[:self.top_n]
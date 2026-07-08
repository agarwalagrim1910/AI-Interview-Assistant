from utils.rag.chunker import create_chunks
from utils.rag.embedder import embed_chunks
from utils.rag.vector_store import VectorStore
from utils.rag.retriever import Retriever
from utils.rag.reranker import Reranker


class RAGPipeline:
    """
    Complete RAG pipeline for resume retrieval.
    """

    def __init__(self):

        self.vector_store = VectorStore()

        self.retriever = None

        self.reranker = Reranker(top_n=2)

        self.is_initialized = False

    # --------------------------------------------------
    # Build Vector Database
    # --------------------------------------------------

    def build(self, resume_text: str):
        """
        Builds the complete vector database from
        the uploaded resume.
        """

        chunks = create_chunks(resume_text)

        embeddings = embed_chunks(chunks)

        self.vector_store.create_index(
            embeddings
        )

        self.vector_store.set_chunks(
            chunks
        )

        self.retriever = Retriever(
            self.vector_store
        )

        self.is_initialized = True

    # --------------------------------------------------
    # Retrieve Relevant Context
    # --------------------------------------------------

    def retrieve_context(
        self,
        query: str,
        top_k: int = 5
    ):
        """
        Retrieves and reranks the most relevant
        resume chunks.
        """

        if not self.is_initialized:

            raise Exception(
                "RAG Pipeline has not been initialized."
            )

        retrieved_chunks = self.retriever.retrieve(
            query=query,
            top_k=top_k
        )

        reranked_chunks = self.reranker.rerank(
            retrieved_chunks
        )

        return reranked_chunks

    # --------------------------------------------------
    # Helper
    # --------------------------------------------------

    def retrieve_context_as_text(
        self,
        query: str,
        top_k: int = 5
    ):
        """
        Returns the reranked chunks as one string.
        """

        chunks = self.retrieve_context(
            query=query,
            top_k=top_k
        )

        return "\n\n".join(
            chunk["text"] for chunk in chunks
        )
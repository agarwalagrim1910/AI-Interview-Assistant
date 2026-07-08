import faiss
import pickle
import numpy as np
import os


# --------------------------------------------------
# Vector Store Class
# --------------------------------------------------

class VectorStore:
    """
    Handles creation, saving, loading and searching
    of the FAISS vector database.
    """

    def __init__(self):

        self.index = None
        self.chunks = []


# --------------------------------------------------
# Create FAISS Index
# --------------------------------------------------

    def create_index(self, embeddings: np.ndarray):
        """
        Creates a FAISS index from embeddings.
        """

        if embeddings.size == 0:
            raise ValueError(
                "Embeddings cannot be empty."
            )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(
            embeddings.astype("float32")
        )


# --------------------------------------------------
# Store Chunks
# --------------------------------------------------

    def set_chunks(self, chunks):

        self.chunks = chunks


# --------------------------------------------------
# Search Similar Chunks
# --------------------------------------------------

    def search(
        self,
        query_embedding,
        top_k=5
    ):
        """
        Search the FAISS index and return the
        most relevant resume chunks along with
        their similarity scores.
        """

        if self.index is None:
            raise ValueError(
                "FAISS index has not been created."
            )

        scores, indices = self.index.search(
            query_embedding.reshape(1, -1).astype("float32"),
            top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if 0 <= idx < len(self.chunks):

                results.append(
                    {
                        "text": self.chunks[idx],
                        "score": float(score)
                    }
                )

        return results


# --------------------------------------------------
# Save Vector Store
# --------------------------------------------------

    def save(
        self,
        folder="vector_db"
    ):

        os.makedirs(
            folder,
            exist_ok=True
        )

        faiss.write_index(

            self.index,

            os.path.join(
                folder,
                "resume_index.faiss"
            )

        )

        with open(

            os.path.join(
                folder,
                "chunks.pkl"
            ),

            "wb"

        ) as f:

            pickle.dump(
                self.chunks,
                f
            )


# --------------------------------------------------
# Load Vector Store
# --------------------------------------------------

    def load(
        self,
        folder="vector_db"
    ):

        self.index = faiss.read_index(

            os.path.join(
                folder,
                "resume_index.faiss"
            )

        )

        with open(

            os.path.join(
                folder,
                "chunks.pkl"
            ),

            "rb"

        ) as f:

            self.chunks = pickle.load(f)
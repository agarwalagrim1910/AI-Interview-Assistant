from sentence_transformers import SentenceTransformer
import numpy as np

# --------------------------------------------------
# Singleton Embedding Model
# --------------------------------------------------

_model = None


def load_embedding_model():
    """
    Loads the Sentence Transformer model only once.
    Reuses it for future embedding requests.
    """

    global _model

    if _model is None:

        print("Loading embedding model...")

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully!")

    return _model


# --------------------------------------------------
# Generate Embedding for One Text
# --------------------------------------------------

def get_embedding(text: str) -> np.ndarray:
    """
    Converts a single text into an embedding vector.
    """

    model = load_embedding_model()

    embedding = model.encode(

        text,

        convert_to_numpy=True,

        normalize_embeddings=True

    )

    return embedding


# --------------------------------------------------
# Generate Embeddings for Multiple Chunks
# --------------------------------------------------

def embed_chunks(chunks: list[str]) -> np.ndarray:
    """
    Converts a list of chunks into embedding vectors.

    Returns:
        numpy.ndarray
        Shape -> (num_chunks, embedding_dimension)
    """

    if not chunks:

        return np.array([])

    model = load_embedding_model()

    embeddings = model.encode(

        chunks,

        convert_to_numpy=True,

        normalize_embeddings=True,

        show_progress_bar=False

    )

    return embeddings
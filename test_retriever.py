from utils.rag.embedder import embed_chunks
from utils.rag.vector_store import VectorStore
from utils.rag.retriever import Retriever

chunks = [

    "Fake News Detection using BERT",

    "AI Interview Assistant using Gemini",

    "Python Java SQL"

]

embeddings = embed_chunks(chunks)

store = VectorStore()

store.create_index(embeddings)

store.set_chunks(chunks)

retriever = Retriever(store)

results = retriever.retrieve(

    "Tell me about BERT",

    top_k=2

)

print()

print("Retrieved Chunks")

print("-" * 40)

for chunk in results:

    print(chunk)

    print()
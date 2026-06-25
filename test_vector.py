from utils.rag.embedder import embed_chunks
from utils.rag.vector_store import VectorStore

chunks = [

    "Fake News Detection using BERT",

    "AI Interview Assistant using Gemini",

    "Python Java SQL"

]

embeddings = embed_chunks(chunks)

store = VectorStore()

store.create_index(embeddings)

store.set_chunks(chunks)

store.save()

print("Vector Store Saved!")

store2 = VectorStore()

store2.load()

print("Vector Store Loaded!")

query = embed_chunks(
    ["Tell me about BERT"]
)[0]

results = store2.search(query)

print()

print(results)
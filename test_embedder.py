from utils.rag.embedder import embed_chunks

chunks = [

    "Fake News Detection using BERT",

    "AI Interview Assistant using Gemini",

    "Python Java SQL"

]

embeddings = embed_chunks(chunks)

print("Embedding Shape:")

print(embeddings.shape)

print()

print("First Embedding")

print(embeddings[0][:10])
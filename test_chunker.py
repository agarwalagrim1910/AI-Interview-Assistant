from utils.rag.chunker import create_chunks

resume = """
Projects

AI Interview Assistant
Built using Gemini API and Streamlit.

Fake News Detection
Built using BERT and Sentence Transformers.

Experience

Microsoft Student Community
Management Head

Skills

Python
Java
Machine Learning
"""

chunks = create_chunks(resume)

print("=" * 60)

for i, chunk in enumerate(chunks, start=1):

    print(f"\nChunk {i}\n")

    print(chunk)

    print("-" * 60)
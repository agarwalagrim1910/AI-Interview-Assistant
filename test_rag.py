from utils.rag.rag_pipeline import RAGPipeline

resume = """
Projects

Fake News Detection using BERT

Image Generation using Stable Diffusion

Experience

Microsoft Student Community

Skills

Python
Java
Machine Learning
"""

rag = RAGPipeline()

rag.build(resume)

context = rag.retrieve_context_as_text(
    "Ask me about BERT"
)

print()

print("=" * 60)

print(context)

print("=" * 60)
# utils/skill_database.py

# ==========================================================
# Skill Database
# ==========================================================

SKILL_DATABASE = {

    # -----------------------------------------
    # Programming Languages
    # -----------------------------------------

    "Programming": [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "TypeScript",
        "Go",
        "Rust",
        "R",
        "SQL"
    ],

    # -----------------------------------------
    # Web Development
    # -----------------------------------------

    "Web Development": [
        "HTML",
        "CSS",
        "Bootstrap",
        "React",
        "Angular",
        "Vue",
        "Node.js",
        "Express",
        "Flask",
        "Django",
        "FastAPI",
        "Spring Boot",
        "Streamlit"
    ],

    # -----------------------------------------
    # Databases
    # -----------------------------------------

    "Databases": [
        "MySQL",
        "PostgreSQL",
        "SQLite",
        "MongoDB",
        "Redis"
    ],

    # -----------------------------------------
    # Artificial Intelligence
    # -----------------------------------------

    "Artificial Intelligence": [
        "Machine Learning",
        "Deep Learning",
        "Neural Networks",
        "TensorFlow",
        "PyTorch",
        "Keras",
        "Scikit-learn",
        "OpenCV",
        "NLP",
        "Computer Vision",
        "BERT",
        "Transformers",
        "LLM",
        "Generative AI",
        "RAG",
        "LangChain",
        "LlamaIndex",
        "FAISS",
        "Sentence Transformers",
        "Embeddings",
        "Vector Database",
        "Prompt Engineering",
        "Gemini",
        "OpenAI"
    ],

    # -----------------------------------------
    # Cloud
    # -----------------------------------------

    "Cloud": [
        "AWS",
        "Azure",
        "Google Cloud",
        "GCP"
    ],

    # -----------------------------------------
    # DevOps
    # -----------------------------------------

    "DevOps": [
        "Docker",
        "Kubernetes",
        "Git",
        "GitHub",
        "CI/CD",
        "Linux"
    ],

    # -----------------------------------------
    # Data Science
    # -----------------------------------------

    "Data Science": [
        "NumPy",
        "Pandas",
        "Matplotlib",
        "Seaborn",
        "Plotly",
        "Power BI",
        "Excel"
    ]
}

# ==========================================================
# Default Category Weights
# ==========================================================

CATEGORY_WEIGHTS = {
    "Programming": 5,
    "Artificial Intelligence": 5,
    "Cloud": 5,
    "Databases": 4,
    "Web Development": 4,
    "DevOps": 4,
    "Data Science": 4
}

# ==========================================================
# Build Skill Weight Dictionary Automatically
# ==========================================================

SKILL_WEIGHTS = {}

for category, skills in SKILL_DATABASE.items():

    default_weight = CATEGORY_WEIGHTS.get(category, 3)

    for skill in skills:
        SKILL_WEIGHTS[skill.lower()] = default_weight

# ==========================================================
# Manual Overrides
# ==========================================================

SKILL_WEIGHTS.update({

    "html": 2,
    "css": 2,
    "bootstrap": 2,

    "git": 3,
    "github": 3,

    "streamlit": 3,

    "excel": 3,
    "power bi": 4
})
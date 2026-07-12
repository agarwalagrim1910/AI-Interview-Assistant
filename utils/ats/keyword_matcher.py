# utils/ats/keyword_matcher.py

# --------------------------------------------------
# Common ATS Skills Database
# --------------------------------------------------

ATS_SKILLS = {

    "Programming": [

        "python", "java", "c", "c++", "javascript",
        "typescript", "sql", "r"

    ],

    "AI/ML": [

        "machine learning",
        "deep learning",
        "nlp",
        "computer vision",
        "bert",
        "tensorflow",
        "keras",
        "pytorch",
        "scikit-learn"

    ],

    "Data": [

        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "power bi",
        "excel"

    ],

    "Backend": [

        "flask",
        "django",
        "fastapi",
        "streamlit"

    ],

    "Database": [

        "mysql",
        "postgresql",
        "mongodb",
        "sqlite"

    ],

    "Cloud & DevOps": [

        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "git",
        "github",
        "ci/cd"

    ]

}


# --------------------------------------------------
# Keyword Matcher
# --------------------------------------------------

def match_keywords(resume_text):
    """
    Detects ATS keywords from the resume.
    """

    resume = resume_text.lower()

    detected = []

    missing = []

    for category, skills in ATS_SKILLS.items():

        for skill in skills:

            if skill in resume:

                detected.append(skill)

            else:

                missing.append(skill)

    return {

        "detected": sorted(set(detected)),

        "missing": sorted(set(missing))

    }
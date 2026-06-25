import re


# --------------------------------------------------
# Resume Section Headings
# --------------------------------------------------

SECTION_PATTERNS = {
    "projects": [
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "major projects",
        "key projects"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "employment history",
        "internships",
        "internship"
    ],

    "education": [
        "education",
        "academic background",
        "qualifications",
        "qualification"
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "technical expertise",
        "programming skills"
    ],

    "certifications": [
        "certifications",
        "certification",
        "courses",
        "licenses"
    ]
}


# --------------------------------------------------
# Clean Extracted Text
# --------------------------------------------------

def clean_text(text: str) -> str:

    if not text:
        return ""

    # Remove tabs
    text = text.replace("\t", " ")

    # Normalize multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Normalize blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text


# --------------------------------------------------
# Find Resume Section
# --------------------------------------------------

def find_section(resume_text, headings):

    # Create heading regex
    heading_pattern = "|".join(
        re.escape(h)
        for h in headings
    )

    # Every possible heading
    all_headings = []

    for values in SECTION_PATTERNS.values():

        all_headings.extend(values)

    stop_pattern = "|".join(
        re.escape(h)
        for h in all_headings
    )

    pattern = rf"""
        (?:{heading_pattern})      # Current Heading
        \s*
        [:]?
        \s*
        (.*?)                      # Section Content
        (?=
            \n\s*(?:{stop_pattern})\s*:?
            |
            $
        )
    """

    match = re.search(

        pattern,

        resume_text,

        flags=re.IGNORECASE | re.DOTALL | re.VERBOSE

    )

    if not match:
        return ""

    return clean_text(
        match.group(1)
    )


# --------------------------------------------------
# Extract Resume Context
# --------------------------------------------------

def extract_resume_context(resume_text):

    resume_text = clean_text(resume_text)

    context = {

        "projects":
        find_section(
            resume_text,
            SECTION_PATTERNS["projects"]
        ),

        "experience":
        find_section(
            resume_text,
            SECTION_PATTERNS["experience"]
        ),

        "education":
        find_section(
            resume_text,
            SECTION_PATTERNS["education"]
        ),

        "skills":
        find_section(
            resume_text,
            SECTION_PATTERNS["skills"]
        ),

        "certifications":
        find_section(
            resume_text,
            SECTION_PATTERNS["certifications"]
        ),

        "full_resume":
        resume_text
    }

    context["metadata"] = {

        "has_projects":
        bool(context["projects"]),

        "has_experience":
        bool(context["experience"]),

        "has_education":
        bool(context["education"]),

        "has_skills":
        bool(context["skills"]),

        "has_certifications":
        bool(context["certifications"])
    }

    return context
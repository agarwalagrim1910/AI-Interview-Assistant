# utils/ats/resume_scorer.py

import re


# --------------------------------------------------
# ATS Resume Scorer
# --------------------------------------------------

def calculate_ats_score(
    resume_text,
    detected_keywords,
    total_keywords
):
    """
    Calculates an ATS score out of 100.
    """

    score = {}

    # -----------------------------------------
    # Skills (25)
    # -----------------------------------------

    skills_score = min(

        25,

        int(
            (len(detected_keywords) / total_keywords) * 25
        )

    )

    score["Skills"] = skills_score

    # -----------------------------------------
    # Projects (20)
    # -----------------------------------------

    project_words = [

        "project",

        "developed",

        "implemented",

        "built",

        "designed"

    ]

    projects = sum(

        word in resume_text.lower()

        for word in project_words

    )

    score["Projects"] = min(
        20,
        projects * 4
    )

    # -----------------------------------------
    # Education (10)
    # -----------------------------------------

    education_keywords = [

        "b.tech",

        "btech",

        "bachelor",

        "university",

        "cgpa"

    ]

    education = any(

        word in resume_text.lower()

        for word in education_keywords

    )

    score["Education"] = 10 if education else 5

    # -----------------------------------------
    # Experience (10)
    # -----------------------------------------

    experience_keywords = [

        "intern",

        "experience",

        "worked",

        "company"

    ]

    experience = any(

        word in resume_text.lower()

        for word in experience_keywords

    )

    score["Experience"] = 10 if experience else 4

    # -----------------------------------------
    # Formatting (15)
    # -----------------------------------------

    formatting_score = 15

    if len(resume_text) < 400:

        formatting_score -= 5

    if len(re.findall(r"\n", resume_text)) < 20:

        formatting_score -= 3

    formatting_score = max(
        formatting_score,
        5
    )

    score["Formatting"] = formatting_score

    # -----------------------------------------
    # Contact Info (10)
    # -----------------------------------------

    email = re.search(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

        resume_text

    )

    phone = re.search(

        r"\d{10}",

        resume_text

    )

    score["Contact"] = 10 if email and phone else 5

    # -----------------------------------------
    # Overall Score
    # -----------------------------------------

    overall = sum(
        score.values()
    )

    return {

        "overall_score": overall,

        "breakdown": score

    }
import re

from utils.skill_database import SKILL_DATABASE


# ==========================================================
# Normalize Text
# ==========================================================

def normalize_text(text):
    return text.lower()


# ==========================================================
# Check Skill Match
# ==========================================================

def contains_skill(text, skill):
    """
    Checks whether a skill exists in text.

    Uses word boundaries to avoid false matches.
    Falls back to substring matching for
    multi-word skills.
    """

    text = normalize_text(text)
    skill = skill.lower()

    # Multi-word skills
    if " " in skill:
        return skill in text

    pattern = rf"\b{re.escape(skill)}\b"

    return re.search(pattern, text) is not None


# ==========================================================
# Flat Skill Extraction
# ==========================================================

def extract_skills(text):
    """
    Returns a sorted list of detected skills.
    """

    detected = set()

    for skills in SKILL_DATABASE.values():

        for skill in skills:

            if contains_skill(text, skill):
                detected.add(skill)

    return sorted(detected)


# ==========================================================
# Categorized Skill Extraction
# ==========================================================

def extract_skills_by_category(text):
    """
    Returns skills grouped by category.
    """

    categorized = {}

    for category, skills in SKILL_DATABASE.items():

        found = []

        for skill in skills:

            if contains_skill(text, skill):
                found.append(skill)

        categorized[category] = sorted(found)

    return categorized


# ==========================================================
# Missing Skills
# ==========================================================

def get_missing_skills(text):
    """
    Returns missing skills grouped by category.
    """

    missing = {}

    for category, skills in SKILL_DATABASE.items():

        category_missing = []

        for skill in skills:

            if not contains_skill(text, skill):
                category_missing.append(skill)

        missing[category] = sorted(category_missing)

    return missing
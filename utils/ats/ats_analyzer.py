# utils/ats/ats_analyzer.py

from utils.ats.keyword_matcher import match_keywords
from utils.ats.resume_scorer import calculate_ats_score
from utils.ats.suggestions import generate_resume_suggestions

from utils.skill_extractor import (
    extract_skills_by_category
)


# --------------------------------------------------
# ATS Analyzer
# --------------------------------------------------

def analyze_resume(resume_text):
    """
    Performs complete ATS analysis.

    Pipeline

    Resume
        ↓
    Keyword Matching
        ↓
    Categorized Skills
        ↓
    ATS Score
        ↓
    ATS Summary
        ↓
    Gemini Suggestions
        ↓
    Final ATS Report
    """

    # -----------------------------------------
    # Keyword Analysis
    # -----------------------------------------

    keyword_result = match_keywords(
        resume_text
    )

    detected = keyword_result["detected"]

    missing = keyword_result["missing"]

    categorized_skills = extract_skills_by_category(
        resume_text
    )

    total_keywords = len(detected) + len(missing)

    # -----------------------------------------
    # ATS Score
    # -----------------------------------------

    score_result = calculate_ats_score(

        resume_text,

        detected,

        total_keywords

    )

    # -----------------------------------------
    # ATS Summary
    # -----------------------------------------

    ats_summary = {

        "resume_length": len(resume_text),

        "detected_skills": detected,

        "categorized_skills": categorized_skills,

        "missing_skills": missing[:20],

        "total_detected": len(detected),

        "total_missing": len(missing),

        "overall_score": score_result["overall_score"],

        "breakdown": score_result["breakdown"]

    }

    # -----------------------------------------
    # AI Suggestions
    # -----------------------------------------

    ai_review = generate_resume_suggestions(

        ats_summary,

        score_result

    )

    # -----------------------------------------
    # Final Result
    # -----------------------------------------

    return {

        "ats_score": score_result["overall_score"],

        "breakdown": score_result["breakdown"],

        "detected_skills": detected,

        "categorized_skills": categorized_skills,

        "missing_skills": missing,

        "ats_summary": ats_summary,

        "ai_review": ai_review

    }
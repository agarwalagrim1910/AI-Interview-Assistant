# utils/ats/ats_analyzer.py

from utils.ats.keyword_matcher import match_keywords
from utils.ats.resume_scorer import calculate_ats_score
from utils.ats.suggestions import generate_resume_suggestions


# --------------------------------------------------
# ATS Analyzer
# --------------------------------------------------

def analyze_resume(resume_text):
    """
    Performs complete ATS analysis.
    """

    # -----------------------------------------
    # Keyword Analysis
    # -----------------------------------------

    keyword_result = match_keywords(
        resume_text
    )

    detected = keyword_result["detected"]

    missing = keyword_result["missing"]

    total_keywords = len(detected) + len(missing)

    # -----------------------------------------
    # ATS Score
    # -----------------------------------------

    score_result = calculate_ats_score(

        resume_text,

        detected,

        total_keywords

    )
    ai_suggestions = generate_resume_suggestions(
    resume_text,
    score_result
)

    # -----------------------------------------
    # Final Result
    # -----------------------------------------

    return {

    "ats_score": score_result["overall_score"],

    "breakdown": score_result["breakdown"],

    "detected_skills": detected,

    "missing_skills": missing,

    "ai_review": ai_suggestions

}
    
    
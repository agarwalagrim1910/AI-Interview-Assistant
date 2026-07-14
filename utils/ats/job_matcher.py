from utils.skill_extractor import extract_skills
from utils.skill_database import SKILL_WEIGHTS
from utils.gemini_service import generate_job_match_analysis


def match_resume_with_job(
    resume_text,
    job_description
):
    """
    Compare Resume Skills with Job Description Skills.

    Pipeline

    Resume
        ↓
    Extract Resume Skills
        ↓
    Extract JD Skills
        ↓
    Weighted Skill Matching
        ↓
    Gemini Analysis
        ↓
    Return Complete Report
    """

    # -----------------------------------------
    # Extract Skills
    # -----------------------------------------

    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        job_description
    )

    # -----------------------------------------
    # Convert to Sets
    # -----------------------------------------

    resume_set = {

        skill.lower()

        for skill in resume_skills

    }

    jd_set = {

        skill.lower()

        for skill in jd_skills

    }

    # -----------------------------------------
    # Matched Skills
    # -----------------------------------------

    matched_skills = sorted(

        resume_set & jd_set

    )

    # -----------------------------------------
    # Missing Skills
    # -----------------------------------------

    missing_skills = sorted(

        jd_set - resume_set

    )

    # -----------------------------------------
    # Weighted Match Score
    # -----------------------------------------

    total_weight = 0
    matched_weight = 0

    for skill in jd_set:

        weight = SKILL_WEIGHTS.get(
            skill,
            1
        )

        total_weight += weight

        if skill in resume_set:

            matched_weight += weight

    if total_weight == 0:

        match_score = 0

    else:

        match_score = round(

            (matched_weight / total_weight) * 100

        )

    # -----------------------------------------
    # Gemini Analysis
    # -----------------------------------------

    gemini_analysis = generate_job_match_analysis(

        {

            "match_score": match_score,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "resume_skills": sorted(
                resume_set
            ),

            "jd_skills": sorted(
                jd_set
            )

        }

    )

    # -----------------------------------------
    # Return Complete Result
    # -----------------------------------------

    return {

        "match_score": match_score,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "resume_skills": sorted(
            resume_set
        ),

        "jd_skills": sorted(
            jd_set
        ),

        "matched_weight": matched_weight,

        "total_weight": total_weight,

        "gemini_analysis": gemini_analysis

    }
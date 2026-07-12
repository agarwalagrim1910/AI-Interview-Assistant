# utils/ats/job_matcher.py

from utils.skill_extractor import extract_skills


class JobMatcher:
    """
    Compares a resume with a job description
    and generates a job match report.
    """

    def __init__(self):

        pass

    # -----------------------------------------
    # Extract JD Skills
    # -----------------------------------------

    def extract_job_skills(
        self,
        job_description
    ):

        return extract_skills(
            job_description
        )

    # -----------------------------------------
    # Compare Skills
    # -----------------------------------------

    def compare_skills(
        self,
        resume_skills,
        jd_skills
    ):

        pass

    # -----------------------------------------
    # Match Score
    # -----------------------------------------

    def calculate_match_score(
        self,
        matched,
        missing,
        total_required
    ):

        pass

    # -----------------------------------------
    # Gemini Analysis
    # -----------------------------------------

    def generate_match_analysis(
        self,
        resume_text,
        job_description,
        score
    ):

        pass
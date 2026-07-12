import json
from utils.gemini_service import client


def generate_resume_suggestions(
    ats_summary,
    ats_result
):
    """
    Generates AI-powered ATS suggestions
    using ATS summary instead of the full resume.
    """

    prompt = f"""
You are an experienced Technical Recruiter and ATS Expert.

Analyze the following ATS summary.

================================
ATS Summary
================================

{json.dumps(ats_summary, indent=2)}

================================
ATS Score
================================

Overall Score: {ats_result["overall_score"]}

Score Breakdown:

{json.dumps(ats_result["breakdown"], indent=2)}

Return ONLY valid JSON.

Format:

{{
    "strengths": [
        "...",
        "...",
        "..."
    ],

    "weaknesses": [
        "...",
        "...",
        "..."
    ],

    "suggestions": [
        "...",
        "...",
        "..."
    ],

    "career_recommendations": [
        "...",
        "...",
        "..."
    ]
}}
"""

    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt

    )

    cleaned = (

        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()

    )

    return json.loads(cleaned)
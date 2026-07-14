import streamlit as st
import os
from datetime import datetime

from utils.pdf_parser import extract_text_from_pdf

from utils.ats.ats_analyzer import analyze_resume
from utils.ats.job_matcher import match_resume_with_job

from utils.generate_ats_report import generate_ats_report
from utils.generate_job_match_report import generate_job_match_report

from utils.ui.styles import load_css

from utils.ui.components import (
    section_title,
    metric_card,
    skill_badges,
    progress_card,
    score_gauge,
    review_card,
)


def show_ats_page():

    # =====================================================
    # LOAD CSS
    # =====================================================

    load_css()

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "ats_result" not in st.session_state:
        st.session_state.ats_result = None

    if "resume_text" not in st.session_state:
        st.session_state.resume_text = ""

    if "job_match_result" not in st.session_state:
        st.session_state.job_match_result = None

    if "ats_report_filename" not in st.session_state:
        st.session_state.ats_report_filename = None

    if "job_match_report_filename" not in st.session_state:
        st.session_state.job_match_report_filename = None

    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title("📄 ATS Resume Analyzer")

    st.write(
        """
        Upload your resume and receive a professional
        ATS compatibility report with AI-powered
        recommendations.
        """
    )

    st.divider()

    # =====================================================
    # RESUME UPLOAD
    # =====================================================

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file is None:

        st.info(
            "Upload your resume to begin analysis."
        )

        return

    # =====================================================
    # ANALYZE RESUME
    # =====================================================

    if st.button(
        "Analyze Resume",
        use_container_width=True
    ):

        with st.spinner(
            "Analyzing Resume..."
        ):

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

            if not resume_text.strip():

                st.error(
                    "Unable to extract text from PDF."
                )

                return

            st.session_state.resume_text = resume_text

            st.session_state.ats_result = analyze_resume(
                resume_text
            )

            # Reset Job Match Results
            st.session_state.job_match_result = None
            st.session_state.job_match_report_filename = None

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            st.session_state.ats_report_filename = (
                f"ats_report_{timestamp}.pdf"
            )

    # =====================================================
    # STOP IF ATS NOT GENERATED
    # =====================================================

    if st.session_state.ats_result is None:

        return

    result = st.session_state.ats_result

    score = result["ats_score"]

    summary = result["ats_summary"]

    breakdown = result["breakdown"]

    detected = result["detected_skills"]

    categorized = result["categorized_skills"]

    missing = result["missing_skills"]

    review = result["ai_review"]

    st.success(
        "✅ ATS Analysis Completed Successfully!"
    )
        # =====================================================
    # ATS DASHBOARD
    # =====================================================

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        section_title("📊 ATS Score")
        score_gauge(
    score,
    "ATS Compatibility"
)

    with right:
        section_title("📈 Resume Summary")

        metric_card(
            "ATS Score",
            f"{score}/100"
        )

        metric_card(
            "Resume Length",
            summary["resume_length"]
        )

        metric_card(
            "Skills Found",
            summary["total_detected"]
        )

        metric_card(
            "Missing Skills",
            summary["total_missing"]
        )

    # =====================================================
    # CATEGORY BREAKDOWN
    # =====================================================

    st.divider()

    section_title("📂 Category Breakdown")

    for category, value in breakdown.items():
        progress_card(
            category,
            value
        )

    # =====================================================
    # DETECTED & MISSING SKILLS
    # =====================================================

    st.divider()

    left, right = st.columns(2)

    with left:
        section_title("✅ Detected Skills")
        skill_badges(detected)

    with right:
        section_title("❌ Missing Skills")
        skill_badges(missing)

    # =====================================================
    # SKILLS BY CATEGORY
    # =====================================================

    st.divider()

    section_title("📚 Skills by Category")

    if categorized:
        for category, skills in categorized.items():
            with st.expander(category):
                if skills:
                    skill_badges(skills)
                else:
                    st.info("No skills detected.")
    else:
        st.info("No categorized skills available.")
            # =====================================================
    # AI REVIEW
    # =====================================================

    st.divider()

    section_title("🤖 AI Resume Review")

    review_card(
        "Strengths",
        review.get("strengths", []),
        "💪"
    )

    review_card(
        "Weaknesses",
        review.get("weaknesses", []),
        "⚠️"
    )

    review_card(
        "Suggestions",
        review.get("suggestions", []),
        "💡"
    )

    review_card(
        "Career Recommendations",
        review.get("career_recommendations", []),
        "🚀"
    )

    # =====================================================
    # DOWNLOAD ATS REPORT
    # =====================================================

    st.divider()

    section_title("📄 Download ATS Report")

    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    report_path = os.path.join(
        reports_dir,
        st.session_state.ats_report_filename
    )

    if not os.path.exists(report_path):
        generate_ats_report(
            result,
            report_path
        )

    with open(report_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    st.download_button(
        label="⬇ Download ATS Report",
        data=pdf_bytes,
        file_name=st.session_state.ats_report_filename,
        mime="application/pdf",
        use_container_width=True
    )

    st.success(
        "✅ ATS Report Ready for Download"
    )
        # =====================================================
    # JOB DESCRIPTION MATCHING
    # =====================================================

    st.divider()

    section_title("💼 Job Description Matching")

    st.write(
        """
        Paste the Job Description below to compare it
        with your resume and receive an AI-powered
        job match analysis.
        """
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=220,
        placeholder="""
Example:

We are looking for a Python Developer with experience
in Machine Learning, SQL, Docker, AWS, Git,
REST APIs and Linux.
"""
    )

    if st.button(
        "🔍 Analyze Job Match",
        use_container_width=True
    ):

        if not job_description.strip():

            st.warning(
                "Please paste a Job Description."
            )

        else:

            with st.spinner(
                "Analyzing Job Match..."
            ):

                st.session_state.job_match_result = (
                    match_resume_with_job(
                        st.session_state.resume_text,
                        job_description
                    )
                )

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                st.session_state.job_match_report_filename = (
                    f"job_match_report_{timestamp}.pdf"
                )

    # =====================================================
    # STOP IF JOB MATCH NOT GENERATED
    # =====================================================

    if st.session_state.job_match_result is None:
        return

    job_match = st.session_state.job_match_result

    match_score = job_match["match_score"]
    matched_skills = job_match["matched_skills"]
    missing_skills = job_match["missing_skills"]
    resume_skills = job_match["resume_skills"]
    jd_skills = job_match["jd_skills"]
    gemini_analysis = job_match["gemini_analysis"]

    st.success(
        "✅ Job Match Analysis Completed Successfully!"
    )
        # =====================================================
    # JOB MATCH DASHBOARD
    # =====================================================

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        section_title("🎯 Job Match Score")
        score_gauge(
        match_score,
        "Job Match Score"
    )
        

    with right:
        section_title("📈 Match Summary")

        metric_card(
            "Match Score",
            f"{match_score}%"
        )

        metric_card(
            "Resume Skills",
            len(resume_skills)
        )

        metric_card(
            "Job Skills",
            len(jd_skills)
        )

        metric_card(
            "Matched Skills",
            len(matched_skills)
        )

    # =====================================================
    # SKILL COMPARISON
    # =====================================================

    st.divider()

    left, right = st.columns(2)

    with left:
        section_title("📄 Resume Skills")
        skill_badges(resume_skills)

    with right:
        section_title("💼 Job Description Skills")
        skill_badges(jd_skills)

    # =====================================================
    # MATCHED / MISSING SKILLS
    # =====================================================

    st.divider()

    left, right = st.columns(2)

    with left:
        section_title("✅ Matched Skills")
        skill_badges(matched_skills)

    with right:
        section_title("❌ Missing Skills")
        skill_badges(missing_skills)

    # =====================================================
    # AI JOB MATCH ANALYSIS
    # =====================================================

    st.divider()

    section_title("🤖 AI Job Match Analysis")

    st.info(
        gemini_analysis.get(
            "overall_feedback",
            "No feedback available."
        )
    )

    review_card(
        "Strengths",
        gemini_analysis.get(
            "strengths",
            []
        ),
        "💪"
    )

    review_card(
        "Missing Skill Analysis",
        gemini_analysis.get(
            "missing_skill_analysis",
            []
        ),
        "⚠️"
    )

    review_card(
        "Resume Improvements",
        gemini_analysis.get(
            "resume_improvements",
            []
        ),
        "💡"
    )

    st.subheader(
        "📌 Application Recommendation"
    )

    recommendation = gemini_analysis.get(
        "application_recommendation",
        "Recommendation unavailable."
    )

    if "apply" in recommendation.lower():
        st.success(recommendation)
    else:
        st.warning(recommendation)
    # =====================================================
    # DOWNLOAD JOB MATCH REPORT
    # =====================================================

    st.divider()

    section_title("📄 Download Job Match Report")

    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    report_path = os.path.join(
        reports_dir,
        st.session_state.job_match_report_filename
    )

    if not os.path.exists(report_path):
        generate_job_match_report(
            job_match,
            report_path
        )

    with open(report_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    st.download_button(
        label="⬇ Download Job Match Report",
        data=pdf_bytes,
        file_name=st.session_state.job_match_report_filename,
        mime="application/pdf",
        use_container_width=True
    )

    st.success(
        "✅ Job Matching Report Ready for Download"
    )

    # =====================================================
    # PAGE COMPLETED
    # =====================================================

    st.divider()

    st.success(
        """
🎉 ATS Analysis and Job Description Matching completed successfully.

You can now:

• Download the ATS Report
• Download the Job Match Report
• Upload another resume to perform a new analysis
        """
    )
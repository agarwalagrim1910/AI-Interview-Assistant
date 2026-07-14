import streamlit as st
from utils.ats.ats_analyzer import analyze_resume
from app_pages.ats import show_ats_page

from database.db import (
    create_tables,
    save_interview,
    get_interviews
)
from utils.pdf_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills

from utils.gemini_service import (
    generate_question,
    evaluate_answer
)

from utils.generate_report import (
    generate_pdf_report
)

from utils.rag.rag_pipeline import (
    RAGPipeline
)
from interview.manager import InterviewManager


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(

    page_title="AI Interview Assistant",

    page_icon="🤖",

    layout="wide"

)


st.title("🤖 AI Interview Assistant")


# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------

page = st.sidebar.radio(

    "Navigation",

    [

        "Interview",

        "ATS Analyzer",

        "History"

    ]

)

if page == "ATS Analyzer":

    show_ats_page()

    st.stop()


TOTAL_QUESTIONS = 5
# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------

def initialize_session():

    defaults = {
        
        "saved_to_db": False,

        "question_number": 1,

        "current_difficulty": "Easy",

        "interview_manager": InterviewManager(),

        "scores": [],

        "evaluated": False,

        "current_result": None,

        "skills": [],

        "resume_text": "",

        "question": "",

        # -----------------------------
        # RAG
        # -----------------------------

        "rag_pipeline": None

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


initialize_session()
create_tables()



# --------------------------------------------------
# Interview History Page
# --------------------------------------------------

if page == "History":

    st.title(
        "📜 Interview History"
    )

    history = get_interviews()


    if not history:

        st.info(
            "No interviews found yet."
        )


    for item in history:

        (
            interview_id,
            date,
            skills,
            questions,
            answers,
            scores,
            feedbacks,
            average_score,
            verdict

        ) = item


        st.subheader(
            f"Interview #{interview_id}"
        )


        st.write(
            f"📅 Date: {date}"
        )


        st.write(
            f"⭐ Score: {average_score}/10"
        )


        st.write(
            f"🏆 Verdict: {verdict}"
        )


        with st.expander(
            "View Details"
        ):

            import json


            questions = json.loads(
                questions
            )

            answers = json.loads(
                answers
            )

            scores = json.loads(
                scores
            )

            feedbacks = json.loads(
                feedbacks
            )


            for i in range(
                len(questions)
            ):

                st.write(
                    f"### Question {i+1}"
                )

                st.write(
                    questions[i]
                )

                st.write(
                    "**Answer:**"
                )

                st.write(
                    answers[i]
                )

                st.write(
                    f"Score: {scores[i]}/10"
                )

                st.write(
                    feedbacks[i]
                )


    st.stop()
# --------------------------------------------------
# Session Safety Check
# --------------------------------------------------

required_states = {

    "questions": [],

    "answers": [],

    "scores": [],

    "feedbacks": [],

    "evaluated": False,

    "current_result": None,

    "question": "",

    "current_difficulty": "Easy",

    "interview_manager": InterviewManager()

}

for key, value in required_states.items():

    if key not in st.session_state:

        st.session_state[key] = value


# --------------------------------------------------
# Reset Interview
# --------------------------------------------------

def reset_interview():

    keys = [
        
        "saved_to_db",

        "question_number",

        "current_difficulty",

        "interview_manager",

        "scores",

        "answers",

        "feedbacks",

        "questions",

        "evaluated",

        "current_result",

        "skills",

        "resume_text",

        "question",

        "rag_pipeline"

    ]

    for key in keys:

        if key in st.session_state:

            del st.session_state[key]

    initialize_session()


# --------------------------------------------------
# Difficulty Logic
# --------------------------------------------------

def get_difficulty(question_number):

    if question_number <= 2:

        return "Easy"

    elif question_number <= 4:

        return "Medium"

    return "Hard"


# --------------------------------------------------
# Build Retrieval Query
# --------------------------------------------------

def build_retrieval_query(
    difficulty
):

    if difficulty == "Easy":

        return (
            "Retrieve the candidate's projects, "
            "core technologies and fundamental concepts."
        )

    elif difficulty == "Medium":

        return (
            "Retrieve implementation details, "
            "design decisions, technical challenges "
            "and comparisons from the candidate's resume."
        )

    return (

        "Retrieve architecture, scalability, "
        "optimization, deployment and production "
        "engineering details from the candidate's resume."

    )


# --------------------------------------------------
# Resume Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(

    "Upload your Resume",

    type=["pdf"]

)

if uploaded_file is None:

    st.info(

        "Please upload your resume to begin the interview."

    )

    st.stop()
# --------------------------------------------------
# Parse Resume + Build RAG Pipeline
# --------------------------------------------------

if not st.session_state.resume_text:

    with st.spinner("Parsing Resume..."):

        # -----------------------------
        # Extract Resume Text
        # -----------------------------

        resume_text = extract_text_from_pdf(
            uploaded_file
        )

        st.session_state.resume_text = resume_text

        # -----------------------------
        # ATS Analysis
        # -----------------------------

        ats_result = analyze_resume(
            resume_text
        )

        st.session_state.ats_result = ats_result

        # -----------------------------
        # Extract Skills
        # -----------------------------

        st.session_state.skills = extract_skills(
            resume_text
        )

        # -----------------------------
        # Build RAG Pipeline
        # -----------------------------

        try:

            rag_pipeline = RAGPipeline()

            with st.spinner(
                "Building Resume Knowledge Base..."
            ):

                rag_pipeline.build(
                    resume_text
                )

            st.session_state.rag_pipeline = (
                rag_pipeline
            )

        except Exception as e:

            st.error(
                f"Failed to build Resume Knowledge Base:\n{e}"
            )

            st.stop()

# --------------------------------------------------
# Get Session Objects
# --------------------------------------------------

skills = st.session_state.skills
# --------------------------------------------------
# ATS Resume Analysis
# --------------------------------------------------

if "ats_result" in st.session_state:

    ats = st.session_state.ats_result

    st.divider()

    st.subheader("📄 ATS Resume Analysis")

    # -----------------------------------------
    # ATS Score
    # -----------------------------------------

    st.metric(

        label="⭐ ATS Score",

        value=f"{ats['ats_score']}/100"

    )

    st.progress(

        ats["ats_score"] / 100

    )

    # -----------------------------------------
    # Score Breakdown
    # -----------------------------------------

    st.subheader("📊 Score Breakdown")

    for category, score in ats["breakdown"].items():

        st.write(f"**{category}:** {score}")

    # -----------------------------------------
    # Detected Skills
    # -----------------------------------------

    st.subheader("✅ Detected Skills")

    if ats["detected_skills"]:

        st.write(", ".join(ats["detected_skills"]))

    else:

        st.warning("No technical skills detected.")

    # -----------------------------------------
    # Missing Skills
    # -----------------------------------------

    st.subheader("⚠️ Recommended Skills")

    if ats["missing_skills"]:

        st.write(", ".join(ats["missing_skills"][:15]))

    else:

        st.success("Excellent skill coverage!")

rag_pipeline = st.session_state.rag_pipeline

# --------------------------------------------------
# Resume Parsed Successfully
# --------------------------------------------------

st.success(
    "✅ Resume Parsed Successfully!"
)

st.subheader(
    "🛠 Detected Skills"
)

if skills:

    cols = st.columns(3)

    for index, skill in enumerate(skills):

        with cols[index % 3]:

            st.success(skill)

else:

    st.warning(
        "No predefined skills were detected."
    )


# --------------------------------------------------
# Current Question
# --------------------------------------------------

difficulty = st.session_state.current_difficulty

st.divider()

st.subheader(
    f"📝 Question "
    f"{st.session_state.question_number}"
    f"/{TOTAL_QUESTIONS}"
)

st.caption(
    f"Difficulty : **{difficulty}**"
)



# --------------------------------------------------
# Generate Interview Question
# --------------------------------------------------

if not st.session_state.question:

    retrieval_query = build_retrieval_query(
        difficulty
    )

    retrieved_context = (
    rag_pipeline.retrieve_context_as_text(
        retrieval_query,
        top_k=5
    )
)

    if not retrieved_context.strip():

        retrieved_context = (
            "No relevant resume context found."
        )

    # Safe skills string
    skills_string = ", ".join(skills)

    if skills_string.strip() == "":

        skills_string = "General Programming"

    with st.spinner(
        "Generating AI Interview Question..."
    ):

        st.session_state.question = generate_question(

    skills=skills_string,

    difficulty=difficulty,

    retrieved_context=retrieved_context,

    previous_questions=st.session_state.get(
        "questions",
        []
    ),

    performance_context=(
        st.session_state.interview_manager
        .get_performance_context()
    )

)

question = st.session_state.question

st.info(question)

# --------------------------------------------------
# Candidate Answer
# --------------------------------------------------

user_answer = st.text_area(

    "Write your answer here",

    height=220,

    key=f"answer_{st.session_state.question_number}"

)
# --------------------------------------------------
# Evaluate Answer
# --------------------------------------------------

if not st.session_state.evaluated:

    if st.button(
        "✅ Evaluate Answer",
        use_container_width=True
    ):

        if user_answer.strip():

            with st.spinner(
                "Evaluating your answer..."
            ):

                result = evaluate_answer(

                    question,

                    user_answer

                )

            score = result.get(
                "score",
                0
            )
            
            st.session_state.interview_manager.analyze_performance(
             score,
             question
            )
            st.session_state.current_difficulty = (
    st.session_state.interview_manager.decide_difficulty(
        st.session_state.current_difficulty,
        score
    )
)


            feedback = result.get(
                "feedback",
                ""
            )

            verdict = result.get(
                "verdict",
                "Unknown"
            )

            # --------------------------------------
            # Store Interview Data
            # --------------------------------------

            st.session_state.questions.append(
                question
            )

            st.session_state.answers.append(
                user_answer
            )

            st.session_state.scores.append(
                score
            )

            st.session_state.feedbacks.append(
                feedback
            )

            st.session_state.current_result = (
                result
            )

            st.session_state.evaluated = True

            st.rerun()

        else:

            st.warning(
                "Please write your answer before evaluation."
            )


# --------------------------------------------------
# Show Evaluation Result
# --------------------------------------------------

if st.session_state.evaluated:

    result = st.session_state.current_result

    score = result["score"]

    feedback = result["feedback"]

    verdict = result["verdict"]

    st.divider()

    st.subheader(
        "📊 Evaluation"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Score",

            f"{score}/10"

        )

        st.progress(
            score / 10
        )

    with col2:

        if verdict == "Pass":

            st.success(
                "✅ Pass"
            )

        elif verdict == "Fail":

            st.error(
                "❌ Fail"
            )

        else:

            st.warning(
                verdict
            )

    st.write(
        "### 💬 Feedback"
    )

    st.write(
        feedback
    )


# --------------------------------------------------
# Next Question
# --------------------------------------------------

    if (
        st.session_state.question_number
        < TOTAL_QUESTIONS
    ):

        if st.button(

            "➡ Next Question",

            use_container_width=True

        ):

            st.session_state.question_number += 1

            st.session_state.question = ""

            st.session_state.current_result = None

            st.session_state.evaluated = False

            st.rerun()

    else:

        if st.button(

            "🏁 Finish Interview",

            use_container_width=True

        ):

            st.session_state.question_number += 1

            st.rerun()
# --------------------------------------------------
# Final Interview Report
# --------------------------------------------------

if st.session_state.question_number > TOTAL_QUESTIONS:

    st.balloons()

    st.header("🎉 Interview Completed")


    average_score = (
        sum(st.session_state.scores)
        / len(st.session_state.scores)
    )


    # --------------------------------------------------
    # Save Interview History
    # --------------------------------------------------

    if not st.session_state.saved_to_db:

        if average_score >= 8:

            final_verdict = "Excellent"

        elif average_score >= 6:

            final_verdict = "Good"

        elif average_score >= 4:

            final_verdict = "Average"

        else:

            final_verdict = "Needs Improvement"


        save_interview(

            skills=st.session_state.skills,

            questions=st.session_state.questions,

            answers=st.session_state.answers,

            scores=st.session_state.scores,

            feedbacks=st.session_state.feedbacks,

            average_score=average_score,

            verdict=final_verdict

        )


        st.session_state.saved_to_db = True


    st.metric(

        label="Average Score",

        value=f"{average_score:.2f}/10"

    )

    st.progress(

        min(

            average_score / 10,

            1.0

        )

    )

    st.divider()

    st.subheader(

        "📋 Interview Summary"

    )

    for i in range(

        len(st.session_state.questions)

    ):

        with st.expander(

            f"Question {i+1}"

        ):

            st.write(

                f"**Question:** {st.session_state.questions[i]}"

            )

            st.write(

                f"**Your Answer:** {st.session_state.answers[i]}"

            )

            st.write(

                f"**Score:** {st.session_state.scores[i]}/10"

            )

            st.write(

                f"**Feedback:** {st.session_state.feedbacks[i]}"

            )

    st.divider()

    st.subheader(

        "🏆 Final Verdict"

    )

    if average_score >= 8:

        st.success(

            "🌟 Excellent Performance! You are interview ready."

        )

    elif average_score >= 6:

        st.success(

            "✅ Good Performance! Improve some technical depth."

        )

    elif average_score >= 4:

        st.warning(

            "📚 Average Performance. Revise weak areas and practice more."

        )

    else:

        st.error(

           "❌ Needs Improvement. Focus on fundamentals first."

        )


    # --------------------------------------------------
    # Generate PDF Report
    # --------------------------------------------------

    pdf = generate_pdf_report(

        skills=st.session_state.skills,

        questions=st.session_state.questions,

        answers=st.session_state.answers,

        scores=st.session_state.scores,

        feedbacks=st.session_state.feedbacks

    )

    st.download_button(

        label="📥 Download Interview Report",

        data=pdf,

        file_name="AI_Interview_Report.pdf",

        mime="application/pdf",

        use_container_width=True

    )

    st.divider()

    if st.button(

        "🔄 Start New Interview",

        use_container_width=True

    ):

        reset_interview()

        st.rerun()
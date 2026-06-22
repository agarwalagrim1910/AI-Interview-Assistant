import streamlit as st

from utils.pdf_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.gemini_service import (
    generate_question,
    evaluate_answer
)

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Interview Assistant")

TOTAL_QUESTIONS = 5


# ---------------------------
# Session State Initialization
# ---------------------------

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "scores" not in st.session_state:
    st.session_state.scores = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = []

if "questions" not in st.session_state:
    st.session_state.questions = []

if "evaluated" not in st.session_state:
    st.session_state.evaluated = False

if "current_result" not in st.session_state:
    st.session_state.current_result = None


# ---------------------------
# Difficulty Logic
# ---------------------------

def get_difficulty(question_no):

    if question_no <= 2:
        return "Easy"

    elif question_no <= 4:
        return "Medium"

    else:
        return "Hard"


# ---------------------------
# Resume Upload
# ---------------------------

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    text = extract_text_from_pdf(uploaded_file)

    st.success("✅ Resume Parsed Successfully!")

    skills = extract_skills(text)

    st.subheader("🛠 Detected Skills")

    for skill in skills:
        st.write("✅", skill)

    # ---------------------------
    # Final Report
    # ---------------------------

    if st.session_state.question_number > TOTAL_QUESTIONS:

        st.header("🎉 Interview Completed")

        avg_score = (
            sum(st.session_state.scores)
            / len(st.session_state.scores)
        )

        st.metric(
            "Average Score",
            f"{avg_score:.2f}/10"
        )

        st.subheader("📋 Question-wise Scores")

        for i, score in enumerate(
            st.session_state.scores,
            start=1
        ):
            st.write(
                f"Question {i}: {score}/10"
            )

        st.subheader("🏆 Final Verdict")

        if avg_score >= 7:
            st.success(
                "🚀 Interview Ready"
            )
        else:
            st.warning(
                "📚 More Practice Needed"
            )

        if st.button("Start New Interview"):

            st.session_state.question_number = 1
            st.session_state.scores = []
            st.session_state.answers = []
            st.session_state.feedbacks = []
            st.session_state.questions = []
            st.session_state.evaluated = False
            st.session_state.current_result = None

            st.rerun()

        st.stop()

    # ---------------------------
    # Current Question
    # ---------------------------

    difficulty = get_difficulty(
        st.session_state.question_number
    )

    st.subheader(
        f"Question {st.session_state.question_number}/{TOTAL_QUESTIONS}"
    )

    st.write(
        f"**Difficulty:** {difficulty}"
    )

    question_key = (
        f"question_{st.session_state.question_number}"
    )

    if question_key not in st.session_state:

        with st.spinner(
            "Generating Question..."
        ):

            st.session_state[question_key] = (
                generate_question(
                    ", ".join(skills),
                    difficulty
                )
            )

    question = st.session_state[question_key]

    st.info(question)

    # ---------------------------
    # Answer Input
    # ---------------------------

    user_answer = st.text_area(
        "Write your answer here",
        height=200,
        key=f"answer_{st.session_state.question_number}"
    )

    # ---------------------------
    # Evaluate Button
    # ---------------------------

    if not st.session_state.evaluated:

        if st.button("Evaluate Answer"):

            if user_answer.strip():

                with st.spinner(
                    "Evaluating Answer..."
                ):

                    result = evaluate_answer(
                        question,
                        user_answer
                    )

                score = result.get(
                    "score",
                    0
                )

                feedback = result.get(
                    "feedback",
                    ""
                )

                verdict = result.get(
                    "verdict",
                    "Unknown"
                )

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

                st.session_state.current_result = {
                    "score": score,
                    "feedback": feedback,
                    "verdict": verdict
                }

                st.session_state.evaluated = True

                st.rerun()

            else:

                st.warning(
                    "Please enter an answer first."
                )

    # ---------------------------
    # Show Result
    # ---------------------------

    if st.session_state.evaluated:

        result = st.session_state.current_result

        score = result["score"]
        feedback = result["feedback"]
        verdict = result["verdict"]

        st.subheader("📊 AI Feedback")

        st.metric(
            "Score",
            f"{score}/10"
        )

        st.progress(score / 10)

        st.write("### Feedback")

        st.write(feedback)

        if verdict == "Pass":
            st.success("✅ Pass")
        else:
            st.error("❌ Fail")

        if st.button("➡ Next Question"):

            st.session_state.question_number += 1
            st.session_state.evaluated = False
            st.session_state.current_result = None

            st.rerun()

    # ---------------------------
    # Resume Content
    # ---------------------------

    with st.expander("📄 Resume Content"):

        st.text(text)
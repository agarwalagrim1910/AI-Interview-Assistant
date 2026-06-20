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

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    # Resume Parsing
    text = extract_text_from_pdf(uploaded_file)

    st.success("✅ Resume Parsed Successfully!")

    # Skill Extraction
    st.subheader("🛠 Detected Skills")

    skills = extract_skills(text)

    for skill in skills:
        st.write("✅", skill)

    # Difficulty Selection
    st.subheader("🎚 Select Difficulty")

    difficulty = st.selectbox(
        "Choose Question Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    # Generate Question Once
    if (
        "question" not in st.session_state
        or st.session_state.get("difficulty") != difficulty
    ):

        st.session_state.question = generate_question(
            ", ".join(skills),
            difficulty
        )

        st.session_state.difficulty = difficulty

    # Interview Question
    st.subheader("🎯 Interview Question")

    st.info(st.session_state.question)

    # Candidate Answer
    st.subheader("✍ Your Answer")

    user_answer = st.text_area(
        "Write your answer here",
        height=200
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Evaluate Answer"):

            if user_answer.strip():

                feedback = evaluate_answer(
                    st.session_state.question,
                    user_answer
                )

                st.subheader("📊 AI Feedback")

                st.write(feedback)

            else:

                st.warning(
                    "Please enter an answer first."
                )

    with col2:

        if st.button("🔄 Generate New Question"):

            st.session_state.question = generate_question(
                ", ".join(skills),
                difficulty
            )

            st.rerun()

    # Resume Content
    with st.expander("📄 Resume Content"):

        st.text(text)
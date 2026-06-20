import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.gemini_service import generate_questions

st.title("AI Interview Assistant")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)

if uploaded_file is not None:

    text = extract_text_from_pdf(uploaded_file)

    st.success("Resume Parsed Successfully!")

    # Skills Section
    st.subheader("Detected Skills")

    skills = extract_skills(text)

    for skill in skills:
        st.write("✅", skill)

    # Gemini Questions Section
    st.subheader("AI Generated Interview Questions")

    questions = generate_questions(skills)

    st.write(questions)

    # Resume Content
    st.subheader("Resume Content")

    st.text(text)